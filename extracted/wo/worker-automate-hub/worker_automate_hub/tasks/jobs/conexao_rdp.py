import asyncio
import platform
import re
import subprocess
import socket
import pyautogui
import os
import pygetwindow as gw
from rich.console import Console
import pygetwindow as gw
from pywinauto import Application, Desktop
from worker_automate_hub.api.client import change_robot_status_true 
from worker_automate_hub.models.dto.rpa_historico_request_dto import RpaHistoricoStatusEnum, RpaRetornoProcessoDTO, RpaTagDTO, RpaTagEnum
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
        sistema_operacional = platform.system().lower()
        console.print(f"Sistema operacional detectado: {sistema_operacional}")
        if sistema_operacional == "windows":
            comando_ping = ["ping", "-n", "1", "-w", "1000", self.ip]
        else:
            comando_ping = ["ping", "-c", "1", "-W", "1", self.ip]
        console.print(f"Executando comando de ping: {' '.join(comando_ping)}")
        try:
            resposta_ping = subprocess.run(comando_ping, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            ping_alcancado = resposta_ping.returncode == 0
            console.print(f"Ping {'sucesso' if ping_alcancado else 'falhou'}")
        except Exception as e:
            logger.error(f"Erro ao executar ping: {e}")
            ping_alcancado = False
        
        porta_aberta = False
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(10)
                console.print(f"Verificando porta 3389 em {self.ip}")
                resposta_porta = sock.connect_ex((self.ip, 3389))
                porta_aberta = resposta_porta == 0
                console.print(f"Porta 3389 {'aberta' if porta_aberta else 'fechada'}")
        except Exception as e:
            logger.error(f"Erro ao verificar a porta RDP: {e}")
            porta_aberta = False
        
        return ping_alcancado and porta_aberta
    
    async def clicar_no_titulo(self):
        janelas_rdp = [
            win
            for win in gw.getAllTitles()
            if self.ip in win
        ]

        for titulo in janelas_rdp:
            janela = gw.getWindowsWithTitle(titulo)[0]
            if not janela:
                console.print(f"Erro ao localizar a janela: {titulo}")
                continue

            console.print(f"Processando janela: {titulo}")
            x, y = janela.left, janela.top

            try:
                pyautogui.moveTo(x + 2, y + 2)
                pyautogui.hotkey("alt", "space")
                await worker_sleep(2)
                pyautogui.press("down", presses=6, interval=0.1)
                await worker_sleep(2)
                pyautogui.hotkey("enter")
                await worker_sleep(2)
                pyautogui.hotkey("enter")
                break

            except Exception as e:
                console.print(f"Erro ao interagir com a janela {titulo}: {e}")

    async def open_rdp(self):
        base_path = os.path.join("worker_automate_hub", "tasks", "jobs")
        rdp_file_path = os.path.join(base_path, "connection.rdp")
        os.makedirs(base_path, exist_ok=True)
        
        rdp_content = f"""screen mode id:i:1
            desktopwidth:i:1920
            desktopheight:i:1080
            use multimon:i:0
            session bpp:i:32
            compression:i:1
            keyboardhook:i:2
            displayconnectionbar:i:1
            disable wallpaper:i:0
            allow font smoothing:i:1
            allow desktop composition:i:1
            disable full window drag:i:0
            disable menu anims:i:0
            disable themes:i:0
            disable cursor setting:i:0
            bitmapcachepersistenable:i:1
            full address:s:{self.ip}
            username:s:{self.user}
            smart sizing:i:1
            winposstr:s:0,1,{(1920 // 4)},{(1080 // 4)},{(1920 // 4) + (1920 // 2)},{(1080 // 4) + (1080 // 2)}
        """

        try:
            with open(rdp_file_path, "w") as file:
                file.write(rdp_content)
            print(f"Arquivo RDP criado: {rdp_file_path}")
        except Exception as error:
            print(f"Erro ao montar o arquivo RDP: {error}")
            return

        try:
            subprocess.Popen(["mstsc", rdp_file_path], close_fds=True, start_new_session=True)
            console.print("Conexão RDP iniciada.")
        except Exception as error:
            console.print(f"Erro ao abrir a conexão RDP: {error}")

    async def verificar_conexao_estabelecida(self):
        janelas_rdp = [
            win
            for win in gw.getAllTitles()
            if self.ip in win
        ]

        janela = None

        for titulo in janelas_rdp:
            janela = gw.getWindowsWithTitle(titulo)[0]
            if not janela:
                console.print(f"Erro ao localizar a janela: {titulo}")
                continue
            else:
                return True

    async def conectar(self):
        console.print(f"Iniciando cliente RDP para {self.ip}")
        try:
            await worker_sleep(3)
            await self.open_rdp()
            await worker_sleep(5)
            
            console.print("Procurando janela RDP")
            try:
                possible_titles = ["Conexão de Área de Trabalho Remota", "Ligação ao ambiente de trabalho remoto"]
                app = None
                app_window = None

                for title in possible_titles:
                    try:
                        app = Application(backend="uia").connect(title=title)
                        app_window = app.window(title=title)
                        console.print(f"Janela encontrada: {title}")
                        break
                    except Exception:
                        continue

                if not app or not app_window:
                    raise Exception("Nenhuma janela com título correspondente foi encontrada.")

                app_window.set_focus()
                console.print("Janela RDP ativada.")

                pyautogui.press("left")
                await worker_sleep(1)
                pyautogui.hotkey("enter")
                await worker_sleep(3)

            except Exception as e:
                console.print(f"Erro ao ativar a janela RDP: {e}", style="bold red")

            app_window = None
            possible_titles_patterns = [
                re.compile(r"Conexão de Área de Trabalho Remota", re.IGNORECASE),
                re.compile(r"Ligação ao ambiente de trabalho remoto", re.IGNORECASE),
                re.compile(r"Segurança do Windows", re.IGNORECASE)
            ]

            janelas = Desktop(backend="uia").windows()
            for janela in janelas:
                titulo = janela.window_text()
                for pattern in possible_titles_patterns:
                    if pattern.search(titulo):
                        try:
                            app = Application(backend="uia").connect(title_re=pattern)
                            app_window = app.window(title_re=pattern)
                            console.print(f"Janela encontrada: {titulo}")
                            break
                        except Exception as e:
                            console.print(f"Erro ao conectar a janela '{titulo}': {e}")
                if app_window:
                    break

            await worker_sleep(2)

            if app_window:
                try:
                    app_window.restore()
                    app_window.set_focus()
                    console.print("Foco definido com sucesso.")
                except Exception as e:
                    console.print(f"Erro ao definir foco na janela: {e}")
            else:
                console.print("Nenhuma janela correspondente foi encontrada.")

            await worker_sleep(5)
            console.print("Inserindo senha.")
            pyautogui.write(self.password, interval=0.1)
            pyautogui.press("enter")
            await worker_sleep(5)
            pyautogui.press("left")
            await worker_sleep(5)
            pyautogui.press("enter")
            console.print("Credenciais inseridas.")
            await worker_sleep(5)
            
            try:
                base_path = os.path.join("worker_automate_hub", "tasks", "jobs")
                rdp_file_path = os.path.join(base_path, "connection.rdp")
                if os.path.exists(rdp_file_path):
                    os.remove(rdp_file_path)
            except Exception as error:
                console.print(f"Erro ao deletar arquivo 'connection.rdp'. Error: {error}")

            conexao_rdp_aberta = await self.verificar_conexao_estabelecida()
            if conexao_rdp_aberta is not True:
                raise ConnectionError("Não foi possível estabelecer conexão RDP.")
            
            return True

        except Exception as e:
            logger.error(f"Erro ao tentar conectar via RDP: {e}")
            return False

async def conexao_rdp(task: RpaProcessoRdpDTO) -> RpaRetornoProcessoDTO:
    try:
        console.print("Iniciando processo de conexão RDP.")
        rdp = RDPConnection(task)
        conectado = await rdp.verificar_conexao()
        if not conectado:
            logger.warning("Não foi possível estabelecer conexão RDP. Verifique o IP e a disponibilidade da porta.")
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno="Não foi possível estabelecer conexão RDP. Verifique o IP e a disponibilidade da porta.",
                status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
            )

        sucesso_conexao = await rdp.conectar()
        if sucesso_conexao:
            console.print("Processo de conexão RDP executado com sucesso.")
            
            #await rdp.clicar_no_titulo()

            #Altera coluna ativo para true or false 
            await change_robot_status_true(rdp.uuid_robo)

            return RpaRetornoProcessoDTO(
                sucesso=True,
                retorno="Conexão RDP estabelecida com sucesso.",
                status=RpaHistoricoStatusEnum.Sucesso,
            )
        else:
            logger.error("Falha ao tentar conectar via RDP.")
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno="Falha ao tentar conectar via RDP.",
                status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
            )
    except Exception as ex:
        err_msg = f"Erro ao executar conexão RDP: {ex}"
        logger.error(err_msg)
        console.print(err_msg, style="bold red")
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=err_msg,
            status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)],
        )
