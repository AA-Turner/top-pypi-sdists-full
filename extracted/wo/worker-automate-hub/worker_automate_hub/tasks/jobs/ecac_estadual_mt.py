import asyncio
import io
import mimetypes
import os
import shutil
import smtplib
import time
import uuid
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

import pyautogui
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from playwright.async_api import async_playwright
from rich.console import Console

from worker_automate_hub.api.client import (
    get_config_by_name,
    sync_get_config_by_name,
)
from worker_automate_hub.models.dto.rpa_historico_request_dto import (
    RpaHistoricoStatusEnum,
    RpaRetornoProcessoDTO,
    RpaTagDTO,
    RpaTagEnum,
)
from worker_automate_hub.models.dto.rpa_processo_entrada_dto import (
    RpaProcessoEntradaDTO,
)
from worker_automate_hub.utils.get_creds_gworkspace import GetCredsGworkspace
from worker_automate_hub.utils.logger import logger

pyautogui.PAUSE = 0.5
pyautogui.FAILSAFE = False
console = Console()


def find_and_click(
    image_path: str,
    description: str,
    confidence: float = 0.8,
    write_text: str | None = None,
    wait_time: float = 2,
) -> None:
    """
    Encontra um elemento na tela com base em uma imagem e clica nele.

    Args:
        image_path: Caminho para a imagem do elemento.
        description: Descrição do elemento.
        confidence: Nível de confiança para encontrar o elemento.
        write_text: Texto a ser inserido no campo.
        wait_time: Tempo de espera após clicar no elemento.

    Returns:
        None
    """
    element = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
    if element:
        pyautogui.click(element)
        console.print(f"[green]'{description}' encontrado e clicado.[/green]")
        if write_text:
            pyautogui.write(write_text, interval=0.05)
            console.print(
                f"[green]Texto '{write_text}' inserido em '{description}'.[/green]"
            )
        time.sleep(wait_time)
    else:
        raise Exception(f"[red]Elemento '{description}' não encontrado![/red]")


def send_email(
    smtp_server: str,
    smtp_port: int,
    smtp_user: str,
    smtp_password: str,
    message_text: str,
    subject: str,
    to: str,
) -> None:
    """
    Envia um e-mail com os dados recebidos.

    Args:
        smtp_server (str): Servidor SMTP
        smtp_port (int): Porta do servidor SMTP
        smtp_user (str): Usuário do servidor SMTP
        smtp_password (str): Senha do usuário do servidor SMTP
        message_text (str): Corpo do e-mail
        subject (str): Assunto do e-mail
        to (str): Destinatário do e-mail
    """
    if not smtp_server:
        raise ValueError("Servidor SMTP não pode ser nulo")
    if not isinstance(smtp_port, int):
        raise ValueError("Porta do servidor SMTP deve ser um inteiro")
    if not smtp_user:
        raise ValueError("Usuário do servidor SMTP não pode ser nulo")
    if not smtp_password:
        raise ValueError("Senha do usuário do servidor SMTP não pode ser nula")
    if not message_text:
        raise ValueError("Corpo do e-mail não pode ser nulo")
    if not subject:
        raise ValueError("Assunto do e-mail não pode ser nulo")
    if not to:
        raise ValueError("Destinatário do e-mail não pode ser nulo")

    message = create_message_with_attachment(smtp_user, to, subject, message_text)
    try:
        send_message(
            smtp_server, smtp_port, smtp_user, smtp_password, smtp_user, to, message
        )
    except Exception as e:
        err_msg = f"Erro ao enviar e-mail: {e}"
        console.print(err_msg, style="bold red")
        logger.error(err_msg)


