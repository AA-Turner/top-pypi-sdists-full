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
import os
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack111l1llll11_opy_
bstack11lll111ll_opy_ = Config.bstack11ll1l11l_opy_()
def bstack11111ll11l1_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack11111ll1l1l_opy_(bstack11111ll1lll_opy_, bstack11111ll11ll_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack11111ll1lll_opy_):
        with open(bstack11111ll1lll_opy_) as f:
            pac = PACFile(f.read())
    elif bstack11111ll11l1_opy_(bstack11111ll1lll_opy_):
        pac = get_pac(url=bstack11111ll1lll_opy_)
    else:
        raise Exception(bstack1l1ll1_opy_ (u"ࠪࡔࡦࡩࠠࡧ࡫࡯ࡩࠥࡪ࡯ࡦࡵࠣࡲࡴࡺࠠࡦࡺ࡬ࡷࡹࡀࠠࡼࡿࠪṹ").format(bstack11111ll1lll_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack1l1ll1_opy_ (u"ࠦ࠽࠴࠸࠯࠺࠱࠼ࠧṺ"), 80))
        bstack11111ll111l_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack11111ll111l_opy_ = bstack1l1ll1_opy_ (u"ࠬ࠶࠮࠱࠰࠳࠲࠵࠭ṻ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack11111ll11ll_opy_, bstack11111ll111l_opy_)
    return proxy_url
def bstack1l1lll111l_opy_(config):
    return bstack1l1ll1_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩṼ") in config or bstack1l1ll1_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫṽ") in config
def bstack11l1lll11_opy_(config):
    if not bstack1l1lll111l_opy_(config):
        return
    if config.get(bstack1l1ll1_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫṾ")):
        return config.get(bstack1l1ll1_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬṿ"))
    if config.get(bstack1l1ll1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧẀ")):
        return config.get(bstack1l1ll1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨẁ"))
def bstack11l111ll_opy_(config, bstack11111ll11ll_opy_):
    proxy = bstack11l1lll11_opy_(config)
    proxies = {}
    if config.get(bstack1l1ll1_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨẂ")) or config.get(bstack1l1ll1_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪẃ")):
        if proxy.endswith(bstack1l1ll1_opy_ (u"ࠧ࠯ࡲࡤࡧࠬẄ")):
            proxies = bstack11l1l11ll1_opy_(proxy, bstack11111ll11ll_opy_)
        else:
            proxies = {
                bstack1l1ll1_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧẅ"): proxy
            }
    bstack11lll111ll_opy_.bstack11l1l1ll_opy_(bstack1l1ll1_opy_ (u"ࠩࡳࡶࡴࡾࡹࡔࡧࡷࡸ࡮ࡴࡧࡴࠩẆ"), proxies)
    return proxies
def bstack11l1l11ll1_opy_(bstack11111ll1lll_opy_, bstack11111ll11ll_opy_):
    proxies = {}
    global bstack11111ll1ll1_opy_
    if bstack1l1ll1_opy_ (u"ࠪࡔࡆࡉ࡟ࡑࡔࡒ࡜࡞࠭ẇ") in globals():
        return bstack11111ll1ll1_opy_
    try:
        proxy = bstack11111ll1l1l_opy_(bstack11111ll1lll_opy_, bstack11111ll11ll_opy_)
        if bstack1l1ll1_opy_ (u"ࠦࡉࡏࡒࡆࡅࡗࠦẈ") in proxy:
            proxies = {}
        elif bstack1l1ll1_opy_ (u"ࠧࡎࡔࡕࡒࠥẉ") in proxy or bstack1l1ll1_opy_ (u"ࠨࡈࡕࡖࡓࡗࠧẊ") in proxy or bstack1l1ll1_opy_ (u"ࠢࡔࡑࡆࡏࡘࠨẋ") in proxy:
            bstack11111ll1l11_opy_ = proxy.split(bstack1l1ll1_opy_ (u"ࠣࠢࠥẌ"))
            if bstack1l1ll1_opy_ (u"ࠤ࠽࠳࠴ࠨẍ") in bstack1l1ll1_opy_ (u"ࠥࠦẎ").join(bstack11111ll1l11_opy_[1:]):
                proxies = {
                    bstack1l1ll1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪẏ"): bstack1l1ll1_opy_ (u"ࠧࠨẐ").join(bstack11111ll1l11_opy_[1:])
                }
            else:
                proxies = {
                    bstack1l1ll1_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬẑ"): str(bstack11111ll1l11_opy_[0]).lower() + bstack1l1ll1_opy_ (u"ࠢ࠻࠱࠲ࠦẒ") + bstack1l1ll1_opy_ (u"ࠣࠤẓ").join(bstack11111ll1l11_opy_[1:])
                }
        elif bstack1l1ll1_opy_ (u"ࠤࡓࡖࡔ࡞࡙ࠣẔ") in proxy:
            bstack11111ll1l11_opy_ = proxy.split(bstack1l1ll1_opy_ (u"ࠥࠤࠧẕ"))
            if bstack1l1ll1_opy_ (u"ࠦ࠿࠵࠯ࠣẖ") in bstack1l1ll1_opy_ (u"ࠧࠨẗ").join(bstack11111ll1l11_opy_[1:]):
                proxies = {
                    bstack1l1ll1_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬẘ"): bstack1l1ll1_opy_ (u"ࠢࠣẙ").join(bstack11111ll1l11_opy_[1:])
                }
            else:
                proxies = {
                    bstack1l1ll1_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧẚ"): bstack1l1ll1_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥẛ") + bstack1l1ll1_opy_ (u"ࠥࠦẜ").join(bstack11111ll1l11_opy_[1:])
                }
        else:
            proxies = {
                bstack1l1ll1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪẝ"): proxy
            }
    except Exception as e:
        print(bstack1l1ll1_opy_ (u"ࠧࡹ࡯࡮ࡧࠣࡩࡷࡸ࡯ࡳࠤẞ"), bstack111l1llll11_opy_.format(bstack11111ll1lll_opy_, str(e)))
    bstack11111ll1ll1_opy_ = proxies
    return proxies