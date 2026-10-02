# -*- coding: utf-8 -*-

import sys

if sys.version_info[:2] >= (3, 10):
    from cryptography import x509
    from cryptography.x509.oid import NameOID
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.hazmat.backends import default_backend
else:
    from OpenSSL import crypto


class WsaaCertificate(object):

    def __init__(self, key):
        self.key = key
        self.country_code = None
        self.state_name = None
        self.company_name = None
        self.company_vat = None

    def validate_values(self):
        """ Validamos que esten todos los campos necesarios seteados """
        values = vars(self)
        for value in values:
            if not values.get(value):
                raise AttributeError('Falta configurar alguno de los siguientes campos:\n'
                                     'Codigo de pais, Provincia, Nombre de la empresa o CUIT')

    def generate_certificate_request(self, hash_sign='sha256', ou='odoo'):

        self.validate_values()

        if sys.version_info[:2] >= (3, 10):
            # Cargamos la clave privada desde el PEM
            try:
                private_key = serialization.load_pem_private_key(
                    self.key.encode('utf-8'),
                    password=None,
                    backend=default_backend()
                )
            except Exception as e:
                raise ValueError("Formato de clave privada inválido") from e

            # Cargamos los datos del certificado
            subject = x509.Name([
                x509.NameAttribute(NameOID.COUNTRY_NAME, self.country_code),
                x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, self.state_name),
                x509.NameAttribute(NameOID.ORGANIZATION_NAME, self.company_name),
                x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, ou),
                x509.NameAttribute(NameOID.COMMON_NAME, self.company_name),
                x509.NameAttribute(NameOID.SERIAL_NUMBER, 'CUIT {}'.format(self.company_vat)),
            ])

            # Validamos que el algoritmo de hash sea válido
            try:
                hash_algo = getattr(hashes, hash_sign.upper())()
            except AttributeError:
                raise ValueError("Algoritmo de hash inválido: " + hash_sign)

            # Creamos y firmamos el certificado
            csr = (
                x509.CertificateSigningRequestBuilder()
                .subject_name(subject)
                .sign(private_key, hash_algo, default_backend())
            )

            return csr.public_bytes(serialization.Encoding.PEM)

        else:
            # Utilizamos la libreria de crypto para generar el pedido de certificado
            req = crypto.X509Req()
            req.get_subject().C = self.country_code
            req.get_subject().ST = self.state_name
            req.get_subject().O = self.company_name
            req.get_subject().OU = ou
            req.get_subject().CN = self.company_name
            req.get_subject().serialNumber = 'CUIT {}'.format(self.company_vat)

            # Validamos el formato de la key
            key = crypto.load_privatekey(crypto.FILETYPE_PEM, self.key)
            self.key = crypto.dump_privatekey(crypto.FILETYPE_PEM, key)

            # Firmamos con la key y el hash el certificado
            req.set_pubkey(key)
            req.sign(key, hash_sign)

            return crypto.dump_certificate_request(crypto.FILETYPE_PEM, req)


class WsaaPrivateKey(object):

    def __init__(self, length=2048):
        self.length = length
        self.key = None

    def generate_rsa_key(self):
        if sys.version_info[:2] >= (3, 10):
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=self.length,
                backend=default_backend()
            )
            self.key = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            )
        else:
            pkey = crypto.PKey()
            pkey.generate_key(crypto.TYPE_RSA, self.length)
            self.key = crypto.dump_privatekey(crypto.FILETYPE_PEM, pkey)
