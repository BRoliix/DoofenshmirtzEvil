from flask import Flask, request, redirect
import base64 as b64

app = Flask(__name__)

@app.route('/api/<user_id>', methods=['GET'])
def redirect_user(user_id):


    subject = request.args.get('subject', default="general", type=str)
    
    tracking_object = {
        'user' : b64.b64decode(user_id).decode('utf-8'),
        'subject' : b64.b64decode(subject).decode('utf-8')
    }
    # Define the target URL format (modify as needed)
    target_url = f"https://example.com/profile/{user_id}?subject={subject}"
    
    return redirect(target_url, code=302)  # 302 Found (Temporary Redirect)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

