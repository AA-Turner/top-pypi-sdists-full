# coding: UTF-8
import sys
bstack11l1l1_opy_ = sys.version_info [0] == 2
bstack111l1l1_opy_ = 2048
bstack11l11ll_opy_ = 7
def bstack1llllll_opy_ (bstack1ll111l_opy_):
    global bstack1l111l_opy_
    bstack1l11l_opy_ = ord (bstack1ll111l_opy_ [-1])
    bstack1111l1l_opy_ = bstack1ll111l_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack1l11l_opy_ % len (bstack1111l1l_opy_)
    bstack1ll1_opy_ = bstack1111l1l_opy_ [:bstack11ll1ll_opy_] + bstack1111l1l_opy_ [bstack11ll1ll_opy_:]
    if bstack11l1l1_opy_:
        bstack1lllll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack111l1l1_opy_ - (bstack11ll1_opy_ + bstack1l11l_opy_) % bstack11l11ll_opy_) for bstack11ll1_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1lllll1l_opy_ = str () .join ([chr (ord (char) - bstack111l1l1_opy_ - (bstack11ll1_opy_ + bstack1l11l_opy_) % bstack11l11ll_opy_) for bstack11ll1_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1lllll1l_opy_)
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
from bstack_utils.constants import (bstack11ll1ll111l_opy_, bstack11l1llll1_opy_, bstack1l1l1111_opy_, bstack1l111111_opy_,
                                    bstack11ll1ll1l1l_opy_, bstack11ll1l111l1_opy_, bstack11ll1lllll1_opy_, bstack11ll1l1111l_opy_)
from bstack_utils.measure import measure
from bstack_utils.messages import bstack11l1l1111l_opy_, bstack11l1lll1ll_opy_
from bstack_utils.proxy import bstack11111111_opy_, bstack1l111ll11l_opy_
from bstack_utils.constants import *
from bstack_utils import bstack1llllll1ll_opy_
from browserstack_sdk._version import __version__
bstack1l1ll1l1l1_opy_ = Config.bstack11ll1ll1l1_opy_()
logger = bstack1llllll1ll_opy_.get_logger(__name__, bstack1llllll1ll_opy_.bstack1llll11llll_opy_())
def bstack11llll1l11l_opy_(config):
    return config[bstack1llllll_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬᦩ")]
def bstack11llll1ll11_opy_(config):
    return config[bstack1llllll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧᦪ")]
def bstack1l111lll11_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack11l11llllll_opy_(obj):
    values = []
    bstack11l1l111lll_opy_ = re.compile(bstack1llllll_opy_ (u"ࡷࠨ࡞ࡄࡗࡖࡘࡔࡓ࡟ࡕࡃࡊࡣࡡࡪࠫࠥࠤᦫ"), re.I)
    for key in obj.keys():
        if bstack11l1l111lll_opy_.match(key):
            values.append(obj[key])
    return values
def bstack11l1ll11111_opy_(config):
    tags = []
    tags.extend(bstack11l11llllll_opy_(os.environ))
    tags.extend(bstack11l11llllll_opy_(config))
    return tags
def bstack11l1l11l11l_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack11l1lll11ll_opy_(bstack11ll1111lll_opy_):
    if not bstack11ll1111lll_opy_:
        return bstack1llllll_opy_ (u"࠭ࠧ᦬")
    return bstack1llllll_opy_ (u"ࠢࡼࡿࠣࠬࢀࢃࠩࠣ᦭").format(bstack11ll1111lll_opy_.name, bstack11ll1111lll_opy_.email)
def bstack11llll11l1l_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack11l1lll1lll_opy_ = repo.common_dir
        info = {
            bstack1llllll_opy_ (u"ࠣࡵ࡫ࡥࠧ᦮"): repo.head.commit.hexsha,
            bstack1llllll_opy_ (u"ࠤࡶ࡬ࡴࡸࡴࡠࡵ࡫ࡥࠧ᦯"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack1llllll_opy_ (u"ࠥࡦࡷࡧ࡮ࡤࡪࠥᦰ"): repo.active_branch.name,
            bstack1llllll_opy_ (u"ࠦࡹࡧࡧࠣᦱ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack1llllll_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡹ࡫ࡲࠣᦲ"): bstack11l1lll11ll_opy_(repo.head.commit.committer),
            bstack1llllll_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡺࡥࡳࡡࡧࡥࡹ࡫ࠢᦳ"): repo.head.commit.committed_datetime.isoformat(),
            bstack1llllll_opy_ (u"ࠢࡢࡷࡷ࡬ࡴࡸࠢᦴ"): bstack11l1lll11ll_opy_(repo.head.commit.author),
            bstack1llllll_opy_ (u"ࠣࡣࡸࡸ࡭ࡵࡲࡠࡦࡤࡸࡪࠨᦵ"): repo.head.commit.authored_datetime.isoformat(),
            bstack1llllll_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡡࡰࡩࡸࡹࡡࡨࡧࠥᦶ"): repo.head.commit.message,
            bstack1llllll_opy_ (u"ࠥࡶࡴࡵࡴࠣᦷ"): repo.git.rev_parse(bstack1llllll_opy_ (u"ࠦ࠲࠳ࡳࡩࡱࡺ࠱ࡹࡵࡰ࡭ࡧࡹࡩࡱࠨᦸ")),
            bstack1llllll_opy_ (u"ࠧࡩ࡯࡮࡯ࡲࡲࡤ࡭ࡩࡵࡡࡧ࡭ࡷࠨᦹ"): bstack11l1lll1lll_opy_,
            bstack1llllll_opy_ (u"ࠨࡷࡰࡴ࡮ࡸࡷ࡫ࡥࡠࡩ࡬ࡸࡤࡪࡩࡳࠤᦺ"): subprocess.check_output([bstack1llllll_opy_ (u"ࠢࡨ࡫ࡷࠦᦻ"), bstack1llllll_opy_ (u"ࠣࡴࡨࡺ࠲ࡶࡡࡳࡵࡨࠦᦼ"), bstack1llllll_opy_ (u"ࠤ࠰࠱࡬࡯ࡴ࠮ࡥࡲࡱࡲࡵ࡮࠮ࡦ࡬ࡶࠧᦽ")]).strip().decode(
                bstack1llllll_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩᦾ")),
            bstack1llllll_opy_ (u"ࠦࡱࡧࡳࡵࡡࡷࡥ࡬ࠨᦿ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack1llllll_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡸࡥࡳࡪࡰࡦࡩࡤࡲࡡࡴࡶࡢࡸࡦ࡭ࠢᧀ"): repo.git.rev_list(
                bstack1llllll_opy_ (u"ࠨࡻࡾ࠰࠱ࡿࢂࠨᧁ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack11l1l1lllll_opy_ = []
        for remote in remotes:
            bstack11ll11l1l11_opy_ = {
                bstack1llllll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᧂ"): remote.name,
                bstack1llllll_opy_ (u"ࠣࡷࡵࡰࠧᧃ"): remote.url,
            }
            bstack11l1l1lllll_opy_.append(bstack11ll11l1l11_opy_)
        bstack11l1llll111_opy_ = {
            bstack1llllll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᧄ"): bstack1llllll_opy_ (u"ࠥ࡫࡮ࡺࠢᧅ"),
            **info,
            bstack1llllll_opy_ (u"ࠦࡷ࡫࡭ࡰࡶࡨࡷࠧᧆ"): bstack11l1l1lllll_opy_
        }
        bstack11l1llll111_opy_ = bstack11ll11l1l1l_opy_(bstack11l1llll111_opy_)
        return bstack11l1llll111_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack1llllll_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡵࡰࡶ࡮ࡤࡸ࡮ࡴࡧࠡࡉ࡬ࡸࠥࡳࡥࡵࡣࡧࡥࡹࡧࠠࡸ࡫ࡷ࡬ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠣᧇ").format(err))
        return {}
def bstack11ll11l1l1l_opy_(bstack11l1llll111_opy_):
    bstack11l1l11l1l1_opy_ = bstack11l1l1ll1ll_opy_(bstack11l1llll111_opy_)
    if bstack11l1l11l1l1_opy_ and bstack11l1l11l1l1_opy_ > bstack11ll1ll1l1l_opy_:
        bstack11l1l1ll111_opy_ = bstack11l1l11l1l1_opy_ - bstack11ll1ll1l1l_opy_
        bstack11l1lllllll_opy_ = bstack11l1l1111ll_opy_(bstack11l1llll111_opy_[bstack1llllll_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡥ࡭ࡦࡵࡶࡥ࡬࡫ࠢᧈ")], bstack11l1l1ll111_opy_)
        bstack11l1llll111_opy_[bstack1llllll_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺ࡟࡮ࡧࡶࡷࡦ࡭ࡥࠣᧉ")] = bstack11l1lllllll_opy_
        logger.info(bstack1llllll_opy_ (u"ࠣࡖ࡫ࡩࠥࡩ࡯࡮࡯࡬ࡸࠥ࡮ࡡࡴࠢࡥࡩࡪࡴࠠࡵࡴࡸࡲࡨࡧࡴࡦࡦ࠱ࠤࡘ࡯ࡺࡦࠢࡲࡪࠥࡩ࡯࡮࡯࡬ࡸࠥࡧࡦࡵࡧࡵࠤࡹࡸࡵ࡯ࡥࡤࡸ࡮ࡵ࡮ࠡ࡫ࡶࠤࢀࢃࠠࡌࡄࠥ᧊")
                    .format(bstack11l1l1ll1ll_opy_(bstack11l1llll111_opy_) / 1024))
    return bstack11l1llll111_opy_
def bstack11l1l1ll1ll_opy_(bstack1lllll1l1_opy_):
    try:
        if bstack1lllll1l1_opy_:
            bstack11l11lll1ll_opy_ = json.dumps(bstack1lllll1l1_opy_)
            bstack11l1l1llll1_opy_ = sys.getsizeof(bstack11l11lll1ll_opy_)
            return bstack11l1l1llll1_opy_
    except Exception as e:
        logger.debug(bstack1llllll_opy_ (u"ࠤࡖࡳࡲ࡫ࡴࡩ࡫ࡱ࡫ࠥࡽࡥ࡯ࡶࠣࡻࡷࡵ࡮ࡨࠢࡺ࡬࡮ࡲࡥࠡࡥࡤࡰࡨࡻ࡬ࡢࡶ࡬ࡲ࡬ࠦࡳࡪࡼࡨࠤࡴ࡬ࠠࡋࡕࡒࡒࠥࡵࡢ࡫ࡧࡦࡸ࠿ࠦࡻࡾࠤ᧋").format(e))
    return -1
def bstack11l1l1111ll_opy_(field, bstack11l1l1l1111_opy_):
    try:
        bstack11l1l1lll1l_opy_ = len(bytes(bstack11ll1l111l1_opy_, bstack1llllll_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩ᧌")))
        bstack11l1ll11l1l_opy_ = bytes(field, bstack1llllll_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪ᧍"))
        bstack11ll11l111l_opy_ = len(bstack11l1ll11l1l_opy_)
        bstack11ll111ll1l_opy_ = ceil(bstack11ll11l111l_opy_ - bstack11l1l1l1111_opy_ - bstack11l1l1lll1l_opy_)
        if bstack11ll111ll1l_opy_ > 0:
            bstack11l11lll11l_opy_ = bstack11l1ll11l1l_opy_[:bstack11ll111ll1l_opy_].decode(bstack1llllll_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫ᧎"), errors=bstack1llllll_opy_ (u"࠭ࡩࡨࡰࡲࡶࡪ࠭᧏")) + bstack11ll1l111l1_opy_
            return bstack11l11lll11l_opy_
    except Exception as e:
        logger.debug(bstack1llllll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡺࡲࡶࡰࡦࡥࡹ࡯࡮ࡨࠢࡩ࡭ࡪࡲࡤ࠭ࠢࡱࡳࡹ࡮ࡩ࡯ࡩࠣࡻࡦࡹࠠࡵࡴࡸࡲࡨࡧࡴࡦࡦࠣ࡬ࡪࡸࡥ࠻ࠢࡾࢁࠧ᧐").format(e))
    return field
def bstack1l1ll111_opy_():
    env = os.environ
    if (bstack1llllll_opy_ (u"ࠣࡌࡈࡒࡐࡏࡎࡔࡡࡘࡖࡑࠨ᧑") in env and len(env[bstack1llllll_opy_ (u"ࠤࡍࡉࡓࡑࡉࡏࡕࡢ࡙ࡗࡒࠢ᧒")]) > 0) or (
            bstack1llllll_opy_ (u"ࠥࡎࡊࡔࡋࡊࡐࡖࡣࡍࡕࡍࡆࠤ᧓") in env and len(env[bstack1llllll_opy_ (u"ࠦࡏࡋࡎࡌࡋࡑࡗࡤࡎࡏࡎࡇࠥ᧔")]) > 0):
        return {
            bstack1llllll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ᧕"): bstack1llllll_opy_ (u"ࠨࡊࡦࡰ࡮࡭ࡳࡹࠢ᧖"),
            bstack1llllll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ᧗"): env.get(bstack1llllll_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦ᧘")),
            bstack1llllll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ᧙"): env.get(bstack1llllll_opy_ (u"ࠥࡎࡔࡈ࡟ࡏࡃࡐࡉࠧ᧚")),
            bstack1llllll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ᧛"): env.get(bstack1llllll_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦ᧜"))
        }
    if env.get(bstack1llllll_opy_ (u"ࠨࡃࡊࠤ᧝")) == bstack1llllll_opy_ (u"ࠢࡵࡴࡸࡩࠧ᧞") and bstack11l1l1ll_opy_(env.get(bstack1llllll_opy_ (u"ࠣࡅࡌࡖࡈࡒࡅࡄࡋࠥ᧟"))):
        return {
            bstack1llllll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᧠"): bstack1llllll_opy_ (u"ࠥࡇ࡮ࡸࡣ࡭ࡧࡆࡍࠧ᧡"),
            bstack1llllll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ᧢"): env.get(bstack1llllll_opy_ (u"ࠧࡉࡉࡓࡅࡏࡉࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣ᧣")),
            bstack1llllll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ᧤"): env.get(bstack1llllll_opy_ (u"ࠢࡄࡋࡕࡇࡑࡋ࡟ࡋࡑࡅࠦ᧥")),
            bstack1llllll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ᧦"): env.get(bstack1llllll_opy_ (u"ࠤࡆࡍࡗࡉࡌࡆࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࠧ᧧"))
        }
    if env.get(bstack1llllll_opy_ (u"ࠥࡇࡎࠨ᧨")) == bstack1llllll_opy_ (u"ࠦࡹࡸࡵࡦࠤ᧩") and bstack11l1l1ll_opy_(env.get(bstack1llllll_opy_ (u"࡚ࠧࡒࡂࡘࡌࡗࠧ᧪"))):
        return {
            bstack1llllll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ᧫"): bstack1llllll_opy_ (u"ࠢࡕࡴࡤࡺ࡮ࡹࠠࡄࡋࠥ᧬"),
            bstack1llllll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ᧭"): env.get(bstack1llllll_opy_ (u"ࠤࡗࡖࡆ࡜ࡉࡔࡡࡅ࡙ࡎࡒࡄࡠ࡙ࡈࡆࡤ࡛ࡒࡍࠤ᧮")),
            bstack1llllll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ᧯"): env.get(bstack1llllll_opy_ (u"࡙ࠦࡘࡁࡗࡋࡖࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨ᧰")),
            bstack1llllll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ᧱"): env.get(bstack1llllll_opy_ (u"ࠨࡔࡓࡃ࡙ࡍࡘࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧ᧲"))
        }
    if env.get(bstack1llllll_opy_ (u"ࠢࡄࡋࠥ᧳")) == bstack1llllll_opy_ (u"ࠣࡶࡵࡹࡪࠨ᧴") and env.get(bstack1llllll_opy_ (u"ࠤࡆࡍࡤࡔࡁࡎࡇࠥ᧵")) == bstack1llllll_opy_ (u"ࠥࡧࡴࡪࡥࡴࡪ࡬ࡴࠧ᧶"):
        return {
            bstack1llllll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᧷"): bstack1llllll_opy_ (u"ࠧࡉ࡯ࡥࡧࡶ࡬࡮ࡶࠢ᧸"),
            bstack1llllll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ᧹"): None,
            bstack1llllll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ᧺"): None,
            bstack1llllll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ᧻"): None
        }
    if env.get(bstack1llllll_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡈࡒࡂࡐࡆࡌࠧ᧼")) and env.get(bstack1llllll_opy_ (u"ࠥࡆࡎ࡚ࡂࡖࡅࡎࡉ࡙ࡥࡃࡐࡏࡐࡍ࡙ࠨ᧽")):
        return {
            bstack1llllll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᧾"): bstack1llllll_opy_ (u"ࠧࡈࡩࡵࡤࡸࡧࡰ࡫ࡴࠣ᧿"),
            bstack1llllll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᨀ"): env.get(bstack1llllll_opy_ (u"ࠢࡃࡋࡗࡆ࡚ࡉࡋࡆࡖࡢࡋࡎ࡚࡟ࡉࡖࡗࡔࡤࡕࡒࡊࡉࡌࡒࠧᨁ")),
            bstack1llllll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᨂ"): None,
            bstack1llllll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᨃ"): env.get(bstack1llllll_opy_ (u"ࠥࡆࡎ࡚ࡂࡖࡅࡎࡉ࡙ࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧᨄ"))
        }
    if env.get(bstack1llllll_opy_ (u"ࠦࡈࡏࠢᨅ")) == bstack1llllll_opy_ (u"ࠧࡺࡲࡶࡧࠥᨆ") and bstack11l1l1ll_opy_(env.get(bstack1llllll_opy_ (u"ࠨࡄࡓࡑࡑࡉࠧᨇ"))):
        return {
            bstack1llllll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᨈ"): bstack1llllll_opy_ (u"ࠣࡆࡵࡳࡳ࡫ࠢᨉ"),
            bstack1llllll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᨊ"): env.get(bstack1llllll_opy_ (u"ࠥࡈࡗࡕࡎࡆࡡࡅ࡙ࡎࡒࡄࡠࡎࡌࡒࡐࠨᨋ")),
            bstack1llllll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᨌ"): None,
            bstack1llllll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᨍ"): env.get(bstack1llllll_opy_ (u"ࠨࡄࡓࡑࡑࡉࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦᨎ"))
        }
    if env.get(bstack1llllll_opy_ (u"ࠢࡄࡋࠥᨏ")) == bstack1llllll_opy_ (u"ࠣࡶࡵࡹࡪࠨᨐ") and bstack11l1l1ll_opy_(env.get(bstack1llllll_opy_ (u"ࠤࡖࡉࡒࡇࡐࡉࡑࡕࡉࠧᨑ"))):
        return {
            bstack1llllll_opy_ (u"ࠥࡲࡦࡳࡥࠣᨒ"): bstack1llllll_opy_ (u"ࠦࡘ࡫࡭ࡢࡲ࡫ࡳࡷ࡫ࠢᨓ"),
            bstack1llllll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᨔ"): env.get(bstack1llllll_opy_ (u"ࠨࡓࡆࡏࡄࡔࡍࡕࡒࡆࡡࡒࡖࡌࡇࡎࡊ࡜ࡄࡘࡎࡕࡎࡠࡗࡕࡐࠧᨕ")),
            bstack1llllll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᨖ"): env.get(bstack1llllll_opy_ (u"ࠣࡕࡈࡑࡆࡖࡈࡐࡔࡈࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨᨗ")),
            bstack1llllll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲᨘࠣ"): env.get(bstack1llllll_opy_ (u"ࠥࡗࡊࡓࡁࡑࡊࡒࡖࡊࡥࡊࡐࡄࡢࡍࡉࠨᨙ"))
        }
    if env.get(bstack1llllll_opy_ (u"ࠦࡈࡏࠢᨚ")) == bstack1llllll_opy_ (u"ࠧࡺࡲࡶࡧࠥᨛ") and bstack11l1l1ll_opy_(env.get(bstack1llllll_opy_ (u"ࠨࡇࡊࡖࡏࡅࡇࡥࡃࡊࠤ᨜"))):
        return {
            bstack1llllll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ᨝"): bstack1llllll_opy_ (u"ࠣࡉ࡬ࡸࡑࡧࡢࠣ᨞"),
            bstack1llllll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ᨟"): env.get(bstack1llllll_opy_ (u"ࠥࡇࡎࡥࡊࡐࡄࡢ࡙ࡗࡒࠢᨠ")),
            bstack1llllll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᨡ"): env.get(bstack1llllll_opy_ (u"ࠧࡉࡉࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥᨢ")),
            bstack1llllll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᨣ"): env.get(bstack1llllll_opy_ (u"ࠢࡄࡋࡢࡎࡔࡈ࡟ࡊࡆࠥᨤ"))
        }
    if env.get(bstack1llllll_opy_ (u"ࠣࡅࡌࠦᨥ")) == bstack1llllll_opy_ (u"ࠤࡷࡶࡺ࡫ࠢᨦ") and bstack11l1l1ll_opy_(env.get(bstack1llllll_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡍࡌࡘࡊࠨᨧ"))):
        return {
            bstack1llllll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᨨ"): bstack1llllll_opy_ (u"ࠧࡈࡵࡪ࡮ࡧ࡯࡮ࡺࡥࠣᨩ"),
            bstack1llllll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᨪ"): env.get(bstack1llllll_opy_ (u"ࠢࡃࡗࡌࡐࡉࡑࡉࡕࡇࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨᨫ")),
            bstack1llllll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᨬ"): env.get(bstack1llllll_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࡤࡒࡁࡃࡇࡏࠦᨭ")) or env.get(bstack1llllll_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡍࡌࡘࡊࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡐࡄࡑࡊࠨᨮ")),
            bstack1llllll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᨯ"): env.get(bstack1llllll_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢᨰ"))
        }
    if bstack11l1l1ll_opy_(env.get(bstack1llllll_opy_ (u"ࠨࡔࡇࡡࡅ࡙ࡎࡒࡄࠣᨱ"))):
        return {
            bstack1llllll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᨲ"): bstack1llllll_opy_ (u"ࠣࡘ࡬ࡷࡺࡧ࡬ࠡࡕࡷࡹࡩ࡯࡯ࠡࡖࡨࡥࡲࠦࡓࡦࡴࡹ࡭ࡨ࡫ࡳࠣᨳ"),
            bstack1llllll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᨴ"): bstack1llllll_opy_ (u"ࠥࡿࢂࢁࡽࠣᨵ").format(env.get(bstack1llllll_opy_ (u"ࠫࡘ࡟ࡓࡕࡇࡐࡣ࡙ࡋࡁࡎࡈࡒ࡙ࡓࡊࡁࡕࡋࡒࡒࡘࡋࡒࡗࡇࡕ࡙ࡗࡏࠧᨶ")), env.get(bstack1llllll_opy_ (u"࡙࡙ࠬࡔࡖࡈࡑࡤ࡚ࡅࡂࡏࡓࡖࡔࡐࡅࡄࡖࡌࡈࠬᨷ"))),
            bstack1llllll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᨸ"): env.get(bstack1llllll_opy_ (u"ࠢࡔ࡛ࡖࡘࡊࡓ࡟ࡅࡇࡉࡍࡓࡏࡔࡊࡑࡑࡍࡉࠨᨹ")),
            bstack1llllll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᨺ"): env.get(bstack1llllll_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊࡉࡅࠤᨻ"))
        }
    if bstack11l1l1ll_opy_(env.get(bstack1llllll_opy_ (u"ࠥࡅࡕࡖࡖࡆ࡛ࡒࡖࠧᨼ"))):
        return {
            bstack1llllll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᨽ"): bstack1llllll_opy_ (u"ࠧࡇࡰࡱࡸࡨࡽࡴࡸࠢᨾ"),
            bstack1llllll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᨿ"): bstack1llllll_opy_ (u"ࠢࡼࡿ࠲ࡴࡷࡵࡪࡦࡥࡷ࠳ࢀࢃ࠯ࡼࡿ࠲ࡦࡺ࡯࡬ࡥࡵ࠲ࡿࢂࠨᩀ").format(env.get(bstack1llllll_opy_ (u"ࠨࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢ࡙ࡗࡒࠧᩁ")), env.get(bstack1llllll_opy_ (u"ࠩࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡆࡉࡃࡐࡗࡑࡘࡤࡔࡁࡎࡇࠪᩂ")), env.get(bstack1llllll_opy_ (u"ࠪࡅࡕࡖࡖࡆ࡛ࡒࡖࡤࡖࡒࡐࡌࡈࡇ࡙ࡥࡓࡍࡗࡊࠫᩃ")), env.get(bstack1llllll_opy_ (u"ࠫࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡂࡖࡋࡏࡈࡤࡏࡄࠨᩄ"))),
            bstack1llllll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᩅ"): env.get(bstack1llllll_opy_ (u"ࠨࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥᩆ")),
            bstack1llllll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᩇ"): env.get(bstack1llllll_opy_ (u"ࠣࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤᩈ"))
        }
    if env.get(bstack1llllll_opy_ (u"ࠤࡄ࡞࡚ࡘࡅࡠࡊࡗࡘࡕࡥࡕࡔࡇࡕࡣࡆࡍࡅࡏࡖࠥᩉ")) and env.get(bstack1llllll_opy_ (u"ࠥࡘࡋࡥࡂࡖࡋࡏࡈࠧᩊ")):
        return {
            bstack1llllll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᩋ"): bstack1llllll_opy_ (u"ࠧࡇࡺࡶࡴࡨࠤࡈࡏࠢᩌ"),
            bstack1llllll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᩍ"): bstack1llllll_opy_ (u"ࠢࡼࡿࡾࢁ࠴ࡥࡢࡶ࡫࡯ࡨ࠴ࡸࡥࡴࡷ࡯ࡸࡸࡅࡢࡶ࡫࡯ࡨࡎࡪ࠽ࡼࡿࠥᩎ").format(env.get(bstack1llllll_opy_ (u"ࠨࡕ࡜ࡗ࡙ࡋࡍࡠࡖࡈࡅࡒࡌࡏࡖࡐࡇࡅ࡙ࡏࡏࡏࡕࡈࡖ࡛ࡋࡒࡖࡔࡌࠫᩏ")), env.get(bstack1llllll_opy_ (u"ࠩࡖ࡝ࡘ࡚ࡅࡎࡡࡗࡉࡆࡓࡐࡓࡑࡍࡉࡈ࡚ࠧᩐ")), env.get(bstack1llllll_opy_ (u"ࠪࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡊࡆࠪᩑ"))),
            bstack1llllll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᩒ"): env.get(bstack1llllll_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡌࡈࠧᩓ")),
            bstack1llllll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᩔ"): env.get(bstack1llllll_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡎࡊࠢᩕ"))
        }
    if any([env.get(bstack1llllll_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࠨᩖ")), env.get(bstack1llllll_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤࡘࡅࡔࡑࡏ࡚ࡊࡊ࡟ࡔࡑࡘࡖࡈࡋ࡟ࡗࡇࡕࡗࡎࡕࡎࠣᩗ")), env.get(bstack1llllll_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡓࡐࡗࡕࡇࡊࡥࡖࡆࡔࡖࡍࡔࡔࠢᩘ"))]):
        return {
            bstack1llllll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᩙ"): bstack1llllll_opy_ (u"ࠧࡇࡗࡔࠢࡆࡳࡩ࡫ࡂࡶ࡫࡯ࡨࠧᩚ"),
            bstack1llllll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᩛ"): env.get(bstack1llllll_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡔ࡚ࡈࡌࡊࡅࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨᩜ")),
            bstack1llllll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᩝ"): env.get(bstack1llllll_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠢᩞ")),
            bstack1llllll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ᩟"): env.get(bstack1llllll_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠤ᩠"))
        }
    if env.get(bstack1llllll_opy_ (u"ࠧࡨࡡ࡮ࡤࡲࡳࡤࡨࡵࡪ࡮ࡧࡒࡺࡳࡢࡦࡴࠥᩡ")):
        return {
            bstack1llllll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᩢ"): bstack1llllll_opy_ (u"ࠢࡃࡣࡰࡦࡴࡵࠢᩣ"),
            bstack1llllll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᩤ"): env.get(bstack1llllll_opy_ (u"ࠤࡥࡥࡲࡨ࡯ࡰࡡࡥࡹ࡮ࡲࡤࡓࡧࡶࡹࡱࡺࡳࡖࡴ࡯ࠦᩥ")),
            bstack1llllll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᩦ"): env.get(bstack1llllll_opy_ (u"ࠦࡧࡧ࡭ࡣࡱࡲࡣࡸ࡮࡯ࡳࡶࡍࡳࡧࡔࡡ࡮ࡧࠥᩧ")),
            bstack1llllll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᩨ"): env.get(bstack1llllll_opy_ (u"ࠨࡢࡢ࡯ࡥࡳࡴࡥࡢࡶ࡫࡯ࡨࡓࡻ࡭ࡣࡧࡵࠦᩩ"))
        }
    if env.get(bstack1llllll_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࠣᩪ")) or env.get(bstack1llllll_opy_ (u"࡙ࠣࡈࡖࡈࡑࡅࡓࡡࡐࡅࡎࡔ࡟ࡑࡋࡓࡉࡑࡏࡎࡆࡡࡖࡘࡆࡘࡔࡆࡆࠥᩫ")):
        return {
            bstack1llllll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᩬ"): bstack1llllll_opy_ (u"࡛ࠥࡪࡸࡣ࡬ࡧࡵࠦᩭ"),
            bstack1llllll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᩮ"): env.get(bstack1llllll_opy_ (u"ࠧ࡝ࡅࡓࡅࡎࡉࡗࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤᩯ")),
            bstack1llllll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᩰ"): bstack1llllll_opy_ (u"ࠢࡎࡣ࡬ࡲࠥࡖࡩࡱࡧ࡯࡭ࡳ࡫ࠢᩱ") if env.get(bstack1llllll_opy_ (u"࡙ࠣࡈࡖࡈࡑࡅࡓࡡࡐࡅࡎࡔ࡟ࡑࡋࡓࡉࡑࡏࡎࡆࡡࡖࡘࡆࡘࡔࡆࡆࠥᩲ")) else None,
            bstack1llllll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᩳ"): env.get(bstack1llllll_opy_ (u"࡛ࠥࡊࡘࡃࡌࡇࡕࡣࡌࡏࡔࡠࡅࡒࡑࡒࡏࡔࠣᩴ"))
        }
    if any([env.get(bstack1llllll_opy_ (u"ࠦࡌࡉࡐࡠࡒࡕࡓࡏࡋࡃࡕࠤ᩵")), env.get(bstack1llllll_opy_ (u"ࠧࡍࡃࡍࡑࡘࡈࡤࡖࡒࡐࡌࡈࡇ࡙ࠨ᩶")), env.get(bstack1llllll_opy_ (u"ࠨࡇࡐࡑࡊࡐࡊࡥࡃࡍࡑࡘࡈࡤࡖࡒࡐࡌࡈࡇ࡙ࠨ᩷"))]):
        return {
            bstack1llllll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ᩸"): bstack1llllll_opy_ (u"ࠣࡉࡲࡳ࡬ࡲࡥࠡࡅ࡯ࡳࡺࡪࠢ᩹"),
            bstack1llllll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ᩺"): None,
            bstack1llllll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ᩻"): env.get(bstack1llllll_opy_ (u"ࠦࡕࡘࡏࡋࡇࡆࡘࡤࡏࡄࠣ᩼")),
            bstack1llllll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ᩽"): env.get(bstack1llllll_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡏࡄࠣ᩾"))
        }
    if env.get(bstack1llllll_opy_ (u"ࠢࡔࡊࡌࡔࡕࡇࡂࡍࡇ᩿ࠥ")):
        return {
            bstack1llllll_opy_ (u"ࠣࡰࡤࡱࡪࠨ᪀"): bstack1llllll_opy_ (u"ࠤࡖ࡬࡮ࡶࡰࡢࡤ࡯ࡩࠧ᪁"),
            bstack1llllll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ᪂"): env.get(bstack1llllll_opy_ (u"ࠦࡘࡎࡉࡑࡒࡄࡆࡑࡋ࡟ࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥ᪃")),
            bstack1llllll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ᪄"): bstack1llllll_opy_ (u"ࠨࡊࡰࡤࠣࠧࢀࢃࠢ᪅").format(env.get(bstack1llllll_opy_ (u"ࠧࡔࡊࡌࡔࡕࡇࡂࡍࡇࡢࡎࡔࡈ࡟ࡊࡆࠪ᪆"))) if env.get(bstack1llllll_opy_ (u"ࠣࡕࡋࡍࡕࡖࡁࡃࡎࡈࡣࡏࡕࡂࡠࡋࡇࠦ᪇")) else None,
            bstack1llllll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ᪈"): env.get(bstack1llllll_opy_ (u"ࠥࡗࡍࡏࡐࡑࡃࡅࡐࡊࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧ᪉"))
        }
    if bstack11l1l1ll_opy_(env.get(bstack1llllll_opy_ (u"ࠦࡓࡋࡔࡍࡋࡉ࡝ࠧ᪊"))):
        return {
            bstack1llllll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ᪋"): bstack1llllll_opy_ (u"ࠨࡎࡦࡶ࡯࡭࡫ࡿࠢ᪌"),
            bstack1llllll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ᪍"): env.get(bstack1llllll_opy_ (u"ࠣࡆࡈࡔࡑࡕ࡙ࡠࡗࡕࡐࠧ᪎")),
            bstack1llllll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ᪏"): env.get(bstack1llllll_opy_ (u"ࠥࡗࡎ࡚ࡅࡠࡐࡄࡑࡊࠨ᪐")),
            bstack1llllll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ᪑"): env.get(bstack1llllll_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡎࡊࠢ᪒"))
        }
    if bstack11l1l1ll_opy_(env.get(bstack1llllll_opy_ (u"ࠨࡇࡊࡖࡋ࡙ࡇࡥࡁࡄࡖࡌࡓࡓ࡙ࠢ᪓"))):
        return {
            bstack1llllll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ᪔"): bstack1llllll_opy_ (u"ࠣࡉ࡬ࡸࡍࡻࡢࠡࡃࡦࡸ࡮ࡵ࡮ࡴࠤ᪕"),
            bstack1llllll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ᪖"): bstack1llllll_opy_ (u"ࠥࡿࢂ࠵ࡻࡾ࠱ࡤࡧࡹ࡯࡯࡯ࡵ࠲ࡶࡺࡴࡳ࠰ࡽࢀࠦ᪗").format(env.get(bstack1llllll_opy_ (u"ࠫࡌࡏࡔࡉࡗࡅࡣࡘࡋࡒࡗࡇࡕࡣ࡚ࡘࡌࠨ᪘")), env.get(bstack1llllll_opy_ (u"ࠬࡍࡉࡕࡊࡘࡆࡤࡘࡅࡑࡑࡖࡍ࡙ࡕࡒ࡚ࠩ᪙")), env.get(bstack1llllll_opy_ (u"࠭ࡇࡊࡖࡋ࡙ࡇࡥࡒࡖࡐࡢࡍࡉ࠭᪚"))),
            bstack1llllll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ᪛"): env.get(bstack1llllll_opy_ (u"ࠣࡉࡌࡘࡍ࡛ࡂࡠ࡙ࡒࡖࡐࡌࡌࡐ࡙ࠥ᪜")),
            bstack1llllll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ᪝"): env.get(bstack1llllll_opy_ (u"ࠥࡋࡎ࡚ࡈࡖࡄࡢࡖ࡚ࡔ࡟ࡊࡆࠥ᪞"))
        }
    if env.get(bstack1llllll_opy_ (u"ࠦࡈࡏࠢ᪟")) == bstack1llllll_opy_ (u"ࠧࡺࡲࡶࡧࠥ᪠") and env.get(bstack1llllll_opy_ (u"ࠨࡖࡆࡔࡆࡉࡑࠨ᪡")) == bstack1llllll_opy_ (u"ࠢ࠲ࠤ᪢"):
        return {
            bstack1llllll_opy_ (u"ࠣࡰࡤࡱࡪࠨ᪣"): bstack1llllll_opy_ (u"ࠤ࡙ࡩࡷࡩࡥ࡭ࠤ᪤"),
            bstack1llllll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ᪥"): bstack1llllll_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࢀࢃࠢ᪦").format(env.get(bstack1llllll_opy_ (u"ࠬ࡜ࡅࡓࡅࡈࡐࡤ࡛ࡒࡍࠩᪧ"))),
            bstack1llllll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ᪨"): None,
            bstack1llllll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ᪩"): None,
        }
    if env.get(bstack1llllll_opy_ (u"ࠣࡖࡈࡅࡒࡉࡉࡕ࡛ࡢ࡚ࡊࡘࡓࡊࡑࡑࠦ᪪")):
        return {
            bstack1llllll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᪫"): bstack1llllll_opy_ (u"ࠥࡘࡪࡧ࡭ࡤ࡫ࡷࡽࠧ᪬"),
            bstack1llllll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ᪭"): None,
            bstack1llllll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ᪮"): env.get(bstack1llllll_opy_ (u"ࠨࡔࡆࡃࡐࡇࡎ࡚࡙ࡠࡒࡕࡓࡏࡋࡃࡕࡡࡑࡅࡒࡋࠢ᪯")),
            bstack1llllll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ᪰"): env.get(bstack1llllll_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢ᪱"))
        }
    if any([env.get(bstack1llllll_opy_ (u"ࠤࡆࡓࡓࡉࡏࡖࡔࡖࡉࠧ᪲")), env.get(bstack1llllll_opy_ (u"ࠥࡇࡔࡔࡃࡐࡗࡕࡗࡊࡥࡕࡓࡎࠥ᪳")), env.get(bstack1llllll_opy_ (u"ࠦࡈࡕࡎࡄࡑࡘࡖࡘࡋ࡟ࡖࡕࡈࡖࡓࡇࡍࡆࠤ᪴")), env.get(bstack1llllll_opy_ (u"ࠧࡉࡏࡏࡅࡒ࡙ࡗ࡙ࡅࡠࡖࡈࡅࡒࠨ᪵"))]):
        return {
            bstack1llllll_opy_ (u"ࠨ࡮ࡢ࡯ࡨ᪶ࠦ"): bstack1llllll_opy_ (u"ࠢࡄࡱࡱࡧࡴࡻࡲࡴࡧ᪷ࠥ"),
            bstack1llllll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯᪸ࠦ"): None,
            bstack1llllll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨ᪹ࠦ"): env.get(bstack1llllll_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡍࡓࡇࡥࡎࡂࡏࡈ᪺ࠦ")) or None,
            bstack1llllll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ᪻"): env.get(bstack1llllll_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡎࡊࠢ᪼"), 0)
        }
    if env.get(bstack1llllll_opy_ (u"ࠨࡇࡐࡡࡍࡓࡇࡥࡎࡂࡏࡈ᪽ࠦ")):
        return {
            bstack1llllll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ᪾"): bstack1llllll_opy_ (u"ࠣࡉࡲࡇࡉࠨᪿ"),
            bstack1llllll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰᫀࠧ"): None,
            bstack1llllll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ᫁"): env.get(bstack1llllll_opy_ (u"ࠦࡌࡕ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤ᫂")),
            bstack1llllll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵ᫃ࠦ"): env.get(bstack1llllll_opy_ (u"ࠨࡇࡐࡡࡓࡍࡕࡋࡌࡊࡐࡈࡣࡈࡕࡕࡏࡖࡈࡖ᫄ࠧ"))
        }
    if env.get(bstack1llllll_opy_ (u"ࠢࡄࡈࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧ᫅")):
        return {
            bstack1llllll_opy_ (u"ࠣࡰࡤࡱࡪࠨ᫆"): bstack1llllll_opy_ (u"ࠤࡆࡳࡩ࡫ࡆࡳࡧࡶ࡬ࠧ᫇"),
            bstack1llllll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ᫈"): env.get(bstack1llllll_opy_ (u"ࠦࡈࡌ࡟ࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥ᫉")),
            bstack1llllll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫᫊ࠢ"): env.get(bstack1llllll_opy_ (u"ࠨࡃࡇࡡࡓࡍࡕࡋࡌࡊࡐࡈࡣࡓࡇࡍࡆࠤ᫋")),
            bstack1llllll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᫌ"): env.get(bstack1llllll_opy_ (u"ࠣࡅࡉࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࠨᫍ"))
        }
    return {bstack1llllll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᫎ"): None}
def get_host_info():
    return {
        bstack1llllll_opy_ (u"ࠥ࡬ࡴࡹࡴ࡯ࡣࡰࡩࠧ᫏"): platform.node(),
        bstack1llllll_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࠨ᫐"): platform.system(),
        bstack1llllll_opy_ (u"ࠧࡺࡹࡱࡧࠥ᫑"): platform.machine(),
        bstack1llllll_opy_ (u"ࠨࡶࡦࡴࡶ࡭ࡴࡴࠢ᫒"): platform.version(),
        bstack1llllll_opy_ (u"ࠢࡢࡴࡦ࡬ࠧ᫓"): platform.architecture()[0]
    }
def bstack11ll1l1l11_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack11ll11l1111_opy_():
    if bstack1l1ll1l1l1_opy_.get_property(bstack1llllll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩ᫔")):
        return bstack1llllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ᫕")
    return bstack1llllll_opy_ (u"ࠪࡹࡳࡱ࡮ࡰࡹࡱࡣ࡬ࡸࡩࡥࠩ᫖")
def bstack11l1l1ll11l_opy_(driver):
    info = {
        bstack1llllll_opy_ (u"ࠫࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪ᫗"): driver.capabilities,
        bstack1llllll_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠩ᫘"): driver.session_id,
        bstack1llllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧ᫙"): driver.capabilities.get(bstack1llllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ᫚"), None),
        bstack1llllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪ᫛"): driver.capabilities.get(bstack1llllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ᫜"), None),
        bstack1llllll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࠬ᫝"): driver.capabilities.get(bstack1llllll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠪ᫞"), None),
        bstack1llllll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ᫟"):driver.capabilities.get(bstack1llllll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ᫠"), None),
    }
    if bstack11ll11l1111_opy_() == bstack1llllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭᫡"):
        if bstack1111111ll_opy_():
            info[bstack1llllll_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࠩ᫢")] = bstack1llllll_opy_ (u"ࠩࡤࡴࡵ࠳ࡡࡶࡶࡲࡱࡦࡺࡥࠨ᫣")
        elif driver.capabilities.get(bstack1llllll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ᫤"), {}).get(bstack1llllll_opy_ (u"ࠫࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥࠨ᫥"), False):
            info[bstack1llllll_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹ࠭᫦")] = bstack1llllll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧࠪ᫧")
        else:
            info[bstack1llllll_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࠨ᫨")] = bstack1llllll_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪ᫩")
    return info
def bstack1111111ll_opy_():
    if bstack1l1ll1l1l1_opy_.get_property(bstack1llllll_opy_ (u"ࠩࡤࡴࡵࡥࡡࡶࡶࡲࡱࡦࡺࡥࠨ᫪")):
        return True
    if bstack11l1l1ll_opy_(os.environ.get(bstack1llllll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫ᫫"), None)):
        return True
    return False
def bstack1l1ll1111_opy_(bstack11l1ll11l11_opy_, url, data, config):
    headers = config.get(bstack1llllll_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬ᫬"), None)
    proxies = bstack11111111_opy_(config, url)
    auth = config.get(bstack1llllll_opy_ (u"ࠬࡧࡵࡵࡪࠪ᫭"), None)
    response = requests.request(
            bstack11l1ll11l11_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack1l1ll111ll_opy_(bstack1ll1l11lll_opy_, size):
    bstack111l1l11_opy_ = []
    while len(bstack1ll1l11lll_opy_) > size:
        bstack1llllllll1_opy_ = bstack1ll1l11lll_opy_[:size]
        bstack111l1l11_opy_.append(bstack1llllllll1_opy_)
        bstack1ll1l11lll_opy_ = bstack1ll1l11lll_opy_[size:]
    bstack111l1l11_opy_.append(bstack1ll1l11lll_opy_)
    return bstack111l1l11_opy_
def bstack11l1ll1llll_opy_(message, bstack11l1ll111l1_opy_=False):
    os.write(1, bytes(message, bstack1llllll_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬ᫮")))
    os.write(1, bytes(bstack1llllll_opy_ (u"ࠧ࡝ࡰࠪ᫯"), bstack1llllll_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧ᫰")))
    if bstack11l1ll111l1_opy_:
        with open(bstack1llllll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠯ࡲ࠵࠶ࡿ࠭ࠨ᫱") + os.environ[bstack1llllll_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡈࡂࡕࡋࡉࡉࡥࡉࡅࠩ᫲")] + bstack1llllll_opy_ (u"ࠫ࠳ࡲ࡯ࡨࠩ᫳"), bstack1llllll_opy_ (u"ࠬࡧࠧ᫴")) as f:
            f.write(message + bstack1llllll_opy_ (u"࠭࡜࡯ࠩ᫵"))
def bstack1l1lllll1l1_opy_():
    return os.environ[bstack1llllll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪ᫶")].lower() == bstack1llllll_opy_ (u"ࠨࡶࡵࡹࡪ࠭᫷")
def bstack111111ll1_opy_(bstack11l1l1ll1l1_opy_):
    return bstack1llllll_opy_ (u"ࠩࡾࢁ࠴ࢁࡽࠨ᫸").format(bstack11ll1ll111l_opy_, bstack11l1l1ll1l1_opy_)
def bstack1l11l1l11l_opy_():
    return bstack111l1l1l11_opy_().replace(tzinfo=None).isoformat() + bstack1llllll_opy_ (u"ࠪ࡞ࠬ᫹")
def bstack11l1l1l1ll1_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack1llllll_opy_ (u"ࠫ࡟࠭᫺"))) - datetime.datetime.fromisoformat(start.rstrip(bstack1llllll_opy_ (u"ࠬࡠࠧ᫻")))).total_seconds() * 1000
def bstack11l1l1l1l11_opy_(timestamp):
    return bstack11l1llll1ll_opy_(timestamp).isoformat() + bstack1llllll_opy_ (u"࡚࠭ࠨ᫼")
def bstack11l1ll11ll1_opy_(bstack11l1ll1111l_opy_):
    date_format = bstack1llllll_opy_ (u"࡛ࠧࠦࠨࡱࠪࡪࠠࠦࡊ࠽ࠩࡒࡀࠥࡔ࠰ࠨࡪࠬ᫽")
    bstack11ll11111l1_opy_ = datetime.datetime.strptime(bstack11l1ll1111l_opy_, date_format)
    return bstack11ll11111l1_opy_.isoformat() + bstack1llllll_opy_ (u"ࠨ࡜ࠪ᫾")
def bstack11l1l111ll1_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack1llllll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ᫿")
    else:
        return bstack1llllll_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᬀ")
def bstack11l1l1ll_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack1llllll_opy_ (u"ࠫࡹࡸࡵࡦࠩᬁ")
def bstack11ll11ll1ll_opy_(val):
    return val.__str__().lower() == bstack1llllll_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫᬂ")
def bstack111l1l1111_opy_(bstack11l1l11ll11_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack11l1l11ll11_opy_ as e:
                print(bstack1llllll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࡼࡿࠣ࠱ࡃࠦࡻࡾ࠼ࠣࡿࢂࠨᬃ").format(func.__name__, bstack11l1l11ll11_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack11l1l1l1l1l_opy_(bstack11ll11l1ll1_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack11ll11l1ll1_opy_(cls, *args, **kwargs)
            except bstack11l1l11ll11_opy_ as e:
                print(bstack1llllll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠡࡽࢀࠤ࠲ࡄࠠࡼࡿ࠽ࠤࢀࢃࠢᬄ").format(bstack11ll11l1ll1_opy_.__name__, bstack11l1l11ll11_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack11l1l1l1l1l_opy_
    else:
        return decorator
def bstack1l1ll1lll_opy_(bstack1111ll1ll1_opy_):
    if os.getenv(bstack1llllll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫᬅ")) is not None:
        return bstack11l1l1ll_opy_(os.getenv(bstack1llllll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠬᬆ")))
    if bstack1llllll_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᬇ") in bstack1111ll1ll1_opy_ and bstack11ll11ll1ll_opy_(bstack1111ll1ll1_opy_[bstack1llllll_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᬈ")]):
        return False
    if bstack1llllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᬉ") in bstack1111ll1ll1_opy_ and bstack11ll11ll1ll_opy_(bstack1111ll1ll1_opy_[bstack1llllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᬊ")]):
        return False
    return True
def bstack11l1ll1l11_opy_():
    try:
        from pytest_bdd import reporting
        bstack11l11lll111_opy_ = os.environ.get(bstack1llllll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡕࡔࡇࡕࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠢᬋ"), None)
        return bstack11l11lll111_opy_ is None or bstack11l11lll111_opy_ == bstack1llllll_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠧᬌ")
    except Exception as e:
        return False
def bstack1l1l1ll11_opy_(hub_url, CONFIG):
    if bstack1llll1ll1_opy_() <= version.parse(bstack1llllll_opy_ (u"ࠩ࠶࠲࠶࠹࠮࠱ࠩᬍ")):
        if hub_url:
            return bstack1llllll_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦᬎ") + hub_url + bstack1llllll_opy_ (u"ࠦ࠿࠾࠰࠰ࡹࡧ࠳࡭ࡻࡢࠣᬏ")
        return bstack1l1l1111_opy_
    if hub_url:
        return bstack1llllll_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࠢᬐ") + hub_url + bstack1llllll_opy_ (u"ࠨ࠯ࡸࡦ࠲࡬ࡺࡨࠢᬑ")
    return bstack1l111111_opy_
def bstack11l1ll111ll_opy_():
    return isinstance(os.getenv(bstack1llllll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐ࡚ࡖࡈࡗ࡙ࡥࡐࡍࡗࡊࡍࡓ࠭ᬒ")), str)
def bstack11ll1l11l1_opy_(url):
    return urlparse(url).hostname
def bstack11llll1111_opy_(hostname):
    for bstack1l1llll11l_opy_ in bstack11l1llll1_opy_:
        regex = re.compile(bstack1l1llll11l_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack11l11llll11_opy_(bstack11l1l111l11_opy_, file_name, logger):
    bstack111l11l1l_opy_ = os.path.join(os.path.expanduser(bstack1llllll_opy_ (u"ࠨࢀࠪᬓ")), bstack11l1l111l11_opy_)
    try:
        if not os.path.exists(bstack111l11l1l_opy_):
            os.makedirs(bstack111l11l1l_opy_)
        file_path = os.path.join(os.path.expanduser(bstack1llllll_opy_ (u"ࠩࢁࠫᬔ")), bstack11l1l111l11_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack1llllll_opy_ (u"ࠪࡻࠬᬕ")):
                pass
            with open(file_path, bstack1llllll_opy_ (u"ࠦࡼ࠱ࠢᬖ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack11l1l1111l_opy_.format(str(e)))
def bstack11l1lll11l1_opy_(file_name, key, value, logger):
    file_path = bstack11l11llll11_opy_(bstack1llllll_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬᬗ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1ll111llll_opy_ = json.load(open(file_path, bstack1llllll_opy_ (u"࠭ࡲࡣࠩᬘ")))
        else:
            bstack1ll111llll_opy_ = {}
        bstack1ll111llll_opy_[key] = value
        with open(file_path, bstack1llllll_opy_ (u"ࠢࡸ࠭ࠥᬙ")) as outfile:
            json.dump(bstack1ll111llll_opy_, outfile)
def bstack1llll1ll_opy_(file_name, logger):
    file_path = bstack11l11llll11_opy_(bstack1llllll_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨᬚ"), file_name, logger)
    bstack1ll111llll_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack1llllll_opy_ (u"ࠩࡵࠫᬛ")) as bstack11l11111l_opy_:
            bstack1ll111llll_opy_ = json.load(bstack11l11111l_opy_)
    return bstack1ll111llll_opy_
def bstack1l1ll11l11_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack1llllll_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡪࡥ࡭ࡧࡷ࡭ࡳ࡭ࠠࡧ࡫࡯ࡩ࠿ࠦࠧᬜ") + file_path + bstack1llllll_opy_ (u"ࠫࠥ࠭ᬝ") + str(e))
def bstack1llll1ll1_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack1llllll_opy_ (u"ࠧࡂࡎࡐࡖࡖࡉ࡙ࡄࠢᬞ")
def bstack1ll11ll1l_opy_(config):
    if bstack1llllll_opy_ (u"࠭ࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬᬟ") in config:
        del (config[bstack1llllll_opy_ (u"ࠧࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ᬠ")])
        return False
    if bstack1llll1ll1_opy_() < version.parse(bstack1llllll_opy_ (u"ࠨ࠵࠱࠸࠳࠶ࠧᬡ")):
        return False
    if bstack1llll1ll1_opy_() >= version.parse(bstack1llllll_opy_ (u"ࠩ࠷࠲࠶࠴࠵ࠨᬢ")):
        return True
    if bstack1llllll_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪᬣ") in config and config[bstack1llllll_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫᬤ")] is False:
        return False
    else:
        return True
def bstack11ll1llll1_opy_(args_list, bstack11ll111l111_opy_):
    index = -1
    for value in bstack11ll111l111_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack111llll1l1_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack111llll1l1_opy_ = bstack111llll1l1_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack1llllll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᬥ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack1llllll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᬦ"), exception=exception)
    def bstack1111l1llll_opy_(self):
        if self.result != bstack1llllll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᬧ"):
            return None
        if isinstance(self.exception_type, str) and bstack1llllll_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࠦᬨ") in self.exception_type:
            return bstack1llllll_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࡊࡸࡲࡰࡴࠥᬩ")
        return bstack1llllll_opy_ (u"࡙ࠥࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠦᬪ")
    def bstack11l1l11ll1l_opy_(self):
        if self.result != bstack1llllll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᬫ"):
            return None
        if self.bstack111llll1l1_opy_:
            return self.bstack111llll1l1_opy_
        return bstack11l1ll1ll1l_opy_(self.exception)
def bstack11l1ll1ll1l_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack11ll11ll11l_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack1lll11l1_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack1l1llll1l1_opy_(config, logger):
    try:
        import playwright
        bstack11l1ll1l1ll_opy_ = playwright.__file__
        bstack11l1l1l1lll_opy_ = os.path.split(bstack11l1ll1l1ll_opy_)
        bstack11l1l1l11l1_opy_ = bstack11l1l1l1lll_opy_[0] + bstack1llllll_opy_ (u"ࠬ࠵ࡤࡳ࡫ࡹࡩࡷ࠵ࡰࡢࡥ࡮ࡥ࡬࡫࠯࡭࡫ࡥ࠳ࡨࡲࡩ࠰ࡥ࡯࡭࠳ࡰࡳࠨᬬ")
        os.environ[bstack1llllll_opy_ (u"࠭ࡇࡍࡑࡅࡅࡑࡥࡁࡈࡇࡑࡘࡤࡎࡔࡕࡒࡢࡔࡗࡕࡘ࡚ࠩᬭ")] = bstack1l111ll11l_opy_(config)
        with open(bstack11l1l1l11l1_opy_, bstack1llllll_opy_ (u"ࠧࡳࠩᬮ")) as f:
            bstack1ll111l1l_opy_ = f.read()
            bstack11l1l111l1l_opy_ = bstack1llllll_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬࠮ࡣࡪࡩࡳࡺࠧᬯ")
            bstack11ll111lll1_opy_ = bstack1ll111l1l_opy_.find(bstack11l1l111l1l_opy_)
            if bstack11ll111lll1_opy_ == -1:
              process = subprocess.Popen(bstack1llllll_opy_ (u"ࠤࡱࡴࡲࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡨ࡮ࡲࡦࡦࡲ࠭ࡢࡩࡨࡲࡹࠨᬰ"), shell=True, cwd=bstack11l1l1l1lll_opy_[0])
              process.wait()
              bstack11ll11ll1l1_opy_ = bstack1llllll_opy_ (u"ࠪࠦࡺࡹࡥࠡࡵࡷࡶ࡮ࡩࡴࠣ࠽ࠪᬱ")
              bstack11ll1111l11_opy_ = bstack1llllll_opy_ (u"ࠦࠧࠨࠠ࡝ࠤࡸࡷࡪࠦࡳࡵࡴ࡬ࡧࡹࡢࠢ࠼ࠢࡦࡳࡳࡹࡴࠡࡽࠣࡦࡴࡵࡴࡴࡶࡵࡥࡵࠦࡽࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࠬ࡭࡬ࡰࡤࡤࡰ࠲ࡧࡧࡦࡰࡷࠫ࠮ࡁࠠࡪࡨࠣࠬࡵࡸ࡯ࡤࡧࡶࡷ࠳࡫࡮ࡷ࠰ࡊࡐࡔࡈࡁࡍࡡࡄࡋࡊࡔࡔࡠࡊࡗࡘࡕࡥࡐࡓࡑ࡛࡝࠮ࠦࡢࡰࡱࡷࡷࡹࡸࡡࡱࠪࠬ࠿ࠥࠨࠢࠣᬲ")
              bstack11l1l1lll11_opy_ = bstack1ll111l1l_opy_.replace(bstack11ll11ll1l1_opy_, bstack11ll1111l11_opy_)
              with open(bstack11l1l1l11l1_opy_, bstack1llllll_opy_ (u"ࠬࡽࠧᬳ")) as f:
                f.write(bstack11l1l1lll11_opy_)
    except Exception as e:
        logger.error(bstack11l1lll1ll_opy_.format(str(e)))
def bstack11111ll1l_opy_():
  try:
    bstack11l1ll1ll11_opy_ = os.path.join(tempfile.gettempdir(), bstack1llllll_opy_ (u"࠭࡯ࡱࡶ࡬ࡱࡦࡲ࡟ࡩࡷࡥࡣࡺࡸ࡬࠯࡬ࡶࡳࡳ᬴࠭"))
    bstack11l1lll1ll1_opy_ = []
    if os.path.exists(bstack11l1ll1ll11_opy_):
      with open(bstack11l1ll1ll11_opy_) as f:
        bstack11l1lll1ll1_opy_ = json.load(f)
      os.remove(bstack11l1ll1ll11_opy_)
    return bstack11l1lll1ll1_opy_
  except:
    pass
  return []
def bstack11lll1ll11_opy_(bstack111ll1ll1_opy_):
  try:
    bstack11l1lll1ll1_opy_ = []
    bstack11l1ll1ll11_opy_ = os.path.join(tempfile.gettempdir(), bstack1llllll_opy_ (u"ࠧࡰࡲࡷ࡭ࡲࡧ࡬ࡠࡪࡸࡦࡤࡻࡲ࡭࠰࡭ࡷࡴࡴࠧᬵ"))
    if os.path.exists(bstack11l1ll1ll11_opy_):
      with open(bstack11l1ll1ll11_opy_) as f:
        bstack11l1lll1ll1_opy_ = json.load(f)
    bstack11l1lll1ll1_opy_.append(bstack111ll1ll1_opy_)
    with open(bstack11l1ll1ll11_opy_, bstack1llllll_opy_ (u"ࠨࡹࠪᬶ")) as f:
        json.dump(bstack11l1lll1ll1_opy_, f)
  except:
    pass
def bstack1l1111111l_opy_(logger, bstack11l1lllll1l_opy_ = False):
  try:
    test_name = os.environ.get(bstack1llllll_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕࡡࡗࡉࡘ࡚࡟ࡏࡃࡐࡉࠬᬷ"), bstack1llllll_opy_ (u"ࠪࠫᬸ"))
    if test_name == bstack1llllll_opy_ (u"ࠫࠬᬹ"):
        test_name = threading.current_thread().__dict__.get(bstack1llllll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡇࡪࡤࡠࡶࡨࡷࡹࡥ࡮ࡢ࡯ࡨࠫᬺ"), bstack1llllll_opy_ (u"࠭ࠧᬻ"))
    bstack11ll111l11l_opy_ = bstack1llllll_opy_ (u"ࠧ࠭ࠢࠪᬼ").join(threading.current_thread().bstackTestErrorMessages)
    if bstack11l1lllll1l_opy_:
        bstack1ll111ll11_opy_ = os.environ.get(bstack1llllll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨᬽ"), bstack1llllll_opy_ (u"ࠩ࠳ࠫᬾ"))
        bstack1ll11l1l1_opy_ = {bstack1llllll_opy_ (u"ࠪࡲࡦࡳࡥࠨᬿ"): test_name, bstack1llllll_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᭀ"): bstack11ll111l11l_opy_, bstack1llllll_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫᭁ"): bstack1ll111ll11_opy_}
        bstack11l1lll111l_opy_ = []
        bstack11l1lll1l1l_opy_ = os.path.join(tempfile.gettempdir(), bstack1llllll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡰࡱࡲࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬᭂ"))
        if os.path.exists(bstack11l1lll1l1l_opy_):
            with open(bstack11l1lll1l1l_opy_) as f:
                bstack11l1lll111l_opy_ = json.load(f)
        bstack11l1lll111l_opy_.append(bstack1ll11l1l1_opy_)
        with open(bstack11l1lll1l1l_opy_, bstack1llllll_opy_ (u"ࠧࡸࠩᭃ")) as f:
            json.dump(bstack11l1lll111l_opy_, f)
    else:
        bstack1ll11l1l1_opy_ = {bstack1llllll_opy_ (u"ࠨࡰࡤࡱࡪ᭄࠭"): test_name, bstack1llllll_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨᭅ"): bstack11ll111l11l_opy_, bstack1llllll_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩᭆ"): str(multiprocessing.current_process().name)}
        if bstack1llllll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴࠨᭇ") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack1ll11l1l1_opy_)
  except Exception as e:
      logger.warn(bstack1llllll_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡳࡷ࡫ࠠࡱࡻࡷࡩࡸࡺࠠࡧࡷࡱࡲࡪࡲࠠࡥࡣࡷࡥ࠿ࠦࡻࡾࠤᭈ").format(e))
def bstack1l111l1l_opy_(error_message, test_name, index, logger):
  try:
    bstack11l1l11lll1_opy_ = []
    bstack1ll11l1l1_opy_ = {bstack1llllll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᭉ"): test_name, bstack1llllll_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ᭊ"): error_message, bstack1llllll_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧᭋ"): index}
    bstack11ll1111l1l_opy_ = os.path.join(tempfile.gettempdir(), bstack1llllll_opy_ (u"ࠩࡵࡳࡧࡵࡴࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰࠪᭌ"))
    if os.path.exists(bstack11ll1111l1l_opy_):
        with open(bstack11ll1111l1l_opy_) as f:
            bstack11l1l11lll1_opy_ = json.load(f)
    bstack11l1l11lll1_opy_.append(bstack1ll11l1l1_opy_)
    with open(bstack11ll1111l1l_opy_, bstack1llllll_opy_ (u"ࠪࡻࠬ᭍")) as f:
        json.dump(bstack11l1l11lll1_opy_, f)
  except Exception as e:
    logger.warn(bstack1llllll_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡶࡲࡶࡪࠦࡲࡰࡤࡲࡸࠥ࡬ࡵ࡯ࡰࡨࡰࠥࡪࡡࡵࡣ࠽ࠤࢀࢃࠢ᭎").format(e))
def bstack1l11llll11_opy_(bstack111111l1l_opy_, name, logger):
  try:
    bstack1ll11l1l1_opy_ = {bstack1llllll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ᭏"): name, bstack1llllll_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ᭐"): bstack111111l1l_opy_, bstack1llllll_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭᭑"): str(threading.current_thread()._name)}
    return bstack1ll11l1l1_opy_
  except Exception as e:
    logger.warn(bstack1llllll_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺ࡯ࡳࡧࠣࡦࡪ࡮ࡡࡷࡧࠣࡪࡺࡴ࡮ࡦ࡮ࠣࡨࡦࡺࡡ࠻ࠢࡾࢁࠧ᭒").format(e))
  return
def bstack11l1ll1l11l_opy_():
    return platform.system() == bstack1llllll_opy_ (u"࡚ࠩ࡭ࡳࡪ࡯ࡸࡵࠪ᭓")
def bstack11llll11l1_opy_(bstack11l1ll1l1l1_opy_, config, logger):
    bstack11l1l1111l1_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack11l1ll1l1l1_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack1llllll_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡪ࡮ࡷࡩࡷࠦࡣࡰࡰࡩ࡭࡬ࠦ࡫ࡦࡻࡶࠤࡧࡿࠠࡳࡧࡪࡩࡽࠦ࡭ࡢࡶࡦ࡬࠿ࠦࡻࡾࠤ᭔").format(e))
    return bstack11l1l1111l1_opy_
def bstack11l1llll1l1_opy_(bstack11ll11ll111_opy_, bstack11ll111ll11_opy_):
    bstack11l1ll1lll1_opy_ = version.parse(bstack11ll11ll111_opy_)
    bstack11l1l1l111l_opy_ = version.parse(bstack11ll111ll11_opy_)
    if bstack11l1ll1lll1_opy_ > bstack11l1l1l111l_opy_:
        return 1
    elif bstack11l1ll1lll1_opy_ < bstack11l1l1l111l_opy_:
        return -1
    else:
        return 0
def bstack111l1l1l11_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack11l1llll1ll_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
def bstack11l1l11l111_opy_(framework):
    from browserstack_sdk._version import __version__
    return str(framework) + str(__version__)
def bstack111l1111l_opy_(options, framework, bstack1lll1l1l1_opy_={}):
    if options is None:
        return
    if getattr(options, bstack1llllll_opy_ (u"ࠫ࡬࡫ࡴࠨ᭕"), None):
        caps = options
    else:
        caps = options.to_capabilities()
    bstack111l1111_opy_ = caps.get(bstack1llllll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭᭖"))
    bstack11ll1111ll1_opy_ = True
    bstack11ll11l1_opy_ = os.environ[bstack1llllll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ᭗")]
    if bstack11ll11ll1ll_opy_(caps.get(bstack1llllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡵࡴࡧ࡚࠷ࡈ࠭᭘"))) or bstack11ll11ll1ll_opy_(caps.get(bstack1llllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡶࡵࡨࡣࡼ࠹ࡣࠨ᭙"))):
        bstack11ll1111ll1_opy_ = False
    if bstack1ll11ll1l_opy_({bstack1llllll_opy_ (u"ࠤࡸࡷࡪ࡝࠳ࡄࠤ᭚"): bstack11ll1111ll1_opy_}):
        bstack111l1111_opy_ = bstack111l1111_opy_ or {}
        bstack111l1111_opy_[bstack1llllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬ᭛")] = bstack11l1l11l111_opy_(framework)
        bstack111l1111_opy_[bstack1llllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭᭜")] = bstack1l1lllll1l1_opy_()
        bstack111l1111_opy_[bstack1llllll_opy_ (u"ࠬࡺࡥࡴࡶ࡫ࡹࡧࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨ᭝")] = bstack11ll11l1_opy_
        bstack111l1111_opy_[bstack1llllll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨ᭞")] = bstack1lll1l1l1_opy_
        if getattr(options, bstack1llllll_opy_ (u"ࠧࡴࡧࡷࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡹࠨ᭟"), None):
            options.set_capability(bstack1llllll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ᭠"), bstack111l1111_opy_)
        else:
            options[bstack1llllll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪ᭡")] = bstack111l1111_opy_
    else:
        if getattr(options, bstack1llllll_opy_ (u"ࠪࡷࡪࡺ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶࡼࠫ᭢"), None):
            options.set_capability(bstack1llllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬ᭣"), bstack11l1l11l111_opy_(framework))
            options.set_capability(bstack1llllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭᭤"), bstack1l1lllll1l1_opy_())
            options.set_capability(bstack1llllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡺࡥࡴࡶ࡫ࡹࡧࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨ᭥"), bstack11ll11l1_opy_)
            options.set_capability(bstack1llllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨ᭦"), bstack1lll1l1l1_opy_)
        else:
            options[bstack1llllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩ᭧")] = bstack11l1l11l111_opy_(framework)
            options[bstack1llllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪ᭨")] = bstack1l1lllll1l1_opy_()
            options[bstack1llllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷࡩࡸࡺࡨࡶࡤࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬ᭩")] = bstack11ll11l1_opy_
            options[bstack1llllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬ᭪")] = bstack1lll1l1l1_opy_
    return options
def bstack11ll1111111_opy_(bstack11l1lll1l11_opy_, framework):
    bstack1lll1l1l1_opy_ = bstack1l1ll1l1l1_opy_.get_property(bstack1llllll_opy_ (u"ࠧࡖࡌࡂ࡛࡚ࡖࡎࡍࡈࡕࡡࡓࡖࡔࡊࡕࡄࡖࡢࡑࡆࡖࠢ᭫"))
    if bstack11l1lll1l11_opy_ and len(bstack11l1lll1l11_opy_.split(bstack1llllll_opy_ (u"࠭ࡣࡢࡲࡶࡁ᭬ࠬ"))) > 1:
        ws_url = bstack11l1lll1l11_opy_.split(bstack1llllll_opy_ (u"ࠧࡤࡣࡳࡷࡂ࠭᭭"))[0]
        if bstack1llllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫ᭮") in ws_url:
            from browserstack_sdk._version import __version__
            bstack11l11llll1l_opy_ = json.loads(urllib.parse.unquote(bstack11l1lll1l11_opy_.split(bstack1llllll_opy_ (u"ࠩࡦࡥࡵࡹ࠽ࠨ᭯"))[1]))
            bstack11l11llll1l_opy_ = bstack11l11llll1l_opy_ or {}
            bstack11ll11l1_opy_ = os.environ[bstack1llllll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ᭰")]
            bstack11l11llll1l_opy_[bstack1llllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬ᭱")] = str(framework) + str(__version__)
            bstack11l11llll1l_opy_[bstack1llllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭᭲")] = bstack1l1lllll1l1_opy_()
            bstack11l11llll1l_opy_[bstack1llllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡺࡥࡴࡶ࡫ࡹࡧࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨ᭳")] = bstack11ll11l1_opy_
            bstack11l11llll1l_opy_[bstack1llllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨ᭴")] = bstack1lll1l1l1_opy_
            bstack11l1lll1l11_opy_ = bstack11l1lll1l11_opy_.split(bstack1llllll_opy_ (u"ࠨࡥࡤࡴࡸࡃࠧ᭵"))[0] + bstack1llllll_opy_ (u"ࠩࡦࡥࡵࡹ࠽ࠨ᭶") + urllib.parse.quote(json.dumps(bstack11l11llll1l_opy_))
    return bstack11l1lll1l11_opy_
def bstack1ll1lll111_opy_():
    global bstack1ll11ll11_opy_
    from playwright._impl._browser_type import BrowserType
    bstack1ll11ll11_opy_ = BrowserType.connect
    return bstack1ll11ll11_opy_
def bstack1111ll1ll_opy_(framework_name):
    global bstack1ll11ll1l1_opy_
    bstack1ll11ll1l1_opy_ = framework_name
    return framework_name
def bstack1l11ll11l1_opy_(self, *args, **kwargs):
    global bstack1ll11ll11_opy_
    try:
        global bstack1ll11ll1l1_opy_
        if bstack1llllll_opy_ (u"ࠪࡻࡸࡋ࡮ࡥࡲࡲ࡭ࡳࡺࠧ᭷") in kwargs:
            kwargs[bstack1llllll_opy_ (u"ࠫࡼࡹࡅ࡯ࡦࡳࡳ࡮ࡴࡴࠨ᭸")] = bstack11ll1111111_opy_(
                kwargs.get(bstack1llllll_opy_ (u"ࠬࡽࡳࡆࡰࡧࡴࡴ࡯࡮ࡵࠩ᭹"), None),
                bstack1ll11ll1l1_opy_
            )
    except Exception as e:
        logger.error(bstack1llllll_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡦࡰࠣࡴࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡔࡆࡎࠤࡨࡧࡰࡴ࠼ࠣࡿࢂࠨ᭺").format(str(e)))
    return bstack1ll11ll11_opy_(self, *args, **kwargs)
def bstack11l11lllll1_opy_(bstack11l1l111111_opy_, proxies):
    proxy_settings = {}
    try:
        if not proxies:
            proxies = bstack11111111_opy_(bstack11l1l111111_opy_, bstack1llllll_opy_ (u"ࠢࠣ᭻"))
        if proxies and proxies.get(bstack1llllll_opy_ (u"ࠣࡪࡷࡸࡵࡹࠢ᭼")):
            parsed_url = urlparse(proxies.get(bstack1llllll_opy_ (u"ࠤ࡫ࡸࡹࡶࡳࠣ᭽")))
            if parsed_url and parsed_url.hostname: proxy_settings[bstack1llllll_opy_ (u"ࠪࡴࡷࡵࡸࡺࡊࡲࡷࡹ࠭᭾")] = str(parsed_url.hostname)
            if parsed_url and parsed_url.port: proxy_settings[bstack1llllll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡓࡳࡷࡺࠧ᭿")] = str(parsed_url.port)
            if parsed_url and parsed_url.username: proxy_settings[bstack1llllll_opy_ (u"ࠬࡶࡲࡰࡺࡼ࡙ࡸ࡫ࡲࠨᮀ")] = str(parsed_url.username)
            if parsed_url and parsed_url.password: proxy_settings[bstack1llllll_opy_ (u"࠭ࡰࡳࡱࡻࡽࡕࡧࡳࡴࠩᮁ")] = str(parsed_url.password)
        return proxy_settings
    except:
        return proxy_settings
def bstack1lllll11ll_opy_(bstack11l1l111111_opy_):
    bstack11ll11l1lll_opy_ = {
        bstack11ll1l1111l_opy_[bstack11l1l11llll_opy_]: bstack11l1l111111_opy_[bstack11l1l11llll_opy_]
        for bstack11l1l11llll_opy_ in bstack11l1l111111_opy_
        if bstack11l1l11llll_opy_ in bstack11ll1l1111l_opy_
    }
    bstack11ll11l1lll_opy_[bstack1llllll_opy_ (u"ࠢࡱࡴࡲࡼࡾ࡙ࡥࡵࡶ࡬ࡲ࡬ࡹࠢᮂ")] = bstack11l11lllll1_opy_(bstack11l1l111111_opy_, bstack1l1ll1l1l1_opy_.get_property(bstack1llllll_opy_ (u"ࠣࡲࡵࡳࡽࡿࡓࡦࡶࡷ࡭ࡳ࡭ࡳࠣᮃ")))
    bstack11ll11l11ll_opy_ = [element.lower() for element in bstack11ll1lllll1_opy_]
    bstack11ll111llll_opy_(bstack11ll11l1lll_opy_, bstack11ll11l11ll_opy_)
    return bstack11ll11l1lll_opy_
def bstack11ll111llll_opy_(d, keys):
    for key in list(d.keys()):
        if key.lower() in keys:
            d[key] = bstack1llllll_opy_ (u"ࠤ࠭࠮࠯࠰ࠢᮄ")
    for value in d.values():
        if isinstance(value, dict):
            bstack11ll111llll_opy_(value, keys)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    bstack11ll111llll_opy_(item, keys)
def bstack1l1llll1111_opy_():
    bstack11l1ll1l111_opy_ = [os.environ.get(bstack1llllll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡍࡑࡋࡓࡠࡆࡌࡖࠧᮅ")), os.path.join(os.path.expanduser(bstack1llllll_opy_ (u"ࠦࢃࠨᮆ")), bstack1llllll_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬᮇ")), os.path.join(bstack1llllll_opy_ (u"࠭࠯ࡵ࡯ࡳࠫᮈ"), bstack1llllll_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧᮉ"))]
    for path in bstack11l1ll1l111_opy_:
        if path is None:
            continue
        try:
            if os.path.exists(path):
                logger.debug(bstack1llllll_opy_ (u"ࠣࡈ࡬ࡰࡪࠦࠧࠣᮊ") + str(path) + bstack1llllll_opy_ (u"ࠤࠪࠤࡪࡾࡩࡴࡶࡶ࠲ࠧᮋ"))
                if not os.access(path, os.W_OK):
                    logger.debug(bstack1llllll_opy_ (u"ࠥࡋ࡮ࡼࡩ࡯ࡩࠣࡴࡪࡸ࡭ࡪࡵࡶ࡭ࡴࡴࡳࠡࡨࡲࡶࠥ࠭ࠢᮌ") + str(path) + bstack1llllll_opy_ (u"ࠦࠬࠨᮍ"))
                    os.chmod(path, 0o777)
                else:
                    logger.debug(bstack1llllll_opy_ (u"ࠧࡌࡩ࡭ࡧࠣࠫࠧᮎ") + str(path) + bstack1llllll_opy_ (u"ࠨࠧࠡࡣ࡯ࡶࡪࡧࡤࡺࠢ࡫ࡥࡸࠦࡴࡩࡧࠣࡶࡪࡷࡵࡪࡴࡨࡨࠥࡶࡥࡳ࡯࡬ࡷࡸ࡯࡯࡯ࡵ࠱ࠦᮏ"))
            else:
                logger.debug(bstack1llllll_opy_ (u"ࠢࡄࡴࡨࡥࡹ࡯࡮ࡨࠢࡩ࡭ࡱ࡫ࠠࠨࠤᮐ") + str(path) + bstack1llllll_opy_ (u"ࠣࠩࠣࡻ࡮ࡺࡨࠡࡹࡵ࡭ࡹ࡫ࠠࡱࡧࡵࡱ࡮ࡹࡳࡪࡱࡱ࠲ࠧᮑ"))
                os.makedirs(path, exist_ok=True)
                os.chmod(path, 0o777)
            logger.debug(bstack1llllll_opy_ (u"ࠤࡒࡴࡪࡸࡡࡵ࡫ࡲࡲࠥࡹࡵࡤࡥࡨࡩࡩ࡫ࡤࠡࡨࡲࡶࠥ࠭ࠢᮒ") + str(path) + bstack1llllll_opy_ (u"ࠥࠫ࠳ࠨᮓ"))
            return path
        except Exception as e:
            logger.debug(bstack1llllll_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࠤࡺࡶࠠࡧ࡫࡯ࡩࠥ࠭ࡻࡱࡣࡷ࡬ࢂ࠭࠺ࠡࠤᮔ") + str(e) + bstack1llllll_opy_ (u"ࠧࠨᮕ"))
    logger.debug(bstack1llllll_opy_ (u"ࠨࡁ࡭࡮ࠣࡴࡦࡺࡨࡴࠢࡩࡥ࡮ࡲࡥࡥ࠰ࠥᮖ"))
    return None
@measure(event_name=EVENTS.bstack11ll1ll1lll_opy_, stage=STAGE.bstack1l1ll11l1_opy_)
def bstack1ll1lllll11_opy_(binary_path, bstack1lll1l111ll_opy_, bs_config):
    logger.debug(bstack1llllll_opy_ (u"ࠢࡄࡷࡵࡶࡪࡴࡴࠡࡅࡏࡍࠥࡖࡡࡵࡪࠣࡪࡴࡻ࡮ࡥ࠼ࠣࡿࢂࠨᮗ").format(binary_path))
    bstack11l1llll11l_opy_ = bstack1llllll_opy_ (u"ࠨࠩᮘ")
    bstack11l1llllll1_opy_ = {
        bstack1llllll_opy_ (u"ࠩࡶࡨࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᮙ"): __version__,
        bstack1llllll_opy_ (u"ࠥࡳࡸࠨᮚ"): platform.system(),
        bstack1llllll_opy_ (u"ࠦࡴࡹ࡟ࡢࡴࡦ࡬ࠧᮛ"): platform.machine(),
        bstack1llllll_opy_ (u"ࠧࡩ࡬ࡪࡡࡹࡩࡷࡹࡩࡰࡰࠥᮜ"): bstack1llllll_opy_ (u"࠭࠰ࠨᮝ"),
        bstack1llllll_opy_ (u"ࠢࡴࡦ࡮ࡣࡱࡧ࡮ࡨࡷࡤ࡫ࡪࠨᮞ"): bstack1llllll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨᮟ")
    }
    bstack11ll11l11l1_opy_(bstack11l1llllll1_opy_)
    try:
        if binary_path:
            bstack11l1llllll1_opy_[bstack1llllll_opy_ (u"ࠩࡦࡰ࡮ࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᮠ")] = subprocess.check_output([binary_path, bstack1llllll_opy_ (u"ࠥࡺࡪࡸࡳࡪࡱࡱࠦᮡ")]).strip().decode(bstack1llllll_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪᮢ"))
        response = requests.request(
            bstack1llllll_opy_ (u"ࠬࡍࡅࡕࠩᮣ"),
            url=bstack111111ll1_opy_(bstack11ll11llll1_opy_),
            headers=None,
            auth=(bs_config[bstack1llllll_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨᮤ")], bs_config[bstack1llllll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪᮥ")]),
            json=None,
            params=bstack11l1llllll1_opy_
        )
        data = response.json()
        if response.status_code == 200 and bstack1llllll_opy_ (u"ࠨࡷࡵࡰࠬᮦ") in data.keys() and bstack1llllll_opy_ (u"ࠩࡸࡴࡩࡧࡴࡦࡦࡢࡧࡱ࡯࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᮧ") in data.keys():
            logger.debug(bstack1llllll_opy_ (u"ࠥࡒࡪ࡫ࡤࠡࡶࡲࠤࡺࡶࡤࡢࡶࡨࠤࡧ࡯࡮ࡢࡴࡼ࠰ࠥࡩࡵࡳࡴࡨࡲࡹࠦࡢࡪࡰࡤࡶࡾࠦࡶࡦࡴࡶ࡭ࡴࡴ࠺ࠡࡽࢀࠦᮨ").format(bstack11l1llllll1_opy_[bstack1llllll_opy_ (u"ࠫࡨࡲࡩࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᮩ")]))
            bstack11l1l11l1ll_opy_ = bstack11l1lll1111_opy_(data[bstack1llllll_opy_ (u"ࠬࡻࡲ࡭᮪ࠩ")], bstack1lll1l111ll_opy_)
            bstack11l1llll11l_opy_ = os.path.join(bstack1lll1l111ll_opy_, bstack11l1l11l1ll_opy_)
            os.chmod(bstack11l1llll11l_opy_, 0o777) # bstack11l11lll1l1_opy_ permission
            return bstack11l1llll11l_opy_
    except Exception as e:
        logger.debug(bstack1llllll_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡩࡵࡷ࡯࡮ࡲࡥࡩ࡯࡮ࡨࠢࡱࡩࡼࠦࡓࡅࡍࠣࡿࢂࠨ᮫").format(e))
    return binary_path
def bstack11ll11l11l1_opy_(bstack11l1llllll1_opy_):
    try:
        if bstack1llllll_opy_ (u"ࠧ࡭࡫ࡱࡹࡽ࠭ᮬ") not in bstack11l1llllll1_opy_[bstack1llllll_opy_ (u"ࠨࡱࡶࠫᮭ")].lower():
            return
        if os.path.exists(bstack1llllll_opy_ (u"ࠤ࠲ࡩࡹࡩ࠯ࡰࡵ࠰ࡶࡪࡲࡥࡢࡵࡨࠦᮮ")):
            with open(bstack1llllll_opy_ (u"ࠥ࠳ࡪࡺࡣ࠰ࡱࡶ࠱ࡷ࡫࡬ࡦࡣࡶࡩࠧᮯ"), bstack1llllll_opy_ (u"ࠦࡷࠨ᮰")) as f:
                bstack11ll11lll11_opy_ = {}
                for line in f:
                    if bstack1llllll_opy_ (u"ࠧࡃࠢ᮱") in line:
                        key, value = line.rstrip().split(bstack1llllll_opy_ (u"ࠨ࠽ࠣ᮲"), 1)
                        bstack11ll11lll11_opy_[key] = value.strip(bstack1llllll_opy_ (u"ࠧࠣ࡞ࠪࠫ᮳"))
                bstack11l1llllll1_opy_[bstack1llllll_opy_ (u"ࠨࡦ࡬ࡷࡹࡸ࡯ࠨ᮴")] = bstack11ll11lll11_opy_.get(bstack1llllll_opy_ (u"ࠤࡌࡈࠧ᮵"), bstack1llllll_opy_ (u"ࠥࠦ᮶"))
        elif os.path.exists(bstack1llllll_opy_ (u"ࠦ࠴࡫ࡴࡤ࠱ࡤࡰࡵ࡯࡮ࡦ࠯ࡵࡩࡱ࡫ࡡࡴࡧࠥ᮷")):
            bstack11l1llllll1_opy_[bstack1llllll_opy_ (u"ࠬࡪࡩࡴࡶࡵࡳࠬ᮸")] = bstack1llllll_opy_ (u"࠭ࡡ࡭ࡲ࡬ࡲࡪ࠭᮹")
    except Exception as e:
        logger.debug(bstack1llllll_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣ࡫ࡪࡺࠠࡥ࡫ࡶࡸࡷࡵࠠࡰࡨࠣࡰ࡮ࡴࡵࡹࠤᮺ") + e)
@measure(event_name=EVENTS.bstack11ll11lllll_opy_, stage=STAGE.bstack1l1ll11l1_opy_)
def bstack11l1lll1111_opy_(bstack11l1ll11lll_opy_, bstack11l1l11111l_opy_):
    logger.debug(bstack1llllll_opy_ (u"ࠣࡆࡲࡻࡳࡲ࡯ࡢࡦ࡬ࡲ࡬ࠦࡓࡅࡍࠣࡦ࡮ࡴࡡࡳࡻࠣࡪࡷࡵ࡭࠻ࠢࠥᮻ") + str(bstack11l1ll11lll_opy_) + bstack1llllll_opy_ (u"ࠤࠥᮼ"))
    zip_path = os.path.join(bstack11l1l11111l_opy_, bstack1llllll_opy_ (u"ࠥࡨࡴࡽ࡮࡭ࡱࡤࡨࡪࡪ࡟ࡧ࡫࡯ࡩ࠳ࢀࡩࡱࠤᮽ"))
    bstack11l1l11l1ll_opy_ = bstack1llllll_opy_ (u"ࠫࠬᮾ")
    with requests.get(bstack11l1ll11lll_opy_, stream=True) as response:
        response.raise_for_status()
        with open(zip_path, bstack1llllll_opy_ (u"ࠧࡽࡢࠣᮿ")) as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        logger.debug(bstack1llllll_opy_ (u"ࠨࡆࡪ࡮ࡨࠤࡩࡵࡷ࡯࡮ࡲࡥࡩ࡫ࡤࠡࡵࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࡱࡿ࠮ࠣᯀ"))
    with zipfile.ZipFile(zip_path, bstack1llllll_opy_ (u"ࠧࡳࠩᯁ")) as zip_ref:
        bstack11ll111111l_opy_ = zip_ref.namelist()
        if len(bstack11ll111111l_opy_) > 0:
            bstack11l1l11l1ll_opy_ = bstack11ll111111l_opy_[0] # bstack11ll111l1ll_opy_ bstack11ll1l1lll1_opy_ will be bstack11l1lllll11_opy_ 1 file i.e. the binary in the zip
        zip_ref.extractall(bstack11l1l11111l_opy_)
        logger.debug(bstack1llllll_opy_ (u"ࠣࡈ࡬ࡰࡪࡹࠠࡴࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࡰࡾࠦࡥࡹࡶࡵࡥࡨࡺࡥࡥࠢࡷࡳࠥ࠭ࠢᯂ") + str(bstack11l1l11111l_opy_) + bstack1llllll_opy_ (u"ࠤࠪࠦᯃ"))
    os.remove(zip_path)
    return bstack11l1l11l1ll_opy_
def get_cli_dir():
    bstack11l1l1l11ll_opy_ = bstack1l1llll1111_opy_()
    if bstack11l1l1l11ll_opy_:
        bstack1lll1l111ll_opy_ = os.path.join(bstack11l1l1l11ll_opy_, bstack1llllll_opy_ (u"ࠥࡧࡱ࡯ࠢᯄ"))
        if not os.path.exists(bstack1lll1l111ll_opy_):
            os.makedirs(bstack1lll1l111ll_opy_, mode=0o777, exist_ok=True)
        return bstack1lll1l111ll_opy_
    else:
        raise FileNotFoundError(bstack1llllll_opy_ (u"ࠦࡓࡵࠠࡸࡴ࡬ࡸࡦࡨ࡬ࡦࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥࡧࡶࡢ࡫࡯ࡥࡧࡲࡥࠡࡨࡲࡶࠥࡺࡨࡦࠢࡖࡈࡐࠦࡢࡪࡰࡤࡶࡾ࠴ࠢᯅ"))
def bstack1lll1ll11l1_opy_(bstack1lll1l111ll_opy_):
    bstack1llllll_opy_ (u"ࠧࠨࠢࡈࡧࡷࠤࡹ࡮ࡥࠡࡲࡤࡸ࡭ࠦࡦࡰࡴࠣࡸ࡭࡫ࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡓࡅࡍࠣࡦ࡮ࡴࡡࡳࡻࠣ࡭ࡳࠦࡡࠡࡹࡵ࡭ࡹࡧࡢ࡭ࡧࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾ࠴ࠢࠣࠤᯆ")
    bstack11ll111l1l1_opy_ = [
        os.path.join(bstack1lll1l111ll_opy_, f)
        for f in os.listdir(bstack1lll1l111ll_opy_)
        if os.path.isfile(os.path.join(bstack1lll1l111ll_opy_, f)) and f.startswith(bstack1llllll_opy_ (u"ࠨࡢࡪࡰࡤࡶࡾ࠳ࠢᯇ"))
    ]
    if len(bstack11ll111l1l1_opy_) > 0:
        return max(bstack11ll111l1l1_opy_, key=os.path.getmtime) # get bstack11ll11111ll_opy_ binary
    return bstack1llllll_opy_ (u"ࠢࠣᯈ")
def bstack1ll1l1lll11_opy_(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = bstack1ll1l1lll11_opy_(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d