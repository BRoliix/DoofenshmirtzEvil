import ollama
import re

class DeepSeekWrapper:
    def __init__(self):
        pass
    
    #function to generate_email using deepseek module , prompting involves email , comapany_name
    def generate_email(self, email_type, company_name):
        prompt = (f"Generate a convincing {email_type} Amazon clone of an ad email template in HTML code for {company_name}. "
                  "Don't mention it's a clone. Don't place any images and don't mention the user name. "
                  "Generate and place any needed names and product details; I don't want placeholder variables.")
        
        response = ollama.generate(model="deepseek-r1:1.5b", prompt=prompt)
        
        # Extracting only the HTML part from the generated response, ignoring any other HTML tags
        match = re.search(r'<html.*?</html>', response['response'], re.DOTALL | re.IGNORECASE)
        cleaned_content = match.group(0) if match else ""
        
        return cleaned_content