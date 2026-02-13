# coding: UTF-8
import sys
bstack111ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack11l11_opy_ (bstack1lll1ll_opy_):
    global bstack11l11l_opy_
    bstack11111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1l11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack11111l1_opy_ = bstack11111l_opy_ % len (bstack1l11_opy_)
    bstack1lll1l_opy_ = bstack1l11_opy_ [:bstack11111l1_opy_] + bstack1l11_opy_ [bstack11111l1_opy_:]
    if bstack111ll11_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    return eval (bstack1l1l1_opy_)
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
from bstack_utils.helper import bstack1l11l11ll1_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack111ll1111l_opy_ import bstack11l111ll1_opy_
class bstack11l11ll11_opy_:
  working_dir = os.getcwd()
  bstack11l1l1ll1_opy_ = False
  config = {}
  bstack1111ll1l11l_opy_ = bstack11l11_opy_ (u"࠭ࠧℜ")
  binary_path = bstack11l11_opy_ (u"ࠧࠨℝ")
  bstack1llll111ll11_opy_ = bstack11l11_opy_ (u"ࠨࠩ℞")
  bstack1lll11ll_opy_ = False
  bstack1llll111l1ll_opy_ = None
  bstack1llll1l1l11l_opy_ = {}
  bstack1lll1llll1ll_opy_ = 300
  bstack1llll1l111ll_opy_ = False
  logger = None
  bstack1llll1111111_opy_ = False
  bstack111111ll_opy_ = False
  percy_build_id = None
  bstack1llll11111l1_opy_ = bstack11l11_opy_ (u"ࠩࠪ℟")
  bstack1llll11lll11_opy_ = {
    bstack11l11_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪ℠") : 1,
    bstack11l11_opy_ (u"ࠫ࡫࡯ࡲࡦࡨࡲࡼࠬ℡") : 2,
    bstack11l11_opy_ (u"ࠬ࡫ࡤࡨࡧࠪ™") : 3,
    bstack11l11_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠭℣") : 4
  }
  def __init__(self) -> None: pass
  def bstack1llll11l1l11_opy_(self):
    bstack1llll11l11ll_opy_ = bstack11l11_opy_ (u"ࠧࠨℤ")
    bstack1llll1l11l11_opy_ = sys.platform
    bstack1llll1111lll_opy_ = bstack11l11_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧ℥")
    if re.match(bstack11l11_opy_ (u"ࠤࡧࡥࡷࡽࡩ࡯ࡾࡰࡥࡨࠦ࡯ࡴࠤΩ"), bstack1llll1l11l11_opy_) != None:
      bstack1llll11l11ll_opy_ = bstack111lll11l1l_opy_ + bstack11l11_opy_ (u"ࠥ࠳ࡵ࡫ࡲࡤࡻ࠰ࡳࡸࡾ࠮ࡻ࡫ࡳࠦ℧")
      self.bstack1llll11111l1_opy_ = bstack11l11_opy_ (u"ࠫࡲࡧࡣࠨℨ")
    elif re.match(bstack11l11_opy_ (u"ࠧࡳࡳࡸ࡫ࡱࢀࡲࡹࡹࡴࡾࡰ࡭ࡳ࡭ࡷࡽࡥࡼ࡫ࡼ࡯࡮ࡽࡤࡦࡧࡼ࡯࡮ࡽࡹ࡬ࡲࡨ࡫ࡼࡦ࡯ࡦࢀࡼ࡯࡮࠴࠴ࠥ℩"), bstack1llll1l11l11_opy_) != None:
      bstack1llll11l11ll_opy_ = bstack111lll11l1l_opy_ + bstack11l11_opy_ (u"ࠨ࠯ࡱࡧࡵࡧࡾ࠳ࡷࡪࡰ࠱ࡾ࡮ࡶࠢK")
      bstack1llll1111lll_opy_ = bstack11l11_opy_ (u"ࠢࡱࡧࡵࡧࡾ࠴ࡥࡹࡧࠥÅ")
      self.bstack1llll11111l1_opy_ = bstack11l11_opy_ (u"ࠨࡹ࡬ࡲࠬℬ")
    else:
      bstack1llll11l11ll_opy_ = bstack111lll11l1l_opy_ + bstack11l11_opy_ (u"ࠤ࠲ࡴࡪࡸࡣࡺ࠯࡯࡭ࡳࡻࡸ࠯ࡼ࡬ࡴࠧℭ")
      self.bstack1llll11111l1_opy_ = bstack11l11_opy_ (u"ࠪࡰ࡮ࡴࡵࡹࠩ℮")
    return bstack1llll11l11ll_opy_, bstack1llll1111lll_opy_
  def bstack1llll1l1ll11_opy_(self):
    try:
      bstack1llll11ll11l_opy_ = [os.path.join(expanduser(bstack11l11_opy_ (u"ࠦࢃࠨℯ")), bstack11l11_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬℰ")), self.working_dir, tempfile.gettempdir()]
      for path in bstack1llll11ll11l_opy_:
        if(self.bstack1llll11l1lll_opy_(path)):
          return path
      raise bstack11l11_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠥℱ")
    except Exception as e:
      self.logger.error(bstack11l11_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡪ࡮ࡴࡤࠡࡣࡹࡥ࡮ࡲࡡࡣ࡮ࡨࠤࡵࡧࡴࡩࠢࡩࡳࡷࠦࡰࡦࡴࡦࡽࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࠲ࠦࡻࡾࠤℲ").format(e))
  def bstack1llll11l1lll_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack1lll1lllllll_opy_(self, bstack1llll11lll1l_opy_):
    return os.path.join(bstack1llll11lll1l_opy_, self.bstack1111ll1l11l_opy_ + bstack11l11_opy_ (u"ࠣ࠰ࡨࡸࡦ࡭ࠢℳ"))
  def bstack1llll111111l_opy_(self, bstack1llll11lll1l_opy_, bstack1llll11ll1l1_opy_):
    if not bstack1llll11ll1l1_opy_: return
    try:
      bstack1llll111l1l1_opy_ = self.bstack1lll1lllllll_opy_(bstack1llll11lll1l_opy_)
      with open(bstack1llll111l1l1_opy_, bstack11l11_opy_ (u"ࠤࡺࠦℴ")) as f:
        f.write(bstack1llll11ll1l1_opy_)
        self.logger.debug(bstack11l11_opy_ (u"ࠥࡗࡦࡼࡥࡥࠢࡱࡩࡼࠦࡅࡕࡣࡪࠤ࡫ࡵࡲࠡࡲࡨࡶࡨࡿࠢℵ"))
    except Exception as e:
      self.logger.error(bstack11l11_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡣࡹࡩࠥࡺࡨࡦࠢࡨࡸࡦ࡭ࠬࠡࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠦℶ").format(e))
  def bstack1llll1111l1l_opy_(self, bstack1llll11lll1l_opy_):
    try:
      bstack1llll111l1l1_opy_ = self.bstack1lll1lllllll_opy_(bstack1llll11lll1l_opy_)
      if os.path.exists(bstack1llll111l1l1_opy_):
        with open(bstack1llll111l1l1_opy_, bstack11l11_opy_ (u"ࠧࡸࠢℷ")) as f:
          bstack1llll11ll1l1_opy_ = f.read().strip()
          return bstack1llll11ll1l1_opy_ if bstack1llll11ll1l1_opy_ else None
    except Exception as e:
      self.logger.error(bstack11l11_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦ࡬ࡰࡣࡧ࡭ࡳ࡭ࠠࡆࡖࡤ࡫࠱ࠦࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠤℸ").format(e))
  def bstack1llll1ll1ll1_opy_(self, bstack1llll11lll1l_opy_, bstack1llll11l11ll_opy_):
    bstack1llll11l1l1l_opy_ = self.bstack1llll1111l1l_opy_(bstack1llll11lll1l_opy_)
    if bstack1llll11l1l1l_opy_:
      try:
        bstack1llll111ll1l_opy_ = self.bstack1llll11llll1_opy_(bstack1llll11l1l1l_opy_, bstack1llll11l11ll_opy_)
        if not bstack1llll111ll1l_opy_:
          self.logger.debug(bstack11l11_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠦࡩࡴࠢࡸࡴࠥࡺ࡯ࠡࡦࡤࡸࡪࠦࠨࡆࡖࡤ࡫ࠥࡻ࡮ࡤࡪࡤࡲ࡬࡫ࡤࠪࠤℹ"))
          return True
        self.logger.debug(bstack11l11_opy_ (u"ࠣࡐࡨࡻࠥࡖࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥࡧࡶࡢ࡫࡯ࡥࡧࡲࡥ࠭ࠢࡧࡳࡼࡴ࡬ࡰࡣࡧ࡭ࡳ࡭ࠠࡶࡲࡧࡥࡹ࡫ࠢ℺"))
        return False
      except Exception as e:
        self.logger.warn(bstack11l11_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡩࡨࡦࡥ࡮ࠤ࡫ࡵࡲࠡࡤ࡬ࡲࡦࡸࡹࠡࡷࡳࡨࡦࡺࡥࡴ࠮ࠣࡹࡸ࡯࡮ࡨࠢࡨࡼ࡮ࡹࡴࡪࡰࡪࠤࡧ࡯࡮ࡢࡴࡼ࠾ࠥࢁࡽࠣ℻").format(e))
    return False
  def bstack1llll11llll1_opy_(self, bstack1llll11l1l1l_opy_, bstack1llll11l11ll_opy_):
    try:
      headers = {
        bstack11l11_opy_ (u"ࠥࡍ࡫࠳ࡎࡰࡰࡨ࠱ࡒࡧࡴࡤࡪࠥℼ"): bstack1llll11l1l1l_opy_
      }
      response = bstack1l11l11ll1_opy_(bstack11l11_opy_ (u"ࠫࡌࡋࡔࠨℽ"), bstack1llll11l11ll_opy_, {}, {bstack11l11_opy_ (u"ࠧ࡮ࡥࡢࡦࡨࡶࡸࠨℾ"): headers})
      if response.status_code == 304:
        return False
      return True
    except Exception as e:
      raise(bstack11l11_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡩࡨࡦࡥ࡮࡭ࡳ࡭ࠠࡧࡱࡵࠤࡕ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠣࡹࡵࡪࡡࡵࡧࡶ࠾ࠥࢁࡽࠣℿ").format(e))
  @measure(event_name=EVENTS.bstack111ll11ll11_opy_, stage=STAGE.bstack111ll11l1_opy_)
  def bstack1llll11l11l1_opy_(self, bstack1llll11l11ll_opy_, bstack1llll1111lll_opy_):
    try:
      bstack1llll1l1llll_opy_ = self.bstack1llll1l1ll11_opy_()
      bstack1llll1l1111l_opy_ = os.path.join(bstack1llll1l1llll_opy_, bstack11l11_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠴ࡺࡪࡲࠪ⅀"))
      bstack1llll11l1ll1_opy_ = os.path.join(bstack1llll1l1llll_opy_, bstack1llll1111lll_opy_)
      if self.bstack1llll1ll1ll1_opy_(bstack1llll1l1llll_opy_, bstack1llll11l11ll_opy_): # if bstack1lll1lllll1l_opy_, bstack1l1111l1111_opy_ bstack1llll11ll1l1_opy_ is bstack1llll1ll1l11_opy_ to bstack111l111ll11_opy_ version available (response 304)
        if os.path.exists(bstack1llll11l1ll1_opy_):
          self.logger.info(bstack11l11_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠠࡧࡱࡸࡲࡩࠦࡩ࡯ࠢࡾࢁ࠱ࠦࡳ࡬࡫ࡳࡴ࡮ࡴࡧࠡࡦࡲࡻࡳࡲ࡯ࡢࡦࠥ⅁").format(bstack1llll11l1ll1_opy_))
          return bstack1llll11l1ll1_opy_
        if os.path.exists(bstack1llll1l1111l_opy_):
          self.logger.info(bstack11l11_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡼ࡬ࡴࠥ࡬࡯ࡶࡰࡧࠤ࡮ࡴࠠࡼࡿ࠯ࠤࡺࡴࡺࡪࡲࡳ࡭ࡳ࡭ࠢ⅂").format(bstack1llll1l1111l_opy_))
          return self.bstack1llll11l1111_opy_(bstack1llll1l1111l_opy_, bstack1llll1111lll_opy_)
      self.logger.info(bstack11l11_opy_ (u"ࠥࡈࡴࡽ࡮࡭ࡱࡤࡨ࡮ࡴࡧࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠠࡧࡴࡲࡱࠥࢁࡽࠣ⅃").format(bstack1llll11l11ll_opy_))
      response = bstack1l11l11ll1_opy_(bstack11l11_opy_ (u"ࠫࡌࡋࡔࠨ⅄"), bstack1llll11l11ll_opy_, {}, {})
      if response.status_code == 200:
        bstack1llll1ll1lll_opy_ = response.headers.get(bstack11l11_opy_ (u"ࠧࡋࡔࡢࡩࠥⅅ"), bstack11l11_opy_ (u"ࠨࠢⅆ"))
        if bstack1llll1ll1lll_opy_:
          self.bstack1llll111111l_opy_(bstack1llll1l1llll_opy_, bstack1llll1ll1lll_opy_)
        with open(bstack1llll1l1111l_opy_, bstack11l11_opy_ (u"ࠧࡸࡤࠪⅇ")) as file:
          file.write(response.content)
        self.logger.info(bstack11l11_opy_ (u"ࠣࡆࡲࡻࡳࡲ࡯ࡢࡦࡨࡨࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠤࡦࡴࡤࠡࡵࡤࡺࡪࡪࠠࡢࡶࠣࡿࢂࠨⅈ").format(bstack1llll1l1111l_opy_))
        return self.bstack1llll11l1111_opy_(bstack1llll1l1111l_opy_, bstack1llll1111lll_opy_)
      else:
        raise(bstack11l11_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠠࡵࡪࡨࠤ࡫࡯࡬ࡦ࠰ࠣࡗࡹࡧࡴࡶࡵࠣࡧࡴࡪࡥ࠻ࠢࡾࢁࠧⅉ").format(response.status_code))
    except Exception as e:
      self.logger.error(bstack11l11_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡤࡰࡹࡱࡰࡴࡧࡤࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿ࠺ࠡࡽࢀࠦ⅊").format(e))
  def bstack1llll1l11lll_opy_(self, bstack1llll11l11ll_opy_, bstack1llll1111lll_opy_):
    try:
      retry = 2
      bstack1llll11l1ll1_opy_ = None
      bstack1llll1l11111_opy_ = False
      while retry > 0:
        bstack1llll11l1ll1_opy_ = self.bstack1llll11l11l1_opy_(bstack1llll11l11ll_opy_, bstack1llll1111lll_opy_)
        bstack1llll1l11111_opy_ = self.bstack1llll111l111_opy_(bstack1llll11l11ll_opy_, bstack1llll1111lll_opy_, bstack1llll11l1ll1_opy_)
        if bstack1llll1l11111_opy_:
          break
        retry -= 1
      return bstack1llll11l1ll1_opy_, bstack1llll1l11111_opy_
    except Exception as e:
      self.logger.error(bstack11l11_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡨࡧࡷࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠣࡴࡦࡺࡨࠣ⅋").format(e))
    return bstack1llll11l1ll1_opy_, False
  def bstack1llll111l111_opy_(self, bstack1llll11l11ll_opy_, bstack1llll1111lll_opy_, bstack1llll11l1ll1_opy_, bstack1llll1ll11ll_opy_ = 0):
    if bstack1llll1ll11ll_opy_ > 1:
      return False
    if bstack1llll11l1ll1_opy_ == None or os.path.exists(bstack1llll11l1ll1_opy_) == False:
      self.logger.warn(bstack11l11_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡵࡧࡴࡩࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨ࠱ࠦࡲࡦࡶࡵࡽ࡮ࡴࡧࠡࡦࡲࡻࡳࡲ࡯ࡢࡦࠥ⅌"))
      return False
    command = bstack11l11_opy_ (u"࠭ࡻࡾࠢ࠰࠱ࡻ࡫ࡲࡴ࡫ࡲࡲࠬ⅍").format(bstack1llll11l1ll1_opy_)
    bstack1lll1llll1l1_opy_ = subprocess.check_output(command, shell=True, text=True)
    if bstack11l11_opy_ (u"ࠧࡁࡲࡨࡶࡨࡿ࠯ࡤ࡮࡬ࠫⅎ") in bstack1lll1llll1l1_opy_:
      return True
    else:
      self.logger.error(bstack11l11_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࡥ࡫ࡩࡨࡱࠠࡧࡣ࡬ࡰࡪࡪࠢ⅏"))
      return False
  def bstack1llll11l1111_opy_(self, bstack1llll1l1111l_opy_, bstack1llll1111lll_opy_):
    try:
      working_dir = os.path.dirname(bstack1llll1l1111l_opy_)
      shutil.unpack_archive(bstack1llll1l1111l_opy_, working_dir)
      bstack1llll11l1ll1_opy_ = os.path.join(working_dir, bstack1llll1111lll_opy_)
      os.chmod(bstack1llll11l1ll1_opy_, 0o755)
      return bstack1llll11l1ll1_opy_
    except Exception as e:
      self.logger.error(bstack11l11_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡻ࡮ࡻ࡫ࡳࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠥ⅐"))
  def bstack1llll11ll111_opy_(self):
    try:
      bstack1lll1llllll1_opy_ = self.config.get(bstack11l11_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩ⅑"))
      bstack1llll11ll111_opy_ = bstack1lll1llllll1_opy_ or (bstack1lll1llllll1_opy_ is None and self.bstack11l1l1ll1_opy_)
      if not bstack1llll11ll111_opy_ or self.config.get(bstack11l11_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ⅒"), None) not in bstack111lll1l11l_opy_:
        return False
      self.bstack1lll11ll_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack11l11_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡦࡨࡸࡪࡩࡴࠡࡲࡨࡶࡨࡿࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢ⅓").format(e))
  def bstack1llll1l1l111_opy_(self):
    try:
      bstack1llll1l1l111_opy_ = self.percy_capture_mode
      return bstack1llll1l1l111_opy_
    except Exception as e:
      self.logger.error(bstack11l11_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡧࡩࡹ࡫ࡣࡵࠢࡳࡩࡷࡩࡹࠡࡥࡤࡴࡹࡻࡲࡦࠢࡰࡳࡩ࡫ࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢ⅔").format(e))
  def init(self, bstack11l1l1ll1_opy_, config, logger):
    self.bstack11l1l1ll1_opy_ = bstack11l1l1ll1_opy_
    self.config = config
    self.logger = logger
    if not self.bstack1llll11ll111_opy_():
      return
    self.bstack1llll1l1l11l_opy_ = config.get(bstack11l11_opy_ (u"ࠧࡱࡧࡵࡧࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭⅕"), {})
    self.percy_capture_mode = config.get(bstack11l11_opy_ (u"ࠨࡲࡨࡶࡨࡿࡃࡢࡲࡷࡹࡷ࡫ࡍࡰࡦࡨࠫ⅖"))
    try:
      bstack1llll11l11ll_opy_, bstack1llll1111lll_opy_ = self.bstack1llll11l1l11_opy_()
      self.bstack1111ll1l11l_opy_ = bstack1llll1111lll_opy_
      bstack1llll11l1ll1_opy_, bstack1llll1l11111_opy_ = self.bstack1llll1l11lll_opy_(bstack1llll11l11ll_opy_, bstack1llll1111lll_opy_)
      if bstack1llll1l11111_opy_:
        self.binary_path = bstack1llll11l1ll1_opy_
        thread = Thread(target=self.bstack1llll1111ll1_opy_)
        thread.start()
      else:
        self.bstack1llll1111111_opy_ = True
        self.logger.error(bstack11l11_opy_ (u"ࠤࡌࡲࡻࡧ࡬ࡪࡦࠣࡴࡪࡸࡣࡺࠢࡳࡥࡹ࡮ࠠࡧࡱࡸࡲࡩࠦ࠭ࠡࡽࢀ࠰࡛ࠥ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡑࡧࡵࡧࡾࠨ⅗").format(bstack1llll11l1ll1_opy_))
    except Exception as e:
      self.logger.error(bstack11l11_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡶࡥࡳࡥࡼ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦ⅘").format(e))
  def bstack1llll1111l11_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack11l11_opy_ (u"ࠫࡱࡵࡧࠨ⅙"), bstack11l11_opy_ (u"ࠬࡶࡥࡳࡥࡼ࠲ࡱࡵࡧࠨ⅚"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack11l11_opy_ (u"ࠨࡐࡶࡵ࡫࡭ࡳ࡭ࠠࡱࡧࡵࡧࡾࠦ࡬ࡰࡩࡶࠤࡦࡺࠠࡼࡿࠥ⅛").format(logfile))
      self.bstack1llll111ll11_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack11l11_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡪࡺࠠࡱࡧࡵࡧࡾࠦ࡬ࡰࡩࠣࡴࡦࡺࡨ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣ⅜").format(e))
  @measure(event_name=EVENTS.bstack111ll1ll1ll_opy_, stage=STAGE.bstack111ll11l1_opy_)
  def bstack1llll1111ll1_opy_(self):
    bstack1llll1l11ll1_opy_ = self.bstack1lll1llll11l_opy_()
    if bstack1llll1l11ll1_opy_ == None:
      self.bstack1llll1111111_opy_ = True
      self.logger.error(bstack11l11_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡵࡱ࡮ࡩࡳࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥ࠮ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡶࡥࡳࡥࡼࠦ⅝"))
      return False
    bstack1llll1l1lll1_opy_ = [bstack11l11_opy_ (u"ࠤࡤࡴࡵࡀࡥࡹࡧࡦ࠾ࡸࡺࡡࡳࡶࠥ⅞") if self.bstack11l1l1ll1_opy_ else bstack11l11_opy_ (u"ࠪࡩࡽ࡫ࡣ࠻ࡵࡷࡥࡷࡺࠧ⅟")]
    bstack1lllll1l111_opy_ = self.bstack1llll1lll111_opy_()
    if bstack1lllll1l111_opy_ != None:
      bstack1llll1l1lll1_opy_.append(bstack11l11_opy_ (u"ࠦ࠲ࡩࠠࡼࡿࠥⅠ").format(bstack1lllll1l111_opy_))
    env = os.environ.copy()
    env[bstack11l11_opy_ (u"ࠧࡖࡅࡓࡅ࡜ࡣ࡙ࡕࡋࡆࡐࠥⅡ")] = bstack1llll1l11ll1_opy_
    env[bstack11l11_opy_ (u"ࠨࡔࡉࡡࡅ࡙ࡎࡒࡄࡠࡗࡘࡍࡉࠨⅢ")] = os.environ.get(bstack11l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬⅣ"), bstack11l11_opy_ (u"ࠨࠩⅤ"))
    bstack1llll111lll1_opy_ = [self.binary_path]
    self.bstack1llll1111l11_opy_()
    self.bstack1llll111l1ll_opy_ = self.bstack1llll111l11l_opy_(bstack1llll111lll1_opy_ + bstack1llll1l1lll1_opy_, env)
    self.logger.debug(bstack11l11_opy_ (u"ࠤࡖࡸࡦࡸࡴࡪࡰࡪࠤࡍ࡫ࡡ࡭ࡶ࡫ࠤࡈ࡮ࡥࡤ࡭ࠥⅥ"))
    bstack1llll1ll11ll_opy_ = 0
    while self.bstack1llll111l1ll_opy_.poll() == None:
      bstack1llll1ll1111_opy_ = self.bstack1llll1l1ll1l_opy_()
      if bstack1llll1ll1111_opy_:
        self.logger.debug(bstack11l11_opy_ (u"ࠥࡌࡪࡧ࡬ࡵࡪࠣࡇ࡭࡫ࡣ࡬ࠢࡶࡹࡨࡩࡥࡴࡵࡩࡹࡱࠨⅦ"))
        self.bstack1llll1l111ll_opy_ = True
        return True
      bstack1llll1ll11ll_opy_ += 1
      self.logger.debug(bstack11l11_opy_ (u"ࠦࡍ࡫ࡡ࡭ࡶ࡫ࠤࡈ࡮ࡥࡤ࡭ࠣࡖࡪࡺࡲࡺࠢ࠰ࠤࢀࢃࠢⅧ").format(bstack1llll1ll11ll_opy_))
      time.sleep(2)
    self.logger.error(bstack11l11_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡱࡧࡵࡧࡾ࠲ࠠࡉࡧࡤࡰࡹ࡮ࠠࡄࡪࡨࡧࡰࠦࡆࡢ࡫࡯ࡩࡩࠦࡡࡧࡶࡨࡶࠥࢁࡽࠡࡣࡷࡸࡪࡳࡰࡵࡵࠥⅨ").format(bstack1llll1ll11ll_opy_))
    self.bstack1llll1111111_opy_ = True
    return False
  def bstack1llll1l1ll1l_opy_(self, bstack1llll1ll11ll_opy_ = 0):
    if bstack1llll1ll11ll_opy_ > 10:
      return False
    try:
      bstack1llll11l111l_opy_ = os.environ.get(bstack11l11_opy_ (u"࠭ࡐࡆࡔࡆ࡝ࡤ࡙ࡅࡓࡘࡈࡖࡤࡇࡄࡅࡔࡈࡗࡘ࠭Ⅹ"), bstack11l11_opy_ (u"ࠧࡩࡶࡷࡴ࠿࠵࠯࡭ࡱࡦࡥࡱ࡮࡯ࡴࡶ࠽࠹࠸࠹࠸ࠨⅪ"))
      bstack1llll1ll11l1_opy_ = bstack1llll11l111l_opy_ + bstack111lll11ll1_opy_
      response = requests.get(bstack1llll1ll11l1_opy_)
      data = response.json()
      self.percy_build_id = data.get(bstack11l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࠧⅫ"), {}).get(bstack11l11_opy_ (u"ࠩ࡬ࡨࠬⅬ"), None)
      return True
    except:
      self.logger.debug(bstack11l11_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡲࡧࡨࡻࡲࡳࡧࡧࠤࡼ࡮ࡩ࡭ࡧࠣࡴࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡩࡧࡤࡰࡹ࡮ࠠࡤࡪࡨࡧࡰࠦࡲࡦࡵࡳࡳࡳࡹࡥࠣⅭ"))
      return False
  def bstack1lll1llll11l_opy_(self):
    bstack1llll111llll_opy_ = bstack11l11_opy_ (u"ࠫࡦࡶࡰࠨⅮ") if self.bstack11l1l1ll1_opy_ else bstack11l11_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧⅯ")
    bstack1llll1ll111l_opy_ = bstack11l11_opy_ (u"ࠨࡵ࡯ࡦࡨࡪ࡮ࡴࡥࡥࠤⅰ") if self.config.get(bstack11l11_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭ⅱ")) is None else True
    bstack11l111111ll_opy_ = bstack11l11_opy_ (u"ࠣࡣࡳ࡭࠴ࡧࡰࡱࡡࡳࡩࡷࡩࡹ࠰ࡩࡨࡸࡤࡶࡲࡰ࡬ࡨࡧࡹࡥࡴࡰ࡭ࡨࡲࡄࡴࡡ࡮ࡧࡀࡿࢂࠬࡴࡺࡲࡨࡁࢀࢃࠦࡱࡧࡵࡧࡾࡃࡻࡾࠤⅲ").format(self.config[bstack11l11_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧⅳ")], bstack1llll111llll_opy_, bstack1llll1ll111l_opy_)
    if self.percy_capture_mode:
      bstack11l111111ll_opy_ += bstack11l11_opy_ (u"ࠥࠪࡵ࡫ࡲࡤࡻࡢࡧࡦࡶࡴࡶࡴࡨࡣࡲࡵࡤࡦ࠿ࡾࢁࠧⅴ").format(self.percy_capture_mode)
    uri = bstack11l111ll1_opy_(bstack11l111111ll_opy_)
    try:
      response = bstack1l11l11ll1_opy_(bstack11l11_opy_ (u"ࠫࡌࡋࡔࠨⅵ"), uri, {}, {bstack11l11_opy_ (u"ࠬࡧࡵࡵࡪࠪⅶ"): (self.config[bstack11l11_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨⅷ")], self.config[bstack11l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪⅸ")])})
      if response.status_code == 200:
        data = response.json()
        self.bstack1lll11ll_opy_ = data.get(bstack11l11_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩⅹ"))
        self.percy_capture_mode = data.get(bstack11l11_opy_ (u"ࠩࡳࡩࡷࡩࡹࡠࡥࡤࡴࡹࡻࡲࡦࡡࡰࡳࡩ࡫ࠧⅺ"))
        os.environ[bstack11l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡉࡗࡉ࡙ࠨⅻ")] = str(self.bstack1lll11ll_opy_)
        os.environ[bstack11l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡊࡘࡃ࡚ࡡࡆࡅࡕ࡚ࡕࡓࡇࡢࡑࡔࡊࡅࠨⅼ")] = str(self.percy_capture_mode)
        if bstack1llll1ll111l_opy_ == bstack11l11_opy_ (u"ࠧࡻ࡮ࡥࡧࡩ࡭ࡳ࡫ࡤࠣⅽ") and str(self.bstack1lll11ll_opy_).lower() == bstack11l11_opy_ (u"ࠨࡴࡳࡷࡨࠦⅾ"):
          self.bstack111111ll_opy_ = True
        if bstack11l11_opy_ (u"ࠢࡵࡱ࡮ࡩࡳࠨⅿ") in data:
          return data[bstack11l11_opy_ (u"ࠣࡶࡲ࡯ࡪࡴࠢↀ")]
        else:
          raise bstack11l11_opy_ (u"ࠩࡗࡳࡰ࡫࡮ࠡࡐࡲࡸࠥࡌ࡯ࡶࡰࡧࠤ࠲ࠦࡻࡾࠩↁ").format(data)
      else:
        raise bstack11l11_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡶࡥࡳࡥࡼࠤࡹࡵ࡫ࡦࡰ࠯ࠤࡗ࡫ࡳࡱࡱࡱࡷࡪࠦࡳࡵࡣࡷࡹࡸࠦ࠭ࠡࡽࢀ࠰ࠥࡘࡥࡴࡲࡲࡲࡸ࡫ࠠࡃࡱࡧࡽࠥ࠳ࠠࡼࡿࠥↂ").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack11l11_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥࡶࡥࡳࡥࡼࠤࡵࡸ࡯࡫ࡧࡦࡸࠧↃ").format(e))
  def bstack1llll1lll111_opy_(self):
    bstack1llll1l1l1ll_opy_ = os.path.join(tempfile.gettempdir(), bstack11l11_opy_ (u"ࠧࡶࡥࡳࡥࡼࡇࡴࡴࡦࡪࡩ࠱࡮ࡸࡵ࡮ࠣↄ"))
    try:
      if bstack11l11_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧↅ") not in self.bstack1llll1l1l11l_opy_:
        self.bstack1llll1l1l11l_opy_[bstack11l11_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨↆ")] = 2
      with open(bstack1llll1l1l1ll_opy_, bstack11l11_opy_ (u"ࠨࡹࠪↇ")) as fp:
        json.dump(self.bstack1llll1l1l11l_opy_, fp)
      return bstack1llll1l1l1ll_opy_
    except Exception as e:
      self.logger.error(bstack11l11_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡩࡲࡦࡣࡷࡩࠥࡶࡥࡳࡥࡼࠤࡨࡵ࡮ࡧ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤↈ").format(e))
  def bstack1llll111l11l_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack1llll11111l1_opy_ == bstack11l11_opy_ (u"ࠪࡻ࡮ࡴࠧ↉"):
        bstack1lll1lllll11_opy_ = [bstack11l11_opy_ (u"ࠫࡨࡳࡤ࠯ࡧࡻࡩࠬ↊"), bstack11l11_opy_ (u"ࠬ࠵ࡣࠨ↋")]
        cmd = bstack1lll1lllll11_opy_ + cmd
      cmd = bstack11l11_opy_ (u"࠭ࠠࠨ↌").join(cmd)
      self.logger.debug(bstack11l11_opy_ (u"ࠢࡓࡷࡱࡲ࡮ࡴࡧࠡࡽࢀࠦ↍").format(cmd))
      with open(self.bstack1llll111ll11_opy_, bstack11l11_opy_ (u"ࠣࡣࠥ↎")) as bstack1llll1l1l1l1_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack1llll1l1l1l1_opy_, text=True, stderr=bstack1llll1l1l1l1_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack1llll1111111_opy_ = True
      self.logger.error(bstack11l11_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡵ࡫ࡲࡤࡻࠣࡻ࡮ࡺࡨࠡࡥࡰࡨࠥ࠳ࠠࡼࡿ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴ࠺ࠡࡽࢀࠦ↏").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack1llll1l111ll_opy_:
        self.logger.info(bstack11l11_opy_ (u"ࠥࡗࡹࡵࡰࡱ࡫ࡱ࡫ࠥࡖࡥࡳࡥࡼࠦ←"))
        cmd = [self.binary_path, bstack11l11_opy_ (u"ࠦࡪࡾࡥࡤ࠼ࡶࡸࡴࡶࠢ↑")]
        self.bstack1llll111l11l_opy_(cmd)
        self.bstack1llll1l111ll_opy_ = False
    except Exception as e:
      self.logger.error(bstack11l11_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡷࡳࡵࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡸ࡫ࡷ࡬ࠥࡩ࡯࡮࡯ࡤࡲࡩࠦ࠭ࠡࡽࢀ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮࠻ࠢࡾࢁࠧ→").format(cmd, e))
  def bstack1ll11ll11_opy_(self):
    if not self.bstack1lll11ll_opy_:
      return
    try:
      bstack1llll1l111l1_opy_ = 0
      while not self.bstack1llll1l111ll_opy_ and bstack1llll1l111l1_opy_ < self.bstack1lll1llll1ll_opy_:
        if self.bstack1llll1111111_opy_:
          self.logger.info(bstack11l11_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡹࡥࡵࡷࡳࠤ࡫ࡧࡩ࡭ࡧࡧࠦ↓"))
          return
        time.sleep(1)
        bstack1llll1l111l1_opy_ += 1
      os.environ[bstack11l11_opy_ (u"ࠧࡑࡇࡕࡇ࡞ࡥࡂࡆࡕࡗࡣࡕࡒࡁࡕࡈࡒࡖࡒ࠭↔")] = str(self.bstack1llll11ll1ll_opy_())
      self.logger.info(bstack11l11_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡴࡧࡷࡹࡵࠦࡣࡰ࡯ࡳࡰࡪࡺࡥࡥࠤ↕"))
    except Exception as e:
      self.logger.error(bstack11l11_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡥࡵࡷࡳࠤࡵ࡫ࡲࡤࡻ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿࠥ↖").format(e))
  def bstack1llll11ll1ll_opy_(self):
    if self.bstack11l1l1ll1_opy_:
      return
    try:
      bstack1llll1ll1l1l_opy_ = [platform[bstack11l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨ↗")].lower() for platform in self.config.get(bstack11l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ↘"), [])]
      bstack1ll1llll1l1_opy_ = sys.maxsize
      bstack1llll11lllll_opy_ = bstack11l11_opy_ (u"ࠬ࠭↙")
      for browser in bstack1llll1ll1l1l_opy_:
        if browser in self.bstack1llll11lll11_opy_:
          bstack1llll11111ll_opy_ = self.bstack1llll11lll11_opy_[browser]
        if bstack1llll11111ll_opy_ < bstack1ll1llll1l1_opy_:
          bstack1ll1llll1l1_opy_ = bstack1llll11111ll_opy_
          bstack1llll11lllll_opy_ = browser
      return bstack1llll11lllll_opy_
    except Exception as e:
      self.logger.error(bstack11l11_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡩ࡭ࡳࡪࠠࡣࡧࡶࡸࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢ↚").format(e))
  @classmethod
  def bstack1l1l1l1111_opy_(self):
    return os.getenv(bstack11l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡆࡔࡆ࡝ࠬ↛"), bstack11l11_opy_ (u"ࠨࡈࡤࡰࡸ࡫ࠧ↜")).lower()
  @classmethod
  def bstack1lllll11l1_opy_(self):
    return os.getenv(bstack11l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡈࡖࡈ࡟࡟ࡄࡃࡓࡘ࡚ࡘࡅࡠࡏࡒࡈࡊ࠭↝"), bstack11l11_opy_ (u"ࠪࠫ↞"))
  @classmethod
  def bstack1l111l1l111_opy_(cls, value):
    cls.bstack111111ll_opy_ = value
  @classmethod
  def bstack1llll1lll11l_opy_(cls):
    return cls.bstack111111ll_opy_
  @classmethod
  def bstack1l111l111ll_opy_(cls, value):
    cls.percy_build_id = value
  @classmethod
  def bstack1llll1l11l1l_opy_(cls):
    return cls.percy_build_id