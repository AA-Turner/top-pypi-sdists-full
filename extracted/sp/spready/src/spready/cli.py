from loguru import logger
import typer
from spready import app, getEnvURL
import json
import os
import logging

from spready.parser import SpreadyDecoratorParser

cliApp = typer.Typer()


@cliApp.command()
def register(credential_path: str):
    result = app.register(getEnvURL())
    with open(credential_path, "w") as f:
        json.dump(result, f)
    print(f"""
          
        ┌───────────────────────────────────────────────┐
        │  Congratulations!                             │
        │                                               │
        │  You've successfully registered your worker   │
        └───────────────────────────────────────────────┘
          
          URL: {getEnvURL()}
          Use `{result['publicKey']}` in API header `x-auth-token` to authenticate

          To create your router module, please refer

          https://driblets.gitbook.io/spready/sproute

        """)


@cliApp.command()
def run(creditial_path: str, module_path: str):
    
    app.run(creditial_path, modulePath=module_path)


if __name__ == "__main__":
    cliApp()