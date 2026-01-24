import socket
import random
from contextlib import closing
import uvicorn
from alm.model import settings
import os
from alm.logger import logging_config, get_logger

# #### 밖에서 정의하면 됨 ####
# app = FastAPI()
# #app.state.api = api
# # CORS 설정
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# update_api = UpdateAPI()
# app.include_router(update_api.get_router())


config = 'llo test'
class PortManager:
    def __init__(self, preferred_ports, min_port=8000, max_port=9000):
        self.preferred_ports = preferred_ports
        self.min_port = min_port
        self.max_port = max_port

    def is_port_available(self, port):
        """특정 포트의 사용 가능 여부 확인"""
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            try:
                sock.bind(('', port))
                return True
            except OSError:
                return False

    def get_available_port(self):
        """사용 가능한 포트 반환"""
        # 선호하는 포트 시도
        for port in self.preferred_ports:
            if self.is_port_available(port):
                return port

        # 랜덤 포트 시도
        used_ports = set()
        while len(used_ports) < (self.max_port - self.min_port):
            port = random.randint(self.min_port, self.max_port)
            if port in used_ports:
                continue

            used_ports.add(port)
            if self.is_port_available(port):
                return port

        raise RuntimeError("No available ports found in the specified range")

def dict_merge(source, target):
    for k, v in target.items():
        if (k in source and isinstance(source[k], dict) and isinstance(target[k], dict)):
            dict_merge(source[k], target[k])
        else:
            source[k] = target[k]

def modify_log_config(config, name: str = ""):
    # Ensure the directory exists
    log_dir = os.path.dirname(config['handlers']['file']['filename'])
    if not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)  # Create the directory if it doesn't exist

    config['formatters']['logger_generated_message']['format'] = '[%(asctime)s|FASTAPI|%(name)s|%(levelname)s|%(filename)s(%(lineno)d)|%(funcName)s] - %(message)s'
    #config['formatters'] = "[%(asctime)s|ai-conductor|%(levelname)s|%(filename)s(%(lineno)s)|%(name)s.%(funcName)s()] %(message)s"
    # config["formatters"]["access"]["fmt"] = "%(asctime)s - %(levelname)s -! %(message)s"
    # config["formatters"]["default"]["fmt"] = "%(asctime)s - %(levelname)s -! %(message)s"
    return config

def run(api, components):

    import os
    from dotenv import dotenv_values
    
    # .env 파일 경로
    env_file_path = '.env'

    # .env 파일 읽기
    env_vars = dotenv_values(env_file_path)

    # 환경 변수 삭제 함수
    def delete_env_vars(keys):
        for key in keys:
            if key in os.environ:
                del os.environ[key]
                #print(f"환경 변수 '{key}'를 삭제했습니다.")

    # .env 파일에서 읽어온 key 값들로 환경 변수 삭제
    keys_to_delete = env_vars.keys()

    delete_env_vars(keys_to_delete)

    components_yaml = components

    port_manager = PortManager(preferred_ports=[components_yaml.local_host.port])

    modified_config = modify_log_config(logging_config)
    if components_yaml.workers == "Default" :
        cpu_count = os.cpu_count()
        workers = int(cpu_count * 2)
    elif type(components_yaml.workers) is int :
        workers = components_yaml.workers
    else :
        raise ValueError(f"You specified workers in config.yaml {components_yaml.workers} which is not 'Default' or a number")

    try:
        port = port_manager.get_available_port()
        settings.logger.info(f"Server starting on port: {port}")
        uvicorn.run("alm.app:app", host=api.host, port=port , log_config = modified_config, workers=workers)
    except Exception as e:
        settings.logger.error(f"Failed to start server: {e}")
        raise