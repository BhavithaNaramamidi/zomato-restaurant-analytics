import mysql.connector
import streamlit as st

@st.cache_resource
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        port=3306,
        user="zomato_user",
        password="Zomato@123",
        database="zomato_db"
    )
