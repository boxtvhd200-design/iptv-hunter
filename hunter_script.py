import requests
from bs4 import BeautifulSoup
import json
import base64
import os

# الإعدادات السحابية (تأكد أن MY_GITHUB_TOKEN مضاف في Secrets)
TOKEN = os.getenv("MY_GITHUB_TOKEN")
REPO = "boxtvhd200-design/iptv-hunter"
FILE_PATH = "iptv_data.json"

def get_headers():
    return {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

def hunt_iptv4sat():
    print("🔎 فحص موقع IPTV4Sat...")
    url = "https://www.iptv4sat.com/category/stb-emu-free/"
    try:
        response = requests.get(url, headers=get_headers(), timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        first_post = soup.find('article')
        title = first_post.find('h2').text.strip()
        return {
            "name": f"IPTV4Sat: {title[:25]}",
            "url": "http://p1.iptvprivateserver.tv", # مثال، يفضل استخراجه يدوياً لاحقاً
            "mac": "00:1A:79:XX:YY:ZZ",
            "source": "IPTV4Sat"
        }
    except:
        return None

def hunt_sourcetv():
    print("🔎 فحص موقع Sourcetv...")
    url = "https://www.sourcetv.info/category/stb-emu/"
    try:
        response = requests.get(url, headers=get_headers(), timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        first_post = soup.find('h2', class_='entry-title')
        title = first_post.text.strip()
        return {
            "name": f"SourceTV: {title[:25]}",
            "url": "http://mag.siptv.app", # مثال
            "mac": "00:1A:79:AA:BB:CC",
            "source": "SourceTV"
        }
    except:
        return None

def update_github(data):
    url = f"https://api.github.com/repos/{REPO}/contents/{FILE_PATH}"
    headers = {"Authorization": f"token {TOKEN}", "Accept": "application/vnd.github.v3+json"}
    
    # جلب SHA لتحديث الملف
    res = requests.get(url, headers=headers)
    sha = res.json().get('sha') if res.status_code == 200 else None
    
    content = base64.b64encode(json.dumps(data, indent=2).encode()).decode()
    payload = {"message": "تحديث صيد متعدد المصادر 🎯", "content": content, "sha": sha}
    
    response = requests.put(url, json=payload, headers=headers)
    if response.status_code in [200, 201]:
        print("🚀 تم تحديث السحابة بنجاح بجميع المصادر!")

if __name__ == "__main__":
    all_servers = []
    
    # الصيد من المصدر الأول
    s1 = hunt_iptv4sat()
    if s1: all_servers.append(s1)
    
    # الصيد من المصدر الثاني
    s2 = hunt_sourcetv()
    if s2: all_servers.append(s2)
    
    if TOKEN and all_servers:
        # إضافة ترقيم (ID) لكل سيرفر
        for i, srv in enumerate(all_servers):
            srv['id'] = i + 1
            
        update_github(all_servers)
