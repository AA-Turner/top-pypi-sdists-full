# coding: UTF-8
import sys
bstack1llllll1_opy_ = sys.version_info [0] == 2
bstack11l1l1l_opy_ = 2048
bstack1ll111_opy_ = 7
def bstack111l111_opy_ (bstack11ll1_opy_):
    global bstack11111_opy_
    bstack1111l11_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1ll11l1_opy_ = bstack11ll1_opy_ [:-1]
    bstack1111ll_opy_ = bstack1111l11_opy_ % len (bstack1ll11l1_opy_)
    bstack1lll1_opy_ = bstack1ll11l1_opy_ [:bstack1111ll_opy_] + bstack1ll11l1_opy_ [bstack1111ll_opy_:]
    if bstack1llllll1_opy_:
        bstack1l1ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    else:
        bstack1l1ll11_opy_ = str () .join ([chr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    return eval (bstack1l1ll11_opy_)
import os
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack111l1ll1lll_opy_
bstack1ll1ll11_opy_ = Config.bstack1ll11ll1_opy_()
def bstack11111ll1111_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack11111l1ll11_opy_(bstack11111l1lll1_opy_, bstack11111l1l1ll_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack11111l1lll1_opy_):
        with open(bstack11111l1lll1_opy_) as f:
            pac = PACFile(f.read())
    elif bstack11111ll1111_opy_(bstack11111l1lll1_opy_):
        pac = get_pac(url=bstack11111l1lll1_opy_)
    else:
        raise Exception(bstack111l111_opy_ (u"ࠪࡔࡦࡩࠠࡧ࡫࡯ࡩࠥࡪ࡯ࡦࡵࠣࡲࡴࡺࠠࡦࡺ࡬ࡷࡹࡀࠠࡼࡿࠪế").format(bstack11111l1lll1_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack111l111_opy_ (u"ࠦ࠽࠴࠸࠯࠺࠱࠼ࠧỀ"), 80))
        bstack11111l1ll1l_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack11111l1ll1l_opy_ = bstack111l111_opy_ (u"ࠬ࠶࠮࠱࠰࠳࠲࠵࠭ề")
    proxy_url = session.get_pac().find_proxy_for_url(bstack11111l1l1ll_opy_, bstack11111l1ll1l_opy_)
    return proxy_url
def bstack11ll11l1_opy_(config):
    return bstack111l111_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩỂ") in config or bstack111l111_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫể") in config
def bstack1l111ll111_opy_(config):
    if not bstack11ll11l1_opy_(config):
        return
    if config.get(bstack111l111_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫỄ")):
        return config.get(bstack111l111_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬễ"))
    if config.get(bstack111l111_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧỆ")):
        return config.get(bstack111l111_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨệ"))
def bstack1lllll11l1_opy_(config, bstack11111l1l1ll_opy_):
    proxy = bstack1l111ll111_opy_(config)
    proxies = {}
    if config.get(bstack111l111_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨỈ")) or config.get(bstack111l111_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪỉ")):
        if proxy.endswith(bstack111l111_opy_ (u"ࠧ࠯ࡲࡤࡧࠬỊ")):
            proxies = bstack1111ll11_opy_(proxy, bstack11111l1l1ll_opy_)
        else:
            proxies = {
                bstack111l111_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧị"): proxy
            }
    bstack1ll1ll11_opy_.bstack1ll11l1l_opy_(bstack111l111_opy_ (u"ࠩࡳࡶࡴࡾࡹࡔࡧࡷࡸ࡮ࡴࡧࡴࠩỌ"), proxies)
    return proxies
def bstack1111ll11_opy_(bstack11111l1lll1_opy_, bstack11111l1l1ll_opy_):
    proxies = {}
    global bstack11111l1llll_opy_
    if bstack111l111_opy_ (u"ࠪࡔࡆࡉ࡟ࡑࡔࡒ࡜࡞࠭ọ") in globals():
        return bstack11111l1llll_opy_
    try:
        proxy = bstack11111l1ll11_opy_(bstack11111l1lll1_opy_, bstack11111l1l1ll_opy_)
        if bstack111l111_opy_ (u"ࠦࡉࡏࡒࡆࡅࡗࠦỎ") in proxy:
            proxies = {}
        elif bstack111l111_opy_ (u"ࠧࡎࡔࡕࡒࠥỏ") in proxy or bstack111l111_opy_ (u"ࠨࡈࡕࡖࡓࡗࠧỐ") in proxy or bstack111l111_opy_ (u"ࠢࡔࡑࡆࡏࡘࠨố") in proxy:
            bstack11111l1l1l1_opy_ = proxy.split(bstack111l111_opy_ (u"ࠣࠢࠥỒ"))
            if bstack111l111_opy_ (u"ࠤ࠽࠳࠴ࠨồ") in bstack111l111_opy_ (u"ࠥࠦỔ").join(bstack11111l1l1l1_opy_[1:]):
                proxies = {
                    bstack111l111_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪổ"): bstack111l111_opy_ (u"ࠧࠨỖ").join(bstack11111l1l1l1_opy_[1:])
                }
            else:
                proxies = {
                    bstack111l111_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬỗ"): str(bstack11111l1l1l1_opy_[0]).lower() + bstack111l111_opy_ (u"ࠢ࠻࠱࠲ࠦỘ") + bstack111l111_opy_ (u"ࠣࠤộ").join(bstack11111l1l1l1_opy_[1:])
                }
        elif bstack111l111_opy_ (u"ࠤࡓࡖࡔ࡞࡙ࠣỚ") in proxy:
            bstack11111l1l1l1_opy_ = proxy.split(bstack111l111_opy_ (u"ࠥࠤࠧớ"))
            if bstack111l111_opy_ (u"ࠦ࠿࠵࠯ࠣỜ") in bstack111l111_opy_ (u"ࠧࠨờ").join(bstack11111l1l1l1_opy_[1:]):
                proxies = {
                    bstack111l111_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬỞ"): bstack111l111_opy_ (u"ࠢࠣở").join(bstack11111l1l1l1_opy_[1:])
                }
            else:
                proxies = {
                    bstack111l111_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧỠ"): bstack111l111_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥỡ") + bstack111l111_opy_ (u"ࠥࠦỢ").join(bstack11111l1l1l1_opy_[1:])
                }
        else:
            proxies = {
                bstack111l111_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪợ"): proxy
            }
    except Exception as e:
        print(bstack111l111_opy_ (u"ࠧࡹ࡯࡮ࡧࠣࡩࡷࡸ࡯ࡳࠤỤ"), bstack111l1ll1lll_opy_.format(bstack11111l1lll1_opy_, str(e)))
    bstack11111l1llll_opy_ = proxies
    return proxies