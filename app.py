import streamlit as st
import pandas as pd
from extractor import *

st.title("AI Auditor Tax Summary Generator")

salary_file = st.file_uploader("Upload Salary Slip", type=["pdf"])
bank_file = st.file_uploader("Upload Bank Statement", type=["pdf"])
invoice_files = st.file_uploader("Upload Business Invoices", type=["pdf"], accept_multiple_files=True)

if st.button("Generate Tax Summary"):

    salary_income = 0
    tax_deducted = 0
    bank_interest = 0
    business_expenses = 0
    pan = ""

    if salary_file:
        text = extract_text_from_pdf(salary_file)
        salary_income, tax_deducted, pan = extract_salary_data(text)

    if bank_file:
        text = extract_text_from_pdf(bank_file)
        bank_interest = extract_bank_interest(text)

    if invoice_files:
        for file in invoice_files:
            text = extract_text_from_pdf(file)
            business_expenses += extract_invoice_total(text)

    data = {
        "Category": [
            "Salary Income",
            "Bank Interest",
            "Business Expenses",
            "Tax Deducted"
        ],
        "Amount": [
            salary_income,
            bank_interest,
            business_expenses,
            tax_deducted
        ]
    }

    df = pd.DataFrame(data)

    st.subheader("Tax Summary")
    st.table(df)

    st.download_button(
        "Download Tax Summary CSV",
        df.to_csv(index=False),
        file_name="tax_summary.csv"
    )
