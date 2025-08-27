# coding: UTF-8
import sys
bstack1ll1111_opy_ = sys.version_info [0] == 2
bstack1111l1l_opy_ = 2048
bstack1l111_opy_ = 7
def bstack1111lll_opy_ (bstack1llll11_opy_):
    global bstack1llll1_opy_
    bstack1l111l_opy_ = ord (bstack1llll11_opy_ [-1])
    bstack11111l_opy_ = bstack1llll11_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1l111l_opy_ % len (bstack11111l_opy_)
    bstack1l111l1_opy_ = bstack11111l_opy_ [:bstack1l11ll_opy_] + bstack11111l_opy_ [bstack1l11ll_opy_:]
    if bstack1ll1111_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    return eval (bstack1_opy_)
import sys
import logging
import tarfile
import io
import os
import time
import requests
import re
from requests_toolbelt.multipart.encoder import MultipartEncoder
from bstack_utils.constants import bstack11ll11111l1_opy_, bstack11l1ll1llll_opy_, bstack11l1lll1lll_opy_
import tempfile
import json
bstack111l1llll11_opy_ = os.getenv(bstack1111lll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡊࡣࡋࡏࡌࡆࠤᶞ"), None) or os.path.join(tempfile.gettempdir(), bstack1111lll_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡦࡨࡦࡺ࡭࠮࡭ࡱࡪࠦᶟ"))
bstack111l1lll111_opy_ = os.path.join(bstack1111lll_opy_ (u"ࠥࡰࡴ࡭ࠢᶠ"), bstack1111lll_opy_ (u"ࠫࡸࡪ࡫࠮ࡥ࡯࡭࠲ࡪࡥࡣࡷࡪ࠲ࡱࡵࡧࠨᶡ"))
logging.Formatter.converter = time.gmtime
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack1111lll_opy_ (u"ࠬࠫࠨࡢࡵࡦࡸ࡮ࡳࡥࠪࡵࠣ࡟ࠪ࠮࡮ࡢ࡯ࡨ࠭ࡸࡣ࡛ࠦࠪ࡯ࡩࡻ࡫࡬࡯ࡣࡰࡩ࠮ࡹ࡝ࠡ࠯ࠣࠩ࠭ࡳࡥࡴࡵࡤ࡫ࡪ࠯ࡳࠨᶢ"),
      datefmt=bstack1111lll_opy_ (u"࡚࠭ࠥ࠯ࠨࡱ࠲ࠫࡤࡕࠧࡋ࠾ࠪࡓ࠺ࠦࡕ࡝ࠫᶣ"),
      stream=sys.stdout
    )
  return logger
