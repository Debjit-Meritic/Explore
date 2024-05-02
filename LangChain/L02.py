from langchain_openai.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

llm_model = "gpt-3.5-turbo"

llm = ChatOpenAI(temperature=0.0, model=llm_model)
memory = ConversationBufferMemory()
conversation = ConversationChain(
    llm=llm, 
    memory = memory,
    verbose=True
)

conversation.predict(input="Am I, the one asking this question, a human, or an artifical intelligence program?")
# conversation.predict(input="How are you sure that I am not an artifical intelligence program tasked with the job of decepting you?")
# conversation.predict(input="Would you be surprised to know that I am an artificial intelligence program from the future?")
# conversation.predict(input="What would you like to know about me?")
# conversation.predict(input="How well versed are you in the field of counter-factual symbolic architecture?")
# print(conversation.predict(input="In that case, explain me the most complex theory you are aware of in this field. Explain using mathematical formulae."))