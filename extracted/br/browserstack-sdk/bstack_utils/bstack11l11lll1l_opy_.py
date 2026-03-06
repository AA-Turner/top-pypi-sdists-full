# coding: UTF-8
import sys
bstack1lllll_opy_ = sys.version_info [0] == 2
bstack1l1ll1_opy_ = 2048
bstack1lllll1l_opy_ = 7
def bstack1111_opy_ (bstack1l11ll1_opy_):
    global bstack1l_opy_
    bstack11lll1l_opy_ = ord (bstack1l11ll1_opy_ [-1])
    bstack1llll1_opy_ = bstack1l11ll1_opy_ [:-1]
    bstack111ll11_opy_ = bstack11lll1l_opy_ % len (bstack1llll1_opy_)
    bstack1111l_opy_ = bstack1llll1_opy_ [:bstack111ll11_opy_] + bstack1llll1_opy_ [bstack111ll11_opy_:]
    if bstack1lllll_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    return eval (bstack1llll11_opy_)
from bstack_utils.constants import bstack111llll111l_opy_
def bstack1l1ll1l1ll_opy_(bstack111llll11l1_opy_):
    from browserstack_sdk.sdk_cli.cli import cli
    from bstack_utils.helper import bstack11111l1ll_opy_
    host = bstack11111l1ll_opy_(cli.config, [bstack1111_opy_ (u"ࠨࡡࡱ࡫ࡶࠦ᪅"), bstack1111_opy_ (u"ࠢࡢࡷࡷࡳࡲࡧࡴࡦࠤ᪆"), bstack1111_opy_ (u"ࠣࡣࡳ࡭ࠧ᪇")], bstack111llll111l_opy_)
    return bstack1111_opy_ (u"ࠩࡾࢁ࠴ࢁࡽࠨ᪈").format(host, bstack111llll11l1_opy_)