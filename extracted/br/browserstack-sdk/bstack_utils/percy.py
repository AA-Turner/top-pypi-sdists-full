# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack111l111_opy_ = 2048
bstack1l111l1_opy_ = 7
def bstack1lll1l_opy_ (bstack1l1l11_opy_):
    global bstack1lll1ll_opy_
    bstack1ll111l_opy_ = ord (bstack1l1l11_opy_ [-1])
    bstack1lll_opy_ = bstack1l1l11_opy_ [:-1]
    bstack11ll1_opy_ = bstack1ll111l_opy_ % len (bstack1lll_opy_)
    bstack11l11l1_opy_ = bstack1lll_opy_ [:bstack11ll1_opy_] + bstack1lll_opy_ [bstack11ll1_opy_:]
    if bstack1lll1l1_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    return eval (bstack111l11_opy_)
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
from bstack_utils.helper import bstack1llll1l111_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack1llll1l1l_opy_ import bstack11ll1ll1l1_opy_
class bstack1l1l1l1l_opy_:
  working_dir = os.getcwd()
  bstack111lll11_opy_ = False
  config = {}
  bstack1111lll1l11_opy_ = bstack1lll1l_opy_ (u"ࠫࠬ≎")
  binary_path = bstack1lll1l_opy_ (u"ࠬ࠭≏")
  bstack1llll11lllll_opy_ = bstack1lll1l_opy_ (u"࠭ࠧ≐")
  bstack111lll111l_opy_ = False
  bstack1llll11ll11l_opy_ = None
  bstack1llll11l1lll_opy_ = {}
  bstack1lll1lllllll_opy_ = 300
  bstack1lll1lll1l11_opy_ = False
  logger = None
  bstack1llll11lll1l_opy_ = False
  bstack1l11l11l_opy_ = False
  percy_build_id = None
  bstack1lll1llll11l_opy_ = bstack1lll1l_opy_ (u"ࠧࠨ≑")
  bstack1llll111lll1_opy_ = {
    bstack1lll1l_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨ≒") : 1,
    bstack1lll1l_opy_ (u"ࠩࡩ࡭ࡷ࡫ࡦࡰࡺࠪ≓") : 2,
    bstack1lll1l_opy_ (u"ࠪࡩࡩ࡭ࡥࠨ≔") : 3,
    bstack1lll1l_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࠫ≕") : 4
  }
  def __init__(self) -> None: pass
  def bstack1llll11lll11_opy_(self):
    bstack1llll1111111_opy_ = bstack1lll1l_opy_ (u"ࠬ࠭≖")
    bstack1llll11ll1l1_opy_ = sys.platform
    bstack1llll11l111l_opy_ = bstack1lll1l_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬ≗")
    if re.match(bstack1lll1l_opy_ (u"ࠢࡥࡣࡵࡻ࡮ࡴࡼ࡮ࡣࡦࠤࡴࡹࠢ≘"), bstack1llll11ll1l1_opy_) != None:
      bstack1llll1111111_opy_ = bstack111l1lll11l_opy_ + bstack1lll1l_opy_ (u"ࠣ࠱ࡳࡩࡷࡩࡹ࠮ࡱࡶࡼ࠳ࢀࡩࡱࠤ≙")
      self.bstack1lll1llll11l_opy_ = bstack1lll1l_opy_ (u"ࠩࡰࡥࡨ࠭≚")
    elif re.match(bstack1lll1l_opy_ (u"ࠥࡱࡸࡽࡩ࡯ࡾࡰࡷࡾࡹࡼ࡮࡫ࡱ࡫ࡼࢂࡣࡺࡩࡺ࡭ࡳࢂࡢࡤࡥࡺ࡭ࡳࢂࡷࡪࡰࡦࡩࢁ࡫࡭ࡤࡾࡺ࡭ࡳ࠹࠲ࠣ≛"), bstack1llll11ll1l1_opy_) != None:
      bstack1llll1111111_opy_ = bstack111l1lll11l_opy_ + bstack1lll1l_opy_ (u"ࠦ࠴ࡶࡥࡳࡥࡼ࠱ࡼ࡯࡮࠯ࡼ࡬ࡴࠧ≜")
      bstack1llll11l111l_opy_ = bstack1lll1l_opy_ (u"ࠧࡶࡥࡳࡥࡼ࠲ࡪࡾࡥࠣ≝")
      self.bstack1lll1llll11l_opy_ = bstack1lll1l_opy_ (u"࠭ࡷࡪࡰࠪ≞")
    else:
      bstack1llll1111111_opy_ = bstack111l1lll11l_opy_ + bstack1lll1l_opy_ (u"ࠢ࠰ࡲࡨࡶࡨࡿ࠭࡭࡫ࡱࡹࡽ࠴ࡺࡪࡲࠥ≟")
      self.bstack1lll1llll11l_opy_ = bstack1lll1l_opy_ (u"ࠨ࡮࡬ࡲࡺࡾࠧ≠")
    return bstack1llll1111111_opy_, bstack1llll11l111l_opy_
  def bstack1lll1lll1lll_opy_(self):
    try:
      bstack1llll111l1ll_opy_ = [os.path.join(expanduser(bstack1lll1l_opy_ (u"ࠤࢁࠦ≡")), bstack1lll1l_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪ≢")), self.working_dir, tempfile.gettempdir()]
      for path in bstack1llll111l1ll_opy_:
        if(self.bstack1lll1llll1l1_opy_(path)):
          return path
      raise bstack1lll1l_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡥࡱࡺࡲࡱࡵࡡࡥࠢࡳࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠣ≣")
    except Exception as e:
      self.logger.error(bstack1lll1l_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡨ࡬ࡲࡩࠦࡡࡷࡣ࡬ࡰࡦࡨ࡬ࡦࠢࡳࡥࡹ࡮ࠠࡧࡱࡵࠤࡵ࡫ࡲࡤࡻࠣࡨࡴࡽ࡮࡭ࡱࡤࡨ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࠰ࠤࢀࢃࠢ≤").format(e))
  def bstack1lll1llll1l1_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack1llll11l1111_opy_(self, bstack1lll1ll1l1ll_opy_):
    return os.path.join(bstack1lll1ll1l1ll_opy_, self.bstack1111lll1l11_opy_ + bstack1lll1l_opy_ (u"ࠨ࠮ࡦࡶࡤ࡫ࠧ≥"))
  def bstack1llll1111ll1_opy_(self, bstack1lll1ll1l1ll_opy_, bstack1llll11llll1_opy_):
    if not bstack1llll11llll1_opy_: return
    try:
      bstack1llll11l1l1l_opy_ = self.bstack1llll11l1111_opy_(bstack1lll1ll1l1ll_opy_)
      with open(bstack1llll11l1l1l_opy_, bstack1lll1l_opy_ (u"ࠢࡸࠤ≦")) as f:
        f.write(bstack1llll11llll1_opy_)
        self.logger.debug(bstack1lll1l_opy_ (u"ࠣࡕࡤࡺࡪࡪࠠ࡯ࡧࡺࠤࡊ࡚ࡡࡨࠢࡩࡳࡷࠦࡰࡦࡴࡦࡽࠧ≧"))
    except Exception as e:
      self.logger.error(bstack1lll1l_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡡࡷࡧࠣࡸ࡭࡫ࠠࡦࡶࡤ࡫࠱ࠦࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠤ≨").format(e))
  def bstack1llll11l1ll1_opy_(self, bstack1lll1ll1l1ll_opy_):
    try:
      bstack1llll11l1l1l_opy_ = self.bstack1llll11l1111_opy_(bstack1lll1ll1l1ll_opy_)
      if os.path.exists(bstack1llll11l1l1l_opy_):
        with open(bstack1llll11l1l1l_opy_, bstack1lll1l_opy_ (u"ࠥࡶࠧ≩")) as f:
          bstack1llll11llll1_opy_ = f.read().strip()
          return bstack1llll11llll1_opy_ if bstack1llll11llll1_opy_ else None
    except Exception as e:
      self.logger.error(bstack1lll1l_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡱࡵࡡࡥ࡫ࡱ࡫ࠥࡋࡔࡢࡩ࠯ࠤࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠢ≪").format(e))
  def bstack1llll1l1l11l_opy_(self, bstack1lll1ll1l1ll_opy_, bstack1llll1111111_opy_):
    bstack1llll111l1l1_opy_ = self.bstack1llll11l1ll1_opy_(bstack1lll1ll1l1ll_opy_)
    if bstack1llll111l1l1_opy_:
      try:
        bstack1llll111llll_opy_ = self.bstack1lll1ll1llll_opy_(bstack1llll111l1l1_opy_, bstack1llll1111111_opy_)
        if not bstack1llll111llll_opy_:
          self.logger.debug(bstack1lll1l_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠤ࡮ࡹࠠࡶࡲࠣࡸࡴࠦࡤࡢࡶࡨࠤ࠭ࡋࡔࡢࡩࠣࡹࡳࡩࡨࡢࡰࡪࡩࡩ࠯ࠢ≫"))
          return True
        self.logger.debug(bstack1lll1l_opy_ (u"ࠨࡎࡦࡹࠣࡔࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠢࡹࡩࡷࡹࡩࡰࡰࠣࡥࡻࡧࡩ࡭ࡣࡥࡰࡪ࠲ࠠࡥࡱࡺࡲࡱࡵࡡࡥ࡫ࡱ࡫ࠥࡻࡰࡥࡣࡷࡩࠧ≬"))
        return False
      except Exception as e:
        self.logger.warn(bstack1lll1l_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡧ࡭࡫ࡣ࡬ࠢࡩࡳࡷࠦࡢࡪࡰࡤࡶࡾࠦࡵࡱࡦࡤࡸࡪࡹࠬࠡࡷࡶ࡭ࡳ࡭ࠠࡦࡺ࡬ࡷࡹ࡯࡮ࡨࠢࡥ࡭ࡳࡧࡲࡺ࠼ࠣࡿࢂࠨ≭").format(e))
    return False
  def bstack1lll1ll1llll_opy_(self, bstack1llll111l1l1_opy_, bstack1llll1111111_opy_):
    try:
      headers = {
        bstack1lll1l_opy_ (u"ࠣࡋࡩ࠱ࡓࡵ࡮ࡦ࠯ࡐࡥࡹࡩࡨࠣ≮"): bstack1llll111l1l1_opy_
      }
      response = bstack1llll1l111_opy_(bstack1lll1l_opy_ (u"ࠩࡊࡉ࡙࠭≯"), bstack1llll1111111_opy_, {}, {bstack1lll1l_opy_ (u"ࠥ࡬ࡪࡧࡤࡦࡴࡶࠦ≰"): headers})
      if response.status_code == 304:
        return False
      return True
    except Exception as e:
      raise(bstack1lll1l_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡧ࡭࡫ࡣ࡬࡫ࡱ࡫ࠥ࡬࡯ࡳࠢࡓࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠡࡷࡳࡨࡦࡺࡥࡴ࠼ࠣࡿࢂࠨ≱").format(e))
  @measure(event_name=EVENTS.bstack111ll1l111l_opy_, stage=STAGE.bstack1lllll1ll1_opy_)
  def bstack1llll111l111_opy_(self, bstack1llll1111111_opy_, bstack1llll11l111l_opy_):
    try:
      bstack1llll1l11l11_opy_ = self.bstack1lll1lll1lll_opy_()
      bstack1llll1l11ll1_opy_ = os.path.join(bstack1llll1l11l11_opy_, bstack1lll1l_opy_ (u"ࠬࡶࡥࡳࡥࡼ࠲ࡿ࡯ࡰࠨ≲"))
      bstack1lll1lllll1l_opy_ = os.path.join(bstack1llll1l11l11_opy_, bstack1llll11l111l_opy_)
      if self.bstack1llll1l1l11l_opy_(bstack1llll1l11l11_opy_, bstack1llll1111111_opy_): # if true, bstack1l111111ll1_opy_ bstack1llll11llll1_opy_ is bstack1lll1llllll1_opy_ to bstack11111ll1ll1_opy_ version available (response 304)
        if os.path.exists(bstack1lll1lllll1l_opy_):
          self.logger.info(bstack1lll1l_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠥ࡬࡯ࡶࡰࡧࠤ࡮ࡴࠠࡼࡿ࠯ࠤࡸࡱࡩࡱࡲ࡬ࡲ࡬ࠦࡤࡰࡹࡱࡰࡴࡧࡤࠣ≳").format(bstack1lll1lllll1l_opy_))
          return bstack1lll1lllll1l_opy_
        if os.path.exists(bstack1llll1l11ll1_opy_):
          self.logger.info(bstack1lll1l_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡺࡪࡲࠣࡪࡴࡻ࡮ࡥࠢ࡬ࡲࠥࢁࡽ࠭ࠢࡸࡲࡿ࡯ࡰࡱ࡫ࡱ࡫ࠧ≴").format(bstack1llll1l11ll1_opy_))
          return self.bstack1llll111ll11_opy_(bstack1llll1l11ll1_opy_, bstack1llll11l111l_opy_)
      self.logger.info(bstack1lll1l_opy_ (u"ࠣࡆࡲࡻࡳࡲ࡯ࡢࡦ࡬ࡲ࡬ࠦࡰࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠥ࡬ࡲࡰ࡯ࠣࡿࢂࠨ≵").format(bstack1llll1111111_opy_))
      response = bstack1llll1l111_opy_(bstack1lll1l_opy_ (u"ࠩࡊࡉ࡙࠭≶"), bstack1llll1111111_opy_, {}, {})
      if response.status_code == 200:
        bstack1llll111111l_opy_ = response.headers.get(bstack1lll1l_opy_ (u"ࠥࡉ࡙ࡧࡧࠣ≷"), bstack1lll1l_opy_ (u"ࠦࠧ≸"))
        if bstack1llll111111l_opy_:
          self.bstack1llll1111ll1_opy_(bstack1llll1l11l11_opy_, bstack1llll111111l_opy_)
        with open(bstack1llll1l11ll1_opy_, bstack1lll1l_opy_ (u"ࠬࡽࡢࠨ≹")) as file:
          file.write(response.content)
        self.logger.info(bstack1lll1l_opy_ (u"ࠨࡄࡰࡹࡱࡰࡴࡧࡤࡦࡦࠣࡴࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠢࡤࡲࡩࠦࡳࡢࡸࡨࡨࠥࡧࡴࠡࡽࢀࠦ≺").format(bstack1llll1l11ll1_opy_))
        return self.bstack1llll111ll11_opy_(bstack1llll1l11ll1_opy_, bstack1llll11l111l_opy_)
      else:
        raise(bstack1lll1l_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠥࡺࡨࡦࠢࡩ࡭ࡱ࡫࠮ࠡࡕࡷࡥࡹࡻࡳࠡࡥࡲࡨࡪࡀࠠࡼࡿࠥ≻").format(response.status_code))
    except Exception as e:
      self.logger.error(bstack1lll1l_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡩࡵࡷ࡯࡮ࡲࡥࡩࠦࡰࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽ࠿ࠦࡻࡾࠤ≼").format(e))
  def bstack1llll1111l11_opy_(self, bstack1llll1111111_opy_, bstack1llll11l111l_opy_):
    try:
      retry = 2
      bstack1lll1lllll1l_opy_ = None
      bstack1llll11ll111_opy_ = False
      while retry > 0:
        bstack1lll1lllll1l_opy_ = self.bstack1llll111l111_opy_(bstack1llll1111111_opy_, bstack1llll11l111l_opy_)
        bstack1llll11ll111_opy_ = self.bstack1llll1l1l111_opy_(bstack1llll1111111_opy_, bstack1llll11l111l_opy_, bstack1lll1lllll1l_opy_)
        if bstack1llll11ll111_opy_:
          break
        retry -= 1
      return bstack1lll1lllll1l_opy_, bstack1llll11ll111_opy_
    except Exception as e:
      self.logger.error(bstack1lll1l_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥ࡭ࡥࡵࠢࡳࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠡࡲࡤࡸ࡭ࠨ≽").format(e))
    return bstack1lll1lllll1l_opy_, False
  def bstack1llll1l1l111_opy_(self, bstack1llll1111111_opy_, bstack1llll11l111l_opy_, bstack1lll1lllll1l_opy_, bstack1llll1111l1l_opy_ = 0):
    if bstack1llll1111l1l_opy_ > 1:
      return False
    if bstack1lll1lllll1l_opy_ == None or os.path.exists(bstack1lll1lllll1l_opy_) == False:
      self.logger.warn(bstack1lll1l_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡳࡥࡹ࡮ࠠ࡯ࡱࡷࠤ࡫ࡵࡵ࡯ࡦ࠯ࠤࡷ࡫ࡴࡳࡻ࡬ࡲ࡬ࠦࡤࡰࡹࡱࡰࡴࡧࡤࠣ≾"))
      return False
    command = bstack1lll1l_opy_ (u"ࠫࢀࢃࠠ࠮࠯ࡹࡩࡷࡹࡩࡰࡰࠪ≿").format(bstack1lll1lllll1l_opy_)
    bstack1llll11l1l11_opy_ = subprocess.check_output(command, shell=True, text=True)
    if bstack1lll1l_opy_ (u"ࠬࡆࡰࡦࡴࡦࡽ࠴ࡩ࡬ࡪࠩ⊀") in bstack1llll11l1l11_opy_:
      return True
    else:
      self.logger.error(bstack1lll1l_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡼࡥࡳࡵ࡬ࡳࡳࠦࡣࡩࡧࡦ࡯ࠥ࡬ࡡࡪ࡮ࡨࡨࠧ⊁"))
      return False
  def bstack1llll111ll11_opy_(self, bstack1llll1l11ll1_opy_, bstack1llll11l111l_opy_):
    try:
      working_dir = os.path.dirname(bstack1llll1l11ll1_opy_)
      shutil.unpack_archive(bstack1llll1l11ll1_opy_, working_dir)
      bstack1lll1lllll1l_opy_ = os.path.join(working_dir, bstack1llll11l111l_opy_)
      os.chmod(bstack1lll1lllll1l_opy_, 0o755)
      return bstack1lll1lllll1l_opy_
    except Exception as e:
      self.logger.error(bstack1lll1l_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡹࡳࢀࡩࡱࠢࡳࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠣ⊂"))
  def bstack1lll1lll1111_opy_(self):
    try:
      bstack1llll111ll1l_opy_ = self.config.get(bstack1lll1l_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧ⊃"))
      bstack1lll1lll1111_opy_ = bstack1llll111ll1l_opy_ or (bstack1llll111ll1l_opy_ is None and self.bstack111lll11_opy_)
      if not bstack1lll1lll1111_opy_ or self.config.get(bstack1lll1l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ⊄"), None) not in bstack111ll11l1l1_opy_:
        return False
      self.bstack111lll111l_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack1lll1l_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡤࡦࡶࡨࡧࡹࠦࡰࡦࡴࡦࡽ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧ⊅").format(e))
  def bstack1llll1l11l1l_opy_(self):
    try:
      bstack1llll1l11l1l_opy_ = self.percy_capture_mode
      return bstack1llll1l11l1l_opy_
    except Exception as e:
      self.logger.error(bstack1lll1l_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡥࡧࡷࡩࡨࡺࠠࡱࡧࡵࡧࡾࠦࡣࡢࡲࡷࡹࡷ࡫ࠠ࡮ࡱࡧࡩ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧ⊆").format(e))
  def init(self, bstack111lll11_opy_, config, logger):
    self.bstack111lll11_opy_ = bstack111lll11_opy_
    self.config = config
    self.logger = logger
    if not self.bstack1lll1lll1111_opy_():
      return
    self.bstack1llll11l1lll_opy_ = config.get(bstack1lll1l_opy_ (u"ࠬࡶࡥࡳࡥࡼࡓࡵࡺࡩࡰࡰࡶࠫ⊇"), {})
    self.percy_capture_mode = config.get(bstack1lll1l_opy_ (u"࠭ࡰࡦࡴࡦࡽࡈࡧࡰࡵࡷࡵࡩࡒࡵࡤࡦࠩ⊈"))
    try:
      bstack1llll1111111_opy_, bstack1llll11l111l_opy_ = self.bstack1llll11lll11_opy_()
      self.bstack1111lll1l11_opy_ = bstack1llll11l111l_opy_
      bstack1lll1lllll1l_opy_, bstack1llll11ll111_opy_ = self.bstack1llll1111l11_opy_(bstack1llll1111111_opy_, bstack1llll11l111l_opy_)
      if bstack1llll11ll111_opy_:
        self.binary_path = bstack1lll1lllll1l_opy_
        thread = Thread(target=self.bstack1llll1l111l1_opy_)
        thread.start()
      else:
        self.bstack1llll11lll1l_opy_ = True
        self.logger.error(bstack1lll1l_opy_ (u"ࠢࡊࡰࡹࡥࡱ࡯ࡤࠡࡲࡨࡶࡨࡿࠠࡱࡣࡷ࡬ࠥ࡬࡯ࡶࡰࡧࠤ࠲ࠦࡻࡾ࠮࡙ࠣࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡖࡥࡳࡥࡼࠦ⊉").format(bstack1lll1lllll1l_opy_))
    except Exception as e:
      self.logger.error(bstack1lll1l_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺࡡࡳࡶࠣࡴࡪࡸࡣࡺ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤ⊊").format(e))
  def bstack1llll111l11l_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack1lll1l_opy_ (u"ࠩ࡯ࡳ࡬࠭⊋"), bstack1lll1l_opy_ (u"ࠪࡴࡪࡸࡣࡺ࠰࡯ࡳ࡬࠭⊌"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack1lll1l_opy_ (u"ࠦࡕࡻࡳࡩ࡫ࡱ࡫ࠥࡶࡥࡳࡥࡼࠤࡱࡵࡧࡴࠢࡤࡸࠥࢁࡽࠣ⊍").format(logfile))
      self.bstack1llll11lllll_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack1lll1l_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡨࡸࠥࡶࡥࡳࡥࡼࠤࡱࡵࡧࠡࡲࡤࡸ࡭࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡿࢂࠨ⊎").format(e))
  @measure(event_name=EVENTS.bstack111l1ll1lll_opy_, stage=STAGE.bstack1lllll1ll1_opy_)
  def bstack1llll1l111l1_opy_(self):
    bstack1llll11l11l1_opy_ = self.bstack1llll1111lll_opy_()
    if bstack1llll11l11l1_opy_ == None:
      self.bstack1llll11lll1l_opy_ = True
      self.logger.error(bstack1lll1l_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡺ࡯࡬ࡧࡱࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪࠬࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸࡺࡡࡳࡶࠣࡴࡪࡸࡣࡺࠤ⊏"))
      return False
    bstack1lll1lll111l_opy_ = [bstack1lll1l_opy_ (u"ࠢࡢࡲࡳ࠾ࡪࡾࡥࡤ࠼ࡶࡸࡦࡸࡴࠣ⊐") if self.bstack111lll11_opy_ else bstack1lll1l_opy_ (u"ࠨࡧࡻࡩࡨࡀࡳࡵࡣࡵࡸࠬ⊑")]
    bstack1lllll1lll1_opy_ = self.bstack1lll1lll11l1_opy_()
    if bstack1lllll1lll1_opy_ != None:
      bstack1lll1lll111l_opy_.append(bstack1lll1l_opy_ (u"ࠤ࠰ࡧࠥࢁࡽࠣ⊒").format(bstack1lllll1lll1_opy_))
    env = os.environ.copy()
    env[bstack1lll1l_opy_ (u"ࠥࡔࡊࡘࡃ࡚ࡡࡗࡓࡐࡋࡎࠣ⊓")] = bstack1llll11l11l1_opy_
    env[bstack1lll1l_opy_ (u"࡙ࠦࡎ࡟ࡃࡗࡌࡐࡉࡥࡕࡖࡋࡇࠦ⊔")] = os.environ.get(bstack1lll1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ⊕"), bstack1lll1l_opy_ (u"࠭ࠧ⊖"))
    bstack1lll1lll1l1l_opy_ = [self.binary_path]
    self.bstack1llll111l11l_opy_()
    self.bstack1llll11ll11l_opy_ = self.bstack1llll1l111ll_opy_(bstack1lll1lll1l1l_opy_ + bstack1lll1lll111l_opy_, env)
    self.logger.debug(bstack1lll1l_opy_ (u"ࠢࡔࡶࡤࡶࡹ࡯࡮ࡨࠢࡋࡩࡦࡲࡴࡩࠢࡆ࡬ࡪࡩ࡫ࠣ⊗"))
    bstack1llll1111l1l_opy_ = 0
    while self.bstack1llll11ll11l_opy_.poll() == None:
      bstack1lll1llll1ll_opy_ = self.bstack1llll11ll1ll_opy_()
      if bstack1lll1llll1ll_opy_:
        self.logger.debug(bstack1lll1l_opy_ (u"ࠣࡊࡨࡥࡱࡺࡨࠡࡅ࡫ࡩࡨࡱࠠࡴࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࠦ⊘"))
        self.bstack1lll1lll1l11_opy_ = True
        return True
      bstack1llll1111l1l_opy_ += 1
      self.logger.debug(bstack1lll1l_opy_ (u"ࠤࡋࡩࡦࡲࡴࡩࠢࡆ࡬ࡪࡩ࡫ࠡࡔࡨࡸࡷࡿࠠ࠮ࠢࡾࢁࠧ⊙").format(bstack1llll1111l1l_opy_))
      time.sleep(2)
    self.logger.error(bstack1lll1l_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡶࡥࡳࡥࡼ࠰ࠥࡎࡥࡢ࡮ࡷ࡬ࠥࡉࡨࡦࡥ࡮ࠤࡋࡧࡩ࡭ࡧࡧࠤࡦ࡬ࡴࡦࡴࠣࡿࢂࠦࡡࡵࡶࡨࡱࡵࡺࡳࠣ⊚").format(bstack1llll1111l1l_opy_))
    self.bstack1llll11lll1l_opy_ = True
    return False
  def bstack1llll11ll1ll_opy_(self, bstack1llll1111l1l_opy_ = 0):
    if bstack1llll1111l1l_opy_ > 10:
      return False
    try:
      bstack1llll1l1l1l1_opy_ = os.environ.get(bstack1lll1l_opy_ (u"ࠫࡕࡋࡒࡄ࡛ࡢࡗࡊࡘࡖࡆࡔࡢࡅࡉࡊࡒࡆࡕࡖࠫ⊛"), bstack1lll1l_opy_ (u"ࠬ࡮ࡴࡵࡲ࠽࠳࠴ࡲ࡯ࡤࡣ࡯࡬ࡴࡹࡴ࠻࠷࠶࠷࠽࠭⊜"))
      bstack1lll1llll111_opy_ = bstack1llll1l1l1l1_opy_ + bstack111ll111l11_opy_
      response = requests.get(bstack1lll1llll111_opy_)
      data = response.json()
      self.percy_build_id = data.get(bstack1lll1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࠬ⊝"), {}).get(bstack1lll1l_opy_ (u"ࠧࡪࡦࠪ⊞"), None)
      return True
    except:
      self.logger.debug(bstack1lll1l_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡰࡥࡦࡹࡷࡸࡥࡥࠢࡺ࡬࡮ࡲࡥࠡࡲࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥ࡮ࡥࡢ࡮ࡷ࡬ࠥࡩࡨࡦࡥ࡮ࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࠨ⊟"))
      return False
  def bstack1llll1111lll_opy_(self):
    bstack1lll1ll1ll11_opy_ = bstack1lll1l_opy_ (u"ࠩࡤࡴࡵ࠭⊠") if self.bstack111lll11_opy_ else bstack1lll1l_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ⊡")
    bstack1llll1l1111l_opy_ = bstack1lll1l_opy_ (u"ࠦࡺࡴࡤࡦࡨ࡬ࡲࡪࡪࠢ⊢") if self.config.get(bstack1lll1l_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫ⊣")) is None else True
    bstack111llll1l11_opy_ = bstack1lll1l_opy_ (u"ࠨࡡࡱ࡫࠲ࡥࡵࡶ࡟ࡱࡧࡵࡧࡾ࠵ࡧࡦࡶࡢࡴࡷࡵࡪࡦࡥࡷࡣࡹࡵ࡫ࡦࡰࡂࡲࡦࡳࡥ࠾ࡽࢀࠪࡹࡿࡰࡦ࠿ࡾࢁࠫࡶࡥࡳࡥࡼࡁࢀࢃࠢ⊤").format(self.config[bstack1lll1l_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬ⊥")], bstack1lll1ll1ll11_opy_, bstack1llll1l1111l_opy_)
    if self.percy_capture_mode:
      bstack111llll1l11_opy_ += bstack1lll1l_opy_ (u"ࠣࠨࡳࡩࡷࡩࡹࡠࡥࡤࡴࡹࡻࡲࡦࡡࡰࡳࡩ࡫࠽ࡼࡿࠥ⊦").format(self.percy_capture_mode)
    uri = bstack11ll1ll1l1_opy_(bstack111llll1l11_opy_)
    try:
      response = bstack1llll1l111_opy_(bstack1lll1l_opy_ (u"ࠩࡊࡉ࡙࠭⊧"), uri, {}, {bstack1lll1l_opy_ (u"ࠪࡥࡺࡺࡨࠨ⊨"): (self.config[bstack1lll1l_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭⊩")], self.config[bstack1lll1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ⊪")])})
      if response.status_code == 200:
        data = response.json()
        self.bstack111lll111l_opy_ = data.get(bstack1lll1l_opy_ (u"࠭ࡳࡶࡥࡦࡩࡸࡹࠧ⊫"))
        self.percy_capture_mode = data.get(bstack1lll1l_opy_ (u"ࠧࡱࡧࡵࡧࡾࡥࡣࡢࡲࡷࡹࡷ࡫࡟࡮ࡱࡧࡩࠬ⊬"))
        os.environ[bstack1lll1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡇࡕࡇ࡞࠭⊭")] = str(self.bstack111lll111l_opy_)
        os.environ[bstack1lll1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡈࡖࡈ࡟࡟ࡄࡃࡓࡘ࡚ࡘࡅࡠࡏࡒࡈࡊ࠭⊮")] = str(self.percy_capture_mode)
        if bstack1llll1l1111l_opy_ == bstack1lll1l_opy_ (u"ࠥࡹࡳࡪࡥࡧ࡫ࡱࡩࡩࠨ⊯") and str(self.bstack111lll111l_opy_).lower() == bstack1lll1l_opy_ (u"ࠦࡹࡸࡵࡦࠤ⊰"):
          self.bstack1l11l11l_opy_ = True
        if bstack1lll1l_opy_ (u"ࠧࡺ࡯࡬ࡧࡱࠦ⊱") in data:
          return data[bstack1lll1l_opy_ (u"ࠨࡴࡰ࡭ࡨࡲࠧ⊲")]
        else:
          raise bstack1lll1l_opy_ (u"ࠧࡕࡱ࡮ࡩࡳࠦࡎࡰࡶࠣࡊࡴࡻ࡮ࡥࠢ࠰ࠤࢀࢃࠧ⊳").format(data)
      else:
        raise bstack1lll1l_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤ࡫࡫ࡴࡤࡪࠣࡴࡪࡸࡣࡺࠢࡷࡳࡰ࡫࡮࠭ࠢࡕࡩࡸࡶ࡯࡯ࡵࡨࠤࡸࡺࡡࡵࡷࡶࠤ࠲ࠦࡻࡾ࠮ࠣࡖࡪࡹࡰࡰࡰࡶࡩࠥࡈ࡯ࡥࡻࠣ࠱ࠥࢁࡽࠣ⊴").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack1lll1l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣࡴࡪࡸࡣࡺࠢࡳࡶࡴࡰࡥࡤࡶࠥ⊵").format(e))
  def bstack1lll1lll11l1_opy_(self):
    bstack1lll1lllll11_opy_ = os.path.join(tempfile.gettempdir(), bstack1lll1l_opy_ (u"ࠥࡴࡪࡸࡣࡺࡅࡲࡲ࡫࡯ࡧ࠯࡬ࡶࡳࡳࠨ⊶"))
    try:
      if bstack1lll1l_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࠬ⊷") not in self.bstack1llll11l1lll_opy_:
        self.bstack1llll11l1lll_opy_[bstack1lll1l_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳ࠭⊸")] = 2
      with open(bstack1lll1lllll11_opy_, bstack1lll1l_opy_ (u"࠭ࡷࠨ⊹")) as fp:
        json.dump(self.bstack1llll11l1lll_opy_, fp)
      return bstack1lll1lllll11_opy_
    except Exception as e:
      self.logger.error(bstack1lll1l_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡧࡷ࡫ࡡࡵࡧࠣࡴࡪࡸࡣࡺࠢࡦࡳࡳ࡬ࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢ⊺").format(e))
  def bstack1llll1l111ll_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack1lll1llll11l_opy_ == bstack1lll1l_opy_ (u"ࠨࡹ࡬ࡲࠬ⊻"):
        bstack1llll11l11ll_opy_ = [bstack1lll1l_opy_ (u"ࠩࡦࡱࡩ࠴ࡥࡹࡧࠪ⊼"), bstack1lll1l_opy_ (u"ࠪ࠳ࡨ࠭⊽")]
        cmd = bstack1llll11l11ll_opy_ + cmd
      cmd = bstack1lll1l_opy_ (u"ࠫࠥ࠭⊾").join(cmd)
      self.logger.debug(bstack1lll1l_opy_ (u"ࠧࡘࡵ࡯ࡰ࡬ࡲ࡬ࠦࡻࡾࠤ⊿").format(cmd))
      with open(self.bstack1llll11lllll_opy_, bstack1lll1l_opy_ (u"ࠨࡡࠣ⋀")) as bstack1llll11111l1_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack1llll11111l1_opy_, text=True, stderr=bstack1llll11111l1_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack1llll11lll1l_opy_ = True
      self.logger.error(bstack1lll1l_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡹࡧࡲࡵࠢࡳࡩࡷࡩࡹࠡࡹ࡬ࡸ࡭ࠦࡣ࡮ࡦࠣ࠱ࠥࢁࡽ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲ࠿ࠦࡻࡾࠤ⋁").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack1lll1lll1l11_opy_:
        self.logger.info(bstack1lll1l_opy_ (u"ࠣࡕࡷࡳࡵࡶࡩ࡯ࡩࠣࡔࡪࡸࡣࡺࠤ⋂"))
        cmd = [self.binary_path, bstack1lll1l_opy_ (u"ࠤࡨࡼࡪࡩ࠺ࡴࡶࡲࡴࠧ⋃")]
        self.bstack1llll1l111ll_opy_(cmd)
        self.bstack1lll1lll1l11_opy_ = False
    except Exception as e:
      self.logger.error(bstack1lll1l_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡵࡱࡳࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡽࡩࡵࡪࠣࡧࡴࡳ࡭ࡢࡰࡧࠤ࠲ࠦࡻࡾ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࡀࠠࡼࡿࠥ⋄").format(cmd, e))
  def bstack1llll11l_opy_(self):
    if not self.bstack111lll111l_opy_:
      return
    try:
      bstack1lll1lll1ll1_opy_ = 0
      while not self.bstack1lll1lll1l11_opy_ and bstack1lll1lll1ll1_opy_ < self.bstack1lll1lllllll_opy_:
        if self.bstack1llll11lll1l_opy_:
          self.logger.info(bstack1lll1l_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡷࡪࡺࡵࡱࠢࡩࡥ࡮ࡲࡥࡥࠤ⋅"))
          return
        time.sleep(1)
        bstack1lll1lll1ll1_opy_ += 1
      os.environ[bstack1lll1l_opy_ (u"ࠬࡖࡅࡓࡅ࡜ࡣࡇࡋࡓࡕࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࠫ⋆")] = str(self.bstack1llll1l11lll_opy_())
      self.logger.info(bstack1lll1l_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡹࡥࡵࡷࡳࠤࡨࡵ࡭ࡱ࡮ࡨࡸࡪࡪࠢ⋇"))
    except Exception as e:
      self.logger.error(bstack1lll1l_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡪࡺࡵࡱࠢࡳࡩࡷࡩࡹ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣ⋈").format(e))
  def bstack1llll1l11lll_opy_(self):
    if self.bstack111lll11_opy_:
      return
    try:
      bstack1lll1ll1lll1_opy_ = [platform[bstack1lll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭⋉")].lower() for platform in self.config.get(bstack1lll1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ⋊"), [])]
      bstack1ll1l1l1lll_opy_ = sys.maxsize
      bstack1lll1lll11ll_opy_ = bstack1lll1l_opy_ (u"ࠪࠫ⋋")
      for browser in bstack1lll1ll1lll1_opy_:
        if browser in self.bstack1llll111lll1_opy_:
          bstack1llll11111ll_opy_ = self.bstack1llll111lll1_opy_[browser]
        if bstack1llll11111ll_opy_ < bstack1ll1l1l1lll_opy_:
          bstack1ll1l1l1lll_opy_ = bstack1llll11111ll_opy_
          bstack1lll1lll11ll_opy_ = browser
      return bstack1lll1lll11ll_opy_
    except Exception as e:
      self.logger.error(bstack1lll1l_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡧ࡫ࡱࡨࠥࡨࡥࡴࡶࠣࡴࡱࡧࡴࡧࡱࡵࡱ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧ⋌").format(e))
  @classmethod
  def bstack11l1ll1lll_opy_(self):
    return os.getenv(bstack1lll1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡋࡒࡄ࡛ࠪ⋍"), bstack1lll1l_opy_ (u"࠭ࡆࡢ࡮ࡶࡩࠬ⋎")).lower()
  @classmethod
  def bstack1lllll1ll_opy_(self):
    return os.getenv(bstack1lll1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡆࡔࡆ࡝ࡤࡉࡁࡑࡖࡘࡖࡊࡥࡍࡐࡆࡈࠫ⋏"), bstack1lll1l_opy_ (u"ࠨࠩ⋐"))
  @classmethod
  def bstack1l1111l1lll_opy_(cls, value):
    cls.bstack1l11l11l_opy_ = value
  @classmethod
  def bstack1llll1l11111_opy_(cls):
    return cls.bstack1l11l11l_opy_
  @classmethod
  def bstack1l1111lll11_opy_(cls, value):
    cls.percy_build_id = value
  @classmethod
  def bstack1lll1ll1ll1l_opy_(cls):
    return cls.percy_build_id