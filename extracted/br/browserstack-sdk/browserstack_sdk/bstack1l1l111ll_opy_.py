# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack11_opy_ = 7
def bstack11l1111_opy_ (bstack111l111_opy_):
    global bstack1l1l11_opy_
    bstack1lll11l_opy_ = ord (bstack111l111_opy_ [-1])
    bstack11l11l1_opy_ = bstack111l111_opy_ [:-1]
    bstack1111lll_opy_ = bstack1lll11l_opy_ % len (bstack11l11l1_opy_)
    bstack11lll11_opy_ = bstack11l11l1_opy_ [:bstack1111lll_opy_] + bstack11l11l1_opy_ [bstack1111lll_opy_:]
    if bstack1l111l_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    return eval (bstack111l11_opy_)
import json
import multiprocessing
import os
from bstack_utils.config import Config
class bstack11llllllll_opy_():
  def __init__(self, args, logger, bstack1111l1lll1_opy_, bstack11111ll1l1_opy_, bstack11111l1111_opy_):
    self.args = args
    self.logger = logger
    self.bstack1111l1lll1_opy_ = bstack1111l1lll1_opy_
    self.bstack11111ll1l1_opy_ = bstack11111ll1l1_opy_
    self.bstack11111l1111_opy_ = bstack11111l1111_opy_
  def bstack11l11l11l_opy_(self, bstack11111l1l11_opy_, bstack1ll11l1ll_opy_, bstack11111l111l_opy_=False):
    bstack1l1ll11l1l_opy_ = []
    manager = multiprocessing.Manager()
    bstack1111l1l1l1_opy_ = manager.list()
    bstack1l1l11l1ll_opy_ = Config.bstack11l1l11l11_opy_()
    if bstack11111l111l_opy_:
      for index, platform in enumerate(self.bstack1111l1lll1_opy_[bstack11l1111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ႀ")]):
        if index == 0:
          bstack1ll11l1ll_opy_[bstack11l1111_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧႁ")] = self.args
        bstack1l1ll11l1l_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack11111l1l11_opy_,
                                                    args=(bstack1ll11l1ll_opy_, bstack1111l1l1l1_opy_)))
    else:
      for index, platform in enumerate(self.bstack1111l1lll1_opy_[bstack11l1111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨႂ")]):
        bstack1l1ll11l1l_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack11111l1l11_opy_,
                                                    args=(bstack1ll11l1ll_opy_, bstack1111l1l1l1_opy_)))
    i = 0
    for t in bstack1l1ll11l1l_opy_:
      try:
        if bstack1l1l11l1ll_opy_.get_property(bstack11l1111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧႃ")):
          os.environ[bstack11l1111_opy_ (u"ࠧࡄࡗࡕࡖࡊࡔࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡈࡆ࡚ࡁࠨႄ")] = json.dumps(self.bstack1111l1lll1_opy_[bstack11l1111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫႅ")][i % self.bstack11111l1111_opy_])
      except Exception as e:
        self.logger.debug(bstack11l1111_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡴࡶࡲࡶ࡮ࡴࡧࠡࡥࡸࡶࡷ࡫࡮ࡵࠢࡳࡰࡦࡺࡦࡰࡴࡰࠤࡩ࡫ࡴࡢ࡫࡯ࡷ࠿ࠦࡻࡾࠤႆ").format(str(e)))
      i += 1
      t.start()
    for t in bstack1l1ll11l1l_opy_:
      t.join()
    return list(bstack1111l1l1l1_opy_)