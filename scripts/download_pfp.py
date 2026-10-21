import urllib.request
import sys
import os
import time
import re

def get_latest_avatar_url(username):
    profile_url = f"https://github.com/{username}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache"
    }
    try:
        print(f"Scraping {profile_url} for the latest avatar link...")
        req = urllib.request.Request(f"{profile_url}?t={int(time.time())}", headers=headers)
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8', errors='ignore')
            
        match = re.search(r'<meta property="og:image" content="([^"]+)"', html)
        if match:
            avatar_url = match.group(1)
            if "?" in avatar_url:
                avatar_url += f"&t={int(time.time())}"
            else:
                avatar_url += f"?t={int(time.time())}"
            print(f"Discovered direct avatar URL: {avatar_url}")
            return avatar_url
    except Exception as e:
        print(f"Failed to scrape profile page: {e}. Falling back to default.")
        
    return f"https://github.com/{username}.png?t={int(time.time())}"

def download_pfp(username=None, output_path="source-photo.jpg"):
    if not username:
        username = os.environ.get("GITHUB_USERNAME", "RoxyBasicNeedBot")
    avatar_url = get_latest_avatar_url(username)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache"
    }
    print(f"Downloading GitHub profile picture from {avatar_url}...")
    try:
        req = urllib.request.Request(avatar_url, headers=headers)
        with urllib.request.urlopen(req) as response:
            with open(output_path, "wb") as f:
                f.write(response.read())
        print(f"Successfully downloaded profile picture and saved to '{output_path}'.")
    except Exception as e:
        print(f"Error downloading profile picture: {e}")
        sys.exit(1)

if __name__ == "__main__":
    download_pfp()
