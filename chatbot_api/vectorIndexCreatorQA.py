# from langchain_community.document_loaders import CSVLoader, UnstructuredExcelLoader
# from langchain.chains.question_answering import load_qa_chain
# from langchain_openai import OpenAI, OpenAIEmbeddings
# from langchain.indexes import VectorstoreIndexCreator
# from langchain.indexes.vectorstore import VectorStoreIndexWrapper
# from langchain.chains import RetrievalQA
# import pandas as pd
# from langchain.vectorstores import Chroma
# import sys
 
# # Suppress deprecation warnings
# import warnings
# warnings.filterwarnings("ignore", category=DeprecationWarning)
 
# # Load the document
# file_path = "C:/Users/priyanka.singhal/Data-Science2024/Priyanka/ITT_Chatbot_React_Django/chatbot_backend/data/Master data.csv"
# loader = CSVLoader(file_path)
 
# # Initialize OpenAI instance with API key
# openai_api_key = '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'
# llm = OpenAI(api_key=openai_api_key, temperature=0)
 
# # Create VectorstoreIndex
# # index_creator = VectorstoreIndexCreator()

# index_creator = VectorstoreIndexCreator(vectorstore_cls=Chroma, vectorstore_kwargs={ "persist_directory": "/persistance/directory/vectorstoresdb"})
# docsearch = index_creator.from_loaders([loader])
 
# retriever = docsearch.vectorstore.as_retriever()
# # Create RetrievalQA chain
# chain = RetrievalQA.from_chain_type(
#     llm=llm,
#     chain_type="stuff",
#     retriever=retriever,
#     input_key="question"
# )
       
 
# # Query the chain
# # query = "What technologies has ITT worked on?"
# user_input = ("Type 1 if you want to create vector database and 2 to load the database")
# if user_input == 1:
#     pass
# else:
#     vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=OpenAIEmbeddings())
#     index = VectorStoreIndexWrapper(vectorstore=vectorstore)
    
# # query = input("Feel free to ask any questions or details you'd like to know about In Time Tec. I'm here to answer any questions you may have!\n")
# # response = chain({"question": query})
# # print("===========================================================================================================================================")
# # print(response['result'])
# # # print("relevant document:", retriever.get_relevant_documents(query))

# while True:
#   if not query:
#     query = input("Feel free to ask any questions or details you'd like to know about In Time Tec. I'm here to answer any questions you may have!\n")
#   if query in ['quit', 'q', 'exit']:
#     sys.exit()
#   result = chain({"question": query})
#   print(result['result'])



import os
import sys

import openai
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader, CSVLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.llms import OpenAI
from langchain.vectorstores import Chroma

def vector_embeddings(query, chat_history):
  openai_api_key = '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'

  # Enable to save to disk & reuse the model (for repeated queries on the same data)
  PERSIST = True

  query = None
  if len(sys.argv) > 1:
    query = sys.argv[1]

  if PERSIST and os.path.exists("./vectorIndexDatabase"):
    print("Reusing index...\n")
    vectorstore = Chroma(persist_directory="./vectorIndexDatabase", embedding_function=OpenAIEmbeddings())
    index = VectorStoreIndexWrapper(vectorstore=vectorstore)
  else:
    #loader = TextLoader("data/data.txt") # Use this line if you only need data.txt
    file_path = "C:/Users/priyanka.singhal/Data-Science2024/Priyanka/ITT_Chatbot_React_Django/chatbot_backend/data/Master data.csv"
    loader = CSVLoader(file_path)
    if PERSIST:
      index = VectorstoreIndexCreator(vectorstore_kwargs={"persist_directory":"./vectorIndexDatabase"}).from_loaders([loader])
    else:
      index = VectorstoreIndexCreator().from_loaders([loader])

  chain = ConversationalRetrievalChain.from_llm(
    llm=ChatOpenAI(model="gpt-3.5-turbo"),
    retriever=index.vectorstore.as_retriever(search_type = "similarity", search_kwargs={"k": 3}),
  )

#   openai_api_key = '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'
#   llm = OpenAI(api_key=openai_api_key, temperature=0)

#   chain = RetrievalQA.from_chain_type(
#       llm=llm,
#       chain_type="stuff",
#       retriever=index.vectorstore.as_retriever(search_kwargs={"k": 1}, search_type="mmr"),
#       input_key="question"
#   )


  result = chain.invoke({"question": query, "chat_history":chat_history})
  return result