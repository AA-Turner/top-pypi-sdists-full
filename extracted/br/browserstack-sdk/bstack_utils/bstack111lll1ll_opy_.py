# coding: UTF-8
import sys
bstack1llllll1_opy_ = sys.version_info [0] == 2
bstack11l1l1l_opy_ = 2048
bstack1ll111_opy_ = 7
def bstack111l111_opy_ (bstack11ll1_opy_):
    global bstack11111_opy_
    bstack1111l11_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1ll11l1_opy_ = bstack11ll1_opy_ [:-1]
    bstack1111ll_opy_ = bstack1111l11_opy_ % len (bstack1ll11l1_opy_)
    bstack1lll1_opy_ = bstack1ll11l1_opy_ [:bstack1111ll_opy_] + bstack1ll11l1_opy_ [bstack1111ll_opy_:]
    if bstack1llllll1_opy_:
        bstack1l1ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    else:
        bstack1l1ll11_opy_ = str () .join ([chr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    return eval (bstack1l1ll11_opy_)
import os
import json
from bstack_utils.bstack1l1111ll_opy_ import get_logger
logger = get_logger(__name__)
class bstack11ll11l1lll_opy_(object):
  bstack11l1l1l1l1_opy_ = os.path.join(os.path.expanduser(bstack111l111_opy_ (u"ࠪࢂࠬᝈ")), bstack111l111_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫᝉ"))
  bstack11ll11ll11l_opy_ = os.path.join(bstack11l1l1l1l1_opy_, bstack111l111_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡹ࠮࡫ࡵࡲࡲࠬᝊ"))
  commands_to_wrap = None
  perform_scan = None
  bstack11l1ll1l1_opy_ = None
  bstack1lllll1ll_opy_ = None
  bstack11ll1l1111l_opy_ = None
  bstack11ll1ll1ll1_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack111l111_opy_ (u"࠭ࡩ࡯ࡵࡷࡥࡳࡩࡥࠨᝋ")):
      cls.instance = super(bstack11ll11l1lll_opy_, cls).__new__(cls)
      cls.instance.bstack11ll11ll111_opy_()
    return cls.instance
  def bstack11ll11ll111_opy_(self):
    try:
      with open(self.bstack11ll11ll11l_opy_, bstack111l111_opy_ (u"ࠧࡳࠩᝌ")) as bstack111llll11_opy_:
        bstack11ll11l1l1l_opy_ = bstack111llll11_opy_.read()
        data = json.loads(bstack11ll11l1l1l_opy_)
        if bstack111l111_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡵࠪᝍ") in data:
          self.bstack11ll11lll11_opy_(data[bstack111l111_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶࠫᝎ")])
        if bstack111l111_opy_ (u"ࠪࡷࡨࡸࡩࡱࡶࡶࠫᝏ") in data:
          self.bstack11lll111l_opy_(data[bstack111l111_opy_ (u"ࠫࡸࡩࡲࡪࡲࡷࡷࠬᝐ")])
        if bstack111l111_opy_ (u"ࠬࡴ࡯࡯ࡄࡖࡸࡦࡩ࡫ࡊࡰࡩࡶࡦࡇ࠱࠲ࡻࡆ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᝑ") in data:
          self.bstack11ll11l1ll1_opy_(data[bstack111l111_opy_ (u"࠭࡮ࡰࡰࡅࡗࡹࡧࡣ࡬ࡋࡱࡪࡷࡧࡁ࠲࠳ࡼࡇ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᝒ")])
    except:
      pass
  def bstack11ll11l1ll1_opy_(self, bstack11ll1ll1ll1_opy_):
    if bstack11ll1ll1ll1_opy_ != None:
      self.bstack11ll1ll1ll1_opy_ = bstack11ll1ll1ll1_opy_
  def bstack11lll111l_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts.get(bstack111l111_opy_ (u"ࠧࡴࡥࡤࡲࠬᝓ"),bstack111l111_opy_ (u"ࠨࠩ᝔"))
      self.bstack11l1ll1l1_opy_ = scripts.get(bstack111l111_opy_ (u"ࠩࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸ࠭᝕"),bstack111l111_opy_ (u"ࠪࠫ᝖"))
      self.bstack1lllll1ll_opy_ = scripts.get(bstack111l111_opy_ (u"ࠫ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࡔࡷࡰࡱࡦࡸࡹࠨ᝗"),bstack111l111_opy_ (u"ࠬ࠭᝘"))
      self.bstack11ll1l1111l_opy_ = scripts.get(bstack111l111_opy_ (u"࠭ࡳࡢࡸࡨࡖࡪࡹࡵ࡭ࡶࡶࠫ᝙"),bstack111l111_opy_ (u"ࠧࠨ᝚"))
  def bstack11ll11lll11_opy_(self, commands_to_wrap):
    if commands_to_wrap != None and len(commands_to_wrap) != 0:
      self.commands_to_wrap = commands_to_wrap
  def store(self):
    try:
      with open(self.bstack11ll11ll11l_opy_, bstack111l111_opy_ (u"ࠨࡹࠪ᝛")) as file:
        json.dump({
          bstack111l111_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡶࠦ᝜"): self.commands_to_wrap,
          bstack111l111_opy_ (u"ࠥࡷࡨࡸࡩࡱࡶࡶࠦ᝝"): {
            bstack111l111_opy_ (u"ࠦࡸࡩࡡ࡯ࠤ᝞"): self.perform_scan,
            bstack111l111_opy_ (u"ࠧ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࠤ᝟"): self.bstack11l1ll1l1_opy_,
            bstack111l111_opy_ (u"ࠨࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࡖࡹࡲࡳࡡࡳࡻࠥᝠ"): self.bstack1lllll1ll_opy_,
            bstack111l111_opy_ (u"ࠢࡴࡣࡹࡩࡗ࡫ࡳࡶ࡮ࡷࡷࠧᝡ"): self.bstack11ll1l1111l_opy_
          },
          bstack111l111_opy_ (u"ࠣࡰࡲࡲࡇ࡙ࡴࡢࡥ࡮ࡍࡳ࡬ࡲࡢࡃ࠴࠵ࡾࡉࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠧᝢ"): self.bstack11ll1ll1ll1_opy_
        }, file)
    except Exception as e:
      logger.error(bstack111l111_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡴࡶࡲࡶ࡮ࡴࡧࠡࡥࡲࡱࡲࡧ࡮ࡥࡵ࠽ࠤࢀࢃࠢᝣ").format(e))
      pass
  def bstack11l11l1l_opy_(self, bstack1ll1l11l111_opy_):
    try:
      return any(command.get(bstack111l111_opy_ (u"ࠪࡲࡦࡳࡥࠨᝤ")) == bstack1ll1l11l111_opy_ for command in self.commands_to_wrap)
    except:
      return False
bstack111lll1ll_opy_ = bstack11ll11l1lll_opy_()