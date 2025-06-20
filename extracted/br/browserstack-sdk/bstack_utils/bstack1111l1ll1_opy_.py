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
import sys
import logging
import tarfile
import io
import os
import time
import requests
import re
from requests_toolbelt.multipart.encoder import MultipartEncoder
from bstack_utils.constants import bstack11ll11111ll_opy_, bstack11ll111l1ll_opy_, bstack11l1ll1llll_opy_
import tempfile
import json
bstack111ll1llll1_opy_ = os.getenv(bstack11ll11_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡌࡥࡆࡊࡎࡈࠦᳱ"), None) or os.path.join(tempfile.gettempdir(), bstack11ll11_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡨࡪࡨࡵࡨ࠰࡯ࡳ࡬ࠨᳲ"))
bstack111ll1lll11_opy_ = os.path.join(bstack11ll11_opy_ (u"ࠧࡲ࡯ࡨࠤᳳ"), bstack11ll11_opy_ (u"࠭ࡳࡥ࡭࠰ࡧࡱ࡯࠭ࡥࡧࡥࡹ࡬࠴࡬ࡰࡩࠪ᳴"))
logging.Formatter.converter = time.gmtime
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack11ll11_opy_ (u"ࠧࠦࠪࡤࡷࡨࡺࡩ࡮ࡧࠬࡷࠥࡡࠥࠩࡰࡤࡱࡪ࠯ࡳ࡞࡝ࠨࠬࡱ࡫ࡶࡦ࡮ࡱࡥࡲ࡫ࠩࡴ࡟ࠣ࠱ࠥࠫࠨ࡮ࡧࡶࡷࡦ࡭ࡥࠪࡵࠪᳵ"),
      datefmt=bstack11ll11_opy_ (u"ࠨࠧ࡜࠱ࠪࡳ࠭ࠦࡦࡗࠩࡍࡀࠥࡎ࠼ࠨࡗ࡟࠭ᳶ"),
      stream=sys.stdout
    )
  return logger
