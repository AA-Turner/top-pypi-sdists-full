from dataclasses import dataclass, asdict
from enum import Enum
from typing import List, Optional, Dict

from acceldata_sdk.models.job import CreateJob
from acceldata_sdk.models.span import Span
from acceldata_sdk.models.span_context import SpanContext
from acceldata_sdk.utils.datetime_utils import DateTimeFormatter
from datetime import datetime
import logging

logger = logging.getLogger('pipeline')
logger.setLevel(logging.INFO)


@dataclass
class Tag:

    def __init__(self, id, name, displayName, *args, **kwargs):
        self.id = id
        self.name = name
        self.displayName = displayName
    id = None
    name = None
    displayName = None
    createdAt = None
    updatedAt = None


@dataclass
class PipelineMetadata:
    """
    Description:
        Pipeline metadata.

    :param owner : (String) owner of the pipeline
    :param team: (String) team of the owner
    :param codeLocation: (String) location of the code
    """
    owner: str = None
    team: str = None
    codeLocation: str = None

class PipelineSourceType(Enum):
    AIRFLOW='AIRFLOW',
    AZURE_DATA_FACTORY='AZURE_DATA_FACTORY',
    OTHERS='OTHERS'

    def to_dict(self):
        return self.name

class CreatePipeline:
    # createdAt = None
    # enabled = None
    # id = None
    # interrupt = None
    # notificationChannels = None
    # schedule = None
    # scheduled = None
    # schedulerType = None
    # updatedAt = None

    def __init__(self, uid: str, name: str,
                 description: str = None, meta: PipelineMetadata = None, createdAt: datetime = None,
                 updatedAt=None, sourceType=None, **context):
        """
        Description:
            Class used for create pipeline in torch catalog
        :param uid: uid of the pipeline
        :param name: name of the pipeline
        :param description: (Optional)description of the pipeline
        :param meta: (PipelineMetadata) meta data of the pipeline
        :param createdAt: (Optional) creation time of the pipeline. If not set, the current time will be used
        :param updatedAt: (Optional) update time of the pipeline. If not set, the current time will be used
        :param context: context map of the pipeline
        """
        self.uid = uid
        self.name = name
        self.description = description
        self.context = context
        if meta is not None:
            self.meta = PipelineMetadata(owner=meta.owner, team=meta.team, codeLocation=meta.codeLocation)
        else:
            self.meta = None
        self.createdAt = DateTimeFormatter.format_datetime(createdAt)
        self.updatedAt = DateTimeFormatter.format_datetime(updatedAt)
        if sourceType is not None:
            self.sourceType = sourceType
        else:
            self.sourceType = None


    def __eq__(self, other):
        return self.uid == other.uid

    def __repr__(self):
        return f"Pipeline({self.uid!r})"

    def add_context(self, key: str, value: str):
        """
        Used to add context in context map
        :param key: key of the context
        :param value: value of the context
        :return: context dir
        """
        self.context[key] = value
        return self.context

class PipelineRunStatus(Enum):
    """
        pipeline run status
    """
    STARTED = 1
    COMPLETED = 2
    FAILED = 3
    ABORTED = 4


class PipelineRunResult(Enum):
    """
        Pipeline run result
    """
    RUNNING = 'RUNNING'
    SUCCESS = 'SUCCESS'
    FAILURE = 'FAILURE'
    CANCELLED = 'CANCELLED'


class NodeType(Enum):
    """
        Pipeline Node Type
    """
    ASSET = 'ASSET'
    FUNCTIONAL = 'FUNCTIONAL'


class NodeAddition(Enum):
    """
        Pipeline Node Addition
    """
    PIPELINE_CREATION = 'PIPELINE_CREATION'
    MANUAL_ADDITION = 'MANUAL_ADDITION'
    QUERY_LOG_ANALYSIS = 'QUERY_LOG_ANALYSIS'


