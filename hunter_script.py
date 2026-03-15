import requests
import json
import base64
import os

# الإعدادات: يستخدم المفتاح السري الذي أضفته في إعدادات GitHub
TOKEN = os.getenv("MY_GITHUB_TOKEN") 
REPO = "boxtvhd200-design/iptv-hunter"
FILE_PATH = "iptv_data.json"

def get_hunted_servers():
    # هنا نضع السيرفرات الجديدة (يمكنك تعديلها لاحقاً لجلبها آلياً)
    return [
        {
            "id": 1,
            "name": "Cloud Auto Server 01",
            "url": "http://p1.iptvprivateserver.tv",
            "mac": "00:1A:79:31:14:CA",
            "status": "active"
        }
    ]

def update_github_file(new_data):
    url = f"https://api.github.com/repos/{REPO}/contents/{FILE_PATH}"
    headers = {"Authorization": f"token {TOKEN}", "Accept": "application/vnd.github.v3+json"}
    
    # الحصول على SHA الملف الحالي لتحديثه
    res = requests.get(url, headers=headers)
    sha = res.json().get('sha') if res.status_code == 200 else None

    # تشفير البيانات بصيغة Base64 المطلوبة من GitHub
    content_b64 = base64.b64encode(json.dumps(new_data, indent=2).encode()).decode()
    
    payload = {
        "message": "تحديث آلي للسيرفرات 🎯",
        "content": content_b64,
        "sha": sha
    }

    requests.put(url, json=payload, headers=headers)

if __name__ == "__main__":
    if TOKEN:
        data = get_hunted_servers()
        update_github_file(data)
        print("✅ تم التحديث بنجاح!")
