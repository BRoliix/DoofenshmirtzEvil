import json
import os
import re
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import fitz
import streamlit as st

# Set page config first (required for cloud deployment)
st.set_page_config(
    page_title="S.S.T.R - Phishing Simulator",
    page_icon="🎣",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Try to import ollama, but handle cloud deployment gracefully
try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
    st.warning("⚠️ Running in demo mode - Ollama not available in cloud environment")

# Constants
SAVED_DOCUMENTS_DIR = "saved_documents"
SCENARIOS_FILE = "mock/phishing_scenarios.json"
MAILHOG_HOST = "localhost"
MAILHOG_PORT = 1025

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

Remember: Only output the email content exactly as specified above, no explanations or additional text. Give only one response as well. Also structure the email so it leads to a link at the end.
ALSO FILL IN ANY DETAILS.
"""


def send_to_mailhog(email_content, target_email):
    """Send email to MailHog for testing"""
    # Parse the email content
    subject_match = re.search(r"SUBJECT:\s*(.*?)(?:\n|$)", email_content)
    body_match = re.search(r"EMAIL:\s*(.*?)(?=SIGNATURE:|$)", email_content, re.DOTALL)
    signature_match = re.search(r"SIGNATURE:\s*(.*?)$", email_content, re.DOTALL)

    subject = subject_match.group(1).strip() if subject_match else "Phishing Test Email"
    body = body_match.group(1).strip() if body_match else email_content
    signature = signature_match.group(1).strip() if signature_match else ""

    # Create message
    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = "security.test@company.local"
    msg["To"] = target_email

    # Combine body and signature
    full_body = f"{body}\n\n{signature}"
    msg.attach(MIMEText(full_body, "plain"))

    try:
        with smtplib.SMTP(MAILHOG_HOST, MAILHOG_PORT) as server:
            server.send_message(msg)
        return True
    except Exception as e:
        st.error(f"Failed to send email: {e}")
        return False


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

    if file_path.lower().endswith(".pdf"):
        try:
            doc = fitz.open(file_path)
            text = ""
            for page in doc:
                text += page.get_text()
            return text
        except Exception as e:
            st.error(f"Error processing PDF: {e}")
            return ""
    elif file_path.lower().endswith(".txt"):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            st.error(f"Error processing text file: {e}")
            return ""
    return ""


def clean_response(response):
    cleaned = re.sub(r"<think>.*?</think>", "", response, flags=re.DOTALL)
    cleaned = re.sub(r"Here\'s.*?:", "", cleaned, flags=re.DOTALL)
    cleaned = re.sub(r"I will.*?:", "", cleaned, flags=re.DOTALL)
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
    # Check if Ollama is available before trying to use it
    if OLLAMA_AVAILABLE:
        formatted_prompt = PHISHING_PROMPT_TEMPLATE.format(
            document_text=document_text,
            target_org=scenario_details["target_org"],
            scenario_type=scenario_details["scenario_type"],
            target_dept=scenario_details["target_dept"],
        )

        try:
            response = ollama.chat(
                model="deepseek-r1:1.5b",  # Changed to the correct model
                # model="gemma3:latest",
                messages=[{"role": "user", "content": formatted_prompt}],
            )
            return clean_response(response["message"]["content"])
        except Exception as e:
            st.warning(f"AI model error: {e}")
    
    # Fallback templates for cloud deployment
        # Enhanced fallback response when Ollama is not available
        st.info("🤖 AI Model unavailable - Using realistic demo templates")
        
        # Different templates based on scenario type
        scenario_templates = {
            "IT System Update": {
                "subject": f"🔒 Critical Security Update Required - {scenario_details['target_org']}",
                "content": f"""Dear {scenario_details['target_dept']} Team Member,

We have identified critical security vulnerabilities affecting {scenario_details['target_org']}'s network infrastructure that require immediate attention.

**URGENT ACTION REQUIRED:**
Due to recent cybersecurity threats targeting organizations in our sector, we must implement emergency security patches across all systems.

To maintain your access and protect sensitive data:
• Verify your credentials immediately using the secure link below
• Complete the security assessment within 24 hours
• Update your authentication preferences

**[SECURE VERIFICATION PORTAL - CLICK HERE]**

Failure to complete this process may result in temporary account restrictions.

Best regards,
{scenario_details['target_org']} IT Security Team
security-updates@{scenario_details['target_org'].lower().replace(' ', '')}.com"""
            },
            "Account Suspension": {
                "subject": f"⚠️ Account Security Alert - Immediate Action Required",
                "content": f"""SECURITY NOTIFICATION: {scenario_details['target_org']}

Dear {scenario_details['target_dept']} Employee,

We have detected suspicious login attempts on your account from an unrecognized device.

ACCOUNT STATUS: ⚠️ TEMPORARILY RESTRICTED

To restore full access:
1. Verify your identity using our secure portal
2. Review and approve recent login activity
3. Update your security settings

**[RESTORE ACCESS - SECURE LOGIN]**

This is an automated security measure to protect your account and {scenario_details['target_org']}'s data.

{scenario_details['target_org']} Security Operations Center
Account Security Team"""
            },
            "Password Expiry": {
                "subject": f"🔑 Password Expires Today - Update Required",
                "content": f"""Password Expiration Notice - {scenario_details['target_org']}

Hello {scenario_details['target_dept']} Team,

Your network password will expire in 4 hours. To prevent service interruption:

EXPIRATION TIME: Today at 11:59 PM
SYSTEMS AFFECTED: Email, Network Drive, VPN Access

**IMMEDIATE STEPS:**
→ Click the secure password reset link below
→ Create a strong new password
→ Verify access to all systems

**[UPDATE PASSWORD NOW - SECURE PORTAL]**

Questions? Contact IT Support: helpdesk@{scenario_details['target_org'].lower().replace(' ', '')}.com

{scenario_details['target_org']} IT Department"""
            }
        }
        
        # Get template or use default
        template = scenario_templates.get(
            scenario_details['scenario_type'], 
            scenario_templates["IT System Update"]
        )
        
        return f"""SUBJECT: {template['subject']}

EMAIL:
{template['content']}

SIGNATURE:
---
This is a simulated phishing email for security training purposes.
Generated in demo mode - AI service unavailable.
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""


def save_scenario(scenario_details):
    try:
        if os.path.exists(SCENARIOS_FILE):
            with open(SCENARIOS_FILE, "r") as f:
                scenarios = json.load(f)
        else:
            scenarios = []

        scenario_details["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        scenarios.append(scenario_details)

        with open(SCENARIOS_FILE, "w") as f:
            json.dump(scenarios, f, indent=4)
    except Exception as e:
        st.error(f"Error saving scenario: {e}")


def main():
    if "initialized" not in st.session_state:
        st.session_state.initialized = True
        clear_uploaded_files()

    st.title("Security Awareness Email Generator")

    with st.sidebar:
        st.header("Organization Context")
        uploaded_file = st.file_uploader(
            "Upload Organization Documents", type=["pdf", "txt"]
        )
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
                    "Custom",
                ],
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
                        "target_dept": target_dept,
                    }

                    generated_email = generate_phishing_email(
                        document_text, scenario_details
                    )
                    st.markdown("### Generated Security Awareness Email")
                    st.markdown(generated_email, unsafe_allow_html=True)
                    save_scenario(scenario_details)
                    st.success("Email generated and saved to history!")

    with tab2:
        st.header("Generated Email History")
        if os.path.exists(SCENARIOS_FILE):
            with open(SCENARIOS_FILE, "r") as f:
                scenarios = json.load(f)
                for scenario in reversed(scenarios):
                    with st.expander(
                        f"📧 {scenario['target_org']} - {scenario['created_at']}"
                    ):
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
    try:
        main()
    except Exception as e:
        st.error(f"Application startup error: {e}")
        st.info("Please refresh the page or check the deployment logs.")
        st.stop()
