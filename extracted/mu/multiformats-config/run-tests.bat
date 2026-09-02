@echo off
mypy --strict multiformats_config
pylint --rcfile=.pylintrc --disable=fixme multiformats_config
@pause
