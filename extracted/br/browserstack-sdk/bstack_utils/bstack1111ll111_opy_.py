# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack1111l_opy_ = 7
def bstack111lll_opy_ (bstack1lll1l_opy_):
    global bstack1l11lll_opy_
    bstack1ll1l1_opy_ = ord (bstack1lll1l_opy_ [-1])
    bstack1ll1l11_opy_ = bstack1lll1l_opy_ [:-1]
    bstack1l_opy_ = bstack1ll1l1_opy_ % len (bstack1ll1l11_opy_)
    bstack1l11ll_opy_ = bstack1ll1l11_opy_ [:bstack1l_opy_] + bstack1ll1l11_opy_ [bstack1l_opy_:]
    if bstack111ll1_opy_:
        bstack1l1l11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    else:
        bstack1l1l11l_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    return eval (bstack1l1l11l_opy_)
import sys
import logging
import tarfile
import io
import os
import time
import requests
import re
from requests_toolbelt.multipart.encoder import MultipartEncoder
from bstack_utils.constants import bstack11ll11ll1ll_opy_, bstack11ll111111l_opy_, bstack11ll111lll1_opy_
import tempfile
import json
bstack111lll111ll_opy_ = os.getenv(bstack111lll_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡋࡤࡌࡉࡍࡇ᳢ࠥ"), None) or os.path.join(tempfile.gettempdir(), bstack111lll_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡧࡩࡧࡻࡧ࠯࡮ࡲ࡫᳣ࠧ"))
bstack111lll1l11l_opy_ = os.path.join(bstack111lll_opy_ (u"ࠦࡱࡵࡧ᳤ࠣ"), bstack111lll_opy_ (u"ࠬࡹࡤ࡬࠯ࡦࡰ࡮࠳ࡤࡦࡤࡸ࡫࠳ࡲ࡯ࡨ᳥ࠩ"))
logging.Formatter.converter = time.gmtime
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack111lll_opy_ (u"࠭ࠥࠩࡣࡶࡧࡹ࡯࡭ࡦࠫࡶࠤࡠࠫࠨ࡯ࡣࡰࡩ࠮ࡹ࡝࡜ࠧࠫࡰࡪࡼࡥ࡭ࡰࡤࡱࡪ࠯ࡳ࡞ࠢ࠰ࠤࠪ࠮࡭ࡦࡵࡶࡥ࡬࡫ࠩࡴ᳦ࠩ"),
      datefmt=bstack111lll_opy_ (u"࡛ࠧࠦ࠰ࠩࡲ࠳ࠥࡥࡖࠨࡌ࠿ࠫࡍ࠻ࠧࡖ࡞᳧ࠬ"),
      stream=sys.stdout
    )
  return logger
