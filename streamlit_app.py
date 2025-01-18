
import streamlit as st
import pandas as pd

# Simulated SME dataset
sme_data = [
    {"GSTIN": "1234ABCD", "Name": "ABC Pvt Ltd", "Revenue": 5000000, "Credit Score": 750, "Risk Level": "Low"},
    {"GSTIN": "5678EFGH", "Name": "XYZ Enterprises", "Revenue": 3000000, "Credit Score": 650, "Risk Level": "Medium"},
    {"GSTIN": "9101IJKL", "Name": "LMN Solutions", "Revenue": 2000000, "Credit Score": 500, "Risk Level": "High"}
]

# Convert to DataFrame
sme_df = pd.DataFrame(sme_data)

# Title
st.title("SME Credit Risk Assessment Tool")

# GSTIN Input
gstin_input = st.text_input("Enter GSTIN:")

# Fetch SME Details
if gstin_input:
    sme = sme_df[sme_df["GSTIN"] == gstin_input]
    if not sme.empty:
        st.subheader("SME Details")
        st.write(sme)
    else:
        st.error("GSTIN not found in the database.")

# Simulate AI Insight
if st.button("Generate AI Insight"):
    if gstin_input and not sme.empty:
        st.subheader("AI-Generated Insight")
        st.write(f"The SME '{sme.iloc[0]['Name']}' has a credit score of {sme.iloc[0]['Credit Score']}, indicating a '{sme.iloc[0]['Risk Level']}' risk.")
    else:
        st.warning("Please enter a valid GSTIN.")
