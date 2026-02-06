# coding: UTF-8
import sys
bstack11ll1l1_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack1ll1lll_opy_ = 7
def bstack11lllll_opy_ (bstack11ll1_opy_):
    global bstack1llllll_opy_
    bstack111l_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1111l11_opy_ = bstack11ll1_opy_ [:-1]
    bstack1lllll1l_opy_ = bstack111l_opy_ % len (bstack1111l11_opy_)
    bstack1ll1ll_opy_ = bstack1111l11_opy_ [:bstack1lllll1l_opy_] + bstack1111l11_opy_ [bstack1lllll1l_opy_:]
    if bstack11ll1l1_opy_:
        bstack1l1llll_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    else:
        bstack1l1llll_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    return eval (bstack1l1llll_opy_)
from bstack_utils.constants import bstack11l11ll1lll_opy_
def bstack1l11l11ll_opy_(bstack11l11ll1ll1_opy_):
    from browserstack_sdk.sdk_cli.cli import cli
    from bstack_utils.helper import bstack1lll1l111_opy_
    host = bstack1lll1l111_opy_(cli.config, [bstack11lllll_opy_ (u"ࠨࡡࡱ࡫ࡶᢩࠦ"), bstack11lllll_opy_ (u"ࠢࡢࡷࡷࡳࡲࡧࡴࡦࠤᢪ"), bstack11lllll_opy_ (u"ࠣࡣࡳ࡭ࠧ᢫")], bstack11l11ll1lll_opy_)
    return bstack11lllll_opy_ (u"ࠩࡾࢁ࠴ࢁࡽࠨ᢬").format(host, bstack11l11ll1ll1_opy_)