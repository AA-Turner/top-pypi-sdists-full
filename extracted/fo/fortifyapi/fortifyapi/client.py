from typing import Union, Tuple
from datetime import date
import time
from socket import gethostname
from .exceptions import *
from .template import *
from .query import Query
from .api import FortifySSCAPI
from requests_toolbelt import MultipartEncoder
from os.path import basename, exists


class FortifySSCClient:

    def __init__(self, url: str, auth: Union[str, Tuple[str, str]], proxies=None, verify=True):
        """
        :param url: url to ssc, including the path. E.g. `https://fortifyssc/ssc`
        :param auth: Authentication, either a token str or a (username, password) tuple
        """
        self._url = url
        self._auth = auth
        self._api = FortifySSCAPI(url, auth, proxies, verify)

        self.versions = Version(self._api, None, self)
        self.projects = Project(self._api, None, self)
        self.pools = CloudPool(self._api, None, self)
        self.workers = CloudWorker(self._api, None, self)
        self.cloudjobs = CloudJob(self._api, None, self)
        self.sscjobs = SSCJob(self._api, None, self)
        self.reports = Report(self._api, None, self)
        self.auth_entities = AuthEntity(self._api, None, self)
        self.local_user = LocalUser(self._api, None, self)
        self.ldap_user = LdapUser(self._api, None, self)
        self.rulepacks = Rulepack(self._api, None, self)
        self.filetoken = FileToken(self._api, None, self)

    def _list(self, endpoint, **kwargs):
        with self._api as api:
            for e in api.page_data(endpoint, **kwargs):
                yield e

    def list_engine_types(self, **kwargs):
        for e in self._list('/api/v1/engineTypes', **kwargs):
            yield Engine(self._api, e, self)

    def list_all_project_versions(self, **kwargs):
        # todo: remove duplicate, same as Version#search
        kwargs['limit'] = -1
        for e in self._list('/api/v1/projectVersions', **kwargs):
            yield Version(self._api, e, None)
            
    def list_all_bugtrackers(self, **kwargs):
        with self._api as api:
            for e in api.page_data(f"/api/v1/bugtrackers", **kwargs):
                yield Bugtracker(self._api, e, self)

    def license(self):
        with self._api as api:
            return api.get('/api/v1/license')

    @property
    def api(self):
        return self._api


class SSCObject(dict):
    def __init__(self, api, obj=None, parent=None):
        super().__init__(obj if obj else {})
        assert isinstance(api, FortifySSCAPI), 'Wrong parameter type, api should be FortifySSCAPI'
        self._api = api
        self.parent = parent

    def __str__(self):
        return f"{self.__class__}({super().__str__()})"

    def is_instance(self):
        return len(self) != 0

    def assert_is_instance(self, msg=None):
        if not self.is_instance():
            raise NotAnInstanceException(msg)


