# coding: UTF-8
import sys
bstack1l1l11l_opy_ = sys.version_info [0] == 2
bstack1ll11l_opy_ = 2048
bstack1l11ll1_opy_ = 7
def bstack1l1ll1_opy_ (bstack111ll1l_opy_):
    global bstack111ll1_opy_
    bstack11ll1ll_opy_ = ord (bstack111ll1l_opy_ [-1])
    bstack1l11ll_opy_ = bstack111ll1l_opy_ [:-1]
    bstack11l1l11_opy_ = bstack11ll1ll_opy_ % len (bstack1l11ll_opy_)
    bstack11ll1_opy_ = bstack1l11ll_opy_ [:bstack11l1l11_opy_] + bstack1l11ll_opy_ [bstack11l1l11_opy_:]
    if bstack1l1l11l_opy_:
        bstack111ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11l_opy_ - (bstack1l1l1ll_opy_ + bstack11ll1ll_opy_) % bstack1l11ll1_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack111ll11_opy_ = str () .join ([chr (ord (char) - bstack1ll11l_opy_ - (bstack1l1l1ll_opy_ + bstack11ll1ll_opy_) % bstack1l11ll1_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack111ll11_opy_)
from bstack_utils.constants import bstack11ll11lll1l_opy_
def bstack1l11l1l1_opy_(bstack11ll11llll1_opy_):
    from browserstack_sdk.sdk_cli.cli import cli
    from bstack_utils.helper import bstack111lll1l1_opy_
    host = bstack111lll1l1_opy_(cli.config, [bstack1l1ll1_opy_ (u"ࠣࡣࡳ࡭ࡸࠨᜣ"), bstack1l1ll1_opy_ (u"ࠤࡤࡹࡹࡵ࡭ࡢࡶࡨࠦᜤ"), bstack1l1ll1_opy_ (u"ࠥࡥࡵ࡯ࠢᜥ")], bstack11ll11lll1l_opy_)
    return bstack1l1ll1_opy_ (u"ࠫࢀࢃ࠯ࡼࡿࠪᜦ").format(host, bstack11ll11llll1_opy_)