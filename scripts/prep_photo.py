import sys
import os
import io
import urllib.request
import time
import re
from PIL import Image
import cv2
import numpy as np

try:
    from rembg import remove
    HAS_REMBG = True
except ImportError:
    HAS_REMBG = False

def get_latest_avatar_url(username):
    profile_url = f"https://github.com/{username}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache"
    }
    try:
        # Add cache buster to profile page request
        print(f"Scraping {profile_url} for the latest avatar link...")
        req = urllib.request.Request(f"{profile_url}?t={int(time.time())}", headers=headers)
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8', errors='ignore')
            
        match = re.search(r'<meta property="og:image" content="([^"]+)"', html)
        if match:
            avatar_url = match.group(1)
            # Add cache buster to avatar image URL
            if "?" in avatar_url:
                avatar_url += f"&t={int(time.time())}"
            else:
                avatar_url += f"?t={int(time.time())}"
            print(f"Discovered direct avatar URL: {avatar_url}")
            return avatar_url
    except Exception as e:
        print(f"Failed to scrape profile page: {e}. Falling back to default.")
        
    return f"https://github.com/{username}.png?t={int(time.time())}"

def main():
    username = os.environ.get("GITHUB_USERNAME", "RoxyBasicNeedBot")
    output_path = "source-prepped.png"
    
    # Check if a custom command line argument is provided (file path or URL)
    if len(sys.argv) >= 2:
        input_source = sys.argv[1]
    else:
        input_source = get_latest_avatar_url(username)
        
    print(f"Loading image from: {input_source}")
    
    try:
        if input_source.startswith("http://") or input_source.startswith("https://"):
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Cache-Control": "no-cache",
                "Pragma": "no-cache"
            }
            req = urllib.request.Request(input_source, headers=headers)
            with urllib.request.urlopen(req) as response:
                image_data = response.read()
            input_image = Image.open(io.BytesIO(image_data))
        else:
            if os.path.exists(input_source):
                input_image = Image.open(input_source)
            else:
                # If argument is just a username, get their latest avatar
                avatar_url = get_latest_avatar_url(input_source)
                print(f"Fetching from: {avatar_url}")
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    "Cache-Control": "no-cache",
                    "Pragma": "no-cache"
                }
                req = urllib.request.Request(avatar_url, headers=headers)
                with urllib.request.urlopen(req) as response:
                    image_data = response.read()
                input_image = Image.open(io.BytesIO(image_data))
    except Exception as e:
        print(f"Error loading image: {e}")
        sys.exit(1)
        
    # 1. Background removal / preparation
    if HAS_REMBG:
        print("Removing background with rembg...")
        rgba_image = remove(input_image)
        img_np = np.array(rgba_image)
    else:
        print("rembg not installed, processing RGBA directly...")
        if input_image.mode != "RGBA":
            rgba_image = input_image.convert("RGBA")
        else:
            rgba_image = input_image
        img_np = np.array(rgba_image)
    
    # 2. Extract channels
    if img_np.shape[2] == 4:
        rgb = img_np[:, :, :3]
        alpha = img_np[:, :, 3]
    else:
        rgb = img_np
        alpha = np.ones((img_np.shape[0], img_np.shape[1]), dtype=np.uint8) * 255
        
    # Convert RGB to grayscale
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    
    # 3. Boost contrast using CLAHE
    print("Applying CLAHE...")
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    clahe_img = clahe.apply(gray)
    
    # 4. Composite onto pure white background
    print("Compositing onto white background...")
    height, width = gray.shape
    white_bg = np.ones((height, width), dtype=np.uint8) * 255
    
    # Blend CLAHE image with white background using the alpha mask
    alpha_factor = alpha.astype(float) / 255.0
    final_img = (clahe_img.astype(float) * alpha_factor + white_bg.astype(float) * (1.0 - alpha_factor)).astype(np.uint8)
    
    # Save the prepped grayscale image
    cv2.imwrite(output_path, final_img)
    print(f"Successfully prepped photo and saved to {output_path}")

if __name__ == "__main__":
    main()
