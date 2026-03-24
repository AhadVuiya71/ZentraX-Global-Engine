from flask import Flask, render_template_string, request, send_file, session
import requests, io, os
from PIL import Image

app = Flask(__name__)
app.secret_key = "ZentraX_Global_Ahad_2026"

# তোমার টোকেন এবং সঠিক ইউআরএল
AUTH_TOKEN = "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"
AI_MODEL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"

HTML_UI = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ZentraX Global Engine</title>
    <style>
        body { background: #000; color: #00ff99; font-family: monospace; text-align: center; padding: 20px; }
        .box { border: 1px solid #00ff99; padding: 20px; border-radius: 10px; background: #011a11; max-width: 500px; margin: auto; }
        textarea { width: 90%; background: #000; color: #fff; border: 1px solid #00ff99; padding: 10px; margin-top: 10px; }
        .btn { background: #00ff99; color: #000; padding: 15px; width: 95%; border: none; font-weight: bold; margin-top: 15px; cursor: pointer; }
        img { width: 100%; border: 2px solid #00ff99; margin-top: 20px; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="box">
        <h2>⚡ ZENTRAX GLOBAL</h2>
        {% if not session.get('auth') %}
            <form method="POST" action="/login">
                <input type="password" name="key" placeholder="Enter Master Key" style="padding:10px; width:80%;">
                <button type="submit" class="btn">UNLOCK SYSTEM</button>
            </form>
        {% else %}
            <p style="color: #fff;">ACCESS GRANTED: AHAD</p>
            <form method="POST" action="/generate">
                <textarea name="prompt" rows="3" placeholder="Describe your creative design..."></textarea>
                <button type="submit" class="btn">EXECUTE GENERATION</button>
            </form>
            {% if msg %}<p style="color: yellow;">> {{ msg }}</p>{% endif %}
            {% if img %}<img src="/view">{% endif %}
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

@app.route('/generate', methods=['POST'])
def generate():
    if not session.get('auth'): return "Unauthorized"
    prompt = request.form.get('prompt')
    headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
    try:
        res = requests.post(AI_MODEL, headers=headers, json={"inputs": prompt}, timeout=60)
        if res.status_code == 200:
            Image.open(io.BytesIO(res.content)).save("out.png")
            return render_template_string(HTML_UI, img=True, msg="Design Ready!")
        return render_template_string(HTML_UI, msg=f"Error {res.status_code}: Server Busy")
    except Exception:
        return render_template_string(HTML_UI, msg="Connection Error")

@app.route('/view')
def view(): return send_file("out.png", mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)