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
import sys
import logging
import tarfile
import io
import os
import time
import requests
import re
from requests_toolbelt.multipart.encoder import MultipartEncoder
from bstack_utils.constants import bstack11ll111l11l_opy_, bstack11ll111ll1l_opy_, bstack11l1ll1l1l1_opy_
import tempfile
import json
bstack111ll11ll11_opy_ = os.getenv(bstack1l1l1l1_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡍ࡟ࡇࡋࡏࡉࠧᳲ"), None) or os.path.join(tempfile.gettempdir(), bstack1l1l1l1_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡩ࡫ࡢࡶࡩ࠱ࡰࡴ࡭ࠢᳳ"))
bstack111ll1l111l_opy_ = os.path.join(bstack1l1l1l1_opy_ (u"ࠨ࡬ࡰࡩࠥ᳴"), bstack1l1l1l1_opy_ (u"ࠧࡴࡦ࡮࠱ࡨࡲࡩ࠮ࡦࡨࡦࡺ࡭࠮࡭ࡱࡪࠫᳵ"))
logging.Formatter.converter = time.gmtime
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack1l1l1l1_opy_ (u"ࠨࠧࠫࡥࡸࡩࡴࡪ࡯ࡨ࠭ࡸ࡛ࠦࠦࠪࡱࡥࡲ࡫ࠩࡴ࡟࡞ࠩ࠭ࡲࡥࡷࡧ࡯ࡲࡦࡳࡥࠪࡵࡠࠤ࠲ࠦࠥࠩ࡯ࡨࡷࡸࡧࡧࡦࠫࡶࠫᳶ"),
      datefmt=bstack1l1l1l1_opy_ (u"ࠩࠨ࡝࠲ࠫ࡭࠮ࠧࡧࡘࠪࡎ࠺ࠦࡏ࠽ࠩࡘࡠࠧ᳷"),
      stream=sys.stdout
    )
  return logger
