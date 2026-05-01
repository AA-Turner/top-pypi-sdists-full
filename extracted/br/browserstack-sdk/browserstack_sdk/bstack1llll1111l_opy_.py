# coding: UTF-8
import sys
bstack1l11_opy_ = sys.version_info [0] == 2
bstack11_opy_ = 2048
bstackl_opy_ = 7
def bstack111ll_opy_ (bstack1ll1ll1_opy_):
    global bstack1ll111_opy_
    bstack1l11l1l_opy_ = ord (bstack1ll1ll1_opy_ [-1])
    bstack1llll_opy_ = bstack1ll1ll1_opy_ [:-1]
    bstack1l1lll_opy_ = bstack1l11l1l_opy_ % len (bstack1llll_opy_)
    bstack1_opy_ = bstack1llll_opy_ [:bstack1l1lll_opy_] + bstack1llll_opy_ [bstack1l1lll_opy_:]
    if bstack1l11_opy_:
        bstack11l1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    else:
        bstack11l1lll_opy_ = str () .join ([chr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    return eval (bstack11l1lll_opy_)
import json
import multiprocessing
import os
from bstack_utils.config import Config
class bstack11lll1lll1_opy_():
  def __init__(self, args, logger, bstack1llll1ll1l1_opy_, bstack1llll1lll11_opy_, bstack1ll111l1l1l_opy_):
    self.args = args
    self.logger = logger
    self.bstack1llll1ll1l1_opy_ = bstack1llll1ll1l1_opy_
    self.bstack1llll1lll11_opy_ = bstack1llll1lll11_opy_
    self.bstack1ll111l1l1l_opy_ = bstack1ll111l1l1l_opy_
  def bstack11ll1111l1_opy_(self, bstack1ll111l1lll_opy_, bstack11l1111ll1_opy_, bstack1ll111l1l11_opy_=False):
    bstack1ll1l1l1l1_opy_ = multiprocessing.get_context(bstack111ll_opy_ (u"ࠩࡶࡴࡦࡽ࡮ࠨᎹ"))
    bstack111111l11l_opy_ = []
    manager = bstack1ll1l1l1l1_opy_.Manager()
    bstack1ll11l1l1ll_opy_ = manager.list()
    global_config = Config.bstack1l1l11ll1_opy_()
    if bstack1ll111l1l11_opy_:
      for index, platform in enumerate(self.bstack1llll1ll1l1_opy_[bstack111ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭Ꮊ")]):
        if index == 0:
          bstack11l1111ll1_opy_[bstack111ll_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧᎻ")] = self.args
        bstack111111l11l_opy_.append(bstack1ll1l1l1l1_opy_.Process(name=str(index),
                                          target=bstack1ll111l1lll_opy_,
                                          args=(bstack11l1111ll1_opy_, bstack1ll11l1l1ll_opy_)))
    else:
      for index, platform in enumerate(self.bstack1llll1ll1l1_opy_[bstack111ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᎼ")]):
        bstack111111l11l_opy_.append(bstack1ll1l1l1l1_opy_.Process(name=str(index),
                                          target=bstack1ll111l1lll_opy_,
                                          args=(bstack11l1111ll1_opy_, bstack1ll11l1l1ll_opy_)))
    i = 0
    for t in bstack111111l11l_opy_:
      try:
        if global_config.get_property(bstack111ll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧᎽ")):
          os.environ[bstack111ll_opy_ (u"ࠧࡄࡗࡕࡖࡊࡔࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡈࡆ࡚ࡁࠨᎾ")] = json.dumps(self.bstack1llll1ll1l1_opy_[bstack111ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᎿ")][i % self.bstack1ll111l1l1l_opy_])
      except Exception as e:
        self.logger.debug(bstack111ll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡴࡶࡲࡶ࡮ࡴࡧࠡࡥࡸࡶࡷ࡫࡮ࡵࠢࡳࡰࡦࡺࡦࡰࡴࡰࠤࡩ࡫ࡴࡢ࡫࡯ࡷ࠿ࠦࡻࡾࠤᏀ").format(str(e)))
      i += 1
      t.start()
    for t in bstack111111l11l_opy_:
      t.join()
    return list(bstack1ll11l1l1ll_opy_)