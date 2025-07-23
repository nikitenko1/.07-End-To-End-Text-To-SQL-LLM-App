from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
import sqlite3
import streamlit as st

from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# Retrieve the API key from the environment variable
api_key = os.getenv("GROQ_API_KEY")

def get_sql_query(user_query):
    groq_sys_prompt = ChatPromptTemplate.from_template("""
                    You are an expert in converting English questions to SQL query!
                    The SQL database has the name SIX_NATIONS and has the following columns - TEAM, STADIUM, 
                    LOCATION and CAPACITY. For example, 
                    Example 1 - How many entries of records are present?, 
                        the SQL command will be something like this SELECT COUNT(*) FROM SIX_NATIONS;
                    Example 2 - Tell me all the team playing in Cardiff LOCATION?, 
                        the SQL command will be something like this SELECT * FROM SIX_NATIONS 
                        where LOCATION="Cardiff"; 
                    also the sql code should not have ``` in beginning or end and sql word in output.
                    Now convert the following question in English to a valid SQL Query: {user_query}. 
                    No preamble, only valid SQL please
                                                       """)
    model="llama3-8b-8192"
    # Initialize the Groq client with the API key
    llm = ChatGroq(
    api_key=api_key,
    model_name=model
    )

    chain = groq_sys_prompt | llm | StrOutputParser()
    response = chain.invoke({"user_query": user_query})
    return response


def return_sql_response(sql_query):
    database = "six_nations.db"
    with sqlite3.connect(database) as conn:
        return conn.execute(sql_query).fetchall()


def main():
    st.set_page_config(page_title="Text To SQL")
    st.header("Talk to your Database!")

    user_query=st.text_input("Input:")
    submit=st.button("Enter")

    if submit:
        sql_query = get_sql_query(user_query)
        retrieved_data = return_sql_response(sql_query)
        st.subheader(f"Retrieving results from the database for the query: [{sql_query}]")
        for row in retrieved_data:
            st.header(row)

if __name__ == '__main__':
    main()