# Langchain docs : https://api.python.langchain.com/en/latest/langchain_api_reference.html#

from langchain_openai.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

from langchain.chains.sequential import SimpleSequentialChain

from langchain.chains.sequential import SequentialChain

from langchain.chains.router import MultiPromptChain
from langchain.chains.router.llm_router import LLMRouterChain, RouterOutputParser
from langchain.prompts import PromptTemplate

llm_model = "gpt-3.5-turbo"

llm = ChatOpenAI(temperature=0.9, model=llm_model)

# prompt1 = ChatPromptTemplate.from_template(
#     "What is the best name to describe \
#     a company that makes {Product}?"
# )

# https://api.python.langchain.com/en/latest/chains/langchain.chains.llm.LLMChain.html#langchain.chains.llm.LLMChain
# chain1 = LLMChain(llm = llm, prompt = prompt1, output_key = "Name", verbose = True)

# prompt2 = ChatPromptTemplate.from_template(
#     "Write a 20 words description for the following \
#     company:{Name}"
# )

# chain2 = LLMChain(llm = llm, prompt = prompt2, output_key = "Description", verbose = True)

# prompt3 = ChatPromptTemplate.from_template(
#     "Come up with a go-to-market strategy for a company based on the following description \
#     description:{Description}"
# )
# chain3 = LLMChain(llm = llm, prompt = prompt3, output_key = "GTM", verbose = True)

# # sschain = SimpleSequentialChain(chains = [chain1, chain2], verbose = True)

# # https://api.python.langchain.com/en/latest/chains/langchain.chains.sequential.SequentialChain.html#langchain.chains.sequential.SequentialChain
# schain = SequentialChain(chains = [chain1, chain2, chain3], input_variables = ["Product"], output_variables = ["Name", "Description", "GTM"])

# product = "ai assistant for financial teams"
# dict = schain(product)
# print(dict["GTM"])

physics_template = """You are a very smart physics professor. \
You are great at answering questions about physics in a concise\
and easy to understand manner. \
When you don't know the answer to a question you admit\
that you don't know.

Here is a question:
{input}"""


math_template = """You are a very good mathematician. \
You are great at answering math questions. \
You are so good because you are able to break down \
hard problems into their component parts, 
answer the component parts, and then put them together\
to answer the broader question.

Here is a question:
{input}"""

history_template = """You are a very good historian. \
You have an excellent knowledge of and understanding of people,\
events and contexts from a range of historical periods. \
You have the ability to think, reflect, debate, discuss and \
evaluate the past. You have a respect for historical evidence\
and the ability to make use of it to support your explanations \
and judgements.

Here is a question:
{input}"""


computerscience_template = """ You are a successful computer scientist.\
You have a passion for creativity, collaboration,\
forward-thinking, confidence, strong problem-solving capabilities,\
understanding of theories and algorithms, and excellent communication \
skills. You are great at answering coding questions. \
You are so good because you know how to solve a problem by \
describing the solution in imperative steps \
that a machine can easily interpret and you know how to \
choose a solution that has a good balance between \
time complexity and space complexity. 

Here is a question:
{input}"""

prompt_infos = [
    {
        "name": "physics", 
        "description": "Good for answering questions about physics", 
        "prompt_template": physics_template
    },
    {
        "name": "math", 
        "description": "Good for answering math questions", 
        "prompt_template": math_template
    },
    {
        "name": "History", 
        "description": "Good for answering history questions", 
        "prompt_template": history_template
    },
    {
        "name": "computer science", 
        "description": "Good for answering computer science questions", 
        "prompt_template": computerscience_template
    }
]

destination_chains = {}
for p_info in prompt_infos:
    name = p_info["name"]
    prompt_template = p_info["prompt_template"]
    prompt = ChatPromptTemplate.from_template(template = prompt_template)
    chain = LLMChain(llm = llm, prompt = prompt, verbose = True)
    destination_chains[name] = chain

destinations = [f"{p['name']}: {p['description']}" for p in prompt_infos]
destinations_str = "\n".join(destinations)
print(destinations_str)

MULTI_PROMPT_ROUTER_TEMPLATE = """Given a raw text input to a \
language model select the model prompt best suited for the input. \
You will be given the names of the available prompts and a \
description of what the prompt is best suited for. \
You may also revise the original input if you think that revising\
it will ultimately lead to a better response from the language model.

<< FORMATTING >>
Return a markdown code snippet with a JSON object formatted to look like:
```json
{{{{
    "destination": string \ name of the prompt to use or "DEFAULT"
    "next_inputs": string \ a potentially modified version of the original input
}}}}
```

REMEMBER: "destination" MUST be one of the candidate prompt \
names specified below OR it can be "DEFAULT" if the input is not\
well suited for any of the candidate prompts.
REMEMBER: "next_inputs" can just be the original input \
if you don't think any modifications are needed.

<< CANDIDATE PROMPTS >>
{destinations}

<< INPUT >>
{{input}}

<< OUTPUT (remember to include the ```json)>>"""

router_template = MULTI_PROMPT_ROUTER_TEMPLATE.format(
    destinations = destinations_str
)

router_prompt = PromptTemplate(
    template = router_template,
    input_variables = ["input"],
    output_parser = RouterOutputParser()
)

# router_chain = LLMRouterChain.from_llm(llm, router_prompt)
llm_chain = LLMChain(llm = llm, prompt = router_prompt, verbose = True)
# https://api.python.langchain.com/en/latest/chains/langchain.chains.router.llm_router.LLMRouterChain.html#langchain.chains.router.llm_router.LLMRouterChain
router_chain = LLMRouterChain(llm_chain = llm_chain)

default_prompt = ChatPromptTemplate.from_template("{input}")
default_chain = LLMChain(llm = llm, prompt = default_prompt, verbose = True)

chain = MultiPromptChain(router_chain = router_chain, destination_chains = destination_chains, default_chain = default_chain, verbose = True)

dict = chain.run("Why is the sky blue?")

print(dict)