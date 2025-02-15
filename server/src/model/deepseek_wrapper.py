import ollama
import re


class DeepSeekWrapper:
    def __init__(self):
        pass

    def generate_email(self, email_type, company_name ):
        prompt = f"Generate a convincing {email_type} email template in html code for {company_name} phishing awareness training. Dont mention that it is a physhon awarenss mail in the emiail it self but show it once they click on click here"
        
        response = ollama.generate(model="deepseek-r1:1.5b", prompt=prompt)
        print(response['response']) #TODO clean response
        cleaned_content = re.sub(r'<think>.*?</think>', '', response['response'],  flags=re.DOTALL )

        return cleaned_content
        