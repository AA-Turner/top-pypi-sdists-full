# coding: UTF-8
import sys
bstack11l11ll_opy_ = sys.version_info [0] == 2
bstack1l1ll11_opy_ = 2048
bstack1ll1l_opy_ = 7
def bstack1ll_opy_ (bstack1l11l1_opy_):
    global bstack1l1l1l1_opy_
    bstack111_opy_ = ord (bstack1l11l1_opy_ [-1])
    bstack11111l_opy_ = bstack1l11l1_opy_ [:-1]
    bstack11l111_opy_ = bstack111_opy_ % len (bstack11111l_opy_)
    bstack1lll11_opy_ = bstack11111l_opy_ [:bstack11l111_opy_] + bstack11111l_opy_ [bstack11l111_opy_:]
    if bstack11l11ll_opy_:
        bstack1ll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    else:
        bstack1ll1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    return eval (bstack1ll1l1_opy_)
import os
from bstack_utils.logger_utils import get_logger
logger = get_logger(__name__)
def bstack1ll1l11l1l_opy_(bstack11l11ll1_opy_):
    bstack1ll_opy_ (u"ࠢࠣࠤࡆࡥࡱࡲࠠࡅࡴ࡬ࡺࡪࡸࡉ࡯࡫ࡷࠤ࡬ࡘࡐࡄࠢࡷࡳࠥ࡭ࡥࡵࠢࡥࡥࡨࡱࡥ࡯ࡦ࠰ࡶࡪࡹ࡯࡭ࡸࡨࡨࠥࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶ࠲ࠥࡘࡥࡵࡷࡵࡲࡸࠦࡤࡪࡥࡷࠤࡴࡸࠠࡏࡱࡱࡩ࠳ࠨࠢࠣᯝ")
    try:
        from browserstack_sdk.sdk_cli.cli import cli
        from browserstack_sdk.sdk_cli.bstack11111ll111_opy_ import bstack11l1111ll_opy_
        from browserstack_sdk.sdk_cli.bstack111lll11ll_opy_ import bstack11ll1l111l_opy_
        from browserstack_sdk import sdk_pb2 as structs
        import json
        import threading
        if not cli.bstack1ll11ll11l_opy_ or not cli.cli_bin_session_id:
            logger.debug(bstack1ll_opy_ (u"ࠣࡥࡤࡰࡱࡥࡤࡳ࡫ࡹࡩࡷࡥࡩ࡯࡫ࡷࡣ࡫ࡸ࡯࡮ࡡࡰࡳࡩࡥࡰࡰࡲࡨࡲ࠿ࠦࡣ࡭࡫ࠣࡲࡴࡺࠠࡳࡧࡤࡨࡾ࠲ࠠࡴ࡭࡬ࡴࡵ࡯࡮ࡨࠤᯞ"))
            return None
        instance = next(iter(bstack11l1111ll_opy_.bstack1l111l11l_opy_.values()), None)
        if not instance:
            logger.debug(bstack1ll_opy_ (u"ࠤࡦࡥࡱࡲ࡟ࡥࡴ࡬ࡺࡪࡸ࡟ࡪࡰ࡬ࡸࡤ࡬ࡲࡰ࡯ࡢࡱࡴࡪ࡟ࡱࡱࡳࡩࡳࡀࠠ࡯ࡱࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠤ࡫ࡵࡵ࡯ࡦࠥᯟ"))
            return None
        req = structs.DriverInitRequest()
        req.bin_session_id = cli.cli_bin_session_id
        req.platform_index = bstack11l11ll1_opy_
        req.ref = instance.ref()
        req.user_input_params = json.dumps({bstack1ll_opy_ (u"ࠪ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩᯠ"): True}).encode(bstack1ll_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥᯡ"))
        req.client_worker_id = bstack1ll_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦᯢ").format(threading.get_ident(), os.getpid())
        logger.debug(bstack1ll_opy_ (u"ࠨࡣࡢ࡮࡯ࡣࡩࡸࡩࡷࡧࡵࡣ࡮ࡴࡩࡵࡡࡩࡶࡴࡳ࡟࡮ࡱࡧࡣࡵࡵࡰࡦࡰ࠽ࠤࡸ࡫࡮ࡥ࡫ࡱ࡫ࠥࡊࡲࡪࡸࡨࡶࡎࡴࡩࡵࠢࡵࡩ࡫ࡃࡻࡾࠢࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࡀࡿࢂࠨᯣ").format(
            instance.ref(), bstack11l11ll1_opy_))
        response = cli.bstack1ll11ll11l_opy_.DriverInit(req)
        if response and response.success and response.capabilities:
            caps = json.loads(response.capabilities.decode(bstack1ll_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨᯤ")))
            if caps:
                bstack11ll1l111l_opy_.bstack1l1l1l1l_opy_(instance, bstack11ll1l111l_opy_.bstack11l1111l1l_opy_, caps)
                logger.debug(bstack1ll_opy_ (u"ࠣࡥࡤࡰࡱࡥࡤࡳ࡫ࡹࡩࡷࡥࡩ࡯࡫ࡷࡣ࡫ࡸ࡯࡮ࡡࡰࡳࡩࡥࡰࡰࡲࡨࡲ࠿ࠦࡄࡳ࡫ࡹࡩࡷࡏ࡮ࡪࡶࠣࡷࡺࡩࡣࡦࡧࡧࡩࡩ࠲ࠠࡨࡱࡷࠤࢀࢃࠠࡤࡣࡳࡥࡧ࡯࡬ࡪࡶࡼࠤࡰ࡫ࡹࡴࠤᯥ").format(len(caps)))
                return caps
        logger.debug(bstack1ll_opy_ (u"ࠤࡦࡥࡱࡲ࡟ࡥࡴ࡬ࡺࡪࡸ࡟ࡪࡰ࡬ࡸࡤ࡬ࡲࡰ࡯ࡢࡱࡴࡪ࡟ࡱࡱࡳࡩࡳࡀࠠࡅࡴ࡬ࡺࡪࡸࡉ࡯࡫ࡷࠤࡷ࡫ࡴࡶࡴࡱࡩࡩࠦࡳࡶࡥࡦࡩࡸࡹ࠽ࡇࡣ࡯ࡷࡪࠦ࡯ࡳࠢࡱࡳࠥࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶ᯦ࠦ"))
        return None
    except Exception as e:
        logger.debug(bstack1ll_opy_ (u"ࠥࡧࡦࡲ࡬ࡠࡦࡵ࡭ࡻ࡫ࡲࡠ࡫ࡱ࡭ࡹࡥࡦࡳࡱࡰࡣࡲࡵࡤࡠࡲࡲࡴࡪࡴ࠺ࠡࡨࡤ࡭ࡱ࡫ࡤ࠻ࠢࡾࢁࠧᯧ").format(e))
        return None