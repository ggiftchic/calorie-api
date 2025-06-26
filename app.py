from flask import Flask, request, jsonify

app = Flask(__name__)

# GET: ใช้เช็กว่า API ยังทำงานอยู่
@app.route("/", methods=["GET"])
def home():
    return "✅ API is live. Use POST /analyze to analyze a photo.", 200

# POST: วิเคราะห์ภาพอาหาร (mock response)
@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()

    photo_data = data.get("photo_data")
    user_id = data.get("user_id")
    filename = data.get("filename")

    # สมมุติว่าคุณยังไม่อยากเรียก GPT จริง ก็ใส่ mock response ง่ายๆแบบนี้ก่อน
    return jsonify({
        "user_id": user_id,
        "filename": filename,
        "total_calories": 450,
        "ingredients_estimated": [
            {"name": "ข้าวสวย", "calories": 200},
            {"name": "ไข่เจียว", "calories": 250}
        ]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)