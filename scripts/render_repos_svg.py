"""
render_repos_svg.py
Renders a 3x2 grid of top featured repositories for RoxyBasicNeedBot.
Highlights Android libraries and Telegram bots.
GitHub-safe SMIL animations.
"""

import json
import os
import re

LANG_COLORS = {
    "Kotlin":     "#a855f7",
    "Python":     "#38bdf8",
    "Java":       "#f59e0b",
    "Android":    "#3ddc84",
    "JavaScript": "#facc15",
    "Shell":      "#4ade80",
}

STAR_D  = "M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"
FORK_D  = "M6 3a3 3 0 1 0 0 6 3 3 0 0 0 0-6zm6 18a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm6-18a3 3 0 1 0 0 6 3 3 0 0 0 0-6zM6 9v3a3 3 0 0 0 3 3h6a3 3 0 0 0 3-3V9"

def strip_emoji(text):
    return re.sub(r'[^\x00-\x7F]+', '', text).strip()

def word_wrap(text, max_len=54):
    text = strip_emoji(text)
    if len(text) <= max_len:
        return text, ""
    cut = text[:max_len].rfind(' ')
    if cut < 20:
        cut = max_len
    return text[:cut], text[cut:].strip()[:max_len]

def xml_escape(text):
    return text.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"','&quot;')

def get_curated_repos(json_path="data/repo_stats.json"):
    repos = []
    if os.path.exists(json_path):
        with open(json_path, encoding="utf-8") as f:
            repos = json.load(f)

    # Priority names for showcase
    priority = [
        "Flare",
        "File-Rename-4GB-Bot-Auto-Rename-Bot",
        "KDownloader",
        "TXT-TO-VIDEO-LEECH-UPLOADER",
        "Vivx",
        "Zip-Maker-Bot-Zip-Creater-Bot",
        "PDF-TOOL-BOT",
        "Telegram-ID-User-Info-Quick-ID-Bot"
    ]

    selected = []
    repo_map = {r.get("name"): r for r in repos}

    for p in priority:
        if p in repo_map and repo_map[p] not in selected:
            selected.append(repo_map[p])

    # Fill remaining from repos if needed
    for r in repos:
        if len(selected) >= 6:
            break
        if r not in selected and r.get("description"):
            selected.append(r)

    return selected[:6]

