"""
**_LIB BCFOX - DOC_**

Args:
    *DRIVER*: Para utitlizar o servico do _driver_ inicie a classe dele como no exemplo abaixo, todas as explicações das opções estão lá.
        - driver_class = bcpkgfox.Instancedriver()

    _SYSTEM_: Caso queira extrair PDF's, criar pastas, mostrar mensagens_box entre outros serviços do systema utilize o comando abaixo **diretamente**.
        - bcpkgfox.System.{def}

    _API_: Utilização de api's use o comando abaixo, **diretamente**
        - bcpkgfox.invoke_api.{def}

"""

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from typing import Optional
import tkinter as tk
import re

from .find_elements import *
from .invoke_api import *
from .get_driver import *
from .system import *

import os

dir_kit = "C:\\TMPIMGKIT\\LAST_IMG"

dirs_defaults = {
    "dir_kit": "C:\\TMPIMGKIT\\LAST_IMG",

    "dir_ggi": "C:\\TMPIMGGI\\LAST_IMG\\",
    "dir_gi": "C:\\TMPIMGI\\",

    "dir_robos": "C:\\TMP_ROBOS",

    "dir_pe": "C:\\TMPIMGPE\\"
}

dirs_sub = {
    "dir_consulta": "C:\\TMPIMGCONSULTA\\",
    "dir_GCPJ": "C:\\TMPIMGGCPJ\\",
    }

sub_pastas = ["LAST_IMG", "FTP", "ftp2", "validacao"]

driver = None
By = By

def get_page_source():
    global driver
    return driver.page_source

def create_dirs(specifics_dirs: Optional[list] = None, disable_print_response: bool = False) -> str:
    """ Cria os diretórios padrões
     - Caso queira criar algum especifico passe em forma de LISTA o caminho deles.
     """
    global dirs
    dirs_created = []

    # Defaults
    for dir_ in dirs_defaults.values():

        if not os.path.exists(dir_):
            os.makedirs(dir_)
            dirs_created.append(dir_)

    # Sub's
    for dir_ in dirs_sub.values():
        for pasta in sub_pastas:

            if not os.path.exists(dir_):
                os.makedirs(dir_)
                dirs_created.append(dir_)

            if not os.path.exists(os.path.join(dir_, pasta)):
                os.makedirs(os.path.join(dir_, pasta))
                dirs_created.append(os.path.join(dir_, pasta))

    # Specifics
    if specifics_dirs:
        for dir_ in specifics_dirs:
            if not os.path.exists(dir_):
                os.makedirs(os.path.join(dir_, pasta))
                dirs_created.append(os.path.join(dir_, pasta))

    # Log
    if disable_print_response == False:
        if dirs_created:
            print(f" {DK_ORANGE}>{RESET} {len(dirs_created)} diretórios padrões criados:") if len(dirs_created) > 1 else print(f" {DK_ORANGE}>{RESET} {len(dirs_created)} diretório criado:")
            for pasta in dirs_created:
                print(f"  {ORANGE}>{RESET} {pasta}")

        else:
            print(f" {DK_ORANGE}>{RESET} Todos os diretórios padrões presentes")

def resource_path(relative_path):
    """
    Returns the absolute path of a resource, whether running normally or in a PyInstaller executable.

    Args:
        relative_path (str): Relative path of the resource.

    Returns:
        str: Absolute path of the resource.
    """
    try: base_path = sys._MEIPASS
    except AttributeError: base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def initialize_driver(extension_path: Optional[str] = None, captcha_name: Optional[str] = None, captcha_api_key: Optional[str] = None) -> WebElement:

    """ Passe somente o nome da pasta, no mesmo diretório da main """
    global driver, dir_kit

    if driver is None:
        driver = get_driver.backcode__dont_use__launch_browser(dir_kit, extension_path,
            captcha_name, captcha_api_key)

        print(driver)
        return driver

def finalize_driver():
    global driver

    driver.quit()
    driver = None
    return None

def get(link):
    global driver
    if driver != None:
        get_driver.backcode__dont_use__get(driver, link)

def wait_for_element_be_clickable(by, value, timeout=10, parent=None):
    global driver
    if driver != None:
        return find_elements.backcode__dont_use__wait_for_element_be_clickable(driver, by.lower(), value, timeout, parent)

    else: raise ValueError("Error: Driver is None")

def find_element_with_wait(by, value, timeout=10, parent=None):
    global driver
    if driver != None:
        return find_elements.backcode__dont_use__find_element_with_wait_backcode(driver, by.lower(), value, timeout, parent)

    else: raise ValueError("Error: Driver is None")

def find_elements_with_wait(by, value, timeout=10, parent=None):
    global driver
    if driver != None:
        return find_elements.backcode__dont_use__find_elements_with_wait_backcode(driver, by.lower(), value, timeout, parent)

    else: raise ValueError("Error: Driver is None")

