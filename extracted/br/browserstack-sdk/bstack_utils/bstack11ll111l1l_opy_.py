# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1ll1111_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll1l1_opy_ (bstack1lll1ll_opy_):
    global bstack1l1l111_opy_
    bstack1l1111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1lll11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack1l1llll_opy_ = bstack1l1111l_opy_ % len (bstack1lll11_opy_)
    bstack11l111l_opy_ = bstack1lll11_opy_ [:bstack1l1llll_opy_] + bstack1lll11_opy_ [bstack1l1llll_opy_:]
    if bstack1l111l_opy_:
        bstack111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    else:
        bstack111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    return eval (bstack111l1l_opy_)
from bstack_utils.constants import bstack11ll11lll1l_opy_
def bstack111l11ll_opy_(bstack11ll11lll11_opy_):
    from browserstack_sdk.sdk_cli.cli import cli
    from bstack_utils.helper import bstack11l111lll1_opy_
    host = bstack11l111lll1_opy_(cli.config, [bstack11ll1l1_opy_ (u"ࠣࡣࡳ࡭ࡸࠨᜣ"), bstack11ll1l1_opy_ (u"ࠤࡤࡹࡹࡵ࡭ࡢࡶࡨࠦᜤ"), bstack11ll1l1_opy_ (u"ࠥࡥࡵ࡯ࠢᜥ")], bstack11ll11lll1l_opy_)
    return bstack11ll1l1_opy_ (u"ࠫࢀࢃ࠯ࡼࡿࠪᜦ").format(host, bstack11ll11lll11_opy_)