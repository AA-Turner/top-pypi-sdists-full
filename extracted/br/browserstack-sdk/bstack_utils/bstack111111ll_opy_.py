# coding: UTF-8
import sys
bstack1llllll1_opy_ = sys.version_info [0] == 2
bstack11l1l1l_opy_ = 2048
bstack1ll111_opy_ = 7
def bstack111l111_opy_ (bstack11ll1_opy_):
    global bstack11111_opy_
    bstack1111l11_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1ll11l1_opy_ = bstack11ll1_opy_ [:-1]
    bstack1111ll_opy_ = bstack1111l11_opy_ % len (bstack1ll11l1_opy_)
    bstack1lll1_opy_ = bstack1ll11l1_opy_ [:bstack1111ll_opy_] + bstack1ll11l1_opy_ [bstack1111ll_opy_:]
    if bstack1llllll1_opy_:
        bstack1l1ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    else:
        bstack1l1ll11_opy_ = str () .join ([chr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    return eval (bstack1l1ll11_opy_)
from bstack_utils.constants import bstack11ll11l11ll_opy_
def bstack1ll1l1ll_opy_(bstack11ll11l1l11_opy_):
    from browserstack_sdk.sdk_cli.cli import cli
    from bstack_utils.helper import bstack1l1ll11l1_opy_
    host = bstack1l1ll11l1_opy_(cli.config, [bstack111l111_opy_ (u"ࠦࡦࡶࡩࡴࠤᝥ"), bstack111l111_opy_ (u"ࠧࡧࡵࡵࡱࡰࡥࡹ࡫ࠢᝦ"), bstack111l111_opy_ (u"ࠨࡡࡱ࡫ࠥᝧ")], bstack11ll11l11ll_opy_)
    return bstack111l111_opy_ (u"ࠧࡼࡿ࠲ࡿࢂ࠭ᝨ").format(host, bstack11ll11l1l11_opy_)