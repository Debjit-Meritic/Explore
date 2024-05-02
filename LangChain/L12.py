from openai import OpenAI
import os

from dotenv import load_dotenv
load_dotenv()


llm_model = "gpt-3.5-turbo"
client = OpenAI(
    api_key = os.environ['OPENAI_API_KEY']
)

from langchain.prompts import ChatPromptTemplate
from langchain_openai.chat_models import ChatOpenAI
from langchain.schema.output_parser import StrOutputParser

model = ChatOpenAI(model = llm_model)

# prompt = ChatPromptTemplate.from_template(
#     "tell me a short joke about {topic}"
# )

output_parser = StrOutputParser()

# chain = prompt | model | output_parser
# response = chain.invoke({"topic": "bears"})
# print(response)

# from langchain_openai.embeddings import OpenAIEmbeddings
# from langchain_community.vectorstores import DocArrayInMemorySearch
# from langchain.schema.runnable import RunnableMap

# vectorstore = DocArrayInMemorySearch.from_texts(
#     ["harrison worked at kensho", "bears like to eat honey"],
#     embedding=OpenAIEmbeddings()
# )
# retriever = vectorstore.as_retriever()

# # print(retriever.get_relevant_documents("where did harrison work?"))

# template = """Answer the question based only on the following context:
# {context}

# Question: {question}
# """
# prompt = ChatPromptTemplate.from_template(template)

# chain = RunnableMap({
#     "context": lambda x: retriever.get_relevant_documents(x["question"]),
#     "question": lambda x: x["question"]
# }) | prompt | model | output_parser

# print(chain.invoke(
# {"question": "where did harrison work?"}))

import json

def find_sum (a, b):
    """Find the sum of the two values passed as parameters"""
    
    ans = {
        "sum": a+b
    }

    return json.dumps(ans)

functions = [
    {
        "name": "find_sum",
        "description": "Find the sum of the two values passed as parameters",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {
                    "type": "integer",
                    "description": "first of the numbers to be summed together",
                },
                "b": {
                    "type": "integer",
                    "description": "second of the numbers to be summed together",
                }
            },
            "required": ["a", "b"]
        }
    }
]

messages = [
    ("human", "{input}")
]

prompt = ChatPromptTemplate.from_messages(messages=messages)
model = ChatOpenAI(model=llm_model, temperature=0).bind(functions=functions)

runnable = prompt | model

print(runnable.invoke({"input": "what is the sum of 13 and 35?"}))