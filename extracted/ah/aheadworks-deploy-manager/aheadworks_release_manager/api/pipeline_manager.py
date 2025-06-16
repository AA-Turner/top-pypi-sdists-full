from aheadworks_bitbucket_manager.api.bitbucket_api_manager import BitbucketApiManager
from aheadworks_bitbucket_manager.model.data.bitbucket import BitbucketConfig
import json
import subprocess
import os
import shutil
import json


class PipelineManager:

    def send_pipelines_to_workspace(self, bitbucket_workspace):
        # Install and configure git
        os.system('apk add git')
        os.system('git config --global user.email "bot@raveinfosys.com"')
        os.system('git config --global user.name "Automatic update"')

        bitbucket_api_manager = BitbucketApiManager(bitbucket_config=BitbucketConfig(bitbucket_workspace=bitbucket_workspace))
        # we only update modules that has 'module-' in the name
        full_repo_list = bitbucket_api_manager.get_repositories(name_contains = "module-")
        print(full_repo_list)

        new_bitbucket_pipelines = self.get_new_pipelines()

        os.system('mkdir tmpgit')
        os.chdir("./tmpgit")
        for url in full_repo_list:
            # skip the source repo module-boilerplate
            if url.find('module-boilerplate') == -1:
                self.update_repository_pipelines(url, new_bitbucket_pipelines)
        os.chdir("..")
        os.system('rm -r tmpgit')

    def get_new_pipelines(self):
        readFile = open("bitbucket-pipelines.yml")
        lines = readFile.readlines()
        readFile.close()
        # The Last line contains a weird comment with the date - strip it
        if lines[-1][0:1] == '#':
            del lines[-1]
        # Strip the "deploy pipelines" pipeline from the result so it won't be possible to send new pipelines from any M2 repo
        firstIndex = None
        lastIndex = None
        firstInstructionIndex = None
        lastInstructionIndex = None
        for index, line in enumerate(lines):
            if line.find('&deployPipelines') != -1:
                firstInstructionIndex = index
            # TODO: This line is going to change once we migrate to deploy-tools library
            elif line.find("send-pipelines-to-workspace") != -1:
                lastInstructionIndex = index + 1
            elif line.find('deploy-pipeline') != -1:
                firstIndex = index
            elif line.find('*deployPipelines') != -1:
                lastIndex = index + 1
        del lines[firstIndex:lastIndex]
        del lines[firstInstructionIndex:lastInstructionIndex]
        return "".join(lines)

    def update_repository_pipelines(self, url, new_bitbucket_pipelines):
        subprocess.Popen(['git', 'clone', url]).communicate()
        module = url.split('/')[-1].replace('.git', '')
        os.chdir(module)
        subprocess.Popen(['ls', '-la']).communicate()
        try:
            output = subprocess.check_output("git branch -al --no-merged", shell=True, text=True)
        except subprocess.CalledProcessError as e:
            # is it a broken/new repo ???
            print(e.returncode)
            print(e.output)
            return

        branches = output.splitlines()
        # 'splitlines' -- from str to list
        # branches_to_update list for update release or develop branches only
        branches_to_update = []

        # always add develop branch
        is_dev_branch_exists = subprocess.check_output("git branch -lr 'origin/develop'", shell=True)
        if is_dev_branch_exists:
            branches_to_update.append("develop")

        # add all unmerged 'release/' branches
        for branch in branches:
            clean_branch = branch.strip().removeprefix("remotes/origin/")
            if clean_branch.startswith('release'):
                branches_to_update.append(clean_branch)
            elif clean_branch.startswith('bugfix'):
                branches_to_update.append(clean_branch)
            elif clean_branch.startswith('feature'):
                branches_to_update.append(clean_branch)

        for branch in branches_to_update:
            subprocess.Popen(['git', 'checkout', branch]).communicate()
            f = open("bitbucket-pipelines.yml", "w")
            f.write(new_bitbucket_pipelines)
            f.close()
            subprocess.Popen(['git', 'add', "bitbucket-pipelines.yml"]).communicate()
            subprocess.Popen(['git', 'commit', '-m' "[SKIP CI] update bitbucket-pipelines.yml"]).communicate()
        subprocess.Popen(['git', 'push', '--all', 'origin']).communicate()
        os.chdir("..")

