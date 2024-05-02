from langchain_experimental.agents.agent_toolkits import create_python_agent
from langchain.agents import load_tools, initialize_agent
from langchain.agents import AgentType
from langchain_experimental.tools.python.tool import PythonREPLTool
from langchain.python import PythonREPL
from langchain_openai.chat_models import ChatOpenAI
import langchain

from langchain.tools import tool 
from datetime import date

llm_model = "gpt-4"

llm = ChatOpenAI(temperature = 0, model = llm_model)

tools = load_tools(["llm-math", "wikipedia"], llm = llm)

agent1 = initialize_agent(
    tools,
    llm,
    agent = AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    handle_parsing_errors = True,
    verbose = True
)

langchain.debug = True

print(agent1("If 12 men take 10 days to perform a work, by what date will the work get finished if I start the work today, April 26th,  with 5 men? Tell me the exact date and day."))

agent2 = create_python_agent(
    llm,
    tool = PythonREPLTool(),
    verbose = True
)

customer_list = [["Harrison", "Chase"], 
                 ["Lang", "Chain"],
                 ["Dolly", "Too"],
                 ["Elle", "Elem"], 
                 ["Geoff","Fusion"], 
                 ["Trance","Former"],
                 ["Jen","Ayai"]
                ]

# print(agent2.run(f"""Sort these customers by \
# last name and then first name \
# and print the output: {customer_list}"""))

@tool
def time(text: str) -> str:
    """Returns todays date, use this for any \
    questions related to knowing todays date. \
    The input should always be an empty string, \
    and this functino will always return todays \
    date - any date mathematics should occur \
    outside this function."""
    return str(date.today())

agent3 = initialize_agent(
    tools + [time],
    llm,
    agent = AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    handle_parsing_erros = True,
    verbose = True 
)

# print(agent3("What is today's date?"))