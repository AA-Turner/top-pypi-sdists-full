# coding: UTF-8
import sys
bstack11ll_opy_ = sys.version_info [0] == 2
bstack11lllll_opy_ = 2048
bstack1llll_opy_ = 7
def bstack11ll11_opy_ (bstack111l1l_opy_):
    global bstack11111ll_opy_
    bstack1llll11_opy_ = ord (bstack111l1l_opy_ [-1])
    bstack1111l11_opy_ = bstack111l1l_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1111l11_opy_)
    bstack11111l_opy_ = bstack1111l11_opy_ [:bstack111l1ll_opy_] + bstack1111l11_opy_ [bstack111l1ll_opy_:]
    if bstack11ll_opy_:
        bstack1l11lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    else:
        bstack1l11lll_opy_ = str () .join ([chr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    return eval (bstack1l11lll_opy_)
import os
from bstack_utils.logger_utils import get_logger
logger = get_logger(__name__)
def bstack1l1l1ll11_opy_(bstack1l11l11ll_opy_):
    bstack11ll11_opy_ (u"ࠦࠧࠨࡃࡢ࡮࡯ࠤࡉࡸࡩࡷࡧࡵࡍࡳ࡯ࡴࠡࡩࡕࡔࡈࠦࡴࡰࠢࡪࡩࡹࠦࡢࡢࡥ࡮ࡩࡳࡪ࠭ࡳࡧࡶࡳࡱࡼࡥࡥࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳ࠯ࠢࡕࡩࡹࡻࡲ࡯ࡵࠣࡨ࡮ࡩࡴࠡࡱࡵࠤࡓࡵ࡮ࡦ࠰ࠥࠦࠧᯚ")
    try:
        from browserstack_sdk.sdk_cli.cli import cli
        from browserstack_sdk.sdk_cli.bstack11l1l1l11_opy_ import bstack1lll1111ll_opy_
        from browserstack_sdk.sdk_cli.bstack1l11111ll1_opy_ import bstack1111l11l1l_opy_
        from browserstack_sdk import sdk_pb2 as structs
        import json
        import threading
        if not cli.bstack1l1l111l1_opy_ or not cli.cli_bin_session_id:
            logger.debug(bstack11ll11_opy_ (u"ࠧࡩࡡ࡭࡮ࡢࡨࡷ࡯ࡶࡦࡴࡢ࡭ࡳ࡯ࡴࡠࡨࡵࡳࡲࡥ࡭ࡰࡦࡢࡴࡴࡶࡥ࡯࠼ࠣࡧࡱ࡯ࠠ࡯ࡱࡷࠤࡷ࡫ࡡࡥࡻ࠯ࠤࡸࡱࡩࡱࡲ࡬ࡲ࡬ࠨᯛ"))
            return None
        instance = next(iter(bstack1lll1111ll_opy_.bstack11111l111l_opy_.values()), None)
        if not instance:
            logger.debug(bstack11ll11_opy_ (u"ࠨࡣࡢ࡮࡯ࡣࡩࡸࡩࡷࡧࡵࡣ࡮ࡴࡩࡵࡡࡩࡶࡴࡳ࡟࡮ࡱࡧࡣࡵࡵࡰࡦࡰ࠽ࠤࡳࡵࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࡊࡷࡧ࡭ࡦࡹࡲࡶࡰࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠡࡨࡲࡹࡳࡪࠢᯜ"))
            return None
        req = structs.DriverInitRequest()
        req.bin_session_id = cli.cli_bin_session_id
        req.platform_index = bstack1l11l11ll_opy_
        req.ref = instance.ref()
        req.user_input_params = json.dumps({bstack11ll11_opy_ (u"ࠧࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ᯝ"): True}).encode(bstack11ll11_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢᯞ"))
        req.client_worker_id = bstack11ll11_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣᯟ").format(threading.get_ident(), os.getpid())
        logger.debug(bstack11ll11_opy_ (u"ࠥࡧࡦࡲ࡬ࡠࡦࡵ࡭ࡻ࡫ࡲࡠ࡫ࡱ࡭ࡹࡥࡦࡳࡱࡰࡣࡲࡵࡤࡠࡲࡲࡴࡪࡴ࠺ࠡࡵࡨࡲࡩ࡯࡮ࡨࠢࡇࡶ࡮ࡼࡥࡳࡋࡱ࡭ࡹࠦࡲࡦࡨࡀࡿࢂࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾ࠽ࡼࡿࠥᯠ").format(
            instance.ref(), bstack1l11l11ll_opy_))
        response = cli.bstack1l1l111l1_opy_.DriverInit(req)
        if response and response.success and response.capabilities:
            caps = json.loads(response.capabilities.decode(bstack11ll11_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥᯡ")))
            if caps:
                bstack1111l11l1l_opy_.bstack1l1l1111l1_opy_(instance, bstack1111l11l1l_opy_.bstack11ll1l111l_opy_, caps)
                logger.debug(bstack11ll11_opy_ (u"ࠧࡩࡡ࡭࡮ࡢࡨࡷ࡯ࡶࡦࡴࡢ࡭ࡳ࡯ࡴࡠࡨࡵࡳࡲࡥ࡭ࡰࡦࡢࡴࡴࡶࡥ࡯࠼ࠣࡈࡷ࡯ࡶࡦࡴࡌࡲ࡮ࡺࠠࡴࡷࡦࡧࡪ࡫ࡤࡦࡦ࠯ࠤ࡬ࡵࡴࠡࡽࢀࠤࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡹࠡ࡭ࡨࡽࡸࠨᯢ").format(len(caps)))
                return caps
        logger.debug(bstack11ll11_opy_ (u"ࠨࡣࡢ࡮࡯ࡣࡩࡸࡩࡷࡧࡵࡣ࡮ࡴࡩࡵࡡࡩࡶࡴࡳ࡟࡮ࡱࡧࡣࡵࡵࡰࡦࡰ࠽ࠤࡉࡸࡩࡷࡧࡵࡍࡳ࡯ࡴࠡࡴࡨࡸࡺࡸ࡮ࡦࡦࠣࡷࡺࡩࡣࡦࡵࡶࡁࡋࡧ࡬ࡴࡧࠣࡳࡷࠦ࡮ࡰࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣᯣ"))
        return None
    except Exception as e:
        logger.debug(bstack11ll11_opy_ (u"ࠢࡤࡣ࡯ࡰࡤࡪࡲࡪࡸࡨࡶࡤ࡯࡮ࡪࡶࡢࡪࡷࡵ࡭ࡠ࡯ࡲࡨࡤࡶ࡯ࡱࡧࡱ࠾ࠥ࡬ࡡࡪ࡮ࡨࡨ࠿ࠦࡻࡾࠤᯤ").format(e))
        return None