def render_repos(json_path="data/repo_stats.json", output_path="repo-showcase.svg"):
    repos = get_curated_repos(json_path)

    W  = 860
    cw = 405
    ch = 130
    gap = 20
    px = 22
    py = 52

    rows = (len(repos) + 1) // 2
    H = py + rows * (ch + gap) + 16

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">')
    svg.append(f'  <rect width="{W}" height="{H}" rx="12" fill="#0d111a" stroke="#2e274a" stroke-width="1.5" />')

    # Header bar
    svg.append(f'  <rect x="0" y="0" width="{W}" height="38" rx="12" fill="#140f28" />')
    svg.append(f'  <rect x="0" y="28" width="{W}" height="10" fill="#140f28" />')
    svg.append(f'  <rect x="0" y="37" width="{W}" height="1" fill="#382a5c" />')
    svg.append(f'  <circle cx="20" cy="16" r="5" fill="#ff5f56" />')
    svg.append(f'  <circle cx="38" cy="16" r="5" fill="#ffbd2e" />')
    svg.append(f'  <circle cx="56" cy="16" r="5" fill="#27c93f" />')
    svg.append(f'  <text x="78" y="21" font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', Helvetica, Arial, sans-serif" font-size="12" font-weight="600" fill="#a5b4fc">roxy@terminal: featured-projects --top=6</text>')

    for i, repo in enumerate(repos):
        col = i % 2
        row = i // 2
        x = px + col * (cw + gap)
        y = py + row * (ch + gap)
        delay = round(0.08 + i * 0.08, 2)

        name  = xml_escape(repo.get("name", ""))
        desc  = repo.get("description", "") or "High performance open source project."
        lang  = repo.get("language", "") or "Kotlin"
        stars = repo.get("stars", 0)
        forks = repo.get("forks", 0)
        color = LANG_COLORS.get(lang, "#a855f7")

        d1, d2 = word_wrap(xml_escape(desc))

        # Card body
        svg.append(f'  <rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="8" fill="#140f28" stroke="#312554" stroke-width="1" opacity="0">')
        svg.append(f'    <animate attributeName="opacity" from="0" to="1" dur="0.45s" begin="{delay}s" fill="freeze" />')
        svg.append('  </rect>')

        # Top accent line
        svg.append(f'  <rect x="{x+1}" y="{y+1}" width="{cw-2}" height="2.5" rx="2" fill="{color}" opacity="0">')
        svg.append(f'    <animate attributeName="opacity" from="0" to="1" dur="0.45s" begin="{delay}s" fill="freeze" />')
        svg.append('  </rect>')

        # Folder git icon
        folder_d = "M2 6a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V6z M12 11v3M10 13l2-2 2 2"
        scale = 14 / 24.0
        svg.append('  <g opacity="0">')
        svg.append(f'    <path d="{folder_d}" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" fill="none" transform="translate({x+14},{y+16}) scale({scale:.4f})" />')
        svg.append(f'    <animate attributeName="opacity" from="0" to="1" dur="0.45s" begin="{delay}s" fill="freeze" />')
        svg.append('  </g>')

        # Repo name
        svg.append(f'  <text x="{x+36}" y="{y+29}" font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', Helvetica, Arial, sans-serif" font-size="13.5" font-weight="700" fill="#38bdf8" opacity="0">{name}')
        svg.append(f'    <animate attributeName="opacity" from="0" to="1" dur="0.45s" begin="{delay}s" fill="freeze" />')
        svg.append('  </text>')

        # Description lines
        svg.append(f'  <text x="{x+14}" y="{y+52}" font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', Helvetica, Arial, sans-serif" font-size="11.5" fill="#94a3b8" opacity="0">{d1}')
        svg.append(f'    <animate attributeName="opacity" from="0" to="1" dur="0.45s" begin="{delay}s" fill="freeze" />')
        svg.append('  </text>')

        if d2:
            svg.append(f'  <text x="{x+14}" y="{y+68}" font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', Helvetica, Arial, sans-serif" font-size="11.5" fill="#94a3b8" opacity="0">{d2}')
            svg.append(f'    <animate attributeName="opacity" from="0" to="1" dur="0.45s" begin="{delay}s" fill="freeze" />')
            svg.append('  </text>')

        # Divider
        svg.append(f'  <line x1="{x+14}" y1="{y+ch-36}" x2="{x+cw-14}" y2="{y+ch-36}" stroke="#251c40" stroke-width="1" />')

        # Language tag
        svg.append(f'  <circle cx="{x+20}" cy="{y+ch-18}" r="5" fill="{color}" opacity="0">')
        svg.append(f'    <animate attributeName="opacity" from="0" to="1" dur="0.45s" begin="{delay}s" fill="freeze" />')
        svg.append('  </circle>')
        svg.append(f'  <text x="{x+32}" y="{y+ch-13}" font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', Helvetica, Arial, sans-serif" font-size="11" font-weight="600" fill="#cbd5e1" opacity="0">{xml_escape(lang)}')
        svg.append(f'    <animate attributeName="opacity" from="0" to="1" dur="0.45s" begin="{delay}s" fill="freeze" />')
        svg.append('  </text>')

        # Star count
        scale_sm = 12 / 24.0
        svg.append('  <g opacity="0">')
        svg.append(f'    <path d="{STAR_D}" stroke="#fbbf24" stroke-width="1.8" fill="none" stroke-linecap="round" stroke-linejoin="round" transform="translate({x+cw-118},{y+ch-26}) scale({scale_sm:.4f})" />')
        svg.append(f'    <animate attributeName="opacity" from="0" to="1" dur="0.45s" begin="{delay}s" fill="freeze" />')
        svg.append('  </g>')
        svg.append(f'  <text x="{x+cw-102}" y="{y+ch-14}" font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', Helvetica, Arial, sans-serif" font-size="11" fill="#fbbf24" font-weight="700" opacity="0">{stars}')
        svg.append(f'    <animate attributeName="opacity" from="0" to="1" dur="0.45s" begin="{delay}s" fill="freeze" />')
        svg.append('  </text>')

        # Fork count
        svg.append('  <g opacity="0">')
        svg.append(f'    <path d="{FORK_D}" stroke="#94a3b8" stroke-width="1.8" fill="none" stroke-linecap="round" stroke-linejoin="round" transform="translate({x+cw-68},{y+ch-26}) scale({scale_sm:.4f})" />')
        svg.append(f'    <animate attributeName="opacity" from="0" to="1" dur="0.45s" begin="{delay}s" fill="freeze" />')
        svg.append('  </g>')
        svg.append(f'  <text x="{x+cw-52}" y="{y+ch-14}" font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', Helvetica, Arial, sans-serif" font-size="11" fill="#94a3b8" opacity="0">{forks}')
        svg.append(f'    <animate attributeName="opacity" from="0" to="1" dur="0.45s" begin="{delay}s" fill="freeze" />')
        svg.append('  </text>')

    svg.append('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"Generated repo showcase: {output_path}")

if __name__ == "__main__":
    render_repos()
