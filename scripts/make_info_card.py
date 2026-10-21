"""
make_info_card.py
Neofetch-style identity card for RoxyBasicNeedBot with terminal header,
custom icons, neon cyberpunk colors, and SMIL animations.
"""
import os

def xml_escape(t):
    return t.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"','&quot;')

def generate_info_card(output_path="info-card.svg", static_mode=False):
    is_static = os.environ.get("STATIC") == "1" or static_mode
    W, H = 490, 490

    ICONS = {
        "user":     "M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2M12 3a4 4 0 1 0 0 8 4 4 0 0 0 0-8z",
        "cpu":      "M9 3H5a2 2 0 0 0-2 2v4m6-6h10a2 2 0 0 1 2 2v4M9 3v18m0 0h10a2 2 0 0 0 2-2V9M9 21H5a2 2 0 0 1-2-2V9m0 0h18",
        "zap":      "M13 2L3 14h9l-1 8 10-12h-9l1-8z",
        "terminal": "M4 17l6-6-6-6M12 19h8",
        "code":     "M16 18l6-6-6-6M8 6l-6 6 6 6",
        "layers":   "M12 2l10 6.5-10 6.5L2 8.5zM2 15.5l10 6.5 10-6.5M2 11l10 6.5L22 11",
        "globe":    "M2 12a10 10 0 1 0 20 0A10 10 0 0 0 2 12zM12 2a14.5 14.5 0 0 1 0 20A14.5 14.5 0 0 1 12 2zM2 12h20",
        "arrow":    "M5 12h14M12 5l7 7-7 7",
    }

    def icon_svg(key, ox, oy, size=13, color="#8b949e"):
        d = ICONS.get(key, "")
        scale = size / 24.0
        return f'<path d="{d}" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" fill="none" transform="translate({ox},{oy}) scale({scale:.4f})" />'

    # (icon_key, key_label, value_text, value_color, key_color, is_spacer)
    rows = [
        ("terminal", "roxy",     "~ % neofetch --profile",       "#a855f7", "#a855f7", False),
        ("user",     "User",     "RoxyBasicNeedBot ⚡",          "#f8fafc", "#06b6d4", False),
        ("cpu",      "Role",     "Android & Bot Engineer",       "#f8fafc", "#06b6d4", False),
        ("zap",      "Uptime",   "24/7  Active Cloud",           "#34d399", "#06b6d4", False),
        ("terminal", "OS",       "Linux • Android • Windows",    "#f8fafc", "#06b6d4", False),
        ("code",     "Core",     "Kotlin • Python",              "#f8fafc", "#06b6d4", False),
        ("layers",   "Framework","Jetpack Compose • Pyrogram",   "#c084fc", "#06b6d4", False),
        ("layers",   "Database", "MongoDB • Room DB",            "#c084fc", "#06b6d4", False),
        (None,       "",         "",                             "",        "",        True),
        ("zap",      "Android",  "Flare • KDownloader • Vivx",   "#f43f5e", "#f43f5e", False),
        ("globe",    "Bots",     "4GB Rename • Video Leech",     "#ec4899", "#ec4899", False),
        ("arrow",    "Telegram", "@roxybasicneedbot1",           "#38bdf8", "#38bdf8", False),
        ("globe",    "Website",  "roxybasicneedbot.unaux.com",   "#38bdf8", "#38bdf8", False),
        (None,       "",         "",                             "",        "",        True),
        ("arrow",    "roxy",     "github ~ % _",                 "#a855f7", "#a855f7", False),
    ]

    line_h = 30
    spacer_h = 10
    start_y = 70

    y_positions = []
    y = start_y
    for row in rows:
        y_positions.append(y)
        if row[5]:  # spacer
            y += spacer_h
        else:
            y += line_h

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">')
    svg.append(f'  <rect width="{W}" height="{H}" rx="12" fill="#0d111a" stroke="#2e274a" stroke-width="1.5" />')
    # Terminal header bar
    svg.append(f'  <rect x="0" y="0" width="{W}" height="40" rx="12" fill="#140f28" />')
    svg.append(f'  <rect x="0" y="30" width="{W}" height="10" fill="#140f28" />')
    svg.append(f'  <rect x="0" y="39" width="{W}" height="1" fill="#382a5c" />')
    svg.append(f'  <circle cx="20" cy="17" r="5.5" fill="#ff5f56" />')
    svg.append(f'  <circle cx="40" cy="17" r="5.5" fill="#ffbd2e" />')
    svg.append(f'  <circle cx="60" cy="17" r="5.5" fill="#27c93f" />')
    svg.append(f'  <text x="82" y="22" font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', Helvetica, Arial, sans-serif" font-size="12" font-weight="600" fill="#a5b4fc">roxy@terminal: ~</text>')

    anim_idx = 0
    for i, (ic, key, val, vcol, kcol, is_spacer) in enumerate(rows):
        y = y_positions[i]
        if is_spacer:
            continue

        delay = round(0.08 + anim_idx * 0.05, 2)
        anim_idx += 1
        op = '0' if not is_static else '1'

        def anim_tag(d, b):
            return f'<animate attributeName="opacity" from="0" to="1" dur="{d}s" begin="{b}s" fill="freeze" />'

        # Icon
        if ic:
            svg.append(f'  <g opacity="{op}">')
            svg.append(f'    {icon_svg(ic, 22, y - 10, size=13, color=kcol)}')
            if not is_static:
                svg.append(f'    {anim_tag(0.35, delay)}')
            svg.append(f'  </g>')

        # Key label
        if key:
            svg.append(f'  <text x="42" y="{y}" font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', Helvetica, Arial, sans-serif" font-size="13" font-weight="700" fill="{kcol}" opacity="{op}">{xml_escape(key)}')
            if not is_static:
                svg.append(f'    {anim_tag(0.35, delay)}')
            svg.append(f'  </text>')

        # Separator colon
        if key and key not in ("roxy",):
            svg.append(f'  <text x="138" y="{y}" font-family="SFMono-Regular, Consolas, \'Liberation Mono\', Menlo, monospace" font-size="13" fill="#382a5c" opacity="{op}">:</text>')

        # Value
        svg.append(f'  <text x="152" y="{y}" font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', Helvetica, Arial, sans-serif" font-size="13" fill="{vcol}" opacity="{op}">{xml_escape(val)}')
        if not is_static:
            svg.append(f'    {anim_tag(0.35, delay)}')
        svg.append(f'  </text>')

    svg.append('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"Generated info card: {output_path}")

if __name__ == "__main__":
    generate_info_card()
