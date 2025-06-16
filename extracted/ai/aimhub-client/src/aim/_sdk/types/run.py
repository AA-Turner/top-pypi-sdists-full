import datetime
import json
import inspect
import logging
import pathlib
import os

from functools import partialmethod

from aim import Container, Sequence, Property
from aim._sdk.utils import utc_timestamp
from aim._sdk import type_utils
from aim._core.callbacks import Caller, events
from aim._ext.system_info import utils as system_utils
from aim._sdk.configs import ContainerOpenMode
from aim._sdk.num_utils import is_number

from .logging import (
    LogLine,
    LogStream,
    LogRecord,
    LogRecordSequence
)

from .experiment import Experiment
from .tag import Tag
from .metric import Metric, SystemMetric
from .image import ImageSequence
from .audio import AudioSequence
from .text import TextSequence
from .distribution import DistributionSequence
from .figures import FigureSequence, Figure3DSequence
from .artifact import Artifact

from typing import Optional, Union, List, Tuple, Dict, Any, Type

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from aim import Repo


@type_utils.query_alias('run')
class Run(Container, Caller):
    name = Property(default=lambda x: f'Run #{x.hash}', type_=str)
    description = Property(default='', type_=str)
    archived = Property(default=False, type_=bool)
    experiment = Property(default='default', ref=Experiment, backref='runs')
    active = Property(expr=lambda x: x.end_time is None)
    duration = Property(expr=lambda x: (x.end_time or utc_timestamp()) - x.creation_time)
    notes = Property(default={}, editable=False)
    tags = Property(default=[], ref=Tag, backref='runs', many=True)

    def __init__(self, hash_: Optional[str] = None, *,
                 repo: Optional[Union[str, 'Repo']] = None,
                 mode: Optional[Union[str, ContainerOpenMode]] = ContainerOpenMode.WRITE):
        super().__init__(hash_, repo=repo, mode=mode)

        self._run_artifacts_uri: str = None

    def enable_system_monitoring(self):
        if not self._is_readonly:
            self['__system_params'] = {
                'packages': system_utils.get_installed_packages(),
                'env_variables': system_utils.get_environment_variables(),
                'git_info': system_utils.get_git_info(),
                'executable': system_utils.get_executable(),
                'arguments': system_utils.get_exec_args()
            }

            self.repo.resource_tracker.register(self)
            self.repo.resource_tracker.start()

    @events.on.logs_collected
    def track_terminal_logs(self, log_lines: List[Tuple[str, int]], **kwargs):
        if self._state.get('cleanup'):
            return
        for (line, line_num) in log_lines:
            self.logs.track(LogLine(line), step=line_num + self._prev_logs_end)

    @events.on.system_resource_stats_collected
    def track_system_resources(self, stats: Dict[str, Any], context: Dict, **kwargs):
        if self._state.get('cleanup'):
            return
        for resource_name, usage in stats.items():
            self.sequences.typed_sequence(SystemMetric, resource_name, context).track(usage)

    @property
    def created_at(self) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(self.creation_time, tz=datetime.timezone.utc)

    @property
    def ended_at(self) -> Optional[datetime.datetime]:
        end_time = self.end_time
        if end_time is not None:
            return datetime.datetime.fromtimestamp(end_time, tz=datetime.timezone.utc)
        else:
            return None

    @property
    def logs(self) -> LogStream:
        if getattr(self, '_logs', None) is None:
            self._logs = LogStream(self, name='logs', context={})
            self._prev_logs_end = self._logs.next_step
        return self._logs

    # logging API
    def _log_message(self, level: int, msg: str, **params):
        frame_info = inspect.getframeinfo(inspect.currentframe().f_back)
        logger_info = (frame_info.filename, frame_info.lineno)
        log_record = LogRecord(msg, level, logger_info=logger_info, **params)
        self.track(log_record, name='__log_records')
        block = (level > logging.WARNING)
        self._status_reporter.check_in(flag_name="new_logs", block=block)

    log_error = partialmethod(_log_message, logging.ERROR)
    log_warning = partialmethod(_log_message, logging.WARNING)
    log_info = partialmethod(_log_message, logging.INFO)
    log_debug = partialmethod(_log_message, logging.DEBUG)

    @property
    def log_records(self) -> LogRecordSequence:
        return LogRecordSequence(self, name='__log_records', context={})

    # artifacts logging API
    @property
    def artifacts_uri(self) -> Optional[str]:
        if self._run_artifacts_uri is None:
            base_uri = self._tree.get('artifacts_uri', None)
            if base_uri is None:
                return None
            self._run_artifacts_uri = os.path.join(base_uri, self.hash)
        return self._run_artifacts_uri

    def set_artifacts_uri(self, uri: str):
        self._tree['artifacts_uri'] = uri
        self._run_artifacts_uri = os.path.join(uri, self.hash)

    def log_artifact(self, path: str, name: Optional[str] = None, *, block: bool = False):
        artifact = Artifact(path, uri=self.artifacts_uri, name=name)
        artifact.upload(block=block)
        self._tree.subtree('artifacts')[artifact.name] = artifact

    def log_artifacts(self, path: str, name: Optional[str] = None, *, block: bool = False):
        dir_path = pathlib.Path(path)
        if name is None:
            name = dir_path.name
        for file_path in dir_path.glob('**/*'):
            if file_path.is_file():
                rel_path = file_path.relative_to(dir_path)
                artifact = Artifact(path=str(file_path), uri=self.artifacts_uri, name=f'{name}/{rel_path}')
                artifact.upload(block=block)
                self._tree.subtree('artifacts')[artifact.name] = artifact

    @property
    def artifacts(self) -> Dict[str, Artifact]:
        return self._tree.get('artifacts', {})

    def track(self, value, name: Optional[str] = None, step: Optional[int] = None, context: Optional[dict] = None, **axis):
        axis['timestamp'] = utc_timestamp()
        context = {} if context is None else context
        if isinstance(value, dict):
            if name is not None:
                raise ValueError('\'name\' argument should not be specified when Calling Run.track() with dict input.')
            for name, value in value.items():
                seq_type = self._get_sequence_type_from_value(value)
                sequence = self.sequences.typed_sequence(seq_type, name, context)
                sequence.track(value, step=step, **axis)
        else:
            if name is None:
                raise ValueError('Calling Run.track() with single value requires \'name\' argument to be specified.')
            seq_type = self._get_sequence_type_from_value(value)
            sequence = self.sequences.typed_sequence(seq_type, name, context)
            sequence.track(value, step=step, **axis)

    def get_metric(self, name: str, context: Optional[dict] = None) -> Metric:
        context = {} if context is None else context
        return self.sequences.typed_sequence(Metric, name, context)

    def get_system_metric(self, name: str, context: Optional[dict] = None) -> SystemMetric:
        context = {} if context is None else context
        return self.sequences.typed_sequence(SystemMetric, name, context)

    def get_text_sequence(self, name: str, context: Optional[dict] = None) -> TextSequence:
        context = {} if context is None else context
        return self.sequences.typed_sequence(TextSequence, name, context)

    def get_image_sequence(self, name: str, context: Optional[dict] = None) -> ImageSequence:
        context = {} if context is None else context
        return self.sequences.typed_sequence(ImageSequence, name, context)

    def get_audio_sequence(self, name: str, context: Optional[dict] = None) -> AudioSequence:
        context = {} if context is None else context
        return self.sequences.typed_sequence(AudioSequence, name, context)

    def get_distribution_sequence(self, name: str, context: Optional[dict] = None) -> DistributionSequence:
        context = {} if context is None else context
        return self.sequences.typed_sequence(DistributionSequence, name, context)

    def get_figure_sequence(self, name: str, context: Optional[dict] = None) -> FigureSequence:
        context = {} if context is None else context
        return self.sequences.typed_sequence(FigureSequence, name, context)

    def get_figure3d_sequence(self, name: str, context: Optional[dict] = None) -> Figure3DSequence:
        context = {} if context is None else context
        return self.sequences.typed_sequence(Figure3DSequence, name, context)

    def dataframe(
        self,
        include_props: bool = True,
        include_params: bool = True,
    ):
        data = {
            'hash': self.hash,
        }

        if include_props:
            data.update(self.collect_properties())

        if include_params:
            from aim._core.storage import treeutils
            for path, val in treeutils.unfold_tree(self[...],
                                                   unfold_array=False,
                                                   depth=3):
                s = ''
                for key in path:
                    if isinstance(key, str):
                        s += f'.{key}' if len(s) else f'{key}'
                    else:
                        s += f'[{key}]'

                if isinstance(val, (tuple, list, dict)):
                    val = json.dumps(val)
                if s not in data.keys():
                    data[s] = val

        import pandas as pd
        df = pd.DataFrame(data, index=[0])
        return df

    @staticmethod
    def _get_sequence_type_from_value(value) -> Type[Sequence]:
        val_type = type_utils.get_object_typename(value)
        if type_utils.is_allowed_type(val_type, type_utils.get_sequence_value_types(Metric)) \
                or is_number(value):
            return Metric
        if type_utils.is_allowed_type(val_type, type_utils.get_sequence_value_types(ImageSequence)):
            return ImageSequence
        if type_utils.is_allowed_type(val_type, type_utils.get_sequence_value_types(AudioSequence)):
            return AudioSequence
        if type_utils.is_allowed_type(val_type, type_utils.get_sequence_value_types(TextSequence)):
            return TextSequence
        if type_utils.is_allowed_type(val_type, type_utils.get_sequence_value_types(DistributionSequence)):
            return DistributionSequence
        if type_utils.is_allowed_type(val_type, type_utils.get_sequence_value_types(FigureSequence)):
            return FigureSequence
        if type_utils.is_allowed_type(val_type, type_utils.get_sequence_value_types(Figure3DSequence)):
            return Figure3DSequence
        return Sequence
