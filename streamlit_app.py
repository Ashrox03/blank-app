import streamlit as st
import sqlite3
import json

# Database Setup
DATABASE = "msme_data.db"

def create_database():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS msme (
            id TEXT PRIMARY KEY,
            name TEXT,
            sector TEXT,
            location TEXT,
            annual_revenue REAL,
            credit_score INTEGER,
            loan_history TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_sample_data():
    sample_data = [
        ("MSME001", "Greenfield Enterprises", "Manufacturing", "Mumbai", 5000000, 720, json.dumps([
            {"amount": 200000, "status": "repaid"},
            {"amount": 500000, "status": "default"}
        ])),
        ("MSME002", "BlueSky Traders", "Retail", "Delhi", 2000000, 680, json.dumps([
            {"amount": 100000, "status": "repaid"}
        ])),
    ]
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.executemany("""
        INSERT OR IGNORE INTO msme (id, name, sector, location, annual_revenue, credit_score, loan_history)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, sample_data)
    conn.commit()
    conn.close()

# Retrieve MSME Data
def retrieve_msme_data(query):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM msme WHERE name LIKE ?", (f"%{query}%",))
    results = cursor.fetchall()
    conn.close()
    return results

# Validation Function
def validate_msme(msme):
    if msme[5] > 700 and msme[4] > 3000000:
        return f"MSME {msme[1]} is eligible for credit."
    else:
        return f"MSME {msme[1]} is not eligible for credit."

# Streamlit App Layout
st.title("MSME Credit Risk Tool")

# Initialize Database
create_database()
insert_sample_data()

# Section: Retrieve MSME Data
st.header("Retrieve MSME Data")
query = st.text_input("Enter MSME name to search:")
if st.button("Search"):
    results = retrieve_msme_data(query)
    if results:
        st.subheader("Search Results:")
        for result in results:
            st.write(f"ID: {result[0]}, Name: {result[1]}, Sector: {result[2]}, Location: {result[3]}, "
                     f"Annual Revenue: {result[4]}, Credit Score: {result[5]}, Loan History: {json.loads(result[6])}")
    else:
        st.warning("No matching MSMEs found.")

# Section: Validate MSME
st.header("Validate MSME")
placeholder_json = {
    "id": "MSME001",
    "name": "Greenfield Enterprises",
    "sector": "Manufacturing",
    "location": "Mumbai",
    "annual_revenue": 5000000,
    "credit_score": 720,
    "loan_history": [
        {"amount": 200000, "status": "repaid"},
        {"amount": 500000, "status": "default"}
    ]
}
st.text("Sample JSON Input:")
st.json(placeholder_json)
msme_json = st.text_area("Enter MSME JSON for validation:")
if st.button("Validate"):
    try:
        msme = json.loads(msme_json)
        result = validate_msme((msme["id"], msme["name"], msme["sector"], msme["location"], msme["annual_revenue"],
                                msme["credit_score"], json.dumps(msme["loan_history"])))
        st.success(result)
    except json.JSONDecodeError:
        st.error("Invalid JSON format. Please check your input.")