def bstack1lll1lll1ll_opy_():
  bstack111ll1l1111_opy_ = os.environ.get(bstack11ll11_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡌࡒࡆࡘ࡙ࡠࡆࡈࡆ࡚ࡍࠢ᳷"), bstack11ll11_opy_ (u"ࠥࡪࡦࡲࡳࡦࠤ᳸"))
  return logging.DEBUG if bstack111ll1l1111_opy_.lower() == bstack11ll11_opy_ (u"ࠦࡹࡸࡵࡦࠤ᳹") else logging.INFO
def bstack1l1ll1l1l11_opy_():
  global bstack111ll1llll1_opy_
  if os.path.exists(bstack111ll1llll1_opy_):
    os.remove(bstack111ll1llll1_opy_)
  if os.path.exists(bstack111ll1lll11_opy_):
    os.remove(bstack111ll1lll11_opy_)
def bstack11ll1l1ll1_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def bstack1lll11l1_opy_(config, log_level):
  bstack111ll111lll_opy_ = log_level
  if bstack11ll11_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧᳺ") in config and config[bstack11ll11_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨ᳻")] in bstack11ll111l1ll_opy_:
    bstack111ll111lll_opy_ = bstack11ll111l1ll_opy_[config[bstack11ll11_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩ᳼")]]
  if config.get(bstack11ll11_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦࡃࡸࡸࡴࡉࡡࡱࡶࡸࡶࡪࡒ࡯ࡨࡵࠪ᳽"), False):
    logging.getLogger().setLevel(bstack111ll111lll_opy_)
    return bstack111ll111lll_opy_
  global bstack111ll1llll1_opy_
  bstack11ll1l1ll1_opy_()
  bstack111ll11l111_opy_ = logging.Formatter(
    fmt=bstack11ll11_opy_ (u"ࠩࠨࠬࡦࡹࡣࡵ࡫ࡰࡩ࠮ࡹࠠ࡜ࠧࠫࡲࡦࡳࡥࠪࡵࡠ࡟ࠪ࠮࡬ࡦࡸࡨࡰࡳࡧ࡭ࡦࠫࡶࡡࠥ࠳ࠠࠦࠪࡰࡩࡸࡹࡡࡨࡧࠬࡷࠬ᳾"),
    datefmt=bstack11ll11_opy_ (u"ࠪࠩ࡞࠳ࠥ࡮࠯ࠨࡨ࡙ࠫࡈ࠻ࠧࡐ࠾࡙࡚ࠪࠨ᳿"),
  )
  bstack111ll1ll1l1_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack111ll1llll1_opy_)
  file_handler.setFormatter(bstack111ll11l111_opy_)
  bstack111ll1ll1l1_opy_.setFormatter(bstack111ll11l111_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack111ll1ll1l1_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack11ll11_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠴ࡷࡦࡤࡧࡶ࡮ࡼࡥࡳ࠰ࡵࡩࡲࡵࡴࡦ࠰ࡵࡩࡲࡵࡴࡦࡡࡦࡳࡳࡴࡥࡤࡶ࡬ࡳࡳ࠭ᴀ"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack111ll1ll1l1_opy_.setLevel(bstack111ll111lll_opy_)
  logging.getLogger().addHandler(bstack111ll1ll1l1_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack111ll111lll_opy_
def bstack111ll11lll1_opy_(config):
  try:
    bstack111ll1l1l11_opy_ = set(bstack11l1ll1llll_opy_)
    bstack111ll1l1lll_opy_ = bstack11ll11_opy_ (u"ࠬ࠭ᴁ")
    with open(bstack11ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭ࠩᴂ")) as bstack111ll11l1ll_opy_:
      bstack111ll11l11l_opy_ = bstack111ll11l1ll_opy_.read()
      bstack111ll1l1lll_opy_ = re.sub(bstack11ll11_opy_ (u"ࡲࠨࡠࠫࡠࡸ࠱ࠩࡀࠥ࠱࠮ࠩࡢ࡮ࠨᴃ"), bstack11ll11_opy_ (u"ࠨࠩᴄ"), bstack111ll11l11l_opy_, flags=re.M)
      bstack111ll1l1lll_opy_ = re.sub(
        bstack11ll11_opy_ (u"ࡴࠪࡢ࠭ࡢࡳࠬࠫࡂࠬࠬᴅ") + bstack11ll11_opy_ (u"ࠪࢀࠬᴆ").join(bstack111ll1l1l11_opy_) + bstack11ll11_opy_ (u"ࠫ࠮࠴ࠪࠥࠩᴇ"),
        bstack11ll11_opy_ (u"ࡷ࠭࡜࠳࠼ࠣ࡟ࡗࡋࡄࡂࡅࡗࡉࡉࡣࠧᴈ"),
        bstack111ll1l1lll_opy_, flags=re.M | re.I
      )
    def bstack111ll1l111l_opy_(dic):
      bstack111ll11l1l1_opy_ = {}
      for key, value in dic.items():
        if key in bstack111ll1l1l11_opy_:
          bstack111ll11l1l1_opy_[key] = bstack11ll11_opy_ (u"࡛࠭ࡓࡇࡇࡅࡈ࡚ࡅࡅ࡟ࠪᴉ")
        else:
          if isinstance(value, dict):
            bstack111ll11l1l1_opy_[key] = bstack111ll1l111l_opy_(value)
          else:
            bstack111ll11l1l1_opy_[key] = value
      return bstack111ll11l1l1_opy_
    bstack111ll11l1l1_opy_ = bstack111ll1l111l_opy_(config)
    return {
      bstack11ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠪᴊ"): bstack111ll1l1lll_opy_,
      bstack11ll11_opy_ (u"ࠨࡨ࡬ࡲࡦࡲࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫᴋ"): json.dumps(bstack111ll11l1l1_opy_)
    }
  except Exception as e:
    return {}
def bstack111ll1lll1l_opy_(inipath, rootpath):
  log_dir = os.path.join(os.getcwd(), bstack11ll11_opy_ (u"ࠩ࡯ࡳ࡬࠭ᴌ"))
  if not os.path.exists(log_dir):
    os.makedirs(log_dir)
  bstack111ll1ll1ll_opy_ = os.path.join(log_dir, bstack11ll11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡧࡴࡴࡦࡪࡩࡶࠫᴍ"))
  if not os.path.exists(bstack111ll1ll1ll_opy_):
    bstack111ll1l1l1l_opy_ = {
      bstack11ll11_opy_ (u"ࠦ࡮ࡴࡩࡱࡣࡷ࡬ࠧᴎ"): str(inipath),
      bstack11ll11_opy_ (u"ࠧࡸ࡯ࡰࡶࡳࡥࡹ࡮ࠢᴏ"): str(rootpath)
    }
    with open(os.path.join(log_dir, bstack11ll11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡣࡰࡰࡩ࡭࡬ࡹ࠮࡫ࡵࡲࡲࠬᴐ")), bstack11ll11_opy_ (u"ࠧࡸࠩᴑ")) as bstack111ll1ll111_opy_:
      bstack111ll1ll111_opy_.write(json.dumps(bstack111ll1l1l1l_opy_))
def bstack111ll1ll11l_opy_():
  try:
    bstack111ll1ll1ll_opy_ = os.path.join(os.getcwd(), bstack11ll11_opy_ (u"ࠨ࡮ࡲ࡫ࠬᴒ"), bstack11ll11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡦࡳࡳ࡬ࡩࡨࡵ࠱࡮ࡸࡵ࡮ࠨᴓ"))
    if os.path.exists(bstack111ll1ll1ll_opy_):
      with open(bstack111ll1ll1ll_opy_, bstack11ll11_opy_ (u"ࠪࡶࠬᴔ")) as bstack111ll1ll111_opy_:
        bstack111ll11ll11_opy_ = json.load(bstack111ll1ll111_opy_)
      return bstack111ll11ll11_opy_.get(bstack11ll11_opy_ (u"ࠫ࡮ࡴࡩࡱࡣࡷ࡬ࠬᴕ"), bstack11ll11_opy_ (u"ࠬ࠭ᴖ")), bstack111ll11ll11_opy_.get(bstack11ll11_opy_ (u"࠭ࡲࡰࡱࡷࡴࡦࡺࡨࠨᴗ"), bstack11ll11_opy_ (u"ࠧࠨᴘ"))
  except:
    pass
  return None, None
def bstack111ll1l11ll_opy_():
  try:
    bstack111ll1ll1ll_opy_ = os.path.join(os.getcwd(), bstack11ll11_opy_ (u"ࠨ࡮ࡲ࡫ࠬᴙ"), bstack11ll11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡦࡳࡳ࡬ࡩࡨࡵ࠱࡮ࡸࡵ࡮ࠨᴚ"))
    if os.path.exists(bstack111ll1ll1ll_opy_):
      os.remove(bstack111ll1ll1ll_opy_)
  except:
    pass
def bstack11ll1lllll_opy_(config):
  try:
    from bstack_utils.helper import bstack1l1ll1llll_opy_, bstack1l1l11ll1_opy_
    from browserstack_sdk.sdk_cli.cli import cli
    global bstack111ll1llll1_opy_
    if config.get(bstack11ll11_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡅࡺࡺ࡯ࡄࡣࡳࡸࡺࡸࡥࡍࡱࡪࡷࠬᴛ"), False):
      return
    uuid = os.getenv(bstack11ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩᴜ")) if os.getenv(bstack11ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪᴝ")) else bstack1l1ll1llll_opy_.get_property(bstack11ll11_opy_ (u"ࠨࡳࡥ࡭ࡕࡹࡳࡏࡤࠣᴞ"))
    if not uuid or uuid == bstack11ll11_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬᴟ"):
      return
    bstack111ll11llll_opy_ = [bstack11ll11_opy_ (u"ࠨࡴࡨࡵࡺ࡯ࡲࡦ࡯ࡨࡲࡹࡹ࠮ࡵࡺࡷࠫᴠ"), bstack11ll11_opy_ (u"ࠩࡓ࡭ࡵ࡬ࡩ࡭ࡧࠪᴡ"), bstack11ll11_opy_ (u"ࠪࡴࡾࡶࡲࡰ࡬ࡨࡧࡹ࠴ࡴࡰ࡯࡯ࠫᴢ"), bstack111ll1llll1_opy_, bstack111ll1lll11_opy_]
    bstack111ll1l11l1_opy_, root_path = bstack111ll1ll11l_opy_()
    if bstack111ll1l11l1_opy_ != None:
      bstack111ll11llll_opy_.append(bstack111ll1l11l1_opy_)
    if root_path != None:
      bstack111ll11llll_opy_.append(os.path.join(root_path, bstack11ll11_opy_ (u"ࠫࡨࡵ࡮ࡧࡶࡨࡷࡹ࠴ࡰࡺࠩᴣ")))
    bstack11ll1l1ll1_opy_()
    logging.shutdown()
    output_file = os.path.join(tempfile.gettempdir(), bstack11ll11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠲ࡲ࡯ࡨࡵ࠰ࠫᴤ") + uuid + bstack11ll11_opy_ (u"࠭࠮ࡵࡣࡵ࠲࡬ࢀࠧᴥ"))
    with tarfile.open(output_file, bstack11ll11_opy_ (u"ࠢࡸ࠼ࡪࡾࠧᴦ")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack111ll11llll_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack111ll11lll1_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack111ll1l1ll1_opy_ = data.encode()
        tarinfo.size = len(bstack111ll1l1ll1_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack111ll1l1ll1_opy_))
    bstack1l1l1llll_opy_ = MultipartEncoder(
      fields= {
        bstack11ll11_opy_ (u"ࠨࡦࡤࡸࡦ࠭ᴧ"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack11ll11_opy_ (u"ࠩࡵࡦࠬᴨ")), bstack11ll11_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰ࡺ࠰࡫ࡿ࡯ࡰࠨᴩ")),
        bstack11ll11_opy_ (u"ࠫࡨࡲࡩࡦࡰࡷࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭ᴪ"): uuid
      }
    )
    bstack111ll11ll1l_opy_ = bstack1l1l11ll1_opy_(cli.config, [bstack11ll11_opy_ (u"ࠧࡧࡰࡪࡵࠥᴫ"), bstack11ll11_opy_ (u"ࠨ࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾࠨᴬ"), bstack11ll11_opy_ (u"ࠢࡶࡲ࡯ࡳࡦࡪࠢᴭ")], bstack11ll11111ll_opy_) if cli.is_running() else bstack11ll11111ll_opy_
    response = requests.post(
      bstack11ll11_opy_ (u"ࠣࡽࢀ࠳ࡨࡲࡩࡦࡰࡷ࠱ࡱࡵࡧࡴ࠱ࡸࡴࡱࡵࡡࡥࠤᴮ").format(bstack111ll11ll1l_opy_),
      data=bstack1l1l1llll_opy_,
      headers={bstack11ll11_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨᴯ"): bstack1l1l1llll_opy_.content_type},
      auth=(config[bstack11ll11_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬᴰ")], config[bstack11ll11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧᴱ")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack11ll11_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤࡺࡶ࡬ࡰࡣࡧࠤࡱࡵࡧࡴ࠼ࠣࠫᴲ") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack11ll11_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡥ࡯ࡦ࡬ࡲ࡬ࠦ࡬ࡰࡩࡶ࠾ࠬᴳ") + str(e))
  finally:
    try:
      bstack1l1ll1l1l11_opy_()
      bstack111ll1l11ll_opy_()
    except:
      pass