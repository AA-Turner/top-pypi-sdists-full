# coding: UTF-8
import sys
bstack111l1l1_opy_ = sys.version_info [0] == 2
bstack1ll1l1l_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack11lll_opy_ (bstack111ll1l_opy_):
    global bstack1l111l_opy_
    bstack1lllll1l_opy_ = ord (bstack111ll1l_opy_ [-1])
    bstack11111ll_opy_ = bstack111ll1l_opy_ [:-1]
    bstack11ll1l1_opy_ = bstack1lllll1l_opy_ % len (bstack11111ll_opy_)
    bstack1lll1l1_opy_ = bstack11111ll_opy_ [:bstack11ll1l1_opy_] + bstack11111ll_opy_ [bstack11ll1l1_opy_:]
    if bstack111l1l1_opy_:
        bstack1ll1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1l1l_opy_ - (bstack11l11l_opy_ + bstack1lllll1l_opy_) % bstack1l11l11_opy_) for bstack11l11l_opy_, char in enumerate (bstack1lll1l1_opy_)])
    else:
        bstack1ll1ll1_opy_ = str () .join ([chr (ord (char) - bstack1ll1l1l_opy_ - (bstack11l11l_opy_ + bstack1lllll1l_opy_) % bstack1l11l11_opy_) for bstack11l11l_opy_, char in enumerate (bstack1lll1l1_opy_)])
    return eval (bstack1ll1ll1_opy_)
import json
import multiprocessing
import os
from bstack_utils.config import Config
class bstack11ll1ll11l_opy_():
  def __init__(self, args, logger, bstack1111ll1ll1_opy_, bstack1111lll111_opy_, bstack1111ll11l1_opy_):
    self.args = args
    self.logger = logger
    self.bstack1111ll1ll1_opy_ = bstack1111ll1ll1_opy_
    self.bstack1111lll111_opy_ = bstack1111lll111_opy_
    self.bstack1111ll11l1_opy_ = bstack1111ll11l1_opy_
  def bstack1111lll1_opy_(self, bstack1111ll1lll_opy_, bstack1l1l1llll1_opy_, bstack1111ll111l_opy_=False):
    bstack111l1111_opy_ = []
    manager = multiprocessing.Manager()
    bstack111l11111l_opy_ = manager.list()
    bstack1llllll11_opy_ = Config.bstack1l1l1l1ll1_opy_()
    if bstack1111ll111l_opy_:
      for index, platform in enumerate(self.bstack1111ll1ll1_opy_[bstack11lll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨဋ")]):
        if index == 0:
          bstack1l1l1llll1_opy_[bstack11lll_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩဌ")] = self.args
        bstack111l1111_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack1111ll1lll_opy_,
                                                    args=(bstack1l1l1llll1_opy_, bstack111l11111l_opy_)))
    else:
      for index, platform in enumerate(self.bstack1111ll1ll1_opy_[bstack11lll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪဍ")]):
        bstack111l1111_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack1111ll1lll_opy_,
                                                    args=(bstack1l1l1llll1_opy_, bstack111l11111l_opy_)))
    i = 0
    for t in bstack111l1111_opy_:
      try:
        if bstack1llllll11_opy_.get_property(bstack11lll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩဎ")):
          os.environ[bstack11lll_opy_ (u"ࠩࡆ࡙ࡗࡘࡅࡏࡖࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡊࡁࡕࡃࠪဏ")] = json.dumps(self.bstack1111ll1ll1_opy_[bstack11lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭တ")][i % self.bstack1111ll11l1_opy_])
      except Exception as e:
        self.logger.debug(bstack11lll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡶࡸࡴࡸࡩ࡯ࡩࠣࡧࡺࡸࡲࡦࡰࡷࠤࡵࡲࡡࡵࡨࡲࡶࡲࠦࡤࡦࡶࡤ࡭ࡱࡹ࠺ࠡࡽࢀࠦထ").format(str(e)))
      i += 1
      t.start()
    for t in bstack111l1111_opy_:
      t.join()
    return list(bstack111l11111l_opy_)