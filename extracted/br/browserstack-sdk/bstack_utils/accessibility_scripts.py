# coding: UTF-8
import sys
bstack11lll11_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack11l1l11_opy_ = 7
def bstack1ll11_opy_ (bstack111lll1_opy_):
    global bstack1ll111l_opy_
    bstack1llll11_opy_ = ord (bstack111lll1_opy_ [-1])
    bstack1_opy_ = bstack111lll1_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1_opy_)
    bstack1l11lll_opy_ = bstack1_opy_ [:bstack111l1ll_opy_] + bstack1_opy_ [bstack111l1ll_opy_:]
    if bstack11lll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    return eval (bstack11l1111_opy_)
import os
import json
from bstack_utils.logger_utils import get_logger
logger = get_logger(__name__)
class bstack111l1lll11l_opy_(object):
  bstack1lll111l11_opy_ = os.path.join(os.path.expanduser(bstack1ll11_opy_ (u"ࠪࢂࠬᮓ")), bstack1ll11_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫᮔ"))
  bstack111l1lll111_opy_ = os.path.join(bstack1lll111l11_opy_, bstack1ll11_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡹ࠮࡫ࡵࡲࡲࠬᮕ"))
  commands_to_wrap = None
  scripts_to_run = None
  perform_scan = None
  get_results = None
  get_results_summary = None
  save_test_results = None
  bstack111lll11111_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack1ll11_opy_ (u"࠭ࡩ࡯ࡵࡷࡥࡳࡩࡥࠨᮖ")):
      cls.instance = super(bstack111l1lll11l_opy_, cls).__new__(cls)
      cls.instance.bstack111l1llll1l_opy_()
    return cls.instance
  def bstack111l1llll1l_opy_(self):
    try:
      with open(self.bstack111l1lll111_opy_, bstack1ll11_opy_ (u"ࠧࡳࠩᮗ")) as bstack1l1ll11l1_opy_:
        bstack111l1lll1l1_opy_ = bstack1l1ll11l1_opy_.read()
        data = json.loads(bstack111l1lll1l1_opy_)
        if bstack1ll11_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡵࠪᮘ") in data:
          self.bstack111lll1l111_opy_(data[bstack1ll11_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶࠫᮙ")])
        if bstack1ll11_opy_ (u"ࠪࡷࡨࡸࡩࡱࡶࡶࡘࡴࡘࡵ࡯ࠩᮚ") in data:
          self.bstack111l1llll11_opy_(data[bstack1ll11_opy_ (u"ࠫࡸࡩࡲࡪࡲࡷࡷ࡙ࡵࡒࡶࡰࠪᮛ")])
        if bstack1ll11_opy_ (u"ࠬࡹࡣࡳ࡫ࡳࡸࡸ࠭ᮜ") in data:
          self.bstack11111l111_opy_(data[bstack1ll11_opy_ (u"࠭ࡳࡤࡴ࡬ࡴࡹࡹࠧᮝ")])
        if bstack1ll11_opy_ (u"ࠧ࡯ࡱࡱࡆࡘࡺࡡࡤ࡭ࡌࡲ࡫ࡸࡡࡂ࠳࠴ࡽࡈ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᮞ") in data:
          self.bstack111l1lll1ll_opy_(data[bstack1ll11_opy_ (u"ࠨࡰࡲࡲࡇ࡙ࡴࡢࡥ࡮ࡍࡳ࡬ࡲࡢࡃ࠴࠵ࡾࡉࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᮟ")])
    except:
      pass
  def bstack111l1lll1ll_opy_(self, bstack111lll11111_opy_):
    if bstack111lll11111_opy_ != None:
      self.bstack111lll11111_opy_ = bstack111lll11111_opy_
  def bstack11111l111_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts.get(bstack1ll11_opy_ (u"ࠩࡶࡧࡦࡴࠧᮠ"),bstack1ll11_opy_ (u"ࠪࠫᮡ"))
      self.get_results = scripts.get(bstack1ll11_opy_ (u"ࠫ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࠨᮢ"),bstack1ll11_opy_ (u"ࠬ࠭ᮣ"))
      self.get_results_summary = scripts.get(bstack1ll11_opy_ (u"࠭ࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࡖࡹࡲࡳࡡࡳࡻࠪᮤ"),bstack1ll11_opy_ (u"ࠧࠨᮥ"))
      self.save_test_results = scripts.get(bstack1ll11_opy_ (u"ࠨࡵࡤࡺࡪࡘࡥࡴࡷ࡯ࡸࡸ࠭ᮦ"),bstack1ll11_opy_ (u"ࠩࠪᮧ"))
  def bstack111lll1l111_opy_(self, commands_to_wrap):
    if commands_to_wrap != None and len(commands_to_wrap) != 0:
      self.commands_to_wrap = commands_to_wrap
  def bstack111l1llll11_opy_(self, scripts_to_run):
    if scripts_to_run != None:
      self.scripts_to_run = scripts_to_run
  def store(self):
    try:
      with open(self.bstack111l1lll111_opy_, bstack1ll11_opy_ (u"ࠪࡻࠬᮨ")) as file:
        json.dump({
          bstack1ll11_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡸࠨᮩ"): self.commands_to_wrap,
          bstack1ll11_opy_ (u"ࠧࡹࡣࡳ࡫ࡳࡸࡸ࡚࡯ࡓࡷࡱ᮪ࠦ"): self.scripts_to_run,
          bstack1ll11_opy_ (u"ࠨࡳࡤࡴ࡬ࡴࡹࡹ᮫ࠢ"): {
            bstack1ll11_opy_ (u"ࠢࡴࡥࡤࡲࠧᮬ"): self.perform_scan,
            bstack1ll11_opy_ (u"ࠣࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࠧᮭ"): self.get_results,
            bstack1ll11_opy_ (u"ࠤࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸ࡙ࡵ࡮࡯ࡤࡶࡾࠨᮮ"): self.get_results_summary,
            bstack1ll11_opy_ (u"ࠥࡷࡦࡼࡥࡓࡧࡶࡹࡱࡺࡳࠣᮯ"): self.save_test_results
          },
          bstack1ll11_opy_ (u"ࠦࡳࡵ࡮ࡃࡕࡷࡥࡨࡱࡉ࡯ࡨࡵࡥࡆ࠷࠱ࡺࡅ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠣ᮰"): self.bstack111lll11111_opy_
        }, file)
    except Exception as e:
      logger.error(bstack1ll11_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡷࡹࡵࡲࡪࡰࡪࠤࡨࡵ࡭࡮ࡣࡱࡨࡸࡀࠠࡼࡿࠥ᮱").format(e))
      pass
  def bstack1lll11ll1_opy_(self, command_name):
    try:
      return any(command.get(bstack1ll11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ᮲")) == command_name for command in self.commands_to_wrap)
    except:
      return False
accessibility_scripts = bstack111l1lll11l_opy_()