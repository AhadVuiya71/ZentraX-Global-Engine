from flask import Flask, render_template_string, request, send_file, session
import requests, io, os, subprocess
from PIL import Image

app = Flask(__name__)
app.secret_key = "ZentraX_Secure_Vault_2026"

AUTH_TOKEN = "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"
AI_MODEL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"

HTML_UI = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ZentraX Global Engine</title>
    <style>
        body { background: #000; color: #00ff99; font-family: monospace; text-align: center; padding: 15px; }
        .box { border: 1px solid #00ff99; padding: 20px; border-radius: 10px; background: #011a11; max-width: 600px; margin: auto; }
        textarea { width: 90%; background: #000; color: #fff; border: 1px solid #00ff99; padding: 10px; margin-top: 10px; }
        .btn { background: #00ff99; color: #000; padding: 12px; width: 95%; border: none; font-weight: bold; margin-top: 10px; cursor: pointer; }
        .file-list { text-align: left; background: #000; padding: 10px; margin-top: 15px; border: 1px dashed #00ff99; font-size: 12px; overflow-x: auto; }
        img { width: 100%; border: 1px solid #00ff99; margin-top: 15px; }
        h3 { color: #fff; margin-bottom: 5px; }
    </style>
</head>
<body>
    <div class="box">
        <h2>⚡ ZENTRAX SYSTEM CONTROL</h2>
        {% if not session.get('auth') %}
            <form method="POST" action="/login">
                <input type="password" name="key" placeholder="Enter Master Key" style="padding:10px; width:80%;">
                <button type="submit" class="btn">UNLOCK SYSTEM</button>
            </form>
        {% else %}
            <p style="color: yellow;">ACCESS: AUTHORIZED ✅</p>
            
            <h3>🎨 AI DESIGN ENGINE</h3>
            <form method="POST" action="/generate">
                <textarea name="prompt" rows="2" placeholder="Describe design..."></textarea>
                <button type="submit" class="btn">EXECUTE GENERATION</button>
            </form>

            <hr style="border: 0.5px solid #333; margin: 20px 0;">

            <h3>📁 FILE SYSTEM ACCESS</h3>
            <form method="POST" action="/list_files">
                <input type="text" name="path" value="." style="width:70%; background:#000; color:#00ff99; border:1px solid #00ff99; padding:5px;">
                <button type="submit" style="background:orange; color:#000; padding:5px; font-weight:bold;">EXPLORE</button>
            </form>

            {% if files %}
            <div class="file-list">
                <strong>Current Path: {{ current_path }}</strong><br>
                {% for file in files %}
                    > {{ file }}<br>
                {% endfor %}
            </div>
            {% endif %}

            {% if msg %}<p style="color: cyan;">> {{ msg }}</p>{% endif %}
            {% if img %}<img src="/view">{% endif %}
            
            <a href="/logout" style="color:red; display:block; margin-top:20px;">[ LOGOUT SYSTEM ]</a>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/')
def home(): return render_template_string(HTML_UI)

@app.route('/login', methods=['POST'])
def login():
    if request.form.get('key') == "Admin123": session['auth'] = True
    return render_template_string(HTML_UI)

@app.route('/logout')
def logout():
    session.clear()
    return render_template_string(HTML_UI, msg="System Locked.")

@app.route('/generate', methods=['POST'])
def generate():
    if not session.get('auth'): return "Unauthorized"
    prompt = request.form.get('prompt')
    headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
    try:
        res = requests.post(AI_MODEL, headers=headers, json={"inputs": prompt}, timeout=60)
        if res.status_code == 200:
            Image.open(io.BytesIO(res.content)).save("out.png")
            return render_template_string(HTML_UI, img=True, msg="Design success!")
        return render_template_string(HTML_UI, msg="Server Busy")
    except: return render_template_string(HTML_UI, msg="Connection Error")

@app.route('/list_files', methods=['POST'])
def list_files():
    if not session.get('auth'): return "Unauthorized"
    path = request.form.get('path')
    try:
        files = os.listdir(path) # ফোনের ফাইল রিড করার কমান্ড
        return render_template_string(HTML_UI, files=files, current_path=path)
    except Exception as e:
        return render_template_string(HTML_UI, msg=f"Error: {str(e)}")

@app.route('/view')
def view(): return send_file("out.png", mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
