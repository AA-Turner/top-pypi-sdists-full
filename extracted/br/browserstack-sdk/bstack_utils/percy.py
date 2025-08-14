# coding: UTF-8
import sys
bstack111_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1llll1_opy_ = 7
def bstack1l1l1ll_opy_ (bstack1l1llll_opy_):
    global bstack11l1l11_opy_
    bstack1l11ll1_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack1l1l111_opy_ = bstack1l1llll_opy_ [:-1]
    bstack1111l11_opy_ = bstack1l11ll1_opy_ % len (bstack1l1l111_opy_)
    bstack11l11ll_opy_ = bstack1l1l111_opy_ [:bstack1111l11_opy_] + bstack1l1l111_opy_ [bstack1111l11_opy_:]
    if bstack111_opy_:
        bstack1lll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack11111l_opy_ + bstack1l11ll1_opy_) % bstack1llll1_opy_) for bstack11111l_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1lll1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack11111l_opy_ + bstack1l11ll1_opy_) % bstack1llll1_opy_) for bstack11111l_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1lll1l1_opy_)
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
from bstack_utils.helper import bstack1llll11ll1_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack1ll1l1llll_opy_ import bstack1llll1111l_opy_
class bstack1lllllll1_opy_:
  working_dir = os.getcwd()
  bstack1ll111ll1l_opy_ = False
  config = {}
  bstack11l11111l1l_opy_ = bstack1l1l1ll_opy_ (u"࠭ࠧậ")
  binary_path = bstack1l1l1ll_opy_ (u"ࠧࠨẮ")
  bstack11111ll1l11_opy_ = bstack1l1l1ll_opy_ (u"ࠨࠩắ")
  bstack1lll1llll1_opy_ = False
  bstack1111ll1ll1l_opy_ = None
  bstack1111l1lll1l_opy_ = {}
  bstack1111l11l1ll_opy_ = 300
  bstack11111l1llll_opy_ = False
  logger = None
  bstack1111l11l11l_opy_ = False
  bstack1l1lll11_opy_ = False
  percy_build_id = None
  bstack1111l1111ll_opy_ = bstack1l1l1ll_opy_ (u"ࠩࠪẰ")
  bstack11111lllll1_opy_ = {
    bstack1l1l1ll_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪằ") : 1,
    bstack1l1l1ll_opy_ (u"ࠫ࡫࡯ࡲࡦࡨࡲࡼࠬẲ") : 2,
    bstack1l1l1ll_opy_ (u"ࠬ࡫ࡤࡨࡧࠪẳ") : 3,
    bstack1l1l1ll_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠭Ẵ") : 4
  }
  def __init__(self) -> None: pass
  def bstack11111ll1lll_opy_(self):
    bstack1111l1ll11l_opy_ = bstack1l1l1ll_opy_ (u"ࠧࠨẵ")
    bstack1111l111l1l_opy_ = sys.platform
    bstack1111ll1l11l_opy_ = bstack1l1l1ll_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧẶ")
    if re.match(bstack1l1l1ll_opy_ (u"ࠤࡧࡥࡷࡽࡩ࡯ࡾࡰࡥࡨࠦ࡯ࡴࠤặ"), bstack1111l111l1l_opy_) != None:
      bstack1111l1ll11l_opy_ = bstack11l1lllll11_opy_ + bstack1l1l1ll_opy_ (u"ࠥ࠳ࡵ࡫ࡲࡤࡻ࠰ࡳࡸࡾ࠮ࡻ࡫ࡳࠦẸ")
      self.bstack1111l1111ll_opy_ = bstack1l1l1ll_opy_ (u"ࠫࡲࡧࡣࠨẹ")
    elif re.match(bstack1l1l1ll_opy_ (u"ࠧࡳࡳࡸ࡫ࡱࢀࡲࡹࡹࡴࡾࡰ࡭ࡳ࡭ࡷࡽࡥࡼ࡫ࡼ࡯࡮ࡽࡤࡦࡧࡼ࡯࡮ࡽࡹ࡬ࡲࡨ࡫ࡼࡦ࡯ࡦࢀࡼ࡯࡮࠴࠴ࠥẺ"), bstack1111l111l1l_opy_) != None:
      bstack1111l1ll11l_opy_ = bstack11l1lllll11_opy_ + bstack1l1l1ll_opy_ (u"ࠨ࠯ࡱࡧࡵࡧࡾ࠳ࡷࡪࡰ࠱ࡾ࡮ࡶࠢẻ")
      bstack1111ll1l11l_opy_ = bstack1l1l1ll_opy_ (u"ࠢࡱࡧࡵࡧࡾ࠴ࡥࡹࡧࠥẼ")
      self.bstack1111l1111ll_opy_ = bstack1l1l1ll_opy_ (u"ࠨࡹ࡬ࡲࠬẽ")
    else:
      bstack1111l1ll11l_opy_ = bstack11l1lllll11_opy_ + bstack1l1l1ll_opy_ (u"ࠤ࠲ࡴࡪࡸࡣࡺ࠯࡯࡭ࡳࡻࡸ࠯ࡼ࡬ࡴࠧẾ")
      self.bstack1111l1111ll_opy_ = bstack1l1l1ll_opy_ (u"ࠪࡰ࡮ࡴࡵࡹࠩế")
    return bstack1111l1ll11l_opy_, bstack1111ll1l11l_opy_
  def bstack1111l11l1l1_opy_(self):
    try:
      bstack11111ll1l1l_opy_ = [os.path.join(expanduser(bstack1l1l1ll_opy_ (u"ࠦࢃࠨỀ")), bstack1l1l1ll_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬề")), self.working_dir, tempfile.gettempdir()]
      for path in bstack11111ll1l1l_opy_:
        if(self.bstack1111l11ll1l_opy_(path)):
          return path
      raise bstack1l1l1ll_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠥỂ")
    except Exception as e:
      self.logger.error(bstack1l1l1ll_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡪ࡮ࡴࡤࠡࡣࡹࡥ࡮ࡲࡡࡣ࡮ࡨࠤࡵࡧࡴࡩࠢࡩࡳࡷࠦࡰࡦࡴࡦࡽࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࠲ࠦࡻࡾࠤể").format(e))
  def bstack1111l11ll1l_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack1111l1ll111_opy_(self, bstack1111l111lll_opy_):
    return os.path.join(bstack1111l111lll_opy_, self.bstack11l11111l1l_opy_ + bstack1l1l1ll_opy_ (u"ࠣ࠰ࡨࡸࡦ࡭ࠢỄ"))
  def bstack11111l1lll1_opy_(self, bstack1111l111lll_opy_, bstack11111ll11ll_opy_):
    if not bstack11111ll11ll_opy_: return
    try:
      bstack11111llllll_opy_ = self.bstack1111l1ll111_opy_(bstack1111l111lll_opy_)
      with open(bstack11111llllll_opy_, bstack1l1l1ll_opy_ (u"ࠤࡺࠦễ")) as f:
        f.write(bstack11111ll11ll_opy_)
        self.logger.debug(bstack1l1l1ll_opy_ (u"ࠥࡗࡦࡼࡥࡥࠢࡱࡩࡼࠦࡅࡕࡣࡪࠤ࡫ࡵࡲࠡࡲࡨࡶࡨࡿࠢỆ"))
    except Exception as e:
      self.logger.error(bstack1l1l1ll_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡣࡹࡩࠥࡺࡨࡦࠢࡨࡸࡦ࡭ࠬࠡࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠦệ").format(e))
  def bstack1111l11llll_opy_(self, bstack1111l111lll_opy_):
    try:
      bstack11111llllll_opy_ = self.bstack1111l1ll111_opy_(bstack1111l111lll_opy_)
      if os.path.exists(bstack11111llllll_opy_):
        with open(bstack11111llllll_opy_, bstack1l1l1ll_opy_ (u"ࠧࡸࠢỈ")) as f:
          bstack11111ll11ll_opy_ = f.read().strip()
          return bstack11111ll11ll_opy_ if bstack11111ll11ll_opy_ else None
    except Exception as e:
      self.logger.error(bstack1l1l1ll_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦ࡬ࡰࡣࡧ࡭ࡳ࡭ࠠࡆࡖࡤ࡫࠱ࠦࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠤỉ").format(e))
  def bstack1111l1l11l1_opy_(self, bstack1111l111lll_opy_, bstack1111l1ll11l_opy_):
    bstack1111l1lll11_opy_ = self.bstack1111l11llll_opy_(bstack1111l111lll_opy_)
    if bstack1111l1lll11_opy_:
      try:
        bstack11111lll1l1_opy_ = self.bstack1111ll11l1l_opy_(bstack1111l1lll11_opy_, bstack1111l1ll11l_opy_)
        if not bstack11111lll1l1_opy_:
          self.logger.debug(bstack1l1l1ll_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠦࡩࡴࠢࡸࡴࠥࡺ࡯ࠡࡦࡤࡸࡪࠦࠨࡆࡖࡤ࡫ࠥࡻ࡮ࡤࡪࡤࡲ࡬࡫ࡤࠪࠤỊ"))
          return True
        self.logger.debug(bstack1l1l1ll_opy_ (u"ࠣࡐࡨࡻࠥࡖࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥࡧࡶࡢ࡫࡯ࡥࡧࡲࡥ࠭ࠢࡧࡳࡼࡴ࡬ࡰࡣࡧ࡭ࡳ࡭ࠠࡶࡲࡧࡥࡹ࡫ࠢị"))
        return False
      except Exception as e:
        self.logger.warn(bstack1l1l1ll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡩࡨࡦࡥ࡮ࠤ࡫ࡵࡲࠡࡤ࡬ࡲࡦࡸࡹࠡࡷࡳࡨࡦࡺࡥࡴ࠮ࠣࡹࡸ࡯࡮ࡨࠢࡨࡼ࡮ࡹࡴࡪࡰࡪࠤࡧ࡯࡮ࡢࡴࡼ࠾ࠥࢁࡽࠣỌ").format(e))
    return False
  def bstack1111ll11l1l_opy_(self, bstack1111l1lll11_opy_, bstack1111l1ll11l_opy_):
    try:
      headers = {
        bstack1l1l1ll_opy_ (u"ࠥࡍ࡫࠳ࡎࡰࡰࡨ࠱ࡒࡧࡴࡤࡪࠥọ"): bstack1111l1lll11_opy_
      }
      response = bstack1llll11ll1_opy_(bstack1l1l1ll_opy_ (u"ࠫࡌࡋࡔࠨỎ"), bstack1111l1ll11l_opy_, {}, {bstack1l1l1ll_opy_ (u"ࠧ࡮ࡥࡢࡦࡨࡶࡸࠨỏ"): headers})
      if response.status_code == 304:
        return False
      return True
    except Exception as e:
      raise(bstack1l1l1ll_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡩࡨࡦࡥ࡮࡭ࡳ࡭ࠠࡧࡱࡵࠤࡕ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠣࡹࡵࡪࡡࡵࡧࡶ࠾ࠥࢁࡽࠣỐ").format(e))
  @measure(event_name=EVENTS.bstack11l1ll11ll1_opy_, stage=STAGE.bstack1l1ll11l1_opy_)
  def bstack1111ll11l11_opy_(self, bstack1111l1ll11l_opy_, bstack1111ll1l11l_opy_):
    try:
      bstack11111llll1l_opy_ = self.bstack1111l11l1l1_opy_()
      bstack1111l11lll1_opy_ = os.path.join(bstack11111llll1l_opy_, bstack1l1l1ll_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠴ࡺࡪࡲࠪố"))
      bstack1111ll1l1ll_opy_ = os.path.join(bstack11111llll1l_opy_, bstack1111ll1l11l_opy_)
      if self.bstack1111l1l11l1_opy_(bstack11111llll1l_opy_, bstack1111l1ll11l_opy_): # if bstack1111ll111ll_opy_, bstack1l1l11l1lll_opy_ bstack11111ll11ll_opy_ is bstack1111l1l1ll1_opy_ to bstack11l11l11l1l_opy_ version available (response 304)
        if os.path.exists(bstack1111ll1l1ll_opy_):
          self.logger.info(bstack1l1l1ll_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠠࡧࡱࡸࡲࡩࠦࡩ࡯ࠢࡾࢁ࠱ࠦࡳ࡬࡫ࡳࡴ࡮ࡴࡧࠡࡦࡲࡻࡳࡲ࡯ࡢࡦࠥỒ").format(bstack1111ll1l1ll_opy_))
          return bstack1111ll1l1ll_opy_
        if os.path.exists(bstack1111l11lll1_opy_):
          self.logger.info(bstack1l1l1ll_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡼ࡬ࡴࠥ࡬࡯ࡶࡰࡧࠤ࡮ࡴࠠࡼࡿ࠯ࠤࡺࡴࡺࡪࡲࡳ࡭ࡳ࡭ࠢồ").format(bstack1111l11lll1_opy_))
          return self.bstack1111l111ll1_opy_(bstack1111l11lll1_opy_, bstack1111ll1l11l_opy_)
      self.logger.info(bstack1l1l1ll_opy_ (u"ࠥࡈࡴࡽ࡮࡭ࡱࡤࡨ࡮ࡴࡧࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠠࡧࡴࡲࡱࠥࢁࡽࠣỔ").format(bstack1111l1ll11l_opy_))
      response = bstack1llll11ll1_opy_(bstack1l1l1ll_opy_ (u"ࠫࡌࡋࡔࠨổ"), bstack1111l1ll11l_opy_, {}, {})
      if response.status_code == 200:
        bstack1111l1ll1ll_opy_ = response.headers.get(bstack1l1l1ll_opy_ (u"ࠧࡋࡔࡢࡩࠥỖ"), bstack1l1l1ll_opy_ (u"ࠨࠢỗ"))
        if bstack1111l1ll1ll_opy_:
          self.bstack11111l1lll1_opy_(bstack11111llll1l_opy_, bstack1111l1ll1ll_opy_)
        with open(bstack1111l11lll1_opy_, bstack1l1l1ll_opy_ (u"ࠧࡸࡤࠪỘ")) as file:
          file.write(response.content)
        self.logger.info(bstack1l1l1ll_opy_ (u"ࠣࡆࡲࡻࡳࡲ࡯ࡢࡦࡨࡨࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠤࡦࡴࡤࠡࡵࡤࡺࡪࡪࠠࡢࡶࠣࡿࢂࠨộ").format(bstack1111l11lll1_opy_))
        return self.bstack1111l111ll1_opy_(bstack1111l11lll1_opy_, bstack1111ll1l11l_opy_)
      else:
        raise(bstack1l1l1ll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠠࡵࡪࡨࠤ࡫࡯࡬ࡦ࠰ࠣࡗࡹࡧࡴࡶࡵࠣࡧࡴࡪࡥ࠻ࠢࡾࢁࠧỚ").format(response.status_code))
    except Exception as e:
      self.logger.error(bstack1l1l1ll_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡤࡰࡹࡱࡰࡴࡧࡤࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿ࠺ࠡࡽࢀࠦớ").format(e))
  def bstack11111lll1ll_opy_(self, bstack1111l1ll11l_opy_, bstack1111ll1l11l_opy_):
    try:
      retry = 2
      bstack1111ll1l1ll_opy_ = None
      bstack1111ll1lll1_opy_ = False
      while retry > 0:
        bstack1111ll1l1ll_opy_ = self.bstack1111ll11l11_opy_(bstack1111l1ll11l_opy_, bstack1111ll1l11l_opy_)
        bstack1111ll1lll1_opy_ = self.bstack11111ll11l1_opy_(bstack1111l1ll11l_opy_, bstack1111ll1l11l_opy_, bstack1111ll1l1ll_opy_)
        if bstack1111ll1lll1_opy_:
          break
        retry -= 1
      return bstack1111ll1l1ll_opy_, bstack1111ll1lll1_opy_
    except Exception as e:
      self.logger.error(bstack1l1l1ll_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡨࡧࡷࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠣࡴࡦࡺࡨࠣỜ").format(e))
    return bstack1111ll1l1ll_opy_, False
  def bstack11111ll11l1_opy_(self, bstack1111l1ll11l_opy_, bstack1111ll1l11l_opy_, bstack1111ll1l1ll_opy_, bstack11111llll11_opy_ = 0):
    if bstack11111llll11_opy_ > 1:
      return False
    if bstack1111ll1l1ll_opy_ == None or os.path.exists(bstack1111ll1l1ll_opy_) == False:
      self.logger.warn(bstack1l1l1ll_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡵࡧࡴࡩࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨ࠱ࠦࡲࡦࡶࡵࡽ࡮ࡴࡧࠡࡦࡲࡻࡳࡲ࡯ࡢࡦࠥờ"))
      return False
    bstack1111l1ll1l1_opy_ = bstack1l1l1ll_opy_ (u"ࡸࠢ࡟࠰࠭ࡄࡵ࡫ࡲࡤࡻ࠲ࡧࡱ࡯ࠠ࡝ࡦ࠮ࡠ࠳ࡢࡤࠬ࡞࠱ࡠࡩ࠱ࠢỞ")
    command = bstack1l1l1ll_opy_ (u"ࠧࡼࡿࠣ࠱࠲ࡼࡥࡳࡵ࡬ࡳࡳ࠭ở").format(bstack1111ll1l1ll_opy_)
    bstack1111ll1l1l1_opy_ = subprocess.check_output(command, shell=True, text=True)
    if re.match(bstack1111l1ll1l1_opy_, bstack1111ll1l1l1_opy_) != None:
      return True
    else:
      self.logger.error(bstack1l1l1ll_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࡥ࡫ࡩࡨࡱࠠࡧࡣ࡬ࡰࡪࡪࠢỠ"))
      return False
  def bstack1111l111ll1_opy_(self, bstack1111l11lll1_opy_, bstack1111ll1l11l_opy_):
    try:
      working_dir = os.path.dirname(bstack1111l11lll1_opy_)
      shutil.unpack_archive(bstack1111l11lll1_opy_, working_dir)
      bstack1111ll1l1ll_opy_ = os.path.join(working_dir, bstack1111ll1l11l_opy_)
      os.chmod(bstack1111ll1l1ll_opy_, 0o755)
      return bstack1111ll1l1ll_opy_
    except Exception as e:
      self.logger.error(bstack1l1l1ll_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡻ࡮ࡻ࡫ࡳࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠥỡ"))
  def bstack1111l111l11_opy_(self):
    try:
      bstack11111lll111_opy_ = self.config.get(bstack1l1l1ll_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩỢ"))
      bstack1111l111l11_opy_ = bstack11111lll111_opy_ or (bstack11111lll111_opy_ is None and self.bstack1ll111ll1l_opy_)
      if not bstack1111l111l11_opy_ or self.config.get(bstack1l1l1ll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧợ"), None) not in bstack11l1ll11l1l_opy_:
        return False
      self.bstack1lll1llll1_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack1l1l1ll_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡦࡨࡸࡪࡩࡴࠡࡲࡨࡶࡨࡿࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢỤ").format(e))
  def bstack1111ll11111_opy_(self):
    try:
      bstack1111ll11111_opy_ = self.percy_capture_mode
      return bstack1111ll11111_opy_
    except Exception as e:
      self.logger.error(bstack1l1l1ll_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡧࡩࡹ࡫ࡣࡵࠢࡳࡩࡷࡩࡹࠡࡥࡤࡴࡹࡻࡲࡦࠢࡰࡳࡩ࡫ࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢụ").format(e))
  def init(self, bstack1ll111ll1l_opy_, config, logger):
    self.bstack1ll111ll1l_opy_ = bstack1ll111ll1l_opy_
    self.config = config
    self.logger = logger
    if not self.bstack1111l111l11_opy_():
      return
    self.bstack1111l1lll1l_opy_ = config.get(bstack1l1l1ll_opy_ (u"ࠧࡱࡧࡵࡧࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭Ủ"), {})
    self.percy_capture_mode = config.get(bstack1l1l1ll_opy_ (u"ࠨࡲࡨࡶࡨࡿࡃࡢࡲࡷࡹࡷ࡫ࡍࡰࡦࡨࠫủ"))
    try:
      bstack1111l1ll11l_opy_, bstack1111ll1l11l_opy_ = self.bstack11111ll1lll_opy_()
      self.bstack11l11111l1l_opy_ = bstack1111ll1l11l_opy_
      bstack1111ll1l1ll_opy_, bstack1111ll1lll1_opy_ = self.bstack11111lll1ll_opy_(bstack1111l1ll11l_opy_, bstack1111ll1l11l_opy_)
      if bstack1111ll1lll1_opy_:
        self.binary_path = bstack1111ll1l1ll_opy_
        thread = Thread(target=self.bstack1111l111111_opy_)
        thread.start()
      else:
        self.bstack1111l11l11l_opy_ = True
        self.logger.error(bstack1l1l1ll_opy_ (u"ࠤࡌࡲࡻࡧ࡬ࡪࡦࠣࡴࡪࡸࡣࡺࠢࡳࡥࡹ࡮ࠠࡧࡱࡸࡲࡩࠦ࠭ࠡࡽࢀ࠰࡛ࠥ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡑࡧࡵࡧࡾࠨỨ").format(bstack1111ll1l1ll_opy_))
    except Exception as e:
      self.logger.error(bstack1l1l1ll_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡶࡥࡳࡥࡼ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦứ").format(e))
  def bstack11111ll1ll1_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack1l1l1ll_opy_ (u"ࠫࡱࡵࡧࠨỪ"), bstack1l1l1ll_opy_ (u"ࠬࡶࡥࡳࡥࡼ࠲ࡱࡵࡧࠨừ"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack1l1l1ll_opy_ (u"ࠨࡐࡶࡵ࡫࡭ࡳ࡭ࠠࡱࡧࡵࡧࡾࠦ࡬ࡰࡩࡶࠤࡦࡺࠠࡼࡿࠥỬ").format(logfile))
      self.bstack11111ll1l11_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack1l1l1ll_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡪࡺࠠࡱࡧࡵࡧࡾࠦ࡬ࡰࡩࠣࡴࡦࡺࡨ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣử").format(e))
  @measure(event_name=EVENTS.bstack11l1lllllll_opy_, stage=STAGE.bstack1l1ll11l1_opy_)
  def bstack1111l111111_opy_(self):
    bstack1111lll1111_opy_ = self.bstack1111ll1l111_opy_()
    if bstack1111lll1111_opy_ == None:
      self.bstack1111l11l11l_opy_ = True
      self.logger.error(bstack1l1l1ll_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡵࡱ࡮ࡩࡳࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥ࠮ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡶࡥࡳࡥࡼࠦỮ"))
      return False
    bstack1111l1l1l11_opy_ = [bstack1l1l1ll_opy_ (u"ࠤࡤࡴࡵࡀࡥࡹࡧࡦ࠾ࡸࡺࡡࡳࡶࠥữ") if self.bstack1ll111ll1l_opy_ else bstack1l1l1ll_opy_ (u"ࠪࡩࡽ࡫ࡣ࠻ࡵࡷࡥࡷࡺࠧỰ")]
    bstack111l1ll111l_opy_ = self.bstack1111ll11ll1_opy_()
    if bstack111l1ll111l_opy_ != None:
      bstack1111l1l1l11_opy_.append(bstack1l1l1ll_opy_ (u"ࠦ࠲ࡩࠠࡼࡿࠥự").format(bstack111l1ll111l_opy_))
    env = os.environ.copy()
    env[bstack1l1l1ll_opy_ (u"ࠧࡖࡅࡓࡅ࡜ࡣ࡙ࡕࡋࡆࡐࠥỲ")] = bstack1111lll1111_opy_
    env[bstack1l1l1ll_opy_ (u"ࠨࡔࡉࡡࡅ࡙ࡎࡒࡄࡠࡗࡘࡍࡉࠨỳ")] = os.environ.get(bstack1l1l1ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬỴ"), bstack1l1l1ll_opy_ (u"ࠨࠩỵ"))
    bstack1111ll111l1_opy_ = [self.binary_path]
    self.bstack11111ll1ll1_opy_()
    self.bstack1111ll1ll1l_opy_ = self.bstack1111l1l111l_opy_(bstack1111ll111l1_opy_ + bstack1111l1l1l11_opy_, env)
    self.logger.debug(bstack1l1l1ll_opy_ (u"ࠤࡖࡸࡦࡸࡴࡪࡰࡪࠤࡍ࡫ࡡ࡭ࡶ࡫ࠤࡈ࡮ࡥࡤ࡭ࠥỶ"))
    bstack11111llll11_opy_ = 0
    while self.bstack1111ll1ll1l_opy_.poll() == None:
      bstack1111l1l11ll_opy_ = self.bstack11111ll111l_opy_()
      if bstack1111l1l11ll_opy_:
        self.logger.debug(bstack1l1l1ll_opy_ (u"ࠥࡌࡪࡧ࡬ࡵࡪࠣࡇ࡭࡫ࡣ࡬ࠢࡶࡹࡨࡩࡥࡴࡵࡩࡹࡱࠨỷ"))
        self.bstack11111l1llll_opy_ = True
        return True
      bstack11111llll11_opy_ += 1
      self.logger.debug(bstack1l1l1ll_opy_ (u"ࠦࡍ࡫ࡡ࡭ࡶ࡫ࠤࡈ࡮ࡥࡤ࡭ࠣࡖࡪࡺࡲࡺࠢ࠰ࠤࢀࢃࠢỸ").format(bstack11111llll11_opy_))
      time.sleep(2)
    self.logger.error(bstack1l1l1ll_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡱࡧࡵࡧࡾ࠲ࠠࡉࡧࡤࡰࡹ࡮ࠠࡄࡪࡨࡧࡰࠦࡆࡢ࡫࡯ࡩࡩࠦࡡࡧࡶࡨࡶࠥࢁࡽࠡࡣࡷࡸࡪࡳࡰࡵࡵࠥỹ").format(bstack11111llll11_opy_))
    self.bstack1111l11l11l_opy_ = True
    return False
  def bstack11111ll111l_opy_(self, bstack11111llll11_opy_ = 0):
    if bstack11111llll11_opy_ > 10:
      return False
    try:
      bstack1111ll1ll11_opy_ = os.environ.get(bstack1l1l1ll_opy_ (u"࠭ࡐࡆࡔࡆ࡝ࡤ࡙ࡅࡓࡘࡈࡖࡤࡇࡄࡅࡔࡈࡗࡘ࠭Ỻ"), bstack1l1l1ll_opy_ (u"ࠧࡩࡶࡷࡴ࠿࠵࠯࡭ࡱࡦࡥࡱ࡮࡯ࡴࡶ࠽࠹࠸࠹࠸ࠨỻ"))
      bstack1111l11l111_opy_ = bstack1111ll1ll11_opy_ + bstack11l1llllll1_opy_
      response = requests.get(bstack1111l11l111_opy_)
      data = response.json()
      self.percy_build_id = data.get(bstack1l1l1ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࠧỼ"), {}).get(bstack1l1l1ll_opy_ (u"ࠩ࡬ࡨࠬỽ"), None)
      return True
    except:
      self.logger.debug(bstack1l1l1ll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡲࡧࡨࡻࡲࡳࡧࡧࠤࡼ࡮ࡩ࡭ࡧࠣࡴࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡩࡧࡤࡰࡹ࡮ࠠࡤࡪࡨࡧࡰࠦࡲࡦࡵࡳࡳࡳࡹࡥࠣỾ"))
      return False
  def bstack1111ll1l111_opy_(self):
    bstack1111l1llll1_opy_ = bstack1l1l1ll_opy_ (u"ࠫࡦࡶࡰࠨỿ") if self.bstack1ll111ll1l_opy_ else bstack1l1l1ll_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧἀ")
    bstack1111ll1llll_opy_ = bstack1l1l1ll_opy_ (u"ࠨࡵ࡯ࡦࡨࡪ࡮ࡴࡥࡥࠤἁ") if self.config.get(bstack1l1l1ll_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭ἂ")) is None else True
    bstack11ll11ll111_opy_ = bstack1l1l1ll_opy_ (u"ࠣࡣࡳ࡭࠴ࡧࡰࡱࡡࡳࡩࡷࡩࡹ࠰ࡩࡨࡸࡤࡶࡲࡰ࡬ࡨࡧࡹࡥࡴࡰ࡭ࡨࡲࡄࡴࡡ࡮ࡧࡀࡿࢂࠬࡴࡺࡲࡨࡁࢀࢃࠦࡱࡧࡵࡧࡾࡃࡻࡾࠤἃ").format(self.config[bstack1l1l1ll_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧἄ")], bstack1111l1llll1_opy_, bstack1111ll1llll_opy_)
    if self.percy_capture_mode:
      bstack11ll11ll111_opy_ += bstack1l1l1ll_opy_ (u"ࠥࠪࡵ࡫ࡲࡤࡻࡢࡧࡦࡶࡴࡶࡴࡨࡣࡲࡵࡤࡦ࠿ࡾࢁࠧἅ").format(self.percy_capture_mode)
    uri = bstack1llll1111l_opy_(bstack11ll11ll111_opy_)
    try:
      response = bstack1llll11ll1_opy_(bstack1l1l1ll_opy_ (u"ࠫࡌࡋࡔࠨἆ"), uri, {}, {bstack1l1l1ll_opy_ (u"ࠬࡧࡵࡵࡪࠪἇ"): (self.config[bstack1l1l1ll_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨἈ")], self.config[bstack1l1l1ll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪἉ")])})
      if response.status_code == 200:
        data = response.json()
        self.bstack1lll1llll1_opy_ = data.get(bstack1l1l1ll_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩἊ"))
        self.percy_capture_mode = data.get(bstack1l1l1ll_opy_ (u"ࠩࡳࡩࡷࡩࡹࡠࡥࡤࡴࡹࡻࡲࡦࡡࡰࡳࡩ࡫ࠧἋ"))
        os.environ[bstack1l1l1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡉࡗࡉ࡙ࠨἌ")] = str(self.bstack1lll1llll1_opy_)
        os.environ[bstack1l1l1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡊࡘࡃ࡚ࡡࡆࡅࡕ࡚ࡕࡓࡇࡢࡑࡔࡊࡅࠨἍ")] = str(self.percy_capture_mode)
        if bstack1111ll1llll_opy_ == bstack1l1l1ll_opy_ (u"ࠧࡻ࡮ࡥࡧࡩ࡭ࡳ࡫ࡤࠣἎ") and str(self.bstack1lll1llll1_opy_).lower() == bstack1l1l1ll_opy_ (u"ࠨࡴࡳࡷࡨࠦἏ"):
          self.bstack1l1lll11_opy_ = True
        if bstack1l1l1ll_opy_ (u"ࠢࡵࡱ࡮ࡩࡳࠨἐ") in data:
          return data[bstack1l1l1ll_opy_ (u"ࠣࡶࡲ࡯ࡪࡴࠢἑ")]
        else:
          raise bstack1l1l1ll_opy_ (u"ࠩࡗࡳࡰ࡫࡮ࠡࡐࡲࡸࠥࡌ࡯ࡶࡰࡧࠤ࠲ࠦࡻࡾࠩἒ").format(data)
      else:
        raise bstack1l1l1ll_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡶࡥࡳࡥࡼࠤࡹࡵ࡫ࡦࡰ࠯ࠤࡗ࡫ࡳࡱࡱࡱࡷࡪࠦࡳࡵࡣࡷࡹࡸࠦ࠭ࠡࡽࢀ࠰ࠥࡘࡥࡴࡲࡲࡲࡸ࡫ࠠࡃࡱࡧࡽࠥ࠳ࠠࡼࡿࠥἓ").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack1l1l1ll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥࡶࡥࡳࡥࡼࠤࡵࡸ࡯࡫ࡧࡦࡸࠧἔ").format(e))
  def bstack1111ll11ll1_opy_(self):
    bstack11111ll1111_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1l1ll_opy_ (u"ࠧࡶࡥࡳࡥࡼࡇࡴࡴࡦࡪࡩ࠱࡮ࡸࡵ࡮ࠣἕ"))
    try:
      if bstack1l1l1ll_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧ἖") not in self.bstack1111l1lll1l_opy_:
        self.bstack1111l1lll1l_opy_[bstack1l1l1ll_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨ἗")] = 2
      with open(bstack11111ll1111_opy_, bstack1l1l1ll_opy_ (u"ࠨࡹࠪἘ")) as fp:
        json.dump(self.bstack1111l1lll1l_opy_, fp)
      return bstack11111ll1111_opy_
    except Exception as e:
      self.logger.error(bstack1l1l1ll_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡩࡲࡦࡣࡷࡩࠥࡶࡥࡳࡥࡼࠤࡨࡵ࡮ࡧ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤἙ").format(e))
  def bstack1111l1l111l_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack1111l1111ll_opy_ == bstack1l1l1ll_opy_ (u"ࠪࡻ࡮ࡴࠧἚ"):
        bstack1111ll11lll_opy_ = [bstack1l1l1ll_opy_ (u"ࠫࡨࡳࡤ࠯ࡧࡻࡩࠬἛ"), bstack1l1l1ll_opy_ (u"ࠬ࠵ࡣࠨἜ")]
        cmd = bstack1111ll11lll_opy_ + cmd
      cmd = bstack1l1l1ll_opy_ (u"࠭ࠠࠨἝ").join(cmd)
      self.logger.debug(bstack1l1l1ll_opy_ (u"ࠢࡓࡷࡱࡲ࡮ࡴࡧࠡࡽࢀࠦ἞").format(cmd))
      with open(self.bstack11111ll1l11_opy_, bstack1l1l1ll_opy_ (u"ࠣࡣࠥ἟")) as bstack1111l11111l_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack1111l11111l_opy_, text=True, stderr=bstack1111l11111l_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack1111l11l11l_opy_ = True
      self.logger.error(bstack1l1l1ll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡵ࡫ࡲࡤࡻࠣࡻ࡮ࡺࡨࠡࡥࡰࡨࠥ࠳ࠠࡼࡿ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴ࠺ࠡࡽࢀࠦἠ").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack11111l1llll_opy_:
        self.logger.info(bstack1l1l1ll_opy_ (u"ࠥࡗࡹࡵࡰࡱ࡫ࡱ࡫ࠥࡖࡥࡳࡥࡼࠦἡ"))
        cmd = [self.binary_path, bstack1l1l1ll_opy_ (u"ࠦࡪࡾࡥࡤ࠼ࡶࡸࡴࡶࠢἢ")]
        self.bstack1111l1l111l_opy_(cmd)
        self.bstack11111l1llll_opy_ = False
    except Exception as e:
      self.logger.error(bstack1l1l1ll_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡷࡳࡵࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡸ࡫ࡷ࡬ࠥࡩ࡯࡮࡯ࡤࡲࡩࠦ࠭ࠡࡽࢀ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮࠻ࠢࡾࢁࠧἣ").format(cmd, e))
  def bstack11l1ll1lll_opy_(self):
    if not self.bstack1lll1llll1_opy_:
      return
    try:
      bstack1111l1lllll_opy_ = 0
      while not self.bstack11111l1llll_opy_ and bstack1111l1lllll_opy_ < self.bstack1111l11l1ll_opy_:
        if self.bstack1111l11l11l_opy_:
          self.logger.info(bstack1l1l1ll_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡹࡥࡵࡷࡳࠤ࡫ࡧࡩ࡭ࡧࡧࠦἤ"))
          return
        time.sleep(1)
        bstack1111l1lllll_opy_ += 1
      os.environ[bstack1l1l1ll_opy_ (u"ࠧࡑࡇࡕࡇ࡞ࡥࡂࡆࡕࡗࡣࡕࡒࡁࡕࡈࡒࡖࡒ࠭ἥ")] = str(self.bstack1111l1l1111_opy_())
      self.logger.info(bstack1l1l1ll_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡴࡧࡷࡹࡵࠦࡣࡰ࡯ࡳࡰࡪࡺࡥࡥࠤἦ"))
    except Exception as e:
      self.logger.error(bstack1l1l1ll_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡥࡵࡷࡳࠤࡵ࡫ࡲࡤࡻ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿࠥἧ").format(e))
  def bstack1111l1l1111_opy_(self):
    if self.bstack1ll111ll1l_opy_:
      return
    try:
      bstack11111lll11l_opy_ = [platform[bstack1l1l1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨἨ")].lower() for platform in self.config.get(bstack1l1l1ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧἩ"), [])]
      bstack1111l1l1lll_opy_ = sys.maxsize
      bstack1111l1111l1_opy_ = bstack1l1l1ll_opy_ (u"ࠬ࠭Ἢ")
      for browser in bstack11111lll11l_opy_:
        if browser in self.bstack11111lllll1_opy_:
          bstack1111ll1111l_opy_ = self.bstack11111lllll1_opy_[browser]
        if bstack1111ll1111l_opy_ < bstack1111l1l1lll_opy_:
          bstack1111l1l1lll_opy_ = bstack1111ll1111l_opy_
          bstack1111l1111l1_opy_ = browser
      return bstack1111l1111l1_opy_
    except Exception as e:
      self.logger.error(bstack1l1l1ll_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡩ࡭ࡳࡪࠠࡣࡧࡶࡸࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢἫ").format(e))
  @classmethod
  def bstack111l1111l_opy_(self):
    return os.getenv(bstack1l1l1ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡆࡔࡆ࡝ࠬἬ"), bstack1l1l1ll_opy_ (u"ࠨࡈࡤࡰࡸ࡫ࠧἭ")).lower()
  @classmethod
  def bstack11lll1l1_opy_(self):
    return os.getenv(bstack1l1l1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡈࡖࡈ࡟࡟ࡄࡃࡓࡘ࡚ࡘࡅࡠࡏࡒࡈࡊ࠭Ἦ"), bstack1l1l1ll_opy_ (u"ࠪࠫἯ"))
  @classmethod
  def bstack1l1l1l11ll1_opy_(cls, value):
    cls.bstack1l1lll11_opy_ = value
  @classmethod
  def bstack1111l1l1l1l_opy_(cls):
    return cls.bstack1l1lll11_opy_
  @classmethod
  def bstack1l1l1l11l11_opy_(cls, value):
    cls.percy_build_id = value
  @classmethod
  def bstack1111l11ll11_opy_(cls):
    return cls.percy_build_id