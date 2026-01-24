# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.assess.rules.non_dataflow_rule import NonDataflowRule
from contrast.agent.policy.registry import register_trigger_rule

crypto_triggers = {
    "crypto-bad-mac": [
        {
            "module": "hashlib",
            "method_name": "new",
            "source": "ARG_0,KWARG:name",
            "good_value": "^(?:MDC2|RIPEMD160|SHA224|SHA256|SHA384|SHA512)",
        },
        {
            "module": "hashlib",
            "method_name": "md5",
        },
        {
            "module": "hashlib",
            "method_name": "sha1",
        },
        {
            "module": "Crypto.Hash.MD2",
            "class_name": "MD2Hash",
            "method_name": "__init__",
        },
        {
            "module": "Crypto.Hash.MD4",
            "class_name": "MD4Hash",
            "method_name": "__init__",
        },
        {
            "module": "Crypto.Hash.MD5",
            "class_name": "MD5Hash",
            "method_name": "__init__",
        },
        {
            "module": "Crypto.Hash.SHA1",
            "class_name": "SHA1Hash",
            "method_name": "__init__",
        },
        {
            "module": "Cryptodome.Hash.MD2",
            "class_name": "MD2Hash",
            "method_name": "__init__",
        },
        {
            "module": "Cryptodome.Hash.MD4",
            "class_name": "MD4Hash",
            "method_name": "__init__",
        },
        {
            "module": "Cryptodome.Hash.MD5",
            "class_name": "MD5Hash",
            "method_name": "__init__",
        },
        {
            "module": "Cryptodome.Hash.SHA1",
            "class_name": "SHA1Hash",
            "method_name": "__init__",
        },
    ],
    "crypto-weak-randomness": [
        {
            "module": "random",
            "method_name": "random",
        },
        {
            "module": "random",
            "method_name": "randint",
        },
        {
            "module": "random",
            "method_name": "randrange",
        },
        {
            "module": "random",
            "method_name": "uniform",
        },
    ],
    "crypto-bad-ciphers": [
        {
            "module": "Crypto.Cipher.Blowfish",
            "method_name": "new",
        },
        {
            "module": "Crypto.Cipher.DES",
            "method_name": "new",
        },
    ],
}


for name, nodes in crypto_triggers.items():
    register_trigger_rule(NonDataflowRule.from_nodes(name, nodes))