def wait_for_element_appear(object, type, timeout=10):
    """
    Aguarda até que um objeto (texto, elemento ou imagem) seja encontrado na tela.

    Args:
        object (str|list): O objeto a ser procurado. Pode ser um caminho de imagem, texto ou elemento XPATH.
        type (str): O tipo de objeto a ser procurado. Pode ser 'imagem', 'texto' ou 'elemento'.
        timeout (int): limite de tempo que vai procurar o objeto, coloque 0 para não ter limite

    Exemplo:
        wait_for('C:\\Caminho\\da\\imagem.png', 'imagem')
        wait_for('Texto a ser encontrado', 'texto')
        wait_for( XPATH_AQUI, 'elemento')
    """
    global driver
    tempo = timeout

    text_type = ['texto', 'string', 'palavra', 'mensagem', 'frase', 'conteúdo', 'texto_visível', 'texto_encontrado', 'texto_display', 'label']
    element_type = [ "element", "elemento", "botao", 'element', 'web_element', 'html_element', 'ui_element', 'interface_element', 'objeto', 'widget', 'campo', 'componente']
    imagem_type = [ 'imagem', 'img', 'imagem_png', 'imagem_jpeg', 'image', 'imagem_exata', 'padrão_imagem', 'foto', 'captura_tela', 'screenshot', 'imagem_visual']

    for escrita in text_type:
        if escrita in type.lower():
            type = "text"

    for escrita in element_type:
        if escrita in type.lower():
            type = "element"

    for escrita in imagem_type:
        if escrita in type.lower():
            type = "image"

    return find_elements.backcode__dont_use__wait_for(driver, object, type, timeout=tempo)

def wait_for_element_disappear(object, type, timeout=10):
    """
    Aguarda até que um objeto desapareça.(texto, elemento ou imagem)

    Args:
        object (str|list): O objeto a ser procurado. Pode ser um caminho de imagem, texto ou elemento XPATH.
        type (str): O tipo de objeto a ser procurado. Pode ser 'imagem', 'texto' ou 'elemento'.
        timeout (int): limite de tempo que vai procurar o objeto, coloque 0 para não ter limite

    Exemplo:
        wait_for('C:\\Caminho\\da\\imagem.png', 'imagem')
        wait_for('Texto a ser encontrado', 'texto')
        wait_for( XPATH_AQUI, 'elemento')
    """
    global driver
    tempo = timeout

    text_type = ['texto', 'string', 'palavra', 'mensagem', 'frase', 'conteúdo', 'texto_visível', 'texto_encontrado', 'texto_display', 'label']
    element_type = [ "element", "elemento", "botao", 'element', 'web_element', 'html_element', 'ui_element', 'interface_element', 'objeto', 'widget', 'campo', 'componente']
    imagem_type = [ 'imagem', 'img', 'imagem_png', 'imagem_jpeg', 'image', 'imagem_exata', 'padrão_imagem', 'foto', 'captura_tela', 'screenshot', 'imagem_visual']

    for escrita in text_type:
        if escrita in type.lower():
            type = "text"

    for escrita in element_type:
        if escrita in type.lower():
            type = "element"

    for escrita in imagem_type:
        if escrita in type.lower():
            type = "image"

    return find_elements.backcode__dont_use__wait_for_d(driver, object, type, timeout=tempo)

def selectfox(elemento, method, key):
    """
    Seleciona uma opção em um elemento <select>.

    - Parâmetros:
        - elemento: Elemento <select> encontrado pelo Selenium.
        - method: Método de seleção ('index', 'text' ou 'value').
        - key: Valor usado na seleção (índice, texto visível ou valor do atributo 'value').

    - Exemplo:
        elemento_select = bc.find_element_with_wait("xpath", '//select[@value="VALUE_DO_PRIMEIRO_SELECT"]')

        primeira_option = selectfox(elemento_select, "text", "TEXTO DO PRIMEIRO SELECT")
        primeira_option = selectfox(elemento_select, "value", "VALUE_DO_PRIMEIRO_SELECT")
        primeira_option = selectfox(elemento_select, "index", "0")

    """

    variations = {
        'index': ['index', 'indice', 'índice', 'posição', 'posição_na_lista', 'opção_numero', 'número_da_opção', 'opcao_indice', 'indice_da_opcao', 'numero_de_entrada'],
        'text': ['text', 'texto', 'texto_visível', 'conteúdo', 'frase', 'texto_exibido', 'palavra', 'mensagem', 'texto_na_página', 'texto_da_opcao'],
        'value': ['value', 'valor', 'valor_opcao', 'valor_da_opcao', 'valor_selecionado', 'value_opcao', 'valor_item', 'opcao_valor', 'item_valor', 'valor_atributo']
    }

    for key_method, values in variations.items():
        if method.lower() in map(str.lower, values):
            method = key_method
            break

    else:
        raise ValueError(f"Método '{method}' não é válido. Escolha entre 'index', 'text' ou 'value'.")

    select = Select(elemento)
    if method == "value":
        select.select_by_value(key)

    if method == "text":
        elements = WebDriverWait(elemento, 10).until(EC.visibility_of_all_elements_located((By.XPATH, '//option')))
        for elm in elements:
            if key.lower().strip() in elm.text.lower().strip():
                select.select_by_visible_text(elm.text)
                return
        raise ModuleNotFoundError(f"Option {key} não encontrada")

    if method == "index":
        select.select_by_index(key)

