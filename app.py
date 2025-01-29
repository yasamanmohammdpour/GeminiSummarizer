import os
from dotenv import load_dotenv
import google.generativeai as genai
import streamlit as st
from docx import Document
from PyPDF2 import PdfReader

load_dotenv()
API_KEY = os.getenv("API_KEY")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def summarize_note(note_text):
    prompt = f"Summarize the text you get {note_text}"

    response = model.generate_content(prompt)
    result = response.text

    return result

# print(summarize_note("My name is Yasaman and I'm MS student in ASU."))

def extract_text_from_docx(file):
    document = Document(file)
    text = [paragraph.text for paragraph in document.paragraphs]
    return "\n".join(text)

def extract_text_from_pdf(file):
    pdf_reader = PdfReader(file)
    text = [page.extract_text() for page in pdf_reader.pages]
    return "\n".join(text)

st.title("Note Summarizer")
st.write("This app uses GEMINI API to summarize your notes.")

uploaded_file = st.file_uploader("Upload a file (DOCX, PDF)", type=["docx", "pdf"])

if uploaded_file:
    if uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        note_text = extract_text_from_docx(uploaded_file)
    elif uploaded_file.type == "application/pdf":
        note_text = extract_text_from_pdf(uploaded_file)
    else:
        st.error("Unsupported file type.")
        note_text = None
else:
    note_text = st.text_area("Or enter your note here:")

if st.button("Summarize"):
    if note_text:
        summarized_text = summarize_note(note_text)
        st.subheader("Summary")
        st.write(summarized_text)
else:
    st.write("Please enter a note to summarize.")