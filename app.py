import os
import google.generativeai as genai
from flask import Flask, request, render_template_string

app = Flask(__name__)

# Configure API Key
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# Updated Latest Gemini Model
model = genai.GenerativeModel('gemini-2.5-flash')

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>AI Text Summarizer</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }
        textarea { width: 100%; height: 150px; padding: 10px; box-sizing: border-box; border-radius: 4px; }
        button { background-color: #007bff; color: white; padding: 10px 15px; border: none; border-radius: 4px; cursor: pointer; }
        .result { background: #f4f4f4; padding: 15px; border-radius: 5px; margin-top: 20px; }
        .error { background: #ffe6e6; color: #d8000c; padding: 15px; border-radius: 5px; margin-top: 20px; }
    </style>
</head>
<body>
    <h2>AI Text Summarizer</h2>
    <form method="post">
        <textarea name="text" placeholder="Write or paste your text here..." required></textarea>
        <br><br>
        <button type="submit">Summarize Text</button>
    </form>
    {% if summary %}
        <div class="result">
            <h3>Summary Result:</h3>
            <p>{{ summary }}</p>
        </div>
    {% endif %}
    {% if error %}
        <div class="error">
            <h3>Error Details:</h3>
            <p>{{ error }}</p>
        </div>
    {% endif %}
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    summary = None
    error = None
    if request.method == 'POST':
        if not api_key:
            error = "GEMINI_API_KEY is missing in Render Environment Variables!"
        else:
            try:
                user_text = request.form.get('text')
                response = model.generate_content(f"Summarize this text in simple words:\n{user_text}")
                summary = response.text
            except Exception as e:
                error = f"API Error: {str(e)}"
                
    return render_template_string(HTML, summary=summary, error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
