set -exu
source ~/.profile

pip install .[dev]
pip install .[examples]
pytest test
