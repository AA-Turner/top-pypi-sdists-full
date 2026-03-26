# coding: UTF-8
import sys
bstack1l11lll_opy_ = sys.version_info [0] == 2
bstack11ll1ll_opy_ = 2048
bstack1111l11_opy_ = 7
def bstack1ll1lll_opy_ (bstack1l11ll_opy_):
    global bstack1lllll1_opy_
    bstack11llll_opy_ = ord (bstack1l11ll_opy_ [-1])
    bstack111l1ll_opy_ = bstack1l11ll_opy_ [:-1]
    bstack1ll1111_opy_ = bstack11llll_opy_ % len (bstack111l1ll_opy_)
    bstack1ll1l1_opy_ = bstack111l1ll_opy_ [:bstack1ll1111_opy_] + bstack111l1ll_opy_ [bstack1ll1111_opy_:]
    if bstack1l11lll_opy_:
        bstack11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    else:
        bstack11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    return eval (bstack11l1l_opy_)
from bstack_utils.constants import bstack111l1lll11l_opy_
def bstack1l11l1ll_opy_(bstack111l1lll111_opy_):
    from browserstack_sdk.sdk_cli.cli import cli
    from bstack_utils.helper import bstack11l11l11ll_opy_
    host = bstack11l11l11ll_opy_(cli.config, [bstack1ll1lll_opy_ (u"ࠦࡦࡶࡩࡴࠤᮢ"), bstack1ll1lll_opy_ (u"ࠧࡧࡵࡵࡱࡰࡥࡹ࡫ࠢᮣ"), bstack1ll1lll_opy_ (u"ࠨࡡࡱ࡫ࠥᮤ")], bstack111l1lll11l_opy_)
    return bstack1ll1lll_opy_ (u"ࠧࡼࡿ࠲ࡿࢂ࠭ᮥ").format(host, bstack111l1lll111_opy_)