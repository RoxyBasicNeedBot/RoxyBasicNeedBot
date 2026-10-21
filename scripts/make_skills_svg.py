"""
make_skills_svg.py
Categorized Tech-Stack panel for RoxyBasicNeedBot with icons, category labels,
colored badges, and staggered SMIL fade-in animations. SMIL only (GitHub safe).
"""

# (label, category, color, icon_path_d)
SKILLS = [
    # Row 1: Core Languages
    ("Kotlin",          "LANG",    "#a855f7", "M2 3h8l10 9-10 9H2l10-9z"),
    ("Python",          "LANG",    "#38bdf8", "M12 2c-3 0-5 1.5-5 4v2h10V6c0-2.5-2-4-5-4zM7 8H5c-2 0-3 1-3 3v2c0 2 1 3 3 3h2v-4h10v4h2c2 0 3-1 3-3v-2c0-2-1-3-3-3h-2M9 4h1M14 14h1"),
    ("Java",            "LANG",    "#f59e0b", "M9 3c-1 3-4 4-4 8h14c0-4-3-5-4-8M7 19h10M8 22h8M12 3v2"),
    ("JavaScript",      "LANG",    "#facc15", "M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 15h-2v-6h2v6zm0-8h-2V7h2v2z"),

    # Row 2: Android & Mobile
    ("Jetpack Compose", "ANDROID", "#4285f4", "M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"),
    ("Android SDK",     "ANDROID", "#3ddc84", "M2 16v-2a6 6 0 0 1 6-6h8a6 6 0 0 1 6 6v2M10 7V5M14 7V5M7 16h10M9 19h6"),
    ("Coroutines/Flow", "ASYNC",   "#ec4899", "M13 2L3 14h9l-1 8 10-12h-9l1-8z"),
    ("Room DB",         "STORAGE", "#c084fc", "M4 6a8 3 0 1 0 16 0A8 3 0 0 0 4 6zM4 6v6a8 3 0 0 0 16 0V6M4 12v6a8 3 0 0 0 16 0v-6"),

    # Row 3: Telegram & Automation
    ("Pyrogram",        "BOTS",    "#0088cc", "M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z"),
    ("Telegram API",    "BOTS",    "#26a5e4", "M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0zM15 9l-6 3 2 1 4-4-3 5 4 1 2-5z"),
    ("MongoDB",         "DATABASE","#47a248", "M12 2C8 6 7 10 7 14c0 4 2.5 7 5 8 2.5-1 5-4 5-8 0-4-1-8-5-12z"),
    ("WorkManager",     "ANDROID", "#f43f5e", "M12 6v6l4 2M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2z"),

    # Row 4: DevOps & Tools
    ("Docker",          "DEVOPS",  "#2496ed", "M4 19h16a2 2 0 0 0 2-2v-5H2v5a2 2 0 0 0 2 2zM4 10h4v2H4zm6 0h4v2h-4zm6 0h4v2h-4z"),
    ("Linux / Ubuntu",  "OS",      "#fcc624", "M12 2a10 10 0 1 0 0 20A10 10 0 0 0 12 2zM8 14s1.5 2 4 2 4-2 4-2M9 9h.01M15 9h.01"),
    ("Git / CI-CD",     "TOOLS",   "#f05032", "M15 18H9M12 21V9M3 9V6a3 3 0 0 1 3-3h12a3 3 0 0 1 3 3v3"),
    ("REST APIs",       "API",     "#38bdf8", "M21 12H3M3 6h18M3 18h18"),
]

def icon_path(d, ox=0, oy=0, size=15, color="#8b949e"):
    scale = size / 24.0
    return f'<path d="{d}" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" fill="none" transform="translate({ox},{oy}) scale({scale:.4f})" />'

def generate_skills(output_path="skills.svg"):
    W = 860
    cols = 4
    badge_w = 190
    badge_h = 48
    gap_x = 18
    gap_y = 14
    pad_x = 23
    pad_top = 56

    rows = (len(SKILLS) + cols - 1) // cols
    H = pad_top + rows * (badge_h + gap_y) + 24

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">')

    # Main panel
    svg.append(f'  <rect width="{W}" height="{H}" rx="14" fill="#0c0e18" stroke="#2b2246" stroke-width="1.5" />')

    # Header bar
    svg.append(f'  <rect x="0" y="0" width="{W}" height="40" rx="14" fill="#140f28" />')
    svg.append(f'  <rect x="0" y="30" width="{W}" height="10" fill="#140f28" />')
    svg.append(f'  <rect x="0" y="39" width="{W}" height="1" fill="#382a5c" />')
    svg.append(f'  <circle cx="20" cy="18" r="5.5" fill="#ff5f56" />')
    svg.append(f'  <circle cx="38" cy="18" r="5.5" fill="#ffbd2e" />')
    svg.append(f'  <circle cx="56" cy="18" r="5.5" fill="#27c93f" />')
    svg.append(f'  <text x="78" y="23" font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', Helvetica, Arial, sans-serif" font-size="12" font-weight="600" fill="#c084fc">roxy@terminal: tech-stack --architecture-matrix</text>')

    for i, (label, category, color, icon_d) in enumerate(SKILLS):
        col_i = i % cols
        row_i = i // cols
        x = pad_x + col_i * (badge_w + gap_x)
        y = pad_top + row_i * (badge_h + gap_y)
        delay = round(0.04 + i * 0.04, 2)

        # Card
        svg.append(f'  <rect x="{x}" y="{y}" width="{badge_w}" height="{badge_h}" rx="8" fill="#130f26" stroke="{color}" stroke-opacity="0.25" stroke-width="1.2" opacity="0">')
        svg.append(f'    <animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="{delay}s" fill="freeze" />')
        svg.append('  </rect>')

        # Accent vertical bar
        svg.append(f'  <rect x="{x}" y="{y+10}" width="3.5" height="{badge_h-20}" rx="1.75" fill="{color}" opacity="0">')
        svg.append(f'    <animate attributeName="opacity" from="0" to="0.95" dur="0.4s" begin="{delay}s" fill="freeze" />')
        svg.append('  </rect>')

        # Icon
        ix = x + 14
        iy = y + 12
        svg.append('  <g opacity="0">')
        svg.append(f'    {icon_path(icon_d, ox=ix, oy=iy, size=16, color=color)}')
        svg.append(f'    <animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="{delay}s" fill="freeze" />')
        svg.append('  </g>')

        # Label
        svg.append(f'  <text x="{x+38}" y="{y+24}" font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', Helvetica, Arial, sans-serif" font-size="12" font-weight="700" fill="#f8fafc" opacity="0">{label}')
        svg.append(f'    <animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="{delay}s" fill="freeze" />')
        svg.append('  </text>')

        # Category micro-badge
        svg.append(f'  <text x="{x+38}" y="{y+38}" font-family="SFMono-Regular, Consolas, \'Liberation Mono\', Menlo, monospace" font-size="9" font-weight="700" fill="{color}" opacity="0">{category}')
        svg.append(f'    <animate attributeName="opacity" from="0" to="0.8" dur="0.4s" begin="{delay}s" fill="freeze" />')
        svg.append('  </text>')

    svg.append('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"Generated skills SVG: {output_path}")

if __name__ == "__main__":
    generate_skills()
