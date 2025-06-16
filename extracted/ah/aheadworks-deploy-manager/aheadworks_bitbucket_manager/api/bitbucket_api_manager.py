import json
import math
from aheadworks_core.model.http.api_request import ApiRequest as Api
from typing import Optional


class BitbucketApiManager:
    """api manager for bitbucket"""

    def __init__(self, bitbucket_config):
        self.sorted_deployments = None
        self.sorted_pipelines = None
        self.config = bitbucket_config
        self.request = Api(config=self.config)

    def get_build_by_commit(self, commit_hash: str, pipe_name, depth=1):
        """
        :param commit_hash: str
        :param pipe_name: bitbucket pipeline name
        :param depth: search depth in parent commits
        :return: build number: int
        :raises Exception: Сommit hash should not be less than 6 symbols.
        """

        if len(commit_hash) < 6:
            raise Exception('Сommit hash should not be less than 6 symbols.')

        build = self.get_build_number(commit_hash=commit_hash, pipe_name=pipe_name)
        if build is None:
            if depth == 0:
                raise Exception('Build not found.')
            else:
                commit = self.get_commit(commit_hash=commit_hash)
                parent_commits = commit['parents']
                if len(parent_commits) > 1:
                    sorted_parent_commits = list()
                    for _ in parent_commits:
                        commit_hash = _['hash']
                        commit = self.get_commit(commit_hash=commit_hash)
                        sorted_parent_commits.append(commit)
                    sorted_parent_commits = sorted(sorted_parent_commits, key=lambda k: (k['date']), reverse=True)
                    parent_commit = sorted_parent_commits[0]['hash']
                else:
                    parent_commit = parent_commits[0]['hash']
            depth -= 1
            return self.get_build_by_commit(parent_commit, pipe_name, depth)

        return build

    def get_build_number(self, commit_hash: str, pipe_name):
        """get bitbucket bld number by commit

        :param commit_hash: bitbucket commit hash, full or short
        :param pipe_name: bitbucket pipeline name
        :return: build number
        """
        build_number = None
        pipelines = self.get_sorted_pipelines()

        for pipeline in pipelines['values']:
            pipeline_commit_hash: Optional[str] = pipeline['target']['commit']['hash']
            if pipeline_commit_hash.find(commit_hash) == 0:
                if 'result' in pipeline['state'] \
                        and pipeline['state']['result']['name'] == 'SUCCESSFUL' \
                        and pipeline['target']['selector']['pattern'] in pipe_name:
                    build_number = pipeline['build_number']
                    break

        return build_number

    def get_build_number_from_deploy(self, commit_hash: str):
        """get bitbucket bld number by commit

        :param commit_hash: bitbucket commit hash, full or short
        :return: build number
        """
        build_number = None
        deploys = self.get_sorted_deployments()

        for deploy in deploys['values']:
            pipeline_uuid = deploy['deployable']['pipeline']['uuid']
            if deploy['release']['commit']['hash'].find(commit_hash) == 0:
                pipeline = self.get_pipeline(pipeline_uuid)
                pipeline_commit_hash: Optional[str] = pipeline['target']['commit']['hash']
                if pipeline_commit_hash.find(commit_hash) == 0:
                    build_number = pipeline['build_number']
                    break

        return build_number

    def get_commit(self, commit_hash: str, config=None):
        if config is None:
            config = self.config
        commit = self.request.get(location='/2.0/repositories/{}/{}/commit/{}'.format(
            config.bitbucket_workspace,
            config.bitbucket_repo_slug,
            commit_hash))
        return json.loads(commit)

    def get_pipeline(self, pipeline_uuid):
        pipeline = self.request.get(location='/2.0/repositories/{}/{}/pipelines/{}'.format(
            self.config.bitbucket_workspace,
            self.config.bitbucket_repo_slug,
            pipeline_uuid))
        return json.loads(pipeline)

    def get_sorted_pipelines(self, params=None):
        if self.sorted_pipelines is None:
            self.sorted_pipelines = self.get_pipelines(params)

            values = self.sorted_pipelines['values']
            values.reverse()
            self.sorted_pipelines['values'] = values

        return self.sorted_pipelines

    def get_pipelines(self, params=None):
        pagelen_default = 100
        if params is None:
            params = {}
        params['pagelen'] = pagelen_default
        deploys = self.request.get(location='/2.0/repositories/{}/{}/pipelines/'.format(
            self.config.bitbucket_workspace,
            self.config.bitbucket_repo_slug
            ), params=params
        )
        result = json.loads(deploys)
        cur_page = result['page']
        count_page = math.ceil(result['size'] / pagelen_default)
        if cur_page < count_page:
            params['page'] = cur_page + 1
            result['values'].extend(self.get_pipelines(params=params)['values'])

        return result

    def get_sorted_deployments(self, params=None):
        if self.sorted_deployments is None:
            self.sorted_deployments = self.get_deployments(params)

            values = self.sorted_deployments['values']
            values = sorted(values, key=lambda k: (k['deployable']['created_on']), reverse=True)
            self.sorted_deployments['values'] = values

        return self.sorted_deployments

    def get_deployments(self, params=None):
        if params is None:
            params = {'pagelen': '100'}
        deploys = self.request.get(location='/2.0/repositories/{}/{}/deployments/'.format(
            self.config.bitbucket_workspace,
            self.config.bitbucket_repo_slug
            ), params=params
        )
        result = json.loads(deploys)
        if 'next' in result.keys():
            query = result['next'].split('?')[1]
            params = {}
            for _ in query.split('&'):
                params[_.split('=')[0]] = _.split('=')[1]
            result['values'].extend(self.get_deployments(params=params)['values'])

        return result

    def upload_artifacts(self, artifacts):
        responses = []
        if type(artifacts) is not list:
            artifacts = [artifacts, ]
        for f in artifacts:
            files = {'files': open(f, 'rb')}
            responses.append(
                self.request.post(
                    location = f"/2.0/repositories/{self.config.bitbucket_workspace}/{self.config.bitbucket_repo_slug}/downloads",
                    files=files
                )
            )
        return responses

    def get_repositories(self, name_contains = None):
        repopage = f"/2.0/repositories/{self.config.bitbucket_workspace}?pagelen=100&fields=next,values.links.clone.href"
        if name_contains:
            repopage = f'{repopage}&q=name~"{name_contains}"'
        full_repo_list = []
        while repopage is not None:
            response_text = self.request.get(location=repopage)
            page_json = json.loads(response_text)
            for repo in page_json['values']:
                repogit=repo['links']['clone'][1]['href']
                full_repo_list.append(repogit)
            repopage = page_json.get('next', None)
            if repopage:
                repopage = repopage.removeprefix('https://api.bitbucket.org')
        return full_repo_list

    def run_pipeline(self, repo, data):
        return self.request.post(
            f"/2.0/repositories/{repo}/pipelines/", json=data
        )
