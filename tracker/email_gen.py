import streamlit as st
import requests

st.title("Local Ollama Email Generator")
st.write("Upload PDF documents to generate the email content using the Deepseek R1 7B model.")

with st.form("email_form", clear_on_submit=False):
    subject = st.text_input("Email Subject", "Project Update")
    sender = st.text_input("Sender Email", "spoofed@example.com")
    recipient = st.text_input("Recipient Email", "recipient@example.com")
    uploaded_files = st.file_uploader("Upload PDF(s)", type=["pdf"], accept_multiple_files=True)
    submit_button = st.form_submit_button("Generate Email")

if submit_button:
    if not uploaded_files:
        st.error("Please upload at least one PDF file.")
    else:
        endpoint = "http://localhost:5000/generate_email"
        data = {
            "subject": subject,
            "sender": sender,
            "recipient": recipient
        }
        files = []
        for uploaded_file in uploaded_files:
            files.append(
                ("pdfs", (uploaded_file.name, uploaded_file, uploaded_file.type))
            )
        try:
            response = requests.post(endpoint, data=data, files=files)
            if response.status_code == 200:
                result = response.json()
                st.success("Email generated successfully!")
                st.write("**Subject:**", result.get("subject"))
                st.write("**From:**", result.get("from"))
                st.write("**To:**", result.get("to"))
                st.write("**Email Body:**")
                st.text_area("", value=result.get("body"), height=300)
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