class Version(SSCObject):

    def __init__(self, api, obj, parent):
        super().__init__(api, obj, parent)
        self.attributes = Attribute(api, obj, self)
        self.issues = Issue(api, obj, self)
        self.custom_tags = CustomTag(api, obj, self)
        self.artifacts = Artifact(api, obj, self)

    def initialize(self, template=DefaultVersionTemplate):
        """
        Called automatically when Version.create is called.

        :return:
        """
        with self._api as api:
            if not isinstance(template, DefaultVersionTemplate):
                template = template()
            data = template.generate(api=api, project_version_id=self['id'])
            return api.bulk_request(data)

    def create(self, version_name, description="", active=True, committed=False, template=DefaultVersionTemplate,
               dataRetentionPolicyOverride=False):
        """ Creates a version for the CURRENT project with required processing rules """

        self.assert_is_instance("Cannot create version for empty project - consider using `create_project_version`")
        assert self.parent['name'] is not None, "how is the parent name None?"
        return self.parent.create(self.parent['name'], version_name, description=description, active=active,
                                  committed=committed, project_id=self.parent['id'],
                                  issue_template_id=self.parent['issueTemplateId'], template=template,
                                  dataRetentionPolicyOverride=dataRetentionPolicyOverride)

    def copy(self, new_name: str, new_description: str = ""):
        """
        Copy THIS project version including findings and finding state.
        Useful for some operations, e.g. pull requests
        """
        self.assert_is_instance()
        return self.create(new_name, new_description, active=self['active'], committed=self['committed'],
                           dataRetentionPolicyOverride=self['dataRetentionPolicyOverride'],
                           template=CloneVersionTemplate(self['id']))

    def list(self, **kwargs):
        if not self.parent:
            raise ParentNotFoundException("No project parent found to query versions from")
        with self._api as api:
            for e in api.page_data(f"/api/v1/projects/{self.parent['id']}/versions", **kwargs):
                p = Project(self._api, e['project'], None) if 'project' in e else self.parent
                yield Version(self._api, e, p)

    def search(self, **kwargs):
        with self._api as api:
            for e in api.page_data(f"/api/v1/projectVersions", **kwargs):
                p = Project(self._api, e['project'], None) if 'project' in e else self.parent
                yield Version(self._api, e, p)

    def list_auth_entities(self, **kwargs):
        self.assert_is_instance()
        with self._api as api:
            for e in api.page_data(f"/api/v1/projectVersions/{self['id']}/authEntities", **kwargs):
                yield AuthEntity(self._api, e, self.parent)

    def get(self, id):
        with self._api as api:
            return Version(self._api, api.get(f"/api/v1/projectVersions/{id}")['data'], self.parent)

    def project_exist(self):
        with self._api as api:
            return

    def delete(self):
        """ Delete the current version """
        self.assert_is_instance()
        with self._api as api:
            return api.delete(f"/api/v1/projectVersions/{self['id']}")

    def get_processing_rules(self, **kwargs):
        self.assert_is_instance()
        with self._api as api:
            return api.get(f"/api/v1/projectVersions/{self['id']}/resultProcessingRules", **kwargs)

    def set_processing_rules(self, rules):
        self.assert_is_instance()
        with self._api as api:
            return api.put(f"/api/v1/projectVersions/{self['id']}/resultProcessingRules", rules)

    def issue_summary(self, series_type='DEFAULT', group_axis_type='ISSUE_FOLDER'):
        self.assert_is_instance()
        with self._api as api:
            return api.get(f"/api/v1/projectVersions/{self['id']}/issueSummaries",
                           seriestype=series_type,
                           groupaxistype=group_axis_type)['data']

    def test(self, application_name: str, version_name: str) -> bool:
        """
        Check whether the specified application name is already defined in the system
        :param application_name: Application or Project name in SSC you want to test the value of.
        :param version_name: Application or Project version you want to test the value of.
        :return: A response object of found for true or false
        """
        with self._api as api:
            return api.post(f"/api/v1/projectVersions/action/test", projectName=application_name,
                            projectVersionName=version_name)['data']['found']
            
    def get_bugtracker(self):
        with self._api as api:
            b = api.get(f"/api/v1/projectVersions/{self['id']}/bugtracker")['data'][0]['bugTracker']
            if b is not None:
                return Bugtracker(self._api, b, self)   
            return b
        
    def set_bugtracker(self, bugtracker):
        with self._api as api:
            b = api.put_array(f"/api/v1/projectVersions/{self['id']}/bugtracker", [bugtracker])['data'][0]['bugTracker']
            if b is not None:
                return Bugtracker(self._api, b, self)   
            return b

    def upload_artifact(self, file_path, process_block=False, engine_type=None, timeout=None):
        """
        Upload an artifact to an SSC version. Supports streaming as to allow extremely large artifact uploads.
        
        :param process_block: Block this method for Artifact processing
        :param engine_type: str To specify the parser to be used to process this artifact, see /ssc/html/ssc/admin/parserplugins
        :param timeout: int Used if blocking, in how many seconds we should timeout and throw an Exception. Default is never.
        """
        self.assert_is_instance()
        with self._api as api:
            query = dict(engineType=engine_type) if engine_type else {}
            m = MultipartEncoder(fields={'file': (basename(file_path), open(file_path, 'rb'), 'application/zip')})
            h = {'Content-Type': m.content_type}
            robj = api._request('POST', f"/api/v1/projectVersions/{self['id']}/artifacts", data=m, params=query, headers=h)
            art = Artifact(self._api, robj['data'], self)
            now = time.time()
            if process_block:
                while True:
                    a = art.get(art['id'])
                    if a['status'] in ['PROCESS_COMPLETE', 'ERROR_PROCESSING', 'REQUIRE_AUTH']:
                        return a
                    time.sleep(1)
                    if timeout and (time.time() - now) > timeout:
                        raise TimeoutError("Upload artifact was blocking and exceeded the timeout")
            return art

    def download_url(self, includeSource=True):
        """Download the current version as fpr, with all triage state"""
        self.assert_is_instance()
        token = FileToken(self._api, None, self).create(purpose='DOWNLOAD')
        return f"{self._api.url}/download/currentStateFprDownload.html?mat={token['token']}&id={self['id']}&clientVersion=24.2.0.0186&includeSource={includeSource}"

    def download(self, includeSource=True):
        with self._api as api:
            return api.get(self.download_url(includeSource))

    def purge(self, purgeBefore, projectVersionIds=None):
        """
        :param purgeBefore: should be a date time, likely `pv['currentState']['lastFprUploadDate']`
        :param projectVersionIds: list of project version ids to purge, else will use the current project version
        """
        if projectVersionIds is None:
            self.assert_is_instance()
            projectVersionIds = [self['id']]
        with self._api as api:
            return api.post('/api/v1/projectVersions/action/purge', {'projectVersionIds': projectVersionIds, 'purgeBefore': purgeBefore})