def create_message_with_attachment(
    sender: str, to: str, subject: str, message_text: str, file: str | None = None
) -> str:
    """
    Cria uma mensagem com um anexo.

    Args:
        sender (str): Remetente do email
        to (str): Destinatário do email
        subject (str): Assunto do email
        message_text (str): Corpo do email
        file (str | None): Caminho do arquivo a ser anexado (opcional)

    Returns:
        str: A mensagem com o anexo no formato de string
    """
    if not sender:
        raise ValueError("Remetente do email não pode ser nulo")
    if not to:
        raise ValueError("Destinatário do email não pode ser nulo")
    if not subject:
        raise ValueError("Assunto do email não pode ser nulo")
    if not message_text:
        raise ValueError("Corpo do email não pode ser nulo")

    message = MIMEMultipart()
    message["to"] = to
    message["from"] = sender
    message["subject"] = subject

    msg = MIMEText(message_text)
    message.attach(msg)

    if file:
        if not os.path.exists(file):
            raise FileNotFoundError(f"Arquivo {file} não encontrado")
        if not os.path.isfile(file):
            raise ValueError(f"{file} não é um arquivo")

        content_type, encoding = mimetypes.guess_type(file)

        if content_type is None or encoding is not None:
            content_type = "application/octet-stream"

        main_type, sub_type = content_type.split("/", 1)
        with open(file, "rb") as f:
            attachment = MIMEBase(main_type, sub_type)
            attachment.set_payload(f.read())
            encoders.encode_base64(attachment)
            attachment.add_header(
                "Content-Disposition", "attachment", filename=os.path.basename(file)
            )
            attachment.add_header("Content-Transfer-Encoding", "base64")
            message.attach(attachment)

    return message.as_string()


def send_message(
    smtp_server: str,
    smtp_port: int,
    smtp_user: str,
    smtp_password: str,
    sender: str,
    recipient: str,
    message: str,
) -> None:
    """
    Envia uma mensagem via SMTP.

    Args:
        smtp_server (str): Servidor SMTP
        smtp_port (int): Porta do servidor SMTP
        smtp_user (str): Usuário do servidor SMTP
        smtp_password (str): Senha do usuário do servidor SMTP
        sender (str): Remetente do e-mail
        recipient (str): Destinatário do e-mail
        message (str): Corpo do e-mail

    Returns:
        None
    """
    if not smtp_server or not smtp_port or not smtp_user or not smtp_password:
        raise ValueError("Parâmetros SMTP não podem ser nulos")

    if not sender or not recipient or not message:
        raise ValueError("Parâmetros de e-mail não podem ser nulos")

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(sender, recipient, message)
            logger.info("Mensagem enviada com sucesso")
    except smtplib.SMTPAuthenticationError:
        console.print(f"Erro de autenticação. Verifique seu nome de usuário e senha.\n")
        logger.error("Erro de autenticação. Verifique seu nome de usuário e senha.")
    except smtplib.SMTPConnectError:
        console.print(
            f"Não foi possível conectar ao servidor SMTP. Verifique o endereço e a porta.\n"
        )
        logger.error(
            "Não foi possível conectar ao servidor SMTP. Verifique o endereço e a porta."
        )
    except smtplib.SMTPRecipientsRefused:
        console.print(
            f"O destinatário foi rejeitado. Verifique o endereço do destinatário.\n"
        )
        logger.error(
            "O destinatário foi rejeitado. Verifique o endereço do destinatário."
        )
    except smtplib.SMTPSenderRefused:
        console.print(
            f"O remetente foi rejeitado. Verifique o endereço do remetente..\n"
        )
        logger.error("O remetente foi rejeitado. Verifique o endereço do remetente.")
    except smtplib.SMTPDataError as e:
        console.print(f"Erro ao enviar dados: {e}\n")
        logger.error(f"Erro ao enviar dados: {e}")
    except Exception as error:
        console.print(f"Ocorreu um erro ao enviar a mensagem: {error} \n")
        logger.error("Ocorreu um erro ao enviar a mensagem: %s" % error)


