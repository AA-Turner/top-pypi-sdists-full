# coding: UTF-8
import sys
bstack1ll11l1_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack11lll_opy_ = 7
def bstack1l11l11_opy_ (bstack1llll11_opy_):
    global bstack11ll1l1_opy_
    bstack111l111_opy_ = ord (bstack1llll11_opy_ [-1])
    bstack11lll11_opy_ = bstack1llll11_opy_ [:-1]
    bstack1ll11_opy_ = bstack111l111_opy_ % len (bstack11lll11_opy_)
    bstack1l1l_opy_ = bstack11lll11_opy_ [:bstack1ll11_opy_] + bstack11lll11_opy_ [bstack1ll11_opy_:]
    if bstack1ll11l1_opy_:
        bstack11l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack111l1l1_opy_ + bstack111l111_opy_) % bstack11lll_opy_) for bstack111l1l1_opy_, char in enumerate (bstack1l1l_opy_)])
    else:
        bstack11l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack111l1l1_opy_ + bstack111l111_opy_) % bstack11lll_opy_) for bstack111l1l1_opy_, char in enumerate (bstack1l1l_opy_)])
    return eval (bstack11l1l1_opy_)
import json
import multiprocessing
import os
from bstack_utils.config import Config
class bstack1llll11l1_opy_():
  def __init__(self, args, logger, bstack11111llll1_opy_, bstack11111ll11l_opy_, bstack11111l1111_opy_):
    self.args = args
    self.logger = logger
    self.bstack11111llll1_opy_ = bstack11111llll1_opy_
    self.bstack11111ll11l_opy_ = bstack11111ll11l_opy_
    self.bstack11111l1111_opy_ = bstack11111l1111_opy_
  def bstack11l1l1llll_opy_(self, bstack11111lll1l_opy_, bstack11ll1l1l_opy_, bstack111111llll_opy_=False):
    bstack1l1l1lll_opy_ = []
    manager = multiprocessing.Manager()
    bstack11111ll111_opy_ = manager.list()
    bstack11l11llll_opy_ = Config.bstack11l111llll_opy_()
    if bstack111111llll_opy_:
      for index, platform in enumerate(self.bstack11111llll1_opy_[bstack1l11l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧႁ")]):
        if index == 0:
          bstack11ll1l1l_opy_[bstack1l11l11_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨႂ")] = self.args
        bstack1l1l1lll_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack11111lll1l_opy_,
                                                    args=(bstack11ll1l1l_opy_, bstack11111ll111_opy_)))
    else:
      for index, platform in enumerate(self.bstack11111llll1_opy_[bstack1l11l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩႃ")]):
        bstack1l1l1lll_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack11111lll1l_opy_,
                                                    args=(bstack11ll1l1l_opy_, bstack11111ll111_opy_)))
    i = 0
    for t in bstack1l1l1lll_opy_:
      try:
        if bstack11l11llll_opy_.get_property(bstack1l11l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨႄ")):
          os.environ[bstack1l11l11_opy_ (u"ࠨࡅࡘࡖࡗࡋࡎࡕࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡉࡇࡔࡂࠩႅ")] = json.dumps(self.bstack11111llll1_opy_[bstack1l11l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬႆ")][i % self.bstack11111l1111_opy_])
      except Exception as e:
        self.logger.debug(bstack1l11l11_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡵࡷࡳࡷ࡯࡮ࡨࠢࡦࡹࡷࡸࡥ࡯ࡶࠣࡴࡱࡧࡴࡧࡱࡵࡱࠥࡪࡥࡵࡣ࡬ࡰࡸࡀࠠࡼࡿࠥႇ").format(str(e)))
      i += 1
      t.start()
    for t in bstack1l1l1lll_opy_:
      t.join()
    return list(bstack11111ll111_opy_)