# ----------------------------------------------------------------------
# Copyright (C) 2024, mellerikat. LGE
# ----------------------------------------------------------------------

"""
ALO
"""

import os
import json
import redis
import uuid
import shutil
import pickle
import tarfile
import re
import yaml
# import pkg_resources  # todo deprecated. should be fixed.
import importlib.metadata
import zipfile
import psutil
import glob
import pyfiglet
import hashlib
import inspect
from abc import ABCMeta, abstractmethod
from enum import Enum
from copy import deepcopy
from datetime import datetime
from collections import OrderedDict
from pathlib import Path
from functools import wraps
from threading import Thread
from pytz import timezone
import subprocess
from alm.model import settings
from alm.exceptions import AloError, AloErrors
from alm.logger import LOG_PROCESS_FILE_NAME, create_pipline_handler, log_start_finish
from alm.model import load_model, SolutionMetadata, update_storage_credential, EXP_FILE_NAME, copytree
from alm.utils import ResourceProfile, ColorMessage, print_table
from alm.__version__ import __version__, COPYRIGHT


logger = settings.logger
TRAIN = 'train'
INFERENCE = 'inference'
MODES = [TRAIN, INFERENCE]
LOG_PIPELINE_FILE_NAME = "pipeline.log"
ARTIFACT = 'artifact'
HISTORY_FOLDER_FORMAT = "%Y%m%dT%H%M%S.%f"
HISTORY_PATTERN = re.compile(r'([0-9]{4}[0-9]{2}[0-9]{2}T[0-9]{2}[0-9]{2}[0-9]{2}.[0-9]{6})($|-error$)')
RUN_PIPELINE_NAME = '__pipeline_names__'
RESULT_INFO_FILE = 'result_info.json'

def add_logger_handler(func):
    """ 데코레이터 함수

    특정 함수의 로그를 별로도 분리하기 위해 default logger에
    파일 핸들러를 추가 후 자동 제거 합니다.

    Args:
        func    (function): original function

    Returns:
        wrapper (function): wrapped function

    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        _handler = create_pipline_handler(os.path.join(".workspace/log", LOG_PIPELINE_FILE_NAME), logger.level)
        _logger = logger
        _logger.addHandler(_handler)
        try:
            result = func(self, *args, **kwargs)
            return result
        except Exception as e:
            _logger.exception(e)
            raise e
        finally:
            _logger.removeHandler(_handler)
            _handler.close()
    return wrapper


RESOURCE_MESSAGE_FORMAT = "".join(["\033[93m",
                                   "\n------------------------------------ %s < CPU/MEMORY/SUMMARY> Info ------------------------------------",
                                   "\n%s",
                                   "\n%s",
                                   "\n%s",
                                   "\033[0m"])


def profile_resource(func):
    """ cpu/memory profiling decorator

    Args:
        func    (function): original function

    Returns:
        wrapper (function): wrapped function

    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not settings.experimental_plan.control.check_resource:
            return func(*args, **kwargs)
        pid = os.getpid()
        ppid = psutil.Process(pid)
        cpu_usage_start = ppid.cpu_percent(interval=None)  # 단순 cpu 사용률
        mem_usage = ResourceProfile(ppid, cpu_usage_start)
        thread = Thread(target=mem_usage.run, daemon=True)
        thread.start()
        result = func(*args, **kwargs)
        mem_usage.enable = False
        cpu, mem = mem_usage.info()
        msg_cpu = "- CPU (min/max/avg) : {:5.1f}% / {:5.1f}% / {:5.1f}%".format(*cpu)
        msg_mem = "- MEM (min/max/avg) : {} / {} / {}".format(*mem)
        pipes = []
        context = args[1]
        stage_name = args[2]
        for pipe_name in context[stage_name][RUN_PIPELINE_NAME]:
            pipes.append(f"{stage_name} - {pipe_name:<15} : "
                         f"Elapsed time ({(context[stage_name][pipe_name]['finishAt'] - context[stage_name][pipe_name]['startAt']).total_seconds():8.3f}) "
                         f"[{context[stage_name][pipe_name]['finishAt'].strftime('%Y-%m-%d %H:%M:%S.%f')}"
                         f" - {context[stage_name][pipe_name]['startAt'].strftime('%Y-%m-%d %H:%M:%S.%f')}]")
        logger.debug(RESOURCE_MESSAGE_FORMAT, stage_name, msg_cpu, msg_mem, "\n".join(pipes))
        return result

    return wrapper

