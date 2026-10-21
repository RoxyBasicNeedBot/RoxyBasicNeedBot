$pythonCmd = if (Test-Path ".venv\Scripts\python.exe") { ".venv\Scripts\python.exe" } else { "python" }

$scripts = @(
    "scripts/make_banner_svg.py",
    "scripts/make_skills_svg.py",
    "scripts/make_stats_card_svg.py",
    "scripts/make_lang_chart_svg.py",
    "scripts/render_repos_svg.py",
    "scripts/make_info_card.py",
    "scripts/make_ascii_svg.py",
    "scripts/render_heatmap_svg.py",
    "scripts/make_matrix_svg.py",
    "scripts/make_invaders_svg.py"
)

foreach ($s in $scripts) {
    Write-Host "Running $s..."
    & $pythonCmd $s
    if ($LASTEXITCODE -ne 0) {
        Write-Host "FAILED: $s"
        exit 1
    }
}
Write-Host "All SVGs generated successfully."
