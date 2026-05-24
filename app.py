from flask import Flask, request, jsonify
import hashlib

app = Flask(__name__)

# Store reset tokens
reset_tokens = {}

# ─────────────────────────────────────────────
# Home Route
# ─────────────────────────────────────────────
@app.route('/')
def home():
    return '''
    <h2>Forgot Password Demo</h2>

    <form method="POST" action="/forgot-password">
        <input type="email" name="email" placeholder="Enter email">
        <button type="submit">Reset Password</button>
    </form>
    '''

# ─────────────────────────────────────────────
# Vulnerable Forgot Password Endpoint
# ─────────────────────────────────────────────
@app.route('/forgot-password', methods=['POST'])
def forgot_password():

    email = request.form.get('email')

    # Create predictable token
    token = hashlib.md5(email.encode()).hexdigest()

    reset_tokens[email] = token

    # Vulnerable Host Header usage
    host = request.headers.get(
        'X-Forwarded-Host',
        request.host
    )

    reset_link = (
        f"http://{host}/reset-password"
        f"?token={token}&email={email}"
    )

    print(f"[DEBUG] Generated reset link: {reset_link}")

    return jsonify({
        "message": "Reset email sent",
        "poisoned_link": reset_link
    })

# ─────────────────────────────────────────────
# Reset Password Route
# ─────────────────────────────────────────────
@app.route('/reset-password')
def reset_password():

    token = request.args.get('token')
    email = request.args.get('email')

    if reset_tokens.get(email) == token:
        return f"Password reset allowed for {email}"

    return "Invalid token", 401

# ─────────────────────────────────────────────
# Run Flask App
# ─────────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=True)