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
import json
import multiprocessing
import os
from bstack_utils.config import Config
class bstack11l1ll11_opy_():
  def __init__(self, args, logger, bstack1lll1lllll1_opy_, bstack1lll1l11l1l_opy_, bstack1lll11llll1_opy_):
    self.args = args
    self.logger = logger
    self.bstack1lll1lllll1_opy_ = bstack1lll1lllll1_opy_
    self.bstack1lll1l11l1l_opy_ = bstack1lll1l11l1l_opy_
    self.bstack1lll11llll1_opy_ = bstack1lll11llll1_opy_
  def bstack11l1ll1ll1_opy_(self, bstack1lll1l111ll_opy_, bstack1l11l1l1ll_opy_, bstack1lll11lll1l_opy_=False):
    bstack1l1lllll11_opy_ = []
    manager = multiprocessing.Manager()
    bstack1lll1lll1ll_opy_ = manager.list()
    global_config = Config.get_instance()
    if bstack1lll11lll1l_opy_:
      for index, platform in enumerate(self.bstack1lll1lllll1_opy_[bstack1ll111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᇳ")]):
        if index == 0:
          bstack1l11l1l1ll_opy_[bstack1ll111_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧᇴ")] = self.args
        bstack1l1lllll11_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack1lll1l111ll_opy_,
                                                    args=(bstack1l11l1l1ll_opy_, bstack1lll1lll1ll_opy_)))
    else:
      for index, platform in enumerate(self.bstack1lll1lllll1_opy_[bstack1ll111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᇵ")]):
        bstack1l1lllll11_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack1lll1l111ll_opy_,
                                                    args=(bstack1l11l1l1ll_opy_, bstack1lll1lll1ll_opy_)))
    i = 0
    for t in bstack1l1lllll11_opy_:
      try:
        if global_config.get_property(bstack1ll111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧᇶ")):
          os.environ[bstack1ll111_opy_ (u"ࠧࡄࡗࡕࡖࡊࡔࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡈࡆ࡚ࡁࠨᇷ")] = json.dumps(self.bstack1lll1lllll1_opy_[bstack1ll111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᇸ")][i % self.bstack1lll11llll1_opy_])
      except Exception as e:
        self.logger.debug(bstack1ll111_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡴࡶࡲࡶ࡮ࡴࡧࠡࡥࡸࡶࡷ࡫࡮ࡵࠢࡳࡰࡦࡺࡦࡰࡴࡰࠤࡩ࡫ࡴࡢ࡫࡯ࡷ࠿ࠦࡻࡾࠤᇹ").format(str(e)))
      i += 1
      t.start()
    for t in bstack1l1lllll11_opy_:
      t.join()
    return list(bstack1lll1lll1ll_opy_)