# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1l11lll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstackl_opy_ (bstack1111111_opy_):
    global bstack1lllll1_opy_
    bstack111l111_opy_ = ord (bstack1111111_opy_ [-1])
    bstack1l11l11_opy_ = bstack1111111_opy_ [:-1]
    bstack1lll1l1_opy_ = bstack111l111_opy_ % len (bstack1l11l11_opy_)
    bstack1llll1_opy_ = bstack1l11l11_opy_ [:bstack1lll1l1_opy_] + bstack1l11l11_opy_ [bstack1lll1l1_opy_:]
    if bstack111ll1_opy_:
        bstack1llll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    else:
        bstack1llll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    return eval (bstack1llll1l_opy_)
import collections
import datetime
import json
import os
import platform
import re
import subprocess
import traceback
import tempfile
import multiprocessing
import threading
import sys
import logging
from math import ceil
import urllib
from urllib.parse import urlparse
import copy
import zipfile
import git
import requests
from packaging import version
from bstack_utils.config import Config
from bstack_utils.constants import (bstack1l111l1l1_opy_, bstack1lllll1ll_opy_, bstack1l111l1ll_opy_,
                                    bstack11l1ll1lll1_opy_, bstack11l1l1lll11_opy_, bstack11l1lllllll_opy_, bstack11l1ll1l1ll_opy_)
