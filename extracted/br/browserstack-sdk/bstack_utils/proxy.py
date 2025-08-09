# coding: UTF-8
import sys
bstack1ll11l_opy_ = sys.version_info [0] == 2
bstack111111l_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack11l1_opy_ (bstack1llllll1_opy_):
    global bstack1l11ll_opy_
    bstack1ll111l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1l111_opy_ = bstack1ll111l_opy_ % len (bstack1l1l1l1_opy_)
    bstack11ll1ll_opy_ = bstack1l1l1l1_opy_ [:bstack1l111_opy_] + bstack1l1l1l1_opy_ [bstack1l111_opy_:]
    if bstack1ll11l_opy_:
        bstack11l1ll_opy_ = unicode () .join ([unichr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    else:
        bstack11l1ll_opy_ = str () .join ([chr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    return eval (bstack11l1ll_opy_)
import os
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack111l1l1ll1l_opy_
bstack1l1llll1l_opy_ = Config.bstack1l1lll11l_opy_()
def bstack111111l1l1l_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack111111l1l11_opy_(bstack111111ll111_opy_, bstack111111l1ll1_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack111111ll111_opy_):
        with open(bstack111111ll111_opy_) as f:
            pac = PACFile(f.read())
    elif bstack111111l1l1l_opy_(bstack111111ll111_opy_):
        pac = get_pac(url=bstack111111ll111_opy_)
    else:
        raise Exception(bstack11l1_opy_ (u"ࠪࡔࡦࡩࠠࡧ࡫࡯ࡩࠥࡪ࡯ࡦࡵࠣࡲࡴࡺࠠࡦࡺ࡬ࡷࡹࡀࠠࡼࡿࠪἽ").format(bstack111111ll111_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack11l1_opy_ (u"ࠦ࠽࠴࠸࠯࠺࠱࠼ࠧἾ"), 80))
        bstack111111l11l1_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack111111l11l1_opy_ = bstack11l1_opy_ (u"ࠬ࠶࠮࠱࠰࠳࠲࠵࠭Ἷ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack111111l1ll1_opy_, bstack111111l11l1_opy_)
    return proxy_url
def bstack111l111l_opy_(config):
    return bstack11l1_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩὀ") in config or bstack11l1_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫὁ") in config
def bstack1ll1l1111_opy_(config):
    if not bstack111l111l_opy_(config):
        return
    if config.get(bstack11l1_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫὂ")):
        return config.get(bstack11l1_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬὃ"))
    if config.get(bstack11l1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧὄ")):
        return config.get(bstack11l1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨὅ"))
def bstack1ll1lll11l_opy_(config, bstack111111l1ll1_opy_):
    proxy = bstack1ll1l1111_opy_(config)
    proxies = {}
    if config.get(bstack11l1_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨ὆")) or config.get(bstack11l1_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪ὇")):
        if proxy.endswith(bstack11l1_opy_ (u"ࠧ࠯ࡲࡤࡧࠬὈ")):
            proxies = bstack1111l1111_opy_(proxy, bstack111111l1ll1_opy_)
        else:
            proxies = {
                bstack11l1_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧὉ"): proxy
            }
    bstack1l1llll1l_opy_.bstack11lll11l_opy_(bstack11l1_opy_ (u"ࠩࡳࡶࡴࡾࡹࡔࡧࡷࡸ࡮ࡴࡧࡴࠩὊ"), proxies)
    return proxies
def bstack1111l1111_opy_(bstack111111ll111_opy_, bstack111111l1ll1_opy_):
    proxies = {}
    global bstack111111l11ll_opy_
    if bstack11l1_opy_ (u"ࠪࡔࡆࡉ࡟ࡑࡔࡒ࡜࡞࠭Ὃ") in globals():
        return bstack111111l11ll_opy_
    try:
        proxy = bstack111111l1l11_opy_(bstack111111ll111_opy_, bstack111111l1ll1_opy_)
        if bstack11l1_opy_ (u"ࠦࡉࡏࡒࡆࡅࡗࠦὌ") in proxy:
            proxies = {}
        elif bstack11l1_opy_ (u"ࠧࡎࡔࡕࡒࠥὍ") in proxy or bstack11l1_opy_ (u"ࠨࡈࡕࡖࡓࡗࠧ὎") in proxy or bstack11l1_opy_ (u"ࠢࡔࡑࡆࡏࡘࠨ὏") in proxy:
            bstack111111l1lll_opy_ = proxy.split(bstack11l1_opy_ (u"ࠣࠢࠥὐ"))
            if bstack11l1_opy_ (u"ࠤ࠽࠳࠴ࠨὑ") in bstack11l1_opy_ (u"ࠥࠦὒ").join(bstack111111l1lll_opy_[1:]):
                proxies = {
                    bstack11l1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪὓ"): bstack11l1_opy_ (u"ࠧࠨὔ").join(bstack111111l1lll_opy_[1:])
                }
            else:
                proxies = {
                    bstack11l1_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬὕ"): str(bstack111111l1lll_opy_[0]).lower() + bstack11l1_opy_ (u"ࠢ࠻࠱࠲ࠦὖ") + bstack11l1_opy_ (u"ࠣࠤὗ").join(bstack111111l1lll_opy_[1:])
                }
        elif bstack11l1_opy_ (u"ࠤࡓࡖࡔ࡞࡙ࠣ὘") in proxy:
            bstack111111l1lll_opy_ = proxy.split(bstack11l1_opy_ (u"ࠥࠤࠧὙ"))
            if bstack11l1_opy_ (u"ࠦ࠿࠵࠯ࠣ὚") in bstack11l1_opy_ (u"ࠧࠨὛ").join(bstack111111l1lll_opy_[1:]):
                proxies = {
                    bstack11l1_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬ὜"): bstack11l1_opy_ (u"ࠢࠣὝ").join(bstack111111l1lll_opy_[1:])
                }
            else:
                proxies = {
                    bstack11l1_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧ὞"): bstack11l1_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥὟ") + bstack11l1_opy_ (u"ࠥࠦὠ").join(bstack111111l1lll_opy_[1:])
                }
        else:
            proxies = {
                bstack11l1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪὡ"): proxy
            }
    except Exception as e:
        print(bstack11l1_opy_ (u"ࠧࡹ࡯࡮ࡧࠣࡩࡷࡸ࡯ࡳࠤὢ"), bstack111l1l1ll1l_opy_.format(bstack111111ll111_opy_, str(e)))
    bstack111111l11ll_opy_ = proxies
    return proxies