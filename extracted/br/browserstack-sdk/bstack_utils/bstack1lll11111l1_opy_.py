# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack111l11l_opy_ = 2048
bstack11l_opy_ = 7
def bstack1l1llll_opy_ (bstack11ll1l1_opy_):
    global bstack111111l_opy_
    bstack111lll_opy_ = ord (bstack11ll1l1_opy_ [-1])
    bstack11llll_opy_ = bstack11ll1l1_opy_ [:-1]
    bstack1l11_opy_ = bstack111lll_opy_ % len (bstack11llll_opy_)
    bstackl_opy_ = bstack11llll_opy_ [:bstack1l11_opy_] + bstack11llll_opy_ [bstack1l11_opy_:]
    if bstack1lll_opy_:
        bstack11l111_opy_ = unicode () .join ([unichr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    else:
        bstack11l111_opy_ = str () .join ([chr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    return eval (bstack11l111_opy_)
from bstack_utils.constants import bstack11111l11ll1_opy_
def bstack11l11111l1_opy_(bstack11111l11lll_opy_):
    from browserstack_sdk.sdk_cli.cli import cli
    from bstack_utils.helper import bstack11l11l111l_opy_
    host = bstack11l11l111l_opy_(cli.config, [bstack1l1llll_opy_ (u"ࠣࡣࡳ࡭ࡸࠨ⁨"), bstack1l1llll_opy_ (u"ࠤࡤࡹࡹࡵ࡭ࡢࡶࡨࠦ⁩"), bstack1l1llll_opy_ (u"ࠥࡥࡵ࡯ࠢ⁪")], bstack11111l11ll1_opy_)
    return bstack1l1llll_opy_ (u"ࠫࢀࢃ࠯ࡼࡿࠪ⁫").format(host, bstack11111l11lll_opy_)