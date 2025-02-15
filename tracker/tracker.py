from flask import Flask, request, redirect, jsonify
import datetime

app = Flask(__name__)

# In-memory list to store click events
clicks = []

@app.route('/track')
def track_click():
    # Get the email from the query string and the user agent from headers
    email = request.args.get('email', 'unknown')
    user_agent = request.headers.get('User-Agent', 'unknown')
    timestamp = datetime.datetime.utcnow().isoformat()
    
    # Record the click event
    click_event = {
        "email": email,
        "user_agent": user_agent,
        "timestamp": timestamp
    }
    clicks.append(click_event)
    
    # Redirect user to a thank-you or landing page
    return redirect("http://amazon.com")

@app.route('/stats')
def stats():
    # Return the recorded click events as JSON
    return jsonify(clicks)

if __name__ == '__main__':
    app.run(port=5000)
