import os
import google.generativeai as genai
from flask import Flask, request, render_template_string

app = Flask(__name__)

# Konfigurazzjoni tal-API Key
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# Użu tal-mudell stabbli gemini-1.5-flash
model = genai.GenerativeModel('gemini-1.5-flash')

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>AI Text Summarizer</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }
        textarea { width: 100%; height: 150px; padding: 10px; box-sizing: border-box; }
        button { background-color: #007bff; color: white; padding: 10px 15px; border: none; border-radius: 4px; cursor: pointer; }
        .result { background: #f4f4f4; padding: 15px; border-radius: 5px; margin-top: 20px; }
    </style>
</head>
<body>
    <h2>AI Text Summarizer</h2>
    <form method="post">
        <textarea name="text" placeholder="Ikteb jew waħħal it-test hawn..." required></textarea>
        <br><br>
        <button type="submit">Iġbor it-Test (Summarize)</button>
    </form>
    {% if summary %}
        <div class="result">
            <h3>Riżultat:</h3>
            <p>{{ summary }}</p>
        </div>
    {% endif %}
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    summary = None
    if request.method == 'POST':
        try:
            user_text = request.form.get('text')
            response = model.generate_content(f"Summarize this text: {user_text}")
            summary = response.text
        except Exception as e:
            summary = f"Iżball: {str(e)}"
    return render_template_string(HTML, summary=summary)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
