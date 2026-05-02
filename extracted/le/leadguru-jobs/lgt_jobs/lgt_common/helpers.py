def update_credentials(credentials, token, cookies):
    credentials.token = token
    credentials.cookies = cookies
    credentials.invalid_creds = False
    return credentials
