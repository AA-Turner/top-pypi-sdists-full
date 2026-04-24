# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack111ll11_opy_ (bstack1111l1_opy_):
    global bstack1llll11_opy_
    bstack1ll11l1_opy_ = ord (bstack1111l1_opy_ [-1])
    bstack11ll_opy_ = bstack1111l1_opy_ [:-1]
    bstack1llll1_opy_ = bstack1ll11l1_opy_ % len (bstack11ll_opy_)
    bstack1ll1_opy_ = bstack11ll_opy_ [:bstack1llll1_opy_] + bstack11ll_opy_ [bstack1llll1_opy_:]
    if bstack11llll_opy_:
        bstack1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1l1_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1l1_opy_)
import os
from bstack_utils.logger_utils import get_logger
logger = get_logger(__name__)
def bstack1ll111111_opy_(bstack1l1ll11l1l_opy_):
    bstack111ll11_opy_ (u"ࠦࠧࠨࡃࡢ࡮࡯ࠤࡉࡸࡩࡷࡧࡵࡍࡳ࡯ࡴࠡࡩࡕࡔࡈࠦࡴࡰࠢࡪࡩࡹࠦࡢࡢࡥ࡮ࡩࡳࡪ࠭ࡳࡧࡶࡳࡱࡼࡥࡥࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳ࠯ࠢࡕࡩࡹࡻࡲ࡯ࡵࠣࡨ࡮ࡩࡴࠡࡱࡵࠤࡓࡵ࡮ࡦ࠰ࠥࠦࠧ᯶")
    try:
        from browserstack_sdk.sdk_cli.cli import cli
        from browserstack_sdk.sdk_cli.bstack1ll111l111_opy_ import bstack11ll11l1l1_opy_
        from browserstack_sdk.sdk_cli.bstack1ll1111ll_opy_ import bstack111ll11111_opy_
        from browserstack_sdk import sdk_pb2 as structs
        import json
        import threading
        if not cli.bstack1l1l1l1l1l_opy_ or not cli.cli_bin_session_id:
            logger.debug(bstack111ll11_opy_ (u"ࠧࡩࡡ࡭࡮ࡢࡨࡷ࡯ࡶࡦࡴࡢ࡭ࡳ࡯ࡴࡠࡨࡵࡳࡲࡥ࡭ࡰࡦࡢࡴࡴࡶࡥ࡯࠼ࠣࡧࡱ࡯ࠠ࡯ࡱࡷࠤࡷ࡫ࡡࡥࡻ࠯ࠤࡸࡱࡩࡱࡲ࡬ࡲ࡬ࠨ᯷"))
            return None
        instance = next(iter(bstack11ll11l1l1_opy_.bstack1111l11ll_opy_.values()), None)
        if not instance:
            logger.debug(bstack111ll11_opy_ (u"ࠨࡣࡢ࡮࡯ࡣࡩࡸࡩࡷࡧࡵࡣ࡮ࡴࡩࡵࡡࡩࡶࡴࡳ࡟࡮ࡱࡧࡣࡵࡵࡰࡦࡰ࠽ࠤࡳࡵࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࡊࡷࡧ࡭ࡦࡹࡲࡶࡰࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠡࡨࡲࡹࡳࡪࠢ᯸"))
            return None
        req = structs.DriverInitRequest()
        req.bin_session_id = cli.cli_bin_session_id
        req.platform_index = bstack1l1ll11l1l_opy_
        req.ref = instance.ref()
        req.user_input_params = json.dumps({bstack111ll11_opy_ (u"ࠧࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭᯹"): True}).encode(bstack111ll11_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢ᯺"))
        req.client_worker_id = bstack111ll11_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣ᯻").format(threading.get_ident(), os.getpid())
        logger.debug(bstack111ll11_opy_ (u"ࠥࡧࡦࡲ࡬ࡠࡦࡵ࡭ࡻ࡫ࡲࡠ࡫ࡱ࡭ࡹࡥࡦࡳࡱࡰࡣࡲࡵࡤࡠࡲࡲࡴࡪࡴ࠺ࠡࡵࡨࡲࡩ࡯࡮ࡨࠢࡇࡶ࡮ࡼࡥࡳࡋࡱ࡭ࡹࠦࡲࡦࡨࡀࡿࢂࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾ࠽ࡼࡿࠥ᯼").format(
            instance.ref(), bstack1l1ll11l1l_opy_))
        response = cli.bstack1l1l1l1l1l_opy_.DriverInit(req)
        if response and response.success and response.capabilities:
            caps = json.loads(response.capabilities.decode(bstack111ll11_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥ᯽")))
            if caps:
                bstack111ll11111_opy_.bstack11l1ll11ll_opy_(instance, bstack111ll11111_opy_.bstack1lllll1l1l_opy_, caps)
                logger.debug(bstack111ll11_opy_ (u"ࠧࡩࡡ࡭࡮ࡢࡨࡷ࡯ࡶࡦࡴࡢ࡭ࡳ࡯ࡴࡠࡨࡵࡳࡲࡥ࡭ࡰࡦࡢࡴࡴࡶࡥ࡯࠼ࠣࡈࡷ࡯ࡶࡦࡴࡌࡲ࡮ࡺࠠࡴࡷࡦࡧࡪ࡫ࡤࡦࡦ࠯ࠤ࡬ࡵࡴࠡࡽࢀࠤࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡹࠡ࡭ࡨࡽࡸࠨ᯾").format(len(caps)))
                return caps
        logger.debug(bstack111ll11_opy_ (u"ࠨࡣࡢ࡮࡯ࡣࡩࡸࡩࡷࡧࡵࡣ࡮ࡴࡩࡵࡡࡩࡶࡴࡳ࡟࡮ࡱࡧࡣࡵࡵࡰࡦࡰ࠽ࠤࡉࡸࡩࡷࡧࡵࡍࡳ࡯ࡴࠡࡴࡨࡸࡺࡸ࡮ࡦࡦࠣࡷࡺࡩࡣࡦࡵࡶࡁࡋࡧ࡬ࡴࡧࠣࡳࡷࠦ࡮ࡰࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣ᯿"))
        return None
    except Exception as e:
        logger.debug(bstack111ll11_opy_ (u"ࠢࡤࡣ࡯ࡰࡤࡪࡲࡪࡸࡨࡶࡤ࡯࡮ࡪࡶࡢࡪࡷࡵ࡭ࡠ࡯ࡲࡨࡤࡶ࡯ࡱࡧࡱ࠾ࠥ࡬ࡡࡪ࡮ࡨࡨ࠿ࠦࡻࡾࠤᰀ").format(e))
        return None