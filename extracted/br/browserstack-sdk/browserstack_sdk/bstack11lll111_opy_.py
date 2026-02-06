# coding: UTF-8
import sys
bstack11ll1l1_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack1ll1lll_opy_ = 7
def bstack11lllll_opy_ (bstack11ll1_opy_):
    global bstack1llllll_opy_
    bstack111l_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1111l11_opy_ = bstack11ll1_opy_ [:-1]
    bstack1lllll1l_opy_ = bstack111l_opy_ % len (bstack1111l11_opy_)
    bstack1ll1ll_opy_ = bstack1111l11_opy_ [:bstack1lllll1l_opy_] + bstack1111l11_opy_ [bstack1lllll1l_opy_:]
    if bstack11ll1l1_opy_:
        bstack1l1llll_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    else:
        bstack1l1llll_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    return eval (bstack1l1llll_opy_)
import json
import multiprocessing
import os
from bstack_utils.config import Config
class bstack1ll1l1l1l_opy_():
  def __init__(self, args, logger, bstack1lllll1lll1_opy_, bstack1lllll11l1l_opy_, bstack1llll111lll_opy_):
    self.args = args
    self.logger = logger
    self.bstack1lllll1lll1_opy_ = bstack1lllll1lll1_opy_
    self.bstack1lllll11l1l_opy_ = bstack1lllll11l1l_opy_
    self.bstack1llll111lll_opy_ = bstack1llll111lll_opy_
  def bstack11lllll11_opy_(self, bstack1llll1lll1l_opy_, bstack1l1l1lllll_opy_, bstack1llll111ll1_opy_=False):
    bstack1l11ll1l1_opy_ = []
    manager = multiprocessing.Manager()
    bstack1llll11l1ll_opy_ = manager.list()
    bstack1l111111_opy_ = Config.bstack1llll1l111_opy_()
    if bstack1llll111ll1_opy_:
      for index, platform in enumerate(self.bstack1lllll1lll1_opy_[bstack11lllll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᄯ")]):
        if index == 0:
          bstack1l1l1lllll_opy_[bstack11lllll_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧᄰ")] = self.args
        bstack1l11ll1l1_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack1llll1lll1l_opy_,
                                                    args=(bstack1l1l1lllll_opy_, bstack1llll11l1ll_opy_)))
    else:
      for index, platform in enumerate(self.bstack1lllll1lll1_opy_[bstack11lllll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᄱ")]):
        bstack1l11ll1l1_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack1llll1lll1l_opy_,
                                                    args=(bstack1l1l1lllll_opy_, bstack1llll11l1ll_opy_)))
    i = 0
    for t in bstack1l11ll1l1_opy_:
      try:
        if bstack1l111111_opy_.get_property(bstack11lllll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧᄲ")):
          os.environ[bstack11lllll_opy_ (u"ࠧࡄࡗࡕࡖࡊࡔࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡈࡆ࡚ࡁࠨᄳ")] = json.dumps(self.bstack1lllll1lll1_opy_[bstack11lllll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᄴ")][i % self.bstack1llll111lll_opy_])
      except Exception as e:
        self.logger.debug(bstack11lllll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡴࡶࡲࡶ࡮ࡴࡧࠡࡥࡸࡶࡷ࡫࡮ࡵࠢࡳࡰࡦࡺࡦࡰࡴࡰࠤࡩ࡫ࡴࡢ࡫࡯ࡷ࠿ࠦࡻࡾࠤᄵ").format(str(e)))
      i += 1
      t.start()
    for t in bstack1l11ll1l1_opy_:
      t.join()
    return list(bstack1llll11l1ll_opy_)