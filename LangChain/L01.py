import os

# for direct api calls to OpenAI
import openai

# for api calls through LangChain
from langchain_openai import ChatOpenAI

# prompt mgmt for chat i.e. sequence of messages
from langchain.prompts import ChatPromptTemplate

from langchain.prompts import HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage

from datetime import date

openai.api_key = os.getenv('OPENAI_API_KEY')

llm_model = "gpt-3.5-turbo"
#---------------------------------------------------
# # Chatting with gpt throught direct api calls 

# def get_completion (prompt, model=llm_model):
#     messages = [
#         {"role": "system", "content": "You are an elementary school science teacher teaching a class of 6 year old kids who refers to everyone as darling."},
#         {"role": "user", "content": prompt}]
    
#     # https://platform.openai.com/docs/api-reference/chat/create
#     response = openai.chat.completions.create(
#         model = model,
#         messages = messages,
#         temperature = 0,
#     )
#     print(response)
#     return response.choices[0].message.content

# print(get_completion("Why is the sky blue?"))

#---------------------------------------------------
# Chatting with gpt through langchain library

chat = ChatOpenAI(temperature = 0.0, model = llm_model, verbose = True)

# chat_template = ChatPromptTemplate.from_messages(
#     [
#         SystemMessage(
#             content=(
#                 "You are a helpful assistant that re-writes the user's text to "
#                 "sound more upbeat."
#             )
#         ),
#         HumanMessagePromptTemplate.from_template("{text}"),
#     ]
# )

# # https://api.python.langchain.com/en/latest/prompts/langchain_core.prompts.chat.ChatPromptTemplate.html
# # https://python.langchain.com/docs/modules/model_io/prompts/quick_start/
# chat_template = ChatPromptTemplate.from_messages(
#     [
#         SystemMessage.construct( content = ("You are an elementary school science teacher teaching a class of 6 year old kids who refers to everyone as darling.")),
#         HumanMessagePromptTemplate.from_template("""Respond to the question that is delimited by triple backticks keeping in mind that the question has been asked by a kid with \
# learning disability, so on top of answering the question, explain the answer in a way which will be easy to understand to the kid. 
# text: '''{text}```""")
#     ]
# )

# {
#     "metric":"",
#     "time_constraint":"",
#     "time_constraint_bucketing":"",
#     "time_constaint_value":"",
#     "attribute_constraint":"",
#     "attribute_constraint_value":"",
# }

chat_template = """\
Your job is to extract relevent information for querying a database with multiple factual and dimensional or attribute columns.\
 Figure out the names of the columns and the values for those columns to be used for querying.

Information about the database is below as a list of names of columns.
database:{db}
When extracting names of columns from the user_text, ensure that the columns exist in the database. If the columns don't exist in the database, then set the field to null.

Extract the following information from the text given at the bottom:

metric: If the user mentions a column present in the database then extract the name as the value of metric, else null.  

metric_present: If metric is present in database as a column, then true, else false.

time_constraint: If the user is mentioning a time constraint, then assume this field to be "Date", else null.

time_constraint_bucketing: If the user mentions unit of time like month, year, or quarter, then use that as the bucket, else null.

time_constraint_start: If the user mentions time period, then extract the start of it as "(month, year)", else null. Extract the month as the name of the month and the year as number.

time_constraint_end: If the user mentions time period, then extract the end of it as "(month, year)", else null. Extract the month as the name of the month and the year as number.

attribute_constraint: If the user mentions a dimensional attribute, then extract the name, else null.

attribute_constraint_value: If the user mentions a value for the attribute constraint, then extract the value. If the value is present in database, then set field as the value, else null.

Format the output as JSON with the following keys:
metric
metric_present
time_constraint_bucketing
time_constraint_start
time_constraint_end
attribute_constraint
attribute_constraint_value

Today's date is {date}.
Here are some example queries to guide you:
---
User: "What happened with the revenue for last quarter?",
Assistant:"(
    "metric": "revenue",
    "metric_present": "True",
    "time_constraint": "Date",
    "time_constraint_bucketing": "quarter",
    "time_constraint_start": "(Jan, 2024)",
    "time_constraint_end": "(Mar, 2024)",
    "attribute_constraint": null,
    "attribute_constraint_value": null
    )"
---
User: "What happened with the subscriptions in Brazil?",
Assistant:"(
    "metric": "subscriptions",
    "metric_present", "True",
    "time_constraint": "Date",
    "time_constraint_bucketing": "month",
    "time_constraint_start": "(Apr, 2024)",
    "time_constraint_end": "(Apr, 2024)",
    "attribute_constraint": "location",
    "attribute_constraint_value": "Brazil"
    )"

user_text: {text}
"""

MKG_data =  """\
Attributes: ["Pillar", "Location"]
Time: ["Date"]
Metrics: ["Revenue", "Leads"]
Values for Pillar: ["OE Adult", "OE Jr", "Enterprise", "Open Mundo"]
Values for Location: ["Brazil", "Chile", "Peru", "Mexico"]
"""



prompt_template = ChatPromptTemplate.from_template(chat_template)
prompt = prompt_template.format_messages(db = MKG_data, date = date.today(), text = "How did revenue do for OE Adult in Brazil this quarter?")


# prompt_template = ChatPromptTemplate.from_template(template)
# print(prompt_template)
# user_message = chat_template.format_messages(text = )
# print(user_message)

response = chat(prompt)
print(response.content)

