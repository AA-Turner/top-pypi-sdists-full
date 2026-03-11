# coding: UTF-8
import sys
bstack1l1ll11_opy_ = sys.version_info [0] == 2
bstack11111l1_opy_ = 2048
bstack1111lll_opy_ = 7
def bstack1ll111_opy_ (bstack1111l1l_opy_):
    global bstack11l111l_opy_
    bstack11l1ll_opy_ = ord (bstack1111l1l_opy_ [-1])
    bstack11lll1l_opy_ = bstack1111l1l_opy_ [:-1]
    bstack111lll_opy_ = bstack11l1ll_opy_ % len (bstack11lll1l_opy_)
    bstack11llll1_opy_ = bstack11lll1l_opy_ [:bstack111lll_opy_] + bstack11lll1l_opy_ [bstack111lll_opy_:]
    if bstack1l1ll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    return eval (bstack11l1111_opy_)
import threading
import tempfile
import os
import time
from datetime import datetime
from bstack_utils.bstack11111l11l11_opy_ import bstack111111ll111_opy_
from bstack_utils.constants import bstack1lll1lll1l11_opy_, bstack1l1lllll1_opy_
from bstack_utils.bstack111ll11l_opy_ import bstack1l1ll111l_opy_
from bstack_utils import logger_utils
bstack1ll1ll111111_opy_ = 10
class bstack111l11l1ll_opy_:
    def __init__(self, bstack11l11lll_opy_, config, bstack11111111lll_opy_=0):
        self.bstack1ll1ll1111l1_opy_ = set()
        self.lock = threading.Lock()
        self.bstack1ll1ll11l1l1_opy_ = bstack1ll111_opy_ (u"ࠥࡿࢂ࠵ࡴࡦࡵࡷࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰ࠲ࡥࡵ࡯࠯ࡷ࠳࠲ࡪࡦ࡯࡬ࡦࡦ࠰ࡸࡪࡹࡴࡴࠤ◷").format(bstack1lll1lll1l11_opy_)
        self.bstack1ll1ll1111ll_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll111_opy_ (u"ࠦࡦࡨ࡯ࡳࡶࡢࡦࡺ࡯࡬ࡥࡡࡾࢁࠧ◸").format(os.environ.get(bstack1ll111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ◹"))))
        self.bstack1ll1ll1l1111_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll111_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࡥࡴࡦࡵࡷࡷࡤࢁࡽ࠯ࡶࡻࡸࠧ◺").format(os.environ.get(bstack1ll111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ◻"))))
        self.bstack1ll1ll111ll1_opy_ = 2
        self.bstack11l11lll_opy_ = bstack11l11lll_opy_
        self.config = config
        self.logger = logger_utils.get_logger(__name__, bstack1l1lllll1_opy_)
        self.bstack11111111lll_opy_ = bstack11111111lll_opy_
        self.bstack1ll1ll11ll1l_opy_ = False
        self.bstack1ll1ll11l11l_opy_ = not (
                            os.environ.get(bstack1ll111_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡗࡌࡐࡉࡥࡒࡖࡐࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠢ◼")) and
                            os.environ.get(bstack1ll111_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡐࡒࡈࡊࡥࡉࡏࡆࡈ࡜ࠧ◽")) and
                            os.environ.get(bstack1ll111_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡓ࡙ࡇࡌࡠࡐࡒࡈࡊࡥࡃࡐࡗࡑࡘࠧ◾"))
                        )
        if bstack1l1ll111l_opy_.bstack11111ll1l11_opy_(config):
            self.bstack1ll1ll111ll1_opy_ = bstack1l1ll111l_opy_.bstack11111111l1l_opy_(config, self.bstack11111111lll_opy_)
            self.bstack1ll1ll111lll_opy_()
    def bstack1ll1ll11l1ll_opy_(self):
        return bstack1ll111_opy_ (u"ࠦࢀࢃ࡟ࡼࡿࠥ◿").format(self.config.get(bstack1ll111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ☀")), os.environ.get(bstack1ll111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡕࡊࡎࡇࡣࡗ࡛ࡎࡠࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠬ☁")))
    def bstack1ll1ll11lll1_opy_(self):
        try:
            if self.bstack1ll1ll11l11l_opy_:
                return
            with self.lock:
                try:
                    with open(self.bstack1ll1ll1l1111_opy_, bstack1ll111_opy_ (u"ࠢࡳࠤ☂")) as f:
                        bstack1ll1ll111l11_opy_ = set(line.strip() for line in f if line.strip())
                except FileNotFoundError:
                    bstack1ll1ll111l11_opy_ = set()
                bstack1ll1ll11ll11_opy_ = bstack1ll1ll111l11_opy_ - self.bstack1ll1ll1111l1_opy_
                if not bstack1ll1ll11ll11_opy_:
                    return
                self.bstack1ll1ll1111l1_opy_.update(bstack1ll1ll11ll11_opy_)
                data = {bstack1ll111_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࡕࡧࡶࡸࡸࠨ☃"): list(self.bstack1ll1ll1111l1_opy_), bstack1ll111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠧ☄"): self.config.get(bstack1ll111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭★")), bstack1ll111_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡕࡹࡳࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠤ☆"): os.environ.get(bstack1ll111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇ࡛ࡉࡍࡆࡢࡖ࡚ࡔ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫ☇")), bstack1ll111_opy_ (u"ࠨࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠦ☈"): self.config.get(bstack1ll111_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬ☉"))}
            response = bstack111111ll111_opy_.bstack1lll1lll1l1l_opy_(self.bstack1ll1ll11l1l1_opy_, data)
            if response.get(bstack1ll111_opy_ (u"ࠣࡵࡷࡥࡹࡻࡳࠣ☊")) == 200:
                self.logger.debug(bstack1ll111_opy_ (u"ࠤࡖࡹࡨࡩࡥࡴࡵࡩࡹࡱࡲࡹࠡࡵࡨࡲࡹࠦࡦࡢ࡫࡯ࡩࡩࠦࡴࡦࡵࡷࡷ࠿ࠦࡻࡾࠤ☋").format(data))
            else:
                self.logger.debug(bstack1ll111_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡰࡧࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡹ࡫ࡳࡵࡵ࠽ࠤࢀࢃࠢ☌").format(response))
        except Exception as e:
            self.logger.debug(bstack1ll111_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡥࡷࡵ࡭ࡳ࡭ࠠࡴࡧࡱࡨ࡮ࡴࡧࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡨࡷࡹࡹ࠺ࠡࡽࢀࠦ☍").format(e))
    def bstack1llll1111111_opy_(self):
        if self.bstack1ll1ll11l11l_opy_:
            with self.lock:
                try:
                    with open(self.bstack1ll1ll1l1111_opy_, bstack1ll111_opy_ (u"ࠧࡸࠢ☎")) as f:
                        bstack1ll1ll11llll_opy_ = set(line.strip() for line in f if line.strip())
                    failed_count = len(bstack1ll1ll11llll_opy_)
                except FileNotFoundError:
                    failed_count = 0
                self.logger.debug(bstack1ll111_opy_ (u"ࠨࡐࡰ࡮࡯ࡩࡩࠦࡦࡢ࡫࡯ࡩࡩࠦࡴࡦࡵࡷࡷࠥࡩ࡯ࡶࡰࡷࠤ࠭ࡲ࡯ࡤࡣ࡯࠭࠿ࠦࡻࡾࠤ☏").format(failed_count))
                if failed_count >= self.bstack1ll1ll111ll1_opy_:
                    self.logger.info(bstack1ll111_opy_ (u"ࠢࡕࡪࡵࡩࡸ࡮࡯࡭ࡦࠣࡧࡷࡵࡳࡴࡧࡧࠤ࠭ࡲ࡯ࡤࡣ࡯࠭࠿ࠦࡻࡾࠢࡁࡁࠥࢁࡽࠣ☐").format(failed_count, self.bstack1ll1ll111ll1_opy_))
                    self.bstack1ll1ll11l111_opy_(failed_count)
                    self.bstack1ll1ll11ll1l_opy_ = True
            return
        try:
            response = bstack111111ll111_opy_.bstack1llll1111111_opy_(bstack1ll111_opy_ (u"ࠣࡽࢀࡃࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫࠽ࡼࡿࠩࡦࡺ࡯࡬ࡥࡔࡸࡲࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲ࠾ࡽࢀࠪࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦ࠿ࡾࢁࠧ☑").format(self.bstack1ll1ll11l1l1_opy_, self.config.get(bstack1ll111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ☒")), os.environ.get(bstack1ll111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅ࡙ࡎࡒࡄࡠࡔࡘࡒࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩ☓")), self.config.get(bstack1ll111_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩ☔"))))
            if response.get(bstack1ll111_opy_ (u"ࠧࡹࡴࡢࡶࡸࡷࠧ☕")) == 200:
                failed_count = response.get(bstack1ll111_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩ࡚ࡥࡴࡶࡶࡇࡴࡻ࡮ࡵࠤ☖"), 0)
                self.logger.debug(bstack1ll111_opy_ (u"ࠢࡑࡱ࡯ࡰࡪࡪࠠࡧࡣ࡬ࡰࡪࡪࠠࡵࡧࡶࡸࡸࠦࡣࡰࡷࡱࡸ࠿ࠦࡻࡾࠤ☗").format(failed_count))
                if failed_count >= self.bstack1ll1ll111ll1_opy_:
                    self.logger.info(bstack1ll111_opy_ (u"ࠣࡖ࡫ࡶࡪࡹࡨࡰ࡮ࡧࠤࡨࡸ࡯ࡴࡵࡨࡨ࠿ࠦࡻࡾࠢࡁࡁࠥࢁࡽࠣ☘").format(failed_count, self.bstack1ll1ll111ll1_opy_))
                    self.bstack1ll1ll11l111_opy_(failed_count)
                    self.bstack1ll1ll11ll1l_opy_ = True
            else:
                self.logger.error(bstack1ll111_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡶ࡯࡭࡮ࠣࡪࡦ࡯࡬ࡦࡦࠣࡸࡪࡹࡴࡴ࠼ࠣࡿࢂࠨ☙").format(response))
        except Exception as e:
            self.logger.error(bstack1ll111_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡤࡶࡴ࡬ࡲ࡬ࠦࡰࡰ࡮࡯࡭ࡳ࡭࠺ࠡࡽࢀࠦ☚").format(e))
    def bstack1ll1ll11l111_opy_(self, failed_count):
        with open(self.bstack1ll1ll1111ll_opy_, bstack1ll111_opy_ (u"ࠦࡼࠨ☛")) as f:
            f.write(bstack1ll111_opy_ (u"࡚ࠧࡨࡳࡧࡶ࡬ࡴࡲࡤࠡࡥࡵࡳࡸࡹࡥࡥࠢࡤࡸࠥࢁࡽ࡝ࡰࠥ☜").format(datetime.now()))
            f.write(bstack1ll111_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡦࡵࡷࡷࠥࡩ࡯ࡶࡰࡷ࠾ࠥࢁࡽ࡝ࡰࠥ☝").format(failed_count))
        self.logger.debug(bstack1ll111_opy_ (u"ࠢࡂࡤࡲࡶࡹࠦࡂࡶ࡫࡯ࡨࠥ࡬ࡩ࡭ࡧࠣࡧࡷ࡫ࡡࡵࡧࡧ࠾ࠥࢁࡽࠣ☞").format(self.bstack1ll1ll1111ll_opy_))
    def bstack1ll1ll111lll_opy_(self):
        def bstack1ll1ll111l1l_opy_():
            while not self.bstack1ll1ll11ll1l_opy_:
                time.sleep(bstack1ll1ll111111_opy_)
                self.bstack1ll1ll11lll1_opy_()
                self.bstack1llll1111111_opy_()
        bstack1ll1ll11111l_opy_ = threading.Thread(target=bstack1ll1ll111l1l_opy_, daemon=True)
        bstack1ll1ll11111l_opy_.start()