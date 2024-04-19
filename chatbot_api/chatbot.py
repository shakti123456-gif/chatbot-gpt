from langchain.retrievers.multi_vector import MultiVectorRetriever
from langchain.storage import InMemoryByteStore
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredPowerPointLoader, CSVLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, OpenAI
from langchain.chains import RetrievalQA
import uuid
# import pandas as pd

loaders = [
    CSVLoader("C:/Users/priyanka.singhal/data-science_2024/Priyanka/COE_QuestionAnswer/Master data.csv"),
    UnstructuredPowerPointLoader("C:/Users/priyanka.singhal/data-science_2024/Priyanka/COE_QuestionAnswer/consolidated slides PPT.pptx"),
]

docs = []
for loader in loaders:
    docs.extend(loader.load())
text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000)
docs = text_splitter.split_documents(docs)

# The vectorstore to use to index the child chunks
vectorstore = Chroma(
    collection_name="full_documents",
    embedding_function=OpenAIEmbeddings()
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

openai_api_key = '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'
llm = OpenAI(api_key=openai_api_key, temperature=0, max_tokens=200)

chain_type = "map_reduce"
chain = RetrievalQA.from_chain_type(llm=llm,chain_type=chain_type ,retriever=retriever,input_key="question")

# query = input("Feel free to ask any questions or details you'd like to know about In Time Tec. I'm here to answer any questions you may have!\n")
# response = chain.invoke({"question": query})
# print("===========================================================================================================================================")
# print(response['result'])

# file_path = 'C:/Users/priyanka.singhal/data-science_2024/Priyanka/COE_QuestionAnswer/COE_QA.xlsx'
# excelSheetData = pd.read_excel(file_path)

# answers = []
# questions = excelSheetData['Question'].astype(str).tolist()
# for question in questions:
#       chain_type = "map_reduce"
#       chain = RetrievalQA.from_chain_type(llm=llm,chain_type=chain_type ,retriever=retriever,input_key="question")
#       result = chain.invoke({"question":question})
#       page_content= result['result']
#       answers.append(page_content)

# df = pd.DataFrame({'Question': questions, 'Answer': answers})

# # Write the DataFrame to an Excel file
# df.to_excel('multivector_questions_and_answers.xlsx', index=False)
