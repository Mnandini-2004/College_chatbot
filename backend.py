from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_cohere import CohereEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain import hub
from langchain.prompts import PromptTemplate
#from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)
from langchain.chains.conversation.memory import ConversationKGMemory
from langchain.chains import ConversationChain
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
def response(user_query,history):
    loader1=PyPDFLoader("SCT1.pdf")
    docs1=loader1.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs1)
    cohere_api_key = "4SD8P6kIuUNhvBIHbi5WQrPKfhZNDG4VloUwWFJr"
    embeddings = CohereEmbeddings(model="embed-english-light-v3.0",cohere_api_key=cohere_api_key)
    vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)
    groq_api_key="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"
    chat = ChatGroq(temperature=0, groq_api_key=groq_api_key, model_name="llama3-70b-8192")

    template = """
        The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. 
        If the AI does not know the answer to a question, it truthfully says it does not know. The AI ONLY uses information contained in the "Relevant Information" section and does not hallucinate.

        Relevant Information:

        {history}

        Conversation:
        Use the following pieces of context to answer the question at the end.
        Don't say based on the given context.
        Say that you don't know when asked a question you don't know, donot make up an answer. Be precise and concise in your answer.

        {context}

        Question: {input}

        Helpful Answer:"""

    prompt = PromptTemplate.from_template(template)
    prompt.format(history = 'history' , context = 'context' , input = 'input')
    from langchain.chains.combine_documents import create_stuff_documents_chain
    document_chain=create_stuff_documents_chain(chat,prompt)
    retriever=vectorstore.as_retriever()
    from langchain.chains import create_retrieval_chain
    retrieval_chain=create_retrieval_chain(retriever,document_chain)
    #user_query="Who is the HOD of CS department"

    res=retrieval_chain.invoke({"input":user_query, "history":history})
    print(res['answer'])
    return res['answer']

user_query="Who is the HOD of CS department"
b=response(user_query,history=any)
print(b)



