# coding: UTF-8
import sys
bstack11ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1ll_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack1l1_opy_ (bstack1111l11_opy_):
    global bstack111l1ll_opy_
    bstack1l111l1_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1llll11_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l1l111_opy_ = bstack1l111l1_opy_ % len (bstack1llll11_opy_)
    bstack11l1l_opy_ = bstack1llll11_opy_ [:bstack1l1l111_opy_] + bstack1llll11_opy_ [bstack1l1l111_opy_:]
    if bstack11ll11_opy_:
        bstack11lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1ll_opy_ - (bstack111l1l1_opy_ + bstack1l111l1_opy_) % bstack1ll11_opy_) for bstack111l1l1_opy_, char in enumerate (bstack11l1l_opy_)])
    else:
        bstack11lll11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1ll_opy_ - (bstack111l1l1_opy_ + bstack1l111l1_opy_) % bstack1ll11_opy_) for bstack111l1l1_opy_, char in enumerate (bstack11l1l_opy_)])
    return eval (bstack11lll11_opy_)
import os
from bstack_utils.logger_utils import get_logger
logger = get_logger(__name__)
def bstack1lll1111l_opy_(bstack1ll11l11ll_opy_):
    bstack1l1_opy_ (u"ࠦࠧࠨࡃࡢ࡮࡯ࠤࡉࡸࡩࡷࡧࡵࡍࡳ࡯ࡴࠡࡩࡕࡔࡈࠦࡴࡰࠢࡪࡩࡹࠦࡢࡢࡥ࡮ࡩࡳࡪ࠭ࡳࡧࡶࡳࡱࡼࡥࡥࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳ࠯ࠢࡕࡩࡹࡻࡲ࡯ࡵࠣࡨ࡮ࡩࡴࠡࡱࡵࠤࡓࡵ࡮ࡦ࠰ࠥࠦࠧ᧩")
    try:
        from browserstack_sdk.sdk_cli.cli import cli
        from browserstack_sdk.sdk_cli.bstack1l1ll111_opy_ import bstack1llllllll1_opy_
        from browserstack_sdk.sdk_cli.bstack1ll11ll111_opy_ import bstack11ll11l1l_opy_
        from browserstack_sdk import sdk_pb2 as structs
        import json
        import threading
        if not cli.bstack1l1ll11l111_opy_ or not cli.cli_bin_session_id:
            logger.debug(bstack1l1_opy_ (u"ࠧࡩࡡ࡭࡮ࡢࡨࡷ࡯ࡶࡦࡴࡢ࡭ࡳ࡯ࡴࡠࡨࡵࡳࡲࡥ࡭ࡰࡦࡢࡴࡴࡶࡥ࡯࠼ࠣࡧࡱ࡯ࠠ࡯ࡱࡷࠤࡷ࡫ࡡࡥࡻ࠯ࠤࡸࡱࡩࡱࡲ࡬ࡲ࡬ࠨ᧪"))
            return None
        instance = next(iter(bstack1llllllll1_opy_.bstack1l11l111l_opy_.values()), None)
        if not instance:
            logger.debug(bstack1l1_opy_ (u"ࠨࡣࡢ࡮࡯ࡣࡩࡸࡩࡷࡧࡵࡣ࡮ࡴࡩࡵࡡࡩࡶࡴࡳ࡟࡮ࡱࡧࡣࡵࡵࡰࡦࡰ࠽ࠤࡳࡵࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࡊࡷࡧ࡭ࡦࡹࡲࡶࡰࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠡࡨࡲࡹࡳࡪࠢ᧫"))
            return None
        req = structs.DriverInitRequest()
        req.bin_session_id = cli.cli_bin_session_id
        req.platform_index = bstack1ll11l11ll_opy_
        req.ref = instance.ref()
        req.user_input_params = json.dumps({bstack1l1_opy_ (u"ࠧࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭᧬"): True}).encode(bstack1l1_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢ᧭"))
        req.client_worker_id = bstack1l1_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣ᧮").format(threading.get_ident(), os.getpid())
        logger.debug(bstack1l1_opy_ (u"ࠥࡧࡦࡲ࡬ࡠࡦࡵ࡭ࡻ࡫ࡲࡠ࡫ࡱ࡭ࡹࡥࡦࡳࡱࡰࡣࡲࡵࡤࡠࡲࡲࡴࡪࡴ࠺ࠡࡵࡨࡲࡩ࡯࡮ࡨࠢࡇࡶ࡮ࡼࡥࡳࡋࡱ࡭ࡹࠦࡲࡦࡨࡀࡿࢂࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾ࠽ࡼࡿࠥ᧯").format(
            instance.ref(), bstack1ll11l11ll_opy_))
        response = cli.bstack1l1ll11l111_opy_.DriverInit(req)
        if response and response.success and response.capabilities:
            caps = json.loads(response.capabilities.decode(bstack1l1_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥ᧰")))
            if caps:
                bstack11ll11l1l_opy_.bstack1ll1l11lll_opy_(instance, bstack11ll11l1l_opy_.bstack1ll1l1l11_opy_, caps)
                logger.debug(bstack1l1_opy_ (u"ࠧࡩࡡ࡭࡮ࡢࡨࡷ࡯ࡶࡦࡴࡢ࡭ࡳ࡯ࡴࡠࡨࡵࡳࡲࡥ࡭ࡰࡦࡢࡴࡴࡶࡥ࡯࠼ࠣࡈࡷ࡯ࡶࡦࡴࡌࡲ࡮ࡺࠠࡴࡷࡦࡧࡪ࡫ࡤࡦࡦ࠯ࠤ࡬ࡵࡴࠡࡽࢀࠤࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡹࠡ࡭ࡨࡽࡸࠨ᧱").format(len(caps)))
                return caps
        logger.debug(bstack1l1_opy_ (u"ࠨࡣࡢ࡮࡯ࡣࡩࡸࡩࡷࡧࡵࡣ࡮ࡴࡩࡵࡡࡩࡶࡴࡳ࡟࡮ࡱࡧࡣࡵࡵࡰࡦࡰ࠽ࠤࡉࡸࡩࡷࡧࡵࡍࡳ࡯ࡴࠡࡴࡨࡸࡺࡸ࡮ࡦࡦࠣࡷࡺࡩࡣࡦࡵࡶࡁࡋࡧ࡬ࡴࡧࠣࡳࡷࠦ࡮ࡰࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣ᧲"))
        return None
    except Exception as e:
        logger.debug(bstack1l1_opy_ (u"ࠢࡤࡣ࡯ࡰࡤࡪࡲࡪࡸࡨࡶࡤ࡯࡮ࡪࡶࡢࡪࡷࡵ࡭ࡠ࡯ࡲࡨࡤࡶ࡯ࡱࡧࡱ࠾ࠥ࡬ࡡࡪ࡮ࡨࡨ࠿ࠦࡻࡾࠤ᧳").format(e))
        return None