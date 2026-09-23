import os
import time
import random
from datetime import datetime
import requests
from git import Repo

# আপনার Pexels API Key
api_key = "DiqA3nNE1bXk1CaViv1inoLX9HW18I8g6GtECOhrp6y8kdloYRvRZRCd"
headers = {"Authorization": api_key}

# সার্চ কিওয়ার্ড লিস্ট
queries = ["nature", "aesthetic", "minimalist", "sunset", "architecture", "technology", "travel"]

def fetch_and_push_image():
    print(f"[{datetime.now()}] পিক্সেল এপিআই থেকে ছবি খোঁজা হচ্ছে...")
    query = random.choice(queries)
    url = f"https://api.pexels.com/v1/search?query={query}&per_page=15"
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            photos = data.get("photos", [])
            
            if photos:
                photo = random.choice(photos)
                image_url = photo["src"]["large"]
                
                # ছবি ডাউনলোড করা
                img_data = requests.get(image_url).content
                
                # 'images' ফোল্ডার তৈরি
                os.makedirs("images", exist_ok=True)
                filename = f"images/pexels_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                
                with open(filename, "wb") as handler:
                    handler.write(img_data)
                print(f"সফলভাবে ডাউনলোড হয়েছে: {filename}")
                
                # গিটহাবে অটো কমিট ও পুশ করার অংশ
                try:
                    repo = Repo(".")
                    # রেন্ডারে গিট পাসওয়ার্ড বা টোকেন সেটআপের জন্য রিমোট ইউআরএল টোকেন সহ দিতে হবে
                    # যেমন: https://<GITHUB_TOKEN>@github.com/mrsohagmia32-cell/Atopick.git
                    repo.git.add(filename)
                    repo.index.commit(f"Auto-fetched Pexels image: {filename} [skip ci]")
                    origin = repo.remote(name='origin')
                    origin.push()
                    print("গিটহাবে সফলভাবে পুশ করা হয়েছে!")
                except Exception as git_err:
                    print(f"গিট পুশ করতে সমস্যা হয়েছে: {git_err}")
            else:
                print("কোনো ছবি পাওয়া যায়নি।")
        else:
            print(f"এপিআই রিকোয়েস্ট ফেল করেছে: {response.status_code}")
    except Exception as e:
        print(f"ত্রুটি দেখা দিয়েছে: {e}")

# মূল ইনফিনিট লুপ (প্রতি ১০ মিনিট পর পর চলবে)
if __name__ == "__main__":
    print("স্টার্ট হয়েছে: রেন্ডার ব্যাকগ্রাউন্ড ওয়ার্কার চালু আছে...")
    while True:
        fetch_and_push_image()
        print("পরবর্তী ছবির জন্য ১০ মিনিট অপেক্ষা করা হচ্ছে...\n")
        time.sleep(600)  # ১০ মিনিট = ৬০০ সেকেন্ড
