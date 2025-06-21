import os
from openai import OpenAI
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app, origins=["https://ai-agent-app-1.onrender.com"])

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# FAQ データをファイルから読み込み
with open("faq_data.txt", encoding="utf-8") as f:
    faq_data = f.read()

@app.route("/inquiry", methods=["POST"])
def inquiry():
    user_message = request.json.get("message", "")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"あなたはカスタマーサポート担当者です。以下のFAQを参考に正確に回答してください。\n\n{faq_data}"},
                {"role": "user", "content": user_message}
            ]
        )
        answer = response.choices[0].message.content
        return jsonify({"answer": answer}), 200, {'Content-Type': 'application/json; charset=utf-8'}
    except Exception as e:
        app.logger.error(f"Error during OpenAI API call: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
