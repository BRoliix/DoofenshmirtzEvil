import ollama
import re


class DeepSeekWrapper:
    def __init__(self):
        pass

    def generate_email(self, email_type, company_name ):
        prompt = f"Generate a convincing {email_type} amazon clone of an ad email template in html code for {company_name}.  Dont mention its clone. Dont place any images and dont mention user name and generate and place any needed names and product details shown i dont want placeholder variables"
        
        response = ollama.generate(model="deepseek-r1:1.5b", prompt=prompt)
        print(response['response']) 
        cleaned_content = re.sub(r'<think>.*?</think>', '', response['response'],  flags=re.DOTALL )

        return cleaned_content
        