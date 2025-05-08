# coding: UTF-8
import sys
bstack111l1ll_opy_ = sys.version_info [0] == 2
bstack1lll11l_opy_ = 2048
bstack11111_opy_ = 7
def bstack1l1lll_opy_ (bstack11l_opy_):
    global bstack1l11l11_opy_
    bstack1_opy_ = ord (bstack11l_opy_ [-1])
    bstack1ll111l_opy_ = bstack11l_opy_ [:-1]
    bstack11l1111_opy_ = bstack1_opy_ % len (bstack1ll111l_opy_)
    bstack11l1l_opy_ = bstack1ll111l_opy_ [:bstack11l1111_opy_] + bstack1ll111l_opy_ [bstack11l1111_opy_:]
    if bstack111l1ll_opy_:
        bstack11llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11l_opy_ - (bstack1lllll_opy_ + bstack1_opy_) % bstack11111_opy_) for bstack1lllll_opy_, char in enumerate (bstack11l1l_opy_)])
    else:
        bstack11llll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11l_opy_ - (bstack1lllll_opy_ + bstack1_opy_) % bstack11111_opy_) for bstack1lllll_opy_, char in enumerate (bstack11l1l_opy_)])
    return eval (bstack11llll1_opy_)
import os
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack11l1111ll1l_opy_
bstack11l1l1l1l_opy_ = Config.bstack1l111l11l_opy_()
def bstack111l1l1lll1_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack111l1l1llll_opy_(bstack111l1ll1l11_opy_, bstack111l1ll1111_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack111l1ll1l11_opy_):
        with open(bstack111l1ll1l11_opy_) as f:
            pac = PACFile(f.read())
    elif bstack111l1l1lll1_opy_(bstack111l1ll1l11_opy_):
        pac = get_pac(url=bstack111l1ll1l11_opy_)
    else:
        raise Exception(bstack1l1lll_opy_ (u"ࠫࡕࡧࡣࠡࡨ࡬ࡰࡪࠦࡤࡰࡧࡶࠤࡳࡵࡴࠡࡧࡻ࡭ࡸࡺ࠺ࠡࡽࢀࠫᴣ").format(bstack111l1ll1l11_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack1l1lll_opy_ (u"ࠧ࠾࠮࠹࠰࠻࠲࠽ࠨᴤ"), 80))
        bstack111l1ll111l_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack111l1ll111l_opy_ = bstack1l1lll_opy_ (u"࠭࠰࠯࠲࠱࠴࠳࠶ࠧᴥ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack111l1ll1111_opy_, bstack111l1ll111l_opy_)
    return proxy_url
def bstack111lll11l_opy_(config):
    return bstack1l1lll_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪᴦ") in config or bstack1l1lll_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬᴧ") in config
def bstack1ll11lll_opy_(config):
    if not bstack111lll11l_opy_(config):
        return
    if config.get(bstack1l1lll_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬᴨ")):
        return config.get(bstack1l1lll_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ᴩ"))
    if config.get(bstack1l1lll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨᴪ")):
        return config.get(bstack1l1lll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩᴫ"))
def bstack11ll1l11l_opy_(config, bstack111l1ll1111_opy_):
    proxy = bstack1ll11lll_opy_(config)
    proxies = {}
    if config.get(bstack1l1lll_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩᴬ")) or config.get(bstack1l1lll_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫᴭ")):
        if proxy.endswith(bstack1l1lll_opy_ (u"ࠨ࠰ࡳࡥࡨ࠭ᴮ")):
            proxies = bstack11llllll_opy_(proxy, bstack111l1ll1111_opy_)
        else:
            proxies = {
                bstack1l1lll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨᴯ"): proxy
            }
    bstack11l1l1l1l_opy_.bstack1l111lll1_opy_(bstack1l1lll_opy_ (u"ࠪࡴࡷࡵࡸࡺࡕࡨࡸࡹ࡯࡮ࡨࡵࠪᴰ"), proxies)
    return proxies
def bstack11llllll_opy_(bstack111l1ll1l11_opy_, bstack111l1ll1111_opy_):
    proxies = {}
    global bstack111l1ll11ll_opy_
    if bstack1l1lll_opy_ (u"ࠫࡕࡇࡃࡠࡒࡕࡓ࡝࡟ࠧᴱ") in globals():
        return bstack111l1ll11ll_opy_
    try:
        proxy = bstack111l1l1llll_opy_(bstack111l1ll1l11_opy_, bstack111l1ll1111_opy_)
        if bstack1l1lll_opy_ (u"ࠧࡊࡉࡓࡇࡆࡘࠧᴲ") in proxy:
            proxies = {}
        elif bstack1l1lll_opy_ (u"ࠨࡈࡕࡖࡓࠦᴳ") in proxy or bstack1l1lll_opy_ (u"ࠢࡉࡖࡗࡔࡘࠨᴴ") in proxy or bstack1l1lll_opy_ (u"ࠣࡕࡒࡇࡐ࡙ࠢᴵ") in proxy:
            bstack111l1ll11l1_opy_ = proxy.split(bstack1l1lll_opy_ (u"ࠤࠣࠦᴶ"))
            if bstack1l1lll_opy_ (u"ࠥ࠾࠴࠵ࠢᴷ") in bstack1l1lll_opy_ (u"ࠦࠧᴸ").join(bstack111l1ll11l1_opy_[1:]):
                proxies = {
                    bstack1l1lll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫᴹ"): bstack1l1lll_opy_ (u"ࠨࠢᴺ").join(bstack111l1ll11l1_opy_[1:])
                }
            else:
                proxies = {
                    bstack1l1lll_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭ᴻ"): str(bstack111l1ll11l1_opy_[0]).lower() + bstack1l1lll_opy_ (u"ࠣ࠼࠲࠳ࠧᴼ") + bstack1l1lll_opy_ (u"ࠤࠥᴽ").join(bstack111l1ll11l1_opy_[1:])
                }
        elif bstack1l1lll_opy_ (u"ࠥࡔࡗࡕࡘ࡚ࠤᴾ") in proxy:
            bstack111l1ll11l1_opy_ = proxy.split(bstack1l1lll_opy_ (u"ࠦࠥࠨᴿ"))
            if bstack1l1lll_opy_ (u"ࠧࡀ࠯࠰ࠤᵀ") in bstack1l1lll_opy_ (u"ࠨࠢᵁ").join(bstack111l1ll11l1_opy_[1:]):
                proxies = {
                    bstack1l1lll_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭ᵂ"): bstack1l1lll_opy_ (u"ࠣࠤᵃ").join(bstack111l1ll11l1_opy_[1:])
                }
            else:
                proxies = {
                    bstack1l1lll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨᵄ"): bstack1l1lll_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦᵅ") + bstack1l1lll_opy_ (u"ࠦࠧᵆ").join(bstack111l1ll11l1_opy_[1:])
                }
        else:
            proxies = {
                bstack1l1lll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫᵇ"): proxy
            }
    except Exception as e:
        print(bstack1l1lll_opy_ (u"ࠨࡳࡰ࡯ࡨࠤࡪࡸࡲࡰࡴࠥᵈ"), bstack11l1111ll1l_opy_.format(bstack111l1ll1l11_opy_, str(e)))
    bstack111l1ll11ll_opy_ = proxies
    return proxies