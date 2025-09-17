# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1ll11l1_opy_ = 7
def bstack1l11ll1_opy_ (bstack1l1llll_opy_):
    global bstack1111ll1_opy_
    bstack1llll11_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack111ll_opy_ = bstack1l1llll_opy_ [:-1]
    bstack11l_opy_ = bstack1llll11_opy_ % len (bstack111ll_opy_)
    bstack1111111_opy_ = bstack111ll_opy_ [:bstack11l_opy_] + bstack111ll_opy_ [bstack11l_opy_:]
    if bstack1lll_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    return eval (bstack1l1l1_opy_)
import os
import json
from bstack_utils.bstack1lll1l1l1l_opy_ import get_logger
logger = get_logger(__name__)
class bstack11ll11l1lll_opy_(object):
  bstack1ll11l111_opy_ = os.path.join(os.path.expanduser(bstack1l11ll1_opy_ (u"ࠩࢁࠫᝎ")), bstack1l11ll1_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪᝏ"))
  bstack11ll11l1ll1_opy_ = os.path.join(bstack1ll11l111_opy_, bstack1l11ll1_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࡸ࠴ࡪࡴࡱࡱࠫᝐ"))
  commands_to_wrap = None
  perform_scan = None
  bstack1l1l111l1l_opy_ = None
  bstack11l11111l1_opy_ = None
  bstack11ll1ll1l11_opy_ = None
  bstack11ll1ll11ll_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack1l11ll1_opy_ (u"ࠬ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠧᝑ")):
      cls.instance = super(bstack11ll11l1lll_opy_, cls).__new__(cls)
      cls.instance.bstack11ll11l11ll_opy_()
    return cls.instance
  def bstack11ll11l11ll_opy_(self):
    try:
      with open(self.bstack11ll11l1ll1_opy_, bstack1l11ll1_opy_ (u"࠭ࡲࠨᝒ")) as bstack11111ll1l_opy_:
        bstack11ll11l1l1l_opy_ = bstack11111ll1l_opy_.read()
        data = json.loads(bstack11ll11l1l1l_opy_)
        if bstack1l11ll1_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡴࠩᝓ") in data:
          self.bstack11ll1l1llll_opy_(data[bstack1l11ll1_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡵࠪ᝔")])
        if bstack1l11ll1_opy_ (u"ࠩࡶࡧࡷ࡯ࡰࡵࡵࠪ᝕") in data:
          self.bstack1lll1l1l11_opy_(data[bstack1l11ll1_opy_ (u"ࠪࡷࡨࡸࡩࡱࡶࡶࠫ᝖")])
        if bstack1l11ll1_opy_ (u"ࠫࡳࡵ࡮ࡃࡕࡷࡥࡨࡱࡉ࡯ࡨࡵࡥࡆ࠷࠱ࡺࡅ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ᝗") in data:
          self.bstack11ll11l1l11_opy_(data[bstack1l11ll1_opy_ (u"ࠬࡴ࡯࡯ࡄࡖࡸࡦࡩ࡫ࡊࡰࡩࡶࡦࡇ࠱࠲ࡻࡆ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ᝘")])
    except:
      pass
  def bstack11ll11l1l11_opy_(self, bstack11ll1ll11ll_opy_):
    if bstack11ll1ll11ll_opy_ != None:
      self.bstack11ll1ll11ll_opy_ = bstack11ll1ll11ll_opy_
  def bstack1lll1l1l11_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts.get(bstack1l11ll1_opy_ (u"࠭ࡳࡤࡣࡱࠫ᝙"),bstack1l11ll1_opy_ (u"ࠧࠨ᝚"))
      self.bstack1l1l111l1l_opy_ = scripts.get(bstack1l11ll1_opy_ (u"ࠨࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࠬ᝛"),bstack1l11ll1_opy_ (u"ࠩࠪ᝜"))
      self.bstack11l11111l1_opy_ = scripts.get(bstack1l11ll1_opy_ (u"ࠪ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࡓࡶ࡯ࡰࡥࡷࡿࠧ᝝"),bstack1l11ll1_opy_ (u"ࠫࠬ᝞"))
      self.bstack11ll1ll1l11_opy_ = scripts.get(bstack1l11ll1_opy_ (u"ࠬࡹࡡࡷࡧࡕࡩࡸࡻ࡬ࡵࡵࠪ᝟"),bstack1l11ll1_opy_ (u"࠭ࠧᝠ"))
  def bstack11ll1l1llll_opy_(self, commands_to_wrap):
    if commands_to_wrap != None and len(commands_to_wrap) != 0:
      self.commands_to_wrap = commands_to_wrap
  def store(self):
    try:
      with open(self.bstack11ll11l1ll1_opy_, bstack1l11ll1_opy_ (u"ࠧࡸࠩᝡ")) as file:
        json.dump({
          bstack1l11ll1_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡵࠥᝢ"): self.commands_to_wrap,
          bstack1l11ll1_opy_ (u"ࠤࡶࡧࡷ࡯ࡰࡵࡵࠥᝣ"): {
            bstack1l11ll1_opy_ (u"ࠥࡷࡨࡧ࡮ࠣᝤ"): self.perform_scan,
            bstack1l11ll1_opy_ (u"ࠦ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࠣᝥ"): self.bstack1l1l111l1l_opy_,
            bstack1l11ll1_opy_ (u"ࠧ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࡕࡸࡱࡲࡧࡲࡺࠤᝦ"): self.bstack11l11111l1_opy_,
            bstack1l11ll1_opy_ (u"ࠨࡳࡢࡸࡨࡖࡪࡹࡵ࡭ࡶࡶࠦᝧ"): self.bstack11ll1ll1l11_opy_
          },
          bstack1l11ll1_opy_ (u"ࠢ࡯ࡱࡱࡆࡘࡺࡡࡤ࡭ࡌࡲ࡫ࡸࡡࡂ࠳࠴ࡽࡈ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠦᝨ"): self.bstack11ll1ll11ll_opy_
        }, file)
    except Exception as e:
      logger.error(bstack1l11ll1_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡳࡵࡱࡵ࡭ࡳ࡭ࠠࡤࡱࡰࡱࡦࡴࡤࡴ࠼ࠣࡿࢂࠨᝩ").format(e))
      pass
  def bstack11llll1l11_opy_(self, command_name):
    try:
      return any(command.get(bstack1l11ll1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᝪ")) == command_name for command in self.commands_to_wrap)
    except:
      return False
bstack1l11l11l_opy_ = bstack11ll11l1lll_opy_()