class Project(SSCObject):

    def __init__(self, api, obj=None, parent=None):
        super().__init__(api, obj, parent)
        self.versions = Version(api, None, self)

    def list(self, **kwargs):
        """
        :param kwargs: The request query parameters
        :returns: Generator of each fortifyapi.Project
        """
        with self._api as api:
            for e in api.page_data('/api/v1/projects', **kwargs):
                yield Project(self._api, e, self.parent)

    def test(self, application_name: str) -> bool:
        """
        Check whether the specified application name is already defined in the system
        :returns: If the application_name was found
        """
        with self._api as api:
            return api.post(f"/api/v1/projects/action/test", applicationName=application_name)['data']['found']

    def get(self, id):
        """
        Get the given project by id
        :param id:
        :returns: fortifyapi.Project
        """
        with self._api as api:
            return Project(self._api, api.get(f"/api/v1/projects/{id}")['data'], self.parent)

    def update(self):
        """
        :returns: The updated Project object
        """
        self.assert_is_instance()
        with self._api as api:
            return Project(self._api, api.put(f"/api/v1/projects/{self['id']}", self)['data'], self)

    def create(self, project_name, version_name, project_id=None, description="Created on " + str(date.today())
               + " from " + gethostname(), active=True,
               committed=False, issue_template_id='Prioritized-HighRisk-Project-Template',
               template=DefaultVersionTemplate, dataRetentionPolicyOverride=False):
        """
        You want to use upsert method for your implementation and NOT this function directly.  project.id is not
        validated which may not be a big deal, but may create problems in edge cases. See also SSC spec,
        project-version-controller, Manage application versions. A variety of associated resources are accessible
         via links.
        :param project_name:
        :param version_name:
        :param project_id:
        :param description:
        :param active:
        :param committed:
        :param issue_template_id:
        :param template:
        :return: Returns the Version object or False
        :rtype: fortifyapi.Version or bool
        """
        with self._api as api:
            r = api.post(f"/api/v1/projectVersions", {
                'name': version_name,
                'description': description,
                'active': active,
                'committed': committed,
                'project': {
                    'id': project_id,  # if this is None it will create the project
                    'name': project_name,
                    'description': description,
                    'issueTemplateId': issue_template_id
                },
                'issueTemplateId': issue_template_id,
                'dataRetentionPolicyOverride': dataRetentionPolicyOverride
            })
            p = Project(self._api, r['data']['project'], None) if 'project' in r['data'] else self

            v = Version(self._api, r['data'], p)
            v.initialize(template=template)
            # get it again, so we see it's true state
            # we should really just re-get the Project, so it has all the proper data
            p = Project(self._api, {}, None).get(p['id'])
            return p.versions.get(v['id'])

    def upsert(self, project_name, version_name, description="Created on " + str(date.today())
               + " from " + gethostname(), active=True,
               committed=False, issue_template_id='Prioritized-HighRisk-Project-Template',
               template=DefaultVersionTemplate) -> Version:
        """
        Implements the Project().create, but will test/ query if project exists, if not it will
        create both Project and version.  A project is dependent on at least one version associated to it.
        """
        def _find_project_version(pname, pver=None):
            q = Query().query("project.name", pname)
            if pver:
                q = q.query("name", pver)
            version = next(self.versions.search(q=q), None)
            if not version:
                q = Query().query("project.name", f"*{pname}*")
                if pver:
                    q = q.query("name", f"*{pver}*")
                version = next(self.versions.search(q=q), None)
            if version:
                return version
            return None

        if self.test(application_name=project_name) is False:
            return self.create(project_name, version_name, description=description, active=active,
                               committed=committed, issue_template_id=issue_template_id, template=template)
        elif self.versions.test(project_name, version_name) is False:
            # just need to make version, but use the projectVersions endpoint as it does not contain the unicode bug
            project_version = _find_project_version(project_name)
            if not project_version:
                raise ParentNotFoundException(f"Somehow `{project_name}` exists yet we cannot query for it")
            return self.create(project_name, version_name, project_id=project_version['project']['id'], description=description,
                               active=active, committed=committed, issue_template_id=issue_template_id,
                               template=template)
        else:
            version = _find_project_version(project_name, version_name)
            if version:
                return version
            else:
                raise ParentNotFoundException(f"Somehow `{project_name}` - `{version_name}` exists yet we cannot query for it")


    def delete(self):
        # delete every version and project will delete
        self.assert_is_instance()
        for v in self.versions.list():
            v.delete()


