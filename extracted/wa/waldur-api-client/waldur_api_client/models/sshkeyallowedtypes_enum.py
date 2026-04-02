from enum import Enum


class SSHKEYALLOWEDTYPESEnum(str, Enum):
    ECDSA_SHA2_NISTP256 = "ecdsa-sha2-nistp256"
    ECDSA_SHA2_NISTP384 = "ecdsa-sha2-nistp384"
    ECDSA_SHA2_NISTP521 = "ecdsa-sha2-nistp521"
    SK_ECDSA_SHA2_NISTP256OPENSSH_COM = "sk-ecdsa-sha2-nistp256@openssh.com"
    SK_SSH_ED25519OPENSSH_COM = "sk-ssh-ed25519@openssh.com"
    SSH_ED25519 = "ssh-ed25519"
    SSH_RSA = "ssh-rsa"

    def __str__(self) -> str:
        return str(self.value)
