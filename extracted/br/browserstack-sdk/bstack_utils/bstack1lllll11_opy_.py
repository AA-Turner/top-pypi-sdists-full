# coding: UTF-8
import sys
bstack1111l11_opy_ = sys.version_info [0] == 2
bstack1lll1l_opy_ = 2048
bstack1l11111_opy_ = 7
def bstack1l1_opy_ (bstack1lll_opy_):
    global bstack111l1l_opy_
    bstack1l11lll_opy_ = ord (bstack1lll_opy_ [-1])
    bstack1l11ll1_opy_ = bstack1lll_opy_ [:-1]
    bstack11llll1_opy_ = bstack1l11lll_opy_ % len (bstack1l11ll1_opy_)
    bstack1l1ll11_opy_ = bstack1l11ll1_opy_ [:bstack11llll1_opy_] + bstack1l11ll1_opy_ [bstack11llll1_opy_:]
    if bstack1111l11_opy_:
        bstack11l1ll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1l_opy_ - (bstack1ll1_opy_ + bstack1l11lll_opy_) % bstack1l11111_opy_) for bstack1ll1_opy_, char in enumerate (bstack1l1ll11_opy_)])
    else:
        bstack11l1ll_opy_ = str () .join ([chr (ord (char) - bstack1lll1l_opy_ - (bstack1ll1_opy_ + bstack1l11lll_opy_) % bstack1l11111_opy_) for bstack1ll1_opy_, char in enumerate (bstack1l1ll11_opy_)])
    return eval (bstack11l1ll_opy_)
from bstack_utils.constants import bstack11ll11ll11l_opy_
def bstack1l11ll1l1l_opy_(bstack11ll11ll111_opy_):
    from browserstack_sdk.sdk_cli.cli import cli
    from bstack_utils.helper import bstack1l1l1111ll_opy_
    host = bstack1l1l1111ll_opy_(cli.config, [bstack1l1_opy_ (u"ࠢࡢࡲ࡬ࡷࠧ᝚"), bstack1l1_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵࡧࠥ᝛"), bstack1l1_opy_ (u"ࠤࡤࡴ࡮ࠨ᝜")], bstack11ll11ll11l_opy_)
    return bstack1l1_opy_ (u"ࠪࡿࢂ࠵ࡻࡾࠩ᝝").format(host, bstack11ll11ll111_opy_)