class Engine(SSCObject):
    pass


class CloudPool(SSCObject):

    def get(self, uuid):
        with self._api as api:
            return CloudPool(self._api, api.get(f"/api/v1/cloudpools/{uuid}")['data'], self.parent)

    def list(self, **kwargs):
        with self._api as api:
            for e in api.page_data(f"/api/v1/cloudpools", **kwargs):
                yield CloudPool(self._api, e, self.parent)

    def create(self, pool_name, description=None):
        with self._api as api:
            r = api.post(f"/api/v1/cloudpools", {
                "name": pool_name,
                "description": description if description else '',
            })
            return CloudPool(self._api, r['data'])

    def delete(self):
        self.assert_is_instance()
        with self._api as api:
            return api.delete(f"/api/v1/cloudpools/{self['uuid']}")

    def assign(self, pool_uuid, worker_uuid):
        """
        This endpoint is one of two that can be implemented, the other is a Post bulk request
        implementing "https://fortify.example.com/ssc/api/v1/cloudpools/{pool_uuid}/versions/action".
        Either one will work
        :param pool_uuid:
        :param worker_uuid:
        :return: ['status'] == success
        """
        with self._api as api:
            r = api.post(f"/api/v1/cloudpools/{pool_uuid}/workers/action", {
                "type": "assign",
                "ids": [worker_uuid] if type(worker_uuid) is str else list(worker_uuid)
            })
            return CloudPool(self._api, r['data'])

    def jobs(self):
        self.assert_is_instance()
        with self._api as api:
            for e in api.page_data(f"/api/v1/cloudpools/{self['uuid']}/jobs"):
                yield CloudJob(self._api, e, self)


