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
import sys
import logging
import tarfile
import io
import os
import time
import requests
import re
from requests_toolbelt.multipart.encoder import MultipartEncoder
from bstack_utils.constants import bstack11ll1111l11_opy_, bstack11l1lll11ll_opy_, bstack11l1lll11l1_opy_
import tempfile
import json
bstack111l1ll11ll_opy_ = os.getenv(bstack1l1l1ll_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡍ࡟ࡇࡋࡏࡉࠧᶶ"), None) or os.path.join(tempfile.gettempdir(), bstack1l1l1ll_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡩ࡫ࡢࡶࡩ࠱ࡰࡴ࡭ࠢᶷ"))
bstack111ll111l11_opy_ = os.path.join(bstack1l1l1ll_opy_ (u"ࠨ࡬ࡰࡩࠥᶸ"), bstack1l1l1ll_opy_ (u"ࠧࡴࡦ࡮࠱ࡨࡲࡩ࠮ࡦࡨࡦࡺ࡭࠮࡭ࡱࡪࠫᶹ"))
logging.Formatter.converter = time.gmtime
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack1l1l1ll_opy_ (u"ࠨࠧࠫࡥࡸࡩࡴࡪ࡯ࡨ࠭ࡸ࡛ࠦࠦࠪࡱࡥࡲ࡫ࠩࡴ࡟࡞ࠩ࠭ࡲࡥࡷࡧ࡯ࡲࡦࡳࡥࠪࡵࡠࠤ࠲ࠦࠥࠩ࡯ࡨࡷࡸࡧࡧࡦࠫࡶࠫᶺ"),
      datefmt=bstack1l1l1ll_opy_ (u"ࠩࠨ࡝࠲ࠫ࡭࠮ࠧࡧࡘࠪࡎ࠺ࠦࡏ࠽ࠩࡘࡠࠧᶻ"),
      stream=sys.stdout
    )
  return logger
