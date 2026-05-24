from flask import Flask, request, render_template_string
import hashlib
import time
import random

app = Flask(__name__)

# Simple in-memory database simulation
users_db = {
    "user@example.com": {"id": 1, "password": "oldpassword123"},
    "admin@test.com": {"id": 2, "password": "admin123"}
}

tokens_db = {}  # Store tokens: {token: {"user_id": id, "email": email}}

# HTML template for the forgot password page
FORGOT_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Vulnerable Password Reset</title>
    <style>
        body { font-family: Arial; max-width: 500px; margin: 50px auto; padding: 20px; }
        input { width: 100%; padding: 10px; margin: 10px 0; }
        button { background: #007bff; color: white; padding: 10px 20px; border: none; cursor: pointer; }
        .message { padding: 10px; margin: 10px 0; background: #d4edda; border: 1px solid #c3e6cb; }
        .error { background: #f8d7da; border: 1px solid #f5c6cb; }
    </style>
</head>
<body>
    <h2>Vulnerable Password Reset Demo</h2>
    <form method="POST" action="/forgot">
        <label>Enter your email:</label>
        <input type="email" name="email" required placeholder="user@example.com">
        <button type="submit">Request Password Reset</button>
    </form>
    {% if message %}
        <div class="message {{ 'error' if error else '' }}">{{ message }}</div>
    {% endif %}
    <hr>
    <p><strong>Test Accounts:</strong></p>
    <ul>
        <li>user@example.com</li>
        <li>admin@test.com</li>
    </ul>
    <p><strong>Lab URL:</strong> http://127.0.0.1:3000</p>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(FORGOT_PAGE)

@app.route("/forgot", methods=["POST"])
def forgot():
    email = request.form["email"]
    
    # VULNERABILITY 1: User Enumeration
    if email not in users_db:
        return render_template_string(FORGOT_PAGE, message="No such user", error=True)
    
    user = users_db[email]
    
    # VULNERABILITY 2: Weak Token Generation (Predictable)
    token = hashlib.md5(
        (email + str(int(time.time()))).encode()
    ).hexdigest()
    
    # VULNERABILITY 3: No Token Expiration
    tokens_db[token] = {
        "user_id": user["id"],
        "email": email,
        "expires": None  # Never expires!
    }
    
    # VULNERABILITY 4: Host Header Injection
    link = f"http://{request.host}/reset?token={token}"
    
    # Simulate sending email (just print it)
    print(f"\n[EMAIL SENT TO {email}]")
    print(f"Reset Link: {link}")
    print(f"Token: {token}\n")
    
    return render_template_string(
        FORGOT_PAGE, 
        message=f"Reset link sent! (Check terminal for the link)"
    )

@app.route("/reset")
def reset():
    token = request.args.get("token")
    if token in tokens_db:
        user_data = tokens_db[token]
        return f"""
        <h2>Reset Password</h2>
        <p>Token valid for: {user_data['email']}</p>
        <form method="POST" action="/do_reset">
            <input type="hidden" name="token" value="{token}">
            <input type="password" name="new_password" placeholder="New Password" required>
            <button type="submit">Reset Password</button>
        </form>
        """
    return "Invalid or expired token", 403

if __name__ == "__main__":
    print("=" * 60)
    print("VULNERABLE PASSWORD RESET LAB")
    print("=" * 60)
    print("Starting server at: http://127.0.0.1:3000")
    print("Press CTRL+C to stop")
    print("=" * 60)
    app.run(debug=True, host="0.0.0.0", port=3000)


