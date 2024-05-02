from openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain.globals import set_debug
set_debug = True

import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

OpenAI.api_key = os.environ["OPENAI_API_KEY"]

# Tools #############################################
from typing import List
from pydantic import BaseModel, Field
from langchain.tools import tool
import json

class AnalysisInput(BaseModel):
    metric: str = Field(description = "Name of the factual column on which the analysis is to be conducted")
    time_constraint: str = Field(description = "Name of the temporal column to be used for temporal filtering")
    time_constraint_bucketing: str = Field(description = "Type of bucketing to be used on temporal column")
    time_constraint_start: List[str] = Field(description = "List containing the start of the time period for temporal filtering where the first element denotes month and the second element denotes year")
    time_constraint_end: List[str] = Field(description = "List containing the end of the time period for temporal filtering where the first element denotes month and the second element denotes year")
    attribute_constraint: List[str] = Field(description = "List of dimensional columns to be used for filtering while performing analysis")
    attribute_constraint_value: List[str] = Field(description = "List of values corresponding to each element in the list of attributes to be used for filtering")
    
@tool(args_schema = AnalysisInput)
def create_analysis(
    
    metric: str,
    time_constraint: str,
    time_constraint_bucketing: str,
    time_constraint_start: List[str],
    time_constraint_end: List[str],
    attribute_constraint: List[str],
    attribute_constraint_value: List[str]
) -> str:
    """Created and return a json containing the information required for performing analysis"""
    info = {
        'metric': metric,
        'time_constraint': time_constraint,
        'time_constraint_bucketing': time_constraint_bucketing,
        'time_constraint_start': time_constraint_start,
        'time_constraint_end': time_constraint_end,
        'attribute_constraint': attribute_constraint,
        'attribute_constraint_value': attribute_constraint_value
    }
    json_info = json.dumps(info, indent = 4)
    # print(json_info)
    f.write("JSON: " + json_info + "\n")
    return json_info

tools = [create_analysis]

# Prompt #############################################
from langchain.prompts import ChatPromptTemplate
from langchain.prompts import MessagesPlaceholder
from datetime import date

system_prompt_template = """\
Your job is to extract relevent information for querying a database with multiple factual and dimensional or attribute columns.\
Figure out the names of the columns and the values for those columns to be used for querying, and then use the create_analysis to perform the analysis. 

Information about the database is below as a list of names of columns.
database:{db}

REMEMBER: When extracting names of columns from the user_text, ensure that the columns exist in the database.\
Do not assume any value for a field unless you can confidently extract it from the user input.\
If you feel you can't extract all the information required to perform analysis, then ask follow up questions.


Today's date is {date}.
"""

MKG_data =  """\
Attributes: ["Pillar", "Location"]
Time: ["Date"]
Metrics: ["Revenue", "Leads"]
Values for Pillar: ["OE Adult", "OE Jr", "Enterprise", "Open Mundo"]
Values for Location: ["Brazil", "Chile", "Peru", "Mexico"]
"""
system_prompt = system_prompt_template.format(db = MKG_data, date = date.today())
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name = "agent_scratchpad")
    ]
)

# Functions and Model #############################################
from langchain.tools.render import format_tool_to_openai_function
functions = [
    format_tool_to_openai_function(f) for f in tools
]
llm_model = "gpt-3.5-turbo"
model = ChatOpenAI(temperature=0, verbose = True, model = llm_model).bind(functions = functions)

# Output Parser #############################################
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser

# Agent Chain #############################################
from langchain.schema.runnable import RunnablePassthrough
from langchain.agents.format_scratchpad import format_to_openai_functions
agent_chain = RunnablePassthrough.assign(
    agent_scratchpad = lambda x: format_to_openai_functions(x["intermediate_steps"])
) | prompt | model | OpenAIFunctionsAgentOutputParser()

# Memory #####################################################
from langchain.memory import ConversationBufferMemory
memory = ConversationBufferMemory(return_messages=True,memory_key="chat_history")

# Agent Executor #############################################
from langchain.agents import AgentExecutor
import textwrap
agent_executor = AgentExecutor(agent = agent_chain, tools = tools, verbose = True, memory = memory)

f = open("conversation.txt", "w")
while(True):
    user_prompt = input()
    if user_prompt == "q":
        break 
    
    f.write("USER: " + textwrap.fill(user_prompt, 100) + "\n")
    f.write("AGENT: " + textwrap.fill(agent_executor({"input": user_prompt})['output'], 100) + "\n\n")
    f.flush()

f.close()