def print_copyright():
    ColorMessage.bold_cyan(f"""{"=" * 80}\n{pyfiglet.figlet_format(" Let's ALO-LLM  -  ! !", font="slant")}\n{"=" * 80}""")
    ColorMessage.bold(COPYRIGHT)

class RestApi(metaclass=ABCMeta):
    def __init__(self):
        self.experimental_plan = None
        self.solution_metadata = None
        print_copyright()
        self.reload()

    def init(self):
        settings.update()
        self.experimental_plan = settings.experimental_plan
        self.solution_metadata = settings.solution_metadata
        if not self.experimental_plan:
            raise AloErrors['ALO-INI-000']('config.yaml information is missing.')

    def install(self):
        source_path = self.checkout_git()
        #self.install_pip(source_path)
        self.install_with_uv(source_path)
        self.load_module()

    def reload(self):
        """ 환경 설정 정보 및 library 재설정
        """
        self.init()
        self.install()
        self.show_version()

    def run(self):
        try:
            self.solve()
        except Exception as e:
            error = e if isinstance(e, AloError) else AloError(str(e))
            logger.exception(error)
            raise error

    def show_version(self):
        logger.info("\033[96m\n=========================================== Info ==========================================="
                    f"\n- Time (UTC)        : {datetime.now(timezone('UTC')).strftime('%Y-%m-%d %H:%M:%S')}"
                    f"\n- Alo               : {__version__}"
                    f"\n- Solution Name     : {self.experimental_plan.name}"
                    f"\n- Solution Version  : {self.experimental_plan.version}"
                    f"\n- Solution Plan     : {self.experimental_plan.uri}"
                    f"\n- Solution Meta     : {self.solution_metadata.uri if self.solution_metadata else ''}"
                    f"\n- Home Directory    : {settings.home}"
                    "\n============================================================================================\033[0m")

    def load_module(self):
        if self.experimental_plan.setting:
            self.experimental_plan.setting.update_pipeline()

    def install_with_uv(self, source_path: str):
        import subprocess
        """
        Installs dependencies using uv into a .venv in the ALO home directory.
        """
        try:
            if self.experimental_plan.setting is None or not self.experimental_plan.setting.pip:
                logger.info("[UV] Skip uv install: solution.pip is not configured.")
                return

            if source_path is None:
                source_path = os.path.dirname(self.experimental_plan.uri)

            venv_path = os.path.join(settings.home, ".venv")
            logger.info(f"[UV] Ensuring virtual environment exists at {venv_path}")

            # Create the virtual environment if it doesn't exist
            # You will need to run this command manually via the terminal or integrate it differently
            # The following line is for demonstration/logging the command, not direct execution:
            # print(f"Command to create venv: uv venv {venv_path}")

            install_args = []
            pip_requirements = self.experimental_plan.setting.pip.requirements

            if pip_requirements is True:
                # Install requirements.txt from the source path
                req_file = os.path.join(source_path, 'requirements.txt')
                if not os.path.exists(req_file):
                    raise AloErrors["ALM-INI-003"](req_file, doc={"message": req_file})
                install_args.append(f"-r {req_file}")
            elif isinstance(pip_requirements, list):
                # Install packages or requirement files from the list
                for req in pip_requirements:
                    if isinstance(req, str) and req.endswith('.txt'):
                        # Resolve path for requirement files relative to the plan file directory if needed
                        req_file_path = req
                        # Assuming requirements listed in plan relative to plan file location
                        if not os.path.isabs(req_file_path):
                            plan_dir = os.path.dirname(self.experimental_plan.uri)
                            req_file_path = os.path.join(plan_dir, req)

                        if not os.path.exists(req_file_path):
                            raise AloErrors["ALM-INI-003"](req_file_path, doc = {"message": req_file})
                        install_args.append(f"-r {req_file_path}")
                    elif isinstance(req, str):
                        # Assume it's a package name or path
                        install_args.append(req)
                    else:
                        logger.warning(f"[UV] Skipping invalid requirement item: {req} (type: {type(req).__name__})")

            if not install_args:
                logger.debug("[UV] No packages or requirements to install.")
                return

            env = None
            # Construct the uv pip install command targeting the created venv
            # Use --verbose for more detailed output during installation
            print("--------------------------------")
            env = os.getenv("KUBERNETES_SERVICE_HOST")
            if env == None:
                print("Run into Local enviorment")
            else:
                print("Run into Cloud EKS enviorment")
            print("--------------------------------")

            if env:
                command = f"uv pip install --verbose --system {' '.join(install_args)}"
            else:
                command = f"uv pip install --verbose {' '.join(install_args)}"
            logger.info(f"[UV] Running install command: {command}")
            try:
                result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
                logger.info("[UV] Installation command output:\n%s", result.stdout)
                if result.stderr:
                    logger.warning("[UV] Installation command stderr:\n%s", result.stderr)
            except subprocess.CalledProcessError as e:
                logger.error("[UV] Installation command failed with error code %d:\n%s", e.returncode, e.stderr)
                raise AloErrors['ALO-INI-002'](f"UV installation command failed: {e.stderr.strip()}") from e
            except FileNotFoundError:
                 logger.error("[UV] 'uv' command not found. Please ensure uv is installed and in your PATH.")
                 raise AloErrors['ALO-INI-002']("'uv' command not found. Please ensure uv is installed and in your PATH.") from None
            except Exception as e:
                logger.exception("[UV] Unexpected error during subprocess execution.")
                raise AloErrors['ALO-INI-002'](f"Unexpected error during uv installation subprocess: {str(e)}") from e


        except Exception as e:
            logger.exception("[UV] Error during uv installation.")
            # Use ALO-INI-002 for initialization errors, including dependency installation
            raise AloErrors['ALO-INI-002'](f"UV installation failed: {str(e)}") from e


    def install_pip(self, source_path: str):
        try:
            if self.experimental_plan.setting is None or not self.experimental_plan.setting.pip:
                return
            if source_path is None:
                source_path = os.path.dirname(self.experimental_plan.uri)
            req_file = os.path.join(source_path, 'requirements.txt')
            if self.experimental_plan.setting.pip.requirements is True and not os.path.exists(req_file):
                raise AloErrors["ALM-INI-003"](req_file, doc = {"message": req_file})

            install_packages = []
            if self.experimental_plan.setting.pip.requirements is True:
                install_packages.append(f"-r {req_file}")
            elif isinstance(self.experimental_plan.setting.pip.requirements, list):
                for req in self.experimental_plan.setting.pip.requirements:
                    if req.endswith('.txt'):
                        req_file = os.path.join(os.path.dirname(self.experimental_plan.uri), req)
                        if not os.path.exists(req_file):
                            raise AloErrors["ALM-INI-003"](req_file, doc = {"message": req_file})
                        req = f"-r {req_file}"
                    install_packages.append(req)
            else:
                logger.debug("[PIP] Skip pip install")
                return

            installed_packages = []
            self.experimental_plan.setting.pip.convert_req_to_list(self.experimental_plan.setting.pip.requirements)
            for package in install_packages:
                try:
                    exists_package = importlib.metadata.version(package)
                    installed_packages.append(package)
                    logger.debug("[PIP] %s already installed: %s", package, exists_package)
                except Exception:
                    logger.debug("[PIP] Start installing package - %s", package)
                    self.experimental_plan.setting.pip.install(package)
                    installed_packages.append(package)
        except Exception as e:
            raise AloErrors['ALO-PIP-014'](str(e), doc = {"message": e }) from e #(str(e)) from e

    def checkout_git(self):
        try:
            if self.experimental_plan.setting is None or self.experimental_plan.setting.git is None:
                logger.info('[GIT] "git" property is not set.')
                return
            name = self.experimental_plan.setting.git.url.path.split('/')[-1].split('.')[0]
            path = f"{settings.workspace}/{name}"
            self.experimental_plan.setting.git.checkout(path)
            logger.debug("[GIT] checkout : %s -> %s", self.experimental_plan.setting.git.url, path)
            return path
        except Exception as e:
            raise AloErrors["ALO-PIP-001"](str(e)) from e

    def run(self):
        from alm.rest_api import run

        llo_api = self.experimental_plan.service_api
        llo_component = self.experimental_plan.components
        run(llo_api, llo_component)


alo_mode = {
    'api': RestApi
}


def Alo():
    """ 실행 옵션에 따른 실행 방식 선택

    Returns: alo 객체

    """
    return alo_mode.get(settings.computing)()