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
from bstack_utils.constants import bstack1111l11l111_opy_
def bstack111l1l1l1l_opy_(bstack1111l111lll_opy_):
    from browserstack_sdk.sdk_cli.cli import cli
    from bstack_utils.helper import bstack111lll1ll_opy_
    host = bstack111lll1ll_opy_(cli.config, [bstack1l111l_opy_ (u"ࠤࡤࡴ࡮ࡹࠢᶟ"), bstack1l111l_opy_ (u"ࠥࡥࡺࡺ࡯࡮ࡣࡷࡩࠧᶠ"), bstack1l111l_opy_ (u"ࠦࡦࡶࡩࠣᶡ")], bstack1111l11l111_opy_)
    return bstack1l111l_opy_ (u"ࠬࢁࡽ࠰ࡽࢀࠫᶢ").format(host, bstack1111l111lll_opy_)