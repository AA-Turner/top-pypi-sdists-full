# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack1111l_opy_ = 7
def bstack111lll_opy_ (bstack1lll1l_opy_):
    global bstack1l11lll_opy_
    bstack1ll1l1_opy_ = ord (bstack1lll1l_opy_ [-1])
    bstack1ll1l11_opy_ = bstack1lll1l_opy_ [:-1]
    bstack1l_opy_ = bstack1ll1l1_opy_ % len (bstack1ll1l11_opy_)
    bstack1l11ll_opy_ = bstack1ll1l11_opy_ [:bstack1l_opy_] + bstack1ll1l11_opy_ [bstack1l_opy_:]
    if bstack111ll1_opy_:
        bstack1l1l11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    else:
        bstack1l1l11l_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    return eval (bstack1l1l11l_opy_)
import os
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack111ll1l11ll_opy_
bstack1ll1l11ll_opy_ = Config.bstack1ll11lll1l_opy_()
def bstack1111ll1l111_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack1111ll11lll_opy_(bstack1111ll1ll1l_opy_, bstack1111ll1l11l_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack1111ll1ll1l_opy_):
        with open(bstack1111ll1ll1l_opy_) as f:
            pac = PACFile(f.read())
    elif bstack1111ll1l111_opy_(bstack1111ll1ll1l_opy_):
        pac = get_pac(url=bstack1111ll1ll1l_opy_)
    else:
        raise Exception(bstack111lll_opy_ (u"ࠫࡕࡧࡣࠡࡨ࡬ࡰࡪࠦࡤࡰࡧࡶࠤࡳࡵࡴࠡࡧࡻ࡭ࡸࡺ࠺ࠡࡽࢀࠫḭ").format(bstack1111ll1ll1l_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack111lll_opy_ (u"ࠧ࠾࠮࠹࠰࠻࠲࠽ࠨḮ"), 80))
        bstack1111ll1ll11_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack1111ll1ll11_opy_ = bstack111lll_opy_ (u"࠭࠰࠯࠲࠱࠴࠳࠶ࠧḯ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack1111ll1l11l_opy_, bstack1111ll1ll11_opy_)
    return proxy_url
def bstack1l11lllll1_opy_(config):
    return bstack111lll_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪḰ") in config or bstack111lll_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬḱ") in config
def bstack11l1l1lll_opy_(config):
    if not bstack1l11lllll1_opy_(config):
        return
    if config.get(bstack111lll_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬḲ")):
        return config.get(bstack111lll_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ḳ"))
    if config.get(bstack111lll_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨḴ")):
        return config.get(bstack111lll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩḵ"))
def bstack1llll1ll11_opy_(config, bstack1111ll1l11l_opy_):
    proxy = bstack11l1l1lll_opy_(config)
    proxies = {}
    if config.get(bstack111lll_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩḶ")) or config.get(bstack111lll_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫḷ")):
        if proxy.endswith(bstack111lll_opy_ (u"ࠨ࠰ࡳࡥࡨ࠭Ḹ")):
            proxies = bstack11l111l11l_opy_(proxy, bstack1111ll1l11l_opy_)
        else:
            proxies = {
                bstack111lll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨḹ"): proxy
            }
    bstack1ll1l11ll_opy_.bstack1lll1llll1_opy_(bstack111lll_opy_ (u"ࠪࡴࡷࡵࡸࡺࡕࡨࡸࡹ࡯࡮ࡨࡵࠪḺ"), proxies)
    return proxies
def bstack11l111l11l_opy_(bstack1111ll1ll1l_opy_, bstack1111ll1l11l_opy_):
    proxies = {}
    global bstack1111ll1l1l1_opy_
    if bstack111lll_opy_ (u"ࠫࡕࡇࡃࡠࡒࡕࡓ࡝࡟ࠧḻ") in globals():
        return bstack1111ll1l1l1_opy_
    try:
        proxy = bstack1111ll11lll_opy_(bstack1111ll1ll1l_opy_, bstack1111ll1l11l_opy_)
        if bstack111lll_opy_ (u"ࠧࡊࡉࡓࡇࡆࡘࠧḼ") in proxy:
            proxies = {}
        elif bstack111lll_opy_ (u"ࠨࡈࡕࡖࡓࠦḽ") in proxy or bstack111lll_opy_ (u"ࠢࡉࡖࡗࡔࡘࠨḾ") in proxy or bstack111lll_opy_ (u"ࠣࡕࡒࡇࡐ࡙ࠢḿ") in proxy:
            bstack1111ll1l1ll_opy_ = proxy.split(bstack111lll_opy_ (u"ࠤࠣࠦṀ"))
            if bstack111lll_opy_ (u"ࠥ࠾࠴࠵ࠢṁ") in bstack111lll_opy_ (u"ࠦࠧṂ").join(bstack1111ll1l1ll_opy_[1:]):
                proxies = {
                    bstack111lll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫṃ"): bstack111lll_opy_ (u"ࠨࠢṄ").join(bstack1111ll1l1ll_opy_[1:])
                }
            else:
                proxies = {
                    bstack111lll_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭ṅ"): str(bstack1111ll1l1ll_opy_[0]).lower() + bstack111lll_opy_ (u"ࠣ࠼࠲࠳ࠧṆ") + bstack111lll_opy_ (u"ࠤࠥṇ").join(bstack1111ll1l1ll_opy_[1:])
                }
        elif bstack111lll_opy_ (u"ࠥࡔࡗࡕࡘ࡚ࠤṈ") in proxy:
            bstack1111ll1l1ll_opy_ = proxy.split(bstack111lll_opy_ (u"ࠦࠥࠨṉ"))
            if bstack111lll_opy_ (u"ࠧࡀ࠯࠰ࠤṊ") in bstack111lll_opy_ (u"ࠨࠢṋ").join(bstack1111ll1l1ll_opy_[1:]):
                proxies = {
                    bstack111lll_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭Ṍ"): bstack111lll_opy_ (u"ࠣࠤṍ").join(bstack1111ll1l1ll_opy_[1:])
                }
            else:
                proxies = {
                    bstack111lll_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨṎ"): bstack111lll_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦṏ") + bstack111lll_opy_ (u"ࠦࠧṐ").join(bstack1111ll1l1ll_opy_[1:])
                }
        else:
            proxies = {
                bstack111lll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫṑ"): proxy
            }
    except Exception as e:
        print(bstack111lll_opy_ (u"ࠨࡳࡰ࡯ࡨࠤࡪࡸࡲࡰࡴࠥṒ"), bstack111ll1l11ll_opy_.format(bstack1111ll1ll1l_opy_, str(e)))
    bstack1111ll1l1l1_opy_ = proxies
    return proxies