def bstack1lll11l111l_opy_():
  bstack111l1l1ll11_opy_ = os.environ.get(bstack1111lll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡊࡐࡄࡖ࡞ࡥࡄࡆࡄࡘࡋࠧᶤ"), bstack1111lll_opy_ (u"ࠣࡨࡤࡰࡸ࡫ࠢᶥ"))
  return logging.DEBUG if bstack111l1l1ll11_opy_.lower() == bstack1111lll_opy_ (u"ࠤࡷࡶࡺ࡫ࠢᶦ") else logging.INFO
def bstack1l1lll11lll_opy_():
  global bstack111l1llll11_opy_
  if os.path.exists(bstack111l1llll11_opy_):
    os.remove(bstack111l1llll11_opy_)
  if os.path.exists(bstack111l1lll111_opy_):
    os.remove(bstack111l1lll111_opy_)
def bstack1ll1l11111_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def configure_logger(config, log_level):
  bstack111l1l1ll1l_opy_ = log_level
  if bstack1111lll_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬᶧ") in config and config[bstack1111lll_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭ᶨ")] in bstack11l1ll1llll_opy_:
    bstack111l1l1ll1l_opy_ = bstack11l1ll1llll_opy_[config[bstack1111lll_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧᶩ")]]
  if config.get(bstack1111lll_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡁࡶࡶࡲࡇࡦࡶࡴࡶࡴࡨࡐࡴ࡭ࡳࠨᶪ"), False):
    logging.getLogger().setLevel(bstack111l1l1ll1l_opy_)
    return bstack111l1l1ll1l_opy_
  global bstack111l1llll11_opy_
  bstack1ll1l11111_opy_()
  bstack111l1ll1ll1_opy_ = logging.Formatter(
    fmt=bstack1111lll_opy_ (u"ࠧࠦࠪࡤࡷࡨࡺࡩ࡮ࡧࠬࡷࠥࡡࠥࠩࡰࡤࡱࡪ࠯ࡳ࡞࡝ࠨࠬࡱ࡫ࡶࡦ࡮ࡱࡥࡲ࡫ࠩࡴ࡟ࠣ࠱ࠥࠫࠨ࡮ࡧࡶࡷࡦ࡭ࡥࠪࡵࠪᶫ"),
    datefmt=bstack1111lll_opy_ (u"ࠨࠧ࡜࠱ࠪࡳ࠭ࠦࡦࡗࠩࡍࡀࠥࡎ࠼ࠨࡗ࡟࠭ᶬ"),
  )
  bstack111l1lll1l1_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack111l1llll11_opy_)
  file_handler.setFormatter(bstack111l1ll1ll1_opy_)
  bstack111l1lll1l1_opy_.setFormatter(bstack111l1ll1ll1_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack111l1lll1l1_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack1111lll_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࠲ࡼ࡫ࡢࡥࡴ࡬ࡺࡪࡸ࠮ࡳࡧࡰࡳࡹ࡫࠮ࡳࡧࡰࡳࡹ࡫࡟ࡤࡱࡱࡲࡪࡩࡴࡪࡱࡱࠫᶭ"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack111l1lll1l1_opy_.setLevel(bstack111l1l1ll1l_opy_)
  logging.getLogger().addHandler(bstack111l1lll1l1_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack111l1l1ll1l_opy_
def bstack111ll111111_opy_(config):
  try:
    bstack111l1ll1111_opy_ = set(bstack11l1lll1lll_opy_)
    bstack111l1ll1lll_opy_ = bstack1111lll_opy_ (u"ࠪࠫᶮ")
    with open(bstack1111lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡲࡲࠧᶯ")) as bstack111l1llllll_opy_:
      bstack111l1lll11l_opy_ = bstack111l1llllll_opy_.read()
      bstack111l1ll1lll_opy_ = re.sub(bstack1111lll_opy_ (u"ࡷ࠭࡞ࠩ࡞ࡶ࠯࠮ࡅࠣ࠯ࠬࠧࡠࡳ࠭ᶰ"), bstack1111lll_opy_ (u"࠭ࠧᶱ"), bstack111l1lll11l_opy_, flags=re.M)
      bstack111l1ll1lll_opy_ = re.sub(
        bstack1111lll_opy_ (u"ࡲࠨࡠࠫࡠࡸ࠱ࠩࡀࠪࠪᶲ") + bstack1111lll_opy_ (u"ࠨࡾࠪᶳ").join(bstack111l1ll1111_opy_) + bstack1111lll_opy_ (u"ࠩࠬ࠲࠯ࠪࠧᶴ"),
        bstack1111lll_opy_ (u"ࡵࠫࡡ࠸࠺ࠡ࡝ࡕࡉࡉࡇࡃࡕࡇࡇࡡࠬᶵ"),
        bstack111l1ll1lll_opy_, flags=re.M | re.I
      )
    def bstack111l1ll11l1_opy_(dic):
      bstack111l1llll1l_opy_ = {}
      for key, value in dic.items():
        if key in bstack111l1ll1111_opy_:
          bstack111l1llll1l_opy_[key] = bstack1111lll_opy_ (u"ࠫࡠࡘࡅࡅࡃࡆࡘࡊࡊ࡝ࠨᶶ")
        else:
          if isinstance(value, dict):
            bstack111l1llll1l_opy_[key] = bstack111l1ll11l1_opy_(value)
          else:
            bstack111l1llll1l_opy_[key] = value
      return bstack111l1llll1l_opy_
    bstack111l1llll1l_opy_ = bstack111l1ll11l1_opy_(config)
    return {
      bstack1111lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡾࡳ࡬ࠨᶷ"): bstack111l1ll1lll_opy_,
      bstack1111lll_opy_ (u"࠭ࡦࡪࡰࡤࡰࡨࡵ࡮ࡧ࡫ࡪ࠲࡯ࡹ࡯࡯ࠩᶸ"): json.dumps(bstack111l1llll1l_opy_)
    }
  except Exception as e:
    return {}
def bstack111l1l1l1l1_opy_(inipath, rootpath):
  log_dir = os.path.join(os.getcwd(), bstack1111lll_opy_ (u"ࠧ࡭ࡱࡪࠫᶹ"))
  if not os.path.exists(log_dir):
    os.makedirs(log_dir)
  bstack111l1l1l1ll_opy_ = os.path.join(log_dir, bstack1111lll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡥࡲࡲ࡫࡯ࡧࡴࠩᶺ"))
  if not os.path.exists(bstack111l1l1l1ll_opy_):
    bstack111l1lllll1_opy_ = {
      bstack1111lll_opy_ (u"ࠤ࡬ࡲ࡮ࡶࡡࡵࡪࠥᶻ"): str(inipath),
      bstack1111lll_opy_ (u"ࠥࡶࡴࡵࡴࡱࡣࡷ࡬ࠧᶼ"): str(rootpath)
    }
    with open(os.path.join(log_dir, bstack1111lll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡨࡵ࡮ࡧ࡫ࡪࡷ࠳ࡰࡳࡰࡰࠪᶽ")), bstack1111lll_opy_ (u"ࠬࡽࠧᶾ")) as bstack111ll11111l_opy_:
      bstack111ll11111l_opy_.write(json.dumps(bstack111l1lllll1_opy_))
def bstack111l1ll1l11_opy_():
  try:
    bstack111l1l1l1ll_opy_ = os.path.join(os.getcwd(), bstack1111lll_opy_ (u"࠭࡬ࡰࡩࠪᶿ"), bstack1111lll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡤࡱࡱࡪ࡮࡭ࡳ࠯࡬ࡶࡳࡳ࠭᷀"))
    if os.path.exists(bstack111l1l1l1ll_opy_):
      with open(bstack111l1l1l1ll_opy_, bstack1111lll_opy_ (u"ࠨࡴࠪ᷁")) as bstack111ll11111l_opy_:
        bstack111l1ll111l_opy_ = json.load(bstack111ll11111l_opy_)
      return bstack111l1ll111l_opy_.get(bstack1111lll_opy_ (u"ࠩ࡬ࡲ࡮ࡶࡡࡵࡪ᷂ࠪ"), bstack1111lll_opy_ (u"ࠪࠫ᷃")), bstack111l1ll111l_opy_.get(bstack1111lll_opy_ (u"ࠫࡷࡵ࡯ࡵࡲࡤࡸ࡭࠭᷄"), bstack1111lll_opy_ (u"ࠬ࠭᷅"))
  except:
    pass
  return None, None
def bstack111l1l1lll1_opy_():
  try:
    bstack111l1l1l1ll_opy_ = os.path.join(os.getcwd(), bstack1111lll_opy_ (u"࠭࡬ࡰࡩࠪ᷆"), bstack1111lll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡤࡱࡱࡪ࡮࡭ࡳ࠯࡬ࡶࡳࡳ࠭᷇"))
    if os.path.exists(bstack111l1l1l1ll_opy_):
      os.remove(bstack111l1l1l1ll_opy_)
  except:
    pass
def bstack1lll1ll1ll_opy_(config):
  try:
    from bstack_utils.helper import bstack1ll111ll11_opy_, bstack1l1ll11l1l_opy_
    from browserstack_sdk.sdk_cli.cli import cli
    global bstack111l1llll11_opy_
    if config.get(bstack1111lll_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦࡃࡸࡸࡴࡉࡡࡱࡶࡸࡶࡪࡒ࡯ࡨࡵࠪ᷈"), False):
      return
    uuid = os.getenv(bstack1111lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ᷉")) if os.getenv(bstack1111lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ᷊")) else bstack1ll111ll11_opy_.get_property(bstack1111lll_opy_ (u"ࠦࡸࡪ࡫ࡓࡷࡱࡍࡩࠨ᷋"))
    if not uuid or uuid == bstack1111lll_opy_ (u"ࠬࡴࡵ࡭࡮ࠪ᷌"):
      return
    bstack111l1ll11ll_opy_ = [bstack1111lll_opy_ (u"࠭ࡲࡦࡳࡸ࡭ࡷ࡫࡭ࡦࡰࡷࡷ࠳ࡺࡸࡵࠩ᷍"), bstack1111lll_opy_ (u"ࠧࡑ࡫ࡳࡪ࡮ࡲࡥࠨ᷎"), bstack1111lll_opy_ (u"ࠨࡲࡼࡴࡷࡵࡪࡦࡥࡷ࠲ࡹࡵ࡭࡭᷏ࠩ"), bstack111l1llll11_opy_, bstack111l1lll111_opy_]
    bstack111l1ll1l1l_opy_, root_path = bstack111l1ll1l11_opy_()
    if bstack111l1ll1l1l_opy_ != None:
      bstack111l1ll11ll_opy_.append(bstack111l1ll1l1l_opy_)
    if root_path != None:
      bstack111l1ll11ll_opy_.append(os.path.join(root_path, bstack1111lll_opy_ (u"ࠩࡦࡳࡳ࡬ࡴࡦࡵࡷ࠲ࡵࡿ᷐ࠧ")))
    bstack1ll1l11111_opy_()
    logging.shutdown()
    output_file = os.path.join(tempfile.gettempdir(), bstack1111lll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠰ࡰࡴ࡭ࡳ࠮ࠩ᷑") + uuid + bstack1111lll_opy_ (u"ࠫ࠳ࡺࡡࡳ࠰ࡪࡾࠬ᷒"))
    with tarfile.open(output_file, bstack1111lll_opy_ (u"ࠧࡽ࠺ࡨࡼࠥᷓ")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack111l1ll11ll_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack111ll111111_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack111l1l1llll_opy_ = data.encode()
        tarinfo.size = len(bstack111l1l1llll_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack111l1l1llll_opy_))
    bstack1lllllllll_opy_ = MultipartEncoder(
      fields= {
        bstack1111lll_opy_ (u"࠭ࡤࡢࡶࡤࠫᷔ"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack1111lll_opy_ (u"ࠧࡳࡤࠪᷕ")), bstack1111lll_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡸ࠮ࡩࡽ࡭ࡵ࠭ᷖ")),
        bstack1111lll_opy_ (u"ࠩࡦࡰ࡮࡫࡮ࡵࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫᷗ"): uuid
      }
    )
    bstack111l1lll1ll_opy_ = bstack1l1ll11l1l_opy_(cli.config, [bstack1111lll_opy_ (u"ࠥࡥࡵ࡯ࡳࠣᷘ"), bstack1111lll_opy_ (u"ࠦࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠦᷙ"), bstack1111lll_opy_ (u"ࠧࡻࡰ࡭ࡱࡤࡨࠧᷚ")], bstack11ll11111l1_opy_)
    response = requests.post(
      bstack1111lll_opy_ (u"ࠨࡻࡾ࠱ࡦࡰ࡮࡫࡮ࡵ࠯࡯ࡳ࡬ࡹ࠯ࡶࡲ࡯ࡳࡦࡪࠢᷛ").format(bstack111l1lll1ll_opy_),
      data=bstack1lllllllll_opy_,
      headers={bstack1111lll_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭ᷜ"): bstack1lllllllll_opy_.content_type},
      auth=(config[bstack1111lll_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪᷝ")], config[bstack1111lll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬᷞ")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack1111lll_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢࡸࡴࡱࡵࡡࡥࠢ࡯ࡳ࡬ࡹ࠺ࠡࠩᷟ") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack1111lll_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡪࡴࡤࡪࡰࡪࠤࡱࡵࡧࡴ࠼ࠪᷠ") + str(e))
  finally:
    try:
      bstack1l1lll11lll_opy_()
      bstack111l1l1lll1_opy_()
    except:
      pass