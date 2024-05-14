import re
from collections import defaultdict
import streamlit as st

# Function to extract tables and fields from SQL query
def extract_tables_and_fields(sql_query):
    # Regular expressions to find table and field names
    table_pattern = re.compile(r'FROM\s+\[?\w+\]?\.\[?\w+\]?\.\[?(\w+)\]? as (\w+)|JOIN\s+\[?\w+\]?\.\[?\w+\]?\.\[?(\w+)\]? as (\w+)', re.IGNORECASE)
    field_pattern = re.compile(r'(\w+)\.(\w+)', re.IGNORECASE)

    # Find all table aliases and their corresponding full names
    tables = {}
    for match in table_pattern.findall(sql_query):
        table_name = match[0] if match[0] else match[2]
        alias = match[1] if match[1] else match[3]
        tables[alias] = table_name

    # Find all fields and map them to their corresponding tables
    fields = defaultdict(list)
    for match in field_pattern.findall(sql_query):
        alias = match[0]
        field = match[1]
        if alias in tables:
            fields[tables[alias]].append(field)

    return tables, fields

# Streamlit UI setup
st.title("SQL Table and Field Extractor")
st.markdown("""
<style>
body {
    font-family: 'Arial', sans-serif;
    background-color: #f0f2f6;
    color: #333;
}
h1 {
    color: #4c4c4c;
    text-align: center;
    margin-bottom: 20px;
}
textarea {
    width: 100%;
    height: 200px;
}
.stTextArea > div > textarea {
    background-color: #f8f9fa;
    border: 1px solid #dfe1e5;
    border-radius: 8px;
    padding: 10px;
    font-size: 14px;
}
.stButton > button {
    background-color: #4c4c4c;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    cursor: pointer;
    font-size: 14px;
}
.stButton > button:hover {
    background-color: #3a3a3a;
}
</style>
""", unsafe_allow_html=True)

sql_query = st.text_area("Enter your SQL query here:")

if st.button("Extract Tables and Fields"):
    if sql_query:
        tables, fields = extract_tables_and_fields(sql_query)
        st.subheader("Extracted Tables and Fields")

        for table, field_list in fields.items():
            st.markdown(f"### Table: `{table}`")
            for field in field_list:
                st.markdown(f"- Field: `{field}`")
    else:
        st.error("Please enter a valid SQL query.")
