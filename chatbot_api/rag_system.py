from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import CSVLoader, UnstructuredPowerPointLoader
import pandas as pd
from datetime import datetime
from  chatbot_backend.settings import OPENAI_API_KEY_value
def rag(query, chat_history):
    
    # embedding = OpenAIEmbeddings(model="gemma-1.1-7b-it")
   
    t0=datetime.now()
    embedding = OpenAIEmbeddings(model="text-embedding-3-large", openai_api_key=OPENAI_API_KEY_value)
    # file_path = "C:/Users/priyanka.singhal/Data-Science2024/Priyanka/ITT_Chatbot_React_Django/chatbot_backend/data/Master data.csv"
    # loader = CSVLoader(file_path)
    # docs = loader.load()
    persist_directory = "./PPTvectorDatabase"

    # text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    # splits = text_splitter.split_documents(docs)
    # vectorstore = Chroma.from_documents(persist_directory = persist_directory, documents=splits, embedding=embedding)
    # vectorstore.persist()
    t1=datetime.now()
    print("t0--------------------",t1-t0)
    vectorstore = Chroma(persist_directory = persist_directory, embedding_function=embedding)
    t2=datetime.now()
    print("t1--------------------",t2-t1)
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    t3=datetime.now()
    print("t2--------------------",t3-t2)
    #gpt-4-vision-preview -> Build system that also process and understand images
    chat_model = ChatOpenAI(model="gpt-3.5-turbo-0613", temperature=0, verbose=True)
    t4=datetime.now()
    print("t3--------------------",t4-t3)
    chain = ConversationalRetrievalChain.from_llm(llm=chat_model, retriever=retriever, verbose=True)
    t5=datetime.now()
    print("t4--------------------",t5-t4)
    res = chain({"question":query, "chat_history":chat_history})
    t6=datetime.now()
    print("t6--------------------",t6-t5)
    return res




