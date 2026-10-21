"""
make_matrix_svg.py
Cyberpunk Matrix Code Rain SVG for RoxyBasicNeedBot.
Embeds real repository names as glowing cyan & violet columns.
Pure SMIL animations (100% GitHub safe).
"""
import json
import os
import sys
import hashlib

MATRIX_CHARS = (
    "0123456789"
    "ABCDEF"
    "abcdef"
    "{}[]()*#@!?%$;:=+-|^~."
    "01100101010011010110"
)

BG_COLOR    = "#0c0e18"
DIM_COLOR   = "#241042"
MID_COLOR   = "#6b21a8"
LEAD_COLOR  = "#a855f7"
HEAD_COLOR  = "#f5d0fe"
HIGHLIGHT   = "#06b6d4"
HL_DIM      = "#155e75"

FONT_SIZE = 12
CHAR_W    = 10
CHAR_H    = 14

def rng(seed):
    h = int(hashlib.md5(str(seed).encode()).hexdigest(), 16)
    return h

def rand_chars(seed, n):
    r = rng(seed)
    result = []
    for i in range(n):
        r = (r * 1664525 + 1013904223) & 0xFFFFFFFF
        result.append(MATRIX_CHARS[r % len(MATRIX_CHARS)])
    return result

def load_repo_names():
    names = []
    if os.path.exists("data/repo_stats.json"):
        try:
            with open("data/repo_stats.json", encoding="utf-8") as f:
                repos = json.load(f)
            for r in repos:
                n = r.get("name", "")
                if n and n not in ("RoxyBasicNeedBot", "qeqe"):
                    clean = n.replace("-Bot", "").replace("-Auto-Rename", "").replace("-Creater", "").replace("-Quick-ID", "")
                    names.append(clean.upper()[:12])
        except Exception:
            pass
    if not names:
        names = ["TXT2VIDEO", "RENAME4GB", "KDOWNLOAD", "FLARE", "ZIPMAKER", "VIVX", "PDFTOOL", "ROXYBOT", "KOTLIN", "PYTHON"]
    return names[:14]

