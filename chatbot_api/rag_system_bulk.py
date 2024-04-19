from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Chroma
from langchain_community.document_loaders import CSVLoader
import pandas as pd

OPENAI_API_KEY = "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"

# Initialize OpenAIEmbeddings
embedding = OpenAIEmbeddings(model="text-embedding-ada-002")

# Load documents
file_path = "C:/Users/priyanka.singhal/Data-Science2024/Priyanka/ITT_Chatbot_React_Django/chatbot_backend/data/Master data.csv"
loader = CSVLoader(file_path)
docs = loader.load()

# Split documents and create vector store
vectorstore = Chroma.from_documents(documents=docs, embedding=embedding)

# Create retriever
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})

# Initialize chat model
chat_model = ChatOpenAI(model="gpt-4-turbo-preview", temperature=0, verbose=True)

# Initialize Conversational Retrieval Chain
chain = ConversationalRetrievalChain.from_llm(llm=chat_model, retriever=retriever, verbose=True)

# Load questions from Excel
file_path = 'C:/Users/priyanka.singhal/Data-Science2024/Priyanka/ITT_Chatbot_React_Django/chatbot_backend/data/COE_QA.xlsx'
excel_sheet_data = pd.read_excel(file_path)
questions = excel_sheet_data['Question'].astype(str).tolist()

def json_to_chathistory(history):
    res = []
    for each in history:
        res.append((each[0], each[1]))
    return res

# Initialize chat history as an empty list
chat_history = []

# Process each question
answers = []
for question in questions:
    # Invoke the chain with the question and current chat history
    response = chain({"question": question, "chat_history": chat_history})
    
    # Extract the answer from the response
    answer = response.get('answer')
    
    if answer:
        # chat_history.extend([question, response])
        answers.append(answer)
        
        # Print the answer
        print(answer)
    else:
        print("No answer found for question:", question)


# Create DataFrame with questions and answers
df = pd.DataFrame({'Question': questions, 'Answer': answers})

# Write the DataFrame to an Excel file
df.to_excel('C:/Users/priyanka.singhal/Data-Science2024/Priyanka/ITT_Chatbot_React_Django/chatbot_backend/data/COE_QA_Updated_priyanka.xlsx', index=False)
