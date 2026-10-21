import sys
import os
import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime, timezone

def fetch_contributions(username):
    url = f"https://github.com/users/{username}/contributions"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    print(f"Fetching contributions from {url}...")
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        print(f"Error: Failed to fetch contributions page. HTTP Status: {res.status_code}")
        sys.exit(1)
        
    soup = BeautifulSoup(res.text, 'html.parser')
    
    # In GitHub's markup, days are typically <td class="ContributionCalendar-day">
    day_elements = soup.find_all("td", class_="ContributionCalendar-day")
    if not day_elements:
        print("Warning: No day elements found with 'ContributionCalendar-day' class. Trying generic fallback...")
        day_elements = soup.find_all(attrs={"data-date": True})
        
    if not day_elements:
        print("Error: Could not find contribution day cells in HTML.")
        sys.exit(1)
        
    print(f"Found {len(day_elements)} day cells. Parsing data...")
    
    # We will also look for tooltip text. GitHub renders <tool-tip for="id"> elements.
    tooltips = {t.get("for"): t.text.strip() for t in soup.find_all("tool-tip") if t.get("for")}
    
    parsed_days = []
    
    for td in day_elements:
        date_str = td.get("data-date")
        if not date_str:
            continue
            
        level_str = td.get("data-level", "0")
        try:
            level = int(level_str)
        except ValueError:
            level = 0
            
        td_id = td.get("id")
        
        # Parse contribution count
        count = 0
        tooltip_text = tooltips.get(td_id, "")
        
        if tooltip_text:
            # Format is usually "No contributions on Friday, July 24, 2026" 
            # or "5 contributions on Saturday, March 15, 2025"
            if tooltip_text.startswith("No contributions"):
                count = 0
            else:
                match = re.match(r"^([\d,]+)\s+contribution", tooltip_text)
                if match:
                    count = int(match.group(1).replace(",", ""))
                else:
                    # Fallback if text format changed slightly
                    count = 1 if level > 0 else 0
        else:
            # Fallback if no tooltip is found
            # Level 0 = 0, Level 1 = 1-2, Level 2 = 3-5, Level 3 = 6-8, Level 4 = 9+
            if level == 0:
                count = 0
            elif level == 1:
                count = 1
            elif level == 2:
                count = 3
            elif level == 3:
                count = 6
            else:
                count = 10
                
        parsed_days.append({
            "date": date_str,
            "count": count,
            "level": level
        })
        
    # Sort chronologically
    parsed_days.sort(key=lambda d: d["date"])
    
    # Calculate stats
    total_contributions = sum(d["count"] for d in parsed_days)
    
    # Compute streaks
    streak_list = []
    curr_streak = 0
    for d in parsed_days:
        if d["count"] > 0:
            curr_streak += 1
        else:
            curr_streak = 0
        streak_list.append(curr_streak)
        
    longest_streak = max(streak_list) if streak_list else 0
    
    # Compute current active streak
    # If the last day has count > 0, the active streak is streak_list[-1]
    # If the last day has count == 0, but the day before has count > 0, we can count the streak from the day before
    # (since the current day might not be finished/recorded yet).
    active_streak = 0
    if len(parsed_days) >= 2:
        if parsed_days[-1]["count"] > 0:
            active_streak = streak_list[-1]
        elif parsed_days[-2]["count"] > 0:
            active_streak = streak_list[-2]
        else:
            active_streak = 0
    elif len(parsed_days) == 1:
        active_streak = 1 if parsed_days[0]["count"] > 0 else 0
        
    # Compute best day
    best_day = {"date": "", "count": 0}
    for d in parsed_days:
        if d["count"] > best_day["count"]:
            best_day = {"date": d["date"], "count": d["count"]}
            
    # Compile output
    output_data = {
        "username": username,
        "last_updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "total_contributions": total_contributions,
        "current_streak": active_streak,
        "longest_streak": longest_streak,
        "best_day": best_day,
        "contributions": parsed_days
    }
    
    # Write to data directory
    os.makedirs("data", exist_ok=True)
    with open("data/contributions.json", "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2)
        
    print(f"Successfully scraped contributions for {username}.")
    print(f"Total: {total_contributions} | Current Streak: {active_streak} | Longest Streak: {longest_streak}")

def main():
    username = os.environ.get("GITHUB_USERNAME", "RoxyBasicNeedBot")
    if len(sys.argv) > 1:
        username = sys.argv[1]
    fetch_contributions(username)

if __name__ == "__main__":
    main()
