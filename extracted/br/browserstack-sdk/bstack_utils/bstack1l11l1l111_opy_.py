# coding: UTF-8
import sys
bstack1ll11l_opy_ = sys.version_info [0] == 2
bstack111111l_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack11l1_opy_ (bstack1llllll1_opy_):
    global bstack1l11ll_opy_
    bstack1ll111l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1l111_opy_ = bstack1ll111l_opy_ % len (bstack1l1l1l1_opy_)
    bstack11ll1ll_opy_ = bstack1l1l1l1_opy_ [:bstack1l111_opy_] + bstack1l1l1l1_opy_ [bstack1l111_opy_:]
    if bstack1ll11l_opy_:
        bstack11l1ll_opy_ = unicode () .join ([unichr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    else:
        bstack11l1ll_opy_ = str () .join ([chr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    return eval (bstack11l1ll_opy_)
import os
import json
from bstack_utils.bstack1l1111111_opy_ import get_logger
logger = get_logger(__name__)
class bstack11ll11lll11_opy_(object):
  bstack1l1lll1111_opy_ = os.path.join(os.path.expanduser(bstack11l1_opy_ (u"ࠧࡿࠩᝅ")), bstack11l1_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨᝆ"))
  bstack11ll11lll1l_opy_ = os.path.join(bstack1l1lll1111_opy_, bstack11l1_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶ࠲࡯ࡹ࡯࡯ࠩᝇ"))
  commands_to_wrap = None
  perform_scan = None
  bstack1lllllll1l_opy_ = None
  bstack11l1l1llll_opy_ = None
  bstack11ll1ll1111_opy_ = None
  bstack11ll1lll111_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack11l1_opy_ (u"ࠪ࡭ࡳࡹࡴࡢࡰࡦࡩࠬᝈ")):
      cls.instance = super(bstack11ll11lll11_opy_, cls).__new__(cls)
      cls.instance.bstack11ll11llll1_opy_()
    return cls.instance
  def bstack11ll11llll1_opy_(self):
    try:
      with open(self.bstack11ll11lll1l_opy_, bstack11l1_opy_ (u"ࠫࡷ࠭ᝉ")) as bstack1llllll1l_opy_:
        bstack11ll11ll1ll_opy_ = bstack1llllll1l_opy_.read()
        data = json.loads(bstack11ll11ll1ll_opy_)
        if bstack11l1_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡹࠧᝊ") in data:
          self.bstack11ll1l11l11_opy_(data[bstack11l1_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࡳࠨᝋ")])
        if bstack11l1_opy_ (u"ࠧࡴࡥࡵ࡭ࡵࡺࡳࠨᝌ") in data:
          self.bstack1llll11111_opy_(data[bstack11l1_opy_ (u"ࠨࡵࡦࡶ࡮ࡶࡴࡴࠩᝍ")])
        if bstack11l1_opy_ (u"ࠩࡱࡳࡳࡈࡓࡵࡣࡦ࡯ࡎࡴࡦࡳࡣࡄ࠵࠶ࡿࡃࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᝎ") in data:
          self.bstack11ll11lllll_opy_(data[bstack11l1_opy_ (u"ࠪࡲࡴࡴࡂࡔࡶࡤࡧࡰࡏ࡮ࡧࡴࡤࡅ࠶࠷ࡹࡄࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᝏ")])
    except:
      pass
  def bstack11ll11lllll_opy_(self, bstack11ll1lll111_opy_):
    if bstack11ll1lll111_opy_ != None:
      self.bstack11ll1lll111_opy_ = bstack11ll1lll111_opy_
  def bstack1llll11111_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts.get(bstack11l1_opy_ (u"ࠫࡸࡩࡡ࡯ࠩᝐ"),bstack11l1_opy_ (u"ࠬ࠭ᝑ"))
      self.bstack1lllllll1l_opy_ = scripts.get(bstack11l1_opy_ (u"࠭ࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࠪᝒ"),bstack11l1_opy_ (u"ࠧࠨᝓ"))
      self.bstack11l1l1llll_opy_ = scripts.get(bstack11l1_opy_ (u"ࠨࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࡘࡻ࡭࡮ࡣࡵࡽࠬ᝔"),bstack11l1_opy_ (u"ࠩࠪ᝕"))
      self.bstack11ll1ll1111_opy_ = scripts.get(bstack11l1_opy_ (u"ࠪࡷࡦࡼࡥࡓࡧࡶࡹࡱࡺࡳࠨ᝖"),bstack11l1_opy_ (u"ࠫࠬ᝗"))
  def bstack11ll1l11l11_opy_(self, commands_to_wrap):
    if commands_to_wrap != None and len(commands_to_wrap) != 0:
      self.commands_to_wrap = commands_to_wrap
  def store(self):
    try:
      with open(self.bstack11ll11lll1l_opy_, bstack11l1_opy_ (u"ࠬࡽࠧ᝘")) as file:
        json.dump({
          bstack11l1_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪࡳࠣ᝙"): self.commands_to_wrap,
          bstack11l1_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࡳࠣ᝚"): {
            bstack11l1_opy_ (u"ࠣࡵࡦࡥࡳࠨ᝛"): self.perform_scan,
            bstack11l1_opy_ (u"ࠤࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸࠨ᝜"): self.bstack1lllllll1l_opy_,
            bstack11l1_opy_ (u"ࠥ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࡓࡶ࡯ࡰࡥࡷࡿࠢ᝝"): self.bstack11l1l1llll_opy_,
            bstack11l1_opy_ (u"ࠦࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠤ᝞"): self.bstack11ll1ll1111_opy_
          },
          bstack11l1_opy_ (u"ࠧࡴ࡯࡯ࡄࡖࡸࡦࡩ࡫ࡊࡰࡩࡶࡦࡇ࠱࠲ࡻࡆ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠤ᝟"): self.bstack11ll1lll111_opy_
        }, file)
    except Exception as e:
      logger.error(bstack11l1_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡸࡺ࡯ࡳ࡫ࡱ࡫ࠥࡩ࡯࡮࡯ࡤࡲࡩࡹ࠺ࠡࡽࢀࠦᝠ").format(e))
      pass
  def bstack1lll1lll11_opy_(self, command_name):
    try:
      return any(command.get(bstack11l1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᝡ")) == command_name for command in self.commands_to_wrap)
    except:
      return False
bstack1l11l1l111_opy_ = bstack11ll11lll11_opy_()