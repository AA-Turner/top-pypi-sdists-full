# coding: UTF-8
import sys
bstack11l1l_opy_ = sys.version_info [0] == 2
bstack1ll11_opy_ = 2048
bstack11ll11_opy_ = 7
def bstack1l111l_opy_ (bstack11l11l_opy_):
    global bstack1l11l_opy_
    bstack1l1111l_opy_ = ord (bstack11l11l_opy_ [-1])
    bstack1l1l11l_opy_ = bstack11l11l_opy_ [:-1]
    bstack111l1_opy_ = bstack1l1111l_opy_ % len (bstack1l1l11l_opy_)
    bstack11l1l1l_opy_ = bstack1l1l11l_opy_ [:bstack111l1_opy_] + bstack1l1l11l_opy_ [bstack111l1_opy_:]
    if bstack11l1l_opy_:
        bstack1111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    else:
        bstack1111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    return eval (bstack1111l1l_opy_)
import os
from bstack_utils.logger_utils import get_logger
logger = get_logger(__name__)
def bstack1l1l1l1l11_opy_(bstack11111l1l1l_opy_):
    bstack1l111l_opy_ (u"ࠦࠧࠨࡃࡢ࡮࡯ࠤࡉࡸࡩࡷࡧࡵࡍࡳ࡯ࡴࠡࡩࡕࡔࡈࠦࡴࡰࠢࡪࡩࡹࠦࡢࡢࡥ࡮ࡩࡳࡪ࠭ࡳࡧࡶࡳࡱࡼࡥࡥࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳ࠯ࠢࡕࡩࡹࡻࡲ࡯ࡵࠣࡨ࡮ࡩࡴࠡࡱࡵࠤࡓࡵ࡮ࡦ࠰ࠥࠦࠧ᯶")
    try:
        from browserstack_sdk.sdk_cli.cli import cli
        from browserstack_sdk.sdk_cli.bstack1111ll1ll1_opy_ import bstack111l1ll1ll_opy_
        from browserstack_sdk.sdk_cli.bstack111l1ll11l_opy_ import bstack11ll1llll_opy_
        from browserstack_sdk import sdk_pb2 as structs
        import json
        import threading
        if not cli.bstack1l1l1111l1_opy_ or not cli.cli_bin_session_id:
            logger.debug(bstack1l111l_opy_ (u"ࠧࡩࡡ࡭࡮ࡢࡨࡷ࡯ࡶࡦࡴࡢ࡭ࡳ࡯ࡴࡠࡨࡵࡳࡲࡥ࡭ࡰࡦࡢࡴࡴࡶࡥ࡯࠼ࠣࡧࡱ࡯ࠠ࡯ࡱࡷࠤࡷ࡫ࡡࡥࡻ࠯ࠤࡸࡱࡩࡱࡲ࡬ࡲ࡬ࠨ᯷"))
            return None
        instance = next(iter(bstack111l1ll1ll_opy_.bstack1l1l1111l_opy_.values()), None)
        if not instance:
            logger.debug(bstack1l111l_opy_ (u"ࠨࡣࡢ࡮࡯ࡣࡩࡸࡩࡷࡧࡵࡣ࡮ࡴࡩࡵࡡࡩࡶࡴࡳ࡟࡮ࡱࡧࡣࡵࡵࡰࡦࡰ࠽ࠤࡳࡵࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࡊࡷࡧ࡭ࡦࡹࡲࡶࡰࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠡࡨࡲࡹࡳࡪࠢ᯸"))
            return None
        req = structs.DriverInitRequest()
        req.bin_session_id = cli.cli_bin_session_id
        req.platform_index = bstack11111l1l1l_opy_
        req.ref = instance.ref()
        req.user_input_params = json.dumps({bstack1l111l_opy_ (u"ࠧࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭᯹"): True}).encode(bstack1l111l_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢ᯺"))
        req.client_worker_id = bstack1l111l_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣ᯻").format(threading.get_ident(), os.getpid())
        logger.debug(bstack1l111l_opy_ (u"ࠥࡧࡦࡲ࡬ࡠࡦࡵ࡭ࡻ࡫ࡲࡠ࡫ࡱ࡭ࡹࡥࡦࡳࡱࡰࡣࡲࡵࡤࡠࡲࡲࡴࡪࡴ࠺ࠡࡵࡨࡲࡩ࡯࡮ࡨࠢࡇࡶ࡮ࡼࡥࡳࡋࡱ࡭ࡹࠦࡲࡦࡨࡀࡿࢂࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾ࠽ࡼࡿࠥ᯼").format(
            instance.ref(), bstack11111l1l1l_opy_))
        response = cli.bstack1l1l1111l1_opy_.DriverInit(req)
        if response and response.success and response.capabilities:
            caps = json.loads(response.capabilities.decode(bstack1l111l_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥ᯽")))
            if caps:
                bstack11ll1llll_opy_.bstack11111ll11l_opy_(instance, bstack11ll1llll_opy_.bstack11lll111l_opy_, caps)
                logger.debug(bstack1l111l_opy_ (u"ࠧࡩࡡ࡭࡮ࡢࡨࡷ࡯ࡶࡦࡴࡢ࡭ࡳ࡯ࡴࡠࡨࡵࡳࡲࡥ࡭ࡰࡦࡢࡴࡴࡶࡥ࡯࠼ࠣࡈࡷ࡯ࡶࡦࡴࡌࡲ࡮ࡺࠠࡴࡷࡦࡧࡪ࡫ࡤࡦࡦ࠯ࠤ࡬ࡵࡴࠡࡽࢀࠤࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡹࠡ࡭ࡨࡽࡸࠨ᯾").format(len(caps)))
                return caps
        logger.debug(bstack1l111l_opy_ (u"ࠨࡣࡢ࡮࡯ࡣࡩࡸࡩࡷࡧࡵࡣ࡮ࡴࡩࡵࡡࡩࡶࡴࡳ࡟࡮ࡱࡧࡣࡵࡵࡰࡦࡰ࠽ࠤࡉࡸࡩࡷࡧࡵࡍࡳ࡯ࡴࠡࡴࡨࡸࡺࡸ࡮ࡦࡦࠣࡷࡺࡩࡣࡦࡵࡶࡁࡋࡧ࡬ࡴࡧࠣࡳࡷࠦ࡮ࡰࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣ᯿"))
        return None
    except Exception as e:
        logger.debug(bstack1l111l_opy_ (u"ࠢࡤࡣ࡯ࡰࡤࡪࡲࡪࡸࡨࡶࡤ࡯࡮ࡪࡶࡢࡪࡷࡵ࡭ࡠ࡯ࡲࡨࡤࡶ࡯ࡱࡧࡱ࠾ࠥ࡬ࡡࡪ࡮ࡨࡨ࠿ࠦࡻࡾࠤᰀ").format(e))
        return None