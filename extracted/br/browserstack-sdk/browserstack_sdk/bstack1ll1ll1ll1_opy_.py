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
import json
import multiprocessing
import os
from bstack_utils.config import Config
class bstack1llllllll11_opy_():
  def __init__(self, args, logger, bstack1llll1lll11_opy_, bstack1lllll11111_opy_, bstack1ll111ll111_opy_):
    self.args = args
    self.logger = logger
    self.bstack1llll1lll11_opy_ = bstack1llll1lll11_opy_
    self.bstack1lllll11111_opy_ = bstack1lllll11111_opy_
    self.bstack1ll111ll111_opy_ = bstack1ll111ll111_opy_
  def bstack11lllll11_opy_(self, bstack1ll11l1l1ll_opy_, bstack1l11ll11l1_opy_, bstack1ll111ll11l_opy_=False):
    bstack1l1ll1l1_opy_ = multiprocessing.get_context(bstack1l111l_opy_ (u"ࠩࡶࡴࡦࡽ࡮ࠨᎫ"))
    bstack11l1llll11_opy_ = []
    manager = bstack1l1ll1l1_opy_.Manager()
    bstack1ll11ll11ll_opy_ = manager.list()
    global_config = Config.bstack1ll11ll111_opy_()
    if bstack1ll111ll11l_opy_:
      for index, platform in enumerate(self.bstack1llll1lll11_opy_[bstack1l111l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭Ꭼ")]):
        if index == 0:
          bstack1l11ll11l1_opy_[bstack1l111l_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧᎭ")] = self.args
        bstack11l1llll11_opy_.append(bstack1l1ll1l1_opy_.Process(name=str(index),
                                          target=bstack1ll11l1l1ll_opy_,
                                          args=(bstack1l11ll11l1_opy_, bstack1ll11ll11ll_opy_)))
    else:
      for index, platform in enumerate(self.bstack1llll1lll11_opy_[bstack1l111l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᎮ")]):
        bstack11l1llll11_opy_.append(bstack1l1ll1l1_opy_.Process(name=str(index),
                                          target=bstack1ll11l1l1ll_opy_,
                                          args=(bstack1l11ll11l1_opy_, bstack1ll11ll11ll_opy_)))
    i = 0
    for t in bstack11l1llll11_opy_:
      try:
        if global_config.get_property(bstack1l111l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧᎯ")):
          os.environ[bstack1l111l_opy_ (u"ࠧࡄࡗࡕࡖࡊࡔࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡈࡆ࡚ࡁࠨᎰ")] = json.dumps(self.bstack1llll1lll11_opy_[bstack1l111l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᎱ")][i % self.bstack1ll111ll111_opy_])
      except Exception as e:
        self.logger.debug(bstack1l111l_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡴࡶࡲࡶ࡮ࡴࡧࠡࡥࡸࡶࡷ࡫࡮ࡵࠢࡳࡰࡦࡺࡦࡰࡴࡰࠤࡩ࡫ࡴࡢ࡫࡯ࡷ࠿ࠦࡻࡾࠤᎲ").format(str(e)))
      i += 1
      t.start()
    for t in bstack11l1llll11_opy_:
      t.join()
    return list(bstack1ll11ll11ll_opy_)