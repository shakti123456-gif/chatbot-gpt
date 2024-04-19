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



llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)

answer_prompt = PromptTemplate.from_template(
  """Given the following user question, corresponding SQL query, and SQL result, answer the user question.

Question: {question}
SQL Query: {query}
SQL Result: {result}
Answer: """
)


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
print(db.dialect)
print(db.get_usable_table_names())

execute_query = QuerySQLDataBaseTool(db=db)
write_query = create_sql_query_chain(llm, db)

answer = answer_prompt | llm | StrOutputParser()
chain = (
  RunnablePassthrough.assign(query=write_query).assign(
    result=itemgetter("query") | execute_query
  )
  | answer
)

result = chain.invoke({"question": "List the different industries ITT has experience working with"})
print(result)