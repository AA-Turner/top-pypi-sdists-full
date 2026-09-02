import os
import pathlib

import click

from jupyter_client.kernelspec import install_kernel_spec
from rich.console import Console
from rich.markdown import Markdown


ERROR_MESSAGE = """
# Automatic installation of jupyter kernel spec failed

To overcome this error, please install the kernelspec manually.

### MacOS/Linux instructions
Please run the following command on the terminal 

```
SITE_PACKAGES=$(pip3 show aws-glue-sessions | grep Location | awk '{print $2}')
  jupyter kernelspec install $SITE_PACKAGES/aws_glue_interactive_sessions_kernel/glue_pyspark
  jupyter kernelspec install $SITE_PACKAGES/aws_glue_interactive_sessions_kernel/glue_spark 
```

### Windows Instructions

1. Change the directory to the aws-glue-sessions install directory within python's site-packages directory.
    Windows PowerShell:
    ```
    cd ((pip3 show aws-glue-sessions | Select-String Location | % {$_ -replace("Location: ","")})+"\aws_glue_interactive_sessions_kernel")
    ```
2. Install the AWS Glue PySpark and AWS Glue Scala kernels.
    ```
    jupyter-kernelspec install glue_pyspark
    ```
    ```
    jupyter-kernelspec install glue_spark
    ```
"""


@click.group()
def cli():
    pass

@click.command()
def install():
    do_install()
def do_install_kernel_spec(kernel_name):
    print(f'Installing jupyter kernelspec for {kernel_name}')
    curr_path = pathlib.Path(__file__).parent.resolve()
    # Documentation : https://jupyter-client.readthedocs.io/en/latest/kernels.html#kernelspecs
    install_kernel_spec(str(curr_path.joinpath(f'{kernel_name}')), user=True, replace=True)
    print(f'Installed kernelspec for {kernel_name}')

def do_install():
    try:
        do_install_kernel_spec('glue_pyspark')
        do_install_kernel_spec('glue_spark')
    except Exception as ex:
        console = Console()
        md = Markdown(ERROR_MESSAGE)
        console.print(md)



if __name__ == '__main__':
    install()
