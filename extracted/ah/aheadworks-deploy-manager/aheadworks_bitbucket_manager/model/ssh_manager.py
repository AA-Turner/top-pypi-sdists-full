import subprocess


class SshManager:

    def run_ssh_command(self, command, connection):
        #host, user, port=22
        host = connection['user'] + '@' + connection['host']

        if connection['port'] != 22:
            subprocess_params = ["ssh", "-p %d" % connection['port'], "%s" % host, command]
        else:
            subprocess_params = ["ssh", "%s" % host, command]

        output = subprocess.check_output(
            subprocess_params,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        output = output.splitlines()

        return output
