import streamlit as st
import json

# Placeholder Data for MSMEs
msme_data = [
    {
        "id": "MSME001",
        "name": "Greenfield Enterprises",
        "sector": "Manufacturing",
        "location": "Mumbai",
        "annual_revenue": 5000000,
        "credit_score": 720,
        "loan_history": [
            {"amount": 200000, "status": "repaid"},
            {"amount": 500000, "status": "default"},
        ],
    },
    {
        "id": "MSME002",
        "name": "BlueSky Traders",
        "sector": "Retail",
        "location": "Delhi",
        "annual_revenue": 2000000,
        "credit_score": 680,
        "loan_history": [
            {"amount": 100000, "status": "repaid"}
        ],
    },
]

# Retrieval Function
def retrieve_msme_data(query):
    results = [msme for msme in msme_data if query.lower() in msme["name"].lower()]
    return results if results else []

# Validation Function
def validate_msme(msme):
    if msme["credit_score"] > 700 and msme["annual_revenue"] > 3000000:
        return f"MSME {msme['name']} is eligible for credit."
    else:
        return f"MSME {msme['name']} is not eligible for credit."

# Streamlit App Layout
st.title("MSME Credit Risk Tool")

# Section: Retrieve MSME Data
st.header("Retrieve MSME Data")
query = st.text_input("Enter MSME name to search:")
if st.button("Search"):
    results = retrieve_msme_data(query)
    if results:
        st.subheader("Search Results:")
        for result in results:
            st.write(f"ID: {result['id']}, Name: {result['name']}, Sector: {result['sector']}, Location: {result['location']}, Annual Revenue: {result['annual_revenue']}, Credit Score: {result['credit_score']}")
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
        result = validate_msme(msme)
        st.success(result)
    except json.JSONDecodeError:
        st.error("Invalid JSON format. Please check your input.")
