from hashlib import sha256
from nsj_gcf_utils.json_util import json_dumps

"""Cria um hash usando SHA256 para ser usado para autenticação pelo webhook.
   Ele recebe a url, o body e o metodo da requisição junto com uma chave especial.
   Depois junta todos os dados e usa SHA256 para criar o hash.
"""
def hash_webhook(url, body, method, key):
    # Converte o body para string caso o body seja um dict(json)
    if isinstance(body, dict):
        body = json_dumps(body)

    # tipagem para ajudar o autocomplete de IDEs
    # str na key caso ela seja um número ou um uuid
    hash: str = url + body + method + str(key) 

    return sha256(hash.encode()).hexdigest()

# Teste para o integrador vmpay
if __name__ == '__main__':
    print(hash_webhook("http://localhost/produtos",{
        "esquema": "estoque",
        "tabela": "produtos",
        "operacao": "I",
        "dados": {
            "especificacao": "teste14",
            "codigo": "1234",
            "codigodebarras": "",
            "estabelecimento":"5e5a86b7-d494-4c31-806a-a5e74862403a",
            "grupoempresarial": "0ef4df5d-9881-4c3c-b8ea-a09149f799a5",
            "grupodeinventario": 0
        }
    }, "POST","124325"))