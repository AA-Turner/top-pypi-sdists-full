# coding: UTF-8
import sys
bstack11ll1l1_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack1ll1lll_opy_ = 7
def bstack11lllll_opy_ (bstack11ll1_opy_):
    global bstack1llllll_opy_
    bstack111l_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1111l11_opy_ = bstack11ll1_opy_ [:-1]
    bstack1lllll1l_opy_ = bstack111l_opy_ % len (bstack1111l11_opy_)
    bstack1ll1ll_opy_ = bstack1111l11_opy_ [:bstack1lllll1l_opy_] + bstack1111l11_opy_ [bstack1lllll1l_opy_:]
    if bstack11ll1l1_opy_:
        bstack1l1llll_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    else:
        bstack1l1llll_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    return eval (bstack1l1llll_opy_)
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
from bstack_utils.constants import (bstack1l1111l11_opy_, bstack11l11ll11l_opy_, bstack1ll1111l_opy_,
                                    bstack11l11l11111_opy_, bstack11l1111l11l_opy_, bstack111llllll11_opy_, bstack11l111lllll_opy_)
from bstack_utils.measure import measure
from bstack_utils.messages import bstack11l1llll_opy_, bstack1lllll11ll_opy_
from bstack_utils.proxy import bstack11l1l1111_opy_, bstack1l1l1l1ll1_opy_
from bstack_utils.constants import *
from bstack_utils import logger_utils
from bstack_utils.bstack11ll1l11_opy_ import bstack1l11l11ll_opy_
from browserstack_sdk._version import __version__
bstack1l111111_opy_ = Config.bstack1llll1l111_opy_()
logger = logger_utils.get_logger(__name__, logger_utils.bstack1ll1ll1l1l1_opy_())
bstack1l111l111l_opy_ = logger_utils.bstack1l1l11111l_opy_(__name__)
def bstack11l1l1ll111_opy_(config):
    return config[bstack11lllll_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨᱡ")]
def bstack11l1l1ll1ll_opy_(config):
    return config[bstack11lllll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪᱢ")]
def bstack111llll111_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack1111lll1111_opy_(obj):
    values = []
    bstack1111lll11l1_opy_ = re.compile(bstack11lllll_opy_ (u"ࡳࠤࡡࡇ࡚࡙ࡔࡐࡏࡢࡘࡆࡍ࡟࡝ࡦ࠮ࠨࠧᱣ"), re.I)
    for key in obj.keys():
        if bstack1111lll11l1_opy_.match(key):
            values.append(obj[key])
    return values
def bstack111l1l111l1_opy_(config):
    tags = []
    tags.extend(bstack1111lll1111_opy_(os.environ))
    tags.extend(bstack1111lll1111_opy_(config))
    return tags
def bstack111ll11ll11_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack111l1l11lll_opy_(bstack1111ll1lll1_opy_):
    if not bstack1111ll1lll1_opy_:
        return bstack11lllll_opy_ (u"ࠩࠪᱤ")
    return bstack11lllll_opy_ (u"ࠥࡿࢂࠦࠨࡼࡿࠬࠦᱥ").format(bstack1111ll1lll1_opy_.name, bstack1111ll1lll1_opy_.email)
def bstack11l1l1l1ll1_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack111l11llll1_opy_ = repo.common_dir
        info = {
            bstack11lllll_opy_ (u"ࠦࡸ࡮ࡡࠣᱦ"): repo.head.commit.hexsha,
            bstack11lllll_opy_ (u"ࠧࡹࡨࡰࡴࡷࡣࡸ࡮ࡡࠣᱧ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack11lllll_opy_ (u"ࠨࡢࡳࡣࡱࡧ࡭ࠨᱨ"): repo.active_branch.name,
            bstack11lllll_opy_ (u"ࠢࡵࡣࡪࠦᱩ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack11lllll_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡵࡧࡵࠦᱪ"): bstack111l1l11lll_opy_(repo.head.commit.committer),
            bstack11lllll_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡶࡨࡶࡤࡪࡡࡵࡧࠥᱫ"): repo.head.commit.committed_datetime.isoformat(),
            bstack11lllll_opy_ (u"ࠥࡥࡺࡺࡨࡰࡴࠥᱬ"): bstack111l1l11lll_opy_(repo.head.commit.author),
            bstack11lllll_opy_ (u"ࠦࡦࡻࡴࡩࡱࡵࡣࡩࡧࡴࡦࠤᱭ"): repo.head.commit.authored_datetime.isoformat(),
            bstack11lllll_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡤࡳࡥࡴࡵࡤ࡫ࡪࠨᱮ"): repo.head.commit.message,
            bstack11lllll_opy_ (u"ࠨࡲࡰࡱࡷࠦᱯ"): repo.git.rev_parse(bstack11lllll_opy_ (u"ࠢ࠮࠯ࡶ࡬ࡴࡽ࠭ࡵࡱࡳࡰࡪࡼࡥ࡭ࠤᱰ")),
            bstack11lllll_opy_ (u"ࠣࡥࡲࡱࡲࡵ࡮ࡠࡩ࡬ࡸࡤࡪࡩࡳࠤᱱ"): bstack111l11llll1_opy_,
            bstack11lllll_opy_ (u"ࠤࡺࡳࡷࡱࡴࡳࡧࡨࡣ࡬࡯ࡴࡠࡦ࡬ࡶࠧᱲ"): subprocess.check_output([bstack11lllll_opy_ (u"ࠥ࡫࡮ࡺࠢᱳ"), bstack11lllll_opy_ (u"ࠦࡷ࡫ࡶ࠮ࡲࡤࡶࡸ࡫ࠢᱴ"), bstack11lllll_opy_ (u"ࠧ࠳࠭ࡨ࡫ࡷ࠱ࡨࡵ࡭࡮ࡱࡱ࠱ࡩ࡯ࡲࠣᱵ")]).strip().decode(
                bstack11lllll_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬᱶ")),
            bstack11lllll_opy_ (u"ࠢ࡭ࡣࡶࡸࡤࡺࡡࡨࠤᱷ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack11lllll_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡴࡡࡶ࡭ࡳࡩࡥࡠ࡮ࡤࡷࡹࡥࡴࡢࡩࠥᱸ"): repo.git.rev_list(
                bstack11lllll_opy_ (u"ࠤࡾࢁ࠳࠴ࡻࡾࠤᱹ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack111l1l1l111_opy_ = []
        for remote in remotes:
            bstack111ll11ll1l_opy_ = {
                bstack11lllll_opy_ (u"ࠥࡲࡦࡳࡥࠣᱺ"): remote.name,
                bstack11lllll_opy_ (u"ࠦࡺࡸ࡬ࠣᱻ"): remote.url,
            }
            bstack111l1l1l111_opy_.append(bstack111ll11ll1l_opy_)
        bstack111l1111l11_opy_ = {
            bstack11lllll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᱼ"): bstack11lllll_opy_ (u"ࠨࡧࡪࡶࠥᱽ"),
            **info,
            bstack11lllll_opy_ (u"ࠢࡳࡧࡰࡳࡹ࡫ࡳࠣ᱾"): bstack111l1l1l111_opy_
        }
        bstack111l1111l11_opy_ = bstack111l11ll1ll_opy_(bstack111l1111l11_opy_)
        return bstack111l1111l11_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack11lllll_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡱࡳࡹࡱࡧࡴࡪࡰࡪࠤࡌ࡯ࡴࠡ࡯ࡨࡸࡦࡪࡡࡵࡣࠣࡻ࡮ࡺࡨࠡࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠦ᱿").format(err))
        return {}
def bstack1111llll1l1_opy_(bstack1111lllll11_opy_=None):
    bstack11lllll_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࡊࡩࡹࠦࡧࡪࡶࠣࡱࡪࡺࡡࡥࡣࡷࡥࠥࡹࡰࡦࡥ࡬ࡪ࡮ࡩࡡ࡭࡮ࡼࠤ࡫ࡵࡲ࡮ࡣࡷࡸࡪࡪࠠࡧࡱࡵࠤࡆࡏࠠࡴࡧ࡯ࡩࡨࡺࡩࡰࡰࠣࡹࡸ࡫ࠠࡤࡣࡶࡩࡸࠦࡦࡰࡴࠣࡩࡦࡩࡨࠡࡨࡲࡰࡩ࡫ࡲࠡ࡫ࡱࠤࡹ࡮ࡥࠡ࡮࡬ࡷࡹ࠴ࠊࠡࠢࠣࠤࡆࡸࡧࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤ࡫ࡵ࡬ࡥࡧࡵࡷࠥ࠮࡬ࡪࡵࡷ࠰ࠥࡵࡰࡵ࡫ࡲࡲࡦࡲࠩ࠻ࠢࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡒࡴࡴࡥ࠻ࠢࡐࡳࡳࡵ࠭ࡳࡧࡳࡳࠥࡧࡰࡱࡴࡲࡥࡨ࡮ࠬࠡࡷࡶࡩࡸࠦࡣࡶࡴࡵࡩࡳࡺࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣ࡟ࡴࡹ࠮ࡨࡧࡷࡧࡼࡪࠨࠪ࡟ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡉࡲࡶࡴࡺࠢ࡯࡭ࡸࡺࠠ࡜࡟࠽ࠤࡒࡻ࡬ࡵ࡫࠰ࡶࡪࡶ࡯ࠡࡣࡳࡴࡷࡵࡡࡤࡪࠣࡻ࡮ࡺࡨࠡࡰࡲࠤࡸࡵࡵࡳࡥࡨࡷࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡥࡥ࠮ࠣࡶࡪࡺࡵࡳࡰࡶࠤࡠࡣࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡍ࡫ࡶࡸࠥࡵࡦࠡࡲࡤࡸ࡭ࡹ࠺ࠡࡏࡸࡰࡹ࡯࠭ࡳࡧࡳࡳࠥࡧࡰࡱࡴࡲࡥࡨ࡮ࠠࡸ࡫ࡷ࡬ࠥࡹࡰࡦࡥ࡬ࡪ࡮ࡩࠠࡧࡱ࡯ࡨࡪࡸࡳࠡࡶࡲࠤࡦࡴࡡ࡭ࡻࡽࡩࠏࠦࠠࠡࠢࡕࡩࡹࡻࡲ࡯ࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡲࡩࡴࡶ࠽ࠤࡑ࡯ࡳࡵࠢࡲࡪࠥࡪࡩࡤࡶࡶ࠰ࠥ࡫ࡡࡤࡪࠣࡧࡴࡴࡴࡢ࡫ࡱ࡭ࡳ࡭ࠠࡨ࡫ࡷࠤࡲ࡫ࡴࡢࡦࡤࡸࡦࠦࡦࡰࡴࠣࡥࠥ࡬࡯࡭ࡦࡨࡶ࠳ࠐࠠࠡࠢࠣࠦࠧࠨᲀ")
    if bstack1111lllll11_opy_ is None:
        bstack1111lllll11_opy_ = [os.getcwd()]
    elif isinstance(bstack1111lllll11_opy_, list) and len(bstack1111lllll11_opy_) == 0:
        return []
    results = []
    for folder in bstack1111lllll11_opy_:
        try:
            if not os.path.exists(folder):
                raise Exception(bstack11lllll_opy_ (u"ࠥࡊࡴࡲࡤࡦࡴࠣࡨࡴ࡫ࡳࠡࡰࡲࡸࠥ࡫ࡸࡪࡵࡷ࠾ࠥࢁࡽࠣᲁ").format(folder))
            repo = git.Repo(folder, search_parent_directories=True)
            result = {
                bstack11lllll_opy_ (u"ࠦࡵࡸࡉࡥࠤᲂ"): bstack11lllll_opy_ (u"ࠧࠨᲃ"),
                bstack11lllll_opy_ (u"ࠨࡦࡪ࡮ࡨࡷࡈ࡮ࡡ࡯ࡩࡨࡨࠧᲄ"): [],
                bstack11lllll_opy_ (u"ࠢࡢࡷࡷ࡬ࡴࡸࡳࠣᲅ"): [],
                bstack11lllll_opy_ (u"ࠣࡲࡵࡈࡦࡺࡥࠣᲆ"): bstack11lllll_opy_ (u"ࠤࠥᲇ"),
                bstack11lllll_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡐࡩࡸࡹࡡࡨࡧࡶࠦᲈ"): [],
                bstack11lllll_opy_ (u"ࠦࡵࡸࡔࡪࡶ࡯ࡩࠧᲉ"): bstack11lllll_opy_ (u"ࠧࠨᲊ"),
                bstack11lllll_opy_ (u"ࠨࡰࡳࡆࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳࠨ᲋"): bstack11lllll_opy_ (u"ࠢࠣ᲌"),
                bstack11lllll_opy_ (u"ࠣࡲࡵࡖࡦࡽࡄࡪࡨࡩࠦ᲍"): bstack11lllll_opy_ (u"ࠤࠥ᲎")
            }
            bstack111ll1l1lll_opy_ = repo.active_branch.name
            bstack111l1lllll1_opy_ = repo.head.commit
            result[bstack11lllll_opy_ (u"ࠥࡴࡷࡏࡤࠣ᲏")] = bstack111l1lllll1_opy_.hexsha
            bstack1111llllll1_opy_ = _111l1ll11l1_opy_(repo)
            logger.debug(bstack11lllll_opy_ (u"ࠦࡇࡧࡳࡦࠢࡥࡶࡦࡴࡣࡩࠢࡩࡳࡷࠦࡣࡰ࡯ࡳࡥࡷ࡯ࡳࡰࡰ࠽ࠤࠧᲐ") + str(bstack1111llllll1_opy_) + bstack11lllll_opy_ (u"ࠧࠨᲑ"))
            if bstack1111llllll1_opy_:
                try:
                    bstack1111ll1ll11_opy_ = repo.git.diff(bstack11lllll_opy_ (u"ࠨ࠭࠮ࡰࡤࡱࡪ࠳࡯࡯࡮ࡼࠦᲒ"), bstack1llll11111l_opy_ (u"ࠢࡼࡤࡤࡷࡪࡥࡢࡳࡣࡱࡧ࡭ࢃ࠮࠯࠰ࡾࡧࡺࡸࡲࡦࡰࡷࡣࡧࡸࡡ࡯ࡥ࡫ࢁࠧᲓ")).split(bstack11lllll_opy_ (u"ࠨ࡞ࡱࠫᲔ"))
                    logger.debug(bstack11lllll_opy_ (u"ࠤࡆ࡬ࡦࡴࡧࡦࡦࠣࡪ࡮ࡲࡥࡴࠢࡥࡩࡹࡽࡥࡦࡰࠣࡿࡧࡧࡳࡦࡡࡥࡶࡦࡴࡣࡩࡿࠣࡥࡳࡪࠠࡼࡥࡸࡶࡷ࡫࡮ࡵࡡࡥࡶࡦࡴࡣࡩࡿ࠽ࠤࠧᲕ") + str(bstack1111ll1ll11_opy_) + bstack11lllll_opy_ (u"ࠥࠦᲖ"))
                    result[bstack11lllll_opy_ (u"ࠦ࡫࡯࡬ࡦࡵࡆ࡬ࡦࡴࡧࡦࡦࠥᲗ")] = [f.strip() for f in bstack1111ll1ll11_opy_ if f.strip()]
                    commits = list(repo.iter_commits(bstack1llll11111l_opy_ (u"ࠧࢁࡢࡢࡵࡨࡣࡧࡸࡡ࡯ࡥ࡫ࢁ࠳࠴ࡻࡤࡷࡵࡶࡪࡴࡴࡠࡤࡵࡥࡳࡩࡨࡾࠤᲘ")))
                except Exception:
                    logger.debug(bstack11lllll_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡪࡩࡹࠦࡣࡩࡣࡱ࡫ࡪࡪࠠࡧ࡫࡯ࡩࡸࠦࡦࡳࡱࡰࠤࡧࡸࡡ࡯ࡥ࡫ࠤࡨࡵ࡭ࡱࡣࡵ࡭ࡸࡵ࡮࠯ࠢࡉࡥࡱࡲࡩ࡯ࡩࠣࡦࡦࡩ࡫ࠡࡶࡲࠤࡷ࡫ࡣࡦࡰࡷࠤࡨࡵ࡭࡮࡫ࡷࡷ࠳ࠨᲙ"))
                    commits = list(repo.iter_commits(max_count=10))
                    if commits:
                        result[bstack11lllll_opy_ (u"ࠢࡧ࡫࡯ࡩࡸࡉࡨࡢࡰࡪࡩࡩࠨᲚ")] = _111l11111l1_opy_(commits[:5])
            else:
                commits = list(repo.iter_commits(max_count=10))
                if commits:
                    result[bstack11lllll_opy_ (u"ࠣࡨ࡬ࡰࡪࡹࡃࡩࡣࡱ࡫ࡪࡪࠢᲛ")] = _111l11111l1_opy_(commits[:5])
            bstack111ll11l11l_opy_ = set()
            bstack111l11ll11l_opy_ = []
            for commit in commits:
                logger.debug(bstack11lllll_opy_ (u"ࠤࡓࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡣࡰ࡯ࡰ࡭ࡹࡀࠠࠣᲜ") + str(commit.message) + bstack11lllll_opy_ (u"ࠥࠦᲝ"))
                bstack111l11l11l1_opy_ = commit.author.name if commit.author else bstack11lllll_opy_ (u"࡚ࠦࡴ࡫࡯ࡱࡺࡲࠧᲞ")
                bstack111ll11l11l_opy_.add(bstack111l11l11l1_opy_)
                bstack111l11ll11l_opy_.append({
                    bstack11lllll_opy_ (u"ࠧࡳࡥࡴࡵࡤ࡫ࡪࠨᲟ"): commit.message.strip(),
                    bstack11lllll_opy_ (u"ࠨࡵࡴࡧࡵࠦᲠ"): bstack111l11l11l1_opy_
                })
            result[bstack11lllll_opy_ (u"ࠢࡢࡷࡷ࡬ࡴࡸࡳࠣᲡ")] = list(bstack111ll11l11l_opy_)
            result[bstack11lllll_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡎࡧࡶࡷࡦ࡭ࡥࡴࠤᲢ")] = bstack111l11ll11l_opy_
            result[bstack11lllll_opy_ (u"ࠤࡳࡶࡉࡧࡴࡦࠤᲣ")] = bstack111l1lllll1_opy_.committed_datetime.strftime(bstack11lllll_opy_ (u"ࠥࠩ࡞࠳ࠥ࡮࠯ࠨࡨࠧᲤ"))
            if (not result[bstack11lllll_opy_ (u"ࠦࡵࡸࡔࡪࡶ࡯ࡩࠧᲥ")] or result[bstack11lllll_opy_ (u"ࠧࡶࡲࡕ࡫ࡷࡰࡪࠨᲦ")].strip() == bstack11lllll_opy_ (u"ࠨࠢᲧ")) and bstack111l1lllll1_opy_.message:
                bstack1111llll1ll_opy_ = bstack111l1lllll1_opy_.message.strip().splitlines()
                result[bstack11lllll_opy_ (u"ࠢࡱࡴࡗ࡭ࡹࡲࡥࠣᲨ")] = bstack1111llll1ll_opy_[0] if bstack1111llll1ll_opy_ else bstack11lllll_opy_ (u"ࠣࠤᲩ")
                if len(bstack1111llll1ll_opy_) > 2:
                    result[bstack11lllll_opy_ (u"ࠤࡳࡶࡉ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠤᲪ")] = bstack11lllll_opy_ (u"ࠪࡠࡳ࠭Ძ").join(bstack1111llll1ll_opy_[2:]).strip()
            results.append(result)
        except Exception as err:
            logger.error(bstack11lllll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡴࡶࡵ࡭ࡣࡷ࡭ࡳ࡭ࠠࡈ࡫ࡷࠤࡲ࡫ࡴࡢࡦࡤࡸࡦࠦࡦࡰࡴࠣࡅࡎࠦࡳࡦ࡮ࡨࡧࡹ࡯࡯࡯ࠢࠫࡪࡴࡲࡤࡦࡴ࠽ࠤࢀࢃࠩ࠻ࠢࡾࢁࠥ࠳ࠠࡼࡿࠥᲬ").format(
                folder,
                type(err).__name__,
                str(err)
            ))
    filtered_results = [
        result
        for result in results
        if _111ll1ll111_opy_(result)
    ]
    return filtered_results
def _111ll1ll111_opy_(result):
    bstack11lllll_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࡎࡥ࡭ࡲࡨࡶࠥࡺ࡯ࠡࡥ࡫ࡩࡨࡱࠠࡪࡨࠣࡥࠥ࡭ࡩࡵࠢࡰࡩࡹࡧࡤࡢࡶࡤࠤࡷ࡫ࡳࡶ࡮ࡷࠤ࡮ࡹࠠࡷࡣ࡯࡭ࡩࠦࠨ࡯ࡱࡱ࠱ࡪࡳࡰࡵࡻࠣࡪ࡮ࡲࡥࡴࡅ࡫ࡥࡳ࡭ࡥࡥࠢࡤࡲࡩࠦࡡࡶࡶ࡫ࡳࡷࡹࠩ࠯ࠌࠣࠤࠥࠦࠢࠣࠤᲭ")
    return (
        isinstance(result.get(bstack11lllll_opy_ (u"ࠨࡦࡪ࡮ࡨࡷࡈ࡮ࡡ࡯ࡩࡨࡨࠧᲮ"), None), list)
        and len(result[bstack11lllll_opy_ (u"ࠢࡧ࡫࡯ࡩࡸࡉࡨࡢࡰࡪࡩࡩࠨᲯ")]) > 0
        and isinstance(result.get(bstack11lllll_opy_ (u"ࠣࡣࡸࡸ࡭ࡵࡲࡴࠤᲰ"), None), list)
        and len(result[bstack11lllll_opy_ (u"ࠤࡤࡹࡹ࡮࡯ࡳࡵࠥᲱ")]) > 0
    )
def _111l1ll11l1_opy_(repo):
    bstack11lllll_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࡘࡷࡿࠠࡵࡱࠣࡨࡪࡺࡥࡳ࡯࡬ࡲࡪࠦࡴࡩࡧࠣࡦࡦࡹࡥࠡࡤࡵࡥࡳࡩࡨࠡࡨࡲࡶࠥࡺࡨࡦࠢࡪ࡭ࡻ࡫࡮ࠡࡴࡨࡴࡴࠦࡷࡪࡶ࡫ࡳࡺࡺࠠࡩࡣࡵࡨࡨࡵࡤࡦࡦࠣࡲࡦࡳࡥࡴࠢࡤࡲࡩࠦࡷࡰࡴ࡮ࠤࡼ࡯ࡴࡩࠢࡤࡰࡱࠦࡖࡄࡕࠣࡴࡷࡵࡶࡪࡦࡨࡶࡸ࠴ࠊࠡࠢࠣࠤࡗ࡫ࡴࡶࡴࡱࡷࠥࡺࡨࡦࠢࡧࡩ࡫ࡧࡵ࡭ࡶࠣࡦࡷࡧ࡮ࡤࡪࠣ࡭࡫ࠦࡰࡰࡵࡶ࡭ࡧࡲࡥ࠭ࠢࡨࡰࡸ࡫ࠠࡏࡱࡱࡩ࠳ࠐࠠࠡࠢࠣࠦࠧࠨᲲ")
    try:
        try:
            origin = repo.remotes.origin
            bstack111l11111ll_opy_ = origin.refs[bstack11lllll_opy_ (u"ࠫࡍࡋࡁࡅࠩᲳ")]
            target = bstack111l11111ll_opy_.reference.name
            if target.startswith(bstack11lllll_opy_ (u"ࠬࡵࡲࡪࡩ࡬ࡲ࠴࠭Ჴ")):
                return target
        except Exception:
            pass
        if repo.remotes and repo.remotes.origin.refs:
            for ref in repo.remotes.origin.refs:
                if ref.name.startswith(bstack11lllll_opy_ (u"࠭࡯ࡳ࡫ࡪ࡭ࡳ࠵ࠧᲵ")):
                    return ref.name
        if repo.heads:
            return repo.heads[0].name
    except Exception:
        pass
    return None
def _111l11111l1_opy_(commits):
    bstack11lllll_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࡈࡧࡷࠤࡱ࡯ࡳࡵࠢࡲࡪࠥࡩࡨࡢࡰࡪࡩࡩࠦࡦࡪ࡮ࡨࡷࠥ࡬ࡲࡰ࡯ࠣࡥࠥࡲࡩࡴࡶࠣࡳ࡫ࠦࡣࡰ࡯ࡰ࡭ࡹࡹ࠮ࠋࠢࠣࠤࠥࠨࠢࠣᲶ")
    bstack1111ll1ll11_opy_ = set()
    try:
        for commit in commits:
            if commit.parents:
                for parent in commit.parents:
                    diff = commit.diff(parent)
                    for bstack111ll11llll_opy_ in diff:
                        if bstack111ll11llll_opy_.a_path:
                            bstack1111ll1ll11_opy_.add(bstack111ll11llll_opy_.a_path)
                        if bstack111ll11llll_opy_.b_path:
                            bstack1111ll1ll11_opy_.add(bstack111ll11llll_opy_.b_path)
    except Exception:
        pass
    return list(bstack1111ll1ll11_opy_)
def bstack111l11ll1ll_opy_(bstack111l1111l11_opy_):
    bstack1111lll1l1l_opy_ = bstack111l11ll111_opy_(bstack111l1111l11_opy_)
    if bstack1111lll1l1l_opy_ and bstack1111lll1l1l_opy_ > bstack11l11l11111_opy_:
        bstack111l1ll11ll_opy_ = bstack1111lll1l1l_opy_ - bstack11l11l11111_opy_
        bstack111l111llll_opy_ = bstack111l1ll1l11_opy_(bstack111l1111l11_opy_[bstack11lllll_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡠ࡯ࡨࡷࡸࡧࡧࡦࠤᲷ")], bstack111l1ll11ll_opy_)
        bstack111l1111l11_opy_[bstack11lllll_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡡࡰࡩࡸࡹࡡࡨࡧࠥᲸ")] = bstack111l111llll_opy_
        logger.info(bstack11lllll_opy_ (u"ࠥࡘ࡭࡫ࠠࡤࡱࡰࡱ࡮ࡺࠠࡩࡣࡶࠤࡧ࡫ࡥ࡯ࠢࡷࡶࡺࡴࡣࡢࡶࡨࡨ࠳ࠦࡓࡪࡼࡨࠤࡴ࡬ࠠࡤࡱࡰࡱ࡮ࡺࠠࡢࡨࡷࡩࡷࠦࡴࡳࡷࡱࡧࡦࡺࡩࡰࡰࠣ࡭ࡸࠦࡻࡾࠢࡎࡆࠧᲹ")
                    .format(bstack111l11ll111_opy_(bstack111l1111l11_opy_) / 1024))
    return bstack111l1111l11_opy_
def bstack111l11ll111_opy_(bstack111l1l1l11_opy_):
    try:
        if bstack111l1l1l11_opy_:
            bstack111l111l1l1_opy_ = json.dumps(bstack111l1l1l11_opy_)
            bstack1111lll111l_opy_ = sys.getsizeof(bstack111l111l1l1_opy_)
            return bstack1111lll111l_opy_
    except Exception as e:
        logger.debug(bstack11lllll_opy_ (u"ࠦࡘࡵ࡭ࡦࡶ࡫࡭ࡳ࡭ࠠࡸࡧࡱࡸࠥࡽࡲࡰࡰࡪࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡦࡲࡣࡶ࡮ࡤࡸ࡮ࡴࡧࠡࡵ࡬ࡾࡪࠦ࡯ࡧࠢࡍࡗࡔࡔࠠࡰࡤ࡭ࡩࡨࡺ࠺ࠡࡽࢀࠦᲺ").format(e))
    return -1
def bstack111l1ll1l11_opy_(field, bstack111lll111ll_opy_):
    try:
        bstack1111ll1llll_opy_ = len(bytes(bstack11l1111l11l_opy_, bstack11lllll_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫ᲻")))
        bstack111ll1l1l11_opy_ = bytes(field, bstack11lllll_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬ᲼"))
        bstack111ll111ll1_opy_ = len(bstack111ll1l1l11_opy_)
        bstack111l111ll11_opy_ = ceil(bstack111ll111ll1_opy_ - bstack111lll111ll_opy_ - bstack1111ll1llll_opy_)
        if bstack111l111ll11_opy_ > 0:
            bstack1111llll111_opy_ = bstack111ll1l1l11_opy_[:bstack111l111ll11_opy_].decode(bstack11lllll_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭Ჽ"), errors=bstack11lllll_opy_ (u"ࠨ࡫ࡪࡲࡴࡸࡥࠨᲾ")) + bstack11l1111l11l_opy_
            return bstack1111llll111_opy_
    except Exception as e:
        logger.debug(bstack11lllll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡵࡴࡸࡲࡨࡧࡴࡪࡰࡪࠤ࡫࡯ࡥ࡭ࡦ࠯ࠤࡳࡵࡴࡩ࡫ࡱ࡫ࠥࡽࡡࡴࠢࡷࡶࡺࡴࡣࡢࡶࡨࡨࠥ࡮ࡥࡳࡧ࠽ࠤࢀࢃࠢᲿ").format(e))
    return field
def bstack11ll1lll1l_opy_():
    env = os.environ
    if (bstack11lllll_opy_ (u"ࠥࡎࡊࡔࡋࡊࡐࡖࡣ࡚ࡘࡌࠣ᳀") in env and len(env[bstack11lllll_opy_ (u"ࠦࡏࡋࡎࡌࡋࡑࡗࡤ࡛ࡒࡍࠤ᳁")]) > 0) or (
            bstack11lllll_opy_ (u"ࠧࡐࡅࡏࡍࡌࡒࡘࡥࡈࡐࡏࡈࠦ᳂") in env and len(env[bstack11lllll_opy_ (u"ࠨࡊࡆࡐࡎࡍࡓ࡙࡟ࡉࡑࡐࡉࠧ᳃")]) > 0):
        return {
            bstack11lllll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ᳄"): bstack11lllll_opy_ (u"ࠣࡌࡨࡲࡰ࡯࡮ࡴࠤ᳅"),
            bstack11lllll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ᳆"): env.get(bstack11lllll_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨ᳇")),
            bstack11lllll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ᳈"): env.get(bstack11lllll_opy_ (u"ࠧࡐࡏࡃࡡࡑࡅࡒࡋࠢ᳉")),
            bstack11lllll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ᳊"): env.get(bstack11lllll_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨ᳋"))
        }
    if env.get(bstack11lllll_opy_ (u"ࠣࡅࡌࠦ᳌")) == bstack11lllll_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ᳍") and bstack1ll1ll111_opy_(env.get(bstack11lllll_opy_ (u"ࠥࡇࡎࡘࡃࡍࡇࡆࡍࠧ᳎"))):
        return {
            bstack11lllll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᳏"): bstack11lllll_opy_ (u"ࠧࡉࡩࡳࡥ࡯ࡩࡈࡏࠢ᳐"),
            bstack11lllll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ᳑"): env.get(bstack11lllll_opy_ (u"ࠢࡄࡋࡕࡇࡑࡋ࡟ࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥ᳒")),
            bstack11lllll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ᳓"): env.get(bstack11lllll_opy_ (u"ࠤࡆࡍࡗࡉࡌࡆࡡࡍࡓࡇࠨ᳔")),
            bstack11lllll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ᳕"): env.get(bstack11lllll_opy_ (u"ࠦࡈࡏࡒࡄࡎࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓ᳖ࠢ"))
        }
    if env.get(bstack11lllll_opy_ (u"ࠧࡉࡉ᳗ࠣ")) == bstack11lllll_opy_ (u"ࠨࡴࡳࡷࡨ᳘ࠦ") and bstack1ll1ll111_opy_(env.get(bstack11lllll_opy_ (u"ࠢࡕࡔࡄ࡚ࡎ࡙᳙ࠢ"))):
        return {
            bstack11lllll_opy_ (u"ࠣࡰࡤࡱࡪࠨ᳚"): bstack11lllll_opy_ (u"ࠤࡗࡶࡦࡼࡩࡴࠢࡆࡍࠧ᳛"),
            bstack11lllll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ᳜"): env.get(bstack11lllll_opy_ (u"࡙ࠦࡘࡁࡗࡋࡖࡣࡇ࡛ࡉࡍࡆࡢ࡛ࡊࡈ࡟ࡖࡔࡏ᳝ࠦ")),
            bstack11lllll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫᳞ࠢ"): env.get(bstack11lllll_opy_ (u"ࠨࡔࡓࡃ࡙ࡍࡘࡥࡊࡐࡄࡢࡒࡆࡓࡅ᳟ࠣ")),
            bstack11lllll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ᳠"): env.get(bstack11lllll_opy_ (u"ࠣࡖࡕࡅ࡛ࡏࡓࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢ᳡"))
        }
    if env.get(bstack11lllll_opy_ (u"ࠤࡆࡍ᳢ࠧ")) == bstack11lllll_opy_ (u"ࠥࡸࡷࡻࡥ᳣ࠣ") and env.get(bstack11lllll_opy_ (u"ࠦࡈࡏ࡟ࡏࡃࡐࡉ᳤ࠧ")) == bstack11lllll_opy_ (u"ࠧࡩ࡯ࡥࡧࡶ࡬࡮ࡶ᳥ࠢ"):
        return {
            bstack11lllll_opy_ (u"ࠨ࡮ࡢ࡯ࡨ᳦ࠦ"): bstack11lllll_opy_ (u"ࠢࡄࡱࡧࡩࡸ࡮ࡩࡱࠤ᳧"),
            bstack11lllll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯᳨ࠦ"): None,
            bstack11lllll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᳩ"): None,
            bstack11lllll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᳪ"): None
        }
    if env.get(bstack11lllll_opy_ (u"ࠦࡇࡏࡔࡃࡗࡆࡏࡊ࡚࡟ࡃࡔࡄࡒࡈࡎࠢᳫ")) and env.get(bstack11lllll_opy_ (u"ࠧࡈࡉࡕࡄࡘࡇࡐࡋࡔࡠࡅࡒࡑࡒࡏࡔࠣᳬ")):
        return {
            bstack11lllll_opy_ (u"ࠨ࡮ࡢ࡯ࡨ᳭ࠦ"): bstack11lllll_opy_ (u"ࠢࡃ࡫ࡷࡦࡺࡩ࡫ࡦࡶࠥᳮ"),
            bstack11lllll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᳯ"): env.get(bstack11lllll_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡍࡉࡕࡡࡋࡘ࡙ࡖ࡟ࡐࡔࡌࡋࡎࡔࠢᳰ")),
            bstack11lllll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᳱ"): None,
            bstack11lllll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᳲ"): env.get(bstack11lllll_opy_ (u"ࠧࡈࡉࡕࡄࡘࡇࡐࡋࡔࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢᳳ"))
        }
    if env.get(bstack11lllll_opy_ (u"ࠨࡃࡊࠤ᳴")) == bstack11lllll_opy_ (u"ࠢࡵࡴࡸࡩࠧᳵ") and bstack1ll1ll111_opy_(env.get(bstack11lllll_opy_ (u"ࠣࡆࡕࡓࡓࡋࠢᳶ"))):
        return {
            bstack11lllll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᳷"): bstack11lllll_opy_ (u"ࠥࡈࡷࡵ࡮ࡦࠤ᳸"),
            bstack11lllll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ᳹"): env.get(bstack11lllll_opy_ (u"ࠧࡊࡒࡐࡐࡈࡣࡇ࡛ࡉࡍࡆࡢࡐࡎࡔࡋࠣᳺ")),
            bstack11lllll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ᳻"): None,
            bstack11lllll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ᳼"): env.get(bstack11lllll_opy_ (u"ࠣࡆࡕࡓࡓࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨ᳽"))
        }
    if env.get(bstack11lllll_opy_ (u"ࠤࡆࡍࠧ᳾")) == bstack11lllll_opy_ (u"ࠥࡸࡷࡻࡥࠣ᳿") and bstack1ll1ll111_opy_(env.get(bstack11lllll_opy_ (u"ࠦࡘࡋࡍࡂࡒࡋࡓࡗࡋࠢᴀ"))):
        return {
            bstack11lllll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᴁ"): bstack11lllll_opy_ (u"ࠨࡓࡦ࡯ࡤࡴ࡭ࡵࡲࡦࠤᴂ"),
            bstack11lllll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᴃ"): env.get(bstack11lllll_opy_ (u"ࠣࡕࡈࡑࡆࡖࡈࡐࡔࡈࡣࡔࡘࡇࡂࡐࡌ࡞ࡆ࡚ࡉࡐࡐࡢ࡙ࡗࡒࠢᴄ")),
            bstack11lllll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᴅ"): env.get(bstack11lllll_opy_ (u"ࠥࡗࡊࡓࡁࡑࡊࡒࡖࡊࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣᴆ")),
            bstack11lllll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᴇ"): env.get(bstack11lllll_opy_ (u"࡙ࠧࡅࡎࡃࡓࡌࡔࡘࡅࡠࡌࡒࡆࡤࡏࡄࠣᴈ"))
        }
    if env.get(bstack11lllll_opy_ (u"ࠨࡃࡊࠤᴉ")) == bstack11lllll_opy_ (u"ࠢࡵࡴࡸࡩࠧᴊ") and bstack1ll1ll111_opy_(env.get(bstack11lllll_opy_ (u"ࠣࡉࡌࡘࡑࡇࡂࡠࡅࡌࠦᴋ"))):
        return {
            bstack11lllll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᴌ"): bstack11lllll_opy_ (u"ࠥࡋ࡮ࡺࡌࡢࡤࠥᴍ"),
            bstack11lllll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᴎ"): env.get(bstack11lllll_opy_ (u"ࠧࡉࡉࡠࡌࡒࡆࡤ࡛ࡒࡍࠤᴏ")),
            bstack11lllll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᴐ"): env.get(bstack11lllll_opy_ (u"ࠢࡄࡋࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧᴑ")),
            bstack11lllll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᴒ"): env.get(bstack11lllll_opy_ (u"ࠤࡆࡍࡤࡐࡏࡃࡡࡌࡈࠧᴓ"))
        }
    if env.get(bstack11lllll_opy_ (u"ࠥࡇࡎࠨᴔ")) == bstack11lllll_opy_ (u"ࠦࡹࡸࡵࡦࠤᴕ") and bstack1ll1ll111_opy_(env.get(bstack11lllll_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࠣᴖ"))):
        return {
            bstack11lllll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᴗ"): bstack11lllll_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡱࡩࡵࡧࠥᴘ"),
            bstack11lllll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᴙ"): env.get(bstack11lllll_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣᴚ")),
            bstack11lllll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᴛ"): env.get(bstack11lllll_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡎࡍ࡙ࡋ࡟ࡍࡃࡅࡉࡑࠨᴜ")) or env.get(bstack11lllll_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡒࡆࡓࡅࠣᴝ")),
            bstack11lllll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᴞ"): env.get(bstack11lllll_opy_ (u"ࠢࡃࡗࡌࡐࡉࡑࡉࡕࡇࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤᴟ"))
        }
    if bstack1ll1ll111_opy_(env.get(bstack11lllll_opy_ (u"ࠣࡖࡉࡣࡇ࡛ࡉࡍࡆࠥᴠ"))):
        return {
            bstack11lllll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᴡ"): bstack11lllll_opy_ (u"࡚ࠥ࡮ࡹࡵࡢ࡮ࠣࡗࡹࡻࡤࡪࡱࠣࡘࡪࡧ࡭ࠡࡕࡨࡶࡻ࡯ࡣࡦࡵࠥᴢ"),
            bstack11lllll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᴣ"): bstack11lllll_opy_ (u"ࠧࢁࡽࡼࡿࠥᴤ").format(env.get(bstack11lllll_opy_ (u"࠭ࡓ࡚ࡕࡗࡉࡒࡥࡔࡆࡃࡐࡊࡔ࡛ࡎࡅࡃࡗࡍࡔࡔࡓࡆࡔ࡙ࡉࡗ࡛ࡒࡊࠩᴥ")), env.get(bstack11lllll_opy_ (u"ࠧࡔ࡛ࡖࡘࡊࡓ࡟ࡕࡇࡄࡑࡕࡘࡏࡋࡇࡆࡘࡎࡊࠧᴦ"))),
            bstack11lllll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᴧ"): env.get(bstack11lllll_opy_ (u"ࠤࡖ࡝ࡘ࡚ࡅࡎࡡࡇࡉࡋࡏࡎࡊࡖࡌࡓࡓࡏࡄࠣᴨ")),
            bstack11lllll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᴩ"): env.get(bstack11lllll_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡋࡇࠦᴪ"))
        }
    if bstack1ll1ll111_opy_(env.get(bstack11lllll_opy_ (u"ࠧࡇࡐࡑࡘࡈ࡝ࡔࡘࠢᴫ"))):
        return {
            bstack11lllll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᴬ"): bstack11lllll_opy_ (u"ࠢࡂࡲࡳࡺࡪࡿ࡯ࡳࠤᴭ"),
            bstack11lllll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᴮ"): bstack11lllll_opy_ (u"ࠤࡾࢁ࠴ࡶࡲࡰ࡬ࡨࡧࡹ࠵ࡻࡾ࠱ࡾࢁ࠴ࡨࡵࡪ࡮ࡧࡷ࠴ࢁࡽࠣᴯ").format(env.get(bstack11lllll_opy_ (u"ࠪࡅࡕࡖࡖࡆ࡛ࡒࡖࡤ࡛ࡒࡍࠩᴰ")), env.get(bstack11lllll_opy_ (u"ࠫࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡁࡄࡅࡒ࡙ࡓ࡚࡟ࡏࡃࡐࡉࠬᴱ")), env.get(bstack11lllll_opy_ (u"ࠬࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡑࡔࡒࡎࡊࡉࡔࡠࡕࡏ࡙ࡌ࠭ᴲ")), env.get(bstack11lllll_opy_ (u"࠭ࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪᴳ"))),
            bstack11lllll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᴴ"): env.get(bstack11lllll_opy_ (u"ࠣࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧᴵ")),
            bstack11lllll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᴶ"): env.get(bstack11lllll_opy_ (u"ࠥࡅࡕࡖࡖࡆ࡛ࡒࡖࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦᴷ"))
        }
    if env.get(bstack11lllll_opy_ (u"ࠦࡆࡠࡕࡓࡇࡢࡌ࡙࡚ࡐࡠࡗࡖࡉࡗࡥࡁࡈࡇࡑࡘࠧᴸ")) and env.get(bstack11lllll_opy_ (u"࡚ࠧࡆࡠࡄࡘࡍࡑࡊࠢᴹ")):
        return {
            bstack11lllll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᴺ"): bstack11lllll_opy_ (u"ࠢࡂࡼࡸࡶࡪࠦࡃࡊࠤᴻ"),
            bstack11lllll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᴼ"): bstack11lllll_opy_ (u"ࠤࡾࢁࢀࢃ࠯ࡠࡤࡸ࡭ࡱࡪ࠯ࡳࡧࡶࡹࡱࡺࡳࡀࡤࡸ࡭ࡱࡪࡉࡥ࠿ࡾࢁࠧᴽ").format(env.get(bstack11lllll_opy_ (u"ࠪࡗ࡞࡙ࡔࡆࡏࡢࡘࡊࡇࡍࡇࡑࡘࡒࡉࡇࡔࡊࡑࡑࡗࡊࡘࡖࡆࡔࡘࡖࡎ࠭ᴾ")), env.get(bstack11lllll_opy_ (u"ࠫࡘ࡟ࡓࡕࡇࡐࡣ࡙ࡋࡁࡎࡒࡕࡓࡏࡋࡃࡕࠩᴿ")), env.get(bstack11lllll_opy_ (u"ࠬࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡌࡈࠬᵀ"))),
            bstack11lllll_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᵁ"): env.get(bstack11lllll_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡎࡊࠢᵂ")),
            bstack11lllll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᵃ"): env.get(bstack11lllll_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊࡉࡅࠤᵄ"))
        }
    if any([env.get(bstack11lllll_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠣᵅ")), env.get(bstack11lllll_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡓࡇࡖࡓࡑ࡜ࡅࡅࡡࡖࡓ࡚ࡘࡃࡆࡡ࡙ࡉࡗ࡙ࡉࡐࡐࠥᵆ")), env.get(bstack11lllll_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡕࡒ࡙ࡗࡉࡅࡠࡘࡈࡖࡘࡏࡏࡏࠤᵇ"))]):
        return {
            bstack11lllll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᵈ"): bstack11lllll_opy_ (u"ࠢࡂ࡙ࡖࠤࡈࡵࡤࡦࡄࡸ࡭ࡱࡪࠢᵉ"),
            bstack11lllll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᵊ"): env.get(bstack11lllll_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤࡖࡕࡃࡎࡌࡇࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣᵋ")),
            bstack11lllll_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᵌ"): env.get(bstack11lllll_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠤᵍ")),
            bstack11lllll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᵎ"): env.get(bstack11lllll_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦᵏ"))
        }
    if env.get(bstack11lllll_opy_ (u"ࠢࡣࡣࡰࡦࡴࡵ࡟ࡣࡷ࡬ࡰࡩࡔࡵ࡮ࡤࡨࡶࠧᵐ")):
        return {
            bstack11lllll_opy_ (u"ࠣࡰࡤࡱࡪࠨᵑ"): bstack11lllll_opy_ (u"ࠤࡅࡥࡲࡨ࡯ࡰࠤᵒ"),
            bstack11lllll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᵓ"): env.get(bstack11lllll_opy_ (u"ࠦࡧࡧ࡭ࡣࡱࡲࡣࡧࡻࡩ࡭ࡦࡕࡩࡸࡻ࡬ࡵࡵࡘࡶࡱࠨᵔ")),
            bstack11lllll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᵕ"): env.get(bstack11lllll_opy_ (u"ࠨࡢࡢ࡯ࡥࡳࡴࡥࡳࡩࡱࡵࡸࡏࡵࡢࡏࡣࡰࡩࠧᵖ")),
            bstack11lllll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᵗ"): env.get(bstack11lllll_opy_ (u"ࠣࡤࡤࡱࡧࡵ࡯ࡠࡤࡸ࡭ࡱࡪࡎࡶ࡯ࡥࡩࡷࠨᵘ"))
        }
    if env.get(bstack11lllll_opy_ (u"ࠤ࡚ࡉࡗࡉࡋࡆࡔࠥᵙ")) or env.get(bstack11lllll_opy_ (u"࡛ࠥࡊࡘࡃࡌࡇࡕࡣࡒࡇࡉࡏࡡࡓࡍࡕࡋࡌࡊࡐࡈࡣࡘ࡚ࡁࡓࡖࡈࡈࠧᵚ")):
        return {
            bstack11lllll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᵛ"): bstack11lllll_opy_ (u"ࠧ࡝ࡥࡳࡥ࡮ࡩࡷࠨᵜ"),
            bstack11lllll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᵝ"): env.get(bstack11lllll_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦᵞ")),
            bstack11lllll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᵟ"): bstack11lllll_opy_ (u"ࠤࡐࡥ࡮ࡴࠠࡑ࡫ࡳࡩࡱ࡯࡮ࡦࠤᵠ") if env.get(bstack11lllll_opy_ (u"࡛ࠥࡊࡘࡃࡌࡇࡕࡣࡒࡇࡉࡏࡡࡓࡍࡕࡋࡌࡊࡐࡈࡣࡘ࡚ࡁࡓࡖࡈࡈࠧᵡ")) else None,
            bstack11lllll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᵢ"): env.get(bstack11lllll_opy_ (u"ࠧ࡝ࡅࡓࡅࡎࡉࡗࡥࡇࡊࡖࡢࡇࡔࡓࡍࡊࡖࠥᵣ"))
        }
    if any([env.get(bstack11lllll_opy_ (u"ࠨࡇࡄࡒࡢࡔࡗࡕࡊࡆࡅࡗࠦᵤ")), env.get(bstack11lllll_opy_ (u"ࠢࡈࡅࡏࡓ࡚ࡊ࡟ࡑࡔࡒࡎࡊࡉࡔࠣᵥ")), env.get(bstack11lllll_opy_ (u"ࠣࡉࡒࡓࡌࡒࡅࡠࡅࡏࡓ࡚ࡊ࡟ࡑࡔࡒࡎࡊࡉࡔࠣᵦ"))]):
        return {
            bstack11lllll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᵧ"): bstack11lllll_opy_ (u"ࠥࡋࡴࡵࡧ࡭ࡧࠣࡇࡱࡵࡵࡥࠤᵨ"),
            bstack11lllll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᵩ"): None,
            bstack11lllll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᵪ"): env.get(bstack11lllll_opy_ (u"ࠨࡐࡓࡑࡍࡉࡈ࡚࡟ࡊࡆࠥᵫ")),
            bstack11lllll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᵬ"): env.get(bstack11lllll_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡊࡆࠥᵭ"))
        }
    if env.get(bstack11lllll_opy_ (u"ࠤࡖࡌࡎࡖࡐࡂࡄࡏࡉࠧᵮ")):
        return {
            bstack11lllll_opy_ (u"ࠥࡲࡦࡳࡥࠣᵯ"): bstack11lllll_opy_ (u"ࠦࡘ࡮ࡩࡱࡲࡤࡦࡱ࡫ࠢᵰ"),
            bstack11lllll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᵱ"): env.get(bstack11lllll_opy_ (u"ࠨࡓࡉࡋࡓࡔࡆࡈࡌࡆࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧᵲ")),
            bstack11lllll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᵳ"): bstack11lllll_opy_ (u"ࠣࡌࡲࡦࠥࠩࡻࡾࠤᵴ").format(env.get(bstack11lllll_opy_ (u"ࠩࡖࡌࡎࡖࡐࡂࡄࡏࡉࡤࡐࡏࡃࡡࡌࡈࠬᵵ"))) if env.get(bstack11lllll_opy_ (u"ࠥࡗࡍࡏࡐࡑࡃࡅࡐࡊࡥࡊࡐࡄࡢࡍࡉࠨᵶ")) else None,
            bstack11lllll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᵷ"): env.get(bstack11lllll_opy_ (u"࡙ࠧࡈࡊࡒࡓࡅࡇࡒࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢᵸ"))
        }
    if bstack1ll1ll111_opy_(env.get(bstack11lllll_opy_ (u"ࠨࡎࡆࡖࡏࡍࡋ࡟ࠢᵹ"))):
        return {
            bstack11lllll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᵺ"): bstack11lllll_opy_ (u"ࠣࡐࡨࡸࡱ࡯ࡦࡺࠤᵻ"),
            bstack11lllll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᵼ"): env.get(bstack11lllll_opy_ (u"ࠥࡈࡊࡖࡌࡐ࡛ࡢ࡙ࡗࡒࠢᵽ")),
            bstack11lllll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᵾ"): env.get(bstack11lllll_opy_ (u"࡙ࠧࡉࡕࡇࡢࡒࡆࡓࡅࠣᵿ")),
            bstack11lllll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᶀ"): env.get(bstack11lllll_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡉࡅࠤᶁ"))
        }
    if bstack1ll1ll111_opy_(env.get(bstack11lllll_opy_ (u"ࠣࡉࡌࡘࡍ࡛ࡂࡠࡃࡆࡘࡎࡕࡎࡔࠤᶂ"))):
        return {
            bstack11lllll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᶃ"): bstack11lllll_opy_ (u"ࠥࡋ࡮ࡺࡈࡶࡤࠣࡅࡨࡺࡩࡰࡰࡶࠦᶄ"),
            bstack11lllll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᶅ"): bstack11lllll_opy_ (u"ࠧࢁࡽ࠰ࡽࢀ࠳ࡦࡩࡴࡪࡱࡱࡷ࠴ࡸࡵ࡯ࡵ࠲ࡿࢂࠨᶆ").format(env.get(bstack11lllll_opy_ (u"࠭ࡇࡊࡖࡋ࡙ࡇࡥࡓࡆࡔ࡙ࡉࡗࡥࡕࡓࡎࠪᶇ")), env.get(bstack11lllll_opy_ (u"ࠧࡈࡋࡗࡌ࡚ࡈ࡟ࡓࡇࡓࡓࡘࡏࡔࡐࡔ࡜ࠫᶈ")), env.get(bstack11lllll_opy_ (u"ࠨࡉࡌࡘࡍ࡛ࡂࡠࡔࡘࡒࡤࡏࡄࠨᶉ"))),
            bstack11lllll_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᶊ"): env.get(bstack11lllll_opy_ (u"ࠥࡋࡎ࡚ࡈࡖࡄࡢ࡛ࡔࡘࡋࡇࡎࡒ࡛ࠧᶋ")),
            bstack11lllll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᶌ"): env.get(bstack11lllll_opy_ (u"ࠧࡍࡉࡕࡊࡘࡆࡤࡘࡕࡏࡡࡌࡈࠧᶍ"))
        }
    if env.get(bstack11lllll_opy_ (u"ࠨࡃࡊࠤᶎ")) == bstack11lllll_opy_ (u"ࠢࡵࡴࡸࡩࠧᶏ") and env.get(bstack11lllll_opy_ (u"ࠣࡘࡈࡖࡈࡋࡌࠣᶐ")) == bstack11lllll_opy_ (u"ࠤ࠴ࠦᶑ"):
        return {
            bstack11lllll_opy_ (u"ࠥࡲࡦࡳࡥࠣᶒ"): bstack11lllll_opy_ (u"࡛ࠦ࡫ࡲࡤࡧ࡯ࠦᶓ"),
            bstack11lllll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᶔ"): bstack11lllll_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࡻࡾࠤᶕ").format(env.get(bstack11lllll_opy_ (u"ࠧࡗࡇࡕࡇࡊࡒ࡟ࡖࡔࡏࠫᶖ"))),
            bstack11lllll_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᶗ"): None,
            bstack11lllll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᶘ"): None,
        }
    if env.get(bstack11lllll_opy_ (u"ࠥࡘࡊࡇࡍࡄࡋࡗ࡝ࡤ࡜ࡅࡓࡕࡌࡓࡓࠨᶙ")):
        return {
            bstack11lllll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᶚ"): bstack11lllll_opy_ (u"࡚ࠧࡥࡢ࡯ࡦ࡭ࡹࡿࠢᶛ"),
            bstack11lllll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᶜ"): None,
            bstack11lllll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᶝ"): env.get(bstack11lllll_opy_ (u"ࠣࡖࡈࡅࡒࡉࡉࡕ࡛ࡢࡔࡗࡕࡊࡆࡅࡗࡣࡓࡇࡍࡆࠤᶞ")),
            bstack11lllll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᶟ"): env.get(bstack11lllll_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤᶠ"))
        }
    if any([env.get(bstack11lllll_opy_ (u"ࠦࡈࡕࡎࡄࡑࡘࡖࡘࡋࠢᶡ")), env.get(bstack11lllll_opy_ (u"ࠧࡉࡏࡏࡅࡒ࡙ࡗ࡙ࡅࡠࡗࡕࡐࠧᶢ")), env.get(bstack11lllll_opy_ (u"ࠨࡃࡐࡐࡆࡓ࡚ࡘࡓࡆࡡࡘࡗࡊࡘࡎࡂࡏࡈࠦᶣ")), env.get(bstack11lllll_opy_ (u"ࠢࡄࡑࡑࡇࡔ࡛ࡒࡔࡇࡢࡘࡊࡇࡍࠣᶤ"))]):
        return {
            bstack11lllll_opy_ (u"ࠣࡰࡤࡱࡪࠨᶥ"): bstack11lllll_opy_ (u"ࠤࡆࡳࡳࡩ࡯ࡶࡴࡶࡩࠧᶦ"),
            bstack11lllll_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᶧ"): None,
            bstack11lllll_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᶨ"): env.get(bstack11lllll_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨᶩ")) or None,
            bstack11lllll_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᶪ"): env.get(bstack11lllll_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡉࡅࠤᶫ"), 0)
        }
    if env.get(bstack11lllll_opy_ (u"ࠣࡉࡒࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨᶬ")):
        return {
            bstack11lllll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᶭ"): bstack11lllll_opy_ (u"ࠥࡋࡴࡉࡄࠣᶮ"),
            bstack11lllll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᶯ"): None,
            bstack11lllll_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᶰ"): env.get(bstack11lllll_opy_ (u"ࠨࡇࡐࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦᶱ")),
            bstack11lllll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᶲ"): env.get(bstack11lllll_opy_ (u"ࠣࡉࡒࡣࡕࡏࡐࡆࡎࡌࡒࡊࡥࡃࡐࡗࡑࡘࡊࡘࠢᶳ"))
        }
    if env.get(bstack11lllll_opy_ (u"ࠤࡆࡊࡤࡈࡕࡊࡎࡇࡣࡎࡊࠢᶴ")):
        return {
            bstack11lllll_opy_ (u"ࠥࡲࡦࡳࡥࠣᶵ"): bstack11lllll_opy_ (u"ࠦࡈࡵࡤࡦࡈࡵࡩࡸ࡮ࠢᶶ"),
            bstack11lllll_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᶷ"): env.get(bstack11lllll_opy_ (u"ࠨࡃࡇࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧᶸ")),
            bstack11lllll_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᶹ"): env.get(bstack11lllll_opy_ (u"ࠣࡅࡉࡣࡕࡏࡐࡆࡎࡌࡒࡊࡥࡎࡂࡏࡈࠦᶺ")),
            bstack11lllll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᶻ"): env.get(bstack11lllll_opy_ (u"ࠥࡇࡋࡥࡂࡖࡋࡏࡈࡤࡏࡄࠣᶼ"))
        }
    return {bstack11lllll_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᶽ"): None}
def get_host_info():
    return {
        bstack11lllll_opy_ (u"ࠧ࡮࡯ࡴࡶࡱࡥࡲ࡫ࠢᶾ"): platform.node(),
        bstack11lllll_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠣᶿ"): platform.system(),
        bstack11lllll_opy_ (u"ࠢࡵࡻࡳࡩࠧ᷀"): platform.machine(),
        bstack11lllll_opy_ (u"ࠣࡸࡨࡶࡸ࡯࡯࡯ࠤ᷁"): platform.version(),
        bstack11lllll_opy_ (u"ࠤࡤࡶࡨ࡮᷂ࠢ"): platform.architecture()[0]
    }
def bstack1ll1l111ll_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack111ll111l11_opy_():
    if bstack1l111111_opy_.get_property(bstack11lllll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࠫ᷃")):
        return bstack11lllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪ᷄")
    return bstack11lllll_opy_ (u"ࠬࡻ࡮࡬ࡰࡲࡻࡳࡥࡧࡳ࡫ࡧࠫ᷅")
def bstack111ll1llll1_opy_(driver):
    info = {
        bstack11lllll_opy_ (u"࠭ࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬ᷆"): driver.capabilities,
        bstack11lllll_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠫ᷇"): driver.session_id,
        bstack11lllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩ᷈"): driver.capabilities.get(bstack11lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ᷉"), None),
        bstack11lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲ᷊ࠬ"): driver.capabilities.get(bstack11lllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ᷋"), None),
        bstack11lllll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࠧ᷌"): driver.capabilities.get(bstack11lllll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠬ᷍"), None),
        bstack11lllll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡࡹࡩࡷࡹࡩࡰࡰ᷎ࠪ"):driver.capabilities.get(bstack11lllll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰ᷏ࠪ"), None),
    }
    if bstack111ll111l11_opy_() == bstack11lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ᷐"):
        if bstack1l1ll11l_opy_():
            info[bstack11lllll_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࠫ᷑")] = bstack11lllll_opy_ (u"ࠫࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧࠪ᷒")
        elif driver.capabilities.get(bstack11lllll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᷓ"), {}).get(bstack11lllll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧࠪᷔ"), False):
            info[bstack11lllll_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࠨᷕ")] = bstack11lllll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡳࡤࡣ࡯ࡩࠬᷖ")
        else:
            info[bstack11lllll_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࠪᷗ")] = bstack11lllll_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩࠬᷘ")
    return info
