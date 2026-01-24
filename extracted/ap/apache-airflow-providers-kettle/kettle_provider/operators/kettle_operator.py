from __future__ import annotations

import os
import shutil

from airflow.compat.functools import cached_property
from airflow.exceptions import AirflowException
from airflow.hooks.subprocess import SubprocessHook
from airflow.models.baseoperator import BaseOperator
from airflow.utils.context import Context


class KettleRunJobOperator(BaseOperator):
    r"""
    Run a Kettle Job. PDI = Pentaho Data Integration

    :param pdipath: PDI HOME env var, or installation location,
        should point directly to the directory where kitchen.sh resides.
        Defaults to /opt/pentaho/data-integration/
    :param filepath: PDI jobs directory. Defaults to /opt/pentaho/data-integration/jobs/
    :param file: If None(default) throws an error, as this is required to run a PDI job.
        Should be a job filename ending with `.kjb`.
    :param logfile: PDI logfile for this particular run. Appends to the file if file 
        already exists. Defaults ot /opt/pentaho/data-integration/logs/pdi.kitchen.log
    :param maxloglines: Maximum log lines in logfile. Defaults to 0 (no limit)
    :param maxlogtimeout: Maximum log age in logfile. Defaults to 0 (no limit)
    :param loglevel: Log level. Possible options include Basic, Detailed, Debug, 
        Rowlevel, Error, Nothing
    :param params: Dictionary of additional parameters (if required by the job). Defaults to None.
    :param output_encoding: Output encoding for return message, UTF-8 is default.

    Airflow will evaluate the exit code of the Kettle Operator. In general, a non-zero exit code will result
    in task failure and zero will result in task success. For more information on possible PDI exit codes refer
    to https://help.hitachivantara.com/Documentation/Pentaho/9.3/Products/Use_Command_Line_Tools_to_Run_Transformations_and_Jobs
    """

    ui_color = '#d49bd0'

    def __init__(
            self,
            *,
            pdipath: str = '/opt/pentaho/data-integration/',
            filepath: str = '/opt/pentaho/data-integration/jobs/',
            file: str | None = None,
            logfile: str = '/opt/pentaho/data-integration/logs/pdi.kitchen.log',
            maxloglines: int = 0,
            maxlogtimeout: int = 0,
            loglevel: str = 'Basic',  # Basic, Detailed, Debug, Rowlevel, Error, Nothing
            params: dict[str, str] | None = None,
            output_encoding: str = 'utf-8',
            **kwargs

    ) -> None:
        super().__init__(**kwargs)
        self.pdipath = pdipath
        self.filepath = filepath
        self.file = file
        self.logfile = logfile
        self.maxloglines = maxloglines
        self.maxlogtimeout = maxlogtimeout
        self.loglevel = loglevel
        self.params = params
        self.output_encoding = output_encoding

    @cached_property
    def subprocess_hook(self):
        return SubprocessHook()
    
    def execute(self, context: Context):
        bash_path = shutil.which('bash') or 'bash'
        # Check if everything is in place
        if not os.path.isdir(self.pdipath):
            raise AirflowException(f'PDI installation at {self.pdipath} not found')
        if not os.path.isdir(self.filepath):
            raise AirflowException(f'PDI kitchen jobs directory {self.filepath} not found')
        if self.file is None:
            raise AirflowException(f'PDI job file has not been specified')
        if not os.path.isfile(os.path.join(self.filepath, self.file)):
            raise AirflowException(f'PDI job file at {os.path.join(self.filepath, self.file)} not found')
        # Construct base pdi_command
        pdi_command = f'./kitchen.sh -file={os.path.join(self.filepath, self.file)} \
            -level={self.loglevel} \
            -logfile={self.logfile} \
            -maxloglines={self.maxloglines} \
            -maxlogtimeout={self.maxlogtimeout} \
            -norep=Y '
        # Get additional parameters
        for k, v in self.params.items():
            pdi_command += f'-param:{k}={v} '
        # Execute the command
        result = self.subprocess_hook.run_command(
            command=[bash_path, '-c', pdi_command],
            output_encoding=self.output_encoding,
            cwd=self.pdipath
        )
        if result.exit_code != 0:
            raise AirflowException(f'Kettle command failed. The command returned a non-zero exit code {result.exit_code}.')
        return result.output


