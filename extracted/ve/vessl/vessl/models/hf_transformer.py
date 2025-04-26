import os
import subprocess
import platform
import time
from importlib.metadata import version

from vessl import vessl_api
from vessl.organization import _get_organization_name
from vessl.util.service_pattern import get_hftransformers_pattern
from vessl.model import (
    create_model_repository,
    read_model_repository,
    upload_model_volume_file,
)
from vessl.models import VesslModel

class ModelForServiceHFTransformer(VesslModel):
    @classmethod
    def init(self, model_name_or_path: str = None, repository_name: str = None):
        assert model_name_or_path != None
        assert repository_name != None
        self.model_name_or_path = model_name_or_path
        self.repository_name = repository_name
        self.model_type = "hf-transformers"

        timestamp = time.time()
        lt = time.localtime(timestamp)
        current_time = time.strftime("%Y%m%d-%H%M%S",lt)
        self.base_path = os.path.join(os.getcwd(), f"vessl_model_{self.model_name_or_path}_{current_time}")
        if not os.path.exists(self.base_path):
            os.makedirs(name = self.base_path)

        entrypoint = "vessl model launch service.py:HfTransformerRunner -p 3000"
        
        python_version = platform.python_version()

        cuda_version = subprocess.Popen("nvidia-smi -q -x 2>/dev/null | grep cuda_version | awk -F'[><]' '{print $3}'", shell=True, stdout=subprocess.PIPE, encoding='utf8').stdout.read().strip()
        if cuda_version == "":
            print("nvidia-smi command not found: cuda_version will be set into None")
            cuda_version = None
        
        try:
            torch_version = version("torch")
        except:
            torch_version = None
        try:
            tensorflow_version = version("tensorflow")
        except:
            tensorflow_version = None

        # torch version has a higher priority
        framework_type = None
        if tensorflow_version != None:
            framework_type = "tensorflow"
        if torch_version != None:
            framework_type = "torch"

        requirements_path = os.path.join(self.base_path, "requirements.txt")
        if not os.path.exists(requirements_path):
            requirements_path = None
        
        pyproject_path = os.path.join(self.base_path, "pyproject.toml")
        if not os.path.exists(pyproject_path):
            pyproject_path = None

        if requirements_path == None and pyproject_path == None:
            default_hf_transformers_requirements = ["transformers"]
            requirements_path = os.path.join(self.base_path, "requirements.txt")
            with open(requirements_path, "w") as f:
                for r in default_hf_transformers_requirements:
                    f.write(f"{r}\n")

        model_number = "supplied_when_registering"
        vessl_model = self.create(
            type=self.model_type,
            repository_name=self.repository_name,
            model_number=model_number,
            entrypoint=entrypoint,
            python_version=python_version,
            weight_name_or_path=self.model_name_or_path,
            requirements_path=requirements_path,
            pyproject_path=pyproject_path,
            cuda_version=cuda_version,
            framework_type=framework_type,
            pytorch_version=torch_version,
            tensorflow_version=tensorflow_version,
            autocreate_repository=True,
        )        

        self.create_ignore_file(dest_dir=self.base_path)
        print("Generated ignore file.")
        vessl_model.save_lockfile(dest_dir=self.base_path)
        print("Saved lockfile.")

        # generate service.py
        # it will automatically get model and tokenizer from config json in future
        service_py = get_hftransformers_pattern()
        service_py = service_py.format(model_type="AutoModelForCausalLM", tokenizer_type="AutoTokenizer", model_name_or_path=f'"{self.model_name_or_path}"')    

        service_dest_path = os.path.join(self.base_path, "service.py")

        if not os.path.exists(service_dest_path):
            with open(service_dest_path, "w") as f:
                f.write(service_py)

        return vessl_model

    def register_model(self, **kwargs):
        if self.model_number == "supplied_when_registering":
            print("Creating a new model.")
            created_model = vessl_api.model_create_api(
                organization_name=_get_organization_name(**kwargs),
                repository_name=self.repository_name,
            )
            model_number = created_model.number
            print(f"Created a new model with number {model_number}.")

        self.model_number = model_number
        self.save_lockfile(self.base_path)
        print("Lockfile saved.")

        try:
            repo = read_model_repository(repository_name=self.repository_name)
        except Exception as e:
            repo = None
        if repo is None:
            create_model_repository(self.repository_name)

        src_path = self.base_path
        print(f"{self.repository_name}-{model_number} {src_path} /")
        upload_model_volume_file(
            repository_name=self.repository_name,
            model_number=model_number,
            source_path=src_path,
            dest_path="/",
        )
        print(f"Registered {self.repository_name}-{model_number}.")