async def ecac_estadual_mt(task: RpaProcessoEntradaDTO) -> RpaRetornoProcessoDTO:
    """
    Processo que realiza a consulta de caixa postal do ECAC Estadual de Mato Grosso para os certificado SIM DISTRIBUIDORA e SIM AVIAÇÃO.

    """
    try:
        # Obtém a resolução da tela
        screen_width, screen_height = pyautogui.size()
        console.print(
            f"Resolução da tela: Width: {screen_width} - Height{screen_height}...\n"
        )
        console.print(f"Task:{task}")

        console.print("Realizando as validações inicias para execução do processo\n")
        console.print("Criando o diretório temporario ...\n")

        cd = Path.cwd()
        temp_dir = f"{cd}\\temp_certificates\\{str(uuid.uuid4())}"
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        console.print("Obtendo configuração para execução do processo ...\n")
        try:
            config = await get_config_by_name("Ecac_Estadual_MT")
            emails_to = config.conConfiguracao.get("emails")
            certificado_path = config.conConfiguracao.get("CertificadoPath")
            certificado_files = config.conConfiguracao.get("CertificadoFile")

            console.print(
                "Obtendo configuração de email para execução do processo ...\n"
            )
            smtp_config = await get_config_by_name("SMTP")

            smtp_server = smtp_config.conConfiguracao.get("server")
            smtp_user = smtp_config.conConfiguracao.get("user")
            smtp_pass = smtp_config.conConfiguracao.get("password")
            smtp_port = smtp_config.conConfiguracao.get("port")

            get_gcp_token = sync_get_config_by_name("GCP_SERVICE_ACCOUNT")
            get_gcp_credentials = sync_get_config_by_name("GCP_CREDENTIALS")
        except Exception as e:
            console.print(
                f"Erro ao obter as configurações para execução do processo, erro: {e}...\n"
            )
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Erro ao obter as configurações para execução do processo, erro: {e}",
                status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
            )

        gcp_credencial = GetCredsGworkspace(
            token_dict=get_gcp_token.conConfiguracao,
            credentials_dict=get_gcp_credentials.conConfiguracao,
        )
        creds = gcp_credencial.get_creds_gworkspace()

        if not creds:
            console.print(f"Erro ao obter autenticação para o GCP...\n")
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Erro ao obter autenticação para o GCP",
                status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
            )

        console.print("Verificando a existência do diretório com locators...\n")
        if os.path.exists("assets/ecac_federal"):
            console.print("Diretório existe..\n")
        else:
            console.print("Diretório não existe..\n")
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Não foi possivel encontrar o diretório com os locators para continuidade do processo, diretório: 'assets/ecac_federal'",
                status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
            )

        console.print(
            "Verificando a existência dos arquivos de certificados no Google Drive...\n"
        )
        drive_service = build("drive", "v3", credentials=creds)
        query = f"'{certificado_path}' in parents"
        results = (
            drive_service.files()
            .list(
                q=query,
                pageSize=1000,
                supportsAllDrives=True,  # Habilita suporte para Shared Drives
                includeItemsFromAllDrives=True,  # Inclui itens de todos os drives
                fields="files(id, name)",
            )
            .execute()
        )

        items = results.get("files", [])

        if not items:
            console.print(f"Nenhum certificado encontrado...\n")
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Nenhum certificado encontrado no diretório do Google Drive",
                status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
            )

        corpo_email = """
        <html>
        <body>
            <p>Caros(as),</p>
            <p>Espero que este e-mail o encontre bem!</p>
            <p>Abaixo, segue um resumo baseado na consulta à caixa postal referente ao estado de GO.</p>
            <p>Resultado da consulta:</p>
        """
        status_exec = False
        for row in certificado_files:
            try:
                empresa = row["Empresa"]
                certificado = row["Certificado"]
                senha = row["Senha"]

                console.print(
                    f"Procurando certificado: {certificado} para a empresa {empresa}...\n"
                )
                drive_service = build("drive", "v3", credentials=creds)
                query = f"'{certificado_path}' in parents and name='{certificado}'"
                results = (
                    drive_service.files()
                    .list(
                        q=query,
                        pageSize=1000,
                        supportsAllDrives=True,  # Habilita suporte para Shared Drives
                        includeItemsFromAllDrives=True,  # Inclui itens de todos os drives
                        fields="files(id, name)",
                    )
                    .execute()
                )

                items = results.get("files", [])

                if items:
                    console.print(
                        f"Certificado: {certificado} para a empresa {empresa} encontrado...\n"
                    )
                    file_id = items[0]["id"]
                    console.print(
                        f"Certificado {certificado} encontrado. Iniciando download...\n"
                    )

                    file_path = os.path.join(temp_dir, certificado)

                    request = drive_service.files().get_media(fileId=file_id)

                    fh = io.FileIO(file_path, "wb")
                    downloader = MediaIoBaseDownload(fh, request)

                    done = False
                    while done is False:
                        status, done = downloader.next_chunk()
                        console.print(f"Download {int(status.progress() * 100)}%.")

                    fh.close()

                    console.print(f"Certificado {certificado} baixado com sucesso.\n")

                    async with async_playwright() as p:
                        browser = await p.firefox.launch(headless=False)
                        console.print("Iniciando o browser")
                        context = await browser.new_context(accept_downloads=True)
                        page = await context.new_page()

                        await asyncio.sleep(3)

                        await page.goto("about:preferences#privacy")

                        locator_path = "assets/ecac_federal"

                        element_find_settings_image = (
                            f"{locator_path}/FindInSettings.PNG"
                        )
                        element_view_certificates = (
                            f"{locator_path}/ViewCertificates.PNG"
                        )
                        element_your_certificates = (
                            f"{locator_path}/YourCertificates.PNG"
                        )
                        element_import_certificates = (
                            f"{locator_path}/ImportCertificate.PNG"
                        )
                        element_insert_path_certificates = (
                            f"{locator_path}/InsertPathCertificate.PNG"
                        )
                        element_open_certificates = (
                            f"{locator_path}/OpenCertificate.PNG"
                        )
                        element_pwd_certificates = (
                            f"{locator_path}/EnterPasswordCertificate.PNG"
                        )
                        element_sign_in_certificates = (
                            f"{locator_path}/SignCertificate.PNG"
                        )
                        element_confirm_certificates = f"{locator_path}/Confirm.PNG"
                        element_sign_in_certificates = (
                            f"{locator_path}/SignCertificate.PNG"
                        )
                        element_popup_certificate = (
                            f"{locator_path}/ImportCertificate_popup.PNG"
                        )

                        console.print(
                            "Importando o certificado no browser (playwright) "
                        )
                        # Configurações
                        find_and_click(element_find_settings_image, "Configurações")
                        pyautogui.write("Cert", interval=0.05)
                        await asyncio.sleep(1)

                        # Certificados
                        find_and_click(element_view_certificates, "Certificados")
                        await asyncio.sleep(1)

                        # Meus Certificados
                        find_and_click(element_your_certificates, "Meus Certificados")
                        await asyncio.sleep(1)

                        # Importar Certificado
                        find_and_click(
                            element_import_certificates, "Importar Certificado"
                        )
                        await asyncio.sleep(2)

                        # Inserir Caminho do Certificado e escrever o caminho do arquivo
                        find_and_click(
                            element_insert_path_certificates,
                            "Inserir Caminho do Certificado",
                            write_text=file_path,
                        )
                        await asyncio.sleep(2)

                        # Abrir Certificado
                        find_and_click(element_open_certificates, "Abrir Certificado")
                        await asyncio.sleep(2)

                        # Inserir Senha do Certificado
                        find_and_click(
                            element_pwd_certificates,
                            "Inserir Senha do Certificado",
                            write_text=senha,
                        )
                        await asyncio.sleep(2)

                        # Assinar Certificado
                        find_and_click(
                            element_sign_in_certificates, "Assinar Certificado"
                        )
                        await asyncio.sleep(2)

                        # Confirmar Importação
                        find_and_click(
                            element_confirm_certificates, "Confirmar Importação"
                        )
                        await asyncio.sleep(2)

                        element_popup_certificate = False
                        try:
                            element_popup_certificate = pyautogui.locateCenterOnScreen(
                                element_popup_certificate, confidence=0.8
                            )
                            element_popup_certificate = True
                        except:
                            pass

                        if not element_popup_certificate:
                            await asyncio.sleep(3)

                            try:
                                await page.goto(
                                    "https://www.sefaz.mt.gov.br/dte/pages/login/Login-Certificado.xhtml",
                                    timeout=1000,
                                )
                                await asyncio.sleep(3)
                                await page.keyboard.press("Enter")
                            except:
                                await page.keyboard.press("Enter")
                                await page.goto(
                                    "https://www.sefaz.mt.gov.br/dte/pages/login/Login-Certificado.xhtml",
                                    timeout=1000,
                                )
                                await asyncio.sleep(3)
                                await page.keyboard.press("Enter")

                                await page.get_by_role(
                                    "link", name="✉ Caixa Postal Eletrônica"
                                ).click()

                                tabela = await page.locator(
                                    "/html/body/div[1]/center/div/div[2]/div/div[2]/div/div[2]/form/div[1]/div[1]/table"
                                )
                                conteudo_html = await tabela.inner_html()

                                imagem = await tabela.locator(
                                    "img#j_idt24\\:contribuintesDT\\:0\\:j_idt35"
                                )

                                atributo_title = await imagem.get_attribute("title")

                                corpo_email += f"""
                                    <h2>Resumo para a empresa {empresa}:</h2>
                                    <table border="1">
                                        {conteudo_html}
                                    </table>
                                    <h2>Situação:</h2>
                                    <p>{atributo_title}</p>
                                    """

                                await page.get_by_role("button", name="Voltar").click()
                                await page.get_by_role("link", name=" Sair").click()
                                await context.close()
                                await browser.close()
                                status_exec = True

                else:
                    console.print(
                        f"Certificado não encontrado no Driver {certificado}...\n"
                    )
                    corpo_email += f"""
                        <h2>Resumo para a empresa {empresa}:</h2>
                        <p>Certificado não encontrado no Google Drive.</p>
                        """
                    

            except Exception as e:
                console.print(
                    f"Não foi possivel concluir a busca para este certificado {certificado}, erro {e}...\n"
                )
                corpo_email += f"""
                <h2>Resumo para a empresa {empresa}:</h2>
                <p>Não foi possivel concluir a busca para este certificado, erro {e}</p>
                """
        if status_exec:
            try:
                corpo_email += """
                    </body>
                    </html>
                    """
                send_email(
                    smtp_server,
                    smtp_port,
                    smtp_user,
                    smtp_pass,
                    corpo_email,
                    "Consulta ECAC_Estadual - MT",
                    emails_to,
                )
                log_msg = f"Processo concluído e e-mail disparado para área de negócio"
                console.print(log_msg)
                return RpaRetornoProcessoDTO(
                    sucesso=True,
                    retorno=log_msg,
                    status=RpaHistoricoStatusEnum.Sucesso,
                )
            except Exception as e:
                log_msg = f"Processo concluído com sucesso, porém houve falha no envio do e-mail para área de negócio"
                console.print(log_msg)
                return RpaRetornoProcessoDTO(
                    sucesso=False,
                    retorno=log_msg,
                    status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
                )

    except Exception as e:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        log_msg = f"Erro Processo do Ecac Estadual MT: {e}"
        logger.error(log_msg)
        console.print(log_msg, style="bold red")
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=log_msg,
            status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
        )