class NodeStatus(Enum):
    """
        Pipeline Node Status
    """
    ACTIVE = 'ACTIVE'
    STALE = 'STALE'
    DELETED = 'DELETED'


class PipelineRun:

    def __init__(self, pipelineId, versionId=None, status=PipelineRunStatus.STARTED, id=None, startedAt: datetime = None,
                 finishedAt: datetime = None, result=None, client=None, args=None,
                 continuationId=None, successEvents=None, errorEvents=None, warningEvents=None, avgExecutionTime=None,
                 *argumentss, **kwargs):
        """
        Description:
                Pipeline run used for instantiate run of the pipeline. To create new pipeline run you need to pass pipelineId, version.
        :param pipelineId: pipleline id
        :param versionId:  pipeline run current version
        :param status: status of the pipeline run
        :param id: pipeline run id
        :param startedAt: An optional parameter used to define the starting time of the pipeline run. If this parameter is not provided, the pipeline will commence at the time of its creation by default.
        :param finishedAt: An optional parameter used to specify the completion time of the pipeline run. If this parameter is not provided, it will be automatically set to the time when the pipeline run is finished.
        :param args: additional args for pipeline run
        :param result: pipeline run result
        """
        self.pipelineId = pipelineId
        self.versionId = versionId
        self.status = status
        self.args = args
        self.result = result
        if continuationId is not None:
            self.continuationId = continuationId
        if successEvents is not None:
            self.successEvents = successEvents
        if errorEvents is not None:
            self.errorEvents = errorEvents
        if warningEvents is not None:
            self.warningEvents = warningEvents
        if avgExecutionTime is not None:
            self.avgExecutionTime = avgExecutionTime
        self.startedAt = startedAt
        self.finishedAt = finishedAt

        if id is not None:
            self.id = id
            self.client = client

    def __eq__(self, other):
        return self.id == other.id

    def __repr__(self):
        return f"PipelineRun({self.__dict__})"

    # convert job object to dict type
    def _convert_job_to_dict(self, job: CreateJob):
        """
        Description:
            Convert createJob class instance to dict type
        :param job: createJob class instance
        :return: dict form of createJob class instance
        """
        job_dict = job.__dict__
        if hasattr(job, 'meta'):
            meta = asdict(job.meta)
            job_dict['meta'] = meta
        input_dict = []
        for ds_in in job.inputs:
            input_dict.append(asdict(ds_in, dict_factory=lambda x: {k: v for (k, v) in x if v is not None}))
        output_dict = []
        for ds_out in job.outputs:
            output_dict.append(asdict(ds_out, dict_factory=lambda x: {k: v for (k, v) in x if v is not None}))
        job_dict['inputs'] = input_dict
        job_dict['outputs'] = output_dict
        job_dict['version'] = self.versionId
        return job_dict

    # create job for pipeline run
    def create_job(self, job: CreateJob):
        """
        Description:
            used to create job for any pipeline run
        :return: Job class instance of created job        """
        if job.uid is None or job.name is None:
            raise Exception('To create a job job uid and name are required')
        payload = self._convert_job_to_dict(job)
        res = self.client.create_job(payload, self.pipelineId)
        if job.bounded_by_span:
            if job.span_uid is not None:
                associated_job_uids = [job.uid]
                span_uid_temp = job.span_uid
                # Get root span to create child span under
                parent_span_context = self.get_root_span()
                if parent_span_context is not None:
                    # Create child span under root span
                    span_context = parent_span_context.create_child_span(
                        uid=span_uid_temp,
                        associatedJobUids=associated_job_uids,
                        with_explicit_time=job.with_explicit_time
                    )
                else:
                    # Create root span under pipeline_run as root span doesn't exist
                    self.create_span(
                        uid=span_uid_temp,
                        associatedJobUids=associated_job_uids,
                        with_explicit_time=job.with_explicit_time
                    )
            else:
                raise Exception('To create a span span_uid is required')
        return res

    # convert pipeline run to dict type
    def _convert_pipeline_run_to_dict(self, pipeline_run=None):
        """
            Description:
                Convert PipelineRun class instance to dict type
            :param pipeline_run: PipelineRun class instance
            :return: dict form of PipelineRun class instance
        """
        payload = pipeline_run.__dict__
        payload['status'] = pipeline_run.status.name
        if pipeline_run.result is not None:
            payload['result'] = pipeline_run.result.name
        else:
            del payload['result']
        pipeline_run_payload = {'run': payload}
        return pipeline_run_payload

    # update run for a pipeline
    def update_pipeline_run(self, result: PipelineRunResult,
                            status: PipelineRunStatus = PipelineRunStatus.STARTED,
                            context_data: {} = None, finishedAt: datetime = None):
        """
        Description:
            used to update an existing pipeline run
        :return: updated pipelineRun class instance
        """
        if finishedAt is not None:
            finishedAt = finishedAt.isoformat()

        update_pipeline_run = PipelineRun(
            pipelineId=self.pipelineId,
            versionId=self.versionId,
            result=result,
            args=context_data,
            status=status,
            finishedAt = finishedAt
        )
        payload = self._convert_pipeline_run_to_dict(update_pipeline_run)
        res = self.client.update_pipeline_run(self.id, payload)
        return res

    # convert span to dict
    def _convert_span_to_dict(self, span: Span, associatedJobUids):
        """
            Description:
                Convert Span class instance to dict type
            :param span: Span class instance
            :return: dict form of Span class instance
        """
        payload = span.__dict__
        payload['status'] = span.status.name
        span_payload = {'span': payload, 'associatedJobUids' : associatedJobUids }
        return span_payload

    # create span for pipeline run
    def create_span(self, uid: str, context_data: dict = None, associatedJobUids = None, createdAt: datetime = None, with_explicit_time: bool = False):
        """
        Description:
            used to create span for any pipeline run
        :param associatedJobUids: list of string (job uids)
        :param context_data
        :param uid: span uid
        :param with_explicit_time: A boolean flag that determines how the span should be started.
        - If set to True, you can specify the start time for the span in subsequent span events.
        - If set to False, the span will be automatically started with the current time at the moment of creation.
        :return: SpanContext of the span
        """
        if uid is None:
            raise Exception('Span uid can not be None. You need to pass span uid to create span')
        create_span = Span(
            uid=uid,
            pipelineRunId=self.id,
            createdAt=createdAt
        )
        if associatedJobUids is None:
            associatedJobUids = []
        elif not isinstance(associatedJobUids, list):
            raise Exception('associatedJobUids should be a list')

        payload = self._convert_span_to_dict(create_span, associatedJobUids)
        logger.debug("create_span method invoked with_explicit_time: ", with_explicit_time)
        res = self.client.create_span(self.id, payload)
        span_context = SpanContext(client=self.client, span=res, context_data=context_data, new_span=True,
                                   with_explicit_time=with_explicit_time)
        return span_context

    def get_span(self, span_uid: str):
        """
            Description:
                Get span of the pipeline run by uid
        :param span_uid: uid of the span
        :return: SpanContext instance of the input span uid
        """
        span = self.client.get_span(pipeline_run_id= self.id, uid=span_uid)
        span_context = SpanContext(client=self.client, span= span)
        return span_context

    def get_root_span(self):
        """
            Description:
                Get root span of the pipeline run
        :return: SpanContext instance of the root span
        """
        span_context = None
        span = self.client.get_root_span( pipeline_run_id=self.id)
        if span is not None:
            span_context = SpanContext(client=self.client, span=span)
        return span_context

    def get_details(self):
        """
            Description:
                Get root span of the pipeline run
        :return: SpanContext instance of the root span
        """
        response = self.client.get_run_details(pipeline_id=self.pipelineId, version_id=self.versionId)
        return response

    def get_spans(self):
        """
            Description:
                Get span of the pipeline run
        :return: SpanContext instance of the input span uid
        """
        spans = self.client.get_spans(pipeline_run_id=self.id)
        span_context_list = []
        for res in spans:
            span_context_list.append(SpanContext(client=self.client, span=res))
        return span_context_list


