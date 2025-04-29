# coding: UTF-8
import sys
bstack11l1l1_opy_ = sys.version_info [0] == 2
bstack111l1l1_opy_ = 2048
bstack11l11ll_opy_ = 7
def bstack1llllll_opy_ (bstack1ll111l_opy_):
    global bstack1l111l_opy_
    bstack1l11l_opy_ = ord (bstack1ll111l_opy_ [-1])
    bstack1111l1l_opy_ = bstack1ll111l_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack1l11l_opy_ % len (bstack1111l1l_opy_)
    bstack1ll1_opy_ = bstack1111l1l_opy_ [:bstack11ll1ll_opy_] + bstack1111l1l_opy_ [bstack11ll1ll_opy_:]
    if bstack11l1l1_opy_:
        bstack1lllll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack111l1l1_opy_ - (bstack11ll1_opy_ + bstack1l11l_opy_) % bstack11l11ll_opy_) for bstack11ll1_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1lllll1l_opy_ = str () .join ([chr (ord (char) - bstack111l1l1_opy_ - (bstack11ll1_opy_ + bstack1l11l_opy_) % bstack11l11ll_opy_) for bstack11ll1_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1lllll1l_opy_)
import json
import multiprocessing
import os
from bstack_utils.config import Config
class bstack1ll11l1ll_opy_():
  def __init__(self, args, logger, bstack1111ll1ll1_opy_, bstack1111ll1l11_opy_, bstack1111ll11ll_opy_):
    self.args = args
    self.logger = logger
    self.bstack1111ll1ll1_opy_ = bstack1111ll1ll1_opy_
    self.bstack1111ll1l11_opy_ = bstack1111ll1l11_opy_
    self.bstack1111ll11ll_opy_ = bstack1111ll11ll_opy_
  def bstack111l1ll1l_opy_(self, bstack111l1111l1_opy_, bstack11lll11111_opy_, bstack1111ll11l1_opy_=False):
    bstack1l1l11llll_opy_ = []
    manager = multiprocessing.Manager()
    bstack1111llll11_opy_ = manager.list()
    bstack1l1ll1l1l1_opy_ = Config.bstack11ll1ll1l1_opy_()
    if bstack1111ll11l1_opy_:
      for index, platform in enumerate(self.bstack1111ll1ll1_opy_[bstack1llllll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨဋ")]):
        if index == 0:
          bstack11lll11111_opy_[bstack1llllll_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩဌ")] = self.args
        bstack1l1l11llll_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack111l1111l1_opy_,
                                                    args=(bstack11lll11111_opy_, bstack1111llll11_opy_)))
    else:
      for index, platform in enumerate(self.bstack1111ll1ll1_opy_[bstack1llllll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪဍ")]):
        bstack1l1l11llll_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack111l1111l1_opy_,
                                                    args=(bstack11lll11111_opy_, bstack1111llll11_opy_)))
    i = 0
    for t in bstack1l1l11llll_opy_:
      try:
        if bstack1l1ll1l1l1_opy_.get_property(bstack1llllll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩဎ")):
          os.environ[bstack1llllll_opy_ (u"ࠩࡆ࡙ࡗࡘࡅࡏࡖࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡊࡁࡕࡃࠪဏ")] = json.dumps(self.bstack1111ll1ll1_opy_[bstack1llllll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭တ")][i % self.bstack1111ll11ll_opy_])
      except Exception as e:
        self.logger.debug(bstack1llllll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡶࡸࡴࡸࡩ࡯ࡩࠣࡧࡺࡸࡲࡦࡰࡷࠤࡵࡲࡡࡵࡨࡲࡶࡲࠦࡤࡦࡶࡤ࡭ࡱࡹ࠺ࠡࡽࢀࠦထ").format(str(e)))
      i += 1
      t.start()
    for t in bstack1l1l11llll_opy_:
      t.join()
    return list(bstack1111llll11_opy_)