def bstack1llll11l111_opy_():
  bstack111ll11ll1l_opy_ = os.environ.get(bstack1l1l1l1_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅࡍࡓࡇࡒ࡚ࡡࡇࡉࡇ࡛ࡇࠣ᳸"), bstack1l1l1l1_opy_ (u"ࠦ࡫ࡧ࡬ࡴࡧࠥ᳹"))
  return logging.DEBUG if bstack111ll11ll1l_opy_.lower() == bstack1l1l1l1_opy_ (u"ࠧࡺࡲࡶࡧࠥᳺ") else logging.INFO
def bstack1l1lll11l11_opy_():
  global bstack111ll11ll11_opy_
  if os.path.exists(bstack111ll11ll11_opy_):
    os.remove(bstack111ll11ll11_opy_)
  if os.path.exists(bstack111ll1l111l_opy_):
    os.remove(bstack111ll1l111l_opy_)
def bstack1l1l1l1lll_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def bstack11l1l11ll_opy_(config, log_level):
  bstack111ll111lll_opy_ = log_level
  if bstack1l1l1l1_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨ᳻") in config and config[bstack1l1l1l1_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩ᳼")] in bstack11ll111ll1l_opy_:
    bstack111ll111lll_opy_ = bstack11ll111ll1l_opy_[config[bstack1l1l1l1_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪ᳽")]]
  if config.get(bstack1l1l1l1_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡹࡹࡵࡃࡢࡲࡷࡹࡷ࡫ࡌࡰࡩࡶࠫ᳾"), False):
    logging.getLogger().setLevel(bstack111ll111lll_opy_)
    return bstack111ll111lll_opy_
  global bstack111ll11ll11_opy_
  bstack1l1l1l1lll_opy_()
  bstack111ll11l1l1_opy_ = logging.Formatter(
    fmt=bstack1l1l1l1_opy_ (u"ࠪࠩ࠭ࡧࡳࡤࡶ࡬ࡱࡪ࠯ࡳࠡ࡝ࠨࠬࡳࡧ࡭ࡦࠫࡶࡡࡠࠫࠨ࡭ࡧࡹࡩࡱࡴࡡ࡮ࡧࠬࡷࡢࠦ࠭ࠡࠧࠫࡱࡪࡹࡳࡢࡩࡨ࠭ࡸ࠭᳿"),
    datefmt=bstack1l1l1l1_opy_ (u"ࠫࠪ࡟࠭ࠦ࡯࠰ࠩࡩ࡚ࠥࡉ࠼ࠨࡑ࠿ࠫࡓ࡛ࠩᴀ"),
  )
  bstack111ll1lll11_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack111ll11ll11_opy_)
  file_handler.setFormatter(bstack111ll11l1l1_opy_)
  bstack111ll1lll11_opy_.setFormatter(bstack111ll11l1l1_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack111ll1lll11_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack1l1l1l1_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࠮ࡸࡧࡥࡨࡷ࡯ࡶࡦࡴ࠱ࡶࡪࡳ࡯ࡵࡧ࠱ࡶࡪࡳ࡯ࡵࡧࡢࡧࡴࡴ࡮ࡦࡥࡷ࡭ࡴࡴࠧᴁ"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack111ll1lll11_opy_.setLevel(bstack111ll111lll_opy_)
  logging.getLogger().addHandler(bstack111ll1lll11_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack111ll111lll_opy_
def bstack111ll11lll1_opy_(config):
  try:
    bstack111ll1l1111_opy_ = set(bstack11l1ll1l1l1_opy_)
    bstack111ll1ll1l1_opy_ = bstack1l1l1l1_opy_ (u"࠭ࠧᴂ")
    with open(bstack1l1l1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠪᴃ")) as bstack111ll11l111_opy_:
      bstack111ll1l11l1_opy_ = bstack111ll11l111_opy_.read()
      bstack111ll1ll1l1_opy_ = re.sub(bstack1l1l1l1_opy_ (u"ࡳࠩࡡࠬࡡࡹࠫࠪࡁࠦ࠲࠯ࠪ࡜࡯ࠩᴄ"), bstack1l1l1l1_opy_ (u"ࠩࠪᴅ"), bstack111ll1l11l1_opy_, flags=re.M)
      bstack111ll1ll1l1_opy_ = re.sub(
        bstack1l1l1l1_opy_ (u"ࡵࠫࡣ࠮࡜ࡴ࠭ࠬࡃ࠭࠭ᴆ") + bstack1l1l1l1_opy_ (u"ࠫࢁ࠭ᴇ").join(bstack111ll1l1111_opy_) + bstack1l1l1l1_opy_ (u"ࠬ࠯࠮ࠫࠦࠪᴈ"),
        bstack1l1l1l1_opy_ (u"ࡸࠧ࡝࠴࠽ࠤࡠࡘࡅࡅࡃࡆࡘࡊࡊ࡝ࠨᴉ"),
        bstack111ll1ll1l1_opy_, flags=re.M | re.I
      )
    def bstack111ll1ll111_opy_(dic):
      bstack111ll1l1ll1_opy_ = {}
      for key, value in dic.items():
        if key in bstack111ll1l1111_opy_:
          bstack111ll1l1ll1_opy_[key] = bstack1l1l1l1_opy_ (u"ࠧ࡜ࡔࡈࡈࡆࡉࡔࡆࡆࡠࠫᴊ")
        else:
          if isinstance(value, dict):
            bstack111ll1l1ll1_opy_[key] = bstack111ll1ll111_opy_(value)
          else:
            bstack111ll1l1ll1_opy_[key] = value
      return bstack111ll1l1ll1_opy_
    bstack111ll1l1ll1_opy_ = bstack111ll1ll111_opy_(config)
    return {
      bstack1l1l1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺ࡯࡯ࠫᴋ"): bstack111ll1ll1l1_opy_,
      bstack1l1l1l1_opy_ (u"ࠩࡩ࡭ࡳࡧ࡬ࡤࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠬᴌ"): json.dumps(bstack111ll1l1ll1_opy_)
    }
  except Exception as e:
    return {}
def bstack111ll1l1l11_opy_(inipath, rootpath):
  log_dir = os.path.join(os.getcwd(), bstack1l1l1l1_opy_ (u"ࠪࡰࡴ࡭ࠧᴍ"))
  if not os.path.exists(log_dir):
    os.makedirs(log_dir)
  bstack111ll1l1l1l_opy_ = os.path.join(log_dir, bstack1l1l1l1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡨࡵ࡮ࡧ࡫ࡪࡷࠬᴎ"))
  if not os.path.exists(bstack111ll1l1l1l_opy_):
    bstack111ll1l11ll_opy_ = {
      bstack1l1l1l1_opy_ (u"ࠧ࡯࡮ࡪࡲࡤࡸ࡭ࠨᴏ"): str(inipath),
      bstack1l1l1l1_opy_ (u"ࠨࡲࡰࡱࡷࡴࡦࡺࡨࠣᴐ"): str(rootpath)
    }
    with open(os.path.join(log_dir, bstack1l1l1l1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡤࡱࡱࡪ࡮࡭ࡳ࠯࡬ࡶࡳࡳ࠭ᴑ")), bstack1l1l1l1_opy_ (u"ࠨࡹࠪᴒ")) as bstack111ll1ll1ll_opy_:
      bstack111ll1ll1ll_opy_.write(json.dumps(bstack111ll1l11ll_opy_))
def bstack111ll1l1lll_opy_():
  try:
    bstack111ll1l1l1l_opy_ = os.path.join(os.getcwd(), bstack1l1l1l1_opy_ (u"ࠩ࡯ࡳ࡬࠭ᴓ"), bstack1l1l1l1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡧࡴࡴࡦࡪࡩࡶ࠲࡯ࡹ࡯࡯ࠩᴔ"))
    if os.path.exists(bstack111ll1l1l1l_opy_):
      with open(bstack111ll1l1l1l_opy_, bstack1l1l1l1_opy_ (u"ࠫࡷ࠭ᴕ")) as bstack111ll1ll1ll_opy_:
        bstack111ll11l11l_opy_ = json.load(bstack111ll1ll1ll_opy_)
      return bstack111ll11l11l_opy_.get(bstack1l1l1l1_opy_ (u"ࠬ࡯࡮ࡪࡲࡤࡸ࡭࠭ᴖ"), bstack1l1l1l1_opy_ (u"࠭ࠧᴗ")), bstack111ll11l11l_opy_.get(bstack1l1l1l1_opy_ (u"ࠧࡳࡱࡲࡸࡵࡧࡴࡩࠩᴘ"), bstack1l1l1l1_opy_ (u"ࠨࠩᴙ"))
  except:
    pass
  return None, None
def bstack111ll11l1ll_opy_():
  try:
    bstack111ll1l1l1l_opy_ = os.path.join(os.getcwd(), bstack1l1l1l1_opy_ (u"ࠩ࡯ࡳ࡬࠭ᴚ"), bstack1l1l1l1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡧࡴࡴࡦࡪࡩࡶ࠲࡯ࡹ࡯࡯ࠩᴛ"))
    if os.path.exists(bstack111ll1l1l1l_opy_):
      os.remove(bstack111ll1l1l1l_opy_)
  except:
    pass
def bstack1111l1111_opy_(config):
  try:
    from bstack_utils.helper import bstack11lll11111_opy_, bstack111l111l_opy_
    from browserstack_sdk.sdk_cli.cli import cli
    global bstack111ll11ll11_opy_
    if config.get(bstack1l1l1l1_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡆࡻࡴࡰࡅࡤࡴࡹࡻࡲࡦࡎࡲ࡫ࡸ࠭ᴜ"), False):
      return
    uuid = os.getenv(bstack1l1l1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪᴝ")) if os.getenv(bstack1l1l1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫᴞ")) else bstack11lll11111_opy_.get_property(bstack1l1l1l1_opy_ (u"ࠢࡴࡦ࡮ࡖࡺࡴࡉࡥࠤᴟ"))
    if not uuid or uuid == bstack1l1l1l1_opy_ (u"ࠨࡰࡸࡰࡱ࠭ᴠ"):
      return
    bstack111ll1llll1_opy_ = [bstack1l1l1l1_opy_ (u"ࠩࡵࡩࡶࡻࡩࡳࡧࡰࡩࡳࡺࡳ࠯ࡶࡻࡸࠬᴡ"), bstack1l1l1l1_opy_ (u"ࠪࡔ࡮ࡶࡦࡪ࡮ࡨࠫᴢ"), bstack1l1l1l1_opy_ (u"ࠫࡵࡿࡰࡳࡱ࡭ࡩࡨࡺ࠮ࡵࡱࡰࡰࠬᴣ"), bstack111ll11ll11_opy_, bstack111ll1l111l_opy_]
    bstack111ll11llll_opy_, root_path = bstack111ll1l1lll_opy_()
    if bstack111ll11llll_opy_ != None:
      bstack111ll1llll1_opy_.append(bstack111ll11llll_opy_)
    if root_path != None:
      bstack111ll1llll1_opy_.append(os.path.join(root_path, bstack1l1l1l1_opy_ (u"ࠬࡩ࡯࡯ࡨࡷࡩࡸࡺ࠮ࡱࡻࠪᴤ")))
    bstack1l1l1l1lll_opy_()
    logging.shutdown()
    output_file = os.path.join(tempfile.gettempdir(), bstack1l1l1l1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࠳࡬ࡰࡩࡶ࠱ࠬᴥ") + uuid + bstack1l1l1l1_opy_ (u"ࠧ࠯ࡶࡤࡶ࠳࡭ࡺࠨᴦ"))
    with tarfile.open(output_file, bstack1l1l1l1_opy_ (u"ࠣࡹ࠽࡫ࡿࠨᴧ")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack111ll1llll1_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack111ll11lll1_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack111ll1ll11l_opy_ = data.encode()
        tarinfo.size = len(bstack111ll1ll11l_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack111ll1ll11l_opy_))
    bstack11ll111ll_opy_ = MultipartEncoder(
      fields= {
        bstack1l1l1l1_opy_ (u"ࠩࡧࡥࡹࡧࠧᴨ"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack1l1l1l1_opy_ (u"ࠪࡶࡧ࠭ᴩ")), bstack1l1l1l1_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱ࡻ࠱࡬ࢀࡩࡱࠩᴪ")),
        bstack1l1l1l1_opy_ (u"ࠬࡩ࡬ࡪࡧࡱࡸࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧᴫ"): uuid
      }
    )
    bstack111ll1lll1l_opy_ = bstack111l111l_opy_(cli.config, [bstack1l1l1l1_opy_ (u"ࠨࡡࡱ࡫ࡶࠦᴬ"), bstack1l1l1l1_opy_ (u"ࠢࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠢᴭ"), bstack1l1l1l1_opy_ (u"ࠣࡷࡳࡰࡴࡧࡤࠣᴮ")], bstack11ll111l11l_opy_) if cli.is_running() else bstack11ll111l11l_opy_
    response = requests.post(
      bstack1l1l1l1_opy_ (u"ࠤࡾࢁ࠴ࡩ࡬ࡪࡧࡱࡸ࠲ࡲ࡯ࡨࡵ࠲ࡹࡵࡲ࡯ࡢࡦࠥᴯ").format(bstack111ll1lll1l_opy_),
      data=bstack11ll111ll_opy_,
      headers={bstack1l1l1l1_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩᴰ"): bstack11ll111ll_opy_.content_type},
      auth=(config[bstack1l1l1l1_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ᴱ")], config[bstack1l1l1l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨᴲ")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack1l1l1l1_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥࡻࡰ࡭ࡱࡤࡨࠥࡲ࡯ࡨࡵ࠽ࠤࠬᴳ") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack1l1l1l1_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡦࡰࡧ࡭ࡳ࡭ࠠ࡭ࡱࡪࡷ࠿࠭ᴴ") + str(e))
  finally:
    try:
      bstack1l1lll11l11_opy_()
      bstack111ll11l1ll_opy_()
    except:
      pass