# coding: UTF-8
import sys
bstack1l11ll1_opy_ = sys.version_info [0] == 2
bstack1lll1l1_opy_ = 2048
bstack11lllll_opy_ = 7
def bstack1l1111l_opy_ (bstack1llllll1_opy_):
    global bstack1ll111_opy_
    bstack11l1l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack11l11l_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1ll11_opy_ = bstack11l1l_opy_ % len (bstack11l11l_opy_)
    bstack11ll1_opy_ = bstack11l11l_opy_ [:bstack1ll11_opy_] + bstack11l11l_opy_ [bstack1ll11_opy_:]
    if bstack1l11ll1_opy_:
        bstack11l1l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack11l1l11_opy_ = str () .join ([chr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack11l1l11_opy_)
import os
from bstack_utils.logger_utils import get_logger
logger = get_logger(__name__)
def bstack11lll1l1l_opy_(bstack11l1lllll1_opy_):
    bstack1l1111l_opy_ (u"ࠨࠢࠣࡅࡤࡰࡱࠦࡄࡳ࡫ࡹࡩࡷࡏ࡮ࡪࡶࠣ࡫ࡗࡖࡃࠡࡶࡲࠤ࡬࡫ࡴࠡࡤࡤࡧࡰ࡫࡮ࡥ࠯ࡵࡩࡸࡵ࡬ࡷࡧࡧࠤࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵ࠱ࠤࡗ࡫ࡴࡶࡴࡱࡷࠥࡪࡩࡤࡶࠣࡳࡷࠦࡎࡰࡰࡨ࠲ࠧࠨࠢ᯸")
    try:
        from browserstack_sdk.sdk_cli.cli import cli
        from browserstack_sdk.sdk_cli.bstack1l11ll1ll1_opy_ import bstack11l1l1ll11_opy_
        from browserstack_sdk.sdk_cli.bstack1llllll11ll_opy_ import bstack111l1l11l_opy_
        from browserstack_sdk import sdk_pb2 as structs
        import json
        import threading
        if not cli.bstack11l1ll1lll_opy_ or not cli.cli_bin_session_id:
            logger.debug(bstack1l1111l_opy_ (u"ࠢࡤࡣ࡯ࡰࡤࡪࡲࡪࡸࡨࡶࡤ࡯࡮ࡪࡶࡢࡪࡷࡵ࡭ࡠ࡯ࡲࡨࡤࡶ࡯ࡱࡧࡱ࠾ࠥࡩ࡬ࡪࠢࡱࡳࡹࠦࡲࡦࡣࡧࡽ࠱ࠦࡳ࡬࡫ࡳࡴ࡮ࡴࡧࠣ᯹"))
            return None
        instance = next(iter(bstack11l1l1ll11_opy_.bstack1lllll1ll1_opy_.values()), None)
        if not instance:
            logger.debug(bstack1l1111l_opy_ (u"ࠣࡥࡤࡰࡱࡥࡤࡳ࡫ࡹࡩࡷࡥࡩ࡯࡫ࡷࡣ࡫ࡸ࡯࡮ࡡࡰࡳࡩࡥࡰࡰࡲࡨࡲ࠿ࠦ࡮ࡰࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠣࡪࡴࡻ࡮ࡥࠤ᯺"))
            return None
        req = structs.DriverInitRequest()
        req.bin_session_id = cli.cli_bin_session_id
        req.platform_index = bstack11l1lllll1_opy_
        req.ref = instance.ref()
        req.user_input_params = json.dumps({bstack1l1111l_opy_ (u"ࠩ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨ᯻"): True}).encode(bstack1l1111l_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤ᯼"))
        req.client_worker_id = bstack1l1111l_opy_ (u"ࠦࢀࢃ࠭ࡼࡿࠥ᯽").format(threading.get_ident(), os.getpid())
        logger.debug(bstack1l1111l_opy_ (u"ࠧࡩࡡ࡭࡮ࡢࡨࡷ࡯ࡶࡦࡴࡢ࡭ࡳ࡯ࡴࡠࡨࡵࡳࡲࡥ࡭ࡰࡦࡢࡴࡴࡶࡥ࡯࠼ࠣࡷࡪࡴࡤࡪࡰࡪࠤࡉࡸࡩࡷࡧࡵࡍࡳ࡯ࡴࠡࡴࡨࡪࡂࢁࡽࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹ࠿ࡾࢁࠧ᯾").format(
            instance.ref(), bstack11l1lllll1_opy_))
        response = cli.bstack11l1ll1lll_opy_.DriverInit(req)
        if response and response.success and response.capabilities:
            caps = json.loads(response.capabilities.decode(bstack1l1111l_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧ᯿")))
            if caps:
                bstack111l1l11l_opy_.bstack111l1llll1_opy_(instance, bstack111l1l11l_opy_.bstack1l111111l_opy_, caps)
                logger.debug(bstack1l1111l_opy_ (u"ࠢࡤࡣ࡯ࡰࡤࡪࡲࡪࡸࡨࡶࡤ࡯࡮ࡪࡶࡢࡪࡷࡵ࡭ࡠ࡯ࡲࡨࡤࡶ࡯ࡱࡧࡱ࠾ࠥࡊࡲࡪࡸࡨࡶࡎࡴࡩࡵࠢࡶࡹࡨࡩࡥࡦࡦࡨࡨ࠱ࠦࡧࡰࡶࠣࡿࢂࠦࡣࡢࡲࡤࡦ࡮ࡲࡩࡵࡻࠣ࡯ࡪࡿࡳࠣᰀ").format(len(caps)))
                return caps
        logger.debug(bstack1l1111l_opy_ (u"ࠣࡥࡤࡰࡱࡥࡤࡳ࡫ࡹࡩࡷࡥࡩ࡯࡫ࡷࡣ࡫ࡸ࡯࡮ࡡࡰࡳࡩࡥࡰࡰࡲࡨࡲ࠿ࠦࡄࡳ࡫ࡹࡩࡷࡏ࡮ࡪࡶࠣࡶࡪࡺࡵࡳࡰࡨࡨࠥࡹࡵࡤࡥࡨࡷࡸࡃࡆࡢ࡮ࡶࡩࠥࡵࡲࠡࡰࡲࠤࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥᰁ"))
        return None
    except Exception as e:
        logger.debug(bstack1l1111l_opy_ (u"ࠤࡦࡥࡱࡲ࡟ࡥࡴ࡬ࡺࡪࡸ࡟ࡪࡰ࡬ࡸࡤ࡬ࡲࡰ࡯ࡢࡱࡴࡪ࡟ࡱࡱࡳࡩࡳࡀࠠࡧࡣ࡬ࡰࡪࡪ࠺ࠡࡽࢀࠦᰂ").format(e))
        return None