from flask import Flask, request, jsonify
import random

app = Flask(__name__)

# Simple user database
users_db = {
    "victim@example.com": {"id": 1, "password": "secret123"}
}

# Store OTPs: {email: otp_code}
otps_db = {}

@app.route("/")
def home():
    """Home page with instructions"""
    return """
    <h2>OTP Verification System (Vulnerable)</h2>
    <h3>Available Endpoints:</h3>
    <ul>
        <li><b>POST /request-otp</b> - Request a 6-digit OTP</li>
        <li><b>POST /verify-otp</b> - Verify OTP (NO RATE LIMIT - VULNERABLE!)</li>
    </ul>
    
    <h3>Test it:</h3>
    <p>1. First request an OTP:</p>
    <code>curl -X POST http://127.0.0.1:5001/request-otp -H "Content-Type: application/json" -d '{"email": "victim@example.com"}'</code>
    
    <p>2. Check your terminal for the OTP</p>
    
    <p>3. Run the brute-force script</p>
    
    <p><b>Status:</b> Server is running. Check terminal for OTPs.</p>
    """

@app.route("/request-otp", methods=["POST"])
def request_otp():
    """Request a 6-digit OTP for password reset"""
    try:
        # Handle both JSON and form data
        if request.is_json:
            email = request.json.get("email")
        else:
            email = request.form.get("email")
        
        if not email:
            return jsonify({"error": "Email required"}), 400
            
        if email not in users_db:
            return jsonify({"error": "User not found"}), 404
        
        # Generate 6-digit OTP
        otp = str(random.randint(0, 99)).zfill(6)
        otps_db[email] = otp
        
        print(f"\n{'='*50}")
        print(f"[OTP GENERATED]")
        print(f"Email: {email}")
        print(f"OTP: {otp}")
        print(f"{'='*50}\n")
        
        return jsonify({
            "success": True,
            "message": "OTP sent to your email",
            "email": email
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/verify-otp", methods=["POST"])
def verify_otp():
    """
    Verify the OTP - VULNERABLE: NO RATE LIMITING!
    """
    try:
        # Handle both JSON and form data
        if request.is_json:
            email = request.json.get("email")
            otp = request.json.get("otp")
        else:
            email = request.form.get("email")
            otp = request.form.get("otp")
        
        if not email or not otp:
            return jsonify({
                "success": False,
                "message": "Email and OTP required"
            }), 400
        
        # Check if OTP exists and matches
        if email in otps_db and otps_db[email] == otp:
            return jsonify({
                "success": True,
                "message": "OTP verified! Password reset allowed.",
                "email": email
            }), 200
        else:
            return jsonify({
                "success": False,
                "message": "Invalid OTP"
            }), 401
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("VULNERABLE OTP VERIFICATION ENDPOINT")
    print("=" * 60)
    print("Server running at: http://127.0.0.1:5001")
    print("\nEndpoints:")
    print("  GET  /              - Home page with instructions")
    print("  POST /request-otp   - Request a 6-digit OTP")
    print("  POST /verify-otp    - Verify OTP (NO RATE LIMIT)")
    print("=" * 60 + "\n")
    app.run(debug=True, host="127.0.0.1", port=5001, threaded=True)