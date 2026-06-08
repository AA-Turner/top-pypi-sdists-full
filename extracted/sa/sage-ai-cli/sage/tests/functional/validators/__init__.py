import subprocess
import sys
import hashlib
from pathlib import Path

def validate_file(path: Path, criteria: dict):
    if "extension" in criteria:
        assert path.suffix == criteria["extension"], f"Expected extension {criteria['extension']}, got {path.suffix}"
    
    if path.suffix == ".pdf":
        with open(path, "rb") as f:
            header = f.read(4)
            assert header == b"%PDF", f"Invalid PDF header: {header}"
            
        if "contains" in criteria:
            import PyPDF2
            with open(path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                text_content = ""
                for page in reader.pages:
                    text_content += page.extract_text()
                assert criteria["contains"] in text_content, f"PDF does not contain required text: {criteria['contains']}"
            
    elif criteria.get("type") == "code":
        if path.suffix == ".py":
            subprocess.run([sys.executable, "-m", "py_compile", str(path)], check=True)
            if "contains" in criteria:
                content = path.read_text()
                assert criteria["contains"] in content, f"Code does not contain required logic: {criteria['contains']}"
                
    elif "contains" in criteria:
        content = path.read_bytes()
        assert criteria["contains"].encode() in content, f"File does not contain {criteria['contains']}"
    
    if "sha256" in criteria:
        sha = hashlib.sha256(path.read_bytes()).hexdigest()
        assert sha == criteria["sha256"], f"Checksum mismatch"

def validate_media(path: Path, criteria: dict):
    if "extension" in criteria:
        assert path.suffix == criteria["extension"], f"Expected extension {criteria['extension']}, got {path.suffix}"
        
    if path.suffix == ".png":
        with open(path, "rb") as f:
            header = f.read(8)
            assert header == b"\x89PNG\r\n\x1a\n", "Not a valid PNG file based on magic bytes"
            
    if path.suffix in [".mp4", ".mp3", ".wav"]:
        cmd = ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", "-show_streams", str(path)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        assert result.returncode == 0, f"ffprobe failed: {result.stderr}"

def validate_website(path: Path, criteria: dict):
    assert path.exists(), "Website entry point missing"
    content = path.read_text()
    if criteria.get("valid_html"):
        assert "<html>" in content.lower() or "import react" in content.lower() or "export default" in content.lower()
        assert "<body>" in content.lower() or "<div" in content.lower()
