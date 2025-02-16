import streamlit as st
from src.deepseek_backend import DeepseekAIBackend

def main():
    st.title("DeepSeek AI Email Generator Test")
    st.write("Enter keywords and optional document context to generate a sample phishing email.")


# Input fields
    keywords = st.text_input("Keywords (comma separated):", "")
    document = st.text_area("Document context (optional):", height=200)

    if st.button("Generate Email"):
        if not keywords.strip():
            st.error("Please provide at least some keywords.")
        else:
            ai_backend = DeepseekAIBackend()  # create instance of the backend
            with st.spinner("Generating email..."):
                generated_email = ai_backend.generate_email(keywords, document)
            st.subheader("Generated Email")
            st.text_area("Email Content", generated_email, height=300)
    if __name__ == "main":
        main()

main()