def generate_matrix(output_path="matrix-rain.svg"):
    W = 860
    H = 240

    num_cols = W // CHAR_W
    num_rows = H // CHAR_H + 6

    repo_names = load_repo_names()

    highlight_cols = {}
    step = num_cols // (len(repo_names) + 1)
    for i, name in enumerate(repo_names):
        col_idx = step * (i + 1)
        highlight_cols[col_idx] = name

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">')

    # Background
    svg.append(f'  <rect width="{W}" height="{H}" rx="14" fill="{BG_COLOR}" stroke="#2b2246" stroke-width="1.5" />')

    # Vignettes
    svg.append('  <defs>')
    svg.append(f'    <linearGradient id="fadeTop" x1="0" y1="0" x2="0" y2="1">')
    svg.append(f'      <stop offset="0%"   stop-color="{BG_COLOR}" stop-opacity="1" />')
    svg.append(f'      <stop offset="35%"  stop-color="{BG_COLOR}" stop-opacity="0" />')
    svg.append(f'    </linearGradient>')
    svg.append(f'    <linearGradient id="fadeBot" x1="0" y1="0" x2="0" y2="1">')
    svg.append(f'      <stop offset="65%"  stop-color="{BG_COLOR}" stop-opacity="0" />')
    svg.append(f'      <stop offset="100%" stop-color="{BG_COLOR}" stop-opacity="1" />')
    svg.append(f'    </linearGradient>')
    svg.append('  </defs>')

    # Falling matrix code streams
    for ci in range(num_cols):
        x = ci * CHAR_W + 1
        r0 = rng(ci * 31337)

        dur   = round(2.5 + (r0 % 1000) / 260.0, 2)
        delay = round((r0 % 2000) / 1000.0, 2)

        is_hl = ci in highlight_cols
        name  = highlight_cols.get(ci, "")

        chars = rand_chars(ci, num_rows)

        if is_hl:
            trail_col = HL_DIM
            lead_col  = HIGHLIGHT
            head_col  = "#e0f2fe"
        else:
            trail_col = DIM_COLOR
            lead_col  = LEAD_COLOR
            head_col  = HEAD_COLOR

        trail_h = num_rows * CHAR_H
        svg.append(f'  <text x="{x}" y="0" font-family="SFMono-Regular, Consolas, \'Liberation Mono\', Menlo, monospace" font-size="{FONT_SIZE}" fill="{trail_col}" dominant-baseline="hanging" xml:space="preserve">')
        for j, ch in enumerate(chars[:-3]):
            svg.append(f'    <tspan x="{x}" dy="{CHAR_H}">{ch}</tspan>')
        svg.append(f'    <animate attributeName="y" from="-{trail_h}" to="{H+CHAR_H}" dur="{dur}s" begin="{delay}s" repeatCount="indefinite" />')
        svg.append('  </text>')

        # Lead characters
        svg.append(f'  <text x="{x}" y="0" font-family="SFMono-Regular, Consolas, \'Liberation Mono\', Menlo, monospace" font-size="{FONT_SIZE}" fill="{lead_col}" dominant-baseline="hanging" xml:space="preserve">')
        for j, ch in enumerate(chars[-3:]):
            svg.append(f'    <tspan x="{x}" dy="{CHAR_H}">{ch}</tspan>')
        svg.append(f'    <animate attributeName="y" from="-{trail_h - (num_rows-3)*CHAR_H}" to="{H+CHAR_H}" dur="{dur}s" begin="{delay}s" repeatCount="indefinite" />')
        svg.append('  </text>')

        # Head character
        svg.append(f'  <text x="{x}" y="0" font-family="SFMono-Regular, Consolas, \'Liberation Mono\', Menlo, monospace" font-size="{FONT_SIZE}" fill="{head_col}" font-weight="bold" dominant-baseline="hanging">{chars[0]}')
        svg.append(f'    <animate attributeName="y" from="-{CHAR_H}" to="{H+CHAR_H}" dur="{dur}s" begin="{delay}s" repeatCount="indefinite" />')
        svg.append('  </text>')

        # Highlight repo column
        if is_hl and name:
            name_y = H // 2 - (len(name) * CHAR_H) // 2
            svg.append(f'  <text x="{x}" y="{name_y}" font-family="SFMono-Regular, Consolas, \'Liberation Mono\', Menlo, monospace" font-size="{FONT_SIZE}" fill="{HIGHLIGHT}" font-weight="bold" xml:space="preserve">')
            for j, ch in enumerate(name):
                svg.append(f'    <tspan x="{x}" dy="{CHAR_H}">{ch}</tspan>')
            svg.append('  </text>')

    # Vignettes
    svg.append(f'  <rect width="{W}" height="{H}" rx="14" fill="url(#fadeTop)" />')
    svg.append(f'  <rect width="{W}" height="{H}" rx="14" fill="url(#fadeBot)" />')

    # Centre badge
    label = "ROXY"
    label_w = 230
    label_x = W // 2 - label_w // 2
    label_y = H // 2 - 26
    svg.append(f'  <rect x="{label_x}" y="{label_y}" width="{label_w}" height="52" rx="10" fill="{BG_COLOR}" fill-opacity="0.9" stroke="#382a5c" stroke-width="1.2" />')
    svg.append(f'  <text x="{W//2}" y="{label_y+32}" text-anchor="middle" font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', Helvetica, Arial, sans-serif" font-size="28" font-weight="900" letter-spacing="8" fill="{LEAD_COLOR}" opacity="0.98">{label}</text>')
    svg.append(f'  <text x="{W//2}" y="{label_y+46}" text-anchor="middle" font-family="SFMono-Regular, Consolas, \'Liberation Mono\', Menlo, monospace" font-size="9.5" font-weight="700" fill="#38bdf8" letter-spacing="2">ANDROID • TELEGRAM • AUTOMATION</text>')

    svg.append('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"Generated matrix rain: {output_path} ({len(highlight_cols)} highlighted repos)")

if __name__ == "__main__":
    generate_matrix()