def pop_up_extract(text: bool = False, accept: bool = False, timeout: int = 10, driver_instance: Optional[WebElement] = None):
    """ Identifica um pop-up simples extraindo o texto e aceitando ele também. \n

    - Como usar:
        Chame a função e registrando ela em uma variável, and if you iniciate a driver without the library pass the driver variable.

    - Exemplo:
        text = bc.pop_up_extract(text:True, accept:True, timeout=5)

    - OBS: Para uma espera infinit (até o elemento aparecer) coloque timeout = 0
    """
    global driver
    extract_text = None

    if not driver_instance: driver_instance = driver
    if timeout == 0:
        timeout = float("inf")

    attempts = 0
    while attempts < timeout:
        try:
            jan = driver_instance.switch_to.alert

            if text == True:
                extract_text = jan.text

            if accept == True:
                jan.accept()

            if extract_text:
                return extract_text
            return

        except Exception as e:
            last_exception = e
            print(e)
            attempts += 1
            time.sleep(0.8)

    raise ValueError("Pop-up não encontrado") from last_exception

def cpf_or_cnpj(numero: str) -> str:
    """
    Identifica se um número é um CPF ou CNPJ.

    - Retorna "CPF" se o número for um CPF válido.
    - Retorna "CNPJ" se o número for um CNPJ válido.
    - Retorna "Inválido" se não for nenhum dos dois.
    """

    # Remove caracteres não numéricos (como pontos e traços)
    numero = re.sub(r"\D", "", numero)

    if len(numero) == 11:
        return "CPF" if numero.isdigit() else "Inválido"

    elif len(numero) == 14:
        return "CNPJ" if numero.isdigit() else "Inválido"

    return "Inválido"

janela = None
@staticmethod
def mostrar_mensagem(mensagem, tamanho_fonte=12, negrito=False, button: Optional[bool] = True):

    global janela

    try: fechar_janela(janela)
    except: pass

    root = tk.Tk()
    root.withdraw()

    janela = tk.Toplevel()
    janela.title("Atenção!")
    janela.configure(bg="white")

    largura, altura = 400, 200
    pos_x = (janela.winfo_screenwidth() - largura) // 2
    pos_y = (janela.winfo_screenheight() - altura) // 2
    janela.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")
    janela.resizable(False, False)
    janela.attributes("-topmost", True)

    estilo_fonte = ("Helvetica", tamanho_fonte, "bold" if negrito else "normal")

    label = tk.Label(janela, text=mensagem, bg="white", fg="black",
                     font=estilo_fonte, wraplength=380, justify="center")
    label.pack(expand=True, padx=20, pady=20)

    if button:
        tk.Button(janela, text="OK", command=lambda: (janela.destroy(), root.destroy()),
                  width=10, font=("Helvetica", 10)).pack(pady=10)

    janela.grab_set()
    janela.focus_set()
    if button: janela.wait_window()
    else: root.mainloop()
    return janela

def fechar_janela(janela_=None):
    global janela
    if janela_ == None: janela.destroy()
    else: janela_.destroy()

def move_mouse_smoothly(element, click=False):
    import pyautogui
    cordenadas_botao_certificado = element.location
    x = cordenadas_botao_certificado["x"]+140
    y = cordenadas_botao_certificado["y"]+112

    actual_position = pyautogui.position()
    mouse_x = actual_position[0]
    mouse_y = actual_position[1]

    print(x, y)
    while True:
        distancia = math.sqrt((x - mouse_x) ** 2 + (y - mouse_y) ** 2)

        # Se a distância for menor que 200 pixels, o movimento será mais lento
        if distancia < 200:
            if mouse_x < x: mouse_x += random.randint(1, 20)
            elif mouse_x > x: mouse_x -= random.randint(1, 20)

            if mouse_y < y: mouse_y += random.randint(1, 10)
            elif mouse_y > y: mouse_y -= random.randint(1, 10)

            pyautogui.moveTo(mouse_x, mouse_y, duration=(random.randint(10, 100) / 1000))

        else:
            # Quando a distância é maior, o movimento é mais rápido
            if mouse_x < x: mouse_x += random.randint(10, 50)
            elif mouse_x > x: mouse_x -= random.randint(10, 50)

            if mouse_y < y: mouse_y += random.randint(5, 20)
            elif mouse_y > y: mouse_y -= random.randint(5, 20)

            pyautogui.moveTo(mouse_x, mouse_y, duration=(random.randint(50, 300) / 1000))

        if distancia < 7:
            if click == True: pyautogui.click()
            break

RESET, GR, ORANGE, DK_ORANGE = "\033[0m", "\033[38;5;34m", "\033[38;5;214m", "\033[38;5;130m"
result = subprocess.run(['pip', 'show', "bcpkgfox"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
version_line = next((line for line in result.stdout.decode().splitlines() if line.startswith('Version:')), None)
try: print(f"\n\n{ORANGE}Biblioteca BCFOX importada - {re.sub(r"[^0-9.b]", "", version_line)}{RESET}")
except: pass
create_dirs()