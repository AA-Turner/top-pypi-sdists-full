# @Author: Dr. Jeffrey Chijioke-Uche
# @Copyright (c) 2024-2025 Dr. Jeffrey Chijioke-Uche, All Rights Reserved.
# @Copyright by: U.S Copyright Office
# @Date: 2024-03-01
# @Last Modified by: Dr. Jeffrey Chijioke-Uche    
# @Last Modified time: 2025-06-09
# @Description: This module provides a connector to IBM Quantum devices using Qiskit Runtime Service.
# @License: Apache License 2.0 and creative commons license 4.0
# @Purpose: Software designed for Pypi package for Quantum Plan Backend Connection IBM Backend QPUs Compute Resources Information
#
# Any derivative works of this code must retain this copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals. Failure to do so will result in a breach of copyrighted software.
# All rights reserved by Dr. Jeffrey Chijioke-Uche, Author and Owner of this software Intellectual Property.
#_________________________________________________________________________________
import os
import warnings
import requests
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv, find_dotenv
from qiskit_ibm_runtime import QiskitRuntimeService, IBMBackend
from .qcon_lib import eagle, heron, flamingo, condor, qcon, eagle_processor, heron_processor, flamingo_processor, condor_processor, egret_processor, falcon_processor, hummingbird_processor, canary_processor
from .qcon_lib import j_eagle_processor, j_heron_processor, j_flamingo_processor, j_condor_processor, j_egret_processor, j_falcon_processor, j_hummingbird_processor, j_canary_processor
from IPython.display import display, Markdown
from PIL import Image
import numpy as np

# ───────────────────────────────────────────────────────────────────────────────
# Constants for output formatting
# ───────────────────────────────────────────────────────────────────────────────
HEADER_LINE = "=" * 82
SUBHEADER_LINE = "-" * 82
HEADER_1 = "\n⚛️ Quantum Plan Backend Connection IBMBackend QPUs Compute Resources Information:"
EMPTY_NOTICE = "⚛️ [QPU EMPTY RETURN NOTICE]:"

# ───────────────────────────────────────────────────────────────────────────────
# Functions to load environment variables
# ───────────────────────────────────────────────────────────────────────────────
def _load_environment():
    load_dotenv()
    path = find_dotenv(usecwd=True)
    if path:
        load_dotenv(path, override=True)
    else:
        home = Path.home() / '.env'
        if home.is_file():
            load_dotenv(home, override=True)

#################
# LOADER:::::::::
#################
_load_environment()


# ───────────────────────────────────────────────────────────────────────────────
def in_jupyter():
    try:
        from IPython import get_ipython
        shell = get_ipython().__class__.__name__
        return shell in ('ZMQInteractiveShell',)  # Jupyter notebook/lab
    except Exception:
        return False

# ───────────────────────────────────────────────────────────────────────────────
# Functions to get the plan information::
# ───────────────────────────────────────────────────────────────────────────────
def _get_plan():
    _load_environment()
    """
    Get the current plan from environment variables.
    Returns:
        tuple: A tuple containing the plan key, plan name, and human-readable tag.
    Raises:
        ValueError: If the plan is not set correctly or if the plan name is missing.
    """
    flags = {
        'open':      os.getenv('OPEN_PLAN','off').strip().lower()=='on',
        'pay-as-you-go':  os.getenv('PAYGO_PLAN','off').strip().lower()=='on',
        'flex':      os.getenv('FLEX_PLAN','off').strip().lower()=='on',
        'premium':   os.getenv('PREMIUM_PLAN','off').strip().lower()=='on',
        'dedicated': os.getenv('DEDICATED_PLAN','off').strip().lower()=='on',
    }
    if sum(flags.values())!=1:
        raise ValueError('⛔️ Exactly one of plan must be set to on - Check your variable setup file.')
    key = next(k for k,v in flags.items() if v)
    name = os.getenv(f'{key.upper()}_PLAN_NAME','').strip()
    if not name:
        raise ValueError(f'⛔️ {key.upper()}_PLAN_NAME must be set when {key.upper()}_PLAN is switched on')
    global plan_option
    
    #_____________________________________________
    # Check if the plan is open or paid
    # Determine the plan type based on the key
    #______________________________________________
    if flags['open']:
        plan_option = os.getenv('OPEN_PLAN_NAME','').strip()
        if not plan_option:
            raise ValueError('⛔️ OPEN_PLAN_NAME must be set when OPEN_PLAN is switched on')
    elif flags['pay-as-you-go']:
        plan_option = os.getenv('PAYGO_PLAN_NAME','').strip()
        if not plan_option:
            raise ValueError('⛔️ PAYGO_PLAN_NAME must be set when PAYGO_PLAN is switched on')
    elif flags['flex']:
        plan_option = os.getenv('FLEX_PLAN_NAME','').strip()
        if not plan_option:
            raise ValueError('⛔️ FLEX_PLAN_NAME must be set when FLEX_PLAN is switched on')
    elif flags['premium']:
        plan_option = os.getenv('PREMIUM_PLAN_NAME','').strip()
        if not plan_option:
            raise ValueError('⛔️ PREMIUM_PLAN_NAME must be set when PREMIUM_PLAN is switched on')
    elif flags['dedicated']:
        plan_option = os.getenv('DEDICATED_PLAN_NAME','').strip()
        if not plan_option:
            raise ValueError('⛔️ DEDICATED_PLAN_NAME must be set when DEDICATED_PLAN is switched on')
    
    #_____________________________________________
    # Check if the plan is open or paid
    # Determine the plan type based on the key
    #______________________________________________
    if key == 'open':
        tag = 'Open Plan'
    else:
        tag = 'Paid Plan'

    return key, name, tag

