"""
make_banner_svg.py
Ultra-premium Cyberpunk Banner SVG for RoxyBasicNeedBot
Featuring multi-layer neon glow, particle field, animated typography,
4 dynamic stat pills, rotating dual-ring tech insignia, and live status badge.
SMIL only (100% GitHub-safe).
"""
import json
import os

def load_stats():
    repos = []
    contrib = {}
    if os.path.exists("data/repo_stats.json"):
        try:
            with open("data/repo_stats.json", encoding="utf-8") as f:
                repos = json.load(f)
        except Exception:
            pass
    if os.path.exists("data/contributions.json"):
        try:
            with open("data/contributions.json", encoding="utf-8") as f:
                contrib = json.load(f)
        except Exception:
            pass

    total_stars = sum(r.get("stars", 0) for r in repos) or 248
    total_forks = sum(r.get("forks", 0) for r in repos) or 131
    total_repos = len(repos) or 13
    total_contrib = contrib.get("total_contributions", 233)
    return total_stars, total_forks, total_repos, total_contrib

def generate_banner(output_path="banner.svg"):
    W, H = 860, 210
    total_stars, total_forks, total_repos, total_contrib = load_stats()

    particles = [
        (45,30),(110,48),(180,24),(260,52),(340,22),(430,42),(520,20),(610,50),(700,28),
        (75,95),(155,75),(235,105),(315,68),(395,92),(485,78),(575,102),(665,82),
        (35,155),(115,138),(195,168),(285,135),(375,162),(465,140),(555,168),(645,145),
        (85,190),(175,182),(265,195),(355,178),(445,192),(535,180),(625,192),
    ]

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H}" width="{W}" height="{H}">')

    svg.append('  <defs>')
    # Deep Cyberpunk Background
    svg.append('    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">')
    svg.append('      <stop offset="0%"   stop-color="#080a14" />')
    svg.append('      <stop offset="45%"  stop-color="#0d101e" />')
    svg.append('      <stop offset="100%" stop-color="#170f2d" />')
    svg.append('    </linearGradient>')
    # Left violet glow
    svg.append('    <radialGradient id="glowL" cx="0%" cy="40%" r="65%">')
    svg.append('      <stop offset="0%"   stop-color="#8b5cf6" stop-opacity="0.6" />')
    svg.append('      <stop offset="60%"  stop-color="#6d28d9" stop-opacity="0.2" />')
    svg.append('      <stop offset="100%" stop-color="#0d101e" stop-opacity="0" />')
    svg.append('    </radialGradient>')
    # Right cyan glow
    svg.append('    <radialGradient id="glowR" cx="100%" cy="60%" r="65%">')
    svg.append('      <stop offset="0%"   stop-color="#06b6d4" stop-opacity="0.5" />')
    svg.append('      <stop offset="60%"  stop-color="#0891b2" stop-opacity="0.15" />')
    svg.append('      <stop offset="100%" stop-color="#0d101e" stop-opacity="0" />')
    svg.append('    </radialGradient>')
    # Text gradient for main title
    svg.append('    <linearGradient id="textGrad" x1="0%" y1="0%" x2="100%" y2="0%">')
    svg.append('      <stop offset="0%"   stop-color="#ffffff" />')
    svg.append('      <stop offset="50%"  stop-color="#e0e7ff" />')
    svg.append('      <stop offset="100%" stop-color="#c084fc" />')
    svg.append('    </linearGradient>')
    # Accent line gradient
    svg.append('    <linearGradient id="lineGrad" x1="0%" y1="0%" x2="100%" y2="0%">')
    svg.append('      <stop offset="0%"   stop-color="#a855f7" />')
    svg.append('      <stop offset="60%"  stop-color="#38bdf8" />')
    svg.append('      <stop offset="100%" stop-color="#06b6d4" />')
    svg.append('    </linearGradient>')
    # Scanline grid pattern
    svg.append('    <pattern id="scan" x="0" y="0" width="1" height="4" patternUnits="userSpaceOnUse">')
    svg.append('      <rect x="0" y="0" width="1" height="1" fill="#ffffff" fill-opacity="0.016" />')
    svg.append('    </pattern>')
    svg.append('  </defs>')

    # ── Background ────────────────────────────────────────────────────────────
    svg.append(f'  <rect width="{W}" height="{H}" rx="14" fill="url(#bgGrad)" />')
    svg.append(f'  <rect width="{W}" height="{H}" rx="14" fill="url(#glowL)" />')
    svg.append(f'  <rect width="{W}" height="{H}" rx="14" fill="url(#glowR)" />')
    svg.append(f'  <rect width="{W}" height="{H}" rx="14" fill="url(#scan)" />')

    # Dual layered border
    svg.append(f'  <rect width="{W}" height="{H}" rx="14" fill="none" stroke="#2d2249" stroke-width="1.5" />')
    svg.append(f'  <rect x="2" y="2" width="{W-4}" height="{H-4}" rx="12" fill="none" stroke="#a855f7" stroke-opacity="0.15" stroke-width="1" />')

    # ── Ambient Star Particles ────────────────────────────────────────────────
    colors = ["#a855f7", "#06b6d4", "#ec4899", "#38bdf8", "#c084fc", "#f43f5e"]
    for i, (px, py) in enumerate(particles):
        r = [1.2, 1.7, 2.2, 1.4][i % 4]
        col = colors[i % len(colors)]
        dur = [3.2, 4.0, 4.8, 3.6, 4.4][i % 5]
        begin = round(i * 0.11, 2)
        svg.append(f'  <circle cx="{px}" cy="{py}" r="{r}" fill="{col}" opacity="0">')
        svg.append(f'    <animate attributeName="opacity" values="0;0.85;0" dur="{dur}s" begin="{begin}s" repeatCount="indefinite" />')
        svg.append('  </circle>')

    # ── Top Sub-Badge: Status & Mode ──────────────────────────────────────────
    svg.append('  <g opacity="0">')
    svg.append('    <animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="0.2s" fill="freeze" />')
    # Status capsule
    svg.append('    <rect x="50" y="32" width="135" height="22" rx="11" fill="#140f28" stroke="#3b2b5f" stroke-width="1" />')
    # Blinking green dot
    svg.append('    <circle cx="62" cy="43" r="4" fill="#34d399">')
    svg.append('      <animate attributeName="opacity" values="1;0.3;1" dur="1.8s" repeatCount="indefinite" />')
    svg.append('    </circle>')
    svg.append('    <text x="73" y="47" font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', Helvetica, Arial, sans-serif" font-size="10" font-weight="700" fill="#38bdf8" letter-spacing="1">SYSTEM ACTIVE</text>')
    # Cloud Tag
    svg.append('    <rect x="195" y="32" width="105" height="22" rx="11" fill="#140f28" stroke="#3b2b5f" stroke-width="1" />')
    svg.append('    <text x="247" y="47" text-anchor="middle" font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', Helvetica, Arial, sans-serif" font-size="10" font-weight="700" fill="#c084fc" letter-spacing="1">24/7 BOT FLEET</text>')
    svg.append('  </g>')

    # ── Main Name Heading ─────────────────────────────────────────────────────
    svg.append(f'  <text font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', Helvetica, Arial, sans-serif" font-size="44" font-weight="900" fill="url(#textGrad)" x="50" y="104" letter-spacing="-0.8" opacity="0">')
    svg.append(f'    RoxyBasicNeedBot ⚡')
    svg.append(f'    <animate attributeName="opacity" from="0" to="1" dur="0.6s" begin="0.35s" fill="freeze" />')
    svg.append(f'    <animate attributeName="x" from="40" to="50" dur="0.6s" begin="0.35s" fill="freeze" />')
    svg.append('  </text>')

    # ── Role Tagline with accent dot separators ───────────────────────────────
    svg.append(f'  <text font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', Helvetica, Arial, sans-serif" font-size="14.5" font-weight="500" fill="#94a3b8" x="52" y="132" opacity="0">')
    svg.append(f'    Android Developer   •   Telegram Bot Architect   •   Automation Wizard')
    svg.append(f'    <animate attributeName="opacity" from="0" to="1" dur="0.6s" begin="0.75s" fill="freeze" />')
    svg.append('  </text>')

    # ── 4 Stats Metric Pills ──────────────────────────────────────────────────
    pills = [
        (f"★ {total_stars}+ Stars",   "#fbbf24", 50,  116),
        (f"⑂ {total_forks}+ Forks",   "#06b6d4", 176, 116),
        (f"◫ {total_repos} Repos",     "#a855f7", 302, 108),
        (f"⚡ {total_contrib} Contribs","#ec4899", 420, 126),
    ]
    for label, color, px, pw in pills:
        svg.append(f'  <rect x="{px}" y="152" width="{pw}" height="26" rx="13" fill="{color}" fill-opacity="0.12" stroke="{color}" stroke-opacity="0.45" stroke-width="1.2" opacity="0">')
        svg.append(f'    <animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="1.0s" fill="freeze" />')
        svg.append('  </rect>')
        svg.append(f'  <text x="{px+pw//2}" y="169" text-anchor="middle" font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', Helvetica, Arial, sans-serif" font-size="11.5" font-weight="700" fill="{color}" opacity="0">{label}')
        svg.append(f'    <animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="1.0s" fill="freeze" />')
        svg.append('  </text>')

    # ── Right Tech Insignia Crest ─────────────────────────────────────────────
    cx, cy = 745, 105
    # Ambient backing aura
    svg.append(f'  <circle cx="{cx}" cy="{cy}" r="74" fill="#140f28" stroke="#37265a" stroke-width="1.5" opacity="0">')
    svg.append(f'    <animate attributeName="opacity" from="0" to="1" dur="0.6s" begin="0.5s" fill="freeze" />')
    svg.append('  </circle>')

    # Outer clockwise rotating dashed neon ring
    svg.append(f'  <circle cx="{cx}" cy="{cy}" r="80" fill="none" stroke="#a855f7" stroke-width="2" stroke-dasharray="14 8 4 8" opacity="0">')
    svg.append(f'    <animate attributeName="opacity" from="0" to="0.75" dur="0.6s" begin="0.7s" fill="freeze" />')
    svg.append(f'    <animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="22s" repeatCount="indefinite" />')
    svg.append('  </circle>')

    # Inner counter-clockwise rotating cyan ring
    svg.append(f'  <circle cx="{cx}" cy="{cy}" r="64" fill="none" stroke="#06b6d4" stroke-width="1.5" stroke-dasharray="6 6" opacity="0">')
    svg.append(f'    <animate attributeName="opacity" from="0" to="0.55" dur="0.5s" begin="0.8s" fill="freeze" />')
    svg.append(f'    <animateTransform attributeName="transform" type="rotate" from="360 {cx} {cy}" to="0 {cx} {cy}" dur="16s" repeatCount="indefinite" />')
    svg.append('  </circle>')

    # Hexagonal / Diamond inner shield
    svg.append(f'  <polygon points="{cx},{cy-42} {cx+36},{cy-20} {cx+36},{cy+22} {cx},{cy+44} {cx-36},{cy+22} {cx-36},{cy-20}" fill="#1a1236" stroke="#c084fc" stroke-width="1.5" opacity="0">')
    svg.append(f'    <animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="0.85s" fill="freeze" />')
    svg.append('  </polygon>')

    # Insignia Initials & Lightning
    svg.append(f'  <text x="{cx}" y="{cy-5}" text-anchor="middle" font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', Helvetica, Arial, sans-serif" font-size="20" font-weight="900" fill="#f8fafc" opacity="0">⚡')
    svg.append(f'    <animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="0.95s" fill="freeze" />')
    svg.append('  </text>')
    svg.append(f'  <text x="{cx}" y="{cy+18}" text-anchor="middle" font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', Helvetica, Arial, sans-serif" font-size="18" font-weight="900" fill="#a855f7" letter-spacing="2" opacity="0">RB')
    svg.append(f'    <animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="0.95s" fill="freeze" />')
    svg.append('  </text>')

    svg.append('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"Generated banner: {output_path}")

if __name__ == "__main__":
    generate_banner()
