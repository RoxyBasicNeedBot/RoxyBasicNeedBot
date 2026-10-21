"""
make_matrix_svg.py
Generates an animated Matrix-style code rain SVG.
Your real repo names are embedded as highlighted "signal" columns
that burn through the green-character rain.
Pure SMIL — 100% GitHub-safe, no JS.
"""
import json, os, sys, hashlib, random

# ── Char sets ──────────────────────────────────────────────────────────────
# ASCII-safe matrix chars: digits, hex, symbols — no multi-byte chars
MATRIX_CHARS = (
    "0123456789"
    "ABCDEF"
    "abcdef"
    "{}[]()*#@!?%$;:=+-|^~."
    "01100101010011010110"
)

# ── Visual settings ────────────────────────────────────────────────────────
BG_COLOR    = "#0d111a"
DIM_COLOR   = "#2e1065"   # trailing chars (dim purple)
MID_COLOR   = "#7c3aed"   # mid-trail
LEAD_COLOR  = "#a855f7"   # leading bright violet
HEAD_COLOR  = "#f5d0fe"   # bright pink/white head
HIGHLIGHT   = "#06b6d4"   # repo name columns (cyan)
HL_DIM      = "#164e63"   # dim version of highlight trail

FONT_SIZE = 12
CHAR_W    = 10   # px per column
CHAR_H    = 14   # px per row (line-height)

def rng(seed):
    """Simple deterministic RNG based on hash."""
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
        with open("data/repo_stats.json") as f:
            repos = json.load(f)
        for r in repos[:12]:  # top 12
            n = r.get("name", "")
            if n:
                names.append(n.upper()[:10])  # cap at 10 chars
    if not names:
        names = ["ROXYBOT", "FLARE", "KDOWNLOAD", "RENAME4GB", "VIVX", "ZIPMAKER", "TELEGRAM", "KOTLIN"]
    return names

