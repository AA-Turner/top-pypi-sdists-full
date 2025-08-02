from datetime import datetime, timezone
from typing import Optional

from _qwak_proto.qwak.feature_store.features.feature_set_pb2 import FeatureSet
from _qwak_proto.qwak.feature_store.features.feature_set_service_pb2 import (
    GetFeatureSetByNameResponse,
)
from croniter import croniter
from qwak.clients.feature_store import FeatureRegistryClient
from qwak.feature_store.execution.backfill import Backfill
from qwak.feature_store.feature_sets.batch import BatchFeatureSet

from qwak_sdk.inner.tools.cli_tools import ask_yesno
from qwak_sdk.tools.colors import Color


class _BackfillLogic:
    featureset: FeatureSet
    batch_featureset: BatchFeatureSet

    def configure_window_backfill(
        self,
        featureset_name: str,
        start_time: Optional[datetime] = None,
        stop_time: Optional[datetime] = None,
        comment: str = None,
        cluster_template: str = None,
    ) -> Optional[Backfill]:
        """
        Configures a window back-fill object. This type of backfill will not reset the entire featureset, but will be
        performed from the requested start time to the requested stop time in ticks calculated according to the
        feature sets scheduling policy.
        @param featureset_name: feature set name to perform the backfill job for
        @type featureset_name: str
        @param start_time: backfill requested start date
        @type start_time: optional[datetime]
        @param stop_time:
        @type stop_time: optional[datetime]
        @param comment:
        @type comment: str
        @param cluster_template:
        @type cluster_template: str
        @return:
        @rtype:
        """
        print(
            f"{Color.BLUE} Backfilling from {start_time} to {stop_time}, "
            f"the following ticks are going to be performed {Color.END}"
        )
        zipped_tick_strs = Backfill.generate_expected_ticks_repr(
            scheduling_policy=self.batch_featureset.scheduling_policy,
            start_time=start_time,
            stop_time=stop_time,
        )
        print("\n".join(zipped_tick_strs))
        if ask_yesno("", force=False):
            backfill_execution = Backfill(
                featureset_name=featureset_name,
                comment=comment,
                cluster_template=cluster_template,
                start_time=start_time,
                stop_time=stop_time,
            )
            return backfill_execution
        return None

    @staticmethod
    def _get_featureset_by_name(featureset_name: str) -> GetFeatureSetByNameResponse:
        registry_client = FeatureRegistryClient()

        return registry_client.get_feature_set_by_name(feature_set_name=featureset_name)

    def get_start_stop_times(
        self,
        requested_start_time: Optional[datetime] = None,
        requested_stop_time: Optional[datetime] = None,
    ) -> tuple:
        start_time: datetime = (
            requested_start_time or self.batch_featureset.backfill.start_date
        ).replace(tzinfo=timezone.utc)
        stop_time: datetime

        if start_time and start_time > datetime.now().replace(tzinfo=timezone.utc):
            stop_time = datetime.utcnow().replace(tzinfo=timezone.utc)
        else:
            stop_time = (
                requested_stop_time or datetime.utcnow().replace(tzinfo=timezone.utc)
            ).replace(tzinfo=timezone.utc)

        return start_time, stop_time

    def is_valid_input(
        self,
        reset_backfill: bool,
        start_time: Optional[datetime],
        stop_time: Optional[datetime],
        featureset_name: str,
    ) -> bool:
        # Validate reset_backfill or start and stop times
        if (not reset_backfill and not start_time and not stop_time) or (
            reset_backfill and (start_time or stop_time)
        ):
            print(
                f"{Color.RED} please specify either --reset-backfill or one or more of --start-time/--stop-time"
            )
            return False

        # Validate featureset exists
        get_featureset_resp = self._get_featureset_by_name(
            featureset_name=featureset_name
        )
        if not get_featureset_resp or not get_featureset_resp.feature_set:
            print(f"{Color.RED} Failed to retrieve featureset {featureset_name}")
            return False

        self.featureset = get_featureset_resp.feature_set
        fs_type_attr: str = self.featureset.feature_set_definition.feature_set_spec.feature_set_type.WhichOneof(
            "set_type"
        )
        # Validate featureset is batch v1
        if fs_type_attr != "batch_feature_set_v1":
            print(
                f"{Color.RED} Feature set {featureset_name} is of type {fs_type_attr}. Only BatchV1 is supported."
            )
            return False

        self.batch_featureset = BatchFeatureSet._from_proto(
            self.featureset.feature_set_definition.feature_set_spec
        )

        # Validate scheduling policy
        if not self.batch_featureset.scheduling_policy or not croniter.is_valid(
            self.batch_featureset.scheduling_policy
        ):
            print(
                f"{Color.RED} Feature set {featureset_name} has an invalid scheduling policy {self.batch_featureset.scheduling_policy}."
            )
            return False

        return True
