import streamlit as st
import psycopg2  # For PostgreSQL
import json

# Database Connection Setup
def connect_to_db():
    return psycopg2.connect(
        dbname="your_db_name",
        user="your_username",
        password="your_password",
        host="your_host",  # e.g., "localhost" or cloud database host
        port="5432"        # Default PostgreSQL port
    )

# Retrieve MSME Data from Database
def retrieve_msme_data_from_db(query):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM msmes WHERE name ILIKE %s", (f"%{query}%",))
    results = cursor.fetchall()
    conn.close()
    return results

# Streamlit App
st.title("MSME Credit Risk Tool")

# Search MSME Data
st.header("Search MSME")
query = st.text_input("Enter MSME name