class CloudWorker(SSCObject):

    def list_unassigned(self, **kwargs):
        with self._api as api:
            for e in api.page_data(f"/api/v1/cloudpools/disabledWorkers", **kwargs):
                yield CloudWorker(self._api, e, self.parent)

    def list(self, **kwargs):
        with self._api as api:
            for e in api.page_data(f"/api/v1/cloudworkers", **kwargs):
                yield CloudWorker(self._api, e, self.parent)


class CloudJob(SSCObject):
    """
    Object represents a Job (Scan Request)

    Schema({
        'jobToken': str,
        '_href': str,
        'cloudPool': object, #CloudPool,
        'cloudWorker': object, #CloudWorker,
        'jobCancellable': bool,
        'jobDuration': int,  # seemingly milliseconds
        'jobExpiryTime': Use(datetime.datetime.fromisoformat),
        'jobFinishedTime': Use(datetime.datetime.fromisoformat),
        'jobHasFpr': bool,
        'jobHasLog': bool,
        'jobQueuedTime': Use(datetime.datetime.fromisoformat),
        'jobStartedTime': Use(datetime.datetime.fromisoformat),
        'jobState': Or(
            'INVALID',
            'PENDING',
            'IN_PROGRESS', # not sure when its this vs SCAN_RUNNING ...
            'UPLOAD_QUEUED',
            'UPLOAD_CANCELED',
            'UPLOAD_COMPLETED',
            'UPLOAD_FAILED',
            'SCAN_FAULTED',
            'SCAN_FAILED',
            'SCAN_TIMEOUT',
            'SCAN_COMPLETED',
            'SCAN_CANCELED',
            'SCAN_RUNNING',
            'CANCELING'
        ),
        'jobToken': str,
        'priority': int,
        'projectId': int,
        'projectName': str,
        'pvId': int,
        'pvName': str,
        'queuedDuration': int,
        'scaArgs': str,
        'scaBuildId': str,
        'scaVersion': str,  # the version of fortify used, e.g. 22.2.2.0004
        'scanDuration': int,
        'submitterEmail': Or(str, None),
        'submitterIpAddress': str,
        'submitterUserName': str
    })
    """

    def list(self, **kwargs):
        with self._api as api:
            for e in api.page_data(f"/api/v1/cloudjobs", **kwargs):
                yield CloudJob(self._api, e, self.parent)

    def list_all(self, **kwargs):
        """ Helper function to just disable paging and get them all """
        kwargs['limit'] = -1
        for e in self.list(**kwargs):
            yield e

    def get(self, job_token):
        with self._api as api:
            return CloudJob(self._api, api.get(f"/api/v1/cloudjobs/{job_token}")['data'], self.parent)

    def cancel(self, job_token: str):
        """
        Manage ScanCentral SAST jobs with state change to CANCEL.  Typical usage
        would be of a large backlog of PENDING jobs, because no sensor was available or is in a bad state.
        :param job_token: Scan Central Job Token assigned to the job
        TODO: fix with return api.post(f"/api/v1/cloudjobs/{job_token}/acion", type="cancel")['data']['status'].  See
        POST /ssc/api/v1/cloudjobs/1076964f-ec72-48e1-a897-6da9683a75df/action HTTP/1.1
        {"type":"cancel"}
        """
        with self._api as api:
            return api.post(f"/api/v1/cloudjobs/action/cancel", jobTokens=[self['jobToken']])


class Scan(SSCObject):

    def get(self, id):
        f"/api/v1/scans/{id}"  # GET

    def list(self, **kwargs):
        with self._api as api:
            for e in api.page_data(f"/api/v1/artifacts/{self['id']}/scans", **kwargs):
                yield Scan(self._api, e, self)


