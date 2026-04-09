# coding: UTF-8
import sys
bstack11ll_opy_ = sys.version_info [0] == 2
bstack11lllll_opy_ = 2048
bstack1llll_opy_ = 7
def bstack11ll11_opy_ (bstack111l1l_opy_):
    global bstack11111ll_opy_
    bstack1llll11_opy_ = ord (bstack111l1l_opy_ [-1])
    bstack1111l11_opy_ = bstack111l1l_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1111l11_opy_)
    bstack11111l_opy_ = bstack1111l11_opy_ [:bstack111l1ll_opy_] + bstack1111l11_opy_ [bstack111l1ll_opy_:]
    if bstack11ll_opy_:
        bstack1l11lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    else:
        bstack1l11lll_opy_ = str () .join ([chr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    return eval (bstack1l11lll_opy_)
from bstack_utils.constants import bstack1111l11llll_opy_
def bstack1111l11l1_opy_(bstack1111l11lll1_opy_):
    from browserstack_sdk.sdk_cli.cli import cli
    from bstack_utils.helper import bstack11lll1lll_opy_
    host = bstack11lll1lll_opy_(cli.config, [bstack11ll11_opy_ (u"ࠤࡤࡴ࡮ࡹࠢᶃ"), bstack11ll11_opy_ (u"ࠥࡥࡺࡺ࡯࡮ࡣࡷࡩࠧᶄ"), bstack11ll11_opy_ (u"ࠦࡦࡶࡩࠣᶅ")], bstack1111l11llll_opy_)
    return bstack11ll11_opy_ (u"ࠬࢁࡽ࠰ࡽࢀࠫᶆ").format(host, bstack1111l11lll1_opy_)