# ───────────────────────────────────────────────────────────────────────────────
# Functions for saving account and listing backends
# ───────────────────────────────────────────────────────────────────────────────
def _get_credentials(key):
    """
    Get the credentials for the specified plan key from environment variables.
    Args:
        key (str): The plan key (e.g., 'open', 'pay-as-you-go', 'flex', 'premium', 'dedicated').
    Returns:
        dict: A dictionary containing the credentials for the specified plan.
    """
    k = key.upper()
    return {
        'name':     os.getenv(f'{k}_PLAN_NAME','').strip(),
        'channel':  os.getenv(f'{k}_PLAN_CHANNEL','').strip(),
        'instance': os.getenv(f'{k}_PLAN_INSTANCE','').strip(),
        'token':    os.getenv('IQP_API_TOKEN','').strip()
    }

# ───────────────────────────────────────────────────────────────────────────────
# Functions to memorize account and list backends
# ───────────────────────────────────────────────────────────────────────────────
def save_account():
    """
    Intelligently Memorize Qiskit Runtime Service account for the current plan.
    """
    key,name,human = _get_plan()
    cred = _get_credentials(key)
    if not all([cred['channel'],cred['instance'],cred['token']]):
        print(f"⛔️ Missing credentials for {human}.")
        return
    try:
        QiskitRuntimeService.save_account(
            channel=cred['channel'], token=cred['token'],
            instance=cred['instance'], name=cred['name'],
            set_as_default=True, overwrite=True, verify=True
        )
        print(f"\n✅ Saved {human} account → instance {cred['instance']}\n")
    except Exception as e:
        print(f"⛔️ Failed to save account for {human}: {e}")

# ───────────────────────────────────────────────────────────────────────────────
# Function to list backends
# ───────────────────────────────────────────────────────────────────────────────
def list_backends():
    """
    Lists available QPUs for the current plan.
    """
    key,_,human = _get_plan()
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore',category=DeprecationWarning)
        service = QiskitRuntimeService()
    names = [b.name for b in service.backends()]
    print(SUBHEADER_LINE)
    print(f"⚛️ Available QPUs ({human}):")
    for n in names:
        print(f" - {n}")
    print(SUBHEADER_LINE + "\n")


