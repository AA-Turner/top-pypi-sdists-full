# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack111l111_opy_ = 2048
bstack1l111l1_opy_ = 7
def bstack1lll1l_opy_ (bstack1l1l11_opy_):
    global bstack1lll1ll_opy_
    bstack1ll111l_opy_ = ord (bstack1l1l11_opy_ [-1])
    bstack1lll_opy_ = bstack1l1l11_opy_ [:-1]
    bstack11ll1_opy_ = bstack1ll111l_opy_ % len (bstack1lll_opy_)
    bstack11l11l1_opy_ = bstack1lll_opy_ [:bstack11ll1_opy_] + bstack1lll_opy_ [bstack11ll1_opy_:]
    if bstack1lll1l1_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    return eval (bstack111l11_opy_)
import os
import time
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack1llllllll11l_opy_
from bstack_utils import logger_utils
global_config = Config.get_instance()
logger = logger_utils.get_logger(__name__, logger_utils.bstack1l1llllll11_opy_())
def bstack1lll1l11l111_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack1lll1l11ll1l_opy_(bstack1lll1l11ll11_opy_, bstack1lll1l11l11l_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack1lll1l11ll11_opy_):
        with open(bstack1lll1l11ll11_opy_) as f:
            pac = PACFile(f.read())
    elif bstack1lll1l11l111_opy_(bstack1lll1l11ll11_opy_):
        pac = get_pac(url=bstack1lll1l11ll11_opy_)
    else:
        raise Exception(bstack1lll1l_opy_ (u"ࠫࡕࡧࡣࠡࡨ࡬ࡰࡪࠦࡤࡰࡧࡶࠤࡳࡵࡴࠡࡧࡻ࡭ࡸࡺ࠺ࠡࡽࢀࠫ⋯").format(bstack1lll1l11ll11_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack1lll1l_opy_ (u"ࠧ࠾࠮࠹࠰࠻࠲࠽ࠨ⋰"), 80))
        bstack1lll1l11l1l1_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack1lll1l11l1l1_opy_ = bstack1lll1l_opy_ (u"࠭࠰࠯࠲࠱࠴࠳࠶ࠧ⋱")
    proxy_url = session.get_pac().find_proxy_for_url(bstack1lll1l11l11l_opy_, bstack1lll1l11l1l1_opy_)
    return proxy_url
def bstack11l1ll11l_opy_(config):
    return bstack1lll1l_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪ⋲") in config or bstack1lll1l_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬ⋳") in config
def bstack11l1lll1l1_opy_(config):
    if not bstack11l1ll11l_opy_(config):
        return
    if config.get(bstack1lll1l_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬ⋴")):
        return config.get(bstack1lll1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭⋵"))
    if config.get(bstack1lll1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨ⋶")):
        return config.get(bstack1lll1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ⋷"))
def bstack11l1l11l11_opy_(config, bstack1lll1l11l11l_opy_):
    proxy = bstack11l1lll1l1_opy_(config)
    proxies = {}
    if config.get(bstack1lll1l_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩ⋸")) or config.get(bstack1lll1l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫ⋹")):
        if proxy.endswith(bstack1lll1l_opy_ (u"ࠨ࠰ࡳࡥࡨ࠭⋺")):
            proxies = bstack111l1l1ll_opy_(proxy, bstack1lll1l11l11l_opy_)
        else:
            proxies = {
                bstack1lll1l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨ⋻"): proxy
            }
    global_config.bstack1l1l1llll_opy_(bstack1lll1l_opy_ (u"ࠪࡴࡷࡵࡸࡺࡕࡨࡸࡹ࡯࡮ࡨࡵࠪ⋼"), proxies)
    return proxies
def bstack111l1l1ll_opy_(bstack1lll1l11ll11_opy_, bstack1lll1l11l11l_opy_):
    proxies = {}
    global bstack1lll1l11lll1_opy_
    if bstack1lll1l_opy_ (u"ࠫࡕࡇࡃࡠࡒࡕࡓ࡝࡟ࠧ⋽") in globals():
        return bstack1lll1l11lll1_opy_
    try:
        proxy = bstack1lll1l11ll1l_opy_(bstack1lll1l11ll11_opy_, bstack1lll1l11l11l_opy_)
        if bstack1lll1l_opy_ (u"ࠧࡊࡉࡓࡇࡆࡘࠧ⋾") in proxy:
            proxies = {}
        elif bstack1lll1l_opy_ (u"ࠨࡈࡕࡖࡓࠦ⋿") in proxy or bstack1lll1l_opy_ (u"ࠢࡉࡖࡗࡔࡘࠨ⌀") in proxy or bstack1lll1l_opy_ (u"ࠣࡕࡒࡇࡐ࡙ࠢ⌁") in proxy:
            bstack1lll1l11l1ll_opy_ = proxy.split(bstack1lll1l_opy_ (u"ࠤࠣࠦ⌂"))
            if bstack1lll1l_opy_ (u"ࠥ࠾࠴࠵ࠢ⌃") in bstack1lll1l_opy_ (u"ࠦࠧ⌄").join(bstack1lll1l11l1ll_opy_[1:]):
                proxies = {
                    bstack1lll1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫ⌅"): bstack1lll1l_opy_ (u"ࠨࠢ⌆").join(bstack1lll1l11l1ll_opy_[1:])
                }
            else:
                proxies = {
                    bstack1lll1l_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭⌇"): str(bstack1lll1l11l1ll_opy_[0]).lower() + bstack1lll1l_opy_ (u"ࠣ࠼࠲࠳ࠧ⌈") + bstack1lll1l_opy_ (u"ࠤࠥ⌉").join(bstack1lll1l11l1ll_opy_[1:])
                }
        elif bstack1lll1l_opy_ (u"ࠥࡔࡗࡕࡘ࡚ࠤ⌊") in proxy:
            bstack1lll1l11l1ll_opy_ = proxy.split(bstack1lll1l_opy_ (u"ࠦࠥࠨ⌋"))
            if bstack1lll1l_opy_ (u"ࠧࡀ࠯࠰ࠤ⌌") in bstack1lll1l_opy_ (u"ࠨࠢ⌍").join(bstack1lll1l11l1ll_opy_[1:]):
                proxies = {
                    bstack1lll1l_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭⌎"): bstack1lll1l_opy_ (u"ࠣࠤ⌏").join(bstack1lll1l11l1ll_opy_[1:])
                }
            else:
                proxies = {
                    bstack1lll1l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨ⌐"): bstack1lll1l_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦ⌑") + bstack1lll1l_opy_ (u"ࠦࠧ⌒").join(bstack1lll1l11l1ll_opy_[1:])
                }
        else:
            proxies = {
                bstack1lll1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫ⌓"): proxy
            }
    except Exception as e:
        print(bstack1lll1l_opy_ (u"ࠨࡳࡰ࡯ࡨࠤࡪࡸࡲࡰࡴࠥ⌔"), bstack1llllllll11l_opy_.format(bstack1lll1l11ll11_opy_, str(e)))
    bstack1lll1l11lll1_opy_ = proxies
    return proxies