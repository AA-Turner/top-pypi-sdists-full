# coding: UTF-8
import sys
bstack11l1l1l_opy_ = sys.version_info [0] == 2
bstack1111ll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack111l_opy_ (bstack11lll11_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l1l1_opy_ = ord (bstack11lll11_opy_ [-1])
    bstack1l111_opy_ = bstack11lll11_opy_ [:-1]
    bstack11llll_opy_ = bstack1l1l1l1_opy_ % len (bstack1l111_opy_)
    bstack1l111l_opy_ = bstack1l111_opy_ [:bstack11llll_opy_] + bstack1l111_opy_ [bstack11llll_opy_:]
    if bstack11l1l1l_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    return eval (bstack1_opy_)
import os
from bstack_utils.logger_utils import get_logger
logger = get_logger(__name__)
def bstack11l1lll111_opy_(bstack11l111lll_opy_):
    bstack111l_opy_ (u"ࠥࠦࠧࡉࡡ࡭࡮ࠣࡈࡷ࡯ࡶࡦࡴࡌࡲ࡮ࡺࠠࡨࡔࡓࡇࠥࡺ࡯ࠡࡩࡨࡸࠥࡨࡡࡤ࡭ࡨࡲࡩ࠳ࡲࡦࡵࡲࡰࡻ࡫ࡤࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹ࠮ࠡࡔࡨࡸࡺࡸ࡮ࡴࠢࡧ࡭ࡨࡺࠠࡰࡴࠣࡒࡴࡴࡥ࠯ࠤࠥࠦᯙ")
    try:
        from browserstack_sdk.sdk_cli.cli import cli
        from browserstack_sdk.sdk_cli.bstack1ll1111111_opy_ import bstack1l1l1ll11l_opy_
        from browserstack_sdk.sdk_cli.bstack1ll111ll_opy_ import bstack11ll1lllll_opy_
        from browserstack_sdk import sdk_pb2 as structs
        import json
        import threading
        if not cli.bstack11l11lll11_opy_ or not cli.cli_bin_session_id:
            logger.debug(bstack111l_opy_ (u"ࠦࡨࡧ࡬࡭ࡡࡧࡶ࡮ࡼࡥࡳࡡ࡬ࡲ࡮ࡺ࡟ࡧࡴࡲࡱࡤࡳ࡯ࡥࡡࡳࡳࡵ࡫࡮࠻ࠢࡦࡰ࡮ࠦ࡮ࡰࡶࠣࡶࡪࡧࡤࡺ࠮ࠣࡷࡰ࡯ࡰࡱ࡫ࡱ࡫ࠧᯚ"))
            return None
        instance = next(iter(bstack1l1l1ll11l_opy_.bstack1l111l111_opy_.values()), None)
        if not instance:
            logger.debug(bstack111l_opy_ (u"ࠧࡩࡡ࡭࡮ࡢࡨࡷ࡯ࡶࡦࡴࡢ࡭ࡳ࡯ࡴࡠࡨࡵࡳࡲࡥ࡭ࡰࡦࡢࡴࡴࡶࡥ࡯࠼ࠣࡲࡴࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠠࡧࡱࡸࡲࡩࠨᯛ"))
            return None
        req = structs.DriverInitRequest()
        req.bin_session_id = cli.cli_bin_session_id
        req.platform_index = bstack11l111lll_opy_
        req.ref = instance.ref()
        req.user_input_params = json.dumps({bstack111l_opy_ (u"࠭ࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬᯜ"): True}).encode(bstack111l_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨᯝ"))
        req.client_worker_id = bstack111l_opy_ (u"ࠣࡽࢀ࠱ࢀࢃࠢᯞ").format(threading.get_ident(), os.getpid())
        logger.debug(bstack111l_opy_ (u"ࠤࡦࡥࡱࡲ࡟ࡥࡴ࡬ࡺࡪࡸ࡟ࡪࡰ࡬ࡸࡤ࡬ࡲࡰ࡯ࡢࡱࡴࡪ࡟ࡱࡱࡳࡩࡳࡀࠠࡴࡧࡱࡨ࡮ࡴࡧࠡࡆࡵ࡭ࡻ࡫ࡲࡊࡰ࡬ࡸࠥࡸࡥࡧ࠿ࡾࢁࠥࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡪࡰࡧࡩࡽࡃࡻࡾࠤᯟ").format(
            instance.ref(), bstack11l111lll_opy_))
        response = cli.bstack11l11lll11_opy_.DriverInit(req)
        if response and response.success and response.capabilities:
            caps = json.loads(response.capabilities.decode(bstack111l_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤᯠ")))
            if caps:
                bstack11ll1lllll_opy_.bstack1l11l1ll11_opy_(instance, bstack11ll1lllll_opy_.bstack1111lll1_opy_, caps)
                logger.debug(bstack111l_opy_ (u"ࠦࡨࡧ࡬࡭ࡡࡧࡶ࡮ࡼࡥࡳࡡ࡬ࡲ࡮ࡺ࡟ࡧࡴࡲࡱࡤࡳ࡯ࡥࡡࡳࡳࡵ࡫࡮࠻ࠢࡇࡶ࡮ࡼࡥࡳࡋࡱ࡭ࡹࠦࡳࡶࡥࡦࡩࡪࡪࡥࡥ࠮ࠣ࡫ࡴࡺࠠࡼࡿࠣࡧࡦࡶࡡࡣ࡫࡯࡭ࡹࡿࠠ࡬ࡧࡼࡷࠧᯡ").format(len(caps)))
                return caps
        logger.debug(bstack111l_opy_ (u"ࠧࡩࡡ࡭࡮ࡢࡨࡷ࡯ࡶࡦࡴࡢ࡭ࡳ࡯ࡴࡠࡨࡵࡳࡲࡥ࡭ࡰࡦࡢࡴࡴࡶࡥ࡯࠼ࠣࡈࡷ࡯ࡶࡦࡴࡌࡲ࡮ࡺࠠࡳࡧࡷࡹࡷࡴࡥࡥࠢࡶࡹࡨࡩࡥࡴࡵࡀࡊࡦࡲࡳࡦࠢࡲࡶࠥࡴ࡯ࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢᯢ"))
        return None
    except Exception as e:
        logger.debug(bstack111l_opy_ (u"ࠨࡣࡢ࡮࡯ࡣࡩࡸࡩࡷࡧࡵࡣ࡮ࡴࡩࡵࡡࡩࡶࡴࡳ࡟࡮ࡱࡧࡣࡵࡵࡰࡦࡰ࠽ࠤ࡫ࡧࡩ࡭ࡧࡧ࠾ࠥࢁࡽࠣᯣ").format(e))
        return None