# ───────────────────────────────────────────────────────────────────────────────
# QCon Intelligent Core QPU Processor Type Analysis
# ───────────────────────────────────────────────────────────────────────────────
def get_qpu_processor_type(backend_name: str) -> dict:
    """
    Connects to IBM Quantum and retrieves the processor type of a specified QPU backend.

    Args:
        backend_name (str): The name of the QPU backend (e.g., 'ibm_osaka', 'ibm_brisbane').

    Returns:
        dict: A dictionary containing the processor type information (family, revision, segment),
              or an empty dictionary if the information is not available or an error occurs.
    """
    try:
        # Initialize the service.
        processor_service = QiskitRuntimeService()

        key,name,human = _get_plan()
        with warnings.catch_warnings():
            warnings.filterwarnings('ignore',category=DeprecationWarning)
            processor_service = QiskitRuntimeService()
        print(HEADER_LINE)
        print(f"\n⚛️ Getting ({human}) Least-busy QPU Processor Info...")
        print(SUBHEADER_LINE)
        if key=='open':
            processor_backend = processor_service.least_busy(
                simulator=False,
                operational=True,
                min_num_qubits=5)
        else:
            cred = _get_credentials(key)
            processor_backend = processor_service.least_busy(
                simulator=False, 
                operational=True,
                instance=cred['instance'],
                min_num_qubits=5
            )
        if not processor_backend:
            raise RuntimeError(f"⛔️ No QPU available for {human}")
        qpus = processor_service.backends(
            simulator=False, 
            operational=True,
            min_num_qubits=5,
        )

        # Get the backend object
        print(f"\n--- 🔳  Processor Details for QConnector Least Busy Backend QPU: {processor_backend.name} ---")
        if hasattr(processor_backend, 'processor_type') and processor_backend.processor_type:
            processor_info = processor_backend.processor_type
            processor_family = processor_info.get('family', 'N/A')
            print(f"🦾 Processor Type: {processor_family}")
            processor_revision = processor_info.get('revision', 'N/A')
            print(f"🦾 Processor Revision: r{processor_revision}")
            status = processor_backend.status()

            # If qpu_status is offline as least busy backend, connect to the next least busy backend
            if not status.operational:
                processor_backend = processor_service.least_busy(
                    simulator=False,
                    operational=True,
                    min_num_qubits=5
                )
                if not processor_backend:
                    raise RuntimeError(f"⛔️ No QPU available for {human}")
                print(f"🔄 Switched to next least busy QPU: {processor_backend.name}")
            
            qpu_light = f"🟢" if status.operational else f"🔴"
            qpu_status = f"{qpu_light} Online" if status.operational else f"{qpu_light} Offline"
            print(f"🦾 Processor status: {qpu_status}")

            processor_lg = None
            # Determine the processor type and display the corresponding image
            #-----------------------------------------------------------------------
            # control logic for processor names in Jupyter Notebook:
            if in_jupyter() and processor_family == 'Eagle':
                img_path = j_eagle_processor
                processor_lg = Image.open(img_path)
                display(processor_lg)
                processor_id = f"{qpu_light} {processor_family} Quantum Processor"
                print(processor_id)
            elif in_jupyter() and processor_family == 'Heron':
                img_path = j_heron_processor
                processor_lg = Image.open(img_path)
                display(processor_lg)
                processor_id = f"{qpu_light} {processor_family} Quantum Processor"
                print(processor_id)
            elif in_jupyter() and processor_family == 'Flamingo':
                img_path = j_flamingo_processor
                processor_lg = Image.open(img_path)
                display(processor_lg)
                processor_id = f"{qpu_light} {processor_family} Quantum Processor"
                print(processor_id)
            elif in_jupyter() and processor_family == 'Condor':
                img_path = j_condor_processor
                processor_lg = Image.open(img_path)
                display(processor_lg)
                processor_id = f"{qpu_light} {processor_family} Quantum Processor"
                print(processor_id)
            elif in_jupyter() and processor_family == 'Egret':
                img_path = j_egret_processor
                processor_lg = Image.open(img_path)
                display(processor_lg)
                processor_id = f"{qpu_light} {processor_family} Quantum Processor"
                print(processor_id)
            elif in_jupyter() and processor_family == 'Falcon':
                img_path = j_falcon_processor
                processor_lg = Image.open(img_path)
                display(processor_lg)
                processor_id = f"{qpu_light} {processor_family} Quantum Processor"
                print(processor_id)
            elif in_jupyter() and processor_family == 'Hummingbird':
                img_path = j_hummingbird_processor
                processor_lg = Image.open(img_path)
                display(processor_lg)
                processor_id = f"{qpu_light} {processor_family} Quantum Processor"
                print(processor_id)
            elif in_jupyter() and processor_family == 'Canary':
                img_path = j_canary_processor
                processor_lg = Image.open(img_path)
                display(processor_lg)
                processor_id = f"{qpu_light} {processor_family} Quantum Processor"
                print(processor_id)
            # If not in Jupyter, fallback to terminal rendering:
            else:
                if processor_family == 'Eagle':
                    img_path = eagle_processor
                    img = Image.open(img_path).convert("L")
                    img.thumbnail((40, 20))  # Resize for terminal
                    chars = np.asarray(list(" .:-=+*#%@"))
                    pixels = np.asarray(img) / 255
                    ascii_img = chars[(pixels * (len(chars) - 1)).astype(int)]
                    lines = ["".join(row) for row in ascii_img]
                    processor_lg = "\n".join(lines)
                    processor_id = f"{qpu_light} {processor_family} Quantum Processor"
                    print(processor_lg)
                    print(processor_id)
                elif processor_family == 'Heron':
                    img_path = heron_processor
                    img = Image.open(img_path).convert("L")
                    img.thumbnail((40, 20))  # Resize for terminal
                    chars = np.asarray(list(" .:-=+*#%@"))
                    pixels = np.asarray(img) / 255
                    ascii_img = chars[(pixels * (len(chars) - 1)).astype(int)]
                    lines = ["".join(row) for row in ascii_img]
                    processor_lg = "\n".join(lines)
                    processor_id = f"{qpu_light} {processor_family} Quantum Processor"
                    print(processor_lg)
                    print(processor_id)
                elif processor_family == 'Flamingo':
                    img_path = flamingo_processor
                    img = Image.open(img_path).convert("L")
                    img.thumbnail((40, 20))  # Resize for terminal
                    chars = np.asarray(list(" .:-=+*#%@"))
                    pixels = np.asarray(img) / 255
                    ascii_img = chars[(pixels * (len(chars) - 1)).astype(int)]
                    lines = ["".join(row) for row in ascii_img]
                    processor_lg = "\n".join(lines)
                    processor_id = f"{qpu_light} {processor_family} Quantum Processor"
                    print(processor_lg)
                    print(processor_id)
                elif processor_family == 'Condor':
                    img_path = condor_processor
                    img = Image.open(img_path).convert("L")
                    img.thumbnail((40, 20))  # Resize for terminal
                    chars = np.asarray(list(" .:-=+*#%@"))
                    pixels = np.asarray(img) / 255
                    ascii_img = chars[(pixels * (len(chars) - 1)).astype(int)]
                    lines = ["".join(row) for row in ascii_img]
                    processor_lg = "\n".join(lines)
                    processor_id = f"{qpu_light} {processor_family} Quantum Processor"
                    print(processor_lg)
                    print(processor_id)
                elif processor_family == 'Egret':
                    img_path = egret_processor
                    img = Image.open(img_path).convert("L")
                    img.thumbnail((40, 20))  # Resize for terminal
                    chars = np.asarray(list(" .:-=+*#%@"))
                    pixels = np.asarray(img) / 255
                    ascii_img = chars[(pixels * (len(chars) - 1)).astype(int)]
                    lines = ["".join(row) for row in ascii_img]
                    processor_lg = "\n".join(lines)
                    processor_id = f"{qpu_light} {processor_family} Quantum Processor"
                    print(processor_lg)
                    print(processor_id)
                elif processor_family == 'Falcon':
                    img_path = falcon_processor
                    img = Image.open(img_path).convert("L")
                    img.thumbnail((40, 20))  # Resize for terminal
                    chars = np.asarray(list(" .:-=+*#%@"))
                    pixels = np.asarray(img) / 255
                    ascii_img = chars[(pixels * (len(chars) - 1)).astype(int)]
                    lines = ["".join(row) for row in ascii_img]
                    processor_lg = "\n".join(lines)
                    processor_id = f"{qpu_light} {processor_family} Quantum Processor"
                    print(processor_lg)
                    print(processor_id)
                elif processor_family == 'Hummingbird':
                    img_path = hummingbird_processor
                    img = Image.open(img_path).convert("L")
                    img.thumbnail((40, 20))  # Resize for terminal
                    chars = np.asarray(list(" .:-=+*#%@"))
                    pixels = np.asarray(img) / 255
                    ascii_img = chars[(pixels * (len(chars) - 1)).astype(int)]
                    lines = ["".join(row) for row in ascii_img]
                    processor_lg = "\n".join(lines)
                    processor_id = f"{qpu_light} {processor_family} Quantum Processor"
                    print(processor_lg)
                    print(processor_id)
                elif processor_family == 'Canary':
                    img_path = canary_processor
                    img = Image.open(img_path).convert("L")
                    img.thumbnail((40, 20))  # Resize for terminal
                    chars = np.asarray(list(" .:-=+*#%@"))
                    pixels = np.asarray(img) / 255
                    ascii_img = chars[(pixels * (len(chars) - 1)).astype(int)]
                    lines = ["".join(row) for row in ascii_img]
                    processor_lg = "\n".join(lines)
                    processor_id = f"{qpu_light} {processor_family} Quantum Processor"
                    print(processor_lg)
                    print(processor_id)
                if processor_lg is None:
                    processor_lg = "⚠️ Processor type image not available for this family."
            return processor_info
        #------------------------------------------------------------------------------------
        else:
            print(f"Processor type information not available for {processor_backend.name}.")
            return {}

    except Exception as e:
        print(f"Error getting backend processor type for {backend_name}: {e}")
        return {}



