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
from bstack_utils.constants import bstack1111l11llll_opy_
def bstack1111ll1ll1_opy_(bstack1111l1l1111_opy_):
    from browserstack_sdk.sdk_cli.cli import cli
    from bstack_utils.helper import bstack1l111l1ll1_opy_
    host = bstack1l111l1ll1_opy_(cli.config, [bstack1ll1l11_opy_ (u"ࠣࡣࡳ࡭ࡸࠨᶂ"), bstack1ll1l11_opy_ (u"ࠤࡤࡹࡹࡵ࡭ࡢࡶࡨࠦᶃ"), bstack1ll1l11_opy_ (u"ࠥࡥࡵ࡯ࠢᶄ")], bstack1111l11llll_opy_)
    return bstack1ll1l11_opy_ (u"ࠫࢀࢃ࠯ࡼࡿࠪᶅ").format(host, bstack1111l1l1111_opy_)