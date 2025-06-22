#
# GAMS - General Algebraic Modeling System Python API
#
# Copyright (c) 2017-2025 GAMS Development Corp. <support@gams.com>
# Copyright (c) 2017-2025 GAMS Software GmbH <support@gams.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import importlib
import sys
import weakref
import yaml
from gams.connect.agents.connectagent import ConnectAgent
from gams.connect.connectvalidator import ConnectValidator
from gams.connect.errors import GamsConnectException
from gams.control import GamsWorkspace
from gams.transfer import Container


class ConnectDatabase(object):
    """
    A ConnectDatabase contains data in the form of a gams.transfer.Container instance.
    Running the execute() method instantiates Connect agents that read, write, or modify
    symbol data.

    Parameters
    ----------
    system_directory : str
        GAMS system directory to be used.
    container : gams.transfer.Container, optional
        A Container to be used by the ConnectDatabase, by default None. If omitted, the ConnectDatabase will instantiate a new and empty container.
    ecdb : gams.core.embedded.ECGAMSDatabase, optional
        When running in a GAMS context (e.g. embedded code), this can be used to allow connection to the embedded code GAMS database, by default None.
    """

    def __init__(self, system_directory, container=None, ecdb=None):
        self._system_directory = system_directory
        self._ecdb = ecdb
        self._schema_cache = {}
        self._ws = GamsWorkspace(system_directory=self._system_directory)
        if container is None:
            self._container = Container(system_directory=self._system_directory)
        else:
            self._container = container
        if self._ecdb:
            ecdb._cdb = self

    def __del__(self):
        pass

    def print_log(self, msg, end="\n"):
        """
        Print msg to the GAMS log if avaiable, uses print() otherwise.

        Parameters
        ----------
        msg : str
            The message to be printed.
        end : str, optional
            String to be put after the message, by default "\n".
        """
        if self._ecdb:
            self._ecdb.printLog(msg, end)
        else:
            print(msg, end=end)
            sys.stdout.flush()

    def _get_agent_class(self, agent_name):
        # Try to load the agent module from 'gams.connect.agents'
        try:
            mod = importlib.import_module("gams.connect.agents." + agent_name.lower())
            err = None
        except ModuleNotFoundError as e:
            err = e
        if err:
            try:
                if (
                    err.name != "gams.connect.agents." + agent_name.lower()
                ):  # the connect agent module itself was found but an import in the source itself did fail
                    raise GamsConnectException(str(err), traceback=True)
                mod = importlib.import_module(agent_name.lower())
                err = None
            except ModuleNotFoundError as e:
                err = e

        # Try to retrieve the agent class from the found module
        if not err:
            try:
                agent_class = vars(mod)[agent_name]
            except KeyError as e:
                err = e

        # Compile error in case of previous errors
        if err:
            msg = f"Connect agent '{agent_name}' not found. The following agents are available: {', '.join(self._get_available_agents())}."
            raise GamsConnectException(msg)

        return agent_class

    def _get_idx_str(self, agent_name, idx_list):
        idx_str = f"{agent_name}"
        if idx_list:
            idx_str += f"({idx_list[0]})"
            for i in idx_list[1:]:
                idx_str = f"PythonCode({i})" + "->" + idx_str
        return idx_str

    def _execute(self, instructions, idx_list=[]):
        if isinstance(instructions, list):
            if all(isinstance(inst, dict) for inst in instructions):
                inst_list = instructions
            else:
                raise GamsConnectException(
                    "Invalid data type for instructions argument. Needs to be 'list of dict'."
                )
        elif isinstance(instructions, dict):
            inst_list = [instructions]
        else:
            raise GamsConnectException(
                f"Invalid data type for instructions argument. Needs to be 'dict' or 'list', but was '{type(instructions).__name__}'."
            )

        agent_instances = []
        for idx, inst in enumerate(inst_list, start=1):
            root = list(inst.keys())
            if len(root) != 1:
                raise GamsConnectException(
                    f"Invalid agent definition with {len(root)} agent names instead of 1."
                )
            agent_name = root[0]
            if not isinstance(agent_name, str):
                raise GamsConnectException(
                    f"Invalid data type for agent name. Needs to be 'str', but was '{type(agent_name).__name__}'."
                )

            inst = inst[agent_name]

            agent_class = self._get_agent_class(agent_name)
            if not issubclass(agent_class, ConnectAgent):
                raise GamsConnectException(
                    f"Agent class '{agent_name}' has to be derived from gams.connect.agents.connectagent.ConnectAgent",
                    traceback=True,
                ) 

            agent_schema = self.load_schema(agent_class.__name__)
            v = ConnectValidator(agent_schema)
            if not v.validate(inst):
                raise GamsConnectException(
                    f"Validation of instructions for agent {self._get_idx_str(agent_name, [idx] + idx_list)} failed: {v.errors}"
                )
            agent_instance = agent_class(self, inst, [idx] + idx_list)
            agent_instances.append(agent_instance)

        for idx, agent in enumerate(agent_instances, start=1):
            agent.setup_log()
            try:
                execute_return = agent.execute()
            except GamsConnectException:
                raise
            except Exception as e:
                e.add_note(self._get_idx_str(agent._agent_name, agent._agent_index) + " failed")
                raise
            agent.restore_log()

            if (
                type(agent).__name__ == "PythonCode" and execute_return
            ):  # PythonCode generated instructions
                self._execute(execute_return, [idx] + idx_list)

    def execute(self, instructions):
        """
        Instantiates and executes one or multiple Connect agents.

        Parameters
        ----------
        instructions : list, dict
            The instructions to be used for instantiating and executing the agents. Use list for executnig multiple agents and dict for a single one.

        Raises
        ----------
        GamsConnectException
            If the instructions are invalid or if the specified agent could not be loaded.
        """
        self._execute(instructions)

    @property
    def container(self):
        return self._container

    @property
    def ecdb(self):
        return self._ecdb

    @property
    def system_directory(self):
        return self._system_directory

    def _get_available_agents(self):
        try:
            agents = []
            with importlib.resources.as_file(
                importlib.resources.files("gams.connect.agents") / "schema"
            ) as schema_path:
                for f in schema_path.rglob('*.yaml'):
                    if f.is_file():
                        agents.append(f.name.split(".")[0])
            return agents
        except:
            return []

    #def _get_close_agent(self, agent_name):
    #    import difflib
    #    agents = self._get_available_agents()
    #    agents = {a.lower(): a for a in agents}  # use case-insensitive comparison since otherwise "csvwriter" -> "ExcelWriter" instead of "CSVWriter
    #    m = difflib.get_close_matches(agent_name.lower(), agents.keys(), n=1, cutoff=0.7)
    #    return agents[m[0]] if m else None

    def load_schema(self, agent):
        """
        Returns the cerberus schema for a specific agent as Python data structure.

        Parameters
        ----------
        agent : str, ConnectAgent
            Either the name of the Connect agent or the ConnectAgent instance itself.

        Returns
        -------
        dict
            Python data structure to be used for validation to ensure correct format of instructions given to a Connect agent.
        """

        if isinstance(agent, str):
            agent_name = agent
        elif isinstance(agent, ConnectAgent):
            agent_name = agent.__class__.__name__
        else:
            raise GamsConnectException(
                f"Parameter 'agent' needs to be of type str or ConnectAgent, but was {type(agent)}."
            )
        with importlib.resources.as_file(
            importlib.resources.files("gams.connect.agents") / "schema"
        ) as schema_path:
            schema_file = schema_path / (agent_name + ".yaml")
            fstat = schema_file.stat()
            mtime = fstat.st_mtime
            size = fstat.st_size
            if (
                agent_name in self._schema_cache
                and mtime == self._schema_cache[agent_name]["mtime"]
                and size == self._schema_cache[agent_name]["size"]
            ):
                schema = self._schema_cache[agent_name]["schema"]
            else:
                schema = schema_file.read_text()
                schema = yaml.safe_load(schema)
                self._schema_cache[agent_name] = {"schema": schema, "mtime": mtime, "size": size}
        return schema
