from aheadworks_bitbucket_manager.model.ssh_manager import SshManager


class DbManager:

    def __init__(self):
        self.ssh_manager = SshManager()

    def create_dump(self, path_to_sh, connection):
        command = 'test -f ' + path_to_sh + ' && echo True || echo False'
        file_exists = self.ssh_manager.run_ssh_command(command, connection)
        file_exists = eval(file_exists[0].strip()) if file_exists else False
        if file_exists:
            result = 'Db dump created'
            self.ssh_manager.run_ssh_command(path_to_sh, connection)
        else:
            result = 'Db dump missed'

        return result
