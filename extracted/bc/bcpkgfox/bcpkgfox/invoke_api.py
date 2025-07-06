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

def invoke_api_proc(link: str, payload_vars: dict, token: str, method: str, print_response: Optional[bool | str] = False) -> str:
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
    OBS2: Caso queria printar o json response intero coloque: 'print_response = "full"'

    """

    if isinstance(print_response, str):
        if print_response.lower().strip() ==  "full":
            print_response = "full"

        else:
            raise ValueError("print_response com variável inválida\n Use tipo 'bool' ou escreva 'full' (str) para response completo")

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

    if print_response == True or print_response == "full":
        print(f'payload: {payload}')

    headers = {"x-access-token": token}

    max_attempts = 5
    for attempt in range(1, max_attempts + 1):
        try:
            # Realiza a requisição com o método correto
            if method == "GET" or method == "DELETE": response_insert = http_methods[method](url, params=payload, headers=headers)
            else: response_insert = http_methods[method](url, json=payload, headers=headers)

            response_insert.raise_for_status()

            if print_response == True or print_response == "full":
                print(response_insert.json())

            if print_response == "full":
                return response_insert.json()

            status = response_insert.json()[0]['STATUS']
            return status

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
