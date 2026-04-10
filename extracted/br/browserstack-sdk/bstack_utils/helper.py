# coding: UTF-8
import sys
bstack11l11ll_opy_ = sys.version_info [0] == 2
bstack1l1ll11_opy_ = 2048
bstack1ll1l_opy_ = 7
def bstack1ll_opy_ (bstack1l11l1_opy_):
    global bstack1l1l1l1_opy_
    bstack111_opy_ = ord (bstack1l11l1_opy_ [-1])
    bstack11111l_opy_ = bstack1l11l1_opy_ [:-1]
    bstack11l111_opy_ = bstack111_opy_ % len (bstack11111l_opy_)
    bstack1lll11_opy_ = bstack11111l_opy_ [:bstack11l111_opy_] + bstack11111l_opy_ [bstack11l111_opy_:]
    if bstack11l11ll_opy_:
        bstack1ll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    else:
        bstack1ll1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    return eval (bstack1ll1l1_opy_)
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
from bstack_utils.constants import (bstack1111ll1ll1_opy_, bstack1lllll1l1l_opy_, bstack111l11lll1_opy_,
                                    bstack1111111llll_opy_, bstack11111l111l1_opy_, bstack111111ll11l_opy_, bstack111111lllll_opy_)
from bstack_utils.measure import measure
from bstack_utils.messages import bstack1l1l1111_opy_, bstack111l11ll11_opy_
from bstack_utils.proxy import bstack11l11ll11_opy_, bstack11lllll1_opy_
from bstack_utils.constants import *
from bstack_utils import logger_utils
from bstack_utils.bstack1l1lll1l_opy_ import bstack1l11llll1_opy_
from browserstack_sdk._version import __version__
global_config = Config.bstack1l111l1111_opy_()
logger = logger_utils.get_logger(__name__, logger_utils.get_log_level())
automation_logger = logger_utils.get_automation_logger(__name__)
def bstack1111l1l111l_opy_(config):
    return config[bstack1ll_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩⅱ")]
def bstack1111ll1l11l_opy_(config):
    return config[bstack1ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫⅲ")]
def bstack1l1111l1l1_opy_():
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
def bstack1llll11llll1_opy_(obj):
    values = []
    bstack1llll111l11l_opy_ = re.compile(bstack1ll_opy_ (u"ࡴࠥࡢࡈ࡛ࡓࡕࡑࡐࡣ࡙ࡇࡇࡠ࡞ࡧ࠯ࠩࠨⅳ"), re.I)
    for key in obj.keys():
        if bstack1llll111l11l_opy_.match(key):
            values.append(obj[key])
    return values
def bstack1llll11lll1l_opy_(config):
    tags = []
    tags.extend(bstack1llll11llll1_opy_(os.environ))
    tags.extend(bstack1llll11llll1_opy_(config))
    return tags
def bstack1llll111llll_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack1llll11111l1_opy_(bstack1lllll1l11l1_opy_):
    if not bstack1lllll1l11l1_opy_:
        return bstack1ll_opy_ (u"ࠪࠫⅴ")
    return bstack1ll_opy_ (u"ࠦࢀࢃࠠࠩࡽࢀ࠭ࠧⅵ").format(bstack1lllll1l11l1_opy_.name, bstack1lllll1l11l1_opy_.email)
def bstack1111lll1l11_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack1llll1ll1ll1_opy_ = repo.common_dir
        info = {
            bstack1ll_opy_ (u"ࠧࡹࡨࡢࠤⅶ"): repo.head.commit.hexsha,
            bstack1ll_opy_ (u"ࠨࡳࡩࡱࡵࡸࡤࡹࡨࡢࠤⅷ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack1ll_opy_ (u"ࠢࡣࡴࡤࡲࡨ࡮ࠢⅸ"): repo.active_branch.name,
            bstack1ll_opy_ (u"ࠣࡶࡤ࡫ࠧⅹ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack1ll_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡶࡨࡶࠧⅺ"): bstack1llll11111l1_opy_(repo.head.commit.committer),
            bstack1ll_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡷࡩࡷࡥࡤࡢࡶࡨࠦⅻ"): repo.head.commit.committed_datetime.isoformat(),
            bstack1ll_opy_ (u"ࠦࡦࡻࡴࡩࡱࡵࠦⅼ"): bstack1llll11111l1_opy_(repo.head.commit.author),
            bstack1ll_opy_ (u"ࠧࡧࡵࡵࡪࡲࡶࡤࡪࡡࡵࡧࠥⅽ"): repo.head.commit.authored_datetime.isoformat(),
            bstack1ll_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡥ࡭ࡦࡵࡶࡥ࡬࡫ࠢⅾ"): repo.head.commit.message,
            bstack1ll_opy_ (u"ࠢࡳࡱࡲࡸࠧⅿ"): repo.git.rev_parse(bstack1ll_opy_ (u"ࠣ࠯࠰ࡷ࡭ࡵࡷ࠮ࡶࡲࡴࡱ࡫ࡶࡦ࡮ࠥↀ")),
            bstack1ll_opy_ (u"ࠤࡦࡳࡲࡳ࡯࡯ࡡࡪ࡭ࡹࡥࡤࡪࡴࠥↁ"): bstack1llll1ll1ll1_opy_,
            bstack1ll_opy_ (u"ࠥࡻࡴࡸ࡫ࡵࡴࡨࡩࡤ࡭ࡩࡵࡡࡧ࡭ࡷࠨↂ"): subprocess.check_output([bstack1ll_opy_ (u"ࠦ࡬࡯ࡴࠣↃ"), bstack1ll_opy_ (u"ࠧࡸࡥࡷ࠯ࡳࡥࡷࡹࡥࠣↄ"), bstack1ll_opy_ (u"ࠨ࠭࠮ࡩ࡬ࡸ࠲ࡩ࡯࡮࡯ࡲࡲ࠲ࡪࡩࡳࠤↅ")]).strip().decode(
                bstack1ll_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭ↆ")),
            bstack1ll_opy_ (u"ࠣ࡮ࡤࡷࡹࡥࡴࡢࡩࠥↇ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack1ll_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡵࡢࡷ࡮ࡴࡣࡦࡡ࡯ࡥࡸࡺ࡟ࡵࡣࡪࠦↈ"): repo.git.rev_list(
                bstack1ll_opy_ (u"ࠥࡿࢂ࠴࠮ࡼࡿࠥ↉").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack1lllll111l1l_opy_ = []
        for remote in remotes:
            bstack1lllll11llll_opy_ = {
                bstack1ll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ↊"): remote.name,
                bstack1ll_opy_ (u"ࠧࡻࡲ࡭ࠤ↋"): remote.url,
            }
            bstack1lllll111l1l_opy_.append(bstack1lllll11llll_opy_)
        bstack1lllll1l111l_opy_ = {
            bstack1ll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ↌"): bstack1ll_opy_ (u"ࠢࡨ࡫ࡷࠦ↍"),
            **info,
            bstack1ll_opy_ (u"ࠣࡴࡨࡱࡴࡺࡥࡴࠤ↎"): bstack1lllll111l1l_opy_
        }
        bstack1lllll1l111l_opy_ = bstack1llll1l1l1ll_opy_(bstack1lllll1l111l_opy_)
        return bstack1lllll1l111l_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack1ll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡲࡴࡺࡲࡡࡵ࡫ࡱ࡫ࠥࡍࡩࡵࠢࡰࡩࡹࡧࡤࡢࡶࡤࠤࡼ࡯ࡴࡩࠢࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠧ↏").format(err))
        return {}
def bstack1llll1ll111l_opy_(bstack1llll11l1ll1_opy_=None):
    bstack1ll_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࡋࡪࡺࠠࡨ࡫ࡷࠤࡲ࡫ࡴࡢࡦࡤࡸࡦࠦࡳࡱࡧࡦ࡭࡫࡯ࡣࡢ࡮࡯ࡽࠥ࡬࡯ࡳ࡯ࡤࡸࡹ࡫ࡤࠡࡨࡲࡶࠥࡇࡉࠡࡵࡨࡰࡪࡩࡴࡪࡱࡱࠤࡺࡹࡥࠡࡥࡤࡷࡪࡹࠠࡧࡱࡵࠤࡪࡧࡣࡩࠢࡩࡳࡱࡪࡥࡳࠢ࡬ࡲࠥࡺࡨࡦࠢ࡯࡭ࡸࡺ࠮ࠋࠢࠣࠤࠥࡇࡲࡨࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥ࡬࡯࡭ࡦࡨࡶࡸࠦࠨ࡭࡫ࡶࡸ࠱ࠦ࡯ࡱࡶ࡬ࡳࡳࡧ࡬ࠪ࠼ࠣࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡓࡵ࡮ࡦ࠼ࠣࡑࡴࡴ࡯࠮ࡴࡨࡴࡴࠦࡡࡱࡲࡵࡳࡦࡩࡨ࠭ࠢࡸࡷࡪࡹࠠࡤࡷࡵࡶࡪࡴࡴࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼࠤࡠࡵࡳ࠯ࡩࡨࡸࡨࡽࡤࠩࠫࡠࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡊࡳࡰࡵࡻࠣࡰ࡮ࡹࡴࠡ࡝ࡠ࠾ࠥࡓࡵ࡭ࡶ࡬࠱ࡷ࡫ࡰࡰࠢࡤࡴࡵࡸ࡯ࡢࡥ࡫ࠤࡼ࡯ࡴࡩࠢࡱࡳࠥࡹ࡯ࡶࡴࡦࡩࡸࠦࡣࡰࡰࡩ࡭࡬ࡻࡲࡦࡦ࠯ࠤࡷ࡫ࡴࡶࡴࡱࡷࠥࡡ࡝ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡎ࡬ࡷࡹࠦ࡯ࡧࠢࡳࡥࡹ࡮ࡳ࠻ࠢࡐࡹࡱࡺࡩ࠮ࡴࡨࡴࡴࠦࡡࡱࡲࡵࡳࡦࡩࡨࠡࡹ࡬ࡸ࡭ࠦࡳࡱࡧࡦ࡭࡫࡯ࡣࠡࡨࡲࡰࡩ࡫ࡲࡴࠢࡷࡳࠥࡧ࡮ࡢ࡮ࡼࡾࡪࠐࠠࠡࠢࠣࡖࡪࡺࡵࡳࡰࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦ࡬ࡪࡵࡷ࠾ࠥࡒࡩࡴࡶࠣࡳ࡫ࠦࡤࡪࡥࡷࡷ࠱ࠦࡥࡢࡥ࡫ࠤࡨࡵ࡮ࡵࡣ࡬ࡲ࡮ࡴࡧࠡࡩ࡬ࡸࠥࡳࡥࡵࡣࡧࡥࡹࡧࠠࡧࡱࡵࠤࡦࠦࡦࡰ࡮ࡧࡩࡷ࠴ࠊࠡࠢࠣࠤࠧࠨࠢ←")
    if bstack1llll11l1ll1_opy_ is None:
        bstack1llll11l1ll1_opy_ = [os.getcwd()]
    elif isinstance(bstack1llll11l1ll1_opy_, list) and len(bstack1llll11l1ll1_opy_) == 0:
        return []
    results = []
    for folder in bstack1llll11l1ll1_opy_:
        try:
            if not os.path.exists(folder):
                raise Exception(bstack1ll_opy_ (u"ࠦࡋࡵ࡬ࡥࡧࡵࠤࡩࡵࡥࡴࠢࡱࡳࡹࠦࡥࡹ࡫ࡶࡸ࠿ࠦࡻࡾࠤ↑").format(folder))
            repo = git.Repo(folder, search_parent_directories=True)
            result = {
                bstack1ll_opy_ (u"ࠧࡶࡲࡊࡦࠥ→"): bstack1ll_opy_ (u"ࠨࠢ↓"),
                bstack1ll_opy_ (u"ࠢࡧ࡫࡯ࡩࡸࡉࡨࡢࡰࡪࡩࡩࠨ↔"): [],
                bstack1ll_opy_ (u"ࠣࡣࡸࡸ࡭ࡵࡲࡴࠤ↕"): [],
                bstack1ll_opy_ (u"ࠤࡳࡶࡉࡧࡴࡦࠤ↖"): bstack1ll_opy_ (u"ࠥࠦ↗"),
                bstack1ll_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡑࡪࡹࡳࡢࡩࡨࡷࠧ↘"): [],
                bstack1ll_opy_ (u"ࠧࡶࡲࡕ࡫ࡷࡰࡪࠨ↙"): bstack1ll_opy_ (u"ࠨࠢ↚"),
                bstack1ll_opy_ (u"ࠢࡱࡴࡇࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠢ↛"): bstack1ll_opy_ (u"ࠣࠤ↜"),
                bstack1ll_opy_ (u"ࠤࡳࡶࡗࡧࡷࡅ࡫ࡩࡪࠧ↝"): bstack1ll_opy_ (u"ࠥࠦ↞")
            }
            bstack1llll1l1l11l_opy_ = repo.active_branch.name
            bstack1llll11l11ll_opy_ = repo.head.commit
            result[bstack1ll_opy_ (u"ࠦࡵࡸࡉࡥࠤ↟")] = bstack1llll11l11ll_opy_.hexsha
            bstack1llll1l11ll1_opy_ = _1lllll1l1l1l_opy_(repo)
            logger.debug(bstack1ll_opy_ (u"ࠧࡈࡡࡴࡧࠣࡦࡷࡧ࡮ࡤࡪࠣࡪࡴࡸࠠࡤࡱࡰࡴࡦࡸࡩࡴࡱࡱ࠾ࠥࠨ↠") + str(bstack1llll1l11ll1_opy_) + bstack1ll_opy_ (u"ࠨࠢ↡"))
            if bstack1llll1l11ll1_opy_:
                try:
                    bstack1llll1llllll_opy_ = repo.git.diff(bstack1ll_opy_ (u"ࠢ࠮࠯ࡱࡥࡲ࡫࠭ࡰࡰ࡯ࡽࠧ↢"), bstack1l1ll1111l1_opy_ (u"ࠣࡽࡥࡥࡸ࡫࡟ࡣࡴࡤࡲࡨ࡮ࡽ࠯࠰࠱ࡿࡨࡻࡲࡳࡧࡱࡸࡤࡨࡲࡢࡰࡦ࡬ࢂࠨ↣")).split(bstack1ll_opy_ (u"ࠩ࡟ࡲࠬ↤"))
                    logger.debug(bstack1ll_opy_ (u"ࠥࡇ࡭ࡧ࡮ࡨࡧࡧࠤ࡫࡯࡬ࡦࡵࠣࡦࡪࡺࡷࡦࡧࡱࠤࢀࡨࡡࡴࡧࡢࡦࡷࡧ࡮ࡤࡪࢀࠤࡦࡴࡤࠡࡽࡦࡹࡷࡸࡥ࡯ࡶࡢࡦࡷࡧ࡮ࡤࡪࢀ࠾ࠥࠨ↥") + str(bstack1llll1llllll_opy_) + bstack1ll_opy_ (u"ࠦࠧ↦"))
                    result[bstack1ll_opy_ (u"ࠧ࡬ࡩ࡭ࡧࡶࡇ࡭ࡧ࡮ࡨࡧࡧࠦ↧")] = [f.strip() for f in bstack1llll1llllll_opy_ if f.strip()]
                    commits = list(repo.iter_commits(bstack1l1ll1111l1_opy_ (u"ࠨࡻࡣࡣࡶࡩࡤࡨࡲࡢࡰࡦ࡬ࢂ࠴࠮ࡼࡥࡸࡶࡷ࡫࡮ࡵࡡࡥࡶࡦࡴࡣࡩࡿࠥ↨")))
                except Exception:
                    logger.debug(bstack1ll_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣ࡫ࡪࡺࠠࡤࡪࡤࡲ࡬࡫ࡤࠡࡨ࡬ࡰࡪࡹࠠࡧࡴࡲࡱࠥࡨࡲࡢࡰࡦ࡬ࠥࡩ࡯࡮ࡲࡤࡶ࡮ࡹ࡯࡯࠰ࠣࡊࡦࡲ࡬ࡪࡰࡪࠤࡧࡧࡣ࡬ࠢࡷࡳࠥࡸࡥࡤࡧࡱࡸࠥࡩ࡯࡮࡯࡬ࡸࡸ࠴ࠢ↩"))
                    commits = list(repo.iter_commits(max_count=10))
                    if commits:
                        result[bstack1ll_opy_ (u"ࠣࡨ࡬ࡰࡪࡹࡃࡩࡣࡱ࡫ࡪࡪࠢ↪")] = _1llllll1llll_opy_(commits[:5])
            else:
                commits = list(repo.iter_commits(max_count=10))
                if commits:
                    result[bstack1ll_opy_ (u"ࠤࡩ࡭ࡱ࡫ࡳࡄࡪࡤࡲ࡬࡫ࡤࠣ↫")] = _1llllll1llll_opy_(commits[:5])
            bstack1llll11l1111_opy_ = set()
            bstack1llll11l11l1_opy_ = []
            for commit in commits:
                logger.debug(bstack1ll_opy_ (u"ࠥࡔࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡤࡱࡰࡱ࡮ࡺ࠺ࠡࠤ↬") + str(commit.message) + bstack1ll_opy_ (u"ࠦࠧ↭"))
                bstack1lllll1ll1ll_opy_ = commit.author.name if commit.author else bstack1ll_opy_ (u"࡛ࠧ࡮࡬ࡰࡲࡻࡳࠨ↮")
                bstack1llll11l1111_opy_.add(bstack1lllll1ll1ll_opy_)
                bstack1llll11l11l1_opy_.append({
                    bstack1ll_opy_ (u"ࠨ࡭ࡦࡵࡶࡥ࡬࡫ࠢ↯"): commit.message.strip(),
                    bstack1ll_opy_ (u"ࠢࡶࡵࡨࡶࠧ↰"): bstack1lllll1ll1ll_opy_
                })
            result[bstack1ll_opy_ (u"ࠣࡣࡸࡸ࡭ࡵࡲࡴࠤ↱")] = list(bstack1llll11l1111_opy_)
            result[bstack1ll_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡏࡨࡷࡸࡧࡧࡦࡵࠥ↲")] = bstack1llll11l11l1_opy_
            result[bstack1ll_opy_ (u"ࠥࡴࡷࡊࡡࡵࡧࠥ↳")] = bstack1llll11l11ll_opy_.committed_datetime.strftime(bstack1ll_opy_ (u"ࠦࠪ࡟࠭ࠦ࡯࠰ࠩࡩࠨ↴"))
            if (not result[bstack1ll_opy_ (u"ࠧࡶࡲࡕ࡫ࡷࡰࡪࠨ↵")] or result[bstack1ll_opy_ (u"ࠨࡰࡳࡖ࡬ࡸࡱ࡫ࠢ↶")].strip() == bstack1ll_opy_ (u"ࠢࠣ↷")) and bstack1llll11l11ll_opy_.message:
                bstack1llll1l1l1l1_opy_ = bstack1llll11l11ll_opy_.message.strip().splitlines()
                result[bstack1ll_opy_ (u"ࠣࡲࡵࡘ࡮ࡺ࡬ࡦࠤ↸")] = bstack1llll1l1l1l1_opy_[0] if bstack1llll1l1l1l1_opy_ else bstack1ll_opy_ (u"ࠤࠥ↹")
                if len(bstack1llll1l1l1l1_opy_) > 2:
                    result[bstack1ll_opy_ (u"ࠥࡴࡷࡊࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠥ↺")] = bstack1ll_opy_ (u"ࠫࡡࡴࠧ↻").join(bstack1llll1l1l1l1_opy_[2:]).strip()
            results.append(result)
        except Exception as err:
            logger.error(bstack1ll_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡵࡰࡶ࡮ࡤࡸ࡮ࡴࡧࠡࡉ࡬ࡸࠥࡳࡥࡵࡣࡧࡥࡹࡧࠠࡧࡱࡵࠤࡆࡏࠠࡴࡧ࡯ࡩࡨࡺࡩࡰࡰࠣࠬ࡫ࡵ࡬ࡥࡧࡵ࠾ࠥࢁࡽࠪ࠼ࠣࡿࢂࠦ࠭ࠡࡽࢀࠦ↼").format(
                folder,
                type(err).__name__,
                str(err)
            ))
    bstack1lllll1111ll_opy_ = [
        result
        for result in results
        if _1llllll1ll11_opy_(result)
    ]
    return bstack1lllll1111ll_opy_
def _1llllll1ll11_opy_(result):
    bstack1ll_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡈࡦ࡮ࡳࡩࡷࠦࡴࡰࠢࡦ࡬ࡪࡩ࡫ࠡ࡫ࡩࠤࡦࠦࡧࡪࡶࠣࡱࡪࡺࡡࡥࡣࡷࡥࠥࡸࡥࡴࡷ࡯ࡸࠥ࡯ࡳࠡࡸࡤࡰ࡮ࡪࠠࠩࡰࡲࡲ࠲࡫࡭ࡱࡶࡼࠤ࡫࡯࡬ࡦࡵࡆ࡬ࡦࡴࡧࡦࡦࠣࡥࡳࡪࠠࡢࡷࡷ࡬ࡴࡸࡳࠪ࠰ࠍࠤࠥࠦࠠࠣࠤࠥ↽")
    return (
        isinstance(result.get(bstack1ll_opy_ (u"ࠢࡧ࡫࡯ࡩࡸࡉࡨࡢࡰࡪࡩࡩࠨ↾"), None), list)
        and len(result[bstack1ll_opy_ (u"ࠣࡨ࡬ࡰࡪࡹࡃࡩࡣࡱ࡫ࡪࡪࠢ↿")]) > 0
        and isinstance(result.get(bstack1ll_opy_ (u"ࠤࡤࡹࡹ࡮࡯ࡳࡵࠥ⇀"), None), list)
        and len(result[bstack1ll_opy_ (u"ࠥࡥࡺࡺࡨࡰࡴࡶࠦ⇁")]) > 0
    )
def _1lllll1l1l1l_opy_(repo):
    bstack1ll_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤ࡙ࡸࡹࠡࡶࡲࠤࡩ࡫ࡴࡦࡴࡰ࡭ࡳ࡫ࠠࡵࡪࡨࠤࡧࡧࡳࡦࠢࡥࡶࡦࡴࡣࡩࠢࡩࡳࡷࠦࡴࡩࡧࠣ࡫࡮ࡼࡥ࡯ࠢࡵࡩࡵࡵࠠࡸ࡫ࡷ࡬ࡴࡻࡴࠡࡪࡤࡶࡩࡩ࡯ࡥࡧࡧࠤࡳࡧ࡭ࡦࡵࠣࡥࡳࡪࠠࡸࡱࡵ࡯ࠥࡽࡩࡵࡪࠣࡥࡱࡲࠠࡗࡅࡖࠤࡵࡸ࡯ࡷ࡫ࡧࡩࡷࡹ࠮ࠋࠢࠣࠤࠥࡘࡥࡵࡷࡵࡲࡸࠦࡴࡩࡧࠣࡨࡪ࡬ࡡࡶ࡮ࡷࠤࡧࡸࡡ࡯ࡥ࡫ࠤ࡮࡬ࠠࡱࡱࡶࡷ࡮ࡨ࡬ࡦ࠮ࠣࡩࡱࡹࡥࠡࡐࡲࡲࡪ࠴ࠊࠡࠢࠣࠤࠧࠨࠢ⇂")
    try:
        try:
            origin = repo.remotes.origin
            bstack1lllll1l1ll1_opy_ = origin.refs[bstack1ll_opy_ (u"ࠬࡎࡅࡂࡆࠪ⇃")]
            target = bstack1lllll1l1ll1_opy_.reference.name
            if target.startswith(bstack1ll_opy_ (u"࠭࡯ࡳ࡫ࡪ࡭ࡳ࠵ࠧ⇄")):
                return target
        except Exception:
            pass
        if repo.remotes and repo.remotes.origin.refs:
            for ref in repo.remotes.origin.refs:
                if ref.name.startswith(bstack1ll_opy_ (u"ࠧࡰࡴ࡬࡫࡮ࡴ࠯ࠨ⇅")):
                    return ref.name
        if repo.heads:
            return repo.heads[0].name
    except Exception:
        pass
    return None
def _1llllll1llll_opy_(commits):
    bstack1ll_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡉࡨࡸࠥࡲࡩࡴࡶࠣࡳ࡫ࠦࡣࡩࡣࡱ࡫ࡪࡪࠠࡧ࡫࡯ࡩࡸࠦࡦࡳࡱࡰࠤࡦࠦ࡬ࡪࡵࡷࠤࡴ࡬ࠠࡤࡱࡰࡱ࡮ࡺࡳ࠯ࠌࠣࠤࠥࠦࠢࠣࠤ⇆")
    bstack1llll1llllll_opy_ = set()
    try:
        for commit in commits:
            if commit.parents:
                for parent in commit.parents:
                    diff = commit.diff(parent)
                    for bstack1lllllll11ll_opy_ in diff:
                        if bstack1lllllll11ll_opy_.a_path:
                            bstack1llll1llllll_opy_.add(bstack1lllllll11ll_opy_.a_path)
                        if bstack1lllllll11ll_opy_.b_path:
                            bstack1llll1llllll_opy_.add(bstack1lllllll11ll_opy_.b_path)
    except Exception:
        pass
    return list(bstack1llll1llllll_opy_)
def bstack1llll1l1l1ll_opy_(bstack1lllll1l111l_opy_):
    bstack1llll1l111l1_opy_ = bstack1llll11ll1ll_opy_(bstack1lllll1l111l_opy_)
    if bstack1llll1l111l1_opy_ and bstack1llll1l111l1_opy_ > bstack1111111llll_opy_:
        bstack1llll1ll1l11_opy_ = bstack1llll1l111l1_opy_ - bstack1111111llll_opy_
        bstack1llll1ll11ll_opy_ = bstack1lllll111111_opy_(bstack1lllll1l111l_opy_[bstack1ll_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡡࡰࡩࡸࡹࡡࡨࡧࠥ⇇")], bstack1llll1ll1l11_opy_)
        bstack1lllll1l111l_opy_[bstack1ll_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡢࡱࡪࡹࡳࡢࡩࡨࠦ⇈")] = bstack1llll1ll11ll_opy_
        logger.info(bstack1ll_opy_ (u"࡙ࠦ࡮ࡥࠡࡥࡲࡱࡲ࡯ࡴࠡࡪࡤࡷࠥࡨࡥࡦࡰࠣࡸࡷࡻ࡮ࡤࡣࡷࡩࡩ࠴ࠠࡔ࡫ࡽࡩࠥࡵࡦࠡࡥࡲࡱࡲ࡯ࡴࠡࡣࡩࡸࡪࡸࠠࡵࡴࡸࡲࡨࡧࡴࡪࡱࡱࠤ࡮ࡹࠠࡼࡿࠣࡏࡇࠨ⇉")
                    .format(bstack1llll11ll1ll_opy_(bstack1lllll1l111l_opy_) / 1024))
    return bstack1lllll1l111l_opy_
def bstack1llll11ll1ll_opy_(json_data):
    try:
        if json_data:
            bstack1lllll111lll_opy_ = json.dumps(json_data)
            bstack1llll11111ll_opy_ = sys.getsizeof(bstack1lllll111lll_opy_)
            return bstack1llll11111ll_opy_
    except Exception as e:
        logger.debug(bstack1ll_opy_ (u"࡙ࠧ࡯࡮ࡧࡷ࡬࡮ࡴࡧࠡࡹࡨࡲࡹࠦࡷࡳࡱࡱ࡫ࠥࡽࡨࡪ࡮ࡨࠤࡨࡧ࡬ࡤࡷ࡯ࡥࡹ࡯࡮ࡨࠢࡶ࡭ࡿ࡫ࠠࡰࡨࠣࡎࡘࡕࡎࠡࡱࡥ࡮ࡪࡩࡴ࠻ࠢࡾࢁࠧ⇊").format(e))
    return -1
def bstack1lllll111111_opy_(field, bstack1llll1lll111_opy_):
    try:
        bstack1lllll1llll1_opy_ = len(bytes(bstack11111l111l1_opy_, bstack1ll_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬ⇋")))
        bstack1lllll11111l_opy_ = bytes(field, bstack1ll_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭⇌"))
        bstack1llll1lllll1_opy_ = len(bstack1lllll11111l_opy_)
        bstack1llll111111l_opy_ = ceil(bstack1llll1lllll1_opy_ - bstack1llll1lll111_opy_ - bstack1lllll1llll1_opy_)
        if bstack1llll111111l_opy_ > 0:
            bstack1lllll111ll1_opy_ = bstack1lllll11111l_opy_[:bstack1llll111111l_opy_].decode(bstack1ll_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧ⇍"), errors=bstack1ll_opy_ (u"ࠩ࡬࡫ࡳࡵࡲࡦࠩ⇎")) + bstack11111l111l1_opy_
            return bstack1lllll111ll1_opy_
    except Exception as e:
        logger.debug(bstack1ll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡶࡵࡹࡳࡩࡡࡵ࡫ࡱ࡫ࠥ࡬ࡩࡦ࡮ࡧ࠰ࠥࡴ࡯ࡵࡪ࡬ࡲ࡬ࠦࡷࡢࡵࠣࡸࡷࡻ࡮ࡤࡣࡷࡩࡩࠦࡨࡦࡴࡨ࠾ࠥࢁࡽࠣ⇏").format(e))
    return field
def bstack1lll11l1ll_opy_():
    env = os.environ
    if (bstack1ll_opy_ (u"ࠦࡏࡋࡎࡌࡋࡑࡗࡤ࡛ࡒࡍࠤ⇐") in env and len(env[bstack1ll_opy_ (u"ࠧࡐࡅࡏࡍࡌࡒࡘࡥࡕࡓࡎࠥ⇑")]) > 0) or (
            bstack1ll_opy_ (u"ࠨࡊࡆࡐࡎࡍࡓ࡙࡟ࡉࡑࡐࡉࠧ⇒") in env and len(env[bstack1ll_opy_ (u"ࠢࡋࡇࡑࡏࡎࡔࡓࡠࡊࡒࡑࡊࠨ⇓")]) > 0):
        return {
            bstack1ll_opy_ (u"ࠣࡰࡤࡱࡪࠨ⇔"): bstack1ll_opy_ (u"ࠤࡍࡩࡳࡱࡩ࡯ࡵࠥ⇕"),
            bstack1ll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ⇖"): env.get(bstack1ll_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢ⇗")),
            bstack1ll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ⇘"): env.get(bstack1ll_opy_ (u"ࠨࡊࡐࡄࡢࡒࡆࡓࡅࠣ⇙")),
            bstack1ll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ⇚"): env.get(bstack1ll_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢ⇛"))
        }
    if env.get(bstack1ll_opy_ (u"ࠤࡆࡍࠧ⇜")) == bstack1ll_opy_ (u"ࠥࡸࡷࡻࡥࠣ⇝") and bstack11l1l1l11l_opy_(env.get(bstack1ll_opy_ (u"ࠦࡈࡏࡒࡄࡎࡈࡇࡎࠨ⇞"))):
        return {
            bstack1ll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ⇟"): bstack1ll_opy_ (u"ࠨࡃࡪࡴࡦࡰࡪࡉࡉࠣ⇠"),
            bstack1ll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ⇡"): env.get(bstack1ll_opy_ (u"ࠣࡅࡌࡖࡈࡒࡅࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦ⇢")),
            bstack1ll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ⇣"): env.get(bstack1ll_opy_ (u"ࠥࡇࡎࡘࡃࡍࡇࡢࡎࡔࡈࠢ⇤")),
            bstack1ll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ⇥"): env.get(bstack1ll_opy_ (u"ࠧࡉࡉࡓࡅࡏࡉࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࠣ⇦"))
        }
    if env.get(bstack1ll_opy_ (u"ࠨࡃࡊࠤ⇧")) == bstack1ll_opy_ (u"ࠢࡵࡴࡸࡩࠧ⇨") and bstack11l1l1l11l_opy_(env.get(bstack1ll_opy_ (u"ࠣࡖࡕࡅ࡛ࡏࡓࠣ⇩"))):
        return {
            bstack1ll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ⇪"): bstack1ll_opy_ (u"ࠥࡘࡷࡧࡶࡪࡵࠣࡇࡎࠨ⇫"),
            bstack1ll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ⇬"): env.get(bstack1ll_opy_ (u"࡚ࠧࡒࡂࡘࡌࡗࡤࡈࡕࡊࡎࡇࡣ࡜ࡋࡂࡠࡗࡕࡐࠧ⇭")),
            bstack1ll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ⇮"): env.get(bstack1ll_opy_ (u"ࠢࡕࡔࡄ࡚ࡎ࡙࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤ⇯")),
            bstack1ll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ⇰"): env.get(bstack1ll_opy_ (u"ࠤࡗࡖࡆ࡜ࡉࡔࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣ⇱"))
        }
    if env.get(bstack1ll_opy_ (u"ࠥࡇࡎࠨ⇲")) == bstack1ll_opy_ (u"ࠦࡹࡸࡵࡦࠤ⇳") and env.get(bstack1ll_opy_ (u"ࠧࡉࡉࡠࡐࡄࡑࡊࠨ⇴")) == bstack1ll_opy_ (u"ࠨࡣࡰࡦࡨࡷ࡭࡯ࡰࠣ⇵"):
        return {
            bstack1ll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ⇶"): bstack1ll_opy_ (u"ࠣࡅࡲࡨࡪࡹࡨࡪࡲࠥ⇷"),
            bstack1ll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ⇸"): None,
            bstack1ll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ⇹"): None,
            bstack1ll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ⇺"): None
        }
    if env.get(bstack1ll_opy_ (u"ࠧࡈࡉࡕࡄࡘࡇࡐࡋࡔࡠࡄࡕࡅࡓࡉࡈࠣ⇻")) and env.get(bstack1ll_opy_ (u"ࠨࡂࡊࡖࡅ࡙ࡈࡑࡅࡕࡡࡆࡓࡒࡓࡉࡕࠤ⇼")):
        return {
            bstack1ll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ⇽"): bstack1ll_opy_ (u"ࠣࡄ࡬ࡸࡧࡻࡣ࡬ࡧࡷࠦ⇾"),
            bstack1ll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ⇿"): env.get(bstack1ll_opy_ (u"ࠥࡆࡎ࡚ࡂࡖࡅࡎࡉ࡙ࡥࡇࡊࡖࡢࡌ࡙࡚ࡐࡠࡑࡕࡍࡌࡏࡎࠣ∀")),
            bstack1ll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ∁"): None,
            bstack1ll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ∂"): env.get(bstack1ll_opy_ (u"ࠨࡂࡊࡖࡅ࡙ࡈࡑࡅࡕࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣ∃"))
        }
    if env.get(bstack1ll_opy_ (u"ࠢࡄࡋࠥ∄")) == bstack1ll_opy_ (u"ࠣࡶࡵࡹࡪࠨ∅") and bstack11l1l1l11l_opy_(env.get(bstack1ll_opy_ (u"ࠤࡇࡖࡔࡔࡅࠣ∆"))):
        return {
            bstack1ll_opy_ (u"ࠥࡲࡦࡳࡥࠣ∇"): bstack1ll_opy_ (u"ࠦࡉࡸ࡯࡯ࡧࠥ∈"),
            bstack1ll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ∉"): env.get(bstack1ll_opy_ (u"ࠨࡄࡓࡑࡑࡉࡤࡈࡕࡊࡎࡇࡣࡑࡏࡎࡌࠤ∊")),
            bstack1ll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ∋"): None,
            bstack1ll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ∌"): env.get(bstack1ll_opy_ (u"ࠤࡇࡖࡔࡔࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢ∍"))
        }
    if env.get(bstack1ll_opy_ (u"ࠥࡇࡎࠨ∎")) == bstack1ll_opy_ (u"ࠦࡹࡸࡵࡦࠤ∏") and bstack11l1l1l11l_opy_(env.get(bstack1ll_opy_ (u"࡙ࠧࡅࡎࡃࡓࡌࡔࡘࡅࠣ∐"))):
        return {
            bstack1ll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ∑"): bstack1ll_opy_ (u"ࠢࡔࡧࡰࡥࡵ࡮࡯ࡳࡧࠥ−"),
            bstack1ll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ∓"): env.get(bstack1ll_opy_ (u"ࠤࡖࡉࡒࡇࡐࡉࡑࡕࡉࡤࡕࡒࡈࡃࡑࡍ࡟ࡇࡔࡊࡑࡑࡣ࡚ࡘࡌࠣ∔")),
            bstack1ll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ∕"): env.get(bstack1ll_opy_ (u"ࠦࡘࡋࡍࡂࡒࡋࡓࡗࡋ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤ∖")),
            bstack1ll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ∗"): env.get(bstack1ll_opy_ (u"ࠨࡓࡆࡏࡄࡔࡍࡕࡒࡆࡡࡍࡓࡇࡥࡉࡅࠤ∘"))
        }
    if env.get(bstack1ll_opy_ (u"ࠢࡄࡋࠥ∙")) == bstack1ll_opy_ (u"ࠣࡶࡵࡹࡪࠨ√") and bstack11l1l1l11l_opy_(env.get(bstack1ll_opy_ (u"ࠤࡊࡍ࡙ࡒࡁࡃࡡࡆࡍࠧ∛"))):
        return {
            bstack1ll_opy_ (u"ࠥࡲࡦࡳࡥࠣ∜"): bstack1ll_opy_ (u"ࠦࡌ࡯ࡴࡍࡣࡥࠦ∝"),
            bstack1ll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ∞"): env.get(bstack1ll_opy_ (u"ࠨࡃࡊࡡࡍࡓࡇࡥࡕࡓࡎࠥ∟")),
            bstack1ll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ∠"): env.get(bstack1ll_opy_ (u"ࠣࡅࡌࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨ∡")),
            bstack1ll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ∢"): env.get(bstack1ll_opy_ (u"ࠥࡇࡎࡥࡊࡐࡄࡢࡍࡉࠨ∣"))
        }
    if env.get(bstack1ll_opy_ (u"ࠦࡈࡏࠢ∤")) == bstack1ll_opy_ (u"ࠧࡺࡲࡶࡧࠥ∥") and bstack11l1l1l11l_opy_(env.get(bstack1ll_opy_ (u"ࠨࡂࡖࡋࡏࡈࡐࡏࡔࡆࠤ∦"))):
        return {
            bstack1ll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ∧"): bstack1ll_opy_ (u"ࠣࡄࡸ࡭ࡱࡪ࡫ࡪࡶࡨࠦ∨"),
            bstack1ll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ∩"): env.get(bstack1ll_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡍࡌࡘࡊࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤ∪")),
            bstack1ll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ∫"): env.get(bstack1ll_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࡠࡎࡄࡆࡊࡒࠢ∬")) or env.get(bstack1ll_opy_ (u"ࠨࡂࡖࡋࡏࡈࡐࡏࡔࡆࡡࡓࡍࡕࡋࡌࡊࡐࡈࡣࡓࡇࡍࡆࠤ∭")),
            bstack1ll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ∮"): env.get(bstack1ll_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥ∯"))
        }
    if bstack11l1l1l11l_opy_(env.get(bstack1ll_opy_ (u"ࠤࡗࡊࡤࡈࡕࡊࡎࡇࠦ∰"))):
        return {
            bstack1ll_opy_ (u"ࠥࡲࡦࡳࡥࠣ∱"): bstack1ll_opy_ (u"࡛ࠦ࡯ࡳࡶࡣ࡯ࠤࡘࡺࡵࡥ࡫ࡲࠤ࡙࡫ࡡ࡮ࠢࡖࡩࡷࡼࡩࡤࡧࡶࠦ∲"),
            bstack1ll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ∳"): bstack1ll_opy_ (u"ࠨࡻࡾࡽࢀࠦ∴").format(env.get(bstack1ll_opy_ (u"ࠧࡔ࡛ࡖࡘࡊࡓ࡟ࡕࡇࡄࡑࡋࡕࡕࡏࡆࡄࡘࡎࡕࡎࡔࡇࡕ࡚ࡊࡘࡕࡓࡋࠪ∵")), env.get(bstack1ll_opy_ (u"ࠨࡕ࡜ࡗ࡙ࡋࡍࡠࡖࡈࡅࡒࡖࡒࡐࡌࡈࡇ࡙ࡏࡄࠨ∶"))),
            bstack1ll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ∷"): env.get(bstack1ll_opy_ (u"ࠥࡗ࡞࡙ࡔࡆࡏࡢࡈࡊࡌࡉࡏࡋࡗࡍࡔࡔࡉࡅࠤ∸")),
            bstack1ll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ∹"): env.get(bstack1ll_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡌࡈࠧ∺"))
        }
    if bstack11l1l1l11l_opy_(env.get(bstack1ll_opy_ (u"ࠨࡁࡑࡒ࡙ࡉ࡞ࡕࡒࠣ∻"))):
        return {
            bstack1ll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ∼"): bstack1ll_opy_ (u"ࠣࡃࡳࡴࡻ࡫ࡹࡰࡴࠥ∽"),
            bstack1ll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ∾"): bstack1ll_opy_ (u"ࠥࡿࢂ࠵ࡰࡳࡱ࡭ࡩࡨࡺ࠯ࡼࡿ࠲ࡿࢂ࠵ࡢࡶ࡫࡯ࡨࡸ࠵ࡻࡾࠤ∿").format(env.get(bstack1ll_opy_ (u"ࠫࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡕࡓࡎࠪ≀")), env.get(bstack1ll_opy_ (u"ࠬࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡂࡅࡆࡓ࡚ࡔࡔࡠࡐࡄࡑࡊ࠭≁")), env.get(bstack1ll_opy_ (u"࠭ࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡒࡕࡓࡏࡋࡃࡕࡡࡖࡐ࡚ࡍࠧ≂")), env.get(bstack1ll_opy_ (u"ࠧࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠫ≃"))),
            bstack1ll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ≄"): env.get(bstack1ll_opy_ (u"ࠤࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨ≅")),
            bstack1ll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ≆"): env.get(bstack1ll_opy_ (u"ࠦࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧ≇"))
        }
    if env.get(bstack1ll_opy_ (u"ࠧࡇ࡚ࡖࡔࡈࡣࡍ࡚ࡔࡑࡡࡘࡗࡊࡘ࡟ࡂࡉࡈࡒ࡙ࠨ≈")) and env.get(bstack1ll_opy_ (u"ࠨࡔࡇࡡࡅ࡙ࡎࡒࡄࠣ≉")):
        return {
            bstack1ll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ≊"): bstack1ll_opy_ (u"ࠣࡃࡽࡹࡷ࡫ࠠࡄࡋࠥ≋"),
            bstack1ll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ≌"): bstack1ll_opy_ (u"ࠥࡿࢂࢁࡽ࠰ࡡࡥࡹ࡮ࡲࡤ࠰ࡴࡨࡷࡺࡲࡴࡴࡁࡥࡹ࡮ࡲࡤࡊࡦࡀࡿࢂࠨ≍").format(env.get(bstack1ll_opy_ (u"ࠫࡘ࡟ࡓࡕࡇࡐࡣ࡙ࡋࡁࡎࡈࡒ࡙ࡓࡊࡁࡕࡋࡒࡒࡘࡋࡒࡗࡇࡕ࡙ࡗࡏࠧ≎")), env.get(bstack1ll_opy_ (u"࡙࡙ࠬࡔࡖࡈࡑࡤ࡚ࡅࡂࡏࡓࡖࡔࡐࡅࡄࡖࠪ≏")), env.get(bstack1ll_opy_ (u"࠭ࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡍࡉ࠭≐"))),
            bstack1ll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ≑"): env.get(bstack1ll_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡏࡄࠣ≒")),
            bstack1ll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ≓"): env.get(bstack1ll_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡊࡆࠥ≔"))
        }
    if any([env.get(bstack1ll_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠤ≕")), env.get(bstack1ll_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡔࡈࡗࡔࡒࡖࡆࡆࡢࡗࡔ࡛ࡒࡄࡇࡢ࡚ࡊࡘࡓࡊࡑࡑࠦ≖")), env.get(bstack1ll_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡖࡓ࡚ࡘࡃࡆࡡ࡙ࡉࡗ࡙ࡉࡐࡐࠥ≗"))]):
        return {
            bstack1ll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ≘"): bstack1ll_opy_ (u"ࠣࡃ࡚ࡗࠥࡉ࡯ࡥࡧࡅࡹ࡮ࡲࡤࠣ≙"),
            bstack1ll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ≚"): env.get(bstack1ll_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡐࡖࡄࡏࡍࡈࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤ≛")),
            bstack1ll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ≜"): env.get(bstack1ll_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠥ≝")),
            bstack1ll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ≞"): env.get(bstack1ll_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧ≟"))
        }
    if env.get(bstack1ll_opy_ (u"ࠣࡤࡤࡱࡧࡵ࡯ࡠࡤࡸ࡭ࡱࡪࡎࡶ࡯ࡥࡩࡷࠨ≠")):
        return {
            bstack1ll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ≡"): bstack1ll_opy_ (u"ࠥࡆࡦࡳࡢࡰࡱࠥ≢"),
            bstack1ll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ≣"): env.get(bstack1ll_opy_ (u"ࠧࡨࡡ࡮ࡤࡲࡳࡤࡨࡵࡪ࡮ࡧࡖࡪࡹࡵ࡭ࡶࡶ࡙ࡷࡲࠢ≤")),
            bstack1ll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ≥"): env.get(bstack1ll_opy_ (u"ࠢࡣࡣࡰࡦࡴࡵ࡟ࡴࡪࡲࡶࡹࡐ࡯ࡣࡐࡤࡱࡪࠨ≦")),
            bstack1ll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ≧"): env.get(bstack1ll_opy_ (u"ࠤࡥࡥࡲࡨ࡯ࡰࡡࡥࡹ࡮ࡲࡤࡏࡷࡰࡦࡪࡸࠢ≨"))
        }
    if env.get(bstack1ll_opy_ (u"࡛ࠥࡊࡘࡃࡌࡇࡕࠦ≩")) or env.get(bstack1ll_opy_ (u"ࠦ࡜ࡋࡒࡄࡍࡈࡖࡤࡓࡁࡊࡐࡢࡔࡎࡖࡅࡍࡋࡑࡉࡤ࡙ࡔࡂࡔࡗࡉࡉࠨ≪")):
        return {
            bstack1ll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ≫"): bstack1ll_opy_ (u"ࠨࡗࡦࡴࡦ࡯ࡪࡸࠢ≬"),
            bstack1ll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ≭"): env.get(bstack1ll_opy_ (u"࡙ࠣࡈࡖࡈࡑࡅࡓࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧ≮")),
            bstack1ll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ≯"): bstack1ll_opy_ (u"ࠥࡑࡦ࡯࡮ࠡࡒ࡬ࡴࡪࡲࡩ࡯ࡧࠥ≰") if env.get(bstack1ll_opy_ (u"ࠦ࡜ࡋࡒࡄࡍࡈࡖࡤࡓࡁࡊࡐࡢࡔࡎࡖࡅࡍࡋࡑࡉࡤ࡙ࡔࡂࡔࡗࡉࡉࠨ≱")) else None,
            bstack1ll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ≲"): env.get(bstack1ll_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘ࡟ࡈࡋࡗࡣࡈࡕࡍࡎࡋࡗࠦ≳"))
        }
    if any([env.get(bstack1ll_opy_ (u"ࠢࡈࡅࡓࡣࡕࡘࡏࡋࡇࡆࡘࠧ≴")), env.get(bstack1ll_opy_ (u"ࠣࡉࡆࡐࡔ࡛ࡄࡠࡒࡕࡓࡏࡋࡃࡕࠤ≵")), env.get(bstack1ll_opy_ (u"ࠤࡊࡓࡔࡍࡌࡆࡡࡆࡐࡔ࡛ࡄࡠࡒࡕࡓࡏࡋࡃࡕࠤ≶"))]):
        return {
            bstack1ll_opy_ (u"ࠥࡲࡦࡳࡥࠣ≷"): bstack1ll_opy_ (u"ࠦࡌࡵ࡯ࡨ࡮ࡨࠤࡈࡲ࡯ࡶࡦࠥ≸"),
            bstack1ll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ≹"): None,
            bstack1ll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ≺"): env.get(bstack1ll_opy_ (u"ࠢࡑࡔࡒࡎࡊࡉࡔࡠࡋࡇࠦ≻")),
            bstack1ll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ≼"): env.get(bstack1ll_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡋࡇࠦ≽"))
        }
    if env.get(bstack1ll_opy_ (u"ࠥࡗࡍࡏࡐࡑࡃࡅࡐࡊࠨ≾")):
        return {
            bstack1ll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ≿"): bstack1ll_opy_ (u"࡙ࠧࡨࡪࡲࡳࡥࡧࡲࡥࠣ⊀"),
            bstack1ll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ⊁"): env.get(bstack1ll_opy_ (u"ࠢࡔࡊࡌࡔࡕࡇࡂࡍࡇࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨ⊂")),
            bstack1ll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ⊃"): bstack1ll_opy_ (u"ࠤࡍࡳࡧࠦࠣࡼࡿࠥ⊄").format(env.get(bstack1ll_opy_ (u"ࠪࡗࡍࡏࡐࡑࡃࡅࡐࡊࡥࡊࡐࡄࡢࡍࡉ࠭⊅"))) if env.get(bstack1ll_opy_ (u"ࠦࡘࡎࡉࡑࡒࡄࡆࡑࡋ࡟ࡋࡑࡅࡣࡎࡊࠢ⊆")) else None,
            bstack1ll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ⊇"): env.get(bstack1ll_opy_ (u"ࠨࡓࡉࡋࡓࡔࡆࡈࡌࡆࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣ⊈"))
        }
    if bstack11l1l1l11l_opy_(env.get(bstack1ll_opy_ (u"ࠢࡏࡇࡗࡐࡎࡌ࡙ࠣ⊉"))):
        return {
            bstack1ll_opy_ (u"ࠣࡰࡤࡱࡪࠨ⊊"): bstack1ll_opy_ (u"ࠤࡑࡩࡹࡲࡩࡧࡻࠥ⊋"),
            bstack1ll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ⊌"): env.get(bstack1ll_opy_ (u"ࠦࡉࡋࡐࡍࡑ࡜ࡣ࡚ࡘࡌࠣ⊍")),
            bstack1ll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ⊎"): env.get(bstack1ll_opy_ (u"ࠨࡓࡊࡖࡈࡣࡓࡇࡍࡆࠤ⊏")),
            bstack1ll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ⊐"): env.get(bstack1ll_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡊࡆࠥ⊑"))
        }
    if bstack11l1l1l11l_opy_(env.get(bstack1ll_opy_ (u"ࠤࡊࡍ࡙ࡎࡕࡃࡡࡄࡇ࡙ࡏࡏࡏࡕࠥ⊒"))):
        return {
            bstack1ll_opy_ (u"ࠥࡲࡦࡳࡥࠣ⊓"): bstack1ll_opy_ (u"ࠦࡌ࡯ࡴࡉࡷࡥࠤࡆࡩࡴࡪࡱࡱࡷࠧ⊔"),
            bstack1ll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ⊕"): bstack1ll_opy_ (u"ࠨࡻࡾ࠱ࡾࢁ࠴ࡧࡣࡵ࡫ࡲࡲࡸ࠵ࡲࡶࡰࡶ࠳ࢀࢃࠢ⊖").format(env.get(bstack1ll_opy_ (u"ࠧࡈࡋࡗࡌ࡚ࡈ࡟ࡔࡇࡕ࡚ࡊࡘ࡟ࡖࡔࡏࠫ⊗")), env.get(bstack1ll_opy_ (u"ࠨࡉࡌࡘࡍ࡛ࡂࡠࡔࡈࡔࡔ࡙ࡉࡕࡑࡕ࡝ࠬ⊘")), env.get(bstack1ll_opy_ (u"ࠩࡊࡍ࡙ࡎࡕࡃࡡࡕ࡙ࡓࡥࡉࡅࠩ⊙"))),
            bstack1ll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ⊚"): env.get(bstack1ll_opy_ (u"ࠦࡌࡏࡔࡉࡗࡅࡣ࡜ࡕࡒࡌࡈࡏࡓ࡜ࠨ⊛")),
            bstack1ll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ⊜"): env.get(bstack1ll_opy_ (u"ࠨࡇࡊࡖࡋ࡙ࡇࡥࡒࡖࡐࡢࡍࡉࠨ⊝"))
        }
    if env.get(bstack1ll_opy_ (u"ࠢࡄࡋࠥ⊞")) == bstack1ll_opy_ (u"ࠣࡶࡵࡹࡪࠨ⊟") and env.get(bstack1ll_opy_ (u"ࠤ࡙ࡉࡗࡉࡅࡍࠤ⊠")) == bstack1ll_opy_ (u"ࠥ࠵ࠧ⊡"):
        return {
            bstack1ll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ⊢"): bstack1ll_opy_ (u"ࠧ࡜ࡥࡳࡥࡨࡰࠧ⊣"),
            bstack1ll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ⊤"): bstack1ll_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࡼࡿࠥ⊥").format(env.get(bstack1ll_opy_ (u"ࠨࡘࡈࡖࡈࡋࡌࡠࡗࡕࡐࠬ⊦"))),
            bstack1ll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ⊧"): None,
            bstack1ll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ⊨"): None,
        }
    if env.get(bstack1ll_opy_ (u"࡙ࠦࡋࡁࡎࡅࡌࡘ࡞ࡥࡖࡆࡔࡖࡍࡔࡔࠢ⊩")):
        return {
            bstack1ll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ⊪"): bstack1ll_opy_ (u"ࠨࡔࡦࡣࡰࡧ࡮ࡺࡹࠣ⊫"),
            bstack1ll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ⊬"): None,
            bstack1ll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ⊭"): env.get(bstack1ll_opy_ (u"ࠤࡗࡉࡆࡓࡃࡊࡖ࡜ࡣࡕࡘࡏࡋࡇࡆࡘࡤࡔࡁࡎࡇࠥ⊮")),
            bstack1ll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ⊯"): env.get(bstack1ll_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥ⊰"))
        }
    if any([env.get(bstack1ll_opy_ (u"ࠧࡉࡏࡏࡅࡒ࡙ࡗ࡙ࡅࠣ⊱")), env.get(bstack1ll_opy_ (u"ࠨࡃࡐࡐࡆࡓ࡚ࡘࡓࡆࡡࡘࡖࡑࠨ⊲")), env.get(bstack1ll_opy_ (u"ࠢࡄࡑࡑࡇࡔ࡛ࡒࡔࡇࡢ࡙ࡘࡋࡒࡏࡃࡐࡉࠧ⊳")), env.get(bstack1ll_opy_ (u"ࠣࡅࡒࡒࡈࡕࡕࡓࡕࡈࡣ࡙ࡋࡁࡎࠤ⊴"))]):
        return {
            bstack1ll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ⊵"): bstack1ll_opy_ (u"ࠥࡇࡴࡴࡣࡰࡷࡵࡷࡪࠨ⊶"),
            bstack1ll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ⊷"): None,
            bstack1ll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ⊸"): env.get(bstack1ll_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢ⊹")) or None,
            bstack1ll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ⊺"): env.get(bstack1ll_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡊࡆࠥ⊻"), 0)
        }
    if env.get(bstack1ll_opy_ (u"ࠤࡊࡓࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢ⊼")):
        return {
            bstack1ll_opy_ (u"ࠥࡲࡦࡳࡥࠣ⊽"): bstack1ll_opy_ (u"ࠦࡌࡵࡃࡅࠤ⊾"),
            bstack1ll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ⊿"): None,
            bstack1ll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ⋀"): env.get(bstack1ll_opy_ (u"ࠢࡈࡑࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧ⋁")),
            bstack1ll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ⋂"): env.get(bstack1ll_opy_ (u"ࠤࡊࡓࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡄࡑࡘࡒ࡙ࡋࡒࠣ⋃"))
        }
    if env.get(bstack1ll_opy_ (u"ࠥࡇࡋࡥࡂࡖࡋࡏࡈࡤࡏࡄࠣ⋄")):
        return {
            bstack1ll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ⋅"): bstack1ll_opy_ (u"ࠧࡉ࡯ࡥࡧࡉࡶࡪࡹࡨࠣ⋆"),
            bstack1ll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ⋇"): env.get(bstack1ll_opy_ (u"ࠢࡄࡈࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨ⋈")),
            bstack1ll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ⋉"): env.get(bstack1ll_opy_ (u"ࠤࡆࡊࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡏࡃࡐࡉࠧ⋊")),
            bstack1ll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ⋋"): env.get(bstack1ll_opy_ (u"ࠦࡈࡌ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠤ⋌"))
        }
    return {bstack1ll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ⋍"): None}
def get_host_info():
    return {
        bstack1ll_opy_ (u"ࠨࡨࡰࡵࡷࡲࡦࡳࡥࠣ⋎"): platform.node(),
        bstack1ll_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠤ⋏"): platform.system(),
        bstack1ll_opy_ (u"ࠣࡶࡼࡴࡪࠨ⋐"): platform.machine(),
        bstack1ll_opy_ (u"ࠤࡹࡩࡷࡹࡩࡰࡰࠥ⋑"): platform.version(),
        bstack1ll_opy_ (u"ࠥࡥࡷࡩࡨࠣ⋒"): platform.architecture()[0]
    }
def bstack1ll1l1ll1l_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack1lllll111l11_opy_():
    if global_config.get_property(bstack1ll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠬ⋓")):
        return bstack1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ⋔")
    return bstack1ll_opy_ (u"࠭ࡵ࡯࡭ࡱࡳࡼࡴ࡟ࡨࡴ࡬ࡨࠬ⋕")
def bstack1ll1llll1l1_opy_(driver):
    info = {
        bstack1ll_opy_ (u"ࠧࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭⋖"): driver.capabilities,
        bstack1ll_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠬ⋗"): driver.session_id,
        bstack1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪ⋘"): driver.capabilities.get(bstack1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨ⋙"), None),
        bstack1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭⋚"): driver.capabilities.get(bstack1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭⋛"), None),
        bstack1ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠨ⋜"): driver.capabilities.get(bstack1ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪ࠭⋝"), None),
        bstack1ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫ⋞"):driver.capabilities.get(bstack1ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫ⋟"), None),
    }
    if bstack1lllll111l11_opy_() == bstack1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ⋠"):
        if bstack1llll1111_opy_():
            info[bstack1ll_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࠬ⋡")] = bstack1ll_opy_ (u"ࠬࡧࡰࡱ࠯ࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ⋢")
        elif driver.capabilities.get(bstack1ll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ⋣"), {}).get(bstack1ll_opy_ (u"ࠧࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨࠫ⋤"), False):
            info[bstack1ll_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࠩ⋥")] = bstack1ll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡴࡥࡤࡰࡪ࠭⋦")
        else:
            info[bstack1ll_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࠫ⋧")] = bstack1ll_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭⋨")
    return info
def bstack1llll1111_opy_():
    if global_config.get_property(bstack1ll_opy_ (u"ࠬࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ⋩")):
        return True
    if bstack11l1l1l11l_opy_(os.environ.get(bstack1ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧ⋪"), None)):
        return True
    return False
def bstack1lllll11ll1l_opy_(bstack1llll11lll11_opy_, url, response, headers=None, data=None):
    bstack1ll_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࡃࡷ࡬ࡰࡩࠦࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡰࡴ࡭ࠠࡱࡣࡵࡥࡲ࡫ࡴࡦࡴࡶࠤ࡫ࡵࡲࠡࡴࡨࡵࡺ࡫ࡳࡵ࠱ࡵࡩࡸࡶ࡯࡯ࡵࡨࠤࡱࡵࡧࡨ࡫ࡱ࡫ࠏࠦࠠࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡵࡩࡶࡻࡥࡴࡶࡢࡸࡾࡶࡥ࠻ࠢࡋࡘ࡙ࡖࠠ࡮ࡧࡷ࡬ࡴࡪࠠࠩࡉࡈࡘ࠱ࠦࡐࡐࡕࡗ࠰ࠥ࡫ࡴࡤ࠰ࠬࠎࠥࠦࠠࠡࠢࠣࠤࠥࡻࡲ࡭࠼ࠣࡖࡪࡷࡵࡦࡵࡷࠤ࡚ࡘࡌ࠰ࡧࡱࡨࡵࡵࡩ࡯ࡶࠍࠤࠥࠦࠠࠡࠢࠣࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࡀࠠࡓࡧࡶࡴࡴࡴࡳࡦࠢࡲࡦ࡯࡫ࡣࡵࠢࡩࡶࡴࡳࠠࡳࡧࡴࡹࡪࡹࡴࡴࠌࠣࠤࠥࠦࠠࠡࠢࠣ࡬ࡪࡧࡤࡦࡴࡶ࠾ࠥࡘࡥࡲࡷࡨࡷࡹࠦࡨࡦࡣࡧࡩࡷࡹࠠࡰࡴࠣࡒࡴࡴࡥࠋࠢࠣࠤࠥࠦࠠࠡࠢࡧࡥࡹࡧ࠺ࠡࡔࡨࡵࡺ࡫ࡳࡵࠢࡍࡗࡔࡔࠠࡥࡣࡷࡥࠥࡵࡲࠡࡐࡲࡲࡪࠐࠠࠡࠢࠣࡖࡪࡺࡵࡳࡰࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡤࡪࡥࡷ࠾ࠥࡌ࡯ࡳ࡯ࡤࡸࡹ࡫ࡤࠡ࡮ࡲ࡫ࠥࡳࡥࡴࡵࡤ࡫ࡪࠦࡷࡪࡶ࡫ࠤࡷ࡫ࡱࡶࡧࡶࡸࠥࡧ࡮ࡥࠢࡵࡩࡸࡶ࡯࡯ࡵࡨࠤࡩࡧࡴࡢࠌࠣࠤࠥࠦࠢࠣࠤ⋫")
    bstack1lllll1ll111_opy_ = {
        bstack1ll_opy_ (u"ࠣࡪࡨࡥࡩ࡫ࡲࡴࠤ⋬"): headers,
        bstack1ll_opy_ (u"ࠤࡰࡩࡹ࡮࡯ࡥࠤ⋭"): bstack1llll11lll11_opy_.upper(),
        bstack1ll_opy_ (u"ࠥࡥ࡬࡫࡮ࡵࠤ⋮"): None,
        bstack1ll_opy_ (u"ࠦࡪࡴࡤࡱࡱ࡬ࡲࡹࠨ⋯"): url,
        bstack1ll_opy_ (u"ࠧࡰࡳࡰࡰࠥ⋰"): data
    }
    try:
        bstack1lllllll1l1l_opy_ = response.json()
        if isinstance(bstack1lllllll1l1l_opy_, dict) and bstack1lllllll1l1l_opy_.get(bstack1ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭⋱"), {}).get(bstack1ll_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨ⋲"), {}).get(bstack1ll_opy_ (u"ࠨࡵࡦࡶ࡮ࡶࡴࡴࠩ⋳")):
            bstack1llll1l1111l_opy_ = json.loads(json.dumps(bstack1lllllll1l1l_opy_))
            bstack1llll1l1111l_opy_[bstack1ll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ⋴")][bstack1ll_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫ⋵")][bstack1ll_opy_ (u"ࠫࡸࡩࡲࡪࡲࡷࡷࠬ⋶")] = bstack1ll_opy_ (u"ࠧࡡࡲࡦࡦࡤࡧࡹ࡫ࡤࠡࡨࡲࡶࠥࡨࡲࡦࡸ࡬ࡸࡾࡣࠢ⋷")
            bstack1lllllll1l1l_opy_ = bstack1llll1l1111l_opy_
    except Exception:
        bstack1lllllll1l1l_opy_ = response.text
    bstack1llll1l11lll_opy_ = {
        bstack1ll_opy_ (u"ࠨࡢࡰࡦࡼࠦ⋸"): bstack1lllllll1l1l_opy_,
        bstack1ll_opy_ (u"ࠢࡴࡶࡤࡸࡺࡹࡃࡰࡦࡨࠦ⋹"): response.status_code
    }
    return {
        bstack1ll_opy_ (u"ࠣࡴࡨࡵࡺ࡫ࡳࡵࠤ⋺"): bstack1lllll1ll111_opy_,
        bstack1ll_opy_ (u"ࠤࡵࡩࡸࡶ࡯࡯ࡵࡨࠦ⋻"): bstack1llll1l11lll_opy_
    }
def bstack1l1111l111_opy_(bstack1llll11lll11_opy_, url, data, config):
    headers = config.get(bstack1ll_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫ⋼"), None)
    proxies = bstack11l11ll11_opy_(config, url)
    auth = config.get(bstack1ll_opy_ (u"ࠫࡦࡻࡴࡩࠩ⋽"), None)
    response = requests.request(
            bstack1llll11lll11_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    try:
        log_message = bstack1lllll11ll1l_opy_(bstack1llll11lll11_opy_, url, response, headers, data)
        automation_logger.debug(json.dumps(log_message, separators=(bstack1ll_opy_ (u"ࠬ࠲ࠧ⋾"), bstack1ll_opy_ (u"࠭࠺ࠨ⋿"))))
    except Exception as e:
        logger.debug(bstack1ll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡲ࡯ࡨࡩ࡬ࡲ࡬ࠦࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡶࡪࡷࡵࡦࡵࡷ࠾ࠥࢁࡽࠣ⌀").format(e))
    return response
def bstack11ll1l1ll1_opy_(bstack111ll11l1l_opy_, size):
    bstack1ll1llll1_opy_ = []
    while len(bstack111ll11l1l_opy_) > size:
        bstack1ll111l1ll_opy_ = bstack111ll11l1l_opy_[:size]
        bstack1ll1llll1_opy_.append(bstack1ll111l1ll_opy_)
        bstack111ll11l1l_opy_ = bstack111ll11l1l_opy_[size:]
    bstack1ll1llll1_opy_.append(bstack111ll11l1l_opy_)
    return bstack1ll1llll1_opy_
def bstack1lllll1lll1l_opy_(message, bstack1llll11lllll_opy_=False):
    os.write(1, bytes(message, bstack1ll_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧ⌁")))
    os.write(1, bytes(bstack1ll_opy_ (u"ࠩ࡟ࡲࠬ⌂"), bstack1ll_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩ⌃")))
    if bstack1llll11lllll_opy_:
        with open(bstack1ll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠱ࡴ࠷࠱ࡺ࠯ࠪ⌄") + os.environ[bstack1ll_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡊࡄࡗࡍࡋࡄࡠࡋࡇࠫ⌅")] + bstack1ll_opy_ (u"࠭࠮࡭ࡱࡪࠫ⌆"), bstack1ll_opy_ (u"ࠧࡢࠩ⌇")) as f:
            f.write(message + bstack1ll_opy_ (u"ࠨ࡞ࡱࠫ⌈"))
def bstack1lll1ll1ll_opy_():
    return os.environ[bstack1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠬ⌉")].lower() == bstack1ll_opy_ (u"ࠪࡸࡷࡻࡥࠨ⌊")
def bstack11l1ll1ll_opy_():
    return bstack1lll1l111l1_opy_().replace(tzinfo=None).isoformat() + bstack1ll_opy_ (u"ࠫ࡟࠭⌋")
def bstack1ll1ll111l1_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack1ll_opy_ (u"ࠬࡠࠧ⌌"))) - datetime.datetime.fromisoformat(start.rstrip(bstack1ll_opy_ (u"࡚࠭ࠨ⌍")))).total_seconds() * 1000
def bstack1llll1lll1l1_opy_(timestamp):
    return bstack1llll111l1l1_opy_(timestamp).isoformat() + bstack1ll_opy_ (u"࡛ࠧࠩ⌎")
def bstack1llll11ll111_opy_(bstack1lllll1l1lll_opy_):
    date_format = bstack1ll_opy_ (u"ࠨࠧ࡜ࠩࡲࠫࡤࠡࠧࡋ࠾ࠪࡓ࠺ࠦࡕ࠱ࠩ࡫࠭⌏")
    bstack1llllll11l1l_opy_ = datetime.datetime.strptime(bstack1lllll1l1lll_opy_, date_format)
    return bstack1llllll11l1l_opy_.isoformat() + bstack1ll_opy_ (u"ࠩ࡝ࠫ⌐")
def bstack1llllll1l11l_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack1ll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ⌑")
    else:
        return bstack1ll_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ⌒")
def bstack11l1l1l11l_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack1ll_opy_ (u"ࠬࡺࡲࡶࡧࠪ⌓")
def bstack1lll1lllllll_opy_(val):
    return val.__str__().lower() == bstack1ll_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬ⌔")
def error_handler(bstack1llll1l1l111_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack1llll1l1l111_opy_ as e:
                print(bstack1ll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠡࡽࢀࠤ࠲ࡄࠠࡼࡿ࠽ࠤࢀࢃࠢ⌕").format(func.__name__, bstack1llll1l1l111_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack1lllll11l1l1_opy_(bstack1llllll1111l_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack1llllll1111l_opy_(cls, *args, **kwargs)
            except bstack1llll1l1l111_opy_ as e:
                print(bstack1ll_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡧࡷࡱࡧࡹ࡯࡯࡯ࠢࡾࢁࠥ࠳࠾ࠡࡽࢀ࠾ࠥࢁࡽࠣ⌖").format(bstack1llllll1111l_opy_.__name__, bstack1llll1l1l111_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack1lllll11l1l1_opy_
    else:
        return decorator
def bstack1lll1111ll_opy_(bstack1lllll11111_opy_):
    if os.getenv(bstack1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠬ⌗")) is not None:
        return bstack11l1l1l11l_opy_(os.getenv(bstack1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓ࠭⌘")))
    if bstack1ll_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨ⌙") in bstack1lllll11111_opy_ and bstack1lll1lllllll_opy_(bstack1lllll11111_opy_[bstack1ll_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩ⌚")]):
        return False
    if bstack1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨ⌛") in bstack1lllll11111_opy_ and bstack1lll1lllllll_opy_(bstack1lllll11111_opy_[bstack1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩ⌜")]):
        return False
    return True
def bstack11lll11ll_opy_():
    try:
        from pytest_bdd import reporting
        bstack1llll1ll11l1_opy_ = os.environ.get(bstack1ll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡖࡕࡈࡖࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠣ⌝"), None)
        return bstack1llll1ll11l1_opy_ is None or bstack1llll1ll11l1_opy_ == bstack1ll_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠨ⌞")
    except Exception as e:
        return False
def bstack1lll11l111_opy_(hub_url, CONFIG):
    if bstack1ll11l11l1_opy_() <= version.parse(bstack1ll_opy_ (u"ࠪ࠷࠳࠷࠳࠯࠲ࠪ⌟")):
        if hub_url:
            return bstack1ll_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧ⌠") + hub_url + bstack1ll_opy_ (u"ࠧࡀ࠸࠱࠱ࡺࡨ࠴࡮ࡵࡣࠤ⌡")
        return bstack1lllll1l1l_opy_
    if hub_url:
        return bstack1ll_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࠣ⌢") + hub_url + bstack1ll_opy_ (u"ࠢ࠰ࡹࡧ࠳࡭ࡻࡢࠣ⌣")
    return bstack111l11lll1_opy_
def bstack1llll1l1lll1_opy_():
    return isinstance(os.getenv(bstack1ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑ࡛ࡗࡉࡘ࡚࡟ࡑࡎࡘࡋࡎࡔࠧ⌤")), str)
def bstack11llllll1_opy_(url):
    return urlparse(url).hostname
def bstack111lll1l1_opy_(hostname):
    for bstack1l1lll111_opy_ in bstack1111ll1ll1_opy_:
        regex = re.compile(bstack1l1lll111_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack1llll1111lll_opy_(bstack1lllll1lll11_opy_, file_name, logger):
    bstack1lllll11ll_opy_ = os.path.join(os.path.expanduser(bstack1ll_opy_ (u"ࠩࢁࠫ⌥")), bstack1lllll1lll11_opy_)
    try:
        if not os.path.exists(bstack1lllll11ll_opy_):
            os.makedirs(bstack1lllll11ll_opy_)
        file_path = os.path.join(os.path.expanduser(bstack1ll_opy_ (u"ࠪࢂࠬ⌦")), bstack1lllll1lll11_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack1ll_opy_ (u"ࠫࡼ࠭⌧")):
                pass
            with open(file_path, bstack1ll_opy_ (u"ࠧࡽࠫࠣ⌨")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack1l1l1111_opy_.format(str(e)))
def bstack1llllll1l1ll_opy_(file_name, key, value, logger):
    file_path = bstack1llll1111lll_opy_(bstack1ll_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭〈"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1111l1l1_opy_ = json.load(open(file_path, bstack1ll_opy_ (u"ࠧࡳࡤࠪ〉")))
        else:
            bstack1111l1l1_opy_ = {}
        bstack1111l1l1_opy_[key] = value
        with open(file_path, bstack1ll_opy_ (u"ࠣࡹ࠮ࠦ⌫")) as outfile:
            json.dump(bstack1111l1l1_opy_, outfile)
def bstack1lll111l1l_opy_(file_name, logger):
    file_path = bstack1llll1111lll_opy_(bstack1ll_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ⌬"), file_name, logger)
    bstack1111l1l1_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack1ll_opy_ (u"ࠪࡶࠬ⌭")) as bstack11lll11l_opy_:
            bstack1111l1l1_opy_ = json.load(bstack11lll11l_opy_)
    return bstack1111l1l1_opy_
def bstack1l1l11l1ll_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack1ll_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡤࡦ࡮ࡨࡸ࡮ࡴࡧࠡࡨ࡬ࡰࡪࡀࠠࠨ⌮") + file_path + bstack1ll_opy_ (u"ࠬࠦࠧ⌯") + str(e))
def bstack1ll11l11l1_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack1ll_opy_ (u"ࠨ࠼ࡏࡑࡗࡗࡊ࡚࠾ࠣ⌰")
def bstack111lll1ll_opy_(config):
    if bstack1ll_opy_ (u"ࠧࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭⌱") in config:
        del (config[bstack1ll_opy_ (u"ࠨ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧ⌲")])
        return False
    if bstack1ll11l11l1_opy_() < version.parse(bstack1ll_opy_ (u"ࠩ࠶࠲࠹࠴࠰ࠨ⌳")):
        return False
    if bstack1ll11l11l1_opy_() >= version.parse(bstack1ll_opy_ (u"ࠪ࠸࠳࠷࠮࠶ࠩ⌴")):
        return True
    if bstack1ll_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫ⌵") in config and config[bstack1ll_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬ⌶")] is False:
        return False
    else:
        return True
def bstack111l11111l_opy_(args_list, bstack1llllll11ll1_opy_):
    index = -1
    for value in bstack1llllll11ll1_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
def bstack1111l1lll11_opy_(a, b):
  for k, v in b.items():
    if isinstance(v, dict) and k in a and isinstance(a[k], dict):
        bstack1111l1lll11_opy_(a[k], v)
    else:
        a[k] = v
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack1llll1l1ll1_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack1llll1l1ll1_opy_ = bstack1llll1l1ll1_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack1ll_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭⌷"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack1ll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ⌸"), exception=exception)
    def bstack1ll111l1lll_opy_(self):
        if self.result != bstack1ll_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ⌹"):
            return None
        if isinstance(self.exception_type, str) and bstack1ll_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࠧ⌺") in self.exception_type:
            return bstack1ll_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࡋࡲࡳࡱࡵࠦ⌻")
        return bstack1ll_opy_ (u"࡚ࠦࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠧ⌼")
    def bstack1llllll1ll1l_opy_(self):
        if self.result != bstack1ll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ⌽"):
            return None
        if self.bstack1llll1l1ll1_opy_:
            return self.bstack1llll1l1ll1_opy_
        return bstack1llll1l11l1l_opy_(self.exception)
def bstack1llll1l11l1l_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack1llllll1l111_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack1llll1lll_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack1ll11l11_opy_(config, logger):
    try:
        import playwright
        bstack1llll111l1ll_opy_ = playwright.__file__
        bstack1llll111l111_opy_ = os.path.split(bstack1llll111l1ll_opy_)
        bstack1llll1l11l11_opy_ = bstack1llll111l111_opy_[0] + bstack1ll_opy_ (u"࠭࠯ࡥࡴ࡬ࡺࡪࡸ࠯ࡱࡣࡦ࡯ࡦ࡭ࡥ࠰࡮࡬ࡦ࠴ࡩ࡬ࡪ࠱ࡦࡰ࡮࠴ࡪࡴࠩ⌾")
        os.environ[bstack1ll_opy_ (u"ࠧࡈࡎࡒࡆࡆࡒ࡟ࡂࡉࡈࡒ࡙ࡥࡈࡕࡖࡓࡣࡕࡘࡏ࡙࡛ࠪ⌿")] = bstack11lllll1_opy_(config)
        with open(bstack1llll1l11l11_opy_, bstack1ll_opy_ (u"ࠨࡴࠪ⍀")) as f:
            file_content = f.read()
            bstack1llll11l1l1l_opy_ = bstack1ll_opy_ (u"ࠩࡪࡰࡴࡨࡡ࡭࠯ࡤ࡫ࡪࡴࡴࠨ⍁")
            bstack1llll11l1l11_opy_ = file_content.find(bstack1llll11l1l1l_opy_)
            if bstack1llll11l1l11_opy_ == -1:
              process = subprocess.Popen(bstack1ll_opy_ (u"ࠥࡲࡵࡳࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡩ࡯ࡳࡧࡧ࡬࠮ࡣࡪࡩࡳࡺࠢ⍂"), shell=True, cwd=bstack1llll111l111_opy_[0])
              process.wait()
              bstack1llllll11111_opy_ = bstack1ll_opy_ (u"ࠫࠧࡻࡳࡦࠢࡶࡸࡷ࡯ࡣࡵࠤ࠾ࠫ⍃")
              bstack1llllll11lll_opy_ = bstack1ll_opy_ (u"ࠧࠨࠢࠡ࡞ࠥࡹࡸ࡫ࠠࡴࡶࡵ࡭ࡨࡺ࡜ࠣ࠽ࠣࡧࡴࡴࡳࡵࠢࡾࠤࡧࡵ࡯ࡵࡵࡷࡶࡦࡶࠠࡾࠢࡀࠤࡷ࡫ࡱࡶ࡫ࡵࡩ࠭࠭ࡧ࡭ࡱࡥࡥࡱ࠳ࡡࡨࡧࡱࡸࠬ࠯࠻ࠡ࡫ࡩࠤ࠭ࡶࡲࡰࡥࡨࡷࡸ࠴ࡥ࡯ࡸ࠱ࡋࡑࡕࡂࡂࡎࡢࡅࡌࡋࡎࡕࡡࡋࡘ࡙ࡖ࡟ࡑࡔࡒ࡜࡞࠯ࠠࡣࡱࡲࡸࡸࡺࡲࡢࡲࠫ࠭ࡀࠦࠢࠣࠤ⍄")
              bstack1llllll111ll_opy_ = file_content.replace(bstack1llllll11111_opy_, bstack1llllll11lll_opy_)
              with open(bstack1llll1l11l11_opy_, bstack1ll_opy_ (u"࠭ࡷࠨ⍅")) as f:
                f.write(bstack1llllll111ll_opy_)
    except Exception as e:
        logger.error(bstack111l11ll11_opy_.format(str(e)))
def bstack1lll1l1lll_opy_():
  try:
    bstack1lllllll11l1_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll_opy_ (u"ࠧࡰࡲࡷ࡭ࡲࡧ࡬ࡠࡪࡸࡦࡤࡻࡲ࡭࠰࡭ࡷࡴࡴࠧ⍆"))
    bstack1llll1111111_opy_ = []
    if os.path.exists(bstack1lllllll11l1_opy_):
      with open(bstack1lllllll11l1_opy_) as f:
        bstack1llll1111111_opy_ = json.load(f)
      os.remove(bstack1lllllll11l1_opy_)
    return bstack1llll1111111_opy_
  except:
    pass
  return []
def bstack111l1l1ll1_opy_(bstack1llll111l_opy_):
  try:
    bstack1llll1111111_opy_ = []
    bstack1lllllll11l1_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll_opy_ (u"ࠨࡱࡳࡸ࡮ࡳࡡ࡭ࡡ࡫ࡹࡧࡥࡵࡳ࡮࠱࡮ࡸࡵ࡮ࠨ⍇"))
    if os.path.exists(bstack1lllllll11l1_opy_):
      with open(bstack1lllllll11l1_opy_) as f:
        bstack1llll1111111_opy_ = json.load(f)
    bstack1llll1111111_opy_.append(bstack1llll111l_opy_)
    with open(bstack1lllllll11l1_opy_, bstack1ll_opy_ (u"ࠩࡺࠫ⍈")) as f:
        json.dump(bstack1llll1111111_opy_, f)
  except:
    pass
def bstack1ll11l1l1l_opy_(logger, bstack1llll111lll1_opy_ = False):
  try:
    test_name = os.environ.get(bstack1ll_opy_ (u"ࠪࡔ࡞࡚ࡅࡔࡖࡢࡘࡊ࡙ࡔࡠࡐࡄࡑࡊ࠭⍉"), bstack1ll_opy_ (u"ࠫࠬ⍊"))
    if test_name == bstack1ll_opy_ (u"ࠬ࠭⍋"):
        test_name = threading.current_thread().__dict__.get(bstack1ll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡈࡤࡥࡡࡷࡩࡸࡺ࡟࡯ࡣࡰࡩࠬ⍌"), bstack1ll_opy_ (u"ࠧࠨ⍍"))
    bstack1llll111ll11_opy_ = bstack1ll_opy_ (u"ࠨ࠮ࠣࠫ⍎").join(threading.current_thread().bstackTestErrorMessages)
    if bstack1llll111lll1_opy_:
        bstack11l11ll1_opy_ = os.environ.get(bstack1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩ⍏"), bstack1ll_opy_ (u"ࠪ࠴ࠬ⍐"))
        bstack1111ll1l1_opy_ = {bstack1ll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ⍑"): test_name, bstack1ll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ⍒"): bstack1llll111ll11_opy_, bstack1ll_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬ⍓"): bstack11l11ll1_opy_}
        bstack1llll1llll1l_opy_ = []
        bstack1lllll1l11ll_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡱࡲࡳࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴ࠯࡬ࡶࡳࡳ࠭⍔"))
        if os.path.exists(bstack1lllll1l11ll_opy_):
            with open(bstack1lllll1l11ll_opy_) as f:
                bstack1llll1llll1l_opy_ = json.load(f)
        bstack1llll1llll1l_opy_.append(bstack1111ll1l1_opy_)
        with open(bstack1lllll1l11ll_opy_, bstack1ll_opy_ (u"ࠨࡹࠪ⍕")) as f:
            json.dump(bstack1llll1llll1l_opy_, f)
    else:
        bstack1111ll1l1_opy_ = {bstack1ll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ⍖"): test_name, bstack1ll_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ⍗"): bstack1llll111ll11_opy_, bstack1ll_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪ⍘"): str(multiprocessing.current_process().name)}
        if bstack1ll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵࠩ⍙") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack1111ll1l1_opy_)
  except Exception as e:
      logger.warn(bstack1ll_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡸࡴࡸࡥࠡࡲࡼࡸࡪࡹࡴࠡࡨࡸࡲࡳ࡫࡬ࠡࡦࡤࡸࡦࡀࠠࡼࡿࠥ⍚").format(e))
def bstack11111ll1ll_opy_(error_message, test_name, index, logger):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1ll_opy_ (u"ࠧࡧ࡫࡯ࡩࡱࡵࡣ࡬ࠢࡱࡳࡹࠦࡡࡷࡣ࡬ࡰࡦࡨ࡬ࡦ࠮ࠣࡹࡸ࡯࡮ࡨࠢࡥࡥࡸ࡯ࡣࠡࡨ࡬ࡰࡪࠦ࡯ࡱࡧࡵࡥࡹ࡯࡯࡯ࡵࠪ⍛"))
    try:
      bstack1lllll11l1ll_opy_ = []
      bstack1111ll1l1_opy_ = {bstack1ll_opy_ (u"ࠨࡰࡤࡱࡪ࠭⍜"): test_name, bstack1ll_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ⍝"): error_message, bstack1ll_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩ⍞"): index}
      bstack1llll11ll11l_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll_opy_ (u"ࠫࡷࡵࡢࡰࡶࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬ⍟"))
      if os.path.exists(bstack1llll11ll11l_opy_):
          with open(bstack1llll11ll11l_opy_) as f:
              bstack1lllll11l1ll_opy_ = json.load(f)
      bstack1lllll11l1ll_opy_.append(bstack1111ll1l1_opy_)
      with open(bstack1llll11ll11l_opy_, bstack1ll_opy_ (u"ࠬࡽࠧ⍠")) as f:
          json.dump(bstack1lllll11l1ll_opy_, f)
    except Exception as e:
      logger.warn(bstack1ll_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡸࡴࡸࡥࠡࡴࡲࡦࡴࡺࠠࡧࡷࡱࡲࡪࡲࠠࡥࡣࡷࡥ࠿ࠦࡻࡾࠤ⍡").format(e))
    return
  bstack1lllll11l1ll_opy_ = []
  bstack1111ll1l1_opy_ = {bstack1ll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ⍢"): test_name, bstack1ll_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ⍣"): error_message, bstack1ll_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨ⍤"): index}
  bstack1llll11ll11l_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠴ࡪࡴࡱࡱࠫ⍥"))
  lock_file = bstack1llll11ll11l_opy_ + bstack1ll_opy_ (u"ࠫ࠳ࡲ࡯ࡤ࡭ࠪ⍦")
  try:
    with FileLock(lock_file, timeout=10):
      if os.path.exists(bstack1llll11ll11l_opy_):
          with open(bstack1llll11ll11l_opy_, bstack1ll_opy_ (u"ࠬࡸࠧ⍧")) as f:
              content = f.read().strip()
              if content:
                  bstack1lllll11l1ll_opy_ = json.load(open(bstack1llll11ll11l_opy_))
      bstack1lllll11l1ll_opy_.append(bstack1111ll1l1_opy_)
      with open(bstack1llll11ll11l_opy_, bstack1ll_opy_ (u"࠭ࡷࠨ⍨")) as f:
          json.dump(bstack1lllll11l1ll_opy_, f)
  except Exception as e:
    logger.warn(bstack1ll_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡹࡵࡲࡦࠢࡵࡳࡧࡵࡴࠡࡨࡸࡲࡳ࡫࡬ࠡࡦࡤࡸࡦࠦࡷࡪࡶ࡫ࠤ࡫࡯࡬ࡦࠢ࡯ࡳࡨࡱࡩ࡯ࡩ࠽ࠤࢀࢃࠢ⍩").format(e))
def bstack11l11llll1_opy_(bstack1ll111111l_opy_, name, logger):
  try:
    bstack1111ll1l1_opy_ = {bstack1ll_opy_ (u"ࠨࡰࡤࡱࡪ࠭⍪"): name, bstack1ll_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ⍫"): bstack1ll111111l_opy_, bstack1ll_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩ⍬"): str(threading.current_thread()._name)}
    return bstack1111ll1l1_opy_
  except Exception as e:
    logger.warn(bstack1ll_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡶࡲࡶࡪࠦࡢࡦࡪࡤࡺࡪࠦࡦࡶࡰࡱࡩࡱࠦࡤࡢࡶࡤ࠾ࠥࢁࡽࠣ⍭").format(e))
  return
def bstack1lllll1lllll_opy_():
    return platform.system() == bstack1ll_opy_ (u"ࠬ࡝ࡩ࡯ࡦࡲࡻࡸ࠭⍮")
def bstack111ll1111_opy_(bstack1lllll11lll1_opy_, config, logger):
    bstack1llll1111l11_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack1lllll11lll1_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack1ll_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡩ࡭ࡱࡺࡥࡳࠢࡦࡳࡳ࡬ࡩࡨࠢ࡮ࡩࡾࡹࠠࡣࡻࠣࡶࡪ࡭ࡥࡹࠢࡰࡥࡹࡩࡨ࠻ࠢࡾࢁࠧ⍯").format(e))
    return bstack1llll1111l11_opy_
def bstack1llll1ll1l1l_opy_(bstack1lllll11l11l_opy_, bstack1lllllll1111_opy_):
    bstack1lllllll111l_opy_ = version.parse(bstack1lllll11l11l_opy_)
    bstack1llll1l1llll_opy_ = version.parse(bstack1lllllll1111_opy_)
    if bstack1lllllll111l_opy_ > bstack1llll1l1llll_opy_:
        return 1
    elif bstack1lllllll111l_opy_ < bstack1llll1l1llll_opy_:
        return -1
    else:
        return 0
def bstack1lll1l111l1_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack1llll111l1l1_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
def bstack1lllll1l1l11_opy_(framework):
    from browserstack_sdk._version import __version__
    return str(framework) + str(__version__)
def bstack111l11ll1l_opy_(options, framework, config, bstack111ll1l1ll_opy_={}):
    if options is None:
        return
    if getattr(options, bstack1ll_opy_ (u"ࠧࡨࡧࡷࠫ⍰"), None):
        caps = options
    else:
        caps = options.to_capabilities()
    bstack111l11l111_opy_ = caps.get(bstack1ll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ⍱"))
    bstack1lll1llllll1_opy_ = True
    bstack1l1111l11l_opy_ = os.environ[bstack1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ⍲")]
    bstack1l111l1l111_opy_ = config.get(bstack1ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ⍳"), False)
    if bstack1l111l1l111_opy_:
        bstack1l1l11ll1ll_opy_ = config.get(bstack1ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫ⍴"), {})
        bstack1l1l11ll1ll_opy_[bstack1ll_opy_ (u"ࠬࡧࡵࡵࡪࡗࡳࡰ࡫࡮ࠨ⍵")] = os.getenv(bstack1ll_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫ⍶"))
        bstack111ll1ll1l_opy_ = json.loads(os.getenv(bstack1ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨ⍷"), bstack1ll_opy_ (u"ࠨࡽࢀࠫ⍸"))).get(bstack1ll_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ⍹"))
    if bstack1lll1lllllll_opy_(caps.get(bstack1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡸࡷࡪ࡝࠳ࡄࠩ⍺"))) or bstack1lll1lllllll_opy_(caps.get(bstack1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡹࡸ࡫࡟ࡸ࠵ࡦࠫ⍻"))):
        bstack1lll1llllll1_opy_ = False
    if bstack111lll1ll_opy_({bstack1ll_opy_ (u"ࠧࡻࡳࡦ࡙࠶ࡇࠧ⍼"): bstack1lll1llllll1_opy_}):
        bstack111l11l111_opy_ = bstack111l11l111_opy_ or {}
        bstack111l11l111_opy_[bstack1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨ⍽")] = bstack1lllll1l1l11_opy_(framework)
        bstack111l11l111_opy_[bstack1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩ⍾")] = bstack1lll1ll1ll_opy_()
        bstack111l11l111_opy_[bstack1ll_opy_ (u"ࠨࡶࡨࡷࡹ࡮ࡵࡣࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫ⍿")] = bstack1l1111l11l_opy_
        bstack111l11l111_opy_[bstack1ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫ⎀")] = bstack111ll1l1ll_opy_
        if bstack1l111l1l111_opy_:
            bstack111l11l111_opy_[bstack1ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ⎁")] = bstack1l111l1l111_opy_
            bstack111l11l111_opy_[bstack1ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫ⎂")] = bstack1l1l11ll1ll_opy_
            bstack111l11l111_opy_[bstack1ll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬ⎃")][bstack1ll_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ⎄")] = bstack111ll1ll1l_opy_
        if getattr(options, bstack1ll_opy_ (u"ࠧࡴࡧࡷࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡹࠨ⎅"), None):
            options.set_capability(bstack1ll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ⎆"), bstack111l11l111_opy_)
        else:
            options[bstack1ll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪ⎇")] = bstack111l11l111_opy_
    else:
        if getattr(options, bstack1ll_opy_ (u"ࠪࡷࡪࡺ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶࡼࠫ⎈"), None):
            options.set_capability(bstack1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬ⎉"), bstack1lllll1l1l11_opy_(framework))
            options.set_capability(bstack1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭⎊"), bstack1lll1ll1ll_opy_())
            options.set_capability(bstack1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡺࡥࡴࡶ࡫ࡹࡧࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨ⎋"), bstack1l1111l11l_opy_)
            options.set_capability(bstack1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨ⎌"), bstack111ll1l1ll_opy_)
            if bstack1l111l1l111_opy_:
                options.set_capability(bstack1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ⎍"), bstack1l111l1l111_opy_)
                options.set_capability(bstack1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ⎎"), bstack1l1l11ll1ll_opy_)
                options.set_capability(bstack1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴ࠰ࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ⎏"), bstack111ll1ll1l_opy_)
        else:
            options[bstack1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬ⎐")] = bstack1lllll1l1l11_opy_(framework)
            options[bstack1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭⎑")] = bstack1lll1ll1ll_opy_()
            options[bstack1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡺࡥࡴࡶ࡫ࡹࡧࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨ⎒")] = bstack1l1111l11l_opy_
            options[bstack1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨ⎓")] = bstack111ll1l1ll_opy_
            if bstack1l111l1l111_opy_:
                options[bstack1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ⎔")] = bstack1l111l1l111_opy_
                options[bstack1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ⎕")] = bstack1l1l11ll1ll_opy_
                options[bstack1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩ⎖")][bstack1ll_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ⎗")] = bstack111ll1ll1l_opy_
    return options
def bstack1llll1llll11_opy_(ws_endpoint, framework):
    bstack111ll1l1ll_opy_ = global_config.get_property(bstack1ll_opy_ (u"ࠧࡖࡌࡂ࡛࡚ࡖࡎࡍࡈࡕࡡࡓࡖࡔࡊࡕࡄࡖࡢࡑࡆࡖࠢ⎘"))
    if ws_endpoint and len(ws_endpoint.split(bstack1ll_opy_ (u"࠭ࡣࡢࡲࡶࡁࠬ⎙"))) > 1:
        ws_url = ws_endpoint.split(bstack1ll_opy_ (u"ࠧࡤࡣࡳࡷࡂ࠭⎚"))[0]
        if bstack1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫ⎛") in ws_url:
            from browserstack_sdk._version import __version__
            bstack1lllll11ll11_opy_ = json.loads(urllib.parse.unquote(ws_endpoint.split(bstack1ll_opy_ (u"ࠩࡦࡥࡵࡹ࠽ࠨ⎜"))[1]))
            bstack1lllll11ll11_opy_ = bstack1lllll11ll11_opy_ or {}
            bstack1l1111l11l_opy_ = os.environ[bstack1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ⎝")]
            bstack1lllll11ll11_opy_[bstack1ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬ⎞")] = str(framework) + str(__version__)
            bstack1lllll11ll11_opy_[bstack1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭⎟")] = bstack1lll1ll1ll_opy_()
            bstack1lllll11ll11_opy_[bstack1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡺࡥࡴࡶ࡫ࡹࡧࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨ⎠")] = bstack1l1111l11l_opy_
            bstack1lllll11ll11_opy_[bstack1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨ⎡")] = bstack111ll1l1ll_opy_
            ws_endpoint = ws_endpoint.split(bstack1ll_opy_ (u"ࠨࡥࡤࡴࡸࡃࠧ⎢"))[0] + bstack1ll_opy_ (u"ࠩࡦࡥࡵࡹ࠽ࠨ⎣") + urllib.parse.quote(json.dumps(bstack1lllll11ll11_opy_))
    return ws_endpoint
def bstack1l11lllll1_opy_():
    global bstack11111l11l_opy_
    from playwright._impl._browser_type import BrowserType
    bstack11111l11l_opy_ = BrowserType.connect
    return bstack11111l11l_opy_
def bstack1lllll11l111_opy_(framework_name):
    global FRAMEWORK_NAME
    FRAMEWORK_NAME = framework_name
    return framework_name
def bstack1l11l11l111_opy_(self, *args, **kwargs):
    global bstack11111l11l_opy_
    try:
        global FRAMEWORK_NAME
        if bstack1ll_opy_ (u"ࠪࡻࡸࡋ࡮ࡥࡲࡲ࡭ࡳࡺࠧ⎤") in kwargs:
            kwargs[bstack1ll_opy_ (u"ࠫࡼࡹࡅ࡯ࡦࡳࡳ࡮ࡴࡴࠨ⎥")] = bstack1llll1llll11_opy_(
                kwargs.get(bstack1ll_opy_ (u"ࠬࡽࡳࡆࡰࡧࡴࡴ࡯࡮ࡵࠩ⎦"), None),
                FRAMEWORK_NAME
            )
    except Exception as e:
        logger.error(bstack1ll_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡦࡰࠣࡴࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡔࡆࡎࠤࡨࡧࡰࡴ࠼ࠣࡿࢂࠨ⎧").format(str(e)))
    return bstack11111l11l_opy_(self, *args, **kwargs)
def bstack1llll1ll1111_opy_(bstack1llll1111ll1_opy_, proxies):
    proxy_settings = {}
    try:
        if not proxies:
            proxies = bstack11l11ll11_opy_(bstack1llll1111ll1_opy_, bstack1ll_opy_ (u"ࠢࠣ⎨"))
        if proxies and proxies.get(bstack1ll_opy_ (u"ࠣࡪࡷࡸࡵࡹࠢ⎩")):
            parsed_url = urlparse(proxies.get(bstack1ll_opy_ (u"ࠤ࡫ࡸࡹࡶࡳࠣ⎪")))
            if parsed_url and parsed_url.hostname: proxy_settings[bstack1ll_opy_ (u"ࠪࡴࡷࡵࡸࡺࡊࡲࡷࡹ࠭⎫")] = str(parsed_url.hostname)
            if parsed_url and parsed_url.port: proxy_settings[bstack1ll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡓࡳࡷࡺࠧ⎬")] = str(parsed_url.port)
            if parsed_url and parsed_url.username: proxy_settings[bstack1ll_opy_ (u"ࠬࡶࡲࡰࡺࡼ࡙ࡸ࡫ࡲࠨ⎭")] = str(parsed_url.username)
            if parsed_url and parsed_url.password: proxy_settings[bstack1ll_opy_ (u"࠭ࡰࡳࡱࡻࡽࡕࡧࡳࡴࠩ⎮")] = str(parsed_url.password)
        return proxy_settings
    except:
        return proxy_settings
def bstack111111l111_opy_(bstack1llll1111ll1_opy_):
    bstack1llllll111l1_opy_ = {
        bstack111111lllll_opy_[bstack1llllll1lll1_opy_]: bstack1llll1111ll1_opy_[bstack1llllll1lll1_opy_]
        for bstack1llllll1lll1_opy_ in bstack1llll1111ll1_opy_
        if bstack1llllll1lll1_opy_ in bstack111111lllll_opy_
    }
    bstack1llllll111l1_opy_[bstack1ll_opy_ (u"ࠢࡱࡴࡲࡼࡾ࡙ࡥࡵࡶ࡬ࡲ࡬ࡹࠢ⎯")] = bstack1llll1ll1111_opy_(bstack1llll1111ll1_opy_, global_config.get_property(bstack1ll_opy_ (u"ࠣࡲࡵࡳࡽࡿࡓࡦࡶࡷ࡭ࡳ࡭ࡳࠣ⎰")))
    bstack1llllll11l11_opy_ = [element.lower() for element in bstack111111ll11l_opy_]
    bstack1llll1l1ll1l_opy_(bstack1llllll111l1_opy_, bstack1llllll11l11_opy_)
    return bstack1llllll111l1_opy_
def bstack1llll1l1ll1l_opy_(d, keys):
    for key in list(d.keys()):
        if key.lower() in keys:
            d[key] = bstack1ll_opy_ (u"ࠤ࠭࠮࠯࠰ࠢ⎱")
    for value in d.values():
        if isinstance(value, dict):
            bstack1llll1l1ll1l_opy_(value, keys)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    bstack1llll1l1ll1l_opy_(item, keys)
def bstack11lll1l1111_opy_():
    bstack1llll1l111ll_opy_ = [os.environ.get(bstack1ll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡍࡑࡋࡓࡠࡆࡌࡖࠧ⎲")), os.path.join(os.path.expanduser(bstack1ll_opy_ (u"ࠦࢃࠨ⎳")), bstack1ll_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ⎴")), os.path.join(bstack1ll_opy_ (u"࠭࠯ࡵ࡯ࡳࠫ⎵"), bstack1ll_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ⎶"))]
    for path in bstack1llll1l111ll_opy_:
        if path is None:
            continue
        try:
            if os.path.exists(path):
                logger.debug(bstack1ll_opy_ (u"ࠣࡈ࡬ࡰࡪࠦࠧࠣ⎷") + str(path) + bstack1ll_opy_ (u"ࠤࠪࠤࡪࡾࡩࡴࡶࡶ࠲ࠧ⎸"))
                if not os.access(path, os.W_OK):
                    logger.debug(bstack1ll_opy_ (u"ࠥࡋ࡮ࡼࡩ࡯ࡩࠣࡴࡪࡸ࡭ࡪࡵࡶ࡭ࡴࡴࡳࠡࡨࡲࡶࠥ࠭ࠢ⎹") + str(path) + bstack1ll_opy_ (u"ࠦࠬࠨ⎺"))
                    os.chmod(path, 0o777)
                else:
                    logger.debug(bstack1ll_opy_ (u"ࠧࡌࡩ࡭ࡧࠣࠫࠧ⎻") + str(path) + bstack1ll_opy_ (u"ࠨࠧࠡࡣ࡯ࡶࡪࡧࡤࡺࠢ࡫ࡥࡸࠦࡴࡩࡧࠣࡶࡪࡷࡵࡪࡴࡨࡨࠥࡶࡥࡳ࡯࡬ࡷࡸ࡯࡯࡯ࡵ࠱ࠦ⎼"))
            else:
                logger.debug(bstack1ll_opy_ (u"ࠢࡄࡴࡨࡥࡹ࡯࡮ࡨࠢࡩ࡭ࡱ࡫ࠠࠨࠤ⎽") + str(path) + bstack1ll_opy_ (u"ࠣࠩࠣࡻ࡮ࡺࡨࠡࡹࡵ࡭ࡹ࡫ࠠࡱࡧࡵࡱ࡮ࡹࡳࡪࡱࡱ࠲ࠧ⎾"))
                os.makedirs(path, exist_ok=True)
                os.chmod(path, 0o777)
            logger.debug(bstack1ll_opy_ (u"ࠤࡒࡴࡪࡸࡡࡵ࡫ࡲࡲࠥࡹࡵࡤࡥࡨࡩࡩ࡫ࡤࠡࡨࡲࡶࠥ࠭ࠢ⎿") + str(path) + bstack1ll_opy_ (u"ࠥࠫ࠳ࠨ⏀"))
            return path
        except Exception as e:
            logger.debug(bstack1ll_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࠤࡺࡶࠠࡧ࡫࡯ࡩࠥ࠭ࡻࡱࡣࡷ࡬ࢂ࠭࠺ࠡࠤ⏁") + str(e) + bstack1ll_opy_ (u"ࠧࠨ⏂"))
    logger.debug(bstack1ll_opy_ (u"ࠨࡁ࡭࡮ࠣࡴࡦࡺࡨࡴࠢࡩࡥ࡮ࡲࡥࡥ࠰ࠥ⏃"))
    return None
@measure(event_name=EVENTS.bstack111111l1l11_opy_, stage=STAGE.bstack11llll111l_opy_)
def bstack1ll1l1l111l_opy_(binary_path, bstack1ll1l11llll_opy_, bs_config):
    logger.debug(bstack1ll_opy_ (u"ࠢࡄࡷࡵࡶࡪࡴࡴࠡࡅࡏࡍࠥࡖࡡࡵࡪࠣࡪࡴࡻ࡮ࡥ࠼ࠣࡿࢂࠨ⏄").format(binary_path))
    bstack1llll1ll1lll_opy_ = bstack1ll_opy_ (u"ࠨࠩ⏅")
    bstack1lllll1ll11l_opy_ = {
        bstack1ll_opy_ (u"ࠩࡶࡨࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ⏆"): __version__,
        bstack1ll_opy_ (u"ࠥࡳࡸࠨ⏇"): platform.system(),
        bstack1ll_opy_ (u"ࠦࡴࡹ࡟ࡢࡴࡦ࡬ࠧ⏈"): platform.machine(),
        bstack1ll_opy_ (u"ࠧࡩ࡬ࡪࡡࡹࡩࡷࡹࡩࡰࡰࠥ⏉"): bstack1ll_opy_ (u"࠭࠰ࠨ⏊"),
        bstack1ll_opy_ (u"ࠢࡴࡦ࡮ࡣࡱࡧ࡮ࡨࡷࡤ࡫ࡪࠨ⏋"): bstack1ll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ⏌")
    }
    bstack1llll11ll1l1_opy_(bstack1lllll1ll11l_opy_)
    try:
        if binary_path:
            if bstack1lllll1lllll_opy_():
                bstack1lllll1ll11l_opy_[bstack1ll_opy_ (u"ࠩࡦࡰ࡮ࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ⏍")] = subprocess.check_output([binary_path, bstack1ll_opy_ (u"ࠥࡺࡪࡸࡳࡪࡱࡱࠦ⏎")]).strip().decode(bstack1ll_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪ⏏"))
            else:
                bstack1lllll1ll11l_opy_[bstack1ll_opy_ (u"ࠬࡩ࡬ࡪࡡࡹࡩࡷࡹࡩࡰࡰࠪ⏐")] = subprocess.check_output([binary_path, bstack1ll_opy_ (u"ࠨࡶࡦࡴࡶ࡭ࡴࡴࠢ⏑")], stderr=subprocess.DEVNULL).strip().decode(bstack1ll_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭⏒"))
        response = requests.request(
            bstack1ll_opy_ (u"ࠨࡉࡈࡘࠬ⏓"),
            url=bstack1l11llll1_opy_(bstack11111ll1l11_opy_),
            headers=None,
            auth=(bs_config[bstack1ll_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ⏔")], bs_config[bstack1ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭⏕")]),
            json=None,
            params=bstack1lllll1ll11l_opy_
        )
        data = response.json()
        if response.status_code == 200 and bstack1ll_opy_ (u"ࠫࡺࡸ࡬ࠨ⏖") in data.keys() and bstack1ll_opy_ (u"ࠬࡻࡰࡥࡣࡷࡩࡩࡥࡣ࡭࡫ࡢࡺࡪࡸࡳࡪࡱࡱࠫ⏗") in data.keys():
            logger.debug(bstack1ll_opy_ (u"ࠨࡎࡦࡧࡧࠤࡹࡵࠠࡶࡲࡧࡥࡹ࡫ࠠࡣ࡫ࡱࡥࡷࡿࠬࠡࡥࡸࡶࡷ࡫࡮ࡵࠢࡥ࡭ࡳࡧࡲࡺࠢࡹࡩࡷࡹࡩࡰࡰ࠽ࠤࢀࢃࠢ⏘").format(bstack1lllll1ll11l_opy_[bstack1ll_opy_ (u"ࠧࡤ࡮࡬ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ⏙")]))
            if bstack1ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡋࡑࡅࡗ࡟࡟ࡖࡔࡏࠫ⏚") in os.environ:
                logger.debug(bstack1ll_opy_ (u"ࠤࡖ࡯࡮ࡶࡰࡪࡰࡪࠤࡧ࡯࡮ࡢࡴࡼࠤࡩࡵࡷ࡯࡮ࡲࡥࡩࠦࡡࡴࠢࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡌࡒࡆࡘ࡙ࡠࡗࡕࡐࠥ࡯ࡳࠡࡵࡨࡸࠧ⏛"))
                data[bstack1ll_opy_ (u"ࠪࡹࡷࡲࠧ⏜")] = os.environ[bstack1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆࡎࡔࡁࡓ࡛ࡢ࡙ࡗࡒࠧ⏝")]
            bstack1llll1lll1ll_opy_ = bstack1lllll1111l1_opy_(data[bstack1ll_opy_ (u"ࠬࡻࡲ࡭ࠩ⏞")], bstack1ll1l11llll_opy_)
            bstack1llll1ll1lll_opy_ = os.path.join(bstack1ll1l11llll_opy_, bstack1llll1lll1ll_opy_)
            os.chmod(bstack1llll1ll1lll_opy_, 0o777) # bstack1llllll1l1l1_opy_ permission
            return bstack1llll1ll1lll_opy_
    except Exception as e:
        logger.debug(bstack1ll_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡩࡵࡷ࡯࡮ࡲࡥࡩ࡯࡮ࡨࠢࡱࡩࡼࠦࡓࡅࡍࠣࡿࢂࠨ⏟").format(e))
    return binary_path
def bstack1llll11ll1l1_opy_(bstack1lllll1ll11l_opy_):
    try:
        if bstack1ll_opy_ (u"ࠧ࡭࡫ࡱࡹࡽ࠭⏠") not in bstack1lllll1ll11l_opy_[bstack1ll_opy_ (u"ࠨࡱࡶࠫ⏡")].lower():
            return
        if os.path.exists(bstack1ll_opy_ (u"ࠤ࠲ࡩࡹࡩ࠯ࡰࡵ࠰ࡶࡪࡲࡥࡢࡵࡨࠦ⏢")):
            with open(bstack1ll_opy_ (u"ࠥ࠳ࡪࡺࡣ࠰ࡱࡶ࠱ࡷ࡫࡬ࡦࡣࡶࡩࠧ⏣"), bstack1ll_opy_ (u"ࠦࡷࠨ⏤")) as f:
                bstack1llll11l1lll_opy_ = {}
                for line in f:
                    if bstack1ll_opy_ (u"ࠧࡃࠢ⏥") in line:
                        key, value = line.rstrip().split(bstack1ll_opy_ (u"ࠨ࠽ࠣ⏦"), 1)
                        bstack1llll11l1lll_opy_[key] = value.strip(bstack1ll_opy_ (u"ࠧࠣ࡞ࠪࠫ⏧"))
                bstack1lllll1ll11l_opy_[bstack1ll_opy_ (u"ࠨࡦ࡬ࡷࡹࡸ࡯ࠨ⏨")] = bstack1llll11l1lll_opy_.get(bstack1ll_opy_ (u"ࠤࡌࡈࠧ⏩"), bstack1ll_opy_ (u"ࠥࠦ⏪"))
        elif os.path.exists(bstack1ll_opy_ (u"ࠦ࠴࡫ࡴࡤ࠱ࡤࡰࡵ࡯࡮ࡦ࠯ࡵࡩࡱ࡫ࡡࡴࡧࠥ⏫")):
            bstack1lllll1ll11l_opy_[bstack1ll_opy_ (u"ࠬࡪࡩࡴࡶࡵࡳࠬ⏬")] = bstack1ll_opy_ (u"࠭ࡡ࡭ࡲ࡬ࡲࡪ࠭⏭")
    except Exception as e:
        logger.debug(bstack1ll_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣ࡫ࡪࡺࠠࡥ࡫ࡶࡸࡷࡵࠠࡰࡨࠣࡰ࡮ࡴࡵࡹࠤ⏮") + e)
@measure(event_name=EVENTS.bstack11111l1l1ll_opy_, stage=STAGE.bstack11llll111l_opy_)
def bstack1lllll1111l1_opy_(bstack1llll1l1ll11_opy_, bstack1lllll1l1111_opy_):
    logger.debug(bstack1ll_opy_ (u"ࠣࡆࡲࡻࡳࡲ࡯ࡢࡦ࡬ࡲ࡬ࠦࡓࡅࡍࠣࡦ࡮ࡴࡡࡳࡻࠣࡪࡷࡵ࡭࠻ࠢࠥ⏯") + str(bstack1llll1l1ll11_opy_) + bstack1ll_opy_ (u"ࠤࠥ⏰"))
    zip_path = os.path.join(bstack1lllll1l1111_opy_, bstack1ll_opy_ (u"ࠥࡨࡴࡽ࡮࡭ࡱࡤࡨࡪࡪ࡟ࡧ࡫࡯ࡩ࠳ࢀࡩࡱࠤ⏱"))
    bstack1llll1lll1ll_opy_ = bstack1ll_opy_ (u"ࠫࠬ⏲")
    with requests.get(bstack1llll1l1ll11_opy_, stream=True) as response:
        response.raise_for_status()
        with open(zip_path, bstack1ll_opy_ (u"ࠧࡽࡢࠣ⏳")) as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        logger.debug(bstack1ll_opy_ (u"ࠨࡆࡪ࡮ࡨࠤࡩࡵࡷ࡯࡮ࡲࡥࡩ࡫ࡤࠡࡵࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࡱࡿ࠮ࠣ⏴"))
    with zipfile.ZipFile(zip_path, bstack1ll_opy_ (u"ࠧࡳࠩ⏵")) as zip_ref:
        bstack1llll1lll11l_opy_ = zip_ref.namelist()
        if len(bstack1llll1lll11l_opy_) > 0:
            bstack1llll1lll1ll_opy_ = bstack1llll1lll11l_opy_[0] # bstack1llll11l111l_opy_ bstack11111l1111l_opy_ will be bstack1llll1111l1l_opy_ 1 file i.e. the binary in the zip
        zip_ref.extractall(bstack1lllll1l1111_opy_)
        logger.debug(bstack1ll_opy_ (u"ࠣࡈ࡬ࡰࡪࡹࠠࡴࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࡰࡾࠦࡥࡹࡶࡵࡥࡨࡺࡥࡥࠢࡷࡳࠥ࠭ࠢ⏶") + str(bstack1lllll1l1111_opy_) + bstack1ll_opy_ (u"ࠤࠪࠦ⏷"))
    os.remove(zip_path)
    return bstack1llll1lll1ll_opy_
def get_cli_dir():
    bstack1lllllll1l11_opy_ = bstack11lll1l1111_opy_()
    if bstack1lllllll1l11_opy_:
        bstack1ll1l11llll_opy_ = os.path.join(bstack1lllllll1l11_opy_, bstack1ll_opy_ (u"ࠥࡧࡱ࡯ࠢ⏸"))
        if not os.path.exists(bstack1ll1l11llll_opy_):
            os.makedirs(bstack1ll1l11llll_opy_, mode=0o777, exist_ok=True)
        return bstack1ll1l11llll_opy_
    else:
        raise FileNotFoundError(bstack1ll_opy_ (u"ࠦࡓࡵࠠࡸࡴ࡬ࡸࡦࡨ࡬ࡦࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥࡧࡶࡢ࡫࡯ࡥࡧࡲࡥࠡࡨࡲࡶࠥࡺࡨࡦࠢࡖࡈࡐࠦࡢࡪࡰࡤࡶࡾ࠴ࠢ⏹"))
def bstack1ll1l11l1l1_opy_(bstack1ll1l11llll_opy_):
    bstack1ll_opy_ (u"ࠧࠨࠢࡈࡧࡷࠤࡹ࡮ࡥࠡࡲࡤࡸ࡭ࠦࡦࡰࡴࠣࡸ࡭࡫ࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡓࡅࡍࠣࡦ࡮ࡴࡡࡳࡻࠣ࡭ࡳࠦࡡࠡࡹࡵ࡭ࡹࡧࡢ࡭ࡧࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾ࠴ࠢࠣࠤ⏺")
    bstack1llll111ll1l_opy_ = [
        os.path.join(bstack1ll1l11llll_opy_, f)
        for f in os.listdir(bstack1ll1l11llll_opy_)
        if os.path.isfile(os.path.join(bstack1ll1l11llll_opy_, f)) and f.startswith(bstack1ll_opy_ (u"ࠨࡢࡪࡰࡤࡶࡾ࠳ࠢ⏻"))
    ]
    if len(bstack1llll111ll1l_opy_) > 0:
        return max(bstack1llll111ll1l_opy_, key=os.path.getmtime) # get bstack1llll1l11111_opy_ binary
    return bstack1ll_opy_ (u"ࠢࠣ⏼")
def bstack1111l1l1lll_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1l111l1llll_opy_(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = bstack1l111l1llll_opy_(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack11lll111ll_opy_(data, keys, default=None):
    bstack1ll_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡕࡤࡪࡪࡲࡹࠡࡩࡨࡸࠥࡧࠠ࡯ࡧࡶࡸࡪࡪࠠࡷࡣ࡯ࡹࡪࠦࡦࡳࡱࡰࠤࡦࠦࡤࡪࡥࡷ࡭ࡴࡴࡡࡳࡻࠣࡳࡷࠦ࡬ࡪࡵࡷ࠲ࠏࠦࠠࠡࠢ࠽ࡴࡦࡸࡡ࡮ࠢࡧࡥࡹࡧ࠺ࠡࡖ࡫ࡩࠥࡪࡩࡤࡶ࡬ࡳࡳࡧࡲࡺࠢࡲࡶࠥࡲࡩࡴࡶࠣࡸࡴࠦࡴࡳࡣࡹࡩࡷࡹࡥ࠯ࠌࠣࠤࠥࠦ࠺ࡱࡣࡵࡥࡲࠦ࡫ࡦࡻࡶ࠾ࠥࡇࠠ࡭࡫ࡶࡸࠥࡵࡦࠡ࡭ࡨࡽࡸ࠵ࡩ࡯ࡦ࡬ࡧࡪࡹࠠࡳࡧࡳࡶࡪࡹࡥ࡯ࡶ࡬ࡲ࡬ࠦࡴࡩࡧࠣࡴࡦࡺࡨ࠯ࠌࠣࠤࠥࠦ࠺ࡱࡣࡵࡥࡲࠦࡤࡦࡨࡤࡹࡱࡺ࠺ࠡࡘࡤࡰࡺ࡫ࠠࡵࡱࠣࡶࡪࡺࡵࡳࡰࠣ࡭࡫ࠦࡴࡩࡧࠣࡴࡦࡺࡨࠡࡦࡲࡩࡸࠦ࡮ࡰࡶࠣࡩࡽ࡯ࡳࡵ࠰ࠍࠤࠥࠦࠠ࠻ࡴࡨࡸࡺࡸ࡮࠻ࠢࡗ࡬ࡪࠦࡶࡢ࡮ࡸࡩࠥࡧࡴࠡࡶ࡫ࡩࠥࡴࡥࡴࡶࡨࡨࠥࡶࡡࡵࡪ࠯ࠤࡴࡸࠠࡥࡧࡩࡥࡺࡲࡴࠡ࡫ࡩࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪ࠮ࠋࠢࠣࠤࠥࠨࠢࠣ⏽")
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
def bstack1ll11l1111_opy_(bstack1lllll1ll1l1_opy_, key, value):
    bstack1ll_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࡖࡸࡴࡸࡥࠡࡅࡏࡍࠥ࡫࡮ࡷ࡫ࡵࡳࡳࡳࡥ࡯ࡶࠣࡺࡦࡸࡩࡢࡤ࡯ࡩࡸࠦ࡭ࡢࡲࡳ࡭ࡳ࡭ࠠࡪࡰࠣࡸ࡭࡫ࠠࡱࡴࡲࡺ࡮ࡪࡥࡥࠢࡧ࡭ࡨࡺࡩࡰࡰࡤࡶࡾ࠴ࠊࠡࠢࠣࠤࡆࡸࡧࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡨࡲࡩࡠࡧࡱࡺࡤࡼࡡࡳࡵࡢࡱࡦࡶ࠺ࠡࡆ࡬ࡧࡹ࡯࡯࡯ࡣࡵࡽࠥࡺ࡯ࠡࡵࡷࡳࡷ࡫ࠠࡦࡰࡹ࡭ࡷࡵ࡮࡮ࡧࡱࡸࠥࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠠ࡮ࡣࡳࡴ࡮ࡴࡧࡴࠌࠣࠤࠥࠦࠠࠡࠢࠣ࡯ࡪࡿ࠺ࠡࡍࡨࡽࠥ࡬ࡲࡰ࡯ࠣࡇࡑࡏ࡟ࡄࡃࡓࡗࡤ࡚ࡏࡠࡅࡒࡒࡋࡏࡇࠋࠢࠣࠤࠥࠦࠠࠡࠢࡹࡥࡱࡻࡥ࠻࡙ࠢࡥࡱࡻࡥࠡࡨࡵࡳࡲࠦࡣࡰ࡯ࡰࡥࡳࡪࠠ࡭࡫ࡱࡩࠥࡧࡲࡨࡷࡰࡩࡳࡺࡳࠋࠢࠣࠤࠥࠨࠢࠣ⏾")
    if key in bstack1ll111llll_opy_:
        bstack11l1l11ll1_opy_ = bstack1ll111llll_opy_[key]
        if isinstance(bstack11l1l11ll1_opy_, list):
            for env_name in bstack11l1l11ll1_opy_:
                bstack1lllll1ll1l1_opy_[env_name] = value
        else:
            bstack1lllll1ll1l1_opy_[bstack11l1l11ll1_opy_] = value