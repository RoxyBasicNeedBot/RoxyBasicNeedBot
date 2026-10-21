"""
make_banner_svg.py
Generates an animated cyberpunk gradient banner SVG for RoxyBasicNeedBot
with particle dots, name reveal, subtitle fade-in, dynamic live stats pills,
and a futuristic avatar insignia.
All animations are SMIL-only (GitHub safe).
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
    total_contrib = contrib.get("total_contributions", 233)
    return total_stars, total_forks, total_contrib

def generate_banner(output_path="banner.svg"):
    W, H = 860, 200
    total_stars, total_forks, total_contrib = load_stats()

    # Organic particle positions
    particles = [
        (60,30),(120,55),(200,20),(300,45),(420,18),(540,38),(660,22),(780,50),
        (90,100),(180,80),(270,110),(360,70),(450,95),(570,85),(690,105),(800,75),
        (40,155),(130,145),(230,165),(340,135),(470,158),(590,142),(710,168),(830,148),
        (75,185),(210,175),(380,190),(520,172),(680,188),(820,178),
    ]

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H}" width="{W}" height="{H}">')

    # ── Defs ──────────────────────────────────────────────────────────────────
    svg.append('  <defs>')
    # Deep Cyberpunk Background: Dark navy to deep obsidian violet
    svg.append('    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">')
    svg.append('      <stop offset="0%"   stop-color="#0a0a16" />')
    svg.append('      <stop offset="50%"  stop-color="#0d111a" />')
    svg.append('      <stop offset="100%" stop-color="#140f28" />')
    svg.append('    </linearGradient>')
    # Left violet glow
    svg.append('    <radialGradient id="glowL" cx="0%" cy="50%" r="60%">')
    svg.append('      <stop offset="0%"   stop-color="#7c3aed" stop-opacity="0.55" />')
    svg.append('      <stop offset="100%" stop-color="#0d1117" stop-opacity="0" />')
    svg.append('    </radialGradient>')
    # Right cyan glow
    svg.append('    <radialGradient id="glowR" cx="100%" cy="50%" r="60%">')
    svg.append('      <stop offset="0%"   stop-color="#06b6d4" stop-opacity="0.45" />')
    svg.append('      <stop offset="100%" stop-color="#0d1117" stop-opacity="0" />')
    svg.append('    </radialGradient>')
    # Line accent gradient
    svg.append('    <linearGradient id="lineGrad" x1="0%" y1="0%" x2="100%" y2="0%">')
    svg.append('      <stop offset="0%"   stop-color="#a855f7" />')
    svg.append('      <stop offset="100%" stop-color="#06b6d4" />')
    svg.append('    </linearGradient>')
    # Scanline pattern
    svg.append('    <pattern id="scan" x="0" y="0" width="1" height="4" patternUnits="userSpaceOnUse">')
    svg.append('      <rect x="0" y="0" width="1" height="1" fill="#ffffff" fill-opacity="0.018" />')
    svg.append('    </pattern>')
    svg.append('  </defs>')

    # ── Background ────────────────────────────────────────────────────────────
    svg.append(f'  <rect width="{W}" height="{H}" rx="12" fill="url(#bgGrad)" />')
    svg.append(f'  <rect width="{W}" height="{H}" rx="12" fill="url(#glowL)" />')
    svg.append(f'  <rect width="{W}" height="{H}" rx="12" fill="url(#glowR)" />')
    svg.append(f'  <rect width="{W}" height="{H}" rx="12" fill="url(#scan)" />')

    # Border with subtle purple tint
    svg.append(f'  <rect width="{W}" height="{H}" rx="12" fill="none" stroke="#2e274a" stroke-width="1.5" />')

    # ── Particles ─────────────────────────────────────────────────────────────
    colors = ["#a855f7", "#06b6d4", "#ec4899", "#38bdf8", "#c084fc", "#30363d"]
    for i, (px, py) in enumerate(particles):
        r = [1.2, 1.6, 2.0, 1.2][i % 4]
        col = colors[i % len(colors)]
        dur = [3.4, 4.2, 5.0, 3.8, 4.6][i % 5]
        begin = round(i * 0.12, 2)
        svg.append(f'  <circle cx="{px}" cy="{py}" r="{r}" fill="{col}" opacity="0">')
        svg.append(f'    <animate attributeName="opacity" values="0;0.75;0" dur="{dur}s" begin="{begin}s" repeatCount="indefinite" />')
        svg.append('  </circle>')

    # ── Accent line ───────────────────────────────────────────────────────────
    svg.append(f'  <rect x="50" y="60" width="0" height="3" rx="1.5" fill="url(#lineGrad)" opacity="0.95">')
    svg.append(f'    <animate attributeName="width" from="0" to="58" dur="0.6s" begin="0.3s" fill="freeze" />')
    svg.append('  </rect>')

    # ── Name text ─────────────────────────────────────────────────────────────
    svg.append(f'  <text font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', Helvetica, Arial, sans-serif" font-size="44" font-weight="800" fill="#f8fafc" x="50" y="110" letter-spacing="-0.5" opacity="0">')
    svg.append(f'    RoxyBasicNeedBot')
    svg.append(f'    <animate attributeName="opacity" from="0" to="1" dur="0.7s" begin="0.4s" fill="freeze" />')
    svg.append(f'    <animate attributeName="x" from="42" to="50" dur="0.6s" begin="0.4s" fill="freeze" />')
    svg.append('  </text>')

    # ── Role tagline ──────────────────────────────────────────────────────────
    svg.append(f'  <text font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', Helvetica, Arial, sans-serif" font-size="14.5" font-weight="500" fill="#94a3b8" x="52" y="138" opacity="0">')
    svg.append(f'    Android Developer  /  Telegram Bot Architect  /  Automation Engineer')
    svg.append(f'    <animate attributeName="opacity" from="0" to="1" dur="0.7s" begin="0.85s" fill="freeze" />')
    svg.append('  </text>')

    # ── Stats pills ───────────────────────────────────────────────────────────
    pills = [
        (f"{total_stars}+ Stars",   "#a855f7", 52,  115),
        (f"{total_forks}+ Forks",   "#06b6d4", 175, 115),
        (f"{total_contrib} Contribs", "#ec4899", 298, 125),
    ]
    for label, color, px, pw in pills:
        svg.append(f'  <rect x="{px}" y="156" width="{pw}" height="25" rx="12.5" fill="{color}" fill-opacity="0.12" stroke="{color}" stroke-opacity="0.45" stroke-width="1" opacity="0">')
        svg.append(f'    <animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="1.1s" fill="freeze" />')
        svg.append('  </rect>')
        svg.append(f'  <text x="{px+pw//2}" y="173" text-anchor="middle" font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', Helvetica, Arial, sans-serif" font-size="11.5" font-weight="600" fill="{color}" opacity="0">{label}')
        svg.append(f'    <animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="1.1s" fill="freeze" />')
        svg.append('  </text>')

    # ── Decorative cyber grid lines ───────────────────────────────────────────
    for gy in range(0, H, 38):
        svg.append(f'  <line x1="{W*0.62}" y1="{gy}" x2="{W}" y2="{gy}" stroke="#221e3b" stroke-width="0.5" />')
    for gx in range(int(W*0.62), W+1, 38):
        svg.append(f'  <line x1="{gx}" y1="0" x2="{gx}" y2="{H}" stroke="#221e3b" stroke-width="0.5" />')

    # ── Right-side decorative cyber badge insignia ────────────────────────────
    cx, cy = 750, 100
    svg.append(f'  <circle cx="{cx}" cy="{cy}" r="64" fill="#140f28" stroke="#3b2d63" stroke-width="1.5" opacity="0">')
    svg.append(f'    <animate attributeName="opacity" from="0" to="1" dur="0.6s" begin="0.6s" fill="freeze" />')
    svg.append('  </circle>')
    # Outer animated neon ring
    svg.append(f'  <circle cx="{cx}" cy="{cy}" r="70" fill="none" stroke="#a855f7" stroke-width="1.8" stroke-dasharray="10 6" opacity="0">')
    svg.append(f'    <animate attributeName="opacity" from="0" to="0.6" dur="0.6s" begin="0.8s" fill="freeze" />')
    svg.append(f'    <animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="24s" repeatCount="indefinite" />')
    svg.append('  </circle>')
    # Inner cyan accent circle
    svg.append(f'  <circle cx="{cx}" cy="{cy}" r="50" fill="none" stroke="#06b6d4" stroke-width="1" stroke-dasharray="4 4" opacity="0">')
    svg.append(f'    <animate attributeName="opacity" from="0" to="0.4" dur="0.5s" begin="0.9s" fill="freeze" />')
    svg.append('  </circle>')
    # Logo text / symbol
    svg.append(f'  <text x="{cx}" y="{cy+8}" text-anchor="middle" font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', Helvetica, Arial, sans-serif" font-size="32" font-weight="800" fill="#a855f7" opacity="0">RB')
    svg.append(f'    <animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="0.9s" fill="freeze" />')
    svg.append('  </text>')

    svg.append('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"Generated banner: {output_path}")

if __name__ == "__main__":
    generate_banner()
