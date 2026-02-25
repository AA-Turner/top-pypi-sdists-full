# coding: UTF-8
import sys
bstack1_opy_ = sys.version_info [0] == 2
bstack11ll1l_opy_ = 2048
bstack1lllllll_opy_ = 7
def bstack11l1l11_opy_ (bstack11lllll_opy_):
    global bstack111l1ll_opy_
    bstack111111l_opy_ = ord (bstack11lllll_opy_ [-1])
    bstack1llllll_opy_ = bstack11lllll_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack111111l_opy_ % len (bstack1llllll_opy_)
    bstack1l11l_opy_ = bstack1llllll_opy_ [:bstack11ll1ll_opy_] + bstack1llllll_opy_ [bstack11ll1ll_opy_:]
    if bstack1_opy_:
        bstack1lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    else:
        bstack1lll11_opy_ = str () .join ([chr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    return eval (bstack1lll11_opy_)
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
from bstack_utils.constants import (bstack1ll11lll1l_opy_, bstack11ll1l1l11_opy_, HTTPS_HUB,
                                    bstack111ll1ll11l_opy_, bstack111ll1lll1l_opy_, bstack111llll1l1l_opy_, bstack111lll11l1l_opy_)
from bstack_utils.measure import measure
from bstack_utils.messages import bstack1111l1lll_opy_, bstack1l1ll1l1l1_opy_
from bstack_utils.proxy import bstack1lll1l11l1_opy_, bstack11lll1ll11_opy_
from bstack_utils.constants import *
from bstack_utils import logger_utils
from bstack_utils.bstack1ll1l11ll_opy_ import bstack11l11lll_opy_
from browserstack_sdk._version import __version__
global_config = Config.get_instance()
logger = logger_utils.get_logger(__name__, logger_utils.bstack1ll1111l11l_opy_())
bstack11ll111ll_opy_ = logger_utils.bstack1lll1lll_opy_(__name__)
def bstack11l11l1111l_opy_(config):
    return config[bstack11l1l11_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬᴷ")]
def bstack11l11l11l11_opy_(config):
    return config[bstack11l1l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧᴸ")]
def bstack11ll1111ll_opy_():
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
def bstack111l1ll1ll1_opy_(obj):
    values = []
    bstack1111llllll1_opy_ = re.compile(bstack11l1l11_opy_ (u"ࡷࠨ࡞ࡄࡗࡖࡘࡔࡓ࡟ࡕࡃࡊࡣࡡࡪࠫࠥࠤᴹ"), re.I)
    for key in obj.keys():
        if bstack1111llllll1_opy_.match(key):
            values.append(obj[key])
    return values
def bstack111l1l1ll11_opy_(config):
    tags = []
    tags.extend(bstack111l1ll1ll1_opy_(os.environ))
    tags.extend(bstack111l1ll1ll1_opy_(config))
    return tags
def bstack111l1l11111_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack111l1l11l1l_opy_(bstack111l1ll111l_opy_):
    if not bstack111l1ll111l_opy_:
        return bstack11l1l11_opy_ (u"࠭ࠧᴺ")
    return bstack11l1l11_opy_ (u"ࠢࡼࡿࠣࠬࢀࢃࠩࠣᴻ").format(bstack111l1ll111l_opy_.name, bstack111l1ll111l_opy_.email)
def bstack11l11ll11ll_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack111l11l1lll_opy_ = repo.common_dir
        info = {
            bstack11l1l11_opy_ (u"ࠣࡵ࡫ࡥࠧᴼ"): repo.head.commit.hexsha,
            bstack11l1l11_opy_ (u"ࠤࡶ࡬ࡴࡸࡴࡠࡵ࡫ࡥࠧᴽ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack11l1l11_opy_ (u"ࠥࡦࡷࡧ࡮ࡤࡪࠥᴾ"): repo.active_branch.name,
            bstack11l1l11_opy_ (u"ࠦࡹࡧࡧࠣᴿ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack11l1l11_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡹ࡫ࡲࠣᵀ"): bstack111l1l11l1l_opy_(repo.head.commit.committer),
            bstack11l1l11_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡺࡥࡳࡡࡧࡥࡹ࡫ࠢᵁ"): repo.head.commit.committed_datetime.isoformat(),
            bstack11l1l11_opy_ (u"ࠢࡢࡷࡷ࡬ࡴࡸࠢᵂ"): bstack111l1l11l1l_opy_(repo.head.commit.author),
            bstack11l1l11_opy_ (u"ࠣࡣࡸࡸ࡭ࡵࡲࡠࡦࡤࡸࡪࠨᵃ"): repo.head.commit.authored_datetime.isoformat(),
            bstack11l1l11_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡡࡰࡩࡸࡹࡡࡨࡧࠥᵄ"): repo.head.commit.message,
            bstack11l1l11_opy_ (u"ࠥࡶࡴࡵࡴࠣᵅ"): repo.git.rev_parse(bstack11l1l11_opy_ (u"ࠦ࠲࠳ࡳࡩࡱࡺ࠱ࡹࡵࡰ࡭ࡧࡹࡩࡱࠨᵆ")),
            bstack11l1l11_opy_ (u"ࠧࡩ࡯࡮࡯ࡲࡲࡤ࡭ࡩࡵࡡࡧ࡭ࡷࠨᵇ"): bstack111l11l1lll_opy_,
            bstack11l1l11_opy_ (u"ࠨࡷࡰࡴ࡮ࡸࡷ࡫ࡥࡠࡩ࡬ࡸࡤࡪࡩࡳࠤᵈ"): subprocess.check_output([bstack11l1l11_opy_ (u"ࠢࡨ࡫ࡷࠦᵉ"), bstack11l1l11_opy_ (u"ࠣࡴࡨࡺ࠲ࡶࡡࡳࡵࡨࠦᵊ"), bstack11l1l11_opy_ (u"ࠤ࠰࠱࡬࡯ࡴ࠮ࡥࡲࡱࡲࡵ࡮࠮ࡦ࡬ࡶࠧᵋ")]).strip().decode(
                bstack11l1l11_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩᵌ")),
            bstack11l1l11_opy_ (u"ࠦࡱࡧࡳࡵࡡࡷࡥ࡬ࠨᵍ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack11l1l11_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡸࡥࡳࡪࡰࡦࡩࡤࡲࡡࡴࡶࡢࡸࡦ࡭ࠢᵎ"): repo.git.rev_list(
                bstack11l1l11_opy_ (u"ࠨࡻࡾ࠰࠱ࡿࢂࠨᵏ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack1111l1ll11l_opy_ = []
        for remote in remotes:
            bstack111l1llll11_opy_ = {
                bstack11l1l11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᵐ"): remote.name,
                bstack11l1l11_opy_ (u"ࠣࡷࡵࡰࠧᵑ"): remote.url,
            }
            bstack1111l1ll11l_opy_.append(bstack111l1llll11_opy_)
        bstack1111llll1ll_opy_ = {
            bstack11l1l11_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᵒ"): bstack11l1l11_opy_ (u"ࠥ࡫࡮ࡺࠢᵓ"),
            **info,
            bstack11l1l11_opy_ (u"ࠦࡷ࡫࡭ࡰࡶࡨࡷࠧᵔ"): bstack1111l1ll11l_opy_
        }
        bstack1111llll1ll_opy_ = bstack1111l1l1lll_opy_(bstack1111llll1ll_opy_)
        return bstack1111llll1ll_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack11l1l11_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡵࡰࡶ࡮ࡤࡸ࡮ࡴࡧࠡࡉ࡬ࡸࠥࡳࡥࡵࡣࡧࡥࡹࡧࠠࡸ࡫ࡷ࡬ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠣᵕ").format(err))
        return {}
def bstack111l111111l_opy_(bstack1111l11l111_opy_=None):
    bstack11l1l11_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡇࡦࡶࠣ࡫࡮ࡺࠠ࡮ࡧࡷࡥࡩࡧࡴࡢࠢࡶࡴࡪࡩࡩࡧ࡫ࡦࡥࡱࡲࡹࠡࡨࡲࡶࡲࡧࡴࡵࡧࡧࠤ࡫ࡵࡲࠡࡃࡌࠤࡸ࡫࡬ࡦࡥࡷ࡭ࡴࡴࠠࡶࡵࡨࠤࡨࡧࡳࡦࡵࠣࡪࡴࡸࠠࡦࡣࡦ࡬ࠥ࡬࡯࡭ࡦࡨࡶࠥ࡯࡮ࠡࡶ࡫ࡩࠥࡲࡩࡴࡶ࠱ࠎࠥࠦࠠࠡࡃࡵ࡫ࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࡨࡲࡰࡩ࡫ࡲࡴࠢࠫࡰ࡮ࡹࡴ࠭ࠢࡲࡴࡹ࡯࡯࡯ࡣ࡯࠭࠿ࠦࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡏࡱࡱࡩ࠿ࠦࡍࡰࡰࡲ࠱ࡷ࡫ࡰࡰࠢࡤࡴࡵࡸ࡯ࡢࡥ࡫࠰ࠥࡻࡳࡦࡵࠣࡧࡺࡸࡲࡦࡰࡷࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠ࡜ࡱࡶ࠲࡬࡫ࡴࡤࡹࡧࠬ࠮ࡣࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡆ࡯ࡳࡸࡾࠦ࡬ࡪࡵࡷࠤࡠࡣ࠺ࠡࡏࡸࡰࡹ࡯࠭ࡳࡧࡳࡳࠥࡧࡰࡱࡴࡲࡥࡨ࡮ࠠࡸ࡫ࡷ࡬ࠥࡴ࡯ࠡࡵࡲࡹࡷࡩࡥࡴࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡩࡩ࠲ࠠࡳࡧࡷࡹࡷࡴࡳࠡ࡝ࡠࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡑ࡯ࡳࡵࠢࡲࡪࠥࡶࡡࡵࡪࡶ࠾ࠥࡓࡵ࡭ࡶ࡬࠱ࡷ࡫ࡰࡰࠢࡤࡴࡵࡸ࡯ࡢࡥ࡫ࠤࡼ࡯ࡴࡩࠢࡶࡴࡪࡩࡩࡧ࡫ࡦࠤ࡫ࡵ࡬ࡥࡧࡵࡷࠥࡺ࡯ࠡࡣࡱࡥࡱࡿࡺࡦࠌࠣࠤࠥࠦࡒࡦࡶࡸࡶࡳࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢ࡯࡭ࡸࡺ࠺ࠡࡎ࡬ࡷࡹࠦ࡯ࡧࠢࡧ࡭ࡨࡺࡳ࠭ࠢࡨࡥࡨ࡮ࠠࡤࡱࡱࡸࡦ࡯࡮ࡪࡰࡪࠤ࡬࡯ࡴࠡ࡯ࡨࡸࡦࡪࡡࡵࡣࠣࡪࡴࡸࠠࡢࠢࡩࡳࡱࡪࡥࡳ࠰ࠍࠤࠥࠦࠠࠣࠤࠥᵖ")
    if bstack1111l11l111_opy_ is None:
        bstack1111l11l111_opy_ = [os.getcwd()]
    elif isinstance(bstack1111l11l111_opy_, list) and len(bstack1111l11l111_opy_) == 0:
        return []
    results = []
    for folder in bstack1111l11l111_opy_:
        try:
            if not os.path.exists(folder):
                raise Exception(bstack11l1l11_opy_ (u"ࠢࡇࡱ࡯ࡨࡪࡸࠠࡥࡱࡨࡷࠥࡴ࡯ࡵࠢࡨࡼ࡮ࡹࡴ࠻ࠢࡾࢁࠧᵗ").format(folder))
            repo = git.Repo(folder, search_parent_directories=True)
            result = {
                bstack11l1l11_opy_ (u"ࠣࡲࡵࡍࡩࠨᵘ"): bstack11l1l11_opy_ (u"ࠤࠥᵙ"),
                bstack11l1l11_opy_ (u"ࠥࡪ࡮ࡲࡥࡴࡅ࡫ࡥࡳ࡭ࡥࡥࠤᵚ"): [],
                bstack11l1l11_opy_ (u"ࠦࡦࡻࡴࡩࡱࡵࡷࠧᵛ"): [],
                bstack11l1l11_opy_ (u"ࠧࡶࡲࡅࡣࡷࡩࠧᵜ"): bstack11l1l11_opy_ (u"ࠨࠢᵝ"),
                bstack11l1l11_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺࡍࡦࡵࡶࡥ࡬࡫ࡳࠣᵞ"): [],
                bstack11l1l11_opy_ (u"ࠣࡲࡵࡘ࡮ࡺ࡬ࡦࠤᵟ"): bstack11l1l11_opy_ (u"ࠤࠥᵠ"),
                bstack11l1l11_opy_ (u"ࠥࡴࡷࡊࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠥᵡ"): bstack11l1l11_opy_ (u"ࠦࠧᵢ"),
                bstack11l1l11_opy_ (u"ࠧࡶࡲࡓࡣࡺࡈ࡮࡬ࡦࠣᵣ"): bstack11l1l11_opy_ (u"ࠨࠢᵤ")
            }
            bstack111l111lll1_opy_ = repo.active_branch.name
            bstack1111l1lll11_opy_ = repo.head.commit
            result[bstack11l1l11_opy_ (u"ࠢࡱࡴࡌࡨࠧᵥ")] = bstack1111l1lll11_opy_.hexsha
            bstack111l1ll1l1l_opy_ = _1111l11llll_opy_(repo)
            logger.debug(bstack11l1l11_opy_ (u"ࠣࡄࡤࡷࡪࠦࡢࡳࡣࡱࡧ࡭ࠦࡦࡰࡴࠣࡧࡴࡳࡰࡢࡴ࡬ࡷࡴࡴ࠺ࠡࠤᵦ") + str(bstack111l1ll1l1l_opy_) + bstack11l1l11_opy_ (u"ࠤࠥᵧ"))
            if bstack111l1ll1l1l_opy_:
                try:
                    bstack111l1l1l1ll_opy_ = repo.git.diff(bstack11l1l11_opy_ (u"ࠥ࠱࠲ࡴࡡ࡮ࡧ࠰ࡳࡳࡲࡹࠣᵨ"), bstack1lll11l11ll_opy_ (u"ࠦࢀࡨࡡࡴࡧࡢࡦࡷࡧ࡮ࡤࡪࢀ࠲࠳࠴ࡻࡤࡷࡵࡶࡪࡴࡴࡠࡤࡵࡥࡳࡩࡨࡾࠤᵩ")).split(bstack11l1l11_opy_ (u"ࠬࡢ࡮ࠨᵪ"))
                    logger.debug(bstack11l1l11_opy_ (u"ࠨࡃࡩࡣࡱ࡫ࡪࡪࠠࡧ࡫࡯ࡩࡸࠦࡢࡦࡶࡺࡩࡪࡴࠠࡼࡤࡤࡷࡪࡥࡢࡳࡣࡱࡧ࡭ࢃࠠࡢࡰࡧࠤࢀࡩࡵࡳࡴࡨࡲࡹࡥࡢࡳࡣࡱࡧ࡭ࢃ࠺ࠡࠤᵫ") + str(bstack111l1l1l1ll_opy_) + bstack11l1l11_opy_ (u"ࠢࠣᵬ"))
                    result[bstack11l1l11_opy_ (u"ࠣࡨ࡬ࡰࡪࡹࡃࡩࡣࡱ࡫ࡪࡪࠢᵭ")] = [f.strip() for f in bstack111l1l1l1ll_opy_ if f.strip()]
                    commits = list(repo.iter_commits(bstack1lll11l11ll_opy_ (u"ࠤࡾࡦࡦࡹࡥࡠࡤࡵࡥࡳࡩࡨࡾ࠰࠱ࡿࡨࡻࡲࡳࡧࡱࡸࡤࡨࡲࡢࡰࡦ࡬ࢂࠨᵮ")))
                except Exception:
                    logger.debug(bstack11l1l11_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡧࡦࡶࠣࡧ࡭ࡧ࡮ࡨࡧࡧࠤ࡫࡯࡬ࡦࡵࠣࡪࡷࡵ࡭ࠡࡤࡵࡥࡳࡩࡨࠡࡥࡲࡱࡵࡧࡲࡪࡵࡲࡲ࠳ࠦࡆࡢ࡮࡯࡭ࡳ࡭ࠠࡣࡣࡦ࡯ࠥࡺ࡯ࠡࡴࡨࡧࡪࡴࡴࠡࡥࡲࡱࡲ࡯ࡴࡴ࠰ࠥᵯ"))
                    commits = list(repo.iter_commits(max_count=10))
                    if commits:
                        result[bstack11l1l11_opy_ (u"ࠦ࡫࡯࡬ࡦࡵࡆ࡬ࡦࡴࡧࡦࡦࠥᵰ")] = _1111l11l1l1_opy_(commits[:5])
            else:
                commits = list(repo.iter_commits(max_count=10))
                if commits:
                    result[bstack11l1l11_opy_ (u"ࠧ࡬ࡩ࡭ࡧࡶࡇ࡭ࡧ࡮ࡨࡧࡧࠦᵱ")] = _1111l11l1l1_opy_(commits[:5])
            bstack1111l1l11ll_opy_ = set()
            bstack111l1lll1l1_opy_ = []
            for commit in commits:
                logger.debug(bstack11l1l11_opy_ (u"ࠨࡐࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡧࡴࡳ࡭ࡪࡶ࠽ࠤࠧᵲ") + str(commit.message) + bstack11l1l11_opy_ (u"ࠢࠣᵳ"))
                bstack1111ll11ll1_opy_ = commit.author.name if commit.author else bstack11l1l11_opy_ (u"ࠣࡗࡱ࡯ࡳࡵࡷ࡯ࠤᵴ")
                bstack1111l1l11ll_opy_.add(bstack1111ll11ll1_opy_)
                bstack111l1lll1l1_opy_.append({
                    bstack11l1l11_opy_ (u"ࠤࡰࡩࡸࡹࡡࡨࡧࠥᵵ"): commit.message.strip(),
                    bstack11l1l11_opy_ (u"ࠥࡹࡸ࡫ࡲࠣᵶ"): bstack1111ll11ll1_opy_
                })
            result[bstack11l1l11_opy_ (u"ࠦࡦࡻࡴࡩࡱࡵࡷࠧᵷ")] = list(bstack1111l1l11ll_opy_)
            result[bstack11l1l11_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡒ࡫ࡳࡴࡣࡪࡩࡸࠨᵸ")] = bstack111l1lll1l1_opy_
            result[bstack11l1l11_opy_ (u"ࠨࡰࡳࡆࡤࡸࡪࠨᵹ")] = bstack1111l1lll11_opy_.committed_datetime.strftime(bstack11l1l11_opy_ (u"࡛ࠢࠦ࠰ࠩࡲ࠳ࠥࡥࠤᵺ"))
            if (not result[bstack11l1l11_opy_ (u"ࠣࡲࡵࡘ࡮ࡺ࡬ࡦࠤᵻ")] or result[bstack11l1l11_opy_ (u"ࠤࡳࡶ࡙࡯ࡴ࡭ࡧࠥᵼ")].strip() == bstack11l1l11_opy_ (u"ࠥࠦᵽ")) and bstack1111l1lll11_opy_.message:
                bstack1111ll11l11_opy_ = bstack1111l1lll11_opy_.message.strip().splitlines()
                result[bstack11l1l11_opy_ (u"ࠦࡵࡸࡔࡪࡶ࡯ࡩࠧᵾ")] = bstack1111ll11l11_opy_[0] if bstack1111ll11l11_opy_ else bstack11l1l11_opy_ (u"ࠧࠨᵿ")
                if len(bstack1111ll11l11_opy_) > 2:
                    result[bstack11l1l11_opy_ (u"ࠨࡰࡳࡆࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳࠨᶀ")] = bstack11l1l11_opy_ (u"ࠧ࡝ࡰࠪᶁ").join(bstack1111ll11l11_opy_[2:]).strip()
            results.append(result)
        except Exception as err:
            logger.error(bstack11l1l11_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡱࡳࡹࡱࡧࡴࡪࡰࡪࠤࡌ࡯ࡴࠡ࡯ࡨࡸࡦࡪࡡࡵࡣࠣࡪࡴࡸࠠࡂࡋࠣࡷࡪࡲࡥࡤࡶ࡬ࡳࡳࠦࠨࡧࡱ࡯ࡨࡪࡸ࠺ࠡࡽࢀ࠭࠿ࠦࡻࡾࠢ࠰ࠤࢀࢃࠢᶂ").format(
                folder,
                type(err).__name__,
                str(err)
            ))
    filtered_results = [
        result
        for result in results
        if _111l1ll11ll_opy_(result)
    ]
    return filtered_results
def _111l1ll11ll_opy_(result):
    bstack11l1l11_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࡋࡩࡱࡶࡥࡳࠢࡷࡳࠥࡩࡨࡦࡥ࡮ࠤ࡮࡬ࠠࡢࠢࡪ࡭ࡹࠦ࡭ࡦࡶࡤࡨࡦࡺࡡࠡࡴࡨࡷࡺࡲࡴࠡ࡫ࡶࠤࡻࡧ࡬ࡪࡦࠣࠬࡳࡵ࡮࠮ࡧࡰࡴࡹࡿࠠࡧ࡫࡯ࡩࡸࡉࡨࡢࡰࡪࡩࡩࠦࡡ࡯ࡦࠣࡥࡺࡺࡨࡰࡴࡶ࠭࠳ࠐࠠࠡࠢࠣࠦࠧࠨᶃ")
    return (
        isinstance(result.get(bstack11l1l11_opy_ (u"ࠥࡪ࡮ࡲࡥࡴࡅ࡫ࡥࡳ࡭ࡥࡥࠤᶄ"), None), list)
        and len(result[bstack11l1l11_opy_ (u"ࠦ࡫࡯࡬ࡦࡵࡆ࡬ࡦࡴࡧࡦࡦࠥᶅ")]) > 0
        and isinstance(result.get(bstack11l1l11_opy_ (u"ࠧࡧࡵࡵࡪࡲࡶࡸࠨᶆ"), None), list)
        and len(result[bstack11l1l11_opy_ (u"ࠨࡡࡶࡶ࡫ࡳࡷࡹࠢᶇ")]) > 0
    )
def _1111l11llll_opy_(repo):
    bstack11l1l11_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࡕࡴࡼࠤࡹࡵࠠࡥࡧࡷࡩࡷࡳࡩ࡯ࡧࠣࡸ࡭࡫ࠠࡣࡣࡶࡩࠥࡨࡲࡢࡰࡦ࡬ࠥ࡬࡯ࡳࠢࡷ࡬ࡪࠦࡧࡪࡸࡨࡲࠥࡸࡥࡱࡱࠣࡻ࡮ࡺࡨࡰࡷࡷࠤ࡭ࡧࡲࡥࡥࡲࡨࡪࡪࠠ࡯ࡣࡰࡩࡸࠦࡡ࡯ࡦࠣࡻࡴࡸ࡫ࠡࡹ࡬ࡸ࡭ࠦࡡ࡭࡮࡚ࠣࡈ࡙ࠠࡱࡴࡲࡺ࡮ࡪࡥࡳࡵ࠱ࠎࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴࠢࡷ࡬ࡪࠦࡤࡦࡨࡤࡹࡱࡺࠠࡣࡴࡤࡲࡨ࡮ࠠࡪࡨࠣࡴࡴࡹࡳࡪࡤ࡯ࡩ࠱ࠦࡥ࡭ࡵࡨࠤࡓࡵ࡮ࡦ࠰ࠍࠤࠥࠦࠠࠣࠤࠥᶈ")
    try:
        try:
            origin = repo.remotes.origin
            bstack111l11ll11l_opy_ = origin.refs[bstack11l1l11_opy_ (u"ࠨࡊࡈࡅࡉ࠭ᶉ")]
            target = bstack111l11ll11l_opy_.reference.name
            if target.startswith(bstack11l1l11_opy_ (u"ࠩࡲࡶ࡮࡭ࡩ࡯࠱ࠪᶊ")):
                return target
        except Exception:
            pass
        if repo.remotes and repo.remotes.origin.refs:
            for ref in repo.remotes.origin.refs:
                if ref.name.startswith(bstack11l1l11_opy_ (u"ࠪࡳࡷ࡯ࡧࡪࡰ࠲ࠫᶋ")):
                    return ref.name
        if repo.heads:
            return repo.heads[0].name
    except Exception:
        pass
    return None
def _1111l11l1l1_opy_(commits):
    bstack11l1l11_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࡌ࡫ࡴࠡ࡮࡬ࡷࡹࠦ࡯ࡧࠢࡦ࡬ࡦࡴࡧࡦࡦࠣࡪ࡮ࡲࡥࡴࠢࡩࡶࡴࡳࠠࡢࠢ࡯࡭ࡸࡺࠠࡰࡨࠣࡧࡴࡳ࡭ࡪࡶࡶ࠲ࠏࠦࠠࠡࠢࠥࠦࠧᶌ")
    bstack111l1l1l1ll_opy_ = set()
    try:
        for commit in commits:
            if commit.parents:
                for parent in commit.parents:
                    diff = commit.diff(parent)
                    for bstack1111l1l11l1_opy_ in diff:
                        if bstack1111l1l11l1_opy_.a_path:
                            bstack111l1l1l1ll_opy_.add(bstack1111l1l11l1_opy_.a_path)
                        if bstack1111l1l11l1_opy_.b_path:
                            bstack111l1l1l1ll_opy_.add(bstack1111l1l11l1_opy_.b_path)
    except Exception:
        pass
    return list(bstack111l1l1l1ll_opy_)
def bstack1111l1l1lll_opy_(bstack1111llll1ll_opy_):
    bstack111l1ll1lll_opy_ = bstack1111llll11l_opy_(bstack1111llll1ll_opy_)
    if bstack111l1ll1lll_opy_ and bstack111l1ll1lll_opy_ > bstack111ll1ll11l_opy_:
        bstack1111lll1l1l_opy_ = bstack111l1ll1lll_opy_ - bstack111ll1ll11l_opy_
        bstack1111l1l111l_opy_ = bstack111l1l111l1_opy_(bstack1111llll1ll_opy_[bstack11l1l11_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡤࡳࡥࡴࡵࡤ࡫ࡪࠨᶍ")], bstack1111lll1l1l_opy_)
        bstack1111llll1ll_opy_[bstack11l1l11_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡥ࡭ࡦࡵࡶࡥ࡬࡫ࠢᶎ")] = bstack1111l1l111l_opy_
        logger.info(bstack11l1l11_opy_ (u"ࠢࡕࡪࡨࠤࡨࡵ࡭࡮࡫ࡷࠤ࡭ࡧࡳࠡࡤࡨࡩࡳࠦࡴࡳࡷࡱࡧࡦࡺࡥࡥ࠰ࠣࡗ࡮ࢀࡥࠡࡱࡩࠤࡨࡵ࡭࡮࡫ࡷࠤࡦ࡬ࡴࡦࡴࠣࡸࡷࡻ࡮ࡤࡣࡷ࡭ࡴࡴࠠࡪࡵࠣࡿࢂࠦࡋࡃࠤᶏ")
                    .format(bstack1111llll11l_opy_(bstack1111llll1ll_opy_) / 1024))
    return bstack1111llll1ll_opy_
def bstack1111llll11l_opy_(bstack1l1lll1ll_opy_):
    try:
        if bstack1l1lll1ll_opy_:
            bstack111l111llll_opy_ = json.dumps(bstack1l1lll1ll_opy_)
            bstack111l1l11l11_opy_ = sys.getsizeof(bstack111l111llll_opy_)
            return bstack111l1l11l11_opy_
    except Exception as e:
        logger.debug(bstack11l1l11_opy_ (u"ࠣࡕࡲࡱࡪࡺࡨࡪࡰࡪࠤࡼ࡫࡮ࡵࠢࡺࡶࡴࡴࡧࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡣ࡯ࡧࡺࡲࡡࡵ࡫ࡱ࡫ࠥࡹࡩࡻࡧࠣࡳ࡫ࠦࡊࡔࡑࡑࠤࡴࡨࡪࡦࡥࡷ࠾ࠥࢁࡽࠣᶐ").format(e))
    return -1
def bstack111l1l111l1_opy_(field, bstack1111ll1l111_opy_):
    try:
        bstack1111l1ll1l1_opy_ = len(bytes(bstack111ll1lll1l_opy_, bstack11l1l11_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨᶑ")))
        bstack1111llll1l1_opy_ = bytes(field, bstack11l1l11_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩᶒ"))
        bstack111l11ll111_opy_ = len(bstack1111llll1l1_opy_)
        bstack1111l1lll1l_opy_ = ceil(bstack111l11ll111_opy_ - bstack1111ll1l111_opy_ - bstack1111l1ll1l1_opy_)
        if bstack1111l1lll1l_opy_ > 0:
            bstack111l11lllll_opy_ = bstack1111llll1l1_opy_[:bstack1111l1lll1l_opy_].decode(bstack11l1l11_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪᶓ"), errors=bstack11l1l11_opy_ (u"ࠬ࡯ࡧ࡯ࡱࡵࡩࠬᶔ")) + bstack111ll1lll1l_opy_
            return bstack111l11lllll_opy_
    except Exception as e:
        logger.debug(bstack11l1l11_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡹࡸࡵ࡯ࡥࡤࡸ࡮ࡴࡧࠡࡨ࡬ࡩࡱࡪࠬࠡࡰࡲࡸ࡭࡯࡮ࡨࠢࡺࡥࡸࠦࡴࡳࡷࡱࡧࡦࡺࡥࡥࠢ࡫ࡩࡷ࡫࠺ࠡࡽࢀࠦᶕ").format(e))
    return field
def bstack1l111l1lll_opy_():
    env = os.environ
    if (bstack11l1l11_opy_ (u"ࠢࡋࡇࡑࡏࡎࡔࡓࡠࡗࡕࡐࠧᶖ") in env and len(env[bstack11l1l11_opy_ (u"ࠣࡌࡈࡒࡐࡏࡎࡔࡡࡘࡖࡑࠨᶗ")]) > 0) or (
            bstack11l1l11_opy_ (u"ࠤࡍࡉࡓࡑࡉࡏࡕࡢࡌࡔࡓࡅࠣᶘ") in env and len(env[bstack11l1l11_opy_ (u"ࠥࡎࡊࡔࡋࡊࡐࡖࡣࡍࡕࡍࡆࠤᶙ")]) > 0):
        return {
            bstack11l1l11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᶚ"): bstack11l1l11_opy_ (u"ࠧࡐࡥ࡯࡭࡬ࡲࡸࠨᶛ"),
            bstack11l1l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᶜ"): env.get(bstack11l1l11_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥᶝ")),
            bstack11l1l11_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᶞ"): env.get(bstack11l1l11_opy_ (u"ࠤࡍࡓࡇࡥࡎࡂࡏࡈࠦᶟ")),
            bstack11l1l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᶠ"): env.get(bstack11l1l11_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥᶡ"))
        }
    if env.get(bstack11l1l11_opy_ (u"ࠧࡉࡉࠣᶢ")) == bstack11l1l11_opy_ (u"ࠨࡴࡳࡷࡨࠦᶣ") and bstack1lll1l111_opy_(env.get(bstack11l1l11_opy_ (u"ࠢࡄࡋࡕࡇࡑࡋࡃࡊࠤᶤ"))):
        return {
            bstack11l1l11_opy_ (u"ࠣࡰࡤࡱࡪࠨᶥ"): bstack11l1l11_opy_ (u"ࠤࡆ࡭ࡷࡩ࡬ࡦࡅࡌࠦᶦ"),
            bstack11l1l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᶧ"): env.get(bstack11l1l11_opy_ (u"ࠦࡈࡏࡒࡄࡎࡈࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢᶨ")),
            bstack11l1l11_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᶩ"): env.get(bstack11l1l11_opy_ (u"ࠨࡃࡊࡔࡆࡐࡊࡥࡊࡐࡄࠥᶪ")),
            bstack11l1l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᶫ"): env.get(bstack11l1l11_opy_ (u"ࠣࡅࡌࡖࡈࡒࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࠦᶬ"))
        }
    if env.get(bstack11l1l11_opy_ (u"ࠤࡆࡍࠧᶭ")) == bstack11l1l11_opy_ (u"ࠥࡸࡷࡻࡥࠣᶮ") and bstack1lll1l111_opy_(env.get(bstack11l1l11_opy_ (u"࡙ࠦࡘࡁࡗࡋࡖࠦᶯ"))):
        return {
            bstack11l1l11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᶰ"): bstack11l1l11_opy_ (u"ࠨࡔࡳࡣࡹ࡭ࡸࠦࡃࡊࠤᶱ"),
            bstack11l1l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᶲ"): env.get(bstack11l1l11_opy_ (u"ࠣࡖࡕࡅ࡛ࡏࡓࡠࡄࡘࡍࡑࡊ࡟ࡘࡇࡅࡣ࡚ࡘࡌࠣᶳ")),
            bstack11l1l11_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᶴ"): env.get(bstack11l1l11_opy_ (u"ࠥࡘࡗࡇࡖࡊࡕࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧᶵ")),
            bstack11l1l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᶶ"): env.get(bstack11l1l11_opy_ (u"࡚ࠧࡒࡂࡘࡌࡗࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦᶷ"))
        }
    if env.get(bstack11l1l11_opy_ (u"ࠨࡃࡊࠤᶸ")) == bstack11l1l11_opy_ (u"ࠢࡵࡴࡸࡩࠧᶹ") and env.get(bstack11l1l11_opy_ (u"ࠣࡅࡌࡣࡓࡇࡍࡆࠤᶺ")) == bstack11l1l11_opy_ (u"ࠤࡦࡳࡩ࡫ࡳࡩ࡫ࡳࠦᶻ"):
        return {
            bstack11l1l11_opy_ (u"ࠥࡲࡦࡳࡥࠣᶼ"): bstack11l1l11_opy_ (u"ࠦࡈࡵࡤࡦࡵ࡫࡭ࡵࠨᶽ"),
            bstack11l1l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᶾ"): None,
            bstack11l1l11_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᶿ"): None,
            bstack11l1l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ᷀"): None
        }
    if env.get(bstack11l1l11_opy_ (u"ࠣࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡇࡘࡁࡏࡅࡋࠦ᷁")) and env.get(bstack11l1l11_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡉࡏࡎࡏࡌࡘ᷂ࠧ")):
        return {
            bstack11l1l11_opy_ (u"ࠥࡲࡦࡳࡥࠣ᷃"): bstack11l1l11_opy_ (u"ࠦࡇ࡯ࡴࡣࡷࡦ࡯ࡪࡺࠢ᷄"),
            bstack11l1l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ᷅"): env.get(bstack11l1l11_opy_ (u"ࠨࡂࡊࡖࡅ࡙ࡈࡑࡅࡕࡡࡊࡍ࡙ࡥࡈࡕࡖࡓࡣࡔࡘࡉࡈࡋࡑࠦ᷆")),
            bstack11l1l11_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ᷇"): None,
            bstack11l1l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ᷈"): env.get(bstack11l1l11_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦ᷉"))
        }
    if env.get(bstack11l1l11_opy_ (u"ࠥࡇࡎࠨ᷊")) == bstack11l1l11_opy_ (u"ࠦࡹࡸࡵࡦࠤ᷋") and bstack1lll1l111_opy_(env.get(bstack11l1l11_opy_ (u"ࠧࡊࡒࡐࡐࡈࠦ᷌"))):
        return {
            bstack11l1l11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ᷍"): bstack11l1l11_opy_ (u"ࠢࡅࡴࡲࡲࡪࠨ᷎"),
            bstack11l1l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯᷏ࠦ"): env.get(bstack11l1l11_opy_ (u"ࠤࡇࡖࡔࡔࡅࡠࡄࡘࡍࡑࡊ࡟ࡍࡋࡑࡏ᷐ࠧ")),
            bstack11l1l11_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ᷑"): None,
            bstack11l1l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ᷒"): env.get(bstack11l1l11_opy_ (u"ࠧࡊࡒࡐࡐࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥᷓ"))
        }
    if env.get(bstack11l1l11_opy_ (u"ࠨࡃࡊࠤᷔ")) == bstack11l1l11_opy_ (u"ࠢࡵࡴࡸࡩࠧᷕ") and bstack1lll1l111_opy_(env.get(bstack11l1l11_opy_ (u"ࠣࡕࡈࡑࡆࡖࡈࡐࡔࡈࠦᷖ"))):
        return {
            bstack11l1l11_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᷗ"): bstack11l1l11_opy_ (u"ࠥࡗࡪࡳࡡࡱࡪࡲࡶࡪࠨᷘ"),
            bstack11l1l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᷙ"): env.get(bstack11l1l11_opy_ (u"࡙ࠧࡅࡎࡃࡓࡌࡔࡘࡅࡠࡑࡕࡋࡆࡔࡉ࡛ࡃࡗࡍࡔࡔ࡟ࡖࡔࡏࠦᷚ")),
            bstack11l1l11_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᷛ"): env.get(bstack11l1l11_opy_ (u"ࠢࡔࡇࡐࡅࡕࡎࡏࡓࡇࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧᷜ")),
            bstack11l1l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᷝ"): env.get(bstack11l1l11_opy_ (u"ࠤࡖࡉࡒࡇࡐࡉࡑࡕࡉࡤࡐࡏࡃࡡࡌࡈࠧᷞ"))
        }
    if env.get(bstack11l1l11_opy_ (u"ࠥࡇࡎࠨᷟ")) == bstack11l1l11_opy_ (u"ࠦࡹࡸࡵࡦࠤᷠ") and bstack1lll1l111_opy_(env.get(bstack11l1l11_opy_ (u"ࠧࡍࡉࡕࡎࡄࡆࡤࡉࡉࠣᷡ"))):
        return {
            bstack11l1l11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᷢ"): bstack11l1l11_opy_ (u"ࠢࡈ࡫ࡷࡐࡦࡨࠢᷣ"),
            bstack11l1l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᷤ"): env.get(bstack11l1l11_opy_ (u"ࠤࡆࡍࡤࡐࡏࡃࡡࡘࡖࡑࠨᷥ")),
            bstack11l1l11_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᷦ"): env.get(bstack11l1l11_opy_ (u"ࠦࡈࡏ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤᷧ")),
            bstack11l1l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᷨ"): env.get(bstack11l1l11_opy_ (u"ࠨࡃࡊࡡࡍࡓࡇࡥࡉࡅࠤᷩ"))
        }
    if env.get(bstack11l1l11_opy_ (u"ࠢࡄࡋࠥᷪ")) == bstack11l1l11_opy_ (u"ࠣࡶࡵࡹࡪࠨᷫ") and bstack1lll1l111_opy_(env.get(bstack11l1l11_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࠧᷬ"))):
        return {
            bstack11l1l11_opy_ (u"ࠥࡲࡦࡳࡥࠣᷭ"): bstack11l1l11_opy_ (u"ࠦࡇࡻࡩ࡭ࡦ࡮࡭ࡹ࡫ࠢᷮ"),
            bstack11l1l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᷯ"): env.get(bstack11l1l11_opy_ (u"ࠨࡂࡖࡋࡏࡈࡐࡏࡔࡆࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧᷰ")),
            bstack11l1l11_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᷱ"): env.get(bstack11l1l11_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࡣࡑࡇࡂࡆࡎࠥᷲ")) or env.get(bstack11l1l11_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡏࡃࡐࡉࠧᷳ")),
            bstack11l1l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᷴ"): env.get(bstack11l1l11_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡎࡍ࡙ࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨ᷵"))
        }
    if bstack1lll1l111_opy_(env.get(bstack11l1l11_opy_ (u"࡚ࠧࡆࡠࡄࡘࡍࡑࡊࠢ᷶"))):
        return {
            bstack11l1l11_opy_ (u"ࠨ࡮ࡢ࡯ࡨ᷷ࠦ"): bstack11l1l11_opy_ (u"ࠢࡗ࡫ࡶࡹࡦࡲࠠࡔࡶࡸࡨ࡮ࡵࠠࡕࡧࡤࡱ࡙ࠥࡥࡳࡸ࡬ࡧࡪࡹ᷸ࠢ"),
            bstack11l1l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯᷹ࠦ"): bstack11l1l11_opy_ (u"ࠤࡾࢁࢀࢃ᷺ࠢ").format(env.get(bstack11l1l11_opy_ (u"ࠪࡗ࡞࡙ࡔࡆࡏࡢࡘࡊࡇࡍࡇࡑࡘࡒࡉࡇࡔࡊࡑࡑࡗࡊࡘࡖࡆࡔࡘࡖࡎ࠭᷻")), env.get(bstack11l1l11_opy_ (u"ࠫࡘ࡟ࡓࡕࡇࡐࡣ࡙ࡋࡁࡎࡒࡕࡓࡏࡋࡃࡕࡋࡇࠫ᷼"))),
            bstack11l1l11_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫᷽ࠢ"): env.get(bstack11l1l11_opy_ (u"ࠨࡓ࡚ࡕࡗࡉࡒࡥࡄࡆࡈࡌࡒࡎ࡚ࡉࡐࡐࡌࡈࠧ᷾")),
            bstack11l1l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ᷿"): env.get(bstack11l1l11_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡏࡄࠣḀ"))
        }
    if bstack1lll1l111_opy_(env.get(bstack11l1l11_opy_ (u"ࠤࡄࡔࡕ࡜ࡅ࡚ࡑࡕࠦḁ"))):
        return {
            bstack11l1l11_opy_ (u"ࠥࡲࡦࡳࡥࠣḂ"): bstack11l1l11_opy_ (u"ࠦࡆࡶࡰࡷࡧࡼࡳࡷࠨḃ"),
            bstack11l1l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣḄ"): bstack11l1l11_opy_ (u"ࠨࡻࡾ࠱ࡳࡶࡴࡰࡥࡤࡶ࠲ࡿࢂ࠵ࡻࡾ࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁࠧḅ").format(env.get(bstack11l1l11_opy_ (u"ࠧࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡘࡖࡑ࠭Ḇ")), env.get(bstack11l1l11_opy_ (u"ࠨࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡅࡈࡉࡏࡖࡐࡗࡣࡓࡇࡍࡆࠩḇ")), env.get(bstack11l1l11_opy_ (u"ࠩࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡕࡘࡏࡋࡇࡆࡘࡤ࡙ࡌࡖࡉࠪḈ")), env.get(bstack11l1l11_opy_ (u"ࠪࡅࡕࡖࡖࡆ࡛ࡒࡖࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧḉ"))),
            bstack11l1l11_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨḊ"): env.get(bstack11l1l11_opy_ (u"ࠧࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤḋ")),
            bstack11l1l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧḌ"): env.get(bstack11l1l11_opy_ (u"ࠢࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣḍ"))
        }
    if env.get(bstack11l1l11_opy_ (u"ࠣࡃ࡝࡙ࡗࡋ࡟ࡉࡖࡗࡔࡤ࡛ࡓࡆࡔࡢࡅࡌࡋࡎࡕࠤḎ")) and env.get(bstack11l1l11_opy_ (u"ࠤࡗࡊࡤࡈࡕࡊࡎࡇࠦḏ")):
        return {
            bstack11l1l11_opy_ (u"ࠥࡲࡦࡳࡥࠣḐ"): bstack11l1l11_opy_ (u"ࠦࡆࢀࡵࡳࡧࠣࡇࡎࠨḑ"),
            bstack11l1l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣḒ"): bstack11l1l11_opy_ (u"ࠨࡻࡾࡽࢀ࠳ࡤࡨࡵࡪ࡮ࡧ࠳ࡷ࡫ࡳࡶ࡮ࡷࡷࡄࡨࡵࡪ࡮ࡧࡍࡩࡃࡻࡾࠤḓ").format(env.get(bstack11l1l11_opy_ (u"ࠧࡔ࡛ࡖࡘࡊࡓ࡟ࡕࡇࡄࡑࡋࡕࡕࡏࡆࡄࡘࡎࡕࡎࡔࡇࡕ࡚ࡊࡘࡕࡓࡋࠪḔ")), env.get(bstack11l1l11_opy_ (u"ࠨࡕ࡜ࡗ࡙ࡋࡍࡠࡖࡈࡅࡒࡖࡒࡐࡌࡈࡇ࡙࠭ḕ")), env.get(bstack11l1l11_opy_ (u"ࠩࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊࡉࡅࠩḖ"))),
            bstack11l1l11_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧḗ"): env.get(bstack11l1l11_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡋࡇࠦḘ")),
            bstack11l1l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦḙ"): env.get(bstack11l1l11_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡍࡉࠨḚ"))
        }
    if any([env.get(bstack11l1l11_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧḛ")), env.get(bstack11l1l11_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡗࡋࡓࡐࡎ࡙ࡉࡉࡥࡓࡐࡗࡕࡇࡊࡥࡖࡆࡔࡖࡍࡔࡔࠢḜ")), env.get(bstack11l1l11_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤ࡙ࡏࡖࡔࡆࡉࡤ࡜ࡅࡓࡕࡌࡓࡓࠨḝ"))]):
        return {
            bstack11l1l11_opy_ (u"ࠥࡲࡦࡳࡥࠣḞ"): bstack11l1l11_opy_ (u"ࠦࡆ࡝ࡓࠡࡅࡲࡨࡪࡈࡵࡪ࡮ࡧࠦḟ"),
            bstack11l1l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣḠ"): env.get(bstack11l1l11_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡓ࡙ࡇࡒࡉࡄࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧḡ")),
            bstack11l1l11_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤḢ"): env.get(bstack11l1l11_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࠨḣ")),
            bstack11l1l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣḤ"): env.get(bstack11l1l11_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠣḥ"))
        }
    if env.get(bstack11l1l11_opy_ (u"ࠦࡧࡧ࡭ࡣࡱࡲࡣࡧࡻࡩ࡭ࡦࡑࡹࡲࡨࡥࡳࠤḦ")):
        return {
            bstack11l1l11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥḧ"): bstack11l1l11_opy_ (u"ࠨࡂࡢ࡯ࡥࡳࡴࠨḨ"),
            bstack11l1l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥḩ"): env.get(bstack11l1l11_opy_ (u"ࠣࡤࡤࡱࡧࡵ࡯ࡠࡤࡸ࡭ࡱࡪࡒࡦࡵࡸࡰࡹࡹࡕࡳ࡮ࠥḪ")),
            bstack11l1l11_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦḫ"): env.get(bstack11l1l11_opy_ (u"ࠥࡦࡦࡳࡢࡰࡱࡢࡷ࡭ࡵࡲࡵࡌࡲࡦࡓࡧ࡭ࡦࠤḬ")),
            bstack11l1l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥḭ"): env.get(bstack11l1l11_opy_ (u"ࠧࡨࡡ࡮ࡤࡲࡳࡤࡨࡵࡪ࡮ࡧࡒࡺࡳࡢࡦࡴࠥḮ"))
        }
    if env.get(bstack11l1l11_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘࠢḯ")) or env.get(bstack11l1l11_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࡠࡏࡄࡍࡓࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡕࡗࡅࡗ࡚ࡅࡅࠤḰ")):
        return {
            bstack11l1l11_opy_ (u"ࠣࡰࡤࡱࡪࠨḱ"): bstack11l1l11_opy_ (u"ࠤ࡚ࡩࡷࡩ࡫ࡦࡴࠥḲ"),
            bstack11l1l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨḳ"): env.get(bstack11l1l11_opy_ (u"ࠦ࡜ࡋࡒࡄࡍࡈࡖࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣḴ")),
            bstack11l1l11_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢḵ"): bstack11l1l11_opy_ (u"ࠨࡍࡢ࡫ࡱࠤࡕ࡯ࡰࡦ࡮࡬ࡲࡪࠨḶ") if env.get(bstack11l1l11_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࡠࡏࡄࡍࡓࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡕࡗࡅࡗ࡚ࡅࡅࠤḷ")) else None,
            bstack11l1l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢḸ"): env.get(bstack11l1l11_opy_ (u"ࠤ࡚ࡉࡗࡉࡋࡆࡔࡢࡋࡎ࡚࡟ࡄࡑࡐࡑࡎ࡚ࠢḹ"))
        }
    if any([env.get(bstack11l1l11_opy_ (u"ࠥࡋࡈࡖ࡟ࡑࡔࡒࡎࡊࡉࡔࠣḺ")), env.get(bstack11l1l11_opy_ (u"ࠦࡌࡉࡌࡐࡗࡇࡣࡕࡘࡏࡋࡇࡆࡘࠧḻ")), env.get(bstack11l1l11_opy_ (u"ࠧࡍࡏࡐࡉࡏࡉࡤࡉࡌࡐࡗࡇࡣࡕࡘࡏࡋࡇࡆࡘࠧḼ"))]):
        return {
            bstack11l1l11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦḽ"): bstack11l1l11_opy_ (u"ࠢࡈࡱࡲ࡫ࡱ࡫ࠠࡄ࡮ࡲࡹࡩࠨḾ"),
            bstack11l1l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦḿ"): None,
            bstack11l1l11_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦṀ"): env.get(bstack11l1l11_opy_ (u"ࠥࡔࡗࡕࡊࡆࡅࡗࡣࡎࡊࠢṁ")),
            bstack11l1l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥṂ"): env.get(bstack11l1l11_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡎࡊࠢṃ"))
        }
    if env.get(bstack11l1l11_opy_ (u"ࠨࡓࡉࡋࡓࡔࡆࡈࡌࡆࠤṄ")):
        return {
            bstack11l1l11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧṅ"): bstack11l1l11_opy_ (u"ࠣࡕ࡫࡭ࡵࡶࡡࡣ࡮ࡨࠦṆ"),
            bstack11l1l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧṇ"): env.get(bstack11l1l11_opy_ (u"ࠥࡗࡍࡏࡐࡑࡃࡅࡐࡊࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤṈ")),
            bstack11l1l11_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨṉ"): bstack11l1l11_opy_ (u"ࠧࡐ࡯ࡣࠢࠦࡿࢂࠨṊ").format(env.get(bstack11l1l11_opy_ (u"࠭ࡓࡉࡋࡓࡔࡆࡈࡌࡆࡡࡍࡓࡇࡥࡉࡅࠩṋ"))) if env.get(bstack11l1l11_opy_ (u"ࠢࡔࡊࡌࡔࡕࡇࡂࡍࡇࡢࡎࡔࡈ࡟ࡊࡆࠥṌ")) else None,
            bstack11l1l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢṍ"): env.get(bstack11l1l11_opy_ (u"ࠤࡖࡌࡎࡖࡐࡂࡄࡏࡉࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦṎ"))
        }
    if bstack1lll1l111_opy_(env.get(bstack11l1l11_opy_ (u"ࠥࡒࡊ࡚ࡌࡊࡈ࡜ࠦṏ"))):
        return {
            bstack11l1l11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤṐ"): bstack11l1l11_opy_ (u"ࠧࡔࡥࡵ࡮࡬ࡪࡾࠨṑ"),
            bstack11l1l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤṒ"): env.get(bstack11l1l11_opy_ (u"ࠢࡅࡇࡓࡐࡔ࡟࡟ࡖࡔࡏࠦṓ")),
            bstack11l1l11_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥṔ"): env.get(bstack11l1l11_opy_ (u"ࠤࡖࡍ࡙ࡋ࡟ࡏࡃࡐࡉࠧṕ")),
            bstack11l1l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤṖ"): env.get(bstack11l1l11_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡍࡉࠨṗ"))
        }
    if bstack1lll1l111_opy_(env.get(bstack11l1l11_opy_ (u"ࠧࡍࡉࡕࡊࡘࡆࡤࡇࡃࡕࡋࡒࡒࡘࠨṘ"))):
        return {
            bstack11l1l11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦṙ"): bstack11l1l11_opy_ (u"ࠢࡈ࡫ࡷࡌࡺࡨࠠࡂࡥࡷ࡭ࡴࡴࡳࠣṚ"),
            bstack11l1l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦṛ"): bstack11l1l11_opy_ (u"ࠤࡾࢁ࠴ࢁࡽ࠰ࡣࡦࡸ࡮ࡵ࡮ࡴ࠱ࡵࡹࡳࡹ࠯ࡼࡿࠥṜ").format(env.get(bstack11l1l11_opy_ (u"ࠪࡋࡎ࡚ࡈࡖࡄࡢࡗࡊࡘࡖࡆࡔࡢ࡙ࡗࡒࠧṝ")), env.get(bstack11l1l11_opy_ (u"ࠫࡌࡏࡔࡉࡗࡅࡣࡗࡋࡐࡐࡕࡌࡘࡔࡘ࡙ࠨṞ")), env.get(bstack11l1l11_opy_ (u"ࠬࡍࡉࡕࡊࡘࡆࡤࡘࡕࡏࡡࡌࡈࠬṟ"))),
            bstack11l1l11_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣṠ"): env.get(bstack11l1l11_opy_ (u"ࠢࡈࡋࡗࡌ࡚ࡈ࡟ࡘࡑࡕࡏࡋࡒࡏࡘࠤṡ")),
            bstack11l1l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢṢ"): env.get(bstack11l1l11_opy_ (u"ࠤࡊࡍ࡙ࡎࡕࡃࡡࡕ࡙ࡓࡥࡉࡅࠤṣ"))
        }
    if env.get(bstack11l1l11_opy_ (u"ࠥࡇࡎࠨṤ")) == bstack11l1l11_opy_ (u"ࠦࡹࡸࡵࡦࠤṥ") and env.get(bstack11l1l11_opy_ (u"ࠧ࡜ࡅࡓࡅࡈࡐࠧṦ")) == bstack11l1l11_opy_ (u"ࠨ࠱ࠣṧ"):
        return {
            bstack11l1l11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧṨ"): bstack11l1l11_opy_ (u"ࠣࡘࡨࡶࡨ࡫࡬ࠣṩ"),
            bstack11l1l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧṪ"): bstack11l1l11_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࡿࢂࠨṫ").format(env.get(bstack11l1l11_opy_ (u"࡛ࠫࡋࡒࡄࡇࡏࡣ࡚ࡘࡌࠨṬ"))),
            bstack11l1l11_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢṭ"): None,
            bstack11l1l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧṮ"): None,
        }
    if env.get(bstack11l1l11_opy_ (u"ࠢࡕࡇࡄࡑࡈࡏࡔ࡚ࡡ࡙ࡉࡗ࡙ࡉࡐࡐࠥṯ")):
        return {
            bstack11l1l11_opy_ (u"ࠣࡰࡤࡱࡪࠨṰ"): bstack11l1l11_opy_ (u"ࠤࡗࡩࡦࡳࡣࡪࡶࡼࠦṱ"),
            bstack11l1l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨṲ"): None,
            bstack11l1l11_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨṳ"): env.get(bstack11l1l11_opy_ (u"࡚ࠧࡅࡂࡏࡆࡍ࡙࡟࡟ࡑࡔࡒࡎࡊࡉࡔࡠࡐࡄࡑࡊࠨṴ")),
            bstack11l1l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧṵ"): env.get(bstack11l1l11_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨṶ"))
        }
    if any([env.get(bstack11l1l11_opy_ (u"ࠣࡅࡒࡒࡈࡕࡕࡓࡕࡈࠦṷ")), env.get(bstack11l1l11_opy_ (u"ࠤࡆࡓࡓࡉࡏࡖࡔࡖࡉࡤ࡛ࡒࡍࠤṸ")), env.get(bstack11l1l11_opy_ (u"ࠥࡇࡔࡔࡃࡐࡗࡕࡗࡊࡥࡕࡔࡇࡕࡒࡆࡓࡅࠣṹ")), env.get(bstack11l1l11_opy_ (u"ࠦࡈࡕࡎࡄࡑࡘࡖࡘࡋ࡟ࡕࡇࡄࡑࠧṺ"))]):
        return {
            bstack11l1l11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥṻ"): bstack11l1l11_opy_ (u"ࠨࡃࡰࡰࡦࡳࡺࡸࡳࡦࠤṼ"),
            bstack11l1l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥṽ"): None,
            bstack11l1l11_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥṾ"): env.get(bstack11l1l11_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥṿ")) or None,
            bstack11l1l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤẀ"): env.get(bstack11l1l11_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡍࡉࠨẁ"), 0)
        }
    if env.get(bstack11l1l11_opy_ (u"ࠧࡍࡏࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥẂ")):
        return {
            bstack11l1l11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦẃ"): bstack11l1l11_opy_ (u"ࠢࡈࡱࡆࡈࠧẄ"),
            bstack11l1l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦẅ"): None,
            bstack11l1l11_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦẆ"): env.get(bstack11l1l11_opy_ (u"ࠥࡋࡔࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣẇ")),
            bstack11l1l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥẈ"): env.get(bstack11l1l11_opy_ (u"ࠧࡍࡏࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡇࡔ࡛ࡎࡕࡇࡕࠦẉ"))
        }
    if env.get(bstack11l1l11_opy_ (u"ࠨࡃࡇࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦẊ")):
        return {
            bstack11l1l11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧẋ"): bstack11l1l11_opy_ (u"ࠣࡅࡲࡨࡪࡌࡲࡦࡵ࡫ࠦẌ"),
            bstack11l1l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧẍ"): env.get(bstack11l1l11_opy_ (u"ࠥࡇࡋࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤẎ")),
            bstack11l1l11_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨẏ"): env.get(bstack11l1l11_opy_ (u"ࠧࡉࡆࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡒࡆࡓࡅࠣẐ")),
            bstack11l1l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧẑ"): env.get(bstack11l1l11_opy_ (u"ࠢࡄࡈࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧẒ"))
        }
    return {bstack11l1l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢẓ"): None}
def get_host_info():
    return {
        bstack11l1l11_opy_ (u"ࠤ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨࠦẔ"): platform.node(),
        bstack11l1l11_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࠧẕ"): platform.system(),
        bstack11l1l11_opy_ (u"ࠦࡹࡿࡰࡦࠤẖ"): platform.machine(),
        bstack11l1l11_opy_ (u"ࠧࡼࡥࡳࡵ࡬ࡳࡳࠨẗ"): platform.version(),
        bstack11l1l11_opy_ (u"ࠨࡡࡳࡥ࡫ࠦẘ"): platform.architecture()[0]
    }
def bstack1ll111l1l_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack111l1llll1l_opy_():
    if global_config.get_property(bstack11l1l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨẙ")):
        return bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧẚ")
    return bstack11l1l11_opy_ (u"ࠩࡸࡲࡰࡴ࡯ࡸࡰࡢ࡫ࡷ࡯ࡤࠨẛ")
def bstack1111lll1l11_opy_(driver):
    info = {
        bstack11l1l11_opy_ (u"ࠪࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩẜ"): driver.capabilities,
        bstack11l1l11_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠨẝ"): driver.session_id,
        bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭ẞ"): driver.capabilities.get(bstack11l1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫẟ"), None),
        bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩẠ"): driver.capabilities.get(bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩạ"), None),
        bstack11l1l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࠫẢ"): driver.capabilities.get(bstack11l1l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠩả"), None),
        bstack11l1l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡥࡶࡦࡴࡶ࡭ࡴࡴࠧẤ"):driver.capabilities.get(bstack11l1l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧấ"), None),
    }
    if bstack111l1llll1l_opy_() == bstack11l1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬẦ"):
        if bstack11l1lll1l_opy_():
            info[bstack11l1l11_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࠨầ")] = bstack11l1l11_opy_ (u"ࠨࡣࡳࡴ࠲ࡧࡵࡵࡱࡰࡥࡹ࡫ࠧẨ")
        elif driver.capabilities.get(bstack11l1l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪẩ"), {}).get(bstack11l1l11_opy_ (u"ࠪࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫ࠧẪ"), False):
            info[bstack11l1l11_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࠬẫ")] = bstack11l1l11_opy_ (u"ࠬࡺࡵࡳࡤࡲࡷࡨࡧ࡬ࡦࠩẬ")
        else:
            info[bstack11l1l11_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺࠧậ")] = bstack11l1l11_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩẮ")
    return info
def bstack11l1lll1l_opy_():
    if global_config.get_property(bstack11l1l11_opy_ (u"ࠨࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠧắ")):
        return True
    if bstack1lll1l111_opy_(os.environ.get(bstack11l1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪẰ"), None)):
        return True
    return False
def bstack1111ll1ll1l_opy_(bstack1111ll1lll1_opy_, url, response, headers=None, data=None):
    bstack11l1l11_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࡆࡺ࡯࡬ࡥࠢࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦ࡬ࡰࡩࠣࡴࡦࡸࡡ࡮ࡧࡷࡩࡷࡹࠠࡧࡱࡵࠤࡷ࡫ࡱࡶࡧࡶࡸ࠴ࡸࡥࡴࡲࡲࡲࡸ࡫ࠠ࡭ࡱࡪ࡫࡮ࡴࡧࠋࠢࠣࠤࠥࡇࡲࡨࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡸࡥࡲࡷࡨࡷࡹࡥࡴࡺࡲࡨ࠾ࠥࡎࡔࡕࡒࠣࡱࡪࡺࡨࡰࡦࠣࠬࡌࡋࡔ࠭ࠢࡓࡓࡘ࡚ࠬࠡࡧࡷࡧ࠳࠯ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡷࡵࡰ࠿ࠦࡒࡦࡳࡸࡩࡸࡺࠠࡖࡔࡏ࠳ࡪࡴࡤࡱࡱ࡬ࡲࡹࠐࠠࠡࠢࠣࠤࠥࠦࠠࡳࡧࡶࡴࡴࡴࡳࡦ࠼ࠣࡖࡪࡹࡰࡰࡰࡶࡩࠥࡵࡢ࡫ࡧࡦࡸࠥ࡬ࡲࡰ࡯ࠣࡶࡪࡷࡵࡦࡵࡷࡷࠏࠦࠠࠡࠢࠣࠤࠥࠦࡨࡦࡣࡧࡩࡷࡹ࠺ࠡࡔࡨࡵࡺ࡫ࡳࡵࠢ࡫ࡩࡦࡪࡥࡳࡵࠣࡳࡷࠦࡎࡰࡰࡨࠎࠥࠦࠠࠡࠢࠣࠤࠥࡪࡡࡵࡣ࠽ࠤࡗ࡫ࡱࡶࡧࡶࡸࠥࡐࡓࡐࡐࠣࡨࡦࡺࡡࠡࡱࡵࠤࡓࡵ࡮ࡦࠌࠣࠤࠥࠦࡒࡦࡶࡸࡶࡳࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡧ࡭ࡨࡺ࠺ࠡࡈࡲࡶࡲࡧࡴࡵࡧࡧࠤࡱࡵࡧࠡ࡯ࡨࡷࡸࡧࡧࡦࠢࡺ࡭ࡹ࡮ࠠࡳࡧࡴࡹࡪࡹࡴࠡࡣࡱࡨࠥࡸࡥࡴࡲࡲࡲࡸ࡫ࠠࡥࡣࡷࡥࠏࠦࠠࠡࠢࠥࠦࠧằ")
    bstack111l1l1ll1l_opy_ = {
        bstack11l1l11_opy_ (u"ࠦ࡭࡫ࡡࡥࡧࡵࡷࠧẲ"): headers,
        bstack11l1l11_opy_ (u"ࠧࡳࡥࡵࡪࡲࡨࠧẳ"): bstack1111ll1lll1_opy_.upper(),
        bstack11l1l11_opy_ (u"ࠨࡡࡨࡧࡱࡸࠧẴ"): None,
        bstack11l1l11_opy_ (u"ࠢࡦࡰࡧࡴࡴ࡯࡮ࡵࠤẵ"): url,
        bstack11l1l11_opy_ (u"ࠣ࡬ࡶࡳࡳࠨẶ"): data
    }
    try:
        bstack111l1l1l1l1_opy_ = response.json()
    except Exception:
        bstack111l1l1l1l1_opy_ = response.text
    bstack1111l1ll111_opy_ = {
        bstack11l1l11_opy_ (u"ࠤࡥࡳࡩࡿࠢặ"): bstack111l1l1l1l1_opy_,
        bstack11l1l11_opy_ (u"ࠥࡷࡹࡧࡴࡶࡵࡆࡳࡩ࡫ࠢẸ"): response.status_code
    }
    return {
        bstack11l1l11_opy_ (u"ࠦࡷ࡫ࡱࡶࡧࡶࡸࠧẹ"): bstack111l1l1ll1l_opy_,
        bstack11l1l11_opy_ (u"ࠧࡸࡥࡴࡲࡲࡲࡸ࡫ࠢẺ"): bstack1111l1ll111_opy_
    }
def bstack11l11llll_opy_(bstack1111ll1lll1_opy_, url, data, config):
    headers = config.get(bstack11l1l11_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧẻ"), None)
    proxies = bstack1lll1l11l1_opy_(config, url)
    auth = config.get(bstack11l1l11_opy_ (u"ࠧࡢࡷࡷ࡬ࠬẼ"), None)
    response = requests.request(
            bstack1111ll1lll1_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    try:
        log_message = bstack1111ll1ll1l_opy_(bstack1111ll1lll1_opy_, url, response, headers, data)
        bstack11ll111ll_opy_.debug(json.dumps(log_message, separators=(bstack11l1l11_opy_ (u"ࠨ࠮ࠪẽ"), bstack11l1l11_opy_ (u"ࠩ࠽ࠫẾ"))))
    except Exception as e:
        logger.debug(bstack11l1l11_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡ࡮ࡲ࡫࡬࡯࡮ࡨࠢࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡲࡦࡳࡸࡩࡸࡺ࠺ࠡࡽࢀࠦế").format(e))
    return response
def bstack111lll11ll_opy_(bstack1l11ll11l1_opy_, size):
    bstack1l11l11l11_opy_ = []
    while len(bstack1l11ll11l1_opy_) > size:
        bstack1l1llll111_opy_ = bstack1l11ll11l1_opy_[:size]
        bstack1l11l11l11_opy_.append(bstack1l1llll111_opy_)
        bstack1l11ll11l1_opy_ = bstack1l11ll11l1_opy_[size:]
    bstack1l11l11l11_opy_.append(bstack1l11ll11l1_opy_)
    return bstack1l11l11l11_opy_
def bstack111l1l11ll1_opy_(message, bstack1111ll11111_opy_=False):
    os.write(1, bytes(message, bstack11l1l11_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪỀ")))
    os.write(1, bytes(bstack11l1l11_opy_ (u"ࠬࡢ࡮ࠨề"), bstack11l1l11_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬỂ")))
    if bstack1111ll11111_opy_:
        with open(bstack11l1l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠭ࡰ࠳࠴ࡽ࠲࠭ể") + os.environ[bstack11l1l11_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡍࡇࡓࡉࡇࡇࡣࡎࡊࠧỄ")] + bstack11l1l11_opy_ (u"ࠩ࠱ࡰࡴ࡭ࠧễ"), bstack11l1l11_opy_ (u"ࠪࡥࠬỆ")) as f:
            f.write(message + bstack11l1l11_opy_ (u"ࠫࡡࡴࠧệ"))
def bstack1l111lll111_opy_():
    return os.environ[bstack11l1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨỈ")].lower() == bstack11l1l11_opy_ (u"࠭ࡴࡳࡷࡨࠫỉ")
def current_time():
    return bstack1llllll1lll_opy_().replace(tzinfo=None).isoformat() + bstack11l1l11_opy_ (u"࡛ࠧࠩỊ")
def time_diff(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack11l1l11_opy_ (u"ࠨ࡜ࠪị"))) - datetime.datetime.fromisoformat(start.rstrip(bstack11l1l11_opy_ (u"ࠩ࡝ࠫỌ")))).total_seconds() * 1000
def bstack111l11l1111_opy_(timestamp):
    return bstack111l1l111ll_opy_(timestamp).isoformat() + bstack11l1l11_opy_ (u"ࠪ࡞ࠬọ")
def bstack111l11l11l1_opy_(bstack111l1l1l11l_opy_):
    date_format = bstack11l1l11_opy_ (u"ࠫࠪ࡟ࠥ࡮ࠧࡧࠤࠪࡎ࠺ࠦࡏ࠽ࠩࡘ࠴ࠥࡧࠩỎ")
    bstack111l11111l1_opy_ = datetime.datetime.strptime(bstack111l1l1l11l_opy_, date_format)
    return bstack111l11111l1_opy_.isoformat() + bstack11l1l11_opy_ (u"ࠬࡠࠧỏ")
def bstack111l11lll1l_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack11l1l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭Ố")
    else:
        return bstack11l1l11_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧố")
def bstack1lll1l111_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack11l1l11_opy_ (u"ࠨࡶࡵࡹࡪ࠭Ồ")
def bstack1111l1l1l11_opy_(val):
    return val.__str__().lower() == bstack11l1l11_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨồ")
def error_handler(bstack111l11ll1ll_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack111l11ll1ll_opy_ as e:
                print(bstack11l1l11_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡩࡹࡳࡩࡴࡪࡱࡱࠤࢀࢃࠠ࠮ࡀࠣࡿࢂࡀࠠࡼࡿࠥỔ").format(func.__name__, bstack111l11ll1ll_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack111l1l1lll1_opy_(bstack1111ll1ll11_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack1111ll1ll11_opy_(cls, *args, **kwargs)
            except bstack111l11ll1ll_opy_ as e:
                print(bstack11l1l11_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡪࡺࡴࡣࡵ࡫ࡲࡲࠥࢁࡽࠡ࠯ࡁࠤࢀࢃ࠺ࠡࡽࢀࠦổ").format(bstack1111ll1ll11_opy_.__name__, bstack111l11ll1ll_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack111l1l1lll1_opy_
    else:
        return decorator
def bstack1lll1l1l_opy_(bstack1llll1lll11_opy_):
    if os.getenv(bstack11l1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨỖ")) is not None:
        return bstack1lll1l111_opy_(os.getenv(bstack11l1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩỗ")))
    if bstack11l1l11_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫỘ") in bstack1llll1lll11_opy_ and bstack1111l1l1l11_opy_(bstack1llll1lll11_opy_[bstack11l1l11_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬộ")]):
        return False
    if bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫỚ") in bstack1llll1lll11_opy_ and bstack1111l1l1l11_opy_(bstack1llll1lll11_opy_[bstack11l1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬớ")]):
        return False
    return True
def bstack1llll1ll1_opy_():
    try:
        from pytest_bdd import reporting
        bstack1111lll11l1_opy_ = os.environ.get(bstack11l1l11_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢ࡙ࡘࡋࡒࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠦỜ"), None)
        return bstack1111lll11l1_opy_ is None or bstack1111lll11l1_opy_ == bstack11l1l11_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠤờ")
    except Exception as e:
        return False
def bstack1l11111111_opy_(hub_url, CONFIG):
    if bstack1l1ll1111l_opy_() <= version.parse(bstack11l1l11_opy_ (u"࠭࠳࠯࠳࠶࠲࠵࠭Ở")):
        if hub_url:
            return bstack11l1l11_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣở") + hub_url + bstack11l1l11_opy_ (u"ࠣ࠼࠻࠴࠴ࡽࡤ࠰ࡪࡸࡦࠧỠ")
        return bstack11ll1l1l11_opy_
    if hub_url:
        return bstack11l1l11_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦỡ") + hub_url + bstack11l1l11_opy_ (u"ࠥ࠳ࡼࡪ࠯ࡩࡷࡥࠦỢ")
    return HTTPS_HUB
def bstack1111l1l1111_opy_():
    return isinstance(os.getenv(bstack11l1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔ࡞࡚ࡅࡔࡖࡢࡔࡑ࡛ࡇࡊࡐࠪợ")), str)
def bstack11l1l111ll_opy_(url):
    return urlparse(url).hostname
def bstack1111l1l1_opy_(hostname):
    for bstack111llll1ll_opy_ in bstack1ll11lll1l_opy_:
        regex = re.compile(bstack111llll1ll_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack111l111ll11_opy_(bstack1111ll111l1_opy_, file_name, logger):
    bstack111l1ll1l1_opy_ = os.path.join(os.path.expanduser(bstack11l1l11_opy_ (u"ࠬࢄࠧỤ")), bstack1111ll111l1_opy_)
    try:
        if not os.path.exists(bstack111l1ll1l1_opy_):
            os.makedirs(bstack111l1ll1l1_opy_)
        file_path = os.path.join(os.path.expanduser(bstack11l1l11_opy_ (u"࠭ࡾࠨụ")), bstack1111ll111l1_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack11l1l11_opy_ (u"ࠧࡸࠩỦ")):
                pass
            with open(file_path, bstack11l1l11_opy_ (u"ࠣࡹ࠮ࠦủ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack1111l1lll_opy_.format(str(e)))
def bstack1111lllllll_opy_(file_name, key, value, logger):
    file_path = bstack111l111ll11_opy_(bstack11l1l11_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩỨ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack11lll1l1l1_opy_ = json.load(open(file_path, bstack11l1l11_opy_ (u"ࠪࡶࡧ࠭ứ")))
        else:
            bstack11lll1l1l1_opy_ = {}
        bstack11lll1l1l1_opy_[key] = value
        with open(file_path, bstack11l1l11_opy_ (u"ࠦࡼ࠱ࠢỪ")) as outfile:
            json.dump(bstack11lll1l1l1_opy_, outfile)
def bstack11l11l1ll1_opy_(file_name, logger):
    file_path = bstack111l111ll11_opy_(bstack11l1l11_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬừ"), file_name, logger)
    bstack11lll1l1l1_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack11l1l11_opy_ (u"࠭ࡲࠨỬ")) as bstack1l1l111ll_opy_:
            bstack11lll1l1l1_opy_ = json.load(bstack1l1l111ll_opy_)
    return bstack11lll1l1l1_opy_
def bstack111ll1lll_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack11l1l11_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡧࡩࡱ࡫ࡴࡪࡰࡪࠤ࡫࡯࡬ࡦ࠼ࠣࠫử") + file_path + bstack11l1l11_opy_ (u"ࠨࠢࠪỮ") + str(e))
def bstack1l1ll1111l_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack11l1l11_opy_ (u"ࠤ࠿ࡒࡔ࡚ࡓࡆࡖࡁࠦữ")
def bstack11ll1l1l1l_opy_(config):
    if bstack11l1l11_opy_ (u"ࠪ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩỰ") in config:
        del (config[bstack11l1l11_opy_ (u"ࠫ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪự")])
        return False
    if bstack1l1ll1111l_opy_() < version.parse(bstack11l1l11_opy_ (u"ࠬ࠹࠮࠵࠰࠳ࠫỲ")):
        return False
    if bstack1l1ll1111l_opy_() >= version.parse(bstack11l1l11_opy_ (u"࠭࠴࠯࠳࠱࠹ࠬỳ")):
        return True
    if bstack11l1l11_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧỴ") in config and config[bstack11l1l11_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨỵ")] is False:
        return False
    else:
        return True
def bstack1l1l1llll1_opy_(args_list, bstack1111l1l1l1l_opy_):
    index = -1
    for value in bstack1111l1l1l1l_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
def bstack11l1l1111ll_opy_(a, b):
  for k, v in b.items():
    if isinstance(v, dict) and k in a and isinstance(a[k], dict):
        bstack11l1l1111ll_opy_(a[k], v)
    else:
        a[k] = v
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack1111l11ll1_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack1111l11ll1_opy_ = bstack1111l11ll1_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack11l1l11_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩỶ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack11l1l11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪỷ"), exception=exception)
    def bstack1lll1ll1l11_opy_(self):
        if self.result != bstack11l1l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫỸ"):
            return None
        if isinstance(self.exception_type, str) and bstack11l1l11_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࠣỹ") in self.exception_type:
            return bstack11l1l11_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢỺ")
        return bstack11l1l11_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣỻ")
    def bstack111l1l11lll_opy_(self):
        if self.result != bstack11l1l11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨỼ"):
            return None
        if self.bstack1111l11ll1_opy_:
            return self.bstack1111l11ll1_opy_
        return bstack111l11l1l1l_opy_(self.exception)
def bstack111l11l1l1l_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack111l11l1ll1_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack11llll11l1_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack11lll1l111_opy_(config, logger):
    try:
        import playwright
        bstack111l1lll1ll_opy_ = playwright.__file__
        bstack1111ll111ll_opy_ = os.path.split(bstack111l1lll1ll_opy_)
        bstack111l1ll1l11_opy_ = bstack1111ll111ll_opy_[0] + bstack11l1l11_opy_ (u"ࠩ࠲ࡨࡷ࡯ࡶࡦࡴ࠲ࡴࡦࡩ࡫ࡢࡩࡨ࠳ࡱ࡯ࡢ࠰ࡥ࡯࡭࠴ࡩ࡬ࡪ࠰࡭ࡷࠬỽ")
        os.environ[bstack11l1l11_opy_ (u"ࠪࡋࡑࡕࡂࡂࡎࡢࡅࡌࡋࡎࡕࡡࡋࡘ࡙ࡖ࡟ࡑࡔࡒ࡜࡞࠭Ỿ")] = bstack11lll1ll11_opy_(config)
        with open(bstack111l1ll1l11_opy_, bstack11l1l11_opy_ (u"ࠫࡷ࠭ỿ")) as f:
            bstack111l1lllll_opy_ = f.read()
            bstack111l111ll1l_opy_ = bstack11l1l11_opy_ (u"ࠬ࡭࡬ࡰࡤࡤࡰ࠲ࡧࡧࡦࡰࡷࠫἀ")
            bstack111l1l1llll_opy_ = bstack111l1lllll_opy_.find(bstack111l111ll1l_opy_)
            if bstack111l1l1llll_opy_ == -1:
              process = subprocess.Popen(bstack11l1l11_opy_ (u"ࠨ࡮ࡱ࡯ࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤ࡬ࡲ࡯ࡣࡣ࡯࠱ࡦ࡭ࡥ࡯ࡶࠥἁ"), shell=True, cwd=bstack1111ll111ll_opy_[0])
              process.wait()
              bstack1111l1llll1_opy_ = bstack11l1l11_opy_ (u"ࠧࠣࡷࡶࡩࠥࡹࡴࡳ࡫ࡦࡸࠧࡁࠧἂ")
              bstack111l111l111_opy_ = bstack11l1l11_opy_ (u"ࠣࠤࠥࠤࡡࠨࡵࡴࡧࠣࡷࡹࡸࡩࡤࡶ࡟ࠦࡀࠦࡣࡰࡰࡶࡸࠥࢁࠠࡣࡱࡲࡸࡸࡺࡲࡢࡲࠣࢁࠥࡃࠠࡳࡧࡴࡹ࡮ࡸࡥࠩࠩࡪࡰࡴࡨࡡ࡭࠯ࡤ࡫ࡪࡴࡴࠨࠫ࠾ࠤ࡮࡬ࠠࠩࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡨࡲࡻ࠴ࡇࡍࡑࡅࡅࡑࡥࡁࡈࡇࡑࡘࡤࡎࡔࡕࡒࡢࡔࡗࡕࡘ࡚ࠫࠣࡦࡴࡵࡴࡴࡶࡵࡥࡵ࠮ࠩ࠼ࠢࠥࠦࠧἃ")
              bstack111l11lll11_opy_ = bstack111l1lllll_opy_.replace(bstack1111l1llll1_opy_, bstack111l111l111_opy_)
              with open(bstack111l1ll1l11_opy_, bstack11l1l11_opy_ (u"ࠩࡺࠫἄ")) as f:
                f.write(bstack111l11lll11_opy_)
    except Exception as e:
        logger.error(bstack1l1ll1l1l1_opy_.format(str(e)))
def bstack1l1l1l1l1_opy_():
  try:
    bstack111l1lll111_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1l11_opy_ (u"ࠪࡳࡵࡺࡩ࡮ࡣ࡯ࡣ࡭ࡻࡢࡠࡷࡵࡰ࠳ࡰࡳࡰࡰࠪἅ"))
    bstack1111l1lllll_opy_ = []
    if os.path.exists(bstack111l1lll111_opy_):
      with open(bstack111l1lll111_opy_) as f:
        bstack1111l1lllll_opy_ = json.load(f)
      os.remove(bstack111l1lll111_opy_)
    return bstack1111l1lllll_opy_
  except:
    pass
  return []
def bstack11l1ll1l1_opy_(bstack11lll11l1_opy_):
  try:
    bstack1111l1lllll_opy_ = []
    bstack111l1lll111_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1l11_opy_ (u"ࠫࡴࡶࡴࡪ࡯ࡤࡰࡤ࡮ࡵࡣࡡࡸࡶࡱ࠴ࡪࡴࡱࡱࠫἆ"))
    if os.path.exists(bstack111l1lll111_opy_):
      with open(bstack111l1lll111_opy_) as f:
        bstack1111l1lllll_opy_ = json.load(f)
    bstack1111l1lllll_opy_.append(bstack11lll11l1_opy_)
    with open(bstack111l1lll111_opy_, bstack11l1l11_opy_ (u"ࠬࡽࠧἇ")) as f:
        json.dump(bstack1111l1lllll_opy_, f)
  except:
    pass
def bstack1llll1l11_opy_(logger, bstack1111l1ll1ll_opy_ = False):
  try:
    test_name = os.environ.get(bstack11l1l11_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙ࡥࡔࡆࡕࡗࡣࡓࡇࡍࡆࠩἈ"), bstack11l1l11_opy_ (u"ࠧࠨἉ"))
    if test_name == bstack11l1l11_opy_ (u"ࠨࠩἊ"):
        test_name = threading.current_thread().__dict__.get(bstack11l1l11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡄࡧࡨࡤࡺࡥࡴࡶࡢࡲࡦࡳࡥࠨἋ"), bstack11l1l11_opy_ (u"ࠪࠫἌ"))
    bstack1111ll11l1l_opy_ = bstack11l1l11_opy_ (u"ࠫ࠱ࠦࠧἍ").join(threading.current_thread().bstackTestErrorMessages)
    if bstack1111l1ll1ll_opy_:
        bstack1ll11ll1l1_opy_ = os.environ.get(bstack11l1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬἎ"), bstack11l1l11_opy_ (u"࠭࠰ࠨἏ"))
        bstack1l1l1l1l1l_opy_ = {bstack11l1l11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬἐ"): test_name, bstack11l1l11_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧἑ"): bstack1111ll11l1l_opy_, bstack11l1l11_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨἒ"): bstack1ll11ll1l1_opy_}
        bstack111l1111lll_opy_ = []
        bstack111l1l1l111_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1l11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡴࡵࡶ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷ࠲࡯ࡹ࡯࡯ࠩἓ"))
        if os.path.exists(bstack111l1l1l111_opy_):
            with open(bstack111l1l1l111_opy_) as f:
                bstack111l1111lll_opy_ = json.load(f)
        bstack111l1111lll_opy_.append(bstack1l1l1l1l1l_opy_)
        with open(bstack111l1l1l111_opy_, bstack11l1l11_opy_ (u"ࠫࡼ࠭ἔ")) as f:
            json.dump(bstack111l1111lll_opy_, f)
    else:
        bstack1l1l1l1l1l_opy_ = {bstack11l1l11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪἕ"): test_name, bstack11l1l11_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ἖"): bstack1111ll11l1l_opy_, bstack11l1l11_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭἗"): str(multiprocessing.current_process().name)}
        if bstack11l1l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸࠬἘ") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack1l1l1l1l1l_opy_)
  except Exception as e:
      logger.warn(bstack11l1l11_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡴࡰࡴࡨࠤࡵࡿࡴࡦࡵࡷࠤ࡫ࡻ࡮࡯ࡧ࡯ࠤࡩࡧࡴࡢ࠼ࠣࡿࢂࠨἙ").format(e))
def bstack111l1l1l11_opy_(error_message, test_name, index, logger):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack11l1l11_opy_ (u"ࠪࡪ࡮ࡲࡥ࡭ࡱࡦ࡯ࠥࡴ࡯ࡵࠢࡤࡺࡦ࡯࡬ࡢࡤ࡯ࡩ࠱ࠦࡵࡴ࡫ࡱ࡫ࠥࡨࡡࡴ࡫ࡦࠤ࡫࡯࡬ࡦࠢࡲࡴࡪࡸࡡࡵ࡫ࡲࡲࡸ࠭Ἒ"))
    try:
      bstack1111lll111l_opy_ = []
      bstack1l1l1l1l1l_opy_ = {bstack11l1l11_opy_ (u"ࠫࡳࡧ࡭ࡦࠩἛ"): test_name, bstack11l1l11_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫἜ"): error_message, bstack11l1l11_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬἝ"): index}
      bstack1111l11lll1_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1l11_opy_ (u"ࠧࡳࡱࡥࡳࡹࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶ࠱࡮ࡸࡵ࡮ࠨ἞"))
      if os.path.exists(bstack1111l11lll1_opy_):
          with open(bstack1111l11lll1_opy_) as f:
              bstack1111lll111l_opy_ = json.load(f)
      bstack1111lll111l_opy_.append(bstack1l1l1l1l1l_opy_)
      with open(bstack1111l11lll1_opy_, bstack11l1l11_opy_ (u"ࠨࡹࠪ἟")) as f:
          json.dump(bstack1111lll111l_opy_, f)
    except Exception as e:
      logger.warn(bstack11l1l11_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡴࡰࡴࡨࠤࡷࡵࡢࡰࡶࠣࡪࡺࡴ࡮ࡦ࡮ࠣࡨࡦࡺࡡ࠻ࠢࡾࢁࠧἠ").format(e))
    return
  bstack1111lll111l_opy_ = []
  bstack1l1l1l1l1l_opy_ = {bstack11l1l11_opy_ (u"ࠪࡲࡦࡳࡥࠨἡ"): test_name, bstack11l1l11_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪἢ"): error_message, bstack11l1l11_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫἣ"): index}
  bstack1111l11lll1_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1l11_opy_ (u"࠭ࡲࡰࡤࡲࡸࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧἤ"))
  lock_file = bstack1111l11lll1_opy_ + bstack11l1l11_opy_ (u"ࠧ࠯࡮ࡲࡧࡰ࠭ἥ")
  try:
    with FileLock(lock_file, timeout=10):
      if os.path.exists(bstack1111l11lll1_opy_):
          with open(bstack1111l11lll1_opy_, bstack11l1l11_opy_ (u"ࠨࡴࠪἦ")) as f:
              content = f.read().strip()
              if content:
                  bstack1111lll111l_opy_ = json.load(open(bstack1111l11lll1_opy_))
      bstack1111lll111l_opy_.append(bstack1l1l1l1l1l_opy_)
      with open(bstack1111l11lll1_opy_, bstack11l1l11_opy_ (u"ࠩࡺࠫἧ")) as f:
          json.dump(bstack1111lll111l_opy_, f)
  except Exception as e:
    logger.warn(bstack11l1l11_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡱࡵࡩࠥࡸ࡯ࡣࡱࡷࠤ࡫ࡻ࡮࡯ࡧ࡯ࠤࡩࡧࡴࡢࠢࡺ࡭ࡹ࡮ࠠࡧ࡫࡯ࡩࠥࡲ࡯ࡤ࡭࡬ࡲ࡬ࡀࠠࡼࡿࠥἨ").format(e))
def bstack111l11111_opy_(bstack1l11l1l11_opy_, name, logger):
  try:
    bstack1l1l1l1l1l_opy_ = {bstack11l1l11_opy_ (u"ࠫࡳࡧ࡭ࡦࠩἩ"): name, bstack11l1l11_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫἪ"): bstack1l11l1l11_opy_, bstack11l1l11_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬἫ"): str(threading.current_thread()._name)}
    return bstack1l1l1l1l1l_opy_
  except Exception as e:
    logger.warn(bstack11l1l11_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡹࡵࡲࡦࠢࡥࡩ࡭ࡧࡶࡦࠢࡩࡹࡳࡴࡥ࡭ࠢࡧࡥࡹࡧ࠺ࠡࡽࢀࠦἬ").format(e))
  return
def bstack111l11l1l11_opy_():
    return platform.system() == bstack11l1l11_opy_ (u"ࠨ࡙࡬ࡲࡩࡵࡷࡴࠩἭ")
def bstack1l1ll1111_opy_(bstack1111lll1ll1_opy_, config, logger):
    bstack1111lll11ll_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack1111lll1ll1_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack11l1l11_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥ࡬ࡩ࡭ࡶࡨࡶࠥࡩ࡯࡯ࡨ࡬࡫ࠥࡱࡥࡺࡵࠣࡦࡾࠦࡲࡦࡩࡨࡼࠥࡳࡡࡵࡥ࡫࠾ࠥࢁࡽࠣἮ").format(e))
    return bstack1111lll11ll_opy_
def bstack111l1111ll1_opy_(bstack111l11111ll_opy_, bstack111l11ll1l1_opy_):
    bstack111l1ll11l1_opy_ = version.parse(bstack111l11111ll_opy_)
    bstack111l1111l1l_opy_ = version.parse(bstack111l11ll1l1_opy_)
    if bstack111l1ll11l1_opy_ > bstack111l1111l1l_opy_:
        return 1
    elif bstack111l1ll11l1_opy_ < bstack111l1111l1l_opy_:
        return -1
    else:
        return 0
def bstack1llllll1lll_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack111l1l111ll_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
def bstack1111lll1lll_opy_(framework):
    from browserstack_sdk._version import __version__
    return str(framework) + str(__version__)
def bstack111l1llll_opy_(options, framework, config, bstack1llll111l_opy_={}):
    if options is None:
        return
    if getattr(options, bstack11l1l11_opy_ (u"ࠪ࡫ࡪࡺࠧἯ"), None):
        caps = options
    else:
        caps = options.to_capabilities()
    bstack1l1l11l1_opy_ = caps.get(bstack11l1l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬἰ"))
    bstack111l11llll1_opy_ = True
    bstack111ll11lll_opy_ = os.environ[bstack11l1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪἱ")]
    bstack1l1ll1l1ll1_opy_ = config.get(bstack11l1l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ἲ"), False)
    if bstack1l1ll1l1ll1_opy_:
        bstack1l1llllll11_opy_ = config.get(bstack11l1l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧἳ"), {})
        bstack1l1llllll11_opy_[bstack11l1l11_opy_ (u"ࠨࡣࡸࡸ࡭࡚࡯࡬ࡧࡱࠫἴ")] = os.getenv(bstack11l1l11_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧἵ"))
        bstack11l1l111l11_opy_ = json.loads(os.getenv(bstack11l1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫἶ"), bstack11l1l11_opy_ (u"ࠫࢀࢃࠧἷ"))).get(bstack11l1l11_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭Ἰ"))
    if bstack1111l1l1l11_opy_(caps.get(bstack11l1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡻࡳࡦ࡙࠶ࡇࠬἹ"))) or bstack1111l1l1l11_opy_(caps.get(bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡵࡴࡧࡢࡻ࠸ࡩࠧἺ"))):
        bstack111l11llll1_opy_ = False
    if bstack11ll1l1l1l_opy_({bstack11l1l11_opy_ (u"ࠣࡷࡶࡩ࡜࠹ࡃࠣἻ"): bstack111l11llll1_opy_}):
        bstack1l1l11l1_opy_ = bstack1l1l11l1_opy_ or {}
        bstack1l1l11l1_opy_[bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫἼ")] = bstack1111lll1lll_opy_(framework)
        bstack1l1l11l1_opy_[bstack11l1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬἽ")] = bstack1l111lll111_opy_()
        bstack1l1l11l1_opy_[bstack11l1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡪࡸࡦࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧἾ")] = bstack111ll11lll_opy_
        bstack1l1l11l1_opy_[bstack11l1l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡔࡷࡵࡤࡶࡥࡷࡑࡦࡶࠧἿ")] = bstack1llll111l_opy_
        if bstack1l1ll1l1ll1_opy_:
            bstack1l1l11l1_opy_[bstack11l1l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ὀ")] = bstack1l1ll1l1ll1_opy_
            bstack1l1l11l1_opy_[bstack11l1l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧὁ")] = bstack1l1llllll11_opy_
            bstack1l1l11l1_opy_[bstack11l1l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨὂ")][bstack11l1l11_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪὃ")] = bstack11l1l111l11_opy_
        if getattr(options, bstack11l1l11_opy_ (u"ࠪࡷࡪࡺ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶࡼࠫὄ"), None):
            options.set_capability(bstack11l1l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬὅ"), bstack1l1l11l1_opy_)
        else:
            options[bstack11l1l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭὆")] = bstack1l1l11l1_opy_
    else:
        if getattr(options, bstack11l1l11_opy_ (u"࠭ࡳࡦࡶࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹࡿࠧ὇"), None):
            options.set_capability(bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨὈ"), bstack1111lll1lll_opy_(framework))
            options.set_capability(bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩὉ"), bstack1l111lll111_opy_())
            options.set_capability(bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡶࡨࡷࡹ࡮ࡵࡣࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫὊ"), bstack111ll11lll_opy_)
            options.set_capability(bstack11l1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫὋ"), bstack1llll111l_opy_)
            if bstack1l1ll1l1ll1_opy_:
                options.set_capability(bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪὌ"), bstack1l1ll1l1ll1_opy_)
                options.set_capability(bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫὍ"), bstack1l1llllll11_opy_)
                options.set_capability(bstack11l1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷ࠳ࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭὎"), bstack11l1l111l11_opy_)
        else:
            options[bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨ὏")] = bstack1111lll1lll_opy_(framework)
            options[bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩὐ")] = bstack1l111lll111_opy_()
            options[bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡶࡨࡷࡹ࡮ࡵࡣࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫὑ")] = bstack111ll11lll_opy_
            options[bstack11l1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫὒ")] = bstack1llll111l_opy_
            if bstack1l1ll1l1ll1_opy_:
                options[bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪὓ")] = bstack1l1ll1l1ll1_opy_
                options[bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫὔ")] = bstack1l1llllll11_opy_
                options[bstack11l1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬὕ")][bstack11l1l11_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨὖ")] = bstack11l1l111l11_opy_
    return options
def bstack111l1111111_opy_(bstack111l1l1111l_opy_, framework):
    bstack1llll111l_opy_ = global_config.get_property(bstack11l1l11_opy_ (u"ࠣࡒࡏࡅ࡞࡝ࡒࡊࡉࡋࡘࡤࡖࡒࡐࡆࡘࡇ࡙ࡥࡍࡂࡒࠥὗ"))
    if bstack111l1l1111l_opy_ and len(bstack111l1l1111l_opy_.split(bstack11l1l11_opy_ (u"ࠩࡦࡥࡵࡹ࠽ࠨ὘"))) > 1:
        ws_url = bstack111l1l1111l_opy_.split(bstack11l1l11_opy_ (u"ࠪࡧࡦࡶࡳ࠾ࠩὙ"))[0]
        if bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧ὚") in ws_url:
            from browserstack_sdk._version import __version__
            bstack111l11l11ll_opy_ = json.loads(urllib.parse.unquote(bstack111l1l1111l_opy_.split(bstack11l1l11_opy_ (u"ࠬࡩࡡࡱࡵࡀࠫὛ"))[1]))
            bstack111l11l11ll_opy_ = bstack111l11l11ll_opy_ or {}
            bstack111ll11lll_opy_ = os.environ[bstack11l1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ὜")]
            bstack111l11l11ll_opy_[bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨὝ")] = str(framework) + str(__version__)
            bstack111l11l11ll_opy_[bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩ὞")] = bstack1l111lll111_opy_()
            bstack111l11l11ll_opy_[bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡶࡨࡷࡹ࡮ࡵࡣࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫὟ")] = bstack111ll11lll_opy_
            bstack111l11l11ll_opy_[bstack11l1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫὠ")] = bstack1llll111l_opy_
            bstack111l1l1111l_opy_ = bstack111l1l1111l_opy_.split(bstack11l1l11_opy_ (u"ࠫࡨࡧࡰࡴ࠿ࠪὡ"))[0] + bstack11l1l11_opy_ (u"ࠬࡩࡡࡱࡵࡀࠫὢ") + urllib.parse.quote(json.dumps(bstack111l11l11ll_opy_))
    return bstack111l1l1111l_opy_
def bstack11llllll1_opy_():
    global bstack1l1l1l1lll_opy_
    from playwright._impl._browser_type import BrowserType
    bstack1l1l1l1lll_opy_ = BrowserType.connect
    return bstack1l1l1l1lll_opy_
def bstack111ll1lll1_opy_(framework_name):
    global bstack11ll1ll111_opy_
    bstack11ll1ll111_opy_ = framework_name
    return framework_name
def bstack1ll1l111l_opy_(self, *args, **kwargs):
    global bstack1l1l1l1lll_opy_
    try:
        global bstack11ll1ll111_opy_
        if bstack11l1l11_opy_ (u"࠭ࡷࡴࡇࡱࡨࡵࡵࡩ࡯ࡶࠪὣ") in kwargs:
            kwargs[bstack11l1l11_opy_ (u"ࠧࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷࠫὤ")] = bstack111l1111111_opy_(
                kwargs.get(bstack11l1l11_opy_ (u"ࠨࡹࡶࡉࡳࡪࡰࡰ࡫ࡱࡸࠬὥ"), None),
                bstack11ll1ll111_opy_
            )
    except Exception as e:
        logger.error(bstack11l1l11_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫ࡩࡳࠦࡰࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡗࡉࡑࠠࡤࡣࡳࡷ࠿ࠦࡻࡾࠤὦ").format(str(e)))
    return bstack1l1l1l1lll_opy_(self, *args, **kwargs)
def bstack111l1lllll1_opy_(bstack1111lllll11_opy_, proxies):
    proxy_settings = {}
    try:
        if not proxies:
            proxies = bstack1lll1l11l1_opy_(bstack1111lllll11_opy_, bstack11l1l11_opy_ (u"ࠥࠦὧ"))
        if proxies and proxies.get(bstack11l1l11_opy_ (u"ࠦ࡭ࡺࡴࡱࡵࠥὨ")):
            parsed_url = urlparse(proxies.get(bstack11l1l11_opy_ (u"ࠧ࡮ࡴࡵࡲࡶࠦὩ")))
            if parsed_url and parsed_url.hostname: proxy_settings[bstack11l1l11_opy_ (u"࠭ࡰࡳࡱࡻࡽࡍࡵࡳࡵࠩὪ")] = str(parsed_url.hostname)
            if parsed_url and parsed_url.port: proxy_settings[bstack11l1l11_opy_ (u"ࠧࡱࡴࡲࡼࡾࡖ࡯ࡳࡶࠪὫ")] = str(parsed_url.port)
            if parsed_url and parsed_url.username: proxy_settings[bstack11l1l11_opy_ (u"ࠨࡲࡵࡳࡽࡿࡕࡴࡧࡵࠫὬ")] = str(parsed_url.username)
            if parsed_url and parsed_url.password: proxy_settings[bstack11l1l11_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡣࡶࡷࠬὭ")] = str(parsed_url.password)
        return proxy_settings
    except:
        return proxy_settings
def bstack1l1ll1l111_opy_(bstack1111lllll11_opy_):
    bstack1111ll1l1ll_opy_ = {
        bstack111lll11l1l_opy_[bstack1111ll1llll_opy_]: bstack1111lllll11_opy_[bstack1111ll1llll_opy_]
        for bstack1111ll1llll_opy_ in bstack1111lllll11_opy_
        if bstack1111ll1llll_opy_ in bstack111lll11l1l_opy_
    }
    bstack1111ll1l1ll_opy_[bstack11l1l11_opy_ (u"ࠥࡴࡷࡵࡸࡺࡕࡨࡸࡹ࡯࡮ࡨࡵࠥὮ")] = bstack111l1lllll1_opy_(bstack1111lllll11_opy_, global_config.get_property(bstack11l1l11_opy_ (u"ࠦࡵࡸ࡯ࡹࡻࡖࡩࡹࡺࡩ࡯ࡩࡶࠦὯ")))
    bstack1111lllll1l_opy_ = [element.lower() for element in bstack111llll1l1l_opy_]
    bstack111l111l1ll_opy_(bstack1111ll1l1ll_opy_, bstack1111lllll1l_opy_)
    return bstack1111ll1l1ll_opy_
def bstack111l111l1ll_opy_(d, keys):
    for key in list(d.keys()):
        if key.lower() in keys:
            d[key] = bstack11l1l11_opy_ (u"ࠧ࠰ࠪࠫࠬࠥὰ")
    for value in d.values():
        if isinstance(value, dict):
            bstack111l111l1ll_opy_(value, keys)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    bstack111l111l1ll_opy_(item, keys)
def bstack1l11ll1111l_opy_():
    bstack111l1ll1111_opy_ = [os.environ.get(bstack11l1l11_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡉࡍࡇࡖࡣࡉࡏࡒࠣά")), os.path.join(os.path.expanduser(bstack11l1l11_opy_ (u"ࠢࡿࠤὲ")), bstack11l1l11_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨέ")), os.path.join(bstack11l1l11_opy_ (u"ࠩ࠲ࡸࡲࡶࠧὴ"), bstack11l1l11_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪή"))]
    for path in bstack111l1ll1111_opy_:
        if path is None:
            continue
        try:
            if os.path.exists(path):
                logger.debug(bstack11l1l11_opy_ (u"ࠦࡋ࡯࡬ࡦࠢࠪࠦὶ") + str(path) + bstack11l1l11_opy_ (u"ࠧ࠭ࠠࡦࡺ࡬ࡷࡹࡹ࠮ࠣί"))
                if not os.access(path, os.W_OK):
                    logger.debug(bstack11l1l11_opy_ (u"ࠨࡇࡪࡸ࡬ࡲ࡬ࠦࡰࡦࡴࡰ࡭ࡸࡹࡩࡰࡰࡶࠤ࡫ࡵࡲࠡࠩࠥὸ") + str(path) + bstack11l1l11_opy_ (u"ࠢࠨࠤό"))
                    os.chmod(path, 0o777)
                else:
                    logger.debug(bstack11l1l11_opy_ (u"ࠣࡈ࡬ࡰࡪࠦࠧࠣὺ") + str(path) + bstack11l1l11_opy_ (u"ࠤࠪࠤࡦࡲࡲࡦࡣࡧࡽࠥ࡮ࡡࡴࠢࡷ࡬ࡪࠦࡲࡦࡳࡸ࡭ࡷ࡫ࡤࠡࡲࡨࡶࡲ࡯ࡳࡴ࡫ࡲࡲࡸ࠴ࠢύ"))
            else:
                logger.debug(bstack11l1l11_opy_ (u"ࠥࡇࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥ࡬ࡩ࡭ࡧࠣࠫࠧὼ") + str(path) + bstack11l1l11_opy_ (u"ࠦࠬࠦࡷࡪࡶ࡫ࠤࡼࡸࡩࡵࡧࠣࡴࡪࡸ࡭ࡪࡵࡶ࡭ࡴࡴ࠮ࠣώ"))
                os.makedirs(path, exist_ok=True)
                os.chmod(path, 0o777)
            logger.debug(bstack11l1l11_opy_ (u"ࠧࡕࡰࡦࡴࡤࡸ࡮ࡵ࡮ࠡࡵࡸࡧࡨ࡫ࡥࡥࡧࡧࠤ࡫ࡵࡲࠡࠩࠥ὾") + str(path) + bstack11l1l11_opy_ (u"ࠨࠧ࠯ࠤ὿"))
            return path
        except Exception as e:
            logger.debug(bstack11l1l11_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࠠࡶࡲࠣࡪ࡮ࡲࡥࠡࠩࡾࡴࡦࡺࡨࡾࠩ࠽ࠤࠧᾀ") + str(e) + bstack11l1l11_opy_ (u"ࠣࠤᾁ"))
    logger.debug(bstack11l1l11_opy_ (u"ࠤࡄࡰࡱࠦࡰࡢࡶ࡫ࡷࠥ࡬ࡡࡪ࡮ࡨࡨ࠳ࠨᾂ"))
    return None
@measure(event_name=EVENTS.bstack111lll1lll1_opy_, stage=STAGE.bstack1l11l1l11l_opy_)
def bstack1lllll1ll11_opy_(binary_path, bstack1llllll1111_opy_, bs_config):
    logger.debug(bstack11l1l11_opy_ (u"ࠥࡇࡺࡸࡲࡦࡰࡷࠤࡈࡒࡉࠡࡒࡤࡸ࡭ࠦࡦࡰࡷࡱࡨ࠿ࠦࡻࡾࠤᾃ").format(binary_path))
    bstack1111ll11lll_opy_ = bstack11l1l11_opy_ (u"ࠫࠬᾄ")
    bstack111l11l111l_opy_ = {
        bstack11l1l11_opy_ (u"ࠬࡹࡤ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪᾅ"): __version__,
        bstack11l1l11_opy_ (u"ࠨ࡯ࡴࠤᾆ"): platform.system(),
        bstack11l1l11_opy_ (u"ࠢࡰࡵࡢࡥࡷࡩࡨࠣᾇ"): platform.machine(),
        bstack11l1l11_opy_ (u"ࠣࡥ࡯࡭ࡤࡼࡥࡳࡵ࡬ࡳࡳࠨᾈ"): bstack11l1l11_opy_ (u"ࠩ࠳ࠫᾉ"),
        bstack11l1l11_opy_ (u"ࠥࡷࡩࡱ࡟࡭ࡣࡱ࡫ࡺࡧࡧࡦࠤᾊ"): bstack11l1l11_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫᾋ")
    }
    bstack1111l11l1ll_opy_(bstack111l11l111l_opy_)
    try:
        if binary_path:
            if bstack111l11l1l11_opy_():
                bstack111l11l111l_opy_[bstack11l1l11_opy_ (u"ࠬࡩ࡬ࡪࡡࡹࡩࡷࡹࡩࡰࡰࠪᾌ")] = subprocess.check_output([binary_path, bstack11l1l11_opy_ (u"ࠨࡶࡦࡴࡶ࡭ࡴࡴࠢᾍ")]).strip().decode(bstack11l1l11_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭ᾎ"))
            else:
                bstack111l11l111l_opy_[bstack11l1l11_opy_ (u"ࠨࡥ࡯࡭ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᾏ")] = subprocess.check_output([binary_path, bstack11l1l11_opy_ (u"ࠤࡹࡩࡷࡹࡩࡰࡰࠥᾐ")], stderr=subprocess.DEVNULL).strip().decode(bstack11l1l11_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩᾑ"))
        response = requests.request(
            bstack11l1l11_opy_ (u"ࠫࡌࡋࡔࠨᾒ"),
            url=bstack11l11lll_opy_(bstack111llll11l1_opy_),
            headers=None,
            auth=(bs_config[bstack11l1l11_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧᾓ")], bs_config[bstack11l1l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩᾔ")]),
            json=None,
            params=bstack111l11l111l_opy_
        )
        data = response.json()
        if response.status_code == 200 and bstack11l1l11_opy_ (u"ࠧࡶࡴ࡯ࠫᾕ") in data.keys() and bstack11l1l11_opy_ (u"ࠨࡷࡳࡨࡦࡺࡥࡥࡡࡦࡰ࡮ࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᾖ") in data.keys():
            logger.debug(bstack11l1l11_opy_ (u"ࠤࡑࡩࡪࡪࠠࡵࡱࠣࡹࡵࡪࡡࡵࡧࠣࡦ࡮ࡴࡡࡳࡻ࠯ࠤࡨࡻࡲࡳࡧࡱࡸࠥࡨࡩ࡯ࡣࡵࡽࠥࡼࡥࡳࡵ࡬ࡳࡳࡀࠠࡼࡿࠥᾗ").format(bstack111l11l111l_opy_[bstack11l1l11_opy_ (u"ࠪࡧࡱ࡯࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᾘ")]))
            if bstack11l1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆࡎࡔࡁࡓ࡛ࡢ࡙ࡗࡒࠧᾙ") in os.environ:
                logger.debug(bstack11l1l11_opy_ (u"࡙ࠧ࡫ࡪࡲࡳ࡭ࡳ࡭ࠠࡣ࡫ࡱࡥࡷࡿࠠࡥࡱࡺࡲࡱࡵࡡࡥࠢࡤࡷࠥࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇࡏࡎࡂࡔ࡜ࡣ࡚ࡘࡌࠡ࡫ࡶࠤࡸ࡫ࡴࠣᾚ"))
                data[bstack11l1l11_opy_ (u"࠭ࡵࡳ࡮ࠪᾛ")] = os.environ[bstack11l1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡊࡐࡄࡖ࡞ࡥࡕࡓࡎࠪᾜ")]
            bstack1111l11l11l_opy_ = bstack1111ll1111l_opy_(data[bstack11l1l11_opy_ (u"ࠨࡷࡵࡰࠬᾝ")], bstack1llllll1111_opy_)
            bstack1111ll11lll_opy_ = os.path.join(bstack1llllll1111_opy_, bstack1111l11l11l_opy_)
            os.chmod(bstack1111ll11lll_opy_, 0o777) # bstack1111l1l1ll1_opy_ permission
            return bstack1111ll11lll_opy_
    except Exception as e:
        logger.debug(bstack11l1l11_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡥࡱࡺࡲࡱࡵࡡࡥ࡫ࡱ࡫ࠥࡴࡥࡸࠢࡖࡈࡐࠦࡻࡾࠤᾞ").format(e))
    return binary_path
def bstack1111l11l1ll_opy_(bstack111l11l111l_opy_):
    try:
        if bstack11l1l11_opy_ (u"ࠪࡰ࡮ࡴࡵࡹࠩᾟ") not in bstack111l11l111l_opy_[bstack11l1l11_opy_ (u"ࠫࡴࡹࠧᾠ")].lower():
            return
        if os.path.exists(bstack11l1l11_opy_ (u"ࠧ࠵ࡥࡵࡥ࠲ࡳࡸ࠳ࡲࡦ࡮ࡨࡥࡸ࡫ࠢᾡ")):
            with open(bstack11l1l11_opy_ (u"ࠨ࠯ࡦࡶࡦ࠳ࡴࡹ࠭ࡳࡧ࡯ࡩࡦࡹࡥࠣᾢ"), bstack11l1l11_opy_ (u"ࠢࡳࠤᾣ")) as f:
                bstack1111lll1111_opy_ = {}
                for line in f:
                    if bstack11l1l11_opy_ (u"ࠣ࠿ࠥᾤ") in line:
                        key, value = line.rstrip().split(bstack11l1l11_opy_ (u"ࠤࡀࠦᾥ"), 1)
                        bstack1111lll1111_opy_[key] = value.strip(bstack11l1l11_opy_ (u"ࠪࠦࡡ࠭ࠧᾦ"))
                bstack111l11l111l_opy_[bstack11l1l11_opy_ (u"ࠫࡩ࡯ࡳࡵࡴࡲࠫᾧ")] = bstack1111lll1111_opy_.get(bstack11l1l11_opy_ (u"ࠧࡏࡄࠣᾨ"), bstack11l1l11_opy_ (u"ࠨࠢᾩ"))
        elif os.path.exists(bstack11l1l11_opy_ (u"ࠢ࠰ࡧࡷࡧ࠴ࡧ࡬ࡱ࡫ࡱࡩ࠲ࡸࡥ࡭ࡧࡤࡷࡪࠨᾪ")):
            bstack111l11l111l_opy_[bstack11l1l11_opy_ (u"ࠨࡦ࡬ࡷࡹࡸ࡯ࠨᾫ")] = bstack11l1l11_opy_ (u"ࠩࡤࡰࡵ࡯࡮ࡦࠩᾬ")
    except Exception as e:
        logger.debug(bstack11l1l11_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡧࡦࡶࠣࡨ࡮ࡹࡴࡳࡱࠣࡳ࡫ࠦ࡬ࡪࡰࡸࡼࠧᾭ") + e)
@measure(event_name=EVENTS.bstack111lll11111_opy_, stage=STAGE.bstack1l11l1l11l_opy_)
def bstack1111ll1111l_opy_(bstack1111l11ll1l_opy_, bstack111l1111l11_opy_):
    logger.debug(bstack11l1l11_opy_ (u"ࠦࡉࡵࡷ࡯࡮ࡲࡥࡩ࡯࡮ࡨࠢࡖࡈࡐࠦࡢࡪࡰࡤࡶࡾࠦࡦࡳࡱࡰ࠾ࠥࠨᾮ") + str(bstack1111l11ll1l_opy_) + bstack11l1l11_opy_ (u"ࠧࠨᾯ"))
    zip_path = os.path.join(bstack111l1111l11_opy_, bstack11l1l11_opy_ (u"ࠨࡤࡰࡹࡱࡰࡴࡧࡤࡦࡦࡢࡪ࡮ࡲࡥ࠯ࡼ࡬ࡴࠧᾰ"))
    bstack1111l11l11l_opy_ = bstack11l1l11_opy_ (u"ࠧࠨᾱ")
    with requests.get(bstack1111l11ll1l_opy_, stream=True) as response:
        response.raise_for_status()
        with open(zip_path, bstack11l1l11_opy_ (u"ࠣࡹࡥࠦᾲ")) as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        logger.debug(bstack11l1l11_opy_ (u"ࠤࡉ࡭ࡱ࡫ࠠࡥࡱࡺࡲࡱࡵࡡࡥࡧࡧࠤࡸࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬࡭ࡻ࠱ࠦᾳ"))
    with zipfile.ZipFile(zip_path, bstack11l1l11_opy_ (u"ࠪࡶࠬᾴ")) as zip_ref:
        bstack1111ll1l11l_opy_ = zip_ref.namelist()
        if len(bstack1111ll1l11l_opy_) > 0:
            bstack1111l11l11l_opy_ = bstack1111ll1l11l_opy_[0] # bstack111l111l1l1_opy_ bstack111llll1lll_opy_ will be bstack1111llll111_opy_ 1 file i.e. the binary in the zip
        zip_ref.extractall(bstack111l1111l11_opy_)
        logger.debug(bstack11l1l11_opy_ (u"ࠦࡋ࡯࡬ࡦࡵࠣࡷࡺࡩࡣࡦࡵࡶࡪࡺࡲ࡬ࡺࠢࡨࡼࡹࡸࡡࡤࡶࡨࡨࠥࡺ࡯ࠡࠩࠥ᾵") + str(bstack111l1111l11_opy_) + bstack11l1l11_opy_ (u"ࠧ࠭ࠢᾶ"))
    os.remove(zip_path)
    return bstack1111l11l11l_opy_
def get_cli_dir():
    bstack1111ll1l1l1_opy_ = bstack1l11ll1111l_opy_()
    if bstack1111ll1l1l1_opy_:
        bstack1llllll1111_opy_ = os.path.join(bstack1111ll1l1l1_opy_, bstack11l1l11_opy_ (u"ࠨࡣ࡭࡫ࠥᾷ"))
        if not os.path.exists(bstack1llllll1111_opy_):
            os.makedirs(bstack1llllll1111_opy_, mode=0o777, exist_ok=True)
        return bstack1llllll1111_opy_
    else:
        raise FileNotFoundError(bstack11l1l11_opy_ (u"ࠢࡏࡱࠣࡻࡷ࡯ࡴࡢࡤ࡯ࡩࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡࡣࡹࡥ࡮ࡲࡡࡣ࡮ࡨࠤ࡫ࡵࡲࠡࡶ࡫ࡩ࡙ࠥࡄࡌࠢࡥ࡭ࡳࡧࡲࡺ࠰ࠥᾸ"))
def bstack1llllll11l1_opy_(bstack1llllll1111_opy_):
    bstack11l1l11_opy_ (u"ࠣࠤࠥࡋࡪࡺࠠࡵࡪࡨࠤࡵࡧࡴࡩࠢࡩࡳࡷࠦࡴࡩࡧࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡖࡈࡐࠦࡢࡪࡰࡤࡶࡾࠦࡩ࡯ࠢࡤࠤࡼࡸࡩࡵࡣࡥࡰࡪࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺ࠰ࠥࠦࠧᾹ")
    bstack1111l11ll11_opy_ = [
        os.path.join(bstack1llllll1111_opy_, f)
        for f in os.listdir(bstack1llllll1111_opy_)
        if os.path.isfile(os.path.join(bstack1llllll1111_opy_, f)) and f.startswith(bstack11l1l11_opy_ (u"ࠤࡥ࡭ࡳࡧࡲࡺ࠯ࠥᾺ"))
    ]
    if len(bstack1111l11ll11_opy_) > 0:
        return max(bstack1111l11ll11_opy_, key=os.path.getmtime) # get bstack111l1lll11l_opy_ binary
    return bstack11l1l11_opy_ (u"ࠥࠦΆ")
def bstack11l111ll1ll_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1l1l1l11l11_opy_(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = bstack1l1l1l11l11_opy_(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack1ll11l1l11_opy_(data, keys, default=None):
    bstack11l1l11_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࡘࡧࡦࡦ࡮ࡼࠤ࡬࡫ࡴࠡࡣࠣࡲࡪࡹࡴࡦࡦࠣࡺࡦࡲࡵࡦࠢࡩࡶࡴࡳࠠࡢࠢࡧ࡭ࡨࡺࡩࡰࡰࡤࡶࡾࠦ࡯ࡳࠢ࡯࡭ࡸࡺ࠮ࠋࠢࠣࠤࠥࡀࡰࡢࡴࡤࡱࠥࡪࡡࡵࡣ࠽ࠤ࡙࡮ࡥࠡࡦ࡬ࡧࡹ࡯࡯࡯ࡣࡵࡽࠥࡵࡲࠡ࡮࡬ࡷࡹࠦࡴࡰࠢࡷࡶࡦࡼࡥࡳࡵࡨ࠲ࠏࠦࠠࠡࠢ࠽ࡴࡦࡸࡡ࡮ࠢ࡮ࡩࡾࡹ࠺ࠡࡃࠣࡰ࡮ࡹࡴࠡࡱࡩࠤࡰ࡫ࡹࡴ࠱࡬ࡲࡩ࡯ࡣࡦࡵࠣࡶࡪࡶࡲࡦࡵࡨࡲࡹ࡯࡮ࡨࠢࡷ࡬ࡪࠦࡰࡢࡶ࡫࠲ࠏࠦࠠࠡࠢ࠽ࡴࡦࡸࡡ࡮ࠢࡧࡩ࡫ࡧࡵ࡭ࡶ࠽ࠤ࡛ࡧ࡬ࡶࡧࠣࡸࡴࠦࡲࡦࡶࡸࡶࡳࠦࡩࡧࠢࡷ࡬ࡪࠦࡰࡢࡶ࡫ࠤࡩࡵࡥࡴࠢࡱࡳࡹࠦࡥࡹ࡫ࡶࡸ࠳ࠐࠠࠡࠢࠣ࠾ࡷ࡫ࡴࡶࡴࡱ࠾࡚ࠥࡨࡦࠢࡹࡥࡱࡻࡥࠡࡣࡷࠤࡹ࡮ࡥࠡࡰࡨࡷࡹ࡫ࡤࠡࡲࡤࡸ࡭࠲ࠠࡰࡴࠣࡨࡪ࡬ࡡࡶ࡮ࡷࠤ࡮࡬ࠠ࡯ࡱࡷࠤ࡫ࡵࡵ࡯ࡦ࠱ࠎࠥࠦࠠࠡࠤࠥࠦᾼ")
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
def bstack11l11l111l_opy_(bstack111l111l11l_opy_, key, value):
    bstack11l1l11_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤ࡙ࠥࡴࡰࡴࡨࠤࡈࡒࡉࠡࡧࡱࡺ࡮ࡸ࡯࡯࡯ࡨࡲࡹࠦࡶࡢࡴ࡬ࡥࡧࡲࡥࡴࠢࡰࡥࡵࡶࡩ࡯ࡩࠣ࡭ࡳࠦࡴࡩࡧࠣࡴࡷࡵࡶࡪࡦࡨࡨࠥࡪࡩࡤࡶ࡬ࡳࡳࡧࡲࡺ࠰ࠍࠤࠥࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡤ࡮࡬ࡣࡪࡴࡶࡠࡸࡤࡶࡸࡥ࡭ࡢࡲ࠽ࠤࡉ࡯ࡣࡵ࡫ࡲࡲࡦࡸࡹࠡࡶࡲࠤࡸࡺ࡯ࡳࡧࠣࡩࡳࡼࡩࡳࡱࡱࡱࡪࡴࡴࠡࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠣࡱࡦࡶࡰࡪࡰࡪࡷࠏࠦࠠࠡࠢࠣࠤࠥࠦ࡫ࡦࡻ࠽ࠤࡐ࡫ࡹࠡࡨࡵࡳࡲࠦࡃࡍࡋࡢࡇࡆࡖࡓࡠࡖࡒࡣࡈࡕࡎࡇࡋࡊࠎࠥࠦࠠࠡࠢࠣࠤࠥࡼࡡ࡭ࡷࡨ࠾ࠥ࡜ࡡ࡭ࡷࡨࠤ࡫ࡸ࡯࡮ࠢࡦࡳࡲࡳࡡ࡯ࡦࠣࡰ࡮ࡴࡥࠡࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠎࠥࠦࠠࠡࠤࠥࠦ᾽")
    if key in bstack11ll1l11l_opy_:
        bstack1lll1lllll_opy_ = bstack11ll1l11l_opy_[key]
        if isinstance(bstack1lll1lllll_opy_, list):
            for env_name in bstack1lll1lllll_opy_:
                bstack111l111l11l_opy_[env_name] = value
        else:
            bstack111l111l11l_opy_[bstack1lll1lllll_opy_] = value