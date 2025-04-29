# coding: UTF-8
import sys
bstack11l1l1_opy_ = sys.version_info [0] == 2
bstack111l1l1_opy_ = 2048
bstack11l11ll_opy_ = 7
def bstack1llllll_opy_ (bstack1ll111l_opy_):
    global bstack1l111l_opy_
    bstack1l11l_opy_ = ord (bstack1ll111l_opy_ [-1])
    bstack1111l1l_opy_ = bstack1ll111l_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack1l11l_opy_ % len (bstack1111l1l_opy_)
    bstack1ll1_opy_ = bstack1111l1l_opy_ [:bstack11ll1ll_opy_] + bstack1111l1l_opy_ [bstack11ll1ll_opy_:]
    if bstack11l1l1_opy_:
        bstack1lllll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack111l1l1_opy_ - (bstack11ll1_opy_ + bstack1l11l_opy_) % bstack11l11ll_opy_) for bstack11ll1_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1lllll1l_opy_ = str () .join ([chr (ord (char) - bstack111l1l1_opy_ - (bstack11ll1_opy_ + bstack1l11l_opy_) % bstack11l11ll_opy_) for bstack11ll1_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1lllll1l_opy_)
import os
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack11l1111llll_opy_
bstack1l1ll1l1l1_opy_ = Config.bstack11ll1ll1l1_opy_()
def bstack111l1ll1111_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack111l1l1lll1_opy_(bstack111l1l1llll_opy_, bstack111l1ll111l_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack111l1l1llll_opy_):
        with open(bstack111l1l1llll_opy_) as f:
            pac = PACFile(f.read())
    elif bstack111l1ll1111_opy_(bstack111l1l1llll_opy_):
        pac = get_pac(url=bstack111l1l1llll_opy_)
    else:
        raise Exception(bstack1llllll_opy_ (u"࠭ࡐࡢࡥࠣࡪ࡮ࡲࡥࠡࡦࡲࡩࡸࠦ࡮ࡰࡶࠣࡩࡽ࡯ࡳࡵ࠼ࠣࡿࢂ࠭ᴞ").format(bstack111l1l1llll_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack1llllll_opy_ (u"ࠢ࠹࠰࠻࠲࠽࠴࠸ࠣᴟ"), 80))
        bstack111l1ll11ll_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack111l1ll11ll_opy_ = bstack1llllll_opy_ (u"ࠨ࠲࠱࠴࠳࠶࠮࠱ࠩᴠ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack111l1ll111l_opy_, bstack111l1ll11ll_opy_)
    return proxy_url
def bstack1l1l1l111l_opy_(config):
    return bstack1llllll_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬᴡ") in config or bstack1llllll_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧᴢ") in config
def bstack1l111ll11l_opy_(config):
    if not bstack1l1l1l111l_opy_(config):
        return
    if config.get(bstack1llllll_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧᴣ")):
        return config.get(bstack1llllll_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨᴤ"))
    if config.get(bstack1llllll_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪᴥ")):
        return config.get(bstack1llllll_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫᴦ"))
def bstack11111111_opy_(config, bstack111l1ll111l_opy_):
    proxy = bstack1l111ll11l_opy_(config)
    proxies = {}
    if config.get(bstack1llllll_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫᴧ")) or config.get(bstack1llllll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ᴨ")):
        if proxy.endswith(bstack1llllll_opy_ (u"ࠪ࠲ࡵࡧࡣࠨᴩ")):
            proxies = bstack11l11lllll_opy_(proxy, bstack111l1ll111l_opy_)
        else:
            proxies = {
                bstack1llllll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪᴪ"): proxy
            }
    bstack1l1ll1l1l1_opy_.bstack1ll1l11ll1_opy_(bstack1llllll_opy_ (u"ࠬࡶࡲࡰࡺࡼࡗࡪࡺࡴࡪࡰࡪࡷࠬᴫ"), proxies)
    return proxies
def bstack11l11lllll_opy_(bstack111l1l1llll_opy_, bstack111l1ll111l_opy_):
    proxies = {}
    global bstack111l1ll11l1_opy_
    if bstack1llllll_opy_ (u"࠭ࡐࡂࡅࡢࡔࡗࡕࡘ࡚ࠩᴬ") in globals():
        return bstack111l1ll11l1_opy_
    try:
        proxy = bstack111l1l1lll1_opy_(bstack111l1l1llll_opy_, bstack111l1ll111l_opy_)
        if bstack1llllll_opy_ (u"ࠢࡅࡋࡕࡉࡈ࡚ࠢᴭ") in proxy:
            proxies = {}
        elif bstack1llllll_opy_ (u"ࠣࡊࡗࡘࡕࠨᴮ") in proxy or bstack1llllll_opy_ (u"ࠤࡋࡘ࡙ࡖࡓࠣᴯ") in proxy or bstack1llllll_opy_ (u"ࠥࡗࡔࡉࡋࡔࠤᴰ") in proxy:
            bstack111l1ll1l11_opy_ = proxy.split(bstack1llllll_opy_ (u"ࠦࠥࠨᴱ"))
            if bstack1llllll_opy_ (u"ࠧࡀ࠯࠰ࠤᴲ") in bstack1llllll_opy_ (u"ࠨࠢᴳ").join(bstack111l1ll1l11_opy_[1:]):
                proxies = {
                    bstack1llllll_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭ᴴ"): bstack1llllll_opy_ (u"ࠣࠤᴵ").join(bstack111l1ll1l11_opy_[1:])
                }
            else:
                proxies = {
                    bstack1llllll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨᴶ"): str(bstack111l1ll1l11_opy_[0]).lower() + bstack1llllll_opy_ (u"ࠥ࠾࠴࠵ࠢᴷ") + bstack1llllll_opy_ (u"ࠦࠧᴸ").join(bstack111l1ll1l11_opy_[1:])
                }
        elif bstack1llllll_opy_ (u"ࠧࡖࡒࡐ࡚࡜ࠦᴹ") in proxy:
            bstack111l1ll1l11_opy_ = proxy.split(bstack1llllll_opy_ (u"ࠨࠠࠣᴺ"))
            if bstack1llllll_opy_ (u"ࠢ࠻࠱࠲ࠦᴻ") in bstack1llllll_opy_ (u"ࠣࠤᴼ").join(bstack111l1ll1l11_opy_[1:]):
                proxies = {
                    bstack1llllll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨᴽ"): bstack1llllll_opy_ (u"ࠥࠦᴾ").join(bstack111l1ll1l11_opy_[1:])
                }
            else:
                proxies = {
                    bstack1llllll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪᴿ"): bstack1llllll_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨᵀ") + bstack1llllll_opy_ (u"ࠨࠢᵁ").join(bstack111l1ll1l11_opy_[1:])
                }
        else:
            proxies = {
                bstack1llllll_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭ᵂ"): proxy
            }
    except Exception as e:
        print(bstack1llllll_opy_ (u"ࠣࡵࡲࡱࡪࠦࡥࡳࡴࡲࡶࠧᵃ"), bstack11l1111llll_opy_.format(bstack111l1l1llll_opy_, str(e)))
    bstack111l1ll11l1_opy_ = proxies
    return proxies