import urllib.request
import json
import sys
import os

def fetch_repos(username=None, output_path="data/repo_stats.json"):
    if not username:
        username = os.environ.get("GITHUB_USERNAME", "RoxyBasicNeedBot")
    url = f"https://api.github.com/users/{username}/repos?per_page=100"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    print(f"Fetching public repositories for '{username}' from GitHub API...")
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            repos_data = json.loads(response.read().decode('utf-8'))
            
        print(f"Fetched {len(repos_data)} repositories.")
        
        # Extract and format relevant stats
        formatted_repos = []
        for r in repos_data:
            # Skip fork repos unless they have high stars
            if r.get("fork") and r.get("stargazers_count", 0) < 5:
                continue
                
            formatted_repos.append({
                "name": r.get("name"),
                "description": r.get("description") or "",
                "stars": r.get("stargazers_count", 0),
                "forks": r.get("forks_count", 0),
                "language": r.get("language") or "Python",
                "html_url": r.get("html_url"),
                "updated_at": r.get("updated_at")
            })
            
        # Sort by star count first, then by updated time
        formatted_repos.sort(key=lambda x: (x["stars"], x["updated_at"]), reverse=True)
        
        os.makedirs("data", exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(formatted_repos, f, indent=2)
            
        print(f"Saved repository stats to '{output_path}'.")
    except Exception as e:
        print(f"Error fetching repositories: {e}")
        sys.exit(1)

if __name__ == "__main__":
    fetch_repos()
