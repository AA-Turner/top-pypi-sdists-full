import os
import subprocess
import sys
import threading
from pathlib import Path
from typing import Optional

import psutil
import requests
import toml
from packaging import version
from rich.console import Console

from worker_automate_hub.utils.logger import logger

console = Console()


def update_version_in_toml(file_path: Path, new_version: str):
    """
    Atualiza a versão do worker no arquivo TOML.

    Args:
        file_path (Path): Caminho completo para o arquivo TOML.
        new_version (str): Nova versão para ser escrita no arquivo TOML.
    """
    try:
        # Abrir e carregar o arquivo TOML
        with open(file_path, "r") as file:
            config = toml.load(file)

        # Alterar a versão
        config["params"]["version"] = new_version

        # Salvar as alterações de volta no arquivo TOML
        with open(file_path, "w") as file:
            toml.dump(config, file)

        console.print(f"Versão atualizada para {new_version} no arquivo {file_path}")
    except Exception as e:
        console.print(f"Erro ao atualizar a versão: {e}")

def create_update_script(new_version: str):
    """
    Cria um arquivo de script .bat para atualizar a versão do worker com o pipx e reiniciar a aplicação.

    Args:
        new_version (str): Nova versão para ser escrita no arquivo TOML.

    Returns:
        Path: Caminho completo para o arquivo update.bat criado.
    """
    try:
        current_dir = Path.cwd()

        # Caminho do arquivo TOML
        toml_file_path = os.path.join(current_dir, 'settings.toml')        

        # Comando para atualizar o pacote via pipx
        update_command = 'pipx upgrade worker-automate-hub --force'

        # Comando para atualizar a versão no arquivo TOML
        update_toml_command = f'python -c "import toml; config=toml.load(\'{toml_file_path}\'); config[\'params\'][\'version\'] = \'{new_version}\'; toml.dump(config, open(\'{toml_file_path}\', \'w\'))"'

        # Comando para reiniciar a aplicação
        restart_command = f'start cmd /K "cd /D {current_dir} && worker-startup.bat"'

        # Caminho do arquivo de log
        log_file_path = os.path.join(current_dir, 'update.log')

        # Criando o conteúdo do script .bat
        script_content = f"""
        @echo off
        taskkill /IM worker.exe /F
        timeout /t 10 /nobreak
        {update_command}
        if %errorlevel% equ 0 (
            echo Update successful, updating version in TOML file...
            {update_toml_command}
            echo Version updated successfully, restarting the application...
            {restart_command}
        ) else (
            echo Update failed. > "{log_file_path}"
            echo Error code: %errorlevel% >> "{log_file_path}"
            echo See pipx output for more details. >> "{log_file_path}"
        )
        exit
        """

        # Caminho completo para o arquivo update.bat
        bat_file_path = os.path.join(current_dir, 'update.bat')

        # Escrevendo o conteúdo no arquivo update.bat
        with open(bat_file_path, 'w') as file:
            file.write(script_content.strip())

        log_msg = "Arquivo de update criado com sucesso!"
        logger.info(log_msg)
        console.print(f"\n{log_msg}\n", style="bold green")
        
        return bat_file_path

    except Exception as e:
        err_msg = "Erro ao criar o arquivo de update: {e}"
        logger.error(err_msg)
        console.print(f"\n{err_msg}\n", style="bold red")


def run_update_script(
    bat_file_path: str,
    stop_event: threading.Event
) -> None:
    """
    Executa o script .bat para atualizar o pacote.

    Args:
    - bat_file_path (str): Caminho completo para o arquivo .bat.
    - stop_event (threading.Event): Um objeto Event que é usado para
      sinalizar para as threads que devem parar.

    Returns:
    None
    """
    try:
        # Executando o script .bat
        subprocess.Popen(['start', 'cmd', '/c', bat_file_path], shell=True)
        
        log_msg = "update.bat executado com sucesso!"
        console.print(f"\n{log_msg}\n", style="bold green")
        logger.info(log_msg)        

        # Sinalizar para as threads que devem parar
        stop_event.set()

        # Encerrar o programa atual
        os.system('exit')
        sys.exit(0)        

    except subprocess.CalledProcessError as e:
        err_msg = f"Erro ao executar o update.bat: {e}"
        console.print(f"\n{err_msg}\n", style="bold red")
        logger.error(f"{err_msg}")

def get_installed_version(package_name: str) -> Optional[str]:
    
    """
    Retorna a versão atual do pacote instalada.

    Args:
    - package_name (str): Nome do pacote que se deseja obter a versão.

    Returns:
    - str: A versão atual do pacote ou None se o pacote não for encontrado.
    """
    try:
        result = subprocess.run(['pipx', 'list'], capture_output=True, text=True, check=True)
        lines = result.stdout.splitlines()
        for line in lines:
            if package_name in line:
                # Parse the version from the line, assuming the line format is 'package_name <version>'
                return line.split(' ')[5].replace(',', '')
    except subprocess.CalledProcessError as e:
        err_msg = f"Ocorreu um erro ao obter a versão do pacote instalada: {e}"
        console.print(f"\n{err_msg}\n", style="bold red")
        logger.error(err_msg)
    return None

def check_for_update(stop_event: threading.Event):
    """
    Verifica se há uma nova versão do pacote disponível no PyPI.

    Se houver uma versão mais recente disponível, atualiza o pacote via pipx e
    reinicia a aplicação.

    Args:
        stop_event (threading.Event): Um objeto Event que é usado para
            sinalizar para as threads que devem parar.
    """
    try:
        package_name = "worker-automate-hub"
        current_version = get_installed_version(package_name)

        response = requests.get(f"https://pypi.org/pypi/{package_name}/json")
        latest_version = response.json()
        console.print("last: "+latest_version["info"]["version"])
        console.print("current: "+current_version)
        if version.parse(latest_version["info"]["version"]) > version.parse(current_version):
            console.print(
                f"Uma nova versão [bold cyan]({latest_version["info"]["version"]})[/bold cyan] está disponível. Atualizando..."
            )
            bat_file_path = create_update_script(latest_version["info"]["version"])
            run_update_script(bat_file_path, stop_event)
        else:            
            current_dir = Path.cwd()

            # Caminho do arquivo TOML
            toml_file_path = os.path.join(current_dir, 'settings.toml')
            update_version_in_toml(toml_file_path, current_version)
            console.print("\nVocê está usando a versão mais atualizada.\n", style="green")
    except Exception as e:
        err_msg = f"Erro ao verificar novas versões do pacote: {e}"
        console.print(f"\n{err_msg}\n", style="bold red")
        logger.error(err_msg)

def close_other_cmd_windows():
    """
    Fecha outras janelas do cmd, deixando apenas a janela atual aberta.
    """
    try:
        current_pid = os.getpid() 
        for proc in psutil.process_iter(attrs=["pid", "name", "cmdline"]):
            try:           
                if proc.info["name"] == "cmd.exe" and proc.info["pid"] != current_pid:
                    proc.terminate()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

    except Exception as e:
        err_msg = f"Erro ao fechar outras janelas do cmd: {e}"
        console.print(f"\n{err_msg}\n", style="bold red")
        logger.error(err_msg)
