import os
import google.generativeai as genai
from flask import Flask, request, render_template_string

app = Flask(__name__)
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

HTML = '''
<!DOCTYPE html>
<html>
<head><title>Text Summarizer</title></head>
<body style="font-family: Arial; max-width: 600px; margin: 50px auto; padding: 20px;">
    <h2>AI Text Summarizer</h2>
    <form method="post">
        <textarea name="text" rows="8" style="width: 100%;" placeholder="Paste your long text here..." required></textarea>
        <br><br>
        <button type="submit" style="padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer;">Summarize</button>
    </form>
    {% if summary %}
        <h3>Summary:</h3>
        <p style="background: #f4f4f4; padding: 15px; border-radius: 5px;">{{ summary }}</p>
    {% endif %}
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    summary = None
    if request.method == 'POST':
        user_text = request.form.get('text')
        response = model.generate_content(f"Summarize this text in simple words:\n{user_text}")
        summary = response.text
    return render_template_string(HTML, summary=summary)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
