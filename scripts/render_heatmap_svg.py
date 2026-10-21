import json
import os
import sys
from datetime import datetime

PALETTE = ["#140f28", "#382063", "#6b21a8", "#9333ea", "#c084fc", "#38bdf8"]

def render_heatmap(json_path="data/contributions.json", output_path="contrib-heatmap.svg"):
    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found. Please run fetch_contributions.py first.")
        sys.exit(1)
        
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    contributions = data["contributions"]
    total = data["total_contributions"]
    current_streak = data["current_streak"]
    longest_streak = data["longest_streak"]
    
    if not contributions:
        print("Error: Contributions list is empty.")
        sys.exit(1)
        
    # 1. Arrange days into columns (weeks)
    columns = []
    current_col = []
    
    # First date info
    first_date = datetime.strptime(contributions[0]['date'], "%Y-%m-%d")
    first_weekday = (first_date.weekday() + 1) % 7 # Sunday = 0, Saturday = 6
    
    # Pad the first week with None
    for _ in range(first_weekday):
        current_col.append(None)
        
    for day in contributions:
        current_col.append(day)
        if len(current_col) == 7:
            columns.append(current_col)
            current_col = []
            
    if current_col:
        while len(current_col) < 7:
            current_col.append(None)
        columns.append(current_col)
        
    # Grid parameters
    rect_size = 10
    rect_gap = 3
    num_cols = len(columns)
    
    # Canvas margins and size
    padding_left = 35
    padding_top = 25
    padding_right = 15
    padding_bottom = 45
    
    grid_w = num_cols * (rect_size + rect_gap) - rect_gap
    grid_h = 7 * (rect_size + rect_gap) - rect_gap
    
    width = padding_left + grid_w + padding_right
    height = padding_top + grid_h + padding_bottom
    
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">')
    svg.append('  <style>')
    svg.append('    .bg { fill: #0d111a; stroke: #2e274a; stroke-width: 1.5; }')
    svg.append('    .label { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; font-size: 9px; fill: #8b949e; }')
    svg.append('    .month-label { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; font-size: 9px; fill: #8b949e; font-weight: 500; }')
    svg.append('    .legend-text { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; font-size: 9px; fill: #8b949e; }')
    svg.append('    .stats-text { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; font-size: 10px; fill: #c9d1d9; font-weight: 500; }')
    svg.append('    @keyframes slideIn {')
    svg.append('      from { transform: scale(0); opacity: 0; }')
    svg.append('      to { transform: scale(1); opacity: 1; }')
    svg.append('    }')
    svg.append('    .day {')
    svg.append('      transform-box: fill-box;')
    svg.append('      transform-origin: center;')
    svg.append('      animation: slideIn 0.3s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;')
    svg.append('      opacity: 0;')
    svg.append('    }')
    svg.append('  </style>')
    
    # Outer terminal panel rect
    svg.append(f'  <rect class="bg" width="{width}" height="{height}" rx="8" />')
    
    # Draw Month labels
    months_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    last_month_name = None
    last_label_col = -10
    
    for c_idx, col in enumerate(columns):
        first_day = next((d for d in col if d is not None), None)
        if first_day:
            date_obj = datetime.strptime(first_day['date'], "%Y-%m-%d")
            m_name = months_names[date_obj.month - 1]
            if m_name != last_month_name and (c_idx - last_label_col) >= 3:
                x_pos = padding_left + c_idx * (rect_size + rect_gap)
                svg.append(f'  <text class="month-label" x="{x_pos}" y="17">{m_name}</text>')
                last_month_name = m_name
                last_label_col = c_idx
                
    # Draw Day of week labels on left
    day_labels = ["Mon", "Wed", "Fri"]
    day_label_rows = [1, 3, 5]
    for label, row_idx in zip(day_labels, day_label_rows):
        y_pos = padding_top + row_idx * (rect_size + rect_gap) + 8
        svg.append(f'  <text class="label" x="12" y="{y_pos}">{label}</text>')
        
    # Draw contribution grid cells
    for c_idx, col in enumerate(columns):
        x_pos = padding_left + c_idx * (rect_size + rect_gap)
        for r_idx, day in enumerate(col):
            if day is None:
                continue
            
            y_pos = padding_top + r_idx * (rect_size + rect_gap)
            level = day["level"]
            count = day["count"]
            
            # Map levels to palette
            if level == 4 and count >= 12:
                color = PALETTE[5]  # Neon green for high count days
            else:
                color = PALETTE[level]
                
            delay = round((c_idx + r_idx) * 0.012, 3)
            
            # Tooltip details
            tooltip_title = f"{count} contributions on {day['date']}" if count > 0 else f"No contributions on {day['date']}"
            
            svg.append(f'  <rect class="day" x="{x_pos}" y="{y_pos}" width="{rect_size}" height="{rect_size}" rx="2" fill="{color}" style="animation-delay: {delay}s;">')
            svg.append(f'    <title>{tooltip_title}</title>')
            svg.append('  </rect>')
            
    # Stats footer (bottom left)
    stats_y = height - 18
    stats_string = f"{total:,} contributions in the last year | Current Streak: {current_streak} days | Longest Streak: {longest_streak} days"
    svg.append(f'  <text class="stats-text" x="15" y="{stats_y}">{stats_string}</text>')
    
    # Legend (bottom right)
    legend_start_x = width - padding_right - (len(PALETTE) * (rect_size + rect_gap)) - 65
    svg.append(f'  <text class="legend-text" x="{legend_start_x}" y="{stats_y}">&lt; Less</text>')
    
    for idx, color in enumerate(PALETTE):
        lx = legend_start_x + 38 + idx * (rect_size + rect_gap)
        ly = stats_y - 8
        svg.append(f'  <rect x="{lx}" y="{ly}" width="{rect_size}" height="{rect_size}" rx="2" fill="{color}" />')
        
    legend_end_x = legend_start_x + 40 + len(PALETTE) * (rect_size + rect_gap)
    svg.append(f'  <text class="legend-text" x="{legend_end_x}" y="{stats_y}">More &gt;</text>')
    
    svg.append('</svg>')
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"Generated heatmap SVG: {output_path}")

if __name__ == "__main__":
    render_heatmap()
