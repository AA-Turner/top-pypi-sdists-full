# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1ll1111_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll1l1_opy_ (bstack1lll1ll_opy_):
    global bstack1l1l111_opy_
    bstack1l1111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1lll11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack1l1llll_opy_ = bstack1l1111l_opy_ % len (bstack1lll11_opy_)
    bstack11l111l_opy_ = bstack1lll11_opy_ [:bstack1l1llll_opy_] + bstack1lll11_opy_ [bstack1l1llll_opy_:]
    if bstack1l111l_opy_:
        bstack111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    else:
        bstack111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    return eval (bstack111l1l_opy_)
import os
import json
from bstack_utils.bstack11l1l1l111_opy_ import get_logger
logger = get_logger(__name__)
class bstack11ll11lllll_opy_(object):
  bstack11ll1l11_opy_ = os.path.join(os.path.expanduser(bstack11ll1l1_opy_ (u"ࠧࡿࠩᜆ")), bstack11ll1l1_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨᜇ"))
  bstack11ll1l11111_opy_ = os.path.join(bstack11ll1l11_opy_, bstack11ll1l1_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶ࠲࡯ࡹ࡯࡯ࠩᜈ"))
  commands_to_wrap = None
  perform_scan = None
  bstack1llllllll_opy_ = None
  bstack1l111l11l1_opy_ = None
  bstack11ll1l1l1ll_opy_ = None
  bstack11lll11l11l_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack11ll1l1_opy_ (u"ࠪ࡭ࡳࡹࡴࡢࡰࡦࡩࠬᜉ")):
      cls.instance = super(bstack11ll11lllll_opy_, cls).__new__(cls)
      cls.instance.bstack11ll1l111l1_opy_()
    return cls.instance
  def bstack11ll1l111l1_opy_(self):
    try:
      with open(self.bstack11ll1l11111_opy_, bstack11ll1l1_opy_ (u"ࠫࡷ࠭ᜊ")) as bstack1ll1lll1ll_opy_:
        bstack11ll1l1111l_opy_ = bstack1ll1lll1ll_opy_.read()
        data = json.loads(bstack11ll1l1111l_opy_)
        if bstack11ll1l1_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡹࠧᜋ") in data:
          self.bstack11lll111l11_opy_(data[bstack11ll1l1_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࡳࠨᜌ")])
        if bstack11ll1l1_opy_ (u"ࠧࡴࡥࡵ࡭ࡵࡺࡳࠨᜍ") in data:
          self.bstack1lll1lll11_opy_(data[bstack11ll1l1_opy_ (u"ࠨࡵࡦࡶ࡮ࡶࡴࡴࠩᜎ")])
        if bstack11ll1l1_opy_ (u"ࠩࡱࡳࡳࡈࡓࡵࡣࡦ࡯ࡎࡴࡦࡳࡣࡄ࠵࠶ࡿࡃࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᜏ") in data:
          self.bstack11ll11llll1_opy_(data[bstack11ll1l1_opy_ (u"ࠪࡲࡴࡴࡂࡔࡶࡤࡧࡰࡏ࡮ࡧࡴࡤࡅ࠶࠷ࡹࡄࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᜐ")])
    except:
      pass
  def bstack11ll11llll1_opy_(self, bstack11lll11l11l_opy_):
    if bstack11lll11l11l_opy_ != None:
      self.bstack11lll11l11l_opy_ = bstack11lll11l11l_opy_
  def bstack1lll1lll11_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts.get(bstack11ll1l1_opy_ (u"ࠫࡸࡩࡡ࡯ࠩᜑ"),bstack11ll1l1_opy_ (u"ࠬ࠭ᜒ"))
      self.bstack1llllllll_opy_ = scripts.get(bstack11ll1l1_opy_ (u"࠭ࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࠪᜓ"),bstack11ll1l1_opy_ (u"ࠧࠨ᜔"))
      self.bstack1l111l11l1_opy_ = scripts.get(bstack11ll1l1_opy_ (u"ࠨࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࡘࡻ࡭࡮ࡣࡵࡽ᜕ࠬ"),bstack11ll1l1_opy_ (u"ࠩࠪ᜖"))
      self.bstack11ll1l1l1ll_opy_ = scripts.get(bstack11ll1l1_opy_ (u"ࠪࡷࡦࡼࡥࡓࡧࡶࡹࡱࡺࡳࠨ᜗"),bstack11ll1l1_opy_ (u"ࠫࠬ᜘"))
  def bstack11lll111l11_opy_(self, commands_to_wrap):
    if commands_to_wrap != None and len(commands_to_wrap) != 0:
      self.commands_to_wrap = commands_to_wrap
  def store(self):
    try:
      with open(self.bstack11ll1l11111_opy_, bstack11ll1l1_opy_ (u"ࠬࡽࠧ᜙")) as file:
        json.dump({
          bstack11ll1l1_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪࡳࠣ᜚"): self.commands_to_wrap,
          bstack11ll1l1_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࡳࠣ᜛"): {
            bstack11ll1l1_opy_ (u"ࠣࡵࡦࡥࡳࠨ᜜"): self.perform_scan,
            bstack11ll1l1_opy_ (u"ࠤࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸࠨ᜝"): self.bstack1llllllll_opy_,
            bstack11ll1l1_opy_ (u"ࠥ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࡓࡶ࡯ࡰࡥࡷࡿࠢ᜞"): self.bstack1l111l11l1_opy_,
            bstack11ll1l1_opy_ (u"ࠦࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠤᜟ"): self.bstack11ll1l1l1ll_opy_
          },
          bstack11ll1l1_opy_ (u"ࠧࡴ࡯࡯ࡄࡖࡸࡦࡩ࡫ࡊࡰࡩࡶࡦࡇ࠱࠲ࡻࡆ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠤᜠ"): self.bstack11lll11l11l_opy_
        }, file)
    except Exception as e:
      logger.error(bstack11ll1l1_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡸࡺ࡯ࡳ࡫ࡱ࡫ࠥࡩ࡯࡮࡯ࡤࡲࡩࡹ࠺ࠡࡽࢀࠦᜡ").format(e))
      pass
  def bstack1ll1l1l1ll_opy_(self, bstack1ll1l11lll1_opy_):
    try:
      return any(command.get(bstack11ll1l1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᜢ")) == bstack1ll1l11lll1_opy_ for command in self.commands_to_wrap)
    except:
      return False
bstack1ll111ll11_opy_ = bstack11ll11lllll_opy_()