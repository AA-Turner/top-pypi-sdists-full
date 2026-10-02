import asyncio
import platform
import subprocess
import socket
import pyautogui
import pygetwindow as gw
from rich.console import Console
from pywinauto import Application
from worker_automate_hub.api.rdp_service import send_rdp_action
from worker_automate_hub.models.dto.rpa_historico_request_dto import (
    RpaHistoricoStatusEnum,
    RpaRetornoProcessoDTO,
    RpaTagDTO,
    RpaTagEnum,
)
from worker_automate_hub.models.dto.rpa_processo_rdp_dto import RpaProcessoRdpDTO
from worker_automate_hub.utils.logger import logger
from worker_automate_hub.utils.util import worker_sleep

console = Console()


class RDPConnection:
    def __init__(self, task: RpaProcessoRdpDTO):
        self.task = task
        self.ip = task.configEntrada.get("ip")
        self.user = task.configEntrada.get("user")
        self.password = task.configEntrada.get("password")
        self.processo = task.configEntrada.get("processo")
        self.uuid_robo = task.configEntrada.get("uuidRobo")

    async def verificar_conexao(self) -> bool:
        """
        Verifica a conectividade com o host remoto via ping e verificação da porta RDP (3389).
        """
        sistema_operacional = platform.system().lower()
        console.print(f"Sistema operacional detectado: {sistema_operacional}")

        comando_ping = (
            ["ping", "-n", "1", "-w", "1000", self.ip]
            if sistema_operacional == "windows"
            else ["ping", "-c", "1", "-W", "1", self.ip]
        )
        console.print(f"Executando comando de ping: {' '.join(comando_ping)}")

        try:
            resposta_ping = subprocess.run(
                comando_ping, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            ping_alcancado = resposta_ping.returncode == 0
            console.print(f"Ping {'sucesso' if ping_alcancado else 'falhou'}")
        except Exception as e:
            console.print(f"Erro ao executar ping: {e}")
            ping_alcancado = False

        porta_aberta = False
        try:
            with socket.create_connection((self.ip, 3389), timeout=10):
                console.print(f"Porta 3389 aberta em {self.ip}")
                porta_aberta = True
        except (socket.timeout, OSError) as e:
            console.print(f"Erro ao verificar a porta RDP: {e}")

        return ping_alcancado and porta_aberta

    async def desligar(self):
        """
        Fecha a conexão RDP interagindo com a janela do cliente RDP.
        """
        janelas_rdp = [win for win in gw.getAllTitles() if self.ip in win]

        if not janelas_rdp:
            console.print(f"Nenhuma janela RDP encontrada para o IP: {self.ip}")
            return

        for titulo in janelas_rdp:
            janela = gw.getWindowsWithTitle(titulo)[0]
            if not janela:
                console.print(f"Erro ao localizar a janela: {titulo}")
                continue

            try:
                janela = gw.getWindowsWithTitle(titulo)[0]
                console.print(f"Processando janela: {titulo}")

                app = Application(backend="uia").connect(title=titulo)
                app_window = app.window(title=titulo)
                console.print(f"Janela encontrada: {titulo}")

                if not app or not app_window:
                    raise Exception(
                        "Nenhuma janela com título correspondente foi encontrada."
                    )

                app_window.set_focus()
                console.print("Janela RDP ativada.")

                x, y = janela.left, janela.top

                pyautogui.moveTo(x + 2, y + 2)
                pyautogui.hotkey("alt", "space")
                await worker_sleep(2)
                pyautogui.press("down", presses=10, interval=0.1)
                await worker_sleep(2)
                pyautogui.press("enter")
                await worker_sleep(2)
                pyautogui.press("enter")
                break

            except Exception as e:
                console.print(f"Erro ao interagir com a janela {titulo}: {e}")
                raise (e)


async def fechar_conexao_rdp(task: RpaProcessoRdpDTO) -> RpaRetornoProcessoDTO:
    """
    Gerencia o processo de fechamento da conexão RDP e retorna um status do processo.
    """
    try:
        rdp_connection = RDPConnection(task)
        console.print("Iniciando o fechamento da conexão RDP.")
        conectado = await rdp_connection.verificar_conexao()

        # if not conectado:
        #    msg = f"A máquina informada não está ligada. Verifique o IP: {rdp_connection.ip} e a disponibilidade da porta."
        #    logger.warning(msg)
        #    return RpaRetornoProcessoDTO(
        #        sucesso=False,
        #        retorno=msg,
        #        status=RpaHistoricoStatusEnum.Falha,
        #        tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
        #    )

        await rdp_connection.desligar()

        if conectado:
            await send_rdp_action(rdp_connection.uuid_robo, "stop")

        return RpaRetornoProcessoDTO(
            sucesso=True,
            retorno="Conexão RDP encerrada com sucesso.",
            status=RpaHistoricoStatusEnum.Sucesso,
        )
    except Exception as ex:
        err_msg = f"Erro ao executar o fechamento da conexão RDP para a máquina {rdp_connection.ip}: {ex}"
        console.print(err_msg)
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=err_msg,
            status=RpaHistoricoStatusEnum.Falha,
            tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
        )
