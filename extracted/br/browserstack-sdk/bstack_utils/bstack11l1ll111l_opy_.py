# coding: UTF-8
import sys
bstack1ll11l1_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack11lll_opy_ = 7
def bstack1l11l11_opy_ (bstack1llll11_opy_):
    global bstack11ll1l1_opy_
    bstack111l111_opy_ = ord (bstack1llll11_opy_ [-1])
    bstack11lll11_opy_ = bstack1llll11_opy_ [:-1]
    bstack1ll11_opy_ = bstack111l111_opy_ % len (bstack11lll11_opy_)
    bstack1l1l_opy_ = bstack11lll11_opy_ [:bstack1ll11_opy_] + bstack11lll11_opy_ [bstack1ll11_opy_:]
    if bstack1ll11l1_opy_:
        bstack11l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack111l1l1_opy_ + bstack111l111_opy_) % bstack11lll_opy_) for bstack111l1l1_opy_, char in enumerate (bstack1l1l_opy_)])
    else:
        bstack11l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack111l1l1_opy_ + bstack111l111_opy_) % bstack11lll_opy_) for bstack111l1l1_opy_, char in enumerate (bstack1l1l_opy_)])
    return eval (bstack11l1l1_opy_)
import os
import json
from bstack_utils.bstack1l1ll11lll_opy_ import get_logger
logger = get_logger(__name__)
class bstack11ll11ll111_opy_(object):
  bstack1l111l1l_opy_ = os.path.join(os.path.expanduser(bstack1l11l11_opy_ (u"࠭ࡾࠨᝄ")), bstack1l11l11_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧᝅ"))
  bstack11ll11l1ll1_opy_ = os.path.join(bstack1l111l1l_opy_, bstack1l11l11_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡵ࠱࡮ࡸࡵ࡮ࠨᝆ"))
  commands_to_wrap = None
  perform_scan = None
  bstack1l1ll1l11_opy_ = None
  bstack11ll1ll111_opy_ = None
  bstack11lll111l1l_opy_ = None
  bstack11lll111l11_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack1l11l11_opy_ (u"ࠩ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠫᝇ")):
      cls.instance = super(bstack11ll11ll111_opy_, cls).__new__(cls)
      cls.instance.bstack11ll11ll1l1_opy_()
    return cls.instance
  def bstack11ll11ll1l1_opy_(self):
    try:
      with open(self.bstack11ll11l1ll1_opy_, bstack1l11l11_opy_ (u"ࠪࡶࠬᝈ")) as bstack1l1ll1l1_opy_:
        bstack11ll11ll11l_opy_ = bstack1l1ll1l1_opy_.read()
        data = json.loads(bstack11ll11ll11l_opy_)
        if bstack1l11l11_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࡸ࠭ᝉ") in data:
          self.bstack11lll11111l_opy_(data[bstack1l11l11_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡹࠧᝊ")])
        if bstack1l11l11_opy_ (u"࠭ࡳࡤࡴ࡬ࡴࡹࡹࠧᝋ") in data:
          self.bstack1llll1111l_opy_(data[bstack1l11l11_opy_ (u"ࠧࡴࡥࡵ࡭ࡵࡺࡳࠨᝌ")])
        if bstack1l11l11_opy_ (u"ࠨࡰࡲࡲࡇ࡙ࡴࡢࡥ࡮ࡍࡳ࡬ࡲࡢࡃ࠴࠵ࡾࡉࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᝍ") in data:
          self.bstack11ll11l1lll_opy_(data[bstack1l11l11_opy_ (u"ࠩࡱࡳࡳࡈࡓࡵࡣࡦ࡯ࡎࡴࡦࡳࡣࡄ࠵࠶ࡿࡃࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᝎ")])
    except:
      pass
  def bstack11ll11l1lll_opy_(self, bstack11lll111l11_opy_):
    if bstack11lll111l11_opy_ != None:
      self.bstack11lll111l11_opy_ = bstack11lll111l11_opy_
  def bstack1llll1111l_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts.get(bstack1l11l11_opy_ (u"ࠪࡷࡨࡧ࡮ࠨᝏ"),bstack1l11l11_opy_ (u"ࠫࠬᝐ"))
      self.bstack1l1ll1l11_opy_ = scripts.get(bstack1l11l11_opy_ (u"ࠬ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࠩᝑ"),bstack1l11l11_opy_ (u"࠭ࠧᝒ"))
      self.bstack11ll1ll111_opy_ = scripts.get(bstack1l11l11_opy_ (u"ࠧࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࡗࡺࡳ࡭ࡢࡴࡼࠫᝓ"),bstack1l11l11_opy_ (u"ࠨࠩ᝔"))
      self.bstack11lll111l1l_opy_ = scripts.get(bstack1l11l11_opy_ (u"ࠩࡶࡥࡻ࡫ࡒࡦࡵࡸࡰࡹࡹࠧ᝕"),bstack1l11l11_opy_ (u"ࠪࠫ᝖"))
  def bstack11lll11111l_opy_(self, commands_to_wrap):
    if commands_to_wrap != None and len(commands_to_wrap) != 0:
      self.commands_to_wrap = commands_to_wrap
  def store(self):
    try:
      with open(self.bstack11ll11l1ll1_opy_, bstack1l11l11_opy_ (u"ࠫࡼ࠭᝗")) as file:
        json.dump({
          bstack1l11l11_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡹࠢ᝘"): self.commands_to_wrap,
          bstack1l11l11_opy_ (u"ࠨࡳࡤࡴ࡬ࡴࡹࡹࠢ᝙"): {
            bstack1l11l11_opy_ (u"ࠢࡴࡥࡤࡲࠧ᝚"): self.perform_scan,
            bstack1l11l11_opy_ (u"ࠣࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࠧ᝛"): self.bstack1l1ll1l11_opy_,
            bstack1l11l11_opy_ (u"ࠤࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸ࡙ࡵ࡮࡯ࡤࡶࡾࠨ᝜"): self.bstack11ll1ll111_opy_,
            bstack1l11l11_opy_ (u"ࠥࡷࡦࡼࡥࡓࡧࡶࡹࡱࡺࡳࠣ᝝"): self.bstack11lll111l1l_opy_
          },
          bstack1l11l11_opy_ (u"ࠦࡳࡵ࡮ࡃࡕࡷࡥࡨࡱࡉ࡯ࡨࡵࡥࡆ࠷࠱ࡺࡅ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠣ᝞"): self.bstack11lll111l11_opy_
        }, file)
    except Exception as e:
      logger.error(bstack1l11l11_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡷࡹࡵࡲࡪࡰࡪࠤࡨࡵ࡭࡮ࡣࡱࡨࡸࡀࠠࡼࡿࠥ᝟").format(e))
      pass
  def bstack11ll111111_opy_(self, bstack1ll1l1111ll_opy_):
    try:
      return any(command.get(bstack1l11l11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᝠ")) == bstack1ll1l1111ll_opy_ for command in self.commands_to_wrap)
    except:
      return False
bstack11l1ll111l_opy_ = bstack11ll11ll111_opy_()