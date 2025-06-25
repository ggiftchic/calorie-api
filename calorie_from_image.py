import openai
import base64
import json
import os
from dotenv import load_dotenv

# โหลด environment variables จาก .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def estimate_calorie_from_image(image_path):
    # อ่านภาพและ encode เป็น base64
    with open(image_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()

    # สร้าง prompt เพื่อให้ตอบกลับมาเป็น JSON เท่านั้น
    system_prompt = (
        "You are a professional nutritionist AI. "
        "Given a food image, break down the meal into its main ingredients and estimate calories per item. "
        "Then return ONLY the JSON object, without any explanation or extra text. Strictly follow this format:\n\n"
        '{\n'
        '  "total_calories": number,\n'
        '  "ingredients_estimated": [\n'
        '    {"name": "ingredient", "calories": number}\n'
        '  ]\n'
        '}\n\n'
        "Respond with only raw JSON. Do not use markdown, do not include code fences, and do not add text before or after the JSON."
    )

    # เรียกใช้ GPT-4o
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            { "role": "system", "content": system_prompt },
            {
                "role": "user",
                "content": [
                    { "type": "text", "text": "Please analyze this food photo and break down calories." },
                    { "type": "image_url", "image_url": { "url": f"data:image/jpeg;base64,{encoded}" } }
                ]
            }
        ]
    )

    result_text = response.choices[0].message['content']
    
    # Debug: print raw output ที่ GPT พ่นกลับมา
    print("🔎 RAW GPT OUTPUT:\n", result_text)

    # พยายามแปลงเป็น JSON
    try:
        result = json.loads(result_text)
    except Exception:
        result = {"error": "Invalid format returned"}
    return result

# 🏃‍♀️ จุดเริ่มต้นของการทำงาน
if __name__ == "__main__":
    image_path = "chickenrice.jpg"  # แก้ชื่อไฟล์รูปตามที่มี
    result = estimate_calorie_from_image(image_path)

    print("\n🧾 ผลลัพธ์:")
    print(json.dumps(result, indent=2, ensure_ascii=False))