import requests
import os
import json
from dotenv import load_dotenv

# 通常在 GitHub Actions 中不需要 load_dotenv()，因为 Secrets 和 Variables 是通过其他方式注入的。
# 但如果你的脚本也可能在本地运行并依赖 .env 文件，可以保留它。
# 如果 REPOSITORY 是 GitHub Actions 的环境变量，可以通过 os.getenv('GITHUB_REPOSITORY') 获取，例如 'owner/repo'
# load_dotenv()

def set_github_action_env_var(name, value):
    """Helper function to set environment variables for GitHub Actions."""
    github_env_file = os.getenv('GITHUB_ENV')
    if github_env_file:
        # Ensure the value is a string. If it's a complex type (like dict/list),
        # it should be stringified (e.g., JSON stringified) before calling this function.
        if not isinstance(value, str):
            print(f"⚠️ Value for {name} is not a string. Attempting to convert. Original type: {type(value)}")
            try:
                value = str(value) # Basic string conversion
            except Exception as e:
                print(f"🔴 Error converting value for {name} to string: {e}. Skipping setting this env var for GitHub Actions.")
                return False

        # For multiline strings, we need to use a delimiter to ensure the whole string is captured.
        # See: https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions#setting-an-environment-variable
        if '\n' in value or '\r' in value:
            delimiter = f"EOF_{name}" # Unique delimiter
            command = f"{name}<<{delimiter}\n{value}\n{delimiter}\n"
        else:
            command = f"{name}={value}\n"

        try:
            with open(github_env_file, "a", encoding='utf-8') as f:
                f.write(command)
            print(f"✅ GitHub Actions environment variable '{name}' was set.")
            return True
        except Exception as e:
            print(f"🔴 Failed to write to GITHUB_ENV file: {e}")
            return False
    else:
        # GITHUB_ENV is not set, likely running locally.
        # For local testing, we can fall back to os.environ
        print(f"ℹ️ GITHUB_ENV not found. Setting '{name}' using os.environ for local context.")
        os.environ[name] = value
        print(f"✅ Local environment variable '{name}' has been set using os.environ.")
        return True # Still consider it a success in local context

def main():
    api_endpoint = "https://api.notionhub.app/get-data"

    # 如果 REPOSITORY 是 GitHub Actions 提供的环境变量，可以这样获取:
    repo_name = os.getenv('GITHUB_REPOSITORY') # e.g., "owner/repo"
    body = {'url': f"https://github.com/{repo_name}"}
    # 目前还是使用你提供的固定 URL

    try:
        response = requests.post(api_endpoint, json=body, timeout=30)
        print(f"📄 API Response Status Code: {response.status_code}")
        print(f"📄 API Response Text: {response.text[:500]}...") # Print first 500 chars for brevity

        response.raise_for_status() # 如果状态码不是 2xx，则会抛出 HTTPError
        api_data = response.json()

        if api_data.get('success') and 'data' in api_data:
            retrieved_data = api_data['data']
            notion_data = retrieved_data.get('notion')
            weread_data = retrieved_data.get('weread')
            code = retrieved_data.get('activationCode')

            if notion_data:
                notion_json_str = json.dumps(notion_data, ensure_ascii=False)
                set_github_action_env_var('NOTION', notion_json_str)
            else:
                print("⚠️ 在 API 响应中未找到 Notion 数据或数据为 null。")
                # 根据需要，您可以选择设置为空字符串或不设置
                # set_github_action_env_var('NOTION', '')

            if weread_data:
                weread_json_str = json.dumps(weread_data, ensure_ascii=False)
                set_github_action_env_var('WEREAD', weread_json_str)
            else:
                print("⚠️ 在 API 响应中未找到 Weread 数据或数据为 null。")

            if code: # code 应该已经是字符串了
                set_github_action_env_var('CODE', str(code)) # Ensure it's a string
            else:
                print("⚠️ 在 API 响应中未找到 CODE 数据或数据为 null。")

        else:
            print(f"🔴 API 调用未成功或响应中缺少 'data' 字段。Success: {api_data.get('success')}")

    except requests.exceptions.HTTPError as http_err:
        print(f"🔴 HTTP 错误: {http_err}")
        print(f"📄 响应内容: {response.text}")
    except requests.exceptions.RequestException as req_err:
        print(f"🔴 请求错误: {req_err}")
    except json.JSONDecodeError as json_err:
        print(f"🔴 JSON 解析错误: {json_err}")
        print(f"📄 无法解析的响应内容: {response.text}")
    except Exception as e:
        print(f"🔴 发生未知错误: {e}")

# --- 主程序入口 ---
if __name__ == "__main__":
    main()