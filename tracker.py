from flask import Flask, request, redirect
import base64 as b64
from datetime import datetime
import os
import json

app = Flask(__name__)

PHISHED_LOG_FILE = 'log.json'


@app.route('/<user_id>', methods=['GET'])
def redirect_user(user_id):
    subject = request.args.get('subject', default="Z2VuZXJhbA==", type=str) 
    
    try:
        decoded_user = b64.b64decode(user_id).decode('utf-8')
        decoded_subject = b64.b64decode(subject).decode('utf-8')
    except Exception as e:
        return "Invalid Base64 encoding", 400  

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    tracking_object = {
        'user': decoded_user,
        'subject': decoded_subject,
        'timestamp': timestamp
    }

    print(tracking_object) 

    try:
        if os.path.exists(PHISHED_LOG_FILE):
            with open( PHISHED_LOG_FILE, 'r') as f:
                log = json.load(f)
        else:
            log = []
        
        log.append(tracking_object)
        
        with open(PHISHED_LOG_FILE, 'w') as f:
            json.dump(log, f, indent=4)
    except Exception as e:
        print(e)
    
    return redirect("https://www.amazon.com", code=302)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999, debug=True)

