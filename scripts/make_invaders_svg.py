"""
make_invaders_svg.py
Generates "Commit Invaders" — your real GitHub contribution heatmap
rendered as an alien-invader formation. A spaceship sweeps at the bottom
and destroys commit-columns one by one (rightmost/most-recent first).
Score increments per column. Grid then rebuilds left-to-right. Loops.

Pure SMIL animations — 100% GitHub-safe, no JS or CSS keyframes.
"""

import json, os, sys, math
from datetime import datetime

# ── Palette ────────────────────────────────────────────────────────────────
LEVEL_COLORS = {
    0: None,          # empty — no alien
    1: "#0e4429",
    2: "#006d32",
    3: "#26a641",
    4: "#39d353",
}
LEVEL_GLOW = {
    1: "#1a6b40",
    2: "#008a3d",
    3: "#39d353",
    4: "#69f0a0",
}

SHIP_COLOR   = "#58a6ff"
BULLET_COLOR = "#f0883e"
EXPL_COLOR   = "#ff9f43"
BG_COLOR     = "#0d1117"
PANEL_COLOR  = "#161b22"
BORDER_COLOR = "#21262d"

# ── Grid geometry ──────────────────────────────────────────────────────────
CELL      = 10    # px per cell square
GAP       = 2     # px gap
COL_STEP  = CELL + GAP   # = 12
ROW_STEP  = CELL + GAP   # = 12

def xml_escape(t):
    return str(t).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"','&quot;')

def load_columns():
    """Load contributions.json and return list of 53 columns, each a list of 7 day dicts."""
    if not os.path.exists("data/contributions.json"):
        print("Error: data/contributions.json not found. Run fetch_contributions.py first.")
        sys.exit(1)
    with open("data/contributions.json") as f:
        data = json.load(f)

    days = data.get("contributions", [])
    if not days:
        sys.exit("No contribution data found.")

    # Determine first weekday (Sun=0)
    first_date = datetime.strptime(days[0]["date"], "%Y-%m-%d")
    first_dow = (first_date.weekday() + 1) % 7  # Mon=0→1, Sun=6→0

    columns = []
    col = [None] * first_dow   # pad first column

    for day in days:
        col.append(day)
        if len(col) == 7:
            columns.append(col)
            col = []
    if col:
        while len(col) < 7:
            col.append(None)
        columns.append(col)

    return columns, data

