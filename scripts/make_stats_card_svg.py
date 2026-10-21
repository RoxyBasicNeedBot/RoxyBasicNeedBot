"""
make_stats_card_svg.py
Generates a GitHub stats score card using repo_stats.json + contributions.json
for RoxyBasicNeedBot.
Displays: Total Stars, Total Forks, Repos, Contributions, Streak.
All animations SMIL only.
"""

import json
import os
import sys

def load_data():
    contrib = {}
    repos = []
    if os.path.exists("data/contributions.json"):
        with open("data/contributions.json", encoding="utf-8") as f:
            contrib = json.load(f)
    if os.path.exists("data/repo_stats.json"):
        with open("data/repo_stats.json", encoding="utf-8") as f:
            repos = json.load(f)
    return contrib, repos

def stat_block(bx, by, bw, bh, icon_d, label, value, color, delay):
    lines = []
    # Card
    lines.append(f'  <rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="8" fill="#140f28" stroke="#312554" stroke-width="1" opacity="0">')
    lines.append(f'    <animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="{delay}s" fill="freeze" />')
    lines.append('  </rect>')
    # Accent top border
    lines.append(f'  <rect x="{bx+1}" y="{by+1}" width="{bw-2}" height="3" rx="2" fill="{color}" opacity="0">')
    lines.append(f'    <animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="{delay}s" fill="freeze" />')
    lines.append('  </rect>')
    # Icon
    scale = 16 / 24.0
    lines.append('  <g opacity="0">')
    lines.append(f'    <path d="{icon_d}" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" fill="none" transform="translate({bx+16},{by+18}) scale({scale:.4f})" />')
    lines.append(f'    <animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="{delay}s" fill="freeze" />')
    lines.append('  </g>')
    # Value
    lines.append(f'  <text x="{bx+bw//2}" y="{by+58}" text-anchor="middle" font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', Helvetica, Arial, sans-serif" font-size="25" font-weight="800" fill="#f8fafc" opacity="0">{value}')
    lines.append(f'    <animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="{delay+0.08}s" fill="freeze" />')
    lines.append('  </text>')
    # Label
    lines.append(f'  <text x="{bx+bw//2}" y="{by+76}" text-anchor="middle" font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', Helvetica, Arial, sans-serif" font-size="11" font-weight="600" fill="#94a3b8" opacity="0">{label}')
    lines.append(f'    <animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="{delay+0.08}s" fill="freeze" />')
    lines.append('  </text>')
    return "\n".join(lines)

def generate_stats(output_path="stats-card.svg"):
    contrib, repos = load_data()

    total_stars   = sum(r.get("stars", 0) for r in repos)
    total_forks   = sum(r.get("forks", 0) for r in repos)
    total_repos   = len(repos)
    total_commits = contrib.get("total_contributions", 233)
    streak        = contrib.get("current_streak", 0)
    longest       = contrib.get("longest_streak", 6)

    W, H = 860, 185

    blocks = [
        ("M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z",
         "Total Stars", f"{total_stars}", "#fbbf24", 0.12),
        ("M15 18H9M12 21V9M3 9V6a3 3 0 0 1 3-3h12a3 3 0 0 1 3 3v3",
         "Total Forks", f"{total_forks}", "#06b6d4", 0.20),
        ("M3 3h7v7H3zM14 3h7v7h-7zM3 14h7v7H3zM14 14h7v7h-7z",
         "Repositories", f"{total_repos}", "#a855f7", 0.28),
        ("M12 20V10M18 20V4M6 20v-4",
         "Contributions", f"{total_commits:,}", "#ec4899", 0.36),
        ("M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01",
         "Current Streak", f"{streak}d", "#38bdf8", 0.44),
        ("M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22",
         "Longest Streak", f"{longest}d", "#c084fc", 0.52),
    ]

    bw = (W - 24 - 5 * 10) // 6
    bh = 94
    by = 50
    bx_start = 14

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
    svg.append(f'  <text x="78" y="21" font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', Helvetica, Arial, sans-serif" font-size="12" font-weight="600" fill="#a5b4fc">roxy@terminal: github stats --user=RoxyBasicNeedBot</text>')

    for i, (icon_d, label, value, color, delay) in enumerate(blocks):
        bx = bx_start + i * (bw + 10)
        svg.append(stat_block(bx, by, bw, bh, icon_d, label, value, color, delay))

    svg.append('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"Generated stats card: {output_path}")

if __name__ == "__main__":
    generate_stats()
