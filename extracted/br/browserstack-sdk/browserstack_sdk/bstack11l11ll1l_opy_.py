# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack111l11l_opy_ = 2048
bstack11l_opy_ = 7
def bstack1l1llll_opy_ (bstack11ll1l1_opy_):
    global bstack111111l_opy_
    bstack111lll_opy_ = ord (bstack11ll1l1_opy_ [-1])
    bstack11llll_opy_ = bstack11ll1l1_opy_ [:-1]
    bstack1l11_opy_ = bstack111lll_opy_ % len (bstack11llll_opy_)
    bstackl_opy_ = bstack11llll_opy_ [:bstack1l11_opy_] + bstack11llll_opy_ [bstack1l11_opy_:]
    if bstack1lll_opy_:
        bstack11l111_opy_ = unicode () .join ([unichr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    else:
        bstack11l111_opy_ = str () .join ([chr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    return eval (bstack11l111_opy_)
import json
import multiprocessing
import os
from bstack_utils.config import Config
class bstack11l11ll11_opy_():
  def __init__(self, args, logger, bstack1ll1llll_opy_, bstack1ll1l11l_opy_, bstack11l11l1l1_opy_):
    self.args = args
    self.logger = logger
    self.bstack1ll1llll_opy_ = bstack1ll1llll_opy_
    self.bstack1ll1l11l_opy_ = bstack1ll1l11l_opy_
    self.bstack11l11l1l1_opy_ = bstack11l11l1l1_opy_
  def bstack11l1l1l11_opy_(self, bstack11ll11ll1_opy_, bstack11l1l11l1_opy_, bstack11l11l1ll_opy_=False):
    bstack11lllllll_opy_ = multiprocessing.get_context(bstack1l1llll_opy_ (u"ࠨࡵࡳࡥࡼࡴࠧಎ"))
    bstack11l1ll1ll_opy_ = []
    manager = bstack11lllllll_opy_.Manager()
    bstack11lll111l_opy_ = manager.list()
    global_config = Config.bstack1lll1l11_opy_()
    if bstack11l11l1ll_opy_:
      for index, platform in enumerate(self.bstack1ll1llll_opy_[bstack1l1llll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬಏ")]):
        if index == 0:
          bstack11l1l11l1_opy_[bstack1l1llll_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ಐ")] = self.args
        bstack11l1ll1ll_opy_.append(bstack11lllllll_opy_.Process(name=str(index),
                                          target=bstack11ll11ll1_opy_,
                                          args=(bstack11l1l11l1_opy_, bstack11lll111l_opy_)))
    else:
      for index, platform in enumerate(self.bstack1ll1llll_opy_[bstack1l1llll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ಑")]):
        bstack11l1ll1ll_opy_.append(bstack11lllllll_opy_.Process(name=str(index),
                                          target=bstack11ll11ll1_opy_,
                                          args=(bstack11l1l11l1_opy_, bstack11lll111l_opy_)))
    i = 0
    for t in bstack11l1ll1ll_opy_:
      try:
        if global_config.get_property(bstack1l1llll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭ಒ")):
          os.environ[bstack1l1llll_opy_ (u"࠭ࡃࡖࡔࡕࡉࡓ࡚࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡇࡅ࡙ࡇࠧಓ")] = json.dumps(self.bstack1ll1llll_opy_[bstack1l1llll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪಔ")][i % self.bstack11l11l1l1_opy_])
      except Exception as e:
        self.logger.debug(bstack1l1llll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡳࡵࡱࡵ࡭ࡳ࡭ࠠࡤࡷࡵࡶࡪࡴࡴࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣࡨࡪࡺࡡࡪ࡮ࡶ࠾ࠥࢁࡽࠣಕ").format(str(e)))
      i += 1
      t.start()
    for t in bstack11l1ll1ll_opy_:
      t.join()
    return list(bstack11lll111l_opy_)