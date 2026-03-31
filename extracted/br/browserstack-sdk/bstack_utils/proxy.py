# coding: UTF-8
import sys
bstack11lll11_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack11l1l11_opy_ = 7
def bstack1ll11_opy_ (bstack111lll1_opy_):
    global bstack1ll111l_opy_
    bstack1llll11_opy_ = ord (bstack111lll1_opy_ [-1])
    bstack1_opy_ = bstack111lll1_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1_opy_)
    bstack1l11lll_opy_ = bstack1_opy_ [:bstack111l1ll_opy_] + bstack1_opy_ [bstack111l1ll_opy_:]
    if bstack11lll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    return eval (bstack11l1111_opy_)
import os
import time
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack1llll1lll1l1_opy_
from bstack_utils import logger_utils
global_config = Config.get_instance()
logger = logger_utils.get_logger(__name__, logger_utils.get_log_level())
def bstack1lll1111l1l1_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack1lll1111llll_opy_(bstack1lll1111ll11_opy_, bstack1lll1111l1ll_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack1lll1111ll11_opy_):
        with open(bstack1lll1111ll11_opy_) as f:
            pac = PACFile(f.read())
    elif bstack1lll1111l1l1_opy_(bstack1lll1111ll11_opy_):
        pac = get_pac(url=bstack1lll1111ll11_opy_)
    else:
        raise Exception(bstack1ll11_opy_ (u"ࠬࡖࡡࡤࠢࡩ࡭ࡱ࡫ࠠࡥࡱࡨࡷࠥࡴ࡯ࡵࠢࡨࡼ࡮ࡹࡴ࠻ࠢࡾࢁࠬ␲").format(bstack1lll1111ll11_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack1ll11_opy_ (u"ࠨ࠸࠯࠺࠱࠼࠳࠾ࠢ␳"), 80))
        bstack1lll1111lll1_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack1lll1111lll1_opy_ = bstack1ll11_opy_ (u"ࠧ࠱࠰࠳࠲࠵࠴࠰ࠨ␴")
    proxy_url = session.get_pac().find_proxy_for_url(bstack1lll1111l1ll_opy_, bstack1lll1111lll1_opy_)
    return proxy_url
def bstack1111lllll_opy_(config):
    return bstack1ll11_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫ␵") in config or bstack1ll11_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭␶") in config
def bstack11l11lll1_opy_(config):
    if not bstack1111lllll_opy_(config):
        return
    if config.get(bstack1ll11_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭␷")):
        return config.get(bstack1ll11_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧ␸"))
    if config.get(bstack1ll11_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ␹")):
        return config.get(bstack1ll11_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪ␺"))
def bstack11lllll1l_opy_(config, bstack1lll1111l1ll_opy_):
    proxy = bstack11l11lll1_opy_(config)
    proxies = {}
    if config.get(bstack1ll11_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪ␻")) or config.get(bstack1ll11_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬ␼")):
        if proxy.endswith(bstack1ll11_opy_ (u"ࠩ࠱ࡴࡦࡩࠧ␽")):
            proxies = bstack111l1l1l_opy_(proxy, bstack1lll1111l1ll_opy_)
        else:
            proxies = {
                bstack1ll11_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩ␾"): proxy
            }
    global_config.bstack1ll11l111_opy_(bstack1ll11_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡖࡩࡹࡺࡩ࡯ࡩࡶࠫ␿"), proxies)
    return proxies
def bstack111l1l1l_opy_(bstack1lll1111ll11_opy_, bstack1lll1111l1ll_opy_):
    proxies = {}
    global bstack1lll111l1111_opy_
    if bstack1ll11_opy_ (u"ࠬࡖࡁࡄࡡࡓࡖࡔ࡞࡙ࠨ⑀") in globals():
        return bstack1lll111l1111_opy_
    try:
        proxy = bstack1lll1111llll_opy_(bstack1lll1111ll11_opy_, bstack1lll1111l1ll_opy_)
        if bstack1ll11_opy_ (u"ࠨࡄࡊࡔࡈࡇ࡙ࠨ⑁") in proxy:
            proxies = {}
        elif bstack1ll11_opy_ (u"ࠢࡉࡖࡗࡔࠧ⑂") in proxy or bstack1ll11_opy_ (u"ࠣࡊࡗࡘࡕ࡙ࠢ⑃") in proxy or bstack1ll11_opy_ (u"ࠤࡖࡓࡈࡑࡓࠣ⑄") in proxy:
            bstack1lll1111ll1l_opy_ = proxy.split(bstack1ll11_opy_ (u"ࠥࠤࠧ⑅"))
            if bstack1ll11_opy_ (u"ࠦ࠿࠵࠯ࠣ⑆") in bstack1ll11_opy_ (u"ࠧࠨ⑇").join(bstack1lll1111ll1l_opy_[1:]):
                proxies = {
                    bstack1ll11_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬ⑈"): bstack1ll11_opy_ (u"ࠢࠣ⑉").join(bstack1lll1111ll1l_opy_[1:])
                }
            else:
                proxies = {
                    bstack1ll11_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧ⑊"): str(bstack1lll1111ll1l_opy_[0]).lower() + bstack1ll11_opy_ (u"ࠤ࠽࠳࠴ࠨ⑋") + bstack1ll11_opy_ (u"ࠥࠦ⑌").join(bstack1lll1111ll1l_opy_[1:])
                }
        elif bstack1ll11_opy_ (u"ࠦࡕࡘࡏ࡙࡛ࠥ⑍") in proxy:
            bstack1lll1111ll1l_opy_ = proxy.split(bstack1ll11_opy_ (u"ࠧࠦࠢ⑎"))
            if bstack1ll11_opy_ (u"ࠨ࠺࠰࠱ࠥ⑏") in bstack1ll11_opy_ (u"ࠢࠣ⑐").join(bstack1lll1111ll1l_opy_[1:]):
                proxies = {
                    bstack1ll11_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧ⑑"): bstack1ll11_opy_ (u"ࠤࠥ⑒").join(bstack1lll1111ll1l_opy_[1:])
                }
            else:
                proxies = {
                    bstack1ll11_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩ⑓"): bstack1ll11_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧ⑔") + bstack1ll11_opy_ (u"ࠧࠨ⑕").join(bstack1lll1111ll1l_opy_[1:])
                }
        else:
            proxies = {
                bstack1ll11_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬ⑖"): proxy
            }
    except Exception as e:
        print(bstack1ll11_opy_ (u"ࠢࡴࡱࡰࡩࠥ࡫ࡲࡳࡱࡵࠦ⑗"), bstack1llll1lll1l1_opy_.format(bstack1lll1111ll11_opy_, str(e)))
    bstack1lll111l1111_opy_ = proxies
    return proxies