# ───────────────────────────────────────────────────────────────────────────────
# Class to connect to Qiskit Runtime Service
# ───────────────────────────────────────────────────────────────────────────────
class QConnectorV2:
    _load_environment()
    """
    QConnectorV2 is a class that connects to the IBM Quantum Qiskit Runtime Service
    and retrieves the least busy QPU backend based on the user's plan.
    It provides information about the backend, including its name, version, and operational status.

    Usage:
    >>> from qiskit_connector import QConnectorV2
    >>> backend = QConnectorV2() as connector:
    >>> print(backend.name)  # Prints the name of the least busy QPU backend
    >>> print(backend.version)  # Prints the version of the backend
    >>> print(backend.num_qubits)  # Prints the number of qubits in the backend
    >>> print(backend.operational)  # Prints whether the backend is operational or not
    >>> print(backend.processor_type)  # Prints the processor type information of the backend
    >>> processor_info = get_qpu_processor_type(backend.name)  # Retrieves processor type
    >>> print(processor_info)  # Prints the processor type information 
    >>> For Open Plan:
            >>> sampler = Sampler(mode=backend)            # Open Plan does not support session
    >>> For Paid Plan:   
            >>> with Session(backend=backend) as session:   # Paid Plan supports session
                    sampler = Sampler(session=session)
                    estimator = Estimator(session=session)         
    """
    def __new__(cls):
        key,name,human = _get_plan()
        with warnings.catch_warnings():
            warnings.filterwarnings('ignore',category=DeprecationWarning)
            service = QiskitRuntimeService()
        print(HEADER_LINE)
        qconnector_icon = qcon
        print(f"{qconnector_icon}")
        print(f"\n⚛️ Connecting ({human}) to least-busy QPU...")
        print(SUBHEADER_LINE)
        if key=='open':
            backend = service.least_busy(
                simulator=False,
                operational=True,
                min_num_qubits=5)
        else:
            cred = _get_credentials(key)
            backend = service.least_busy(
                simulator=False, 
                operational=True,
                instance=cred['instance'],
                min_num_qubits=5
            )
        if not backend:
            raise RuntimeError(f"⛔️ No QPU available for {human}")
        qpus = service.backends(
            simulator=False, 
            operational=True,
            min_num_qubits=5,
        )
        
        for qpu in qpus:
            status = qpu.status()
            qpu_light = f"🟢" if status.operational else f"🔴"
            qpu_status = f"{qpu_light} Online" if status.operational else f"{qpu_light} Offline"

        print(f"⚛️ Connected [{human}] → Realtime Least Busy QPU:: [{backend.name}]")
        for q in qpus:
            print(f"- {q.name}")
        print("")
        least_busy_qpu_now = f"[{backend.name}]"
        print(f"🖥️ Least Busy QPU Now: {least_busy_qpu_now}")
        print(f"🖥️ Version: {getattr(backend,'version','N/A')}")
        print(f"🖥️ Qubits Count: {getattr(backend,'num_qubits','N/A')}")
        print(f"🖥️ Backend [{backend.name}] ready for use: ✔️ Yes")
        print(f"🖥️ Operational: {getattr(backend,'operational', plan_option.capitalize()+' Plan')}")
        qpu_names = [{least_busy_qpu_now}]
        for name in qpu_names:
            processor_details = get_qpu_processor_type(name)
        print(HEADER_LINE + "\n")
        print("🖥️ Your Plan:", human)
        print("🖥️ Least Busy QPU:", backend.name)
        print("🖥️ Backend Status:", qpu_status)
        return backend

