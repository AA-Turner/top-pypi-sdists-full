# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1lll_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack1ll1l11_opy_ (bstack11l1lll_opy_):
    global bstack1l11ll1_opy_
    bstack111lll_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1l11_opy_ = bstack11l1lll_opy_ [:-1]
    bstack111111_opy_ = bstack111lll_opy_ % len (bstack1l1l11_opy_)
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ [:bstack111111_opy_] + bstack1l1l11_opy_ [bstack111111_opy_:]
    if bstack1ll11_opy_:
        bstack1llllll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    else:
        bstack1llllll_opy_ = str () .join ([chr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    return eval (bstack1llllll_opy_)
import threading
import tempfile
import os
import time
from datetime import datetime
from bstack_utils.bstack1111l11ll1l_opy_ import bstack1111l11l11l_opy_
from bstack_utils.constants import bstack111111lllll_opy_, bstack1ll11l1111_opy_
from bstack_utils.bstack111l1llll_opy_ import bstack11l1ll1ll_opy_
from bstack_utils import logger_utils
bstack1lllllllll11_opy_ = 10
class bstack1l111111l_opy_:
    def __init__(self, bstack11l1lll1l_opy_, config, bstack1111111l11l_opy_=0):
        self.bstack1lllllllllll_opy_ = set()
        self.lock = threading.Lock()
        self.bstack11111111lll_opy_ = bstack1ll1l11_opy_ (u"ࠧࢁࡽ࠰ࡶࡨࡷࡹࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲ࠴ࡧࡰࡪ࠱ࡹ࠵࠴࡬ࡡࡪ࡮ࡨࡨ࠲ࡺࡥࡴࡶࡶࠦℷ").format(bstack111111lllll_opy_)
        self.bstack1111111lll1_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll1l11_opy_ (u"ࠨࡡࡣࡱࡵࡸࡤࡨࡵࡪ࡮ࡧࡣࢀࢃࠢℸ").format(os.environ.get(bstack1ll1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬℹ"))))
        self.bstack111111l111l_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll1l11_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࡠࡶࡨࡷࡹࡹ࡟ࡼࡿ࠱ࡸࡽࡺࠢ℺").format(os.environ.get(bstack1ll1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ℻"))))
        self.bstack1111111111l_opy_ = 2
        self.bstack11l1lll1l_opy_ = bstack11l1lll1l_opy_
        self.config = config
        self.logger = logger_utils.get_logger(__name__, bstack1ll11l1111_opy_)
        self.bstack1111111l11l_opy_ = bstack1111111l11l_opy_
        self.bstack111111111l1_opy_ = False
        self.bstack1llllllllll1_opy_ = not (
                            os.environ.get(bstack1ll1l11_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅ࡙ࡎࡒࡄࡠࡔࡘࡒࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠤℼ")) and
                            os.environ.get(bstack1ll1l11_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡒࡔࡊࡅࡠࡋࡑࡈࡊ࡞ࠢℽ")) and
                            os.environ.get(bstack1ll1l11_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡕࡔࡂࡎࡢࡒࡔࡊࡅࡠࡅࡒ࡙ࡓ࡚ࠢℾ"))
                        )
        if bstack11l1ll1ll_opy_.bstack11111111l1l_opy_(config):
            self.bstack1111111111l_opy_ = bstack11l1ll1ll_opy_.bstack1111111l1ll_opy_(config, self.bstack1111111l11l_opy_)
            self.bstack111111111ll_opy_()
    def bstack11111111111_opy_(self):
        return bstack1ll1l11_opy_ (u"ࠨࡻࡾࡡࡾࢁࠧℿ").format(self.config.get(bstack1ll1l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ⅀")), os.environ.get(bstack1ll1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡗࡌࡐࡉࡥࡒࡖࡐࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧ⅁")))
    def bstack1111111llll_opy_(self):
        try:
            if self.bstack1llllllllll1_opy_:
                return
            with self.lock:
                try:
                    with open(self.bstack111111l111l_opy_, bstack1ll1l11_opy_ (u"ࠤࡵࠦ⅂")) as f:
                        bstack1111111l111_opy_ = set(line.strip() for line in f if line.strip())
                except FileNotFoundError:
                    bstack1111111l111_opy_ = set()
                bstack11111111ll1_opy_ = bstack1111111l111_opy_ - self.bstack1lllllllllll_opy_
                if not bstack11111111ll1_opy_:
                    return
                self.bstack1lllllllllll_opy_.update(bstack11111111ll1_opy_)
                data = {bstack1ll1l11_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࡗࡩࡸࡺࡳࠣ⅃"): list(self.bstack1lllllllllll_opy_), bstack1ll1l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠢ⅄"): self.config.get(bstack1ll1l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨⅅ")), bstack1ll1l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡗࡻ࡮ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠦⅆ"): os.environ.get(bstack1ll1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡖࡋࡏࡈࡤࡘࡕࡏࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭ⅇ")), bstack1ll1l11_opy_ (u"ࠣࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪࠨⅈ"): self.config.get(bstack1ll1l11_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧⅉ"))}
            response = bstack1111l11l11l_opy_.bstack1111111ll1l_opy_(self.bstack11111111lll_opy_, data)
            if response.get(bstack1ll1l11_opy_ (u"ࠥࡷࡹࡧࡴࡶࡵࠥ⅊")) == 200:
                self.logger.debug(bstack1ll1l11_opy_ (u"ࠦࡘࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬࡭ࡻࠣࡷࡪࡴࡴࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡨࡷࡹࡹ࠺ࠡࡽࢀࠦ⅋").format(data))
            else:
                self.logger.debug(bstack1ll1l11_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡲࡩࠦࡦࡢ࡫࡯ࡩࡩࠦࡴࡦࡵࡷࡷ࠿ࠦࡻࡾࠤ⅌").format(response))
        except Exception as e:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡧࡹࡷ࡯࡮ࡨࠢࡶࡩࡳࡪࡩ࡯ࡩࠣࡪࡦ࡯࡬ࡦࡦࠣࡸࡪࡹࡴࡴ࠼ࠣࡿࢂࠨ⅍").format(e))
    def bstack111111l1111_opy_(self):
        if self.bstack1llllllllll1_opy_:
            with self.lock:
                try:
                    with open(self.bstack111111l111l_opy_, bstack1ll1l11_opy_ (u"ࠢࡳࠤⅎ")) as f:
                        bstack1111111l1l1_opy_ = set(line.strip() for line in f if line.strip())
                    failed_count = len(bstack1111111l1l1_opy_)
                except FileNotFoundError:
                    failed_count = 0
                self.logger.debug(bstack1ll1l11_opy_ (u"ࠣࡒࡲࡰࡱ࡫ࡤࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡨࡷࡹࡹࠠࡤࡱࡸࡲࡹࠦࠨ࡭ࡱࡦࡥࡱ࠯࠺ࠡࡽࢀࠦ⅏").format(failed_count))
                if failed_count >= self.bstack1111111111l_opy_:
                    self.logger.info(bstack1ll1l11_opy_ (u"ࠤࡗ࡬ࡷ࡫ࡳࡩࡱ࡯ࡨࠥࡩࡲࡰࡵࡶࡩࡩࠦࠨ࡭ࡱࡦࡥࡱ࠯࠺ࠡࡽࢀࠤࡃࡃࠠࡼࡿࠥ⅐").format(failed_count, self.bstack1111111111l_opy_))
                    self.bstack11111111l11_opy_(failed_count)
                    self.bstack111111111l1_opy_ = True
            return
        try:
            response = bstack1111l11l11l_opy_.bstack111111l1111_opy_(bstack1ll1l11_opy_ (u"ࠥࡿࢂࡅࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦ࠿ࡾࢁࠫࡨࡵࡪ࡮ࡧࡖࡺࡴࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࡀࡿࢂࠬࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࡁࢀࢃࠢ⅑").format(self.bstack11111111lll_opy_, self.config.get(bstack1ll1l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ⅒")), os.environ.get(bstack1ll1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇ࡛ࡉࡍࡆࡢࡖ࡚ࡔ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫ⅓")), self.config.get(bstack1ll1l11_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫ⅔"))))
            if response.get(bstack1ll1l11_opy_ (u"ࠢࡴࡶࡤࡸࡺࡹࠢ⅕")) == 200:
                failed_count = response.get(bstack1ll1l11_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࡕࡧࡶࡸࡸࡉ࡯ࡶࡰࡷࠦ⅖"), 0)
                self.logger.debug(bstack1ll1l11_opy_ (u"ࠤࡓࡳࡱࡲࡥࡥࠢࡩࡥ࡮ࡲࡥࡥࠢࡷࡩࡸࡺࡳࠡࡥࡲࡹࡳࡺ࠺ࠡࡽࢀࠦ⅗").format(failed_count))
                if failed_count >= self.bstack1111111111l_opy_:
                    self.logger.info(bstack1ll1l11_opy_ (u"ࠥࡘ࡭ࡸࡥࡴࡪࡲࡰࡩࠦࡣࡳࡱࡶࡷࡪࡪ࠺ࠡࡽࢀࠤࡃࡃࠠࡼࡿࠥ⅘").format(failed_count, self.bstack1111111111l_opy_))
                    self.bstack11111111l11_opy_(failed_count)
                    self.bstack111111111l1_opy_ = True
            else:
                self.logger.error(bstack1ll1l11_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡱ࡯ࡰࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡺࡥࡴࡶࡶ࠾ࠥࢁࡽࠣ⅙").format(response))
        except Exception as e:
            self.logger.error(bstack1ll1l11_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡦࡸࡶ࡮ࡴࡧࠡࡲࡲࡰࡱ࡯࡮ࡨ࠼ࠣࡿࢂࠨ⅚").format(e))
    def bstack11111111l11_opy_(self, failed_count):
        with open(self.bstack1111111lll1_opy_, bstack1ll1l11_opy_ (u"ࠨࡷࠣ⅛")) as f:
            f.write(bstack1ll1l11_opy_ (u"ࠢࡕࡪࡵࡩࡸ࡮࡯࡭ࡦࠣࡧࡷࡵࡳࡴࡧࡧࠤࡦࡺࠠࡼࡿ࡟ࡲࠧ⅜").format(datetime.now()))
            f.write(bstack1ll1l11_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡨࡷࡹࡹࠠࡤࡱࡸࡲࡹࡀࠠࡼࡿ࡟ࡲࠧ⅝").format(failed_count))
        self.logger.debug(bstack1ll1l11_opy_ (u"ࠤࡄࡦࡴࡸࡴࠡࡄࡸ࡭ࡱࡪࠠࡧ࡫࡯ࡩࠥࡩࡲࡦࡣࡷࡩࡩࡀࠠࡼࡿࠥ⅞").format(self.bstack1111111lll1_opy_))
    def bstack111111111ll_opy_(self):
        def bstack1lllllllll1l_opy_():
            while not self.bstack111111111l1_opy_:
                time.sleep(bstack1lllllllll11_opy_)
                self.bstack1111111llll_opy_()
                self.bstack111111l1111_opy_()
        bstack1111111ll11_opy_ = threading.Thread(target=bstack1lllllllll1l_opy_, daemon=True)
        bstack1111111ll11_opy_.start()