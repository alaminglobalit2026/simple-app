import os
import google.generativeai as genai
from flask import Flask, request, render_template_string

app = Flask(__name__)

# Configure API Key
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# Updated Supported Model
model = genai.GenerativeModel('gemini-3.8-flash')

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>AI Text Summarizer</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 650px; margin: 40px auto; padding: 20px; line-height: 1.6; }
        .student-info { background: #eef2ff; border: 1px solid #c7d2fe; padding: 12px 20px; border-radius: 8px; margin-bottom: 25px; }
        .student-info h3 { margin: 0 0 5px 0; color: #3730a3; font-size: 18px; }
        .student-info p { margin: 0; color: #4338ca; font-weight: bold; font-size: 15px; }
        textarea { width: 100%; height: 150px; padding: 10px; box-sizing: border-box; border-radius: 6px; border: 1px solid #ccc; font-size: 14px; }
        button { background-color: #2563eb; color: white; padding: 12px 20px; border: none; border-radius: 6px; cursor: pointer; font-size: 15px; font-weight: bold; width: 100%; }
        button:hover { background-color: #1d4ed8; }
        .result { background: #f8fafc; border: 1px solid #e2e8f0; padding: 20px; border-radius: 8px; margin-top: 25px; }
        .error { background: #fef2f2; border: 1px solid #fecaca; color: #dc2626; padding: 15px; border-radius: 8px; margin-top: 25px; }
    </style>
</head>
<body>
    <div class="student-info">
        <h3>Assignment Submission</h3>
        <p>Student Name: AL AMIN</p>
        <p>Student ID: 2026512806</p>
    </div>

    <h2>AI Text Summarizer Application</h2>
    <form method="post">
        <textarea name="text" placeholder="Write or paste your text here..." required></textarea>
        <br><br>
        <button type="submit">Summarize Text</button>
    </form>

    {% if summary %}
        <div class="result">
            <h3 style="margin-top:0;">Summary Result:</h3>
            <p>{{ summary }}</p>
        </div>
    {% endif %}

    {% if error %}
        <div class="error">
            <h3 style="margin-top:0;">Error Details:</h3>
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
