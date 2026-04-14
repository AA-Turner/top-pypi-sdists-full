# coding: UTF-8
import sys
bstack11l1l_opy_ = sys.version_info [0] == 2
bstack1ll11_opy_ = 2048
bstack11ll11_opy_ = 7
def bstack1l111l_opy_ (bstack11l11l_opy_):
    global bstack1l11l_opy_
    bstack1l1111l_opy_ = ord (bstack11l11l_opy_ [-1])
    bstack1l1l11l_opy_ = bstack11l11l_opy_ [:-1]
    bstack111l1_opy_ = bstack1l1111l_opy_ % len (bstack1l1l11l_opy_)
    bstack11l1l1l_opy_ = bstack1l1l11l_opy_ [:bstack111l1_opy_] + bstack1l1l11l_opy_ [bstack111l1_opy_:]
    if bstack11l1l_opy_:
        bstack1111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    else:
        bstack1111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    return eval (bstack1111l1l_opy_)
import os
import time
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack1lll1l11ll1l_opy_
from bstack_utils import logger_utils
global_config = Config.bstack1ll11ll111_opy_()
logger = logger_utils.get_logger(__name__, logger_utils.get_log_level())
def bstack1ll1l11lll1l_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack1ll1l11lllll_opy_(bstack1ll1l1l1111l_opy_, bstack1ll1l11llll1_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack1ll1l1l1111l_opy_):
        with open(bstack1ll1l1l1111l_opy_) as f:
            pac = PACFile(f.read())
    elif bstack1ll1l11lll1l_opy_(bstack1ll1l1l1111l_opy_):
        pac = get_pac(url=bstack1ll1l1l1111l_opy_)
    else:
        raise Exception(bstack1l111l_opy_ (u"ࠧࡑࡣࡦࠤ࡫࡯࡬ࡦࠢࡧࡳࡪࡹࠠ࡯ࡱࡷࠤࡪࡾࡩࡴࡶ࠽ࠤࢀࢃࠧ☥").format(bstack1ll1l1l1111l_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack1l111l_opy_ (u"ࠣ࠺࠱࠼࠳࠾࠮࠹ࠤ☦"), 80))
        bstack1ll1l11lll11_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack1ll1l11lll11_opy_ = bstack1l111l_opy_ (u"ࠩ࠳࠲࠵࠴࠰࠯࠲ࠪ☧")
    proxy_url = session.get_pac().find_proxy_for_url(bstack1ll1l11llll1_opy_, bstack1ll1l11lll11_opy_)
    return proxy_url
def bstack11ll11111_opy_(config):
    return bstack1l111l_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭☨") in config or bstack1l111l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨ☩") in config
def bstack1l1llll111_opy_(config):
    if not bstack11ll11111_opy_(config):
        return
    if config.get(bstack1l111l_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨ☪")):
        return config.get(bstack1l111l_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩ☫"))
    if config.get(bstack1l111l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫ☬")):
        return config.get(bstack1l111l_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬ☭"))
def bstack1111ll1l1l_opy_(config, bstack1ll1l11llll1_opy_):
    proxy = bstack1l1llll111_opy_(config)
    proxies = {}
    if config.get(bstack1l111l_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬ☮")) or config.get(bstack1l111l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧ☯")):
        if proxy.endswith(bstack1l111l_opy_ (u"ࠫ࠳ࡶࡡࡤࠩ☰")):
            proxies = bstack1111111ll_opy_(proxy, bstack1ll1l11llll1_opy_)
        else:
            proxies = {
                bstack1l111l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫ☱"): proxy
            }
    global_config.bstack1llllll11ll_opy_(bstack1l111l_opy_ (u"࠭ࡰࡳࡱࡻࡽࡘ࡫ࡴࡵ࡫ࡱ࡫ࡸ࠭☲"), proxies)
    return proxies
def bstack1111111ll_opy_(bstack1ll1l1l1111l_opy_, bstack1ll1l11llll1_opy_):
    proxies = {}
    global bstack1ll1l11ll1ll_opy_
    if bstack1l111l_opy_ (u"ࠧࡑࡃࡆࡣࡕࡘࡏ࡙࡛ࠪ☳") in globals():
        return bstack1ll1l11ll1ll_opy_
    try:
        proxy = bstack1ll1l11lllll_opy_(bstack1ll1l1l1111l_opy_, bstack1ll1l11llll1_opy_)
        if bstack1l111l_opy_ (u"ࠣࡆࡌࡖࡊࡉࡔࠣ☴") in proxy:
            proxies = {}
        elif bstack1l111l_opy_ (u"ࠤࡋࡘ࡙ࡖࠢ☵") in proxy or bstack1l111l_opy_ (u"ࠥࡌ࡙࡚ࡐࡔࠤ☶") in proxy or bstack1l111l_opy_ (u"ࠦࡘࡕࡃࡌࡕࠥ☷") in proxy:
            bstack1ll1l1l11111_opy_ = proxy.split(bstack1l111l_opy_ (u"ࠧࠦࠢ☸"))
            if bstack1l111l_opy_ (u"ࠨ࠺࠰࠱ࠥ☹") in bstack1l111l_opy_ (u"ࠢࠣ☺").join(bstack1ll1l1l11111_opy_[1:]):
                proxies = {
                    bstack1l111l_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧ☻"): bstack1l111l_opy_ (u"ࠤࠥ☼").join(bstack1ll1l1l11111_opy_[1:])
                }
            else:
                proxies = {
                    bstack1l111l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩ☽"): str(bstack1ll1l1l11111_opy_[0]).lower() + bstack1l111l_opy_ (u"ࠦ࠿࠵࠯ࠣ☾") + bstack1l111l_opy_ (u"ࠧࠨ☿").join(bstack1ll1l1l11111_opy_[1:])
                }
        elif bstack1l111l_opy_ (u"ࠨࡐࡓࡑ࡛࡝ࠧ♀") in proxy:
            bstack1ll1l1l11111_opy_ = proxy.split(bstack1l111l_opy_ (u"ࠢࠡࠤ♁"))
            if bstack1l111l_opy_ (u"ࠣ࠼࠲࠳ࠧ♂") in bstack1l111l_opy_ (u"ࠤࠥ♃").join(bstack1ll1l1l11111_opy_[1:]):
                proxies = {
                    bstack1l111l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩ♄"): bstack1l111l_opy_ (u"ࠦࠧ♅").join(bstack1ll1l1l11111_opy_[1:])
                }
            else:
                proxies = {
                    bstack1l111l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫ♆"): bstack1l111l_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢ♇") + bstack1l111l_opy_ (u"ࠢࠣ♈").join(bstack1ll1l1l11111_opy_[1:])
                }
        else:
            proxies = {
                bstack1l111l_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧ♉"): proxy
            }
    except Exception as e:
        print(bstack1l111l_opy_ (u"ࠤࡶࡳࡲ࡫ࠠࡦࡴࡵࡳࡷࠨ♊"), bstack1lll1l11ll1l_opy_.format(bstack1ll1l1l1111l_opy_, str(e)))
    bstack1ll1l11ll1ll_opy_ = proxies
    return proxies