#!/usr/bin/env python3
"""
Novita Sandbox Test Environment Setup Script

This script is used for:
1. Creating a sandbox based on a template
2. Creating static files in a specified directory inside the sandbox
3. Returning the sandbox ID for subsequent tests

Note: Sandboxes are not automatically cleaned up, manual cleanup via cleanup_sandbox.py is required
"""

import sys
import json
import argparse
from novita_sandbox.core import Sandbox

# Template configuration
TEMPLATE_NAME = "base"
TEMPLATE_ID = "3udmy5pkzmvd35i4w5am"

# Static page HTML content
INDEX_HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Static Site</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .container {
            text-align: center;
            color: white;
            padding: 2rem;
        }
        h1 {
            font-size: 3rem;
            margin-bottom: 1rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
        p {
            font-size: 1.25rem;
            opacity: 0.9;
        }
        .status {
            margin-top: 2rem;
            padding: 1rem 2rem;
            background: rgba(255,255,255,0.2);
            border-radius: 8px;
            backdrop-filter: blur(10px);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Static Site Running</h1>
        <p>Nginx is running on port 80</p>
        <div class="status">
            <p>✅ Service is healthy</p>
        </div>
    </div>
</body>
</html>
"""

# Dockerfile content - Start nginx static server
# Note: COPY uses "." because the build context is the content of the arti_dir directory in the sandbox
DOCKERFILE_CONTENT = """FROM nginx:1.27-alpine

# Remove default pages
RUN rm -rf /usr/share/nginx/html/*

# Copy static files to nginx default directory
# Build context is the content of the arti_dir directory in the sandbox
COPY . /var/www/html/
RUN cp -r /var/www/html/* /usr/share/nginx/html/

# Expose port 80
EXPOSE 80

# Run nginx in foreground mode
CMD ["nginx", "-g", "daemon off;"]
"""


def create_sandbox(template: str = None, timeout: int = 1800) -> Sandbox:
    """
    Create a sandbox instance
    
    Args:
        template: Template ID or template name
        timeout: Sandbox timeout (seconds), default 30 minutes
    
    Returns:
        Sandbox instance
    """
    template = template or TEMPLATE_NAME
    print(f"Creating sandbox using template '{template}'...")
    
    sandbox = Sandbox.create(template, timeout=timeout)
    print(f"Sandbox created successfully, ID: {sandbox.sandbox_id}")
    
    return sandbox


def setup_static_site(sandbox: Sandbox, app_dir: str = "/app", http_port: int = 80) -> dict:
    """
    Setup static site files in the sandbox
    
    Args:
        sandbox: Sandbox instance
        app_dir: Application directory path
        http_port: HTTP service port
    
    Returns:
        Dictionary containing sandbox information
    """
    # Create index.html file
    index_path = f"{app_dir}/index.html"
    print(f"Creating file: {index_path}")
    
    result = sandbox.files.write(index_path, INDEX_HTML_CONTENT)
    print(f"File creation result: {result}")
    
    # Get access URL
    host = sandbox.get_host(http_port)
    url = f"https://{host}"
    print(f"Static site access URL: {url}")
    
    return {
        "sandbox_id": sandbox.sandbox_id,
        "app_dir": app_dir,
        "files": [index_path],
        "dockerfile": DOCKERFILE_CONTENT.strip(),
        "host": host,
        "url": url,
        "http_port": http_port
    }


def create_test_sandbox(
    output_file: str = None,
    template: str = None,
    timeout: int = 1800,
    http_port: int = 80,
) -> dict:
    """
    Create test sandbox and setup static site
    
    Args:
        output_file: Output JSON file path
        template: Template ID or template name
        timeout: Sandbox timeout (seconds)
        http_port: HTTP service port
    
    Returns:
        Sandbox information dictionary
    """
    try:
        # Create sandbox
        sandbox = create_sandbox(template=template, timeout=timeout)
        
        # Setup static site
        result = setup_static_site(sandbox, http_port=http_port)
        result["status"] = "success"
        
        print(f"\n=== Sandbox Creation Complete ===")
        print(f"Sandbox ID: {result['sandbox_id']}")
        print(f"App Directory: {result['app_dir']}")
        print(f"Created Files: {result['files']}")
        print(f"Access URL: {result['url']}")
        print(f"\n⚠️  Note: Sandbox will not be automatically cleaned up, please run after testing:")
        print(f"   python cleanup_sandbox.py {result['sandbox_id']}")
        
        # Output to file
        if output_file:
            with open(output_file, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"\nResult saved to: {output_file}")
        
        # Output JSON to stdout (for script parsing)
        print(f"\n__SANDBOX_INFO_START__")
        print(json.dumps(result))
        print(f"__SANDBOX_INFO_END__")
        
        return result
        
    except Exception as e:
        error_result = {
            "status": "error",
            "error": str(e)
        }
        print(f"Error: {e}", file=sys.stderr)
        return error_result


def main():
    parser = argparse.ArgumentParser(
        description="Create novita test sandbox",
        epilog="Note: Sandbox will not be automatically cleaned up, please manually run cleanup_sandbox.py after testing"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output JSON file path"
    )
    parser.add_argument(
        "--template", "-t",
        default=TEMPLATE_NAME,
        help=f"Sandbox template name or ID (default: {TEMPLATE_NAME})"
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=600,
        help="Sandbox timeout (seconds, default: 600)"
    )
    parser.add_argument(
        "--port", "-p",
        type=int,
        default=80,
        help="HTTP service port (default: 80)"
    )
    
    args = parser.parse_args()
    
    result = create_test_sandbox(
        output_file=args.output,
        template=args.template,
        timeout=args.timeout,
        http_port=args.port
    )
    
    sys.exit(0 if result.get("status") == "success" else 1)


if __name__ == "__main__":
    main()
