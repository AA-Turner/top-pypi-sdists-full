# coding: UTF-8
import sys
bstack1l11ll1_opy_ = sys.version_info [0] == 2
bstack1lll1l1_opy_ = 2048
bstack11lllll_opy_ = 7
def bstack1l1111l_opy_ (bstack1llllll1_opy_):
    global bstack1ll111_opy_
    bstack11l1l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack11l11l_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1ll11_opy_ = bstack11l1l_opy_ % len (bstack11l11l_opy_)
    bstack11ll1_opy_ = bstack11l11l_opy_ [:bstack1ll11_opy_] + bstack11l11l_opy_ [bstack1ll11_opy_:]
    if bstack1l11ll1_opy_:
        bstack11l1l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack11l1l11_opy_ = str () .join ([chr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack11l1l11_opy_)
import os
import json
from bstack_utils.logger_utils import get_logger
logger = get_logger(__name__)
class bstack1111l11ll11_opy_(object):
  bstack1111l11l1l_opy_ = os.path.join(os.path.expanduser(bstack1l1111l_opy_ (u"ࠧࡿࠩᶁ")), bstack1l1111l_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨᶂ"))
  bstack1111l11l1ll_opy_ = os.path.join(bstack1111l11l1l_opy_, bstack1l1111l_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶ࠲࡯ࡹ࡯࡯ࠩᶃ"))
  commands_to_wrap = None
  scripts_to_run = None
  perform_scan = None
  get_results = None
  get_results_summary = None
  save_test_results = None
  bstack1111l1lllll_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack1l1111l_opy_ (u"ࠪ࡭ࡳࡹࡴࡢࡰࡦࡩࠬᶄ")):
      cls.instance = super(bstack1111l11ll11_opy_, cls).__new__(cls)
      cls.instance.bstack1111l11l111_opy_()
    return cls.instance
  def bstack1111l11l111_opy_(self):
    try:
      with open(self.bstack1111l11l1ll_opy_, bstack1l1111l_opy_ (u"ࠫࡷ࠭ᶅ")) as bstack11111ll11_opy_:
        bstack1111l11l11l_opy_ = bstack11111ll11_opy_.read()
        data = json.loads(bstack1111l11l11l_opy_)
        if bstack1l1111l_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡹࠧᶆ") in data:
          self.bstack1l11ll1lll1_opy_(data[bstack1l1111l_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࡳࠨᶇ")])
        if bstack1l1111l_opy_ (u"ࠧࡴࡥࡵ࡭ࡵࡺࡳࡕࡱࡕࡹࡳ࠭ᶈ") in data:
          self.bstack1111l11l1l1_opy_(data[bstack1l1111l_opy_ (u"ࠨࡵࡦࡶ࡮ࡶࡴࡴࡖࡲࡖࡺࡴࠧᶉ")])
        if bstack1l1111l_opy_ (u"ࠩࡶࡧࡷ࡯ࡰࡵࡵࠪᶊ") in data:
          self.bstack1l111l1l11_opy_(data[bstack1l1111l_opy_ (u"ࠪࡷࡨࡸࡩࡱࡶࡶࠫᶋ")])
        if bstack1l1111l_opy_ (u"ࠫࡳࡵ࡮ࡃࡕࡷࡥࡨࡱࡉ࡯ࡨࡵࡥࡆ࠷࠱ࡺࡅ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᶌ") in data:
          self.bstack1111l111lll_opy_(data[bstack1l1111l_opy_ (u"ࠬࡴ࡯࡯ࡄࡖࡸࡦࡩ࡫ࡊࡰࡩࡶࡦࡇ࠱࠲ࡻࡆ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᶍ")])
    except:
      pass
  def bstack1111l111lll_opy_(self, bstack1111l1lllll_opy_):
    if bstack1111l1lllll_opy_ != None:
      self.bstack1111l1lllll_opy_ = bstack1111l1lllll_opy_
  def bstack1l111l1l11_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts.get(bstack1l1111l_opy_ (u"࠭ࡳࡤࡣࡱࠫᶎ"),bstack1l1111l_opy_ (u"ࠧࠨᶏ"))
      self.get_results = scripts.get(bstack1l1111l_opy_ (u"ࠨࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࠬᶐ"),bstack1l1111l_opy_ (u"ࠩࠪᶑ"))
      self.get_results_summary = scripts.get(bstack1l1111l_opy_ (u"ࠪ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࡓࡶ࡯ࡰࡥࡷࡿࠧᶒ"),bstack1l1111l_opy_ (u"ࠫࠬᶓ"))
      self.save_test_results = scripts.get(bstack1l1111l_opy_ (u"ࠬࡹࡡࡷࡧࡕࡩࡸࡻ࡬ࡵࡵࠪᶔ"),bstack1l1111l_opy_ (u"࠭ࠧᶕ"))
  def bstack1l11ll1lll1_opy_(self, commands_to_wrap):
    if commands_to_wrap != None and len(commands_to_wrap) != 0:
      self.commands_to_wrap = commands_to_wrap
  def bstack1111l11l1l1_opy_(self, scripts_to_run):
    if scripts_to_run != None:
      self.scripts_to_run = scripts_to_run
  def store(self):
    try:
      with open(self.bstack1111l11l1ll_opy_, bstack1l1111l_opy_ (u"ࠧࡸࠩᶖ")) as file:
        json.dump({
          bstack1l1111l_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡵࠥᶗ"): self.commands_to_wrap,
          bstack1l1111l_opy_ (u"ࠤࡶࡧࡷ࡯ࡰࡵࡵࡗࡳࡗࡻ࡮ࠣᶘ"): self.scripts_to_run,
          bstack1l1111l_opy_ (u"ࠥࡷࡨࡸࡩࡱࡶࡶࠦᶙ"): {
            bstack1l1111l_opy_ (u"ࠦࡸࡩࡡ࡯ࠤᶚ"): self.perform_scan,
            bstack1l1111l_opy_ (u"ࠧ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࠤᶛ"): self.get_results,
            bstack1l1111l_opy_ (u"ࠨࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࡖࡹࡲࡳࡡࡳࡻࠥᶜ"): self.get_results_summary,
            bstack1l1111l_opy_ (u"ࠢࡴࡣࡹࡩࡗ࡫ࡳࡶ࡮ࡷࡷࠧᶝ"): self.save_test_results
          },
          bstack1l1111l_opy_ (u"ࠣࡰࡲࡲࡇ࡙ࡴࡢࡥ࡮ࡍࡳ࡬ࡲࡢࡃ࠴࠵ࡾࡉࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠧᶞ"): self.bstack1111l1lllll_opy_
        }, file)
    except Exception as e:
      logger.error(bstack1l1111l_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡴࡶࡲࡶ࡮ࡴࡧࠡࡥࡲࡱࡲࡧ࡮ࡥࡵ࠽ࠤࢀࢃࠢᶟ").format(e))
      pass
  def bstack1111lllll_opy_(self, command_name):
    try:
      return any(command.get(bstack1l1111l_opy_ (u"ࠪࡲࡦࡳࡥࠨᶠ")) == command_name for command in self.commands_to_wrap)
    except:
      return False
accessibility_scripts = bstack1111l11ll11_opy_()