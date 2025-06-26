from flask import Flask, request, jsonify
import openai, json, os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# เช็กว่า API ยังทำงาน
@app.route("/", methods=["GET"])
def home():
    return "✅ API is live. Use POST /analyze to analyze a photo.", 200

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()

    # รับค่าจาก frontend
    photo_data = data.get("photo_data")
    user_id = data.get("user_id")
    filename = data.get("filename")
    date = data.get("date")                  # 📌 เพิ่ม date
    meal = data.get("meal")                  # 📌 เพิ่ม meal
    content_type = data.get("content_type", "image/jpeg")

    if not (photo_data and date and meal):
        return jsonify({"error": "Missing required fields"}), 400

    # ลบ prefix base64 เช่น "data:image/jpeg;base64,"
    if photo_data.startswith("data:image"):
        base64_img = photo_data.split(",")[1]
    else:
        base64_img = photo_data

    # 🧠 Prompt format สำหรับ GPT-4o
    system_prompt = (
        "You are a professional nutritionist AI. "
        "Given a food image, estimate total calories and provide ingredient breakdown. "
        "Respond ONLY in this exact JSON format:\n"
        '{\n'
        '  "total_calories": number,\n'
        '  "ingredients_estimated": [ {"name": "ingredient", "calories": number} ]\n'
        '}\n'
        "No explanation. Only JSON."
    )

    try:
        # เรียก GPT-4o
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Please analyze this meal."},
                        {"type": "image_url", "image_url": {
                            "url": f"data:{content_type};base64,{base64_img}"
                        }}
                    ]
                }
            ]
        )

        # แปลงผลลัพธ์ที่ GPT พ่นกลับมา
        result_text = response.choices[0].message.content
        gpt_result = json.loads(result_text)

        return jsonify({
            "date": date,
            "meal": meal,
            "total_calories": gpt_result["total_calories"],
            "ingredients_estimated": gpt_result["ingredients_estimated"]
        })

    except Exception as e:
        return jsonify({
            "error": "Failed to analyze image",
            "detail": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)