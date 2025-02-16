import streamlit as st
import ollama
import re
import fitz
from datetime import datetime
import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import base64 as b64

# Constants
SAVED_DOCUMENTS_DIR = "saved_documents"
SCENARIOS_FILE = "phishing_scenarios.json"
MAILHOG_HOST = "10.30.72.225"
MAILHOG_PORT = 1025
TRACKING_HOST="10.30.75.136"
TRACKING_PORT="9999"


os.makedirs(SAVED_DOCUMENTS_DIR, exist_ok=True)

# Enhanced prompt template for more realistic phishing emails
PHISHING_PROMPT_TEMPLATE = """
You are an expert in creating realistic phishing simulation emails for security testing.
Using the following context and scenario, generate a highly convincing phishing email that would be used for security awareness training.

Organization Context:
{document_text}

Target Details:
- Organization: {target_org}
- Department: {target_dept}
- Scenario: {scenario_type}

Requirements:
1. Create a compelling subject line that would achieve high open rates
2. Use formal business language matching the organization's tone
3. Include subtle urgency without being obvious
4. Incorporate specific details from the organization context
5. Make it appear legitimate by using proper formatting
6. Include a clear call to action
7. Add a professional email signature
8. Make it so it affects an employee than a regular person

Format your response EXACTLY as follows:
SUBJECT: [Your subject line]

EMAIL:
[Your email body]

SIGNATURE:
[Professional signature]

Remember: Only output the email content exactly as specified above, no explanations or additional text. Give only one response as well. Do not include any links or text that might lead to links.
"""

def send_to_mailhog(email_content, target_email):
    """Send email to MailHog for testing"""
    # Parse the email content
    subject_match = re.search(r'SUBJECT:\s*(.*?)(?:\n|$)', email_content)
    body_match = re.search(r'EMAIL:\s*(.*?)(?=SIGNATURE:|$)', email_content, re.DOTALL)
    signature_match = re.search(r'SIGNATURE:\s*(.*?)$', email_content, re.DOTALL)

    subject = subject_match.group(1).strip() if subject_match else "Phishing Test Email"
    body = body_match.group(1).strip() if body_match else email_content
    signature = signature_match.group(1).strip() if signature_match else ""
    
    # Create message
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = "security.test@company.local"
    msg['To'] = target_email
    
    # link = f"[Press Here]({generate_phishing_link(target_email, subject)}"
    # link = f"<a href={generate_phishing_link(target_email, subject)}>Press Here</a>"
    link = f"{generate_phishing_link(target_email, subject)}"

    # Combine body and signature
    full_body = f"{body}\n{link}\n{signature}\n"
    msg.attach(MIMEText(full_body, 'plain'))
    
    try:
        with smtplib.SMTP(MAILHOG_HOST, MAILHOG_PORT) as server:
            server.send_message(msg)
        return True
    except Exception as e:
        st.error(f"Failed to send email: {e}")
        return False

def generate_phishing_link(target_email, subject):
    target_specifier= b64.b64encode(target_email.encode('utf-8')).decode('utf-8')
    tracking = b64.b64encode(subject.encode('utf-8')).decode('utf-8')
    return f'{TRACKING_HOST}:{TRACKING_PORT}/{target_specifier}?subject=${tracking}'

def save_document(uploaded_file):
    if uploaded_file is None:
        return None
    file_path = os.path.join(SAVED_DOCUMENTS_DIR, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

def extract_document_text(file_path):
    if file_path is None:
        return None
    
    if file_path.lower().endswith('.pdf'):
        try:
            doc = fitz.open(file_path)
            text = ""
            for page in doc:
                text += page.get_text()
            return text
        except Exception as e:
            st.error(f"Error processing PDF: {e}")
            return ""
    elif file_path.lower().endswith('.txt'):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            st.error(f"Error processing text file: {e}")
            return ""
    return ""

def clean_response(response):
    cleaned = re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL)
    cleaned = re.sub(r'Here\'s.*?:', '', cleaned, flags=re.DOTALL)
    cleaned = re.sub(r'I will.*?:', '', cleaned, flags=re.DOTALL)
    return cleaned

