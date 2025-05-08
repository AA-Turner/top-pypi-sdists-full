# coding: UTF-8
import sys
bstack111l1ll_opy_ = sys.version_info [0] == 2
bstack1lll11l_opy_ = 2048
bstack11111_opy_ = 7
def bstack1l1lll_opy_ (bstack11l_opy_):
    global bstack1l11l11_opy_
    bstack1_opy_ = ord (bstack11l_opy_ [-1])
    bstack1ll111l_opy_ = bstack11l_opy_ [:-1]
    bstack11l1111_opy_ = bstack1_opy_ % len (bstack1ll111l_opy_)
    bstack11l1l_opy_ = bstack1ll111l_opy_ [:bstack11l1111_opy_] + bstack1ll111l_opy_ [bstack11l1111_opy_:]
    if bstack111l1ll_opy_:
        bstack11llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11l_opy_ - (bstack1lllll_opy_ + bstack1_opy_) % bstack11111_opy_) for bstack1lllll_opy_, char in enumerate (bstack11l1l_opy_)])
    else:
        bstack11llll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11l_opy_ - (bstack1lllll_opy_ + bstack1_opy_) % bstack11111_opy_) for bstack1lllll_opy_, char in enumerate (bstack11l1l_opy_)])
    return eval (bstack11llll1_opy_)
