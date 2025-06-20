# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1ll1ll_opy_ = 2048
bstack1l1l11l_opy_ = 7
def bstack11ll11_opy_ (bstack11l1lll_opy_):
    global bstack1l1l_opy_
    bstack1lll111_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1lll_opy_ = bstack11l1lll_opy_ [:-1]
    bstack1ll1lll_opy_ = bstack1lll111_opy_ % len (bstack1l1lll_opy_)
    bstack11l1l11_opy_ = bstack1l1lll_opy_ [:bstack1ll1lll_opy_] + bstack1l1lll_opy_ [bstack1ll1lll_opy_:]
    if bstack1ll1l1l_opy_:
        bstack111l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    else:
        bstack111l_opy_ = str () .join ([chr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    return eval (bstack111l_opy_)
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
from bstack_utils.helper import bstack1llll1ll_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack11l1111ll1_opy_ import bstack11ll11l1ll_opy_
class bstack1l1111ll1_opy_:
  working_dir = os.getcwd()
  bstack1lll1l111l_opy_ = False
  config = {}
  bstack11l1111lll1_opy_ = bstack11ll11_opy_ (u"ࠩࠪᶻ")
  binary_path = bstack11ll11_opy_ (u"ࠪࠫᶼ")
  bstack1111ll1llll_opy_ = bstack11ll11_opy_ (u"ࠫࠬᶽ")
  bstack1lll1l1111_opy_ = False
  bstack1111llll11l_opy_ = None
  bstack1111lll11ll_opy_ = {}
  bstack111l111l111_opy_ = 300
  bstack1111lll111l_opy_ = False
  logger = None
  bstack111l111ll11_opy_ = False
  bstack11l1ll11l_opy_ = False
  percy_build_id = None
  bstack111l1111l1l_opy_ = bstack11ll11_opy_ (u"ࠬ࠭ᶾ")
  bstack111l11l1ll1_opy_ = {
    bstack11ll11_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭ᶿ") : 1,
    bstack11ll11_opy_ (u"ࠧࡧ࡫ࡵࡩ࡫ࡵࡸࠨ᷀") : 2,
    bstack11ll11_opy_ (u"ࠨࡧࡧ࡫ࡪ࠭᷁") : 3,
    bstack11ll11_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪ᷂ࠩ") : 4
  }
  def __init__(self) -> None: pass
  def bstack1111lll1111_opy_(self):
    bstack111l11l111l_opy_ = bstack11ll11_opy_ (u"ࠪࠫ᷃")
    bstack111l111l1l1_opy_ = sys.platform
    bstack1111lll1lll_opy_ = bstack11ll11_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪ᷄")
    if re.match(bstack11ll11_opy_ (u"ࠧࡪࡡࡳࡹ࡬ࡲࢁࡳࡡࡤࠢࡲࡷࠧ᷅"), bstack111l111l1l1_opy_) != None:
      bstack111l11l111l_opy_ = bstack11l1llll1l1_opy_ + bstack11ll11_opy_ (u"ࠨ࠯ࡱࡧࡵࡧࡾ࠳࡯ࡴࡺ࠱ࡾ࡮ࡶࠢ᷆")
      self.bstack111l1111l1l_opy_ = bstack11ll11_opy_ (u"ࠧ࡮ࡣࡦࠫ᷇")
    elif re.match(bstack11ll11_opy_ (u"ࠣ࡯ࡶࡻ࡮ࡴࡼ࡮ࡵࡼࡷࢁࡳࡩ࡯ࡩࡺࢀࡨࡿࡧࡸ࡫ࡱࢀࡧࡩࡣࡸ࡫ࡱࢀࡼ࡯࡮ࡤࡧࡿࡩࡲࡩࡼࡸ࡫ࡱ࠷࠷ࠨ᷈"), bstack111l111l1l1_opy_) != None:
      bstack111l11l111l_opy_ = bstack11l1llll1l1_opy_ + bstack11ll11_opy_ (u"ࠤ࠲ࡴࡪࡸࡣࡺ࠯ࡺ࡭ࡳ࠴ࡺࡪࡲࠥ᷉")
      bstack1111lll1lll_opy_ = bstack11ll11_opy_ (u"ࠥࡴࡪࡸࡣࡺ࠰ࡨࡼࡪࠨ᷊")
      self.bstack111l1111l1l_opy_ = bstack11ll11_opy_ (u"ࠫࡼ࡯࡮ࠨ᷋")
    else:
      bstack111l11l111l_opy_ = bstack11l1llll1l1_opy_ + bstack11ll11_opy_ (u"ࠧ࠵ࡰࡦࡴࡦࡽ࠲ࡲࡩ࡯ࡷࡻ࠲ࡿ࡯ࡰࠣ᷌")
      self.bstack111l1111l1l_opy_ = bstack11ll11_opy_ (u"࠭࡬ࡪࡰࡸࡼࠬ᷍")
    return bstack111l11l111l_opy_, bstack1111lll1lll_opy_
  def bstack1111ll11l1l_opy_(self):
    try:
      bstack1111lllllll_opy_ = [os.path.join(expanduser(bstack11ll11_opy_ (u"ࠢࡿࠤ᷎")), bstack11ll11_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ᷏")), self.working_dir, tempfile.gettempdir()]
      for path in bstack1111lllllll_opy_:
        if(self.bstack111l111l11l_opy_(path)):
          return path
      raise bstack11ll11_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠠࡱࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠨ᷐")
    except Exception as e:
      self.logger.error(bstack11ll11_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡦࡪࡰࡧࠤࡦࡼࡡࡪ࡮ࡤࡦࡱ࡫ࠠࡱࡣࡷ࡬ࠥ࡬࡯ࡳࠢࡳࡩࡷࡩࡹࠡࡦࡲࡻࡳࡲ࡯ࡢࡦ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠ࠮ࠢࡾࢁࠧ᷑").format(e))
  def bstack111l111l11l_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack1111ll1lll1_opy_(self, bstack1111l1l1lll_opy_):
    return os.path.join(bstack1111l1l1lll_opy_, self.bstack11l1111lll1_opy_ + bstack11ll11_opy_ (u"ࠦ࠳࡫ࡴࡢࡩࠥ᷒"))
  def bstack1111llll111_opy_(self, bstack1111l1l1lll_opy_, bstack111l11l11l1_opy_):
    if not bstack111l11l11l1_opy_: return
    try:
      bstack111l11111ll_opy_ = self.bstack1111ll1lll1_opy_(bstack1111l1l1lll_opy_)
      with open(bstack111l11111ll_opy_, bstack11ll11_opy_ (u"ࠧࡽࠢᷓ")) as f:
        f.write(bstack111l11l11l1_opy_)
        self.logger.debug(bstack11ll11_opy_ (u"ࠨࡓࡢࡸࡨࡨࠥࡴࡥࡸࠢࡈࡘࡦ࡭ࠠࡧࡱࡵࠤࡵ࡫ࡲࡤࡻࠥᷔ"))
    except Exception as e:
      self.logger.error(bstack11ll11_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡦࡼࡥࠡࡶ࡫ࡩࠥ࡫ࡴࡢࡩ࠯ࠤࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠢᷕ").format(e))
  def bstack1111lll11l1_opy_(self, bstack1111l1l1lll_opy_):
    try:
      bstack111l11111ll_opy_ = self.bstack1111ll1lll1_opy_(bstack1111l1l1lll_opy_)
      if os.path.exists(bstack111l11111ll_opy_):
        with open(bstack111l11111ll_opy_, bstack11ll11_opy_ (u"ࠣࡴࠥᷖ")) as f:
          bstack111l11l11l1_opy_ = f.read().strip()
          return bstack111l11l11l1_opy_ if bstack111l11l11l1_opy_ else None
    except Exception as e:
      self.logger.error(bstack11ll11_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢ࡯ࡳࡦࡪࡩ࡯ࡩࠣࡉ࡙ࡧࡧ࠭ࠢࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠧᷗ").format(e))
  def bstack111l111llll_opy_(self, bstack1111l1l1lll_opy_, bstack111l11l111l_opy_):
    bstack1111l1ll11l_opy_ = self.bstack1111lll11l1_opy_(bstack1111l1l1lll_opy_)
    if bstack1111l1ll11l_opy_:
      try:
        bstack1111ll1l11l_opy_ = self.bstack1111ll11l11_opy_(bstack1111l1ll11l_opy_, bstack111l11l111l_opy_)
        if not bstack1111ll1l11l_opy_:
          self.logger.debug(bstack11ll11_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠢ࡬ࡷࠥࡻࡰࠡࡶࡲࠤࡩࡧࡴࡦࠢࠫࡉ࡙ࡧࡧࠡࡷࡱࡧ࡭ࡧ࡮ࡨࡧࡧ࠭ࠧᷘ"))
          return True
        self.logger.debug(bstack11ll11_opy_ (u"ࠦࡓ࡫ࡷࠡࡒࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࡣࡹࡥ࡮ࡲࡡࡣ࡮ࡨ࠰ࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࡩ࡯ࡩࠣࡹࡵࡪࡡࡵࡧࠥᷙ"))
        return False
      except Exception as e:
        self.logger.warn(bstack11ll11_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡥ࡫ࡩࡨࡱࠠࡧࡱࡵࠤࡧ࡯࡮ࡢࡴࡼࠤࡺࡶࡤࡢࡶࡨࡷ࠱ࠦࡵࡴ࡫ࡱ࡫ࠥ࡫ࡸࡪࡵࡷ࡭ࡳ࡭ࠠࡣ࡫ࡱࡥࡷࡿ࠺ࠡࡽࢀࠦᷚ").format(e))
    return False
  def bstack1111ll11l11_opy_(self, bstack1111l1ll11l_opy_, bstack111l11l111l_opy_):
    try:
      headers = {
        bstack11ll11_opy_ (u"ࠨࡉࡧ࠯ࡑࡳࡳ࡫࠭ࡎࡣࡷࡧ࡭ࠨᷛ"): bstack1111l1ll11l_opy_
      }
      response = bstack1llll1ll_opy_(bstack11ll11_opy_ (u"ࠧࡈࡇࡗࠫᷜ"), bstack111l11l111l_opy_, {}, {bstack11ll11_opy_ (u"ࠣࡪࡨࡥࡩ࡫ࡲࡴࠤᷝ"): headers})
      if response.status_code == 304:
        return False
      return True
    except Exception as e:
      raise(bstack11ll11_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡥ࡫ࡩࡨࡱࡩ࡯ࡩࠣࡪࡴࡸࠠࡑࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠦࡵࡱࡦࡤࡸࡪࡹ࠺ࠡࡽࢀࠦᷞ").format(e))
  @measure(event_name=EVENTS.bstack11l1ll1lll1_opy_, stage=STAGE.bstack1lll11llll_opy_)
  def bstack111l111111l_opy_(self, bstack111l11l111l_opy_, bstack1111lll1lll_opy_):
    try:
      bstack1111llll1ll_opy_ = self.bstack1111ll11l1l_opy_()
      bstack111l1111ll1_opy_ = os.path.join(bstack1111llll1ll_opy_, bstack11ll11_opy_ (u"ࠪࡴࡪࡸࡣࡺ࠰ࡽ࡭ࡵ࠭ᷟ"))
      bstack1111l1l1l1l_opy_ = os.path.join(bstack1111llll1ll_opy_, bstack1111lll1lll_opy_)
      if self.bstack111l111llll_opy_(bstack1111llll1ll_opy_, bstack111l11l111l_opy_): # if bstack1111lll1l11_opy_, bstack1l1l1l11lll_opy_ bstack111l11l11l1_opy_ is bstack111l111ll1l_opy_ to bstack11l11111l1l_opy_ version available (response 304)
        if os.path.exists(bstack1111l1l1l1l_opy_):
          self.logger.info(bstack11ll11_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠣࡪࡴࡻ࡮ࡥࠢ࡬ࡲࠥࢁࡽ࠭ࠢࡶ࡯࡮ࡶࡰࡪࡰࡪࠤࡩࡵࡷ࡯࡮ࡲࡥࡩࠨᷠ").format(bstack1111l1l1l1l_opy_))
          return bstack1111l1l1l1l_opy_
        if os.path.exists(bstack111l1111ll1_opy_):
          self.logger.info(bstack11ll11_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡿ࡯ࡰࠡࡨࡲࡹࡳࡪࠠࡪࡰࠣࡿࢂ࠲ࠠࡶࡰࡽ࡭ࡵࡶࡩ࡯ࡩࠥᷡ").format(bstack111l1111ll1_opy_))
          return self.bstack1111l1llll1_opy_(bstack111l1111ll1_opy_, bstack1111lll1lll_opy_)
      self.logger.info(bstack11ll11_opy_ (u"ࠨࡄࡰࡹࡱࡰࡴࡧࡤࡪࡰࡪࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠣࡪࡷࡵ࡭ࠡࡽࢀࠦᷢ").format(bstack111l11l111l_opy_))
      response = bstack1llll1ll_opy_(bstack11ll11_opy_ (u"ࠧࡈࡇࡗࠫᷣ"), bstack111l11l111l_opy_, {}, {})
      if response.status_code == 200:
        bstack1111ll1ll1l_opy_ = response.headers.get(bstack11ll11_opy_ (u"ࠣࡇࡗࡥ࡬ࠨᷤ"), bstack11ll11_opy_ (u"ࠤࠥᷥ"))
        if bstack1111ll1ll1l_opy_:
          self.bstack1111llll111_opy_(bstack1111llll1ll_opy_, bstack1111ll1ll1l_opy_)
        with open(bstack111l1111ll1_opy_, bstack11ll11_opy_ (u"ࠪࡻࡧ࠭ᷦ")) as file:
          file.write(response.content)
        self.logger.info(bstack11ll11_opy_ (u"ࠦࡉࡵࡷ࡯࡮ࡲࡥࡩ࡫ࡤࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠠࡢࡰࡧࠤࡸࡧࡶࡦࡦࠣࡥࡹࠦࡻࡾࠤᷧ").format(bstack111l1111ll1_opy_))
        return self.bstack1111l1llll1_opy_(bstack111l1111ll1_opy_, bstack1111lll1lll_opy_)
      else:
        raise(bstack11ll11_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡦࡲࡻࡳࡲ࡯ࡢࡦࠣࡸ࡭࡫ࠠࡧ࡫࡯ࡩ࠳ࠦࡓࡵࡣࡷࡹࡸࠦࡣࡰࡦࡨ࠾ࠥࢁࡽࠣᷨ").format(response.status_code))
    except Exception as e:
      self.logger.error(bstack11ll11_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻ࠽ࠤࢀࢃࠢᷩ").format(e))
  def bstack1111lllll11_opy_(self, bstack111l11l111l_opy_, bstack1111lll1lll_opy_):
    try:
      retry = 2
      bstack1111l1l1l1l_opy_ = None
      bstack111l111lll1_opy_ = False
      while retry > 0:
        bstack1111l1l1l1l_opy_ = self.bstack111l111111l_opy_(bstack111l11l111l_opy_, bstack1111lll1lll_opy_)
        bstack111l111lll1_opy_ = self.bstack1111ll1111l_opy_(bstack111l11l111l_opy_, bstack1111lll1lll_opy_, bstack1111l1l1l1l_opy_)
        if bstack111l111lll1_opy_:
          break
        retry -= 1
      return bstack1111l1l1l1l_opy_, bstack111l111lll1_opy_
    except Exception as e:
      self.logger.error(bstack11ll11_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣ࡫ࡪࡺࠠࡱࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠦࡰࡢࡶ࡫ࠦᷪ").format(e))
    return bstack1111l1l1l1l_opy_, False
  def bstack1111ll1111l_opy_(self, bstack111l11l111l_opy_, bstack1111lll1lll_opy_, bstack1111l1l1l1l_opy_, bstack111l11111l1_opy_ = 0):
    if bstack111l11111l1_opy_ > 1:
      return False
    if bstack1111l1l1l1l_opy_ == None or os.path.exists(bstack1111l1l1l1l_opy_) == False:
      self.logger.warn(bstack11ll11_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡱࡣࡷ࡬ࠥࡴ࡯ࡵࠢࡩࡳࡺࡴࡤ࠭ࠢࡵࡩࡹࡸࡹࡪࡰࡪࠤࡩࡵࡷ࡯࡮ࡲࡥࡩࠨᷫ"))
      return False
    bstack1111ll1l1ll_opy_ = bstack11ll11_opy_ (u"ࡴࠥࡢ࠳࠰ࡀࡱࡧࡵࡧࡾ࠵ࡣ࡭࡫ࠣࡠࡩ࠱࡜࠯࡞ࡧ࠯ࡡ࠴࡜ࡥ࠭ࠥᷬ")
    command = bstack11ll11_opy_ (u"ࠪࡿࢂࠦ࠭࠮ࡸࡨࡶࡸ࡯࡯࡯ࠩᷭ").format(bstack1111l1l1l1l_opy_)
    bstack111l1111111_opy_ = subprocess.check_output(command, shell=True, text=True)
    if re.match(bstack1111ll1l1ll_opy_, bstack111l1111111_opy_) != None:
      return True
    else:
      self.logger.error(bstack11ll11_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡺࡪࡸࡳࡪࡱࡱࠤࡨ࡮ࡥࡤ࡭ࠣࡪࡦ࡯࡬ࡦࡦࠥᷮ"))
      return False
  def bstack1111l1llll1_opy_(self, bstack111l1111ll1_opy_, bstack1111lll1lll_opy_):
    try:
      working_dir = os.path.dirname(bstack111l1111ll1_opy_)
      shutil.unpack_archive(bstack111l1111ll1_opy_, working_dir)
      bstack1111l1l1l1l_opy_ = os.path.join(working_dir, bstack1111lll1lll_opy_)
      os.chmod(bstack1111l1l1l1l_opy_, 0o755)
      return bstack1111l1l1l1l_opy_
    except Exception as e:
      self.logger.error(bstack11ll11_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡷࡱࡾ࡮ࡶࠠࡱࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠨᷯ"))
  def bstack111l11l1l11_opy_(self):
    try:
      bstack1111l1ll1l1_opy_ = self.config.get(bstack11ll11_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬᷰ"))
      bstack111l11l1l11_opy_ = bstack1111l1ll1l1_opy_ or (bstack1111l1ll1l1_opy_ is None and self.bstack1lll1l111l_opy_)
      if not bstack111l11l1l11_opy_ or self.config.get(bstack11ll11_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪᷱ"), None) not in bstack11l1lll1l11_opy_:
        return False
      self.bstack1lll1l1111_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack11ll11_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡩ࡫ࡴࡦࡥࡷࠤࡵ࡫ࡲࡤࡻ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿࠥᷲ").format(e))
  def bstack1111lll1ll1_opy_(self):
    try:
      bstack1111lll1ll1_opy_ = self.percy_capture_mode
      return bstack1111lll1ll1_opy_
    except Exception as e:
      self.logger.error(bstack11ll11_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡪࡥࡵࡧࡦࡸࠥࡶࡥࡳࡥࡼࠤࡨࡧࡰࡵࡷࡵࡩࠥࡳ࡯ࡥࡧ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿࠥᷳ").format(e))
  def init(self, bstack1lll1l111l_opy_, config, logger):
    self.bstack1lll1l111l_opy_ = bstack1lll1l111l_opy_
    self.config = config
    self.logger = logger
    if not self.bstack111l11l1l11_opy_():
      return
    self.bstack1111lll11ll_opy_ = config.get(bstack11ll11_opy_ (u"ࠪࡴࡪࡸࡣࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩᷴ"), {})
    self.percy_capture_mode = config.get(bstack11ll11_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡆࡥࡵࡺࡵࡳࡧࡐࡳࡩ࡫ࠧ᷵"))
    try:
      bstack111l11l111l_opy_, bstack1111lll1lll_opy_ = self.bstack1111lll1111_opy_()
      self.bstack11l1111lll1_opy_ = bstack1111lll1lll_opy_
      bstack1111l1l1l1l_opy_, bstack111l111lll1_opy_ = self.bstack1111lllll11_opy_(bstack111l11l111l_opy_, bstack1111lll1lll_opy_)
      if bstack111l111lll1_opy_:
        self.binary_path = bstack1111l1l1l1l_opy_
        thread = Thread(target=self.bstack1111lll1l1l_opy_)
        thread.start()
      else:
        self.bstack111l111ll11_opy_ = True
        self.logger.error(bstack11ll11_opy_ (u"ࠧࡏ࡮ࡷࡣ࡯࡭ࡩࠦࡰࡦࡴࡦࡽࠥࡶࡡࡵࡪࠣࡪࡴࡻ࡮ࡥࠢ࠰ࠤࢀࢃࠬࠡࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺࡡࡳࡶࠣࡔࡪࡸࡣࡺࠤ᷶").format(bstack1111l1l1l1l_opy_))
    except Exception as e:
      self.logger.error(bstack11ll11_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡲࡨࡶࡨࡿࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃ᷷ࠢ").format(e))
  def bstack1111l1ll1ll_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack11ll11_opy_ (u"ࠧ࡭ࡱࡪ᷸ࠫ"), bstack11ll11_opy_ (u"ࠨࡲࡨࡶࡨࡿ࠮࡭ࡱࡪ᷹ࠫ"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack11ll11_opy_ (u"ࠤࡓࡹࡸ࡮ࡩ࡯ࡩࠣࡴࡪࡸࡣࡺࠢ࡯ࡳ࡬ࡹࠠࡢࡶࠣࡿࢂࠨ᷺").format(logfile))
      self.bstack1111ll1llll_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack11ll11_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡦࡶࠣࡴࡪࡸࡣࡺࠢ࡯ࡳ࡬ࠦࡰࡢࡶ࡫࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦ᷻").format(e))
  @measure(event_name=EVENTS.bstack11l1llll11l_opy_, stage=STAGE.bstack1lll11llll_opy_)
  def bstack1111lll1l1l_opy_(self):
    bstack1111l1lll1l_opy_ = self.bstack1111l1lllll_opy_()
    if bstack1111l1lll1l_opy_ == None:
      self.bstack111l111ll11_opy_ = True
      self.logger.error(bstack11ll11_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡸࡴࡱࡥ࡯ࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨ࠱ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡲࡨࡶࡨࡿࠢ᷼"))
      return False
    command_args = [bstack11ll11_opy_ (u"ࠧࡧࡰࡱ࠼ࡨࡼࡪࡩ࠺ࡴࡶࡤࡶࡹࠨ᷽") if self.bstack1lll1l111l_opy_ else bstack11ll11_opy_ (u"࠭ࡥࡹࡧࡦ࠾ࡸࡺࡡࡳࡶࠪ᷾")]
    bstack111ll1ll1ll_opy_ = self.bstack111l11l11ll_opy_()
    if bstack111ll1ll1ll_opy_ != None:
      command_args.append(bstack11ll11_opy_ (u"ࠢ࠮ࡥࠣࡿࢂࠨ᷿").format(bstack111ll1ll1ll_opy_))
    env = os.environ.copy()
    env[bstack11ll11_opy_ (u"ࠣࡒࡈࡖࡈ࡟࡟ࡕࡑࡎࡉࡓࠨḀ")] = bstack1111l1lll1l_opy_
    env[bstack11ll11_opy_ (u"ࠤࡗࡌࡤࡈࡕࡊࡎࡇࡣ࡚࡛ࡉࡅࠤḁ")] = os.environ.get(bstack11ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨḂ"), bstack11ll11_opy_ (u"ࠫࠬḃ"))
    bstack1111ll11111_opy_ = [self.binary_path]
    self.bstack1111l1ll1ll_opy_()
    self.bstack1111llll11l_opy_ = self.bstack111l111l1ll_opy_(bstack1111ll11111_opy_ + command_args, env)
    self.logger.debug(bstack11ll11_opy_ (u"࡙ࠧࡴࡢࡴࡷ࡭ࡳ࡭ࠠࡉࡧࡤࡰࡹ࡮ࠠࡄࡪࡨࡧࡰࠨḄ"))
    bstack111l11111l1_opy_ = 0
    while self.bstack1111llll11l_opy_.poll() == None:
      bstack1111llll1l1_opy_ = self.bstack111l1111lll_opy_()
      if bstack1111llll1l1_opy_:
        self.logger.debug(bstack11ll11_opy_ (u"ࠨࡈࡦࡣ࡯ࡸ࡭ࠦࡃࡩࡧࡦ࡯ࠥࡹࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭ࠤḅ"))
        self.bstack1111lll111l_opy_ = True
        return True
      bstack111l11111l1_opy_ += 1
      self.logger.debug(bstack11ll11_opy_ (u"ࠢࡉࡧࡤࡰࡹ࡮ࠠࡄࡪࡨࡧࡰࠦࡒࡦࡶࡵࡽࠥ࠳ࠠࡼࡿࠥḆ").format(bstack111l11111l1_opy_))
      time.sleep(2)
    self.logger.error(bstack11ll11_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸࡺࡡࡳࡶࠣࡴࡪࡸࡣࡺ࠮ࠣࡌࡪࡧ࡬ࡵࡪࠣࡇ࡭࡫ࡣ࡬ࠢࡉࡥ࡮ࡲࡥࡥࠢࡤࡪࡹ࡫ࡲࠡࡽࢀࠤࡦࡺࡴࡦ࡯ࡳࡸࡸࠨḇ").format(bstack111l11111l1_opy_))
    self.bstack111l111ll11_opy_ = True
    return False
  def bstack111l1111lll_opy_(self, bstack111l11111l1_opy_ = 0):
    if bstack111l11111l1_opy_ > 10:
      return False
    try:
      bstack1111ll11ll1_opy_ = os.environ.get(bstack11ll11_opy_ (u"ࠩࡓࡉࡗࡉ࡙ࡠࡕࡈࡖ࡛ࡋࡒࡠࡃࡇࡈࡗࡋࡓࡔࠩḈ"), bstack11ll11_opy_ (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲ࡰࡴࡩࡡ࡭ࡪࡲࡷࡹࡀ࠵࠴࠵࠻ࠫḉ"))
      bstack1111l1lll11_opy_ = bstack1111ll11ll1_opy_ + bstack11ll11l1111_opy_
      response = requests.get(bstack1111l1lll11_opy_)
      data = response.json()
      self.percy_build_id = data.get(bstack11ll11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࠪḊ"), {}).get(bstack11ll11_opy_ (u"ࠬ࡯ࡤࠨḋ"), None)
      return True
    except:
      self.logger.debug(bstack11ll11_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡵࡣࡤࡷࡵࡶࡪࡪࠠࡸࡪ࡬ࡰࡪࠦࡰࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣ࡬ࡪࡧ࡬ࡵࡪࠣࡧ࡭࡫ࡣ࡬ࠢࡵࡩࡸࡶ࡯࡯ࡵࡨࠦḌ"))
      return False
  def bstack1111l1lllll_opy_(self):
    bstack1111l1l1ll1_opy_ = bstack11ll11_opy_ (u"ࠧࡢࡲࡳࠫḍ") if self.bstack1lll1l111l_opy_ else bstack11ll11_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪḎ")
    bstack1111ll11lll_opy_ = bstack11ll11_opy_ (u"ࠤࡸࡲࡩ࡫ࡦࡪࡰࡨࡨࠧḏ") if self.config.get(bstack11ll11_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩḐ")) is None else True
    bstack11ll1l11l11_opy_ = bstack11ll11_opy_ (u"ࠦࡦࡶࡩ࠰ࡣࡳࡴࡤࡶࡥࡳࡥࡼ࠳࡬࡫ࡴࡠࡲࡵࡳ࡯࡫ࡣࡵࡡࡷࡳࡰ࡫࡮ࡀࡰࡤࡱࡪࡃࡻࡾࠨࡷࡽࡵ࡫࠽ࡼࡿࠩࡴࡪࡸࡣࡺ࠿ࡾࢁࠧḑ").format(self.config[bstack11ll11_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪḒ")], bstack1111l1l1ll1_opy_, bstack1111ll11lll_opy_)
    if self.percy_capture_mode:
      bstack11ll1l11l11_opy_ += bstack11ll11_opy_ (u"ࠨࠦࡱࡧࡵࡧࡾࡥࡣࡢࡲࡷࡹࡷ࡫࡟࡮ࡱࡧࡩࡂࢁࡽࠣḓ").format(self.percy_capture_mode)
    uri = bstack11ll11l1ll_opy_(bstack11ll1l11l11_opy_)
    try:
      response = bstack1llll1ll_opy_(bstack11ll11_opy_ (u"ࠧࡈࡇࡗࠫḔ"), uri, {}, {bstack11ll11_opy_ (u"ࠨࡣࡸࡸ࡭࠭ḕ"): (self.config[bstack11ll11_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫḖ")], self.config[bstack11ll11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ḗ")])})
      if response.status_code == 200:
        data = response.json()
        self.bstack1lll1l1111_opy_ = data.get(bstack11ll11_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬḘ"))
        self.percy_capture_mode = data.get(bstack11ll11_opy_ (u"ࠬࡶࡥࡳࡥࡼࡣࡨࡧࡰࡵࡷࡵࡩࡤࡳ࡯ࡥࡧࠪḙ"))
        os.environ[bstack11ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡅࡓࡅ࡜ࠫḚ")] = str(self.bstack1lll1l1111_opy_)
        os.environ[bstack11ll11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡆࡔࡆ࡝ࡤࡉࡁࡑࡖࡘࡖࡊࡥࡍࡐࡆࡈࠫḛ")] = str(self.percy_capture_mode)
        if bstack1111ll11lll_opy_ == bstack11ll11_opy_ (u"ࠣࡷࡱࡨࡪ࡬ࡩ࡯ࡧࡧࠦḜ") and str(self.bstack1lll1l1111_opy_).lower() == bstack11ll11_opy_ (u"ࠤࡷࡶࡺ࡫ࠢḝ"):
          self.bstack11l1ll11l_opy_ = True
        if bstack11ll11_opy_ (u"ࠥࡸࡴࡱࡥ࡯ࠤḞ") in data:
          return data[bstack11ll11_opy_ (u"ࠦࡹࡵ࡫ࡦࡰࠥḟ")]
        else:
          raise bstack11ll11_opy_ (u"࡚ࠬ࡯࡬ࡧࡱࠤࡓࡵࡴࠡࡈࡲࡹࡳࡪࠠ࠮ࠢࡾࢁࠬḠ").format(data)
      else:
        raise bstack11ll11_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡩࡩࡹࡩࡨࠡࡲࡨࡶࡨࡿࠠࡵࡱ࡮ࡩࡳ࠲ࠠࡓࡧࡶࡴࡴࡴࡳࡦࠢࡶࡸࡦࡺࡵࡴࠢ࠰ࠤࢀࢃࠬࠡࡔࡨࡷࡵࡵ࡮ࡴࡧࠣࡆࡴࡪࡹࠡ࠯ࠣࡿࢂࠨḡ").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack11ll11_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡣࡳࡧࡤࡸ࡮ࡴࡧࠡࡲࡨࡶࡨࡿࠠࡱࡴࡲ࡮ࡪࡩࡴࠣḢ").format(e))
  def bstack111l11l11ll_opy_(self):
    bstack1111l1ll111_opy_ = os.path.join(tempfile.gettempdir(), bstack11ll11_opy_ (u"ࠣࡲࡨࡶࡨࡿࡃࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠦḣ"))
    try:
      if bstack11ll11_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࠪḤ") not in self.bstack1111lll11ll_opy_:
        self.bstack1111lll11ll_opy_[bstack11ll11_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࠫḥ")] = 2
      with open(bstack1111l1ll111_opy_, bstack11ll11_opy_ (u"ࠫࡼ࠭Ḧ")) as fp:
        json.dump(self.bstack1111lll11ll_opy_, fp)
      return bstack1111l1ll111_opy_
    except Exception as e:
      self.logger.error(bstack11ll11_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡥࡵࡩࡦࡺࡥࠡࡲࡨࡶࡨࡿࠠࡤࡱࡱࡪ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧḧ").format(e))
  def bstack111l111l1ll_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack111l1111l1l_opy_ == bstack11ll11_opy_ (u"࠭ࡷࡪࡰࠪḨ"):
        bstack1111llllll1_opy_ = [bstack11ll11_opy_ (u"ࠧࡤ࡯ࡧ࠲ࡪࡾࡥࠨḩ"), bstack11ll11_opy_ (u"ࠨ࠱ࡦࠫḪ")]
        cmd = bstack1111llllll1_opy_ + cmd
      cmd = bstack11ll11_opy_ (u"ࠩࠣࠫḫ").join(cmd)
      self.logger.debug(bstack11ll11_opy_ (u"ࠥࡖࡺࡴ࡮ࡪࡰࡪࠤࢀࢃࠢḬ").format(cmd))
      with open(self.bstack1111ll1llll_opy_, bstack11ll11_opy_ (u"ࠦࡦࠨḭ")) as bstack111l11l1111_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack111l11l1111_opy_, text=True, stderr=bstack111l11l1111_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack111l111ll11_opy_ = True
      self.logger.error(bstack11ll11_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡱࡧࡵࡧࡾࠦࡷࡪࡶ࡫ࠤࡨࡳࡤࠡ࠯ࠣࡿࢂ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰ࠽ࠤࢀࢃࠢḮ").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack1111lll111l_opy_:
        self.logger.info(bstack11ll11_opy_ (u"ࠨࡓࡵࡱࡳࡴ࡮ࡴࡧࠡࡒࡨࡶࡨࡿࠢḯ"))
        cmd = [self.binary_path, bstack11ll11_opy_ (u"ࠢࡦࡺࡨࡧ࠿ࡹࡴࡰࡲࠥḰ")]
        self.bstack111l111l1ll_opy_(cmd)
        self.bstack1111lll111l_opy_ = False
    except Exception as e:
      self.logger.error(bstack11ll11_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸࡺ࡯ࡱࠢࡶࡩࡸࡹࡩࡰࡰࠣࡻ࡮ࡺࡨࠡࡥࡲࡱࡲࡧ࡮ࡥࠢ࠰ࠤࢀࢃࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱ࠾ࠥࢁࡽࠣḱ").format(cmd, e))
  def bstack1ll11lll_opy_(self):
    if not self.bstack1lll1l1111_opy_:
      return
    try:
      bstack111l11l1l1l_opy_ = 0
      while not self.bstack1111lll111l_opy_ and bstack111l11l1l1l_opy_ < self.bstack111l111l111_opy_:
        if self.bstack111l111ll11_opy_:
          self.logger.info(bstack11ll11_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡵࡨࡸࡺࡶࠠࡧࡣ࡬ࡰࡪࡪࠢḲ"))
          return
        time.sleep(1)
        bstack111l11l1l1l_opy_ += 1
      os.environ[bstack11ll11_opy_ (u"ࠪࡔࡊࡘࡃ࡚ࡡࡅࡉࡘ࡚࡟ࡑࡎࡄࡘࡋࡕࡒࡎࠩḳ")] = str(self.bstack1111ll1l111_opy_())
      self.logger.info(bstack11ll11_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡷࡪࡺࡵࡱࠢࡦࡳࡲࡶ࡬ࡦࡶࡨࡨࠧḴ"))
    except Exception as e:
      self.logger.error(bstack11ll11_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡨࡸࡺࡶࠠࡱࡧࡵࡧࡾ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡿࢂࠨḵ").format(e))
  def bstack1111ll1l111_opy_(self):
    if self.bstack1lll1l111l_opy_:
      return
    try:
      bstack1111lllll1l_opy_ = [platform[bstack11ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫḶ")].lower() for platform in self.config.get(bstack11ll11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪḷ"), [])]
      bstack1111ll111ll_opy_ = sys.maxsize
      bstack111l1111l11_opy_ = bstack11ll11_opy_ (u"ࠨࠩḸ")
      for browser in bstack1111lllll1l_opy_:
        if browser in self.bstack111l11l1ll1_opy_:
          bstack1111ll111l1_opy_ = self.bstack111l11l1ll1_opy_[browser]
        if bstack1111ll111l1_opy_ < bstack1111ll111ll_opy_:
          bstack1111ll111ll_opy_ = bstack1111ll111l1_opy_
          bstack111l1111l11_opy_ = browser
      return bstack111l1111l11_opy_
    except Exception as e:
      self.logger.error(bstack11ll11_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥ࡬ࡩ࡯ࡦࠣࡦࡪࡹࡴࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿࠥḹ").format(e))
  @classmethod
  def bstack11ll1ll1l_opy_(self):
    return os.getenv(bstack11ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡉࡗࡉ࡙ࠨḺ"), bstack11ll11_opy_ (u"ࠫࡋࡧ࡬ࡴࡧࠪḻ")).lower()
  @classmethod
  def bstack1l1l11l1_opy_(self):
    return os.getenv(bstack11ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡋࡒࡄ࡛ࡢࡇࡆࡖࡔࡖࡔࡈࡣࡒࡕࡄࡆࠩḼ"), bstack11ll11_opy_ (u"࠭ࠧḽ"))
  @classmethod
  def bstack1l1l1ll1lll_opy_(cls, value):
    cls.bstack11l1ll11l_opy_ = value
  @classmethod
  def bstack1111ll1ll11_opy_(cls):
    return cls.bstack11l1ll11l_opy_
  @classmethod
  def bstack1l1l1lll1ll_opy_(cls, value):
    cls.percy_build_id = value
  @classmethod
  def bstack1111ll1l1l1_opy_(cls):
    return cls.percy_build_id