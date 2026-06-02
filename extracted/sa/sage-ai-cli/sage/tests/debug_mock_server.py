import re
import json
import os

with open("/Users/laynefaler/.gemini/antigravity/brain/c83ce90c-9e34-44d5-af14-b1ee6d85c486/mock_server_debug.log", "r", encoding="utf-8") as f:
    log_content = f.read()

requests = log_content.split("=====================================")
print(f"Total requests: {len(requests)}")

config_basenames = {
    "package.json", "tsconfig.json", "vite.config.ts", ".env", ".env.example",
    ".gitignore", ".npmrc", "babel.config.js", "metro.config.js", "tailwind.config.js",
    "postcss.config.js", "webpack.config.js"
}

for idx, req in enumerate(requests):
    if "RESPONSE LENGTH: 2" not in req:
        continue
    
    # Extract LAST MESSAGE
    msg_match = re.search(r"LAST MESSAGE:\s*(.*?)\n(?:DOMAIN:|FILENAME:|IS_RN:)", req, re.DOTALL)
    if not msg_match:
        continue
    
    last_msg = msg_match.group(1).strip()
    
    filtered_history = last_msg.lower()
    
    is_repair = (
        "return only a json object" in filtered_history
        or "fix a '" in filtered_history
        or "failure in a" in filtered_history
    )
    
    if is_repair:
        files_to_fix = []
        matches = re.findall(r"##\s+([^\s\n`]+)", last_msg)
        for m in matches:
            m_clean = m.strip("`:")
            if m_clean and "." in m_clean:
                files_to_fix.append(m_clean)
        
        if not files_to_fix:
            path_matches = re.findall(
                r'\b(?:frontend/|backend/|src/|[\w\-]+/)*[\w\-]+\.(?:py|tsx?|jsx?|go|rs|cpp|h|html|css|json)\b',
                last_msg
            )
            for pm in path_matches:
                pm_clean = pm.strip("`'\"\\:,()[]{}<>")
                if pm_clean and "." in pm_clean:
                    files_to_fix.append(pm_clean)
        
        fixes_dict = {}
        for fpath in set(files_to_fix):
            orig_fpath = fpath
            if "src/" in fpath:
                parts = fpath.split("src/", 1)
                fpath = "frontend/src/" + parts[1]
            elif "index.html" in fpath:
                fpath = "frontend/index.html"
            elif "main.jsx" in fpath:
                fpath = "frontend/src/main.jsx"
            elif "main.tsx" in fpath:
                fpath = "frontend/src/main.tsx"
            elif "App.jsx" in fpath:
                fpath = "frontend/src/App.jsx"
            elif "App.tsx" in fpath:
                fpath = "frontend/src/App.tsx"

            basename = os.path.basename(fpath)
            if basename in config_basenames:
                continue
            
            ext = basename.split(".")[-1].lower() if "." in basename else ""
            is_test_file = "test" in basename.lower() or "spec" in basename.lower()
            
            if basename == "index.html":
                fixes_dict[fpath] = "index.html content"
            elif basename == "main.jsx":
                fixes_dict[fpath] = "main.jsx content"
            elif basename == "main.tsx":
                fixes_dict[fpath] = "main.tsx content"
            else:
                if ext in ("jsx", "tsx"):
                    fixes_dict[fpath] = "jsx/tsx content"
                else:
                    fixes_dict[fpath] = "fallback content"
        
        print(f"Request {idx}: is_repair={is_repair}, files_to_fix={files_to_fix}, fixes_dict={fixes_dict}")
