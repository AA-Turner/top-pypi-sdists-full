import asyncio
import importlib.metadata
import threading

import inquirer
import psutil
from inquirer.themes import GreenPassion
from rich.console import Console
from typer import Context, Exit, Option, Typer

from worker_automate_hub.api.client import get_workers, load_environments
from worker_automate_hub.core.so_manipulation import (
    add_worker_config,
    download_tesseract,
    update_assets_v2,
    write_env_config,
)
from worker_automate_hub.utils.updater import check_for_update
from worker_automate_hub.utils.util import (
    add_start_on_boot_to_registry,
    create_worker_bat,
)

from .worker import run_worker

console = Console()
app = Typer()
stop_event = threading.Event()  # Evento para parar as threads


HELP_MESSAGE = """
[b]Worker[/] - Grupo Argenta

Forma de uso: [b]worker [SUBCOMANDO] [ARGUMENTOS][/]

Existem 3 subcomandos disponíveis para essa aplicação

- [b]run[/]: Inicializa o Worker na máquina atual e começa a solicitar trabalho para o orquestrador.
- [b]validate[/]: Verifica se o Worker atual está configurado corretamente e pronto para ser inicializado.
- [b]assets[/]: Realiza a limpeza e depois download na pasta assets de todos arquivos utilizado pelo worker durante execução.

[b]Exemplos de uso:[/]
 [b][blue]RUN[/][/]
    [green][b]worker[/][/] [b]run[/]

 [b][blue]UPDATE[/][/]
    [green][b]worker[/][/] [b]update[/]

 [b][blue]VALIDATE[/][/]
    [green][b]worker[/][/] [b]validate[/]

---

[b]Help:[/]
 [b]Para mais informações[/]
    [green][b]worker[/][/] --help

 [b]Para ver a versão instalada[/]
    [green][b]worker[/][/] --version

 [b]Para gerar o arquivo de configuração[/]
    [green][b]worker[/][/] --configure

 [b]Para informações detalhadas
    [blue][link=https://github.com/SIM-Rede/worker-automate-hub]Repo no GIT Argenta[/][/] | [blue][link=https://pypi.org/project/worker-automate-hub/]Publicação no PyPI[/][/]
"""


def function_help(flag: bool):
    if flag:
        console.print(
            importlib.metadata.version("worker-automate-hub"),
            style="bold blue",
        )
        raise Exit(code=0)


def function_configure(flag: bool):

    if flag:
        console.clear()
        environment_names = [
            "local",
            "qa",
            "main",
        ]
        q = [
            inquirer.Text("vault_token", "Por favor digite o token do Vault"),
            inquirer.List("env_list", "Selecione o ambiente", environment_names),
        ]
        r = inquirer.prompt(q, theme=GreenPassion())

        env_sel, credentials = load_environments(r["env_list"], r["vault_token"])
        write_env_config(env_sel, credentials)
        workers = asyncio.run(get_workers())

        if workers == None:
            console.print("\nNenhum worker encontrado.\n", style="yellow")
            raise Exit(code=0)
        else:

            nomes_workers = [worker["nomRobo"] for worker in workers]
            q2 = [
                inquirer.List(
                    "worker_list", "Selecione um Worker", choices=nomes_workers
                )
            ]
            r2 = inquirer.prompt(q2, theme=GreenPassion())
            worker_sel = next(
                worker for worker in workers if worker["nomRobo"] == r2["worker_list"]
            )
            add_worker_config(worker_sel)

            q3 = [
                inquirer.Confirm(
                    "reg_config",
                    message="Adicionar configuração de inicialização aos registros do Windows?",
                )
            ]
            r3 = inquirer.prompt(q3, theme=GreenPassion())

            if r3["reg_config"]:
                add_start_on_boot_to_registry()

            q4 = [
                inquirer.Confirm(
                    "assets_config",
                    message="Atualizar a pasta assets?",
                )
            ]
            r4 = inquirer.prompt(q4, theme=GreenPassion())

            if r4["assets_config"]:                
                update_assets_v2()

            q5 = [
                inquirer.Confirm(
                    "worker_bat", message="Criar o arquivo worker-startup.bat?"
                )
            ]
            r5 = inquirer.prompt(q5, theme=GreenPassion())

            if r5["worker_bat"]:
                create_worker_bat()

            q6 = [
                inquirer.Confirm(
                    "tesseract_install", message="Iniciar a instalação do Tesseract?"
                )
            ]
            r6 = inquirer.prompt(q6, theme=GreenPassion())

            if r6["tesseract_install"]:
                asyncio.run(download_tesseract())

            console.print(
                "\nConfiguração finalizada com sucesso!\n", style="bold green"
            )

            raise Exit(code=0)


@app.callback(invoke_without_command=True)
def main(
    ctx: Context,
    version: bool = Option(False, callback=function_help, is_flag=True),
    configure: bool = Option(False, callback=function_configure, is_flag=True),
):
    if ctx.invoked_subcommand:
        return
    console.print(HELP_MESSAGE)


def is_command_running(command):
    """
    Verifica se um comando CLI está sendo executado em outro terminal.

    :param command: O comando CLI a ser verificado (lista de strings).
    :return: True se o comando estiver sendo executado, False caso contrário.
    """
    command_str = " ".join(command)
    rep = 0
    for proc in psutil.process_iter(["pid", "name", "cmdline"]):
        try:
            cmdline = proc.info["cmdline"]
            if cmdline and isinstance(cmdline, list):
                cmdline_str = " ".join(cmdline)
                if command_str in cmdline_str:
                    print(cmdline_str)
                    rep += 1

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    if rep > 1:
        return True
    else:
        return False


from typer import Option


@app.command()
def run(
    force: bool = Option(
        False,
        "--force",
        help="Força a execução mesmo se outro comando já estiver rodando.",
    ),
    assets: bool = Option(
        False,
        "--assets",
        help="Executa o download da pasta assets atualizada.",
    ),
):
    if assets:
        update_assets_v2()
        
    command = ["worker", "run"]
    if not force and is_command_running(command):
        console.print(
            "\nO script já está em execução. Saindo...\n", style="bold yellow"
        )
        raise Exit(code=0)    
    else:
        run_worker(stop_event)


@app.command()
def update():
    check_for_update(stop_event)