class Artifact(SSCObject):

    def __init__(self, api, obj=None, parent=None):
        super().__init__(api, obj, parent)
        self.scans = Scan(api, None, self)

    def get(self, id):
        with self._api as api:
            return Artifact(self._api, api.get(f"/api/v1/artifacts/{id}")['data'], self.parent)

    def list(self, **kwargs):
        self.assert_is_instance()
        with self._api as api:
            for e in api.page_data(f"/api/v1/projectVersions/{self['id']}/artifacts", **kwargs):
                yield Artifact(self._api, e, self)

    def delete(self, id):
        f"/api/v1/artifacts/{id}" # DELETE
        raise NotImplementedError()

    def approve(self):
        f"/api/v1/artifacts/action/approve" # POST
        raise NotImplementedError()

    def download_url(self, includeSource=True):
        """Note, this downloads a given artifact directly, it will not contain any project version state"""
        self.assert_is_instance()
        token = FileToken(self._api, None, self).create(purpose='DOWNLOAD')
        return f"{self._api.url}/download/artifactDownload.html?mat={token['token']}&id={self['id']}&includeSource={includeSource}"

    def download(self, includeSource=True):
        with self._api as api:
            return api.get(self.download_url(includeSource))


class Issue(SSCObject):
    NOT_SET = -1
    NOT_AN_ISSUE = 0
    RELIABILITY_ISSUE = 1
    BAD_PRACTICE = 2
    SUSPICIOUS = 3
    EXPLOITABLE = 4

    def list(self, **kwargs):
        with self._api as api:
            for e in api.page_data(f"/api/v1/projectVersions/{self.parent['id']}/issues", **kwargs):
                yield Issue(self._api, e, self.parent)

    def get(self, id):
        with self._api as api:
            return Issue(self._api, api.get(f"/api/v1/projectVersions/{self.parent['id']}/issues/{id}")['data'], self.parent)

    def assign(self, user):
        """
        :param user: user id?
        """
        self.assert_is_instance()
        o = dict(user=user)
        f"/api/v1/projectVersions/{self.parent['id']}/issues/action/assignUser"

    def audit(self,  analysis, comment="via automation", user=None, suppressed=False, tags=None):
        """
        :param analysis: zero to four
        :param comment: Issue comment
        :param user: Username to assign, else None
        :param suppressed: Will suppress the issue
        :param tags: ?
        """
        self.assert_is_instance()
        assert analysis in [
            Issue.NOT_SET,
            Issue.NOT_AN_ISSUE,
            Issue.RELIABILITY_ISSUE,
            Issue.BAD_PRACTICE,
            Issue.SUSPICIOUS,
            Issue.EXPLOITABLE
        ], "Not a valid analysis type"
        o = {
            'issues': [{
                'id': self['id'],
                'revision': self['revision']
            }],
            'comment': comment,
            'suppressed': suppressed,
            'customTagAudit': [{
                'customTagGuid': '87f2364f-dcd4-49e6-861d-f8d3f351686b',
                'newCustomTagIndex': analysis
            }]
        }
        if user:
            o['user'] = user
        if tags:
            if isinstance(tags, list):
                for t in tags:
                    o['customTagAudit'].append(t)
            else:
                o['customTagAudit'].append(tags)

        with self._api as api:
            return api.post(f"/api/v1/projectVersions/{self.parent['id']}/issues/action/audit", o)

    def suppress(self, suppressed=True):
        self.assert_is_instance()
        o = {
            'issues': [{
                'id': self['id'],
                'revision': self['revision']
            }],
            "suppressed": suppressed
        }
        with self._api as api:
            return api.post(f"/api/v1/projectVersions/{self.parent['id']}/issues/action/suppress", o)

    def unsuppress(self):
        self.suppress(False)