class KettleRunTransformationOperator(BaseOperator):
    r"""
    Run a Kettle Transformation. PDI = Pentaho Data Integration

    :param pdipath: PDI HOME env var, or installation location,
        should point directly to the directory where pan.sh resides.
        Defaults to /opt/pentaho/data-integration/
    :param filepath: PDI transformation directory. Defaults to /opt/pentaho/data-integration/transformations/
    :param file: If None(default) throws an error, as this is required to run a PDI transformation.
        Should be a transformation filename ending with `.ktr`.
    :param logfile: PDI logfile for this particular run. Appends to the file if file 
        already exists. Defaults ot /opt/pentaho/data-integration/logs/pdi.kitchen.log
    :param maxloglines: Maximum log lines in logfile. Defaults to 0 (no limit)
    :param maxlogtimeout: Maximum log age in logfile. Defaults to 0 (no limit)
    :param loglevel: Log level. Possible options include Basic, Detailed, Debug, 
        Rowlevel, Error, Nothing
    :param params: Dictionary of additional parameters (if required by the transformation). Defaults to None.
    :param output_encoding: Output encoding for return message, UTF-8 is default.

    Airflow will evaluate the exit code of the Kettle Operator. In general, a non-zero exit code will result
    in task failure and zero will result in task success. For more information on possible PDI exit codes refer
    to https://help.hitachivantara.com/Documentation/Pentaho/9.3/Products/Use_Command_Line_Tools_to_Run_Transformations_and_Jobs
    """

    ui_color = '#c78b9d'

    def __init__(
            self,
            *,
            pdipath: str = '/opt/pentaho/data-integration/',
            filepath: str = '/opt/pentaho/data-integration/transformations/',
            file: str | None = None,
            logfile: str = '/opt/pentaho/data-integration/logs/pdi.kitchen.log',
            maxloglines: int = 0,
            maxlogtimeout: int = 0,
            loglevel: str = 'Basic',  # Basic, Detailed, Debug, Rowlevel, Error, Nothing
            params: dict[str, str] | None = None,
            output_encoding: str = 'utf-8',
            **kwargs

    ) -> None:
        super().__init__(**kwargs)
        self.pdipath = pdipath
        self.filepath = filepath
        self.file = file
        self.logfile = logfile
        self.maxloglines = maxloglines
        self.maxlogtimeout = maxlogtimeout
        self.loglevel = loglevel
        self.params = params
        self.output_encoding = output_encoding

    @cached_property
    def subprocess_hook(self):
        return SubprocessHook()
    
    def execute(self, context: Context):
        bash_path = shutil.which('bash') or 'bash'
        # Check if everything is in place
        if not os.path.isdir(self.pdipath):
            raise AirflowException(f'PDI installation at {self.pdipath} not found')
        if not os.path.isdir(self.filepath):
            raise AirflowException(f'PDI pan transformations directory {self.filepath} not found')
        if self.file is None:
            raise AirflowException(f'PDI transformation file has not been specified')
        if not os.path.isfile(os.path.join(self.filepath, self.file)):
            raise AirflowException(f'PDI transformation file at {os.path.join(self.filepath, self.file)} not found')
        # Construct base pdi_command
        pdi_command = f'./pan.sh -file={os.path.join(self.filepath, self.file)} \
            -level={self.loglevel} \
            -logfile={self.logfile} \
            -maxloglines={self.maxloglines} \
            -maxlogtimeout={self.maxlogtimeout} \
            -norep=Y '
        # Get additional parameters
        for k, v in self.params.items():
            pdi_command += f'-param:{k}={v} '
        # Execute the command
        result = self.subprocess_hook.run_command(
            command=[bash_path, '-c', pdi_command],
            output_encoding=self.output_encoding,
            cwd=self.pdipath
        )
        if result.exit_code != 0:
            raise AirflowException(f'Kettle command failed. The command returned a non-zero exit code {result.exit_code}.')
        return result.output