from bstack_utils.measure import measure
from bstack_utils.messages import bstack1l111llll_opy_, bstack1l111ll1l_opy_
from bstack_utils.proxy import bstack111l11ll1_opy_, bstack1l1ll1l1ll_opy_
from bstack_utils.constants import *
from bstack_utils import bstack1ll11l1ll_opy_
from bstack_utils.bstack1l111l11_opy_ import bstack1ll1lll11_opy_
from browserstack_sdk._version import __version__
bstack1l1llll1l1_opy_ = Config.bstack1l1l11ll_opy_()
logger = bstack1ll11l1ll_opy_.get_logger(__name__, bstack1ll11l1ll_opy_.bstack1lll1l11lll_opy_())
def bstack11ll1l1111l_opy_(config):
    return config[bstackl_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ᫯")]
def bstack11ll1l1l11l_opy_(config):
    return config[bstackl_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ᫰")]
def bstack11llllllll_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack11l11l11111_opy_(obj):
    values = []
    bstack111lll1l11l_opy_ = re.compile(bstackl_opy_ (u"ࡴࠥࡢࡈ࡛ࡓࡕࡑࡐࡣ࡙ࡇࡇࡠ࡞ࡧ࠯ࠩࠨ᫱"), re.I)
    for key in obj.keys():
        if bstack111lll1l11l_opy_.match(key):
            values.append(obj[key])
    return values
def bstack111llll11l1_opy_(config):
    tags = []
    tags.extend(bstack11l11l11111_opy_(os.environ))
    tags.extend(bstack11l11l11111_opy_(config))
    return tags
def bstack11l1111l1l1_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack111lll1ll1l_opy_(bstack111lllll11l_opy_):
    if not bstack111lllll11l_opy_:
        return bstackl_opy_ (u"ࠪࠫ᫲")
    return bstackl_opy_ (u"ࠦࢀࢃࠠࠩࡽࢀ࠭ࠧ᫳").format(bstack111lllll11l_opy_.name, bstack111lllll11l_opy_.email)
def bstack11lll111ll1_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack111llll1ll1_opy_ = repo.common_dir
        info = {
            bstackl_opy_ (u"ࠧࡹࡨࡢࠤ᫴"): repo.head.commit.hexsha,
            bstackl_opy_ (u"ࠨࡳࡩࡱࡵࡸࡤࡹࡨࡢࠤ᫵"): repo.git.rev_parse(repo.head.commit, short=True),
            bstackl_opy_ (u"ࠢࡣࡴࡤࡲࡨ࡮ࠢ᫶"): repo.active_branch.name,
            bstackl_opy_ (u"ࠣࡶࡤ࡫ࠧ᫷"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstackl_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡶࡨࡶࠧ᫸"): bstack111lll1ll1l_opy_(repo.head.commit.committer),
            bstackl_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡷࡩࡷࡥࡤࡢࡶࡨࠦ᫹"): repo.head.commit.committed_datetime.isoformat(),
            bstackl_opy_ (u"ࠦࡦࡻࡴࡩࡱࡵࠦ᫺"): bstack111lll1ll1l_opy_(repo.head.commit.author),
            bstackl_opy_ (u"ࠧࡧࡵࡵࡪࡲࡶࡤࡪࡡࡵࡧࠥ᫻"): repo.head.commit.authored_datetime.isoformat(),
            bstackl_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡥ࡭ࡦࡵࡶࡥ࡬࡫ࠢ᫼"): repo.head.commit.message,
            bstackl_opy_ (u"ࠢࡳࡱࡲࡸࠧ᫽"): repo.git.rev_parse(bstackl_opy_ (u"ࠣ࠯࠰ࡷ࡭ࡵࡷ࠮ࡶࡲࡴࡱ࡫ࡶࡦ࡮ࠥ᫾")),
            bstackl_opy_ (u"ࠤࡦࡳࡲࡳ࡯࡯ࡡࡪ࡭ࡹࡥࡤࡪࡴࠥ᫿"): bstack111llll1ll1_opy_,
            bstackl_opy_ (u"ࠥࡻࡴࡸ࡫ࡵࡴࡨࡩࡤ࡭ࡩࡵࡡࡧ࡭ࡷࠨᬀ"): subprocess.check_output([bstackl_opy_ (u"ࠦ࡬࡯ࡴࠣᬁ"), bstackl_opy_ (u"ࠧࡸࡥࡷ࠯ࡳࡥࡷࡹࡥࠣᬂ"), bstackl_opy_ (u"ࠨ࠭࠮ࡩ࡬ࡸ࠲ࡩ࡯࡮࡯ࡲࡲ࠲ࡪࡩࡳࠤᬃ")]).strip().decode(
                bstackl_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭ᬄ")),
            bstackl_opy_ (u"ࠣ࡮ࡤࡷࡹࡥࡴࡢࡩࠥᬅ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstackl_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡵࡢࡷ࡮ࡴࡣࡦࡡ࡯ࡥࡸࡺ࡟ࡵࡣࡪࠦᬆ"): repo.git.rev_list(
                bstackl_opy_ (u"ࠥࡿࢂ࠴࠮ࡼࡿࠥᬇ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack111llll1lll_opy_ = []
        for remote in remotes:
            bstack11l1l111111_opy_ = {
                bstackl_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᬈ"): remote.name,
                bstackl_opy_ (u"ࠧࡻࡲ࡭ࠤᬉ"): remote.url,
            }
            bstack111llll1lll_opy_.append(bstack11l1l111111_opy_)
        bstack11l11lll1ll_opy_ = {
            bstackl_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᬊ"): bstackl_opy_ (u"ࠢࡨ࡫ࡷࠦᬋ"),
            **info,
            bstackl_opy_ (u"ࠣࡴࡨࡱࡴࡺࡥࡴࠤᬌ"): bstack111llll1lll_opy_
        }
        bstack11l11lll1ll_opy_ = bstack11l111l1l1l_opy_(bstack11l11lll1ll_opy_)
        return bstack11l11lll1ll_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstackl_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡲࡴࡺࡲࡡࡵ࡫ࡱ࡫ࠥࡍࡩࡵࠢࡰࡩࡹࡧࡤࡢࡶࡤࠤࡼ࡯ࡴࡩࠢࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠧᬍ").format(err))
        return {}
def bstack11l111l1l1l_opy_(bstack11l11lll1ll_opy_):
    bstack11l11ll11ll_opy_ = bstack111lll1l111_opy_(bstack11l11lll1ll_opy_)
    if bstack11l11ll11ll_opy_ and bstack11l11ll11ll_opy_ > bstack11l1ll1lll1_opy_:
        bstack11l11l1l11l_opy_ = bstack11l11ll11ll_opy_ - bstack11l1ll1lll1_opy_
        bstack11l111ll1l1_opy_ = bstack11l111ll111_opy_(bstack11l11lll1ll_opy_[bstackl_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡢࡱࡪࡹࡳࡢࡩࡨࠦᬎ")], bstack11l11l1l11l_opy_)
        bstack11l11lll1ll_opy_[bstackl_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡣࡲ࡫ࡳࡴࡣࡪࡩࠧᬏ")] = bstack11l111ll1l1_opy_
        logger.info(bstackl_opy_ (u"࡚ࠧࡨࡦࠢࡦࡳࡲࡳࡩࡵࠢ࡫ࡥࡸࠦࡢࡦࡧࡱࠤࡹࡸࡵ࡯ࡥࡤࡸࡪࡪ࠮ࠡࡕ࡬ࡾࡪࠦ࡯ࡧࠢࡦࡳࡲࡳࡩࡵࠢࡤࡪࡹ࡫ࡲࠡࡶࡵࡹࡳࡩࡡࡵ࡫ࡲࡲࠥ࡯ࡳࠡࡽࢀࠤࡐࡈࠢᬐ")
                    .format(bstack111lll1l111_opy_(bstack11l11lll1ll_opy_) / 1024))
    return bstack11l11lll1ll_opy_
def bstack111lll1l111_opy_(bstack1ll1l1lll_opy_):
    try:
        if bstack1ll1l1lll_opy_:
            bstack11l11lllll1_opy_ = json.dumps(bstack1ll1l1lll_opy_)
            bstack111lll1llll_opy_ = sys.getsizeof(bstack11l11lllll1_opy_)
            return bstack111lll1llll_opy_
    except Exception as e:
        logger.debug(bstackl_opy_ (u"ࠨࡓࡰ࡯ࡨࡸ࡭࡯࡮ࡨࠢࡺࡩࡳࡺࠠࡸࡴࡲࡲ࡬ࠦࡷࡩ࡫࡯ࡩࠥࡩࡡ࡭ࡥࡸࡰࡦࡺࡩ࡯ࡩࠣࡷ࡮ࢀࡥࠡࡱࡩࠤࡏ࡙ࡏࡏࠢࡲࡦ࡯࡫ࡣࡵ࠼ࠣࡿࢂࠨᬑ").format(e))
    return -1
def bstack11l111ll111_opy_(field, bstack11l11l1l111_opy_):
    try:
        bstack111lllll1l1_opy_ = len(bytes(bstack11l1l1lll11_opy_, bstackl_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭ᬒ")))
        bstack111llll1111_opy_ = bytes(field, bstackl_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧᬓ"))
        bstack11l1111l111_opy_ = len(bstack111llll1111_opy_)
        bstack11l11l11l1l_opy_ = ceil(bstack11l1111l111_opy_ - bstack11l11l1l111_opy_ - bstack111lllll1l1_opy_)
        if bstack11l11l11l1l_opy_ > 0:
            bstack11l11l111l1_opy_ = bstack111llll1111_opy_[:bstack11l11l11l1l_opy_].decode(bstackl_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨᬔ"), errors=bstackl_opy_ (u"ࠪ࡭࡬ࡴ࡯ࡳࡧࠪᬕ")) + bstack11l1l1lll11_opy_
            return bstack11l11l111l1_opy_
    except Exception as e:
        logger.debug(bstackl_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡷࡶࡺࡴࡣࡢࡶ࡬ࡲ࡬ࠦࡦࡪࡧ࡯ࡨ࠱ࠦ࡮ࡰࡶ࡫࡭ࡳ࡭ࠠࡸࡣࡶࠤࡹࡸࡵ࡯ࡥࡤࡸࡪࡪࠠࡩࡧࡵࡩ࠿ࠦࡻࡾࠤᬖ").format(e))
    return field
def bstack1111l1l1l_opy_():
    env = os.environ
    if (bstackl_opy_ (u"ࠧࡐࡅࡏࡍࡌࡒࡘࡥࡕࡓࡎࠥᬗ") in env and len(env[bstackl_opy_ (u"ࠨࡊࡆࡐࡎࡍࡓ࡙࡟ࡖࡔࡏࠦᬘ")]) > 0) or (
            bstackl_opy_ (u"ࠢࡋࡇࡑࡏࡎࡔࡓࡠࡊࡒࡑࡊࠨᬙ") in env and len(env[bstackl_opy_ (u"ࠣࡌࡈࡒࡐࡏࡎࡔࡡࡋࡓࡒࡋࠢᬚ")]) > 0):
        return {
            bstackl_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᬛ"): bstackl_opy_ (u"ࠥࡎࡪࡴ࡫ࡪࡰࡶࠦᬜ"),
            bstackl_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᬝ"): env.get(bstackl_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣᬞ")),
            bstackl_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᬟ"): env.get(bstackl_opy_ (u"ࠢࡋࡑࡅࡣࡓࡇࡍࡆࠤᬠ")),
            bstackl_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᬡ"): env.get(bstackl_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣᬢ"))
        }
    if env.get(bstackl_opy_ (u"ࠥࡇࡎࠨᬣ")) == bstackl_opy_ (u"ࠦࡹࡸࡵࡦࠤᬤ") and bstack11l1111ll_opy_(env.get(bstackl_opy_ (u"ࠧࡉࡉࡓࡅࡏࡉࡈࡏࠢᬥ"))):
        return {
            bstackl_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᬦ"): bstackl_opy_ (u"ࠢࡄ࡫ࡵࡧࡱ࡫ࡃࡊࠤᬧ"),
            bstackl_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᬨ"): env.get(bstackl_opy_ (u"ࠤࡆࡍࡗࡉࡌࡆࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧᬩ")),
            bstackl_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᬪ"): env.get(bstackl_opy_ (u"ࠦࡈࡏࡒࡄࡎࡈࡣࡏࡕࡂࠣᬫ")),
            bstackl_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᬬ"): env.get(bstackl_opy_ (u"ࠨࡃࡊࡔࡆࡐࡊࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࠤᬭ"))
        }
    if env.get(bstackl_opy_ (u"ࠢࡄࡋࠥᬮ")) == bstackl_opy_ (u"ࠣࡶࡵࡹࡪࠨᬯ") and bstack11l1111ll_opy_(env.get(bstackl_opy_ (u"ࠤࡗࡖࡆ࡜ࡉࡔࠤᬰ"))):
        return {
            bstackl_opy_ (u"ࠥࡲࡦࡳࡥࠣᬱ"): bstackl_opy_ (u"࡙ࠦࡸࡡࡷ࡫ࡶࠤࡈࡏࠢᬲ"),
            bstackl_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᬳ"): env.get(bstackl_opy_ (u"ࠨࡔࡓࡃ࡙ࡍࡘࡥࡂࡖࡋࡏࡈࡤ࡝ࡅࡃࡡࡘࡖࡑࠨ᬴")),
            bstackl_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᬵ"): env.get(bstackl_opy_ (u"ࠣࡖࡕࡅ࡛ࡏࡓࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥᬶ")),
            bstackl_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᬷ"): env.get(bstackl_opy_ (u"ࠥࡘࡗࡇࡖࡊࡕࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤᬸ"))
        }
    if env.get(bstackl_opy_ (u"ࠦࡈࡏࠢᬹ")) == bstackl_opy_ (u"ࠧࡺࡲࡶࡧࠥᬺ") and env.get(bstackl_opy_ (u"ࠨࡃࡊࡡࡑࡅࡒࡋࠢᬻ")) == bstackl_opy_ (u"ࠢࡤࡱࡧࡩࡸ࡮ࡩࡱࠤᬼ"):
        return {
            bstackl_opy_ (u"ࠣࡰࡤࡱࡪࠨᬽ"): bstackl_opy_ (u"ࠤࡆࡳࡩ࡫ࡳࡩ࡫ࡳࠦᬾ"),
            bstackl_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᬿ"): None,
            bstackl_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᭀ"): None,
            bstackl_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᭁ"): None
        }
    if env.get(bstackl_opy_ (u"ࠨࡂࡊࡖࡅ࡙ࡈࡑࡅࡕࡡࡅࡖࡆࡔࡃࡉࠤᭂ")) and env.get(bstackl_opy_ (u"ࠢࡃࡋࡗࡆ࡚ࡉࡋࡆࡖࡢࡇࡔࡓࡍࡊࡖࠥᭃ")):
        return {
            bstackl_opy_ (u"ࠣࡰࡤࡱࡪࠨ᭄"): bstackl_opy_ (u"ࠤࡅ࡭ࡹࡨࡵࡤ࡭ࡨࡸࠧᭅ"),
            bstackl_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᭆ"): env.get(bstackl_opy_ (u"ࠦࡇࡏࡔࡃࡗࡆࡏࡊ࡚࡟ࡈࡋࡗࡣࡍ࡚ࡔࡑࡡࡒࡖࡎࡍࡉࡏࠤᭇ")),
            bstackl_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᭈ"): None,
            bstackl_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᭉ"): env.get(bstackl_opy_ (u"ࠢࡃࡋࡗࡆ࡚ࡉࡋࡆࡖࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤᭊ"))
        }
    if env.get(bstackl_opy_ (u"ࠣࡅࡌࠦᭋ")) == bstackl_opy_ (u"ࠤࡷࡶࡺ࡫ࠢᭌ") and bstack11l1111ll_opy_(env.get(bstackl_opy_ (u"ࠥࡈࡗࡕࡎࡆࠤ᭍"))):
        return {
            bstackl_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᭎"): bstackl_opy_ (u"ࠧࡊࡲࡰࡰࡨࠦ᭏"),
            bstackl_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ᭐"): env.get(bstackl_opy_ (u"ࠢࡅࡔࡒࡒࡊࡥࡂࡖࡋࡏࡈࡤࡒࡉࡏࡍࠥ᭑")),
            bstackl_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ᭒"): None,
            bstackl_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ᭓"): env.get(bstackl_opy_ (u"ࠥࡈࡗࡕࡎࡆࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣ᭔"))
        }
    if env.get(bstackl_opy_ (u"ࠦࡈࡏࠢ᭕")) == bstackl_opy_ (u"ࠧࡺࡲࡶࡧࠥ᭖") and bstack11l1111ll_opy_(env.get(bstackl_opy_ (u"ࠨࡓࡆࡏࡄࡔࡍࡕࡒࡆࠤ᭗"))):
        return {
            bstackl_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ᭘"): bstackl_opy_ (u"ࠣࡕࡨࡱࡦࡶࡨࡰࡴࡨࠦ᭙"),
            bstackl_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ᭚"): env.get(bstackl_opy_ (u"ࠥࡗࡊࡓࡁࡑࡊࡒࡖࡊࡥࡏࡓࡉࡄࡒࡎࡠࡁࡕࡋࡒࡒࡤ࡛ࡒࡍࠤ᭛")),
            bstackl_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ᭜"): env.get(bstackl_opy_ (u"࡙ࠧࡅࡎࡃࡓࡌࡔࡘࡅࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥ᭝")),
            bstackl_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ᭞"): env.get(bstackl_opy_ (u"ࠢࡔࡇࡐࡅࡕࡎࡏࡓࡇࡢࡎࡔࡈ࡟ࡊࡆࠥ᭟"))
        }
    if env.get(bstackl_opy_ (u"ࠣࡅࡌࠦ᭠")) == bstackl_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ᭡") and bstack11l1111ll_opy_(env.get(bstackl_opy_ (u"ࠥࡋࡎ࡚ࡌࡂࡄࡢࡇࡎࠨ᭢"))):
        return {
            bstackl_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᭣"): bstackl_opy_ (u"ࠧࡍࡩࡵࡎࡤࡦࠧ᭤"),
            bstackl_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ᭥"): env.get(bstackl_opy_ (u"ࠢࡄࡋࡢࡎࡔࡈ࡟ࡖࡔࡏࠦ᭦")),
            bstackl_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ᭧"): env.get(bstackl_opy_ (u"ࠤࡆࡍࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢ᭨")),
            bstackl_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ᭩"): env.get(bstackl_opy_ (u"ࠦࡈࡏ࡟ࡋࡑࡅࡣࡎࡊࠢ᭪"))
        }
    if env.get(bstackl_opy_ (u"ࠧࡉࡉࠣ᭫")) == bstackl_opy_ (u"ࠨࡴࡳࡷࡨ᭬ࠦ") and bstack11l1111ll_opy_(env.get(bstackl_opy_ (u"ࠢࡃࡗࡌࡐࡉࡑࡉࡕࡇࠥ᭭"))):
        return {
            bstackl_opy_ (u"ࠣࡰࡤࡱࡪࠨ᭮"): bstackl_opy_ (u"ࠤࡅࡹ࡮ࡲࡤ࡬࡫ࡷࡩࠧ᭯"),
            bstackl_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ᭰"): env.get(bstackl_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡎࡍ࡙ࡋ࡟ࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥ᭱")),
            bstackl_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ᭲"): env.get(bstackl_opy_ (u"ࠨࡂࡖࡋࡏࡈࡐࡏࡔࡆࡡࡏࡅࡇࡋࡌࠣ᭳")) or env.get(bstackl_opy_ (u"ࠢࡃࡗࡌࡐࡉࡑࡉࡕࡇࡢࡔࡎࡖࡅࡍࡋࡑࡉࡤࡔࡁࡎࡇࠥ᭴")),
            bstackl_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ᭵"): env.get(bstackl_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦ᭶"))
        }
    if bstack11l1111ll_opy_(env.get(bstackl_opy_ (u"ࠥࡘࡋࡥࡂࡖࡋࡏࡈࠧ᭷"))):
        return {
            bstackl_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᭸"): bstackl_opy_ (u"ࠧ࡜ࡩࡴࡷࡤࡰ࡙ࠥࡴࡶࡦ࡬ࡳ࡚ࠥࡥࡢ࡯ࠣࡗࡪࡸࡶࡪࡥࡨࡷࠧ᭹"),
            bstackl_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ᭺"): bstackl_opy_ (u"ࠢࡼࡿࡾࢁࠧ᭻").format(env.get(bstackl_opy_ (u"ࠨࡕ࡜ࡗ࡙ࡋࡍࡠࡖࡈࡅࡒࡌࡏࡖࡐࡇࡅ࡙ࡏࡏࡏࡕࡈࡖ࡛ࡋࡒࡖࡔࡌࠫ᭼")), env.get(bstackl_opy_ (u"ࠩࡖ࡝ࡘ࡚ࡅࡎࡡࡗࡉࡆࡓࡐࡓࡑࡍࡉࡈ࡚ࡉࡅࠩ᭽"))),
            bstackl_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ᭾"): env.get(bstackl_opy_ (u"ࠦࡘ࡟ࡓࡕࡇࡐࡣࡉࡋࡆࡊࡐࡌࡘࡎࡕࡎࡊࡆࠥ᭿")),
            bstackl_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᮀ"): env.get(bstackl_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡍࡉࠨᮁ"))
        }
    if bstack11l1111ll_opy_(env.get(bstackl_opy_ (u"ࠢࡂࡒࡓ࡚ࡊ࡟ࡏࡓࠤᮂ"))):
        return {
            bstackl_opy_ (u"ࠣࡰࡤࡱࡪࠨᮃ"): bstackl_opy_ (u"ࠤࡄࡴࡵࡼࡥࡺࡱࡵࠦᮄ"),
            bstackl_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᮅ"): bstackl_opy_ (u"ࠦࢀࢃ࠯ࡱࡴࡲ࡮ࡪࡩࡴ࠰ࡽࢀ࠳ࢀࢃ࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࡼࡿࠥᮆ").format(env.get(bstackl_opy_ (u"ࠬࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡖࡔࡏࠫᮇ")), env.get(bstackl_opy_ (u"࠭ࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡃࡆࡇࡔ࡛ࡎࡕࡡࡑࡅࡒࡋࠧᮈ")), env.get(bstackl_opy_ (u"ࠧࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡓࡖࡔࡐࡅࡄࡖࡢࡗࡑ࡛ࡇࠨᮉ")), env.get(bstackl_opy_ (u"ࠨࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠬᮊ"))),
            bstackl_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᮋ"): env.get(bstackl_opy_ (u"ࠥࡅࡕࡖࡖࡆ࡛ࡒࡖࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢᮌ")),
            bstackl_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᮍ"): env.get(bstackl_opy_ (u"ࠧࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨᮎ"))
        }
    if env.get(bstackl_opy_ (u"ࠨࡁ࡛ࡗࡕࡉࡤࡎࡔࡕࡒࡢ࡙ࡘࡋࡒࡠࡃࡊࡉࡓ࡚ࠢᮏ")) and env.get(bstackl_opy_ (u"ࠢࡕࡈࡢࡆ࡚ࡏࡌࡅࠤᮐ")):
        return {
            bstackl_opy_ (u"ࠣࡰࡤࡱࡪࠨᮑ"): bstackl_opy_ (u"ࠤࡄࡾࡺࡸࡥࠡࡅࡌࠦᮒ"),
            bstackl_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᮓ"): bstackl_opy_ (u"ࠦࢀࢃࡻࡾ࠱ࡢࡦࡺ࡯࡬ࡥ࠱ࡵࡩࡸࡻ࡬ࡵࡵࡂࡦࡺ࡯࡬ࡥࡋࡧࡁࢀࢃࠢᮔ").format(env.get(bstackl_opy_ (u"࡙࡙ࠬࡔࡖࡈࡑࡤ࡚ࡅࡂࡏࡉࡓ࡚ࡔࡄࡂࡖࡌࡓࡓ࡙ࡅࡓࡘࡈࡖ࡚ࡘࡉࠨᮕ")), env.get(bstackl_opy_ (u"࠭ࡓ࡚ࡕࡗࡉࡒࡥࡔࡆࡃࡐࡔࡗࡕࡊࡆࡅࡗࠫᮖ")), env.get(bstackl_opy_ (u"ࠧࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡎࡊࠧᮗ"))),
            bstackl_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᮘ"): env.get(bstackl_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊࡉࡅࠤᮙ")),
            bstackl_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᮚ"): env.get(bstackl_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡋࡇࠦᮛ"))
        }
    if any([env.get(bstackl_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠥᮜ")), env.get(bstackl_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡕࡉࡘࡕࡌࡗࡇࡇࡣࡘࡕࡕࡓࡅࡈࡣ࡛ࡋࡒࡔࡋࡒࡒࠧᮝ")), env.get(bstackl_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡗࡔ࡛ࡒࡄࡇࡢ࡚ࡊࡘࡓࡊࡑࡑࠦᮞ"))]):
        return {
            bstackl_opy_ (u"ࠣࡰࡤࡱࡪࠨᮟ"): bstackl_opy_ (u"ࠤࡄ࡛ࡘࠦࡃࡰࡦࡨࡆࡺ࡯࡬ࡥࠤᮠ"),
            bstackl_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᮡ"): env.get(bstackl_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡑࡗࡅࡐࡎࡉ࡟ࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥᮢ")),
            bstackl_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᮣ"): env.get(bstackl_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦᮤ")),
            bstackl_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᮥ"): env.get(bstackl_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࠨᮦ"))
        }
    if env.get(bstackl_opy_ (u"ࠤࡥࡥࡲࡨ࡯ࡰࡡࡥࡹ࡮ࡲࡤࡏࡷࡰࡦࡪࡸࠢᮧ")):
        return {
            bstackl_opy_ (u"ࠥࡲࡦࡳࡥࠣᮨ"): bstackl_opy_ (u"ࠦࡇࡧ࡭ࡣࡱࡲࠦᮩ"),
            bstackl_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬᮪ࠣ"): env.get(bstackl_opy_ (u"ࠨࡢࡢ࡯ࡥࡳࡴࡥࡢࡶ࡫࡯ࡨࡗ࡫ࡳࡶ࡮ࡷࡷ࡚ࡸ࡬᮫ࠣ")),
            bstackl_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᮬ"): env.get(bstackl_opy_ (u"ࠣࡤࡤࡱࡧࡵ࡯ࡠࡵ࡫ࡳࡷࡺࡊࡰࡤࡑࡥࡲ࡫ࠢᮭ")),
            bstackl_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᮮ"): env.get(bstackl_opy_ (u"ࠥࡦࡦࡳࡢࡰࡱࡢࡦࡺ࡯࡬ࡥࡐࡸࡱࡧ࡫ࡲࠣᮯ"))
        }
    if env.get(bstackl_opy_ (u"ࠦ࡜ࡋࡒࡄࡍࡈࡖࠧ᮰")) or env.get(bstackl_opy_ (u"ࠧ࡝ࡅࡓࡅࡎࡉࡗࡥࡍࡂࡋࡑࡣࡕࡏࡐࡆࡎࡌࡒࡊࡥࡓࡕࡃࡕࡘࡊࡊࠢ᮱")):
        return {
            bstackl_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ᮲"): bstackl_opy_ (u"ࠢࡘࡧࡵࡧࡰ࡫ࡲࠣ᮳"),
            bstackl_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ᮴"): env.get(bstackl_opy_ (u"ࠤ࡚ࡉࡗࡉࡋࡆࡔࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨ᮵")),
            bstackl_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ᮶"): bstackl_opy_ (u"ࠦࡒࡧࡩ࡯ࠢࡓ࡭ࡵ࡫࡬ࡪࡰࡨࠦ᮷") if env.get(bstackl_opy_ (u"ࠧ࡝ࡅࡓࡅࡎࡉࡗࡥࡍࡂࡋࡑࡣࡕࡏࡐࡆࡎࡌࡒࡊࡥࡓࡕࡃࡕࡘࡊࡊࠢ᮸")) else None,
            bstackl_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ᮹"): env.get(bstackl_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࡠࡉࡌࡘࡤࡉࡏࡎࡏࡌࡘࠧᮺ"))
        }
    if any([env.get(bstackl_opy_ (u"ࠣࡉࡆࡔࡤࡖࡒࡐࡌࡈࡇ࡙ࠨᮻ")), env.get(bstackl_opy_ (u"ࠤࡊࡇࡑࡕࡕࡅࡡࡓࡖࡔࡐࡅࡄࡖࠥᮼ")), env.get(bstackl_opy_ (u"ࠥࡋࡔࡕࡇࡍࡇࡢࡇࡑࡕࡕࡅࡡࡓࡖࡔࡐࡅࡄࡖࠥᮽ"))]):
        return {
            bstackl_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᮾ"): bstackl_opy_ (u"ࠧࡍ࡯ࡰࡩ࡯ࡩࠥࡉ࡬ࡰࡷࡧࠦᮿ"),
            bstackl_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᯀ"): None,
            bstackl_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᯁ"): env.get(bstackl_opy_ (u"ࠣࡒࡕࡓࡏࡋࡃࡕࡡࡌࡈࠧᯂ")),
            bstackl_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᯃ"): env.get(bstackl_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡌࡈࠧᯄ"))
        }
    if env.get(bstackl_opy_ (u"ࠦࡘࡎࡉࡑࡒࡄࡆࡑࡋࠢᯅ")):
        return {
            bstackl_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᯆ"): bstackl_opy_ (u"ࠨࡓࡩ࡫ࡳࡴࡦࡨ࡬ࡦࠤᯇ"),
            bstackl_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᯈ"): env.get(bstackl_opy_ (u"ࠣࡕࡋࡍࡕࡖࡁࡃࡎࡈࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢᯉ")),
            bstackl_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᯊ"): bstackl_opy_ (u"ࠥࡎࡴࡨࠠࠤࡽࢀࠦᯋ").format(env.get(bstackl_opy_ (u"ࠫࡘࡎࡉࡑࡒࡄࡆࡑࡋ࡟ࡋࡑࡅࡣࡎࡊࠧᯌ"))) if env.get(bstackl_opy_ (u"࡙ࠧࡈࡊࡒࡓࡅࡇࡒࡅࡠࡌࡒࡆࡤࡏࡄࠣᯍ")) else None,
            bstackl_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᯎ"): env.get(bstackl_opy_ (u"ࠢࡔࡊࡌࡔࡕࡇࡂࡍࡇࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤᯏ"))
        }
    if bstack11l1111ll_opy_(env.get(bstackl_opy_ (u"ࠣࡐࡈࡘࡑࡏࡆ࡚ࠤᯐ"))):
        return {
            bstackl_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᯑ"): bstackl_opy_ (u"ࠥࡒࡪࡺ࡬ࡪࡨࡼࠦᯒ"),
            bstackl_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᯓ"): env.get(bstackl_opy_ (u"ࠧࡊࡅࡑࡎࡒ࡝ࡤ࡛ࡒࡍࠤᯔ")),
            bstackl_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᯕ"): env.get(bstackl_opy_ (u"ࠢࡔࡋࡗࡉࡤࡔࡁࡎࡇࠥᯖ")),
            bstackl_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᯗ"): env.get(bstackl_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡋࡇࠦᯘ"))
        }
    if bstack11l1111ll_opy_(env.get(bstackl_opy_ (u"ࠥࡋࡎ࡚ࡈࡖࡄࡢࡅࡈ࡚ࡉࡐࡐࡖࠦᯙ"))):
        return {
            bstackl_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᯚ"): bstackl_opy_ (u"ࠧࡍࡩࡵࡊࡸࡦࠥࡇࡣࡵ࡫ࡲࡲࡸࠨᯛ"),
            bstackl_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᯜ"): bstackl_opy_ (u"ࠢࡼࡿ࠲ࡿࢂ࠵ࡡࡤࡶ࡬ࡳࡳࡹ࠯ࡳࡷࡱࡷ࠴ࢁࡽࠣᯝ").format(env.get(bstackl_opy_ (u"ࠨࡉࡌࡘࡍ࡛ࡂࡠࡕࡈࡖ࡛ࡋࡒࡠࡗࡕࡐࠬᯞ")), env.get(bstackl_opy_ (u"ࠩࡊࡍ࡙ࡎࡕࡃࡡࡕࡉࡕࡕࡓࡊࡖࡒࡖ࡞࠭ᯟ")), env.get(bstackl_opy_ (u"ࠪࡋࡎ࡚ࡈࡖࡄࡢࡖ࡚ࡔ࡟ࡊࡆࠪᯠ"))),
            bstackl_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᯡ"): env.get(bstackl_opy_ (u"ࠧࡍࡉࡕࡊࡘࡆࡤ࡝ࡏࡓࡍࡉࡐࡔ࡝ࠢᯢ")),
            bstackl_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᯣ"): env.get(bstackl_opy_ (u"ࠢࡈࡋࡗࡌ࡚ࡈ࡟ࡓࡗࡑࡣࡎࡊࠢᯤ"))
        }
    if env.get(bstackl_opy_ (u"ࠣࡅࡌࠦᯥ")) == bstackl_opy_ (u"ࠤࡷࡶࡺ࡫᯦ࠢ") and env.get(bstackl_opy_ (u"࡚ࠥࡊࡘࡃࡆࡎࠥᯧ")) == bstackl_opy_ (u"ࠦ࠶ࠨᯨ"):
        return {
            bstackl_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᯩ"): bstackl_opy_ (u"ࠨࡖࡦࡴࡦࡩࡱࠨᯪ"),
            bstackl_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᯫ"): bstackl_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࡽࢀࠦᯬ").format(env.get(bstackl_opy_ (u"࡙ࠩࡉࡗࡉࡅࡍࡡࡘࡖࡑ࠭ᯭ"))),
            bstackl_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᯮ"): None,
            bstackl_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᯯ"): None,
        }
    if env.get(bstackl_opy_ (u"࡚ࠧࡅࡂࡏࡆࡍ࡙࡟࡟ࡗࡇࡕࡗࡎࡕࡎࠣᯰ")):
        return {
            bstackl_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᯱ"): bstackl_opy_ (u"ࠢࡕࡧࡤࡱࡨ࡯ࡴࡺࠤ᯲"),
            bstackl_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯᯳ࠦ"): None,
            bstackl_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ᯴"): env.get(bstackl_opy_ (u"ࠥࡘࡊࡇࡍࡄࡋࡗ࡝ࡤࡖࡒࡐࡌࡈࡇ࡙ࡥࡎࡂࡏࡈࠦ᯵")),
            bstackl_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ᯶"): env.get(bstackl_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦ᯷"))
        }
    if any([env.get(bstackl_opy_ (u"ࠨࡃࡐࡐࡆࡓ࡚ࡘࡓࡆࠤ᯸")), env.get(bstackl_opy_ (u"ࠢࡄࡑࡑࡇࡔ࡛ࡒࡔࡇࡢ࡙ࡗࡒࠢ᯹")), env.get(bstackl_opy_ (u"ࠣࡅࡒࡒࡈࡕࡕࡓࡕࡈࡣ࡚࡙ࡅࡓࡐࡄࡑࡊࠨ᯺")), env.get(bstackl_opy_ (u"ࠤࡆࡓࡓࡉࡏࡖࡔࡖࡉࡤ࡚ࡅࡂࡏࠥ᯻"))]):
        return {
            bstackl_opy_ (u"ࠥࡲࡦࡳࡥࠣ᯼"): bstackl_opy_ (u"ࠦࡈࡵ࡮ࡤࡱࡸࡶࡸ࡫ࠢ᯽"),
            bstackl_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ᯾"): None,
            bstackl_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ᯿"): env.get(bstackl_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣᰀ")) or None,
            bstackl_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᰁ"): env.get(bstackl_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡋࡇࠦᰂ"), 0)
        }
    if env.get(bstackl_opy_ (u"ࠥࡋࡔࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣᰃ")):
        return {
            bstackl_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᰄ"): bstackl_opy_ (u"ࠧࡍ࡯ࡄࡆࠥᰅ"),
            bstackl_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᰆ"): None,
            bstackl_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᰇ"): env.get(bstackl_opy_ (u"ࠣࡉࡒࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨᰈ")),
            bstackl_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᰉ"): env.get(bstackl_opy_ (u"ࠥࡋࡔࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡅࡒ࡙ࡓ࡚ࡅࡓࠤᰊ"))
        }
    if env.get(bstackl_opy_ (u"ࠦࡈࡌ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠤᰋ")):
        return {
            bstackl_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᰌ"): bstackl_opy_ (u"ࠨࡃࡰࡦࡨࡊࡷ࡫ࡳࡩࠤᰍ"),
            bstackl_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᰎ"): env.get(bstackl_opy_ (u"ࠣࡅࡉࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢᰏ")),
            bstackl_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᰐ"): env.get(bstackl_opy_ (u"ࠥࡇࡋࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡐࡄࡑࡊࠨᰑ")),
            bstackl_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᰒ"): env.get(bstackl_opy_ (u"ࠧࡉࡆࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠥᰓ"))
        }
    return {bstackl_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᰔ"): None}
def get_host_info():
    return {
        bstackl_opy_ (u"ࠢࡩࡱࡶࡸࡳࡧ࡭ࡦࠤᰕ"): platform.node(),
        bstackl_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠥᰖ"): platform.system(),
        bstackl_opy_ (u"ࠤࡷࡽࡵ࡫ࠢᰗ"): platform.machine(),
        bstackl_opy_ (u"ࠥࡺࡪࡸࡳࡪࡱࡱࠦᰘ"): platform.version(),
        bstackl_opy_ (u"ࠦࡦࡸࡣࡩࠤᰙ"): platform.architecture()[0]
    }
def bstack1lllllll1l_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack111lll11lll_opy_():
    if bstack1l1llll1l1_opy_.get_property(bstackl_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭ᰚ")):
        return bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬᰛ")
    return bstackl_opy_ (u"ࠧࡶࡰ࡮ࡲࡴࡽ࡮ࡠࡩࡵ࡭ࡩ࠭ᰜ")
def bstack11l11lll11l_opy_(driver):
    info = {
        bstackl_opy_ (u"ࠨࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᰝ"): driver.capabilities,
        bstackl_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩ࠭ᰞ"): driver.session_id,
        bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫᰟ"): driver.capabilities.get(bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩᰠ"), None),
        bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᰡ"): driver.capabilities.get(bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᰢ"), None),
        bstackl_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩᰣ"): driver.capabilities.get(bstackl_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠧᰤ"), None),
        bstackl_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᰥ"):driver.capabilities.get(bstackl_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬᰦ"), None),
    }
    if bstack111lll11lll_opy_() == bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪᰧ"):
        if bstack1llllll111_opy_():
            info[bstackl_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹ࠭ᰨ")] = bstackl_opy_ (u"࠭ࡡࡱࡲ࠰ࡥࡺࡺ࡯࡮ࡣࡷࡩࠬᰩ")
        elif driver.capabilities.get(bstackl_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᰪ"), {}).get(bstackl_opy_ (u"ࠨࡶࡸࡶࡧࡵࡳࡤࡣ࡯ࡩࠬᰫ"), False):
            info[bstackl_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࠪᰬ")] = bstackl_opy_ (u"ࠪࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫ࠧᰭ")
        else:
            info[bstackl_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࠬᰮ")] = bstackl_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧᰯ")
    return info
def bstack1llllll111_opy_():
    if bstack1l1llll1l1_opy_.get_property(bstackl_opy_ (u"࠭ࡡࡱࡲࡢࡥࡺࡺ࡯࡮ࡣࡷࡩࠬᰰ")):
        return True
    if bstack11l1111ll_opy_(os.environ.get(bstackl_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨᰱ"), None)):
        return True
    return False
def bstack11llll1l1l_opy_(bstack11l111l11ll_opy_, url, data, config):
    headers = config.get(bstackl_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩᰲ"), None)
    proxies = bstack111l11ll1_opy_(config, url)
    auth = config.get(bstackl_opy_ (u"ࠩࡤࡹࡹ࡮ࠧᰳ"), None)
    response = requests.request(
            bstack11l111l11ll_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack111l1llll_opy_(bstack1lllll111_opy_, size):
    bstack111lll1l_opy_ = []
    while len(bstack1lllll111_opy_) > size:
        bstack11l1l111l1_opy_ = bstack1lllll111_opy_[:size]
        bstack111lll1l_opy_.append(bstack11l1l111l1_opy_)
        bstack1lllll111_opy_ = bstack1lllll111_opy_[size:]
    bstack111lll1l_opy_.append(bstack1lllll111_opy_)
    return bstack111lll1l_opy_
def bstack111lllllll1_opy_(message, bstack111lll1l1ll_opy_=False):
    os.write(1, bytes(message, bstackl_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩᰴ")))
    os.write(1, bytes(bstackl_opy_ (u"ࠫࡡࡴࠧᰵ"), bstackl_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫᰶ")))
    if bstack111lll1l1ll_opy_:
        with open(bstackl_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࠳࡯࠲࠳ࡼ࠱᰷ࠬ") + os.environ[bstackl_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉ࠭᰸")] + bstackl_opy_ (u"ࠨ࠰࡯ࡳ࡬࠭᰹"), bstackl_opy_ (u"ࠩࡤࠫ᰺")) as f:
            f.write(message + bstackl_opy_ (u"ࠪࡠࡳ࠭᰻"))
def bstack1l1ll11l11l_opy_():
    return os.environ[bstackl_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧ᰼")].lower() == bstackl_opy_ (u"ࠬࡺࡲࡶࡧࠪ᰽")
def bstack1lll111111_opy_():
    return bstack111l1111ll_opy_().replace(tzinfo=None).isoformat() + bstackl_opy_ (u"࡚࠭ࠨ᰾")
def bstack11l1111ll1l_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstackl_opy_ (u"࡛ࠧࠩ᰿"))) - datetime.datetime.fromisoformat(start.rstrip(bstackl_opy_ (u"ࠨ࡜ࠪ᱀")))).total_seconds() * 1000
def bstack11l11l111ll_opy_(timestamp):
    return bstack11l111llll1_opy_(timestamp).isoformat() + bstackl_opy_ (u"ࠩ࡝ࠫ᱁")
def bstack11l111111ll_opy_(bstack11l111l11l1_opy_):
    date_format = bstackl_opy_ (u"ࠪࠩ࡞ࠫ࡭ࠦࡦࠣࠩࡍࡀࠥࡎ࠼ࠨࡗ࠳ࠫࡦࠨ᱂")
    bstack11l111lllll_opy_ = datetime.datetime.strptime(bstack11l111l11l1_opy_, date_format)
    return bstack11l111lllll_opy_.isoformat() + bstackl_opy_ (u"ࠫ࡟࠭᱃")
def bstack11l11ll1111_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstackl_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ᱄")
    else:
        return bstackl_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭᱅")
def bstack11l1111ll_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstackl_opy_ (u"ࠧࡵࡴࡸࡩࠬ᱆")
def bstack11l11111l1l_opy_(val):
    return val.__str__().lower() == bstackl_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧ᱇")
def bstack111l1lll11_opy_(bstack11l1111l11l_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack11l1111l11l_opy_ as e:
                print(bstackl_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡨࡸࡲࡨࡺࡩࡰࡰࠣࡿࢂࠦ࠭࠿ࠢࡾࢁ࠿ࠦࡻࡾࠤ᱈").format(func.__name__, bstack11l1111l11l_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack11l11ll1l1l_opy_(bstack11l11l1ll11_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack11l11l1ll11_opy_(cls, *args, **kwargs)
            except bstack11l1111l11l_opy_ as e:
                print(bstackl_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡩࡹࡳࡩࡴࡪࡱࡱࠤࢀࢃࠠ࠮ࡀࠣࡿࢂࡀࠠࡼࡿࠥ᱉").format(bstack11l11l1ll11_opy_.__name__, bstack11l1111l11l_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack11l11ll1l1l_opy_
    else:
        return decorator
def bstack1l11l11ll_opy_(bstack1111l1111l_opy_):
    if os.getenv(bstackl_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧ᱊")) is not None:
        return bstack11l1111ll_opy_(os.getenv(bstackl_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨ᱋")))
    if bstackl_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪ᱌") in bstack1111l1111l_opy_ and bstack11l11111l1l_opy_(bstack1111l1111l_opy_[bstackl_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫᱍ")]):
        return False
    if bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᱎ") in bstack1111l1111l_opy_ and bstack11l11111l1l_opy_(bstack1111l1111l_opy_[bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫᱏ")]):
        return False
    return True
def bstack1llll111ll_opy_():
    try:
        from pytest_bdd import reporting
        bstack11l1l11111l_opy_ = os.environ.get(bstackl_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡘࡗࡊࡘ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠥ᱐"), None)
        return bstack11l1l11111l_opy_ is None or bstack11l1l11111l_opy_ == bstackl_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠣ᱑")
    except Exception as e:
        return False
def bstack1111l1111_opy_(hub_url, CONFIG):
    if bstack111l11lll_opy_() <= version.parse(bstackl_opy_ (u"ࠬ࠹࠮࠲࠵࠱࠴ࠬ᱒")):
        if hub_url:
            return bstackl_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢ᱓") + hub_url + bstackl_opy_ (u"ࠢ࠻࠺࠳࠳ࡼࡪ࠯ࡩࡷࡥࠦ᱔")
        return bstack1lllll1ll_opy_
    if hub_url:
        return bstackl_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࠥ᱕") + hub_url + bstackl_opy_ (u"ࠤ࠲ࡻࡩ࠵ࡨࡶࡤࠥ᱖")
    return bstack1l111l1ll_opy_
def bstack11l11l1llll_opy_():
    return isinstance(os.getenv(bstackl_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓ࡝࡙ࡋࡓࡕࡡࡓࡐ࡚ࡍࡉࡏࠩ᱗")), str)
def bstack1l1ll1ll1l_opy_(url):
    return urlparse(url).hostname
def bstack1l11ll1l1l_opy_(hostname):
    for bstack1lll1llll_opy_ in bstack1l111l1l1_opy_:
        regex = re.compile(bstack1lll1llll_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack11l1l111l11_opy_(bstack11l1111111l_opy_, file_name, logger):
    bstack1l1l1l1lll_opy_ = os.path.join(os.path.expanduser(bstackl_opy_ (u"ࠫࢃ࠭᱘")), bstack11l1111111l_opy_)
    try:
        if not os.path.exists(bstack1l1l1l1lll_opy_):
            os.makedirs(bstack1l1l1l1lll_opy_)
        file_path = os.path.join(os.path.expanduser(bstackl_opy_ (u"ࠬࢄࠧ᱙")), bstack11l1111111l_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstackl_opy_ (u"࠭ࡷࠨᱚ")):
                pass
            with open(file_path, bstackl_opy_ (u"ࠢࡸ࠭ࠥᱛ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack1l111llll_opy_.format(str(e)))
def bstack11l1111l1ll_opy_(file_name, key, value, logger):
    file_path = bstack11l1l111l11_opy_(bstackl_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨᱜ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1lllll1l1_opy_ = json.load(open(file_path, bstackl_opy_ (u"ࠩࡵࡦࠬᱝ")))
        else:
            bstack1lllll1l1_opy_ = {}
        bstack1lllll1l1_opy_[key] = value
        with open(file_path, bstackl_opy_ (u"ࠥࡻ࠰ࠨᱞ")) as outfile:
            json.dump(bstack1lllll1l1_opy_, outfile)
def bstack11111l1l_opy_(file_name, logger):
    file_path = bstack11l1l111l11_opy_(bstackl_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫᱟ"), file_name, logger)
    bstack1lllll1l1_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstackl_opy_ (u"ࠬࡸࠧᱠ")) as bstack11l11111l1_opy_:
            bstack1lllll1l1_opy_ = json.load(bstack11l11111l1_opy_)
    return bstack1lllll1l1_opy_
def bstack11l111l11l_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstackl_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡦࡨࡰࡪࡺࡩ࡯ࡩࠣࡪ࡮ࡲࡥ࠻ࠢࠪᱡ") + file_path + bstackl_opy_ (u"ࠧࠡࠩᱢ") + str(e))
def bstack111l11lll_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstackl_opy_ (u"ࠣ࠾ࡑࡓ࡙࡙ࡅࡕࡀࠥᱣ")
def bstack1l1lllll_opy_(config):
    if bstackl_opy_ (u"ࠩ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨᱤ") in config:
        del (config[bstackl_opy_ (u"ࠪ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩᱥ")])
        return False
    if bstack111l11lll_opy_() < version.parse(bstackl_opy_ (u"ࠫ࠸࠴࠴࠯࠲ࠪᱦ")):
        return False
    if bstack111l11lll_opy_() >= version.parse(bstackl_opy_ (u"ࠬ࠺࠮࠲࠰࠸ࠫᱧ")):
        return True
    if bstackl_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ᱨ") in config and config[bstackl_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧᱩ")] is False:
        return False
    else:
        return True
def bstack1ll1ll11l_opy_(args_list, bstack11l11llll11_opy_):
    index = -1
    for value in bstack11l11llll11_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
def bstack11ll1ll1l11_opy_(a, b):
  for k, v in b.items():
    if isinstance(v, dict) and k in a and isinstance(a[k], dict):
        bstack11ll1ll1l11_opy_(a[k], v)
    else:
        a[k] = v
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack111ll1l1ll_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack111ll1l1ll_opy_ = bstack111ll1l1ll_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstackl_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨᱪ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstackl_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᱫ"), exception=exception)
    def bstack111111ll11_opy_(self):
        if self.result != bstackl_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᱬ"):
            return None
        if isinstance(self.exception_type, str) and bstackl_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࠢᱭ") in self.exception_type:
            return bstackl_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࡆࡴࡵࡳࡷࠨᱮ")
        return bstackl_opy_ (u"ࠨࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠢᱯ")
    def bstack111llllllll_opy_(self):
        if self.result != bstackl_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᱰ"):
            return None
        if self.bstack111ll1l1ll_opy_:
            return self.bstack111ll1l1ll_opy_
        return bstack111lllll111_opy_(self.exception)
def bstack111lllll111_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack11l11ll1ll1_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack11ll1111ll_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack1111ll1l_opy_(config, logger):
    try:
        import playwright
        bstack11l111l1111_opy_ = playwright.__file__
        bstack111llllll11_opy_ = os.path.split(bstack11l111l1111_opy_)
        bstack11l1111ll11_opy_ = bstack111llllll11_opy_[0] + bstackl_opy_ (u"ࠨ࠱ࡧࡶ࡮ࡼࡥࡳ࠱ࡳࡥࡨࡱࡡࡨࡧ࠲ࡰ࡮ࡨ࠯ࡤ࡮࡬࠳ࡨࡲࡩ࠯࡬ࡶࠫᱱ")
        os.environ[bstackl_opy_ (u"ࠩࡊࡐࡔࡈࡁࡍࡡࡄࡋࡊࡔࡔࡠࡊࡗࡘࡕࡥࡐࡓࡑ࡛࡝ࠬᱲ")] = bstack1l1ll1l1ll_opy_(config)
        with open(bstack11l1111ll11_opy_, bstackl_opy_ (u"ࠪࡶࠬᱳ")) as f:
            bstack1lllll11ll_opy_ = f.read()
            bstack11l11ll1l11_opy_ = bstackl_opy_ (u"ࠫ࡬ࡲ࡯ࡣࡣ࡯࠱ࡦ࡭ࡥ࡯ࡶࠪᱴ")
            bstack111llll111l_opy_ = bstack1lllll11ll_opy_.find(bstack11l11ll1l11_opy_)
            if bstack111llll111l_opy_ == -1:
              process = subprocess.Popen(bstackl_opy_ (u"ࠧࡴࡰ࡮ࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣ࡫ࡱࡵࡢࡢ࡮࠰ࡥ࡬࡫࡮ࡵࠤᱵ"), shell=True, cwd=bstack111llllll11_opy_[0])
              process.wait()
              bstack111lll1l1l1_opy_ = bstackl_opy_ (u"࠭ࠢࡶࡵࡨࠤࡸࡺࡲࡪࡥࡷࠦࡀ࠭ᱶ")
              bstack111lll1lll1_opy_ = bstackl_opy_ (u"ࠢࠣࠤࠣࡠࠧࡻࡳࡦࠢࡶࡸࡷ࡯ࡣࡵ࡞ࠥ࠿ࠥࡩ࡯࡯ࡵࡷࠤࢀࠦࡢࡰࡱࡷࡷࡹࡸࡡࡱࠢࢀࠤࡂࠦࡲࡦࡳࡸ࡭ࡷ࡫ࠨࠨࡩ࡯ࡳࡧࡧ࡬࠮ࡣࡪࡩࡳࡺࠧࠪ࠽ࠣ࡭࡫ࠦࠨࡱࡴࡲࡧࡪࡹࡳ࠯ࡧࡱࡺ࠳ࡍࡌࡐࡄࡄࡐࡤࡇࡇࡆࡐࡗࡣࡍ࡚ࡔࡑࡡࡓࡖࡔ࡞࡙ࠪࠢࡥࡳࡴࡺࡳࡵࡴࡤࡴ࠭࠯࠻ࠡࠤࠥࠦᱷ")
              bstack111lll11ll1_opy_ = bstack1lllll11ll_opy_.replace(bstack111lll1l1l1_opy_, bstack111lll1lll1_opy_)
              with open(bstack11l1111ll11_opy_, bstackl_opy_ (u"ࠨࡹࠪᱸ")) as f:
                f.write(bstack111lll11ll1_opy_)
    except Exception as e:
        logger.error(bstack1l111ll1l_opy_.format(str(e)))
def bstack1111l1ll1_opy_():
  try:
    bstack11l11l11ll1_opy_ = os.path.join(tempfile.gettempdir(), bstackl_opy_ (u"ࠩࡲࡴࡹ࡯࡭ࡢ࡮ࡢ࡬ࡺࡨ࡟ࡶࡴ࡯࠲࡯ࡹ࡯࡯ࠩᱹ"))
    bstack11l1111lll1_opy_ = []
    if os.path.exists(bstack11l11l11ll1_opy_):
      with open(bstack11l11l11ll1_opy_) as f:
        bstack11l1111lll1_opy_ = json.load(f)
      os.remove(bstack11l11l11ll1_opy_)
    return bstack11l1111lll1_opy_
  except:
    pass
  return []
def bstack1ll111ll1_opy_(bstack1l11l111_opy_):
  try:
    bstack11l1111lll1_opy_ = []
    bstack11l11l11ll1_opy_ = os.path.join(tempfile.gettempdir(), bstackl_opy_ (u"ࠪࡳࡵࡺࡩ࡮ࡣ࡯ࡣ࡭ࡻࡢࡠࡷࡵࡰ࠳ࡰࡳࡰࡰࠪᱺ"))
    if os.path.exists(bstack11l11l11ll1_opy_):
      with open(bstack11l11l11ll1_opy_) as f:
        bstack11l1111lll1_opy_ = json.load(f)
    bstack11l1111lll1_opy_.append(bstack1l11l111_opy_)
    with open(bstack11l11l11ll1_opy_, bstackl_opy_ (u"ࠫࡼ࠭ᱻ")) as f:
        json.dump(bstack11l1111lll1_opy_, f)
  except:
    pass
def bstack1lll111l11_opy_(logger, bstack11l11l11lll_opy_ = False):
  try:
    test_name = os.environ.get(bstackl_opy_ (u"ࠬࡖ࡙ࡕࡇࡖࡘࡤ࡚ࡅࡔࡖࡢࡒࡆࡓࡅࠨᱼ"), bstackl_opy_ (u"࠭ࠧᱽ"))
    if test_name == bstackl_opy_ (u"ࠧࠨ᱾"):
        test_name = threading.current_thread().__dict__.get(bstackl_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡃࡦࡧࡣࡹ࡫ࡳࡵࡡࡱࡥࡲ࡫ࠧ᱿"), bstackl_opy_ (u"ࠩࠪᲀ"))
    bstack111llllll1l_opy_ = bstackl_opy_ (u"ࠪ࠰ࠥ࠭ᲁ").join(threading.current_thread().bstackTestErrorMessages)
    if bstack11l11l11lll_opy_:
        bstack1ll11l11l_opy_ = os.environ.get(bstackl_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫᲂ"), bstackl_opy_ (u"ࠬ࠶ࠧᲃ"))
        bstack1l111ll11l_opy_ = {bstackl_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᲄ"): test_name, bstackl_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ᲅ"): bstack111llllll1l_opy_, bstackl_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧᲆ"): bstack1ll11l11l_opy_}
        bstack11l11l1lll1_opy_ = []
        bstack11l11l1l1ll_opy_ = os.path.join(tempfile.gettempdir(), bstackl_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡳࡴࡵࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶ࠱࡮ࡸࡵ࡮ࠨᲇ"))
        if os.path.exists(bstack11l11l1l1ll_opy_):
            with open(bstack11l11l1l1ll_opy_) as f:
                bstack11l11l1lll1_opy_ = json.load(f)
        bstack11l11l1lll1_opy_.append(bstack1l111ll11l_opy_)
        with open(bstack11l11l1l1ll_opy_, bstackl_opy_ (u"ࠪࡻࠬᲈ")) as f:
            json.dump(bstack11l11l1lll1_opy_, f)
    else:
        bstack1l111ll11l_opy_ = {bstackl_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᲉ"): test_name, bstackl_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫᲊ"): bstack111llllll1l_opy_, bstackl_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬ᲋"): str(multiprocessing.current_process().name)}
        if bstackl_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷࠫ᲌") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack1l111ll11l_opy_)
  except Exception as e:
      logger.warn(bstackl_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺ࡯ࡳࡧࠣࡴࡾࡺࡥࡴࡶࠣࡪࡺࡴ࡮ࡦ࡮ࠣࡨࡦࡺࡡ࠻ࠢࡾࢁࠧ᲍").format(e))
def bstack1l11llll11_opy_(error_message, test_name, index, logger):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstackl_opy_ (u"ࠩࡩ࡭ࡱ࡫࡬ࡰࡥ࡮ࠤࡳࡵࡴࠡࡣࡹࡥ࡮ࡲࡡࡣ࡮ࡨ࠰ࠥࡻࡳࡪࡰࡪࠤࡧࡧࡳࡪࡥࠣࡪ࡮ࡲࡥࠡࡱࡳࡩࡷࡧࡴࡪࡱࡱࡷࠬ᲎"))
    try:
      bstack111lllll1ll_opy_ = []
      bstack1l111ll11l_opy_ = {bstackl_opy_ (u"ࠪࡲࡦࡳࡥࠨ᲏"): test_name, bstackl_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᲐ"): error_message, bstackl_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫᲑ"): index}
      bstack11l111ll1ll_opy_ = os.path.join(tempfile.gettempdir(), bstackl_opy_ (u"࠭ࡲࡰࡤࡲࡸࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧᲒ"))
      if os.path.exists(bstack11l111ll1ll_opy_):
          with open(bstack11l111ll1ll_opy_) as f:
              bstack111lllll1ll_opy_ = json.load(f)
      bstack111lllll1ll_opy_.append(bstack1l111ll11l_opy_)
      with open(bstack11l111ll1ll_opy_, bstackl_opy_ (u"ࠧࡸࠩᲓ")) as f:
          json.dump(bstack111lllll1ll_opy_, f)
    except Exception as e:
      logger.warn(bstackl_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺ࡯ࡳࡧࠣࡶࡴࡨ࡯ࡵࠢࡩࡹࡳࡴࡥ࡭ࠢࡧࡥࡹࡧ࠺ࠡࡽࢀࠦᲔ").format(e))
    return
  bstack111lllll1ll_opy_ = []
  bstack1l111ll11l_opy_ = {bstackl_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᲕ"): test_name, bstackl_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩᲖ"): error_message, bstackl_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪᲗ"): index}
  bstack11l111ll1ll_opy_ = os.path.join(tempfile.gettempdir(), bstackl_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴ࠯࡬ࡶࡳࡳ࠭Ი"))
  lock_file = bstack11l111ll1ll_opy_ + bstackl_opy_ (u"࠭࠮࡭ࡱࡦ࡯ࠬᲙ")
  try:
    with FileLock(lock_file, timeout=10):
      if os.path.exists(bstack11l111ll1ll_opy_):
          with open(bstack11l111ll1ll_opy_, bstackl_opy_ (u"ࠧࡳࠩᲚ")) as f:
              content = f.read().strip()
              if content:
                  bstack111lllll1ll_opy_ = json.load(open(bstack11l111ll1ll_opy_))
      bstack111lllll1ll_opy_.append(bstack1l111ll11l_opy_)
      with open(bstack11l111ll1ll_opy_, bstackl_opy_ (u"ࠨࡹࠪᲛ")) as f:
          json.dump(bstack111lllll1ll_opy_, f)
  except Exception as e:
    logger.warn(bstackl_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡴࡰࡴࡨࠤࡷࡵࡢࡰࡶࠣࡪࡺࡴ࡮ࡦ࡮ࠣࡨࡦࡺࡡࠡࡹ࡬ࡸ࡭ࠦࡦࡪ࡮ࡨࠤࡱࡵࡣ࡬࡫ࡱ࡫࠿ࠦࡻࡾࠤᲜ").format(e))
def bstack1l111l1l11_opy_(bstack1ll11llll1_opy_, name, logger):
  try:
    bstack1l111ll11l_opy_ = {bstackl_opy_ (u"ࠪࡲࡦࡳࡥࠨᲝ"): name, bstackl_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᲞ"): bstack1ll11llll1_opy_, bstackl_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫᲟ"): str(threading.current_thread()._name)}
    return bstack1l111ll11l_opy_
  except Exception as e:
    logger.warn(bstackl_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡸࡴࡸࡥࠡࡤࡨ࡬ࡦࡼࡥࠡࡨࡸࡲࡳ࡫࡬ࠡࡦࡤࡸࡦࡀࠠࡼࡿࠥᲠ").format(e))
  return
def bstack11l111l1l11_opy_():
    return platform.system() == bstackl_opy_ (u"ࠧࡘ࡫ࡱࡨࡴࡽࡳࠨᲡ")
def bstack11ll1lll1l_opy_(bstack11l111l111l_opy_, config, logger):
    bstack11l1l1111l1_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack11l111l111l_opy_.match(key)}
    except Exception as e:
        logger.debug(bstackl_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡫࡯࡬ࡵࡧࡵࠤࡨࡵ࡮ࡧ࡫ࡪࠤࡰ࡫ࡹࡴࠢࡥࡽࠥࡸࡥࡨࡧࡻࠤࡲࡧࡴࡤࡪ࠽ࠤࢀࢃࠢᲢ").format(e))
    return bstack11l1l1111l1_opy_
def bstack11l11llllll_opy_(bstack11l111l1lll_opy_, bstack11l11lll1l1_opy_):
    bstack11l11llll1l_opy_ = version.parse(bstack11l111l1lll_opy_)
    bstack11l11ll1lll_opy_ = version.parse(bstack11l11lll1l1_opy_)
    if bstack11l11llll1l_opy_ > bstack11l11ll1lll_opy_:
        return 1
    elif bstack11l11llll1l_opy_ < bstack11l11ll1lll_opy_:
        return -1
    else:
        return 0
def bstack111l1111ll_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack11l111llll1_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
def bstack11l11l1ll1l_opy_(framework):
    from browserstack_sdk._version import __version__
    return str(framework) + str(__version__)
def bstack11lll1ll11_opy_(options, framework, config, bstack1l1l11l1_opy_={}):
    if options is None:
        return
    if getattr(options, bstackl_opy_ (u"ࠩࡪࡩࡹ࠭Უ"), None):
        caps = options
    else:
        caps = options.to_capabilities()
    bstack1l1l1l1l11_opy_ = caps.get(bstackl_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᲤ"))
    bstack11l1111llll_opy_ = True
    bstack1llll1l1_opy_ = os.environ[bstackl_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩᲥ")]
    bstack1ll111l1ll1_opy_ = config.get(bstackl_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᲦ"), False)
    if bstack1ll111l1ll1_opy_:
        bstack1ll1lll1lll_opy_ = config.get(bstackl_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭Ყ"), {})
        bstack1ll1lll1lll_opy_[bstackl_opy_ (u"ࠧࡢࡷࡷ࡬࡙ࡵ࡫ࡦࡰࠪᲨ")] = os.getenv(bstackl_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭Ჩ"))
        bstack11ll11lll11_opy_ = json.loads(os.getenv(bstackl_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪᲪ"), bstackl_opy_ (u"ࠪࡿࢂ࠭Ძ"))).get(bstackl_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᲬ"))
    if bstack11l11111l1l_opy_(caps.get(bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡺࡹࡥࡘ࠵ࡆࠫᲭ"))) or bstack11l11111l1l_opy_(caps.get(bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡻࡳࡦࡡࡺ࠷ࡨ࠭Ხ"))):
        bstack11l1111llll_opy_ = False
    if bstack1l1lllll_opy_({bstackl_opy_ (u"ࠢࡶࡵࡨ࡛࠸ࡉࠢᲯ"): bstack11l1111llll_opy_}):
        bstack1l1l1l1l11_opy_ = bstack1l1l1l1l11_opy_ or {}
        bstack1l1l1l1l11_opy_[bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪᲰ")] = bstack11l11l1ll1l_opy_(framework)
        bstack1l1l1l1l11_opy_[bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫᲱ")] = bstack1l1ll11l11l_opy_()
        bstack1l1l1l1l11_opy_[bstackl_opy_ (u"ࠪࡸࡪࡹࡴࡩࡷࡥࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭Ჲ")] = bstack1llll1l1_opy_
        bstack1l1l1l1l11_opy_[bstackl_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭Ჳ")] = bstack1l1l11l1_opy_
        if bstack1ll111l1ll1_opy_:
            bstack1l1l1l1l11_opy_[bstackl_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᲴ")] = bstack1ll111l1ll1_opy_
            bstack1l1l1l1l11_opy_[bstackl_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭Ჵ")] = bstack1ll1lll1lll_opy_
            bstack1l1l1l1l11_opy_[bstackl_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧᲶ")][bstackl_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᲷ")] = bstack11ll11lll11_opy_
        if getattr(options, bstackl_opy_ (u"ࠩࡶࡩࡹࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵࡻࠪᲸ"), None):
            options.set_capability(bstackl_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᲹ"), bstack1l1l1l1l11_opy_)
        else:
            options[bstackl_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᲺ")] = bstack1l1l1l1l11_opy_
    else:
        if getattr(options, bstackl_opy_ (u"ࠬࡹࡥࡵࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸࡾ࠭᲻"), None):
            options.set_capability(bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧ᲼"), bstack11l11l1ll1l_opy_(framework))
            options.set_capability(bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᲽ"), bstack1l1ll11l11l_opy_())
            options.set_capability(bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡵࡧࡶࡸ࡭ࡻࡢࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪᲾ"), bstack1llll1l1_opy_)
            options.set_capability(bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪᲿ"), bstack1l1l11l1_opy_)
            if bstack1ll111l1ll1_opy_:
                options.set_capability(bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ᳀"), bstack1ll111l1ll1_opy_)
                options.set_capability(bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ᳁"), bstack1ll1lll1lll_opy_)
                options.set_capability(bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶ࠲ࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ᳂"), bstack11ll11lll11_opy_)
        else:
            options[bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧ᳃")] = bstack11l11l1ll1l_opy_(framework)
            options[bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨ᳄")] = bstack1l1ll11l11l_opy_()
            options[bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡵࡧࡶࡸ࡭ࡻࡢࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪ᳅")] = bstack1llll1l1_opy_
            options[bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪ᳆")] = bstack1l1l11l1_opy_
            if bstack1ll111l1ll1_opy_:
                options[bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ᳇")] = bstack1ll111l1ll1_opy_
                options[bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ᳈")] = bstack1ll1lll1lll_opy_
                options[bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫ᳉")][bstackl_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ᳊")] = bstack11ll11lll11_opy_
    return options
def bstack11l111l1ll1_opy_(bstack111llll1l11_opy_, framework):
    bstack1l1l11l1_opy_ = bstack1l1llll1l1_opy_.get_property(bstackl_opy_ (u"ࠢࡑࡎࡄ࡝࡜ࡘࡉࡈࡊࡗࡣࡕࡘࡏࡅࡗࡆࡘࡤࡓࡁࡑࠤ᳋"))
    if bstack111llll1l11_opy_ and len(bstack111llll1l11_opy_.split(bstackl_opy_ (u"ࠨࡥࡤࡴࡸࡃࠧ᳌"))) > 1:
        ws_url = bstack111llll1l11_opy_.split(bstackl_opy_ (u"ࠩࡦࡥࡵࡹ࠽ࠨ᳍"))[0]
        if bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭᳎") in ws_url:
            from browserstack_sdk._version import __version__
            bstack111llll11ll_opy_ = json.loads(urllib.parse.unquote(bstack111llll1l11_opy_.split(bstackl_opy_ (u"ࠫࡨࡧࡰࡴ࠿ࠪ᳏"))[1]))
            bstack111llll11ll_opy_ = bstack111llll11ll_opy_ or {}
            bstack1llll1l1_opy_ = os.environ[bstackl_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ᳐")]
            bstack111llll11ll_opy_[bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧ᳑")] = str(framework) + str(__version__)
            bstack111llll11ll_opy_[bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨ᳒")] = bstack1l1ll11l11l_opy_()
            bstack111llll11ll_opy_[bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡵࡧࡶࡸ࡭ࡻࡢࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪ᳓")] = bstack1llll1l1_opy_
            bstack111llll11ll_opy_[bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲ᳔ࠪ")] = bstack1l1l11l1_opy_
            bstack111llll1l11_opy_ = bstack111llll1l11_opy_.split(bstackl_opy_ (u"ࠪࡧࡦࡶࡳ࠾᳕ࠩ"))[0] + bstackl_opy_ (u"ࠫࡨࡧࡰࡴ࠿᳖ࠪ") + urllib.parse.quote(json.dumps(bstack111llll11ll_opy_))
    return bstack111llll1l11_opy_
def bstack1lll11ll1l_opy_():
    global bstack11l1111l1_opy_
    from playwright._impl._browser_type import BrowserType
    bstack11l1111l1_opy_ = BrowserType.connect
    return bstack11l1111l1_opy_
def bstack1111ll111_opy_(framework_name):
    global bstack1l1l1ll1ll_opy_
    bstack1l1l1ll1ll_opy_ = framework_name
    return framework_name
def bstack1lllll1111_opy_(self, *args, **kwargs):
    global bstack11l1111l1_opy_
    try:
        global bstack1l1l1ll1ll_opy_
        if bstackl_opy_ (u"ࠬࡽࡳࡆࡰࡧࡴࡴ࡯࡮ࡵ᳗ࠩ") in kwargs:
            kwargs[bstackl_opy_ (u"࠭ࡷࡴࡇࡱࡨࡵࡵࡩ࡯ࡶ᳘ࠪ")] = bstack11l111l1ll1_opy_(
                kwargs.get(bstackl_opy_ (u"ࠧࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷ᳙ࠫ"), None),
                bstack1l1l1ll1ll_opy_
            )
    except Exception as e:
        logger.error(bstackl_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪࡨࡲࠥࡶࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡖࡈࡐࠦࡣࡢࡲࡶ࠾ࠥࢁࡽࠣ᳚").format(str(e)))
    return bstack11l1111l1_opy_(self, *args, **kwargs)
def bstack111lll1111l_opy_(bstack11l11ll111l_opy_, proxies):
    proxy_settings = {}
    try:
        if not proxies:
            proxies = bstack111l11ll1_opy_(bstack11l11ll111l_opy_, bstackl_opy_ (u"ࠤࠥ᳛"))
        if proxies and proxies.get(bstackl_opy_ (u"ࠥ࡬ࡹࡺࡰࡴࠤ᳜")):
            parsed_url = urlparse(proxies.get(bstackl_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ᳝ࠥ")))
            if parsed_url and parsed_url.hostname: proxy_settings[bstackl_opy_ (u"ࠬࡶࡲࡰࡺࡼࡌࡴࡹࡴࠨ᳞")] = str(parsed_url.hostname)
            if parsed_url and parsed_url.port: proxy_settings[bstackl_opy_ (u"࠭ࡰࡳࡱࡻࡽࡕࡵࡲࡵ᳟ࠩ")] = str(parsed_url.port)
            if parsed_url and parsed_url.username: proxy_settings[bstackl_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡛ࡳࡦࡴࠪ᳠")] = str(parsed_url.username)
            if parsed_url and parsed_url.password: proxy_settings[bstackl_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡢࡵࡶࠫ᳡")] = str(parsed_url.password)
        return proxy_settings
    except:
        return proxy_settings
def bstack1l1lll11l_opy_(bstack11l11ll111l_opy_):
    bstack11l11111ll1_opy_ = {
        bstack11l1ll1l1ll_opy_[bstack11l1l1111ll_opy_]: bstack11l11ll111l_opy_[bstack11l1l1111ll_opy_]
        for bstack11l1l1111ll_opy_ in bstack11l11ll111l_opy_
        if bstack11l1l1111ll_opy_ in bstack11l1ll1l1ll_opy_
    }
    bstack11l11111ll1_opy_[bstackl_opy_ (u"ࠤࡳࡶࡴࡾࡹࡔࡧࡷࡸ࡮ࡴࡧࡴࠤ᳢")] = bstack111lll1111l_opy_(bstack11l11ll111l_opy_, bstack1l1llll1l1_opy_.get_property(bstackl_opy_ (u"ࠥࡴࡷࡵࡸࡺࡕࡨࡸࡹ࡯࡮ࡨࡵ᳣ࠥ")))
    bstack11l11111111_opy_ = [element.lower() for element in bstack11l1lllllll_opy_]
    bstack111lll111l1_opy_(bstack11l11111ll1_opy_, bstack11l11111111_opy_)
    return bstack11l11111ll1_opy_
def bstack111lll111l1_opy_(d, keys):
    for key in list(d.keys()):
        if key.lower() in keys:
            d[key] = bstackl_opy_ (u"ࠦ࠯࠰ࠪࠫࠤ᳤")
    for value in d.values():
        if isinstance(value, dict):
            bstack111lll111l1_opy_(value, keys)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    bstack111lll111l1_opy_(item, keys)
def bstack1l1l1llllll_opy_():
    bstack11l111lll1l_opy_ = [os.environ.get(bstackl_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡏࡌࡆࡕࡢࡈࡎࡘ᳥ࠢ")), os.path.join(os.path.expanduser(bstackl_opy_ (u"ࠨࡾ᳦ࠣ")), bstackl_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ᳧ࠧ")), os.path.join(bstackl_opy_ (u"ࠨ࠱ࡷࡱࡵ᳨࠭"), bstackl_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩᳩ"))]
    for path in bstack11l111lll1l_opy_:
        if path is None:
            continue
        try:
            if os.path.exists(path):
                logger.debug(bstackl_opy_ (u"ࠥࡊ࡮ࡲࡥࠡࠩࠥᳪ") + str(path) + bstackl_opy_ (u"ࠦࠬࠦࡥࡹ࡫ࡶࡸࡸ࠴ࠢᳫ"))
                if not os.access(path, os.W_OK):
                    logger.debug(bstackl_opy_ (u"ࠧࡍࡩࡷ࡫ࡱ࡫ࠥࡶࡥࡳ࡯࡬ࡷࡸ࡯࡯࡯ࡵࠣࡪࡴࡸࠠࠨࠤᳬ") + str(path) + bstackl_opy_ (u"ࠨ᳭ࠧࠣ"))
                    os.chmod(path, 0o777)
                else:
                    logger.debug(bstackl_opy_ (u"ࠢࡇ࡫࡯ࡩࠥ࠭ࠢᳮ") + str(path) + bstackl_opy_ (u"ࠣࠩࠣࡥࡱࡸࡥࡢࡦࡼࠤ࡭ࡧࡳࠡࡶ࡫ࡩࠥࡸࡥࡲࡷ࡬ࡶࡪࡪࠠࡱࡧࡵࡱ࡮ࡹࡳࡪࡱࡱࡷ࠳ࠨᳯ"))
            else:
                logger.debug(bstackl_opy_ (u"ࠤࡆࡶࡪࡧࡴࡪࡰࡪࠤ࡫࡯࡬ࡦࠢࠪࠦᳰ") + str(path) + bstackl_opy_ (u"ࠥࠫࠥࡽࡩࡵࡪࠣࡻࡷ࡯ࡴࡦࠢࡳࡩࡷࡳࡩࡴࡵ࡬ࡳࡳ࠴ࠢᳱ"))
                os.makedirs(path, exist_ok=True)
                os.chmod(path, 0o777)
            logger.debug(bstackl_opy_ (u"ࠦࡔࡶࡥࡳࡣࡷ࡭ࡴࡴࠠࡴࡷࡦࡧࡪ࡫ࡤࡦࡦࠣࡪࡴࡸࠠࠨࠤᳲ") + str(path) + bstackl_opy_ (u"ࠧ࠭࠮ࠣᳳ"))
            return path
        except Exception as e:
            logger.debug(bstackl_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࠦࡵࡱࠢࡩ࡭ࡱ࡫ࠠࠨࡽࡳࡥࡹ࡮ࡽࠨ࠼ࠣࠦ᳴") + str(e) + bstackl_opy_ (u"ࠢࠣᳵ"))
    logger.debug(bstackl_opy_ (u"ࠣࡃ࡯ࡰࠥࡶࡡࡵࡪࡶࠤ࡫ࡧࡩ࡭ࡧࡧ࠲ࠧᳶ"))
    return None
@measure(event_name=EVENTS.bstack11l1l1lll1l_opy_, stage=STAGE.bstack1l1111ll1_opy_)
def bstack1ll1llll1l1_opy_(binary_path, bstack1ll1lll11l1_opy_, bs_config):
    logger.debug(bstackl_opy_ (u"ࠤࡆࡹࡷࡸࡥ࡯ࡶࠣࡇࡑࡏࠠࡑࡣࡷ࡬ࠥ࡬࡯ࡶࡰࡧ࠾ࠥࢁࡽࠣ᳷").format(binary_path))
    bstack111lll111ll_opy_ = bstackl_opy_ (u"ࠪࠫ᳸")
    bstack11l11111l11_opy_ = {
        bstackl_opy_ (u"ࠫࡸࡪ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ᳹"): __version__,
        bstackl_opy_ (u"ࠧࡵࡳࠣᳺ"): platform.system(),
        bstackl_opy_ (u"ࠨ࡯ࡴࡡࡤࡶࡨ࡮ࠢ᳻"): platform.machine(),
        bstackl_opy_ (u"ࠢࡤ࡮࡬ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧ᳼"): bstackl_opy_ (u"ࠨ࠲ࠪ᳽"),
        bstackl_opy_ (u"ࠤࡶࡨࡰࡥ࡬ࡢࡰࡪࡹࡦ࡭ࡥࠣ᳾"): bstackl_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪ᳿")
    }
    bstack11l111111l1_opy_(bstack11l11111l11_opy_)
    try:
        if binary_path:
            bstack11l11111l11_opy_[bstackl_opy_ (u"ࠫࡨࡲࡩࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᴀ")] = subprocess.check_output([binary_path, bstackl_opy_ (u"ࠧࡼࡥࡳࡵ࡬ࡳࡳࠨᴁ")]).strip().decode(bstackl_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬᴂ"))
        response = requests.request(
            bstackl_opy_ (u"ࠧࡈࡇࡗࠫᴃ"),
            url=bstack1ll1lll11_opy_(bstack11l1lll111l_opy_),
            headers=None,
            auth=(bs_config[bstackl_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪᴄ")], bs_config[bstackl_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬᴅ")]),
            json=None,
            params=bstack11l11111l11_opy_
        )
        data = response.json()
        if response.status_code == 200 and bstackl_opy_ (u"ࠪࡹࡷࡲࠧᴆ") in data.keys() and bstackl_opy_ (u"ࠫࡺࡶࡤࡢࡶࡨࡨࡤࡩ࡬ࡪࡡࡹࡩࡷࡹࡩࡰࡰࠪᴇ") in data.keys():
            logger.debug(bstackl_opy_ (u"ࠧࡔࡥࡦࡦࠣࡸࡴࠦࡵࡱࡦࡤࡸࡪࠦࡢࡪࡰࡤࡶࡾ࠲ࠠࡤࡷࡵࡶࡪࡴࡴࠡࡤ࡬ࡲࡦࡸࡹࠡࡸࡨࡶࡸ࡯࡯࡯࠼ࠣࡿࢂࠨᴈ").format(bstack11l11111l11_opy_[bstackl_opy_ (u"࠭ࡣ࡭࡫ࡢࡺࡪࡸࡳࡪࡱࡱࠫᴉ")]))
            if bstackl_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡊࡐࡄࡖ࡞ࡥࡕࡓࡎࠪᴊ") in os.environ:
                logger.debug(bstackl_opy_ (u"ࠣࡕ࡮࡭ࡵࡶࡩ࡯ࡩࠣࡦ࡮ࡴࡡࡳࡻࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠥࡧࡳࠡࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡋࡑࡅࡗ࡟࡟ࡖࡔࡏࠤ࡮ࡹࠠࡴࡧࡷࠦᴋ"))
                data[bstackl_opy_ (u"ࠩࡸࡶࡱ࠭ᴌ")] = os.environ[bstackl_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅࡍࡓࡇࡒ࡚ࡡࡘࡖࡑ࠭ᴍ")]
            bstack111lll1ll11_opy_ = bstack11l111lll11_opy_(data[bstackl_opy_ (u"ࠫࡺࡸ࡬ࠨᴎ")], bstack1ll1lll11l1_opy_)
            bstack111lll111ll_opy_ = os.path.join(bstack1ll1lll11l1_opy_, bstack111lll1ll11_opy_)
            os.chmod(bstack111lll111ll_opy_, 0o777) # bstack11l111ll11l_opy_ permission
            return bstack111lll111ll_opy_
    except Exception as e:
        logger.debug(bstackl_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡨࡴࡽ࡮࡭ࡱࡤࡨ࡮ࡴࡧࠡࡰࡨࡻ࡙ࠥࡄࡌࠢࡾࢁࠧᴏ").format(e))
    return binary_path
def bstack11l111111l1_opy_(bstack11l11111l11_opy_):
    try:
        if bstackl_opy_ (u"࠭࡬ࡪࡰࡸࡼࠬᴐ") not in bstack11l11111l11_opy_[bstackl_opy_ (u"ࠧࡰࡵࠪᴑ")].lower():
            return
        if os.path.exists(bstackl_opy_ (u"ࠣ࠱ࡨࡸࡨ࠵࡯ࡴ࠯ࡵࡩࡱ࡫ࡡࡴࡧࠥᴒ")):
            with open(bstackl_opy_ (u"ࠤ࠲ࡩࡹࡩ࠯ࡰࡵ࠰ࡶࡪࡲࡥࡢࡵࡨࠦᴓ"), bstackl_opy_ (u"ࠥࡶࠧᴔ")) as f:
                bstack11l11ll11l1_opy_ = {}
                for line in f:
                    if bstackl_opy_ (u"ࠦࡂࠨᴕ") in line:
                        key, value = line.rstrip().split(bstackl_opy_ (u"ࠧࡃࠢᴖ"), 1)
                        bstack11l11ll11l1_opy_[key] = value.strip(bstackl_opy_ (u"࠭ࠢ࡝ࠩࠪᴗ"))
                bstack11l11111l11_opy_[bstackl_opy_ (u"ࠧࡥ࡫ࡶࡸࡷࡵࠧᴘ")] = bstack11l11ll11l1_opy_.get(bstackl_opy_ (u"ࠣࡋࡇࠦᴙ"), bstackl_opy_ (u"ࠤࠥᴚ"))
        elif os.path.exists(bstackl_opy_ (u"ࠥ࠳ࡪࡺࡣ࠰ࡣ࡯ࡴ࡮ࡴࡥ࠮ࡴࡨࡰࡪࡧࡳࡦࠤᴛ")):
            bstack11l11111l11_opy_[bstackl_opy_ (u"ࠫࡩ࡯ࡳࡵࡴࡲࠫᴜ")] = bstackl_opy_ (u"ࠬࡧ࡬ࡱ࡫ࡱࡩࠬᴝ")
    except Exception as e:
        logger.debug(bstackl_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡪࡩࡹࠦࡤࡪࡵࡷࡶࡴࠦ࡯ࡧࠢ࡯࡭ࡳࡻࡸࠣᴞ") + e)
@measure(event_name=EVENTS.bstack11l1ll11l1l_opy_, stage=STAGE.bstack1l1111ll1_opy_)
def bstack11l111lll11_opy_(bstack111llll1l1l_opy_, bstack11l11111lll_opy_):
    logger.debug(bstackl_opy_ (u"ࠢࡅࡱࡺࡲࡱࡵࡡࡥ࡫ࡱ࡫࡙ࠥࡄࡌࠢࡥ࡭ࡳࡧࡲࡺࠢࡩࡶࡴࡳ࠺ࠡࠤᴟ") + str(bstack111llll1l1l_opy_) + bstackl_opy_ (u"ࠣࠤᴠ"))
    zip_path = os.path.join(bstack11l11111lll_opy_, bstackl_opy_ (u"ࠤࡧࡳࡼࡴ࡬ࡰࡣࡧࡩࡩࡥࡦࡪ࡮ࡨ࠲ࡿ࡯ࡰࠣᴡ"))
    bstack111lll1ll11_opy_ = bstackl_opy_ (u"ࠪࠫᴢ")
    with requests.get(bstack111llll1l1l_opy_, stream=True) as response:
        response.raise_for_status()
        with open(zip_path, bstackl_opy_ (u"ࠦࡼࡨࠢᴣ")) as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        logger.debug(bstackl_opy_ (u"ࠧࡌࡩ࡭ࡧࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࡪࡪࠠࡴࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࡰࡾ࠴ࠢᴤ"))
    with zipfile.ZipFile(zip_path, bstackl_opy_ (u"࠭ࡲࠨᴥ")) as zip_ref:
        bstack11l11l1l1l1_opy_ = zip_ref.namelist()
        if len(bstack11l11l1l1l1_opy_) > 0:
            bstack111lll1ll11_opy_ = bstack11l11l1l1l1_opy_[0] # bstack11l11lll111_opy_ bstack11l1ll111l1_opy_ will be bstack111lll11l11_opy_ 1 file i.e. the binary in the zip
        zip_ref.extractall(bstack11l11111lll_opy_)
        logger.debug(bstackl_opy_ (u"ࠢࡇ࡫࡯ࡩࡸࠦࡳࡶࡥࡦࡩࡸࡹࡦࡶ࡮࡯ࡽࠥ࡫ࡸࡵࡴࡤࡧࡹ࡫ࡤࠡࡶࡲࠤࠬࠨᴦ") + str(bstack11l11111lll_opy_) + bstackl_opy_ (u"ࠣࠩࠥᴧ"))
    os.remove(zip_path)
    return bstack111lll1ll11_opy_
def get_cli_dir():
    bstack11l11l1111l_opy_ = bstack1l1l1llllll_opy_()
    if bstack11l11l1111l_opy_:
        bstack1ll1lll11l1_opy_ = os.path.join(bstack11l11l1111l_opy_, bstackl_opy_ (u"ࠤࡦࡰ࡮ࠨᴨ"))
        if not os.path.exists(bstack1ll1lll11l1_opy_):
            os.makedirs(bstack1ll1lll11l1_opy_, mode=0o777, exist_ok=True)
        return bstack1ll1lll11l1_opy_
    else:
        raise FileNotFoundError(bstackl_opy_ (u"ࠥࡒࡴࠦࡷࡳ࡫ࡷࡥࡧࡲࡥࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼࠤࡦࡼࡡࡪ࡮ࡤࡦࡱ࡫ࠠࡧࡱࡵࠤࡹ࡮ࡥࠡࡕࡇࡏࠥࡨࡩ࡯ࡣࡵࡽ࠳ࠨᴩ"))
def bstack1lll11lllll_opy_(bstack1ll1lll11l1_opy_):
    bstackl_opy_ (u"ࠦࠧࠨࡇࡦࡶࠣࡸ࡭࡫ࠠࡱࡣࡷ࡬ࠥ࡬࡯ࡳࠢࡷ࡬ࡪࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯࡙ࠥࡄࡌࠢࡥ࡭ࡳࡧࡲࡺࠢ࡬ࡲࠥࡧࠠࡸࡴ࡬ࡸࡦࡨ࡬ࡦࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽ࠳ࠨࠢࠣᴪ")
    bstack11l11l11l11_opy_ = [
        os.path.join(bstack1ll1lll11l1_opy_, f)
        for f in os.listdir(bstack1ll1lll11l1_opy_)
        if os.path.isfile(os.path.join(bstack1ll1lll11l1_opy_, f)) and f.startswith(bstackl_opy_ (u"ࠧࡨࡩ࡯ࡣࡵࡽ࠲ࠨᴫ"))
    ]
    if len(bstack11l11l11l11_opy_) > 0:
        return max(bstack11l11l11l11_opy_, key=os.path.getmtime) # get bstack111lll11l1l_opy_ binary
    return bstackl_opy_ (u"ࠨࠢᴬ")
def bstack11lll1111l1_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1ll111lll1l_opy_(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = bstack1ll111lll1l_opy_(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack11ll1ll1_opy_(data, keys, default=None):
    bstackl_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࡔࡣࡩࡩࡱࡿࠠࡨࡧࡷࠤࡦࠦ࡮ࡦࡵࡷࡩࡩࠦࡶࡢ࡮ࡸࡩࠥ࡬ࡲࡰ࡯ࠣࡥࠥࡪࡩࡤࡶ࡬ࡳࡳࡧࡲࡺࠢࡲࡶࠥࡲࡩࡴࡶ࠱ࠎࠥࠦࠠࠡ࠼ࡳࡥࡷࡧ࡭ࠡࡦࡤࡸࡦࡀࠠࡕࡪࡨࠤࡩ࡯ࡣࡵ࡫ࡲࡲࡦࡸࡹࠡࡱࡵࠤࡱ࡯ࡳࡵࠢࡷࡳࠥࡺࡲࡢࡸࡨࡶࡸ࡫࠮ࠋࠢࠣࠤࠥࡀࡰࡢࡴࡤࡱࠥࡱࡥࡺࡵ࠽ࠤࡆࠦ࡬ࡪࡵࡷࠤࡴ࡬ࠠ࡬ࡧࡼࡷ࠴࡯࡮ࡥ࡫ࡦࡩࡸࠦࡲࡦࡲࡵࡩࡸ࡫࡮ࡵ࡫ࡱ࡫ࠥࡺࡨࡦࠢࡳࡥࡹ࡮࠮ࠋࠢࠣࠤࠥࡀࡰࡢࡴࡤࡱࠥࡪࡥࡧࡣࡸࡰࡹࡀࠠࡗࡣ࡯ࡹࡪࠦࡴࡰࠢࡵࡩࡹࡻࡲ࡯ࠢ࡬ࡪࠥࡺࡨࡦࠢࡳࡥࡹ࡮ࠠࡥࡱࡨࡷࠥࡴ࡯ࡵࠢࡨࡼ࡮ࡹࡴ࠯ࠌࠣࠤࠥࠦ࠺ࡳࡧࡷࡹࡷࡴ࠺ࠡࡖ࡫ࡩࠥࡼࡡ࡭ࡷࡨࠤࡦࡺࠠࡵࡪࡨࠤࡳ࡫ࡳࡵࡧࡧࠤࡵࡧࡴࡩ࠮ࠣࡳࡷࠦࡤࡦࡨࡤࡹࡱࡺࠠࡪࡨࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩ࠴ࠊࠡࠢࠣࠤࠧࠨࠢᴭ")
    if not data:
        return default
    current = data
    try:
        for key in keys:
            if isinstance(current, dict):
                current = current[key]
            elif isinstance(current, list) and isinstance(key, int):
                current = current[key]
            else:
                return default
        return current
    except (KeyError, IndexError, TypeError):
        return default