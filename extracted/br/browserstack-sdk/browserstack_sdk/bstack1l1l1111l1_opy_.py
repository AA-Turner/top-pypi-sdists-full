# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack1111l_opy_ = 7
def bstack111lll_opy_ (bstack1lll1l_opy_):
    global bstack1l11lll_opy_
    bstack1ll1l1_opy_ = ord (bstack1lll1l_opy_ [-1])
    bstack1ll1l11_opy_ = bstack1lll1l_opy_ [:-1]
    bstack1l_opy_ = bstack1ll1l1_opy_ % len (bstack1ll1l11_opy_)
    bstack1l11ll_opy_ = bstack1ll1l11_opy_ [:bstack1l_opy_] + bstack1ll1l11_opy_ [bstack1l_opy_:]
    if bstack111ll1_opy_:
        bstack1l1l11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    else:
        bstack1l1l11l_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    return eval (bstack1l1l11l_opy_)
import json
import multiprocessing
import os
from bstack_utils.config import Config
class bstack11111l11_opy_():
  def __init__(self, args, logger, bstack1111l1l1ll_opy_, bstack1111ll1111_opy_, bstack1111l111ll_opy_):
    self.args = args
    self.logger = logger
    self.bstack1111l1l1ll_opy_ = bstack1111l1l1ll_opy_
    self.bstack1111ll1111_opy_ = bstack1111ll1111_opy_
    self.bstack1111l111ll_opy_ = bstack1111l111ll_opy_
  def bstack1ll11ll111_opy_(self, bstack1111ll1l11_opy_, bstack1lll1l11_opy_, bstack1111l11l11_opy_=False):
    bstack1l111ll1l_opy_ = []
    manager = multiprocessing.Manager()
    bstack1111l1llll_opy_ = manager.list()
    bstack1ll1l11ll_opy_ = Config.bstack1ll11lll1l_opy_()
    if bstack1111l11l11_opy_:
      for index, platform in enumerate(self.bstack1111l1l1ll_opy_[bstack111lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ်࠭")]):
        if index == 0:
          bstack1lll1l11_opy_[bstack111lll_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧျ")] = self.args
        bstack1l111ll1l_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack1111ll1l11_opy_,
                                                    args=(bstack1lll1l11_opy_, bstack1111l1llll_opy_)))
    else:
      for index, platform in enumerate(self.bstack1111l1l1ll_opy_[bstack111lll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨြ")]):
        bstack1l111ll1l_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack1111ll1l11_opy_,
                                                    args=(bstack1lll1l11_opy_, bstack1111l1llll_opy_)))
    i = 0
    for t in bstack1l111ll1l_opy_:
      try:
        if bstack1ll1l11ll_opy_.get_property(bstack111lll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧွ")):
          os.environ[bstack111lll_opy_ (u"ࠧࡄࡗࡕࡖࡊࡔࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡈࡆ࡚ࡁࠨှ")] = json.dumps(self.bstack1111l1l1ll_opy_[bstack111lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫဿ")][i % self.bstack1111l111ll_opy_])
      except Exception as e:
        self.logger.debug(bstack111lll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡴࡶࡲࡶ࡮ࡴࡧࠡࡥࡸࡶࡷ࡫࡮ࡵࠢࡳࡰࡦࡺࡦࡰࡴࡰࠤࡩ࡫ࡴࡢ࡫࡯ࡷ࠿ࠦࡻࡾࠤ၀").format(str(e)))
      i += 1
      t.start()
    for t in bstack1l111ll1l_opy_:
      t.join()
    return list(bstack1111l1llll_opy_)