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
from bstack_utils.constants import bstack1111l111lll_opy_
def bstack11111l1ll_opy_(bstack1111l11l111_opy_):
    from browserstack_sdk.sdk_cli.cli import cli
    from bstack_utils.helper import bstack11ll1lll11_opy_
    host = bstack11ll1lll11_opy_(cli.config, [bstack111ll11_opy_ (u"ࠤࡤࡴ࡮ࡹࠢᶟ"), bstack111ll11_opy_ (u"ࠥࡥࡺࡺ࡯࡮ࡣࡷࡩࠧᶠ"), bstack111ll11_opy_ (u"ࠦࡦࡶࡩࠣᶡ")], bstack1111l111lll_opy_)
    return bstack111ll11_opy_ (u"ࠬࢁࡽ࠰ࡽࢀࠫᶢ").format(host, bstack1111l11l111_opy_)