from typing import Optional
import time

def invoke_api_list(link: str, token: str, method: Optional[str] = "GET", headers: Optional[str] = None, print_response: Optional[bool] = False) -> dict:
    import requests

    """
    Exemplo de uso abaixo:

        import BCFOX as bc

        def invoke_api_list(self):
            link = 'https://linK_api.com.br/apis/{parametros}'
            token = 12345ABCDE12345ABCDE12345ABCDE12345ABCDE12345

            bc.invoke_api_list(link, token, print_response=True)

        OBS: o print_response vem por padrão desligado, caso você queira ativa o print da view coloque 'ON'

        """
    http_methods = {
        "POST": requests.post,
        "GET": requests.get,
        "PUT": requests.put,
        "DELETE": requests.delete,
        "PATCH": requests.patch
    }

    # Verifica se o método fornecido é válido
    method = method.upper()
    if method not in http_methods:
        raise ValueError(f"Método HTTP inválido. Use um dos seguintes: {', '.join(http_methods.keys())}.")

    payload = {}
    if headers is None: headers = {"x-access-token": token}
    else: {headers: token}

    max_attempts = 5
    for attempt in range(1, max_attempts + 1):
        from .get_driver import RD, RESET
        try:

            # Realiza a requisição com o método correto
            if method == "GET" or method == "DELETE": response_insert = http_methods[method](link, params=payload, headers=headers)
            else: response_insert = http_methods[method](link, json=payload, headers=headers)
            if "Sequelize" in response_insert.json(): raise SystemError(f" {RD}>>> {response_insert.json()}{RESET}")

            if print_response == True:
                print(f"\n{response_insert.json()}")

            return response_insert.json()

        except Exception as e:
            print(f"Tentativa {attempt} falhou: {e}")

            if attempt < max_attempts:
                print("Tentando novamente em 5 segundos...")
                time.sleep(5)
                continue

            else: raise ValueError("Api list falhou")

def invoke_api_proc(link: str, payload_vars: dict, token: str, method: str, print_response: Optional[bool] = False) -> str:
    import requests

    """
    Exemplo de uso abaixo:

    import BCFOX as bc

    def invoke_api_proc_final(self):
        link = https://linK_api.com.br/apis/{parametros}
        token = 12345ABCDE12345ABCDE12345ABCDE12345ABCDE12345

        payload = [
        {"ID":self.id},
        {"STATUS":self.status},
        {"PAGAMENTO":self.pagamento}
        ...
        ]

        bc.invoke_api_proc_final(link, payload, token, print_response=True)

    OBS: o print_response vem por padrão desligado, caso você queria ver o returno do response coloque 'ON'

    """

    http_methods = {
        "POST": requests.post,
        "GET": requests.get,
        "PUT": requests.put,
        "DELETE": requests.delete,
        "PATCH": requests.patch,
    }

    # Verifica se o método fornecido é válido
    method = method.upper()
    if method not in http_methods:
        raise ValueError(f"Método HTTP inválido. Use um dos seguintes: {', '.join(http_methods.keys())}.")

    # PROC PARA FINALIZAR PROCESSO
    url = link

    payload = payload_vars

    if print_response == True:
        print(f'payload: {payload}')

    headers = {"x-access-token": token}

    max_attempts = 5
    for attempt in range(1, max_attempts + 1):
        try:
            # Realiza a requisição com o método correto
            if method == "GET" or method == "DELETE": response_insert = http_methods[method](url, params=payload, headers=headers)
            else: response_insert = http_methods[method](url, json=payload, headers=headers)

            response_insert.raise_for_status()

            if print_response == True:
                print(response_insert.json())

            try:
                status = response_insert.json()[0]['STATUS']

                if status != 200:
                    from .get_driver import ORANGE, RESET, RD
                    print(f' {ORANGE} > {RD}Erro ao atualizar caso!{RESET}')
                    invoke_api_proc()
                else: return status
            except: pass
            return None

        except Exception as e:
            print(f"Tentativa {attempt} falhou: {e}")

            if attempt < max_attempts:
                print("Tentando novamente em 5 segundos...")
                time.sleep(5)
                continue

            else: raise ValueError("Api proc final falhou")

def invoke_api_proc_log(link, id_robo, token):
    import requests

    """Só colocar o ID do robo e o Token direto """

    payload = {
        "id": id_robo
    }

    print(payload)

    headers = {
        "x-access-token": token}

    responseinsert = requests.request(
        "POST", link, json=payload, headers=headers)
    print(f"\n{responseinsert.json()}")

# FIX: Não funcional ainda, está aqui como base para o futuro
def captcha_solver():
    import requests


    # Configurações
    API_KEY = "40efad0ffa6a4398bb7829185b1729e9"
    SITE_KEY = "6LeARtIZAAAAAEyCjkSFdYCBZG6JahcIveDriif3"  # A "sitekey" do reCAPTCHA
    PAGE_URL = "https://consorcio.cnpseguradora.com.br/"  # URL onde o CAPTCHA aparece

    def enviar_captcha():
        url = "https://2captcha.com/in.php"
        payload = {
            "key": API_KEY,
            "method": "userrecaptcha",
            "googlekey": SITE_KEY,
            "pageurl": PAGE_URL,
            "json": 1,
        }
        response = requests.post(url, data=payload)
        result = response.json()

        if result.get("status") == 1:
            return result.get("request")  # ID da tarefa
        else:
            raise Exception(f"Erro ao enviar CAPTCHA: {result.get('request')}")

    def verificar_captcha(task_id):
        url = "https://2captcha.com/res.php"
        payload = {
            "key": API_KEY,
            "action": "get",
            "id": task_id,
            "json": 1,
        }

        while True:
            response = requests.get(url, params=payload)
            result = response.json()

            if result.get("status") == 1:  # Solução disponível
                return result.get("request")  # TOKEN do CAPTCHA
            elif result.get("request") == "CAPCHA_NOT_READY":  # Ainda processando
                time.sleep(5)  # Aguardar antes de tentar novamente
            else:
                raise Exception(f"Erro ao verificar CAPTCHA: {result.get('request')}")

    def resolver_recaptcha():
        try:
            print("Enviando CAPTCHA para o TwoCaptcha...")
            task_id = enviar_captcha()
            print(f"Tarefa enviada! ID: {task_id}")

            print("Aguardando solução...")
            token = verificar_captcha(task_id)
            print(f"CAPTCHA resolvido! Token: {token}")

            return token
        except Exception as e:
            print(f"Erro: {e}")

    id = enviar_captcha()
    verificar_captcha(id)
    token_resolution = resolver_recaptcha()

    self.driver.execute_script("""
        var element = document.querySelector('input[id="g-recaptcha-response]"');
        if (element) {
            element.setAttribute('type', 'text');
        }
    """)

    self.driver.execute_script(f"""
    const element = document.querySelector('textarea[id="g-recaptcha-response"]');
    if (element) {{
        element.value = "{token_resolution}";
    }}
    """)