class Attachment(SSCObject):

    def list(self, **kwargs):
        with self._api as api:
            for e in api.page_data(f"/api/v1/issues/{self.id}/attachments", **kwargs):
                yield Attachment(self._api, e)

    def get(self, id):
        f"/api/v1/projectVersions/{self.id}/attributes/{id}" # GET
        raise NotImplementedError()

    def update(self):
        f"/api/v1/projectVersions/{self.parent.id}/attributes/{self.id}" # UPDATE
        raise NotImplementedError()

    def delete(self, id):
        f"/api/v1/projectVersions/{self.parent.id}/attributes/{self.id}" # UPDATE
        raise NotImplementedError()

    def upload(self):
        f"/api/v1/issues/{self.id}/attachments" # POST
        raise NotImplementedError()

    def delete_all(self):
        f"/api/v1/issues/{self.parent.id}/attachments" # DELETE
        raise NotImplementedError()


class Attribute(SSCObject):

    def list(self, **kwargs):
        with self._api as api:
            for e in api.page_data(f"/api/v1/projectVersions/{self['id']}/attributes", **kwargs):
                yield Attribute(self._api, e, self.parent)

    def get(self, id):
        f"/api/v1/projectVersions/{self['id']}/attributes/{id}" # GET
        raise NotImplementedError()

    def create(self):
        f"/api/v1/projectVersions/{self['id']}/attributes" # POST
        raise NotImplementedError()

    def update(self):
        f"/api/v1/projectVersions/{self['id']}/attributes"  # PUT
        raise NotImplementedError()


class Report(SSCObject):

    def list(self, **kwargs):
        with self._api as api:
            for e in api.page_data(f"/api/v1/reports", **kwargs):
                yield Report(self._api, e, self.parent)

    def get(self, id):
        f"/api/v1/reports/{id}"
        raise NotImplementedError()

    def create(self):
        f"/api/v1/reports" # POST
        raise NotImplementedError()

    def delete(self):
        """ Delete the current report """
        with self._api as api:
            return api.delete(f"/api/v1/reports/{self['id']}")


class FileToken(SSCObject):

    def create(self, purpose='DOWNLOAD'):
        """
        :param purpose: valid values are `DOWNLOAD` and `UPLOAD`
        """
        assert purpose in ['UPLOAD', 'DOWNLOAD'], "Unsupported purpose"

        with self._api as api:
            return FileToken(self._api, api.post(f"/api/v1/fileTokens", {'fileTokenType': purpose})['data'], self.parent)

    def delete(self):
        assert False, "Have not tested this"
        with self._api as api:
            return api.delete(f"/api/v1/fileTokens", self['id'])


class Token(SSCObject):

    def list(self, **kwargs):
        f"/api/v1/tokens" # GET
        raise NotImplementedError()

    def create(self, **kwargs):
        f"/api/v1/tokens"  # POST
        raise NotImplementedError()

    def update(self):
        f"/api/v1/tokens/{self['id']}"  # PUT
        raise NotImplementedError()

    def delete(self):
        f"/api/v1/tokens/{self['id']}"  # DELETE
        raise NotImplementedError()

    def revoke(self):
        f"/api/v1/tokens/revoke"  # POST with body
        raise NotImplementedError()


class Rulepack(SSCObject):

    def list(self, **kwargs):
        with self._api as api:
            for e in api.page_data(f"/api/v1/coreRulepacks", **kwargs):
                yield Rulepack(self._api, e, self.parent)

    def upload(self, file_path):
        """
        Known return 'code' values:
        * -10000: good -- messages vary
        * -10003: bad -- messages vary

        :param file_path str: The path to the rulepack file to upload
        :return: list(`RulepacksBatchProcessStatus`) - Normally `[{'code': -10000, 'message': 'some message', 'rulepackResourceId': 1234}]`
        """
        assert file_path, "file_path is required"
        assert exists(file_path), "file_path does not exist"

        with self._api as api:
            with open(file_path, 'rb') as f:
                return api._request('post', "/api/v1/coreRulepacks", files={'file': f})['data']

    def delete(self):
        self.assert_is_instance()
        with self._api as api:
            return api.delete(f"/api/v1/coreRulepacks/{self['id']}")

    def update(self):
        with self._api as api:
            for rules in api.page_data(f"/api/v1/updateRulepacks"):
                yield Rulepack(self._api, rules, self.parent)


