from django.shortcuts import render
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Chroma
from rest_framework.decorators import api_view
from langchain_community.document_loaders import CSVLoader
import pandas as pd

from langchain.text_splitter import RecursiveCharacterTextSplitter

def rag_multiple_database(query, chat_history):
    
    OPENAI_API_KEY = "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"

    # embedding = OpenAIEmbeddings(model="text-embedding-ada-002")
    embedding = OpenAIEmbeddings(model="text-embedding-ada-002", openai_api_key=OPENAI_API_KEY)
    
    Techlist =['PHP', '.Net', 'Python', 'aeyc', 'hp', 'ios', 'redbuilt','salesforce', 'simplot', 'truckstop', 'aws']
    
    matched_item = None

    # Check if any item in Techlist is mentioned in the query
    for item in Techlist:
        if item.lower() in query.lower():
            # If there is a match, set the matched_item and break the loop
            matched_item = item
            break
        
    # print(matched_item)
    if matched_item:
        persist_directory = "./vectorDatabases/"+matched_item
        # print(persist_directory)
        vectorstore=Chroma(persist_directory = persist_directory, embedding_function = embedding)
    else:
        persist_directory = "./vectorDatabases/master"
        vectorstore=Chroma(persist_directory = persist_directory, embedding_function = embedding)
    
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    # #gpt-4-vision-preview -> Build system that also process and understand images
    chat_model = ChatOpenAI(model="gpt-4-turbo-preview", temperature=0, verbose=True)

    chain = ConversationalRetrievalChain.from_llm(llm=chat_model, retriever=retriever, verbose=True)
    
    res = chain({"question":query, "chat_history":chat_history})
    
    return res


# resp = rag_multiple_database('Name the projects that used salesforce ?', [])
# print(resp)

