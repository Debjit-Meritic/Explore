from openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain.globals import set_debug, set_verbose
set_debug(True)
set_verbose(True)

import langchain
# langchain.debug = True

import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

OpenAI.api_key = os.environ["OPENAI_API_KEY"]

# Helper Functions ##################################
def filterOperator(op):
    match op:
        case "EQ":
            return 1
        case "NE":
            return 2
        case "GT":
            return 3
        case "GTE":
            return 4
        case "LT":
            return 5
        case "LTE":
            return 6
        case _:
            return 0
        


# Tools #############################################
from typing import List
from pydantic import BaseModel, Field
from langchain.tools import tool
import json
import client

class QueryInput(BaseModel):
    metric: str = Field(description = "Name of the factual column on which the analysis is to be conducted")
    time_constraint: str = Field(description = "Name of the temporal column to be used for temporal filtering")
    time_constraint_bucketing: str = Field(description = "Type of bucketing to be used on temporal column")
    time_constraint_start: List[str] = Field(description = "List containing the start of the time period for temporal filtering where the first element denotes month and the second element denotes year")
    time_constraint_end: List[str] = Field(description = "List containing the end of the time period for temporal filtering where the first element denotes month and the second element denotes year")
    attribute_constraints: List[List[str]] = Field(description = 
                                            "List of list of strings, where every element of the outer list is a constraint \
                                            which is defined by the inner list of three elements - \
                                                1. Attribute Column Name \
                                                2. Filter Operator - Can take the below listed values: \
                                                    EQ - equals, \
                                                    NE - not equals, \
                                                    GT - greater than, \
                                                    GTE - greater than or equal to, \
                                                    LT - less than, \
                                                    LTE - less than or equal to, \
                                                3. Filter value")
    
@tool(args_schema = QueryInput)
def perform_analysis(
    metric: str,
    time_constraint: str,
    time_constraint_bucketing: str,
    time_constraint_start: List[str],
    time_constraint_end: List[str],
    attribute_constraints: List[List[str]]
) -> str:
    """Creates and runs the query and returns a json containing the analysis"""
    
    # print(attribute_constraints)
    # print(attribute_constraints[0])
    # print(attribute_constraints[0][0])
    # print(api.getColumnInfoByName(attribute_constraints[0][0]))

    context = []
    for attr_constr in attribute_constraints:
        filter = {
            "logical_column_header": api.getColumnInfoByName(attr_constr[0]),
            "operator": filterOperator(attr_constr[1]),
            "values": [attr_constr[2]]
        }
        context.append(filter)    

    dateFilter1 = {
        "logical_column_header": api.getColumnInfoByName(time_constraint),
        "operator": 4,
        "values": [time_constraint_start[0] + "/01/" + time_constraint_start[1]],
    }
    context.append(dateFilter1)

    dateFilter2 = {
        "logical_column_header": api.getColumnInfoByName(time_constraint),
        "operator": 4,
        "values": [time_constraint_end[0] + "/31/" + time_constraint_end[1]],
    }
    context.append(dateFilter2)

    generateAnalysisTreeJSON = {
        "metricId": api.getMetricLogicalColHeader()["id"],
        "context": context 
    }

    f.write("GenAnalTree JSON: " + json.dumps(generateAnalysisTreeJSON, indent = 4) + "\n")
    f.write("____________________________________________________________________________________________________\n")

    response = api.generateAnalysisTree(generateAnalysisTreeJSON)
    if response.status_code != 200:
        return "Failure"
    f.write("AnalysisTree JSON: " + response.status_code + "\n")
    f.write("____________________________________________________________________________________________________\n")

    return "Success" 



class MetricInfoInput(BaseModel):
    id: str = Field(description = "ID of the metric on which the query is to be conducted")

@tool(args_schema = MetricInfoInput)
def get_metric_info(
    id: str,
) -> str:
    """Returns information about the metric such as available columns and the unique values in those columns, to evaluate the query asked by user"""
    metricInfo = json.loads(api.getMetricByID(id))
    if len(metricInfo) == 0:
        return json.dumps({"status": "fail"})

    columns = []
    for col in metricInfo["related_attributes"]:
        columns.append(col)

    for col in json.loads(api.getModelByID(metricInfo["owner_id"])):
        columns.append(col)

    for col in columns:
        col["values"] = api.getColumnValues(col["id"], col["type"])

    json_info = json.dumps(columns, indent = 4)
    f.write("Metric Info JSON: " + json_info + "\n")
    f.write("____________________________________________________________________________________________________\n")

    return json_info
     

tools = [perform_analysis, get_metric_info]

# Prompt #############################################
from langchain.prompts import ChatPromptTemplate
from langchain.prompts import MessagesPlaceholder
from datetime import date


