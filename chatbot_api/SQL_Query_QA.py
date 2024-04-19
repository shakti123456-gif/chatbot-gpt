from operator import itemgetter

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain.chains import create_sql_query_chain
from langchain_community.utilities import SQLDatabase
import pandas as pd
from sqlalchemy import create_engine
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime

def get_quantitative_answer(query):
    
    llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)
    t1=datetime.now()
    answer_prompt = PromptTemplate.from_template(
        """Given the following user question, corresponding SQL query, and SQL result, answer the user question.

    Question: {question}
    SQL Query: {query}
    SQL Result: {result}
    Answer: """
    )
    t2=datetime.now()
    print(t1,t2,"t2,t1",t2-t1)

    # file_path = "C:/Users/priyanka.singhal/Data-Science2024/Priyanka/ITT_Chatbot_React_Django/chatbot_backend/data/Master data.csv"

    # df = pd.read_csv(file_path)

    # # Convert all text data to lowercase
    # df = df.applymap(lambda x: x.lower() if isinstance(x, str) else x)

    # # Save the modified DataFrame back to CSV
    # df.to_csv(file_path, index=False)

    # engine = create_engine("sqlite:///ITT_data.db")
    # df.to_sql("ITT", engine, index=False)

    # db = SQLDatabase(engine=engine)
    # print(db.dialect)
    # print(db.get_usable_table_names())
    db = SQLDatabase.from_uri("sqlite:///ITT_data.db")
    t3=datetime.now()
    print(t3,t2,"---------------t3",t3-t2)
    execute_query = QuerySQLDataBaseTool(db=db)
    write_query = create_sql_query_chain(llm, db)
    t4=datetime.now()
    print(t4,t3,'-------------',t4-t3)
    answer = answer_prompt | llm | StrOutputParser()
    t5=datetime.now()
    chain = (
        RunnablePassthrough.assign(query=write_query).assign(
            result=itemgetter("query") | execute_query
        )
        | answer
    )
    t6=datetime.now()
    print(t5,t6,"t6----------------------------",t6-t5)
    result = chain.invoke({"question": query})
    t7=datetime.now()
    print(t6,t7,"--------------------t7",t7-t6)
    return result
