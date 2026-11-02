"""Optional .env loader for the MANUAL cloud_sync_test.py integration script.
python-dotenv is not a matrx-files dependency; this helper only matters when a
developer runs the live-credential script by hand from a workspace that has it.
"""

try:
    from dotenv import load_dotenv
except ImportError:  # bare venv / no dev workspace — the manual script will rely on real env vars
    def load_dotenv(*a, **k):
        return False

load_dotenv()
