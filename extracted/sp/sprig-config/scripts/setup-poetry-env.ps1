# scripts/setup-poetry-env.ps1
$PY = py -3.13 -c "import sys; print(sys.executable)"
poetry env use "$PY"
poetry config virtualenvs.in-project true
poetry env remove --all
poetry install