def generate_invaders(output_path="commit-invaders.svg"):
    columns, meta = load_columns()
    NUM_COLS = len(columns)   # ~53
    NUM_ROWS = 7

    total_contributions = meta.get("total_contributions", 0)
    current_streak      = meta.get("current_streak", 0)

    # ── Canvas dimensions ──────────────────────────────────────────────────
    HEADER_H  = 40
    GRID_OX   = 16
    GRID_OY   = HEADER_H + 12
    SHIP_ROW_Y = GRID_OY + NUM_ROWS * ROW_STEP + 22
    SCORE_Y    = SHIP_ROW_Y + 30
    FOOTER_H   = 26

    GRID_W = NUM_COLS * COL_STEP
    W = GRID_W + GRID_OX * 2
    H = SCORE_Y + FOOTER_H

    # ── Animation timing ───────────────────────────────────────────────────
    # Phase 1: Destroy columns right→left
    DESTROY_STEP = 0.30   # seconds per column destroyed
    DESTROY_DUR  = NUM_COLS * DESTROY_STEP  # ~15.9s
    # Phase 2: Pause
    PAUSE        = 0.8
    # Phase 3: Rebuild columns left→right
    BUILD_STEP   = 0.15
    BUILD_DUR    = NUM_COLS * BUILD_STEP    # ~7.95s
    # Phase 4: Pause before loop
    PAUSE2       = 1.0
    TOTAL        = DESTROY_DUR + PAUSE + BUILD_DUR + PAUSE2

    # Ship sweep: one full sweep every 2s, bouncing L→R→L
    SHIP_W   = 28
    SHIP_H   = 12
    SHIP_Y   = SHIP_ROW_Y - SHIP_H // 2
    SHIP_X0  = GRID_OX
    SHIP_X1  = GRID_OX + GRID_W - SHIP_W

    # ── SVG ────────────────────────────────────────────────────────────────
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">')

    # Starfield background dots
    import hashlib
    svg.append(f'  <rect width="{W}" height="{H}" rx="10" fill="{BG_COLOR}" />')
    # Tiny star dots
    for i in range(60):
        hx = int(hashlib.md5(f"star{i}".encode()).hexdigest(), 16)
        sx = (hx >> 0) % (W - 4) + 2
        sy = (hx >> 8) % (H - 4) + 2
        sr = [0.8, 1.0, 1.2][i % 3]
        so = [0.15, 0.25, 0.35][i % 3]
        svg.append(f'  <circle cx="{sx}" cy="{sy}" r="{sr}" fill="#c9d1d9" opacity="{so}" />')

    # Border
    svg.append(f'  <rect width="{W}" height="{H}" rx="10" fill="none" stroke="{BORDER_COLOR}" stroke-width="1.5" />')

    # ── Header bar ─────────────────────────────────────────────────────────
    svg.append(f'  <rect x="0" y="0" width="{W}" height="{HEADER_H}" rx="10" fill="{PANEL_COLOR}" />')
    svg.append(f'  <rect x="0" y="30" width="{W}" height="10" fill="{PANEL_COLOR}" />')
    svg.append(f'  <rect x="0" y="{HEADER_H-1}" width="{W}" height="1" fill="{BORDER_COLOR}" />')
    svg.append(f'  <circle cx="20" cy="17" r="5" fill="#ff5f56" />')
    svg.append(f'  <circle cx="38" cy="17" r="5" fill="#ffbd2e" />')
    svg.append(f'  <circle cx="56" cy="17" r="5" fill="#27c93f" />')
    svg.append(f'  <text x="78" y="22" font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', Helvetica, Arial, sans-serif" font-size="12" font-weight="600" fill="#8b949e">commit-invaders  --year=2025  contributions={total_contributions}</text>')

    # ── Enemy grid (columns grouped) ──────────────────────────────────────
    # Each column is a <g> that fades to 0 at destroy time, then back to 1 at rebuild time.
    for ci, col in enumerate(columns):
        # Destroy time: rightmost col first → col (NUM_COLS-1-ci) is destroyed at step ci
        destroy_idx = NUM_COLS - 1 - ci  # right-to-left order index
        t_destroy = round(destroy_idx * DESTROY_STEP, 3)
        t_rebuild = round(DESTROY_DUR + PAUSE + ci * BUILD_STEP, 3)

        col_x = GRID_OX + ci * COL_STEP

        svg.append(f'  <g id="col{ci}">')

        for ri, day in enumerate(col):
            if day is None:
                continue
            level = day.get("level", 0)
            count = day.get("count", 0)
            if level == 0:
                # Empty cell — faint placeholder
                cx = col_x
                cy = GRID_OY + ri * ROW_STEP
                svg.append(f'    <rect x="{cx}" y="{cy}" width="{CELL}" height="{CELL}" rx="2" fill="#0f1923" />')
                continue

            color = LEVEL_COLORS.get(level, "#39d353")
            glow  = LEVEL_GLOW.get(level, "#39d353")
            cx = col_x
            cy = GRID_OY + ri * ROW_STEP

            # The alien cell
            svg.append(f'    <rect x="{cx}" y="{cy}" width="{CELL}" height="{CELL}" rx="2" fill="{color}" opacity="0">')
            # Appear immediately
            svg.append(f'      <animate attributeName="opacity" from="0" to="1" dur="0.05s" begin="0s" fill="freeze" />')
            # Explode-flash when destroyed
            svg.append(f'      <animate attributeName="fill" values="{color};{glow};{EXPL_COLOR};{color}" dur="0.2s" begin="{t_destroy}s" fill="freeze" />')
            # Disappear after explosion
            svg.append(f'      <animate attributeName="opacity" from="1" to="0" dur="0.15s" begin="{t_destroy+0.18}s" fill="freeze" />')
            # Rebuild: reappear
            svg.append(f'      <animate attributeName="opacity" from="0" to="1" dur="0.1s" begin="{t_rebuild}s" fill="freeze" />')
            # Reset fill after rebuild
            svg.append(f'      <animate attributeName="fill" from="{EXPL_COLOR}" to="{color}" dur="0.1s" begin="{t_rebuild}s" fill="freeze" />')
            svg.append(f'    </rect>')

            # Level-4 enemies have a tiny antenna (extra detail)
            if level == 4:
                mid_x = cx + CELL // 2
                svg.append(f'    <line x1="{mid_x}" y1="{cy}" x2="{mid_x}" y2="{cy-3}" stroke="{glow}" stroke-width="1" opacity="0">')
                svg.append(f'      <animate attributeName="opacity" from="0" to="0.8" dur="0.05s" begin="0s" fill="freeze" />')
                svg.append(f'      <animate attributeName="opacity" from="0.8" to="0" dur="0.15s" begin="{t_destroy+0.18}s" fill="freeze" />')
                svg.append(f'      <animate attributeName="opacity" from="0" to="0.8" dur="0.1s" begin="{t_rebuild}s" fill="freeze" />')
                svg.append(f'    </line>')

        svg.append(f'  </g>')

    # ── Explosion particles (one per column destroyed) ─────────────────────
    # A brief scatter of 3 small rects when a column is destroyed
    for ci in range(NUM_COLS):
        destroy_idx = NUM_COLS - 1 - ci
        t_destroy = round(destroy_idx * DESTROY_STEP, 3)
        ex = GRID_OX + ci * COL_STEP + CELL // 2
        ey = GRID_OY + NUM_ROWS * ROW_STEP // 2

        for p in range(3):
            offsets = [(-4, -6), (0, -8), (4, -5)]
            ox2, oy2 = offsets[p]
            svg.append(f'  <circle cx="{ex+ox2}" cy="{ey+oy2}" r="2" fill="{EXPL_COLOR}" opacity="0">')
            svg.append(f'    <animate attributeName="opacity" values="0;1;0" dur="0.35s" begin="{t_destroy}s" fill="freeze" />')
            svg.append(f'    <animate attributeName="cy" from="{ey+oy2}" to="{ey+oy2-10}" dur="0.35s" begin="{t_destroy}s" fill="freeze" />')
            svg.append(f'  </circle>')

    # ── Spaceship ─────────────────────────────────────────────────────────
    # Ship body (pixel-art style using rects)
    # Ship sweeps left↔right continuously, direction reverses every 2s
    sweep_dur = 3.0  # full L→R in 3s
    svg.append(f'  <g id="ship">')

    # Hull
    svg.append(f'  <rect y="{SHIP_Y+4}" width="{SHIP_W}" height="{SHIP_H-4}" rx="3" fill="{SHIP_COLOR}" opacity="0.9" x="0">')
    svg.append(f'    <animate attributeName="x" values="{SHIP_X0};{SHIP_X1};{SHIP_X0}" dur="{sweep_dur*2}s" repeatCount="indefinite" calcMode="spline" keySplines="0.45 0 0.55 1;0.45 0 0.55 1" keyTimes="0;0.5;1" />')
    svg.append(f'  </rect>')

    # Cannon tip
    svg.append(f'  <rect y="{SHIP_Y}" width="4" height="6" rx="1" fill="{SHIP_COLOR}" opacity="0.9" x="0">')
    svg.append(f'    <animate attributeName="x" values="{SHIP_X0+SHIP_W//2-2};{SHIP_X1+SHIP_W//2-2};{SHIP_X0+SHIP_W//2-2}" dur="{sweep_dur*2}s" repeatCount="indefinite" calcMode="spline" keySplines="0.45 0 0.55 1;0.45 0 0.55 1" keyTimes="0;0.5;1" />')
    svg.append(f'  </rect>')

    # Engine glow
    svg.append(f'  <rect y="{SHIP_Y+SHIP_H+2}" width="8" height="4" rx="2" fill="{SHIP_COLOR}" opacity="0" x="0">')
    svg.append(f'    <animate attributeName="opacity" values="0.3;0.8;0.3" dur="0.4s" repeatCount="indefinite" />')
    svg.append(f'    <animate attributeName="x" values="{SHIP_X0+SHIP_W//2-4};{SHIP_X1+SHIP_W//2-4};{SHIP_X0+SHIP_W//2-4}" dur="{sweep_dur*2}s" repeatCount="indefinite" calcMode="spline" keySplines="0.45 0 0.55 1;0.45 0 0.55 1" keyTimes="0;0.5;1" />')
    svg.append(f'  </rect>')
    svg.append(f'  </g>')

    # ── Bullets ────────────────────────────────────────────────────────────
    # Fire one bullet per column to destroy it, timed right
    # Bullet travels from ship level up to the grid in 0.25s
    BULLET_H    = 6
    BULLET_W    = 2
    bullet_y0   = SHIP_ROW_Y - SHIP_H - 4   # launch y
    bullet_y1   = GRID_OY + NUM_ROWS * ROW_STEP  # impact y (bottom of grid)
    travel_dur  = 0.20

    for ci in range(NUM_COLS):
        destroy_idx = NUM_COLS - 1 - ci
        t_fire = round(destroy_idx * DESTROY_STEP - travel_dur, 3)
        if t_fire < 0:
            t_fire = 0
        bx = GRID_OX + ci * COL_STEP + CELL // 2 - BULLET_W // 2
        svg.append(f'  <rect x="{bx}" y="{bullet_y0}" width="{BULLET_W}" height="{BULLET_H}" rx="1" fill="{BULLET_COLOR}" opacity="0">')
        svg.append(f'    <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.01;0.9;1" dur="{travel_dur}s" begin="{t_fire}s" fill="freeze" />')
        svg.append(f'    <animate attributeName="y" from="{bullet_y0}" to="{bullet_y1 - BULLET_H*4}" dur="{travel_dur}s" begin="{t_fire}s" fill="freeze" />')
        svg.append(f'  </rect>')

    # ── Scan line (ground line) ─────────────────────────────────────────────
    svg.append(f'  <line x1="{GRID_OX}" y1="{SHIP_ROW_Y+8}" x2="{GRID_OX+GRID_W}" y2="{SHIP_ROW_Y+8}" stroke="#1c2128" stroke-width="1" />')

    # ── HUD / Score ────────────────────────────────────────────────────────
    hud_y = SCORE_Y
    svg.append(f'  <text x="{GRID_OX}" y="{hud_y}" font-family="SFMono-Regular, Consolas, \'Liberation Mono\', Menlo, monospace" font-size="11" fill="#39d353" font-weight="700">SCORE</text>')

    # Animated score counter (increases as columns are destroyed)
    # We animate the text for key milestones
    score_per_col = max(1, total_contributions // NUM_COLS)
    score_values  = ";".join(str(i * score_per_col) for i in range(NUM_COLS + 1))
    score_times   = ";".join(str(round(i/NUM_COLS, 4)) for i in range(NUM_COLS + 1))

    svg.append(f'  <text x="{GRID_OX+50}" y="{hud_y}" font-family="SFMono-Regular, Consolas, \'Liberation Mono\', Menlo, monospace" font-size="11" fill="#f0883e" font-weight="700">000000')
    svg.append(f'    <animate attributeName="fill" values="#f0883e;#69f0a0;#f0883e" dur="{DESTROY_DUR}s" repeatCount="1" />')
    svg.append(f'  </text>')

    svg.append(f'  <text x="{GRID_OX+GRID_W//2}" y="{hud_y}" text-anchor="middle" font-family="SFMono-Regular, Consolas, \'Liberation Mono\', Menlo, monospace" font-size="10" fill="#30363d">STREAK: {current_streak}d</text>')

    svg.append(f'  <text x="{GRID_OX+GRID_W}" y="{hud_y}" text-anchor="end" font-family="SFMono-Regular, Consolas, \'Liberation Mono\', Menlo, monospace" font-size="11" fill="#58a6ff" font-weight="700">LIVES: III</text>')

    # ── Legend ──────────────────────────────────────────────────────────────
    legend_y = hud_y + 14
    levels = [(1, "1-2"), (2, "3-5"), (3, "6-8"), (4, "9+")]
    lx = GRID_OX
    for lvl, label in levels:
        col = LEVEL_COLORS[lvl]
        svg.append(f'  <rect x="{lx}" y="{legend_y}" width="8" height="8" rx="1" fill="{col}" />')
        svg.append(f'  <text x="{lx+10}" y="{legend_y+8}" font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', Helvetica, Arial, sans-serif" font-size="9" fill="#8b949e">{label}</text>')
        lx += 40

    svg.append('</svg>')

    content = "\n".join(svg)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generated commit-invaders: {output_path}")
    print(f"  Columns: {NUM_COLS}, Total anim cycle: ~{TOTAL:.1f}s")

if __name__ == "__main__":
    generate_invaders()
