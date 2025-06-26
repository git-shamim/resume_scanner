# utils/file_handler.py
import pdfplumber
import docx2txt

def extract_text_from_file(uploaded_file):
    if uploaded_file.name.endswith('.pdf'):
        with pdfplumber.open(uploaded_file) as pdf:
            return "\n".join([page.extract_text() or "" for page in pdf.pages])
    elif uploaded_file.name.endswith('.docx'):
        return docx2txt.process(uploaded_file)
    elif uploaded_file.name.endswith('.txt'):
        return uploaded_file.read().decode("utf-8")
    else:
        return ""
