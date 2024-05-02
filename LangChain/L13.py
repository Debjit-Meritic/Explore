from openai import OpenAI
import os

from dotenv import load_dotenv
load_dotenv()


llm_model = "gpt-3.5-turbo"
# client = OpenAI(
#     api_key = os.environ['OPENAI_API_KEY']
# )

from typing import List
from pydantic import BaseModel, Field

class User(BaseModel):
    name: str
    age: int
    email: str

# foo = User(name = "Joe", age = "12", email = "joe@gmail.com")
# print(foo.name)

from langchain_core.utils.function_calling import convert_pydantic_to_openai_function
from langchain_openai import ChatOpenAI

class WeatherSearch(BaseModel):
    """Call this with an airport code to get the weather at that airport"""
    airport_code: str = Field(description="airport code to get weather for")

weather_function = convert_pydantic_to_openai_function(WeatherSearch)
# print(weather_function)

model = ChatOpenAI()
# print(model.invoke("what is the weather in SF today?", functions = [weather_function]))

model_with_function = model.bind(functions = [weather_function])
print(model_with_function.invoke("what is the weather in sf?"))
