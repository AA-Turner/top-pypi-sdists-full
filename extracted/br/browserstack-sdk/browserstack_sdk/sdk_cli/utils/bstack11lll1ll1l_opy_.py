# coding: UTF-8
import sys
bstack111l1l_opy_ = sys.version_info [0] == 2
bstack1111l11_opy_ = 2048
bstackl_opy_ = 7
def bstack11lll1_opy_ (bstack1l1l111_opy_):
    global bstack11l1l1_opy_
    bstack1111l_opy_ = ord (bstack1l1l111_opy_ [-1])
    bstack1l111_opy_ = bstack1l1l111_opy_ [:-1]
    bstack11111ll_opy_ = bstack1111l_opy_ % len (bstack1l111_opy_)
    bstack111l_opy_ = bstack1l111_opy_ [:bstack11111ll_opy_] + bstack1l111_opy_ [bstack11111ll_opy_:]
    if bstack111l1l_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    return eval (bstack1llll11_opy_)
import os
from bstack_utils.logger_utils import get_logger
logger = get_logger(__name__)
def bstack1l11llll_opy_(bstack11l111lll1_opy_):
    bstack11lll1_opy_ (u"ࠣࠤࠥࡇࡦࡲ࡬ࠡࡆࡵ࡭ࡻ࡫ࡲࡊࡰ࡬ࡸࠥ࡭ࡒࡑࡅࠣࡸࡴࠦࡧࡦࡶࠣࡦࡦࡩ࡫ࡦࡰࡧ࠱ࡷ࡫ࡳࡰ࡮ࡹࡩࡩࠦࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷ࠳ࠦࡒࡦࡶࡸࡶࡳࡹࠠࡥ࡫ࡦࡸࠥࡵࡲࠡࡐࡲࡲࡪ࠴ࠢࠣࠤ᧦")
    try:
        from browserstack_sdk.sdk_cli.cli import cli
        from browserstack_sdk.sdk_cli.bstack1llll1ll1l_opy_ import bstack1l1lll1111_opy_
        from browserstack_sdk.sdk_cli.bstack11l1l1ll1_opy_ import bstack1l1l11ll1l_opy_
        from browserstack_sdk import sdk_pb2 as structs
        import json
        import threading
        if not cli.bstack1l1lll11l11_opy_ or not cli.cli_bin_session_id:
            logger.debug(bstack11lll1_opy_ (u"ࠤࡦࡥࡱࡲ࡟ࡥࡴ࡬ࡺࡪࡸ࡟ࡪࡰ࡬ࡸࡤ࡬ࡲࡰ࡯ࡢࡱࡴࡪ࡟ࡱࡱࡳࡩࡳࡀࠠࡤ࡮࡬ࠤࡳࡵࡴࠡࡴࡨࡥࡩࡿࠬࠡࡵ࡮࡭ࡵࡶࡩ࡯ࡩࠥ᧧"))
            return None
        instance = next(iter(bstack1l1lll1111_opy_.bstack11l1lll111_opy_.values()), None)
        if not instance:
            logger.debug(bstack11lll1_opy_ (u"ࠥࡧࡦࡲ࡬ࡠࡦࡵ࡭ࡻ࡫ࡲࡠ࡫ࡱ࡭ࡹࡥࡦࡳࡱࡰࡣࡲࡵࡤࡠࡲࡲࡴࡪࡴ࠺ࠡࡰࡲࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠥ࡬࡯ࡶࡰࡧࠦ᧨"))
            return None
        req = structs.DriverInitRequest()
        req.bin_session_id = cli.cli_bin_session_id
        req.platform_index = bstack11l111lll1_opy_
        req.ref = instance.ref()
        req.user_input_params = json.dumps({bstack11lll1_opy_ (u"ࠫ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪ᧩"): True}).encode(bstack11lll1_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦ᧪"))
        req.client_worker_id = bstack11lll1_opy_ (u"ࠨࡻࡾ࠯ࡾࢁࠧ᧫").format(threading.get_ident(), os.getpid())
        logger.debug(bstack11lll1_opy_ (u"ࠢࡤࡣ࡯ࡰࡤࡪࡲࡪࡸࡨࡶࡤ࡯࡮ࡪࡶࡢࡪࡷࡵ࡭ࡠ࡯ࡲࡨࡤࡶ࡯ࡱࡧࡱ࠾ࠥࡹࡥ࡯ࡦ࡬ࡲ࡬ࠦࡄࡳ࡫ࡹࡩࡷࡏ࡮ࡪࡶࠣࡶࡪ࡬࠽ࡼࡿࠣࡴࡱࡧࡴࡧࡱࡵࡱࡤ࡯࡮ࡥࡧࡻࡁࢀࢃࠢ᧬").format(
            instance.ref(), bstack11l111lll1_opy_))
        response = cli.bstack1l1lll11l11_opy_.DriverInit(req)
        if response and response.success and response.capabilities:
            caps = json.loads(response.capabilities.decode(bstack11lll1_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢ᧭")))
            if caps:
                bstack1l1l11ll1l_opy_.bstack1ll1ll1l1l_opy_(instance, bstack1l1l11ll1l_opy_.bstack1l1l111l11_opy_, caps)
                logger.debug(bstack11lll1_opy_ (u"ࠤࡦࡥࡱࡲ࡟ࡥࡴ࡬ࡺࡪࡸ࡟ࡪࡰ࡬ࡸࡤ࡬ࡲࡰ࡯ࡢࡱࡴࡪ࡟ࡱࡱࡳࡩࡳࡀࠠࡅࡴ࡬ࡺࡪࡸࡉ࡯࡫ࡷࠤࡸࡻࡣࡤࡧࡨࡨࡪࡪࠬࠡࡩࡲࡸࠥࢁࡽࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷࡽࠥࡱࡥࡺࡵࠥ᧮").format(len(caps)))
                return caps
        logger.debug(bstack11lll1_opy_ (u"ࠥࡧࡦࡲ࡬ࡠࡦࡵ࡭ࡻ࡫ࡲࡠ࡫ࡱ࡭ࡹࡥࡦࡳࡱࡰࡣࡲࡵࡤࡠࡲࡲࡴࡪࡴ࠺ࠡࡆࡵ࡭ࡻ࡫ࡲࡊࡰ࡬ࡸࠥࡸࡥࡵࡷࡵࡲࡪࡪࠠࡴࡷࡦࡧࡪࡹࡳ࠾ࡈࡤࡰࡸ࡫ࠠࡰࡴࠣࡲࡴࠦࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧ᧯"))
        return None
    except Exception as e:
        logger.debug(bstack11lll1_opy_ (u"ࠦࡨࡧ࡬࡭ࡡࡧࡶ࡮ࡼࡥࡳࡡ࡬ࡲ࡮ࡺ࡟ࡧࡴࡲࡱࡤࡳ࡯ࡥࡡࡳࡳࡵ࡫࡮࠻ࠢࡩࡥ࡮ࡲࡥࡥ࠼ࠣࡿࢂࠨ᧰").format(e))
        return None