class CustomTag(SSCObject):
    """ Specifically for project versions """

    def list(self, **kwargs):
        with self._api as api:
            for e in api.page_data(f"/api/v1/projectVersions/{self.parent['id']}/customTags", **kwargs):
                yield CustomTag(self._api, e, self.parent)

    def create(self, **kwargs):
        f"/api/v1/projectVersions/{self.parent['id']}/customTags"
        raise NotImplementedError()

    def update(self):
        f"/api/v1/projectVersions/{self.parent['id']}/customTags/{self['id']}"
        raise NotImplementedError()


class Role(SSCObject):

    def list(self, **kwargs):
        with self._api as api:
            for e in api.page_data(f"/api/v1/roles", **kwargs):
                yield Roles(self._api, e, self.parent)


class AuthEntity(SSCObject):

    def list(self, **kwargs):
        with self._api as api:
            for e in api.page_data(f"/api/v1/authEntities", **kwargs):
                yield AuthEntity(self._api, e, self.parent)

    def get(self, id, **kwargs):
        with self._api as api:
            return api.get(f"/api/v1/authEntities/{id}", **kwargs)['data']

    def find_ldap_user(self, username):
        with self._api as api:
            data = api.get(f"/api/v1/authEntities", q="isLdap:true",
                           embed='roles(name)', entityName=username, orderby='entityName',
                           start=0, limit=-1)['data']
            if len(data) > 0:
                return AuthEntity(self._api, data[0], self.parent)
            return None

    def assign_to_versions(self, versions):
        """
        :rtype boolean: Succeess
        """
        self.assert_is_instance()
        if type(versions) is list or type(versions) is tuple:
            cva = versions
        else:
            cva = [versions]
        with self._api as api:
            return api.post(f"/api/v1/authEntities/{self['id']}/projectVersions/action", {
                "type": "assign",
                "ids": cva
            })['data']['status'] == 'success'


class LocalGroup(SSCObject):
    pass


class User(SSCObject):

    def get(self, username):
        pass


# Stub for methods to be added later
class Roles(SSCObject):
    pass


class LocalUser(SSCObject):
    """
    List local users in Fortify SSC.
    Args: Additional query parameters to filter results
    Yields: LocalUser: Local user object from the endpoint
    """
    def list(self, **kwargs):
        with self._api as api:
            for u in api.page_data("/api/v1/localUsers", **kwargs):
                yield LocalUser(self._api, u, self.parent)
                

class LdapUser(SSCObject):

    def list(self, ldaptype='USER', **kwargs):
        kwargs['ldaptype'] = ldaptype
        with self._api as api:
            for e in api.page_data(f"/api/v1/ldapObjects", **kwargs):
                yield LdapUser(self._api, e, self.parent)

    def add(self, roles=None):
        self.assert_is_instance()
        if roles:
            self['roles'] = roles
        elif 'roles' not in self:
            self['roles'] = [{'id': 'developer'}]
        with self._api as api:
            return LdapUser(self._api, api.post(f"/api/v1/ldapObjects", self)['data'], self)


class Bugtracker(SSCObject):
    pass


class SSCJob(SSCObject):

    def list(self, **kwargs):
        with self._api as api:
            for e in api.page_data("/api/v1/jobs", **kwargs):
                yield SSCJob(self._api, e, self.parent)

    def get(self, jobName, **kwargs):
        with self._api as api:
            return api.get(f"/api/v1/jobs/{jobName}", **kwargs)

    def update(self):
        self.assert_is_instance()
        with self._api as api:
            return api.put(f"/api/v1/jobs/{self['jobName']}", self)

    def list_active_jobs(self):
        """convinence method to list all active jobs"""
        yield from self.list(q='state:RUNNING+or+state:PREPARED', orderby='-createTime')