# ───────────────────────────────────────────────────────────────────────────────
# Class to get the Qiskit Runtime Service plan
# ───────────────────────────────────────────────────────────────────────────────
class QPlanV2:
    """ QPlanV2 is a class that retrieves the current plan information
    from environment variables and provides a human-readable tag for the plan.                                                              
    It is used to determine the type of plan the user is subscribed to, such as Open Plan, Pay-as-you-go Plan, Flex Plan, Premium Plan, or Dedicated Plan.          

    Usage:
    >>> from qiskit_connector import QPlanV2 as plan
    >>> current = plan()  # Retrieves the current plan information
    >>> print(current)    # Prints the human-readable plan (Openn Plan or Paid Plan)
    """
    def __new__(cls):
        _,_,human = _get_plan()
        return human

# ───────────────────────────────────────────────────────────────────────────────
# Footer function to display copyright information
# ───────────────────────────────────────────────────────────────────────────────
def footer():
    year = datetime.today().year
    print(HEADER_LINE)
    print(f"Software Design by: Dr. Jeffrey Chijioke-Uche , IBM Quantum Ambassador ©{year}\n")
    print("⚛️ Copyright (c) 2025 Dr. Jeffrey Chijioke-Uche, All Rights Reserved.")
    print("⚛️ Copyrighted by: U.S Copyright Office")
    print("⚛️ Licensed under Apache License 2.0 and creative commons license 4.0")
    print("⚛️ Ownership & All Rights Reserved.\n")

