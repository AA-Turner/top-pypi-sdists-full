import json
import tempfile

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


class GetCredsGworkspace:
    def __init__(self, token_dict=None, credentials_dict=None, scopes=None):
        self.token_dict = token_dict
        self.credentials_dict = credentials_dict
        self.scopes = scopes or ["https://www.googleapis.com/auth/spreadsheets",
                                "https://www.googleapis.com/auth/drive",
                                "https://mail.google.com/",
                                ]

    def get_creds_gworkspace(self):
        creds = None
        try:
            if self.token_dict:
                with tempfile.NamedTemporaryFile(mode='w+', delete=False) as token_file:
                    json.dump(self.token_dict, token_file)
                    token_file.flush()
                    token_path = token_file.name

                    creds = Credentials.from_authorized_user_file(token_path, self.scopes)
            
            # Caso o arquivo de token não exista ou não seja válido
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    # Usar arquivo temporário para as credenciais
                    if self.credentials_dict:
                        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as creds_file:
                            json.dump(self.credentials_dict, creds_file)
                            creds_file.flush()
                            creds_path = creds_file.name

                        flow = InstalledAppFlow.from_client_secrets_file(creds_path, self.scopes)
                        creds = flow.run_local_server(port=0)

                    # Escreve o novo token no arquivo temporário
                    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as token_file:
                        token_file.write(creds.to_json())

        except Exception as e:
            return None

        return creds