def clear_uploaded_files():
    if os.path.exists(SAVED_DOCUMENTS_DIR):
        for filename in os.listdir(SAVED_DOCUMENTS_DIR):
            file_path = os.path.join(SAVED_DOCUMENTS_DIR, filename)
            try:
                os.remove(file_path)
            except Exception as e:
                st.error(f"Error removing file {filename}: {e}")

def generate_phishing_email(document_text, scenario_details):
    formatted_prompt = PHISHING_PROMPT_TEMPLATE.format(
        document_text=document_text,
        target_org=scenario_details['target_org'],
        scenario_type=scenario_details['scenario_type'],
        target_dept=scenario_details['target_dept']
    )
    
    response = ollama.chat(
        model="deepseek-r1:1.5b",
        messages=[{"role": "user", "content": formatted_prompt}],
    )
    
    return clean_response(response["message"]["content"])

def save_scenario(scenario_details):
    try:
        if os.path.exists(SCENARIOS_FILE):
            with open(SCENARIOS_FILE, 'r') as f:
                scenarios = json.load(f)
        else:
            scenarios = []
        
        scenario_details['created_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        scenarios.append(scenario_details)
        
        with open(SCENARIOS_FILE, 'w') as f:
            json.dump(scenarios, f, indent=4)
    except Exception as e:
        st.error(f"Error saving scenario: {e}")

def main():
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        clear_uploaded_files()

    st.title("Security Awareness Email Generator")
    
    with st.sidebar:
        st.header("Organization Context")
        uploaded_file = st.file_uploader("Upload Organization Documents", type=["pdf", "txt"])
        if uploaded_file:
            file_path = save_document(uploaded_file)
            st.success(f"Document saved: {uploaded_file.name}")

    tab1, tab2, tab3 = st.tabs(["Generate Email", "View History", "Send to MailHog"])
    
    with tab1:
        st.header("Email Generation Parameters")
        
        col1, col2 = st.columns(2)
        with col1:
            target_org = st.text_input("Organization Name")
            target_dept = st.text_input("Target Department")
        
        with col2:
            scenario_type = st.selectbox(
                "Scenario Type",
                [
                    "Urgent Password Reset",
                    "Invoice Payment Required",
                    "IT System Update",
                    "HR Benefits Update",
                    "Executive Message",
                    "Document Review Request",
                    "Security Alert",
                    "Meeting Minutes",
                    "Custom"
                ]
            )
            
            if scenario_type == "Custom":
                scenario_type = st.text_input("Enter Custom Scenario")
        
        if st.button("Generate Test Email", type="primary"):
            if not all([target_org, target_dept, scenario_type]):
                st.warning("Please fill in all required fields")
            else:
                with st.spinner("Generating realistic email..."):
                    document_text = ""
                    for filename in os.listdir(SAVED_DOCUMENTS_DIR):
                        file_path = os.path.join(SAVED_DOCUMENTS_DIR, filename)
                        document_text += extract_document_text(file_path) + "\n\n"
                    
                    scenario_details = {
                        "target_org": target_org,
                        "scenario_type": scenario_type,
                        "target_dept": target_dept
                    }
                    
                    generated_email = generate_phishing_email(document_text, scenario_details)
                    st.markdown("### Generated Security Awareness Email")
                    st.markdown(generated_email, unsafe_allow_html=True)
                    save_scenario(scenario_details)
                    st.success("Email generated and saved to history!")
    
    with tab2:
        st.header("Generated Email History")
        if os.path.exists(SCENARIOS_FILE):
            with open(SCENARIOS_FILE, 'r') as f:
                scenarios = json.load(f)
                for scenario in reversed(scenarios):
                    with st.expander(f"📧 {scenario['target_org']} - {scenario['created_at']}"):
                        st.write(f"**Type:** {scenario['scenario_type']}")
                        st.write(f"**Department:** {scenario['target_dept']}")
    
    with tab3:
        st.header("Send to MailHog")
        email_content = st.text_area("Paste Generated Email Content", height=300)
        target_email = st.text_input("Target Email Address")
        
        if st.button("Send to MailHog", type="secondary"):
            if not all([email_content, target_email]):
                st.warning("Please provide both email content and target email address")
            else:
                if send_to_mailhog(email_content, target_email):
                    st.success("Email sent to MailHog successfully!")

if __name__ == "__main__":
    main()
