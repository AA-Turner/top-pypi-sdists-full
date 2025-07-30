'''
A grande maioria das classes e funções tem descrição explicando com detalhes o funcionamento e parametros
Para ver clicar na classe/função e apertar ctrl+K ctrl+I (VSCODE)
'''
import neri_library as nr  # Só precisa de um import para
from neri_library import DK_ORANGE, ORANGE, GR, RD, RESET  # Colors for terminal

# Default
import time
import sys
import os

class Browser():
    def __init__(self):
        super().__init__()

        self.arguments = None
        self.instance = None
        self.browser = None
        self.el = None

    @staticmethod
    def __simple_example():
        '''
        Aqui é só um exemplo de como é fácil iniciar um navegador com a lib.
        Ja vem com configurações para evitar detecção e passar por captchas.
        '''
        Browser = nr.Instancedriver().initialize_driver()
        Browser.get('URL SITE')


    def browser_iniciate(self):
        '''
        Aqui é um exemplo de driver em produção.
        '''
        print(f'{ORANGE} [ Inicializando Browser ] {RESET}')

        # Inicia a instância do Navegador
        self.instance = nr.Instancedriver(
            Browser= 'Chrome',
            # Browser="Firefox",
            # Browser="edge",
            # Browser="internet explorer",
        )

        # Inicia a instancia dos argumentos (opcional, não precisa por nenhum)
        self.arguments = self.instance.arguments # Instância dos argumentos

        # Fix: Abaixo alguns dos principais exemplos de argumento do selenium (tem todos)
        # Exemplos de args para desligar indicadores de automação
        self.arguments.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.arguments.add_experimental_option("useAutomationExtension", False)
        self.arguments.add_argument("--disable-blink-features=AutomationControlled")
        self.arguments.add_argument("--disable-blink-features")
        self.arguments.add_argument("--disable-infobars")
        self.arguments.add_argument("--disable-blink-features=AutomationControlled")
        self.arguments.add_argument("--blink-settings=imagesEnabled=false")

        # Exemplos de args para evitar detecção da automação nos sites e captchas
        # Fix: Mas ja vem por padrão diversos argumentos tratando isso na função de 'initialize_driver' 
        self.arguments.add_argument("--disable-background-networking")
        self.arguments.add_argument("--disable-sync")
        self.arguments.add_argument("--disable-client-side-phishing-detection")
        self.arguments.add_argument("--disable-popup-blocking")
        self.arguments.add_argument("--disable-default-apps")
        self.arguments.add_argument("--disable-features=IsolateOrigins,site-per-process")
        self.arguments.add_argument("--disable-features=BlockInsecurePrivateNetworkRequests")
        self.arguments.add_argument("--ignore-certificate-errors")
        self.arguments.add_argument("--disable-gpu")

        # Abaixo alguns exemplos para remover os logs do terminal (deixar mais limpo)
        self.arguments.add_argument("--log-level=3")
        self.arguments.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.arguments.add_experimental_option("useAutomationExtension", False)

        # Exemplo de adicionar extensão (pega automático tanto pasta como .crx)
        # self.instance.add_extensions('your_extension')

        # Inicia o browser (driver)
        self.browser = self.instance.initialize_driver(maximize=True)

        # Instancia o 'finder', contém todas as funções de busca envolvendo o navegador
        self.finder = self.instance.elements

