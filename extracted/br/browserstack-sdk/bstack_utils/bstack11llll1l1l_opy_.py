# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1ll1ll_opy_ = 2048
bstack1l1l11l_opy_ = 7
def bstack11ll11_opy_ (bstack11l1lll_opy_):
    global bstack1l1l_opy_
    bstack1lll111_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1lll_opy_ = bstack11l1lll_opy_ [:-1]
    bstack1ll1lll_opy_ = bstack1lll111_opy_ % len (bstack1l1lll_opy_)
    bstack11l1l11_opy_ = bstack1l1lll_opy_ [:bstack1ll1lll_opy_] + bstack1l1lll_opy_ [bstack1ll1lll_opy_:]
    if bstack1ll1l1l_opy_:
        bstack111l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    else:
        bstack111l_opy_ = str () .join ([chr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    return eval (bstack111l_opy_)
import os
import json
from bstack_utils.bstack1111l1ll1_opy_ import get_logger
logger = get_logger(__name__)
class bstack11ll1l1l111_opy_(object):
  bstack1l11l111l1_opy_ = os.path.join(os.path.expanduser(bstack11ll11_opy_ (u"ࠩࢁࠫᛥ")), bstack11ll11_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪᛦ"))
  bstack11ll1l11lll_opy_ = os.path.join(bstack1l11l111l1_opy_, bstack11ll11_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࡸ࠴ࡪࡴࡱࡱࠫᛧ"))
  commands_to_wrap = None
  perform_scan = None
  bstack1ll1l1llll_opy_ = None
  bstack1l1l1l111l_opy_ = None
  bstack11lll1l1111_opy_ = None
  bstack11lll1l1ll1_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack11ll11_opy_ (u"ࠬ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠧᛨ")):
      cls.instance = super(bstack11ll1l1l111_opy_, cls).__new__(cls)
      cls.instance.bstack11ll1l11l1l_opy_()
    return cls.instance
  def bstack11ll1l11l1l_opy_(self):
    try:
      with open(self.bstack11ll1l11lll_opy_, bstack11ll11_opy_ (u"࠭ࡲࠨᛩ")) as bstack111111l1l_opy_:
        bstack11ll1l11ll1_opy_ = bstack111111l1l_opy_.read()
        data = json.loads(bstack11ll1l11ll1_opy_)
        if bstack11ll11_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡴࠩᛪ") in data:
          self.bstack11lll111lll_opy_(data[bstack11ll11_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡵࠪ᛫")])
        if bstack11ll11_opy_ (u"ࠩࡶࡧࡷ࡯ࡰࡵࡵࠪ᛬") in data:
          self.bstack11ll1ll1ll_opy_(data[bstack11ll11_opy_ (u"ࠪࡷࡨࡸࡩࡱࡶࡶࠫ᛭")])
        if bstack11ll11_opy_ (u"ࠫࡳࡵ࡮ࡃࡕࡷࡥࡨࡱࡉ࡯ࡨࡵࡥࡆ࠷࠱ࡺࡅ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᛮ") in data:
          self.bstack11ll1l1l11l_opy_(data[bstack11ll11_opy_ (u"ࠬࡴ࡯࡯ࡄࡖࡸࡦࡩ࡫ࡊࡰࡩࡶࡦࡇ࠱࠲ࡻࡆ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᛯ")])
    except:
      pass
  def bstack11ll1l1l11l_opy_(self, bstack11lll1l1ll1_opy_):
    if bstack11lll1l1ll1_opy_ != None:
      self.bstack11lll1l1ll1_opy_ = bstack11lll1l1ll1_opy_
  def bstack11ll1ll1ll_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts.get(bstack11ll11_opy_ (u"࠭ࡳࡤࡣࡱࠫᛰ"),bstack11ll11_opy_ (u"ࠧࠨᛱ"))
      self.bstack1ll1l1llll_opy_ = scripts.get(bstack11ll11_opy_ (u"ࠨࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࠬᛲ"),bstack11ll11_opy_ (u"ࠩࠪᛳ"))
      self.bstack1l1l1l111l_opy_ = scripts.get(bstack11ll11_opy_ (u"ࠪ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࡓࡶ࡯ࡰࡥࡷࡿࠧᛴ"),bstack11ll11_opy_ (u"ࠫࠬᛵ"))
      self.bstack11lll1l1111_opy_ = scripts.get(bstack11ll11_opy_ (u"ࠬࡹࡡࡷࡧࡕࡩࡸࡻ࡬ࡵࡵࠪᛶ"),bstack11ll11_opy_ (u"࠭ࠧᛷ"))
  def bstack11lll111lll_opy_(self, commands_to_wrap):
    if commands_to_wrap != None and len(commands_to_wrap) != 0:
      self.commands_to_wrap = commands_to_wrap
  def store(self):
    try:
      with open(self.bstack11ll1l11lll_opy_, bstack11ll11_opy_ (u"ࠧࡸࠩᛸ")) as file:
        json.dump({
          bstack11ll11_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡵࠥ᛹"): self.commands_to_wrap,
          bstack11ll11_opy_ (u"ࠤࡶࡧࡷ࡯ࡰࡵࡵࠥ᛺"): {
            bstack11ll11_opy_ (u"ࠥࡷࡨࡧ࡮ࠣ᛻"): self.perform_scan,
            bstack11ll11_opy_ (u"ࠦ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࠣ᛼"): self.bstack1ll1l1llll_opy_,
            bstack11ll11_opy_ (u"ࠧ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࡕࡸࡱࡲࡧࡲࡺࠤ᛽"): self.bstack1l1l1l111l_opy_,
            bstack11ll11_opy_ (u"ࠨࡳࡢࡸࡨࡖࡪࡹࡵ࡭ࡶࡶࠦ᛾"): self.bstack11lll1l1111_opy_
          },
          bstack11ll11_opy_ (u"ࠢ࡯ࡱࡱࡆࡘࡺࡡࡤ࡭ࡌࡲ࡫ࡸࡡࡂ࠳࠴ࡽࡈ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠦ᛿"): self.bstack11lll1l1ll1_opy_
        }, file)
    except Exception as e:
      logger.error(bstack11ll11_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡳࡵࡱࡵ࡭ࡳ࡭ࠠࡤࡱࡰࡱࡦࡴࡤࡴ࠼ࠣࡿࢂࠨᜀ").format(e))
      pass
  def bstack1l1ll1l11l_opy_(self, bstack1ll11ll1lll_opy_):
    try:
      return any(command.get(bstack11ll11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᜁ")) == bstack1ll11ll1lll_opy_ for command in self.commands_to_wrap)
    except:
      return False
bstack11llll1l1l_opy_ = bstack11ll1l1l111_opy_()