@dataclass
class Node:
    id = None
    type: NodeType = None
    assetId = None
    pipelineId = None
    name = None
    description = None
    context = None
    meta: PipelineMetadata = None
    versionId = None
    uid = None
    createdVia: NodeAddition = NodeAddition.PIPELINE_CREATION
    status: NodeStatus = NodeStatus.ACTIVE
    parentId = None

    def __init__(self,
                 id = None,
                 type: NodeType = None,
                 assetId = None,
                 pipelineId = None,
                 name = None,
                 description = None,
                 context = None,
                 meta: PipelineMetadata = None,
                 versionId = None,
                 uid = None,
                 createdVia: NodeAddition = NodeAddition.PIPELINE_CREATION,
                 status: NodeStatus = NodeStatus.ACTIVE,
                 parentId = None, *args, **kwargs
                 ):
        self.id = id
        self.type = type
        self.assetId = assetId
        self.pipelineId = pipelineId
        self.name = name
        self.description = description
        self.context = context
        if isinstance(meta, dict):
            self.meta = PipelineMetadata(**meta)
        else:
            self.meta = meta
        self.versionId = versionId
        self.uid = uid
        self.createdVia = createdVia
        self.status = status
        self.parentId = parentId

    def __repr__(self):
        return f"Node({self.__dict__})"


