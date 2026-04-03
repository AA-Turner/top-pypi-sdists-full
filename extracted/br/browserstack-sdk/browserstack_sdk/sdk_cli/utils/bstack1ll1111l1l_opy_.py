# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1lll_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack1ll1l11_opy_ (bstack11l1lll_opy_):
    global bstack1l11ll1_opy_
    bstack111lll_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1l11_opy_ = bstack11l1lll_opy_ [:-1]
    bstack111111_opy_ = bstack111lll_opy_ % len (bstack1l1l11_opy_)
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ [:bstack111111_opy_] + bstack1l1l11_opy_ [bstack111111_opy_:]
    if bstack1ll11_opy_:
        bstack1llllll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    else:
        bstack1llllll_opy_ = str () .join ([chr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    return eval (bstack1llllll_opy_)
import os
from bstack_utils.logger_utils import get_logger
logger = get_logger(__name__)
def bstack1l111lll_opy_(bstack11ll1l111_opy_):
    bstack1ll1l11_opy_ (u"ࠥࠦࠧࡉࡡ࡭࡮ࠣࡈࡷ࡯ࡶࡦࡴࡌࡲ࡮ࡺࠠࡨࡔࡓࡇࠥࡺ࡯ࠡࡩࡨࡸࠥࡨࡡࡤ࡭ࡨࡲࡩ࠳ࡲࡦࡵࡲࡰࡻ࡫ࡤࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹ࠮ࠡࡔࡨࡸࡺࡸ࡮ࡴࠢࡧ࡭ࡨࡺࠠࡰࡴࠣࡒࡴࡴࡥ࠯ࠤࠥࠦᯙ")
    try:
        from browserstack_sdk.sdk_cli.cli import cli
        from browserstack_sdk.sdk_cli.bstack1l1l1ll1ll_opy_ import bstack1111lll1ll_opy_
        from browserstack_sdk.sdk_cli.bstack1lll1l1l11_opy_ import bstack1l1l11ll1l_opy_
        from browserstack_sdk import sdk_pb2 as structs
        import json
        import threading
        if not cli.bstack1llll11l11_opy_ or not cli.cli_bin_session_id:
            logger.debug(bstack1ll1l11_opy_ (u"ࠦࡨࡧ࡬࡭ࡡࡧࡶ࡮ࡼࡥࡳࡡ࡬ࡲ࡮ࡺ࡟ࡧࡴࡲࡱࡤࡳ࡯ࡥࡡࡳࡳࡵ࡫࡮࠻ࠢࡦࡰ࡮ࠦ࡮ࡰࡶࠣࡶࡪࡧࡤࡺ࠮ࠣࡷࡰ࡯ࡰࡱ࡫ࡱ࡫ࠧᯚ"))
            return None
        instance = next(iter(bstack1111lll1ll_opy_.bstack11l111111_opy_.values()), None)
        if not instance:
            logger.debug(bstack1ll1l11_opy_ (u"ࠧࡩࡡ࡭࡮ࡢࡨࡷ࡯ࡶࡦࡴࡢ࡭ࡳ࡯ࡴࡠࡨࡵࡳࡲࡥ࡭ࡰࡦࡢࡴࡴࡶࡥ࡯࠼ࠣࡲࡴࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠠࡧࡱࡸࡲࡩࠨᯛ"))
            return None
        req = structs.DriverInitRequest()
        req.bin_session_id = cli.cli_bin_session_id
        req.platform_index = bstack11ll1l111_opy_
        req.ref = instance.ref()
        req.user_input_params = json.dumps({bstack1ll1l11_opy_ (u"࠭ࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬᯜ"): True}).encode(bstack1ll1l11_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨᯝ"))
        req.client_worker_id = bstack1ll1l11_opy_ (u"ࠣࡽࢀ࠱ࢀࢃࠢᯞ").format(threading.get_ident(), os.getpid())
        logger.debug(bstack1ll1l11_opy_ (u"ࠤࡦࡥࡱࡲ࡟ࡥࡴ࡬ࡺࡪࡸ࡟ࡪࡰ࡬ࡸࡤ࡬ࡲࡰ࡯ࡢࡱࡴࡪ࡟ࡱࡱࡳࡩࡳࡀࠠࡴࡧࡱࡨ࡮ࡴࡧࠡࡆࡵ࡭ࡻ࡫ࡲࡊࡰ࡬ࡸࠥࡸࡥࡧ࠿ࡾࢁࠥࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡪࡰࡧࡩࡽࡃࡻࡾࠤᯟ").format(
            instance.ref(), bstack11ll1l111_opy_))
        response = cli.bstack1llll11l11_opy_.DriverInit(req)
        if response and response.success and response.capabilities:
            caps = json.loads(response.capabilities.decode(bstack1ll1l11_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤᯠ")))
            if caps:
                bstack1l1l11ll1l_opy_.bstack1ll11l1ll_opy_(instance, bstack1l1l11ll1l_opy_.bstack11l111l11l_opy_, caps)
                logger.debug(bstack1ll1l11_opy_ (u"ࠦࡨࡧ࡬࡭ࡡࡧࡶ࡮ࡼࡥࡳࡡ࡬ࡲ࡮ࡺ࡟ࡧࡴࡲࡱࡤࡳ࡯ࡥࡡࡳࡳࡵ࡫࡮࠻ࠢࡇࡶ࡮ࡼࡥࡳࡋࡱ࡭ࡹࠦࡳࡶࡥࡦࡩࡪࡪࡥࡥ࠮ࠣ࡫ࡴࡺࠠࡼࡿࠣࡧࡦࡶࡡࡣ࡫࡯࡭ࡹࡿࠠ࡬ࡧࡼࡷࠧᯡ").format(len(caps)))
                return caps
        logger.debug(bstack1ll1l11_opy_ (u"ࠧࡩࡡ࡭࡮ࡢࡨࡷ࡯ࡶࡦࡴࡢ࡭ࡳ࡯ࡴࡠࡨࡵࡳࡲࡥ࡭ࡰࡦࡢࡴࡴࡶࡥ࡯࠼ࠣࡈࡷ࡯ࡶࡦࡴࡌࡲ࡮ࡺࠠࡳࡧࡷࡹࡷࡴࡥࡥࠢࡶࡹࡨࡩࡥࡴࡵࡀࡊࡦࡲࡳࡦࠢࡲࡶࠥࡴ࡯ࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢᯢ"))
        return None
    except Exception as e:
        logger.debug(bstack1ll1l11_opy_ (u"ࠨࡣࡢ࡮࡯ࡣࡩࡸࡩࡷࡧࡵࡣ࡮ࡴࡩࡵࡡࡩࡶࡴࡳ࡟࡮ࡱࡧࡣࡵࡵࡰࡦࡰ࠽ࠤ࡫ࡧࡩ࡭ࡧࡧ࠾ࠥࢁࡽࠣᯣ").format(e))
        return None