def bstack1lllll1l11l_opy_():
  bstack111lll1ll1l_opy_ = os.environ.get(bstack111lll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡋࡑࡅࡗ࡟࡟ࡅࡇࡅ࡙ࡌࠨ᳨"), bstack111lll_opy_ (u"ࠤࡩࡥࡱࡹࡥࠣᳩ"))
  return logging.DEBUG if bstack111lll1ll1l_opy_.lower() == bstack111lll_opy_ (u"ࠥࡸࡷࡻࡥࠣᳪ") else logging.INFO
def bstack1l1lllll1ll_opy_():
  global bstack111lll111ll_opy_
  if os.path.exists(bstack111lll111ll_opy_):
    os.remove(bstack111lll111ll_opy_)
  if os.path.exists(bstack111lll1l11l_opy_):
    os.remove(bstack111lll1l11l_opy_)
def bstack1l111l111l_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def bstack1llll1111l_opy_(config, log_level):
  bstack111lll11l1l_opy_ = log_level
  if bstack111lll_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭ᳫ") in config and config[bstack111lll_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧᳬ")] in bstack11ll111111l_opy_:
    bstack111lll11l1l_opy_ = bstack11ll111111l_opy_[config[bstack111lll_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨ᳭")]]
  if config.get(bstack111lll_opy_ (u"ࠧࡥ࡫ࡶࡥࡧࡲࡥࡂࡷࡷࡳࡈࡧࡰࡵࡷࡵࡩࡑࡵࡧࡴࠩᳮ"), False):
    logging.getLogger().setLevel(bstack111lll11l1l_opy_)
    return bstack111lll11l1l_opy_
  global bstack111lll111ll_opy_
  bstack1l111l111l_opy_()
  bstack111lll1ll11_opy_ = logging.Formatter(
    fmt=bstack111lll_opy_ (u"ࠨࠧࠫࡥࡸࡩࡴࡪ࡯ࡨ࠭ࡸ࡛ࠦࠦࠪࡱࡥࡲ࡫ࠩࡴ࡟࡞ࠩ࠭ࡲࡥࡷࡧ࡯ࡲࡦࡳࡥࠪࡵࡠࠤ࠲ࠦࠥࠩ࡯ࡨࡷࡸࡧࡧࡦࠫࡶࠫᳯ"),
    datefmt=bstack111lll_opy_ (u"ࠩࠨ࡝࠲ࠫ࡭࠮ࠧࡧࡘࠪࡎ࠺ࠦࡏ࠽ࠩࡘࡠࠧᳰ"),
  )
  bstack111lll1l1ll_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack111lll111ll_opy_)
  file_handler.setFormatter(bstack111lll1ll11_opy_)
  bstack111lll1l1ll_opy_.setFormatter(bstack111lll1ll11_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack111lll1l1ll_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack111lll_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱ࠳ࡽࡥࡣࡦࡵ࡭ࡻ࡫ࡲ࠯ࡴࡨࡱࡴࡺࡥ࠯ࡴࡨࡱࡴࡺࡥࡠࡥࡲࡲࡳ࡫ࡣࡵ࡫ࡲࡲࠬᳱ"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack111lll1l1ll_opy_.setLevel(bstack111lll11l1l_opy_)
  logging.getLogger().addHandler(bstack111lll1l1ll_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack111lll11l1l_opy_
def bstack111lll1l111_opy_(config):
  try:
    bstack111lll111l1_opy_ = set(bstack11ll111lll1_opy_)
    bstack111lll1l1l1_opy_ = bstack111lll_opy_ (u"ࠫࠬᳲ")
    with open(bstack111lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡾࡳ࡬ࠨᳳ")) as bstack111lll11l11_opy_:
      bstack111lll11lll_opy_ = bstack111lll11l11_opy_.read()
      bstack111lll1l1l1_opy_ = re.sub(bstack111lll_opy_ (u"ࡸࠧ࡟ࠪ࡟ࡷ࠰࠯࠿ࠤ࠰࠭ࠨࡡࡴࠧ᳴"), bstack111lll_opy_ (u"ࠧࠨᳵ"), bstack111lll11lll_opy_, flags=re.M)
      bstack111lll1l1l1_opy_ = re.sub(
        bstack111lll_opy_ (u"ࡳࠩࡡࠬࡡࡹࠫࠪࡁࠫࠫᳶ") + bstack111lll_opy_ (u"ࠩࡿࠫ᳷").join(bstack111lll111l1_opy_) + bstack111lll_opy_ (u"ࠪ࠭࠳࠰ࠤࠨ᳸"),
        bstack111lll_opy_ (u"ࡶࠬࡢ࠲࠻ࠢ࡞ࡖࡊࡊࡁࡄࡖࡈࡈࡢ࠭᳹"),
        bstack111lll1l1l1_opy_, flags=re.M | re.I
      )
    def bstack111ll1ll111_opy_(dic):
      bstack111lll1111l_opy_ = {}
      for key, value in dic.items():
        if key in bstack111lll111l1_opy_:
          bstack111lll1111l_opy_[key] = bstack111lll_opy_ (u"ࠬࡡࡒࡆࡆࡄࡇ࡙ࡋࡄ࡞ࠩᳺ")
        else:
          if isinstance(value, dict):
            bstack111lll1111l_opy_[key] = bstack111ll1ll111_opy_(value)
          else:
            bstack111lll1111l_opy_[key] = value
      return bstack111lll1111l_opy_
    bstack111lll1111l_opy_ = bstack111ll1ll111_opy_(config)
    return {
      bstack111lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭ࠩ᳻"): bstack111lll1l1l1_opy_,
      bstack111lll_opy_ (u"ࠧࡧ࡫ࡱࡥࡱࡩ࡯࡯ࡨ࡬࡫࠳ࡰࡳࡰࡰࠪ᳼"): json.dumps(bstack111lll1111l_opy_)
    }
  except Exception as e:
    return {}
def bstack111ll1ll1l1_opy_(inipath, rootpath):
  log_dir = os.path.join(os.getcwd(), bstack111lll_opy_ (u"ࠨ࡮ࡲ࡫ࠬ᳽"))
  if not os.path.exists(log_dir):
    os.makedirs(log_dir)
  bstack111ll1l1lll_opy_ = os.path.join(log_dir, bstack111lll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡦࡳࡳ࡬ࡩࡨࡵࠪ᳾"))
  if not os.path.exists(bstack111ll1l1lll_opy_):
    bstack111ll1lllll_opy_ = {
      bstack111lll_opy_ (u"ࠥ࡭ࡳ࡯ࡰࡢࡶ࡫ࠦ᳿"): str(inipath),
      bstack111lll_opy_ (u"ࠦࡷࡵ࡯ࡵࡲࡤࡸ࡭ࠨᴀ"): str(rootpath)
    }
    with open(os.path.join(log_dir, bstack111lll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡤࡩ࡯࡯ࡨ࡬࡫ࡸ࠴ࡪࡴࡱࡱࠫᴁ")), bstack111lll_opy_ (u"࠭ࡷࠨᴂ")) as bstack111ll1lll11_opy_:
      bstack111ll1lll11_opy_.write(json.dumps(bstack111ll1lllll_opy_))
def bstack111ll1lll1l_opy_():
  try:
    bstack111ll1l1lll_opy_ = os.path.join(os.getcwd(), bstack111lll_opy_ (u"ࠧ࡭ࡱࡪࠫᴃ"), bstack111lll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡥࡲࡲ࡫࡯ࡧࡴ࠰࡭ࡷࡴࡴࠧᴄ"))
    if os.path.exists(bstack111ll1l1lll_opy_):
      with open(bstack111ll1l1lll_opy_, bstack111lll_opy_ (u"ࠩࡵࠫᴅ")) as bstack111ll1lll11_opy_:
        bstack111lll11ll1_opy_ = json.load(bstack111ll1lll11_opy_)
      return bstack111lll11ll1_opy_.get(bstack111lll_opy_ (u"ࠪ࡭ࡳ࡯ࡰࡢࡶ࡫ࠫᴆ"), bstack111lll_opy_ (u"ࠫࠬᴇ")), bstack111lll11ll1_opy_.get(bstack111lll_opy_ (u"ࠬࡸ࡯ࡰࡶࡳࡥࡹ࡮ࠧᴈ"), bstack111lll_opy_ (u"࠭ࠧᴉ"))
  except:
    pass
  return None, None
def bstack111ll1ll1ll_opy_():
  try:
    bstack111ll1l1lll_opy_ = os.path.join(os.getcwd(), bstack111lll_opy_ (u"ࠧ࡭ࡱࡪࠫᴊ"), bstack111lll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡥࡲࡲ࡫࡯ࡧࡴ࠰࡭ࡷࡴࡴࠧᴋ"))
    if os.path.exists(bstack111ll1l1lll_opy_):
      os.remove(bstack111ll1l1lll_opy_)
  except:
    pass
def bstack11l1111ll_opy_(config):
  try:
    from bstack_utils.helper import bstack1ll1l11ll_opy_, bstack111llll1l_opy_
    from browserstack_sdk.sdk_cli.cli import cli
    global bstack111lll111ll_opy_
    if config.get(bstack111lll_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡹࡹࡵࡃࡢࡲࡷࡹࡷ࡫ࡌࡰࡩࡶࠫᴌ"), False):
      return
    uuid = os.getenv(bstack111lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨᴍ")) if os.getenv(bstack111lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩᴎ")) else bstack1ll1l11ll_opy_.get_property(bstack111lll_opy_ (u"ࠧࡹࡤ࡬ࡔࡸࡲࡎࡪࠢᴏ"))
    if not uuid or uuid == bstack111lll_opy_ (u"࠭࡮ࡶ࡮࡯ࠫᴐ"):
      return
    bstack111ll1ll11l_opy_ = [bstack111lll_opy_ (u"ࠧࡳࡧࡴࡹ࡮ࡸࡥ࡮ࡧࡱࡸࡸ࠴ࡴࡹࡶࠪᴑ"), bstack111lll_opy_ (u"ࠨࡒ࡬ࡴ࡫࡯࡬ࡦࠩᴒ"), bstack111lll_opy_ (u"ࠩࡳࡽࡵࡸ࡯࡫ࡧࡦࡸ࠳ࡺ࡯࡮࡮ࠪᴓ"), bstack111lll111ll_opy_, bstack111lll1l11l_opy_]
    bstack111ll1llll1_opy_, root_path = bstack111ll1lll1l_opy_()
    if bstack111ll1llll1_opy_ != None:
      bstack111ll1ll11l_opy_.append(bstack111ll1llll1_opy_)
    if root_path != None:
      bstack111ll1ll11l_opy_.append(os.path.join(root_path, bstack111lll_opy_ (u"ࠪࡧࡴࡴࡦࡵࡧࡶࡸ࠳ࡶࡹࠨᴔ")))
    bstack1l111l111l_opy_()
    logging.shutdown()
    output_file = os.path.join(tempfile.gettempdir(), bstack111lll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠱ࡱࡵࡧࡴ࠯ࠪᴕ") + uuid + bstack111lll_opy_ (u"ࠬ࠴ࡴࡢࡴ࠱࡫ࡿ࠭ᴖ"))
    with tarfile.open(output_file, bstack111lll_opy_ (u"ࠨࡷ࠻ࡩࡽࠦᴗ")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack111ll1ll11l_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack111lll1l111_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack111lll1lll1_opy_ = data.encode()
        tarinfo.size = len(bstack111lll1lll1_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack111lll1lll1_opy_))
    bstack11l1ll11l_opy_ = MultipartEncoder(
      fields= {
        bstack111lll_opy_ (u"ࠧࡥࡣࡷࡥࠬᴘ"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack111lll_opy_ (u"ࠨࡴࡥࠫᴙ")), bstack111lll_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯ࡹ࠯ࡪࡾ࡮ࡶࠧᴚ")),
        bstack111lll_opy_ (u"ࠪࡧࡱ࡯ࡥ࡯ࡶࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬᴛ"): uuid
      }
    )
    bstack111lll11111_opy_ = bstack111llll1l_opy_(cli.config, [bstack111lll_opy_ (u"ࠦࡦࡶࡩࡴࠤᴜ"), bstack111lll_opy_ (u"ࠧࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠧᴝ"), bstack111lll_opy_ (u"ࠨࡵࡱ࡮ࡲࡥࡩࠨᴞ")], bstack11ll11ll1ll_opy_) if cli.is_running() else bstack11ll11ll1ll_opy_
    response = requests.post(
      bstack111lll_opy_ (u"ࠢࡼࡿ࠲ࡧࡱ࡯ࡥ࡯ࡶ࠰ࡰࡴ࡭ࡳ࠰ࡷࡳࡰࡴࡧࡤࠣᴟ").format(bstack111lll11111_opy_),
      data=bstack11l1ll11l_opy_,
      headers={bstack111lll_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧᴠ"): bstack11l1ll11l_opy_.content_type},
      auth=(config[bstack111lll_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫᴡ")], config[bstack111lll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ᴢ")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack111lll_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣࡹࡵࡲ࡯ࡢࡦࠣࡰࡴ࡭ࡳ࠻ࠢࠪᴣ") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack111lll_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸ࡫࡮ࡥ࡫ࡱ࡫ࠥࡲ࡯ࡨࡵ࠽ࠫᴤ") + str(e))
  finally:
    try:
      bstack1l1lllll1ll_opy_()
      bstack111ll1ll1ll_opy_()
    except:
      pass