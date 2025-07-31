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
from bstack_utils.helper import bstack1l11lllll_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack1ll11l1l1_opy_ import bstack11lll11l1l_opy_
class bstack1l11l11l_opy_:
  working_dir = os.getcwd()
  bstack1ll111ll11_opy_ = False
  config = {}
  bstack11l11l1l1l1_opy_ = bstack1l11l11_opy_ (u"࠭ࠧẟ")
  binary_path = bstack1l11l11_opy_ (u"ࠧࠨẠ")
  bstack11111ll1l11_opy_ = bstack1l11l11_opy_ (u"ࠨࠩạ")
  bstack1l1l1l1l1_opy_ = False
  bstack1111l1111ll_opy_ = None
  bstack1111l111l1l_opy_ = {}
  bstack1111l1ll11l_opy_ = 300
  bstack1111l1lllll_opy_ = False
  logger = None
  bstack1111l11l1ll_opy_ = False
  bstack11l111l1l1_opy_ = False
  percy_build_id = None
  bstack11111ll1ll1_opy_ = bstack1l11l11_opy_ (u"ࠩࠪẢ")
  bstack1111ll1ll1l_opy_ = {
    bstack1l11l11_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪả") : 1,
    bstack1l11l11_opy_ (u"ࠫ࡫࡯ࡲࡦࡨࡲࡼࠬẤ") : 2,
    bstack1l11l11_opy_ (u"ࠬ࡫ࡤࡨࡧࠪấ") : 3,
    bstack1l11l11_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠭Ầ") : 4
  }
  def __init__(self) -> None: pass
  def bstack11111llllll_opy_(self):
    bstack1111l1l11ll_opy_ = bstack1l11l11_opy_ (u"ࠧࠨầ")
    bstack1111l1l1lll_opy_ = sys.platform
    bstack11111l1ll1l_opy_ = bstack1l11l11_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧẨ")
    if re.match(bstack1l11l11_opy_ (u"ࠤࡧࡥࡷࡽࡩ࡯ࡾࡰࡥࡨࠦ࡯ࡴࠤẩ"), bstack1111l1l1lll_opy_) != None:
      bstack1111l1l11ll_opy_ = bstack11l1ll1l1l1_opy_ + bstack1l11l11_opy_ (u"ࠥ࠳ࡵ࡫ࡲࡤࡻ࠰ࡳࡸࡾ࠮ࡻ࡫ࡳࠦẪ")
      self.bstack11111ll1ll1_opy_ = bstack1l11l11_opy_ (u"ࠫࡲࡧࡣࠨẫ")
    elif re.match(bstack1l11l11_opy_ (u"ࠧࡳࡳࡸ࡫ࡱࢀࡲࡹࡹࡴࡾࡰ࡭ࡳ࡭ࡷࡽࡥࡼ࡫ࡼ࡯࡮ࡽࡤࡦࡧࡼ࡯࡮ࡽࡹ࡬ࡲࡨ࡫ࡼࡦ࡯ࡦࢀࡼ࡯࡮࠴࠴ࠥẬ"), bstack1111l1l1lll_opy_) != None:
      bstack1111l1l11ll_opy_ = bstack11l1ll1l1l1_opy_ + bstack1l11l11_opy_ (u"ࠨ࠯ࡱࡧࡵࡧࡾ࠳ࡷࡪࡰ࠱ࡾ࡮ࡶࠢậ")
      bstack11111l1ll1l_opy_ = bstack1l11l11_opy_ (u"ࠢࡱࡧࡵࡧࡾ࠴ࡥࡹࡧࠥẮ")
      self.bstack11111ll1ll1_opy_ = bstack1l11l11_opy_ (u"ࠨࡹ࡬ࡲࠬắ")
    else:
      bstack1111l1l11ll_opy_ = bstack11l1ll1l1l1_opy_ + bstack1l11l11_opy_ (u"ࠤ࠲ࡴࡪࡸࡣࡺ࠯࡯࡭ࡳࡻࡸ࠯ࡼ࡬ࡴࠧẰ")
      self.bstack11111ll1ll1_opy_ = bstack1l11l11_opy_ (u"ࠪࡰ࡮ࡴࡵࡹࠩằ")
    return bstack1111l1l11ll_opy_, bstack11111l1ll1l_opy_
  def bstack11111ll111l_opy_(self):
    try:
      bstack1111l11111l_opy_ = [os.path.join(expanduser(bstack1l11l11_opy_ (u"ࠦࢃࠨẲ")), bstack1l11l11_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬẳ")), self.working_dir, tempfile.gettempdir()]
      for path in bstack1111l11111l_opy_:
        if(self.bstack1111ll1l1ll_opy_(path)):
          return path
      raise bstack1l11l11_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠥẴ")
    except Exception as e:
      self.logger.error(bstack1l11l11_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡪ࡮ࡴࡤࠡࡣࡹࡥ࡮ࡲࡡࡣ࡮ࡨࠤࡵࡧࡴࡩࠢࡩࡳࡷࠦࡰࡦࡴࡦࡽࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࠲ࠦࡻࡾࠤẵ").format(e))
  def bstack1111ll1l1ll_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack11111ll1lll_opy_(self, bstack11111lll111_opy_):
    return os.path.join(bstack11111lll111_opy_, self.bstack11l11l1l1l1_opy_ + bstack1l11l11_opy_ (u"ࠣ࠰ࡨࡸࡦ࡭ࠢẶ"))
  def bstack1111ll11111_opy_(self, bstack11111lll111_opy_, bstack11111ll11l1_opy_):
    if not bstack11111ll11l1_opy_: return
    try:
      bstack11111l1ll11_opy_ = self.bstack11111ll1lll_opy_(bstack11111lll111_opy_)
      with open(bstack11111l1ll11_opy_, bstack1l11l11_opy_ (u"ࠤࡺࠦặ")) as f:
        f.write(bstack11111ll11l1_opy_)
        self.logger.debug(bstack1l11l11_opy_ (u"ࠥࡗࡦࡼࡥࡥࠢࡱࡩࡼࠦࡅࡕࡣࡪࠤ࡫ࡵࡲࠡࡲࡨࡶࡨࡿࠢẸ"))
    except Exception as e:
      self.logger.error(bstack1l11l11_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡣࡹࡩࠥࡺࡨࡦࠢࡨࡸࡦ࡭ࠬࠡࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠦẹ").format(e))
  def bstack1111l11lll1_opy_(self, bstack11111lll111_opy_):
    try:
      bstack11111l1ll11_opy_ = self.bstack11111ll1lll_opy_(bstack11111lll111_opy_)
      if os.path.exists(bstack11111l1ll11_opy_):
        with open(bstack11111l1ll11_opy_, bstack1l11l11_opy_ (u"ࠧࡸࠢẺ")) as f:
          bstack11111ll11l1_opy_ = f.read().strip()
          return bstack11111ll11l1_opy_ if bstack11111ll11l1_opy_ else None
    except Exception as e:
      self.logger.error(bstack1l11l11_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦ࡬ࡰࡣࡧ࡭ࡳ࡭ࠠࡆࡖࡤ࡫࠱ࠦࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠤẻ").format(e))
  def bstack1111ll11ll1_opy_(self, bstack11111lll111_opy_, bstack1111l1l11ll_opy_):
    bstack1111ll1ll11_opy_ = self.bstack1111l11lll1_opy_(bstack11111lll111_opy_)
    if bstack1111ll1ll11_opy_:
      try:
        bstack1111l1l1l11_opy_ = self.bstack1111ll111l1_opy_(bstack1111ll1ll11_opy_, bstack1111l1l11ll_opy_)
        if not bstack1111l1l1l11_opy_:
          self.logger.debug(bstack1l11l11_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠦࡩࡴࠢࡸࡴࠥࡺ࡯ࠡࡦࡤࡸࡪࠦࠨࡆࡖࡤ࡫ࠥࡻ࡮ࡤࡪࡤࡲ࡬࡫ࡤࠪࠤẼ"))
          return True
        self.logger.debug(bstack1l11l11_opy_ (u"ࠣࡐࡨࡻࠥࡖࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥࡧࡶࡢ࡫࡯ࡥࡧࡲࡥ࠭ࠢࡧࡳࡼࡴ࡬ࡰࡣࡧ࡭ࡳ࡭ࠠࡶࡲࡧࡥࡹ࡫ࠢẽ"))
        return False
      except Exception as e:
        self.logger.warn(bstack1l11l11_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡩࡨࡦࡥ࡮ࠤ࡫ࡵࡲࠡࡤ࡬ࡲࡦࡸࡹࠡࡷࡳࡨࡦࡺࡥࡴ࠮ࠣࡹࡸ࡯࡮ࡨࠢࡨࡼ࡮ࡹࡴࡪࡰࡪࠤࡧ࡯࡮ࡢࡴࡼ࠾ࠥࢁࡽࠣẾ").format(e))
    return False
  def bstack1111ll111l1_opy_(self, bstack1111ll1ll11_opy_, bstack1111l1l11ll_opy_):
    try:
      headers = {
        bstack1l11l11_opy_ (u"ࠥࡍ࡫࠳ࡎࡰࡰࡨ࠱ࡒࡧࡴࡤࡪࠥế"): bstack1111ll1ll11_opy_
      }
      response = bstack1l11lllll_opy_(bstack1l11l11_opy_ (u"ࠫࡌࡋࡔࠨỀ"), bstack1111l1l11ll_opy_, {}, {bstack1l11l11_opy_ (u"ࠧ࡮ࡥࡢࡦࡨࡶࡸࠨề"): headers})
      if response.status_code == 304:
        return False
      return True
    except Exception as e:
      raise(bstack1l11l11_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡩࡨࡦࡥ࡮࡭ࡳ࡭ࠠࡧࡱࡵࠤࡕ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠣࡹࡵࡪࡡࡵࡧࡶ࠾ࠥࢁࡽࠣỂ").format(e))
  @measure(event_name=EVENTS.bstack11l1ll11l1l_opy_, stage=STAGE.bstack1lll11l1_opy_)
  def bstack1111l1lll11_opy_(self, bstack1111l1l11ll_opy_, bstack11111l1ll1l_opy_):
    try:
      bstack1111ll11l1l_opy_ = self.bstack11111ll111l_opy_()
      bstack11111llll11_opy_ = os.path.join(bstack1111ll11l1l_opy_, bstack1l11l11_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠴ࡺࡪࡲࠪể"))
      bstack1111ll11lll_opy_ = os.path.join(bstack1111ll11l1l_opy_, bstack11111l1ll1l_opy_)
      if self.bstack1111ll11ll1_opy_(bstack1111ll11l1l_opy_, bstack1111l1l11ll_opy_): # if bstack11111llll1l_opy_, bstack1l1l111l1ll_opy_ bstack11111ll11l1_opy_ is bstack1111l11l111_opy_ to bstack11l11lllll1_opy_ version available (response 304)
        if os.path.exists(bstack1111ll11lll_opy_):
          self.logger.info(bstack1l11l11_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠠࡧࡱࡸࡲࡩࠦࡩ࡯ࠢࡾࢁ࠱ࠦࡳ࡬࡫ࡳࡴ࡮ࡴࡧࠡࡦࡲࡻࡳࡲ࡯ࡢࡦࠥỄ").format(bstack1111ll11lll_opy_))
          return bstack1111ll11lll_opy_
        if os.path.exists(bstack11111llll11_opy_):
          self.logger.info(bstack1l11l11_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡼ࡬ࡴࠥ࡬࡯ࡶࡰࡧࠤ࡮ࡴࠠࡼࡿ࠯ࠤࡺࡴࡺࡪࡲࡳ࡭ࡳ࡭ࠢễ").format(bstack11111llll11_opy_))
          return self.bstack1111l111ll1_opy_(bstack11111llll11_opy_, bstack11111l1ll1l_opy_)
      self.logger.info(bstack1l11l11_opy_ (u"ࠥࡈࡴࡽ࡮࡭ࡱࡤࡨ࡮ࡴࡧࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠠࡧࡴࡲࡱࠥࢁࡽࠣỆ").format(bstack1111l1l11ll_opy_))
      response = bstack1l11lllll_opy_(bstack1l11l11_opy_ (u"ࠫࡌࡋࡔࠨệ"), bstack1111l1l11ll_opy_, {}, {})
      if response.status_code == 200:
        bstack1111l111lll_opy_ = response.headers.get(bstack1l11l11_opy_ (u"ࠧࡋࡔࡢࡩࠥỈ"), bstack1l11l11_opy_ (u"ࠨࠢỉ"))
        if bstack1111l111lll_opy_:
          self.bstack1111ll11111_opy_(bstack1111ll11l1l_opy_, bstack1111l111lll_opy_)
        with open(bstack11111llll11_opy_, bstack1l11l11_opy_ (u"ࠧࡸࡤࠪỊ")) as file:
          file.write(response.content)
        self.logger.info(bstack1l11l11_opy_ (u"ࠣࡆࡲࡻࡳࡲ࡯ࡢࡦࡨࡨࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠤࡦࡴࡤࠡࡵࡤࡺࡪࡪࠠࡢࡶࠣࡿࢂࠨị").format(bstack11111llll11_opy_))
        return self.bstack1111l111ll1_opy_(bstack11111llll11_opy_, bstack11111l1ll1l_opy_)
      else:
        raise(bstack1l11l11_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠠࡵࡪࡨࠤ࡫࡯࡬ࡦ࠰ࠣࡗࡹࡧࡴࡶࡵࠣࡧࡴࡪࡥ࠻ࠢࡾࢁࠧỌ").format(response.status_code))
    except Exception as e:
      self.logger.error(bstack1l11l11_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡤࡰࡹࡱࡰࡴࡧࡤࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿ࠺ࠡࡽࢀࠦọ").format(e))
  def bstack1111l1l111l_opy_(self, bstack1111l1l11ll_opy_, bstack11111l1ll1l_opy_):
    try:
      retry = 2
      bstack1111ll11lll_opy_ = None
      bstack1111l11ll11_opy_ = False
      while retry > 0:
        bstack1111ll11lll_opy_ = self.bstack1111l1lll11_opy_(bstack1111l1l11ll_opy_, bstack11111l1ll1l_opy_)
        bstack1111l11ll11_opy_ = self.bstack11111l1lll1_opy_(bstack1111l1l11ll_opy_, bstack11111l1ll1l_opy_, bstack1111ll11lll_opy_)
        if bstack1111l11ll11_opy_:
          break
        retry -= 1
      return bstack1111ll11lll_opy_, bstack1111l11ll11_opy_
    except Exception as e:
      self.logger.error(bstack1l11l11_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡨࡧࡷࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠣࡴࡦࡺࡨࠣỎ").format(e))
    return bstack1111ll11lll_opy_, False
  def bstack11111l1lll1_opy_(self, bstack1111l1l11ll_opy_, bstack11111l1ll1l_opy_, bstack1111ll11lll_opy_, bstack1111l1l1l1l_opy_ = 0):
    if bstack1111l1l1l1l_opy_ > 1:
      return False
    if bstack1111ll11lll_opy_ == None or os.path.exists(bstack1111ll11lll_opy_) == False:
      self.logger.warn(bstack1l11l11_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡵࡧࡴࡩࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨ࠱ࠦࡲࡦࡶࡵࡽ࡮ࡴࡧࠡࡦࡲࡻࡳࡲ࡯ࡢࡦࠥỏ"))
      return False
    bstack1111l1l11l1_opy_ = bstack1l11l11_opy_ (u"ࡸࠢ࡟࠰࠭ࡄࡵ࡫ࡲࡤࡻ࠲ࡧࡱ࡯ࠠ࡝ࡦ࠮ࡠ࠳ࡢࡤࠬ࡞࠱ࡠࡩ࠱ࠢỐ")
    command = bstack1l11l11_opy_ (u"ࠧࡼࡿࠣ࠱࠲ࡼࡥࡳࡵ࡬ࡳࡳ࠭ố").format(bstack1111ll11lll_opy_)
    bstack1111l11ll1l_opy_ = subprocess.check_output(command, shell=True, text=True)
    if re.match(bstack1111l1l11l1_opy_, bstack1111l11ll1l_opy_) != None:
      return True
    else:
      self.logger.error(bstack1l11l11_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࡥ࡫ࡩࡨࡱࠠࡧࡣ࡬ࡰࡪࡪࠢỒ"))
      return False
  def bstack1111l111ll1_opy_(self, bstack11111llll11_opy_, bstack11111l1ll1l_opy_):
    try:
      working_dir = os.path.dirname(bstack11111llll11_opy_)
      shutil.unpack_archive(bstack11111llll11_opy_, working_dir)
      bstack1111ll11lll_opy_ = os.path.join(working_dir, bstack11111l1ll1l_opy_)
      os.chmod(bstack1111ll11lll_opy_, 0o755)
      return bstack1111ll11lll_opy_
    except Exception as e:
      self.logger.error(bstack1l11l11_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡻ࡮ࡻ࡫ࡳࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠥồ"))
  def bstack11111lll1ll_opy_(self):
    try:
      bstack1111ll1l111_opy_ = self.config.get(bstack1l11l11_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩỔ"))
      bstack11111lll1ll_opy_ = bstack1111ll1l111_opy_ or (bstack1111ll1l111_opy_ is None and self.bstack1ll111ll11_opy_)
      if not bstack11111lll1ll_opy_ or self.config.get(bstack1l11l11_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧổ"), None) not in bstack11l1ll1l11l_opy_:
        return False
      self.bstack1l1l1l1l1_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack1l11l11_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡦࡨࡸࡪࡩࡴࠡࡲࡨࡶࡨࡿࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢỖ").format(e))
  def bstack1111l1lll1l_opy_(self):
    try:
      bstack1111l1lll1l_opy_ = self.percy_capture_mode
      return bstack1111l1lll1l_opy_
    except Exception as e:
      self.logger.error(bstack1l11l11_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡧࡩࡹ࡫ࡣࡵࠢࡳࡩࡷࡩࡹࠡࡥࡤࡴࡹࡻࡲࡦࠢࡰࡳࡩ࡫ࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢỗ").format(e))
  def init(self, bstack1ll111ll11_opy_, config, logger):
    self.bstack1ll111ll11_opy_ = bstack1ll111ll11_opy_
    self.config = config
    self.logger = logger
    if not self.bstack11111lll1ll_opy_():
      return
    self.bstack1111l111l1l_opy_ = config.get(bstack1l11l11_opy_ (u"ࠧࡱࡧࡵࡧࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭Ộ"), {})
    self.percy_capture_mode = config.get(bstack1l11l11_opy_ (u"ࠨࡲࡨࡶࡨࡿࡃࡢࡲࡷࡹࡷ࡫ࡍࡰࡦࡨࠫộ"))
    try:
      bstack1111l1l11ll_opy_, bstack11111l1ll1l_opy_ = self.bstack11111llllll_opy_()
      self.bstack11l11l1l1l1_opy_ = bstack11111l1ll1l_opy_
      bstack1111ll11lll_opy_, bstack1111l11ll11_opy_ = self.bstack1111l1l111l_opy_(bstack1111l1l11ll_opy_, bstack11111l1ll1l_opy_)
      if bstack1111l11ll11_opy_:
        self.binary_path = bstack1111ll11lll_opy_
        thread = Thread(target=self.bstack1111l11l1l1_opy_)
        thread.start()
      else:
        self.bstack1111l11l1ll_opy_ = True
        self.logger.error(bstack1l11l11_opy_ (u"ࠤࡌࡲࡻࡧ࡬ࡪࡦࠣࡴࡪࡸࡣࡺࠢࡳࡥࡹ࡮ࠠࡧࡱࡸࡲࡩࠦ࠭ࠡࡽࢀ࠰࡛ࠥ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡑࡧࡵࡧࡾࠨỚ").format(bstack1111ll11lll_opy_))
    except Exception as e:
      self.logger.error(bstack1l11l11_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡶࡥࡳࡥࡼ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦớ").format(e))
  def bstack11111lllll1_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack1l11l11_opy_ (u"ࠫࡱࡵࡧࠨỜ"), bstack1l11l11_opy_ (u"ࠬࡶࡥࡳࡥࡼ࠲ࡱࡵࡧࠨờ"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack1l11l11_opy_ (u"ࠨࡐࡶࡵ࡫࡭ࡳ࡭ࠠࡱࡧࡵࡧࡾࠦ࡬ࡰࡩࡶࠤࡦࡺࠠࡼࡿࠥỞ").format(logfile))
      self.bstack11111ll1l11_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack1l11l11_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡪࡺࠠࡱࡧࡵࡧࡾࠦ࡬ࡰࡩࠣࡴࡦࡺࡨ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣở").format(e))
  @measure(event_name=EVENTS.bstack11l1ll111l1_opy_, stage=STAGE.bstack1lll11l1_opy_)
  def bstack1111l11l1l1_opy_(self):
    bstack1111ll1l11l_opy_ = self.bstack1111l11l11l_opy_()
    if bstack1111ll1l11l_opy_ == None:
      self.bstack1111l11l1ll_opy_ = True
      self.logger.error(bstack1l11l11_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡵࡱ࡮ࡩࡳࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥ࠮ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡶࡥࡳࡥࡼࠦỠ"))
      return False
    command_args = [bstack1l11l11_opy_ (u"ࠤࡤࡴࡵࡀࡥࡹࡧࡦ࠾ࡸࡺࡡࡳࡶࠥỡ") if self.bstack1ll111ll11_opy_ else bstack1l11l11_opy_ (u"ࠪࡩࡽ࡫ࡣ࠻ࡵࡷࡥࡷࡺࠧỢ")]
    bstack111l1lll11l_opy_ = self.bstack1111l1ll1ll_opy_()
    if bstack111l1lll11l_opy_ != None:
      command_args.append(bstack1l11l11_opy_ (u"ࠦ࠲ࡩࠠࡼࡿࠥợ").format(bstack111l1lll11l_opy_))
    env = os.environ.copy()
    env[bstack1l11l11_opy_ (u"ࠧࡖࡅࡓࡅ࡜ࡣ࡙ࡕࡋࡆࡐࠥỤ")] = bstack1111ll1l11l_opy_
    env[bstack1l11l11_opy_ (u"ࠨࡔࡉࡡࡅ࡙ࡎࡒࡄࡠࡗࡘࡍࡉࠨụ")] = os.environ.get(bstack1l11l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬỦ"), bstack1l11l11_opy_ (u"ࠨࠩủ"))
    bstack11111l1llll_opy_ = [self.binary_path]
    self.bstack11111lllll1_opy_()
    self.bstack1111l1111ll_opy_ = self.bstack11111ll1111_opy_(bstack11111l1llll_opy_ + command_args, env)
    self.logger.debug(bstack1l11l11_opy_ (u"ࠤࡖࡸࡦࡸࡴࡪࡰࡪࠤࡍ࡫ࡡ࡭ࡶ࡫ࠤࡈ࡮ࡥࡤ࡭ࠥỨ"))
    bstack1111l1l1l1l_opy_ = 0
    while self.bstack1111l1111ll_opy_.poll() == None:
      bstack11111lll1l1_opy_ = self.bstack1111ll111ll_opy_()
      if bstack11111lll1l1_opy_:
        self.logger.debug(bstack1l11l11_opy_ (u"ࠥࡌࡪࡧ࡬ࡵࡪࠣࡇ࡭࡫ࡣ࡬ࠢࡶࡹࡨࡩࡥࡴࡵࡩࡹࡱࠨứ"))
        self.bstack1111l1lllll_opy_ = True
        return True
      bstack1111l1l1l1l_opy_ += 1
      self.logger.debug(bstack1l11l11_opy_ (u"ࠦࡍ࡫ࡡ࡭ࡶ࡫ࠤࡈ࡮ࡥࡤ࡭ࠣࡖࡪࡺࡲࡺࠢ࠰ࠤࢀࢃࠢỪ").format(bstack1111l1l1l1l_opy_))
      time.sleep(2)
    self.logger.error(bstack1l11l11_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡱࡧࡵࡧࡾ࠲ࠠࡉࡧࡤࡰࡹ࡮ࠠࡄࡪࡨࡧࡰࠦࡆࡢ࡫࡯ࡩࡩࠦࡡࡧࡶࡨࡶࠥࢁࡽࠡࡣࡷࡸࡪࡳࡰࡵࡵࠥừ").format(bstack1111l1l1l1l_opy_))
    self.bstack1111l11l1ll_opy_ = True
    return False
  def bstack1111ll111ll_opy_(self, bstack1111l1l1l1l_opy_ = 0):
    if bstack1111l1l1l1l_opy_ > 10:
      return False
    try:
      bstack1111l1llll1_opy_ = os.environ.get(bstack1l11l11_opy_ (u"࠭ࡐࡆࡔࡆ࡝ࡤ࡙ࡅࡓࡘࡈࡖࡤࡇࡄࡅࡔࡈࡗࡘ࠭Ử"), bstack1l11l11_opy_ (u"ࠧࡩࡶࡷࡴ࠿࠵࠯࡭ࡱࡦࡥࡱ࡮࡯ࡴࡶ࠽࠹࠸࠹࠸ࠨử"))
      bstack1111l1ll111_opy_ = bstack1111l1llll1_opy_ + bstack11l1llll111_opy_
      response = requests.get(bstack1111l1ll111_opy_)
      data = response.json()
      self.percy_build_id = data.get(bstack1l11l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࠧỮ"), {}).get(bstack1l11l11_opy_ (u"ࠩ࡬ࡨࠬữ"), None)
      return True
    except:
      self.logger.debug(bstack1l11l11_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡲࡧࡨࡻࡲࡳࡧࡧࠤࡼ࡮ࡩ࡭ࡧࠣࡴࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡩࡧࡤࡰࡹ࡮ࠠࡤࡪࡨࡧࡰࠦࡲࡦࡵࡳࡳࡳࡹࡥࠣỰ"))
      return False
  def bstack1111l11l11l_opy_(self):
    bstack1111l1111l1_opy_ = bstack1l11l11_opy_ (u"ࠫࡦࡶࡰࠨự") if self.bstack1ll111ll11_opy_ else bstack1l11l11_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧỲ")
    bstack1111l1l1111_opy_ = bstack1l11l11_opy_ (u"ࠨࡵ࡯ࡦࡨࡪ࡮ࡴࡥࡥࠤỳ") if self.config.get(bstack1l11l11_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭Ỵ")) is None else True
    bstack11ll11l1l1l_opy_ = bstack1l11l11_opy_ (u"ࠣࡣࡳ࡭࠴ࡧࡰࡱࡡࡳࡩࡷࡩࡹ࠰ࡩࡨࡸࡤࡶࡲࡰ࡬ࡨࡧࡹࡥࡴࡰ࡭ࡨࡲࡄࡴࡡ࡮ࡧࡀࡿࢂࠬࡴࡺࡲࡨࡁࢀࢃࠦࡱࡧࡵࡧࡾࡃࡻࡾࠤỵ").format(self.config[bstack1l11l11_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧỶ")], bstack1111l1111l1_opy_, bstack1111l1l1111_opy_)
    if self.percy_capture_mode:
      bstack11ll11l1l1l_opy_ += bstack1l11l11_opy_ (u"ࠥࠪࡵ࡫ࡲࡤࡻࡢࡧࡦࡶࡴࡶࡴࡨࡣࡲࡵࡤࡦ࠿ࡾࢁࠧỷ").format(self.percy_capture_mode)
    uri = bstack11lll11l1l_opy_(bstack11ll11l1l1l_opy_)
    try:
      response = bstack1l11lllll_opy_(bstack1l11l11_opy_ (u"ࠫࡌࡋࡔࠨỸ"), uri, {}, {bstack1l11l11_opy_ (u"ࠬࡧࡵࡵࡪࠪỹ"): (self.config[bstack1l11l11_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨỺ")], self.config[bstack1l11l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪỻ")])})
      if response.status_code == 200:
        data = response.json()
        self.bstack1l1l1l1l1_opy_ = data.get(bstack1l11l11_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩỼ"))
        self.percy_capture_mode = data.get(bstack1l11l11_opy_ (u"ࠩࡳࡩࡷࡩࡹࡠࡥࡤࡴࡹࡻࡲࡦࡡࡰࡳࡩ࡫ࠧỽ"))
        os.environ[bstack1l11l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡉࡗࡉ࡙ࠨỾ")] = str(self.bstack1l1l1l1l1_opy_)
        os.environ[bstack1l11l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡊࡘࡃ࡚ࡡࡆࡅࡕ࡚ࡕࡓࡇࡢࡑࡔࡊࡅࠨỿ")] = str(self.percy_capture_mode)
        if bstack1111l1l1111_opy_ == bstack1l11l11_opy_ (u"ࠧࡻ࡮ࡥࡧࡩ࡭ࡳ࡫ࡤࠣἀ") and str(self.bstack1l1l1l1l1_opy_).lower() == bstack1l11l11_opy_ (u"ࠨࡴࡳࡷࡨࠦἁ"):
          self.bstack11l111l1l1_opy_ = True
        if bstack1l11l11_opy_ (u"ࠢࡵࡱ࡮ࡩࡳࠨἂ") in data:
          return data[bstack1l11l11_opy_ (u"ࠣࡶࡲ࡯ࡪࡴࠢἃ")]
        else:
          raise bstack1l11l11_opy_ (u"ࠩࡗࡳࡰ࡫࡮ࠡࡐࡲࡸࠥࡌ࡯ࡶࡰࡧࠤ࠲ࠦࡻࡾࠩἄ").format(data)
      else:
        raise bstack1l11l11_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡶࡥࡳࡥࡼࠤࡹࡵ࡫ࡦࡰ࠯ࠤࡗ࡫ࡳࡱࡱࡱࡷࡪࠦࡳࡵࡣࡷࡹࡸࠦ࠭ࠡࡽࢀ࠰ࠥࡘࡥࡴࡲࡲࡲࡸ࡫ࠠࡃࡱࡧࡽࠥ࠳ࠠࡼࡿࠥἅ").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack1l11l11_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥࡶࡥࡳࡥࡼࠤࡵࡸ࡯࡫ࡧࡦࡸࠧἆ").format(e))
  def bstack1111l1ll1ll_opy_(self):
    bstack1111ll11l11_opy_ = os.path.join(tempfile.gettempdir(), bstack1l11l11_opy_ (u"ࠧࡶࡥࡳࡥࡼࡇࡴࡴࡦࡪࡩ࠱࡮ࡸࡵ࡮ࠣἇ"))
    try:
      if bstack1l11l11_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧἈ") not in self.bstack1111l111l1l_opy_:
        self.bstack1111l111l1l_opy_[bstack1l11l11_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨἉ")] = 2
      with open(bstack1111ll11l11_opy_, bstack1l11l11_opy_ (u"ࠨࡹࠪἊ")) as fp:
        json.dump(self.bstack1111l111l1l_opy_, fp)
      return bstack1111ll11l11_opy_
    except Exception as e:
      self.logger.error(bstack1l11l11_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡩࡲࡦࡣࡷࡩࠥࡶࡥࡳࡥࡼࠤࡨࡵ࡮ࡧ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤἋ").format(e))
  def bstack11111ll1111_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack11111ll1ll1_opy_ == bstack1l11l11_opy_ (u"ࠪࡻ࡮ࡴࠧἌ"):
        bstack11111ll11ll_opy_ = [bstack1l11l11_opy_ (u"ࠫࡨࡳࡤ࠯ࡧࡻࡩࠬἍ"), bstack1l11l11_opy_ (u"ࠬ࠵ࡣࠨἎ")]
        cmd = bstack11111ll11ll_opy_ + cmd
      cmd = bstack1l11l11_opy_ (u"࠭ࠠࠨἏ").join(cmd)
      self.logger.debug(bstack1l11l11_opy_ (u"ࠢࡓࡷࡱࡲ࡮ࡴࡧࠡࡽࢀࠦἐ").format(cmd))
      with open(self.bstack11111ll1l11_opy_, bstack1l11l11_opy_ (u"ࠣࡣࠥἑ")) as bstack1111l11llll_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack1111l11llll_opy_, text=True, stderr=bstack1111l11llll_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack1111l11l1ll_opy_ = True
      self.logger.error(bstack1l11l11_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡵ࡫ࡲࡤࡻࠣࡻ࡮ࡺࡨࠡࡥࡰࡨࠥ࠳ࠠࡼࡿ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴ࠺ࠡࡽࢀࠦἒ").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack1111l1lllll_opy_:
        self.logger.info(bstack1l11l11_opy_ (u"ࠥࡗࡹࡵࡰࡱ࡫ࡱ࡫ࠥࡖࡥࡳࡥࡼࠦἓ"))
        cmd = [self.binary_path, bstack1l11l11_opy_ (u"ࠦࡪࡾࡥࡤ࠼ࡶࡸࡴࡶࠢἔ")]
        self.bstack11111ll1111_opy_(cmd)
        self.bstack1111l1lllll_opy_ = False
    except Exception as e:
      self.logger.error(bstack1l11l11_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡷࡳࡵࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡸ࡫ࡷ࡬ࠥࡩ࡯࡮࡯ࡤࡲࡩࠦ࠭ࠡࡽࢀ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮࠻ࠢࡾࢁࠧἕ").format(cmd, e))
  def bstack1l1l111l11_opy_(self):
    if not self.bstack1l1l1l1l1_opy_:
      return
    try:
      bstack11111ll1l1l_opy_ = 0
      while not self.bstack1111l1lllll_opy_ and bstack11111ll1l1l_opy_ < self.bstack1111l1ll11l_opy_:
        if self.bstack1111l11l1ll_opy_:
          self.logger.info(bstack1l11l11_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡹࡥࡵࡷࡳࠤ࡫ࡧࡩ࡭ࡧࡧࠦ἖"))
          return
        time.sleep(1)
        bstack11111ll1l1l_opy_ += 1
      os.environ[bstack1l11l11_opy_ (u"ࠧࡑࡇࡕࡇ࡞ࡥࡂࡆࡕࡗࡣࡕࡒࡁࡕࡈࡒࡖࡒ࠭἗")] = str(self.bstack1111l111l11_opy_())
      self.logger.info(bstack1l11l11_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡴࡧࡷࡹࡵࠦࡣࡰ࡯ࡳࡰࡪࡺࡥࡥࠤἘ"))
    except Exception as e:
      self.logger.error(bstack1l11l11_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡥࡵࡷࡳࠤࡵ࡫ࡲࡤࡻ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿࠥἙ").format(e))
  def bstack1111l111l11_opy_(self):
    if self.bstack1ll111ll11_opy_:
      return
    try:
      bstack11111lll11l_opy_ = [platform[bstack1l11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨἚ")].lower() for platform in self.config.get(bstack1l11l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧἛ"), [])]
      bstack1111ll1111l_opy_ = sys.maxsize
      bstack1111l1l1ll1_opy_ = bstack1l11l11_opy_ (u"ࠬ࠭Ἔ")
      for browser in bstack11111lll11l_opy_:
        if browser in self.bstack1111ll1ll1l_opy_:
          bstack1111ll1l1l1_opy_ = self.bstack1111ll1ll1l_opy_[browser]
        if bstack1111ll1l1l1_opy_ < bstack1111ll1111l_opy_:
          bstack1111ll1111l_opy_ = bstack1111ll1l1l1_opy_
          bstack1111l1l1ll1_opy_ = browser
      return bstack1111l1l1ll1_opy_
    except Exception as e:
      self.logger.error(bstack1l11l11_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡩ࡭ࡳࡪࠠࡣࡧࡶࡸࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢἝ").format(e))
  @classmethod
  def bstack1l1lll1ll_opy_(self):
    return os.getenv(bstack1l11l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡆࡔࡆ࡝ࠬ἞"), bstack1l11l11_opy_ (u"ࠨࡈࡤࡰࡸ࡫ࠧ἟")).lower()
  @classmethod
  def bstack1l1ll111l_opy_(self):
    return os.getenv(bstack1l11l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡈࡖࡈ࡟࡟ࡄࡃࡓࡘ࡚ࡘࡅࡠࡏࡒࡈࡊ࠭ἠ"), bstack1l11l11_opy_ (u"ࠪࠫἡ"))
  @classmethod
  def bstack1l1l1l11111_opy_(cls, value):
    cls.bstack11l111l1l1_opy_ = value
  @classmethod
  def bstack1111l1ll1l1_opy_(cls):
    return cls.bstack11l111l1l1_opy_
  @classmethod
  def bstack1l1l1l111l1_opy_(cls, value):
    cls.percy_build_id = value
  @classmethod
  def bstack1111l111111_opy_(cls):
    return cls.percy_build_id