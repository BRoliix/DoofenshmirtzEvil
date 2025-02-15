
# main.py
from src.model.deepseek_wrapper import DeepSeekWrapper
from src.email.sender import EmailSender
from src.config import SMTP_CONFIG


from flask import Flask, request, abort, Response
import os

app = Flask(__name__)
TEMPLATES_DIR = 'templates'


@app.route('/generate/<company_name>')
def generate_response(company_name):
    # Look for template file
    template_path = os.path.join(TEMPLATES_DIR, f"{company_name}.html")
    
    if not os.path.exists(template_path):
        abort(404, description="Company template not found")
    
    # Read template content
    with open(template_path, 'r') as f:
        template_content = f.read()
    
    # Generate response
    generated = DeepSeekWrapper().generate_email(email_type=template_content, company_name=company_name)
    
    # Determine response format
    response_format = request.args.get('format', 'html')
    
    # Create appropriate response
    if response_format.lower() == 'text':
        return Response(generated, content_type='text/plain')
    else:
        return Response(generated, content_type='text/html')

if __name__ == '__main__':
    # Create templates directory if not exists
    os.makedirs(TEMPLATES_DIR, exist_ok=True)
    app.run(host='0.0.0.0', port=7777, debug=True)

