import json
from typing import Dict
import dateutil.parser
import docker
from aheadworks_core.model.http.api_request import ApiRequest as Api
from aheadworks_bitbucket_manager.api.bitbucket_api_manager import BitbucketApiManager
import re


class DockerhubApiManager:
    """DockerHub api manager"""

    def __init__(self, docker_hub_config, bitbucket_config):
        """
        :param repo: DockerHub repository name
        """
        self.bitbucket_api_manager = BitbucketApiManager(bitbucket_config)
        self.config = docker_hub_config
        self.request = Api(config=self.config)
        self.pull_expire_date = self.config.pull_expire_date
        self.push_expire_date = self.config.push_expire_date
        self.count_image_to_save = 8

    def remove_deprecated_versions_images(self, repo):
        tags = self.get_tags(repo)
        minor_version_images = list()
        for i in tags['results']:
            match_value = re.search('[0-9]-[0-9]', i['name'])
            if match_value:
                minor_version_images.append(i)
        images = list()
        if len(minor_version_images) <= self.count_image_to_save:
            # todo refactoring, add to log
            print(f'there less than {self.count_image_to_save} images, Nothing will be removed')
            return None
        minor_version_images = sorted(minor_version_images, key=lambda x: x['name'].split('-')[-1], reverse=True)
        for i in minor_version_images[self.count_image_to_save:]:
            tag_last_pulled = i['tag_last_pulled']
            pull_date = dateutil.parser.parse(tag_last_pulled).replace(tzinfo=None) or None
            push_date = dateutil.parser.parse(i['tag_last_pushed']).replace(tzinfo=None)
            if push_date < self.push_expire_date and (pull_date < self.pull_expire_date or pull_date is None):
                self.remove_tag(i['name'], repo)
                images.append(i['name'])
                # todo refactoring, add to log
                print(f'removes {self.config.dockerhub_user}/{repo}:{i["name"]}')
        if len(images) == 0:
            # todo refactoring, add to log
            print('there no images older than 30 days. Nothing will be removed')
        return

    def get_images_by_commit(self, commit_hash: str, repo, pipe_name):
        """
        :param commit_hash:
        :param repo:
        :return:
        :raises Exception: Images for this build not exists.
        """

        build_number = self.bitbucket_api_manager.get_build_by_commit(commit_hash, pipe_name)

        tag_names = []
        tags = self.get_tags(repo)['results']
        images = list()
        for tag in tags:
            tag_names.append(tag['name'])
            if tag['name'].find(f'-{str(build_number)}') != -1:
                images.append(f'{self.config.dockerhub_user}/{repo}:{tag["name"]}')
        if len(images) == 0:
            raise Exception(
                "Images for this build not exists. DH Repo: %s, Build: %s, Commit: %s, Tags count: %s, Tags: %s"
                % (repo, build_number, commit_hash, len(tags), repr(tag_names))
            )

        return images

    def renew_images_by_tag(self, commit_hash, repo, pipe_name):
        images = self.get_images_by_commit(commit_hash, repo, pipe_name)
        self.retag_images(images, repo)
        return True

    def retag_images(self, images: list, repo):
        """
        :param images:
        :param repo:
        :return:
        """

        docker_client = self._docker_client_login()
        for i in images:
            image = docker_client.images.pull(i)
            repository, tag = i.split(':')
            new_tag = '-'.join(tag.split('-')[0:-1])
            image.tag(repository, new_tag)
            docker_client.images.push(f"{repository}:{new_tag}")
            print(f"rename {i} to {repository}:{new_tag}")
            self.remove_tag(tag, repo)

    def get_tags(self, repo):
        headers: Dict = self.config.auth_headder
        params = (('page_size', '10000'),)
        r = self.request.get(location='/v2/repositories/{}/{}/tags/?page_size=10000'.format(
                             self.config.dockerhub_user,
                             repo),
                             params=params,
                             headers=headers)
        return json.loads(r)

    def remove_tag(self, tag_name, repo):
        headers: Dict = self.config.auth_headder
        r = self.request.delete(location='/v2/repositories/{}/{}/tags/{}/'.format(
                                self.config.dockerhub_user,
                                repo,
                                tag_name),
                                headers=headers)
        return r

    def push_images(self, images):
        docker_client = self._docker_client_login()
        result = ''
        for image in images:
            for line in docker_client.images.push(image, stream=True, decode=True):
                result += str(line) + '\n'
        return result

    def _docker_client_login(self):
        docker_client = docker.from_env()
        docker_client.login(username=self.config.dockerhub_user, password=self.config.dockerhub_password)
        return docker_client
