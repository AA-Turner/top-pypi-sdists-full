# coding: UTF-8
import sys
bstack111l1l_opy_ = sys.version_info [0] == 2
bstack1111l11_opy_ = 2048
bstackl_opy_ = 7
def bstack11lll1_opy_ (bstack1l1l111_opy_):
    global bstack11l1l1_opy_
    bstack1111l_opy_ = ord (bstack1l1l111_opy_ [-1])
    bstack1l111_opy_ = bstack1l1l111_opy_ [:-1]
    bstack11111ll_opy_ = bstack1111l_opy_ % len (bstack1l111_opy_)
    bstack111l_opy_ = bstack1l111_opy_ [:bstack11111ll_opy_] + bstack1l111_opy_ [bstack11111ll_opy_:]
    if bstack111l1l_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    return eval (bstack1llll11_opy_)
import os
import json
from bstack_utils.logger_utils import get_logger
logger = get_logger(__name__)
class bstack111ll111ll1_opy_(object):
  bstack1111llll1_opy_ = os.path.join(os.path.expanduser(bstack11lll1_opy_ (u"ࠪࢂࠬ᭢")), bstack11lll1_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ᭣"))
  bstack111ll111lll_opy_ = os.path.join(bstack1111llll1_opy_, bstack11lll1_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡹ࠮࡫ࡵࡲࡲࠬ᭤"))
  commands_to_wrap = None
  scripts_to_run = None
  perform_scan = None
  get_results = None
  get_results_summary = None
  save_test_results = None
  bstack111ll1l1111_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack11lll1_opy_ (u"࠭ࡩ࡯ࡵࡷࡥࡳࡩࡥࠨ᭥")):
      cls.instance = super(bstack111ll111ll1_opy_, cls).__new__(cls)
      cls.instance.bstack111ll11l111_opy_()
    return cls.instance
  def bstack111ll11l111_opy_(self):
    try:
      with open(self.bstack111ll111lll_opy_, bstack11lll1_opy_ (u"ࠧࡳࠩ᭦")) as bstack11l111ll11_opy_:
        bstack111ll11l11l_opy_ = bstack11l111ll11_opy_.read()
        data = json.loads(bstack111ll11l11l_opy_)
        if bstack11lll1_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡵࠪ᭧") in data:
          self.bstack111ll1lll11_opy_(data[bstack11lll1_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶࠫ᭨")])
        if bstack11lll1_opy_ (u"ࠪࡷࡨࡸࡩࡱࡶࡶࡘࡴࡘࡵ࡯ࠩ᭩") in data:
          self.bstack111ll11l1ll_opy_(data[bstack11lll1_opy_ (u"ࠫࡸࡩࡲࡪࡲࡷࡷ࡙ࡵࡒࡶࡰࠪ᭪")])
        if bstack11lll1_opy_ (u"ࠬࡹࡣࡳ࡫ࡳࡸࡸ࠭᭫") in data:
          self.bstack11lll1l11_opy_(data[bstack11lll1_opy_ (u"࠭ࡳࡤࡴ࡬ࡴࡹࡹ᭬ࠧ")])
        if bstack11lll1_opy_ (u"ࠧ࡯ࡱࡱࡆࡘࡺࡡࡤ࡭ࡌࡲ࡫ࡸࡡࡂ࠳࠴ࡽࡈ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫ᭭") in data:
          self.bstack111ll11l1l1_opy_(data[bstack11lll1_opy_ (u"ࠨࡰࡲࡲࡇ࡙ࡴࡢࡥ࡮ࡍࡳ࡬ࡲࡢࡃ࠴࠵ࡾࡉࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ᭮")])
    except:
      pass
  def bstack111ll11l1l1_opy_(self, bstack111ll1l1111_opy_):
    if bstack111ll1l1111_opy_ != None:
      self.bstack111ll1l1111_opy_ = bstack111ll1l1111_opy_
  def bstack11lll1l11_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts.get(bstack11lll1_opy_ (u"ࠩࡶࡧࡦࡴࠧ᭯"),bstack11lll1_opy_ (u"ࠪࠫ᭰"))
      self.get_results = scripts.get(bstack11lll1_opy_ (u"ࠫ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࠨ᭱"),bstack11lll1_opy_ (u"ࠬ࠭᭲"))
      self.get_results_summary = scripts.get(bstack11lll1_opy_ (u"࠭ࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࡖࡹࡲࡳࡡࡳࡻࠪ᭳"),bstack11lll1_opy_ (u"ࠧࠨ᭴"))
      self.save_test_results = scripts.get(bstack11lll1_opy_ (u"ࠨࡵࡤࡺࡪࡘࡥࡴࡷ࡯ࡸࡸ࠭᭵"),bstack11lll1_opy_ (u"ࠩࠪ᭶"))
  def bstack111ll1lll11_opy_(self, commands_to_wrap):
    if commands_to_wrap != None and len(commands_to_wrap) != 0:
      self.commands_to_wrap = commands_to_wrap
  def bstack111ll11l1ll_opy_(self, scripts_to_run):
    if scripts_to_run != None:
      self.scripts_to_run = scripts_to_run
  def store(self):
    try:
      with open(self.bstack111ll111lll_opy_, bstack11lll1_opy_ (u"ࠪࡻࠬ᭷")) as file:
        json.dump({
          bstack11lll1_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡸࠨ᭸"): self.commands_to_wrap,
          bstack11lll1_opy_ (u"ࠧࡹࡣࡳ࡫ࡳࡸࡸ࡚࡯ࡓࡷࡱࠦ᭹"): self.scripts_to_run,
          bstack11lll1_opy_ (u"ࠨࡳࡤࡴ࡬ࡴࡹࡹࠢ᭺"): {
            bstack11lll1_opy_ (u"ࠢࡴࡥࡤࡲࠧ᭻"): self.perform_scan,
            bstack11lll1_opy_ (u"ࠣࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࠧ᭼"): self.get_results,
            bstack11lll1_opy_ (u"ࠤࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸ࡙ࡵ࡮࡯ࡤࡶࡾࠨ᭽"): self.get_results_summary,
            bstack11lll1_opy_ (u"ࠥࡷࡦࡼࡥࡓࡧࡶࡹࡱࡺࡳࠣ᭾"): self.save_test_results
          },
          bstack11lll1_opy_ (u"ࠦࡳࡵ࡮ࡃࡕࡷࡥࡨࡱࡉ࡯ࡨࡵࡥࡆ࠷࠱ࡺࡅ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠣ᭿"): self.bstack111ll1l1111_opy_
        }, file)
    except Exception as e:
      logger.error(bstack11lll1_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡷࡹࡵࡲࡪࡰࡪࠤࡨࡵ࡭࡮ࡣࡱࡨࡸࡀࠠࡼࡿࠥᮀ").format(e))
      pass
  def bstack1l11ll1111_opy_(self, command_name):
    try:
      return any(command.get(bstack11lll1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᮁ")) == command_name for command in self.commands_to_wrap)
    except:
      return False
accessibility_scripts = bstack111ll111ll1_opy_()