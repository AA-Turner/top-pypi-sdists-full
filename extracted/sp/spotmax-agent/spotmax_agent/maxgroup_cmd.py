import base64
import json
import logging
import os
import subprocess
import threading
import time

from .basemodule import Module
from .utils import parse_yml, safeget, safe_get_url, safe_post_url

MAX_OUTPUT_STRING = 46000


class Cmd:
    def __init__(self, script_id, script, timeout, status, output, thread):
        self.script_id = script_id
        self.script = script
        self.timeout = timeout

        self.status = status
        self.output = output

        self.thread = thread
        self.lock = threading.RLock()

    def finish_handled_cmd(self):
        self.status = 'HANDLED'
        self.script = None
        self.timeout = None
        self.thread = None
        self.output = None


class SpotmaxCmdExecutor(Module):
    def __init__(self, *args, **kargs):
        super().__init__(*args)
        self.log = logging.getLogger('spotmax-agent')

        self.authentication_token = kargs['authentication_token']
        self.instance_id = kargs['instance_id']
        self.account_id = kargs['account_id']

        ifile = os.path.splitext(__file__)[0] + '.yml'
        yml = os.path.join(os.path.dirname(__file__), ifile)
        self.config = parse_yml(yml, self.log)
        self.process_scripts = {}
        self.update_url = None

    def load_splay(self):
        """
        delay for the worker to start
        :return:
        int value of delay in seconds
        """
        retval = safeget(self.config, 'splay')
        if not retval:
            self.log.debug("splay is not defined, returning default 10")
            retval = 10
        return int(retval)

    def load_interval(self):
        """
        delay for the worker interval
        :return:
        int value of interval in seconds
        """
        retval = safeget(self.config, 'interval')
        if not retval:
            self.log.debug("interval is not defined, returning default 10")
            retval = 10
        return int(retval)

    def get_enable(self):
        """
        check if the worker is enabled
        :return: Boolean
        """
        retval = safeget(self.config, 'enabled')
        return retval

    def run(self):

        if self.account_id:
            self.update_url = safeget(self.config, 'cmd_update_url_with_account_id')
            cmd_url_template = safeget(self.config, 'cmd_url_with_account_id')
        else:
            self.update_url = safeget(self.config, 'cmd_update_url')
            cmd_url_template = safeget(self.config, 'cmd_url')

        self.update_current_processes()

        if cmd_url_template:

            if self.account_id:
                cmdurl = cmd_url_template.format(self.instance_id, self.account_id)
                self.update_url = self.update_url.format(self.account_id)
                self.log.debug('The update url is ' + self.update_url + ' and the account_id is ' + self.account_id)
            else:
                cmdurl = cmd_url_template.format(self.instance_id)

            rawresponse = safe_get_url(cmdurl, self.authentication_token, self.log)
            response = safeget(rawresponse, 'response')
            if response and response['status']['code'] == 200:
                items = response['items']

                self.log.debug("items (count: {}): {}".format(len(items), items))
                self.log.info("Executor: retrieved {} items from server".format(len(items)))
                for item in items:
                    script = safeget(item, 'script')
                    script_id = safeget(item, 'id')
                    timeout = safeget(item, 'timeout')
                    if not script_id:
                        self.log.error("cmd id can't be null, skipping")
                        continue

                    cmd = Cmd(script_id, script, timeout, None, None, None)

                    # check is script already exists
                    if self.is_script_exist(script_id):
                        self.log.info("script is already known to agent")
                        continue
                    else:
                        cmd.status = 'RUNNING'
                        # add to processes scripts
                        self.add_to_script_manager(script_id, cmd)
                        self.update_cmd_status_to_server(script_id)

                    cmd.thread = self.execute_and_call(cmd)
            else:
                self.log.warning("got bad response from server... [{}]".format(response))
        else:
            self.log.warning("unable to get script server url template, check Worker configuration")

    def update_cmd_status_to_server(self, script_id):
        cmd = self.process_scripts[script_id]
        if cmd:
            lock = cmd.lock
            with lock:
                # report back an update
                wrapper = {}
                cmd_status = {'cmdId': script_id, 'status': cmd.status}
                if cmd.output:
                    cmd_status.update({'output': cmd.output.decode('utf-8')})
                wrapper.update({'cmdStatus': cmd_status})
                message = json.dumps(wrapper)
                self.log.info("updating status message: {}".format(cmd_status))
                safe_post_url(self.update_url, message, self.authentication_token, self.log)

    def execute_and_call(self, cmd):
        """
        This prepares to runs in another thread
        :param cmd:
        :return: thread
        """
        if cmd.script:
            if cmd.timeout:
                self.log.info("running the script (timeout '{}')...".format(cmd.timeout))
            else:
                self.log.info("running the script without any timeout...")

            script = base64.b64decode(cmd.script).decode('utf-8')
            self.log.debug("script: '{:.48}...'".format(script))

            # another thread
            def run_in_thread(callback):
                stdout = None
                stderr = None
                status = 'FINISHED'
                try:
                    process = subprocess.Popen(script, shell=True, cwd='/', universal_newlines=True,
                                               stdout=subprocess.PIPE,
                                               stderr=subprocess.PIPE, )
                    if not cmd.timeout:
                        # without any timeout
                        (stdout, stderr) = process.communicate()
                        stdout = stdout.strip()
                        stderr = stderr.strip()
                    else:
                        time.sleep(cmd.timeout)
                        if process.poll() is None:
                            process.kill()
                            self.log.error(
                                "script timeout exception occurs. CMD timeout of {0} exceeded".format(cmd.timeout))
                            stderr = 'Script timeout'
                            status = 'FAILED'
                        else:
                            (stdout, stderr) = process.communicate()
                            stdout = stdout.strip()
                            stderr = stderr.strip()

                except Exception as e:
                    self.log.error("script execution exception occurs: {0}".format(e.__str__()))
                    stderr = 'Script execution exception'
                    status = 'FAILED'

                stderr_size = len(stderr)
                stdout_size = len(stdout)
                total_size = stderr_size + stdout_size

                if (total_size > MAX_OUTPUT_STRING):
                    self.log.warn("[WARN] Script output is too long!")
                    self.log.info(
                        "stdout character length:{0}, stderr character length:{1}".format(stdout_size, stderr_size))
                    if (stderr_size > MAX_OUTPUT_STRING):
                        stderr = stderr[0::MAX_OUTPUT_STRING]
                        stdout = "Spotinst agent: Not enough space for standard IO"
                    else:
                        end = int(MAX_OUTPUT_STRING - stderr_size)
                        self.log.info("left space for standard output: {}".format(end))
                        stdout = (stdout[:end] + '..')
                        self.log.debug("[DEBUG] {0}".format(stdout))

                output = {'stdout': stdout, 'stderr': stderr}
                callback(cmd.script_id, status, output)

            thread = threading.Thread(target=run_in_thread, args=(self.handle_result,))
            thread.start()
            return thread

    def handle_result(self, script_id, status, output):
        """
        This handle script result
        :param script_id:
        :param status:
        :param output:
        :return:
        """
        self.log.debug("script id:{}, status:{}, ~output:'{!s:.120s}...'".format(script_id, status, output))
        cmd = self.process_scripts[script_id]
        with cmd.lock:
            cmd.status = status
            encoded_output = base64.b64encode(bytes(json.dumps(output)))
            cmd.output = encoded_output

        self.update_cmd_status_to_server(script_id)

        # remove from script manager
        self.log.info("Finish executing script (token:{})".format(script_id))
        with cmd.lock:
            cmd.finish_handled_cmd()
        self.log.info("-- Executor: Command done --")

    def update_current_processes(self):
        self.log.debug("checking & updating current threads")
        for c in self.process_scripts.values():
            with c.lock:
                if c.status == 'RUNNING':
                    self.log.debug("looking into script {}".format(c.script_id))
                    if c.thread.isAlive():
                        self.log.info("updating script {} 'RUNNING' status to server".format(c.script_id))
                        self.update_cmd_status_to_server(c.script_id)
                    else:
                        # remove from dictionary
                        self.log.error("script {} is running but thread is dead".format(c.script_id))
                        c.finish_handled_cmd()

    def add_to_script_manager(self, script_id, cmd):
        self.process_scripts[script_id] = cmd

    def is_script_exist(self, t):
        if t in self.process_scripts:
            return True
        else:
            return False
