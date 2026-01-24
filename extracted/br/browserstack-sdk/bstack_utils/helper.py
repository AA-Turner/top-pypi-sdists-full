# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l11ll1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l1111_opy_ (bstack11l11ll_opy_):
    global bstack111l1l1_opy_
    bstack111l1ll_opy_ = ord (bstack11l11ll_opy_ [-1])
    bstack1l1l1_opy_ = bstack11l11ll_opy_ [:-1]
    bstack111111_opy_ = bstack111l1ll_opy_ % len (bstack1l1l1_opy_)
    bstack1lllll1l_opy_ = bstack1l1l1_opy_ [:bstack111111_opy_] + bstack1l1l1_opy_ [bstack111111_opy_:]
    if bstack1l111l_opy_:
        bstack1lll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    else:
        bstack1lll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    return eval (bstack1lll1l_opy_)
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
from bstack_utils.constants import (bstack1ll111l1l_opy_, bstack111ll11l_opy_, bstack1l1l1l1ll1_opy_,
                                    bstack11l111ll1ll_opy_, bstack11l11l1l1ll_opy_, bstack11l11111l1l_opy_, bstack11l111llll1_opy_)
from bstack_utils.measure import measure
from bstack_utils.messages import bstack1l1l1111_opy_, bstack111111111_opy_
from bstack_utils.proxy import bstack1l11ll11l1_opy_, bstack1ll1l1l1_opy_
from bstack_utils.constants import *
from bstack_utils import bstack111llll1ll_opy_
from bstack_utils.bstack11l1lll1ll_opy_ import bstack111lll1l1_opy_
from browserstack_sdk._version import __version__
bstack1llllll11l_opy_ = Config.bstack111ll1lll1_opy_()
logger = bstack111llll1ll_opy_.get_logger(__name__, bstack111llll1ll_opy_.bstack1ll11l1l111_opy_())
bstack11l1lll11_opy_ = bstack111llll1ll_opy_.bstack1l11ll11l_opy_(__name__)
def bstack11l1l11l1ll_opy_(config):
    return config[bstack1l1111_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬ᰻")]
def bstack11l1l11ll11_opy_(config):
    return config[bstack1l1111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ᰼")]
def bstack111l11ll1_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack111ll1lll11_opy_(obj):
    values = []
    bstack111ll1l11ll_opy_ = re.compile(bstack1l1111_opy_ (u"ࡷࠨ࡞ࡄࡗࡖࡘࡔࡓ࡟ࡕࡃࡊࡣࡡࡪࠫࠥࠤ᰽"), re.I)
    for key in obj.keys():
        if bstack111ll1l11ll_opy_.match(key):
            values.append(obj[key])
    return values
def bstack111l11111l1_opy_(config):
    tags = []
    tags.extend(bstack111ll1lll11_opy_(os.environ))
    tags.extend(bstack111ll1lll11_opy_(config))
    return tags
def bstack111lll111ll_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack111l1111l11_opy_(bstack111l11l1111_opy_):
    if not bstack111l11l1111_opy_:
        return bstack1l1111_opy_ (u"࠭ࠧ᰾")
    return bstack1l1111_opy_ (u"ࠢࡼࡿࠣࠬࢀࢃࠩࠣ᰿").format(bstack111l11l1111_opy_.name, bstack111l11l1111_opy_.email)
def bstack11l1l11ll1l_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack111ll1lllll_opy_ = repo.common_dir
        info = {
            bstack1l1111_opy_ (u"ࠣࡵ࡫ࡥࠧ᱀"): repo.head.commit.hexsha,
            bstack1l1111_opy_ (u"ࠤࡶ࡬ࡴࡸࡴࡠࡵ࡫ࡥࠧ᱁"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack1l1111_opy_ (u"ࠥࡦࡷࡧ࡮ࡤࡪࠥ᱂"): repo.active_branch.name,
            bstack1l1111_opy_ (u"ࠦࡹࡧࡧࠣ᱃"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack1l1111_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡹ࡫ࡲࠣ᱄"): bstack111l1111l11_opy_(repo.head.commit.committer),
            bstack1l1111_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡺࡥࡳࡡࡧࡥࡹ࡫ࠢ᱅"): repo.head.commit.committed_datetime.isoformat(),
            bstack1l1111_opy_ (u"ࠢࡢࡷࡷ࡬ࡴࡸࠢ᱆"): bstack111l1111l11_opy_(repo.head.commit.author),
            bstack1l1111_opy_ (u"ࠣࡣࡸࡸ࡭ࡵࡲࡠࡦࡤࡸࡪࠨ᱇"): repo.head.commit.authored_datetime.isoformat(),
            bstack1l1111_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡡࡰࡩࡸࡹࡡࡨࡧࠥ᱈"): repo.head.commit.message,
            bstack1l1111_opy_ (u"ࠥࡶࡴࡵࡴࠣ᱉"): repo.git.rev_parse(bstack1l1111_opy_ (u"ࠦ࠲࠳ࡳࡩࡱࡺ࠱ࡹࡵࡰ࡭ࡧࡹࡩࡱࠨ᱊")),
            bstack1l1111_opy_ (u"ࠧࡩ࡯࡮࡯ࡲࡲࡤ࡭ࡩࡵࡡࡧ࡭ࡷࠨ᱋"): bstack111ll1lllll_opy_,
            bstack1l1111_opy_ (u"ࠨࡷࡰࡴ࡮ࡸࡷ࡫ࡥࡠࡩ࡬ࡸࡤࡪࡩࡳࠤ᱌"): subprocess.check_output([bstack1l1111_opy_ (u"ࠢࡨ࡫ࡷࠦᱍ"), bstack1l1111_opy_ (u"ࠣࡴࡨࡺ࠲ࡶࡡࡳࡵࡨࠦᱎ"), bstack1l1111_opy_ (u"ࠤ࠰࠱࡬࡯ࡴ࠮ࡥࡲࡱࡲࡵ࡮࠮ࡦ࡬ࡶࠧᱏ")]).strip().decode(
                bstack1l1111_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩ᱐")),
            bstack1l1111_opy_ (u"ࠦࡱࡧࡳࡵࡡࡷࡥ࡬ࠨ᱑"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack1l1111_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡸࡥࡳࡪࡰࡦࡩࡤࡲࡡࡴࡶࡢࡸࡦ࡭ࠢ᱒"): repo.git.rev_list(
                bstack1l1111_opy_ (u"ࠨࡻࡾ࠰࠱ࡿࢂࠨ᱓").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack111l11ll111_opy_ = []
        for remote in remotes:
            bstack111lll1l1ll_opy_ = {
                bstack1l1111_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ᱔"): remote.name,
                bstack1l1111_opy_ (u"ࠣࡷࡵࡰࠧ᱕"): remote.url,
            }
            bstack111l11ll111_opy_.append(bstack111lll1l1ll_opy_)
        bstack111l11l1lll_opy_ = {
            bstack1l1111_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᱖"): bstack1l1111_opy_ (u"ࠥ࡫࡮ࡺࠢ᱗"),
            **info,
            bstack1l1111_opy_ (u"ࠦࡷ࡫࡭ࡰࡶࡨࡷࠧ᱘"): bstack111l11ll111_opy_
        }
        bstack111l11l1lll_opy_ = bstack111ll11l11l_opy_(bstack111l11l1lll_opy_)
        return bstack111l11l1lll_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack1l1111_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡵࡰࡶ࡮ࡤࡸ࡮ࡴࡧࠡࡉ࡬ࡸࠥࡳࡥࡵࡣࡧࡥࡹࡧࠠࡸ࡫ࡷ࡬ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠣ᱙").format(err))
        return {}
def bstack111ll1l1l1l_opy_(bstack111ll11l1ll_opy_=None):
    bstack1l1111_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡇࡦࡶࠣ࡫࡮ࡺࠠ࡮ࡧࡷࡥࡩࡧࡴࡢࠢࡶࡴࡪࡩࡩࡧ࡫ࡦࡥࡱࡲࡹࠡࡨࡲࡶࡲࡧࡴࡵࡧࡧࠤ࡫ࡵࡲࠡࡃࡌࠤࡸ࡫࡬ࡦࡥࡷ࡭ࡴࡴࠠࡶࡵࡨࠤࡨࡧࡳࡦࡵࠣࡪࡴࡸࠠࡦࡣࡦ࡬ࠥ࡬࡯࡭ࡦࡨࡶࠥ࡯࡮ࠡࡶ࡫ࡩࠥࡲࡩࡴࡶ࠱ࠎࠥࠦࠠࠡࡃࡵ࡫ࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࡨࡲࡰࡩ࡫ࡲࡴࠢࠫࡰ࡮ࡹࡴ࠭ࠢࡲࡴࡹ࡯࡯࡯ࡣ࡯࠭࠿ࠦࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡏࡱࡱࡩ࠿ࠦࡍࡰࡰࡲ࠱ࡷ࡫ࡰࡰࠢࡤࡴࡵࡸ࡯ࡢࡥ࡫࠰ࠥࡻࡳࡦࡵࠣࡧࡺࡸࡲࡦࡰࡷࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠ࡜ࡱࡶ࠲࡬࡫ࡴࡤࡹࡧࠬ࠮ࡣࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡆ࡯ࡳࡸࡾࠦ࡬ࡪࡵࡷࠤࡠࡣ࠺ࠡࡏࡸࡰࡹ࡯࠭ࡳࡧࡳࡳࠥࡧࡰࡱࡴࡲࡥࡨ࡮ࠠࡸ࡫ࡷ࡬ࠥࡴ࡯ࠡࡵࡲࡹࡷࡩࡥࡴࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡩࡩ࠲ࠠࡳࡧࡷࡹࡷࡴࡳࠡ࡝ࡠࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡑ࡯ࡳࡵࠢࡲࡪࠥࡶࡡࡵࡪࡶ࠾ࠥࡓࡵ࡭ࡶ࡬࠱ࡷ࡫ࡰࡰࠢࡤࡴࡵࡸ࡯ࡢࡥ࡫ࠤࡼ࡯ࡴࡩࠢࡶࡴࡪࡩࡩࡧ࡫ࡦࠤ࡫ࡵ࡬ࡥࡧࡵࡷࠥࡺ࡯ࠡࡣࡱࡥࡱࡿࡺࡦࠌࠣࠤࠥࠦࡒࡦࡶࡸࡶࡳࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢ࡯࡭ࡸࡺ࠺ࠡࡎ࡬ࡷࡹࠦ࡯ࡧࠢࡧ࡭ࡨࡺࡳ࠭ࠢࡨࡥࡨ࡮ࠠࡤࡱࡱࡸࡦ࡯࡮ࡪࡰࡪࠤ࡬࡯ࡴࠡ࡯ࡨࡸࡦࡪࡡࡵࡣࠣࡪࡴࡸࠠࡢࠢࡩࡳࡱࡪࡥࡳ࠰ࠍࠤࠥࠦࠠࠣࠤࠥᱚ")
    if bstack111ll11l1ll_opy_ is None:
        bstack111ll11l1ll_opy_ = [os.getcwd()]
    elif isinstance(bstack111ll11l1ll_opy_, list) and len(bstack111ll11l1ll_opy_) == 0:
        return []
    results = []
    for folder in bstack111ll11l1ll_opy_:
        try:
            if not os.path.exists(folder):
                raise Exception(bstack1l1111_opy_ (u"ࠢࡇࡱ࡯ࡨࡪࡸࠠࡥࡱࡨࡷࠥࡴ࡯ࡵࠢࡨࡼ࡮ࡹࡴ࠻ࠢࡾࢁࠧᱛ").format(folder))
            repo = git.Repo(folder, search_parent_directories=True)
            result = {
                bstack1l1111_opy_ (u"ࠣࡲࡵࡍࡩࠨᱜ"): bstack1l1111_opy_ (u"ࠤࠥᱝ"),
                bstack1l1111_opy_ (u"ࠥࡪ࡮ࡲࡥࡴࡅ࡫ࡥࡳ࡭ࡥࡥࠤᱞ"): [],
                bstack1l1111_opy_ (u"ࠦࡦࡻࡴࡩࡱࡵࡷࠧᱟ"): [],
                bstack1l1111_opy_ (u"ࠧࡶࡲࡅࡣࡷࡩࠧᱠ"): bstack1l1111_opy_ (u"ࠨࠢᱡ"),
                bstack1l1111_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺࡍࡦࡵࡶࡥ࡬࡫ࡳࠣᱢ"): [],
                bstack1l1111_opy_ (u"ࠣࡲࡵࡘ࡮ࡺ࡬ࡦࠤᱣ"): bstack1l1111_opy_ (u"ࠤࠥᱤ"),
                bstack1l1111_opy_ (u"ࠥࡴࡷࡊࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠥᱥ"): bstack1l1111_opy_ (u"ࠦࠧᱦ"),
                bstack1l1111_opy_ (u"ࠧࡶࡲࡓࡣࡺࡈ࡮࡬ࡦࠣᱧ"): bstack1l1111_opy_ (u"ࠨࠢᱨ")
            }
            bstack111ll1l1lll_opy_ = repo.active_branch.name
            bstack111ll1111ll_opy_ = repo.head.commit
            result[bstack1l1111_opy_ (u"ࠢࡱࡴࡌࡨࠧᱩ")] = bstack111ll1111ll_opy_.hexsha
            bstack111ll11llll_opy_ = _111l1l1lll1_opy_(repo)
            logger.debug(bstack1l1111_opy_ (u"ࠣࡄࡤࡷࡪࠦࡢࡳࡣࡱࡧ࡭ࠦࡦࡰࡴࠣࡧࡴࡳࡰࡢࡴ࡬ࡷࡴࡴ࠺ࠡࠤᱪ") + str(bstack111ll11llll_opy_) + bstack1l1111_opy_ (u"ࠤࠥᱫ"))
            if bstack111ll11llll_opy_:
                try:
                    bstack111lll1111l_opy_ = repo.git.diff(bstack1l1111_opy_ (u"ࠥ࠱࠲ࡴࡡ࡮ࡧ࠰ࡳࡳࡲࡹࠣᱬ"), bstack1ll1ll1l1ll_opy_ (u"ࠦࢀࡨࡡࡴࡧࡢࡦࡷࡧ࡮ࡤࡪࢀ࠲࠳࠴ࡻࡤࡷࡵࡶࡪࡴࡴࡠࡤࡵࡥࡳࡩࡨࡾࠤᱭ")).split(bstack1l1111_opy_ (u"ࠬࡢ࡮ࠨᱮ"))
                    logger.debug(bstack1l1111_opy_ (u"ࠨࡃࡩࡣࡱ࡫ࡪࡪࠠࡧ࡫࡯ࡩࡸࠦࡢࡦࡶࡺࡩࡪࡴࠠࡼࡤࡤࡷࡪࡥࡢࡳࡣࡱࡧ࡭ࢃࠠࡢࡰࡧࠤࢀࡩࡵࡳࡴࡨࡲࡹࡥࡢࡳࡣࡱࡧ࡭ࢃ࠺ࠡࠤᱯ") + str(bstack111lll1111l_opy_) + bstack1l1111_opy_ (u"ࠢࠣᱰ"))
                    result[bstack1l1111_opy_ (u"ࠣࡨ࡬ࡰࡪࡹࡃࡩࡣࡱ࡫ࡪࡪࠢᱱ")] = [f.strip() for f in bstack111lll1111l_opy_ if f.strip()]
                    commits = list(repo.iter_commits(bstack1ll1ll1l1ll_opy_ (u"ࠤࡾࡦࡦࡹࡥࡠࡤࡵࡥࡳࡩࡨࡾ࠰࠱ࡿࡨࡻࡲࡳࡧࡱࡸࡤࡨࡲࡢࡰࡦ࡬ࢂࠨᱲ")))
                except Exception:
                    logger.debug(bstack1l1111_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡧࡦࡶࠣࡧ࡭ࡧ࡮ࡨࡧࡧࠤ࡫࡯࡬ࡦࡵࠣࡪࡷࡵ࡭ࠡࡤࡵࡥࡳࡩࡨࠡࡥࡲࡱࡵࡧࡲࡪࡵࡲࡲ࠳ࠦࡆࡢ࡮࡯࡭ࡳ࡭ࠠࡣࡣࡦ࡯ࠥࡺ࡯ࠡࡴࡨࡧࡪࡴࡴࠡࡥࡲࡱࡲ࡯ࡴࡴ࠰ࠥᱳ"))
                    commits = list(repo.iter_commits(max_count=10))
                    if commits:
                        result[bstack1l1111_opy_ (u"ࠦ࡫࡯࡬ࡦࡵࡆ࡬ࡦࡴࡧࡦࡦࠥᱴ")] = _111l11lll1l_opy_(commits[:5])
            else:
                commits = list(repo.iter_commits(max_count=10))
                if commits:
                    result[bstack1l1111_opy_ (u"ࠧ࡬ࡩ࡭ࡧࡶࡇ࡭ࡧ࡮ࡨࡧࡧࠦᱵ")] = _111l11lll1l_opy_(commits[:5])
            bstack111l1llll11_opy_ = set()
            bstack111l1l11l11_opy_ = []
            for commit in commits:
                logger.debug(bstack1l1111_opy_ (u"ࠨࡐࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡧࡴࡳ࡭ࡪࡶ࠽ࠤࠧᱶ") + str(commit.message) + bstack1l1111_opy_ (u"ࠢࠣᱷ"))
                bstack111l11l1l1l_opy_ = commit.author.name if commit.author else bstack1l1111_opy_ (u"ࠣࡗࡱ࡯ࡳࡵࡷ࡯ࠤᱸ")
                bstack111l1llll11_opy_.add(bstack111l11l1l1l_opy_)
                bstack111l1l11l11_opy_.append({
                    bstack1l1111_opy_ (u"ࠤࡰࡩࡸࡹࡡࡨࡧࠥᱹ"): commit.message.strip(),
                    bstack1l1111_opy_ (u"ࠥࡹࡸ࡫ࡲࠣᱺ"): bstack111l11l1l1l_opy_
                })
            result[bstack1l1111_opy_ (u"ࠦࡦࡻࡴࡩࡱࡵࡷࠧᱻ")] = list(bstack111l1llll11_opy_)
            result[bstack1l1111_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡒ࡫ࡳࡴࡣࡪࡩࡸࠨᱼ")] = bstack111l1l11l11_opy_
            result[bstack1l1111_opy_ (u"ࠨࡰࡳࡆࡤࡸࡪࠨᱽ")] = bstack111ll1111ll_opy_.committed_datetime.strftime(bstack1l1111_opy_ (u"࡛ࠢࠦ࠰ࠩࡲ࠳ࠥࡥࠤ᱾"))
            if (not result[bstack1l1111_opy_ (u"ࠣࡲࡵࡘ࡮ࡺ࡬ࡦࠤ᱿")] or result[bstack1l1111_opy_ (u"ࠤࡳࡶ࡙࡯ࡴ࡭ࡧࠥᲀ")].strip() == bstack1l1111_opy_ (u"ࠥࠦᲁ")) and bstack111ll1111ll_opy_.message:
                bstack111l1l11ll1_opy_ = bstack111ll1111ll_opy_.message.strip().splitlines()
                result[bstack1l1111_opy_ (u"ࠦࡵࡸࡔࡪࡶ࡯ࡩࠧᲂ")] = bstack111l1l11ll1_opy_[0] if bstack111l1l11ll1_opy_ else bstack1l1111_opy_ (u"ࠧࠨᲃ")
                if len(bstack111l1l11ll1_opy_) > 2:
                    result[bstack1l1111_opy_ (u"ࠨࡰࡳࡆࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳࠨᲄ")] = bstack1l1111_opy_ (u"ࠧ࡝ࡰࠪᲅ").join(bstack111l1l11ll1_opy_[2:]).strip()
            results.append(result)
        except Exception as err:
            logger.error(bstack1l1111_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡱࡳࡹࡱࡧࡴࡪࡰࡪࠤࡌ࡯ࡴࠡ࡯ࡨࡸࡦࡪࡡࡵࡣࠣࡪࡴࡸࠠࡂࡋࠣࡷࡪࡲࡥࡤࡶ࡬ࡳࡳࠦࠨࡧࡱ࡯ࡨࡪࡸ࠺ࠡࡽࢀ࠭࠿ࠦࡻࡾࠢ࠰ࠤࢀࢃࠢᲆ").format(
                folder,
                type(err).__name__,
                str(err)
            ))
    filtered_results = [
        result
        for result in results
        if _111l1l111ll_opy_(result)
    ]
    return filtered_results
def _111l1l111ll_opy_(result):
    bstack1l1111_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࡋࡩࡱࡶࡥࡳࠢࡷࡳࠥࡩࡨࡦࡥ࡮ࠤ࡮࡬ࠠࡢࠢࡪ࡭ࡹࠦ࡭ࡦࡶࡤࡨࡦࡺࡡࠡࡴࡨࡷࡺࡲࡴࠡ࡫ࡶࠤࡻࡧ࡬ࡪࡦࠣࠬࡳࡵ࡮࠮ࡧࡰࡴࡹࡿࠠࡧ࡫࡯ࡩࡸࡉࡨࡢࡰࡪࡩࡩࠦࡡ࡯ࡦࠣࡥࡺࡺࡨࡰࡴࡶ࠭࠳ࠐࠠࠡࠢࠣࠦࠧࠨᲇ")
    return (
        isinstance(result.get(bstack1l1111_opy_ (u"ࠥࡪ࡮ࡲࡥࡴࡅ࡫ࡥࡳ࡭ࡥࡥࠤᲈ"), None), list)
        and len(result[bstack1l1111_opy_ (u"ࠦ࡫࡯࡬ࡦࡵࡆ࡬ࡦࡴࡧࡦࡦࠥᲉ")]) > 0
        and isinstance(result.get(bstack1l1111_opy_ (u"ࠧࡧࡵࡵࡪࡲࡶࡸࠨᲊ"), None), list)
        and len(result[bstack1l1111_opy_ (u"ࠨࡡࡶࡶ࡫ࡳࡷࡹࠢ᲋")]) > 0
    )
def _111l1l1lll1_opy_(repo):
    bstack1l1111_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࡕࡴࡼࠤࡹࡵࠠࡥࡧࡷࡩࡷࡳࡩ࡯ࡧࠣࡸ࡭࡫ࠠࡣࡣࡶࡩࠥࡨࡲࡢࡰࡦ࡬ࠥ࡬࡯ࡳࠢࡷ࡬ࡪࠦࡧࡪࡸࡨࡲࠥࡸࡥࡱࡱࠣࡻ࡮ࡺࡨࡰࡷࡷࠤ࡭ࡧࡲࡥࡥࡲࡨࡪࡪࠠ࡯ࡣࡰࡩࡸࠦࡡ࡯ࡦࠣࡻࡴࡸ࡫ࠡࡹ࡬ࡸ࡭ࠦࡡ࡭࡮࡚ࠣࡈ࡙ࠠࡱࡴࡲࡺ࡮ࡪࡥࡳࡵ࠱ࠎࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴࠢࡷ࡬ࡪࠦࡤࡦࡨࡤࡹࡱࡺࠠࡣࡴࡤࡲࡨ࡮ࠠࡪࡨࠣࡴࡴࡹࡳࡪࡤ࡯ࡩ࠱ࠦࡥ࡭ࡵࡨࠤࡓࡵ࡮ࡦ࠰ࠍࠤࠥࠦࠠࠣࠤࠥ᲌")
    try:
        try:
            origin = repo.remotes.origin
            bstack111ll1ll1l1_opy_ = origin.refs[bstack1l1111_opy_ (u"ࠨࡊࡈࡅࡉ࠭᲍")]
            target = bstack111ll1ll1l1_opy_.reference.name
            if target.startswith(bstack1l1111_opy_ (u"ࠩࡲࡶ࡮࡭ࡩ࡯࠱ࠪ᲎")):
                return target
        except Exception:
            pass
        if repo.remotes and repo.remotes.origin.refs:
            for ref in repo.remotes.origin.refs:
                if ref.name.startswith(bstack1l1111_opy_ (u"ࠪࡳࡷ࡯ࡧࡪࡰ࠲ࠫ᲏")):
                    return ref.name
        if repo.heads:
            return repo.heads[0].name
    except Exception:
        pass
    return None
def _111l11lll1l_opy_(commits):
    bstack1l1111_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࡌ࡫ࡴࠡ࡮࡬ࡷࡹࠦ࡯ࡧࠢࡦ࡬ࡦࡴࡧࡦࡦࠣࡪ࡮ࡲࡥࡴࠢࡩࡶࡴࡳࠠࡢࠢ࡯࡭ࡸࡺࠠࡰࡨࠣࡧࡴࡳ࡭ࡪࡶࡶ࠲ࠏࠦࠠࠡࠢࠥࠦࠧᲐ")
    bstack111lll1111l_opy_ = set()
    try:
        for commit in commits:
            if commit.parents:
                for parent in commit.parents:
                    diff = commit.diff(parent)
                    for bstack111l1l1l111_opy_ in diff:
                        if bstack111l1l1l111_opy_.a_path:
                            bstack111lll1111l_opy_.add(bstack111l1l1l111_opy_.a_path)
                        if bstack111l1l1l111_opy_.b_path:
                            bstack111lll1111l_opy_.add(bstack111l1l1l111_opy_.b_path)
    except Exception:
        pass
    return list(bstack111lll1111l_opy_)
def bstack111ll11l11l_opy_(bstack111l11l1lll_opy_):
    bstack111l1l1l1l1_opy_ = bstack111l111llll_opy_(bstack111l11l1lll_opy_)
    if bstack111l1l1l1l1_opy_ and bstack111l1l1l1l1_opy_ > bstack11l111ll1ll_opy_:
        bstack111l1llllll_opy_ = bstack111l1l1l1l1_opy_ - bstack11l111ll1ll_opy_
        bstack111ll11ll1l_opy_ = bstack1111llllll1_opy_(bstack111l11l1lll_opy_[bstack1l1111_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡤࡳࡥࡴࡵࡤ࡫ࡪࠨᲑ")], bstack111l1llllll_opy_)
        bstack111l11l1lll_opy_[bstack1l1111_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡥ࡭ࡦࡵࡶࡥ࡬࡫ࠢᲒ")] = bstack111ll11ll1l_opy_
        logger.info(bstack1l1111_opy_ (u"ࠢࡕࡪࡨࠤࡨࡵ࡭࡮࡫ࡷࠤ࡭ࡧࡳࠡࡤࡨࡩࡳࠦࡴࡳࡷࡱࡧࡦࡺࡥࡥ࠰ࠣࡗ࡮ࢀࡥࠡࡱࡩࠤࡨࡵ࡭࡮࡫ࡷࠤࡦ࡬ࡴࡦࡴࠣࡸࡷࡻ࡮ࡤࡣࡷ࡭ࡴࡴࠠࡪࡵࠣࡿࢂࠦࡋࡃࠤᲓ")
                    .format(bstack111l111llll_opy_(bstack111l11l1lll_opy_) / 1024))
    return bstack111l11l1lll_opy_
def bstack111l111llll_opy_(bstack11l11l11l1_opy_):
    try:
        if bstack11l11l11l1_opy_:
            bstack111l11l11ll_opy_ = json.dumps(bstack11l11l11l1_opy_)
            bstack111l1l11lll_opy_ = sys.getsizeof(bstack111l11l11ll_opy_)
            return bstack111l1l11lll_opy_
    except Exception as e:
        logger.debug(bstack1l1111_opy_ (u"ࠣࡕࡲࡱࡪࡺࡨࡪࡰࡪࠤࡼ࡫࡮ࡵࠢࡺࡶࡴࡴࡧࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡣ࡯ࡧࡺࡲࡡࡵ࡫ࡱ࡫ࠥࡹࡩࡻࡧࠣࡳ࡫ࠦࡊࡔࡑࡑࠤࡴࡨࡪࡦࡥࡷ࠾ࠥࢁࡽࠣᲔ").format(e))
    return -1
def bstack1111llllll1_opy_(field, bstack111l11ll1ll_opy_):
    try:
        bstack111lll11l11_opy_ = len(bytes(bstack11l11l1l1ll_opy_, bstack1l1111_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨᲕ")))
        bstack111ll1lll1l_opy_ = bytes(field, bstack1l1111_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩᲖ"))
        bstack111ll11111l_opy_ = len(bstack111ll1lll1l_opy_)
        bstack111l11l1l11_opy_ = ceil(bstack111ll11111l_opy_ - bstack111l11ll1ll_opy_ - bstack111lll11l11_opy_)
        if bstack111l11l1l11_opy_ > 0:
            bstack1111lllll11_opy_ = bstack111ll1lll1l_opy_[:bstack111l11l1l11_opy_].decode(bstack1l1111_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪᲗ"), errors=bstack1l1111_opy_ (u"ࠬ࡯ࡧ࡯ࡱࡵࡩࠬᲘ")) + bstack11l11l1l1ll_opy_
            return bstack1111lllll11_opy_
    except Exception as e:
        logger.debug(bstack1l1111_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡹࡸࡵ࡯ࡥࡤࡸ࡮ࡴࡧࠡࡨ࡬ࡩࡱࡪࠬࠡࡰࡲࡸ࡭࡯࡮ࡨࠢࡺࡥࡸࠦࡴࡳࡷࡱࡧࡦࡺࡥࡥࠢ࡫ࡩࡷ࡫࠺ࠡࡽࢀࠦᲙ").format(e))
    return field
def bstack1l11ll1l1_opy_():
    env = os.environ
    if (bstack1l1111_opy_ (u"ࠢࡋࡇࡑࡏࡎࡔࡓࡠࡗࡕࡐࠧᲚ") in env and len(env[bstack1l1111_opy_ (u"ࠣࡌࡈࡒࡐࡏࡎࡔࡡࡘࡖࡑࠨᲛ")]) > 0) or (
            bstack1l1111_opy_ (u"ࠤࡍࡉࡓࡑࡉࡏࡕࡢࡌࡔࡓࡅࠣᲜ") in env and len(env[bstack1l1111_opy_ (u"ࠥࡎࡊࡔࡋࡊࡐࡖࡣࡍࡕࡍࡆࠤᲝ")]) > 0):
        return {
            bstack1l1111_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᲞ"): bstack1l1111_opy_ (u"ࠧࡐࡥ࡯࡭࡬ࡲࡸࠨᲟ"),
            bstack1l1111_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᲠ"): env.get(bstack1l1111_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥᲡ")),
            bstack1l1111_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᲢ"): env.get(bstack1l1111_opy_ (u"ࠤࡍࡓࡇࡥࡎࡂࡏࡈࠦᲣ")),
            bstack1l1111_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᲤ"): env.get(bstack1l1111_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥᲥ"))
        }
    if env.get(bstack1l1111_opy_ (u"ࠧࡉࡉࠣᲦ")) == bstack1l1111_opy_ (u"ࠨࡴࡳࡷࡨࠦᲧ") and bstack1l1111lll1_opy_(env.get(bstack1l1111_opy_ (u"ࠢࡄࡋࡕࡇࡑࡋࡃࡊࠤᲨ"))):
        return {
            bstack1l1111_opy_ (u"ࠣࡰࡤࡱࡪࠨᲩ"): bstack1l1111_opy_ (u"ࠤࡆ࡭ࡷࡩ࡬ࡦࡅࡌࠦᲪ"),
            bstack1l1111_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᲫ"): env.get(bstack1l1111_opy_ (u"ࠦࡈࡏࡒࡄࡎࡈࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢᲬ")),
            bstack1l1111_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᲭ"): env.get(bstack1l1111_opy_ (u"ࠨࡃࡊࡔࡆࡐࡊࡥࡊࡐࡄࠥᲮ")),
            bstack1l1111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᲯ"): env.get(bstack1l1111_opy_ (u"ࠣࡅࡌࡖࡈࡒࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࠦᲰ"))
        }
    if env.get(bstack1l1111_opy_ (u"ࠤࡆࡍࠧᲱ")) == bstack1l1111_opy_ (u"ࠥࡸࡷࡻࡥࠣᲲ") and bstack1l1111lll1_opy_(env.get(bstack1l1111_opy_ (u"࡙ࠦࡘࡁࡗࡋࡖࠦᲳ"))):
        return {
            bstack1l1111_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᲴ"): bstack1l1111_opy_ (u"ࠨࡔࡳࡣࡹ࡭ࡸࠦࡃࡊࠤᲵ"),
            bstack1l1111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᲶ"): env.get(bstack1l1111_opy_ (u"ࠣࡖࡕࡅ࡛ࡏࡓࡠࡄࡘࡍࡑࡊ࡟ࡘࡇࡅࡣ࡚ࡘࡌࠣᲷ")),
            bstack1l1111_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᲸ"): env.get(bstack1l1111_opy_ (u"ࠥࡘࡗࡇࡖࡊࡕࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧᲹ")),
            bstack1l1111_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᲺ"): env.get(bstack1l1111_opy_ (u"࡚ࠧࡒࡂࡘࡌࡗࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦ᲻"))
        }
    if env.get(bstack1l1111_opy_ (u"ࠨࡃࡊࠤ᲼")) == bstack1l1111_opy_ (u"ࠢࡵࡴࡸࡩࠧᲽ") and env.get(bstack1l1111_opy_ (u"ࠣࡅࡌࡣࡓࡇࡍࡆࠤᲾ")) == bstack1l1111_opy_ (u"ࠤࡦࡳࡩ࡫ࡳࡩ࡫ࡳࠦᲿ"):
        return {
            bstack1l1111_opy_ (u"ࠥࡲࡦࡳࡥࠣ᳀"): bstack1l1111_opy_ (u"ࠦࡈࡵࡤࡦࡵ࡫࡭ࡵࠨ᳁"),
            bstack1l1111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ᳂"): None,
            bstack1l1111_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ᳃"): None,
            bstack1l1111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ᳄"): None
        }
    if env.get(bstack1l1111_opy_ (u"ࠣࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡇࡘࡁࡏࡅࡋࠦ᳅")) and env.get(bstack1l1111_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡉࡏࡎࡏࡌࡘࠧ᳆")):
        return {
            bstack1l1111_opy_ (u"ࠥࡲࡦࡳࡥࠣ᳇"): bstack1l1111_opy_ (u"ࠦࡇ࡯ࡴࡣࡷࡦ࡯ࡪࡺࠢ᳈"),
            bstack1l1111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ᳉"): env.get(bstack1l1111_opy_ (u"ࠨࡂࡊࡖࡅ࡙ࡈࡑࡅࡕࡡࡊࡍ࡙ࡥࡈࡕࡖࡓࡣࡔࡘࡉࡈࡋࡑࠦ᳊")),
            bstack1l1111_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ᳋"): None,
            bstack1l1111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ᳌"): env.get(bstack1l1111_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦ᳍"))
        }
    if env.get(bstack1l1111_opy_ (u"ࠥࡇࡎࠨ᳎")) == bstack1l1111_opy_ (u"ࠦࡹࡸࡵࡦࠤ᳏") and bstack1l1111lll1_opy_(env.get(bstack1l1111_opy_ (u"ࠧࡊࡒࡐࡐࡈࠦ᳐"))):
        return {
            bstack1l1111_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ᳑"): bstack1l1111_opy_ (u"ࠢࡅࡴࡲࡲࡪࠨ᳒"),
            bstack1l1111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ᳓"): env.get(bstack1l1111_opy_ (u"ࠤࡇࡖࡔࡔࡅࡠࡄࡘࡍࡑࡊ࡟ࡍࡋࡑࡏ᳔ࠧ")),
            bstack1l1111_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩ᳕ࠧ"): None,
            bstack1l1111_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴ᳖ࠥ"): env.get(bstack1l1111_opy_ (u"ࠧࡊࡒࡐࡐࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔ᳗ࠥ"))
        }
    if env.get(bstack1l1111_opy_ (u"ࠨࡃࡊࠤ᳘")) == bstack1l1111_opy_ (u"ࠢࡵࡴࡸࡩ᳙ࠧ") and bstack1l1111lll1_opy_(env.get(bstack1l1111_opy_ (u"ࠣࡕࡈࡑࡆࡖࡈࡐࡔࡈࠦ᳚"))):
        return {
            bstack1l1111_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᳛"): bstack1l1111_opy_ (u"ࠥࡗࡪࡳࡡࡱࡪࡲࡶࡪࠨ᳜"),
            bstack1l1111_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲ᳝ࠢ"): env.get(bstack1l1111_opy_ (u"࡙ࠧࡅࡎࡃࡓࡌࡔࡘࡅࡠࡑࡕࡋࡆࡔࡉ࡛ࡃࡗࡍࡔࡔ࡟ࡖࡔࡏ᳞ࠦ")),
            bstack1l1111_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥ᳟ࠣ"): env.get(bstack1l1111_opy_ (u"ࠢࡔࡇࡐࡅࡕࡎࡏࡓࡇࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧ᳠")),
            bstack1l1111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ᳡"): env.get(bstack1l1111_opy_ (u"ࠤࡖࡉࡒࡇࡐࡉࡑࡕࡉࡤࡐࡏࡃࡡࡌࡈ᳢ࠧ"))
        }
    if env.get(bstack1l1111_opy_ (u"ࠥࡇࡎࠨ᳣")) == bstack1l1111_opy_ (u"ࠦࡹࡸࡵࡦࠤ᳤") and bstack1l1111lll1_opy_(env.get(bstack1l1111_opy_ (u"ࠧࡍࡉࡕࡎࡄࡆࡤࡉࡉ᳥ࠣ"))):
        return {
            bstack1l1111_opy_ (u"ࠨ࡮ࡢ࡯ࡨ᳦ࠦ"): bstack1l1111_opy_ (u"ࠢࡈ࡫ࡷࡐࡦࡨ᳧ࠢ"),
            bstack1l1111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯᳨ࠦ"): env.get(bstack1l1111_opy_ (u"ࠤࡆࡍࡤࡐࡏࡃࡡࡘࡖࡑࠨᳩ")),
            bstack1l1111_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᳪ"): env.get(bstack1l1111_opy_ (u"ࠦࡈࡏ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤᳫ")),
            bstack1l1111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᳬ"): env.get(bstack1l1111_opy_ (u"ࠨࡃࡊࡡࡍࡓࡇࡥࡉࡅࠤ᳭"))
        }
    if env.get(bstack1l1111_opy_ (u"ࠢࡄࡋࠥᳮ")) == bstack1l1111_opy_ (u"ࠣࡶࡵࡹࡪࠨᳯ") and bstack1l1111lll1_opy_(env.get(bstack1l1111_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࠧᳰ"))):
        return {
            bstack1l1111_opy_ (u"ࠥࡲࡦࡳࡥࠣᳱ"): bstack1l1111_opy_ (u"ࠦࡇࡻࡩ࡭ࡦ࡮࡭ࡹ࡫ࠢᳲ"),
            bstack1l1111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᳳ"): env.get(bstack1l1111_opy_ (u"ࠨࡂࡖࡋࡏࡈࡐࡏࡔࡆࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧ᳴")),
            bstack1l1111_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᳵ"): env.get(bstack1l1111_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࡣࡑࡇࡂࡆࡎࠥᳶ")) or env.get(bstack1l1111_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡏࡃࡐࡉࠧ᳷")),
            bstack1l1111_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ᳸"): env.get(bstack1l1111_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡎࡍ࡙ࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨ᳹"))
        }
    if bstack1l1111lll1_opy_(env.get(bstack1l1111_opy_ (u"࡚ࠧࡆࡠࡄࡘࡍࡑࡊࠢᳺ"))):
        return {
            bstack1l1111_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ᳻"): bstack1l1111_opy_ (u"ࠢࡗ࡫ࡶࡹࡦࡲࠠࡔࡶࡸࡨ࡮ࡵࠠࡕࡧࡤࡱ࡙ࠥࡥࡳࡸ࡬ࡧࡪࡹࠢ᳼"),
            bstack1l1111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ᳽"): bstack1l1111_opy_ (u"ࠤࡾࢁࢀࢃࠢ᳾").format(env.get(bstack1l1111_opy_ (u"ࠪࡗ࡞࡙ࡔࡆࡏࡢࡘࡊࡇࡍࡇࡑࡘࡒࡉࡇࡔࡊࡑࡑࡗࡊࡘࡖࡆࡔࡘࡖࡎ࠭᳿")), env.get(bstack1l1111_opy_ (u"ࠫࡘ࡟ࡓࡕࡇࡐࡣ࡙ࡋࡁࡎࡒࡕࡓࡏࡋࡃࡕࡋࡇࠫᴀ"))),
            bstack1l1111_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᴁ"): env.get(bstack1l1111_opy_ (u"ࠨࡓ࡚ࡕࡗࡉࡒࡥࡄࡆࡈࡌࡒࡎ࡚ࡉࡐࡐࡌࡈࠧᴂ")),
            bstack1l1111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᴃ"): env.get(bstack1l1111_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡏࡄࠣᴄ"))
        }
    if bstack1l1111lll1_opy_(env.get(bstack1l1111_opy_ (u"ࠤࡄࡔࡕ࡜ࡅ࡚ࡑࡕࠦᴅ"))):
        return {
            bstack1l1111_opy_ (u"ࠥࡲࡦࡳࡥࠣᴆ"): bstack1l1111_opy_ (u"ࠦࡆࡶࡰࡷࡧࡼࡳࡷࠨᴇ"),
            bstack1l1111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᴈ"): bstack1l1111_opy_ (u"ࠨࡻࡾ࠱ࡳࡶࡴࡰࡥࡤࡶ࠲ࡿࢂ࠵ࡻࡾ࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁࠧᴉ").format(env.get(bstack1l1111_opy_ (u"ࠧࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡘࡖࡑ࠭ᴊ")), env.get(bstack1l1111_opy_ (u"ࠨࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡅࡈࡉࡏࡖࡐࡗࡣࡓࡇࡍࡆࠩᴋ")), env.get(bstack1l1111_opy_ (u"ࠩࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡕࡘࡏࡋࡇࡆࡘࡤ࡙ࡌࡖࡉࠪᴌ")), env.get(bstack1l1111_opy_ (u"ࠪࡅࡕࡖࡖࡆ࡛ࡒࡖࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧᴍ"))),
            bstack1l1111_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᴎ"): env.get(bstack1l1111_opy_ (u"ࠧࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤᴏ")),
            bstack1l1111_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᴐ"): env.get(bstack1l1111_opy_ (u"ࠢࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣᴑ"))
        }
    if env.get(bstack1l1111_opy_ (u"ࠣࡃ࡝࡙ࡗࡋ࡟ࡉࡖࡗࡔࡤ࡛ࡓࡆࡔࡢࡅࡌࡋࡎࡕࠤᴒ")) and env.get(bstack1l1111_opy_ (u"ࠤࡗࡊࡤࡈࡕࡊࡎࡇࠦᴓ")):
        return {
            bstack1l1111_opy_ (u"ࠥࡲࡦࡳࡥࠣᴔ"): bstack1l1111_opy_ (u"ࠦࡆࢀࡵࡳࡧࠣࡇࡎࠨᴕ"),
            bstack1l1111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᴖ"): bstack1l1111_opy_ (u"ࠨࡻࡾࡽࢀ࠳ࡤࡨࡵࡪ࡮ࡧ࠳ࡷ࡫ࡳࡶ࡮ࡷࡷࡄࡨࡵࡪ࡮ࡧࡍࡩࡃࡻࡾࠤᴗ").format(env.get(bstack1l1111_opy_ (u"ࠧࡔ࡛ࡖࡘࡊࡓ࡟ࡕࡇࡄࡑࡋࡕࡕࡏࡆࡄࡘࡎࡕࡎࡔࡇࡕ࡚ࡊࡘࡕࡓࡋࠪᴘ")), env.get(bstack1l1111_opy_ (u"ࠨࡕ࡜ࡗ࡙ࡋࡍࡠࡖࡈࡅࡒࡖࡒࡐࡌࡈࡇ࡙࠭ᴙ")), env.get(bstack1l1111_opy_ (u"ࠩࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊࡉࡅࠩᴚ"))),
            bstack1l1111_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᴛ"): env.get(bstack1l1111_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡋࡇࠦᴜ")),
            bstack1l1111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᴝ"): env.get(bstack1l1111_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡍࡉࠨᴞ"))
        }
    if any([env.get(bstack1l1111_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧᴟ")), env.get(bstack1l1111_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡗࡋࡓࡐࡎ࡙ࡉࡉࡥࡓࡐࡗࡕࡇࡊࡥࡖࡆࡔࡖࡍࡔࡔࠢᴠ")), env.get(bstack1l1111_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤ࡙ࡏࡖࡔࡆࡉࡤ࡜ࡅࡓࡕࡌࡓࡓࠨᴡ"))]):
        return {
            bstack1l1111_opy_ (u"ࠥࡲࡦࡳࡥࠣᴢ"): bstack1l1111_opy_ (u"ࠦࡆ࡝ࡓࠡࡅࡲࡨࡪࡈࡵࡪ࡮ࡧࠦᴣ"),
            bstack1l1111_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᴤ"): env.get(bstack1l1111_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡓ࡙ࡇࡒࡉࡄࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧᴥ")),
            bstack1l1111_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᴦ"): env.get(bstack1l1111_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࠨᴧ")),
            bstack1l1111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᴨ"): env.get(bstack1l1111_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠣᴩ"))
        }
    if env.get(bstack1l1111_opy_ (u"ࠦࡧࡧ࡭ࡣࡱࡲࡣࡧࡻࡩ࡭ࡦࡑࡹࡲࡨࡥࡳࠤᴪ")):
        return {
            bstack1l1111_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᴫ"): bstack1l1111_opy_ (u"ࠨࡂࡢ࡯ࡥࡳࡴࠨᴬ"),
            bstack1l1111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᴭ"): env.get(bstack1l1111_opy_ (u"ࠣࡤࡤࡱࡧࡵ࡯ࡠࡤࡸ࡭ࡱࡪࡒࡦࡵࡸࡰࡹࡹࡕࡳ࡮ࠥᴮ")),
            bstack1l1111_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᴯ"): env.get(bstack1l1111_opy_ (u"ࠥࡦࡦࡳࡢࡰࡱࡢࡷ࡭ࡵࡲࡵࡌࡲࡦࡓࡧ࡭ࡦࠤᴰ")),
            bstack1l1111_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᴱ"): env.get(bstack1l1111_opy_ (u"ࠧࡨࡡ࡮ࡤࡲࡳࡤࡨࡵࡪ࡮ࡧࡒࡺࡳࡢࡦࡴࠥᴲ"))
        }
    if env.get(bstack1l1111_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘࠢᴳ")) or env.get(bstack1l1111_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࡠࡏࡄࡍࡓࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡕࡗࡅࡗ࡚ࡅࡅࠤᴴ")):
        return {
            bstack1l1111_opy_ (u"ࠣࡰࡤࡱࡪࠨᴵ"): bstack1l1111_opy_ (u"ࠤ࡚ࡩࡷࡩ࡫ࡦࡴࠥᴶ"),
            bstack1l1111_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᴷ"): env.get(bstack1l1111_opy_ (u"ࠦ࡜ࡋࡒࡄࡍࡈࡖࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣᴸ")),
            bstack1l1111_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᴹ"): bstack1l1111_opy_ (u"ࠨࡍࡢ࡫ࡱࠤࡕ࡯ࡰࡦ࡮࡬ࡲࡪࠨᴺ") if env.get(bstack1l1111_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࡠࡏࡄࡍࡓࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡕࡗࡅࡗ࡚ࡅࡅࠤᴻ")) else None,
            bstack1l1111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᴼ"): env.get(bstack1l1111_opy_ (u"ࠤ࡚ࡉࡗࡉࡋࡆࡔࡢࡋࡎ࡚࡟ࡄࡑࡐࡑࡎ࡚ࠢᴽ"))
        }
    if any([env.get(bstack1l1111_opy_ (u"ࠥࡋࡈࡖ࡟ࡑࡔࡒࡎࡊࡉࡔࠣᴾ")), env.get(bstack1l1111_opy_ (u"ࠦࡌࡉࡌࡐࡗࡇࡣࡕࡘࡏࡋࡇࡆࡘࠧᴿ")), env.get(bstack1l1111_opy_ (u"ࠧࡍࡏࡐࡉࡏࡉࡤࡉࡌࡐࡗࡇࡣࡕࡘࡏࡋࡇࡆࡘࠧᵀ"))]):
        return {
            bstack1l1111_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᵁ"): bstack1l1111_opy_ (u"ࠢࡈࡱࡲ࡫ࡱ࡫ࠠࡄ࡮ࡲࡹࡩࠨᵂ"),
            bstack1l1111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᵃ"): None,
            bstack1l1111_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᵄ"): env.get(bstack1l1111_opy_ (u"ࠥࡔࡗࡕࡊࡆࡅࡗࡣࡎࡊࠢᵅ")),
            bstack1l1111_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᵆ"): env.get(bstack1l1111_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡎࡊࠢᵇ"))
        }
    if env.get(bstack1l1111_opy_ (u"ࠨࡓࡉࡋࡓࡔࡆࡈࡌࡆࠤᵈ")):
        return {
            bstack1l1111_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᵉ"): bstack1l1111_opy_ (u"ࠣࡕ࡫࡭ࡵࡶࡡࡣ࡮ࡨࠦᵊ"),
            bstack1l1111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᵋ"): env.get(bstack1l1111_opy_ (u"ࠥࡗࡍࡏࡐࡑࡃࡅࡐࡊࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤᵌ")),
            bstack1l1111_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᵍ"): bstack1l1111_opy_ (u"ࠧࡐ࡯ࡣࠢࠦࡿࢂࠨᵎ").format(env.get(bstack1l1111_opy_ (u"࠭ࡓࡉࡋࡓࡔࡆࡈࡌࡆࡡࡍࡓࡇࡥࡉࡅࠩᵏ"))) if env.get(bstack1l1111_opy_ (u"ࠢࡔࡊࡌࡔࡕࡇࡂࡍࡇࡢࡎࡔࡈ࡟ࡊࡆࠥᵐ")) else None,
            bstack1l1111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᵑ"): env.get(bstack1l1111_opy_ (u"ࠤࡖࡌࡎࡖࡐࡂࡄࡏࡉࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦᵒ"))
        }
    if bstack1l1111lll1_opy_(env.get(bstack1l1111_opy_ (u"ࠥࡒࡊ࡚ࡌࡊࡈ࡜ࠦᵓ"))):
        return {
            bstack1l1111_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᵔ"): bstack1l1111_opy_ (u"ࠧࡔࡥࡵ࡮࡬ࡪࡾࠨᵕ"),
            bstack1l1111_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᵖ"): env.get(bstack1l1111_opy_ (u"ࠢࡅࡇࡓࡐࡔ࡟࡟ࡖࡔࡏࠦᵗ")),
            bstack1l1111_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᵘ"): env.get(bstack1l1111_opy_ (u"ࠤࡖࡍ࡙ࡋ࡟ࡏࡃࡐࡉࠧᵙ")),
            bstack1l1111_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᵚ"): env.get(bstack1l1111_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡍࡉࠨᵛ"))
        }
    if bstack1l1111lll1_opy_(env.get(bstack1l1111_opy_ (u"ࠧࡍࡉࡕࡊࡘࡆࡤࡇࡃࡕࡋࡒࡒࡘࠨᵜ"))):
        return {
            bstack1l1111_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᵝ"): bstack1l1111_opy_ (u"ࠢࡈ࡫ࡷࡌࡺࡨࠠࡂࡥࡷ࡭ࡴࡴࡳࠣᵞ"),
            bstack1l1111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᵟ"): bstack1l1111_opy_ (u"ࠤࡾࢁ࠴ࢁࡽ࠰ࡣࡦࡸ࡮ࡵ࡮ࡴ࠱ࡵࡹࡳࡹ࠯ࡼࡿࠥᵠ").format(env.get(bstack1l1111_opy_ (u"ࠪࡋࡎ࡚ࡈࡖࡄࡢࡗࡊࡘࡖࡆࡔࡢ࡙ࡗࡒࠧᵡ")), env.get(bstack1l1111_opy_ (u"ࠫࡌࡏࡔࡉࡗࡅࡣࡗࡋࡐࡐࡕࡌࡘࡔࡘ࡙ࠨᵢ")), env.get(bstack1l1111_opy_ (u"ࠬࡍࡉࡕࡊࡘࡆࡤࡘࡕࡏࡡࡌࡈࠬᵣ"))),
            bstack1l1111_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᵤ"): env.get(bstack1l1111_opy_ (u"ࠢࡈࡋࡗࡌ࡚ࡈ࡟ࡘࡑࡕࡏࡋࡒࡏࡘࠤᵥ")),
            bstack1l1111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᵦ"): env.get(bstack1l1111_opy_ (u"ࠤࡊࡍ࡙ࡎࡕࡃࡡࡕ࡙ࡓࡥࡉࡅࠤᵧ"))
        }
    if env.get(bstack1l1111_opy_ (u"ࠥࡇࡎࠨᵨ")) == bstack1l1111_opy_ (u"ࠦࡹࡸࡵࡦࠤᵩ") and env.get(bstack1l1111_opy_ (u"ࠧ࡜ࡅࡓࡅࡈࡐࠧᵪ")) == bstack1l1111_opy_ (u"ࠨ࠱ࠣᵫ"):
        return {
            bstack1l1111_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᵬ"): bstack1l1111_opy_ (u"ࠣࡘࡨࡶࡨ࡫࡬ࠣᵭ"),
            bstack1l1111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᵮ"): bstack1l1111_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࡿࢂࠨᵯ").format(env.get(bstack1l1111_opy_ (u"࡛ࠫࡋࡒࡄࡇࡏࡣ࡚ࡘࡌࠨᵰ"))),
            bstack1l1111_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᵱ"): None,
            bstack1l1111_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᵲ"): None,
        }
    if env.get(bstack1l1111_opy_ (u"ࠢࡕࡇࡄࡑࡈࡏࡔ࡚ࡡ࡙ࡉࡗ࡙ࡉࡐࡐࠥᵳ")):
        return {
            bstack1l1111_opy_ (u"ࠣࡰࡤࡱࡪࠨᵴ"): bstack1l1111_opy_ (u"ࠤࡗࡩࡦࡳࡣࡪࡶࡼࠦᵵ"),
            bstack1l1111_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᵶ"): None,
            bstack1l1111_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᵷ"): env.get(bstack1l1111_opy_ (u"࡚ࠧࡅࡂࡏࡆࡍ࡙࡟࡟ࡑࡔࡒࡎࡊࡉࡔࡠࡐࡄࡑࡊࠨᵸ")),
            bstack1l1111_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᵹ"): env.get(bstack1l1111_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨᵺ"))
        }
    if any([env.get(bstack1l1111_opy_ (u"ࠣࡅࡒࡒࡈࡕࡕࡓࡕࡈࠦᵻ")), env.get(bstack1l1111_opy_ (u"ࠤࡆࡓࡓࡉࡏࡖࡔࡖࡉࡤ࡛ࡒࡍࠤᵼ")), env.get(bstack1l1111_opy_ (u"ࠥࡇࡔࡔࡃࡐࡗࡕࡗࡊࡥࡕࡔࡇࡕࡒࡆࡓࡅࠣᵽ")), env.get(bstack1l1111_opy_ (u"ࠦࡈࡕࡎࡄࡑࡘࡖࡘࡋ࡟ࡕࡇࡄࡑࠧᵾ"))]):
        return {
            bstack1l1111_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᵿ"): bstack1l1111_opy_ (u"ࠨࡃࡰࡰࡦࡳࡺࡸࡳࡦࠤᶀ"),
            bstack1l1111_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᶁ"): None,
            bstack1l1111_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᶂ"): env.get(bstack1l1111_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥᶃ")) or None,
            bstack1l1111_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᶄ"): env.get(bstack1l1111_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡍࡉࠨᶅ"), 0)
        }
    if env.get(bstack1l1111_opy_ (u"ࠧࡍࡏࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥᶆ")):
        return {
            bstack1l1111_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᶇ"): bstack1l1111_opy_ (u"ࠢࡈࡱࡆࡈࠧᶈ"),
            bstack1l1111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᶉ"): None,
            bstack1l1111_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᶊ"): env.get(bstack1l1111_opy_ (u"ࠥࡋࡔࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣᶋ")),
            bstack1l1111_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᶌ"): env.get(bstack1l1111_opy_ (u"ࠧࡍࡏࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡇࡔ࡛ࡎࡕࡇࡕࠦᶍ"))
        }
    if env.get(bstack1l1111_opy_ (u"ࠨࡃࡇࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦᶎ")):
        return {
            bstack1l1111_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᶏ"): bstack1l1111_opy_ (u"ࠣࡅࡲࡨࡪࡌࡲࡦࡵ࡫ࠦᶐ"),
            bstack1l1111_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᶑ"): env.get(bstack1l1111_opy_ (u"ࠥࡇࡋࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤᶒ")),
            bstack1l1111_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᶓ"): env.get(bstack1l1111_opy_ (u"ࠧࡉࡆࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡒࡆࡓࡅࠣᶔ")),
            bstack1l1111_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᶕ"): env.get(bstack1l1111_opy_ (u"ࠢࡄࡈࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧᶖ"))
        }
    return {bstack1l1111_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᶗ"): None}
def get_host_info():
    return {
        bstack1l1111_opy_ (u"ࠤ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨࠦᶘ"): platform.node(),
        bstack1l1111_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࠧᶙ"): platform.system(),
        bstack1l1111_opy_ (u"ࠦࡹࡿࡰࡦࠤᶚ"): platform.machine(),
        bstack1l1111_opy_ (u"ࠧࡼࡥࡳࡵ࡬ࡳࡳࠨᶛ"): platform.version(),
        bstack1l1111_opy_ (u"ࠨࡡࡳࡥ࡫ࠦᶜ"): platform.architecture()[0]
    }
def bstack1111l111_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack111l1llll1l_opy_():
    if bstack1llllll11l_opy_.get_property(bstack1l1111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨᶝ")):
        return bstack1l1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧᶞ")
    return bstack1l1111_opy_ (u"ࠩࡸࡲࡰࡴ࡯ࡸࡰࡢ࡫ࡷ࡯ࡤࠨᶟ")
def bstack111l1l11l1l_opy_(driver):
    info = {
        bstack1l1111_opy_ (u"ࠪࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᶠ"): driver.capabilities,
        bstack1l1111_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠨᶡ"): driver.session_id,
        bstack1l1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭ᶢ"): driver.capabilities.get(bstack1l1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫᶣ"), None),
        bstack1l1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᶤ"): driver.capabilities.get(bstack1l1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᶥ"), None),
        bstack1l1111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࠫᶦ"): driver.capabilities.get(bstack1l1111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠩᶧ"), None),
        bstack1l1111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᶨ"):driver.capabilities.get(bstack1l1111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧᶩ"), None),
    }
    if bstack111l1llll1l_opy_() == bstack1l1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬᶪ"):
        if bstack1111ll111_opy_():
            info[bstack1l1111_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࠨᶫ")] = bstack1l1111_opy_ (u"ࠨࡣࡳࡴ࠲ࡧࡵࡵࡱࡰࡥࡹ࡫ࠧᶬ")
        elif driver.capabilities.get(bstack1l1111_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᶭ"), {}).get(bstack1l1111_opy_ (u"ࠪࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫ࠧᶮ"), False):
            info[bstack1l1111_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࠬᶯ")] = bstack1l1111_opy_ (u"ࠬࡺࡵࡳࡤࡲࡷࡨࡧ࡬ࡦࠩᶰ")
        else:
            info[bstack1l1111_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺࠧᶱ")] = bstack1l1111_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩᶲ")
    return info
def bstack1111ll111_opy_():
    if bstack1llllll11l_opy_.get_property(bstack1l1111_opy_ (u"ࠨࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠧᶳ")):
        return True
    if bstack1l1111lll1_opy_(os.environ.get(bstack1l1111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪᶴ"), None)):
        return True
    return False
def bstack111l11l111l_opy_(bstack111l1l1l11l_opy_, url, response, headers=None, data=None):
    bstack1l1111_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࡆࡺ࡯࡬ࡥࠢࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦ࡬ࡰࡩࠣࡴࡦࡸࡡ࡮ࡧࡷࡩࡷࡹࠠࡧࡱࡵࠤࡷ࡫ࡱࡶࡧࡶࡸ࠴ࡸࡥࡴࡲࡲࡲࡸ࡫ࠠ࡭ࡱࡪ࡫࡮ࡴࡧࠋࠢࠣࠤࠥࡇࡲࡨࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡸࡥࡲࡷࡨࡷࡹࡥࡴࡺࡲࡨ࠾ࠥࡎࡔࡕࡒࠣࡱࡪࡺࡨࡰࡦࠣࠬࡌࡋࡔ࠭ࠢࡓࡓࡘ࡚ࠬࠡࡧࡷࡧ࠳࠯ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡷࡵࡰ࠿ࠦࡒࡦࡳࡸࡩࡸࡺࠠࡖࡔࡏ࠳ࡪࡴࡤࡱࡱ࡬ࡲࡹࠐࠠࠡࠢࠣࠤࠥࠦࠠࡳࡧࡶࡴࡴࡴࡳࡦ࠼ࠣࡖࡪࡹࡰࡰࡰࡶࡩࠥࡵࡢ࡫ࡧࡦࡸࠥ࡬ࡲࡰ࡯ࠣࡶࡪࡷࡵࡦࡵࡷࡷࠏࠦࠠࠡࠢࠣࠤࠥࠦࡨࡦࡣࡧࡩࡷࡹ࠺ࠡࡔࡨࡵࡺ࡫ࡳࡵࠢ࡫ࡩࡦࡪࡥࡳࡵࠣࡳࡷࠦࡎࡰࡰࡨࠎࠥࠦࠠࠡࠢࠣࠤࠥࡪࡡࡵࡣ࠽ࠤࡗ࡫ࡱࡶࡧࡶࡸࠥࡐࡓࡐࡐࠣࡨࡦࡺࡡࠡࡱࡵࠤࡓࡵ࡮ࡦࠌࠣࠤࠥࠦࡒࡦࡶࡸࡶࡳࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡧ࡭ࡨࡺ࠺ࠡࡈࡲࡶࡲࡧࡴࡵࡧࡧࠤࡱࡵࡧࠡ࡯ࡨࡷࡸࡧࡧࡦࠢࡺ࡭ࡹ࡮ࠠࡳࡧࡴࡹࡪࡹࡴࠡࡣࡱࡨࠥࡸࡥࡴࡲࡲࡲࡸ࡫ࠠࡥࡣࡷࡥࠏࠦࠠࠡࠢࠥࠦࠧᶵ")
    bstack111l1lll1l1_opy_ = {
        bstack1l1111_opy_ (u"ࠦ࡭࡫ࡡࡥࡧࡵࡷࠧᶶ"): headers,
        bstack1l1111_opy_ (u"ࠧࡳࡥࡵࡪࡲࡨࠧᶷ"): bstack111l1l1l11l_opy_.upper(),
        bstack1l1111_opy_ (u"ࠨࡡࡨࡧࡱࡸࠧᶸ"): None,
        bstack1l1111_opy_ (u"ࠢࡦࡰࡧࡴࡴ࡯࡮ࡵࠤᶹ"): url,
        bstack1l1111_opy_ (u"ࠣ࡬ࡶࡳࡳࠨᶺ"): data
    }
    try:
        bstack111ll1l111l_opy_ = response.json()
    except Exception:
        bstack111ll1l111l_opy_ = response.text
    bstack111l1111lll_opy_ = {
        bstack1l1111_opy_ (u"ࠤࡥࡳࡩࡿࠢᶻ"): bstack111ll1l111l_opy_,
        bstack1l1111_opy_ (u"ࠥࡷࡹࡧࡴࡶࡵࡆࡳࡩ࡫ࠢᶼ"): response.status_code
    }
    return {
        bstack1l1111_opy_ (u"ࠦࡷ࡫ࡱࡶࡧࡶࡸࠧᶽ"): bstack111l1lll1l1_opy_,
        bstack1l1111_opy_ (u"ࠧࡸࡥࡴࡲࡲࡲࡸ࡫ࠢᶾ"): bstack111l1111lll_opy_
    }
def bstack1l1ll11111_opy_(bstack111l1l1l11l_opy_, url, data, config):
    headers = config.get(bstack1l1111_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧᶿ"), None)
    proxies = bstack1l11ll11l1_opy_(config, url)
    auth = config.get(bstack1l1111_opy_ (u"ࠧࡢࡷࡷ࡬ࠬ᷀"), None)
    response = requests.request(
            bstack111l1l1l11l_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    try:
        log_message = bstack111l11l111l_opy_(bstack111l1l1l11l_opy_, url, response, headers, data)
        bstack11l1lll11_opy_.debug(json.dumps(log_message, separators=(bstack1l1111_opy_ (u"ࠨ࠮ࠪ᷁"), bstack1l1111_opy_ (u"ࠩ࠽᷂ࠫ"))))
    except Exception as e:
        logger.debug(bstack1l1111_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡ࡮ࡲ࡫࡬࡯࡮ࡨࠢࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡲࡦࡳࡸࡩࡸࡺ࠺ࠡࡽࢀࠦ᷃").format(e))
    return response
def bstack1lll11l1ll_opy_(bstack1ll11ll1l1_opy_, size):
    bstack1llll111l1_opy_ = []
    while len(bstack1ll11ll1l1_opy_) > size:
        bstack1l1l111l11_opy_ = bstack1ll11ll1l1_opy_[:size]
        bstack1llll111l1_opy_.append(bstack1l1l111l11_opy_)
        bstack1ll11ll1l1_opy_ = bstack1ll11ll1l1_opy_[size:]
    bstack1llll111l1_opy_.append(bstack1ll11ll1l1_opy_)
    return bstack1llll111l1_opy_
def bstack111ll11l111_opy_(message, bstack111l1lllll1_opy_=False):
    os.write(1, bytes(message, bstack1l1111_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪ᷄")))
    os.write(1, bytes(bstack1l1111_opy_ (u"ࠬࡢ࡮ࠨ᷅"), bstack1l1111_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬ᷆")))
    if bstack111l1lllll1_opy_:
        with open(bstack1l1111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠭ࡰ࠳࠴ࡽ࠲࠭᷇") + os.environ[bstack1l1111_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡍࡇࡓࡉࡇࡇࡣࡎࡊࠧ᷈")] + bstack1l1111_opy_ (u"ࠩ࠱ࡰࡴ࡭ࠧ᷉"), bstack1l1111_opy_ (u"ࠪࡥ᷊ࠬ")) as f:
            f.write(message + bstack1l1111_opy_ (u"ࠫࡡࡴࠧ᷋"))
def bstack1l1l1l111l1_opy_():
    return os.environ[bstack1l1111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨ᷌")].lower() == bstack1l1111_opy_ (u"࠭ࡴࡳࡷࡨࠫ᷍")
def bstack1111l11l1_opy_():
    return bstack11111l1l11_opy_().replace(tzinfo=None).isoformat() + bstack1l1111_opy_ (u"᷎࡛ࠧࠩ")
def bstack111l1l1l1ll_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack1l1111_opy_ (u"ࠨ࡜᷏ࠪ"))) - datetime.datetime.fromisoformat(start.rstrip(bstack1l1111_opy_ (u"ࠩ࡝᷐ࠫ")))).total_seconds() * 1000
def bstack111l1ll11l1_opy_(timestamp):
    return bstack111l1lll1ll_opy_(timestamp).isoformat() + bstack1l1111_opy_ (u"ࠪ࡞ࠬ᷑")
def bstack111ll11ll11_opy_(bstack111l11l11l1_opy_):
    date_format = bstack1l1111_opy_ (u"ࠫࠪ࡟ࠥ࡮ࠧࡧࠤࠪࡎ࠺ࠦࡏ࠽ࠩࡘ࠴ࠥࡧࠩ᷒")
    bstack111ll111l11_opy_ = datetime.datetime.strptime(bstack111l11l11l1_opy_, date_format)
    return bstack111ll111l11_opy_.isoformat() + bstack1l1111_opy_ (u"ࠬࡠࠧᷓ")
def bstack111ll1l11l1_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack1l1111_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᷔ")
    else:
        return bstack1l1111_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᷕ")
def bstack1l1111lll1_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack1l1111_opy_ (u"ࠨࡶࡵࡹࡪ࠭ᷖ")
def bstack111ll1ll1ll_opy_(val):
    return val.__str__().lower() == bstack1l1111_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨᷗ")
def error_handler(bstack1111lll1lll_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack1111lll1lll_opy_ as e:
                print(bstack1l1111_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡩࡹࡳࡩࡴࡪࡱࡱࠤࢀࢃࠠ࠮ࡀࠣࡿࢂࡀࠠࡼࡿࠥᷘ").format(func.__name__, bstack1111lll1lll_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack111l111l1ll_opy_(bstack111ll111ll1_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack111ll111ll1_opy_(cls, *args, **kwargs)
            except bstack1111lll1lll_opy_ as e:
                print(bstack1l1111_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡪࡺࡴࡣࡵ࡫ࡲࡲࠥࢁࡽࠡ࠯ࡁࠤࢀࢃ࠺ࠡࡽࢀࠦᷙ").format(bstack111ll111ll1_opy_.__name__, bstack1111lll1lll_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack111l111l1ll_opy_
    else:
        return decorator
def bstack1l111111l1_opy_(bstack1llll1l1lll_opy_):
    if os.getenv(bstack1l1111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨᷚ")) is not None:
        return bstack1l1111lll1_opy_(os.getenv(bstack1l1111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩᷛ")))
    if bstack1l1111_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫᷜ") in bstack1llll1l1lll_opy_ and bstack111ll1ll1ll_opy_(bstack1llll1l1lll_opy_[bstack1l1111_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᷝ")]):
        return False
    if bstack1l1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫᷞ") in bstack1llll1l1lll_opy_ and bstack111ll1ll1ll_opy_(bstack1llll1l1lll_opy_[bstack1l1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᷟ")]):
        return False
    return True
def bstack1llllll1l_opy_():
    try:
        from pytest_bdd import reporting
        bstack111l11111ll_opy_ = os.environ.get(bstack1l1111_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢ࡙ࡘࡋࡒࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠦᷠ"), None)
        return bstack111l11111ll_opy_ is None or bstack111l11111ll_opy_ == bstack1l1111_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠤᷡ")
    except Exception as e:
        return False
def bstack1l1l11l1_opy_(hub_url, CONFIG):
    if bstack11ll111l_opy_() <= version.parse(bstack1l1111_opy_ (u"࠭࠳࠯࠳࠶࠲࠵࠭ᷢ")):
        if hub_url:
            return bstack1l1111_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣᷣ") + hub_url + bstack1l1111_opy_ (u"ࠣ࠼࠻࠴࠴ࡽࡤ࠰ࡪࡸࡦࠧᷤ")
        return bstack111ll11l_opy_
    if hub_url:
        return bstack1l1111_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦᷥ") + hub_url + bstack1l1111_opy_ (u"ࠥ࠳ࡼࡪ࠯ࡩࡷࡥࠦᷦ")
    return bstack1l1l1l1ll1_opy_
def bstack111l1111111_opy_():
    return isinstance(os.getenv(bstack1l1111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔ࡞࡚ࡅࡔࡖࡢࡔࡑ࡛ࡇࡊࡐࠪᷧ")), str)
def bstack1l11l1l1l1_opy_(url):
    return urlparse(url).hostname
def bstack11ll1ll1_opy_(hostname):
    for bstack111ll1ll11_opy_ in bstack1ll111l1l_opy_:
        regex = re.compile(bstack111ll1ll11_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack111ll1l1l11_opy_(bstack111lll11lll_opy_, file_name, logger):
    bstack1l1llllll1_opy_ = os.path.join(os.path.expanduser(bstack1l1111_opy_ (u"ࠬࢄࠧᷨ")), bstack111lll11lll_opy_)
    try:
        if not os.path.exists(bstack1l1llllll1_opy_):
            os.makedirs(bstack1l1llllll1_opy_)
        file_path = os.path.join(os.path.expanduser(bstack1l1111_opy_ (u"࠭ࡾࠨᷩ")), bstack111lll11lll_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack1l1111_opy_ (u"ࠧࡸࠩᷪ")):
                pass
            with open(file_path, bstack1l1111_opy_ (u"ࠣࡹ࠮ࠦᷫ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack1l1l1111_opy_.format(str(e)))
def bstack111l1ll1l1l_opy_(file_name, key, value, logger):
    file_path = bstack111ll1l1l11_opy_(bstack1l1111_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩᷬ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack11l1l11lll_opy_ = json.load(open(file_path, bstack1l1111_opy_ (u"ࠪࡶࡧ࠭ᷭ")))
        else:
            bstack11l1l11lll_opy_ = {}
        bstack11l1l11lll_opy_[key] = value
        with open(file_path, bstack1l1111_opy_ (u"ࠦࡼ࠱ࠢᷮ")) as outfile:
            json.dump(bstack11l1l11lll_opy_, outfile)
def bstack11lllll1_opy_(file_name, logger):
    file_path = bstack111ll1l1l11_opy_(bstack1l1111_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬᷯ"), file_name, logger)
    bstack11l1l11lll_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack1l1111_opy_ (u"࠭ࡲࠨᷰ")) as bstack111ll1ll_opy_:
            bstack11l1l11lll_opy_ = json.load(bstack111ll1ll_opy_)
    return bstack11l1l11lll_opy_
def bstack1l111llll_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack1l1111_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡧࡩࡱ࡫ࡴࡪࡰࡪࠤ࡫࡯࡬ࡦ࠼ࠣࠫᷱ") + file_path + bstack1l1111_opy_ (u"ࠨࠢࠪᷲ") + str(e))
def bstack11ll111l_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack1l1111_opy_ (u"ࠤ࠿ࡒࡔ࡚ࡓࡆࡖࡁࠦᷳ")
def bstack111l1lll11_opy_(config):
    if bstack1l1111_opy_ (u"ࠪ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩᷴ") in config:
        del (config[bstack1l1111_opy_ (u"ࠫ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪ᷵")])
        return False
    if bstack11ll111l_opy_() < version.parse(bstack1l1111_opy_ (u"ࠬ࠹࠮࠵࠰࠳ࠫ᷶")):
        return False
    if bstack11ll111l_opy_() >= version.parse(bstack1l1111_opy_ (u"࠭࠴࠯࠳࠱࠹᷷ࠬ")):
        return True
    if bstack1l1111_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉ᷸ࠧ") in config and config[bstack1l1111_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨ᷹")] is False:
        return False
    else:
        return True
def bstack111ll1l1_opy_(args_list, bstack111lll111l1_opy_):
    index = -1
    for value in bstack111lll111l1_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
def bstack11l1lll111l_opy_(a, b):
  for k, v in b.items():
    if isinstance(v, dict) and k in a and isinstance(a[k], dict):
        bstack11l1lll111l_opy_(a[k], v)
    else:
        a[k] = v
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack1111lll11l_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack1111lll11l_opy_ = bstack1111lll11l_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack1l1111_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥ᷺ࠩ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack1l1111_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ᷻"), exception=exception)
    def bstack1llll1111l1_opy_(self):
        if self.result != bstack1l1111_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ᷼"):
            return None
        if isinstance(self.exception_type, str) and bstack1l1111_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮᷽ࠣ") in self.exception_type:
            return bstack1l1111_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢ᷾")
        return bstack1l1111_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲ᷿ࠣ")
    def bstack111l1lll11l_opy_(self):
        if self.result != bstack1l1111_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨḀ"):
            return None
        if self.bstack1111lll11l_opy_:
            return self.bstack1111lll11l_opy_
        return bstack1111lllll1l_opy_(self.exception)
def bstack1111lllll1l_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack1111llll1ll_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack111111lll_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack11111ll1_opy_(config, logger):
    try:
        import playwright
        bstack111lll1ll11_opy_ = playwright.__file__
        bstack111l1l1llll_opy_ = os.path.split(bstack111lll1ll11_opy_)
        bstack111l1l11111_opy_ = bstack111l1l1llll_opy_[0] + bstack1l1111_opy_ (u"ࠩ࠲ࡨࡷ࡯ࡶࡦࡴ࠲ࡴࡦࡩ࡫ࡢࡩࡨ࠳ࡱ࡯ࡢ࠰ࡥ࡯࡭࠴ࡩ࡬ࡪ࠰࡭ࡷࠬḁ")
        os.environ[bstack1l1111_opy_ (u"ࠪࡋࡑࡕࡂࡂࡎࡢࡅࡌࡋࡎࡕࡡࡋࡘ࡙ࡖ࡟ࡑࡔࡒ࡜࡞࠭Ḃ")] = bstack1ll1l1l1_opy_(config)
        with open(bstack111l1l11111_opy_, bstack1l1111_opy_ (u"ࠫࡷ࠭ḃ")) as f:
            bstack1l111l1l1_opy_ = f.read()
            bstack111l1l1ll1l_opy_ = bstack1l1111_opy_ (u"ࠬ࡭࡬ࡰࡤࡤࡰ࠲ࡧࡧࡦࡰࡷࠫḄ")
            bstack111l11ll11l_opy_ = bstack1l111l1l1_opy_.find(bstack111l1l1ll1l_opy_)
            if bstack111l11ll11l_opy_ == -1:
              process = subprocess.Popen(bstack1l1111_opy_ (u"ࠨ࡮ࡱ࡯ࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤ࡬ࡲ࡯ࡣࡣ࡯࠱ࡦ࡭ࡥ࡯ࡶࠥḅ"), shell=True, cwd=bstack111l1l1llll_opy_[0])
              process.wait()
              bstack111l11lllll_opy_ = bstack1l1111_opy_ (u"ࠧࠣࡷࡶࡩࠥࡹࡴࡳ࡫ࡦࡸࠧࡁࠧḆ")
              bstack111lll1l1l1_opy_ = bstack1l1111_opy_ (u"ࠣࠤࠥࠤࡡࠨࡵࡴࡧࠣࡷࡹࡸࡩࡤࡶ࡟ࠦࡀࠦࡣࡰࡰࡶࡸࠥࢁࠠࡣࡱࡲࡸࡸࡺࡲࡢࡲࠣࢁࠥࡃࠠࡳࡧࡴࡹ࡮ࡸࡥࠩࠩࡪࡰࡴࡨࡡ࡭࠯ࡤ࡫ࡪࡴࡴࠨࠫ࠾ࠤ࡮࡬ࠠࠩࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡨࡲࡻ࠴ࡇࡍࡑࡅࡅࡑࡥࡁࡈࡇࡑࡘࡤࡎࡔࡕࡒࡢࡔࡗࡕࡘ࡚ࠫࠣࡦࡴࡵࡴࡴࡶࡵࡥࡵ࠮ࠩ࠼ࠢࠥࠦࠧḇ")
              bstack111l1ll1ll1_opy_ = bstack1l111l1l1_opy_.replace(bstack111l11lllll_opy_, bstack111lll1l1l1_opy_)
              with open(bstack111l1l11111_opy_, bstack1l1111_opy_ (u"ࠩࡺࠫḈ")) as f:
                f.write(bstack111l1ll1ll1_opy_)
    except Exception as e:
        logger.error(bstack111111111_opy_.format(str(e)))
def bstack1111lll1l_opy_():
  try:
    bstack111l111l11l_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1111_opy_ (u"ࠪࡳࡵࡺࡩ࡮ࡣ࡯ࡣ࡭ࡻࡢࡠࡷࡵࡰ࠳ࡰࡳࡰࡰࠪḉ"))
    bstack111ll111lll_opy_ = []
    if os.path.exists(bstack111l111l11l_opy_):
      with open(bstack111l111l11l_opy_) as f:
        bstack111ll111lll_opy_ = json.load(f)
      os.remove(bstack111l111l11l_opy_)
    return bstack111ll111lll_opy_
  except:
    pass
  return []
def bstack1l1lllll1_opy_(bstack1ll1ll1l11_opy_):
  try:
    bstack111ll111lll_opy_ = []
    bstack111l111l11l_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1111_opy_ (u"ࠫࡴࡶࡴࡪ࡯ࡤࡰࡤ࡮ࡵࡣࡡࡸࡶࡱ࠴ࡪࡴࡱࡱࠫḊ"))
    if os.path.exists(bstack111l111l11l_opy_):
      with open(bstack111l111l11l_opy_) as f:
        bstack111ll111lll_opy_ = json.load(f)
    bstack111ll111lll_opy_.append(bstack1ll1ll1l11_opy_)
    with open(bstack111l111l11l_opy_, bstack1l1111_opy_ (u"ࠬࡽࠧḋ")) as f:
        json.dump(bstack111ll111lll_opy_, f)
  except:
    pass
def bstack11lll11l11_opy_(logger, bstack111lll11ll1_opy_ = False):
  try:
    test_name = os.environ.get(bstack1l1111_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙ࡥࡔࡆࡕࡗࡣࡓࡇࡍࡆࠩḌ"), bstack1l1111_opy_ (u"ࠧࠨḍ"))
    if test_name == bstack1l1111_opy_ (u"ࠨࠩḎ"):
        test_name = threading.current_thread().__dict__.get(bstack1l1111_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡄࡧࡨࡤࡺࡥࡴࡶࡢࡲࡦࡳࡥࠨḏ"), bstack1l1111_opy_ (u"ࠪࠫḐ"))
    bstack1111lllllll_opy_ = bstack1l1111_opy_ (u"ࠫ࠱ࠦࠧḑ").join(threading.current_thread().bstackTestErrorMessages)
    if bstack111lll11ll1_opy_:
        bstack11llll11l1_opy_ = os.environ.get(bstack1l1111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬḒ"), bstack1l1111_opy_ (u"࠭࠰ࠨḓ"))
        bstack1ll1l1ll_opy_ = {bstack1l1111_opy_ (u"ࠧ࡯ࡣࡰࡩࠬḔ"): test_name, bstack1l1111_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧḕ"): bstack1111lllllll_opy_, bstack1l1111_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨḖ"): bstack11llll11l1_opy_}
        bstack111l1ll111l_opy_ = []
        bstack111ll1ll11l_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1111_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡴࡵࡶ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷ࠲࡯ࡹ࡯࡯ࠩḗ"))
        if os.path.exists(bstack111ll1ll11l_opy_):
            with open(bstack111ll1ll11l_opy_) as f:
                bstack111l1ll111l_opy_ = json.load(f)
        bstack111l1ll111l_opy_.append(bstack1ll1l1ll_opy_)
        with open(bstack111ll1ll11l_opy_, bstack1l1111_opy_ (u"ࠫࡼ࠭Ḙ")) as f:
            json.dump(bstack111l1ll111l_opy_, f)
    else:
        bstack1ll1l1ll_opy_ = {bstack1l1111_opy_ (u"ࠬࡴࡡ࡮ࡧࠪḙ"): test_name, bstack1l1111_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬḚ"): bstack1111lllllll_opy_, bstack1l1111_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭ḛ"): str(multiprocessing.current_process().name)}
        if bstack1l1111_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸࠬḜ") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack1ll1l1ll_opy_)
  except Exception as e:
      logger.warn(bstack1l1111_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡴࡰࡴࡨࠤࡵࡿࡴࡦࡵࡷࠤ࡫ࡻ࡮࡯ࡧ࡯ࠤࡩࡧࡴࡢ࠼ࠣࡿࢂࠨḝ").format(e))
def bstack1l1111l111_opy_(error_message, test_name, index, logger):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack1l1111_opy_ (u"ࠪࡪ࡮ࡲࡥ࡭ࡱࡦ࡯ࠥࡴ࡯ࡵࠢࡤࡺࡦ࡯࡬ࡢࡤ࡯ࡩ࠱ࠦࡵࡴ࡫ࡱ࡫ࠥࡨࡡࡴ࡫ࡦࠤ࡫࡯࡬ࡦࠢࡲࡴࡪࡸࡡࡵ࡫ࡲࡲࡸ࠭Ḟ"))
    try:
      bstack111lll1ll1l_opy_ = []
      bstack1ll1l1ll_opy_ = {bstack1l1111_opy_ (u"ࠫࡳࡧ࡭ࡦࠩḟ"): test_name, bstack1l1111_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫḠ"): error_message, bstack1l1111_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬḡ"): index}
      bstack111l1ll11ll_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1111_opy_ (u"ࠧࡳࡱࡥࡳࡹࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶ࠱࡮ࡸࡵ࡮ࠨḢ"))
      if os.path.exists(bstack111l1ll11ll_opy_):
          with open(bstack111l1ll11ll_opy_) as f:
              bstack111lll1ll1l_opy_ = json.load(f)
      bstack111lll1ll1l_opy_.append(bstack1ll1l1ll_opy_)
      with open(bstack111l1ll11ll_opy_, bstack1l1111_opy_ (u"ࠨࡹࠪḣ")) as f:
          json.dump(bstack111lll1ll1l_opy_, f)
    except Exception as e:
      logger.warn(bstack1l1111_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡴࡰࡴࡨࠤࡷࡵࡢࡰࡶࠣࡪࡺࡴ࡮ࡦ࡮ࠣࡨࡦࡺࡡ࠻ࠢࡾࢁࠧḤ").format(e))
    return
  bstack111lll1ll1l_opy_ = []
  bstack1ll1l1ll_opy_ = {bstack1l1111_opy_ (u"ࠪࡲࡦࡳࡥࠨḥ"): test_name, bstack1l1111_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪḦ"): error_message, bstack1l1111_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫḧ"): index}
  bstack111l1ll11ll_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1111_opy_ (u"࠭ࡲࡰࡤࡲࡸࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧḨ"))
  lock_file = bstack111l1ll11ll_opy_ + bstack1l1111_opy_ (u"ࠧ࠯࡮ࡲࡧࡰ࠭ḩ")
  try:
    with FileLock(lock_file, timeout=10):
      if os.path.exists(bstack111l1ll11ll_opy_):
          with open(bstack111l1ll11ll_opy_, bstack1l1111_opy_ (u"ࠨࡴࠪḪ")) as f:
              content = f.read().strip()
              if content:
                  bstack111lll1ll1l_opy_ = json.load(open(bstack111l1ll11ll_opy_))
      bstack111lll1ll1l_opy_.append(bstack1ll1l1ll_opy_)
      with open(bstack111l1ll11ll_opy_, bstack1l1111_opy_ (u"ࠩࡺࠫḫ")) as f:
          json.dump(bstack111lll1ll1l_opy_, f)
  except Exception as e:
    logger.warn(bstack1l1111_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡱࡵࡩࠥࡸ࡯ࡣࡱࡷࠤ࡫ࡻ࡮࡯ࡧ࡯ࠤࡩࡧࡴࡢࠢࡺ࡭ࡹ࡮ࠠࡧ࡫࡯ࡩࠥࡲ࡯ࡤ࡭࡬ࡲ࡬ࡀࠠࡼࡿࠥḬ").format(e))
def bstack1llllll111_opy_(bstack1l11111l1l_opy_, name, logger):
  try:
    bstack1ll1l1ll_opy_ = {bstack1l1111_opy_ (u"ࠫࡳࡧ࡭ࡦࠩḭ"): name, bstack1l1111_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫḮ"): bstack1l11111l1l_opy_, bstack1l1111_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬḯ"): str(threading.current_thread()._name)}
    return bstack1ll1l1ll_opy_
  except Exception as e:
    logger.warn(bstack1l1111_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡹࡵࡲࡦࠢࡥࡩ࡭ࡧࡶࡦࠢࡩࡹࡳࡴࡥ࡭ࠢࡧࡥࡹࡧ࠺ࠡࡽࢀࠦḰ").format(e))
  return
def bstack111lll11111_opy_():
    return platform.system() == bstack1l1111_opy_ (u"ࠨ࡙࡬ࡲࡩࡵࡷࡴࠩḱ")
def bstack11l111111_opy_(bstack111l111l1l1_opy_, config, logger):
    bstack111l1l1111l_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack111l111l1l1_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack1l1111_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥ࡬ࡩ࡭ࡶࡨࡶࠥࡩ࡯࡯ࡨ࡬࡫ࠥࡱࡥࡺࡵࠣࡦࡾࠦࡲࡦࡩࡨࡼࠥࡳࡡࡵࡥ࡫࠾ࠥࢁࡽࠣḲ").format(e))
    return bstack111l1l1111l_opy_
def bstack111ll11l1l1_opy_(bstack111ll1111l1_opy_, bstack111ll1l1ll1_opy_):
    bstack111l1111l1l_opy_ = version.parse(bstack111ll1111l1_opy_)
    bstack111lll1l11l_opy_ = version.parse(bstack111ll1l1ll1_opy_)
    if bstack111l1111l1l_opy_ > bstack111lll1l11l_opy_:
        return 1
    elif bstack111l1111l1l_opy_ < bstack111lll1l11l_opy_:
        return -1
    else:
        return 0
def bstack11111l1l11_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack111l1lll1ll_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
def bstack1111lll1ll1_opy_(framework):
    from browserstack_sdk._version import __version__
    return str(framework) + str(__version__)
def bstack1l1lll11_opy_(options, framework, config, bstack1l1111lll_opy_={}):
    if options is None:
        return
    if getattr(options, bstack1l1111_opy_ (u"ࠪ࡫ࡪࡺࠧḳ"), None):
        caps = options
    else:
        caps = options.to_capabilities()
    bstack11lll111ll_opy_ = caps.get(bstack1l1111_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬḴ"))
    bstack111l11llll1_opy_ = True
    bstack1llllll1l1_opy_ = os.environ[bstack1l1111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪḵ")]
    bstack1l1ll11l111_opy_ = config.get(bstack1l1111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭Ḷ"), False)
    if bstack1l1ll11l111_opy_:
        bstack1ll11l11l1l_opy_ = config.get(bstack1l1111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧḷ"), {})
        bstack1ll11l11l1l_opy_[bstack1l1111_opy_ (u"ࠨࡣࡸࡸ࡭࡚࡯࡬ࡧࡱࠫḸ")] = os.getenv(bstack1l1111_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧḹ"))
        bstack11l1l11lll1_opy_ = json.loads(os.getenv(bstack1l1111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫḺ"), bstack1l1111_opy_ (u"ࠫࢀࢃࠧḻ"))).get(bstack1l1111_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭Ḽ"))
    if bstack111ll1ll1ll_opy_(caps.get(bstack1l1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡻࡳࡦ࡙࠶ࡇࠬḽ"))) or bstack111ll1ll1ll_opy_(caps.get(bstack1l1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡵࡴࡧࡢࡻ࠸ࡩࠧḾ"))):
        bstack111l11llll1_opy_ = False
    if bstack111l1lll11_opy_({bstack1l1111_opy_ (u"ࠣࡷࡶࡩ࡜࠹ࡃࠣḿ"): bstack111l11llll1_opy_}):
        bstack11lll111ll_opy_ = bstack11lll111ll_opy_ or {}
        bstack11lll111ll_opy_[bstack1l1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫṀ")] = bstack1111lll1ll1_opy_(framework)
        bstack11lll111ll_opy_[bstack1l1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬṁ")] = bstack1l1l1l111l1_opy_()
        bstack11lll111ll_opy_[bstack1l1111_opy_ (u"ࠫࡹ࡫ࡳࡵࡪࡸࡦࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧṂ")] = bstack1llllll1l1_opy_
        bstack11lll111ll_opy_[bstack1l1111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡔࡷࡵࡤࡶࡥࡷࡑࡦࡶࠧṃ")] = bstack1l1111lll_opy_
        if bstack1l1ll11l111_opy_:
            bstack11lll111ll_opy_[bstack1l1111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭Ṅ")] = bstack1l1ll11l111_opy_
            bstack11lll111ll_opy_[bstack1l1111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧṅ")] = bstack1ll11l11l1l_opy_
            bstack11lll111ll_opy_[bstack1l1111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨṆ")][bstack1l1111_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪṇ")] = bstack11l1l11lll1_opy_
        if getattr(options, bstack1l1111_opy_ (u"ࠪࡷࡪࡺ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶࡼࠫṈ"), None):
            options.set_capability(bstack1l1111_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬṉ"), bstack11lll111ll_opy_)
        else:
            options[bstack1l1111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭Ṋ")] = bstack11lll111ll_opy_
    else:
        if getattr(options, bstack1l1111_opy_ (u"࠭ࡳࡦࡶࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹࡿࠧṋ"), None):
            options.set_capability(bstack1l1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨṌ"), bstack1111lll1ll1_opy_(framework))
            options.set_capability(bstack1l1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩṍ"), bstack1l1l1l111l1_opy_())
            options.set_capability(bstack1l1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡶࡨࡷࡹ࡮ࡵࡣࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫṎ"), bstack1llllll1l1_opy_)
            options.set_capability(bstack1l1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫṏ"), bstack1l1111lll_opy_)
            if bstack1l1ll11l111_opy_:
                options.set_capability(bstack1l1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪṐ"), bstack1l1ll11l111_opy_)
                options.set_capability(bstack1l1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫṑ"), bstack1ll11l11l1l_opy_)
                options.set_capability(bstack1l1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷ࠳ࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭Ṓ"), bstack11l1l11lll1_opy_)
        else:
            options[bstack1l1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨṓ")] = bstack1111lll1ll1_opy_(framework)
            options[bstack1l1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩṔ")] = bstack1l1l1l111l1_opy_()
            options[bstack1l1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡶࡨࡷࡹ࡮ࡵࡣࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫṕ")] = bstack1llllll1l1_opy_
            options[bstack1l1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫṖ")] = bstack1l1111lll_opy_
            if bstack1l1ll11l111_opy_:
                options[bstack1l1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪṗ")] = bstack1l1ll11l111_opy_
                options[bstack1l1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫṘ")] = bstack1ll11l11l1l_opy_
                options[bstack1l1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬṙ")][bstack1l1111_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨṚ")] = bstack11l1l11lll1_opy_
    return options
def bstack111lll11l1l_opy_(bstack111l11l1ll1_opy_, framework):
    bstack1l1111lll_opy_ = bstack1llllll11l_opy_.get_property(bstack1l1111_opy_ (u"ࠣࡒࡏࡅ࡞࡝ࡒࡊࡉࡋࡘࡤࡖࡒࡐࡆࡘࡇ࡙ࡥࡍࡂࡒࠥṛ"))
    if bstack111l11l1ll1_opy_ and len(bstack111l11l1ll1_opy_.split(bstack1l1111_opy_ (u"ࠩࡦࡥࡵࡹ࠽ࠨṜ"))) > 1:
        ws_url = bstack111l11l1ll1_opy_.split(bstack1l1111_opy_ (u"ࠪࡧࡦࡶࡳ࠾ࠩṝ"))[0]
        if bstack1l1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧṞ") in ws_url:
            from browserstack_sdk._version import __version__
            bstack111lll1l111_opy_ = json.loads(urllib.parse.unquote(bstack111l11l1ll1_opy_.split(bstack1l1111_opy_ (u"ࠬࡩࡡࡱࡵࡀࠫṟ"))[1]))
            bstack111lll1l111_opy_ = bstack111lll1l111_opy_ or {}
            bstack1llllll1l1_opy_ = os.environ[bstack1l1111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫṠ")]
            bstack111lll1l111_opy_[bstack1l1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨṡ")] = str(framework) + str(__version__)
            bstack111lll1l111_opy_[bstack1l1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩṢ")] = bstack1l1l1l111l1_opy_()
            bstack111lll1l111_opy_[bstack1l1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡶࡨࡷࡹ࡮ࡵࡣࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫṣ")] = bstack1llllll1l1_opy_
            bstack111lll1l111_opy_[bstack1l1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫṤ")] = bstack1l1111lll_opy_
            bstack111l11l1ll1_opy_ = bstack111l11l1ll1_opy_.split(bstack1l1111_opy_ (u"ࠫࡨࡧࡰࡴ࠿ࠪṥ"))[0] + bstack1l1111_opy_ (u"ࠬࡩࡡࡱࡵࡀࠫṦ") + urllib.parse.quote(json.dumps(bstack111lll1l111_opy_))
    return bstack111l11l1ll1_opy_
def bstack1l111lll1_opy_():
    global bstack1ll1ll111_opy_
    from playwright._impl._browser_type import BrowserType
    bstack1ll1ll111_opy_ = BrowserType.connect
    return bstack1ll1ll111_opy_
def bstack11lll1l111_opy_(framework_name):
    global bstack111l111l_opy_
    bstack111l111l_opy_ = framework_name
    return framework_name
def bstack1ll11111ll_opy_(self, *args, **kwargs):
    global bstack1ll1ll111_opy_
    try:
        global bstack111l111l_opy_
        if bstack1l1111_opy_ (u"࠭ࡷࡴࡇࡱࡨࡵࡵࡩ࡯ࡶࠪṧ") in kwargs:
            kwargs[bstack1l1111_opy_ (u"ࠧࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷࠫṨ")] = bstack111lll11l1l_opy_(
                kwargs.get(bstack1l1111_opy_ (u"ࠨࡹࡶࡉࡳࡪࡰࡰ࡫ࡱࡸࠬṩ"), None),
                bstack111l111l_opy_
            )
    except Exception as e:
        logger.error(bstack1l1111_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫ࡩࡳࠦࡰࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡗࡉࡑࠠࡤࡣࡳࡷ࠿ࠦࡻࡾࠤṪ").format(str(e)))
    return bstack1ll1ll111_opy_(self, *args, **kwargs)
def bstack111ll1l1111_opy_(bstack111l1l1ll11_opy_, proxies):
    proxy_settings = {}
    try:
        if not proxies:
            proxies = bstack1l11ll11l1_opy_(bstack111l1l1ll11_opy_, bstack1l1111_opy_ (u"ࠥࠦṫ"))
        if proxies and proxies.get(bstack1l1111_opy_ (u"ࠦ࡭ࡺࡴࡱࡵࠥṬ")):
            parsed_url = urlparse(proxies.get(bstack1l1111_opy_ (u"ࠧ࡮ࡴࡵࡲࡶࠦṭ")))
            if parsed_url and parsed_url.hostname: proxy_settings[bstack1l1111_opy_ (u"࠭ࡰࡳࡱࡻࡽࡍࡵࡳࡵࠩṮ")] = str(parsed_url.hostname)
            if parsed_url and parsed_url.port: proxy_settings[bstack1l1111_opy_ (u"ࠧࡱࡴࡲࡼࡾࡖ࡯ࡳࡶࠪṯ")] = str(parsed_url.port)
            if parsed_url and parsed_url.username: proxy_settings[bstack1l1111_opy_ (u"ࠨࡲࡵࡳࡽࡿࡕࡴࡧࡵࠫṰ")] = str(parsed_url.username)
            if parsed_url and parsed_url.password: proxy_settings[bstack1l1111_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡣࡶࡷࠬṱ")] = str(parsed_url.password)
        return proxy_settings
    except:
        return proxy_settings
def bstack11l1l1ll1_opy_(bstack111l1l1ll11_opy_):
    bstack111l11ll1l1_opy_ = {
        bstack11l111llll1_opy_[bstack111l1lll111_opy_]: bstack111l1l1ll11_opy_[bstack111l1lll111_opy_]
        for bstack111l1lll111_opy_ in bstack111l1l1ll11_opy_
        if bstack111l1lll111_opy_ in bstack11l111llll1_opy_
    }
    bstack111l11ll1l1_opy_[bstack1l1111_opy_ (u"ࠥࡴࡷࡵࡸࡺࡕࡨࡸࡹ࡯࡮ࡨࡵࠥṲ")] = bstack111ll1l1111_opy_(bstack111l1l1ll11_opy_, bstack1llllll11l_opy_.get_property(bstack1l1111_opy_ (u"ࠦࡵࡸ࡯ࡹࡻࡖࡩࡹࡺࡩ࡯ࡩࡶࠦṳ")))
    bstack111l1111ll1_opy_ = [element.lower() for element in bstack11l11111l1l_opy_]
    bstack1111llll111_opy_(bstack111l11ll1l1_opy_, bstack111l1111ll1_opy_)
    return bstack111l11ll1l1_opy_
def bstack1111llll111_opy_(d, keys):
    for key in list(d.keys()):
        if key.lower() in keys:
            d[key] = bstack1l1111_opy_ (u"ࠧ࠰ࠪࠫࠬࠥṴ")
    for value in d.values():
        if isinstance(value, dict):
            bstack1111llll111_opy_(value, keys)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    bstack1111llll111_opy_(item, keys)
def bstack1l1l1111l11_opy_():
    bstack111ll1llll1_opy_ = [os.environ.get(bstack1l1111_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡉࡍࡇࡖࡣࡉࡏࡒࠣṵ")), os.path.join(os.path.expanduser(bstack1l1111_opy_ (u"ࠢࡿࠤṶ")), bstack1l1111_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨṷ")), os.path.join(bstack1l1111_opy_ (u"ࠩ࠲ࡸࡲࡶࠧṸ"), bstack1l1111_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪṹ"))]
    for path in bstack111ll1llll1_opy_:
        if path is None:
            continue
        try:
            if os.path.exists(path):
                logger.debug(bstack1l1111_opy_ (u"ࠦࡋ࡯࡬ࡦࠢࠪࠦṺ") + str(path) + bstack1l1111_opy_ (u"ࠧ࠭ࠠࡦࡺ࡬ࡷࡹࡹ࠮ࠣṻ"))
                if not os.access(path, os.W_OK):
                    logger.debug(bstack1l1111_opy_ (u"ࠨࡇࡪࡸ࡬ࡲ࡬ࠦࡰࡦࡴࡰ࡭ࡸࡹࡩࡰࡰࡶࠤ࡫ࡵࡲࠡࠩࠥṼ") + str(path) + bstack1l1111_opy_ (u"ࠢࠨࠤṽ"))
                    os.chmod(path, 0o777)
                else:
                    logger.debug(bstack1l1111_opy_ (u"ࠣࡈ࡬ࡰࡪࠦࠧࠣṾ") + str(path) + bstack1l1111_opy_ (u"ࠤࠪࠤࡦࡲࡲࡦࡣࡧࡽࠥ࡮ࡡࡴࠢࡷ࡬ࡪࠦࡲࡦࡳࡸ࡭ࡷ࡫ࡤࠡࡲࡨࡶࡲ࡯ࡳࡴ࡫ࡲࡲࡸ࠴ࠢṿ"))
            else:
                logger.debug(bstack1l1111_opy_ (u"ࠥࡇࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥ࡬ࡩ࡭ࡧࠣࠫࠧẀ") + str(path) + bstack1l1111_opy_ (u"ࠦࠬࠦࡷࡪࡶ࡫ࠤࡼࡸࡩࡵࡧࠣࡴࡪࡸ࡭ࡪࡵࡶ࡭ࡴࡴ࠮ࠣẁ"))
                os.makedirs(path, exist_ok=True)
                os.chmod(path, 0o777)
            logger.debug(bstack1l1111_opy_ (u"ࠧࡕࡰࡦࡴࡤࡸ࡮ࡵ࡮ࠡࡵࡸࡧࡨ࡫ࡥࡥࡧࡧࠤ࡫ࡵࡲࠡࠩࠥẂ") + str(path) + bstack1l1111_opy_ (u"ࠨࠧ࠯ࠤẃ"))
            return path
        except Exception as e:
            logger.debug(bstack1l1111_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࠠࡶࡲࠣࡪ࡮ࡲࡥࠡࠩࡾࡴࡦࡺࡨࡾࠩ࠽ࠤࠧẄ") + str(e) + bstack1l1111_opy_ (u"ࠣࠤẅ"))
    logger.debug(bstack1l1111_opy_ (u"ࠤࡄࡰࡱࠦࡰࡢࡶ࡫ࡷࠥ࡬ࡡࡪ࡮ࡨࡨ࠳ࠨẆ"))
    return None
@measure(event_name=EVENTS.bstack11l11l1l1l1_opy_, stage=STAGE.bstack1111lll11_opy_)
def bstack1ll111lllll_opy_(binary_path, bstack1ll1lllll1l_opy_, bs_config):
    logger.debug(bstack1l1111_opy_ (u"ࠥࡇࡺࡸࡲࡦࡰࡷࠤࡈࡒࡉࠡࡒࡤࡸ࡭ࠦࡦࡰࡷࡱࡨ࠿ࠦࡻࡾࠤẇ").format(binary_path))
    bstack111ll11lll1_opy_ = bstack1l1111_opy_ (u"ࠫࠬẈ")
    bstack1111llll1l1_opy_ = {
        bstack1l1111_opy_ (u"ࠬࡹࡤ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪẉ"): __version__,
        bstack1l1111_opy_ (u"ࠨ࡯ࡴࠤẊ"): platform.system(),
        bstack1l1111_opy_ (u"ࠢࡰࡵࡢࡥࡷࡩࡨࠣẋ"): platform.machine(),
        bstack1l1111_opy_ (u"ࠣࡥ࡯࡭ࡤࡼࡥࡳࡵ࡬ࡳࡳࠨẌ"): bstack1l1111_opy_ (u"ࠩ࠳ࠫẍ"),
        bstack1l1111_opy_ (u"ࠥࡷࡩࡱ࡟࡭ࡣࡱ࡫ࡺࡧࡧࡦࠤẎ"): bstack1l1111_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫẏ")
    }
    bstack111l111lll1_opy_(bstack1111llll1l1_opy_)
    try:
        if binary_path:
            if bstack111lll11111_opy_():
                bstack1111llll1l1_opy_[bstack1l1111_opy_ (u"ࠬࡩ࡬ࡪࡡࡹࡩࡷࡹࡩࡰࡰࠪẐ")] = subprocess.check_output([binary_path, bstack1l1111_opy_ (u"ࠨࡶࡦࡴࡶ࡭ࡴࡴࠢẑ")]).strip().decode(bstack1l1111_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭Ẓ"))
            else:
                bstack1111llll1l1_opy_[bstack1l1111_opy_ (u"ࠨࡥ࡯࡭ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ẓ")] = subprocess.check_output([binary_path, bstack1l1111_opy_ (u"ࠤࡹࡩࡷࡹࡩࡰࡰࠥẔ")], stderr=subprocess.DEVNULL).strip().decode(bstack1l1111_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩẕ"))
        response = requests.request(
            bstack1l1111_opy_ (u"ࠫࡌࡋࡔࠨẖ"),
            url=bstack111lll1l1_opy_(bstack11l11111ll1_opy_),
            headers=None,
            auth=(bs_config[bstack1l1111_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧẗ")], bs_config[bstack1l1111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩẘ")]),
            json=None,
            params=bstack1111llll1l1_opy_
        )
        data = response.json()
        if response.status_code == 200 and bstack1l1111_opy_ (u"ࠧࡶࡴ࡯ࠫẙ") in data.keys() and bstack1l1111_opy_ (u"ࠨࡷࡳࡨࡦࡺࡥࡥࡡࡦࡰ࡮ࡥࡶࡦࡴࡶ࡭ࡴࡴࠧẚ") in data.keys():
            logger.debug(bstack1l1111_opy_ (u"ࠤࡑࡩࡪࡪࠠࡵࡱࠣࡹࡵࡪࡡࡵࡧࠣࡦ࡮ࡴࡡࡳࡻ࠯ࠤࡨࡻࡲࡳࡧࡱࡸࠥࡨࡩ࡯ࡣࡵࡽࠥࡼࡥࡳࡵ࡬ࡳࡳࡀࠠࡼࡿࠥẛ").format(bstack1111llll1l1_opy_[bstack1l1111_opy_ (u"ࠪࡧࡱ࡯࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨẜ")]))
            if bstack1l1111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆࡎࡔࡁࡓ࡛ࡢ࡙ࡗࡒࠧẝ") in os.environ:
                logger.debug(bstack1l1111_opy_ (u"࡙ࠧ࡫ࡪࡲࡳ࡭ࡳ࡭ࠠࡣ࡫ࡱࡥࡷࡿࠠࡥࡱࡺࡲࡱࡵࡡࡥࠢࡤࡷࠥࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇࡏࡎࡂࡔ࡜ࡣ࡚ࡘࡌࠡ࡫ࡶࠤࡸ࡫ࡴࠣẞ"))
                data[bstack1l1111_opy_ (u"࠭ࡵࡳ࡮ࠪẟ")] = os.environ[bstack1l1111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡊࡐࡄࡖ࡞ࡥࡕࡓࡎࠪẠ")]
            bstack111l111l111_opy_ = bstack111l1l111l1_opy_(data[bstack1l1111_opy_ (u"ࠨࡷࡵࡰࠬạ")], bstack1ll1lllll1l_opy_)
            bstack111ll11lll1_opy_ = os.path.join(bstack1ll1lllll1l_opy_, bstack111l111l111_opy_)
            os.chmod(bstack111ll11lll1_opy_, 0o777) # bstack111ll111111_opy_ permission
            return bstack111ll11lll1_opy_
    except Exception as e:
        logger.debug(bstack1l1111_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡥࡱࡺࡲࡱࡵࡡࡥ࡫ࡱ࡫ࠥࡴࡥࡸࠢࡖࡈࡐࠦࡻࡾࠤẢ").format(e))
    return binary_path
def bstack111l111lll1_opy_(bstack1111llll1l1_opy_):
    try:
        if bstack1l1111_opy_ (u"ࠪࡰ࡮ࡴࡵࡹࠩả") not in bstack1111llll1l1_opy_[bstack1l1111_opy_ (u"ࠫࡴࡹࠧẤ")].lower():
            return
        if os.path.exists(bstack1l1111_opy_ (u"ࠧ࠵ࡥࡵࡥ࠲ࡳࡸ࠳ࡲࡦ࡮ࡨࡥࡸ࡫ࠢấ")):
            with open(bstack1l1111_opy_ (u"ࠨ࠯ࡦࡶࡦ࠳ࡴࡹ࠭ࡳࡧ࡯ࡩࡦࡹࡥࠣẦ"), bstack1l1111_opy_ (u"ࠢࡳࠤầ")) as f:
                bstack111ll1ll111_opy_ = {}
                for line in f:
                    if bstack1l1111_opy_ (u"ࠣ࠿ࠥẨ") in line:
                        key, value = line.rstrip().split(bstack1l1111_opy_ (u"ࠤࡀࠦẩ"), 1)
                        bstack111ll1ll111_opy_[key] = value.strip(bstack1l1111_opy_ (u"ࠪࠦࡡ࠭ࠧẪ"))
                bstack1111llll1l1_opy_[bstack1l1111_opy_ (u"ࠫࡩ࡯ࡳࡵࡴࡲࠫẫ")] = bstack111ll1ll111_opy_.get(bstack1l1111_opy_ (u"ࠧࡏࡄࠣẬ"), bstack1l1111_opy_ (u"ࠨࠢậ"))
        elif os.path.exists(bstack1l1111_opy_ (u"ࠢ࠰ࡧࡷࡧ࠴ࡧ࡬ࡱ࡫ࡱࡩ࠲ࡸࡥ࡭ࡧࡤࡷࡪࠨẮ")):
            bstack1111llll1l1_opy_[bstack1l1111_opy_ (u"ࠨࡦ࡬ࡷࡹࡸ࡯ࠨắ")] = bstack1l1111_opy_ (u"ࠩࡤࡰࡵ࡯࡮ࡦࠩẰ")
    except Exception as e:
        logger.debug(bstack1l1111_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡧࡦࡶࠣࡨ࡮ࡹࡴࡳࡱࠣࡳ࡫ࠦ࡬ࡪࡰࡸࡼࠧằ") + e)
@measure(event_name=EVENTS.bstack11l1111lll1_opy_, stage=STAGE.bstack1111lll11_opy_)
def bstack111l1l111l1_opy_(bstack111l111ll11_opy_, bstack111l1ll1111_opy_):
    logger.debug(bstack1l1111_opy_ (u"ࠦࡉࡵࡷ࡯࡮ࡲࡥࡩ࡯࡮ࡨࠢࡖࡈࡐࠦࡢࡪࡰࡤࡶࡾࠦࡦࡳࡱࡰ࠾ࠥࠨẲ") + str(bstack111l111ll11_opy_) + bstack1l1111_opy_ (u"ࠧࠨẳ"))
    zip_path = os.path.join(bstack111l1ll1111_opy_, bstack1l1111_opy_ (u"ࠨࡤࡰࡹࡱࡰࡴࡧࡤࡦࡦࡢࡪ࡮ࡲࡥ࠯ࡼ࡬ࡴࠧẴ"))
    bstack111l111l111_opy_ = bstack1l1111_opy_ (u"ࠧࠨẵ")
    with requests.get(bstack111l111ll11_opy_, stream=True) as response:
        response.raise_for_status()
        with open(zip_path, bstack1l1111_opy_ (u"ࠣࡹࡥࠦẶ")) as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        logger.debug(bstack1l1111_opy_ (u"ࠤࡉ࡭ࡱ࡫ࠠࡥࡱࡺࡲࡱࡵࡡࡥࡧࡧࠤࡸࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬࡭ࡻ࠱ࠦặ"))
    with zipfile.ZipFile(zip_path, bstack1l1111_opy_ (u"ࠪࡶࠬẸ")) as zip_ref:
        bstack111l111111l_opy_ = zip_ref.namelist()
        if len(bstack111l111111l_opy_) > 0:
            bstack111l111l111_opy_ = bstack111l111111l_opy_[0] # bstack111l111ll1l_opy_ bstack11l11l1l11l_opy_ will be bstack111l1ll1l11_opy_ 1 file i.e. the binary in the zip
        zip_ref.extractall(bstack111l1ll1111_opy_)
        logger.debug(bstack1l1111_opy_ (u"ࠦࡋ࡯࡬ࡦࡵࠣࡷࡺࡩࡣࡦࡵࡶࡪࡺࡲ࡬ࡺࠢࡨࡼࡹࡸࡡࡤࡶࡨࡨࠥࡺ࡯ࠡࠩࠥẹ") + str(bstack111l1ll1111_opy_) + bstack1l1111_opy_ (u"ࠧ࠭ࠢẺ"))
    os.remove(zip_path)
    return bstack111l111l111_opy_
def get_cli_dir():
    bstack1111llll11l_opy_ = bstack1l1l1111l11_opy_()
    if bstack1111llll11l_opy_:
        bstack1ll1lllll1l_opy_ = os.path.join(bstack1111llll11l_opy_, bstack1l1111_opy_ (u"ࠨࡣ࡭࡫ࠥẻ"))
        if not os.path.exists(bstack1ll1lllll1l_opy_):
            os.makedirs(bstack1ll1lllll1l_opy_, mode=0o777, exist_ok=True)
        return bstack1ll1lllll1l_opy_
    else:
        raise FileNotFoundError(bstack1l1111_opy_ (u"ࠢࡏࡱࠣࡻࡷ࡯ࡴࡢࡤ࡯ࡩࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡࡣࡹࡥ࡮ࡲࡡࡣ࡮ࡨࠤ࡫ࡵࡲࠡࡶ࡫ࡩ࡙ࠥࡄࡌࠢࡥ࡭ࡳࡧࡲࡺ࠰ࠥẼ"))
def bstack1ll11lll11l_opy_(bstack1ll1lllll1l_opy_):
    bstack1l1111_opy_ (u"ࠣࠤࠥࡋࡪࡺࠠࡵࡪࡨࠤࡵࡧࡴࡩࠢࡩࡳࡷࠦࡴࡩࡧࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡖࡈࡐࠦࡢࡪࡰࡤࡶࡾࠦࡩ࡯ࠢࡤࠤࡼࡸࡩࡵࡣࡥࡰࡪࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺ࠰ࠥࠦࠧẽ")
    bstack111ll111l1l_opy_ = [
        os.path.join(bstack1ll1lllll1l_opy_, f)
        for f in os.listdir(bstack1ll1lllll1l_opy_)
        if os.path.isfile(os.path.join(bstack1ll1lllll1l_opy_, f)) and f.startswith(bstack1l1111_opy_ (u"ࠤࡥ࡭ࡳࡧࡲࡺ࠯ࠥẾ"))
    ]
    if len(bstack111ll111l1l_opy_) > 0:
        return max(bstack111ll111l1l_opy_, key=os.path.getmtime) # get bstack111l1ll1lll_opy_ binary
    return bstack1l1111_opy_ (u"ࠥࠦế")
def bstack11l1l1ll1l1_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1l1lll111l1_opy_(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = bstack1l1lll111l1_opy_(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack11ll1l11_opy_(data, keys, default=None):
    bstack1l1111_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࡘࡧࡦࡦ࡮ࡼࠤ࡬࡫ࡴࠡࡣࠣࡲࡪࡹࡴࡦࡦࠣࡺࡦࡲࡵࡦࠢࡩࡶࡴࡳࠠࡢࠢࡧ࡭ࡨࡺࡩࡰࡰࡤࡶࡾࠦ࡯ࡳࠢ࡯࡭ࡸࡺ࠮ࠋࠢࠣࠤࠥࡀࡰࡢࡴࡤࡱࠥࡪࡡࡵࡣ࠽ࠤ࡙࡮ࡥࠡࡦ࡬ࡧࡹ࡯࡯࡯ࡣࡵࡽࠥࡵࡲࠡ࡮࡬ࡷࡹࠦࡴࡰࠢࡷࡶࡦࡼࡥࡳࡵࡨ࠲ࠏࠦࠠࠡࠢ࠽ࡴࡦࡸࡡ࡮ࠢ࡮ࡩࡾࡹ࠺ࠡࡃࠣࡰ࡮ࡹࡴࠡࡱࡩࠤࡰ࡫ࡹࡴ࠱࡬ࡲࡩ࡯ࡣࡦࡵࠣࡶࡪࡶࡲࡦࡵࡨࡲࡹ࡯࡮ࡨࠢࡷ࡬ࡪࠦࡰࡢࡶ࡫࠲ࠏࠦࠠࠡࠢ࠽ࡴࡦࡸࡡ࡮ࠢࡧࡩ࡫ࡧࡵ࡭ࡶ࠽ࠤ࡛ࡧ࡬ࡶࡧࠣࡸࡴࠦࡲࡦࡶࡸࡶࡳࠦࡩࡧࠢࡷ࡬ࡪࠦࡰࡢࡶ࡫ࠤࡩࡵࡥࡴࠢࡱࡳࡹࠦࡥࡹ࡫ࡶࡸ࠳ࠐࠠࠡࠢࠣ࠾ࡷ࡫ࡴࡶࡴࡱ࠾࡚ࠥࡨࡦࠢࡹࡥࡱࡻࡥࠡࡣࡷࠤࡹ࡮ࡥࠡࡰࡨࡷࡹ࡫ࡤࠡࡲࡤࡸ࡭࠲ࠠࡰࡴࠣࡨࡪ࡬ࡡࡶ࡮ࡷࠤ࡮࡬ࠠ࡯ࡱࡷࠤ࡫ࡵࡵ࡯ࡦ࠱ࠎࠥࠦࠠࠡࠤࠥࠦỀ")
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
def bstack111l11ll_opy_(bstack111l11lll11_opy_, key, value):
    bstack1l1111_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤ࡙ࠥࡴࡰࡴࡨࠤࡈࡒࡉࠡࡧࡱࡺ࡮ࡸ࡯࡯࡯ࡨࡲࡹࠦࡶࡢࡴ࡬ࡥࡧࡲࡥࡴࠢࡰࡥࡵࡶࡩ࡯ࡩࠣ࡭ࡳࠦࡴࡩࡧࠣࡴࡷࡵࡶࡪࡦࡨࡨࠥࡪࡩࡤࡶ࡬ࡳࡳࡧࡲࡺ࠰ࠍࠤࠥࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡤ࡮࡬ࡣࡪࡴࡶࡠࡸࡤࡶࡸࡥ࡭ࡢࡲ࠽ࠤࡉ࡯ࡣࡵ࡫ࡲࡲࡦࡸࡹࠡࡶࡲࠤࡸࡺ࡯ࡳࡧࠣࡩࡳࡼࡩࡳࡱࡱࡱࡪࡴࡴࠡࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠣࡱࡦࡶࡰࡪࡰࡪࡷࠏࠦࠠࠡࠢࠣࠤࠥࠦ࡫ࡦࡻ࠽ࠤࡐ࡫ࡹࠡࡨࡵࡳࡲࠦࡃࡍࡋࡢࡇࡆࡖࡓࡠࡖࡒࡣࡈࡕࡎࡇࡋࡊࠎࠥࠦࠠࠡࠢࠣࠤࠥࡼࡡ࡭ࡷࡨ࠾ࠥ࡜ࡡ࡭ࡷࡨࠤ࡫ࡸ࡯࡮ࠢࡦࡳࡲࡳࡡ࡯ࡦࠣࡰ࡮ࡴࡥࠡࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠎࠥࠦࠠࠡࠤࠥࠦề")
    if key in bstack1l1lll1l1_opy_:
        bstack1l11lllll1_opy_ = bstack1l1lll1l1_opy_[key]
        if isinstance(bstack1l11lllll1_opy_, list):
            for env_name in bstack1l11lllll1_opy_:
                bstack111l11lll11_opy_[env_name] = value
        else:
            bstack111l11lll11_opy_[bstack1l11lllll1_opy_] = value