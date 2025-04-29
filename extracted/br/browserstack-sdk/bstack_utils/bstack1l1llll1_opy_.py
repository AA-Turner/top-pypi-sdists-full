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
import os
import json
from bstack_utils.bstack1llllll1ll_opy_ import get_logger
logger = get_logger(__name__)
class bstack11lll1ll111_opy_(object):
  bstack111l11l1l_opy_ = os.path.join(os.path.expanduser(bstack1llllll_opy_ (u"ࠫࢃ࠭ᘸ")), bstack1llllll_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬᘹ"))
  bstack11lll1l1lll_opy_ = os.path.join(bstack111l11l1l_opy_, bstack1llllll_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࡳ࠯࡬ࡶࡳࡳ࠭ᘺ"))
  commands_to_wrap = None
  perform_scan = None
  bstack11lll1ll_opy_ = None
  bstack111l111l_opy_ = None
  bstack11llll1l1l1_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack1llllll_opy_ (u"ࠧࡪࡰࡶࡸࡦࡴࡣࡦࠩᘻ")):
      cls.instance = super(bstack11lll1ll111_opy_, cls).__new__(cls)
      cls.instance.bstack11lll1l1l1l_opy_()
    return cls.instance
  def bstack11lll1l1l1l_opy_(self):
    try:
      with open(self.bstack11lll1l1lll_opy_, bstack1llllll_opy_ (u"ࠨࡴࠪᘼ")) as bstack11l11111l_opy_:
        bstack11lll1l1ll1_opy_ = bstack11l11111l_opy_.read()
        data = json.loads(bstack11lll1l1ll1_opy_)
        if bstack1llllll_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶࠫᘽ") in data:
          self.bstack11llll1l1ll_opy_(data[bstack1llllll_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡷࠬᘾ")])
        if bstack1llllll_opy_ (u"ࠫࡸࡩࡲࡪࡲࡷࡷࠬᘿ") in data:
          self.bstack1l11ll1ll_opy_(data[bstack1llllll_opy_ (u"ࠬࡹࡣࡳ࡫ࡳࡸࡸ࠭ᙀ")])
    except:
      pass
  def bstack1l11ll1ll_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts.get(bstack1llllll_opy_ (u"࠭ࡳࡤࡣࡱࠫᙁ"),bstack1llllll_opy_ (u"ࠧࠨᙂ"))
      self.bstack11lll1ll_opy_ = scripts.get(bstack1llllll_opy_ (u"ࠨࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࠬᙃ"),bstack1llllll_opy_ (u"ࠩࠪᙄ"))
      self.bstack111l111l_opy_ = scripts.get(bstack1llllll_opy_ (u"ࠪ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࡓࡶ࡯ࡰࡥࡷࡿࠧᙅ"),bstack1llllll_opy_ (u"ࠫࠬᙆ"))
      self.bstack11llll1l1l1_opy_ = scripts.get(bstack1llllll_opy_ (u"ࠬࡹࡡࡷࡧࡕࡩࡸࡻ࡬ࡵࡵࠪᙇ"),bstack1llllll_opy_ (u"࠭ࠧᙈ"))
  def bstack11llll1l1ll_opy_(self, commands_to_wrap):
    if commands_to_wrap != None and len(commands_to_wrap) != 0:
      self.commands_to_wrap = commands_to_wrap
  def store(self):
    try:
      with open(self.bstack11lll1l1lll_opy_, bstack1llllll_opy_ (u"ࠧࡸࠩᙉ")) as file:
        json.dump({
          bstack1llllll_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡵࠥᙊ"): self.commands_to_wrap,
          bstack1llllll_opy_ (u"ࠤࡶࡧࡷ࡯ࡰࡵࡵࠥᙋ"): {
            bstack1llllll_opy_ (u"ࠥࡷࡨࡧ࡮ࠣᙌ"): self.perform_scan,
            bstack1llllll_opy_ (u"ࠦ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࠣᙍ"): self.bstack11lll1ll_opy_,
            bstack1llllll_opy_ (u"ࠧ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࡕࡸࡱࡲࡧࡲࡺࠤᙎ"): self.bstack111l111l_opy_,
            bstack1llllll_opy_ (u"ࠨࡳࡢࡸࡨࡖࡪࡹࡵ࡭ࡶࡶࠦᙏ"): self.bstack11llll1l1l1_opy_
          }
        }, file)
    except Exception as e:
      logger.error(bstack1llllll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡹࡴࡰࡴ࡬ࡲ࡬ࠦࡣࡰ࡯ࡰࡥࡳࡪࡳ࠻ࠢࡾࢁࠧᙐ").format(e))
      pass
  def bstack11lll111l_opy_(self, bstack1ll1l1lll1l_opy_):
    try:
      return any(command.get(bstack1llllll_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᙑ")) == bstack1ll1l1lll1l_opy_ for command in self.commands_to_wrap)
    except:
      return False
bstack1l1llll1_opy_ = bstack11lll1ll111_opy_()