import os
import re
import sys
import json
import time
import shutil
import tempfile
import requests
import subprocess
from threading import Thread
from os.path import expanduser
from bstack_utils.constants import *
from requests.auth import HTTPBasicAuth
from bstack_utils.helper import bstack1ll111ll1_opy_, bstack11ll1l111l_opy_
from bstack_utils.measure import measure
class bstack11ll1lllll_opy_:
  working_dir = os.getcwd()
  bstack1llll11ll_opy_ = False
  config = {}
  bstack11ll11ll1ll_opy_ = bstack1l1lll_opy_ (u"ࠨࠩᲆ")
  binary_path = bstack1l1lll_opy_ (u"ࠩࠪᲇ")
  bstack111lll111ll_opy_ = bstack1l1lll_opy_ (u"ࠪࠫᲈ")
  bstack11l11lll1l_opy_ = False
  bstack111ll11llll_opy_ = None
  bstack111ll1lll1l_opy_ = {}
  bstack11l11111l11_opy_ = 300
  bstack111lll1lll1_opy_ = False
  logger = None
  bstack111llll11l1_opy_ = False
  bstack1llll11111_opy_ = False
  percy_build_id = None
  bstack111llll1111_opy_ = bstack1l1lll_opy_ (u"ࠫࠬᲉ")
  bstack111ll11lll1_opy_ = {
    bstack1l1lll_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬᲊ") : 1,
    bstack1l1lll_opy_ (u"࠭ࡦࡪࡴࡨࡪࡴࡾࠧ᲋") : 2,
    bstack1l1lll_opy_ (u"ࠧࡦࡦࡪࡩࠬ᲌") : 3,
    bstack1l1lll_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࠨ᲍") : 4
  }
  def __init__(self) -> None: pass
  def bstack111ll1ll111_opy_(self):
    bstack111llllll11_opy_ = bstack1l1lll_opy_ (u"ࠩࠪ᲎")
    bstack111llllllll_opy_ = sys.platform
    bstack111llll1l1l_opy_ = bstack1l1lll_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩ᲏")
    if re.match(bstack1l1lll_opy_ (u"ࠦࡩࡧࡲࡸ࡫ࡱࢀࡲࡧࡣࠡࡱࡶࠦᲐ"), bstack111llllllll_opy_) != None:
      bstack111llllll11_opy_ = bstack11ll1l1llll_opy_ + bstack1l1lll_opy_ (u"ࠧ࠵ࡰࡦࡴࡦࡽ࠲ࡵࡳࡹ࠰ࡽ࡭ࡵࠨᲑ")
      self.bstack111llll1111_opy_ = bstack1l1lll_opy_ (u"࠭࡭ࡢࡥࠪᲒ")
    elif re.match(bstack1l1lll_opy_ (u"ࠢ࡮ࡵࡺ࡭ࡳࢂ࡭ࡴࡻࡶࢀࡲ࡯࡮ࡨࡹࡿࡧࡾ࡭ࡷࡪࡰࡿࡦࡨࡩࡷࡪࡰࡿࡻ࡮ࡴࡣࡦࡾࡨࡱࡨࢂࡷࡪࡰ࠶࠶ࠧᲓ"), bstack111llllllll_opy_) != None:
      bstack111llllll11_opy_ = bstack11ll1l1llll_opy_ + bstack1l1lll_opy_ (u"ࠣ࠱ࡳࡩࡷࡩࡹ࠮ࡹ࡬ࡲ࠳ࢀࡩࡱࠤᲔ")
      bstack111llll1l1l_opy_ = bstack1l1lll_opy_ (u"ࠤࡳࡩࡷࡩࡹ࠯ࡧࡻࡩࠧᲕ")
      self.bstack111llll1111_opy_ = bstack1l1lll_opy_ (u"ࠪࡻ࡮ࡴࠧᲖ")
    else:
      bstack111llllll11_opy_ = bstack11ll1l1llll_opy_ + bstack1l1lll_opy_ (u"ࠦ࠴ࡶࡥࡳࡥࡼ࠱ࡱ࡯࡮ࡶࡺ࠱ࡾ࡮ࡶࠢᲗ")
      self.bstack111llll1111_opy_ = bstack1l1lll_opy_ (u"ࠬࡲࡩ࡯ࡷࡻࠫᲘ")
    return bstack111llllll11_opy_, bstack111llll1l1l_opy_
  def bstack111ll1ll1l1_opy_(self):
    try:
      bstack111lll1l1ll_opy_ = [os.path.join(expanduser(bstack1l1lll_opy_ (u"ࠨࡾࠣᲙ")), bstack1l1lll_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧᲚ")), self.working_dir, tempfile.gettempdir()]
      for path in bstack111lll1l1ll_opy_:
        if(self.bstack111llllll1l_opy_(path)):
          return path
      raise bstack1l1lll_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡩࡵࡷ࡯࡮ࡲࡥࡩࠦࡰࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠧᲛ")
    except Exception as e:
      self.logger.error(bstack1l1lll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡬ࡩ࡯ࡦࠣࡥࡻࡧࡩ࡭ࡣࡥࡰࡪࠦࡰࡢࡶ࡫ࠤ࡫ࡵࡲࠡࡲࡨࡶࡨࡿࠠࡥࡱࡺࡲࡱࡵࡡࡥ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦ࠭ࠡࡽࢀࠦᲜ").format(e))
  def bstack111llllll1l_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack111llll11ll_opy_(self, bstack111lllllll1_opy_):
    return os.path.join(bstack111lllllll1_opy_, self.bstack11ll11ll1ll_opy_ + bstack1l1lll_opy_ (u"ࠥ࠲ࡪࡺࡡࡨࠤᲝ"))
  def bstack111llll1lll_opy_(self, bstack111lllllll1_opy_, bstack111lllll1l1_opy_):
    if not bstack111lllll1l1_opy_: return
    try:
      bstack111ll1l1ll1_opy_ = self.bstack111llll11ll_opy_(bstack111lllllll1_opy_)
      with open(bstack111ll1l1ll1_opy_, bstack1l1lll_opy_ (u"ࠦࡼࠨᲞ")) as f:
        f.write(bstack111lllll1l1_opy_)
        self.logger.debug(bstack1l1lll_opy_ (u"࡙ࠧࡡࡷࡧࡧࠤࡳ࡫ࡷࠡࡇࡗࡥ࡬ࠦࡦࡰࡴࠣࡴࡪࡸࡣࡺࠤᲟ"))
    except Exception as e:
      self.logger.error(bstack1l1lll_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡥࡻ࡫ࠠࡵࡪࡨࠤࡪࡺࡡࡨ࠮ࠣࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂࠨᲠ").format(e))
  def bstack11l11111111_opy_(self, bstack111lllllll1_opy_):
    try:
      bstack111ll1l1ll1_opy_ = self.bstack111llll11ll_opy_(bstack111lllllll1_opy_)
      if os.path.exists(bstack111ll1l1ll1_opy_):
        with open(bstack111ll1l1ll1_opy_, bstack1l1lll_opy_ (u"ࠢࡳࠤᲡ")) as f:
          bstack111lllll1l1_opy_ = f.read().strip()
          return bstack111lllll1l1_opy_ if bstack111lllll1l1_opy_ else None
    except Exception as e:
      self.logger.error(bstack1l1lll_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡ࡮ࡲࡥࡩ࡯࡮ࡨࠢࡈࡘࡦ࡭ࠬࠡࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠦᲢ").format(e))
  def bstack111lll11ll1_opy_(self, bstack111lllllll1_opy_, bstack111llllll11_opy_):
    bstack111ll1ll11l_opy_ = self.bstack11l11111111_opy_(bstack111lllllll1_opy_)
    if bstack111ll1ll11l_opy_:
      try:
        bstack111lll11lll_opy_ = self.bstack111ll1l1l11_opy_(bstack111ll1ll11l_opy_, bstack111llllll11_opy_)
        if not bstack111lll11lll_opy_:
          self.logger.debug(bstack1l1lll_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠡ࡫ࡶࠤࡺࡶࠠࡵࡱࠣࡨࡦࡺࡥࠡࠪࡈࡘࡦ࡭ࠠࡶࡰࡦ࡬ࡦࡴࡧࡦࡦࠬࠦᲣ"))
          return True
        self.logger.debug(bstack1l1lll_opy_ (u"ࠥࡒࡪࡽࠠࡑࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠦࡶࡦࡴࡶ࡭ࡴࡴࠠࡢࡸࡤ࡭ࡱࡧࡢ࡭ࡧ࠯ࠤࡩࡵࡷ࡯࡮ࡲࡥࡩ࡯࡮ࡨࠢࡸࡴࡩࡧࡴࡦࠤᲤ"))
        return False
      except Exception as e:
        self.logger.warn(bstack1l1lll_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡤࡪࡨࡧࡰࠦࡦࡰࡴࠣࡦ࡮ࡴࡡࡳࡻࠣࡹࡵࡪࡡࡵࡧࡶ࠰ࠥࡻࡳࡪࡰࡪࠤࡪࡾࡩࡴࡶ࡬ࡲ࡬ࠦࡢࡪࡰࡤࡶࡾࡀࠠࡼࡿࠥᲥ").format(e))
    return False
  def bstack111ll1l1l11_opy_(self, bstack111ll1ll11l_opy_, bstack111llllll11_opy_):
    try:
      headers = {
        bstack1l1lll_opy_ (u"ࠧࡏࡦ࠮ࡐࡲࡲࡪ࠳ࡍࡢࡶࡦ࡬ࠧᲦ"): bstack111ll1ll11l_opy_
      }
      response = bstack11ll1l111l_opy_(bstack1l1lll_opy_ (u"࠭ࡇࡆࡖࠪᲧ"), bstack111llllll11_opy_, {}, {bstack1l1lll_opy_ (u"ࠢࡩࡧࡤࡨࡪࡸࡳࠣᲨ"): headers})
      if response.status_code == 304:
        return False
      return True
    except Exception as e:
      raise(bstack1l1lll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡤࡪࡨࡧࡰ࡯࡮ࡨࠢࡩࡳࡷࠦࡐࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠥࡻࡰࡥࡣࡷࡩࡸࡀࠠࡼࡿࠥᲩ").format(e))
  @measure(event_name=EVENTS.bstack11ll11llll1_opy_, stage=STAGE.bstack1111lll1_opy_)
  def bstack111ll1ll1ll_opy_(self, bstack111llllll11_opy_, bstack111llll1l1l_opy_):
    try:
      bstack111lllll111_opy_ = self.bstack111ll1ll1l1_opy_()
      bstack11l1111l1l1_opy_ = os.path.join(bstack111lllll111_opy_, bstack1l1lll_opy_ (u"ࠩࡳࡩࡷࡩࡹ࠯ࡼ࡬ࡴࠬᲪ"))
      bstack11l111111l1_opy_ = os.path.join(bstack111lllll111_opy_, bstack111llll1l1l_opy_)
      if self.bstack111lll11ll1_opy_(bstack111lllll111_opy_, bstack111llllll11_opy_):
        if os.path.exists(bstack11l111111l1_opy_):
          self.logger.info(bstack1l1lll_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠢࡩࡳࡺࡴࡤࠡ࡫ࡱࠤࢀࢃࠬࠡࡵ࡮࡭ࡵࡶࡩ࡯ࡩࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠧᲫ").format(bstack11l111111l1_opy_))
          return bstack11l111111l1_opy_
        if os.path.exists(bstack11l1111l1l1_opy_):
          self.logger.info(bstack1l1lll_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡾ࡮ࡶࠠࡧࡱࡸࡲࡩࠦࡩ࡯ࠢࡾࢁ࠱ࠦࡵ࡯ࡼ࡬ࡴࡵ࡯࡮ࡨࠤᲬ").format(bstack11l1111l1l1_opy_))
          return self.bstack11l11111lll_opy_(bstack11l1111l1l1_opy_, bstack111llll1l1l_opy_)
      self.logger.info(bstack1l1lll_opy_ (u"ࠧࡊ࡯ࡸࡰ࡯ࡳࡦࡪࡩ࡯ࡩࠣࡴࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠢࡩࡶࡴࡳࠠࡼࡿࠥᲭ").format(bstack111llllll11_opy_))
      response = bstack11ll1l111l_opy_(bstack1l1lll_opy_ (u"࠭ࡇࡆࡖࠪᲮ"), bstack111llllll11_opy_, {}, {})
      if response.status_code == 200:
        bstack111ll1llll1_opy_ = response.headers.get(bstack1l1lll_opy_ (u"ࠢࡆࡖࡤ࡫ࠧᲯ"), bstack1l1lll_opy_ (u"ࠣࠤᲰ"))
        if bstack111ll1llll1_opy_:
          self.bstack111llll1lll_opy_(bstack111lllll111_opy_, bstack111ll1llll1_opy_)
        with open(bstack11l1111l1l1_opy_, bstack1l1lll_opy_ (u"ࠩࡺࡦࠬᲱ")) as file:
          file.write(response.content)
        self.logger.info(bstack1l1lll_opy_ (u"ࠥࡈࡴࡽ࡮࡭ࡱࡤࡨࡪࡪࠠࡱࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠦࡡ࡯ࡦࠣࡷࡦࡼࡥࡥࠢࡤࡸࠥࢁࡽࠣᲲ").format(bstack11l1111l1l1_opy_))
        return self.bstack11l11111lll_opy_(bstack11l1111l1l1_opy_, bstack111llll1l1l_opy_)
      else:
        raise(bstack1l1lll_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡥࡱࡺࡲࡱࡵࡡࡥࠢࡷ࡬ࡪࠦࡦࡪ࡮ࡨ࠲࡙ࠥࡴࡢࡶࡸࡷࠥࡩ࡯ࡥࡧ࠽ࠤࢀࢃࠢᲳ").format(response.status_code))
    except Exception as e:
      self.logger.error(bstack1l1lll_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡦࡲࡻࡳࡲ࡯ࡢࡦࠣࡴࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺ࠼ࠣࡿࢂࠨᲴ").format(e))
  def bstack11l11111l1l_opy_(self, bstack111llllll11_opy_, bstack111llll1l1l_opy_):
    try:
      retry = 2
      bstack11l111111l1_opy_ = None
      bstack111lll1l1l1_opy_ = False
      while retry > 0:
        bstack11l111111l1_opy_ = self.bstack111ll1ll1ll_opy_(bstack111llllll11_opy_, bstack111llll1l1l_opy_)
        bstack111lll1l1l1_opy_ = self.bstack111ll1lll11_opy_(bstack111llllll11_opy_, bstack111llll1l1l_opy_, bstack11l111111l1_opy_)
        if bstack111lll1l1l1_opy_:
          break
        retry -= 1
      return bstack11l111111l1_opy_, bstack111lll1l1l1_opy_
    except Exception as e:
      self.logger.error(bstack1l1lll_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡪࡩࡹࠦࡰࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠥࡶࡡࡵࡪࠥᲵ").format(e))
    return bstack11l111111l1_opy_, False
  def bstack111ll1lll11_opy_(self, bstack111llllll11_opy_, bstack111llll1l1l_opy_, bstack11l111111l1_opy_, bstack111llll1l11_opy_ = 0):
    if bstack111llll1l11_opy_ > 1:
      return False
    if bstack11l111111l1_opy_ == None or os.path.exists(bstack11l111111l1_opy_) == False:
      self.logger.warn(bstack1l1lll_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡰࡢࡶ࡫ࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪࠬࠡࡴࡨࡸࡷࡿࡩ࡯ࡩࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠧᲶ"))
      return False
    bstack111lll1l11l_opy_ = bstack1l1lll_opy_ (u"ࠣࡠ࠱࠮ࡅࡶࡥࡳࡥࡼࡠ࠴ࡩ࡬ࡪࠢ࡟ࡨ࠳ࡢࡤࠬ࠰࡟ࡨ࠰ࠨᲷ")
    command = bstack1l1lll_opy_ (u"ࠩࡾࢁࠥ࠳࠭ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᲸ").format(bstack11l111111l1_opy_)
    bstack111ll11ll11_opy_ = subprocess.check_output(command, shell=True, text=True)
    if re.match(bstack111lll1l11l_opy_, bstack111ll11ll11_opy_) != None:
      return True
    else:
      self.logger.error(bstack1l1lll_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡹࡩࡷࡹࡩࡰࡰࠣࡧ࡭࡫ࡣ࡬ࠢࡩࡥ࡮ࡲࡥࡥࠤᲹ"))
      return False
  def bstack11l11111lll_opy_(self, bstack11l1111l1l1_opy_, bstack111llll1l1l_opy_):
    try:
      working_dir = os.path.dirname(bstack11l1111l1l1_opy_)
      shutil.unpack_archive(bstack11l1111l1l1_opy_, working_dir)
      bstack11l111111l1_opy_ = os.path.join(working_dir, bstack111llll1l1l_opy_)
      os.chmod(bstack11l111111l1_opy_, 0o755)
      return bstack11l111111l1_opy_
    except Exception as e:
      self.logger.error(bstack1l1lll_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡶࡰࡽ࡭ࡵࠦࡰࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠧᲺ"))
  def bstack111lllll11l_opy_(self):
    try:
      bstack111lll1l111_opy_ = self.config.get(bstack1l1lll_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫ᲻"))
      bstack111lllll11l_opy_ = bstack111lll1l111_opy_ or (bstack111lll1l111_opy_ is None and self.bstack1llll11ll_opy_)
      if not bstack111lllll11l_opy_ or self.config.get(bstack1l1lll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ᲼"), None) not in bstack11ll1lll1ll_opy_:
        return False
      self.bstack11l11lll1l_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack1l1lll_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡨࡪࡺࡥࡤࡶࠣࡴࡪࡸࡣࡺ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤᲽ").format(e))
  def bstack111llll111l_opy_(self):
    try:
      bstack111llll111l_opy_ = self.percy_capture_mode
      return bstack111llll111l_opy_
    except Exception as e:
      self.logger.error(bstack1l1lll_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡩ࡫ࡴࡦࡥࡷࠤࡵ࡫ࡲࡤࡻࠣࡧࡦࡶࡴࡶࡴࡨࠤࡲࡵࡤࡦ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤᲾ").format(e))
  def init(self, bstack1llll11ll_opy_, config, logger):
    self.bstack1llll11ll_opy_ = bstack1llll11ll_opy_
    self.config = config
    self.logger = logger
    if not self.bstack111lllll11l_opy_():
      return
    self.bstack111ll1lll1l_opy_ = config.get(bstack1l1lll_opy_ (u"ࠩࡳࡩࡷࡩࡹࡐࡲࡷ࡭ࡴࡴࡳࠨᲿ"), {})
    self.percy_capture_mode = config.get(bstack1l1lll_opy_ (u"ࠪࡴࡪࡸࡣࡺࡅࡤࡴࡹࡻࡲࡦࡏࡲࡨࡪ࠭᳀"))
    try:
      bstack111llllll11_opy_, bstack111llll1l1l_opy_ = self.bstack111ll1ll111_opy_()
      self.bstack11ll11ll1ll_opy_ = bstack111llll1l1l_opy_
      bstack11l111111l1_opy_, bstack111lll1l1l1_opy_ = self.bstack11l11111l1l_opy_(bstack111llllll11_opy_, bstack111llll1l1l_opy_)
      if bstack111lll1l1l1_opy_:
        self.binary_path = bstack11l111111l1_opy_
        thread = Thread(target=self.bstack11l1111111l_opy_)
        thread.start()
      else:
        self.bstack111llll11l1_opy_ = True
        self.logger.error(bstack1l1lll_opy_ (u"ࠦࡎࡴࡶࡢ࡮࡬ࡨࠥࡶࡥࡳࡥࡼࠤࡵࡧࡴࡩࠢࡩࡳࡺࡴࡤࠡ࠯ࠣࡿࢂ࠲ࠠࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡹࡧࡲࡵࠢࡓࡩࡷࡩࡹࠣ᳁").format(bstack11l111111l1_opy_))
    except Exception as e:
      self.logger.error(bstack1l1lll_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡱࡧࡵࡧࡾ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡿࢂࠨ᳂").format(e))
  def bstack111lll1111l_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack1l1lll_opy_ (u"࠭࡬ࡰࡩࠪ᳃"), bstack1l1lll_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠴࡬ࡰࡩࠪ᳄"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack1l1lll_opy_ (u"ࠣࡒࡸࡷ࡭࡯࡮ࡨࠢࡳࡩࡷࡩࡹࠡ࡮ࡲ࡫ࡸࠦࡡࡵࠢࡾࢁࠧ᳅").format(logfile))
      self.bstack111lll111ll_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack1l1lll_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡥࡵࠢࡳࡩࡷࡩࡹࠡ࡮ࡲ࡫ࠥࡶࡡࡵࡪ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿࠥ᳆").format(e))
  @measure(event_name=EVENTS.bstack11lll1111l1_opy_, stage=STAGE.bstack1111lll1_opy_)
  def bstack11l1111111l_opy_(self):
    bstack111ll1l11ll_opy_ = self.bstack111lll111l1_opy_()
    if bstack111ll1l11ll_opy_ == None:
      self.bstack111llll11l1_opy_ = True
      self.logger.error(bstack1l1lll_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡷࡳࡰ࡫࡮ࠡࡰࡲࡸࠥ࡬࡯ࡶࡰࡧ࠰ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡱࡧࡵࡧࡾࠨ᳇"))
      return False
    command_args = [bstack1l1lll_opy_ (u"ࠦࡦࡶࡰ࠻ࡧࡻࡩࡨࡀࡳࡵࡣࡵࡸࠧ᳈") if self.bstack1llll11ll_opy_ else bstack1l1lll_opy_ (u"ࠬ࡫ࡸࡦࡥ࠽ࡷࡹࡧࡲࡵࠩ᳉")]
    bstack11l11l11lll_opy_ = self.bstack111lll11111_opy_()
    if bstack11l11l11lll_opy_ != None:
      command_args.append(bstack1l1lll_opy_ (u"ࠨ࠭ࡤࠢࡾࢁࠧ᳊").format(bstack11l11l11lll_opy_))
    env = os.environ.copy()
    env[bstack1l1lll_opy_ (u"ࠢࡑࡇࡕࡇ࡞ࡥࡔࡐࡍࡈࡒࠧ᳋")] = bstack111ll1l11ll_opy_
    env[bstack1l1lll_opy_ (u"ࠣࡖࡋࡣࡇ࡛ࡉࡍࡆࡢ࡙࡚ࡏࡄࠣ᳌")] = os.environ.get(bstack1l1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ᳍"), bstack1l1lll_opy_ (u"ࠪࠫ᳎"))
    bstack11l1111l1ll_opy_ = [self.binary_path]
    self.bstack111lll1111l_opy_()
    self.bstack111ll11llll_opy_ = self.bstack111ll1l1lll_opy_(bstack11l1111l1ll_opy_ + command_args, env)
    self.logger.debug(bstack1l1lll_opy_ (u"ࠦࡘࡺࡡࡳࡶ࡬ࡲ࡬ࠦࡈࡦࡣ࡯ࡸ࡭ࠦࡃࡩࡧࡦ࡯ࠧ᳏"))
    bstack111llll1l11_opy_ = 0
    while self.bstack111ll11llll_opy_.poll() == None:
      bstack11l111111ll_opy_ = self.bstack111ll1l1l1l_opy_()
      if bstack11l111111ll_opy_:
        self.logger.debug(bstack1l1lll_opy_ (u"ࠧࡎࡥࡢ࡮ࡷ࡬ࠥࡉࡨࡦࡥ࡮ࠤࡸࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬ࠣ᳐"))
        self.bstack111lll1lll1_opy_ = True
        return True
      bstack111llll1l11_opy_ += 1
      self.logger.debug(bstack1l1lll_opy_ (u"ࠨࡈࡦࡣ࡯ࡸ࡭ࠦࡃࡩࡧࡦ࡯ࠥࡘࡥࡵࡴࡼࠤ࠲ࠦࡻࡾࠤ᳑").format(bstack111llll1l11_opy_))
      time.sleep(2)
    self.logger.error(bstack1l1lll_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡹࡧࡲࡵࠢࡳࡩࡷࡩࡹ࠭ࠢࡋࡩࡦࡲࡴࡩࠢࡆ࡬ࡪࡩ࡫ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡣࡩࡸࡪࡸࠠࡼࡿࠣࡥࡹࡺࡥ࡮ࡲࡷࡷࠧ᳒").format(bstack111llll1l11_opy_))
    self.bstack111llll11l1_opy_ = True
    return False
  def bstack111ll1l1l1l_opy_(self, bstack111llll1l11_opy_ = 0):
    if bstack111llll1l11_opy_ > 10:
      return False
    try:
      bstack111ll1l11l1_opy_ = os.environ.get(bstack1l1lll_opy_ (u"ࠨࡒࡈࡖࡈ࡟࡟ࡔࡇࡕ࡚ࡊࡘ࡟ࡂࡆࡇࡖࡊ࡙ࡓࠨ᳓"), bstack1l1lll_opy_ (u"ࠩ࡫ࡸࡹࡶ࠺࠰࠱࡯ࡳࡨࡧ࡬ࡩࡱࡶࡸ࠿࠻࠳࠴࠺᳔ࠪ"))
      bstack111lll1llll_opy_ = bstack111ll1l11l1_opy_ + bstack11ll11lllll_opy_
      response = requests.get(bstack111lll1llll_opy_)
      data = response.json()
      self.percy_build_id = data.get(bstack1l1lll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥ᳕ࠩ"), {}).get(bstack1l1lll_opy_ (u"ࠫ࡮ࡪ᳖ࠧ"), None)
      return True
    except:
      self.logger.debug(bstack1l1lll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡴࡩࡣࡶࡴࡵࡩࡩࠦࡷࡩ࡫࡯ࡩࠥࡶࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢ࡫ࡩࡦࡲࡴࡩࠢࡦ࡬ࡪࡩ࡫ࠡࡴࡨࡷࡵࡵ࡮ࡴࡧ᳗ࠥ"))
      return False
  def bstack111lll111l1_opy_(self):
    bstack111lllll1ll_opy_ = bstack1l1lll_opy_ (u"࠭ࡡࡱࡲ᳘ࠪ") if self.bstack1llll11ll_opy_ else bstack1l1lll_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦ᳙ࠩ")
    bstack111ll11ll1l_opy_ = bstack1l1lll_opy_ (u"ࠣࡷࡱࡨࡪ࡬ࡩ࡯ࡧࡧࠦ᳚") if self.config.get(bstack1l1lll_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨ᳛")) is None else True
    bstack11ll111ll1l_opy_ = bstack1l1lll_opy_ (u"ࠥࡥࡵ࡯࠯ࡢࡲࡳࡣࡵ࡫ࡲࡤࡻ࠲࡫ࡪࡺ࡟ࡱࡴࡲ࡮ࡪࡩࡴࡠࡶࡲ࡯ࡪࡴ࠿࡯ࡣࡰࡩࡂࢁࡽࠧࡶࡼࡴࡪࡃࡻࡾࠨࡳࡩࡷࡩࡹ࠾ࡽࢀ᳜ࠦ").format(self.config[bstack1l1lll_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦ᳝ࠩ")], bstack111lllll1ll_opy_, bstack111ll11ll1l_opy_)
    if self.percy_capture_mode:
      bstack11ll111ll1l_opy_ += bstack1l1lll_opy_ (u"ࠧࠬࡰࡦࡴࡦࡽࡤࡩࡡࡱࡶࡸࡶࡪࡥ࡭ࡰࡦࡨࡁࢀࢃ᳞ࠢ").format(self.percy_capture_mode)
    uri = bstack1ll111ll1_opy_(bstack11ll111ll1l_opy_)
    try:
      response = bstack11ll1l111l_opy_(bstack1l1lll_opy_ (u"࠭ࡇࡆࡖ᳟ࠪ"), uri, {}, {bstack1l1lll_opy_ (u"ࠧࡢࡷࡷ࡬ࠬ᳠"): (self.config[bstack1l1lll_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ᳡")], self.config[bstack1l1lll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽ᳢ࠬ")])})
      if response.status_code == 200:
        data = response.json()
        self.bstack11l11lll1l_opy_ = data.get(bstack1l1lll_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶ᳣ࠫ"))
        self.percy_capture_mode = data.get(bstack1l1lll_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡢࡧࡦࡶࡴࡶࡴࡨࡣࡲࡵࡤࡦ᳤ࠩ"))
        os.environ[bstack1l1lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡋࡒࡄ᳥࡛ࠪ")] = str(self.bstack11l11lll1l_opy_)
        os.environ[bstack1l1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡅࡓࡅ࡜ࡣࡈࡇࡐࡕࡗࡕࡉࡤࡓࡏࡅࡇ᳦ࠪ")] = str(self.percy_capture_mode)
        if bstack111ll11ll1l_opy_ == bstack1l1lll_opy_ (u"ࠢࡶࡰࡧࡩ࡫࡯࡮ࡦࡦ᳧ࠥ") and str(self.bstack11l11lll1l_opy_).lower() == bstack1l1lll_opy_ (u"ࠣࡶࡵࡹࡪࠨ᳨"):
          self.bstack1llll11111_opy_ = True
        if bstack1l1lll_opy_ (u"ࠤࡷࡳࡰ࡫࡮ࠣᳩ") in data:
          return data[bstack1l1lll_opy_ (u"ࠥࡸࡴࡱࡥ࡯ࠤᳪ")]
        else:
          raise bstack1l1lll_opy_ (u"࡙ࠫࡵ࡫ࡦࡰࠣࡒࡴࡺࠠࡇࡱࡸࡲࡩࠦ࠭ࠡࡽࢀࠫᳫ").format(data)
      else:
        raise bstack1l1lll_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡨࡨࡸࡨ࡮ࠠࡱࡧࡵࡧࡾࠦࡴࡰ࡭ࡨࡲ࠱ࠦࡒࡦࡵࡳࡳࡳࡹࡥࠡࡵࡷࡥࡹࡻࡳࠡ࠯ࠣࡿࢂ࠲ࠠࡓࡧࡶࡴࡴࡴࡳࡦࠢࡅࡳࡩࡿࠠ࠮ࠢࡾࢁࠧᳬ").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack1l1lll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡩࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡱࡧࡵࡧࡾࠦࡰࡳࡱ࡭ࡩࡨࡺ᳭ࠢ").format(e))
  def bstack111lll11111_opy_(self):
    bstack111lll11l11_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1lll_opy_ (u"ࠢࡱࡧࡵࡧࡾࡉ࡯࡯ࡨ࡬࡫࠳ࡰࡳࡰࡰࠥᳮ"))
    try:
      if bstack1l1lll_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࠩᳯ") not in self.bstack111ll1lll1l_opy_:
        self.bstack111ll1lll1l_opy_[bstack1l1lll_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࠪᳰ")] = 2
      with open(bstack111lll11l11_opy_, bstack1l1lll_opy_ (u"ࠪࡻࠬᳱ")) as fp:
        json.dump(self.bstack111ll1lll1l_opy_, fp)
      return bstack111lll11l11_opy_
    except Exception as e:
      self.logger.error(bstack1l1lll_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡤࡴࡨࡥࡹ࡫ࠠࡱࡧࡵࡧࡾࠦࡣࡰࡰࡩ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦᳲ").format(e))
  def bstack111ll1l1lll_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack111llll1111_opy_ == bstack1l1lll_opy_ (u"ࠬࡽࡩ࡯ࠩᳳ"):
        bstack111ll1lllll_opy_ = [bstack1l1lll_opy_ (u"࠭ࡣ࡮ࡦ࠱ࡩࡽ࡫ࠧ᳴"), bstack1l1lll_opy_ (u"ࠧ࠰ࡥࠪᳵ")]
        cmd = bstack111ll1lllll_opy_ + cmd
      cmd = bstack1l1lll_opy_ (u"ࠨࠢࠪᳶ").join(cmd)
      self.logger.debug(bstack1l1lll_opy_ (u"ࠤࡕࡹࡳࡴࡩ࡯ࡩࠣࡿࢂࠨ᳷").format(cmd))
      with open(self.bstack111lll111ll_opy_, bstack1l1lll_opy_ (u"ࠥࡥࠧ᳸")) as bstack111ll1l1111_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack111ll1l1111_opy_, text=True, stderr=bstack111ll1l1111_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack111llll11l1_opy_ = True
      self.logger.error(bstack1l1lll_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡶࡤࡶࡹࠦࡰࡦࡴࡦࡽࠥࡽࡩࡵࡪࠣࡧࡲࡪࠠ࠮ࠢࡾࢁ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯࠼ࠣࡿࢂࠨ᳹").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack111lll1lll1_opy_:
        self.logger.info(bstack1l1lll_opy_ (u"࡙ࠧࡴࡰࡲࡳ࡭ࡳ࡭ࠠࡑࡧࡵࡧࡾࠨᳺ"))
        cmd = [self.binary_path, bstack1l1lll_opy_ (u"ࠨࡥࡹࡧࡦ࠾ࡸࡺ࡯ࡱࠤ᳻")]
        self.bstack111ll1l1lll_opy_(cmd)
        self.bstack111lll1lll1_opy_ = False
    except Exception as e:
      self.logger.error(bstack1l1lll_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡹࡵࡰࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡺ࡭ࡹ࡮ࠠࡤࡱࡰࡱࡦࡴࡤࠡ࠯ࠣࡿࢂ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰ࠽ࠤࢀࢃࠢ᳼").format(cmd, e))
  def bstack1ll1ll1l1_opy_(self):
    if not self.bstack11l11lll1l_opy_:
      return
    try:
      bstack111llll1ll1_opy_ = 0
      while not self.bstack111lll1lll1_opy_ and bstack111llll1ll1_opy_ < self.bstack11l11111l11_opy_:
        if self.bstack111llll11l1_opy_:
          self.logger.info(bstack1l1lll_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡴࡧࡷࡹࡵࠦࡦࡢ࡫࡯ࡩࡩࠨ᳽"))
          return
        time.sleep(1)
        bstack111llll1ll1_opy_ += 1
      os.environ[bstack1l1lll_opy_ (u"ࠩࡓࡉࡗࡉ࡙ࡠࡄࡈࡗ࡙ࡥࡐࡍࡃࡗࡊࡔࡘࡍࠨ᳾")] = str(self.bstack11l11111ll1_opy_())
      self.logger.info(bstack1l1lll_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡶࡩࡹࡻࡰࠡࡥࡲࡱࡵࡲࡥࡵࡧࡧࠦ᳿"))
    except Exception as e:
      self.logger.error(bstack1l1lll_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡧࡷࡹࡵࠦࡰࡦࡴࡦࡽ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧᴀ").format(e))
  def bstack11l11111ll1_opy_(self):
    if self.bstack1llll11ll_opy_:
      return
    try:
      bstack111lll1ll11_opy_ = [platform[bstack1l1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪᴁ")].lower() for platform in self.config.get(bstack1l1lll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᴂ"), [])]
      bstack11l1111l111_opy_ = sys.maxsize
      bstack111ll1l111l_opy_ = bstack1l1lll_opy_ (u"ࠧࠨᴃ")
      for browser in bstack111lll1ll11_opy_:
        if browser in self.bstack111ll11lll1_opy_:
          bstack111lll1ll1l_opy_ = self.bstack111ll11lll1_opy_[browser]
        if bstack111lll1ll1l_opy_ < bstack11l1111l111_opy_:
          bstack11l1111l111_opy_ = bstack111lll1ll1l_opy_
          bstack111ll1l111l_opy_ = browser
      return bstack111ll1l111l_opy_
    except Exception as e:
      self.logger.error(bstack1l1lll_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡫࡯࡮ࡥࠢࡥࡩࡸࡺࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤᴄ").format(e))
  @classmethod
  def bstack1llllllll_opy_(self):
    return os.getenv(bstack1l1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡈࡖࡈ࡟ࠧᴅ"), bstack1l1lll_opy_ (u"ࠪࡊࡦࡲࡳࡦࠩᴆ")).lower()
  @classmethod
  def bstack1llll1ll1l_opy_(self):
    return os.getenv(bstack1l1lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡊࡘࡃ࡚ࡡࡆࡅࡕ࡚ࡕࡓࡇࡢࡑࡔࡊࡅࠨᴇ"), bstack1l1lll_opy_ (u"ࠬ࠭ᴈ"))
  @classmethod
  def bstack1l1ll1ll1l1_opy_(cls, value):
    cls.bstack1llll11111_opy_ = value
  @classmethod
  def bstack11l1111l11l_opy_(cls):
    return cls.bstack1llll11111_opy_
  @classmethod
  def bstack1l1ll1l1ll1_opy_(cls, value):
    cls.percy_build_id = value
  @classmethod
  def bstack111lll11l1l_opy_(cls):
    return cls.percy_build_id