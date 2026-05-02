import asyncio
import aiohttp
from rich.console import Console
from worker_automate_hub.config.settings import load_env_config
from worker_automate_hub.utils.logger import logger

console = Console()

async def send_rdp_action(uuid_robo: str, action: str):
    env_config, _ = load_env_config()
    
    body = {
        "uuidRobo": uuid_robo, 
        "action": action
    }
    
    headers_basic = {
        "Authorization": f"Basic {env_config['API_AUTHORIZATION']}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    url = f"{env_config['API_BASE_URL']}/robo/api/manage"

    try:
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=True)) as session:
            async with session.post(url, json=body, headers=headers_basic) as response:
                if response.status == 200:
                    data = await response.json()
                    logger.info(f"Ação '{action}' enviada com sucesso: {data}")
                    console.print(f"Ação '{action}' enviada com sucesso.", style="bold green")
                    return data
                else:
                    err_msg = f"Erro ao enviar ação '{action}': {response.status} - {await response.text()}"
                    logger.error(err_msg)
                    console.print(err_msg, style="bold red")
                    return {"error": err_msg}

    except Exception as e:
        err_msg = f"Erro ao comunicar com o endpoint RDP: {e}"
        logger.error(err_msg)
        console.print(err_msg, style="bold red")
        return {"error": str(e)}
