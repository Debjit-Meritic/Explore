from openai import OpenAI
import os
import json

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

client = OpenAI(api_key = os.getenv('OPENAI_API_KEY'))

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=1, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message.content


# text = f"""
# You should express what you want a model to do by \ 
# providing instructions that are as clear and \ 
# specific as you can possibly make them. \ 
# This will guide the model towards the desired output, \ 
# and reduce the chances of receiving irrelevant \ 
# or incorrect responses. Don't confuse writing a \ 
# clear prompt with writing a short prompt. \ 
# In many cases, longer prompts provide more clarity \ 
# and context for the model, which can lead to \ 
# more detailed and relevant outputs.
# """
# prompt = f"""
# Summarize the text delimited by triple backticks \ 
# into a single sentence.
# ```{text}```
# """
# response = get_completion(prompt)
# print(response)

# prompt = f"""
# Generate a list of three made-up book titles along \ 
# with their authors and genres. 
# Provide them in JSON format with the following keys: 
# book_id, title, author, genre.
# """
# response = get_completion(prompt)
# print(response)

# text_1 = f"""
# The sun is shining brightly today, and the birds are \
# singing. It's a beautiful day to go for a \ 
# walk in the park. The flowers are blooming, and the \ 
# trees are swaying gently in the breeze. People \ 
# are out and about, enjoying the lovely weather. \ 
# Some are having picnics, while others are playing \ 
# games or simply relaxing on the grass. It's a \ 
# perfect day to spend time outdoors and appreciate the \ 
# beauty of nature.
# """
# prompt = f"""
# You will be provided with text delimited by triple quotes. 
# If it contains a sequence of instructions, \ 
# re-write those instructions in the following format:

# Step 1 - ...
# Step 2 - …
# …
# Step N - …

# If the text does not contain a sequence of instructions, \ 
# then simply write \"No steps provided.\"

# \"\"\"{text_1}\"\"\"
# """
# response = get_completion(prompt)
# print("Completion for Text 1:")
# print(response)

# text = f"""
# In a charming village, siblings Jack and Jill set out on \ 
# a quest to fetch water from a hilltop \ 
# well. As they climbed, singing joyfully, misfortune \ 
# struck—Jack tripped on a stone and tumbled \ 
# down the hill, with Jill following suit. \ 
# Though slightly battered, the pair returned home to \ 
# comforting embraces. Despite the mishap, \ 
# their adventurous spirits remained undimmed, and they \ 
# continued exploring with delight.
# """
# # example 1
# prompt_1 = f"""
# Perform the following actions: 
# 1 - Summarize the following text delimited by triple \
# backticks with 1 sentence.
# 2 - Translate the summary into French.
# 3 - List each name in the French summary.
# 4 - Output a json object that contains the following \
# keys: french_summary, num_names.

# Separate your answers with line breaks.

# Text:
# ```{text}```
# """
# response = get_completion(prompt_1)
# print("Completion for prompt 1:")
# print(response)

# fact_sheet_chair = """
# OVERVIEW
# - Part of a beautiful family of mid-century inspired office furniture, 
# including filing cabinets, desks, bookcases, meeting tables, and more.
# - Several options of shell color and base finishes.
# - Available with plastic back and front upholstery (SWC-100) 
# or full upholstery (SWC-110) in 10 fabric and 6 leather options.
# - Base finish options are: stainless steel, matte black, 
# gloss white, or chrome.
# - Chair is available with or without armrests.
# - Suitable for home or business settings.
# - Qualified for contract use.

# CONSTRUCTION
# - 5-wheel plastic coated aluminum base.
# - Pneumatic chair adjust for easy raise/lower action.

# DIMENSIONS
# - WIDTH 53 CM | 20.87”
# - DEPTH 51 CM | 20.08”
# - HEIGHT 80 CM | 31.50”
# - SEAT HEIGHT 44 CM | 17.32”
# - SEAT DEPTH 41 CM | 16.14”

# OPTIONS
# - Soft or hard-floor caster options.
# - Two choices of seat foam densities: 
#  medium (1.8 lb/ft3) or high (2.8 lb/ft3)
# - Armless or 8 position PU armrests 

# MATERIALS
# SHELL BASE GLIDER
# - Cast Aluminum with modified nylon PA6/PA66 coating.
# - Shell thickness: 10 mm.
# SEAT
# - HD36 foam

# COUNTRY OF ORIGIN
# - Italy
# """

# prompt1 = f"""
# Your task is to help a marketing team create a 
# description for a retail website of a product based 
# on a technical fact sheet.

# Write a product description based on the information 
# provided in the technical specifications delimited by 
# triple backticks.

# Use exactly 50 words.

# Technical specifications: ```{fact_sheet_chair}```
# """

# string_input_counts = []
# for i in range(0, 11):
#     response = get_completion(prompt1)
#     print(str(i) + ":" + response + "\n")
#     string_input_counts.append(len(response.split(" ")))

# prompt2 = f"""
# {{
#     "Task": "Help a marketing team create a 
# description for a retail website of a product based 
# on a technical fact sheet by following the instructions and return the output STRICTLY in the mentioned output_format",
#     "Instructions": [
#         {{"1": "Write a product description based on the provided technical specification"}},
#         {{"2": "Summarise the product description in exactly 80 words."}},
#         {{"3": "Check if the summary is 80 words long. If not then rewrite the summary in 80 words."}}
#     ],
#     "Technical specifications": "{fact_sheet_chair}"}},
#     "Output_Format": "json with with key step number and value as the generated summary at each step. "
# """

# json_input_counts1 = []
# json_input_counts2 = []
# json_input_counts3 = []
# for i in range(1, 11):
#     response = get_completion(prompt2)
#     json_response = json.loads(response)
#     if "1" in json_response:
#         summary1 = json.loads(response)["1"]
#         print(str(i) + "/1" ":" + summary1 + "\n")
#         json_input_counts1.append(len(summary1.split(" ")))

#     if "2" in json_response:
#         summary2 = json.loads(response)["2"]
#         print(str(i) + "/2" ":" + summary2 + "\n")
#         json_input_counts2.append(len(summary2.split(" ")))

#     if "3" in json_response:
#         summary3 = json.loads(response)["3"]
#         print(str(i) + "/3" ":" + summary3 + "\n")
#         json_input_counts3.append(len(summary3.split(" ")))

    

# print("String: " + str(sum(string_input_counts)/len(string_input_counts)))
# print("JSON/1: " + str(sum(json_input_counts1)/len(json_input_counts1)))
# print("JSON/2: " + str(sum(json_input_counts2)/len(json_input_counts2)))
# print("JSON/3: " + str(sum(json_input_counts3)/len(json_input_counts3)))

prompt = f"""
How many lines does the text delimited by triple backticks contain.
Note that a line is defined by the period symbol(.). To count the number of lines, count the number of periods in the text.   
Return the answer as json with key "number_of_lines".
```Hi. Hello. How is that this sentence was written without any consideration. An abomination I tell you.```
"""
line_count = []
for i in range(1, 11):
    response = get_completion(prompt)
    print(i)
    line_count.append(json.loads(response)["number_of_lines"])

print("avg no. of lines: " + str(sum(line_count)/len(line_count)))