# ───────────────────────────────────────────────────────────────────────────────
# QCon Intelligent Core Module
# ───────────────────────────────────────────────────────────────────────────────
class QConIntelligentCore:
    def __init__(self):
        self.status = {}

    def QConnectorIntelli(self):
        if 'QConnectorV2' in globals():
            print("✅ QConnectorV2 class is active")
            self.status["QConnectorV2 class"] = "Checked"
        else:
            print("❌ QConnectorV2 class is missing & required")
            self.status["QConnectorV2 class"] = "Missing"

    def QPlanIntelli(self):
        if 'QPlanV2' in globals():
            print("✅ QPlanV2 class is active")
            self.status["QPlanV2 class"] = "Checked"
        else:
            print("❌ QPlanV2 class is missing & required")
            self.status["QPlanV2 class"] = "Missing"

    def QFooterIntelli(self):
        if 'footer' in globals() and callable(globals()['footer']):
            print("✅ footer() function is active")
            self.status["footer() function"] = "Checked"
        else:
            print("❌ footer() function is missing & required")
            self.status["footer() function"] = "Missing"

    def QBackendIntelli(self):
        if 'list_backends' in globals() and callable(globals()['list_backends']):
            print("✅ list_backends() function is active")
            self.status["list_backends() function"] = "Checked"
        else:
            print("❌ list_backends() function is missing & required")
            self.status["list_backends() function"] = "Missing"

    def QSaveAccountIntelli(self):
        if 'save_account' in globals() and callable(globals()['save_account']):
            print("✅ save_account() function is active")
            self.status["save_account() function"] = "Checked"
        else:
            print("❌ save_account() function is missing & required")
            self.status["save_account() function"] = "Missing"

    def QGetCredentialsIntelli(self):
        if '_get_credentials' in globals() and callable(globals()['_get_credentials']):
            print("✅ _get_credentials() function is active")
            self.status["_get_credentials() function"] = "Checked"
        else:
            print("❌ _get_credentials() function is missing & required")
            self.status["_get_credentials() function"] = "Missing"

    def QSummary(self):
        print("\n📊 Summary Report:")
        print(f"{'Component':<35}Status")
        print("-" * 50)
        for key, value in self.status.items():
            print(f"{key:<35}{value}")
        print("-" * 50)
        print("✅ Intelligence scan complete.")