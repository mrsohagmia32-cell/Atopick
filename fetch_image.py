import os
import time
import random
import threading
from datetime import datetime
from flask import Flask
import requests
from git import Repo

# ফ্লাস্ক অ্যাপ ইনিশিয়ালাইজ করা
app = Flask(__name__)

@app.route("/")
def home():
    return "Pexels Image Fetcher Worker is running live and active!"

# পিক্সেল এপিআই কি
api_key = "DiqA3nNE1bXk1CaViv1inoLX9HW18I8g6GtECOhrp6y8kdloYRvRZRCd"
headers = {"Authorization": api_key}

# সার্চ কিওয়ার্ড লিস্ট
queries = ["nature", "aesthetic", "minimalist", "sunset", "architecture", "technology", "travel"]

def fetch_and_push_image():
    while True:
        try:
            print(f"\n[{datetime.now()}] পিক্সেল এপিআই থেকে ছবি খোঁজা শুরু হয়েছে...")
            query = random.choice(queries)
            url = f"https://api.pexels.com/v1/search?query={query}&per_page=15"
            
            # ১০ সেকেন্ড টাইমআউট সহ এপিআই রিকোয়েস্ট
            response = requests.get(url, headers=headers, timeout=10)
            print(f"এপিআই রেসপন্স কোড: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                photos = data.get("photos", [])
                
                if photos:
                    photo = random.choice(photos)
                    image_url = photo["src"]["large"]
                    
                    print(f"ছবি ডাউনলোড করা হচ্ছে: {image_url}")
                    img_response = requests.get(image_url, timeout=15)
                    
                    if img_response.status_code == 200:
                        img_data = img_response.content
                        
                        # 'images' ফোল্ডার তৈরি
                        os.makedirs("images", exist_ok=True)
                        filename = f"images/pexels_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                        
                        with open(filename, "wb") as handler:
                            handler.write(img_data)
                        print(f"লোকাল মেশিনে সফলভাবে সেভ হয়েছে: {filename}")
                        
                        # গিটহাবে অটো কমিট ও পুশ করার অংশ
                        try:
                            repo = Repo(".")
                            
                            # গিট কনফিগারেশন সেট করা (রেন্ডারের জন্য জরুরি)
                            repo.git.config("user.email", "bot@atopick.com")
                            repo.git.config("user.name", "Atopick Bot")
                            
                            github_token = os.environ.get("GITHUB_TOKEN")
                            if github_token:
                                repo.git.remote("set-url", "origin", f"https://{github_token}@github.com/mrsohagmia32-cell/Atopick.git")
                            
                            repo.git.add(filename)
                            repo.index.commit(f"Auto-fetched Pexels image: {filename} [skip ci]")
                            origin = repo.remote(name='origin')
                            origin.push()
                            print("🎉 গিটহাবে সফলভাবে ছবি পুশ করা হয়েছে!")
                        except Exception as git_err:
                            print(f"❌ গিট পুশ করতে সমস্যা হয়েছে: {git_err}")
                    else:
                        print("❌ ছবি ডাউনলোড করা সম্ভব হয়নি।")
                else:
                    print("⚠️ পিক্সেল এপিআই থেকে কোনো ছবি পাওয়া যায়নি।")
            else:
                print(f"❌ এপিআই রিকোয়েস্ট ফেল করেছে। স্ট্যাটাস কোড: {response.status_code}")
        except Exception as e:
            print(f"❌ কোডে বড় কোনো ত্রুটি দেখা দিয়েছে: {e}")
            
        print("⏳ পরবর্তী ছবির জন্য ১০ মিনিট অপেক্ষা করা হচ্ছে...")
        time.sleep(600)  # ১০ মিনিট

def start_background_task():
    t = threading.Thread(target=fetch_and_push_image)
    t.daemon = True
    t.start()

if __name__ == "__main__":
    start_background_task()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
