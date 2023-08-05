from google_auth_oauthlib.flow import InstalledAppFlow

CLIENT_SECRET_FILE = 'path/to/your/client_secret.json'
SCOPES = ['https://www.googleapis.com/auth/gmail.send']  # Use appropriate scope

def get_refresh_token():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
    flow.run_local_server(port=0)

if __name__ == "__main__":
    get_refresh_token()