@dataclass 
class Edge:
    id = None
    fromId = None
    toId = None
    fromAssetType: NodeType = None
    toAssetType: NodeType = None
    versionId = None

    def __init__(self,
                 id = None,
                 fromId = None,
                 toId = None,
                 fromAssetType: NodeType = None,
                 toAssetType: NodeType = None,
                 versionId = None, *args, **kwargs
                 ):
        self.id = id
        self.fromId = fromId
        self.toId = toId
        self.fromAssetType = fromAssetType
        self.toAssetType = toAssetType
        self.versionId = versionId

    def __repr__(self):
        return f"Edge({self.__dict__})"


class Pipeline:
    def __init__(self, uid: str,
                 name: str,
                 description: str = None,
                 meta: PipelineMetadata = None,
                 createdAt: str = None,
                 enabled: bool = None,
                 id: int = None,
                 interrupt: bool = None,
                 notificationChannels=None,
                 schedule: str = None,
                 scheduled: bool = None,
                 schedulerType: str = None,
                 updatedAt=None,
                 context=None,
                 client=None,
                 tags=None,
                 *args, **kwargs):
        """
        Description:
            Class of the pipeline
        :param uid: uid of the pipeline
        :param name: name of the pipeline
        :param description: pipeline desc
        :param meta: (PipelineMetadata)metadata of the pipeline
        :param createdAt: creation time of pipeline
        :param enabled: True if pipeline is interrupted else false
        :param id: pipeline id
        :param updatedAt: updated time of the given pipeline
        :param context: context data for the pipeline (dir)
        :param kwrgs:
        """
        self.uid = uid
        self.name = name
        self.createdAt = createdAt
        self.enabled = enabled
        self.interrupt = interrupt
        self.notificationChannels = notificationChannels
        self.schedule = schedule
        self.scheduled = scheduled
        self.schedulerType = schedulerType
        self.id = id
        self.updatedAt = updatedAt
        self.description = description
        self.context = context
        if isinstance(meta, dict):
            self.meta = PipelineMetadata(**meta)
        else:
            self.meta = meta

        self.tags = list()
        if tags is not None:
            for obj in tags:
                if isinstance(obj, dict):
                    self.tags.append(Tag(**obj))
                else:
                    self.tags.append(obj)
        self.client = client

    def __repr__(self):
        return f"Pipeline({self.__dict__})"

    def __eq__(self, other):
        return self.uid == other.uid

    # convert job object to dict type
    def _convert_job_to_dict(self, job: CreateJob):
        """
        Description:
            Convert createJob class instance to dict type
        :param job: createJob class instance
        :return: dict form of createJob class instance
        """
        job_dict = job.__dict__
        if hasattr(job, 'meta'):
            meta = asdict(job.meta)
            job_dict['meta'] = meta
        input_dict = []
        for ds_in in job.inputs:
            input_dict.append(asdict(ds_in, dict_factory=lambda x: {k: v for (k, v) in x if v is not None}))
        output_dict = []
        for ds_out in job.outputs:
            output_dict.append(asdict(ds_out, dict_factory=lambda x: {k: v for (k, v) in x if v is not None}))
        job_dict['inputs'] = input_dict
        job_dict['outputs'] = output_dict
        pipeline_run = self.client.get_pipeline_run(job.pipeline_run_id)
        job_dict['version'] = pipeline_run.versionId
        return job_dict

    # to create job for any given pipeline
    def create_job(self, job: CreateJob):
        """
        Description:
            Used to create job and span in a pipeline
        :param job: createJob class instance that you want to add in pipeline
        :return: Job class instance of created job
        """
        if job.uid is None or job.name is None or job.pipeline_run_id is None:
            raise Exception('To create a job job uid, name and pipeline_run_id is required')

        payload = self._convert_job_to_dict(job)
        res = self.client.create_job(payload, self.id)
        if job.bounded_by_span:
            if job.pipeline_run_id is not None and job.span_uid is not None:
                associated_job_uids = [job.uid]
                span_uid_temp = job.span_uid
                # Get root span to create child span under
                pipeline_run = self.get_run(job.pipeline_run_id)
                parent_span_context = pipeline_run.get_root_span()
                if parent_span_context is not None:
                    # Create child span under root span
                    span_context = parent_span_context.create_child_span(
                        uid=span_uid_temp,
                        associatedJobUids=associated_job_uids,
                        with_explicit_time=job.with_explicit_time
                    )
                else:
                    # Create root span under pipeline_run as root span doesn't exist
                    pipeline_run.create_span(
                        uid=span_uid_temp,
                        associatedJobUids=associated_job_uids,
                        with_explicit_time=job.with_explicit_time
                    )
            else:
                raise Exception('To create a span span_uid and pipeline_run_id are required')
        return res

    # to delete pipeline
    def delete(self):
        """
        Description:
            Used to delete a pipeline
        """
        res = self.client.delete_pipeline(self.id)
        return res

    # convert pipeline run to dict type
    def _convert_pipeline_run_to_dict(self, pipeline_run: PipelineRun):
        """
            Description:
                Convert PipelineRun class instance to dict type
            :param pipeline_run: PipelineRun class instance
            :return: dict form of PipelineRun class instance
        """
        payload = pipeline_run.__dict__
        payload['status'] = pipeline_run.status.name
        if pipeline_run.result is not None:
            payload['result'] = pipeline_run.result.name
        else:
            del payload['result']
        pipeline_run_payload = {'run': payload}
        return pipeline_run_payload

    # create run for a pipeline
    def create_pipeline_run(self, context_data: {} = None, continuation_id: str = None,
                            startedAt: datetime = None) -> PipelineRun:
        """
        Description:
            used to create a pipeline run
        :param context_data: pipeline run argument
        :param continuation_id: continuation_id of pipeline run. Default value is None
        :return: pipelineRun class instance
        """
        if startedAt is not None:
            startedAt = DateTimeFormatter.format_datetime(startedAt)
            create_pipeline_run = PipelineRun(
                pipelineId=self.id,
                args=context_data,
                continuationId=continuation_id,
                startedAt=startedAt
            )
        else:
            create_pipeline_run = PipelineRun(
                pipelineId=self.id,
                args=context_data,
                continuationId=continuation_id
            )
        payload = self._convert_pipeline_run_to_dict(create_pipeline_run)
        res = self.client.create_pipeline_run(payload)
        return res

    def get_latest_pipeline_run(self) -> PipelineRun:
        return self.client.get_latest_pipeline_run(pipeline_id=self.id)

    def get_run(self, pipeline_run_id=None, continuation_id=None) -> PipelineRun:
        return self.client.get_pipeline_run(
            pipeline_run_id=pipeline_run_id,
            continuation_id=continuation_id,
            pipeline_id=self.id
        )

    def get_runs(self) -> List[PipelineRun]:
        return self.client.get_pipeline_runs(pipeline_id=self.id)


