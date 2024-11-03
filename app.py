from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

# OpenAI API 密鑰從環境變數中取得
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["GET", "POST"])
def index():
    response_text = ""
    if request.method == "POST":
        user_input = request.form["user_input"]

        # 設定 OpenAI API 請求
        api_url = "https://api.openai.com/v1/completions"
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }


    # Prepare API request payload
    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.4,
        "max_tokens": 1000
    }



        try:
            response = requests.post(api_url, headers=headers, json=data)
            response.raise_for_status()
            response_text = response.json()["choices"][0]["text"].strip()
        except Exception as e:
            response_text = "Hello world"
            #response_text = f"出現錯誤：{str(e)}"

    return render_template("index.html", response_text=response_text)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)