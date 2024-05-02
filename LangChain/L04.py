from langchain.chains.retrieval_qa import RetrievalQA
from langchain_openai.chat_models import ChatOpenAI
from langchain.document_loaders import CSVLoader
from langchain_community.vectorstores import DocArrayInMemorySearch
from IPython.display import display, Markdown
from langchain_openai.llms import OpenAI


# qna on a document by storing the text of the doc in a vector db and running querries on the vector db using llm