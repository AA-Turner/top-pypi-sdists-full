# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack1l1lll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack1l1l1l1_opy_ (bstack1111l11_opy_):
    global bstack11l111_opy_
    bstack11ll1l_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1l111_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l11l_opy_ = bstack11ll1l_opy_ % len (bstack1l111_opy_)
    bstack1ll11l_opy_ = bstack1l111_opy_ [:bstack1l11l_opy_] + bstack1l111_opy_ [bstack1l11l_opy_:]
    if bstack11llll_opy_:
        bstack1lll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    else:
        bstack1lll1_opy_ = str () .join ([chr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    return eval (bstack1lll1_opy_)
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
from bstack_utils.helper import bstack1l1llll1ll_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack1l1l1l11l1_opy_ import bstack111l1ll1_opy_
class bstack11lllll1_opy_:
  working_dir = os.getcwd()
  bstack1lll1111_opy_ = False
  config = {}
  bstack11l11lll1l1_opy_ = bstack1l1l1l1_opy_ (u"ࠪࠫᶼ")
  binary_path = bstack1l1l1l1_opy_ (u"ࠫࠬᶽ")
  bstack1111ll1l111_opy_ = bstack1l1l1l1_opy_ (u"ࠬ࠭ᶾ")
  bstack1l11111lll_opy_ = False
  bstack111l11l11l1_opy_ = None
  bstack1111ll1ll11_opy_ = {}
  bstack111l11l111l_opy_ = 300
  bstack1111ll11ll1_opy_ = False
  logger = None
  bstack1111lllll11_opy_ = False
  bstack111lll111_opy_ = False
  percy_build_id = None
  bstack1111ll11l1l_opy_ = bstack1l1l1l1_opy_ (u"࠭ࠧᶿ")
  bstack111l11l1ll1_opy_ = {
    bstack1l1l1l1_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧ᷀") : 1,
    bstack1l1l1l1_opy_ (u"ࠨࡨ࡬ࡶࡪ࡬࡯ࡹࠩ᷁") : 2,
    bstack1l1l1l1_opy_ (u"ࠩࡨࡨ࡬࡫᷂ࠧ") : 3,
    bstack1l1l1l1_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࠪ᷃") : 4
  }
  def __init__(self) -> None: pass
  def bstack111l11111l1_opy_(self):
    bstack1111l1ll11l_opy_ = bstack1l1l1l1_opy_ (u"ࠫࠬ᷄")
    bstack1111lllllll_opy_ = sys.platform
    bstack111l11l1l11_opy_ = bstack1l1l1l1_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫ᷅")
    if re.match(bstack1l1l1l1_opy_ (u"ࠨࡤࡢࡴࡺ࡭ࡳࢂ࡭ࡢࡥࠣࡳࡸࠨ᷆"), bstack1111lllllll_opy_) != None:
      bstack1111l1ll11l_opy_ = bstack11l1llllll1_opy_ + bstack1l1l1l1_opy_ (u"ࠢ࠰ࡲࡨࡶࡨࡿ࠭ࡰࡵࡻ࠲ࡿ࡯ࡰࠣ᷇")
      self.bstack1111ll11l1l_opy_ = bstack1l1l1l1_opy_ (u"ࠨ࡯ࡤࡧࠬ᷈")
    elif re.match(bstack1l1l1l1_opy_ (u"ࠤࡰࡷࡼ࡯࡮ࡽ࡯ࡶࡽࡸࢂ࡭ࡪࡰࡪࡻࢁࡩࡹࡨࡹ࡬ࡲࢁࡨࡣࡤࡹ࡬ࡲࢁࡽࡩ࡯ࡥࡨࢀࡪࡳࡣࡽࡹ࡬ࡲ࠸࠸ࠢ᷉"), bstack1111lllllll_opy_) != None:
      bstack1111l1ll11l_opy_ = bstack11l1llllll1_opy_ + bstack1l1l1l1_opy_ (u"ࠥ࠳ࡵ࡫ࡲࡤࡻ࠰ࡻ࡮ࡴ࠮ࡻ࡫ࡳ᷊ࠦ")
      bstack111l11l1l11_opy_ = bstack1l1l1l1_opy_ (u"ࠦࡵ࡫ࡲࡤࡻ࠱ࡩࡽ࡫ࠢ᷋")
      self.bstack1111ll11l1l_opy_ = bstack1l1l1l1_opy_ (u"ࠬࡽࡩ࡯ࠩ᷌")
    else:
      bstack1111l1ll11l_opy_ = bstack11l1llllll1_opy_ + bstack1l1l1l1_opy_ (u"ࠨ࠯ࡱࡧࡵࡧࡾ࠳࡬ࡪࡰࡸࡼ࠳ࢀࡩࡱࠤ᷍")
      self.bstack1111ll11l1l_opy_ = bstack1l1l1l1_opy_ (u"ࠧ࡭࡫ࡱࡹࡽ᷎࠭")
    return bstack1111l1ll11l_opy_, bstack111l11l1l11_opy_
  def bstack1111lll11ll_opy_(self):
    try:
      bstack1111ll111l1_opy_ = [os.path.join(expanduser(bstack1l1l1l1_opy_ (u"ࠣࢀ᷏ࠥ")), bstack1l1l1l1_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬᷐ࠩ")), self.working_dir, tempfile.gettempdir()]
      for path in bstack1111ll111l1_opy_:
        if(self.bstack1111ll1l1ll_opy_(path)):
          return path
      raise bstack1l1l1l1_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡤࡰࡹࡱࡰࡴࡧࡤࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠢ᷑")
    except Exception as e:
      self.logger.error(bstack1l1l1l1_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡧ࡫ࡱࡨࠥࡧࡶࡢ࡫࡯ࡥࡧࡲࡥࠡࡲࡤࡸ࡭ࠦࡦࡰࡴࠣࡴࡪࡸࡣࡺࠢࡧࡳࡼࡴ࡬ࡰࡣࡧ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࠯ࠣࡿࢂࠨ᷒").format(e))
  def bstack1111ll1l1ll_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack111l11l1l1l_opy_(self, bstack111l11l1111_opy_):
    return os.path.join(bstack111l11l1111_opy_, self.bstack11l11lll1l1_opy_ + bstack1l1l1l1_opy_ (u"ࠧ࠴ࡥࡵࡣࡪࠦᷓ"))
  def bstack1111llll111_opy_(self, bstack111l11l1111_opy_, bstack1111lll111l_opy_):
    if not bstack1111lll111l_opy_: return
    try:
      bstack111l1111ll1_opy_ = self.bstack111l11l1l1l_opy_(bstack111l11l1111_opy_)
      with open(bstack111l1111ll1_opy_, bstack1l1l1l1_opy_ (u"ࠨࡷࠣᷔ")) as f:
        f.write(bstack1111lll111l_opy_)
        self.logger.debug(bstack1l1l1l1_opy_ (u"ࠢࡔࡣࡹࡩࡩࠦ࡮ࡦࡹࠣࡉ࡙ࡧࡧࠡࡨࡲࡶࠥࡶࡥࡳࡥࡼࠦᷕ"))
    except Exception as e:
      self.logger.error(bstack1l1l1l1_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡧࡶࡦࠢࡷ࡬ࡪࠦࡥࡵࡣࡪ࠰ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠣᷖ").format(e))
  def bstack111l111l11l_opy_(self, bstack111l11l1111_opy_):
    try:
      bstack111l1111ll1_opy_ = self.bstack111l11l1l1l_opy_(bstack111l11l1111_opy_)
      if os.path.exists(bstack111l1111ll1_opy_):
        with open(bstack111l1111ll1_opy_, bstack1l1l1l1_opy_ (u"ࠤࡵࠦᷗ")) as f:
          bstack1111lll111l_opy_ = f.read().strip()
          return bstack1111lll111l_opy_ if bstack1111lll111l_opy_ else None
    except Exception as e:
      self.logger.error(bstack1l1l1l1_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡰࡴࡧࡤࡪࡰࡪࠤࡊ࡚ࡡࡨ࠮ࠣࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂࠨᷘ").format(e))
  def bstack111l111l111_opy_(self, bstack111l11l1111_opy_, bstack1111l1ll11l_opy_):
    bstack1111llll11l_opy_ = self.bstack111l111l11l_opy_(bstack111l11l1111_opy_)
    if bstack1111llll11l_opy_:
      try:
        bstack1111ll1lll1_opy_ = self.bstack1111ll1l1l1_opy_(bstack1111llll11l_opy_, bstack1111l1ll11l_opy_)
        if not bstack1111ll1lll1_opy_:
          self.logger.debug(bstack1l1l1l1_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠣ࡭ࡸࠦࡵࡱࠢࡷࡳࠥࡪࡡࡵࡧࠣࠬࡊ࡚ࡡࡨࠢࡸࡲࡨ࡮ࡡ࡯ࡩࡨࡨ࠮ࠨᷙ"))
          return True
        self.logger.debug(bstack1l1l1l1_opy_ (u"ࠧࡔࡥࡸࠢࡓࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࡤࡺࡦ࡯࡬ࡢࡤ࡯ࡩ࠱ࠦࡤࡰࡹࡱࡰࡴࡧࡤࡪࡰࡪࠤࡺࡶࡤࡢࡶࡨࠦᷚ"))
        return False
      except Exception as e:
        self.logger.warn(bstack1l1l1l1_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡦ࡬ࡪࡩ࡫ࠡࡨࡲࡶࠥࡨࡩ࡯ࡣࡵࡽࠥࡻࡰࡥࡣࡷࡩࡸ࠲ࠠࡶࡵ࡬ࡲ࡬ࠦࡥࡹ࡫ࡶࡸ࡮ࡴࡧࠡࡤ࡬ࡲࡦࡸࡹ࠻ࠢࡾࢁࠧᷛ").format(e))
    return False
  def bstack1111ll1l1l1_opy_(self, bstack1111llll11l_opy_, bstack1111l1ll11l_opy_):
    try:
      headers = {
        bstack1l1l1l1_opy_ (u"ࠢࡊࡨ࠰ࡒࡴࡴࡥ࠮ࡏࡤࡸࡨ࡮ࠢᷜ"): bstack1111llll11l_opy_
      }
      response = bstack1l1llll1ll_opy_(bstack1l1l1l1_opy_ (u"ࠨࡉࡈࡘࠬᷝ"), bstack1111l1ll11l_opy_, {}, {bstack1l1l1l1_opy_ (u"ࠤ࡫ࡩࡦࡪࡥࡳࡵࠥᷞ"): headers})
      if response.status_code == 304:
        return False
      return True
    except Exception as e:
      raise(bstack1l1l1l1_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡦ࡬ࡪࡩ࡫ࡪࡰࡪࠤ࡫ࡵࡲࠡࡒࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠠࡶࡲࡧࡥࡹ࡫ࡳ࠻ࠢࡾࢁࠧᷟ").format(e))
  @measure(event_name=EVENTS.bstack11ll1111l1l_opy_, stage=STAGE.bstack1l1lll1lll_opy_)
  def bstack1111ll1l11l_opy_(self, bstack1111l1ll11l_opy_, bstack111l11l1l11_opy_):
    try:
      bstack111l11111ll_opy_ = self.bstack1111lll11ll_opy_()
      bstack111l111ll1l_opy_ = os.path.join(bstack111l11111ll_opy_, bstack1l1l1l1_opy_ (u"ࠫࡵ࡫ࡲࡤࡻ࠱ࡾ࡮ࡶࠧᷠ"))
      bstack1111l1l1l1l_opy_ = os.path.join(bstack111l11111ll_opy_, bstack111l11l1l11_opy_)
      if self.bstack111l111l111_opy_(bstack111l11111ll_opy_, bstack1111l1ll11l_opy_): # if bstack1111ll11111_opy_, bstack1l1l1l11111_opy_ bstack1111lll111l_opy_ is bstack1111ll11lll_opy_ to bstack11l11ll1l11_opy_ version available (response 304)
        if os.path.exists(bstack1111l1l1l1l_opy_):
          self.logger.info(bstack1l1l1l1_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠤ࡫ࡵࡵ࡯ࡦࠣ࡭ࡳࠦࡻࡾ࠮ࠣࡷࡰ࡯ࡰࡱ࡫ࡱ࡫ࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠢᷡ").format(bstack1111l1l1l1l_opy_))
          return bstack1111l1l1l1l_opy_
        if os.path.exists(bstack111l111ll1l_opy_):
          self.logger.info(bstack1l1l1l1_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࢀࡩࡱࠢࡩࡳࡺࡴࡤࠡ࡫ࡱࠤࢀࢃࠬࠡࡷࡱࡾ࡮ࡶࡰࡪࡰࡪࠦᷢ").format(bstack111l111ll1l_opy_))
          return self.bstack1111lll1111_opy_(bstack111l111ll1l_opy_, bstack111l11l1l11_opy_)
      self.logger.info(bstack1l1l1l1_opy_ (u"ࠢࡅࡱࡺࡲࡱࡵࡡࡥ࡫ࡱ࡫ࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠤ࡫ࡸ࡯࡮ࠢࡾࢁࠧᷣ").format(bstack1111l1ll11l_opy_))
      response = bstack1l1llll1ll_opy_(bstack1l1l1l1_opy_ (u"ࠨࡉࡈࡘࠬᷤ"), bstack1111l1ll11l_opy_, {}, {})
      if response.status_code == 200:
        bstack111l111l1l1_opy_ = response.headers.get(bstack1l1l1l1_opy_ (u"ࠤࡈࡘࡦ࡭ࠢᷥ"), bstack1l1l1l1_opy_ (u"ࠥࠦᷦ"))
        if bstack111l111l1l1_opy_:
          self.bstack1111llll111_opy_(bstack111l11111ll_opy_, bstack111l111l1l1_opy_)
        with open(bstack111l111ll1l_opy_, bstack1l1l1l1_opy_ (u"ࠫࡼࡨࠧᷧ")) as file:
          file.write(response.content)
        self.logger.info(bstack1l1l1l1_opy_ (u"ࠧࡊ࡯ࡸࡰ࡯ࡳࡦࡪࡥࡥࠢࡳࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠡࡣࡱࡨࠥࡹࡡࡷࡧࡧࠤࡦࡺࠠࡼࡿࠥᷨ").format(bstack111l111ll1l_opy_))
        return self.bstack1111lll1111_opy_(bstack111l111ll1l_opy_, bstack111l11l1l11_opy_)
      else:
        raise(bstack1l1l1l1_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࠤࡹ࡮ࡥࠡࡨ࡬ࡰࡪ࠴ࠠࡔࡶࡤࡸࡺࡹࠠࡤࡱࡧࡩ࠿ࠦࡻࡾࠤᷩ").format(response.status_code))
    except Exception as e:
      self.logger.error(bstack1l1l1l1_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼ࠾ࠥࢁࡽࠣᷪ").format(e))
  def bstack1111ll1111l_opy_(self, bstack1111l1ll11l_opy_, bstack111l11l1l11_opy_):
    try:
      retry = 2
      bstack1111l1l1l1l_opy_ = None
      bstack1111l1lll1l_opy_ = False
      while retry > 0:
        bstack1111l1l1l1l_opy_ = self.bstack1111ll1l11l_opy_(bstack1111l1ll11l_opy_, bstack111l11l1l11_opy_)
        bstack1111l1lll1l_opy_ = self.bstack1111l1llll1_opy_(bstack1111l1ll11l_opy_, bstack111l11l1l11_opy_, bstack1111l1l1l1l_opy_)
        if bstack1111l1lll1l_opy_:
          break
        retry -= 1
      return bstack1111l1l1l1l_opy_, bstack1111l1lll1l_opy_
    except Exception as e:
      self.logger.error(bstack1l1l1l1_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡬࡫ࡴࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠠࡱࡣࡷ࡬ࠧᷫ").format(e))
    return bstack1111l1l1l1l_opy_, False
  def bstack1111l1llll1_opy_(self, bstack1111l1ll11l_opy_, bstack111l11l1l11_opy_, bstack1111l1l1l1l_opy_, bstack1111l1lll11_opy_ = 0):
    if bstack1111l1lll11_opy_ > 1:
      return False
    if bstack1111l1l1l1l_opy_ == None or os.path.exists(bstack1111l1l1l1l_opy_) == False:
      self.logger.warn(bstack1l1l1l1_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡲࡤࡸ࡭ࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥ࠮ࠣࡶࡪࡺࡲࡺ࡫ࡱ࡫ࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠢᷬ"))
      return False
    bstack111l111l1ll_opy_ = bstack1l1l1l1_opy_ (u"ࡵࠦࡣ࠴ࠪࡁࡲࡨࡶࡨࡿ࠯ࡤ࡮࡬ࠤࡡࡪࠫ࡝࠰࡟ࡨ࠰ࡢ࠮࡝ࡦ࠮ࠦᷭ")
    command = bstack1l1l1l1_opy_ (u"ࠫࢀࢃࠠ࠮࠯ࡹࡩࡷࡹࡩࡰࡰࠪᷮ").format(bstack1111l1l1l1l_opy_)
    bstack111l111lll1_opy_ = subprocess.check_output(command, shell=True, text=True)
    if re.match(bstack111l111l1ll_opy_, bstack111l111lll1_opy_) != None:
      return True
    else:
      self.logger.error(bstack1l1l1l1_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥࡩࡨࡦࡥ࡮ࠤ࡫ࡧࡩ࡭ࡧࡧࠦᷯ"))
      return False
  def bstack1111lll1111_opy_(self, bstack111l111ll1l_opy_, bstack111l11l1l11_opy_):
    try:
      working_dir = os.path.dirname(bstack111l111ll1l_opy_)
      shutil.unpack_archive(bstack111l111ll1l_opy_, working_dir)
      bstack1111l1l1l1l_opy_ = os.path.join(working_dir, bstack111l11l1l11_opy_)
      os.chmod(bstack1111l1l1l1l_opy_, 0o755)
      return bstack1111l1l1l1l_opy_
    except Exception as e:
      self.logger.error(bstack1l1l1l1_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡸࡲࡿ࡯ࡰࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠢᷰ"))
  def bstack1111llll1l1_opy_(self):
    try:
      bstack1111l1ll1ll_opy_ = self.config.get(bstack1l1l1l1_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭ᷱ"))
      bstack1111llll1l1_opy_ = bstack1111l1ll1ll_opy_ or (bstack1111l1ll1ll_opy_ is None and self.bstack1lll1111_opy_)
      if not bstack1111llll1l1_opy_ or self.config.get(bstack1l1l1l1_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫᷲ"), None) not in bstack11ll11111l1_opy_:
        return False
      self.bstack1l11111lll_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack1l1l1l1_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡪࡥࡵࡧࡦࡸࠥࡶࡥࡳࡥࡼ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦᷳ").format(e))
  def bstack111l11l11ll_opy_(self):
    try:
      bstack111l11l11ll_opy_ = self.percy_capture_mode
      return bstack111l11l11ll_opy_
    except Exception as e:
      self.logger.error(bstack1l1l1l1_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡤࡦࡶࡨࡧࡹࠦࡰࡦࡴࡦࡽࠥࡩࡡࡱࡶࡸࡶࡪࠦ࡭ࡰࡦࡨ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦᷴ").format(e))
  def init(self, bstack1lll1111_opy_, config, logger):
    self.bstack1lll1111_opy_ = bstack1lll1111_opy_
    self.config = config
    self.logger = logger
    if not self.bstack1111llll1l1_opy_():
      return
    self.bstack1111ll1ll11_opy_ = config.get(bstack1l1l1l1_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ᷵"), {})
    self.percy_capture_mode = config.get(bstack1l1l1l1_opy_ (u"ࠬࡶࡥࡳࡥࡼࡇࡦࡶࡴࡶࡴࡨࡑࡴࡪࡥࠨ᷶"))
    try:
      bstack1111l1ll11l_opy_, bstack111l11l1l11_opy_ = self.bstack111l11111l1_opy_()
      self.bstack11l11lll1l1_opy_ = bstack111l11l1l11_opy_
      bstack1111l1l1l1l_opy_, bstack1111l1lll1l_opy_ = self.bstack1111ll1111l_opy_(bstack1111l1ll11l_opy_, bstack111l11l1l11_opy_)
      if bstack1111l1lll1l_opy_:
        self.binary_path = bstack1111l1l1l1l_opy_
        thread = Thread(target=self.bstack111l111llll_opy_)
        thread.start()
      else:
        self.bstack1111lllll11_opy_ = True
        self.logger.error(bstack1l1l1l1_opy_ (u"ࠨࡉ࡯ࡸࡤࡰ࡮ࡪࠠࡱࡧࡵࡧࡾࠦࡰࡢࡶ࡫ࠤ࡫ࡵࡵ࡯ࡦࠣ࠱ࠥࢁࡽ࠭ࠢࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡕ࡫ࡲࡤࡻ᷷ࠥ").format(bstack1111l1l1l1l_opy_))
    except Exception as e:
      self.logger.error(bstack1l1l1l1_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡹࡧࡲࡵࠢࡳࡩࡷࡩࡹ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽ᷸ࠣ").format(e))
  def bstack111l1111l1l_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack1l1l1l1_opy_ (u"ࠨ࡮ࡲ࡫᷹ࠬ"), bstack1l1l1l1_opy_ (u"ࠩࡳࡩࡷࡩࡹ࠯࡮ࡲ࡫᷺ࠬ"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack1l1l1l1_opy_ (u"ࠥࡔࡺࡹࡨࡪࡰࡪࠤࡵ࡫ࡲࡤࡻࠣࡰࡴ࡭ࡳࠡࡣࡷࠤࢀࢃࠢ᷻").format(logfile))
      self.bstack1111ll1l111_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack1l1l1l1_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡧࡷࠤࡵ࡫ࡲࡤࡻࠣࡰࡴ࡭ࠠࡱࡣࡷ࡬࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧ᷼").format(e))
  @measure(event_name=EVENTS.bstack11l1lll111l_opy_, stage=STAGE.bstack1l1lll1lll_opy_)
  def bstack111l111llll_opy_(self):
    bstack111l1111l11_opy_ = self.bstack1111l1lllll_opy_()
    if bstack111l1111l11_opy_ == None:
      self.bstack1111lllll11_opy_ = True
      self.logger.error(bstack1l1l1l1_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡹࡵ࡫ࡦࡰࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩ࠲ࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡹࡧࡲࡵࠢࡳࡩࡷࡩࡹ᷽ࠣ"))
      return False
    command_args = [bstack1l1l1l1_opy_ (u"ࠨࡡࡱࡲ࠽ࡩࡽ࡫ࡣ࠻ࡵࡷࡥࡷࡺࠢ᷾") if self.bstack1lll1111_opy_ else bstack1l1l1l1_opy_ (u"ࠧࡦࡺࡨࡧ࠿ࡹࡴࡢࡴࡷ᷿ࠫ")]
    bstack111ll1l1l1l_opy_ = self.bstack1111l1l1lll_opy_()
    if bstack111ll1l1l1l_opy_ != None:
      command_args.append(bstack1l1l1l1_opy_ (u"ࠣ࠯ࡦࠤࢀࢃࠢḀ").format(bstack111ll1l1l1l_opy_))
    env = os.environ.copy()
    env[bstack1l1l1l1_opy_ (u"ࠤࡓࡉࡗࡉ࡙ࡠࡖࡒࡏࡊࡔࠢḁ")] = bstack111l1111l11_opy_
    env[bstack1l1l1l1_opy_ (u"ࠥࡘࡍࡥࡂࡖࡋࡏࡈࡤ࡛ࡕࡊࡆࠥḂ")] = os.environ.get(bstack1l1l1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩḃ"), bstack1l1l1l1_opy_ (u"ࠬ࠭Ḅ"))
    bstack1111lll1ll1_opy_ = [self.binary_path]
    self.bstack111l1111l1l_opy_()
    self.bstack111l11l11l1_opy_ = self.bstack1111llllll1_opy_(bstack1111lll1ll1_opy_ + command_args, env)
    self.logger.debug(bstack1l1l1l1_opy_ (u"ࠨࡓࡵࡣࡵࡸ࡮ࡴࡧࠡࡊࡨࡥࡱࡺࡨࠡࡅ࡫ࡩࡨࡱࠢḅ"))
    bstack1111l1lll11_opy_ = 0
    while self.bstack111l11l11l1_opy_.poll() == None:
      bstack111l111111l_opy_ = self.bstack111l1111111_opy_()
      if bstack111l111111l_opy_:
        self.logger.debug(bstack1l1l1l1_opy_ (u"ࠢࡉࡧࡤࡰࡹ࡮ࠠࡄࡪࡨࡧࡰࠦࡳࡶࡥࡦࡩࡸࡹࡦࡶ࡮ࠥḆ"))
        self.bstack1111ll11ll1_opy_ = True
        return True
      bstack1111l1lll11_opy_ += 1
      self.logger.debug(bstack1l1l1l1_opy_ (u"ࠣࡊࡨࡥࡱࡺࡨࠡࡅ࡫ࡩࡨࡱࠠࡓࡧࡷࡶࡾࠦ࠭ࠡࡽࢀࠦḇ").format(bstack1111l1lll11_opy_))
      time.sleep(2)
    self.logger.error(bstack1l1l1l1_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡵ࡫ࡲࡤࡻ࠯ࠤࡍ࡫ࡡ࡭ࡶ࡫ࠤࡈ࡮ࡥࡤ࡭ࠣࡊࡦ࡯࡬ࡦࡦࠣࡥ࡫ࡺࡥࡳࠢࡾࢁࠥࡧࡴࡵࡧࡰࡴࡹࡹࠢḈ").format(bstack1111l1lll11_opy_))
    self.bstack1111lllll11_opy_ = True
    return False
  def bstack111l1111111_opy_(self, bstack1111l1lll11_opy_ = 0):
    if bstack1111l1lll11_opy_ > 10:
      return False
    try:
      bstack1111ll1ll1l_opy_ = os.environ.get(bstack1l1l1l1_opy_ (u"ࠪࡔࡊࡘࡃ࡚ࡡࡖࡉࡗ࡜ࡅࡓࡡࡄࡈࡉࡘࡅࡔࡕࠪḉ"), bstack1l1l1l1_opy_ (u"ࠫ࡭ࡺࡴࡱ࠼࠲࠳ࡱࡵࡣࡢ࡮࡫ࡳࡸࡺ࠺࠶࠵࠶࠼ࠬḊ"))
      bstack111l1111lll_opy_ = bstack1111ll1ll1l_opy_ + bstack11l1ll1lll1_opy_
      response = requests.get(bstack111l1111lll_opy_)
      data = response.json()
      self.percy_build_id = data.get(bstack1l1l1l1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࠫḋ"), {}).get(bstack1l1l1l1_opy_ (u"࠭ࡩࡥࠩḌ"), None)
      return True
    except:
      self.logger.debug(bstack1l1l1l1_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦ࡯ࡤࡥࡸࡶࡷ࡫ࡤࠡࡹ࡫࡭ࡱ࡫ࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤ࡭࡫ࡡ࡭ࡶ࡫ࠤࡨ࡮ࡥࡤ࡭ࠣࡶࡪࡹࡰࡰࡰࡶࡩࠧḍ"))
      return False
  def bstack1111l1lllll_opy_(self):
    bstack1111l1ll111_opy_ = bstack1l1l1l1_opy_ (u"ࠨࡣࡳࡴࠬḎ") if self.bstack1lll1111_opy_ else bstack1l1l1l1_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫḏ")
    bstack1111lllll1l_opy_ = bstack1l1l1l1_opy_ (u"ࠥࡹࡳࡪࡥࡧ࡫ࡱࡩࡩࠨḐ") if self.config.get(bstack1l1l1l1_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪḑ")) is None else True
    bstack11ll1l11l11_opy_ = bstack1l1l1l1_opy_ (u"ࠧࡧࡰࡪ࠱ࡤࡴࡵࡥࡰࡦࡴࡦࡽ࠴࡭ࡥࡵࡡࡳࡶࡴࡰࡥࡤࡶࡢࡸࡴࡱࡥ࡯ࡁࡱࡥࡲ࡫࠽ࡼࡿࠩࡸࡾࡶࡥ࠾ࡽࢀࠪࡵ࡫ࡲࡤࡻࡀࡿࢂࠨḒ").format(self.config[bstack1l1l1l1_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫḓ")], bstack1111l1ll111_opy_, bstack1111lllll1l_opy_)
    if self.percy_capture_mode:
      bstack11ll1l11l11_opy_ += bstack1l1l1l1_opy_ (u"ࠢࠧࡲࡨࡶࡨࡿ࡟ࡤࡣࡳࡸࡺࡸࡥࡠ࡯ࡲࡨࡪࡃࡻࡾࠤḔ").format(self.percy_capture_mode)
    uri = bstack111l1ll1_opy_(bstack11ll1l11l11_opy_)
    try:
      response = bstack1l1llll1ll_opy_(bstack1l1l1l1_opy_ (u"ࠨࡉࡈࡘࠬḕ"), uri, {}, {bstack1l1l1l1_opy_ (u"ࠩࡤࡹࡹ࡮ࠧḖ"): (self.config[bstack1l1l1l1_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬḗ")], self.config[bstack1l1l1l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧḘ")])})
      if response.status_code == 200:
        data = response.json()
        self.bstack1l11111lll_opy_ = data.get(bstack1l1l1l1_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭ḙ"))
        self.percy_capture_mode = data.get(bstack1l1l1l1_opy_ (u"࠭ࡰࡦࡴࡦࡽࡤࡩࡡࡱࡶࡸࡶࡪࡥ࡭ࡰࡦࡨࠫḚ"))
        os.environ[bstack1l1l1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡆࡔࡆ࡝ࠬḛ")] = str(self.bstack1l11111lll_opy_)
        os.environ[bstack1l1l1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡇࡕࡇ࡞ࡥࡃࡂࡒࡗ࡙ࡗࡋ࡟ࡎࡑࡇࡉࠬḜ")] = str(self.percy_capture_mode)
        if bstack1111lllll1l_opy_ == bstack1l1l1l1_opy_ (u"ࠤࡸࡲࡩ࡫ࡦࡪࡰࡨࡨࠧḝ") and str(self.bstack1l11111lll_opy_).lower() == bstack1l1l1l1_opy_ (u"ࠥࡸࡷࡻࡥࠣḞ"):
          self.bstack111lll111_opy_ = True
        if bstack1l1l1l1_opy_ (u"ࠦࡹࡵ࡫ࡦࡰࠥḟ") in data:
          return data[bstack1l1l1l1_opy_ (u"ࠧࡺ࡯࡬ࡧࡱࠦḠ")]
        else:
          raise bstack1l1l1l1_opy_ (u"࠭ࡔࡰ࡭ࡨࡲࠥࡔ࡯ࡵࠢࡉࡳࡺࡴࡤࠡ࠯ࠣࡿࢂ࠭ḡ").format(data)
      else:
        raise bstack1l1l1l1_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡳࡩࡷࡩࡹࠡࡶࡲ࡯ࡪࡴࠬࠡࡔࡨࡷࡵࡵ࡮ࡴࡧࠣࡷࡹࡧࡴࡶࡵࠣ࠱ࠥࢁࡽ࠭ࠢࡕࡩࡸࡶ࡯࡯ࡵࡨࠤࡇࡵࡤࡺࠢ࠰ࠤࢀࢃࠢḢ").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack1l1l1l1_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡤࡴࡨࡥࡹ࡯࡮ࡨࠢࡳࡩࡷࡩࡹࠡࡲࡵࡳ࡯࡫ࡣࡵࠤḣ").format(e))
  def bstack1111l1l1lll_opy_(self):
    bstack1111lll1l1l_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1l1l1_opy_ (u"ࠤࡳࡩࡷࡩࡹࡄࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠧḤ"))
    try:
      if bstack1l1l1l1_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࠫḥ") not in self.bstack1111ll1ll11_opy_:
        self.bstack1111ll1ll11_opy_[bstack1l1l1l1_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࠬḦ")] = 2
      with open(bstack1111lll1l1l_opy_, bstack1l1l1l1_opy_ (u"ࠬࡽࠧḧ")) as fp:
        json.dump(self.bstack1111ll1ll11_opy_, fp)
      return bstack1111lll1l1l_opy_
    except Exception as e:
      self.logger.error(bstack1l1l1l1_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡦࡶࡪࡧࡴࡦࠢࡳࡩࡷࡩࡹࠡࡥࡲࡲ࡫࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡿࢂࠨḨ").format(e))
  def bstack1111llllll1_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack1111ll11l1l_opy_ == bstack1l1l1l1_opy_ (u"ࠧࡸ࡫ࡱࠫḩ"):
        bstack1111ll11l11_opy_ = [bstack1l1l1l1_opy_ (u"ࠨࡥࡰࡨ࠳࡫ࡸࡦࠩḪ"), bstack1l1l1l1_opy_ (u"ࠩ࠲ࡧࠬḫ")]
        cmd = bstack1111ll11l11_opy_ + cmd
      cmd = bstack1l1l1l1_opy_ (u"ࠪࠤࠬḬ").join(cmd)
      self.logger.debug(bstack1l1l1l1_opy_ (u"ࠦࡗࡻ࡮࡯࡫ࡱ࡫ࠥࢁࡽࠣḭ").format(cmd))
      with open(self.bstack1111ll1l111_opy_, bstack1l1l1l1_opy_ (u"ࠧࡧࠢḮ")) as bstack1111ll111ll_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack1111ll111ll_opy_, text=True, stderr=bstack1111ll111ll_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack1111lllll11_opy_ = True
      self.logger.error(bstack1l1l1l1_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡲࡨࡶࡨࡿࠠࡸ࡫ࡷ࡬ࠥࡩ࡭ࡥࠢ࠰ࠤࢀࢃࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱ࠾ࠥࢁࡽࠣḯ").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack1111ll11ll1_opy_:
        self.logger.info(bstack1l1l1l1_opy_ (u"ࠢࡔࡶࡲࡴࡵ࡯࡮ࡨࠢࡓࡩࡷࡩࡹࠣḰ"))
        cmd = [self.binary_path, bstack1l1l1l1_opy_ (u"ࠣࡧࡻࡩࡨࡀࡳࡵࡱࡳࠦḱ")]
        self.bstack1111llllll1_opy_(cmd)
        self.bstack1111ll11ll1_opy_ = False
    except Exception as e:
      self.logger.error(bstack1l1l1l1_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡴࡰࡲࠣࡷࡪࡹࡳࡪࡱࡱࠤࡼ࡯ࡴࡩࠢࡦࡳࡲࡳࡡ࡯ࡦࠣ࠱ࠥࢁࡽ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲ࠿ࠦࡻࡾࠤḲ").format(cmd, e))
  def bstack1l1111l1l1_opy_(self):
    if not self.bstack1l11111lll_opy_:
      return
    try:
      bstack111l111ll11_opy_ = 0
      while not self.bstack1111ll11ll1_opy_ and bstack111l111ll11_opy_ < self.bstack111l11l111l_opy_:
        if self.bstack1111lllll11_opy_:
          self.logger.info(bstack1l1l1l1_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡶࡩࡹࡻࡰࠡࡨࡤ࡭ࡱ࡫ࡤࠣḳ"))
          return
        time.sleep(1)
        bstack111l111ll11_opy_ += 1
      os.environ[bstack1l1l1l1_opy_ (u"ࠫࡕࡋࡒࡄ࡛ࡢࡆࡊ࡙ࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࠪḴ")] = str(self.bstack1111ll1llll_opy_())
      self.logger.info(bstack1l1l1l1_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡸ࡫ࡴࡶࡲࠣࡧࡴࡳࡰ࡭ࡧࡷࡩࡩࠨḵ"))
    except Exception as e:
      self.logger.error(bstack1l1l1l1_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡩࡹࡻࡰࠡࡲࡨࡶࡨࡿࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢḶ").format(e))
  def bstack1111ll1llll_opy_(self):
    if self.bstack1lll1111_opy_:
      return
    try:
      bstack1111l1l1ll1_opy_ = [platform[bstack1l1l1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬḷ")].lower() for platform in self.config.get(bstack1l1l1l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫḸ"), [])]
      bstack1111lll1l11_opy_ = sys.maxsize
      bstack1111llll1ll_opy_ = bstack1l1l1l1_opy_ (u"ࠩࠪḹ")
      for browser in bstack1111l1l1ll1_opy_:
        if browser in self.bstack111l11l1ll1_opy_:
          bstack1111lll11l1_opy_ = self.bstack111l11l1ll1_opy_[browser]
        if bstack1111lll11l1_opy_ < bstack1111lll1l11_opy_:
          bstack1111lll1l11_opy_ = bstack1111lll11l1_opy_
          bstack1111llll1ll_opy_ = browser
      return bstack1111llll1ll_opy_
    except Exception as e:
      self.logger.error(bstack1l1l1l1_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡪࡰࡧࠤࡧ࡫ࡳࡵࠢࡳࡰࡦࡺࡦࡰࡴࡰ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦḺ").format(e))
  @classmethod
  def bstack1l111l11_opy_(self):
    return os.getenv(bstack1l1l1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡊࡘࡃ࡚ࠩḻ"), bstack1l1l1l1_opy_ (u"ࠬࡌࡡ࡭ࡵࡨࠫḼ")).lower()
  @classmethod
  def bstack111l1ll11_opy_(self):
    return os.getenv(bstack1l1l1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡅࡓࡅ࡜ࡣࡈࡇࡐࡕࡗࡕࡉࡤࡓࡏࡅࡇࠪḽ"), bstack1l1l1l1_opy_ (u"ࠧࠨḾ"))
  @classmethod
  def bstack1l1l1ll1l1l_opy_(cls, value):
    cls.bstack111lll111_opy_ = value
  @classmethod
  def bstack1111lll1lll_opy_(cls):
    return cls.bstack111lll111_opy_
  @classmethod
  def bstack1l1l1ll1ll1_opy_(cls, value):
    cls.percy_build_id = value
  @classmethod
  def bstack1111l1ll1l1_opy_(cls):
    return cls.percy_build_id