# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack1l1lll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack1l1l1l1_opy_ (bstack1111l11_opy_):
    global bstack11l111_opy_
    bstack11ll1l_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1l111_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l11l_opy_ = bstack11ll1l_opy_ % len (bstack1l111_opy_)
    bstack1ll11l_opy_ = bstack1l111_opy_ [:bstack1l11l_opy_] + bstack1l111_opy_ [bstack1l11l_opy_:]
    if bstack11llll_opy_:
        bstack1lll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    else:
        bstack1lll1_opy_ = str () .join ([chr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    return eval (bstack1lll1_opy_)
from bstack_utils.constants import bstack11ll1l111ll_opy_
def bstack111l1ll1_opy_(bstack11ll1l11l11_opy_):
    from browserstack_sdk.sdk_cli.cli import cli
    from bstack_utils.helper import bstack111l111l_opy_
    host = bstack111l111l_opy_(cli.config, [bstack1l1l1l1_opy_ (u"ࠦࡦࡶࡩࡴࠤᜃ"), bstack1l1l1l1_opy_ (u"ࠧࡧࡵࡵࡱࡰࡥࡹ࡫ࠢᜄ"), bstack1l1l1l1_opy_ (u"ࠨࡡࡱ࡫ࠥᜅ")], bstack11ll1l111ll_opy_) if cli.is_running() else bstack11ll1l111ll_opy_
    return bstack1l1l1l1_opy_ (u"ࠧࡼࡿ࠲ࡿࢂ࠭ᜆ").format(host, bstack11ll1l11l11_opy_)