import os

API_URL = "https://api.spotml.io"

if os.getenv("SPOTML_ENV") == "LOCAL":
    API_URL = "http://localhost:3000"