def bstack1lll11ll111_opy_():
  bstack111l1ll1ll1_opy_ = os.environ.get(bstack1l1l1ll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅࡍࡓࡇࡒ࡚ࡡࡇࡉࡇ࡛ࡇࠣᶼ"), bstack1l1l1ll_opy_ (u"ࠦ࡫ࡧ࡬ࡴࡧࠥᶽ"))
  return logging.DEBUG if bstack111l1ll1ll1_opy_.lower() == bstack1l1l1ll_opy_ (u"ࠧࡺࡲࡶࡧࠥᶾ") else logging.INFO
def bstack1l1lll11l1l_opy_():
  global bstack111l1ll11ll_opy_
  if os.path.exists(bstack111l1ll11ll_opy_):
    os.remove(bstack111l1ll11ll_opy_)
  if os.path.exists(bstack111ll111l11_opy_):
    os.remove(bstack111ll111l11_opy_)
def bstack1llll111l1_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def configure_logger(config, log_level):
  bstack111l1llllll_opy_ = log_level
  if bstack1l1l1ll_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨᶿ") in config and config[bstack1l1l1ll_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩ᷀")] in bstack11l1lll11ll_opy_:
    bstack111l1llllll_opy_ = bstack11l1lll11ll_opy_[config[bstack1l1l1ll_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪ᷁")]]
  if config.get(bstack1l1l1ll_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡹࡹࡵࡃࡢࡲࡷࡹࡷ࡫ࡌࡰࡩࡶ᷂ࠫ"), False):
    logging.getLogger().setLevel(bstack111l1llllll_opy_)
    return bstack111l1llllll_opy_
  global bstack111l1ll11ll_opy_
  bstack1llll111l1_opy_()
  bstack111l1llll1l_opy_ = logging.Formatter(
    fmt=bstack1l1l1ll_opy_ (u"ࠪࠩ࠭ࡧࡳࡤࡶ࡬ࡱࡪ࠯ࡳࠡ࡝ࠨࠬࡳࡧ࡭ࡦࠫࡶࡡࡠࠫࠨ࡭ࡧࡹࡩࡱࡴࡡ࡮ࡧࠬࡷࡢࠦ࠭ࠡࠧࠫࡱࡪࡹࡳࡢࡩࡨ࠭ࡸ࠭᷃"),
    datefmt=bstack1l1l1ll_opy_ (u"ࠫࠪ࡟࠭ࠦ࡯࠰ࠩࡩ࡚ࠥࡉ࠼ࠨࡑ࠿ࠫࡓ࡛ࠩ᷄"),
  )
  bstack111ll111111_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack111l1ll11ll_opy_)
  file_handler.setFormatter(bstack111l1llll1l_opy_)
  bstack111ll111111_opy_.setFormatter(bstack111l1llll1l_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack111ll111111_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack1l1l1ll_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࠮ࡸࡧࡥࡨࡷ࡯ࡶࡦࡴ࠱ࡶࡪࡳ࡯ࡵࡧ࠱ࡶࡪࡳ࡯ࡵࡧࡢࡧࡴࡴ࡮ࡦࡥࡷ࡭ࡴࡴࠧ᷅"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack111ll111111_opy_.setLevel(bstack111l1llllll_opy_)
  logging.getLogger().addHandler(bstack111ll111111_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack111l1llllll_opy_
def bstack111l1l1ll1l_opy_(config):
  try:
    bstack111ll1111ll_opy_ = set(bstack11l1lll11l1_opy_)
    bstack111l1ll1lll_opy_ = bstack1l1l1ll_opy_ (u"࠭ࠧ᷆")
    with open(bstack1l1l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠪ᷇")) as bstack111l1lll111_opy_:
      bstack111l1ll11l1_opy_ = bstack111l1lll111_opy_.read()
      bstack111l1ll1lll_opy_ = re.sub(bstack1l1l1ll_opy_ (u"ࡳࠩࡡࠬࡡࡹࠫࠪࡁࠦ࠲࠯ࠪ࡜࡯ࠩ᷈"), bstack1l1l1ll_opy_ (u"ࠩࠪ᷉"), bstack111l1ll11l1_opy_, flags=re.M)
      bstack111l1ll1lll_opy_ = re.sub(
        bstack1l1l1ll_opy_ (u"ࡵࠫࡣ࠮࡜ࡴ࠭ࠬࡃ᷊࠭࠭") + bstack1l1l1ll_opy_ (u"ࠫࢁ࠭᷋").join(bstack111ll1111ll_opy_) + bstack1l1l1ll_opy_ (u"ࠬ࠯࠮ࠫࠦࠪ᷌"),
        bstack1l1l1ll_opy_ (u"ࡸࠧ࡝࠴࠽ࠤࡠࡘࡅࡅࡃࡆࡘࡊࡊ࡝ࠨ᷍"),
        bstack111l1ll1lll_opy_, flags=re.M | re.I
      )
    def bstack111l1llll11_opy_(dic):
      bstack111ll1111l1_opy_ = {}
      for key, value in dic.items():
        if key in bstack111ll1111ll_opy_:
          bstack111ll1111l1_opy_[key] = bstack1l1l1ll_opy_ (u"ࠧ࡜ࡔࡈࡈࡆࡉࡔࡆࡆࡠ᷎ࠫ")
        else:
          if isinstance(value, dict):
            bstack111ll1111l1_opy_[key] = bstack111l1llll11_opy_(value)
          else:
            bstack111ll1111l1_opy_[key] = value
      return bstack111ll1111l1_opy_
    bstack111ll1111l1_opy_ = bstack111l1llll11_opy_(config)
    return {
      bstack1l1l1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺ࡯࡯᷏ࠫ"): bstack111l1ll1lll_opy_,
      bstack1l1l1ll_opy_ (u"ࠩࡩ࡭ࡳࡧ࡬ࡤࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲ᷐ࠬ"): json.dumps(bstack111ll1111l1_opy_)
    }
  except Exception as e:
    return {}
def bstack111l1lll1ll_opy_(inipath, rootpath):
  log_dir = os.path.join(os.getcwd(), bstack1l1l1ll_opy_ (u"ࠪࡰࡴ࡭ࠧ᷑"))
  if not os.path.exists(log_dir):
    os.makedirs(log_dir)
  bstack111l1ll111l_opy_ = os.path.join(log_dir, bstack1l1l1ll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡨࡵ࡮ࡧ࡫ࡪࡷࠬ᷒"))
  if not os.path.exists(bstack111l1ll111l_opy_):
    bstack111l1lll1l1_opy_ = {
      bstack1l1l1ll_opy_ (u"ࠧ࡯࡮ࡪࡲࡤࡸ࡭ࠨᷓ"): str(inipath),
      bstack1l1l1ll_opy_ (u"ࠨࡲࡰࡱࡷࡴࡦࡺࡨࠣᷔ"): str(rootpath)
    }
    with open(os.path.join(log_dir, bstack1l1l1ll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡤࡱࡱࡪ࡮࡭ࡳ࠯࡬ࡶࡳࡳ࠭ᷕ")), bstack1l1l1ll_opy_ (u"ࠨࡹࠪᷖ")) as bstack111l1ll1l1l_opy_:
      bstack111l1ll1l1l_opy_.write(json.dumps(bstack111l1lll1l1_opy_))
def bstack111l1lll11l_opy_():
  try:
    bstack111l1ll111l_opy_ = os.path.join(os.getcwd(), bstack1l1l1ll_opy_ (u"ࠩ࡯ࡳ࡬࠭ᷗ"), bstack1l1l1ll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡧࡴࡴࡦࡪࡩࡶ࠲࡯ࡹ࡯࡯ࠩᷘ"))
    if os.path.exists(bstack111l1ll111l_opy_):
      with open(bstack111l1ll111l_opy_, bstack1l1l1ll_opy_ (u"ࠫࡷ࠭ᷙ")) as bstack111l1ll1l1l_opy_:
        bstack111l1ll1111_opy_ = json.load(bstack111l1ll1l1l_opy_)
      return bstack111l1ll1111_opy_.get(bstack1l1l1ll_opy_ (u"ࠬ࡯࡮ࡪࡲࡤࡸ࡭࠭ᷚ"), bstack1l1l1ll_opy_ (u"࠭ࠧᷛ")), bstack111l1ll1111_opy_.get(bstack1l1l1ll_opy_ (u"ࠧࡳࡱࡲࡸࡵࡧࡴࡩࠩᷜ"), bstack1l1l1ll_opy_ (u"ࠨࠩᷝ"))
  except:
    pass
  return None, None
def bstack111l1l1llll_opy_():
  try:
    bstack111l1ll111l_opy_ = os.path.join(os.getcwd(), bstack1l1l1ll_opy_ (u"ࠩ࡯ࡳ࡬࠭ᷞ"), bstack1l1l1ll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡧࡴࡴࡦࡪࡩࡶ࠲࡯ࡹ࡯࡯ࠩᷟ"))
    if os.path.exists(bstack111l1ll111l_opy_):
      os.remove(bstack111l1ll111l_opy_)
  except:
    pass
def bstack1lll1ll11l_opy_(config):
  try:
    from bstack_utils.helper import bstack1l1l1111l1_opy_, bstack1ll11llll_opy_
    from browserstack_sdk.sdk_cli.cli import cli
    global bstack111l1ll11ll_opy_
    if config.get(bstack1l1l1ll_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡆࡻࡴࡰࡅࡤࡴࡹࡻࡲࡦࡎࡲ࡫ࡸ࠭ᷠ"), False):
      return
    uuid = os.getenv(bstack1l1l1ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪᷡ")) if os.getenv(bstack1l1l1ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫᷢ")) else bstack1l1l1111l1_opy_.get_property(bstack1l1l1ll_opy_ (u"ࠢࡴࡦ࡮ࡖࡺࡴࡉࡥࠤᷣ"))
    if not uuid or uuid == bstack1l1l1ll_opy_ (u"ࠨࡰࡸࡰࡱ࠭ᷤ"):
      return
    bstack111l1lllll1_opy_ = [bstack1l1l1ll_opy_ (u"ࠩࡵࡩࡶࡻࡩࡳࡧࡰࡩࡳࡺࡳ࠯ࡶࡻࡸࠬᷥ"), bstack1l1l1ll_opy_ (u"ࠪࡔ࡮ࡶࡦࡪ࡮ࡨࠫᷦ"), bstack1l1l1ll_opy_ (u"ࠫࡵࡿࡰࡳࡱ࡭ࡩࡨࡺ࠮ࡵࡱࡰࡰࠬᷧ"), bstack111l1ll11ll_opy_, bstack111ll111l11_opy_]
    bstack111l1l1lll1_opy_, root_path = bstack111l1lll11l_opy_()
    if bstack111l1l1lll1_opy_ != None:
      bstack111l1lllll1_opy_.append(bstack111l1l1lll1_opy_)
    if root_path != None:
      bstack111l1lllll1_opy_.append(os.path.join(root_path, bstack1l1l1ll_opy_ (u"ࠬࡩ࡯࡯ࡨࡷࡩࡸࡺ࠮ࡱࡻࠪᷨ")))
    bstack1llll111l1_opy_()
    logging.shutdown()
    output_file = os.path.join(tempfile.gettempdir(), bstack1l1l1ll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࠳࡬ࡰࡩࡶ࠱ࠬᷩ") + uuid + bstack1l1l1ll_opy_ (u"ࠧ࠯ࡶࡤࡶ࠳࡭ࡺࠨᷪ"))
    with tarfile.open(output_file, bstack1l1l1ll_opy_ (u"ࠣࡹ࠽࡫ࡿࠨᷫ")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack111l1lllll1_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack111l1l1ll1l_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack111ll11111l_opy_ = data.encode()
        tarinfo.size = len(bstack111ll11111l_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack111ll11111l_opy_))
    bstack11ll11ll1l_opy_ = MultipartEncoder(
      fields= {
        bstack1l1l1ll_opy_ (u"ࠩࡧࡥࡹࡧࠧᷬ"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack1l1l1ll_opy_ (u"ࠪࡶࡧ࠭ᷭ")), bstack1l1l1ll_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱ࡻ࠱࡬ࢀࡩࡱࠩᷮ")),
        bstack1l1l1ll_opy_ (u"ࠬࡩ࡬ࡪࡧࡱࡸࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧᷯ"): uuid
      }
    )
    bstack111l1ll1l11_opy_ = bstack1ll11llll_opy_(cli.config, [bstack1l1l1ll_opy_ (u"ࠨࡡࡱ࡫ࡶࠦᷰ"), bstack1l1l1ll_opy_ (u"ࠢࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠢᷱ"), bstack1l1l1ll_opy_ (u"ࠣࡷࡳࡰࡴࡧࡤࠣᷲ")], bstack11ll1111l11_opy_)
    response = requests.post(
      bstack1l1l1ll_opy_ (u"ࠤࡾࢁ࠴ࡩ࡬ࡪࡧࡱࡸ࠲ࡲ࡯ࡨࡵ࠲ࡹࡵࡲ࡯ࡢࡦࠥᷳ").format(bstack111l1ll1l11_opy_),
      data=bstack11ll11ll1l_opy_,
      headers={bstack1l1l1ll_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩᷴ"): bstack11ll11ll1l_opy_.content_type},
      auth=(config[bstack1l1l1ll_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭᷵")], config[bstack1l1l1ll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ᷶")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack1l1l1ll_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥࡻࡰ࡭ࡱࡤࡨࠥࡲ࡯ࡨࡵ࠽ࠤ᷷ࠬ") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack1l1l1ll_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡦࡰࡧ࡭ࡳ࡭ࠠ࡭ࡱࡪࡷ࠿᷸࠭") + str(e))
  finally:
    try:
      bstack1l1lll11l1l_opy_()
      bstack111l1l1llll_opy_()
    except:
      pass