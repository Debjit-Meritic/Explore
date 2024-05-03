import json
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.utils.function_calling import convert_to_openai_tool
from langgraph.graph import END, MessageGraph
import os
from typing import List


# Define the multiply function
@tool
def multiply(first_number: int, second_number: int):
    """Multiplies two numbers together."""
    return first_number * second_number


# Create an instance of the OpenAI model
# https://api.python.langchain.com/en/latest/chat_models/langchain_openai.chat_models.base.ChatOpenAI.html#langchain_openai.chat_models.base.ChatOpenAI
model = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4", verbose=True, temperature = 1.0)

# Bind the multiply tool to the OpenAI model
model_with_tools = model.bind(tools=[convert_to_openai_tool(multiply)])

# Create the message graph
graph = MessageGraph()


def invoke_model(state):
    """Invoke the model with the current state."""
    return model_with_tools.invoke(state)


graph.add_node("oracle", invoke_model)


def invoke_tool(state: List[BaseMessage]):
    tool_calls = state[-1].additional_kwargs.get("tool_calls", [])
    multiply_call = None

    for tool_call in tool_calls:
        if tool_call.get("function").get("name") == "multiply":
            multiply_call = tool_call

    if multiply_call is None:
        raise Exception("No adder input found.")

    res = multiply.invoke(
        json.loads(multiply_call.get("function").get("arguments"))
    )

    return ToolMessage(
        tool_call_id=multiply_call.get("id"),
        content=res
    )

graph.add_node("multiply", invoke_tool)
graph.add_edge("multiply", END)
graph.set_entry_point("oracle")

# Define conditional routing
def router(state: List[BaseMessage]):
    print(state[-1].additional_kwargs.get("tool_calls", []))
    tool_calls = state[-1].additional_kwargs.get("tool_calls", [])
    if len(tool_calls):
        return "multiply"
    else:
        return "end"

graph.add_conditional_edges("oracle", router, {
    "multiply": "multiply",
    "end": END,
})

# Compile the graph to make it runnable
runnable = graph.compile()


def process_message(message):
    """Process a message through the LangChain graph."""
    response = runnable.invoke(HumanMessage(message))
    return response