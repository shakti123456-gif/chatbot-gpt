import pandas as pd
from langchain_openai import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import CSVLoader
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings
)
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA

# OpenAI API key
openai_api_key = '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'
# Create an OpenAI instance
llm = OpenAI(temperature=0, openai_api_key=openai_api_key)

# load the document
file_path = "C:/Users/priyanka.singhal/Data-Science2024/Priyanka/ITT_Chatbot_React_Django/chatbot_backend/data/Master data.csv"
loader = CSVLoader(file_path)
documents = loader.load()

# split it into chunks
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

# create the open-source embedding function
embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

file_path = 'C:/Users/priyanka.singhal/Data-Science2024/Priyanka/ITT_Chatbot_React_Django/chatbot_backend/data/COE_QA.xlsx'
excelSheetData = pd.read_excel(file_path)

answers = []
questions = excelSheetData['Question'].astype(str).tolist()
for question in questions:
      db = Chroma(persist_directory="chroma_db", embedding_function=embedding_function)
      retriever = db.as_retriever(search_type="similarity", search_kwargs={"k":2})
      qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=True)
      result = qa.invoke({"query":question})
    #   questions.append(question)
      page_content= result['result']
      answers.append(page_content)

df = pd.DataFrame({'Question': questions, 'Answer': answers})

# Write the DataFrame to an Excel file
df.to_excel('C:/Users/priyanka.singhal/Data-Science2024/Priyanka/ITT_Chatbot_React_Django/chatbot_backend/data/COE_QA_sentence_transformer.xlsx', index=False)
