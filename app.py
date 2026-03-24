from flask import Flask, render_template_string, request, send_file, session
import requests
import io
from PIL import Image

app = Flask(__name__)
app.secret_key = "Ahad_ZentraX_Secure_2026"

# তোমার টোকেন এবং সঠিক ইউআরএল
AUTH_TOKEN = "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"
# সরাসরি মডেল ইউআরএল ব্যবহার করছি এরর এড়াতে
AI_MODEL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"

HTML_FIXED_UI = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ZentraX Master</title>
    <style>
        body { background: #000; color: #00ff99; font-family: monospace; text-align: center; padding: 20px; }
        .box { border: 1px solid #00ff99; padding: 20px; border-radius: 10px; background: #011a11; }
        textarea { width: 90%; background: #000; color: #fff; border: 1px solid #00ff99; padding: 10px; }
        .btn { background: #00ff99; color: #000; padding: 15px; width: 95%; border: none; font-weight: bold; margin-top: 10px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="box">
        <h2>⚡ ZENTRAX MASTER CONTROL</h2>
        {% if not session.get('auth') %}
            <form method="POST" action="/login">
                <input type="password" name="key" placeholder="Passcode" style="padding:10px; width:80%;">
                <button type="submit" class="btn">UNLOCK</button>
            </form>
        {% else %}
            <p>ACCESS: AUTHORIZED</p>
            <form method="POST" action="/generate">
                <textarea name="prompt" rows="3" placeholder="Enter design details..."></textarea>
                <button type="submit" class="btn">GENERATE DESIGN</button>
            </form>
            {% if msg %}<p style="font-size:12px; color:yellow;">> {{ msg }}</p>{% endif %}
            {% if img %}
                <img src="/view" style="width:100%; margin-top:15px; border:1px solid #fff;">
            {% endif %}
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/')
def home(): return render_template_string(HTML_FIXED_UI)

@app.route('/login', methods=['POST'])
def login():
    if request.form.get('key') == "Admin123": # তোমার পাসকোড
        session['auth'] = True
    return render_template_string(HTML_FIXED_UI)

@app.route('/generate', methods=['POST'])
def generate():
    if not session.get('auth'): return "Unauthorized"
    prompt = request.form.get('prompt')
    headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
    try:
        # রিকোয়েস্ট পাঠানোর সঠিক নিয়ম
        res = requests.post(AI_MODEL, headers=headers, json={"inputs": prompt}, timeout=60)
        
        if res.status_code == 200:
            Image.open(io.BytesIO(res.content)).save("ahad_final.png")
            return render_template_string(HTML_FIXED_UI, img=True, msg="Design generated successfully!")
        elif res.status_code == 503:
            return render_template_string(HTML_FIXED_UI, msg="Model is loading. Please wait 30 seconds.")
        else:
            return render_template_string(HTML_FIXED_UI, msg=f"Error {res.status_code}: API Endpoint issue.")
    except Exception as e:
        return render_template_string(HTML_FIXED_UI, msg=f"Connection Error: {str(e)}")

@app.route('/view')
def view(): return send_file("ahad_final.png", mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)