from langchain.retrievers.multi_vector import MultiVectorRetriever
from langchain.storage import InMemoryByteStore
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredPowerPointLoader, CSVLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, OpenAI, ChatOpenAI
from langchain.chains import RetrievalQA,ConversationalRetrievalChain
import uuid
import pandas as pd

def multivector_QA(query, chat_history):
    # Define document loaders
    loaders = [
    CSVLoader("C:/Users/priyanka.singhal/data-science_2024/Priyanka/COE_QuestionAnswer/Master data.csv"),
    UnstructuredPowerPointLoader("C:/Users/priyanka.singhal/data-science_2024/Priyanka/COE_QuestionAnswer/consolidated slides PPT.pptx"),
    ]

    docs = []
    for loader in loaders:
        docs.extend(loader.load())
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000)
    docs = text_splitter.split_documents(docs)
    print(docs)
    
    # f = open("C:/Users/priyanka.singhal/Data-Science2024/Priyanka/ITT_Chatbot_React_Django/chatbot_backend/data/splitted_documents.txt", "w")
    # f.write(docs)
    # f.close()
    persist_directory = "./MultivectorDB"

    # The vectorstore to use to index the child chunks
    vectorstore = Chroma.from_documents(
        documents=docs,
        persist_directory = persist_directory,
        collection_name="full_documents",
        embedding=OpenAIEmbeddings()
    )

    # The storage layer for the parent documents
    store = InMemoryByteStore()
    id_key = "doc_id"
    # The retriever (empty to start)
    retriever = MultiVectorRetriever(
        vectorstore=vectorstore,
        byte_store=store,
        id_key=id_key,
    )

    doc_ids = [str(uuid.uuid4()) for _ in docs]
    print(doc_ids)
    # The splitter to use to create smaller chunks
    child_text_splitter = RecursiveCharacterTextSplitter(chunk_size=400)

    sub_docs = []
    for i, doc in enumerate(docs):
        _id = doc_ids[i]
        _sub_docs = child_text_splitter.split_documents([doc])
        for _doc in _sub_docs:
            _doc.metadata[id_key] = _id
        sub_docs.extend(_sub_docs)

    retriever.vectorstore.add_documents(sub_docs)
    retriever.docstore.mset(list(zip(doc_ids, docs)))

    # openai_api_key = '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'
    # llm = OpenAI(api_key=openai_api_key, temperature=0, max_tokens=200)

    # chain_type = "map_reduce"
    # chain = RetrievalQA.from_chain_type(llm=llm,chain_type=chain_type ,retriever=retriever,input_key="question")
    
    chat_model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.5, verbose=True)

    chain = ConversationalRetrievalChain.from_llm(llm=chat_model, retriever=retriever, verbose=True)

    response = chain({"question": query, "chat_history":chat_history})
    # response = chain.invoke({"question": query})

    # print(response)
    return response

# chat_history = []
# file_path = 'C:/Users/priyanka.singhal/Data-Science2024/Priyanka/ITT_Chatbot_React_Django/chatbot_backend/data/COE_QA.xlsx'
# excel_sheet_data = pd.read_excel(file_path)
# questions = excel_sheet_data['Question'].astype(str).tolist()

# # Process each question
# answers = []
# for question in questions:
#     # Invoke the chain with the question and current chat history
#     res = multivector_QA(question, [])
    
#     # Extract the answer from the response
#     answer = res.get('answer')
    
#     if answer:
#         # chat_history.append([question, res['chat_history']])
#         answers.append(answer)
        
#         # Print the answer
#         print(answer)
#     else:
#         print("No answer found for question:", question)


# # Create DataFrame with questions and answers
# df = pd.DataFrame({'Question': questions, 'Answer': answers})

# # Write the DataFrame to an Excel file
# df.to_excel('C:/Users/priyanka.singhal/Data-Science2024/Priyanka/ITT_Chatbot_React_Django/chatbot_backend/data/multivector_updated.xlsx', index=False)

# multivector_QA("What is ITT?", [])
