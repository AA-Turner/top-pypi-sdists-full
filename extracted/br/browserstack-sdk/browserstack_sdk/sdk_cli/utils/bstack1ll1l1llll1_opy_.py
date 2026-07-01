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
import os
from bstack_utils.logger_utils import get_logger
logger = get_logger(__name__)
def bstack1ll1lll1l11_opy_(bstack1ll1l111l1_opy_):
    bstack1l1llll_opy_ (u"ࠥࠦࠧࡉࡡ࡭࡮ࠣࡈࡷ࡯ࡶࡦࡴࡌࡲ࡮ࡺࠠࡨࡔࡓࡇࠥࡺ࡯ࠡࡩࡨࡸࠥࡨࡡࡤ࡭ࡨࡲࡩ࠳ࡲࡦࡵࡲࡰࡻ࡫ࡤࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹ࠮ࠡࡔࡨࡸࡺࡸ࡮ࡴࠢࡧ࡭ࡨࡺࠠࡰࡴࠣࡒࡴࡴࡥ࠯ࠤࠥࠦằ")
    try:
        from browserstack_sdk.sdk_cli.cli import cli
        from browserstack_sdk.sdk_cli.automation_framework import bstack1l111l1l_opy_
        from browserstack_sdk.sdk_cli.bstack1l1ll1l1_opy_ import bstack111ll111_opy_
        from browserstack_sdk import sdk_pb2 as structs
        import json
        import threading
        if not cli.cli_service or not cli.cli_bin_session_id:
            logger.debug(bstack1l1llll_opy_ (u"ࠦࡨࡧ࡬࡭ࡡࡧࡶ࡮ࡼࡥࡳࡡ࡬ࡲ࡮ࡺ࡟ࡧࡴࡲࡱࡤࡳ࡯ࡥࡡࡳࡳࡵ࡫࡮࠻ࠢࡦࡰ࡮ࠦ࡮ࡰࡶࠣࡶࡪࡧࡤࡺ࠮ࠣࡷࡰ࡯ࡰࡱ࡫ࡱ࡫ࠧẲ"))
            return None
        instance = next(iter(bstack1l111l1l_opy_.instances.values()), None)
        if not instance:
            logger.debug(bstack1l1llll_opy_ (u"ࠧࡩࡡ࡭࡮ࡢࡨࡷ࡯ࡶࡦࡴࡢ࡭ࡳ࡯ࡴࡠࡨࡵࡳࡲࡥ࡭ࡰࡦࡢࡴࡴࡶࡥ࡯࠼ࠣࡲࡴࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠠࡧࡱࡸࡲࡩࠨẳ"))
            return None
        req = structs.DriverInitRequest()
        req.bin_session_id = cli.cli_bin_session_id
        req.platform_index = bstack1ll1l111l1_opy_
        req.ref = instance.ref()
        req.user_input_params = json.dumps({bstack1l1llll_opy_ (u"࠭ࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬẴ"): True}).encode(bstack1l1llll_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨẵ"))
        req.client_worker_id = bstack1l1llll_opy_ (u"ࠣࡽࢀ࠱ࢀࢃࠢẶ").format(threading.get_ident(), os.getpid())
        logger.debug(bstack1l1llll_opy_ (u"ࠤࡦࡥࡱࡲ࡟ࡥࡴ࡬ࡺࡪࡸ࡟ࡪࡰ࡬ࡸࡤ࡬ࡲࡰ࡯ࡢࡱࡴࡪ࡟ࡱࡱࡳࡩࡳࡀࠠࡴࡧࡱࡨ࡮ࡴࡧࠡࡆࡵ࡭ࡻ࡫ࡲࡊࡰ࡬ࡸࠥࡸࡥࡧ࠿ࡾࢁࠥࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡪࡰࡧࡩࡽࡃࡻࡾࠤặ").format(
            instance.ref(), bstack1ll1l111l1_opy_))
        response = cli.cli_service.DriverInit(req)
        if response and response.success and response.capabilities:
            caps = json.loads(response.capabilities.decode(bstack1l1llll_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤẸ")))
            if caps:
                bstack111ll111_opy_.set_state(instance, bstack111ll111_opy_.bstack1l111lll_opy_, caps)
                logger.debug(bstack1l1llll_opy_ (u"ࠦࡨࡧ࡬࡭ࡡࡧࡶ࡮ࡼࡥࡳࡡ࡬ࡲ࡮ࡺ࡟ࡧࡴࡲࡱࡤࡳ࡯ࡥࡡࡳࡳࡵ࡫࡮࠻ࠢࡇࡶ࡮ࡼࡥࡳࡋࡱ࡭ࡹࠦࡳࡶࡥࡦࡩࡪࡪࡥࡥ࠮ࠣ࡫ࡴࡺࠠࡼࡿࠣࡧࡦࡶࡡࡣ࡫࡯࡭ࡹࡿࠠ࡬ࡧࡼࡷࠧẹ").format(len(caps)))
                return caps
        logger.debug(bstack1l1llll_opy_ (u"ࠧࡩࡡ࡭࡮ࡢࡨࡷ࡯ࡶࡦࡴࡢ࡭ࡳ࡯ࡴࡠࡨࡵࡳࡲࡥ࡭ࡰࡦࡢࡴࡴࡶࡥ࡯࠼ࠣࡈࡷ࡯ࡶࡦࡴࡌࡲ࡮ࡺࠠࡳࡧࡷࡹࡷࡴࡥࡥࠢࡶࡹࡨࡩࡥࡴࡵࡀࡊࡦࡲࡳࡦࠢࡲࡶࠥࡴ࡯ࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢẺ"))
        return None
    except Exception as e:
        logger.debug(bstack1l1llll_opy_ (u"ࠨࡣࡢ࡮࡯ࡣࡩࡸࡩࡷࡧࡵࡣ࡮ࡴࡩࡵࡡࡩࡶࡴࡳ࡟࡮ࡱࡧࡣࡵࡵࡰࡦࡰ࠽ࠤ࡫ࡧࡩ࡭ࡧࡧ࠾ࠥࢁࡽࠣẻ").format(e))
        return None