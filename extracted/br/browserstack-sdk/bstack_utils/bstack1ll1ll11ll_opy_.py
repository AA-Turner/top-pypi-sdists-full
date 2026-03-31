# coding: UTF-8
import sys
bstack11lll11_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack11l1l11_opy_ = 7
def bstack1ll11_opy_ (bstack111lll1_opy_):
    global bstack1ll111l_opy_
    bstack1llll11_opy_ = ord (bstack111lll1_opy_ [-1])
    bstack1_opy_ = bstack111lll1_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1_opy_)
    bstack1l11lll_opy_ = bstack1_opy_ [:bstack111l1ll_opy_] + bstack1_opy_ [bstack111l1ll_opy_:]
    if bstack11lll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    return eval (bstack11l1111_opy_)
from bstack_utils.constants import bstack111l1ll1ll1_opy_
def bstack1llll1ll1l_opy_(bstack111l1ll1lll_opy_):
    from browserstack_sdk.sdk_cli.cli import cli
    from bstack_utils.helper import bstack1l11llll11_opy_
    host = bstack1l11llll11_opy_(cli.config, [bstack1ll11_opy_ (u"ࠢࡢࡲ࡬ࡷࠧ᮳"), bstack1ll11_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵࡧࠥ᮴"), bstack1ll11_opy_ (u"ࠤࡤࡴ࡮ࠨ᮵")], bstack111l1ll1ll1_opy_)
    return bstack1ll11_opy_ (u"ࠪࡿࢂ࠵ࡻࡾࠩ᮶").format(host, bstack111l1ll1lll_opy_)