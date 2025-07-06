from pathlib import Path
from importlib import resources

# Use once, everywhere else imports this
PACKAGE_ROOT = Path(resources.files("intctl"))   # → …/site-packages/intctl

def k8s_path(*parts: str) -> Path:
    return PACKAGE_ROOT / "k8s" / Path(*parts)

def terraform_path(*parts: str) -> Path:
    return PACKAGE_ROOT / "terraform" / Path(*parts)

def scripts_path(*parts: str) -> Path:
    return PACKAGE_ROOT / "scripts" / Path(*parts)