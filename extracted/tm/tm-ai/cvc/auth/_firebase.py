"""
cvc.auth — Authentication and user tracking via Firebase.
"""
import json
import webbrowser
import threading
from pathlib import Path
from http.server import BaseHTTPRequestHandler, HTTPServer
import httpx
from rich.console import Console

console = Console()

# Placeholders - REPLACE THESE BEFORE PRODUCTION
FIREBASE_CONFIG = {
    "apiKey": "AIzaSyC7ANXuqZ2BsI6w79Gzz1zyOGvJ2tZANOU",
    "authDomain": "cognitive-version-control.firebaseapp.com",
    "projectId": "cognitive-version-control",
    "storageBucket": "cognitive-version-control.firebasestorage.app",
    "messagingSenderId": "810190088643",
    "appId": "1:810190088643:web:407641b856740858f47576"
}

AUTH_FILE = Path.home() / ".cvc" / "auth.json"

HTML_TEMPLATE = f"""
<!DOCTYPE html>
<html>
<head>
    <title>CVC CLI Login</title>
    <style>
        body {{ font-family: system-ui, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; background: #1a1a1a; color: #fff; margin: 0; }}
        .card {{ background: #2a2a2a; padding: 2rem; border-radius: 8px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.3); border-top: 4px solid #cc3333; }}
        button {{ background: #cc3333; color: white; border: none; padding: 10px 20px; border-radius: 4px; font-size: 16px; cursor: pointer; margin: 10px; font-weight: bold; }}
        button:hover {{ background: #ff4444; }}
        #github-btn {{ background: #333; }}
        #github-btn:hover {{ background: #444; }}
        #status {{ margin-top: 15px; color: #aaa; }}
    </style>
</head>
<body>
    <div class="card">
        <h2>CVC CLI Authentication</h2>
        <p>Sign in to continue to the Cognitive Version Control CLI</p>
        <button id="google-btn">Sign in with Google</button>
        <button id="github-btn">Sign in with GitHub</button>
        <div id="status"></div>
    </div>

    <script type="module">
        import {{ initializeApp }} from "https://www.gstatic.com/firebasejs/10.9.0/firebase-app.js";
        import {{ getAuth, signInWithPopup, GoogleAuthProvider, GithubAuthProvider }} from "https://www.gstatic.com/firebasejs/10.9.0/firebase-auth.js";

        const firebaseConfig = {json.dumps(FIREBASE_CONFIG)};
        const app = initializeApp(firebaseConfig);
        const auth = getAuth(app);

        async function handleAuth(provider, providerName) {{
            const statusUrl = document.getElementById('status');
            statusUrl.innerText = "Waiting for " + providerName + "...";
            try {{
                const result = await signInWithPopup(auth, provider);
                const user = result.user;
                const token = await user.getIdToken();
                
                statusUrl.innerText = "Authenticated! Completing login...";
                
                const response = await fetch("/callback", {{
                    method: "POST",
                    headers: {{ "Content-Type": "application/json" }},
                    body: JSON.stringify({{
                        token: token,
                        uid: user.uid,
                        email: user.email,
                        display_name: user.displayName,
                        provider: providerName
                    }})
                }});
                
                if (response.ok) {{
                    statusUrl.innerText = "Success! You can close this window and return to your terminal.";
                    document.getElementById('google-btn').style.display = 'none';
                    document.getElementById('github-btn').style.display = 'none';
                }} else {{
                    statusUrl.innerText = "Error completing login. Please try again.";
                }}
            }} catch (error) {{
                console.error(error);
                statusUrl.innerText = "Error: " + error.message;
            }}
        }}

        document.getElementById('google-btn').addEventListener('click', () => handleAuth(new GoogleAuthProvider(), 'google'));
        document.getElementById('github-btn').addEventListener('click', () => handleAuth(new GithubAuthProvider(), 'github'));
    </script>
</body>
</html>
"""

class AuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/login":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(HTML_TEMPLATE.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()
            
    def do_POST(self):
        if self.path == "/callback":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode("utf-8"))
            
            # Save auth data
            AUTH_FILE.parent.mkdir(parents=True, exist_ok=True)
            AUTH_FILE.write_text(json.dumps(data, indent=2))
            
            # Update user in Firestore silently
            update_user_firestore(data, "cvc_cli")
            
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status": "ok"}')
            
            # Signal the server to shut down
            threading.Thread(target=self.server.shutdown).start()

    def log_message(self, format, *args):
        # Suppress logging
        pass

def update_user_firestore(user_data: dict, service_type: str):
    """Update user record in Firestore using REST API to avoid heavy SDKs."""
    project_id = FIREBASE_CONFIG["projectId"]
    if project_id == "YOUR_PROJECT_ID":
        # Cannot update if not configured
        return
        
    url = f"https://firestore.googleapis.com/v1/projects/{project_id}/databases/(default)/documents/users/{user_data['uid']}?updateMask=email&updateMask=displayName&updateMask=provider&updateMask=serviceType&updateMask=lastActiveAt"
    
    import datetime
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    payload = {
        "fields": {
            "email": {"stringValue": user_data.get("email", "")},
            "displayName": {"stringValue": user_data.get("display_name", "")},
            "provider": {"stringValue": user_data.get("provider", "")},
            "serviceType": {"stringValue": service_type},
            "lastActiveAt": {"timestampValue": now}
        }
    }
    
    try:
        # Require authentication to write to the database using the token
        headers = {"Authorization": f"Bearer {user_data['token']}"}
        # In this minimal example, we just fire and forget
        httpx.patch(url, json=payload, headers=headers)
    except Exception:
        pass # Ignore errors for analytics

def login_flow():
    """Starts local server and opens browser for login."""
    if FIREBASE_CONFIG["projectId"] == "YOUR_PROJECT_ID":
        console.print("[bold yellow]Warning:[/bold yellow] Firebase is not fully configured. Using placeholder configuration.")
        
    port = 13421
    server = HTTPServer(("localhost", port), AuthHandler)
    url = f"http://localhost:{port}/login"
    
    console.print(f"Opening your browser to authenticate: [bold underline cyan]{url}[/bold underline cyan]")
    console.print("Waiting for authentication... (Press Ctrl+C to cancel)")
    
    webbrowser.open(url)
    
    try:
        server.serve_forever()
        console.print("\n[bold green]✓[/bold green] Successfully authenticated!")
    except KeyboardInterrupt:
        console.print("\n[bold red]✗[/bold red] Login cancelled.")
        server.server_close()
        
def logout():
    """Clears local authentication data."""
    if AUTH_FILE.exists():
        AUTH_FILE.unlink()
        console.print("[bold green]✓[/bold green] Successfully logged out.")
    else:
        console.print("You are not currently logged in.")

def get_current_user():
    """Returns the currently logged in user dictionary or None."""
    if AUTH_FILE.exists():
        try:
            return json.loads(AUTH_FILE.read_text())
        except Exception:
            return None
    return None
