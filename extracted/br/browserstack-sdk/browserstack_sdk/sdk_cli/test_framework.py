# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack111l11l_opy_ = 2048
bstack11l_opy_ = 7
def bstack1l1llll_opy_ (bstack11ll1l1_opy_):
    global bstack111111l_opy_
    bstack111lll_opy_ = ord (bstack11ll1l1_opy_ [-1])
    bstack11llll_opy_ = bstack11ll1l1_opy_ [:-1]
    bstack1l11_opy_ = bstack111lll_opy_ % len (bstack11llll_opy_)
    bstackl_opy_ = bstack11llll_opy_ [:bstack1l11_opy_] + bstack11llll_opy_ [bstack1l11_opy_:]
    if bstack1lll_opy_:
        bstack11l111_opy_ = unicode () .join ([unichr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    else:
        bstack11l111_opy_ = str () .join ([chr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    return eval (bstack11l111_opy_)
import logging
from enum import Enum
import os
import threading
import traceback
from typing import Dict, List, Any, Callable, Tuple, Union
import abc
from datetime import datetime, timezone
from dataclasses import dataclass
from browserstack_sdk.sdk_cli.async_dispatcher import AsyncDispatcher
from browserstack_sdk.sdk_cli.tracked_instance import TrackedInstance, bstack1l11ll1l1l1_opy_
class TestHookState(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack1l1llll_opy_ (u"ࠣࡖࡨࡷࡹࡎ࡯ࡰ࡭ࡖࡸࡦࡺࡥ࠯ࡽࢀࠦᷝ").format(self.name)
class TestFrameworkState(Enum):
    NONE = 0
    BEFORE_ALL = 1
    LOG = 2
    SETUP_FIXTURE = 3
    INIT_TEST = 4
    BEFORE_EACH = 5
    AFTER_EACH = 6
    TEST = 7
    STEP = 8
    LOG_REPORT = 9
    AFTER_ALL = 10
    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        return NotImplemented
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented
    def __repr__(self) -> str:
        return bstack1l1llll_opy_ (u"ࠤࡗࡩࡸࡺࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࡕࡷࡥࡹ࡫࠮ࡼࡿࠥᷞ").format(self.name)
class TestFrameworkTest(TrackedInstance):
    test_frameworks: List[str]
    test_framework_versions: Dict[str, str]
    state: TestFrameworkState
    bstack1l11ll11ll1_opy_: datetime
    bstack1l11ll1111l_opy_: datetime
    def __init__(
        self,
        context: bstack1l11ll1l1l1_opy_,
        test_frameworks: List[str],
        test_framework_versions: Dict[str, str],
        state=TestFrameworkState.NONE,
    ):
        super().__init__(context)
        self.test_frameworks = test_frameworks
        self.test_framework_versions = test_framework_versions
        self.state = state
        self.bstack1l11ll11ll1_opy_ = datetime.now(tz=timezone.utc)
        self.bstack1l11ll1111l_opy_ = datetime.now(tz=timezone.utc)
    def set_state(self, bstack1l11l1llll1_opy_: TestFrameworkState):
        bstack1l11ll11111_opy_ = TestFrameworkState(bstack1l11l1llll1_opy_).name
        if not bstack1l11ll11111_opy_:
            return False
        if bstack1l11l1llll1_opy_ == self.state:
            return False
        self.state = bstack1l11l1llll1_opy_
        self.bstack1l11ll1111l_opy_ = datetime.now(tz=timezone.utc)
        return True
@dataclass
class TestFrameworkContext:
    test_framework_name: str
    test_framework_version: str
    platform_index: int
@dataclass
class LogEntry:
    kind: str
    message: str
    level: Union[None, str] = None
    timestamp: Union[None, datetime] = datetime.now(tz=timezone.utc)
    fileName: str = None
    fileSize: int = None
    attachmentType: str = None
    filePath: str = None
    test_run_uuid: str = None
    build_run_uuid: str = None
    hook_run_uuid: str = None
class TestFramework(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    KEY_TEST_UUID = bstack1l1llll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡷࡸ࡭ࡩࠨᷟ")
    KEY_TEST_ID = bstack1l1llll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡬ࡨࠧᷠ")
    KEY_TEST_NAME = bstack1l1llll_opy_ (u"ࠧࡺࡥࡴࡶࡢࡲࡦࡳࡥࠣᷡ")
    KEY_TEST_FILE_PATH = bstack1l1llll_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫࡯࡬ࡦࡡࡳࡥࡹ࡮ࠢᷢ")
    KEY_TEST_TAGS = bstack1l1llll_opy_ (u"ࠢࡵࡧࡶࡸࡤࡺࡡࡨࡵࠥᷣ")
    KEY_TEST_RESULT = bstack1l1llll_opy_ (u"ࠣࡶࡨࡷࡹࡥࡲࡦࡵࡸࡰࡹࠨᷤ")
    KEY_TEST_RESULT_AT = bstack1l1llll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡳࡧࡶࡹࡱࡺ࡟ࡢࡶࠥᷥ")
    KEY_TEST_STARTED_AT = bstack1l1llll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠧᷦ")
    KEY_TEST_ENDED_AT = bstack1l1llll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡨࡲࡩ࡫ࡤࡠࡣࡷࠦᷧ")
    KEY_TEST_LOCATION = bstack1l1llll_opy_ (u"ࠧࡺࡥࡴࡶࡢࡰࡴࡩࡡࡵ࡫ࡲࡲࠧᷨ")
    KEY_TEST_FRAMEWORK_NAME = bstack1l1llll_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࠧᷩ")
    KEY_TEST_FRAMEWORK_VERSION = bstack1l1llll_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠤᷪ")
    bstack111l1l1l1ll_opy_ = bstack1l1llll_opy_ (u"ࠣࡶࡨࡷࡹࡥࡣࡰࡦࡨࠦᷫ")
    KEY_TEST_RERUN_NAME = bstack1l1llll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡳࡧࡵࡹࡳࡥ࡮ࡢ࡯ࡨࠦᷬ")
    KEY_PLATFORM_INDEX = bstack1l1llll_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡤ࡯࡮ࡥࡧࡻࠦᷭ")
    KEY_TEST_FAILURE = bstack1l1llll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩࡥ࡮ࡲࡵࡳࡧࠥᷮ")
    KEY_TEST_FAILURE_TYPE = bstack1l1llll_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠤᷯ")
    KEY_TEST_LOGS = bstack1l1llll_opy_ (u"ࠨࡴࡦࡵࡷࡣࡱࡵࡧࡴࠤᷰ")
    KEY_TEST_META = bstack1l1llll_opy_ (u"ࠢࡵࡧࡶࡸࡤࡳࡥࡵࡣࠥᷱ")
    KEY_TEST_SCOPES = bstack1l1llll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡳࡤࡱࡳࡩࡸ࠭ᷲ")
    KEY_AUTOMATE_SESSION_NAME = bstack1l1llll_opy_ (u"ࠤࡤࡹࡹࡵ࡭ࡢࡶࡨࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡴࡡ࡮ࡧࠥᷳ")
    KEY_EVENT_STARTED_AT = bstack1l1llll_opy_ (u"ࠥࡩࡻ࡫࡮ࡵࡡࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹࠨᷴ")
    KEY_EVENT_ENDED_AT = bstack1l1llll_opy_ (u"ࠦࡪࡼࡥ࡯ࡶࡢࡩࡳࡪࡥࡥࡡࡤࡸࠧ᷵")
    KEY_HOOK_ID = bstack1l1llll_opy_ (u"ࠧ࡮࡯ࡰ࡭ࡢ࡭ࡩࠨ᷶")
    KEY_HOOK_RESULT = bstack1l1llll_opy_ (u"ࠨࡨࡰࡱ࡮ࡣࡷ࡫ࡳࡶ࡮ࡷ᷷ࠦ")
    KEY_HOOK_LOGS = bstack1l1llll_opy_ (u"ࠢࡩࡱࡲ࡯ࡤࡲ࡯ࡨࡵ᷸ࠥ")
    KEY_HOOK_NAME = bstack1l1llll_opy_ (u"ࠣࡪࡲࡳࡰࡥ࡮ࡢ࡯ࡨ᷹ࠦ")
    bstack111ll111111_opy_ = bstack1l1llll_opy_ (u"ࠤ࡯ࡳ࡬ࡹ᷺ࠢ")
    KEY_CUSTOM_TAGS = bstack1l1llll_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯ࡢࡱࡪࡺࡡࡥࡣࡷࡥࠧ᷻")
    DEFAULT_TEST_RESULT = bstack1l1llll_opy_ (u"ࠦࡵ࡫࡮ࡥ࡫ࡱ࡫ࠧ᷼")
    DEFAULT_HOOK_RESULT = bstack1l1llll_opy_ (u"ࠧࡶࡥ࡯ࡦ࡬ࡲ࡬ࠨ᷽")
    KIND_SCREENSHOT = bstack1l1llll_opy_ (u"ࠨࡔࡆࡕࡗࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࠣ᷾")
    KIND_LOG = bstack1l1llll_opy_ (u"ࠢࡕࡇࡖࡘࡤࡒࡏࡈࠤ᷿")
    KIND_ATTACHMENT = bstack1l1llll_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖࠥḀ")
    instances: Dict[str, TestFrameworkTest] = dict()
    hook_regsitry: Dict[str, List[Callable]] = dict()
    test_frameworks: List[str]
    test_framework_versions: Dict[str, str]
    def __init__(
        self,
        test_frameworks: List[str],
        test_framework_versions: Dict[str, str],
        async_dispatcher: AsyncDispatcher
    ):
        self.test_frameworks = test_frameworks
        self.test_framework_versions = test_framework_versions
        self.async_dispatcher = async_dispatcher
    def track_event(
        self,
        context: TestFrameworkContext,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        self.logger.debug(bstack1l1llll_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽࢀࠤࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࡃࡻࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࡿࢂࠨḁ").format(test_framework_state,test_hook_state,args,kwargs))
    def run_hooks(
        self,
        instance: TestFrameworkTest,
        hook_info: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        hook_registry_key = TestFramework.hook_info_to_registry_key(hook_info)
        if not hook_registry_key in TestFramework.hook_regsitry:
            return
        self.logger.debug(bstack1l1llll_opy_ (u"ࠥ࡭ࡳࡼ࡯࡬࡫ࡱ࡫ࠥࢁࡽࠡࡥࡤࡰࡱࡨࡡࡤ࡭ࡶࠦḂ").format(len(TestFramework.hook_regsitry[hook_registry_key])))
        for callback in TestFramework.hook_regsitry[hook_registry_key]:
            try:
                callback(self, instance, hook_info, *args, **kwargs)
            except Exception as e:
                self.logger.error(bstack1l1llll_opy_ (u"ࠦࡪࡸࡲࡰࡴࠣ࡭ࡳࡼ࡯࡬࡫ࡱ࡫ࠥࡩࡡ࡭࡮ࡥࡥࡨࡱ࠺ࠡࡽࢀࠦḃ").format(e))
                traceback.print_exc()
    @abc.abstractmethod
    def is_pytest_framework(self):
        return
    @abc.abstractmethod
    def is_robot_framework(self):
        return
    @abc.abstractmethod
    def is_behave_framework(self):
        return
    @abc.abstractmethod
    def get_log_entries(self, instance, hook_info):
        return
    @abc.abstractmethod
    def clear_logs(self, instance, hook_info):
        return
    @staticmethod
    def get_tracked_instance(target: object, strict=True):
        if target is None:
            return None
        ctx = TrackedInstance.create_context(target)
        instance = TestFramework.instances.get(ctx.id, None)
        if instance and instance.bstack1l11ll111l1_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def get_current_instances(reverse=True) -> List[TestFrameworkTest]:
        thread_id = threading.get_ident()
        process_id = os.getpid()
        return sorted(
            filter(
                lambda t: t.context.thread_id == thread_id
                and t.context.process_id == process_id,
                TestFramework.instances.values(),
            ),
            key=lambda t: t.bstack1l11ll11ll1_opy_,
            reverse=reverse,
        )
    @staticmethod
    def get_context_instances(ctx: bstack1l11ll1l1l1_opy_, reverse=True) -> List[TestFrameworkTest]:
        return sorted(
            filter(
                lambda t: t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                TestFramework.instances.values(),
            ),
            key=lambda t: t.bstack1l11ll11ll1_opy_,
            reverse=reverse,
        )
    @staticmethod
    def has_state(instance: TestFrameworkTest, key: str):
        return instance and key in instance.data
    @staticmethod
    def get_state(instance: TestFrameworkTest, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def set_state(instance: TestFrameworkTest, key: str, value: Any):
        TestFramework.logger.debug(bstack1l1llll_opy_ (u"ࠧࡹࡥࡵࡡࡶࡸࡦࡺࡥ࠻ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀࢃࠠ࡬ࡧࡼࡁࢀࢃࠠࡷࡣ࡯ࡹࡪࡃࡻࡾࠤḄ").format(instance.ref(),key,value))
        instance.data[key] = value
        return True
    @staticmethod
    def set_state_entries(instance: TestFrameworkTest, entries: Dict[str, Any]):
        TestFramework.logger.debug(bstack1l1llll_opy_ (u"ࠨࡳࡦࡶࡢࡷࡹࡧࡴࡦࡡࡨࡲࡹࡸࡩࡦࡵ࠽ࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡾࠢࡨࡲࡹࡸࡩࡦࡵࡀࡿࢂࠨḅ").format(instance.ref(),entries,))
        instance.data.update(entries)
        return True
    @staticmethod
    def bstack111l111l1l1_opy_(instance: TestFrameworkState, key: str, value: Any):
        TestFramework.logger.debug(bstack1l1llll_opy_ (u"ࠢࡶࡲࡧࡥࡹ࡫࡟ࡴࡶࡤࡸࡪࡀࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾࢁࠥࡱࡥࡺ࠿ࡾࢁࠥࡼࡡ࡭ࡷࡨࡁࢀࢃࠢḆ").format(instance.ref(),key,value))
        instance.data.update(key, value)
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = TestFramework.get_tracked_instance(target, strict)
        return TestFramework.get_state(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = TestFramework.get_tracked_instance(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    @staticmethod
    def bstack111l1ll11ll_opy_(instance: TestFrameworkTest, key: str, value: object):
        if instance == None:
            return
        instance.data[key] = value
    @staticmethod
    def bstack111ll111l11_opy_(instance: TestFrameworkTest, key: str):
        return instance.data[key]
    @staticmethod
    def hook_info_to_registry_key(hook_info: Tuple[TestFrameworkState, TestHookState]):
        return bstack1l1llll_opy_ (u"ࠣ࠼ࠥḇ").join((TestFrameworkState(hook_info[0]).name, TestHookState(hook_info[1]).name))
    @staticmethod
    def set_hook_callback(hook_info: Tuple[TestFrameworkState, TestHookState], callback: Callable):
        hook_registry_key = TestFramework.hook_info_to_registry_key(hook_info)
        TestFramework.logger.debug(bstack1l1llll_opy_ (u"ࠤࡶࡩࡹࡥࡨࡰࡱ࡮ࡣࡨࡧ࡬࡭ࡤࡤࡧࡰࡀࠠࡩࡱࡲ࡯ࡤࡸࡥࡨ࡫ࡶࡸࡷࡿ࡟࡬ࡧࡼࡁࢀࢃࠢḈ").format(hook_registry_key))
        if not hook_registry_key in TestFramework.hook_regsitry:
            TestFramework.hook_regsitry[hook_registry_key] = []
        TestFramework.hook_regsitry[hook_registry_key].append(callback)
    @staticmethod
    def object_fqcn(o):
        klass = o.__class__
        module = klass.__module__
        if module == bstack1l1llll_opy_ (u"ࠥࡦࡺ࡯࡬ࡵ࡫ࡱࡷࠧḉ"):
            return klass.__qualname__
        return module + bstack1l1llll_opy_ (u"ࠦ࠳ࠨḊ") + klass.__qualname__
    @staticmethod
    def extract_keys(obj, keys, default_value=None):
        return {k: getattr(obj, k, default_value) for k in keys}