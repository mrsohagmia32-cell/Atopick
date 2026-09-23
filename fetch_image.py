import os
import requests
import random
from datetime import datetime

# আপনার Pexels API Key
api_key = "DiqA3nNE1bXk1CaViv1inoLX9HW18I8g6GtECOhrp6y8kdloYRvRZRCd"
headers = {"Authorization": api_key}

# সার্চ কিওয়ার্ড লিস্ট (এখান থেকে যেকোনো একটি র্যান্ডমলি বেছে নেওয়া হবে)
queries = ["nature", "aesthetic", "minimalist", "sunset", "architecture", "technology", "travel"]
query = random.choice(queries)

# Pexels API থেকে ছবি সার্চ করা
url = f"https://api.pexels.com/v1/search?query={query}&per_page=15"
response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    photos = data.get("photos", [])
    
    if photos:
        # র্যান্ডম একটি ছবি সিলেক্ট করা
        photo = random.choice(photos)
        image_url = photo["src"]["large"]
        
        # ছবি ডাউনলোড করা
        img_data = requests.get(image_url).content
        
        # 'images' নামের ফোল্ডার তৈরি (যদি না থাকে)
        os.makedirs("images", exist_ok=True)
        
        # ইউনিক ফাইলের নাম তৈরি (টাইমস্ট্যাম্প সহ)
        filename = f"images/pexels_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        
        with open(filename, "wb") as handler:
            handler.write(img_data)
        print(f"Successfully downloaded: {filename}")
    else:
        print("No photos found.")
else:
    print(f"Failed to fetch from Pexels API: {response.status_code}")
