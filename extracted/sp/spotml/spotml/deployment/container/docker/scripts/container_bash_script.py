import os
import chevron
from spotml.deployment.utils.commands import get_bash_command
from spotml.deployment.container.docker.scripts.abstract_docker_script import AbstractDockerScript


class ContainerBashScript(AbstractDockerScript):

    def render(self) -> str:
        # read template file
        template_path = os.path.join(os.path.dirname(__file__), 'data', 'container_bash.sh.tpl')
        with open(template_path) as f:
            template = f.read()

        # render the script
        content = chevron.render(template, data={
            'docker_exec_bash': self.commands.exec(get_bash_command(), interactive=True, tty=True,
                                                   container_name='$SPOTML_CONTAINER_NAME',
                                                   working_dir='$SPOTML_CONTAINER_WORKING_DIR'),
        })

        return content
