# coding: UTF-8
import sys
bstack1llll1l_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1l_opy_ = 7
def bstack1ll11ll_opy_ (bstack1ll1lll_opy_):
    global bstack1ll1l1l_opy_
    bstack1ll11l_opy_ = ord (bstack1ll1lll_opy_ [-1])
    bstack1l11_opy_ = bstack1ll1lll_opy_ [:-1]
    bstack1l1l1ll_opy_ = bstack1ll11l_opy_ % len (bstack1l11_opy_)
    bstack111111_opy_ = bstack1l11_opy_ [:bstack1l1l1ll_opy_] + bstack1l11_opy_ [bstack1l1l1ll_opy_:]
    if bstack1llll1l_opy_:
        bstack1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    else:
        bstack1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    return eval (bstack1lll_opy_)
import os
import json
from bstack_utils.bstack1lll1llll_opy_ import get_logger
logger = get_logger(__name__)
class bstack11ll111l1ll_opy_(object):
  bstack1l1111lll1_opy_ = os.path.join(os.path.expanduser(bstack1ll11ll_opy_ (u"ࠨࢀࠪ᝔")), bstack1ll11ll_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ᝕"))
  bstack11ll111ll11_opy_ = os.path.join(bstack1l1111lll1_opy_, bstack1ll11ll_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡷ࠳ࡰࡳࡰࡰࠪ᝖"))
  commands_to_wrap = None
  perform_scan = None
  bstack1l11l111_opy_ = None
  bstack1lll11l1_opy_ = None
  bstack11ll1l1lll1_opy_ = None
  bstack11ll1l11l11_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack1ll11ll_opy_ (u"ࠫ࡮ࡴࡳࡵࡣࡱࡧࡪ࠭᝗")):
      cls.instance = super(bstack11ll111l1ll_opy_, cls).__new__(cls)
      cls.instance.bstack11ll111l1l1_opy_()
    return cls.instance
  def bstack11ll111l1l1_opy_(self):
    try:
      with open(self.bstack11ll111ll11_opy_, bstack1ll11ll_opy_ (u"ࠬࡸࠧ᝘")) as bstack1l11ll11_opy_:
        bstack11ll111l111_opy_ = bstack1l11ll11_opy_.read()
        data = json.loads(bstack11ll111l111_opy_)
        if bstack1ll11ll_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࡳࠨ᝙") in data:
          self.bstack11ll11l1l11_opy_(data[bstack1ll11ll_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡴࠩ᝚")])
        if bstack1ll11ll_opy_ (u"ࠨࡵࡦࡶ࡮ࡶࡴࡴࠩ᝛") in data:
          self.bstack1l111l11_opy_(data[bstack1ll11ll_opy_ (u"ࠩࡶࡧࡷ࡯ࡰࡵࡵࠪ᝜")])
        if bstack1ll11ll_opy_ (u"ࠪࡲࡴࡴࡂࡔࡶࡤࡧࡰࡏ࡮ࡧࡴࡤࡅ࠶࠷ࡹࡄࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ᝝") in data:
          self.bstack11ll111l11l_opy_(data[bstack1ll11ll_opy_ (u"ࠫࡳࡵ࡮ࡃࡕࡷࡥࡨࡱࡉ࡯ࡨࡵࡥࡆ࠷࠱ࡺࡅ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ᝞")])
    except:
      pass
  def bstack11ll111l11l_opy_(self, bstack11ll1l11l11_opy_):
    if bstack11ll1l11l11_opy_ != None:
      self.bstack11ll1l11l11_opy_ = bstack11ll1l11l11_opy_
  def bstack1l111l11_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts.get(bstack1ll11ll_opy_ (u"ࠬࡹࡣࡢࡰࠪ᝟"),bstack1ll11ll_opy_ (u"࠭ࠧᝠ"))
      self.bstack1l11l111_opy_ = scripts.get(bstack1ll11ll_opy_ (u"ࠧࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࠫᝡ"),bstack1ll11ll_opy_ (u"ࠨࠩᝢ"))
      self.bstack1lll11l1_opy_ = scripts.get(bstack1ll11ll_opy_ (u"ࠩࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸ࡙ࡵ࡮࡯ࡤࡶࡾ࠭ᝣ"),bstack1ll11ll_opy_ (u"ࠪࠫᝤ"))
      self.bstack11ll1l1lll1_opy_ = scripts.get(bstack1ll11ll_opy_ (u"ࠫࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠩᝥ"),bstack1ll11ll_opy_ (u"ࠬ࠭ᝦ"))
  def bstack11ll11l1l11_opy_(self, commands_to_wrap):
    if commands_to_wrap != None and len(commands_to_wrap) != 0:
      self.commands_to_wrap = commands_to_wrap
  def store(self):
    try:
      with open(self.bstack11ll111ll11_opy_, bstack1ll11ll_opy_ (u"࠭ࡷࠨᝧ")) as file:
        json.dump({
          bstack1ll11ll_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࡴࠤᝨ"): self.commands_to_wrap,
          bstack1ll11ll_opy_ (u"ࠣࡵࡦࡶ࡮ࡶࡴࡴࠤᝩ"): {
            bstack1ll11ll_opy_ (u"ࠤࡶࡧࡦࡴࠢᝪ"): self.perform_scan,
            bstack1ll11ll_opy_ (u"ࠥ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࠢᝫ"): self.bstack1l11l111_opy_,
            bstack1ll11ll_opy_ (u"ࠦ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࡔࡷࡰࡱࡦࡸࡹࠣᝬ"): self.bstack1lll11l1_opy_,
            bstack1ll11ll_opy_ (u"ࠧࡹࡡࡷࡧࡕࡩࡸࡻ࡬ࡵࡵࠥ᝭"): self.bstack11ll1l1lll1_opy_
          },
          bstack1ll11ll_opy_ (u"ࠨ࡮ࡰࡰࡅࡗࡹࡧࡣ࡬ࡋࡱࡪࡷࡧࡁ࠲࠳ࡼࡇ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠥᝮ"): self.bstack11ll1l11l11_opy_
        }, file)
    except Exception as e:
      logger.error(bstack1ll11ll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡹࡴࡰࡴ࡬ࡲ࡬ࠦࡣࡰ࡯ࡰࡥࡳࡪࡳ࠻ࠢࡾࢁࠧᝯ").format(e))
      pass
  def bstack1ll1l1llll_opy_(self, command_name):
    try:
      return any(command.get(bstack1ll11ll_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᝰ")) == command_name for command in self.commands_to_wrap)
    except:
      return False
bstack1llll111_opy_ = bstack11ll111l1ll_opy_()