from typing import List, Optional, Dict, Any


class PipelineListingInfo:
    def __init__(
            self,
            assetNodesCount: int,
            functionalNodesCount: int,
            latestRunFinishedAt: Optional[str],
            latestRunId: Optional[int],
            latestRunResult: Optional[str],
            latestRunStartedAt: Optional[str],
            latestRunVersionId: Optional[int],
            pipelineSummary: 'PipelineSummary',
            successfulPoliciesCount: int,
            totalPoliciesCount: int,
            totalRunsCount: int,
            *args, **kwargs
    ):
        self.assetNodesCount = assetNodesCount
        self.functionalNodesCount = functionalNodesCount
        self.latestRunFinishedAt = latestRunFinishedAt
        self.latestRunId = latestRunId
        self.latestRunResult = latestRunResult
        self.latestRunStartedAt = latestRunStartedAt
        self.latestRunVersionId = latestRunVersionId
        self.pipelineSummary = pipelineSummary
        self.successfulPoliciesCount = successfulPoliciesCount
        self.totalPoliciesCount = totalPoliciesCount
        self.totalRunsCount = totalRunsCount

    def __repr__(self):
        return (
            f"PipelineListingInfo("
            f"pipelineSummary={self.pipelineSummary.name}, "
            f"assetNodesCount={self.assetNodesCount}, "
            f"functionalNodesCount={self.functionalNodesCount}, "
            f"latestRunResult={self.latestRunResult}, "
            f"totalRunsCount={self.totalRunsCount})"
        )


