# ======================================== IMPORTS ========================================
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# ======================================== HOOK ========================================
# Embarque tous les fichiers de données
datas = collect_data_files('pyverse2d')

# Embarque les sous-modules cachés
hiddenimports = collect_submodules('pyverse2d')