def bstack1l1ll11l_opy_():
    if bstack1l111111_opy_.get_property(bstack11lllll_opy_ (u"ࠫࡦࡶࡰࡠࡣࡸࡸࡴࡳࡡࡵࡧࠪᷙ")):
        return True
    if bstack1ll1ll111_opy_(os.environ.get(bstack11lllll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭ᷚ"), None)):
        return True
    return False
def bstack1111lll1l11_opy_(bstack111ll1lll11_opy_, url, response, headers=None, data=None):
    bstack11lllll_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡂࡶ࡫࡯ࡨࠥࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢ࡯ࡳ࡬ࠦࡰࡢࡴࡤࡱࡪࡺࡥࡳࡵࠣࡪࡴࡸࠠࡳࡧࡴࡹࡪࡹࡴ࠰ࡴࡨࡷࡵࡵ࡮ࡴࡧࠣࡰࡴ࡭ࡧࡪࡰࡪࠎࠥࠦࠠࠡࡃࡵ࡫ࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࡴࡨࡵࡺ࡫ࡳࡵࡡࡷࡽࡵ࡫࠺ࠡࡊࡗࡘࡕࠦ࡭ࡦࡶ࡫ࡳࡩࠦࠨࡈࡇࡗ࠰ࠥࡖࡏࡔࡖ࠯ࠤࡪࡺࡣ࠯ࠫࠍࠤࠥࠦࠠࠡࠢࠣࠤࡺࡸ࡬࠻ࠢࡕࡩࡶࡻࡥࡴࡶ࡙ࠣࡗࡒ࠯ࡦࡰࡧࡴࡴ࡯࡮ࡵࠌࠣࠤࠥࠦࠠࠡࠢࠣࡶࡪࡹࡰࡰࡰࡶࡩ࠿ࠦࡒࡦࡵࡳࡳࡳࡹࡥࠡࡱࡥ࡮ࡪࡩࡴࠡࡨࡵࡳࡲࠦࡲࡦࡳࡸࡩࡸࡺࡳࠋࠢࠣࠤࠥࠦࠠࠡࠢ࡫ࡩࡦࡪࡥࡳࡵ࠽ࠤࡗ࡫ࡱࡶࡧࡶࡸࠥ࡮ࡥࡢࡦࡨࡶࡸࠦ࡯ࡳࠢࡑࡳࡳ࡫ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡦࡤࡸࡦࡀࠠࡓࡧࡴࡹࡪࡹࡴࠡࡌࡖࡓࡓࠦࡤࡢࡶࡤࠤࡴࡸࠠࡏࡱࡱࡩࠏࠦࠠࠡࠢࡕࡩࡹࡻࡲ࡯ࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡪࡩࡤࡶ࠽ࠤࡋࡵࡲ࡮ࡣࡷࡸࡪࡪࠠ࡭ࡱࡪࠤࡲ࡫ࡳࡴࡣࡪࡩࠥࡽࡩࡵࡪࠣࡶࡪࡷࡵࡦࡵࡷࠤࡦࡴࡤࠡࡴࡨࡷࡵࡵ࡮ࡴࡧࠣࡨࡦࡺࡡࠋࠢࠣࠤࠥࠨࠢࠣᷛ")
    bstack111ll11l111_opy_ = {
        bstack11lllll_opy_ (u"ࠢࡩࡧࡤࡨࡪࡸࡳࠣᷜ"): headers,
        bstack11lllll_opy_ (u"ࠣ࡯ࡨࡸ࡭ࡵࡤࠣᷝ"): bstack111ll1lll11_opy_.upper(),
        bstack11lllll_opy_ (u"ࠤࡤ࡫ࡪࡴࡴࠣᷞ"): None,
        bstack11lllll_opy_ (u"ࠥࡩࡳࡪࡰࡰ࡫ࡱࡸࠧᷟ"): url,
        bstack11lllll_opy_ (u"ࠦ࡯ࡹ࡯࡯ࠤᷠ"): data
    }
    try:
        bstack111l1llll1l_opy_ = response.json()
    except Exception:
        bstack111l1llll1l_opy_ = response.text
    bstack111ll11111l_opy_ = {
        bstack11lllll_opy_ (u"ࠧࡨ࡯ࡥࡻࠥᷡ"): bstack111l1llll1l_opy_,
        bstack11lllll_opy_ (u"ࠨࡳࡵࡣࡷࡹࡸࡉ࡯ࡥࡧࠥᷢ"): response.status_code
    }
    return {
        bstack11lllll_opy_ (u"ࠢࡳࡧࡴࡹࡪࡹࡴࠣᷣ"): bstack111ll11l111_opy_,
        bstack11lllll_opy_ (u"ࠣࡴࡨࡷࡵࡵ࡮ࡴࡧࠥᷤ"): bstack111ll11111l_opy_
    }
def bstack111ll111_opy_(bstack111ll1lll11_opy_, url, data, config):
    headers = config.get(bstack11lllll_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪᷥ"), None)
    proxies = bstack11l1l1111_opy_(config, url)
    auth = config.get(bstack11lllll_opy_ (u"ࠪࡥࡺࡺࡨࠨᷦ"), None)
    response = requests.request(
            bstack111ll1lll11_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    try:
        log_message = bstack1111lll1l11_opy_(bstack111ll1lll11_opy_, url, response, headers, data)
        bstack1l111l111l_opy_.debug(json.dumps(log_message, separators=(bstack11lllll_opy_ (u"ࠫ࠱࠭ᷧ"), bstack11lllll_opy_ (u"ࠬࡀࠧᷨ"))))
    except Exception as e:
        logger.debug(bstack11lllll_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡱࡵࡧࡨ࡫ࡱ࡫ࠥࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡵࡩࡶࡻࡥࡴࡶ࠽ࠤࢀࢃࠢᷩ").format(e))
    return response
def bstack11l11l111_opy_(bstack111l11l111_opy_, size):
    bstack11l11llll_opy_ = []
    while len(bstack111l11l111_opy_) > size:
        bstack1ll11l111_opy_ = bstack111l11l111_opy_[:size]
        bstack11l11llll_opy_.append(bstack1ll11l111_opy_)
        bstack111l11l111_opy_ = bstack111l11l111_opy_[size:]
    bstack11l11llll_opy_.append(bstack111l11l111_opy_)
    return bstack11l11llll_opy_
def bstack1111lllll1l_opy_(message, bstack1111llll11l_opy_=False):
    os.write(1, bytes(message, bstack11lllll_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭ᷪ")))
    os.write(1, bytes(bstack11lllll_opy_ (u"ࠨ࡞ࡱࠫᷫ"), bstack11lllll_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨᷬ")))
    if bstack1111llll11l_opy_:
        with open(bstack11lllll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠰ࡳ࠶࠷ࡹ࠮ࠩᷭ") + os.environ[bstack11lllll_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡉࡃࡖࡌࡊࡊ࡟ࡊࡆࠪᷮ")] + bstack11lllll_opy_ (u"ࠬ࠴࡬ࡰࡩࠪᷯ"), bstack11lllll_opy_ (u"࠭ࡡࠨᷰ")) as f:
            f.write(message + bstack11lllll_opy_ (u"ࠧ࡝ࡰࠪᷱ"))
def bstack1l11llll111_opy_():
    return os.environ[bstack11lllll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫᷲ")].lower() == bstack11lllll_opy_ (u"ࠩࡷࡶࡺ࡫ࠧᷳ")
def bstack1lll11lll1_opy_():
    return bstack11111ll1ll_opy_().replace(tzinfo=None).isoformat() + bstack11lllll_opy_ (u"ࠪ࡞ࠬᷴ")
def bstack111ll1l1ll1_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack11lllll_opy_ (u"ࠫ࡟࠭᷵"))) - datetime.datetime.fromisoformat(start.rstrip(bstack11lllll_opy_ (u"ࠬࡠࠧ᷶")))).total_seconds() * 1000
def bstack111l11l1l1l_opy_(timestamp):
    return bstack111ll1l111l_opy_(timestamp).isoformat() + bstack11lllll_opy_ (u"࡚࠭ࠨ᷷")
def bstack111l1ll1lll_opy_(bstack111l1l11l1l_opy_):
    date_format = bstack11lllll_opy_ (u"࡛ࠧࠦࠨࡱࠪࡪࠠࠦࡊ࠽ࠩࡒࡀࠥࡔ࠰ࠨࡪ᷸ࠬ")
    bstack111ll111111_opy_ = datetime.datetime.strptime(bstack111l1l11l1l_opy_, date_format)
    return bstack111ll111111_opy_.isoformat() + bstack11lllll_opy_ (u"ࠨ࡜᷹ࠪ")
def bstack111ll1111l1_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack11lllll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥ᷺ࠩ")
    else:
        return bstack11lllll_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ᷻")
def bstack1ll1ll111_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack11lllll_opy_ (u"ࠫࡹࡸࡵࡦࠩ᷼")
def bstack111ll1ll11l_opy_(val):
    return val.__str__().lower() == bstack11lllll_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨ᷽ࠫ")
def error_handler(bstack111ll1ll1ll_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack111ll1ll1ll_opy_ as e:
                print(bstack11lllll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࡼࡿࠣ࠱ࡃࠦࡻࡾ࠼ࠣࡿࢂࠨ᷾").format(func.__name__, bstack111ll1ll1ll_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack111l1l11l11_opy_(bstack111l1ll1ll1_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack111l1ll1ll1_opy_(cls, *args, **kwargs)
            except bstack111ll1ll1ll_opy_ as e:
                print(bstack11lllll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠡࡽࢀࠤ࠲ࡄࠠࡼࡿ࠽ࠤࢀࢃ᷿ࠢ").format(bstack111l1ll1ll1_opy_.__name__, bstack111ll1ll1ll_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack111l1l11l11_opy_
    else:
        return decorator
def bstack1l111lll1l_opy_(bstack1lllll1lll1_opy_):
    if os.getenv(bstack11lllll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫḀ")) is not None:
        return bstack1ll1ll111_opy_(os.getenv(bstack11lllll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠬḁ")))
    if bstack11lllll_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧḂ") in bstack1lllll1lll1_opy_ and bstack111ll1ll11l_opy_(bstack1lllll1lll1_opy_[bstack11lllll_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨḃ")]):
        return False
    if bstack11lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧḄ") in bstack1lllll1lll1_opy_ and bstack111ll1ll11l_opy_(bstack1lllll1lll1_opy_[bstack11lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨḅ")]):
        return False
    return True
def bstack11l111l111_opy_():
    try:
        from pytest_bdd import reporting
        bstack111l11l11ll_opy_ = os.environ.get(bstack11lllll_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡕࡔࡇࡕࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠢḆ"), None)
        return bstack111l11l11ll_opy_ is None or bstack111l11l11ll_opy_ == bstack11lllll_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠧḇ")
    except Exception as e:
        return False
def bstack1l1llll111_opy_(hub_url, CONFIG):
    if bstack111l1ll1l_opy_() <= version.parse(bstack11lllll_opy_ (u"ࠩ࠶࠲࠶࠹࠮࠱ࠩḈ")):
        if hub_url:
            return bstack11lllll_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦḉ") + hub_url + bstack11lllll_opy_ (u"ࠦ࠿࠾࠰࠰ࡹࡧ࠳࡭ࡻࡢࠣḊ")
        return bstack11l11ll11l_opy_
    if hub_url:
        return bstack11lllll_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࠢḋ") + hub_url + bstack11lllll_opy_ (u"ࠨ࠯ࡸࡦ࠲࡬ࡺࡨࠢḌ")
    return bstack1ll1111l_opy_
def bstack111l111l111_opy_():
    return isinstance(os.getenv(bstack11lllll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐ࡚ࡖࡈࡗ࡙ࡥࡐࡍࡗࡊࡍࡓ࠭ḍ")), str)
def bstack11ll11l11l_opy_(url):
    return urlparse(url).hostname
def bstack1l11111lll_opy_(hostname):
    for bstack1l1ll11lll_opy_ in bstack1l1111l11_opy_:
        regex = re.compile(bstack1l1ll11lll_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack111ll1l11ll_opy_(bstack111l1lll1l1_opy_, file_name, logger):
    bstack1111l11ll_opy_ = os.path.join(os.path.expanduser(bstack11lllll_opy_ (u"ࠨࢀࠪḎ")), bstack111l1lll1l1_opy_)
    try:
        if not os.path.exists(bstack1111l11ll_opy_):
            os.makedirs(bstack1111l11ll_opy_)
        file_path = os.path.join(os.path.expanduser(bstack11lllll_opy_ (u"ࠩࢁࠫḏ")), bstack111l1lll1l1_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack11lllll_opy_ (u"ࠪࡻࠬḐ")):
                pass
            with open(file_path, bstack11lllll_opy_ (u"ࠦࡼ࠱ࠢḑ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack11l1llll_opy_.format(str(e)))
def bstack111l111l11l_opy_(file_name, key, value, logger):
    file_path = bstack111ll1l11ll_opy_(bstack11lllll_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬḒ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1ll1ll1l1_opy_ = json.load(open(file_path, bstack11lllll_opy_ (u"࠭ࡲࡣࠩḓ")))
        else:
            bstack1ll1ll1l1_opy_ = {}
        bstack1ll1ll1l1_opy_[key] = value
        with open(file_path, bstack11lllll_opy_ (u"ࠢࡸ࠭ࠥḔ")) as outfile:
            json.dump(bstack1ll1ll1l1_opy_, outfile)
def bstack1l1l1111l_opy_(file_name, logger):
    file_path = bstack111ll1l11ll_opy_(bstack11lllll_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨḕ"), file_name, logger)
    bstack1ll1ll1l1_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack11lllll_opy_ (u"ࠩࡵࠫḖ")) as bstack1111ll1l1_opy_:
            bstack1ll1ll1l1_opy_ = json.load(bstack1111ll1l1_opy_)
    return bstack1ll1ll1l1_opy_
def bstack1111lll11_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack11lllll_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡪࡥ࡭ࡧࡷ࡭ࡳ࡭ࠠࡧ࡫࡯ࡩ࠿ࠦࠧḗ") + file_path + bstack11lllll_opy_ (u"ࠫࠥ࠭Ḙ") + str(e))
def bstack111l1ll1l_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack11lllll_opy_ (u"ࠧࡂࡎࡐࡖࡖࡉ࡙ࡄࠢḙ")
def bstack1l1ll11ll_opy_(config):
    if bstack11lllll_opy_ (u"࠭ࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬḚ") in config:
        del (config[bstack11lllll_opy_ (u"ࠧࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ḛ")])
        return False
    if bstack111l1ll1l_opy_() < version.parse(bstack11lllll_opy_ (u"ࠨ࠵࠱࠸࠳࠶ࠧḜ")):
        return False
    if bstack111l1ll1l_opy_() >= version.parse(bstack11lllll_opy_ (u"ࠩ࠷࠲࠶࠴࠵ࠨḝ")):
        return True
    if bstack11lllll_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪḞ") in config and config[bstack11lllll_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫḟ")] is False:
        return False
    else:
        return True
def bstack111l111l1_opy_(args_list, bstack111l1lll1ll_opy_):
    index = -1
    for value in bstack111l1lll1ll_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
def bstack11l1l1l1lll_opy_(a, b):
  for k, v in b.items():
    if isinstance(v, dict) and k in a and isinstance(a[k], dict):
        bstack11l1l1l1lll_opy_(a[k], v)
    else:
        a[k] = v
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack1111ll11l1_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack1111ll11l1_opy_ = bstack1111ll11l1_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack11lllll_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬḠ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack11lllll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ḡ"), exception=exception)
    def bstack1llll1111ll_opy_(self):
        if self.result != bstack11lllll_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧḢ"):
            return None
        if isinstance(self.exception_type, str) and bstack11lllll_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࠦḣ") in self.exception_type:
            return bstack11lllll_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࡊࡸࡲࡰࡴࠥḤ")
        return bstack11lllll_opy_ (u"࡙ࠥࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠦḥ")
    def bstack111ll11lll1_opy_(self):
        if self.result != bstack11lllll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫḦ"):
            return None
        if self.bstack1111ll11l1_opy_:
            return self.bstack1111ll11l1_opy_
        return bstack111l11lll11_opy_(self.exception)
def bstack111l11lll11_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack111l1l11111_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack1l1ll1ll1_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack11lll111l_opy_(config, logger):
    try:
        import playwright
        bstack111l1l1l1l1_opy_ = playwright.__file__
        bstack111l1ll1l1l_opy_ = os.path.split(bstack111l1l1l1l1_opy_)
        bstack111ll11l1l1_opy_ = bstack111l1ll1l1l_opy_[0] + bstack11lllll_opy_ (u"ࠬ࠵ࡤࡳ࡫ࡹࡩࡷ࠵ࡰࡢࡥ࡮ࡥ࡬࡫࠯࡭࡫ࡥ࠳ࡨࡲࡩ࠰ࡥ࡯࡭࠳ࡰࡳࠨḧ")
        os.environ[bstack11lllll_opy_ (u"࠭ࡇࡍࡑࡅࡅࡑࡥࡁࡈࡇࡑࡘࡤࡎࡔࡕࡒࡢࡔࡗࡕࡘ࡚ࠩḨ")] = bstack1l1l1l1ll1_opy_(config)
        with open(bstack111ll11l1l1_opy_, bstack11lllll_opy_ (u"ࠧࡳࠩḩ")) as f:
            bstack1111lllll_opy_ = f.read()
            bstack111l1111l1l_opy_ = bstack11lllll_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬࠮ࡣࡪࡩࡳࡺࠧḪ")
            bstack111l11lllll_opy_ = bstack1111lllll_opy_.find(bstack111l1111l1l_opy_)
            if bstack111l11lllll_opy_ == -1:
              process = subprocess.Popen(bstack11lllll_opy_ (u"ࠤࡱࡴࡲࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡨ࡮ࡲࡦࡦࡲ࠭ࡢࡩࡨࡲࡹࠨḫ"), shell=True, cwd=bstack111l1ll1l1l_opy_[0])
              process.wait()
              bstack111l11ll1l1_opy_ = bstack11lllll_opy_ (u"ࠪࠦࡺࡹࡥࠡࡵࡷࡶ࡮ࡩࡴࠣ࠽ࠪḬ")
              bstack111l1l1l11l_opy_ = bstack11lllll_opy_ (u"ࠦࠧࠨࠠ࡝ࠤࡸࡷࡪࠦࡳࡵࡴ࡬ࡧࡹࡢࠢ࠼ࠢࡦࡳࡳࡹࡴࠡࡽࠣࡦࡴࡵࡴࡴࡶࡵࡥࡵࠦࡽࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࠬ࡭࡬ࡰࡤࡤࡰ࠲ࡧࡧࡦࡰࡷࠫ࠮ࡁࠠࡪࡨࠣࠬࡵࡸ࡯ࡤࡧࡶࡷ࠳࡫࡮ࡷ࠰ࡊࡐࡔࡈࡁࡍࡡࡄࡋࡊࡔࡔࡠࡊࡗࡘࡕࡥࡐࡓࡑ࡛࡝࠮ࠦࡢࡰࡱࡷࡷࡹࡸࡡࡱࠪࠬ࠿ࠥࠨࠢࠣḭ")
              bstack111ll1l1l1l_opy_ = bstack1111lllll_opy_.replace(bstack111l11ll1l1_opy_, bstack111l1l1l11l_opy_)
              with open(bstack111ll11l1l1_opy_, bstack11lllll_opy_ (u"ࠬࡽࠧḮ")) as f:
                f.write(bstack111ll1l1l1l_opy_)
    except Exception as e:
        logger.error(bstack1lllll11ll_opy_.format(str(e)))
def bstack11l1ll1l11_opy_():
  try:
    bstack111ll1111ll_opy_ = os.path.join(tempfile.gettempdir(), bstack11lllll_opy_ (u"࠭࡯ࡱࡶ࡬ࡱࡦࡲ࡟ࡩࡷࡥࡣࡺࡸ࡬࠯࡬ࡶࡳࡳ࠭ḯ"))
    bstack111l1l1ll1l_opy_ = []
    if os.path.exists(bstack111ll1111ll_opy_):
      with open(bstack111ll1111ll_opy_) as f:
        bstack111l1l1ll1l_opy_ = json.load(f)
      os.remove(bstack111ll1111ll_opy_)
    return bstack111l1l1ll1l_opy_
  except:
    pass
  return []
def bstack1llll11lll_opy_(bstack1l1l1l1l11_opy_):
  try:
    bstack111l1l1ll1l_opy_ = []
    bstack111ll1111ll_opy_ = os.path.join(tempfile.gettempdir(), bstack11lllll_opy_ (u"ࠧࡰࡲࡷ࡭ࡲࡧ࡬ࡠࡪࡸࡦࡤࡻࡲ࡭࠰࡭ࡷࡴࡴࠧḰ"))
    if os.path.exists(bstack111ll1111ll_opy_):
      with open(bstack111ll1111ll_opy_) as f:
        bstack111l1l1ll1l_opy_ = json.load(f)
    bstack111l1l1ll1l_opy_.append(bstack1l1l1l1l11_opy_)
    with open(bstack111ll1111ll_opy_, bstack11lllll_opy_ (u"ࠨࡹࠪḱ")) as f:
        json.dump(bstack111l1l1ll1l_opy_, f)
  except:
    pass
def bstack11l1lll1l_opy_(logger, bstack111lll11111_opy_ = False):
  try:
    test_name = os.environ.get(bstack11lllll_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕࡡࡗࡉࡘ࡚࡟ࡏࡃࡐࡉࠬḲ"), bstack11lllll_opy_ (u"ࠪࠫḳ"))
    if test_name == bstack11lllll_opy_ (u"ࠫࠬḴ"):
        test_name = threading.current_thread().__dict__.get(bstack11lllll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡇࡪࡤࡠࡶࡨࡷࡹࡥ࡮ࡢ࡯ࡨࠫḵ"), bstack11lllll_opy_ (u"࠭ࠧḶ"))
    bstack111l1ll111l_opy_ = bstack11lllll_opy_ (u"ࠧ࠭ࠢࠪḷ").join(threading.current_thread().bstackTestErrorMessages)
    if bstack111lll11111_opy_:
        bstack11111l111_opy_ = os.environ.get(bstack11lllll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨḸ"), bstack11lllll_opy_ (u"ࠩ࠳ࠫḹ"))
        bstack11l111ll1l_opy_ = {bstack11lllll_opy_ (u"ࠪࡲࡦࡳࡥࠨḺ"): test_name, bstack11lllll_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪḻ"): bstack111l1ll111l_opy_, bstack11lllll_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫḼ"): bstack11111l111_opy_}
        bstack1111lll1lll_opy_ = []
        bstack1111ll1ll1l_opy_ = os.path.join(tempfile.gettempdir(), bstack11lllll_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡰࡱࡲࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬḽ"))
        if os.path.exists(bstack1111ll1ll1l_opy_):
            with open(bstack1111ll1ll1l_opy_) as f:
                bstack1111lll1lll_opy_ = json.load(f)
        bstack1111lll1lll_opy_.append(bstack11l111ll1l_opy_)
        with open(bstack1111ll1ll1l_opy_, bstack11lllll_opy_ (u"ࠧࡸࠩḾ")) as f:
            json.dump(bstack1111lll1lll_opy_, f)
    else:
        bstack11l111ll1l_opy_ = {bstack11lllll_opy_ (u"ࠨࡰࡤࡱࡪ࠭ḿ"): test_name, bstack11lllll_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨṀ"): bstack111l1ll111l_opy_, bstack11lllll_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩṁ"): str(multiprocessing.current_process().name)}
        if bstack11lllll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴࠨṂ") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack11l111ll1l_opy_)
  except Exception as e:
      logger.warn(bstack11lllll_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡳࡷ࡫ࠠࡱࡻࡷࡩࡸࡺࠠࡧࡷࡱࡲࡪࡲࠠࡥࡣࡷࡥ࠿ࠦࡻࡾࠤṃ").format(e))
def bstack1lll11ll1_opy_(error_message, test_name, index, logger):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack11lllll_opy_ (u"࠭ࡦࡪ࡮ࡨࡰࡴࡩ࡫ࠡࡰࡲࡸࠥࡧࡶࡢ࡫࡯ࡥࡧࡲࡥ࠭ࠢࡸࡷ࡮ࡴࡧࠡࡤࡤࡷ࡮ࡩࠠࡧ࡫࡯ࡩࠥࡵࡰࡦࡴࡤࡸ࡮ࡵ࡮ࡴࠩṄ"))
    try:
      bstack111l11lll1l_opy_ = []
      bstack11l111ll1l_opy_ = {bstack11lllll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬṅ"): test_name, bstack11lllll_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧṆ"): error_message, bstack11lllll_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨṇ"): index}
      bstack1111lllllll_opy_ = os.path.join(tempfile.gettempdir(), bstack11lllll_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠴ࡪࡴࡱࡱࠫṈ"))
      if os.path.exists(bstack1111lllllll_opy_):
          with open(bstack1111lllllll_opy_) as f:
              bstack111l11lll1l_opy_ = json.load(f)
      bstack111l11lll1l_opy_.append(bstack11l111ll1l_opy_)
      with open(bstack1111lllllll_opy_, bstack11lllll_opy_ (u"ࠫࡼ࠭ṉ")) as f:
          json.dump(bstack111l11lll1l_opy_, f)
    except Exception as e:
      logger.warn(bstack11lllll_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡳࡷ࡫ࠠࡳࡱࡥࡳࡹࠦࡦࡶࡰࡱࡩࡱࠦࡤࡢࡶࡤ࠾ࠥࢁࡽࠣṊ").format(e))
    return
  bstack111l11lll1l_opy_ = []
  bstack11l111ll1l_opy_ = {bstack11lllll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫṋ"): test_name, bstack11lllll_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭Ṍ"): error_message, bstack11lllll_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧṍ"): index}
  bstack1111lllllll_opy_ = os.path.join(tempfile.gettempdir(), bstack11lllll_opy_ (u"ࠩࡵࡳࡧࡵࡴࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰࠪṎ"))
  lock_file = bstack1111lllllll_opy_ + bstack11lllll_opy_ (u"ࠪ࠲ࡱࡵࡣ࡬ࠩṏ")
  try:
    with FileLock(lock_file, timeout=10):
      if os.path.exists(bstack1111lllllll_opy_):
          with open(bstack1111lllllll_opy_, bstack11lllll_opy_ (u"ࠫࡷ࠭Ṑ")) as f:
              content = f.read().strip()
              if content:
                  bstack111l11lll1l_opy_ = json.load(open(bstack1111lllllll_opy_))
      bstack111l11lll1l_opy_.append(bstack11l111ll1l_opy_)
      with open(bstack1111lllllll_opy_, bstack11lllll_opy_ (u"ࠬࡽࠧṑ")) as f:
          json.dump(bstack111l11lll1l_opy_, f)
  except Exception as e:
    logger.warn(bstack11lllll_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡸࡴࡸࡥࠡࡴࡲࡦࡴࡺࠠࡧࡷࡱࡲࡪࡲࠠࡥࡣࡷࡥࠥࡽࡩࡵࡪࠣࡪ࡮ࡲࡥࠡ࡮ࡲࡧࡰ࡯࡮ࡨ࠼ࠣࡿࢂࠨṒ").format(e))
def bstack1lll1l1l1_opy_(bstack11l1lll1_opy_, name, logger):
  try:
    bstack11l111ll1l_opy_ = {bstack11lllll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬṓ"): name, bstack11lllll_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧṔ"): bstack11l1lll1_opy_, bstack11lllll_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨṕ"): str(threading.current_thread()._name)}
    return bstack11l111ll1l_opy_
  except Exception as e:
    logger.warn(bstack11lllll_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡱࡵࡩࠥࡨࡥࡩࡣࡹࡩࠥ࡬ࡵ࡯ࡰࡨࡰࠥࡪࡡࡵࡣ࠽ࠤࢀࢃࠢṖ").format(e))
  return
def bstack111ll1lllll_opy_():
    return platform.system() == bstack11lllll_opy_ (u"ࠫ࡜࡯࡮ࡥࡱࡺࡷࠬṗ")
def bstack1l1ll1ll_opy_(bstack111l11l111l_opy_, config, logger):
    bstack111l111111l_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack111l11l111l_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack11lllll_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡨ࡬ࡰࡹ࡫ࡲࠡࡥࡲࡲ࡫࡯ࡧࠡ࡭ࡨࡽࡸࠦࡢࡺࠢࡵࡩ࡬࡫ࡸࠡ࡯ࡤࡸࡨ࡮࠺ࠡࡽࢀࠦṘ").format(e))
    return bstack111l111111l_opy_
def bstack111ll1l11l1_opy_(bstack1111lll11ll_opy_, bstack111ll111l1l_opy_):
    bstack111l1llllll_opy_ = version.parse(bstack1111lll11ll_opy_)
    bstack111l1l11ll1_opy_ = version.parse(bstack111ll111l1l_opy_)
    if bstack111l1llllll_opy_ > bstack111l1l11ll1_opy_:
        return 1
    elif bstack111l1llllll_opy_ < bstack111l1l11ll1_opy_:
        return -1
    else:
        return 0
def bstack11111ll1ll_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack111ll1l111l_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
def bstack111l11l1111_opy_(framework):
    from browserstack_sdk._version import __version__
    return str(framework) + str(__version__)
def bstack1l1ll1ll11_opy_(options, framework, config, bstack1l1l111ll1_opy_={}):
    if options is None:
        return
    if getattr(options, bstack11lllll_opy_ (u"࠭ࡧࡦࡶࠪṙ"), None):
        caps = options
    else:
        caps = options.to_capabilities()
    bstack1ll1ll1l1l_opy_ = caps.get(bstack11lllll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨṚ"))
    bstack111l1111111_opy_ = True
    bstack111llllll1_opy_ = os.environ[bstack11lllll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ṛ")]
    bstack1l1ll11l1l1_opy_ = config.get(bstack11lllll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩṜ"), False)
    if bstack1l1ll11l1l1_opy_:
        bstack1ll1111111l_opy_ = config.get(bstack11lllll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪṝ"), {})
        bstack1ll1111111l_opy_[bstack11lllll_opy_ (u"ࠫࡦࡻࡴࡩࡖࡲ࡯ࡪࡴࠧṞ")] = os.getenv(bstack11lllll_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪṟ"))
        bstack11l1l11ll1l_opy_ = json.loads(os.getenv(bstack11lllll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧṠ"), bstack11lllll_opy_ (u"ࠧࡼࡿࠪṡ"))).get(bstack11lllll_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩṢ"))
    if bstack111ll1ll11l_opy_(caps.get(bstack11lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡷࡶࡩ࡜࠹ࡃࠨṣ"))) or bstack111ll1ll11l_opy_(caps.get(bstack11lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡸࡷࡪࡥࡷ࠴ࡥࠪṤ"))):
        bstack111l1111111_opy_ = False
    if bstack1l1ll11ll_opy_({bstack11lllll_opy_ (u"ࠦࡺࡹࡥࡘ࠵ࡆࠦṥ"): bstack111l1111111_opy_}):
        bstack1ll1ll1l1l_opy_ = bstack1ll1ll1l1l_opy_ or {}
        bstack1ll1ll1l1l_opy_[bstack11lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧṦ")] = bstack111l11l1111_opy_(framework)
        bstack1ll1ll1l1l_opy_[bstack11lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨṧ")] = bstack1l11llll111_opy_()
        bstack1ll1ll1l1l_opy_[bstack11lllll_opy_ (u"ࠧࡵࡧࡶࡸ࡭ࡻࡢࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪṨ")] = bstack111llllll1_opy_
        bstack1ll1ll1l1l_opy_[bstack11lllll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪṩ")] = bstack1l1l111ll1_opy_
        if bstack1l1ll11l1l1_opy_:
            bstack1ll1ll1l1l_opy_[bstack11lllll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩṪ")] = bstack1l1ll11l1l1_opy_
            bstack1ll1ll1l1l_opy_[bstack11lllll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪṫ")] = bstack1ll1111111l_opy_
            bstack1ll1ll1l1l_opy_[bstack11lllll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫṬ")][bstack11lllll_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ṭ")] = bstack11l1l11ll1l_opy_
        if getattr(options, bstack11lllll_opy_ (u"࠭ࡳࡦࡶࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹࡿࠧṮ"), None):
            options.set_capability(bstack11lllll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨṯ"), bstack1ll1ll1l1l_opy_)
        else:
            options[bstack11lllll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩṰ")] = bstack1ll1ll1l1l_opy_
    else:
        if getattr(options, bstack11lllll_opy_ (u"ࠩࡶࡩࡹࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵࡻࠪṱ"), None):
            options.set_capability(bstack11lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫṲ"), bstack111l11l1111_opy_(framework))
            options.set_capability(bstack11lllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬṳ"), bstack1l11llll111_opy_())
            options.set_capability(bstack11lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡹ࡫ࡳࡵࡪࡸࡦࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧṴ"), bstack111llllll1_opy_)
            options.set_capability(bstack11lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡵࡪ࡮ࡧࡔࡷࡵࡤࡶࡥࡷࡑࡦࡶࠧṵ"), bstack1l1l111ll1_opy_)
            if bstack1l1ll11l1l1_opy_:
                options.set_capability(bstack11lllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭Ṷ"), bstack1l1ll11l1l1_opy_)
                options.set_capability(bstack11lllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧṷ"), bstack1ll1111111l_opy_)
                options.set_capability(bstack11lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳ࠯ࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩṸ"), bstack11l1l11ll1l_opy_)
        else:
            options[bstack11lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫṹ")] = bstack111l11l1111_opy_(framework)
            options[bstack11lllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬṺ")] = bstack1l11llll111_opy_()
            options[bstack11lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡹ࡫ࡳࡵࡪࡸࡦࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧṻ")] = bstack111llllll1_opy_
            options[bstack11lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡵࡪ࡮ࡧࡔࡷࡵࡤࡶࡥࡷࡑࡦࡶࠧṼ")] = bstack1l1l111ll1_opy_
            if bstack1l1ll11l1l1_opy_:
                options[bstack11lllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ṽ")] = bstack1l1ll11l1l1_opy_
                options[bstack11lllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧṾ")] = bstack1ll1111111l_opy_
                options[bstack11lllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨṿ")][bstack11lllll_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫẀ")] = bstack11l1l11ll1l_opy_
    return options
def bstack111l1lll11l_opy_(bstack111l1l1l1ll_opy_, framework):
    bstack1l1l111ll1_opy_ = bstack1l111111_opy_.get_property(bstack11lllll_opy_ (u"ࠦࡕࡒࡁ࡚࡙ࡕࡍࡌࡎࡔࡠࡒࡕࡓࡉ࡛ࡃࡕࡡࡐࡅࡕࠨẁ"))
    if bstack111l1l1l1ll_opy_ and len(bstack111l1l1l1ll_opy_.split(bstack11lllll_opy_ (u"ࠬࡩࡡࡱࡵࡀࠫẂ"))) > 1:
        ws_url = bstack111l1l1l1ll_opy_.split(bstack11lllll_opy_ (u"࠭ࡣࡢࡲࡶࡁࠬẃ"))[0]
        if bstack11lllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪẄ") in ws_url:
            from browserstack_sdk._version import __version__
            bstack111l1llll11_opy_ = json.loads(urllib.parse.unquote(bstack111l1l1l1ll_opy_.split(bstack11lllll_opy_ (u"ࠨࡥࡤࡴࡸࡃࠧẅ"))[1]))
            bstack111l1llll11_opy_ = bstack111l1llll11_opy_ or {}
            bstack111llllll1_opy_ = os.environ[bstack11lllll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧẆ")]
            bstack111l1llll11_opy_[bstack11lllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫẇ")] = str(framework) + str(__version__)
            bstack111l1llll11_opy_[bstack11lllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬẈ")] = bstack1l11llll111_opy_()
            bstack111l1llll11_opy_[bstack11lllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡹ࡫ࡳࡵࡪࡸࡦࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧẉ")] = bstack111llllll1_opy_
            bstack111l1llll11_opy_[bstack11lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡵࡪ࡮ࡧࡔࡷࡵࡤࡶࡥࡷࡑࡦࡶࠧẊ")] = bstack1l1l111ll1_opy_
            bstack111l1l1l1ll_opy_ = bstack111l1l1l1ll_opy_.split(bstack11lllll_opy_ (u"ࠧࡤࡣࡳࡷࡂ࠭ẋ"))[0] + bstack11lllll_opy_ (u"ࠨࡥࡤࡴࡸࡃࠧẌ") + urllib.parse.quote(json.dumps(bstack111l1llll11_opy_))
    return bstack111l1l1l1ll_opy_
def bstack1ll11ll11_opy_():
    global bstack1l111111ll_opy_
    from playwright._impl._browser_type import BrowserType
    bstack1l111111ll_opy_ = BrowserType.connect
    return bstack1l111111ll_opy_
def bstack1l1ll1llll_opy_(framework_name):
    global bstack111ll1111_opy_
    bstack111ll1111_opy_ = framework_name
    return framework_name
def bstack1ll1l11l1l_opy_(self, *args, **kwargs):
    global bstack1l111111ll_opy_
    try:
        global bstack111ll1111_opy_
        if bstack11lllll_opy_ (u"ࠩࡺࡷࡊࡴࡤࡱࡱ࡬ࡲࡹ࠭ẍ") in kwargs:
            kwargs[bstack11lllll_opy_ (u"ࠪࡻࡸࡋ࡮ࡥࡲࡲ࡭ࡳࡺࠧẎ")] = bstack111l1lll11l_opy_(
                kwargs.get(bstack11lllll_opy_ (u"ࠫࡼࡹࡅ࡯ࡦࡳࡳ࡮ࡴࡴࠨẏ"), None),
                bstack111ll1111_opy_
            )
    except Exception as e:
        logger.error(bstack11lllll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡥ࡯ࠢࡳࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡓࡅࡍࠣࡧࡦࡶࡳ࠻ࠢࡾࢁࠧẐ").format(str(e)))
    return bstack1l111111ll_opy_(self, *args, **kwargs)
def bstack111l11l1l11_opy_(bstack111ll1lll1l_opy_, proxies):
    proxy_settings = {}
    try:
        if not proxies:
            proxies = bstack11l1l1111_opy_(bstack111ll1lll1l_opy_, bstack11lllll_opy_ (u"ࠨࠢẑ"))
        if proxies and proxies.get(bstack11lllll_opy_ (u"ࠢࡩࡶࡷࡴࡸࠨẒ")):
            parsed_url = urlparse(proxies.get(bstack11lllll_opy_ (u"ࠣࡪࡷࡸࡵࡹࠢẓ")))
            if parsed_url and parsed_url.hostname: proxy_settings[bstack11lllll_opy_ (u"ࠩࡳࡶࡴࡾࡹࡉࡱࡶࡸࠬẔ")] = str(parsed_url.hostname)
            if parsed_url and parsed_url.port: proxy_settings[bstack11lllll_opy_ (u"ࠪࡴࡷࡵࡸࡺࡒࡲࡶࡹ࠭ẕ")] = str(parsed_url.port)
            if parsed_url and parsed_url.username: proxy_settings[bstack11lllll_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡘࡷࡪࡸࠧẖ")] = str(parsed_url.username)
            if parsed_url and parsed_url.password: proxy_settings[bstack11lllll_opy_ (u"ࠬࡶࡲࡰࡺࡼࡔࡦࡹࡳࠨẗ")] = str(parsed_url.password)
        return proxy_settings
    except:
        return proxy_settings
def bstack1l1lll1111_opy_(bstack111ll1lll1l_opy_):
    bstack111lll111l1_opy_ = {
        bstack11l111lllll_opy_[bstack111lll1111l_opy_]: bstack111ll1lll1l_opy_[bstack111lll1111l_opy_]
        for bstack111lll1111l_opy_ in bstack111ll1lll1l_opy_
        if bstack111lll1111l_opy_ in bstack11l111lllll_opy_
    }
    bstack111lll111l1_opy_[bstack11lllll_opy_ (u"ࠨࡰࡳࡱࡻࡽࡘ࡫ࡴࡵ࡫ࡱ࡫ࡸࠨẘ")] = bstack111l11l1l11_opy_(bstack111ll1lll1l_opy_, bstack1l111111_opy_.get_property(bstack11lllll_opy_ (u"ࠢࡱࡴࡲࡼࡾ࡙ࡥࡵࡶ࡬ࡲ࡬ࡹࠢẙ")))
    bstack111l111l1ll_opy_ = [element.lower() for element in bstack111llllll11_opy_]
    bstack111ll11l1ll_opy_(bstack111lll111l1_opy_, bstack111l111l1ll_opy_)
    return bstack111lll111l1_opy_
def bstack111ll11l1ll_opy_(d, keys):
    for key in list(d.keys()):
        if key.lower() in keys:
            d[key] = bstack11lllll_opy_ (u"ࠣࠬ࠭࠮࠯ࠨẚ")
    for value in d.values():
        if isinstance(value, dict):
            bstack111ll11l1ll_opy_(value, keys)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    bstack111ll11l1ll_opy_(item, keys)
def bstack1l11lll1lll_opy_():
    bstack111l111ll1l_opy_ = [os.environ.get(bstack11lllll_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡌࡐࡊ࡙࡟ࡅࡋࡕࠦẛ")), os.path.join(os.path.expanduser(bstack11lllll_opy_ (u"ࠥࢂࠧẜ")), bstack11lllll_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫẝ")), os.path.join(bstack11lllll_opy_ (u"ࠬ࠵ࡴ࡮ࡲࠪẞ"), bstack11lllll_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ẟ"))]
    for path in bstack111l111ll1l_opy_:
        if path is None:
            continue
        try:
            if os.path.exists(path):
                logger.debug(bstack11lllll_opy_ (u"ࠢࡇ࡫࡯ࡩࠥ࠭ࠢẠ") + str(path) + bstack11lllll_opy_ (u"ࠣࠩࠣࡩࡽ࡯ࡳࡵࡵ࠱ࠦạ"))
                if not os.access(path, os.W_OK):
                    logger.debug(bstack11lllll_opy_ (u"ࠤࡊ࡭ࡻ࡯࡮ࡨࠢࡳࡩࡷࡳࡩࡴࡵ࡬ࡳࡳࡹࠠࡧࡱࡵࠤࠬࠨẢ") + str(path) + bstack11lllll_opy_ (u"ࠥࠫࠧả"))
                    os.chmod(path, 0o777)
                else:
                    logger.debug(bstack11lllll_opy_ (u"ࠦࡋ࡯࡬ࡦࠢࠪࠦẤ") + str(path) + bstack11lllll_opy_ (u"ࠧ࠭ࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡪࡤࡷࠥࡺࡨࡦࠢࡵࡩࡶࡻࡩࡳࡧࡧࠤࡵ࡫ࡲ࡮࡫ࡶࡷ࡮ࡵ࡮ࡴ࠰ࠥấ"))
            else:
                logger.debug(bstack11lllll_opy_ (u"ࠨࡃࡳࡧࡤࡸ࡮ࡴࡧࠡࡨ࡬ࡰࡪࠦࠧࠣẦ") + str(path) + bstack11lllll_opy_ (u"ࠢࠨࠢࡺ࡭ࡹ࡮ࠠࡸࡴ࡬ࡸࡪࠦࡰࡦࡴࡰ࡭ࡸࡹࡩࡰࡰ࠱ࠦầ"))
                os.makedirs(path, exist_ok=True)
                os.chmod(path, 0o777)
            logger.debug(bstack11lllll_opy_ (u"ࠣࡑࡳࡩࡷࡧࡴࡪࡱࡱࠤࡸࡻࡣࡤࡧࡨࡨࡪࡪࠠࡧࡱࡵࠤࠬࠨẨ") + str(path) + bstack11lllll_opy_ (u"ࠤࠪ࠲ࠧẩ"))
            return path
        except Exception as e:
            logger.debug(bstack11lllll_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࠣࡹࡵࠦࡦࡪ࡮ࡨࠤࠬࢁࡰࡢࡶ࡫ࢁࠬࡀࠠࠣẪ") + str(e) + bstack11lllll_opy_ (u"ࠦࠧẫ"))
    logger.debug(bstack11lllll_opy_ (u"ࠧࡇ࡬࡭ࠢࡳࡥࡹ࡮ࡳࠡࡨࡤ࡭ࡱ࡫ࡤ࠯ࠤẬ"))
    return None
@measure(event_name=EVENTS.bstack111lllll1ll_opy_, stage=STAGE.bstack1llll11111_opy_)
def bstack1ll111l1111_opy_(binary_path, bstack1ll111lll1l_opy_, bs_config):
    logger.debug(bstack11lllll_opy_ (u"ࠨࡃࡶࡴࡵࡩࡳࡺࠠࡄࡎࡌࠤࡕࡧࡴࡩࠢࡩࡳࡺࡴࡤ࠻ࠢࡾࢁࠧậ").format(binary_path))
    bstack111ll1ll1l1_opy_ = bstack11lllll_opy_ (u"ࠧࠨẮ")
    bstack111l11l1lll_opy_ = {
        bstack11lllll_opy_ (u"ࠨࡵࡧ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ắ"): __version__,
        bstack11lllll_opy_ (u"ࠤࡲࡷࠧẰ"): platform.system(),
        bstack11lllll_opy_ (u"ࠥࡳࡸࡥࡡࡳࡥ࡫ࠦằ"): platform.machine(),
        bstack11lllll_opy_ (u"ࠦࡨࡲࡩࡠࡸࡨࡶࡸ࡯࡯࡯ࠤẲ"): bstack11lllll_opy_ (u"ࠬ࠶ࠧẳ"),
        bstack11lllll_opy_ (u"ࠨࡳࡥ࡭ࡢࡰࡦࡴࡧࡶࡣࡪࡩࠧẴ"): bstack11lllll_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧẵ")
    }
    bstack111l1111lll_opy_(bstack111l11l1lll_opy_)
    try:
        if binary_path:
            if bstack111ll1lllll_opy_():
                bstack111l11l1lll_opy_[bstack11lllll_opy_ (u"ࠨࡥ࡯࡭ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭Ặ")] = subprocess.check_output([binary_path, bstack11lllll_opy_ (u"ࠤࡹࡩࡷࡹࡩࡰࡰࠥặ")]).strip().decode(bstack11lllll_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩẸ"))
            else:
                bstack111l11l1lll_opy_[bstack11lllll_opy_ (u"ࠫࡨࡲࡩࡠࡸࡨࡶࡸ࡯࡯࡯ࠩẹ")] = subprocess.check_output([binary_path, bstack11lllll_opy_ (u"ࠧࡼࡥࡳࡵ࡬ࡳࡳࠨẺ")], stderr=subprocess.DEVNULL).strip().decode(bstack11lllll_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬẻ"))
        response = requests.request(
            bstack11lllll_opy_ (u"ࠧࡈࡇࡗࠫẼ"),
            url=bstack1l11l11ll_opy_(bstack11l1111ll11_opy_),
            headers=None,
            auth=(bs_config[bstack11lllll_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪẽ")], bs_config[bstack11lllll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬẾ")]),
            json=None,
            params=bstack111l11l1lll_opy_
        )
        data = response.json()
        if response.status_code == 200 and bstack11lllll_opy_ (u"ࠪࡹࡷࡲࠧế") in data.keys() and bstack11lllll_opy_ (u"ࠫࡺࡶࡤࡢࡶࡨࡨࡤࡩ࡬ࡪࡡࡹࡩࡷࡹࡩࡰࡰࠪỀ") in data.keys():
            logger.debug(bstack11lllll_opy_ (u"ࠧࡔࡥࡦࡦࠣࡸࡴࠦࡵࡱࡦࡤࡸࡪࠦࡢࡪࡰࡤࡶࡾ࠲ࠠࡤࡷࡵࡶࡪࡴࡴࠡࡤ࡬ࡲࡦࡸࡹࠡࡸࡨࡶࡸ࡯࡯࡯࠼ࠣࡿࢂࠨề").format(bstack111l11l1lll_opy_[bstack11lllll_opy_ (u"࠭ࡣ࡭࡫ࡢࡺࡪࡸࡳࡪࡱࡱࠫỂ")]))
            if bstack11lllll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡊࡐࡄࡖ࡞ࡥࡕࡓࡎࠪể") in os.environ:
                logger.debug(bstack11lllll_opy_ (u"ࠣࡕ࡮࡭ࡵࡶࡩ࡯ࡩࠣࡦ࡮ࡴࡡࡳࡻࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠥࡧࡳࠡࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡋࡑࡅࡗ࡟࡟ࡖࡔࡏࠤ࡮ࡹࠠࡴࡧࡷࠦỄ"))
                data[bstack11lllll_opy_ (u"ࠩࡸࡶࡱ࠭ễ")] = os.environ[bstack11lllll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅࡍࡓࡇࡒ࡚ࡡࡘࡖࡑ࠭Ệ")]
            bstack111l1l1llll_opy_ = bstack111l1ll1111_opy_(data[bstack11lllll_opy_ (u"ࠫࡺࡸ࡬ࠨệ")], bstack1ll111lll1l_opy_)
            bstack111ll1ll1l1_opy_ = os.path.join(bstack1ll111lll1l_opy_, bstack111l1l1llll_opy_)
            os.chmod(bstack111ll1ll1l1_opy_, 0o777) # bstack111l1l1ll11_opy_ permission
            return bstack111ll1ll1l1_opy_
    except Exception as e:
        logger.debug(bstack11lllll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡨࡴࡽ࡮࡭ࡱࡤࡨ࡮ࡴࡧࠡࡰࡨࡻ࡙ࠥࡄࡌࠢࡾࢁࠧỈ").format(e))
    return binary_path
def bstack111l1111lll_opy_(bstack111l11l1lll_opy_):
    try:
        if bstack11lllll_opy_ (u"࠭࡬ࡪࡰࡸࡼࠬỉ") not in bstack111l11l1lll_opy_[bstack11lllll_opy_ (u"ࠧࡰࡵࠪỊ")].lower():
            return
        if os.path.exists(bstack11lllll_opy_ (u"ࠣ࠱ࡨࡸࡨ࠵࡯ࡴ࠯ࡵࡩࡱ࡫ࡡࡴࡧࠥị")):
            with open(bstack11lllll_opy_ (u"ࠤ࠲ࡩࡹࡩ࠯ࡰࡵ࠰ࡶࡪࡲࡥࡢࡵࡨࠦỌ"), bstack11lllll_opy_ (u"ࠥࡶࠧọ")) as f:
                bstack111l1l1111l_opy_ = {}
                for line in f:
                    if bstack11lllll_opy_ (u"ࠦࡂࠨỎ") in line:
                        key, value = line.rstrip().split(bstack11lllll_opy_ (u"ࠧࡃࠢỏ"), 1)
                        bstack111l1l1111l_opy_[key] = value.strip(bstack11lllll_opy_ (u"࠭ࠢ࡝ࠩࠪỐ"))
                bstack111l11l1lll_opy_[bstack11lllll_opy_ (u"ࠧࡥ࡫ࡶࡸࡷࡵࠧố")] = bstack111l1l1111l_opy_.get(bstack11lllll_opy_ (u"ࠣࡋࡇࠦỒ"), bstack11lllll_opy_ (u"ࠤࠥồ"))
        elif os.path.exists(bstack11lllll_opy_ (u"ࠥ࠳ࡪࡺࡣ࠰ࡣ࡯ࡴ࡮ࡴࡥ࠮ࡴࡨࡰࡪࡧࡳࡦࠤỔ")):
            bstack111l11l1lll_opy_[bstack11lllll_opy_ (u"ࠫࡩ࡯ࡳࡵࡴࡲࠫổ")] = bstack11lllll_opy_ (u"ࠬࡧ࡬ࡱ࡫ࡱࡩࠬỖ")
    except Exception as e:
        logger.debug(bstack11lllll_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡪࡩࡹࠦࡤࡪࡵࡷࡶࡴࠦ࡯ࡧࠢ࡯࡭ࡳࡻࡸࠣỗ") + e)
@measure(event_name=EVENTS.bstack11l111lll1l_opy_, stage=STAGE.bstack1llll11111_opy_)
def bstack111l1ll1111_opy_(bstack111l11l1ll1_opy_, bstack111l111lll1_opy_):
    logger.debug(bstack11lllll_opy_ (u"ࠢࡅࡱࡺࡲࡱࡵࡡࡥ࡫ࡱ࡫࡙ࠥࡄࡌࠢࡥ࡭ࡳࡧࡲࡺࠢࡩࡶࡴࡳ࠺ࠡࠤỘ") + str(bstack111l11l1ll1_opy_) + bstack11lllll_opy_ (u"ࠣࠤộ"))
    zip_path = os.path.join(bstack111l111lll1_opy_, bstack11lllll_opy_ (u"ࠤࡧࡳࡼࡴ࡬ࡰࡣࡧࡩࡩࡥࡦࡪ࡮ࡨ࠲ࡿ࡯ࡰࠣỚ"))
    bstack111l1l1llll_opy_ = bstack11lllll_opy_ (u"ࠪࠫớ")
    with requests.get(bstack111l11l1ll1_opy_, stream=True) as response:
        response.raise_for_status()
        with open(zip_path, bstack11lllll_opy_ (u"ࠦࡼࡨࠢỜ")) as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        logger.debug(bstack11lllll_opy_ (u"ࠧࡌࡩ࡭ࡧࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࡪࡪࠠࡴࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࡰࡾ࠴ࠢờ"))
    with zipfile.ZipFile(zip_path, bstack11lllll_opy_ (u"࠭ࡲࠨỞ")) as zip_ref:
        bstack1111lll1ll1_opy_ = zip_ref.namelist()
        if len(bstack1111lll1ll1_opy_) > 0:
            bstack111l1l1llll_opy_ = bstack1111lll1ll1_opy_[0] # bstack111l1111ll1_opy_ bstack11l11111lll_opy_ will be bstack111l1l111ll_opy_ 1 file i.e. the binary in the zip
        zip_ref.extractall(bstack111l111lll1_opy_)
        logger.debug(bstack11lllll_opy_ (u"ࠢࡇ࡫࡯ࡩࡸࠦࡳࡶࡥࡦࡩࡸࡹࡦࡶ࡮࡯ࡽࠥ࡫ࡸࡵࡴࡤࡧࡹ࡫ࡤࠡࡶࡲࠤࠬࠨở") + str(bstack111l111lll1_opy_) + bstack11lllll_opy_ (u"ࠣࠩࠥỠ"))
    os.remove(zip_path)
    return bstack111l1l1llll_opy_
def get_cli_dir():
    bstack111l1lll111_opy_ = bstack1l11lll1lll_opy_()
    if bstack111l1lll111_opy_:
        bstack1ll111lll1l_opy_ = os.path.join(bstack111l1lll111_opy_, bstack11lllll_opy_ (u"ࠤࡦࡰ࡮ࠨỡ"))
        if not os.path.exists(bstack1ll111lll1l_opy_):
            os.makedirs(bstack1ll111lll1l_opy_, mode=0o777, exist_ok=True)
        return bstack1ll111lll1l_opy_
    else:
        raise FileNotFoundError(bstack11lllll_opy_ (u"ࠥࡒࡴࠦࡷࡳ࡫ࡷࡥࡧࡲࡥࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼࠤࡦࡼࡡࡪ࡮ࡤࡦࡱ࡫ࠠࡧࡱࡵࠤࡹ࡮ࡥࠡࡕࡇࡏࠥࡨࡩ࡯ࡣࡵࡽ࠳ࠨỢ"))
def bstack1ll11ll111l_opy_(bstack1ll111lll1l_opy_):
    bstack11lllll_opy_ (u"ࠦࠧࠨࡇࡦࡶࠣࡸ࡭࡫ࠠࡱࡣࡷ࡬ࠥ࡬࡯ࡳࠢࡷ࡬ࡪࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯࡙ࠥࡄࡌࠢࡥ࡭ࡳࡧࡲࡺࠢ࡬ࡲࠥࡧࠠࡸࡴ࡬ࡸࡦࡨ࡬ࡦࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽ࠳ࠨࠢࠣợ")
    bstack111ll111lll_opy_ = [
        os.path.join(bstack1ll111lll1l_opy_, f)
        for f in os.listdir(bstack1ll111lll1l_opy_)
        if os.path.isfile(os.path.join(bstack1ll111lll1l_opy_, f)) and f.startswith(bstack11lllll_opy_ (u"ࠧࡨࡩ࡯ࡣࡵࡽ࠲ࠨỤ"))
    ]
    if len(bstack111ll111lll_opy_) > 0:
        return max(bstack111ll111lll_opy_, key=os.path.getmtime) # get bstack111ll1l1111_opy_ binary
    return bstack11lllll_opy_ (u"ࠨࠢụ")
def bstack11l1l111l11_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1l1lll11l11_opy_(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = bstack1l1lll11l11_opy_(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack1lll1l111_opy_(data, keys, default=None):
    bstack11lllll_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࡔࡣࡩࡩࡱࡿࠠࡨࡧࡷࠤࡦࠦ࡮ࡦࡵࡷࡩࡩࠦࡶࡢ࡮ࡸࡩࠥ࡬ࡲࡰ࡯ࠣࡥࠥࡪࡩࡤࡶ࡬ࡳࡳࡧࡲࡺࠢࡲࡶࠥࡲࡩࡴࡶ࠱ࠎࠥࠦࠠࠡ࠼ࡳࡥࡷࡧ࡭ࠡࡦࡤࡸࡦࡀࠠࡕࡪࡨࠤࡩ࡯ࡣࡵ࡫ࡲࡲࡦࡸࡹࠡࡱࡵࠤࡱ࡯ࡳࡵࠢࡷࡳࠥࡺࡲࡢࡸࡨࡶࡸ࡫࠮ࠋࠢࠣࠤࠥࡀࡰࡢࡴࡤࡱࠥࡱࡥࡺࡵ࠽ࠤࡆࠦ࡬ࡪࡵࡷࠤࡴ࡬ࠠ࡬ࡧࡼࡷ࠴࡯࡮ࡥ࡫ࡦࡩࡸࠦࡲࡦࡲࡵࡩࡸ࡫࡮ࡵ࡫ࡱ࡫ࠥࡺࡨࡦࠢࡳࡥࡹ࡮࠮ࠋࠢࠣࠤࠥࡀࡰࡢࡴࡤࡱࠥࡪࡥࡧࡣࡸࡰࡹࡀࠠࡗࡣ࡯ࡹࡪࠦࡴࡰࠢࡵࡩࡹࡻࡲ࡯ࠢ࡬ࡪࠥࡺࡨࡦࠢࡳࡥࡹ࡮ࠠࡥࡱࡨࡷࠥࡴ࡯ࡵࠢࡨࡼ࡮ࡹࡴ࠯ࠌࠣࠤࠥࠦ࠺ࡳࡧࡷࡹࡷࡴ࠺ࠡࡖ࡫ࡩࠥࡼࡡ࡭ࡷࡨࠤࡦࡺࠠࡵࡪࡨࠤࡳ࡫ࡳࡵࡧࡧࠤࡵࡧࡴࡩ࠮ࠣࡳࡷࠦࡤࡦࡨࡤࡹࡱࡺࠠࡪࡨࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩ࠴ࠊࠡࠢࠣࠤࠧࠨࠢỦ")
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
def bstack1l1l1111_opy_(bstack111l1l1lll1_opy_, key, value):
    bstack11lllll_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡕࡷࡳࡷ࡫ࠠࡄࡎࡌࠤࡪࡴࡶࡪࡴࡲࡲࡲ࡫࡮ࡵࠢࡹࡥࡷ࡯ࡡࡣ࡮ࡨࡷࠥࡳࡡࡱࡲ࡬ࡲ࡬ࠦࡩ࡯ࠢࡷ࡬ࡪࠦࡰࡳࡱࡹ࡭ࡩ࡫ࡤࠡࡦ࡬ࡧࡹ࡯࡯࡯ࡣࡵࡽ࠳ࠐࠠࠡࠢࠣࡅࡷ࡭ࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡧࡱ࡯࡟ࡦࡰࡹࡣࡻࡧࡲࡴࡡࡰࡥࡵࡀࠠࡅ࡫ࡦࡸ࡮ࡵ࡮ࡢࡴࡼࠤࡹࡵࠠࡴࡶࡲࡶࡪࠦࡥ࡯ࡸ࡬ࡶࡴࡴ࡭ࡦࡰࡷࠤࡻࡧࡲࡪࡣࡥࡰࡪࠦ࡭ࡢࡲࡳ࡭ࡳ࡭ࡳࠋࠢࠣࠤࠥࠦࠠࠡࠢ࡮ࡩࡾࡀࠠࡌࡧࡼࠤ࡫ࡸ࡯࡮ࠢࡆࡐࡎࡥࡃࡂࡒࡖࡣ࡙ࡕ࡟ࡄࡑࡑࡊࡎࡍࠊࠡࠢࠣࠤࠥࠦࠠࠡࡸࡤࡰࡺ࡫࠺ࠡࡘࡤࡰࡺ࡫ࠠࡧࡴࡲࡱࠥࡩ࡯࡮࡯ࡤࡲࡩࠦ࡬ࡪࡰࡨࠤࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠊࠡࠢࠣࠤࠧࠨࠢủ")
    if key in bstack1ll1ll1ll1_opy_:
        bstack1l1ll111l_opy_ = bstack1ll1ll1ll1_opy_[key]
        if isinstance(bstack1l1ll111l_opy_, list):
            for env_name in bstack1l1ll111l_opy_:
                bstack111l1l1lll1_opy_[env_name] = value
        else:
            bstack111l1l1lll1_opy_[bstack1l1ll111l_opy_] = value