class PipelineSummary:
    def __init__(self, id: int, name: str, meta: 'PipelineSummaryMeta', *args, **kwargs):
        self.id = id
        self.name = name
        self.meta = meta

    def __repr__(self):
        return f"PipelineSummary(id={self.id}, name={self.name}, meta={self.meta})"


class PipelineSummaryMeta:
    def __init__(self, codeLocation: str, owner: str, team: str):
        self.codeLocation = codeLocation
        self.owner = owner
        self.team = team

    def __repr__(self):
        return (
            f"PipelineSummaryMeta(codeLocation={self.codeLocation}, "
            f"owner={self.owner}, team={self.team})"
        )


class PipelineDetails:
    pipeline: Pipeline = None
    nodes: List[Node] = list()
    edges: List[Edge] = list()

    def __init__(self, pipeline=None, nodes=None, edges=None, *args, **kwargs):
        if isinstance(pipeline, dict):
            self.pipeline = Pipeline(**pipeline)
        else:
            self.pipeline = pipeline
        self.nodes = list()
        if nodes is not None:
            for obj in nodes:
                if isinstance(obj, dict):
                    self.nodes.append(Node(**obj))
                else:
                    self.nodes.append(obj)
        self.edges = list()
        if edges is not None:
            for obj in edges:
                if isinstance(obj, dict):
                    self.edges.append(Edge(**obj))
                else:
                    self.edges.append(obj)

    def __repr__(self):
        return f"PipelineDetails({self.__dict__})"
