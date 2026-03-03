# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll111_opy_ (bstack1l1l1l1_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l11_opy_ = ord (bstack1l1l1l1_opy_ [-1])
    bstack11l11l1_opy_ = bstack1l1l1l1_opy_ [:-1]
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ % len (bstack11l11l1_opy_)
    bstack1l1ll1l_opy_ = bstack11l11l1_opy_ [:bstack1ll1l1l_opy_] + bstack11l11l1_opy_ [bstack1ll1l1l_opy_:]
    if bstack1lll1l1_opy_:
        bstack11l1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    else:
        bstack11l1ll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    return eval (bstack11l1ll1_opy_)
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
from math import ceil
from unittest import result
import urllib
from urllib.parse import urlparse
import zipfile
import git
import requests
from packaging import version
from bstack_utils.config import Config
from bstack_utils.constants import (bstack1l1lllll11_opy_, bstack1l11l11l11_opy_, HTTPS_HUB,
                                    bstack111ll1ll11l_opy_, bstack111llll11ll_opy_, bstack111ll1l1l11_opy_, bstack111llll11l1_opy_)
from bstack_utils.measure import measure
from bstack_utils.messages import bstack11l11lll11_opy_, bstack1lll111111_opy_
from bstack_utils.proxy import bstack1111llll1l_opy_, bstack1111lllll1_opy_
from bstack_utils.constants import *
from bstack_utils import logger_utils
from bstack_utils.bstack11ll1l11l_opy_ import bstack1l1l1111ll_opy_
from browserstack_sdk._version import __version__
global_config = Config.get_instance()
logger = logger_utils.get_logger(__name__, logger_utils.bstack1ll1l11ll1l_opy_())
bstack1l1ll1ll11_opy_ = logger_utils.bstack11l1l11ll_opy_(__name__)
def bstack11l111ll1l1_opy_(config):
    return config[bstack11ll111_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩᴴ")]
def bstack11l11lll111_opy_(config):
    return config[bstack11ll111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫᴵ")]
def bstack1l1111lll1_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def is_robot_playwright_installed():
    try:
        import Browser
        return True
    except ImportError:
        return False
def bstack111l1ll11ll_opy_(obj):
    values = []
    bstack111l1lll1l1_opy_ = re.compile(bstack11ll111_opy_ (u"ࡴࠥࡢࡈ࡛ࡓࡕࡑࡐࡣ࡙ࡇࡇࡠ࡞ࡧ࠯ࠩࠨᴶ"), re.I)
    for key in obj.keys():
        if bstack111l1lll1l1_opy_.match(key):
            values.append(obj[key])
    return values
def bstack111l1llll1l_opy_(config):
    tags = []
    tags.extend(bstack111l1ll11ll_opy_(os.environ))
    tags.extend(bstack111l1ll11ll_opy_(config))
    return tags
def bstack1111l1ll1l1_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack1111l1l1111_opy_(bstack1111l1lllll_opy_):
    if not bstack1111l1lllll_opy_:
        return bstack11ll111_opy_ (u"ࠪࠫᴷ")
    return bstack11ll111_opy_ (u"ࠦࢀࢃࠠࠩࡽࢀ࠭ࠧᴸ").format(bstack1111l1lllll_opy_.name, bstack1111l1lllll_opy_.email)
def bstack11l11ll1111_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack1111ll11ll1_opy_ = repo.common_dir
        info = {
            bstack11ll111_opy_ (u"ࠧࡹࡨࡢࠤᴹ"): repo.head.commit.hexsha,
            bstack11ll111_opy_ (u"ࠨࡳࡩࡱࡵࡸࡤࡹࡨࡢࠤᴺ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack11ll111_opy_ (u"ࠢࡣࡴࡤࡲࡨ࡮ࠢᴻ"): repo.active_branch.name,
            bstack11ll111_opy_ (u"ࠣࡶࡤ࡫ࠧᴼ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack11ll111_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡶࡨࡶࠧᴽ"): bstack1111l1l1111_opy_(repo.head.commit.committer),
            bstack11ll111_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡷࡩࡷࡥࡤࡢࡶࡨࠦᴾ"): repo.head.commit.committed_datetime.isoformat(),
            bstack11ll111_opy_ (u"ࠦࡦࡻࡴࡩࡱࡵࠦᴿ"): bstack1111l1l1111_opy_(repo.head.commit.author),
            bstack11ll111_opy_ (u"ࠧࡧࡵࡵࡪࡲࡶࡤࡪࡡࡵࡧࠥᵀ"): repo.head.commit.authored_datetime.isoformat(),
            bstack11ll111_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡥ࡭ࡦࡵࡶࡥ࡬࡫ࠢᵁ"): repo.head.commit.message,
            bstack11ll111_opy_ (u"ࠢࡳࡱࡲࡸࠧᵂ"): repo.git.rev_parse(bstack11ll111_opy_ (u"ࠣ࠯࠰ࡷ࡭ࡵࡷ࠮ࡶࡲࡴࡱ࡫ࡶࡦ࡮ࠥᵃ")),
            bstack11ll111_opy_ (u"ࠤࡦࡳࡲࡳ࡯࡯ࡡࡪ࡭ࡹࡥࡤࡪࡴࠥᵄ"): bstack1111ll11ll1_opy_,
            bstack11ll111_opy_ (u"ࠥࡻࡴࡸ࡫ࡵࡴࡨࡩࡤ࡭ࡩࡵࡡࡧ࡭ࡷࠨᵅ"): subprocess.check_output([bstack11ll111_opy_ (u"ࠦ࡬࡯ࡴࠣᵆ"), bstack11ll111_opy_ (u"ࠧࡸࡥࡷ࠯ࡳࡥࡷࡹࡥࠣᵇ"), bstack11ll111_opy_ (u"ࠨ࠭࠮ࡩ࡬ࡸ࠲ࡩ࡯࡮࡯ࡲࡲ࠲ࡪࡩࡳࠤᵈ")]).strip().decode(
                bstack11ll111_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭ᵉ")),
            bstack11ll111_opy_ (u"ࠣ࡮ࡤࡷࡹࡥࡴࡢࡩࠥᵊ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack11ll111_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡵࡢࡷ࡮ࡴࡣࡦࡡ࡯ࡥࡸࡺ࡟ࡵࡣࡪࠦᵋ"): repo.git.rev_list(
                bstack11ll111_opy_ (u"ࠥࡿࢂ࠴࠮ࡼࡿࠥᵌ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack1111llll1ll_opy_ = []
        for remote in remotes:
            bstack111l11llll1_opy_ = {
                bstack11ll111_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᵍ"): remote.name,
                bstack11ll111_opy_ (u"ࠧࡻࡲ࡭ࠤᵎ"): remote.url,
            }
            bstack1111llll1ll_opy_.append(bstack111l11llll1_opy_)
        bstack1111l11l1l1_opy_ = {
            bstack11ll111_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᵏ"): bstack11ll111_opy_ (u"ࠢࡨ࡫ࡷࠦᵐ"),
            **info,
            bstack11ll111_opy_ (u"ࠣࡴࡨࡱࡴࡺࡥࡴࠤᵑ"): bstack1111llll1ll_opy_
        }
        bstack1111l11l1l1_opy_ = bstack1111l11l111_opy_(bstack1111l11l1l1_opy_)
        return bstack1111l11l1l1_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack11ll111_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡲࡴࡺࡲࡡࡵ࡫ࡱ࡫ࠥࡍࡩࡵࠢࡰࡩࡹࡧࡤࡢࡶࡤࠤࡼ࡯ࡴࡩࠢࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠧᵒ").format(err))
        return {}
def bstack1111lll1111_opy_(bstack1111ll1l11l_opy_=None):
    bstack11ll111_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࡋࡪࡺࠠࡨ࡫ࡷࠤࡲ࡫ࡴࡢࡦࡤࡸࡦࠦࡳࡱࡧࡦ࡭࡫࡯ࡣࡢ࡮࡯ࡽࠥ࡬࡯ࡳ࡯ࡤࡸࡹ࡫ࡤࠡࡨࡲࡶࠥࡇࡉࠡࡵࡨࡰࡪࡩࡴࡪࡱࡱࠤࡺࡹࡥࠡࡥࡤࡷࡪࡹࠠࡧࡱࡵࠤࡪࡧࡣࡩࠢࡩࡳࡱࡪࡥࡳࠢ࡬ࡲࠥࡺࡨࡦࠢ࡯࡭ࡸࡺ࠮ࠋࠢࠣࠤࠥࡇࡲࡨࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥ࡬࡯࡭ࡦࡨࡶࡸࠦࠨ࡭࡫ࡶࡸ࠱ࠦ࡯ࡱࡶ࡬ࡳࡳࡧ࡬ࠪ࠼ࠣࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡓࡵ࡮ࡦ࠼ࠣࡑࡴࡴ࡯࠮ࡴࡨࡴࡴࠦࡡࡱࡲࡵࡳࡦࡩࡨ࠭ࠢࡸࡷࡪࡹࠠࡤࡷࡵࡶࡪࡴࡴࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼࠤࡠࡵࡳ࠯ࡩࡨࡸࡨࡽࡤࠩࠫࡠࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡊࡳࡰࡵࡻࠣࡰ࡮ࡹࡴࠡ࡝ࡠ࠾ࠥࡓࡵ࡭ࡶ࡬࠱ࡷ࡫ࡰࡰࠢࡤࡴࡵࡸ࡯ࡢࡥ࡫ࠤࡼ࡯ࡴࡩࠢࡱࡳࠥࡹ࡯ࡶࡴࡦࡩࡸࠦࡣࡰࡰࡩ࡭࡬ࡻࡲࡦࡦ࠯ࠤࡷ࡫ࡴࡶࡴࡱࡷࠥࡡ࡝ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡎ࡬ࡷࡹࠦ࡯ࡧࠢࡳࡥࡹ࡮ࡳ࠻ࠢࡐࡹࡱࡺࡩ࠮ࡴࡨࡴࡴࠦࡡࡱࡲࡵࡳࡦࡩࡨࠡࡹ࡬ࡸ࡭ࠦࡳࡱࡧࡦ࡭࡫࡯ࡣࠡࡨࡲࡰࡩ࡫ࡲࡴࠢࡷࡳࠥࡧ࡮ࡢ࡮ࡼࡾࡪࠐࠠࠡࠢࠣࡖࡪࡺࡵࡳࡰࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦ࡬ࡪࡵࡷ࠾ࠥࡒࡩࡴࡶࠣࡳ࡫ࠦࡤࡪࡥࡷࡷ࠱ࠦࡥࡢࡥ࡫ࠤࡨࡵ࡮ࡵࡣ࡬ࡲ࡮ࡴࡧࠡࡩ࡬ࡸࠥࡳࡥࡵࡣࡧࡥࡹࡧࠠࡧࡱࡵࠤࡦࠦࡦࡰ࡮ࡧࡩࡷ࠴ࠊࠡࠢࠣࠤࠧࠨࠢᵓ")
    if bstack1111ll1l11l_opy_ is None:
        bstack1111ll1l11l_opy_ = [os.getcwd()]
    elif isinstance(bstack1111ll1l11l_opy_, list) and len(bstack1111ll1l11l_opy_) == 0:
        return []
    results = []
    for folder in bstack1111ll1l11l_opy_:
        try:
            if not os.path.exists(folder):
                raise Exception(bstack11ll111_opy_ (u"ࠦࡋࡵ࡬ࡥࡧࡵࠤࡩࡵࡥࡴࠢࡱࡳࡹࠦࡥࡹ࡫ࡶࡸ࠿ࠦࡻࡾࠤᵔ").format(folder))
            repo = git.Repo(folder, search_parent_directories=True)
            result = {
                bstack11ll111_opy_ (u"ࠧࡶࡲࡊࡦࠥᵕ"): bstack11ll111_opy_ (u"ࠨࠢᵖ"),
                bstack11ll111_opy_ (u"ࠢࡧ࡫࡯ࡩࡸࡉࡨࡢࡰࡪࡩࡩࠨᵗ"): [],
                bstack11ll111_opy_ (u"ࠣࡣࡸࡸ࡭ࡵࡲࡴࠤᵘ"): [],
                bstack11ll111_opy_ (u"ࠤࡳࡶࡉࡧࡴࡦࠤᵙ"): bstack11ll111_opy_ (u"ࠥࠦᵚ"),
                bstack11ll111_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡑࡪࡹࡳࡢࡩࡨࡷࠧᵛ"): [],
                bstack11ll111_opy_ (u"ࠧࡶࡲࡕ࡫ࡷࡰࡪࠨᵜ"): bstack11ll111_opy_ (u"ࠨࠢᵝ"),
                bstack11ll111_opy_ (u"ࠢࡱࡴࡇࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠢᵞ"): bstack11ll111_opy_ (u"ࠣࠤᵟ"),
                bstack11ll111_opy_ (u"ࠤࡳࡶࡗࡧࡷࡅ࡫ࡩࡪࠧᵠ"): bstack11ll111_opy_ (u"ࠥࠦᵡ")
            }
            bstack111l1ll1l1l_opy_ = repo.active_branch.name
            bstack1111lll11l1_opy_ = repo.head.commit
            result[bstack11ll111_opy_ (u"ࠦࡵࡸࡉࡥࠤᵢ")] = bstack1111lll11l1_opy_.hexsha
            bstack111l1l111l1_opy_ = _1111l11l11l_opy_(repo)
            logger.debug(bstack11ll111_opy_ (u"ࠧࡈࡡࡴࡧࠣࡦࡷࡧ࡮ࡤࡪࠣࡪࡴࡸࠠࡤࡱࡰࡴࡦࡸࡩࡴࡱࡱ࠾ࠥࠨᵣ") + str(bstack111l1l111l1_opy_) + bstack11ll111_opy_ (u"ࠨࠢᵤ"))
            if bstack111l1l111l1_opy_:
                try:
                    bstack1111l1l1lll_opy_ = repo.git.diff(bstack11ll111_opy_ (u"ࠢ࠮࠯ࡱࡥࡲ࡫࠭ࡰࡰ࡯ࡽࠧᵥ"), bstack1lll11111l1_opy_ (u"ࠣࡽࡥࡥࡸ࡫࡟ࡣࡴࡤࡲࡨ࡮ࡽ࠯࠰࠱ࡿࡨࡻࡲࡳࡧࡱࡸࡤࡨࡲࡢࡰࡦ࡬ࢂࠨᵦ")).split(bstack11ll111_opy_ (u"ࠩ࡟ࡲࠬᵧ"))
                    logger.debug(bstack11ll111_opy_ (u"ࠥࡇ࡭ࡧ࡮ࡨࡧࡧࠤ࡫࡯࡬ࡦࡵࠣࡦࡪࡺࡷࡦࡧࡱࠤࢀࡨࡡࡴࡧࡢࡦࡷࡧ࡮ࡤࡪࢀࠤࡦࡴࡤࠡࡽࡦࡹࡷࡸࡥ࡯ࡶࡢࡦࡷࡧ࡮ࡤࡪࢀ࠾ࠥࠨᵨ") + str(bstack1111l1l1lll_opy_) + bstack11ll111_opy_ (u"ࠦࠧᵩ"))
                    result[bstack11ll111_opy_ (u"ࠧ࡬ࡩ࡭ࡧࡶࡇ࡭ࡧ࡮ࡨࡧࡧࠦᵪ")] = [f.strip() for f in bstack1111l1l1lll_opy_ if f.strip()]
                    commits = list(repo.iter_commits(bstack1lll11111l1_opy_ (u"ࠨࡻࡣࡣࡶࡩࡤࡨࡲࡢࡰࡦ࡬ࢂ࠴࠮ࡼࡥࡸࡶࡷ࡫࡮ࡵࡡࡥࡶࡦࡴࡣࡩࡿࠥᵫ")))
                except Exception:
                    logger.debug(bstack11ll111_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣ࡫ࡪࡺࠠࡤࡪࡤࡲ࡬࡫ࡤࠡࡨ࡬ࡰࡪࡹࠠࡧࡴࡲࡱࠥࡨࡲࡢࡰࡦ࡬ࠥࡩ࡯࡮ࡲࡤࡶ࡮ࡹ࡯࡯࠰ࠣࡊࡦࡲ࡬ࡪࡰࡪࠤࡧࡧࡣ࡬ࠢࡷࡳࠥࡸࡥࡤࡧࡱࡸࠥࡩ࡯࡮࡯࡬ࡸࡸ࠴ࠢᵬ"))
                    commits = list(repo.iter_commits(max_count=10))
                    if commits:
                        result[bstack11ll111_opy_ (u"ࠣࡨ࡬ࡰࡪࡹࡃࡩࡣࡱ࡫ࡪࡪࠢᵭ")] = _1111l1ll1ll_opy_(commits[:5])
            else:
                commits = list(repo.iter_commits(max_count=10))
                if commits:
                    result[bstack11ll111_opy_ (u"ࠤࡩ࡭ࡱ࡫ࡳࡄࡪࡤࡲ࡬࡫ࡤࠣᵮ")] = _1111l1ll1ll_opy_(commits[:5])
            bstack1111l1l1l1l_opy_ = set()
            bstack1111lllll11_opy_ = []
            for commit in commits:
                logger.debug(bstack11ll111_opy_ (u"ࠥࡔࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡤࡱࡰࡱ࡮ࡺ࠺ࠡࠤᵯ") + str(commit.message) + bstack11ll111_opy_ (u"ࠦࠧᵰ"))
                bstack111l1l11111_opy_ = commit.author.name if commit.author else bstack11ll111_opy_ (u"࡛ࠧ࡮࡬ࡰࡲࡻࡳࠨᵱ")
                bstack1111l1l1l1l_opy_.add(bstack111l1l11111_opy_)
                bstack1111lllll11_opy_.append({
                    bstack11ll111_opy_ (u"ࠨ࡭ࡦࡵࡶࡥ࡬࡫ࠢᵲ"): commit.message.strip(),
                    bstack11ll111_opy_ (u"ࠢࡶࡵࡨࡶࠧᵳ"): bstack111l1l11111_opy_
                })
            result[bstack11ll111_opy_ (u"ࠣࡣࡸࡸ࡭ࡵࡲࡴࠤᵴ")] = list(bstack1111l1l1l1l_opy_)
            result[bstack11ll111_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡏࡨࡷࡸࡧࡧࡦࡵࠥᵵ")] = bstack1111lllll11_opy_
            result[bstack11ll111_opy_ (u"ࠥࡴࡷࡊࡡࡵࡧࠥᵶ")] = bstack1111lll11l1_opy_.committed_datetime.strftime(bstack11ll111_opy_ (u"ࠦࠪ࡟࠭ࠦ࡯࠰ࠩࡩࠨᵷ"))
            if (not result[bstack11ll111_opy_ (u"ࠧࡶࡲࡕ࡫ࡷࡰࡪࠨᵸ")] or result[bstack11ll111_opy_ (u"ࠨࡰࡳࡖ࡬ࡸࡱ࡫ࠢᵹ")].strip() == bstack11ll111_opy_ (u"ࠢࠣᵺ")) and bstack1111lll11l1_opy_.message:
                bstack1111lllllll_opy_ = bstack1111lll11l1_opy_.message.strip().splitlines()
                result[bstack11ll111_opy_ (u"ࠣࡲࡵࡘ࡮ࡺ࡬ࡦࠤᵻ")] = bstack1111lllllll_opy_[0] if bstack1111lllllll_opy_ else bstack11ll111_opy_ (u"ࠤࠥᵼ")
                if len(bstack1111lllllll_opy_) > 2:
                    result[bstack11ll111_opy_ (u"ࠥࡴࡷࡊࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠥᵽ")] = bstack11ll111_opy_ (u"ࠫࡡࡴࠧᵾ").join(bstack1111lllllll_opy_[2:]).strip()
            results.append(result)
        except Exception as err:
            logger.error(bstack11ll111_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡵࡰࡶ࡮ࡤࡸ࡮ࡴࡧࠡࡉ࡬ࡸࠥࡳࡥࡵࡣࡧࡥࡹࡧࠠࡧࡱࡵࠤࡆࡏࠠࡴࡧ࡯ࡩࡨࡺࡩࡰࡰࠣࠬ࡫ࡵ࡬ࡥࡧࡵ࠾ࠥࢁࡽࠪ࠼ࠣࡿࢂࠦ࠭ࠡࡽࢀࠦᵿ").format(
                folder,
                type(err).__name__,
                str(err)
            ))
    filtered_results = [
        result
        for result in results
        if _1111lll1l1l_opy_(result)
    ]
    return filtered_results
def _1111lll1l1l_opy_(result):
    bstack11ll111_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡈࡦ࡮ࡳࡩࡷࠦࡴࡰࠢࡦ࡬ࡪࡩ࡫ࠡ࡫ࡩࠤࡦࠦࡧࡪࡶࠣࡱࡪࡺࡡࡥࡣࡷࡥࠥࡸࡥࡴࡷ࡯ࡸࠥ࡯ࡳࠡࡸࡤࡰ࡮ࡪࠠࠩࡰࡲࡲ࠲࡫࡭ࡱࡶࡼࠤ࡫࡯࡬ࡦࡵࡆ࡬ࡦࡴࡧࡦࡦࠣࡥࡳࡪࠠࡢࡷࡷ࡬ࡴࡸࡳࠪ࠰ࠍࠤࠥࠦࠠࠣࠤࠥᶀ")
    return (
        isinstance(result.get(bstack11ll111_opy_ (u"ࠢࡧ࡫࡯ࡩࡸࡉࡨࡢࡰࡪࡩࡩࠨᶁ"), None), list)
        and len(result[bstack11ll111_opy_ (u"ࠣࡨ࡬ࡰࡪࡹࡃࡩࡣࡱ࡫ࡪࡪࠢᶂ")]) > 0
        and isinstance(result.get(bstack11ll111_opy_ (u"ࠤࡤࡹࡹ࡮࡯ࡳࡵࠥᶃ"), None), list)
        and len(result[bstack11ll111_opy_ (u"ࠥࡥࡺࡺࡨࡰࡴࡶࠦᶄ")]) > 0
    )
def _1111l11l11l_opy_(repo):
    bstack11ll111_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤ࡙ࡸࡹࠡࡶࡲࠤࡩ࡫ࡴࡦࡴࡰ࡭ࡳ࡫ࠠࡵࡪࡨࠤࡧࡧࡳࡦࠢࡥࡶࡦࡴࡣࡩࠢࡩࡳࡷࠦࡴࡩࡧࠣ࡫࡮ࡼࡥ࡯ࠢࡵࡩࡵࡵࠠࡸ࡫ࡷ࡬ࡴࡻࡴࠡࡪࡤࡶࡩࡩ࡯ࡥࡧࡧࠤࡳࡧ࡭ࡦࡵࠣࡥࡳࡪࠠࡸࡱࡵ࡯ࠥࡽࡩࡵࡪࠣࡥࡱࡲࠠࡗࡅࡖࠤࡵࡸ࡯ࡷ࡫ࡧࡩࡷࡹ࠮ࠋࠢࠣࠤࠥࡘࡥࡵࡷࡵࡲࡸࠦࡴࡩࡧࠣࡨࡪ࡬ࡡࡶ࡮ࡷࠤࡧࡸࡡ࡯ࡥ࡫ࠤ࡮࡬ࠠࡱࡱࡶࡷ࡮ࡨ࡬ࡦ࠮ࠣࡩࡱࡹࡥࠡࡐࡲࡲࡪ࠴ࠊࠡࠢࠣࠤࠧࠨࠢᶅ")
    try:
        try:
            origin = repo.remotes.origin
            bstack1111l11lll1_opy_ = origin.refs[bstack11ll111_opy_ (u"ࠬࡎࡅࡂࡆࠪᶆ")]
            target = bstack1111l11lll1_opy_.reference.name
            if target.startswith(bstack11ll111_opy_ (u"࠭࡯ࡳ࡫ࡪ࡭ࡳ࠵ࠧᶇ")):
                return target
        except Exception:
            pass
        if repo.remotes and repo.remotes.origin.refs:
            for ref in repo.remotes.origin.refs:
                if ref.name.startswith(bstack11ll111_opy_ (u"ࠧࡰࡴ࡬࡫࡮ࡴ࠯ࠨᶈ")):
                    return ref.name
        if repo.heads:
            return repo.heads[0].name
    except Exception:
        pass
    return None
def _1111l1ll1ll_opy_(commits):
    bstack11ll111_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡉࡨࡸࠥࡲࡩࡴࡶࠣࡳ࡫ࠦࡣࡩࡣࡱ࡫ࡪࡪࠠࡧ࡫࡯ࡩࡸࠦࡦࡳࡱࡰࠤࡦࠦ࡬ࡪࡵࡷࠤࡴ࡬ࠠࡤࡱࡰࡱ࡮ࡺࡳ࠯ࠌࠣࠤࠥࠦࠢࠣࠤᶉ")
    bstack1111l1l1lll_opy_ = set()
    try:
        for commit in commits:
            if commit.parents:
                for parent in commit.parents:
                    diff = commit.diff(parent)
                    for bstack111l1ll1ll1_opy_ in diff:
                        if bstack111l1ll1ll1_opy_.a_path:
                            bstack1111l1l1lll_opy_.add(bstack111l1ll1ll1_opy_.a_path)
                        if bstack111l1ll1ll1_opy_.b_path:
                            bstack1111l1l1lll_opy_.add(bstack111l1ll1ll1_opy_.b_path)
    except Exception:
        pass
    return list(bstack1111l1l1lll_opy_)
def bstack1111l11l111_opy_(bstack1111l11l1l1_opy_):
    bstack1111l11l1ll_opy_ = bstack111l1ll1111_opy_(bstack1111l11l1l1_opy_)
    if bstack1111l11l1ll_opy_ and bstack1111l11l1ll_opy_ > bstack111ll1ll11l_opy_:
        bstack1111l1l11l1_opy_ = bstack1111l11l1ll_opy_ - bstack111ll1ll11l_opy_
        bstack1111llllll1_opy_ = bstack111l111ll11_opy_(bstack1111l11l1l1_opy_[bstack11ll111_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡡࡰࡩࡸࡹࡡࡨࡧࠥᶊ")], bstack1111l1l11l1_opy_)
        bstack1111l11l1l1_opy_[bstack11ll111_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡢࡱࡪࡹࡳࡢࡩࡨࠦᶋ")] = bstack1111llllll1_opy_
        logger.info(bstack11ll111_opy_ (u"࡙ࠦ࡮ࡥࠡࡥࡲࡱࡲ࡯ࡴࠡࡪࡤࡷࠥࡨࡥࡦࡰࠣࡸࡷࡻ࡮ࡤࡣࡷࡩࡩ࠴ࠠࡔ࡫ࡽࡩࠥࡵࡦࠡࡥࡲࡱࡲ࡯ࡴࠡࡣࡩࡸࡪࡸࠠࡵࡴࡸࡲࡨࡧࡴࡪࡱࡱࠤ࡮ࡹࠠࡼࡿࠣࡏࡇࠨᶌ")
                    .format(bstack111l1ll1111_opy_(bstack1111l11l1l1_opy_) / 1024))
    return bstack1111l11l1l1_opy_
def bstack111l1ll1111_opy_(bstack1ll11111_opy_):
    try:
        if bstack1ll11111_opy_:
            bstack111l1lll1ll_opy_ = json.dumps(bstack1ll11111_opy_)
            bstack111l11lllll_opy_ = sys.getsizeof(bstack111l1lll1ll_opy_)
            return bstack111l11lllll_opy_
    except Exception as e:
        logger.debug(bstack11ll111_opy_ (u"࡙ࠧ࡯࡮ࡧࡷ࡬࡮ࡴࡧࠡࡹࡨࡲࡹࠦࡷࡳࡱࡱ࡫ࠥࡽࡨࡪ࡮ࡨࠤࡨࡧ࡬ࡤࡷ࡯ࡥࡹ࡯࡮ࡨࠢࡶ࡭ࡿ࡫ࠠࡰࡨࠣࡎࡘࡕࡎࠡࡱࡥ࡮ࡪࡩࡴ࠻ࠢࡾࢁࠧᶍ").format(e))
    return -1
def bstack111l111ll11_opy_(field, bstack111l1l11l11_opy_):
    try:
        bstack1111l1lll11_opy_ = len(bytes(bstack111llll11ll_opy_, bstack11ll111_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬᶎ")))
        bstack1111ll1ll11_opy_ = bytes(field, bstack11ll111_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭ᶏ"))
        bstack111l1ll11l1_opy_ = len(bstack1111ll1ll11_opy_)
        bstack1111llll11l_opy_ = ceil(bstack111l1ll11l1_opy_ - bstack111l1l11l11_opy_ - bstack1111l1lll11_opy_)
        if bstack1111llll11l_opy_ > 0:
            bstack1111llll1l1_opy_ = bstack1111ll1ll11_opy_[:bstack1111llll11l_opy_].decode(bstack11ll111_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧᶐ"), errors=bstack11ll111_opy_ (u"ࠩ࡬࡫ࡳࡵࡲࡦࠩᶑ")) + bstack111llll11ll_opy_
            return bstack1111llll1l1_opy_
    except Exception as e:
        logger.debug(bstack11ll111_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡶࡵࡹࡳࡩࡡࡵ࡫ࡱ࡫ࠥ࡬ࡩࡦ࡮ࡧ࠰ࠥࡴ࡯ࡵࡪ࡬ࡲ࡬ࠦࡷࡢࡵࠣࡸࡷࡻ࡮ࡤࡣࡷࡩࡩࠦࡨࡦࡴࡨ࠾ࠥࢁࡽࠣᶒ").format(e))
    return field
def bstack1llll111_opy_():
    env = os.environ
    if (bstack11ll111_opy_ (u"ࠦࡏࡋࡎࡌࡋࡑࡗࡤ࡛ࡒࡍࠤᶓ") in env and len(env[bstack11ll111_opy_ (u"ࠧࡐࡅࡏࡍࡌࡒࡘࡥࡕࡓࡎࠥᶔ")]) > 0) or (
            bstack11ll111_opy_ (u"ࠨࡊࡆࡐࡎࡍࡓ࡙࡟ࡉࡑࡐࡉࠧᶕ") in env and len(env[bstack11ll111_opy_ (u"ࠢࡋࡇࡑࡏࡎࡔࡓࡠࡊࡒࡑࡊࠨᶖ")]) > 0):
        return {
            bstack11ll111_opy_ (u"ࠣࡰࡤࡱࡪࠨᶗ"): bstack11ll111_opy_ (u"ࠤࡍࡩࡳࡱࡩ࡯ࡵࠥᶘ"),
            bstack11ll111_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᶙ"): env.get(bstack11ll111_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢᶚ")),
            bstack11ll111_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᶛ"): env.get(bstack11ll111_opy_ (u"ࠨࡊࡐࡄࡢࡒࡆࡓࡅࠣᶜ")),
            bstack11ll111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᶝ"): env.get(bstack11ll111_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢᶞ"))
        }
    if env.get(bstack11ll111_opy_ (u"ࠤࡆࡍࠧᶟ")) == bstack11ll111_opy_ (u"ࠥࡸࡷࡻࡥࠣᶠ") and bstack11l1lll1_opy_(env.get(bstack11ll111_opy_ (u"ࠦࡈࡏࡒࡄࡎࡈࡇࡎࠨᶡ"))):
        return {
            bstack11ll111_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᶢ"): bstack11ll111_opy_ (u"ࠨࡃࡪࡴࡦࡰࡪࡉࡉࠣᶣ"),
            bstack11ll111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᶤ"): env.get(bstack11ll111_opy_ (u"ࠣࡅࡌࡖࡈࡒࡅࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦᶥ")),
            bstack11ll111_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᶦ"): env.get(bstack11ll111_opy_ (u"ࠥࡇࡎࡘࡃࡍࡇࡢࡎࡔࡈࠢᶧ")),
            bstack11ll111_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᶨ"): env.get(bstack11ll111_opy_ (u"ࠧࡉࡉࡓࡅࡏࡉࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࠣᶩ"))
        }
    if env.get(bstack11ll111_opy_ (u"ࠨࡃࡊࠤᶪ")) == bstack11ll111_opy_ (u"ࠢࡵࡴࡸࡩࠧᶫ") and bstack11l1lll1_opy_(env.get(bstack11ll111_opy_ (u"ࠣࡖࡕࡅ࡛ࡏࡓࠣᶬ"))):
        return {
            bstack11ll111_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᶭ"): bstack11ll111_opy_ (u"ࠥࡘࡷࡧࡶࡪࡵࠣࡇࡎࠨᶮ"),
            bstack11ll111_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᶯ"): env.get(bstack11ll111_opy_ (u"࡚ࠧࡒࡂࡘࡌࡗࡤࡈࡕࡊࡎࡇࡣ࡜ࡋࡂࡠࡗࡕࡐࠧᶰ")),
            bstack11ll111_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᶱ"): env.get(bstack11ll111_opy_ (u"ࠢࡕࡔࡄ࡚ࡎ࡙࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤᶲ")),
            bstack11ll111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᶳ"): env.get(bstack11ll111_opy_ (u"ࠤࡗࡖࡆ࡜ࡉࡔࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣᶴ"))
        }
    if env.get(bstack11ll111_opy_ (u"ࠥࡇࡎࠨᶵ")) == bstack11ll111_opy_ (u"ࠦࡹࡸࡵࡦࠤᶶ") and env.get(bstack11ll111_opy_ (u"ࠧࡉࡉࡠࡐࡄࡑࡊࠨᶷ")) == bstack11ll111_opy_ (u"ࠨࡣࡰࡦࡨࡷ࡭࡯ࡰࠣᶸ"):
        return {
            bstack11ll111_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᶹ"): bstack11ll111_opy_ (u"ࠣࡅࡲࡨࡪࡹࡨࡪࡲࠥᶺ"),
            bstack11ll111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᶻ"): None,
            bstack11ll111_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᶼ"): None,
            bstack11ll111_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᶽ"): None
        }
    if env.get(bstack11ll111_opy_ (u"ࠧࡈࡉࡕࡄࡘࡇࡐࡋࡔࡠࡄࡕࡅࡓࡉࡈࠣᶾ")) and env.get(bstack11ll111_opy_ (u"ࠨࡂࡊࡖࡅ࡙ࡈࡑࡅࡕࡡࡆࡓࡒࡓࡉࡕࠤᶿ")):
        return {
            bstack11ll111_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ᷀"): bstack11ll111_opy_ (u"ࠣࡄ࡬ࡸࡧࡻࡣ࡬ࡧࡷࠦ᷁"),
            bstack11ll111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰ᷂ࠧ"): env.get(bstack11ll111_opy_ (u"ࠥࡆࡎ࡚ࡂࡖࡅࡎࡉ࡙ࡥࡇࡊࡖࡢࡌ࡙࡚ࡐࡠࡑࡕࡍࡌࡏࡎࠣ᷃")),
            bstack11ll111_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ᷄"): None,
            bstack11ll111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ᷅"): env.get(bstack11ll111_opy_ (u"ࠨࡂࡊࡖࡅ࡙ࡈࡑࡅࡕࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣ᷆"))
        }
    if env.get(bstack11ll111_opy_ (u"ࠢࡄࡋࠥ᷇")) == bstack11ll111_opy_ (u"ࠣࡶࡵࡹࡪࠨ᷈") and bstack11l1lll1_opy_(env.get(bstack11ll111_opy_ (u"ࠤࡇࡖࡔࡔࡅࠣ᷉"))):
        return {
            bstack11ll111_opy_ (u"ࠥࡲࡦࡳࡥ᷊ࠣ"): bstack11ll111_opy_ (u"ࠦࡉࡸ࡯࡯ࡧࠥ᷋"),
            bstack11ll111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ᷌"): env.get(bstack11ll111_opy_ (u"ࠨࡄࡓࡑࡑࡉࡤࡈࡕࡊࡎࡇࡣࡑࡏࡎࡌࠤ᷍")),
            bstack11ll111_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ᷎"): None,
            bstack11ll111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸ᷏ࠢ"): env.get(bstack11ll111_opy_ (u"ࠤࡇࡖࡔࡔࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘ᷐ࠢ"))
        }
    if env.get(bstack11ll111_opy_ (u"ࠥࡇࡎࠨ᷑")) == bstack11ll111_opy_ (u"ࠦࡹࡸࡵࡦࠤ᷒") and bstack11l1lll1_opy_(env.get(bstack11ll111_opy_ (u"࡙ࠧࡅࡎࡃࡓࡌࡔࡘࡅࠣᷓ"))):
        return {
            bstack11ll111_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᷔ"): bstack11ll111_opy_ (u"ࠢࡔࡧࡰࡥࡵ࡮࡯ࡳࡧࠥᷕ"),
            bstack11ll111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᷖ"): env.get(bstack11ll111_opy_ (u"ࠤࡖࡉࡒࡇࡐࡉࡑࡕࡉࡤࡕࡒࡈࡃࡑࡍ࡟ࡇࡔࡊࡑࡑࡣ࡚ࡘࡌࠣᷗ")),
            bstack11ll111_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᷘ"): env.get(bstack11ll111_opy_ (u"ࠦࡘࡋࡍࡂࡒࡋࡓࡗࡋ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤᷙ")),
            bstack11ll111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᷚ"): env.get(bstack11ll111_opy_ (u"ࠨࡓࡆࡏࡄࡔࡍࡕࡒࡆࡡࡍࡓࡇࡥࡉࡅࠤᷛ"))
        }
    if env.get(bstack11ll111_opy_ (u"ࠢࡄࡋࠥᷜ")) == bstack11ll111_opy_ (u"ࠣࡶࡵࡹࡪࠨᷝ") and bstack11l1lll1_opy_(env.get(bstack11ll111_opy_ (u"ࠤࡊࡍ࡙ࡒࡁࡃࡡࡆࡍࠧᷞ"))):
        return {
            bstack11ll111_opy_ (u"ࠥࡲࡦࡳࡥࠣᷟ"): bstack11ll111_opy_ (u"ࠦࡌ࡯ࡴࡍࡣࡥࠦᷠ"),
            bstack11ll111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᷡ"): env.get(bstack11ll111_opy_ (u"ࠨࡃࡊࡡࡍࡓࡇࡥࡕࡓࡎࠥᷢ")),
            bstack11ll111_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᷣ"): env.get(bstack11ll111_opy_ (u"ࠣࡅࡌࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨᷤ")),
            bstack11ll111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᷥ"): env.get(bstack11ll111_opy_ (u"ࠥࡇࡎࡥࡊࡐࡄࡢࡍࡉࠨᷦ"))
        }
    if env.get(bstack11ll111_opy_ (u"ࠦࡈࡏࠢᷧ")) == bstack11ll111_opy_ (u"ࠧࡺࡲࡶࡧࠥᷨ") and bstack11l1lll1_opy_(env.get(bstack11ll111_opy_ (u"ࠨࡂࡖࡋࡏࡈࡐࡏࡔࡆࠤᷩ"))):
        return {
            bstack11ll111_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᷪ"): bstack11ll111_opy_ (u"ࠣࡄࡸ࡭ࡱࡪ࡫ࡪࡶࡨࠦᷫ"),
            bstack11ll111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᷬ"): env.get(bstack11ll111_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡍࡌࡘࡊࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤᷭ")),
            bstack11ll111_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᷮ"): env.get(bstack11ll111_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࡠࡎࡄࡆࡊࡒࠢᷯ")) or env.get(bstack11ll111_opy_ (u"ࠨࡂࡖࡋࡏࡈࡐࡏࡔࡆࡡࡓࡍࡕࡋࡌࡊࡐࡈࡣࡓࡇࡍࡆࠤᷰ")),
            bstack11ll111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᷱ"): env.get(bstack11ll111_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥᷲ"))
        }
    if bstack11l1lll1_opy_(env.get(bstack11ll111_opy_ (u"ࠤࡗࡊࡤࡈࡕࡊࡎࡇࠦᷳ"))):
        return {
            bstack11ll111_opy_ (u"ࠥࡲࡦࡳࡥࠣᷴ"): bstack11ll111_opy_ (u"࡛ࠦ࡯ࡳࡶࡣ࡯ࠤࡘࡺࡵࡥ࡫ࡲࠤ࡙࡫ࡡ࡮ࠢࡖࡩࡷࡼࡩࡤࡧࡶࠦ᷵"),
            bstack11ll111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ᷶"): bstack11ll111_opy_ (u"ࠨࡻࡾࡽࢀ᷷ࠦ").format(env.get(bstack11ll111_opy_ (u"ࠧࡔ࡛ࡖࡘࡊࡓ࡟ࡕࡇࡄࡑࡋࡕࡕࡏࡆࡄࡘࡎࡕࡎࡔࡇࡕ࡚ࡊࡘࡕࡓࡋ᷸ࠪ")), env.get(bstack11ll111_opy_ (u"ࠨࡕ࡜ࡗ࡙ࡋࡍࡠࡖࡈࡅࡒࡖࡒࡐࡌࡈࡇ࡙ࡏࡄࠨ᷹"))),
            bstack11ll111_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨ᷺ࠦ"): env.get(bstack11ll111_opy_ (u"ࠥࡗ࡞࡙ࡔࡆࡏࡢࡈࡊࡌࡉࡏࡋࡗࡍࡔࡔࡉࡅࠤ᷻")),
            bstack11ll111_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ᷼"): env.get(bstack11ll111_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡌࡈ᷽ࠧ"))
        }
    if bstack11l1lll1_opy_(env.get(bstack11ll111_opy_ (u"ࠨࡁࡑࡒ࡙ࡉ࡞ࡕࡒࠣ᷾"))):
        return {
            bstack11ll111_opy_ (u"ࠢ࡯ࡣࡰࡩ᷿ࠧ"): bstack11ll111_opy_ (u"ࠣࡃࡳࡴࡻ࡫ࡹࡰࡴࠥḀ"),
            bstack11ll111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧḁ"): bstack11ll111_opy_ (u"ࠥࡿࢂ࠵ࡰࡳࡱ࡭ࡩࡨࡺ࠯ࡼࡿ࠲ࡿࢂ࠵ࡢࡶ࡫࡯ࡨࡸ࠵ࡻࡾࠤḂ").format(env.get(bstack11ll111_opy_ (u"ࠫࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡕࡓࡎࠪḃ")), env.get(bstack11ll111_opy_ (u"ࠬࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡂࡅࡆࡓ࡚ࡔࡔࡠࡐࡄࡑࡊ࠭Ḅ")), env.get(bstack11ll111_opy_ (u"࠭ࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡒࡕࡓࡏࡋࡃࡕࡡࡖࡐ࡚ࡍࠧḅ")), env.get(bstack11ll111_opy_ (u"ࠧࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠫḆ"))),
            bstack11ll111_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥḇ"): env.get(bstack11ll111_opy_ (u"ࠤࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨḈ")),
            bstack11ll111_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤḉ"): env.get(bstack11ll111_opy_ (u"ࠦࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧḊ"))
        }
    if env.get(bstack11ll111_opy_ (u"ࠧࡇ࡚ࡖࡔࡈࡣࡍ࡚ࡔࡑࡡࡘࡗࡊࡘ࡟ࡂࡉࡈࡒ࡙ࠨḋ")) and env.get(bstack11ll111_opy_ (u"ࠨࡔࡇࡡࡅ࡙ࡎࡒࡄࠣḌ")):
        return {
            bstack11ll111_opy_ (u"ࠢ࡯ࡣࡰࡩࠧḍ"): bstack11ll111_opy_ (u"ࠣࡃࡽࡹࡷ࡫ࠠࡄࡋࠥḎ"),
            bstack11ll111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧḏ"): bstack11ll111_opy_ (u"ࠥࡿࢂࢁࡽ࠰ࡡࡥࡹ࡮ࡲࡤ࠰ࡴࡨࡷࡺࡲࡴࡴࡁࡥࡹ࡮ࡲࡤࡊࡦࡀࡿࢂࠨḐ").format(env.get(bstack11ll111_opy_ (u"ࠫࡘ࡟ࡓࡕࡇࡐࡣ࡙ࡋࡁࡎࡈࡒ࡙ࡓࡊࡁࡕࡋࡒࡒࡘࡋࡒࡗࡇࡕ࡙ࡗࡏࠧḑ")), env.get(bstack11ll111_opy_ (u"࡙࡙ࠬࡔࡖࡈࡑࡤ࡚ࡅࡂࡏࡓࡖࡔࡐࡅࡄࡖࠪḒ")), env.get(bstack11ll111_opy_ (u"࠭ࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡍࡉ࠭ḓ"))),
            bstack11ll111_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤḔ"): env.get(bstack11ll111_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡏࡄࠣḕ")),
            bstack11ll111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣḖ"): env.get(bstack11ll111_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡊࡆࠥḗ"))
        }
    if any([env.get(bstack11ll111_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠤḘ")), env.get(bstack11ll111_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡔࡈࡗࡔࡒࡖࡆࡆࡢࡗࡔ࡛ࡒࡄࡇࡢ࡚ࡊࡘࡓࡊࡑࡑࠦḙ")), env.get(bstack11ll111_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡖࡓ࡚ࡘࡃࡆࡡ࡙ࡉࡗ࡙ࡉࡐࡐࠥḚ"))]):
        return {
            bstack11ll111_opy_ (u"ࠢ࡯ࡣࡰࡩࠧḛ"): bstack11ll111_opy_ (u"ࠣࡃ࡚ࡗࠥࡉ࡯ࡥࡧࡅࡹ࡮ࡲࡤࠣḜ"),
            bstack11ll111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧḝ"): env.get(bstack11ll111_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡐࡖࡄࡏࡍࡈࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤḞ")),
            bstack11ll111_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨḟ"): env.get(bstack11ll111_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠥḠ")),
            bstack11ll111_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧḡ"): env.get(bstack11ll111_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧḢ"))
        }
    if env.get(bstack11ll111_opy_ (u"ࠣࡤࡤࡱࡧࡵ࡯ࡠࡤࡸ࡭ࡱࡪࡎࡶ࡯ࡥࡩࡷࠨḣ")):
        return {
            bstack11ll111_opy_ (u"ࠤࡱࡥࡲ࡫ࠢḤ"): bstack11ll111_opy_ (u"ࠥࡆࡦࡳࡢࡰࡱࠥḥ"),
            bstack11ll111_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢḦ"): env.get(bstack11ll111_opy_ (u"ࠧࡨࡡ࡮ࡤࡲࡳࡤࡨࡵࡪ࡮ࡧࡖࡪࡹࡵ࡭ࡶࡶ࡙ࡷࡲࠢḧ")),
            bstack11ll111_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣḨ"): env.get(bstack11ll111_opy_ (u"ࠢࡣࡣࡰࡦࡴࡵ࡟ࡴࡪࡲࡶࡹࡐ࡯ࡣࡐࡤࡱࡪࠨḩ")),
            bstack11ll111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢḪ"): env.get(bstack11ll111_opy_ (u"ࠤࡥࡥࡲࡨ࡯ࡰࡡࡥࡹ࡮ࡲࡤࡏࡷࡰࡦࡪࡸࠢḫ"))
        }
    if env.get(bstack11ll111_opy_ (u"࡛ࠥࡊࡘࡃࡌࡇࡕࠦḬ")) or env.get(bstack11ll111_opy_ (u"ࠦ࡜ࡋࡒࡄࡍࡈࡖࡤࡓࡁࡊࡐࡢࡔࡎࡖࡅࡍࡋࡑࡉࡤ࡙ࡔࡂࡔࡗࡉࡉࠨḭ")):
        return {
            bstack11ll111_opy_ (u"ࠧࡴࡡ࡮ࡧࠥḮ"): bstack11ll111_opy_ (u"ࠨࡗࡦࡴࡦ࡯ࡪࡸࠢḯ"),
            bstack11ll111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥḰ"): env.get(bstack11ll111_opy_ (u"࡙ࠣࡈࡖࡈࡑࡅࡓࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧḱ")),
            bstack11ll111_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦḲ"): bstack11ll111_opy_ (u"ࠥࡑࡦ࡯࡮ࠡࡒ࡬ࡴࡪࡲࡩ࡯ࡧࠥḳ") if env.get(bstack11ll111_opy_ (u"ࠦ࡜ࡋࡒࡄࡍࡈࡖࡤࡓࡁࡊࡐࡢࡔࡎࡖࡅࡍࡋࡑࡉࡤ࡙ࡔࡂࡔࡗࡉࡉࠨḴ")) else None,
            bstack11ll111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦḵ"): env.get(bstack11ll111_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘ࡟ࡈࡋࡗࡣࡈࡕࡍࡎࡋࡗࠦḶ"))
        }
    if any([env.get(bstack11ll111_opy_ (u"ࠢࡈࡅࡓࡣࡕࡘࡏࡋࡇࡆࡘࠧḷ")), env.get(bstack11ll111_opy_ (u"ࠣࡉࡆࡐࡔ࡛ࡄࡠࡒࡕࡓࡏࡋࡃࡕࠤḸ")), env.get(bstack11ll111_opy_ (u"ࠤࡊࡓࡔࡍࡌࡆࡡࡆࡐࡔ࡛ࡄࡠࡒࡕࡓࡏࡋࡃࡕࠤḹ"))]):
        return {
            bstack11ll111_opy_ (u"ࠥࡲࡦࡳࡥࠣḺ"): bstack11ll111_opy_ (u"ࠦࡌࡵ࡯ࡨ࡮ࡨࠤࡈࡲ࡯ࡶࡦࠥḻ"),
            bstack11ll111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣḼ"): None,
            bstack11ll111_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣḽ"): env.get(bstack11ll111_opy_ (u"ࠢࡑࡔࡒࡎࡊࡉࡔࡠࡋࡇࠦḾ")),
            bstack11ll111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢḿ"): env.get(bstack11ll111_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡋࡇࠦṀ"))
        }
    if env.get(bstack11ll111_opy_ (u"ࠥࡗࡍࡏࡐࡑࡃࡅࡐࡊࠨṁ")):
        return {
            bstack11ll111_opy_ (u"ࠦࡳࡧ࡭ࡦࠤṂ"): bstack11ll111_opy_ (u"࡙ࠧࡨࡪࡲࡳࡥࡧࡲࡥࠣṃ"),
            bstack11ll111_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤṄ"): env.get(bstack11ll111_opy_ (u"ࠢࡔࡊࡌࡔࡕࡇࡂࡍࡇࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨṅ")),
            bstack11ll111_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥṆ"): bstack11ll111_opy_ (u"ࠤࡍࡳࡧࠦࠣࡼࡿࠥṇ").format(env.get(bstack11ll111_opy_ (u"ࠪࡗࡍࡏࡐࡑࡃࡅࡐࡊࡥࡊࡐࡄࡢࡍࡉ࠭Ṉ"))) if env.get(bstack11ll111_opy_ (u"ࠦࡘࡎࡉࡑࡒࡄࡆࡑࡋ࡟ࡋࡑࡅࡣࡎࡊࠢṉ")) else None,
            bstack11ll111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦṊ"): env.get(bstack11ll111_opy_ (u"ࠨࡓࡉࡋࡓࡔࡆࡈࡌࡆࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣṋ"))
        }
    if bstack11l1lll1_opy_(env.get(bstack11ll111_opy_ (u"ࠢࡏࡇࡗࡐࡎࡌ࡙ࠣṌ"))):
        return {
            bstack11ll111_opy_ (u"ࠣࡰࡤࡱࡪࠨṍ"): bstack11ll111_opy_ (u"ࠤࡑࡩࡹࡲࡩࡧࡻࠥṎ"),
            bstack11ll111_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨṏ"): env.get(bstack11ll111_opy_ (u"ࠦࡉࡋࡐࡍࡑ࡜ࡣ࡚ࡘࡌࠣṐ")),
            bstack11ll111_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢṑ"): env.get(bstack11ll111_opy_ (u"ࠨࡓࡊࡖࡈࡣࡓࡇࡍࡆࠤṒ")),
            bstack11ll111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨṓ"): env.get(bstack11ll111_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡊࡆࠥṔ"))
        }
    if bstack11l1lll1_opy_(env.get(bstack11ll111_opy_ (u"ࠤࡊࡍ࡙ࡎࡕࡃࡡࡄࡇ࡙ࡏࡏࡏࡕࠥṕ"))):
        return {
            bstack11ll111_opy_ (u"ࠥࡲࡦࡳࡥࠣṖ"): bstack11ll111_opy_ (u"ࠦࡌ࡯ࡴࡉࡷࡥࠤࡆࡩࡴࡪࡱࡱࡷࠧṗ"),
            bstack11ll111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣṘ"): bstack11ll111_opy_ (u"ࠨࡻࡾ࠱ࡾࢁ࠴ࡧࡣࡵ࡫ࡲࡲࡸ࠵ࡲࡶࡰࡶ࠳ࢀࢃࠢṙ").format(env.get(bstack11ll111_opy_ (u"ࠧࡈࡋࡗࡌ࡚ࡈ࡟ࡔࡇࡕ࡚ࡊࡘ࡟ࡖࡔࡏࠫṚ")), env.get(bstack11ll111_opy_ (u"ࠨࡉࡌࡘࡍ࡛ࡂࡠࡔࡈࡔࡔ࡙ࡉࡕࡑࡕ࡝ࠬṛ")), env.get(bstack11ll111_opy_ (u"ࠩࡊࡍ࡙ࡎࡕࡃࡡࡕ࡙ࡓࡥࡉࡅࠩṜ"))),
            bstack11ll111_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧṝ"): env.get(bstack11ll111_opy_ (u"ࠦࡌࡏࡔࡉࡗࡅࡣ࡜ࡕࡒࡌࡈࡏࡓ࡜ࠨṞ")),
            bstack11ll111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦṟ"): env.get(bstack11ll111_opy_ (u"ࠨࡇࡊࡖࡋ࡙ࡇࡥࡒࡖࡐࡢࡍࡉࠨṠ"))
        }
    if env.get(bstack11ll111_opy_ (u"ࠢࡄࡋࠥṡ")) == bstack11ll111_opy_ (u"ࠣࡶࡵࡹࡪࠨṢ") and env.get(bstack11ll111_opy_ (u"ࠤ࡙ࡉࡗࡉࡅࡍࠤṣ")) == bstack11ll111_opy_ (u"ࠥ࠵ࠧṤ"):
        return {
            bstack11ll111_opy_ (u"ࠦࡳࡧ࡭ࡦࠤṥ"): bstack11ll111_opy_ (u"ࠧ࡜ࡥࡳࡥࡨࡰࠧṦ"),
            bstack11ll111_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤṧ"): bstack11ll111_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࡼࡿࠥṨ").format(env.get(bstack11ll111_opy_ (u"ࠨࡘࡈࡖࡈࡋࡌࡠࡗࡕࡐࠬṩ"))),
            bstack11ll111_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦṪ"): None,
            bstack11ll111_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤṫ"): None,
        }
    if env.get(bstack11ll111_opy_ (u"࡙ࠦࡋࡁࡎࡅࡌࡘ࡞ࡥࡖࡆࡔࡖࡍࡔࡔࠢṬ")):
        return {
            bstack11ll111_opy_ (u"ࠧࡴࡡ࡮ࡧࠥṭ"): bstack11ll111_opy_ (u"ࠨࡔࡦࡣࡰࡧ࡮ࡺࡹࠣṮ"),
            bstack11ll111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥṯ"): None,
            bstack11ll111_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥṰ"): env.get(bstack11ll111_opy_ (u"ࠤࡗࡉࡆࡓࡃࡊࡖ࡜ࡣࡕࡘࡏࡋࡇࡆࡘࡤࡔࡁࡎࡇࠥṱ")),
            bstack11ll111_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤṲ"): env.get(bstack11ll111_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥṳ"))
        }
    if any([env.get(bstack11ll111_opy_ (u"ࠧࡉࡏࡏࡅࡒ࡙ࡗ࡙ࡅࠣṴ")), env.get(bstack11ll111_opy_ (u"ࠨࡃࡐࡐࡆࡓ࡚ࡘࡓࡆࡡࡘࡖࡑࠨṵ")), env.get(bstack11ll111_opy_ (u"ࠢࡄࡑࡑࡇࡔ࡛ࡒࡔࡇࡢ࡙ࡘࡋࡒࡏࡃࡐࡉࠧṶ")), env.get(bstack11ll111_opy_ (u"ࠣࡅࡒࡒࡈࡕࡕࡓࡕࡈࡣ࡙ࡋࡁࡎࠤṷ"))]):
        return {
            bstack11ll111_opy_ (u"ࠤࡱࡥࡲ࡫ࠢṸ"): bstack11ll111_opy_ (u"ࠥࡇࡴࡴࡣࡰࡷࡵࡷࡪࠨṹ"),
            bstack11ll111_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢṺ"): None,
            bstack11ll111_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢṻ"): env.get(bstack11ll111_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢṼ")) or None,
            bstack11ll111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨṽ"): env.get(bstack11ll111_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡊࡆࠥṾ"), 0)
        }
    if env.get(bstack11ll111_opy_ (u"ࠤࡊࡓࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢṿ")):
        return {
            bstack11ll111_opy_ (u"ࠥࡲࡦࡳࡥࠣẀ"): bstack11ll111_opy_ (u"ࠦࡌࡵࡃࡅࠤẁ"),
            bstack11ll111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣẂ"): None,
            bstack11ll111_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣẃ"): env.get(bstack11ll111_opy_ (u"ࠢࡈࡑࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧẄ")),
            bstack11ll111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢẅ"): env.get(bstack11ll111_opy_ (u"ࠤࡊࡓࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡄࡑࡘࡒ࡙ࡋࡒࠣẆ"))
        }
    if env.get(bstack11ll111_opy_ (u"ࠥࡇࡋࡥࡂࡖࡋࡏࡈࡤࡏࡄࠣẇ")):
        return {
            bstack11ll111_opy_ (u"ࠦࡳࡧ࡭ࡦࠤẈ"): bstack11ll111_opy_ (u"ࠧࡉ࡯ࡥࡧࡉࡶࡪࡹࡨࠣẉ"),
            bstack11ll111_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤẊ"): env.get(bstack11ll111_opy_ (u"ࠢࡄࡈࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨẋ")),
            bstack11ll111_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥẌ"): env.get(bstack11ll111_opy_ (u"ࠤࡆࡊࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡏࡃࡐࡉࠧẍ")),
            bstack11ll111_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤẎ"): env.get(bstack11ll111_opy_ (u"ࠦࡈࡌ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠤẏ"))
        }
    return {bstack11ll111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦẐ"): None}
def get_host_info():
    return {
        bstack11ll111_opy_ (u"ࠨࡨࡰࡵࡷࡲࡦࡳࡥࠣẑ"): platform.node(),
        bstack11ll111_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠤẒ"): platform.system(),
        bstack11ll111_opy_ (u"ࠣࡶࡼࡴࡪࠨẓ"): platform.machine(),
        bstack11ll111_opy_ (u"ࠤࡹࡩࡷࡹࡩࡰࡰࠥẔ"): platform.version(),
        bstack11ll111_opy_ (u"ࠥࡥࡷࡩࡨࠣẕ"): platform.architecture()[0]
    }
def bstack1lllll11l_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack111l1ll1lll_opy_():
    if global_config.get_property(bstack11ll111_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠬẖ")):
        return bstack11ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫẗ")
    return bstack11ll111_opy_ (u"࠭ࡵ࡯࡭ࡱࡳࡼࡴ࡟ࡨࡴ࡬ࡨࠬẘ")
def bstack111l11l111l_opy_(driver):
    info = {
        bstack11ll111_opy_ (u"ࠧࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ẙ"): driver.capabilities,
        bstack11ll111_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠬẚ"): driver.session_id,
        bstack11ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪẛ"): driver.capabilities.get(bstack11ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨẜ"), None),
        bstack11ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ẝ"): driver.capabilities.get(bstack11ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ẞ"), None),
        bstack11ll111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠨẟ"): driver.capabilities.get(bstack11ll111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪ࠭Ạ"), None),
        bstack11ll111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫạ"):driver.capabilities.get(bstack11ll111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫẢ"), None),
    }
    if bstack111l1ll1lll_opy_() == bstack11ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩả"):
        if bstack1l1111l11_opy_():
            info[bstack11ll111_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࠬẤ")] = bstack11ll111_opy_ (u"ࠬࡧࡰࡱ࠯ࡤࡹࡹࡵ࡭ࡢࡶࡨࠫấ")
        elif driver.capabilities.get(bstack11ll111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧẦ"), {}).get(bstack11ll111_opy_ (u"ࠧࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨࠫầ"), False):
            info[bstack11ll111_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࠩẨ")] = bstack11ll111_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡴࡥࡤࡰࡪ࠭ẩ")
        else:
            info[bstack11ll111_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࠫẪ")] = bstack11ll111_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ẫ")
    return info
def bstack1l1111l11_opy_():
    if global_config.get_property(bstack11ll111_opy_ (u"ࠬࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠫẬ")):
        return True
    if bstack11l1lll1_opy_(os.environ.get(bstack11ll111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧậ"), None)):
        return True
    return False
def bstack1111ll111ll_opy_(bstack111l11l1l11_opy_, url, response, headers=None, data=None):
    bstack11ll111_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࡃࡷ࡬ࡰࡩࠦࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡰࡴ࡭ࠠࡱࡣࡵࡥࡲ࡫ࡴࡦࡴࡶࠤ࡫ࡵࡲࠡࡴࡨࡵࡺ࡫ࡳࡵ࠱ࡵࡩࡸࡶ࡯࡯ࡵࡨࠤࡱࡵࡧࡨ࡫ࡱ࡫ࠏࠦࠠࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡵࡩࡶࡻࡥࡴࡶࡢࡸࡾࡶࡥ࠻ࠢࡋࡘ࡙ࡖࠠ࡮ࡧࡷ࡬ࡴࡪࠠࠩࡉࡈࡘ࠱ࠦࡐࡐࡕࡗ࠰ࠥ࡫ࡴࡤ࠰ࠬࠎࠥࠦࠠࠡࠢࠣࠤࠥࡻࡲ࡭࠼ࠣࡖࡪࡷࡵࡦࡵࡷࠤ࡚ࡘࡌ࠰ࡧࡱࡨࡵࡵࡩ࡯ࡶࠍࠤࠥࠦࠠࠡࠢࠣࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࡀࠠࡓࡧࡶࡴࡴࡴࡳࡦࠢࡲࡦ࡯࡫ࡣࡵࠢࡩࡶࡴࡳࠠࡳࡧࡴࡹࡪࡹࡴࡴࠌࠣࠤࠥࠦࠠࠡࠢࠣ࡬ࡪࡧࡤࡦࡴࡶ࠾ࠥࡘࡥࡲࡷࡨࡷࡹࠦࡨࡦࡣࡧࡩࡷࡹࠠࡰࡴࠣࡒࡴࡴࡥࠋࠢࠣࠤࠥࠦࠠࠡࠢࡧࡥࡹࡧ࠺ࠡࡔࡨࡵࡺ࡫ࡳࡵࠢࡍࡗࡔࡔࠠࡥࡣࡷࡥࠥࡵࡲࠡࡐࡲࡲࡪࠐࠠࠡࠢࠣࡖࡪࡺࡵࡳࡰࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡤࡪࡥࡷ࠾ࠥࡌ࡯ࡳ࡯ࡤࡸࡹ࡫ࡤࠡ࡮ࡲ࡫ࠥࡳࡥࡴࡵࡤ࡫ࡪࠦࡷࡪࡶ࡫ࠤࡷ࡫ࡱࡶࡧࡶࡸࠥࡧ࡮ࡥࠢࡵࡩࡸࡶ࡯࡯ࡵࡨࠤࡩࡧࡴࡢࠌࠣࠤࠥࠦࠢࠣࠤẮ")
    bstack1111ll1l1ll_opy_ = {
        bstack11ll111_opy_ (u"ࠣࡪࡨࡥࡩ࡫ࡲࡴࠤắ"): headers,
        bstack11ll111_opy_ (u"ࠤࡰࡩࡹ࡮࡯ࡥࠤẰ"): bstack111l11l1l11_opy_.upper(),
        bstack11ll111_opy_ (u"ࠥࡥ࡬࡫࡮ࡵࠤằ"): None,
        bstack11ll111_opy_ (u"ࠦࡪࡴࡤࡱࡱ࡬ࡲࡹࠨẲ"): url,
        bstack11ll111_opy_ (u"ࠧࡰࡳࡰࡰࠥẳ"): data
    }
    try:
        bstack1111ll111l1_opy_ = response.json()
    except Exception:
        bstack1111ll111l1_opy_ = response.text
    bstack111l11lll11_opy_ = {
        bstack11ll111_opy_ (u"ࠨࡢࡰࡦࡼࠦẴ"): bstack1111ll111l1_opy_,
        bstack11ll111_opy_ (u"ࠢࡴࡶࡤࡸࡺࡹࡃࡰࡦࡨࠦẵ"): response.status_code
    }
    return {
        bstack11ll111_opy_ (u"ࠣࡴࡨࡵࡺ࡫ࡳࡵࠤẶ"): bstack1111ll1l1ll_opy_,
        bstack11ll111_opy_ (u"ࠤࡵࡩࡸࡶ࡯࡯ࡵࡨࠦặ"): bstack111l11lll11_opy_
    }
def bstack1l1l11ll_opy_(bstack111l11l1l11_opy_, url, data, config):
    headers = config.get(bstack11ll111_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫẸ"), None)
    proxies = bstack1111llll1l_opy_(config, url)
    auth = config.get(bstack11ll111_opy_ (u"ࠫࡦࡻࡴࡩࠩẹ"), None)
    response = requests.request(
            bstack111l11l1l11_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    try:
        log_message = bstack1111ll111ll_opy_(bstack111l11l1l11_opy_, url, response, headers, data)
        bstack1l1ll1ll11_opy_.debug(json.dumps(log_message, separators=(bstack11ll111_opy_ (u"ࠬ࠲ࠧẺ"), bstack11ll111_opy_ (u"࠭࠺ࠨẻ"))))
    except Exception as e:
        logger.debug(bstack11ll111_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡲ࡯ࡨࡩ࡬ࡲ࡬ࠦࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡶࡪࡷࡵࡦࡵࡷ࠾ࠥࢁࡽࠣẼ").format(e))
    return response
def bstack111llllll1_opy_(bstack1l1llll111_opy_, size):
    bstack1111llll1_opy_ = []
    while len(bstack1l1llll111_opy_) > size:
        bstack1ll1ll11_opy_ = bstack1l1llll111_opy_[:size]
        bstack1111llll1_opy_.append(bstack1ll1ll11_opy_)
        bstack1l1llll111_opy_ = bstack1l1llll111_opy_[size:]
    bstack1111llll1_opy_.append(bstack1l1llll111_opy_)
    return bstack1111llll1_opy_
def bstack111l111l1ll_opy_(message, bstack1111l1l1l11_opy_=False):
    os.write(1, bytes(message, bstack11ll111_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧẽ")))
    os.write(1, bytes(bstack11ll111_opy_ (u"ࠩ࡟ࡲࠬẾ"), bstack11ll111_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩế")))
    if bstack1111l1l1l11_opy_:
        with open(bstack11ll111_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠱ࡴ࠷࠱ࡺ࠯ࠪỀ") + os.environ[bstack11ll111_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡊࡄࡗࡍࡋࡄࡠࡋࡇࠫề")] + bstack11ll111_opy_ (u"࠭࠮࡭ࡱࡪࠫỂ"), bstack11ll111_opy_ (u"ࠧࡢࠩể")) as f:
            f.write(message + bstack11ll111_opy_ (u"ࠨ࡞ࡱࠫỄ"))
def bstack1l11l1111ll_opy_():
    return os.environ[bstack11ll111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠬễ")].lower() == bstack11ll111_opy_ (u"ࠪࡸࡷࡻࡥࠨỆ")
def current_time():
    return bstack1111111l11_opy_().replace(tzinfo=None).isoformat() + bstack11ll111_opy_ (u"ࠫ࡟࠭ệ")
def time_diff(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack11ll111_opy_ (u"ࠬࡠࠧỈ"))) - datetime.datetime.fromisoformat(start.rstrip(bstack11ll111_opy_ (u"࡚࠭ࠨỉ")))).total_seconds() * 1000
def bstack1111l1ll11l_opy_(timestamp):
    return bstack111l1111l11_opy_(timestamp).isoformat() + bstack11ll111_opy_ (u"࡛ࠧࠩỊ")
def bstack111l1l1111l_opy_(bstack1111l1l111l_opy_):
    date_format = bstack11ll111_opy_ (u"ࠨࠧ࡜ࠩࡲࠫࡤࠡࠧࡋ࠾ࠪࡓ࠺ࠦࡕ࠱ࠩ࡫࠭ị")
    bstack111l111lll1_opy_ = datetime.datetime.strptime(bstack1111l1l111l_opy_, date_format)
    return bstack111l111lll1_opy_.isoformat() + bstack11ll111_opy_ (u"ࠩ࡝ࠫỌ")
def bstack1111l11ll1l_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack11ll111_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪọ")
    else:
        return bstack11ll111_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫỎ")
def bstack11l1lll1_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack11ll111_opy_ (u"ࠬࡺࡲࡶࡧࠪỏ")
def bstack1111l11llll_opy_(val):
    return val.__str__().lower() == bstack11ll111_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬỐ")
def error_handler(bstack111l11l1111_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack111l11l1111_opy_ as e:
                print(bstack11ll111_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠡࡽࢀࠤ࠲ࡄࠠࡼࡿ࠽ࠤࢀࢃࠢố").format(func.__name__, bstack111l11l1111_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack1111ll1ll1l_opy_(bstack111l1l1l1l1_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack111l1l1l1l1_opy_(cls, *args, **kwargs)
            except bstack111l11l1111_opy_ as e:
                print(bstack11ll111_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡧࡷࡱࡧࡹ࡯࡯࡯ࠢࡾࢁࠥ࠳࠾ࠡࡽࢀ࠾ࠥࢁࡽࠣỒ").format(bstack111l1l1l1l1_opy_.__name__, bstack111l11l1111_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack1111ll1ll1l_opy_
    else:
        return decorator
def bstack11l1llllll_opy_(bstack1llll111l1l_opy_):
    if os.getenv(bstack11ll111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠬồ")) is not None:
        return bstack11l1lll1_opy_(os.getenv(bstack11ll111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓ࠭Ổ")))
    if bstack11ll111_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨổ") in bstack1llll111l1l_opy_ and bstack1111l11llll_opy_(bstack1llll111l1l_opy_[bstack11ll111_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩỖ")]):
        return False
    if bstack11ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨỗ") in bstack1llll111l1l_opy_ and bstack1111l11llll_opy_(bstack1llll111l1l_opy_[bstack11ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩỘ")]):
        return False
    return True
def bstack111l1lll_opy_():
    try:
        from pytest_bdd import reporting
        bstack111l1l1ll1l_opy_ = os.environ.get(bstack11ll111_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡖࡕࡈࡖࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠣộ"), None)
        return bstack111l1l1ll1l_opy_ is None or bstack111l1l1ll1l_opy_ == bstack11ll111_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠨỚ")
    except Exception as e:
        return False
def bstack1l111lll11_opy_(hub_url, CONFIG):
    if bstack1ll1lll11_opy_() <= version.parse(bstack11ll111_opy_ (u"ࠪ࠷࠳࠷࠳࠯࠲ࠪớ")):
        if hub_url:
            return bstack11ll111_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧỜ") + hub_url + bstack11ll111_opy_ (u"ࠧࡀ࠸࠱࠱ࡺࡨ࠴࡮ࡵࡣࠤờ")
        return bstack1l11l11l11_opy_
    if hub_url:
        return bstack11ll111_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࠣỞ") + hub_url + bstack11ll111_opy_ (u"ࠢ࠰ࡹࡧ࠳࡭ࡻࡢࠣở")
    return HTTPS_HUB
def bstack111l111l111_opy_():
    return isinstance(os.getenv(bstack11ll111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑ࡛ࡗࡉࡘ࡚࡟ࡑࡎࡘࡋࡎࡔࠧỠ")), str)
def bstack1lllll1111_opy_(url):
    return urlparse(url).hostname
def bstack11lll1111l_opy_(hostname):
    for bstack11lll11l_opy_ in bstack1l1lllll11_opy_:
        regex = re.compile(bstack11lll11l_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack111l1l1lll1_opy_(bstack111l111l11l_opy_, file_name, logger):
    bstack11l111l11l_opy_ = os.path.join(os.path.expanduser(bstack11ll111_opy_ (u"ࠩࢁࠫỡ")), bstack111l111l11l_opy_)
    try:
        if not os.path.exists(bstack11l111l11l_opy_):
            os.makedirs(bstack11l111l11l_opy_)
        file_path = os.path.join(os.path.expanduser(bstack11ll111_opy_ (u"ࠪࢂࠬỢ")), bstack111l111l11l_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack11ll111_opy_ (u"ࠫࡼ࠭ợ")):
                pass
            with open(file_path, bstack11ll111_opy_ (u"ࠧࡽࠫࠣỤ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack11l11lll11_opy_.format(str(e)))
def bstack1111lll1ll1_opy_(file_name, key, value, logger):
    file_path = bstack111l1l1lll1_opy_(bstack11ll111_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ụ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack111llll1ll_opy_ = json.load(open(file_path, bstack11ll111_opy_ (u"ࠧࡳࡤࠪỦ")))
        else:
            bstack111llll1ll_opy_ = {}
        bstack111llll1ll_opy_[key] = value
        with open(file_path, bstack11ll111_opy_ (u"ࠣࡹ࠮ࠦủ")) as outfile:
            json.dump(bstack111llll1ll_opy_, outfile)
def bstack11lll1l111_opy_(file_name, logger):
    file_path = bstack111l1l1lll1_opy_(bstack11ll111_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩỨ"), file_name, logger)
    bstack111llll1ll_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack11ll111_opy_ (u"ࠪࡶࠬứ")) as bstack11l111l11_opy_:
            bstack111llll1ll_opy_ = json.load(bstack11l111l11_opy_)
    return bstack111llll1ll_opy_
def bstack11ll1111_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack11ll111_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡤࡦ࡮ࡨࡸ࡮ࡴࡧࠡࡨ࡬ࡰࡪࡀࠠࠨỪ") + file_path + bstack11ll111_opy_ (u"ࠬࠦࠧừ") + str(e))
def bstack1ll1lll11_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack11ll111_opy_ (u"ࠨ࠼ࡏࡑࡗࡗࡊ࡚࠾ࠣỬ")
def bstack1ll1lll1l1_opy_(config):
    if bstack11ll111_opy_ (u"ࠧࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ử") in config:
        del (config[bstack11ll111_opy_ (u"ࠨ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧỮ")])
        return False
    if bstack1ll1lll11_opy_() < version.parse(bstack11ll111_opy_ (u"ࠩ࠶࠲࠹࠴࠰ࠨữ")):
        return False
    if bstack1ll1lll11_opy_() >= version.parse(bstack11ll111_opy_ (u"ࠪ࠸࠳࠷࠮࠶ࠩỰ")):
        return True
    if bstack11ll111_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫự") in config and config[bstack11ll111_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬỲ")] is False:
        return False
    else:
        return True
def bstack11lllll111_opy_(args_list, bstack111l1l11ll1_opy_):
    index = -1
    for value in bstack111l1l11ll1_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
def bstack11l1l111111_opy_(a, b):
  for k, v in b.items():
    if isinstance(v, dict) and k in a and isinstance(a[k], dict):
        bstack11l1l111111_opy_(a[k], v)
    else:
        a[k] = v
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack1111ll1lll_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack1111ll1lll_opy_ = bstack1111ll1lll_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack11ll111_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ỳ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack11ll111_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧỴ"), exception=exception)
    def bstack1lll1ll11ll_opy_(self):
        if self.result != bstack11ll111_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨỵ"):
            return None
        if isinstance(self.exception_type, str) and bstack11ll111_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࠧỶ") in self.exception_type:
            return bstack11ll111_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࡋࡲࡳࡱࡵࠦỷ")
        return bstack11ll111_opy_ (u"࡚ࠦࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠧỸ")
    def bstack111l1l111ll_opy_(self):
        if self.result != bstack11ll111_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬỹ"):
            return None
        if self.bstack1111ll1lll_opy_:
            return self.bstack1111ll1lll_opy_
        return bstack111l11lll1l_opy_(self.exception)
def bstack111l11lll1l_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack111l11ll111_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack1lll11l111_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack1ll1llll11_opy_(config, logger):
    try:
        import playwright
        bstack1111lllll1l_opy_ = playwright.__file__
        bstack1111ll11l1l_opy_ = os.path.split(bstack1111lllll1l_opy_)
        bstack111l11ll11l_opy_ = bstack1111ll11l1l_opy_[0] + bstack11ll111_opy_ (u"࠭࠯ࡥࡴ࡬ࡺࡪࡸ࠯ࡱࡣࡦ࡯ࡦ࡭ࡥ࠰࡮࡬ࡦ࠴ࡩ࡬ࡪ࠱ࡦࡰ࡮࠴ࡪࡴࠩỺ")
        os.environ[bstack11ll111_opy_ (u"ࠧࡈࡎࡒࡆࡆࡒ࡟ࡂࡉࡈࡒ࡙ࡥࡈࡕࡖࡓࡣࡕࡘࡏ࡙࡛ࠪỻ")] = bstack1111lllll1_opy_(config)
        with open(bstack111l11ll11l_opy_, bstack11ll111_opy_ (u"ࠨࡴࠪỼ")) as f:
            bstack1l1111111_opy_ = f.read()
            bstack1111lll111l_opy_ = bstack11ll111_opy_ (u"ࠩࡪࡰࡴࡨࡡ࡭࠯ࡤ࡫ࡪࡴࡴࠨỽ")
            bstack1111ll11l11_opy_ = bstack1l1111111_opy_.find(bstack1111lll111l_opy_)
            if bstack1111ll11l11_opy_ == -1:
              process = subprocess.Popen(bstack11ll111_opy_ (u"ࠥࡲࡵࡳࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡩ࡯ࡳࡧࡧ࡬࠮ࡣࡪࡩࡳࡺࠢỾ"), shell=True, cwd=bstack1111ll11l1l_opy_[0])
              process.wait()
              bstack111l11ll1ll_opy_ = bstack11ll111_opy_ (u"ࠫࠧࡻࡳࡦࠢࡶࡸࡷ࡯ࡣࡵࠤ࠾ࠫỿ")
              bstack111l11l1ll1_opy_ = bstack11ll111_opy_ (u"ࠧࠨࠢࠡ࡞ࠥࡹࡸ࡫ࠠࡴࡶࡵ࡭ࡨࡺ࡜ࠣ࠽ࠣࡧࡴࡴࡳࡵࠢࡾࠤࡧࡵ࡯ࡵࡵࡷࡶࡦࡶࠠࡾࠢࡀࠤࡷ࡫ࡱࡶ࡫ࡵࡩ࠭࠭ࡧ࡭ࡱࡥࡥࡱ࠳ࡡࡨࡧࡱࡸࠬ࠯࠻ࠡ࡫ࡩࠤ࠭ࡶࡲࡰࡥࡨࡷࡸ࠴ࡥ࡯ࡸ࠱ࡋࡑࡕࡂࡂࡎࡢࡅࡌࡋࡎࡕࡡࡋࡘ࡙ࡖ࡟ࡑࡔࡒ࡜࡞࠯ࠠࡣࡱࡲࡸࡸࡺࡲࡢࡲࠫ࠭ࡀࠦࠢࠣࠤἀ")
              bstack1111ll1llll_opy_ = bstack1l1111111_opy_.replace(bstack111l11ll1ll_opy_, bstack111l11l1ll1_opy_)
              with open(bstack111l11ll11l_opy_, bstack11ll111_opy_ (u"࠭ࡷࠨἁ")) as f:
                f.write(bstack1111ll1llll_opy_)
    except Exception as e:
        logger.error(bstack1lll111111_opy_.format(str(e)))
def bstack11lllll1l1_opy_():
  try:
    bstack1111llll111_opy_ = os.path.join(tempfile.gettempdir(), bstack11ll111_opy_ (u"ࠧࡰࡲࡷ࡭ࡲࡧ࡬ࡠࡪࡸࡦࡤࡻࡲ࡭࠰࡭ࡷࡴࡴࠧἂ"))
    bstack111l1111lll_opy_ = []
    if os.path.exists(bstack1111llll111_opy_):
      with open(bstack1111llll111_opy_) as f:
        bstack111l1111lll_opy_ = json.load(f)
      os.remove(bstack1111llll111_opy_)
    return bstack111l1111lll_opy_
  except:
    pass
  return []
def bstack1l111111_opy_(bstack1ll1111l11_opy_):
  try:
    bstack111l1111lll_opy_ = []
    bstack1111llll111_opy_ = os.path.join(tempfile.gettempdir(), bstack11ll111_opy_ (u"ࠨࡱࡳࡸ࡮ࡳࡡ࡭ࡡ࡫ࡹࡧࡥࡵࡳ࡮࠱࡮ࡸࡵ࡮ࠨἃ"))
    if os.path.exists(bstack1111llll111_opy_):
      with open(bstack1111llll111_opy_) as f:
        bstack111l1111lll_opy_ = json.load(f)
    bstack111l1111lll_opy_.append(bstack1ll1111l11_opy_)
    with open(bstack1111llll111_opy_, bstack11ll111_opy_ (u"ࠩࡺࠫἄ")) as f:
        json.dump(bstack111l1111lll_opy_, f)
  except:
    pass
def bstack11ll1l11ll_opy_(logger, bstack111l1l1ll11_opy_ = False):
  try:
    test_name = os.environ.get(bstack11ll111_opy_ (u"ࠪࡔ࡞࡚ࡅࡔࡖࡢࡘࡊ࡙ࡔࡠࡐࡄࡑࡊ࠭ἅ"), bstack11ll111_opy_ (u"ࠫࠬἆ"))
    if test_name == bstack11ll111_opy_ (u"ࠬ࠭ἇ"):
        test_name = threading.current_thread().__dict__.get(bstack11ll111_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡈࡤࡥࡡࡷࡩࡸࡺ࡟࡯ࡣࡰࡩࠬἈ"), bstack11ll111_opy_ (u"ࠧࠨἉ"))
    bstack111l1lll11l_opy_ = bstack11ll111_opy_ (u"ࠨ࠮ࠣࠫἊ").join(threading.current_thread().bstackTestErrorMessages)
    if bstack111l1l1ll11_opy_:
        bstack1l111l111_opy_ = os.environ.get(bstack11ll111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩἋ"), bstack11ll111_opy_ (u"ࠪ࠴ࠬἌ"))
        bstack111l11llll_opy_ = {bstack11ll111_opy_ (u"ࠫࡳࡧ࡭ࡦࠩἍ"): test_name, bstack11ll111_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫἎ"): bstack111l1lll11l_opy_, bstack11ll111_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬἏ"): bstack1l111l111_opy_}
        bstack111l1111111_opy_ = []
        bstack111l1l1l111_opy_ = os.path.join(tempfile.gettempdir(), bstack11ll111_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡱࡲࡳࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴ࠯࡬ࡶࡳࡳ࠭ἐ"))
        if os.path.exists(bstack111l1l1l111_opy_):
            with open(bstack111l1l1l111_opy_) as f:
                bstack111l1111111_opy_ = json.load(f)
        bstack111l1111111_opy_.append(bstack111l11llll_opy_)
        with open(bstack111l1l1l111_opy_, bstack11ll111_opy_ (u"ࠨࡹࠪἑ")) as f:
            json.dump(bstack111l1111111_opy_, f)
    else:
        bstack111l11llll_opy_ = {bstack11ll111_opy_ (u"ࠩࡱࡥࡲ࡫ࠧἒ"): test_name, bstack11ll111_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩἓ"): bstack111l1lll11l_opy_, bstack11ll111_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪἔ"): str(multiprocessing.current_process().name)}
        if bstack11ll111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵࠩἕ") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack111l11llll_opy_)
  except Exception as e:
      logger.warn(bstack11ll111_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡸࡴࡸࡥࠡࡲࡼࡸࡪࡹࡴࠡࡨࡸࡲࡳ࡫࡬ࠡࡦࡤࡸࡦࡀࠠࡼࡿࠥ἖").format(e))
def bstack111lll111l_opy_(error_message, test_name, index, logger):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack11ll111_opy_ (u"ࠧࡧ࡫࡯ࡩࡱࡵࡣ࡬ࠢࡱࡳࡹࠦࡡࡷࡣ࡬ࡰࡦࡨ࡬ࡦ࠮ࠣࡹࡸ࡯࡮ࡨࠢࡥࡥࡸ࡯ࡣࠡࡨ࡬ࡰࡪࠦ࡯ࡱࡧࡵࡥࡹ࡯࡯࡯ࡵࠪ἗"))
    try:
      bstack1111l1l1ll1_opy_ = []
      bstack111l11llll_opy_ = {bstack11ll111_opy_ (u"ࠨࡰࡤࡱࡪ࠭Ἐ"): test_name, bstack11ll111_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨἙ"): error_message, bstack11ll111_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩἚ"): index}
      bstack1111ll1lll1_opy_ = os.path.join(tempfile.gettempdir(), bstack11ll111_opy_ (u"ࠫࡷࡵࡢࡰࡶࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬἛ"))
      if os.path.exists(bstack1111ll1lll1_opy_):
          with open(bstack1111ll1lll1_opy_) as f:
              bstack1111l1l1ll1_opy_ = json.load(f)
      bstack1111l1l1ll1_opy_.append(bstack111l11llll_opy_)
      with open(bstack1111ll1lll1_opy_, bstack11ll111_opy_ (u"ࠬࡽࠧἜ")) as f:
          json.dump(bstack1111l1l1ll1_opy_, f)
    except Exception as e:
      logger.warn(bstack11ll111_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡸࡴࡸࡥࠡࡴࡲࡦࡴࡺࠠࡧࡷࡱࡲࡪࡲࠠࡥࡣࡷࡥ࠿ࠦࡻࡾࠤἝ").format(e))
    return
  bstack1111l1l1ll1_opy_ = []
  bstack111l11llll_opy_ = {bstack11ll111_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ἞"): test_name, bstack11ll111_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ἟"): error_message, bstack11ll111_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨἠ"): index}
  bstack1111ll1lll1_opy_ = os.path.join(tempfile.gettempdir(), bstack11ll111_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠴ࡪࡴࡱࡱࠫἡ"))
  lock_file = bstack1111ll1lll1_opy_ + bstack11ll111_opy_ (u"ࠫ࠳ࡲ࡯ࡤ࡭ࠪἢ")
  try:
    with FileLock(lock_file, timeout=10):
      if os.path.exists(bstack1111ll1lll1_opy_):
          with open(bstack1111ll1lll1_opy_, bstack11ll111_opy_ (u"ࠬࡸࠧἣ")) as f:
              content = f.read().strip()
              if content:
                  bstack1111l1l1ll1_opy_ = json.load(open(bstack1111ll1lll1_opy_))
      bstack1111l1l1ll1_opy_.append(bstack111l11llll_opy_)
      with open(bstack1111ll1lll1_opy_, bstack11ll111_opy_ (u"࠭ࡷࠨἤ")) as f:
          json.dump(bstack1111l1l1ll1_opy_, f)
  except Exception as e:
    logger.warn(bstack11ll111_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡹࡵࡲࡦࠢࡵࡳࡧࡵࡴࠡࡨࡸࡲࡳ࡫࡬ࠡࡦࡤࡸࡦࠦࡷࡪࡶ࡫ࠤ࡫࡯࡬ࡦࠢ࡯ࡳࡨࡱࡩ࡯ࡩ࠽ࠤࢀࢃࠢἥ").format(e))
def bstack1l11l1lll_opy_(bstack11111l11l_opy_, name, logger):
  try:
    bstack111l11llll_opy_ = {bstack11ll111_opy_ (u"ࠨࡰࡤࡱࡪ࠭ἦ"): name, bstack11ll111_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨἧ"): bstack11111l11l_opy_, bstack11ll111_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩἨ"): str(threading.current_thread()._name)}
    return bstack111l11llll_opy_
  except Exception as e:
    logger.warn(bstack11ll111_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡶࡲࡶࡪࠦࡢࡦࡪࡤࡺࡪࠦࡦࡶࡰࡱࡩࡱࠦࡤࡢࡶࡤ࠾ࠥࢁࡽࠣἩ").format(e))
  return
def bstack111l1111l1l_opy_():
    return platform.system() == bstack11ll111_opy_ (u"ࠬ࡝ࡩ࡯ࡦࡲࡻࡸ࠭Ἢ")
def bstack11ll1llll1_opy_(bstack111l11l11l1_opy_, config, logger):
    bstack1111ll1l1l1_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack111l11l11l1_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack11ll111_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡩ࡭ࡱࡺࡥࡳࠢࡦࡳࡳ࡬ࡩࡨࠢ࡮ࡩࡾࡹࠠࡣࡻࠣࡶࡪ࡭ࡥࡹࠢࡰࡥࡹࡩࡨ࠻ࠢࡾࢁࠧἫ").format(e))
    return bstack1111ll1l1l1_opy_
def bstack111l1l11l1l_opy_(bstack1111l111lll_opy_, bstack111l1l1llll_opy_):
    bstack1111lll11ll_opy_ = version.parse(bstack1111l111lll_opy_)
    bstack1111ll1l111_opy_ = version.parse(bstack111l1l1llll_opy_)
    if bstack1111lll11ll_opy_ > bstack1111ll1l111_opy_:
        return 1
    elif bstack1111lll11ll_opy_ < bstack1111ll1l111_opy_:
        return -1
    else:
        return 0
def bstack1111111l11_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack111l1111l11_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
def bstack1111l1llll1_opy_(framework):
    from browserstack_sdk._version import __version__
    return str(framework) + str(__version__)
def bstack111ll11l11_opy_(options, framework, config, bstack1l11l1l1ll_opy_={}):
    if options is None:
        return
    if getattr(options, bstack11ll111_opy_ (u"ࠧࡨࡧࡷࠫἬ"), None):
        caps = options
    else:
        caps = options.to_capabilities()
    bstack1l1l1l11_opy_ = caps.get(bstack11ll111_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩἭ"))
    bstack1111l1l11ll_opy_ = True
    bstack111lllllll_opy_ = os.environ[bstack11ll111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧἮ")]
    bstack1l1l1ll111l_opy_ = config.get(bstack11ll111_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪἯ"), False)
    if bstack1l1l1ll111l_opy_:
        bstack1ll11llll1l_opy_ = config.get(bstack11ll111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫἰ"), {})
        bstack1ll11llll1l_opy_[bstack11ll111_opy_ (u"ࠬࡧࡵࡵࡪࡗࡳࡰ࡫࡮ࠨἱ")] = os.getenv(bstack11ll111_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫἲ"))
        bstack11l11ll1l1l_opy_ = json.loads(os.getenv(bstack11ll111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨἳ"), bstack11ll111_opy_ (u"ࠨࡽࢀࠫἴ"))).get(bstack11ll111_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪἵ"))
    if bstack1111l11llll_opy_(caps.get(bstack11ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡸࡷࡪ࡝࠳ࡄࠩἶ"))) or bstack1111l11llll_opy_(caps.get(bstack11ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡹࡸ࡫࡟ࡸ࠵ࡦࠫἷ"))):
        bstack1111l1l11ll_opy_ = False
    if bstack1ll1lll1l1_opy_({bstack11ll111_opy_ (u"ࠧࡻࡳࡦ࡙࠶ࡇࠧἸ"): bstack1111l1l11ll_opy_}):
        bstack1l1l1l11_opy_ = bstack1l1l1l11_opy_ or {}
        bstack1l1l1l11_opy_[bstack11ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨἹ")] = bstack1111l1llll1_opy_(framework)
        bstack1l1l1l11_opy_[bstack11ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩἺ")] = bstack1l11l1111ll_opy_()
        bstack1l1l1l11_opy_[bstack11ll111_opy_ (u"ࠨࡶࡨࡷࡹ࡮ࡵࡣࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫἻ")] = bstack111lllllll_opy_
        bstack1l1l1l11_opy_[bstack11ll111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫἼ")] = bstack1l11l1l1ll_opy_
        if bstack1l1l1ll111l_opy_:
            bstack1l1l1l11_opy_[bstack11ll111_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪἽ")] = bstack1l1l1ll111l_opy_
            bstack1l1l1l11_opy_[bstack11ll111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫἾ")] = bstack1ll11llll1l_opy_
            bstack1l1l1l11_opy_[bstack11ll111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬἿ")][bstack11ll111_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧὀ")] = bstack11l11ll1l1l_opy_
        if getattr(options, bstack11ll111_opy_ (u"ࠧࡴࡧࡷࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡹࠨὁ"), None):
            options.set_capability(bstack11ll111_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩὂ"), bstack1l1l1l11_opy_)
        else:
            options[bstack11ll111_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪὃ")] = bstack1l1l1l11_opy_
    else:
        if getattr(options, bstack11ll111_opy_ (u"ࠪࡷࡪࡺ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶࡼࠫὄ"), None):
            options.set_capability(bstack11ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬὅ"), bstack1111l1llll1_opy_(framework))
            options.set_capability(bstack11ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭὆"), bstack1l11l1111ll_opy_())
            options.set_capability(bstack11ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡺࡥࡴࡶ࡫ࡹࡧࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨ὇"), bstack111lllllll_opy_)
            options.set_capability(bstack11ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨὈ"), bstack1l11l1l1ll_opy_)
            if bstack1l1l1ll111l_opy_:
                options.set_capability(bstack11ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧὉ"), bstack1l1l1ll111l_opy_)
                options.set_capability(bstack11ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨὊ"), bstack1ll11llll1l_opy_)
                options.set_capability(bstack11ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴ࠰ࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪὋ"), bstack11l11ll1l1l_opy_)
        else:
            options[bstack11ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬὌ")] = bstack1111l1llll1_opy_(framework)
            options[bstack11ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭Ὅ")] = bstack1l11l1111ll_opy_()
            options[bstack11ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡺࡥࡴࡶ࡫ࡹࡧࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨ὎")] = bstack111lllllll_opy_
            options[bstack11ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨ὏")] = bstack1l11l1l1ll_opy_
            if bstack1l1l1ll111l_opy_:
                options[bstack11ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧὐ")] = bstack1l1l1ll111l_opy_
                options[bstack11ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨὑ")] = bstack1ll11llll1l_opy_
                options[bstack11ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩὒ")][bstack11ll111_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬὓ")] = bstack11l11ll1l1l_opy_
    return options
def bstack111l1ll111l_opy_(bstack111l11ll1l1_opy_, framework):
    bstack1l11l1l1ll_opy_ = global_config.get_property(bstack11ll111_opy_ (u"ࠧࡖࡌࡂ࡛࡚ࡖࡎࡍࡈࡕࡡࡓࡖࡔࡊࡕࡄࡖࡢࡑࡆࡖࠢὔ"))
    if bstack111l11ll1l1_opy_ and len(bstack111l11ll1l1_opy_.split(bstack11ll111_opy_ (u"࠭ࡣࡢࡲࡶࡁࠬὕ"))) > 1:
        ws_url = bstack111l11ll1l1_opy_.split(bstack11ll111_opy_ (u"ࠧࡤࡣࡳࡷࡂ࠭ὖ"))[0]
        if bstack11ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫὗ") in ws_url:
            from browserstack_sdk._version import __version__
            bstack1111l1ll111_opy_ = json.loads(urllib.parse.unquote(bstack111l11ll1l1_opy_.split(bstack11ll111_opy_ (u"ࠩࡦࡥࡵࡹ࠽ࠨ὘"))[1]))
            bstack1111l1ll111_opy_ = bstack1111l1ll111_opy_ or {}
            bstack111lllllll_opy_ = os.environ[bstack11ll111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨὙ")]
            bstack1111l1ll111_opy_[bstack11ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬ὚")] = str(framework) + str(__version__)
            bstack1111l1ll111_opy_[bstack11ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭Ὓ")] = bstack1l11l1111ll_opy_()
            bstack1111l1ll111_opy_[bstack11ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡺࡥࡴࡶ࡫ࡹࡧࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨ὜")] = bstack111lllllll_opy_
            bstack1111l1ll111_opy_[bstack11ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨὝ")] = bstack1l11l1l1ll_opy_
            bstack111l11ll1l1_opy_ = bstack111l11ll1l1_opy_.split(bstack11ll111_opy_ (u"ࠨࡥࡤࡴࡸࡃࠧ὞"))[0] + bstack11ll111_opy_ (u"ࠩࡦࡥࡵࡹ࠽ࠨὟ") + urllib.parse.quote(json.dumps(bstack1111l1ll111_opy_))
    return bstack111l11ll1l1_opy_
def bstack1l1l111l_opy_():
    global bstack1ll1l11lll_opy_
    from playwright._impl._browser_type import BrowserType
    bstack1ll1l11lll_opy_ = BrowserType.connect
    return bstack1ll1l11lll_opy_
def bstack11l11l11_opy_(framework_name):
    global bstack111l11111l_opy_
    bstack111l11111l_opy_ = framework_name
    return framework_name
def bstack1l1ll1lll1_opy_(self, *args, **kwargs):
    global bstack1ll1l11lll_opy_
    try:
        global bstack111l11111l_opy_
        if bstack11ll111_opy_ (u"ࠪࡻࡸࡋ࡮ࡥࡲࡲ࡭ࡳࡺࠧὠ") in kwargs:
            kwargs[bstack11ll111_opy_ (u"ࠫࡼࡹࡅ࡯ࡦࡳࡳ࡮ࡴࡴࠨὡ")] = bstack111l1ll111l_opy_(
                kwargs.get(bstack11ll111_opy_ (u"ࠬࡽࡳࡆࡰࡧࡴࡴ࡯࡮ࡵࠩὢ"), None),
                bstack111l11111l_opy_
            )
    except Exception as e:
        logger.error(bstack11ll111_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡦࡰࠣࡴࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡔࡆࡎࠤࡨࡧࡰࡴ࠼ࠣࡿࢂࠨὣ").format(str(e)))
    return bstack1ll1l11lll_opy_(self, *args, **kwargs)
def bstack111l11111l1_opy_(bstack1111ll11lll_opy_, proxies):
    proxy_settings = {}
    try:
        if not proxies:
            proxies = bstack1111llll1l_opy_(bstack1111ll11lll_opy_, bstack11ll111_opy_ (u"ࠢࠣὤ"))
        if proxies and proxies.get(bstack11ll111_opy_ (u"ࠣࡪࡷࡸࡵࡹࠢὥ")):
            parsed_url = urlparse(proxies.get(bstack11ll111_opy_ (u"ࠤ࡫ࡸࡹࡶࡳࠣὦ")))
            if parsed_url and parsed_url.hostname: proxy_settings[bstack11ll111_opy_ (u"ࠪࡴࡷࡵࡸࡺࡊࡲࡷࡹ࠭ὧ")] = str(parsed_url.hostname)
            if parsed_url and parsed_url.port: proxy_settings[bstack11ll111_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡓࡳࡷࡺࠧὨ")] = str(parsed_url.port)
            if parsed_url and parsed_url.username: proxy_settings[bstack11ll111_opy_ (u"ࠬࡶࡲࡰࡺࡼ࡙ࡸ࡫ࡲࠨὩ")] = str(parsed_url.username)
            if parsed_url and parsed_url.password: proxy_settings[bstack11ll111_opy_ (u"࠭ࡰࡳࡱࡻࡽࡕࡧࡳࡴࠩὪ")] = str(parsed_url.password)
        return proxy_settings
    except:
        return proxy_settings
def bstack1l111lllll_opy_(bstack1111ll11lll_opy_):
    bstack111l1l1l11l_opy_ = {
        bstack111llll11l1_opy_[bstack111l11l1lll_opy_]: bstack1111ll11lll_opy_[bstack111l11l1lll_opy_]
        for bstack111l11l1lll_opy_ in bstack1111ll11lll_opy_
        if bstack111l11l1lll_opy_ in bstack111llll11l1_opy_
    }
    bstack111l1l1l11l_opy_[bstack11ll111_opy_ (u"ࠢࡱࡴࡲࡼࡾ࡙ࡥࡵࡶ࡬ࡲ࡬ࡹࠢὫ")] = bstack111l11111l1_opy_(bstack1111ll11lll_opy_, global_config.get_property(bstack11ll111_opy_ (u"ࠣࡲࡵࡳࡽࡿࡓࡦࡶࡷ࡭ࡳ࡭ࡳࠣὬ")))
    bstack111l111llll_opy_ = [element.lower() for element in bstack111ll1l1l11_opy_]
    bstack111l11l11ll_opy_(bstack111l1l1l11l_opy_, bstack111l111llll_opy_)
    return bstack111l1l1l11l_opy_
def bstack111l11l11ll_opy_(d, keys):
    for key in list(d.keys()):
        if key.lower() in keys:
            d[key] = bstack11ll111_opy_ (u"ࠤ࠭࠮࠯࠰ࠢὭ")
    for value in d.values():
        if isinstance(value, dict):
            bstack111l11l11ll_opy_(value, keys)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    bstack111l11l11ll_opy_(item, keys)
def bstack1l11llll11l_opy_():
    bstack1111ll11111_opy_ = [os.environ.get(bstack11ll111_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡍࡑࡋࡓࡠࡆࡌࡖࠧὮ")), os.path.join(os.path.expanduser(bstack11ll111_opy_ (u"ࠦࢃࠨὯ")), bstack11ll111_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬὰ")), os.path.join(bstack11ll111_opy_ (u"࠭࠯ࡵ࡯ࡳࠫά"), bstack11ll111_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧὲ"))]
    for path in bstack1111ll11111_opy_:
        if path is None:
            continue
        try:
            if os.path.exists(path):
                logger.debug(bstack11ll111_opy_ (u"ࠣࡈ࡬ࡰࡪࠦࠧࠣέ") + str(path) + bstack11ll111_opy_ (u"ࠤࠪࠤࡪࡾࡩࡴࡶࡶ࠲ࠧὴ"))
                if not os.access(path, os.W_OK):
                    logger.debug(bstack11ll111_opy_ (u"ࠥࡋ࡮ࡼࡩ࡯ࡩࠣࡴࡪࡸ࡭ࡪࡵࡶ࡭ࡴࡴࡳࠡࡨࡲࡶࠥ࠭ࠢή") + str(path) + bstack11ll111_opy_ (u"ࠦࠬࠨὶ"))
                    os.chmod(path, 0o777)
                else:
                    logger.debug(bstack11ll111_opy_ (u"ࠧࡌࡩ࡭ࡧࠣࠫࠧί") + str(path) + bstack11ll111_opy_ (u"ࠨࠧࠡࡣ࡯ࡶࡪࡧࡤࡺࠢ࡫ࡥࡸࠦࡴࡩࡧࠣࡶࡪࡷࡵࡪࡴࡨࡨࠥࡶࡥࡳ࡯࡬ࡷࡸ࡯࡯࡯ࡵ࠱ࠦὸ"))
            else:
                logger.debug(bstack11ll111_opy_ (u"ࠢࡄࡴࡨࡥࡹ࡯࡮ࡨࠢࡩ࡭ࡱ࡫ࠠࠨࠤό") + str(path) + bstack11ll111_opy_ (u"ࠣࠩࠣࡻ࡮ࡺࡨࠡࡹࡵ࡭ࡹ࡫ࠠࡱࡧࡵࡱ࡮ࡹࡳࡪࡱࡱ࠲ࠧὺ"))
                os.makedirs(path, exist_ok=True)
                os.chmod(path, 0o777)
            logger.debug(bstack11ll111_opy_ (u"ࠤࡒࡴࡪࡸࡡࡵ࡫ࡲࡲࠥࡹࡵࡤࡥࡨࡩࡩ࡫ࡤࠡࡨࡲࡶࠥ࠭ࠢύ") + str(path) + bstack11ll111_opy_ (u"ࠥࠫ࠳ࠨὼ"))
            return path
        except Exception as e:
            logger.debug(bstack11ll111_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࠤࡺࡶࠠࡧ࡫࡯ࡩࠥ࠭ࡻࡱࡣࡷ࡬ࢂ࠭࠺ࠡࠤώ") + str(e) + bstack11ll111_opy_ (u"ࠧࠨ὾"))
    logger.debug(bstack11ll111_opy_ (u"ࠨࡁ࡭࡮ࠣࡴࡦࡺࡨࡴࠢࡩࡥ࡮ࡲࡥࡥ࠰ࠥ὿"))
    return None
@measure(event_name=EVENTS.bstack111ll1l1lll_opy_, stage=STAGE.bstack1111l1111_opy_)
def bstack1lllll1ll1l_opy_(binary_path, bstack1llllll1l11_opy_, bs_config):
    logger.debug(bstack11ll111_opy_ (u"ࠢࡄࡷࡵࡶࡪࡴࡴࠡࡅࡏࡍࠥࡖࡡࡵࡪࠣࡪࡴࡻ࡮ࡥ࠼ࠣࡿࢂࠨᾀ").format(binary_path))
    bstack1111lll1lll_opy_ = bstack11ll111_opy_ (u"ࠨࠩᾁ")
    bstack1111l1lll1l_opy_ = {
        bstack11ll111_opy_ (u"ࠩࡶࡨࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᾂ"): __version__,
        bstack11ll111_opy_ (u"ࠥࡳࡸࠨᾃ"): platform.system(),
        bstack11ll111_opy_ (u"ࠦࡴࡹ࡟ࡢࡴࡦ࡬ࠧᾄ"): platform.machine(),
        bstack11ll111_opy_ (u"ࠧࡩ࡬ࡪࡡࡹࡩࡷࡹࡩࡰࡰࠥᾅ"): bstack11ll111_opy_ (u"࠭࠰ࠨᾆ"),
        bstack11ll111_opy_ (u"ࠢࡴࡦ࡮ࡣࡱࡧ࡮ࡨࡷࡤ࡫ࡪࠨᾇ"): bstack11ll111_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨᾈ")
    }
    bstack1111ll1111l_opy_(bstack1111l1lll1l_opy_)
    try:
        if binary_path:
            if bstack111l1111l1l_opy_():
                bstack1111l1lll1l_opy_[bstack11ll111_opy_ (u"ࠩࡦࡰ࡮ࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᾉ")] = subprocess.check_output([binary_path, bstack11ll111_opy_ (u"ࠥࡺࡪࡸࡳࡪࡱࡱࠦᾊ")]).strip().decode(bstack11ll111_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪᾋ"))
            else:
                bstack1111l1lll1l_opy_[bstack11ll111_opy_ (u"ࠬࡩ࡬ࡪࡡࡹࡩࡷࡹࡩࡰࡰࠪᾌ")] = subprocess.check_output([binary_path, bstack11ll111_opy_ (u"ࠨࡶࡦࡴࡶ࡭ࡴࡴࠢᾍ")], stderr=subprocess.DEVNULL).strip().decode(bstack11ll111_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭ᾎ"))
        response = requests.request(
            bstack11ll111_opy_ (u"ࠨࡉࡈࡘࠬᾏ"),
            url=bstack1l1l1111ll_opy_(bstack111lll1lll1_opy_),
            headers=None,
            auth=(bs_config[bstack11ll111_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫᾐ")], bs_config[bstack11ll111_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ᾑ")]),
            json=None,
            params=bstack1111l1lll1l_opy_
        )
        data = response.json()
        if response.status_code == 200 and bstack11ll111_opy_ (u"ࠫࡺࡸ࡬ࠨᾒ") in data.keys() and bstack11ll111_opy_ (u"ࠬࡻࡰࡥࡣࡷࡩࡩࡥࡣ࡭࡫ࡢࡺࡪࡸࡳࡪࡱࡱࠫᾓ") in data.keys():
            logger.debug(bstack11ll111_opy_ (u"ࠨࡎࡦࡧࡧࠤࡹࡵࠠࡶࡲࡧࡥࡹ࡫ࠠࡣ࡫ࡱࡥࡷࡿࠬࠡࡥࡸࡶࡷ࡫࡮ࡵࠢࡥ࡭ࡳࡧࡲࡺࠢࡹࡩࡷࡹࡩࡰࡰ࠽ࠤࢀࢃࠢᾔ").format(bstack1111l1lll1l_opy_[bstack11ll111_opy_ (u"ࠧࡤ࡮࡬ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᾕ")]))
            if bstack11ll111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡋࡑࡅࡗ࡟࡟ࡖࡔࡏࠫᾖ") in os.environ:
                logger.debug(bstack11ll111_opy_ (u"ࠤࡖ࡯࡮ࡶࡰࡪࡰࡪࠤࡧ࡯࡮ࡢࡴࡼࠤࡩࡵࡷ࡯࡮ࡲࡥࡩࠦࡡࡴࠢࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡌࡒࡆࡘ࡙ࡠࡗࡕࡐࠥ࡯ࡳࠡࡵࡨࡸࠧᾗ"))
                data[bstack11ll111_opy_ (u"ࠪࡹࡷࡲࠧᾘ")] = os.environ[bstack11ll111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆࡎࡔࡁࡓ࡛ࡢ࡙ࡗࡒࠧᾙ")]
            bstack111l1l11lll_opy_ = bstack111l1l1l1ll_opy_(data[bstack11ll111_opy_ (u"ࠬࡻࡲ࡭ࠩᾚ")], bstack1llllll1l11_opy_)
            bstack1111lll1lll_opy_ = os.path.join(bstack1llllll1l11_opy_, bstack111l1l11lll_opy_)
            os.chmod(bstack1111lll1lll_opy_, 0o777) # bstack111l1llll11_opy_ permission
            return bstack1111lll1lll_opy_
    except Exception as e:
        logger.debug(bstack11ll111_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡩࡵࡷ࡯࡮ࡲࡥࡩ࡯࡮ࡨࠢࡱࡩࡼࠦࡓࡅࡍࠣࡿࢂࠨᾛ").format(e))
    return binary_path
def bstack1111ll1111l_opy_(bstack1111l1lll1l_opy_):
    try:
        if bstack11ll111_opy_ (u"ࠧ࡭࡫ࡱࡹࡽ࠭ᾜ") not in bstack1111l1lll1l_opy_[bstack11ll111_opy_ (u"ࠨࡱࡶࠫᾝ")].lower():
            return
        if os.path.exists(bstack11ll111_opy_ (u"ࠤ࠲ࡩࡹࡩ࠯ࡰࡵ࠰ࡶࡪࡲࡥࡢࡵࡨࠦᾞ")):
            with open(bstack11ll111_opy_ (u"ࠥ࠳ࡪࡺࡣ࠰ࡱࡶ࠱ࡷ࡫࡬ࡦࡣࡶࡩࠧᾟ"), bstack11ll111_opy_ (u"ࠦࡷࠨᾠ")) as f:
                bstack111l1ll1l11_opy_ = {}
                for line in f:
                    if bstack11ll111_opy_ (u"ࠧࡃࠢᾡ") in line:
                        key, value = line.rstrip().split(bstack11ll111_opy_ (u"ࠨ࠽ࠣᾢ"), 1)
                        bstack111l1ll1l11_opy_[key] = value.strip(bstack11ll111_opy_ (u"ࠧࠣ࡞ࠪࠫᾣ"))
                bstack1111l1lll1l_opy_[bstack11ll111_opy_ (u"ࠨࡦ࡬ࡷࡹࡸ࡯ࠨᾤ")] = bstack111l1ll1l11_opy_.get(bstack11ll111_opy_ (u"ࠤࡌࡈࠧᾥ"), bstack11ll111_opy_ (u"ࠥࠦᾦ"))
        elif os.path.exists(bstack11ll111_opy_ (u"ࠦ࠴࡫ࡴࡤ࠱ࡤࡰࡵ࡯࡮ࡦ࠯ࡵࡩࡱ࡫ࡡࡴࡧࠥᾧ")):
            bstack1111l1lll1l_opy_[bstack11ll111_opy_ (u"ࠬࡪࡩࡴࡶࡵࡳࠬᾨ")] = bstack11ll111_opy_ (u"࠭ࡡ࡭ࡲ࡬ࡲࡪ࠭ᾩ")
    except Exception as e:
        logger.debug(bstack11ll111_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣ࡫ࡪࡺࠠࡥ࡫ࡶࡸࡷࡵࠠࡰࡨࠣࡰ࡮ࡴࡵࡹࠤᾪ") + e)
@measure(event_name=EVENTS.bstack111lll111ll_opy_, stage=STAGE.bstack1111l1111_opy_)
def bstack111l1l1l1ll_opy_(bstack111l11111ll_opy_, bstack1111l11ll11_opy_):
    logger.debug(bstack11ll111_opy_ (u"ࠣࡆࡲࡻࡳࡲ࡯ࡢࡦ࡬ࡲ࡬ࠦࡓࡅࡍࠣࡦ࡮ࡴࡡࡳࡻࠣࡪࡷࡵ࡭࠻ࠢࠥᾫ") + str(bstack111l11111ll_opy_) + bstack11ll111_opy_ (u"ࠤࠥᾬ"))
    zip_path = os.path.join(bstack1111l11ll11_opy_, bstack11ll111_opy_ (u"ࠥࡨࡴࡽ࡮࡭ࡱࡤࡨࡪࡪ࡟ࡧ࡫࡯ࡩ࠳ࢀࡩࡱࠤᾭ"))
    bstack111l1l11lll_opy_ = bstack11ll111_opy_ (u"ࠫࠬᾮ")
    with requests.get(bstack111l11111ll_opy_, stream=True) as response:
        response.raise_for_status()
        with open(zip_path, bstack11ll111_opy_ (u"ࠧࡽࡢࠣᾯ")) as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        logger.debug(bstack11ll111_opy_ (u"ࠨࡆࡪ࡮ࡨࠤࡩࡵࡷ࡯࡮ࡲࡥࡩ࡫ࡤࠡࡵࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࡱࡿ࠮ࠣᾰ"))
    with zipfile.ZipFile(zip_path, bstack11ll111_opy_ (u"ࠧࡳࠩᾱ")) as zip_ref:
        bstack111l111ll1l_opy_ = zip_ref.namelist()
        if len(bstack111l111ll1l_opy_) > 0:
            bstack111l1l11lll_opy_ = bstack111l111ll1l_opy_[0] # bstack111l11l1l1l_opy_ bstack111lll1111l_opy_ will be bstack111l111111l_opy_ 1 file i.e. the binary in the zip
        zip_ref.extractall(bstack1111l11ll11_opy_)
        logger.debug(bstack11ll111_opy_ (u"ࠣࡈ࡬ࡰࡪࡹࠠࡴࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࡰࡾࠦࡥࡹࡶࡵࡥࡨࡺࡥࡥࠢࡷࡳࠥ࠭ࠢᾲ") + str(bstack1111l11ll11_opy_) + bstack11ll111_opy_ (u"ࠤࠪࠦᾳ"))
    os.remove(zip_path)
    return bstack111l1l11lll_opy_
def get_cli_dir():
    bstack111l1lll111_opy_ = bstack1l11llll11l_opy_()
    if bstack111l1lll111_opy_:
        bstack1llllll1l11_opy_ = os.path.join(bstack111l1lll111_opy_, bstack11ll111_opy_ (u"ࠥࡧࡱ࡯ࠢᾴ"))
        if not os.path.exists(bstack1llllll1l11_opy_):
            os.makedirs(bstack1llllll1l11_opy_, mode=0o777, exist_ok=True)
        return bstack1llllll1l11_opy_
    else:
        raise FileNotFoundError(bstack11ll111_opy_ (u"ࠦࡓࡵࠠࡸࡴ࡬ࡸࡦࡨ࡬ࡦࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥࡧࡶࡢ࡫࡯ࡥࡧࡲࡥࠡࡨࡲࡶࠥࡺࡨࡦࠢࡖࡈࡐࠦࡢࡪࡰࡤࡶࡾ࠴ࠢ᾵"))
def bstack1lllll1llll_opy_(bstack1llllll1l11_opy_):
    bstack11ll111_opy_ (u"ࠧࠨࠢࡈࡧࡷࠤࡹ࡮ࡥࠡࡲࡤࡸ࡭ࠦࡦࡰࡴࠣࡸ࡭࡫ࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡓࡅࡍࠣࡦ࡮ࡴࡡࡳࡻࠣ࡭ࡳࠦࡡࠡࡹࡵ࡭ࡹࡧࡢ࡭ࡧࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾ࠴ࠢࠣࠤᾶ")
    bstack1111lll1l11_opy_ = [
        os.path.join(bstack1llllll1l11_opy_, f)
        for f in os.listdir(bstack1llllll1l11_opy_)
        if os.path.isfile(os.path.join(bstack1llllll1l11_opy_, f)) and f.startswith(bstack11ll111_opy_ (u"ࠨࡢࡪࡰࡤࡶࡾ࠳ࠢᾷ"))
    ]
    if len(bstack1111lll1l11_opy_) > 0:
        return max(bstack1111lll1l11_opy_, key=os.path.getmtime) # get bstack111l1111ll1_opy_ binary
    return bstack11ll111_opy_ (u"ࠢࠣᾸ")
def bstack11l11lll1ll_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1l1l11lllll_opy_(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = bstack1l1l11lllll_opy_(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack1llll1ll_opy_(data, keys, default=None):
    bstack11ll111_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡕࡤࡪࡪࡲࡹࠡࡩࡨࡸࠥࡧࠠ࡯ࡧࡶࡸࡪࡪࠠࡷࡣ࡯ࡹࡪࠦࡦࡳࡱࡰࠤࡦࠦࡤࡪࡥࡷ࡭ࡴࡴࡡࡳࡻࠣࡳࡷࠦ࡬ࡪࡵࡷ࠲ࠏࠦࠠࠡࠢ࠽ࡴࡦࡸࡡ࡮ࠢࡧࡥࡹࡧ࠺ࠡࡖ࡫ࡩࠥࡪࡩࡤࡶ࡬ࡳࡳࡧࡲࡺࠢࡲࡶࠥࡲࡩࡴࡶࠣࡸࡴࠦࡴࡳࡣࡹࡩࡷࡹࡥ࠯ࠌࠣࠤࠥࠦ࠺ࡱࡣࡵࡥࡲࠦ࡫ࡦࡻࡶ࠾ࠥࡇࠠ࡭࡫ࡶࡸࠥࡵࡦࠡ࡭ࡨࡽࡸ࠵ࡩ࡯ࡦ࡬ࡧࡪࡹࠠࡳࡧࡳࡶࡪࡹࡥ࡯ࡶ࡬ࡲ࡬ࠦࡴࡩࡧࠣࡴࡦࡺࡨ࠯ࠌࠣࠤࠥࠦ࠺ࡱࡣࡵࡥࡲࠦࡤࡦࡨࡤࡹࡱࡺ࠺ࠡࡘࡤࡰࡺ࡫ࠠࡵࡱࠣࡶࡪࡺࡵࡳࡰࠣ࡭࡫ࠦࡴࡩࡧࠣࡴࡦࡺࡨࠡࡦࡲࡩࡸࠦ࡮ࡰࡶࠣࡩࡽ࡯ࡳࡵ࠰ࠍࠤࠥࠦࠠ࠻ࡴࡨࡸࡺࡸ࡮࠻ࠢࡗ࡬ࡪࠦࡶࡢ࡮ࡸࡩࠥࡧࡴࠡࡶ࡫ࡩࠥࡴࡥࡴࡶࡨࡨࠥࡶࡡࡵࡪ࠯ࠤࡴࡸࠠࡥࡧࡩࡥࡺࡲࡴࠡ࡫ࡩࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪ࠮ࠋࠢࠣࠤࠥࠨࠢࠣᾹ")
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
def bstack11l1l11l11_opy_(bstack111l111l1l1_opy_, key, value):
    bstack11ll111_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࡖࡸࡴࡸࡥࠡࡅࡏࡍࠥ࡫࡮ࡷ࡫ࡵࡳࡳࡳࡥ࡯ࡶࠣࡺࡦࡸࡩࡢࡤ࡯ࡩࡸࠦ࡭ࡢࡲࡳ࡭ࡳ࡭ࠠࡪࡰࠣࡸ࡭࡫ࠠࡱࡴࡲࡺ࡮ࡪࡥࡥࠢࡧ࡭ࡨࡺࡩࡰࡰࡤࡶࡾ࠴ࠊࠡࠢࠣࠤࡆࡸࡧࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡨࡲࡩࡠࡧࡱࡺࡤࡼࡡࡳࡵࡢࡱࡦࡶ࠺ࠡࡆ࡬ࡧࡹ࡯࡯࡯ࡣࡵࡽࠥࡺ࡯ࠡࡵࡷࡳࡷ࡫ࠠࡦࡰࡹ࡭ࡷࡵ࡮࡮ࡧࡱࡸࠥࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠠ࡮ࡣࡳࡴ࡮ࡴࡧࡴࠌࠣࠤࠥࠦࠠࠡࠢࠣ࡯ࡪࡿ࠺ࠡࡍࡨࡽࠥ࡬ࡲࡰ࡯ࠣࡇࡑࡏ࡟ࡄࡃࡓࡗࡤ࡚ࡏࡠࡅࡒࡒࡋࡏࡇࠋࠢࠣࠤࠥࠦࠠࠡࠢࡹࡥࡱࡻࡥ࠻࡙ࠢࡥࡱࡻࡥࠡࡨࡵࡳࡲࠦࡣࡰ࡯ࡰࡥࡳࡪࠠ࡭࡫ࡱࡩࠥࡧࡲࡨࡷࡰࡩࡳࡺࡳࠋࠢࠣࠤࠥࠨࠢࠣᾺ")
    if key in bstack1l11llll11_opy_:
        bstack111llll1l_opy_ = bstack1l11llll11_opy_[key]
        if isinstance(bstack111llll1l_opy_, list):
            for env_name in bstack111llll1l_opy_:
                bstack111l111l1l1_opy_[env_name] = value
        else:
            bstack111l111l1l1_opy_[bstack111llll1l_opy_] = value