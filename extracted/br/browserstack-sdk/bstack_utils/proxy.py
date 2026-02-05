# coding: UTF-8
import sys
bstack11111l_opy_ = sys.version_info [0] == 2
bstack1111_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack11l1ll1_opy_ (bstack111ll_opy_):
    global bstack11lll11_opy_
    bstack11111l1_opy_ = ord (bstack111ll_opy_ [-1])
    bstack1l11l1l_opy_ = bstack111ll_opy_ [:-1]
    bstack1111l1_opy_ = bstack11111l1_opy_ % len (bstack1l11l1l_opy_)
    bstack111ll1_opy_ = bstack1l11l1l_opy_ [:bstack1111l1_opy_] + bstack1l11l1l_opy_ [bstack1111l1_opy_:]
    if bstack11111l_opy_:
        bstack1llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    else:
        bstack1llll1_opy_ = str () .join ([chr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    return eval (bstack1llll1_opy_)
import os
import time
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack1111l111111_opy_
from bstack_utils import bstack1l1111l1l_opy_
bstack11lll111l_opy_ = Config.bstack1l11l11l1_opy_()
logger = bstack1l1111l1l_opy_.get_logger(__name__, bstack1l1111l1l_opy_.bstack1lll111l11l_opy_())
def bstack1llll11l11ll_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack1llll11l111l_opy_(bstack1llll11l11l1_opy_, bstack1llll11l1l11_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack1llll11l11l1_opy_):
        with open(bstack1llll11l11l1_opy_) as f:
            pac = PACFile(f.read())
    elif bstack1llll11l11ll_opy_(bstack1llll11l11l1_opy_):
        pac = get_pac(url=bstack1llll11l11l1_opy_)
    else:
        raise Exception(bstack11l1ll1_opy_ (u"ࠨࡒࡤࡧࠥ࡬ࡩ࡭ࡧࠣࡨࡴ࡫ࡳࠡࡰࡲࡸࠥ࡫ࡸࡪࡵࡷ࠾ࠥࢁࡽࠨ⃑").format(bstack1llll11l11l1_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack11l1ll1_opy_ (u"ࠤ࠻࠲࠽࠴࠸࠯࠺⃒ࠥ"), 80))
        bstack1llll11l1l1l_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack1llll11l1l1l_opy_ = bstack11l1ll1_opy_ (u"ࠪ࠴࠳࠶࠮࠱࠰࠳⃓ࠫ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack1llll11l1l11_opy_, bstack1llll11l1l1l_opy_)
    return proxy_url
def bstack1l1l1l111_opy_(config):
    return bstack11l1ll1_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧ⃔") in config or bstack11l1ll1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ⃕") in config
def bstack11l11lll1l_opy_(config):
    if not bstack1l1l1l111_opy_(config):
        return
    if config.get(bstack11l1ll1_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩ⃖")):
        return config.get(bstack11l1ll1_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪ⃗"))
    if config.get(bstack11l1ll1_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽ⃘ࠬ")):
        return config.get(bstack11l1ll1_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ⃙࠭"))
def bstack11l1lll111_opy_(config, bstack1llll11l1l11_opy_):
    proxy = bstack11l11lll1l_opy_(config)
    proxies = {}
    if config.get(bstack11l1ll1_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ⃚࠭")) or config.get(bstack11l1ll1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨ⃛")):
        if proxy.endswith(bstack11l1ll1_opy_ (u"ࠬ࠴ࡰࡢࡥࠪ⃜")):
            proxies = bstack11l11l1l1_opy_(proxy, bstack1llll11l1l11_opy_)
        else:
            proxies = {
                bstack11l1ll1_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬ⃝"): proxy
            }
    bstack11lll111l_opy_.bstack1l1l1111ll_opy_(bstack11l1ll1_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡙ࡥࡵࡶ࡬ࡲ࡬ࡹࠧ⃞"), proxies)
    return proxies
def bstack11l11l1l1_opy_(bstack1llll11l11l1_opy_, bstack1llll11l1l11_opy_):
    proxies = {}
    global bstack1llll11l1111_opy_
    if bstack11l1ll1_opy_ (u"ࠨࡒࡄࡇࡤࡖࡒࡐ࡚࡜ࠫ⃟") in globals():
        return bstack1llll11l1111_opy_
    try:
        proxy = bstack1llll11l111l_opy_(bstack1llll11l11l1_opy_, bstack1llll11l1l11_opy_)
        if bstack11l1ll1_opy_ (u"ࠤࡇࡍࡗࡋࡃࡕࠤ⃠") in proxy:
            proxies = {}
        elif bstack11l1ll1_opy_ (u"ࠥࡌ࡙࡚ࡐࠣ⃡") in proxy or bstack11l1ll1_opy_ (u"ࠦࡍ࡚ࡔࡑࡕࠥ⃢") in proxy or bstack11l1ll1_opy_ (u"࡙ࠧࡏࡄࡍࡖࠦ⃣") in proxy:
            bstack1llll11l1ll1_opy_ = proxy.split(bstack11l1ll1_opy_ (u"ࠨࠠࠣ⃤"))
            if bstack11l1ll1_opy_ (u"ࠢ࠻࠱࠲⃥ࠦ") in bstack11l1ll1_opy_ (u"ࠣࠤ⃦").join(bstack1llll11l1ll1_opy_[1:]):
                proxies = {
                    bstack11l1ll1_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨ⃧"): bstack11l1ll1_opy_ (u"⃨ࠥࠦ").join(bstack1llll11l1ll1_opy_[1:])
                }
            else:
                proxies = {
                    bstack11l1ll1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪ⃩"): str(bstack1llll11l1ll1_opy_[0]).lower() + bstack11l1ll1_opy_ (u"ࠧࡀ࠯࠰ࠤ⃪") + bstack11l1ll1_opy_ (u"ࠨ⃫ࠢ").join(bstack1llll11l1ll1_opy_[1:])
                }
        elif bstack11l1ll1_opy_ (u"ࠢࡑࡔࡒ࡜࡞ࠨ⃬") in proxy:
            bstack1llll11l1ll1_opy_ = proxy.split(bstack11l1ll1_opy_ (u"⃭ࠣࠢࠥ"))
            if bstack11l1ll1_opy_ (u"ࠤ࠽࠳࠴ࠨ⃮") in bstack11l1ll1_opy_ (u"⃯ࠥࠦ").join(bstack1llll11l1ll1_opy_[1:]):
                proxies = {
                    bstack11l1ll1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪ⃰"): bstack11l1ll1_opy_ (u"ࠧࠨ⃱").join(bstack1llll11l1ll1_opy_[1:])
                }
            else:
                proxies = {
                    bstack11l1ll1_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬ⃲"): bstack11l1ll1_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣ⃳") + bstack11l1ll1_opy_ (u"ࠣࠤ⃴").join(bstack1llll11l1ll1_opy_[1:])
                }
        else:
            proxies = {
                bstack11l1ll1_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨ⃵"): proxy
            }
    except Exception as e:
        print(bstack11l1ll1_opy_ (u"ࠥࡷࡴࡳࡥࠡࡧࡵࡶࡴࡸࠢ⃶"), bstack1111l111111_opy_.format(bstack1llll11l11l1_opy_, str(e)))
    bstack1llll11l1111_opy_ = proxies
    return proxies