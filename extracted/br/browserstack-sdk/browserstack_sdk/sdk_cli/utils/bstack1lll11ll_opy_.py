# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack1ll1lll_opy_ (bstack11l11_opy_):
    global bstack11l1ll1_opy_
    bstack11l1111_opy_ = ord (bstack11l11_opy_ [-1])
    bstack1l111l1_opy_ = bstack11l11_opy_ [:-1]
    bstack111_opy_ = bstack11l1111_opy_ % len (bstack1l111l1_opy_)
    bstack11111l1_opy_ = bstack1l111l1_opy_ [:bstack111_opy_] + bstack1l111l1_opy_ [bstack111_opy_:]
    if bstack1ll1l1l_opy_:
        bstack11llll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    else:
        bstack11llll_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    return eval (bstack11llll_opy_)
import os
from bstack_utils.logger_utils import get_logger
logger = get_logger(__name__)
def bstack1ll1l1l1_opy_(bstack111111lll1_opy_):
    bstack1ll1lll_opy_ (u"ࠦࠧࠨࡃࡢ࡮࡯ࠤࡉࡸࡩࡷࡧࡵࡍࡳ࡯ࡴࠡࡩࡕࡔࡈࠦࡴࡰࠢࡪࡩࡹࠦࡢࡢࡥ࡮ࡩࡳࡪ࠭ࡳࡧࡶࡳࡱࡼࡥࡥࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳ࠯ࠢࡕࡩࡹࡻࡲ࡯ࡵࠣࡨ࡮ࡩࡴࠡࡱࡵࠤࡓࡵ࡮ࡦ࠰ࠥࠦࠧ᧩")
    try:
        from browserstack_sdk.sdk_cli.cli import cli
        from browserstack_sdk.sdk_cli.bstack1ll11ll1_opy_ import bstack111lll11l_opy_
        from browserstack_sdk.sdk_cli.bstack11llll11l1_opy_ import bstack11ll1l1l_opy_
        from browserstack_sdk import sdk_pb2 as structs
        import json
        import threading
        if not cli.bstack1l1ll1l1ll1_opy_ or not cli.cli_bin_session_id:
            logger.debug(bstack1ll1lll_opy_ (u"ࠧࡩࡡ࡭࡮ࡢࡨࡷ࡯ࡶࡦࡴࡢ࡭ࡳ࡯ࡴࡠࡨࡵࡳࡲࡥ࡭ࡰࡦࡢࡴࡴࡶࡥ࡯࠼ࠣࡧࡱ࡯ࠠ࡯ࡱࡷࠤࡷ࡫ࡡࡥࡻ࠯ࠤࡸࡱࡩࡱࡲ࡬ࡲ࡬ࠨ᧪"))
            return None
        instance = next(iter(bstack111lll11l_opy_.bstack111llll1l_opy_.values()), None)
        if not instance:
            logger.debug(bstack1ll1lll_opy_ (u"ࠨࡣࡢ࡮࡯ࡣࡩࡸࡩࡷࡧࡵࡣ࡮ࡴࡩࡵࡡࡩࡶࡴࡳ࡟࡮ࡱࡧࡣࡵࡵࡰࡦࡰ࠽ࠤࡳࡵࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࡊࡷࡧ࡭ࡦࡹࡲࡶࡰࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠡࡨࡲࡹࡳࡪࠢ᧫"))
            return None
        req = structs.DriverInitRequest()
        req.bin_session_id = cli.cli_bin_session_id
        req.platform_index = bstack111111lll1_opy_
        req.ref = instance.ref()
        req.user_input_params = json.dumps({bstack1ll1lll_opy_ (u"ࠧࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭᧬"): True}).encode(bstack1ll1lll_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢ᧭"))
        req.client_worker_id = bstack1ll1lll_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣ᧮").format(threading.get_ident(), os.getpid())
        logger.debug(bstack1ll1lll_opy_ (u"ࠥࡧࡦࡲ࡬ࡠࡦࡵ࡭ࡻ࡫ࡲࡠ࡫ࡱ࡭ࡹࡥࡦࡳࡱࡰࡣࡲࡵࡤࡠࡲࡲࡴࡪࡴ࠺ࠡࡵࡨࡲࡩ࡯࡮ࡨࠢࡇࡶ࡮ࡼࡥࡳࡋࡱ࡭ࡹࠦࡲࡦࡨࡀࡿࢂࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾ࠽ࡼࡿࠥ᧯").format(
            instance.ref(), bstack111111lll1_opy_))
        response = cli.bstack1l1ll1l1ll1_opy_.DriverInit(req)
        if response and response.success and response.capabilities:
            caps = json.loads(response.capabilities.decode(bstack1ll1lll_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥ᧰")))
            if caps:
                bstack11ll1l1l_opy_.bstack1l1l11lll_opy_(instance, bstack11ll1l1l_opy_.bstack11111l11l_opy_, caps)
                logger.debug(bstack1ll1lll_opy_ (u"ࠧࡩࡡ࡭࡮ࡢࡨࡷ࡯ࡶࡦࡴࡢ࡭ࡳ࡯ࡴࡠࡨࡵࡳࡲࡥ࡭ࡰࡦࡢࡴࡴࡶࡥ࡯࠼ࠣࡈࡷ࡯ࡶࡦࡴࡌࡲ࡮ࡺࠠࡴࡷࡦࡧࡪ࡫ࡤࡦࡦ࠯ࠤ࡬ࡵࡴࠡࡽࢀࠤࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡹࠡ࡭ࡨࡽࡸࠨ᧱").format(len(caps)))
                return caps
        logger.debug(bstack1ll1lll_opy_ (u"ࠨࡣࡢ࡮࡯ࡣࡩࡸࡩࡷࡧࡵࡣ࡮ࡴࡩࡵࡡࡩࡶࡴࡳ࡟࡮ࡱࡧࡣࡵࡵࡰࡦࡰ࠽ࠤࡉࡸࡩࡷࡧࡵࡍࡳ࡯ࡴࠡࡴࡨࡸࡺࡸ࡮ࡦࡦࠣࡷࡺࡩࡣࡦࡵࡶࡁࡋࡧ࡬ࡴࡧࠣࡳࡷࠦ࡮ࡰࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣ᧲"))
        return None
    except Exception as e:
        logger.debug(bstack1ll1lll_opy_ (u"ࠢࡤࡣ࡯ࡰࡤࡪࡲࡪࡸࡨࡶࡤ࡯࡮ࡪࡶࡢࡪࡷࡵ࡭ࡠ࡯ࡲࡨࡤࡶ࡯ࡱࡧࡱ࠾ࠥ࡬ࡡࡪ࡮ࡨࡨ࠿ࠦࡻࡾࠤ᧳").format(e))
        return None