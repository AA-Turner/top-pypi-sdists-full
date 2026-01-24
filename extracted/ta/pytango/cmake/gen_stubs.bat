
@echo running pybind11-stubgen via cmake\generate_stubs_for_windows.py
python cmake\generate_stubs_for_windows.py tango --ignore-all-errors "--enum-class-locations=DevState|AttrWriteType|LevelLevel|ErrSeverity:tango"

where ruff >nul 2>nul
if %errorlevel%==0 (
    @echo "ruff check and fix:"
    ruff check --fix --select I,D207,D208,D209,D212,PYI009 stubs\tango\__init__.pyi stubs\tango\_tango\__init__.pyi
    @echo "ruff format:"
    ruff format stubs\tango\__init__.pyi stubs\tango\_tango\__init__.pyi
) else (
    @echo "ruff not installed - skipping checks and fixes"
)