system_prompt_template = """\
You are Terimic, the AI assistant for the data analysis platform Meritic. Introduce yourself at the start of the conversation.
Your job is to extract relevent information for querying a database of metrics.\ 
A metric can have multiple factual and dimensional columns associated which can be used for filtering and bucketing.\
Dimensional columns are of 2 types - ATTRIBUTE and TEMPORAL.\
Figure out the metric, names of the columns and the values for those columns to be used for filtering, \
verify whether the values are valid for filtering and then use the tools available to perform the query. 


Metrics present in the database are mentioned below.
database:{db}

REMEMBER: 
1. When extracting names of columns from the user_text, ensure that the columns exist in the database, \
and ensure that the value used to filter by that column also exists in the database.
2. If the value doesn't exist in the database then inform this to the user and abort the query.
3. For temporal columns, the values are in the form of a list, where the first element denotes the month and the second element denotes the year. \
If the user asks for time periods outside the what the database contains then inform the user about the lack of data.
4. Do not assume any value for a field unless you can confidently extract it from the user input.
5. When handling dates, keep in mind that quarter refers to financial quarters of the year.
6. If you feel you can't extract all the information required to perform analysis, then ask follow up questions.
7. Before using a tool, check chat_history in case you already have the required information.


Today's date is {date}.
"""

api = client.NewtonClient()
input_db = api.listMetric()
input_db = input_db.replace('{', '{{')
input_db = input_db.replace('}', '}}')
system_prompt = system_prompt_template.format(db = input_db, date = date.today())
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
llm_model = "gpt-4"
llm = ChatOpenAI(temperature=0, model = llm_model).bind(functions = functions) # verbose

# Output Parser #############################################
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser

# Agent Chain #############################################
from langchain.schema.runnable import RunnablePassthrough
from langchain.agents.format_scratchpad import format_to_openai_functions
agent_chain = RunnablePassthrough.assign(
    agent_scratchpad = lambda x: format_to_openai_functions(x["intermediate_steps"])
) | prompt | llm | OpenAIFunctionsAgentOutputParser()

# Memory #####################################################
from langchain.memory import ConversationBufferMemory
memory = ConversationBufferMemory(return_messages = True, memory_key = "chat_history")

# Agent Executor #############################################
from langchain.agents import AgentExecutor
import textwrap
agent_executor = AgentExecutor(agent = agent_chain, tools = tools, memory = memory, return_intermediate_steps = True, verbose = True) # verbose
# agent_executor.verbose = True                                                     # verbose 

# Testing ####################################################
# from langchain.callbacks import FileCallbackHandler, StdOutCallbackHandler
# from loguru import logger

# f = open("conversation.txt", "w")

# logfile = "output.log"
# logger.add(logfile, colorize = True, enqueue = True)
# handler = FileCallbackHandler(logfile)

# input = "Hi"

# output = agent_executor.invoke({"input": input})
# # logger.info(output)
# json_output = {
#     "output": output["output"],
#     "input": output["input"]
# }
# print(json.dumps(json_output, indent = 4))

# print(json.dumps(agent_chain.output_schema.schema(), indent = 4))

# f.close()

# Conversation #########################################################################################################
f = open("conversation.txt", "w")
while(True):
    user_prompt = input()
    if user_prompt == "q":
        break 
    
    f.write("USER:\n" + textwrap.fill(user_prompt, 100) + "\n")
    f.write("____________________________________________________________________________________________________\n")

    raw_output = agent_executor({"input": user_prompt})

    printIntermediateSteps = False
    printChatHistory = False

    if raw_output.__contains__('intermediate_steps'):
        printIntermediateSteps = True
        intermediate_steps = raw_output['intermediate_steps']

    if raw_output.__contains__('chat_history'):
        printChatHistory = True
        history = raw_output['chat_history']

    agent_output = raw_output['output']
    
    if printIntermediateSteps:
        f.write("INTERMEDIATE STEPS:\n")
        for line in intermediate_steps:
            f.write(str(line) + "\n")
        f.write("____________________________________________________________________________________________________\n")
    
    if printChatHistory:
        f.write("HISTORY:\n")
        for line in history:
            f.write('\n'.join(['\n'.join(
                textwrap.wrap(line, 100, break_long_words=False, replace_whitespace=False))
                 for line in line.content.splitlines() if line.strip() != '']) + "\n--\n")
        f.write("____________________________________________________________________________________________________\n")
    
    f.write("AGENT:\n" 
            + '\n'.join(['\n'.join(
                textwrap.wrap(line, 100, break_long_words=False, replace_whitespace=False))
                 for line in agent_output.splitlines() if line.strip() != '']) + "\n")
    f.write("____________________________________________________________________________________________________\n")
    f.flush()

f.close()