class RPA_example(Browser):
    def __init__(self):
        super().__init__()

    def open_site(self):
        self.driver.get('https://github.com/NeriAzv')

        self.cidade = cidade
        self.pop_up_protection.start()

        # Pesquisa
        pesquisa = self.find_element_w(By.ID, 'searchGeneral')
        time.sleep(1)
        pesquisa.send_keys(cidade)

        # Espera carregamento pesquisa
        tempo = 0
        while tempo < 30:
            resultados = self.find_elements_w(By.XPATH, '//ul[@id="autocompleteSuggestions"]//li')

            if resultados:
                break
            else:
                time.sleep(1)
                tempo += 1

        # Resutaldos pesquisa
        elemento_resultados_pesquisa = self.find_element_w(By.ID, 'autocompleteSuggestions')
        soup = BeautifulSoup(elemento_resultados_pesquisa.get_attribute('outerHTML'), 'html.parser')
        ul = soup.find('ul', id='autocompleteSuggestions')

        cidades_extraidas = []
        extrair = False
        for tag in ul.find_all(recursive=False):
            if tag.name == 'h6':
                if 'Cidades' in tag.text:
                    extrair = True
                    continue
                elif extrair:
                    break

            if extrair and tag.name == 'li':
                cidades_extraidas.append(tag)

        if not cidades_extraidas:
            raise Exception(f"{RED} > Cidade {cidade} não presente no site, verifique o nome. {RESET}")

        # Eu poderia ter clicado no ultimo for, mas estou fazendo separado pegar todas as cidades e fazer um LOG mais organizado
        for cidade_site in cidades_extraidas:
            cidade_site_formatado = self.remover_acentos(cidade_site.text).lower()
            cidade_user_formatado = self.remover_acentos(cidade).lower()

            # Retorna em porcentagem quanto similar está com o nome do site (evita erros de usuários)
            if cidade_site_formatado in cidade_site_formatado:

                self.find_element_w(
                    By.XPATH,
                    f'//ul[@id="autocompleteSuggestions"]//li[normalize-space()="{cidade_site.text.strip()}"]'
                ).click()

                return

        raise Exception(f"{RED} > Cidade {cidade} não presente no site, verifique o nome. {RESET}")

    def extrair_previsao(self) -> dict:

        espera_site = 0
        while espera_site <= 5:

            try:
                soup = BeautifulSoup(self.driver.page_source, "html.parser")
                ul = soup.find("ul", class_="variables-list")
                resultado_json = {
                    "cidade": self.cidade,
                    "temperatura_min": None,
                    "temperatura_max": None,
                    "condicao": None,
                    "umidade_min": None,
                    "umidade_max": None,
                    "vento": None,
                }

                if not ul:
                    return resultado_json

                for li in ul.find_all("li", class_="item"):
                    label = li.find("span", class_="variable").get_text(strip=True)

                    if label == "Temperatura":
                        spans = li.select("span.-gray-light")
                        min_txt = spans[0].get_text(strip=True)
                        max_txt = spans[1].get_text(strip=True)
                        resultado_json["temperatura_min"] = min_txt if min_txt.endswith("°") else min_txt + "°"
                        resultado_json["temperatura_max"] = max_txt if max_txt.endswith("°") else max_txt + "°"

                    elif label == "Umidade":
                        spans = li.select("span.-gray-light")
                        resultado_json["umidade_min"] = spans[0].get_text(strip=True)
                        resultado_json["umidade_max"] = spans[1].get_text(strip=True)

                    elif label == "Vento":
                        texto = li.find("div", class_="_flex").get_text(separator=" ", strip=True)
                        texto_limpo = " ".join(texto.split())
                        resultado_json["vento"] = texto_limpo.replace("Vento", "", 1).strip()

                    elif label == "Sol":
                        nasc, _, pst = li.find("span", recursive=False).get_text(strip=True).partition(" ")
                        resultado_json["condicao"] = f"{nasc} {pst}"

                return resultado_json

            except:
                time.sleep(1)
                espera_site +=1



class Logs:
    ''' Server somente para impressão de resultados, não afeta o funcionamento do robo '''
    def imprimir_logs(self, log_resultado: dict):
        if not log_resultado:
            return

        print(f"\n{BOLD}{BLUE} {log_resultado.get('cidade', '').title()}:{RESET}")

        # Itera sobre o dict
        for chave, valor in log_resultado.items():
            if chave == "cidade":
                continue
            print(f" - {BLUE}{chave.capitalize()}:{RESET} {valor}")

def main():

    # Instâncias
    br = Browser()
    rpa = RPA_example()

    br.browser_iniciate()
    rpa.open_site()

if __name__ == "__main__":
    print(f'{DK_ORANGE} [ Robo Iniciado ] {RESET}')
    main()