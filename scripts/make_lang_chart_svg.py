"""
make_lang_chart_svg.py
Renders an animated horizontal bar chart of top programming languages
derived from repo_stats.json for RoxyBasicNeedBot. SMIL animations only.
"""

import json
import os
import sys
from collections import Counter

LANG_COLORS = {
    "Kotlin":     "#a855f7",
    "Python":     "#38bdf8",
    "Java":       "#f59e0b",
    "Android":    "#3ddc84",
    "JavaScript": "#facc15",
    "Shell":      "#4ade80",
    "Dart":       "#06b6d4",
    "Other":      "#94a3b8",
}

def generate_lang_chart(output_path="lang-chart.svg"):
    repos = []
    if os.path.exists("data/repo_stats.json"):
        with open("data/repo_stats.json", encoding="utf-8") as f:
            repos = json.load(f)

    # Aggregate by language (weighted by stars+1 so active repos dominate)
    counts = Counter()
    for r in repos:
        lang = r.get("language") or "Python"
        weight = r.get("stars", 0) + r.get("forks", 0) * 2 + 1
        counts[lang] += weight

    top = counts.most_common(6)
    total = sum(v for _, v in top) or 1

    W = 860
    bar_h = 22
    bar_max_w = 560
    label_x = 30
    bar_x = 180
    row_gap = 34
    chart_top = 58
    H = chart_top + len(top) * row_gap + 20

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
    svg.append(f'  <text x="78" y="21" font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', Helvetica, Arial, sans-serif" font-size="12" font-weight="600" fill="#a5b4fc">roxy@terminal: language-breakdown --weighted</text>')

    for i, (lang, score) in enumerate(top):
        pct = score / total
        filled_w = max(4.0, round(pct * bar_max_w, 1))
        color = LANG_COLORS.get(lang, "#a855f7")
        y = chart_top + i * row_gap
        delay = round(0.08 + i * 0.08, 2)

        # Language name
        svg.append(f'  <text x="{label_x}" y="{y + 16}" font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', Helvetica, Arial, sans-serif" font-size="13" font-weight="600" fill="#f1f5f9" text-anchor="start" opacity="0">{lang}')
        svg.append(f'    <animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="{delay}s" fill="freeze" />')
        svg.append('  </text>')

        # Bar track
        svg.append(f'  <rect x="{bar_x}" y="{y+4}" width="{bar_max_w}" height="{bar_h}" rx="{bar_h//2}" fill="#140f28" stroke="#312554" stroke-width="1" />')

        # Bar fill (animated)
        svg.append(f'  <rect x="{bar_x}" y="{y+4}" width="0" height="{bar_h}" rx="{bar_h//2}" fill="{color}">')
        svg.append(f'    <animate attributeName="width" from="0" to="{filled_w}" dur="0.8s" begin="{delay}s" fill="freeze" calcMode="spline" keySplines="0.16 1 0.3 1" keyTimes="0;1" />')
        svg.append('  </rect>')

        # Color dot
        svg.append(f'  <circle cx="{bar_x - 14}" cy="{y + 15}" r="5" fill="{color}" opacity="0">')
        svg.append(f'    <animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="{delay}s" fill="freeze" />')
        svg.append('  </circle>')

        # Percentage label
        pct_label = f"{pct*100:.1f}%"
        svg.append(f'  <text x="{bar_x + bar_max_w + 14}" y="{y + 17}" font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', Helvetica, Arial, sans-serif" font-size="12" fill="{color}" font-weight="700" opacity="0">{pct_label}')
        svg.append(f'    <animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="{delay + 0.3}s" fill="freeze" />')
        svg.append('  </text>')

    svg.append('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"Generated language chart: {output_path}")

if __name__ == "__main__":
    generate_lang_chart()