def generate_matrix(output_path="matrix-rain.svg"):
    W = 860
    H = 240

    num_cols  = W // CHAR_W          # ~86 columns
    num_rows  = H // CHAR_H + 6      # visible rows + buffer

    repo_names = load_repo_names()

    # Pick columns that will display repo names (evenly distributed)
    highlight_cols = {}
    step = num_cols // (len(repo_names) + 1)
    for i, name in enumerate(repo_names):
        col_idx = step * (i + 1)
        highlight_cols[col_idx] = name

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">')

    # Background
    svg.append(f'  <rect width="{W}" height="{H}" rx="10" fill="{BG_COLOR}" />')

    # Top/bottom vignette fade for polish
    svg.append('  <defs>')
    svg.append(f'    <linearGradient id="fadeTop" x1="0" y1="0" x2="0" y2="1">')
    svg.append(f'      <stop offset="0%"   stop-color="{BG_COLOR}" stop-opacity="1" />')
    svg.append(f'      <stop offset="30%"  stop-color="{BG_COLOR}" stop-opacity="0" />')
    svg.append(f'    </linearGradient>')
    svg.append(f'    <linearGradient id="fadeBot" x1="0" y1="0" x2="0" y2="1">')
    svg.append(f'      <stop offset="70%"  stop-color="{BG_COLOR}" stop-opacity="0" />')
    svg.append(f'      <stop offset="100%" stop-color="{BG_COLOR}" stop-opacity="1" />')
    svg.append(f'    </linearGradient>')
    svg.append('  </defs>')

    # ── Falling columns ────────────────────────────────────────────────────
    for ci in range(num_cols):
        x = ci * CHAR_W + 1
        r0 = rng(ci * 31337)

        # Speed: faster on left, varies
        dur  = round(2.5 + (r0 % 1000) / 250.0, 2)   # 2.5s – 6.5s
        delay = round((r0 % 2000) / 1000.0, 2)         # 0 – 2s stagger

        is_hl = ci in highlight_cols
        name  = highlight_cols.get(ci, "")

        # Build character stream (num_rows chars)
        chars = rand_chars(ci, num_rows)

        # Color layers: dim trail → mid → lead head
        # We render 3 overlapping streams per column to simulate the gradient:

        if is_hl:
            trail_col = HL_DIM
            lead_col  = HIGHLIGHT
            head_col  = "#a8d8ff"
        else:
            trail_col = DIM_COLOR
            lead_col  = LEAD_COLOR
            head_col  = HEAD_COLOR

        # Render trail (dim, all chars)
        trail_text = "&#10;".join(chars)
        trail_h = num_rows * CHAR_H
        svg.append(f'  <text x="{x}" y="0" font-family="SFMono-Regular, Consolas, \'Liberation Mono\', Menlo, monospace" font-size="{FONT_SIZE}" fill="{trail_col}" dominant-baseline="hanging" xml:space="preserve">')
        for j, ch in enumerate(chars[:-3]):
            svg.append(f'    <tspan x="{x}" dy="{CHAR_H}">{ch}</tspan>')
        svg.append(f'    <animate attributeName="y" from="-{trail_h}" to="{H+CHAR_H}" dur="{dur}s" begin="{delay}s" repeatCount="indefinite" />')
        svg.append(f'  </text>')

        # Render bright lead (last 3 chars + head)
        svg.append(f'  <text x="{x}" y="0" font-family="SFMono-Regular, Consolas, \'Liberation Mono\', Menlo, monospace" font-size="{FONT_SIZE}" fill="{lead_col}" dominant-baseline="hanging" xml:space="preserve">')
        for j, ch in enumerate(chars[-3:]):
            svg.append(f'    <tspan x="{x}" dy="{CHAR_H}">{ch}</tspan>')
        svg.append(f'    <animate attributeName="y" from="-{trail_h - (num_rows-3)*CHAR_H}" to="{H+CHAR_H}" dur="{dur}s" begin="{delay}s" repeatCount="indefinite" />')
        svg.append(f'  </text>')

        # Render head (1 white-green char, at front of stream)
        svg.append(f'  <text x="{x}" y="0" font-family="SFMono-Regular, Consolas, \'Liberation Mono\', Menlo, monospace" font-size="{FONT_SIZE}" fill="{head_col}" font-weight="bold" dominant-baseline="hanging">{chars[0]}')
        svg.append(f'    <animate attributeName="y" from="-{CHAR_H}" to="{H+CHAR_H}" dur="{dur}s" begin="{delay}s" repeatCount="indefinite" />')
        svg.append(f'  </text>')

        # Highlighted name column: overlay the repo name as a fixed bright label
        if is_hl and name:
            name_y = H // 2 - (len(name) * CHAR_H) // 2
            svg.append(f'  <text x="{x}" y="{name_y}" font-family="SFMono-Regular, Consolas, \'Liberation Mono\', Menlo, monospace" font-size="{FONT_SIZE}" fill="{HIGHLIGHT}" font-weight="bold" xml:space="preserve">')
            for j, ch in enumerate(name):
                svg.append(f'    <tspan x="{x}" dy="{CHAR_H}">{ch}</tspan>')
            svg.append(f'  </text>')

    # ── Vignette overlays ──────────────────────────────────────────────────
    svg.append(f'  <rect width="{W}" height="{H}" rx="10" fill="url(#fadeTop)" />')
    svg.append(f'  <rect width="{W}" height="{H}" rx="10" fill="url(#fadeBot)" />')

    # ── Centre overlay: username ───────────────────────────────────────────
    # Semi-transparent backing
    label = "ROXY"
    label_w = len(label) * 44
    label_x = W // 2 - label_w // 2 - 14
    label_y = H // 2 - 24
    svg.append(f'  <rect x="{label_x}" y="{label_y}" width="{label_w+28}" height="48" rx="8" fill="{BG_COLOR}" fill-opacity="0.88" stroke="#382a5c" stroke-width="1" />')
    svg.append(f'  <text x="{W//2}" y="{label_y+34}" text-anchor="middle" font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', Helvetica, Arial, sans-serif" font-size="32" font-weight="800" letter-spacing="8" fill="{LEAD_COLOR}" opacity="0.95">{label}</text>')

    # Subtitle
    svg.append(f'  <text x="{W//2}" y="{label_y+52}" text-anchor="middle" font-family="SFMono-Regular, Consolas, \'Liberation Mono\', Menlo, monospace" font-size="11" fill="#38bdf8" letter-spacing="2">ANDROID  ·  TELEGRAM BOTS  ·  AUTOMATION</text>')

    # Border
    svg.append(f'  <rect width="{W}" height="{H}" rx="12" fill="none" stroke="#2e274a" stroke-width="1.5" />')

    svg.append('</svg>')

    content = "\n".join(svg)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generated matrix rain: {output_path} — {num_cols} columns, {len(highlight_cols)} highlighted")

if __name__ == "__main__":
    generate_matrix()
