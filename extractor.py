import pdfplumber
import re

def extract_text_from_pdf(file):

    text = ""

    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text

    return text


def extract_salary_data(text):

    salary = 0
    tax = 0
    pan = ""

    gross = re.search(r"GROSS.*?(\d{3,})", text, re.I)
    tds = re.search(r"INCOME TAX.*?(\d{2,})", text, re.I)
    pan_match = re.search(r"[A-Z]{5}[0-9]{4}[A-Z]", text)

    if gross:
        salary = int(gross.group(1))

    if tds:
        tax = int(tds.group(1))

    if pan_match:
        pan = pan_match.group()

    return salary, tax, pan


def extract_bank_interest(text):

    interest = 0

    matches = re.findall(r"INTEREST.*?(\d+)", text, re.I)

    for m in matches:
        interest += int(m)

    return interest


def extract_invoice_total(text):

    total = 0

    matches = re.findall(r"TOTAL.*?(\d+)", text, re.I)

    for m in matches:
        total += int(m)

    return total
