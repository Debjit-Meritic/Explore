from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain.agents.format_scratchpad.openai_tools import format_to_openai_tool_messages
import json

from langchain.globals import set_debug, set_verbose
set_debug(True)
set_verbose(True)

# import os
# from dotenv import load_dotenv, find_dotenv
# load_dotenv(find_dotenv())

# OpenAI.api_key = os.environ["OPENAI_API_KEY"]

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant. Make sure to use the tools available to you for responding.",
        ),
        # ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

@tool
def exponentiate(x: float, y: float) -> float:
    """Raise 'x' to the 'y'."""
    return str(x**y)
    
tools = [exponentiate]

llm = ChatOpenAI(model = "gpt-4", temperature=0)
llm_with_tools = llm.bind_tools(tools)
# print(llm.invoke([
# 	("system", "You're a helpful assistant"), 
# 	("human", "what's 5 raised to the 2.743"),
# ]))

# agent = create_tool_calling_agent(llm, tools, prompt)
def format_and_print(x):
    print("########################")
    print(x)
    print("########################")
    return format_to_openai_tool_messages(x["intermediate_steps"])
agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_to_openai_tool_messages(x["intermediate_steps"]),
        "test": lambda x: print(x)
    }
    | prompt 
    | llm_with_tools
    | OpenAIToolsAgentOutputParser()
)
agent_executor = AgentExecutor(agent = agent, tools = tools)
agent_executor.invoke({"input": "how much is 2.5 raised to 2.5?"})


# runnable = (
#     {"equation_statement": RunnablePassthrough()} | prompt | llm | StrOutputParser()
# )
# print(json.dumps(agent.input_schema.schema(), indent = 4))
# print(prompt.partial_variables)

