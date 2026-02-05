# coding: UTF-8
import sys
bstack11111l_opy_ = sys.version_info [0] == 2
bstack1111_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack11l1ll1_opy_ (bstack111ll_opy_):
    global bstack11lll11_opy_
    bstack11111l1_opy_ = ord (bstack111ll_opy_ [-1])
    bstack1l11l1l_opy_ = bstack111ll_opy_ [:-1]
    bstack1111l1_opy_ = bstack11111l1_opy_ % len (bstack1l11l1l_opy_)
    bstack111ll1_opy_ = bstack1l11l1l_opy_ [:bstack1111l1_opy_] + bstack1l11l1l_opy_ [bstack1111l1_opy_:]
    if bstack11111l_opy_:
        bstack1llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    else:
        bstack1llll1_opy_ = str () .join ([chr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    return eval (bstack1llll1_opy_)
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
from bstack_utils.constants import (bstack1ll1111l_opy_, bstack111ll1l1l_opy_, bstack1lll1111l_opy_,
                                    bstack11l11111lll_opy_, bstack11l1111l111_opy_, bstack11l111l11ll_opy_, bstack11l11l11l11_opy_)
from bstack_utils.measure import measure
from bstack_utils.messages import bstack1l111l1111_opy_, bstack11lllll1ll_opy_
from bstack_utils.proxy import bstack11l1lll111_opy_, bstack11l11lll1l_opy_
from bstack_utils.constants import *
from bstack_utils import bstack1l1111l1l_opy_
from bstack_utils.bstack1111l111l_opy_ import bstack11l1l1ll11_opy_
from browserstack_sdk._version import __version__
bstack11lll111l_opy_ = Config.bstack1l11l11l1_opy_()
logger = bstack1l1111l1l_opy_.get_logger(__name__, bstack1l1111l1l_opy_.bstack1lll111l11l_opy_())
bstack11llll111_opy_ = bstack1l1111l1l_opy_.bstack11l1111l11_opy_(__name__)
def bstack11l1l1l111l_opy_(config):
    return config[bstack11l1ll1_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ᱁")]
def bstack11l1ll11111_opy_(config):
    return config[bstack11l1ll1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭᱂")]
def bstack1ll1111ll1_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack111l1l11ll1_opy_(obj):
    values = []
    bstack1111lll1l1l_opy_ = re.compile(bstack11l1ll1_opy_ (u"ࡶࠧࡤࡃࡖࡕࡗࡓࡒࡥࡔࡂࡉࡢࡠࡩ࠱ࠤࠣ᱃"), re.I)
    for key in obj.keys():
        if bstack1111lll1l1l_opy_.match(key):
            values.append(obj[key])
    return values
def bstack111l1ll1l1l_opy_(config):
    tags = []
    tags.extend(bstack111l1l11ll1_opy_(os.environ))
    tags.extend(bstack111l1l11ll1_opy_(config))
    return tags
def bstack111l111llll_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack111ll1ll1ll_opy_(bstack1111llll11l_opy_):
    if not bstack1111llll11l_opy_:
        return bstack11l1ll1_opy_ (u"ࠬ࠭᱄")
    return bstack11l1ll1_opy_ (u"ࠨࡻࡾࠢࠫࡿࢂ࠯ࠢ᱅").format(bstack1111llll11l_opy_.name, bstack1111llll11l_opy_.email)
def bstack11l1ll11lll_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack1111lll11ll_opy_ = repo.common_dir
        info = {
            bstack11l1ll1_opy_ (u"ࠢࡴࡪࡤࠦ᱆"): repo.head.commit.hexsha,
            bstack11l1ll1_opy_ (u"ࠣࡵ࡫ࡳࡷࡺ࡟ࡴࡪࡤࠦ᱇"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack11l1ll1_opy_ (u"ࠤࡥࡶࡦࡴࡣࡩࠤ᱈"): repo.active_branch.name,
            bstack11l1ll1_opy_ (u"ࠥࡸࡦ࡭ࠢ᱉"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack11l1ll1_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡸࡪࡸࠢ᱊"): bstack111ll1ll1ll_opy_(repo.head.commit.committer),
            bstack11l1ll1_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡹ࡫ࡲࡠࡦࡤࡸࡪࠨ᱋"): repo.head.commit.committed_datetime.isoformat(),
            bstack11l1ll1_opy_ (u"ࠨࡡࡶࡶ࡫ࡳࡷࠨ᱌"): bstack111ll1ll1ll_opy_(repo.head.commit.author),
            bstack11l1ll1_opy_ (u"ࠢࡢࡷࡷ࡬ࡴࡸ࡟ࡥࡣࡷࡩࠧᱍ"): repo.head.commit.authored_datetime.isoformat(),
            bstack11l1ll1_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡠ࡯ࡨࡷࡸࡧࡧࡦࠤᱎ"): repo.head.commit.message,
            bstack11l1ll1_opy_ (u"ࠤࡵࡳࡴࡺࠢᱏ"): repo.git.rev_parse(bstack11l1ll1_opy_ (u"ࠥ࠱࠲ࡹࡨࡰࡹ࠰ࡸࡴࡶ࡬ࡦࡸࡨࡰࠧ᱐")),
            bstack11l1ll1_opy_ (u"ࠦࡨࡵ࡭࡮ࡱࡱࡣ࡬࡯ࡴࡠࡦ࡬ࡶࠧ᱑"): bstack1111lll11ll_opy_,
            bstack11l1ll1_opy_ (u"ࠧࡽ࡯ࡳ࡭ࡷࡶࡪ࡫࡟ࡨ࡫ࡷࡣࡩ࡯ࡲࠣ᱒"): subprocess.check_output([bstack11l1ll1_opy_ (u"ࠨࡧࡪࡶࠥ᱓"), bstack11l1ll1_opy_ (u"ࠢࡳࡧࡹ࠱ࡵࡧࡲࡴࡧࠥ᱔"), bstack11l1ll1_opy_ (u"ࠣ࠯࠰࡫࡮ࡺ࠭ࡤࡱࡰࡱࡴࡴ࠭ࡥ࡫ࡵࠦ᱕")]).strip().decode(
                bstack11l1ll1_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨ᱖")),
            bstack11l1ll1_opy_ (u"ࠥࡰࡦࡹࡴࡠࡶࡤ࡫ࠧ᱗"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack11l1ll1_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡷࡤࡹࡩ࡯ࡥࡨࡣࡱࡧࡳࡵࡡࡷࡥ࡬ࠨ᱘"): repo.git.rev_list(
                bstack11l1ll1_opy_ (u"ࠧࢁࡽ࠯࠰ࡾࢁࠧ᱙").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack111l11ll1ll_opy_ = []
        for remote in remotes:
            bstack1111lll1lll_opy_ = {
                bstack11l1ll1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᱚ"): remote.name,
                bstack11l1ll1_opy_ (u"ࠢࡶࡴ࡯ࠦᱛ"): remote.url,
            }
            bstack111l11ll1ll_opy_.append(bstack1111lll1lll_opy_)
        bstack1111llll111_opy_ = {
            bstack11l1ll1_opy_ (u"ࠣࡰࡤࡱࡪࠨᱜ"): bstack11l1ll1_opy_ (u"ࠤࡪ࡭ࡹࠨᱝ"),
            **info,
            bstack11l1ll1_opy_ (u"ࠥࡶࡪࡳ࡯ࡵࡧࡶࠦᱞ"): bstack111l11ll1ll_opy_
        }
        bstack1111llll111_opy_ = bstack111ll1l1lll_opy_(bstack1111llll111_opy_)
        return bstack1111llll111_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack11l1ll1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡴࡶࡵ࡭ࡣࡷ࡭ࡳ࡭ࠠࡈ࡫ࡷࠤࡲ࡫ࡴࡢࡦࡤࡸࡦࠦࡷࡪࡶ࡫ࠤࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠢᱟ").format(err))
        return {}
def bstack111ll1ll1l1_opy_(bstack111l11111ll_opy_=None):
    bstack11l1ll1_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࡍࡥࡵࠢࡪ࡭ࡹࠦ࡭ࡦࡶࡤࡨࡦࡺࡡࠡࡵࡳࡩࡨ࡯ࡦࡪࡥࡤࡰࡱࡿࠠࡧࡱࡵࡱࡦࡺࡴࡦࡦࠣࡪࡴࡸࠠࡂࡋࠣࡷࡪࡲࡥࡤࡶ࡬ࡳࡳࠦࡵࡴࡧࠣࡧࡦࡹࡥࡴࠢࡩࡳࡷࠦࡥࡢࡥ࡫ࠤ࡫ࡵ࡬ࡥࡧࡵࠤ࡮ࡴࠠࡵࡪࡨࠤࡱ࡯ࡳࡵ࠰ࠍࠤࠥࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡧࡱ࡯ࡨࡪࡸࡳࠡࠪ࡯࡭ࡸࡺࠬࠡࡱࡳࡸ࡮ࡵ࡮ࡢ࡮ࠬ࠾ࠥࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡎࡰࡰࡨ࠾ࠥࡓ࡯࡯ࡱ࠰ࡶࡪࡶ࡯ࠡࡣࡳࡴࡷࡵࡡࡤࡪ࠯ࠤࡺࡹࡥࡴࠢࡦࡹࡷࡸࡥ࡯ࡶࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾ࡛ࠦࡰࡵ࠱࡫ࡪࡺࡣࡸࡦࠫ࠭ࡢࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡅ࡮ࡲࡷࡽࠥࡲࡩࡴࡶࠣ࡟ࡢࡀࠠࡎࡷ࡯ࡸ࡮࠳ࡲࡦࡲࡲࠤࡦࡶࡰࡳࡱࡤࡧ࡭ࠦࡷࡪࡶ࡫ࠤࡳࡵࠠࡴࡱࡸࡶࡨ࡫ࡳࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡨࡨ࠱ࠦࡲࡦࡶࡸࡶࡳࡹࠠ࡜࡟ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡐ࡮ࡹࡴࠡࡱࡩࠤࡵࡧࡴࡩࡵ࠽ࠤࡒࡻ࡬ࡵ࡫࠰ࡶࡪࡶ࡯ࠡࡣࡳࡴࡷࡵࡡࡤࡪࠣࡻ࡮ࡺࡨࠡࡵࡳࡩࡨ࡯ࡦࡪࡥࠣࡪࡴࡲࡤࡦࡴࡶࠤࡹࡵࠠࡢࡰࡤࡰࡾࢀࡥࠋࠢࠣࠤࠥࡘࡥࡵࡷࡵࡲࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡ࡮࡬ࡷࡹࡀࠠࡍ࡫ࡶࡸࠥࡵࡦࠡࡦ࡬ࡧࡹࡹࠬࠡࡧࡤࡧ࡭ࠦࡣࡰࡰࡷࡥ࡮ࡴࡩ࡯ࡩࠣ࡫࡮ࡺࠠ࡮ࡧࡷࡥࡩࡧࡴࡢࠢࡩࡳࡷࠦࡡࠡࡨࡲࡰࡩ࡫ࡲ࠯ࠌࠣࠤࠥࠦࠢࠣࠤᱠ")
    if bstack111l11111ll_opy_ is None:
        bstack111l11111ll_opy_ = [os.getcwd()]
    elif isinstance(bstack111l11111ll_opy_, list) and len(bstack111l11111ll_opy_) == 0:
        return []
    results = []
    for folder in bstack111l11111ll_opy_:
        try:
            if not os.path.exists(folder):
                raise Exception(bstack11l1ll1_opy_ (u"ࠨࡆࡰ࡮ࡧࡩࡷࠦࡤࡰࡧࡶࠤࡳࡵࡴࠡࡧࡻ࡭ࡸࡺ࠺ࠡࡽࢀࠦᱡ").format(folder))
            repo = git.Repo(folder, search_parent_directories=True)
            result = {
                bstack11l1ll1_opy_ (u"ࠢࡱࡴࡌࡨࠧᱢ"): bstack11l1ll1_opy_ (u"ࠣࠤᱣ"),
                bstack11l1ll1_opy_ (u"ࠤࡩ࡭ࡱ࡫ࡳࡄࡪࡤࡲ࡬࡫ࡤࠣᱤ"): [],
                bstack11l1ll1_opy_ (u"ࠥࡥࡺࡺࡨࡰࡴࡶࠦᱥ"): [],
                bstack11l1ll1_opy_ (u"ࠦࡵࡸࡄࡢࡶࡨࠦᱦ"): bstack11l1ll1_opy_ (u"ࠧࠨᱧ"),
                bstack11l1ll1_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡓࡥࡴࡵࡤ࡫ࡪࡹࠢᱨ"): [],
                bstack11l1ll1_opy_ (u"ࠢࡱࡴࡗ࡭ࡹࡲࡥࠣᱩ"): bstack11l1ll1_opy_ (u"ࠣࠤᱪ"),
                bstack11l1ll1_opy_ (u"ࠤࡳࡶࡉ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠤᱫ"): bstack11l1ll1_opy_ (u"ࠥࠦᱬ"),
                bstack11l1ll1_opy_ (u"ࠦࡵࡸࡒࡢࡹࡇ࡭࡫࡬ࠢᱭ"): bstack11l1ll1_opy_ (u"ࠧࠨᱮ")
            }
            bstack111l1l1llll_opy_ = repo.active_branch.name
            bstack111l11l11ll_opy_ = repo.head.commit
            result[bstack11l1ll1_opy_ (u"ࠨࡰࡳࡋࡧࠦᱯ")] = bstack111l11l11ll_opy_.hexsha
            bstack111l1ll11l1_opy_ = _111l11lll1l_opy_(repo)
            logger.debug(bstack11l1ll1_opy_ (u"ࠢࡃࡣࡶࡩࠥࡨࡲࡢࡰࡦ࡬ࠥ࡬࡯ࡳࠢࡦࡳࡲࡶࡡࡳ࡫ࡶࡳࡳࡀࠠࠣᱰ") + str(bstack111l1ll11l1_opy_) + bstack11l1ll1_opy_ (u"ࠣࠤᱱ"))
            if bstack111l1ll11l1_opy_:
                try:
                    bstack111lll1l1l1_opy_ = repo.git.diff(bstack11l1ll1_opy_ (u"ࠤ࠰࠱ࡳࡧ࡭ࡦ࠯ࡲࡲࡱࡿࠢᱲ"), bstack1ll1ll11l1l_opy_ (u"ࠥࡿࡧࡧࡳࡦࡡࡥࡶࡦࡴࡣࡩࡿ࠱࠲࠳ࢁࡣࡶࡴࡵࡩࡳࡺ࡟ࡣࡴࡤࡲࡨ࡮ࡽࠣᱳ")).split(bstack11l1ll1_opy_ (u"ࠫࡡࡴࠧᱴ"))
                    logger.debug(bstack11l1ll1_opy_ (u"ࠧࡉࡨࡢࡰࡪࡩࡩࠦࡦࡪ࡮ࡨࡷࠥࡨࡥࡵࡹࡨࡩࡳࠦࡻࡣࡣࡶࡩࡤࡨࡲࡢࡰࡦ࡬ࢂࠦࡡ࡯ࡦࠣࡿࡨࡻࡲࡳࡧࡱࡸࡤࡨࡲࡢࡰࡦ࡬ࢂࡀࠠࠣᱵ") + str(bstack111lll1l1l1_opy_) + bstack11l1ll1_opy_ (u"ࠨࠢᱶ"))
                    result[bstack11l1ll1_opy_ (u"ࠢࡧ࡫࡯ࡩࡸࡉࡨࡢࡰࡪࡩࡩࠨᱷ")] = [f.strip() for f in bstack111lll1l1l1_opy_ if f.strip()]
                    commits = list(repo.iter_commits(bstack1ll1ll11l1l_opy_ (u"ࠣࡽࡥࡥࡸ࡫࡟ࡣࡴࡤࡲࡨ࡮ࡽ࠯࠰ࡾࡧࡺࡸࡲࡦࡰࡷࡣࡧࡸࡡ࡯ࡥ࡫ࢁࠧᱸ")))
                except Exception:
                    logger.debug(bstack11l1ll1_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡭ࡥࡵࠢࡦ࡬ࡦࡴࡧࡦࡦࠣࡪ࡮ࡲࡥࡴࠢࡩࡶࡴࡳࠠࡣࡴࡤࡲࡨ࡮ࠠࡤࡱࡰࡴࡦࡸࡩࡴࡱࡱ࠲ࠥࡌࡡ࡭࡮࡬ࡲ࡬ࠦࡢࡢࡥ࡮ࠤࡹࡵࠠࡳࡧࡦࡩࡳࡺࠠࡤࡱࡰࡱ࡮ࡺࡳ࠯ࠤᱹ"))
                    commits = list(repo.iter_commits(max_count=10))
                    if commits:
                        result[bstack11l1ll1_opy_ (u"ࠥࡪ࡮ࡲࡥࡴࡅ࡫ࡥࡳ࡭ࡥࡥࠤᱺ")] = _111l1l11l1l_opy_(commits[:5])
            else:
                commits = list(repo.iter_commits(max_count=10))
                if commits:
                    result[bstack11l1ll1_opy_ (u"ࠦ࡫࡯࡬ࡦࡵࡆ࡬ࡦࡴࡧࡦࡦࠥᱻ")] = _111l1l11l1l_opy_(commits[:5])
            bstack111l11ll1l1_opy_ = set()
            bstack111ll11ll11_opy_ = []
            for commit in commits:
                logger.debug(bstack11l1ll1_opy_ (u"ࠧࡖࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡦࡳࡲࡳࡩࡵ࠼ࠣࠦᱼ") + str(commit.message) + bstack11l1ll1_opy_ (u"ࠨࠢᱽ"))
                bstack111l11ll11l_opy_ = commit.author.name if commit.author else bstack11l1ll1_opy_ (u"ࠢࡖࡰ࡮ࡲࡴࡽ࡮ࠣ᱾")
                bstack111l11ll1l1_opy_.add(bstack111l11ll11l_opy_)
                bstack111ll11ll11_opy_.append({
                    bstack11l1ll1_opy_ (u"ࠣ࡯ࡨࡷࡸࡧࡧࡦࠤ᱿"): commit.message.strip(),
                    bstack11l1ll1_opy_ (u"ࠤࡸࡷࡪࡸࠢᲀ"): bstack111l11ll11l_opy_
                })
            result[bstack11l1ll1_opy_ (u"ࠥࡥࡺࡺࡨࡰࡴࡶࠦᲁ")] = list(bstack111l11ll1l1_opy_)
            result[bstack11l1ll1_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡑࡪࡹࡳࡢࡩࡨࡷࠧᲂ")] = bstack111ll11ll11_opy_
            result[bstack11l1ll1_opy_ (u"ࠧࡶࡲࡅࡣࡷࡩࠧᲃ")] = bstack111l11l11ll_opy_.committed_datetime.strftime(bstack11l1ll1_opy_ (u"ࠨ࡚ࠥ࠯ࠨࡱ࠲ࠫࡤࠣᲄ"))
            if (not result[bstack11l1ll1_opy_ (u"ࠢࡱࡴࡗ࡭ࡹࡲࡥࠣᲅ")] or result[bstack11l1ll1_opy_ (u"ࠣࡲࡵࡘ࡮ࡺ࡬ࡦࠤᲆ")].strip() == bstack11l1ll1_opy_ (u"ࠤࠥᲇ")) and bstack111l11l11ll_opy_.message:
                bstack111l1l1111l_opy_ = bstack111l11l11ll_opy_.message.strip().splitlines()
                result[bstack11l1ll1_opy_ (u"ࠥࡴࡷ࡚ࡩࡵ࡮ࡨࠦᲈ")] = bstack111l1l1111l_opy_[0] if bstack111l1l1111l_opy_ else bstack11l1ll1_opy_ (u"ࠦࠧᲉ")
                if len(bstack111l1l1111l_opy_) > 2:
                    result[bstack11l1ll1_opy_ (u"ࠧࡶࡲࡅࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠧᲊ")] = bstack11l1ll1_opy_ (u"࠭࡜࡯ࠩ᲋").join(bstack111l1l1111l_opy_[2:]).strip()
            results.append(result)
        except Exception as err:
            logger.error(bstack11l1ll1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡰࡲࡸࡰࡦࡺࡩ࡯ࡩࠣࡋ࡮ࡺࠠ࡮ࡧࡷࡥࡩࡧࡴࡢࠢࡩࡳࡷࠦࡁࡊࠢࡶࡩࡱ࡫ࡣࡵ࡫ࡲࡲࠥ࠮ࡦࡰ࡮ࡧࡩࡷࡀࠠࡼࡿࠬ࠾ࠥࢁࡽࠡ࠯ࠣࡿࢂࠨ᲌").format(
                folder,
                type(err).__name__,
                str(err)
            ))
    filtered_results = [
        result
        for result in results
        if _111l1l1ll1l_opy_(result)
    ]
    return filtered_results
def _111l1l1ll1l_opy_(result):
    bstack11l1ll1_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡊࡨࡰࡵ࡫ࡲࠡࡶࡲࠤࡨ࡮ࡥࡤ࡭ࠣ࡭࡫ࠦࡡࠡࡩ࡬ࡸࠥࡳࡥࡵࡣࡧࡥࡹࡧࠠࡳࡧࡶࡹࡱࡺࠠࡪࡵࠣࡺࡦࡲࡩࡥࠢࠫࡲࡴࡴ࠭ࡦ࡯ࡳࡸࡾࠦࡦࡪ࡮ࡨࡷࡈ࡮ࡡ࡯ࡩࡨࡨࠥࡧ࡮ࡥࠢࡤࡹࡹ࡮࡯ࡳࡵࠬ࠲ࠏࠦࠠࠡࠢࠥࠦࠧ᲍")
    return (
        isinstance(result.get(bstack11l1ll1_opy_ (u"ࠤࡩ࡭ࡱ࡫ࡳࡄࡪࡤࡲ࡬࡫ࡤࠣ᲎"), None), list)
        and len(result[bstack11l1ll1_opy_ (u"ࠥࡪ࡮ࡲࡥࡴࡅ࡫ࡥࡳ࡭ࡥࡥࠤ᲏")]) > 0
        and isinstance(result.get(bstack11l1ll1_opy_ (u"ࠦࡦࡻࡴࡩࡱࡵࡷࠧᲐ"), None), list)
        and len(result[bstack11l1ll1_opy_ (u"ࠧࡧࡵࡵࡪࡲࡶࡸࠨᲑ")]) > 0
    )
def _111l11lll1l_opy_(repo):
    bstack11l1ll1_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡔࡳࡻࠣࡸࡴࠦࡤࡦࡶࡨࡶࡲ࡯࡮ࡦࠢࡷ࡬ࡪࠦࡢࡢࡵࡨࠤࡧࡸࡡ࡯ࡥ࡫ࠤ࡫ࡵࡲࠡࡶ࡫ࡩࠥ࡭ࡩࡷࡧࡱࠤࡷ࡫ࡰࡰࠢࡺ࡭ࡹ࡮࡯ࡶࡶࠣ࡬ࡦࡸࡤࡤࡱࡧࡩࡩࠦ࡮ࡢ࡯ࡨࡷࠥࡧ࡮ࡥࠢࡺࡳࡷࡱࠠࡸ࡫ࡷ࡬ࠥࡧ࡬࡭࡙ࠢࡇࡘࠦࡰࡳࡱࡹ࡭ࡩ࡫ࡲࡴ࠰ࠍࠤࠥࠦࠠࡓࡧࡷࡹࡷࡴࡳࠡࡶ࡫ࡩࠥࡪࡥࡧࡣࡸࡰࡹࠦࡢࡳࡣࡱࡧ࡭ࠦࡩࡧࠢࡳࡳࡸࡹࡩࡣ࡮ࡨ࠰ࠥ࡫࡬ࡴࡧࠣࡒࡴࡴࡥ࠯ࠌࠣࠤࠥࠦࠢࠣࠤᲒ")
    try:
        try:
            origin = repo.remotes.origin
            bstack111l11l1lll_opy_ = origin.refs[bstack11l1ll1_opy_ (u"ࠧࡉࡇࡄࡈࠬᲓ")]
            target = bstack111l11l1lll_opy_.reference.name
            if target.startswith(bstack11l1ll1_opy_ (u"ࠨࡱࡵ࡭࡬࡯࡮࠰ࠩᲔ")):
                return target
        except Exception:
            pass
        if repo.remotes and repo.remotes.origin.refs:
            for ref in repo.remotes.origin.refs:
                if ref.name.startswith(bstack11l1ll1_opy_ (u"ࠩࡲࡶ࡮࡭ࡩ࡯࠱ࠪᲕ")):
                    return ref.name
        if repo.heads:
            return repo.heads[0].name
    except Exception:
        pass
    return None
def _111l1l11l1l_opy_(commits):
    bstack11l1ll1_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࡋࡪࡺࠠ࡭࡫ࡶࡸࠥࡵࡦࠡࡥ࡫ࡥࡳ࡭ࡥࡥࠢࡩ࡭ࡱ࡫ࡳࠡࡨࡵࡳࡲࠦࡡࠡ࡮࡬ࡷࡹࠦ࡯ࡧࠢࡦࡳࡲࡳࡩࡵࡵ࠱ࠎࠥࠦࠠࠡࠤࠥࠦᲖ")
    bstack111lll1l1l1_opy_ = set()
    try:
        for commit in commits:
            if commit.parents:
                for parent in commit.parents:
                    diff = commit.diff(parent)
                    for bstack111l1l1lll1_opy_ in diff:
                        if bstack111l1l1lll1_opy_.a_path:
                            bstack111lll1l1l1_opy_.add(bstack111l1l1lll1_opy_.a_path)
                        if bstack111l1l1lll1_opy_.b_path:
                            bstack111lll1l1l1_opy_.add(bstack111l1l1lll1_opy_.b_path)
    except Exception:
        pass
    return list(bstack111lll1l1l1_opy_)
def bstack111ll1l1lll_opy_(bstack1111llll111_opy_):
    bstack111l11l111l_opy_ = bstack111ll11lll1_opy_(bstack1111llll111_opy_)
    if bstack111l11l111l_opy_ and bstack111l11l111l_opy_ > bstack11l11111lll_opy_:
        bstack111lll11l1l_opy_ = bstack111l11l111l_opy_ - bstack11l11111lll_opy_
        bstack111ll1l11l1_opy_ = bstack111l1l11111_opy_(bstack1111llll111_opy_[bstack11l1ll1_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡣࡲ࡫ࡳࡴࡣࡪࡩࠧᲗ")], bstack111lll11l1l_opy_)
        bstack1111llll111_opy_[bstack11l1ll1_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡤࡳࡥࡴࡵࡤ࡫ࡪࠨᲘ")] = bstack111ll1l11l1_opy_
        logger.info(bstack11l1ll1_opy_ (u"ࠨࡔࡩࡧࠣࡧࡴࡳ࡭ࡪࡶࠣ࡬ࡦࡹࠠࡣࡧࡨࡲࠥࡺࡲࡶࡰࡦࡥࡹ࡫ࡤ࠯ࠢࡖ࡭ࡿ࡫ࠠࡰࡨࠣࡧࡴࡳ࡭ࡪࡶࠣࡥ࡫ࡺࡥࡳࠢࡷࡶࡺࡴࡣࡢࡶ࡬ࡳࡳࠦࡩࡴࠢࡾࢁࠥࡑࡂࠣᲙ")
                    .format(bstack111ll11lll1_opy_(bstack1111llll111_opy_) / 1024))
    return bstack1111llll111_opy_
def bstack111ll11lll1_opy_(bstack1l1ll1ll11_opy_):
    try:
        if bstack1l1ll1ll11_opy_:
            bstack111ll1111ll_opy_ = json.dumps(bstack1l1ll1ll11_opy_)
            bstack111l1lll1l1_opy_ = sys.getsizeof(bstack111ll1111ll_opy_)
            return bstack111l1lll1l1_opy_
    except Exception as e:
        logger.debug(bstack11l1ll1_opy_ (u"ࠢࡔࡱࡰࡩࡹ࡮ࡩ࡯ࡩࠣࡻࡪࡴࡴࠡࡹࡵࡳࡳ࡭ࠠࡸࡪ࡬ࡰࡪࠦࡣࡢ࡮ࡦࡹࡱࡧࡴࡪࡰࡪࠤࡸ࡯ࡺࡦࠢࡲࡪࠥࡐࡓࡐࡐࠣࡳࡧࡰࡥࡤࡶ࠽ࠤࢀࢃࠢᲚ").format(e))
    return -1
def bstack111l1l11111_opy_(field, bstack111ll111l1l_opy_):
    try:
        bstack111lll11ll1_opy_ = len(bytes(bstack11l1111l111_opy_, bstack11l1ll1_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧᲛ")))
        bstack111l1ll111l_opy_ = bytes(field, bstack11l1ll1_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨᲜ"))
        bstack111l1l111ll_opy_ = len(bstack111l1ll111l_opy_)
        bstack111l1111ll1_opy_ = ceil(bstack111l1l111ll_opy_ - bstack111ll111l1l_opy_ - bstack111lll11ll1_opy_)
        if bstack111l1111ll1_opy_ > 0:
            bstack111l1111lll_opy_ = bstack111l1ll111l_opy_[:bstack111l1111ll1_opy_].decode(bstack11l1ll1_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩᲝ"), errors=bstack11l1ll1_opy_ (u"ࠫ࡮࡭࡮ࡰࡴࡨࠫᲞ")) + bstack11l1111l111_opy_
            return bstack111l1111lll_opy_
    except Exception as e:
        logger.debug(bstack11l1ll1_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡸࡷࡻ࡮ࡤࡣࡷ࡭ࡳ࡭ࠠࡧ࡫ࡨࡰࡩ࠲ࠠ࡯ࡱࡷ࡬࡮ࡴࡧࠡࡹࡤࡷࠥࡺࡲࡶࡰࡦࡥࡹ࡫ࡤࠡࡪࡨࡶࡪࡀࠠࡼࡿࠥᲟ").format(e))
    return field
def bstack11l1lll11l_opy_():
    env = os.environ
    if (bstack11l1ll1_opy_ (u"ࠨࡊࡆࡐࡎࡍࡓ࡙࡟ࡖࡔࡏࠦᲠ") in env and len(env[bstack11l1ll1_opy_ (u"ࠢࡋࡇࡑࡏࡎࡔࡓࡠࡗࡕࡐࠧᲡ")]) > 0) or (
            bstack11l1ll1_opy_ (u"ࠣࡌࡈࡒࡐࡏࡎࡔࡡࡋࡓࡒࡋࠢᲢ") in env and len(env[bstack11l1ll1_opy_ (u"ࠤࡍࡉࡓࡑࡉࡏࡕࡢࡌࡔࡓࡅࠣᲣ")]) > 0):
        return {
            bstack11l1ll1_opy_ (u"ࠥࡲࡦࡳࡥࠣᲤ"): bstack11l1ll1_opy_ (u"ࠦࡏ࡫࡮࡬࡫ࡱࡷࠧᲥ"),
            bstack11l1ll1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᲦ"): env.get(bstack11l1ll1_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤᲧ")),
            bstack11l1ll1_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᲨ"): env.get(bstack11l1ll1_opy_ (u"ࠣࡌࡒࡆࡤࡔࡁࡎࡇࠥᲩ")),
            bstack11l1ll1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᲪ"): env.get(bstack11l1ll1_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤᲫ"))
        }
    if env.get(bstack11l1ll1_opy_ (u"ࠦࡈࡏࠢᲬ")) == bstack11l1ll1_opy_ (u"ࠧࡺࡲࡶࡧࠥᲭ") and bstack1ll1lll1l_opy_(env.get(bstack11l1ll1_opy_ (u"ࠨࡃࡊࡔࡆࡐࡊࡉࡉࠣᲮ"))):
        return {
            bstack11l1ll1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᲯ"): bstack11l1ll1_opy_ (u"ࠣࡅ࡬ࡶࡨࡲࡥࡄࡋࠥᲰ"),
            bstack11l1ll1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᲱ"): env.get(bstack11l1ll1_opy_ (u"ࠥࡇࡎࡘࡃࡍࡇࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨᲲ")),
            bstack11l1ll1_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᲳ"): env.get(bstack11l1ll1_opy_ (u"ࠧࡉࡉࡓࡅࡏࡉࡤࡐࡏࡃࠤᲴ")),
            bstack11l1ll1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᲵ"): env.get(bstack11l1ll1_opy_ (u"ࠢࡄࡋࡕࡇࡑࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࠥᲶ"))
        }
    if env.get(bstack11l1ll1_opy_ (u"ࠣࡅࡌࠦᲷ")) == bstack11l1ll1_opy_ (u"ࠤࡷࡶࡺ࡫ࠢᲸ") and bstack1ll1lll1l_opy_(env.get(bstack11l1ll1_opy_ (u"ࠥࡘࡗࡇࡖࡊࡕࠥᲹ"))):
        return {
            bstack11l1ll1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᲺ"): bstack11l1ll1_opy_ (u"࡚ࠧࡲࡢࡸ࡬ࡷࠥࡉࡉࠣ᲻"),
            bstack11l1ll1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ᲼"): env.get(bstack11l1ll1_opy_ (u"ࠢࡕࡔࡄ࡚ࡎ࡙࡟ࡃࡗࡌࡐࡉࡥࡗࡆࡄࡢ࡙ࡗࡒࠢᲽ")),
            bstack11l1ll1_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᲾ"): env.get(bstack11l1ll1_opy_ (u"ࠤࡗࡖࡆ࡜ࡉࡔࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦᲿ")),
            bstack11l1ll1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ᳀"): env.get(bstack11l1ll1_opy_ (u"࡙ࠦࡘࡁࡗࡋࡖࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥ᳁"))
        }
    if env.get(bstack11l1ll1_opy_ (u"ࠧࡉࡉࠣ᳂")) == bstack11l1ll1_opy_ (u"ࠨࡴࡳࡷࡨࠦ᳃") and env.get(bstack11l1ll1_opy_ (u"ࠢࡄࡋࡢࡒࡆࡓࡅࠣ᳄")) == bstack11l1ll1_opy_ (u"ࠣࡥࡲࡨࡪࡹࡨࡪࡲࠥ᳅"):
        return {
            bstack11l1ll1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᳆"): bstack11l1ll1_opy_ (u"ࠥࡇࡴࡪࡥࡴࡪ࡬ࡴࠧ᳇"),
            bstack11l1ll1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ᳈"): None,
            bstack11l1ll1_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ᳉"): None,
            bstack11l1ll1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ᳊"): None
        }
    if env.get(bstack11l1ll1_opy_ (u"ࠢࡃࡋࡗࡆ࡚ࡉࡋࡆࡖࡢࡆࡗࡇࡎࡄࡊࠥ᳋")) and env.get(bstack11l1ll1_opy_ (u"ࠣࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡈࡕࡍࡎࡋࡗࠦ᳌")):
        return {
            bstack11l1ll1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᳍"): bstack11l1ll1_opy_ (u"ࠥࡆ࡮ࡺࡢࡶࡥ࡮ࡩࡹࠨ᳎"),
            bstack11l1ll1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ᳏"): env.get(bstack11l1ll1_opy_ (u"ࠧࡈࡉࡕࡄࡘࡇࡐࡋࡔࡠࡉࡌࡘࡤࡎࡔࡕࡒࡢࡓࡗࡏࡇࡊࡐࠥ᳐")),
            bstack11l1ll1_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ᳑"): None,
            bstack11l1ll1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ᳒"): env.get(bstack11l1ll1_opy_ (u"ࠣࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥ᳓"))
        }
    if env.get(bstack11l1ll1_opy_ (u"ࠤࡆࡍ᳔ࠧ")) == bstack11l1ll1_opy_ (u"ࠥࡸࡷࡻࡥ᳕ࠣ") and bstack1ll1lll1l_opy_(env.get(bstack11l1ll1_opy_ (u"ࠦࡉࡘࡏࡏࡇ᳖ࠥ"))):
        return {
            bstack11l1ll1_opy_ (u"ࠧࡴࡡ࡮ࡧ᳗ࠥ"): bstack11l1ll1_opy_ (u"ࠨࡄࡳࡱࡱࡩ᳘ࠧ"),
            bstack11l1ll1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮᳙ࠥ"): env.get(bstack11l1ll1_opy_ (u"ࠣࡆࡕࡓࡓࡋ࡟ࡃࡗࡌࡐࡉࡥࡌࡊࡐࡎࠦ᳚")),
            bstack11l1ll1_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ᳛"): None,
            bstack11l1ll1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ᳜"): env.get(bstack11l1ll1_opy_ (u"ࠦࡉࡘࡏࡏࡇࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤ᳝"))
        }
    if env.get(bstack11l1ll1_opy_ (u"ࠧࡉࡉ᳞ࠣ")) == bstack11l1ll1_opy_ (u"ࠨࡴࡳࡷࡨ᳟ࠦ") and bstack1ll1lll1l_opy_(env.get(bstack11l1ll1_opy_ (u"ࠢࡔࡇࡐࡅࡕࡎࡏࡓࡇࠥ᳠"))):
        return {
            bstack11l1ll1_opy_ (u"ࠣࡰࡤࡱࡪࠨ᳡"): bstack11l1ll1_opy_ (u"ࠤࡖࡩࡲࡧࡰࡩࡱࡵࡩ᳢ࠧ"),
            bstack11l1ll1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ᳣"): env.get(bstack11l1ll1_opy_ (u"ࠦࡘࡋࡍࡂࡒࡋࡓࡗࡋ࡟ࡐࡔࡊࡅࡓࡏ࡚ࡂࡖࡌࡓࡓࡥࡕࡓࡎ᳤ࠥ")),
            bstack11l1ll1_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫᳥ࠢ"): env.get(bstack11l1ll1_opy_ (u"ࠨࡓࡆࡏࡄࡔࡍࡕࡒࡆࡡࡍࡓࡇࡥࡎࡂࡏࡈ᳦ࠦ")),
            bstack11l1ll1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ᳧"): env.get(bstack11l1ll1_opy_ (u"ࠣࡕࡈࡑࡆࡖࡈࡐࡔࡈࡣࡏࡕࡂࡠࡋࡇ᳨ࠦ"))
        }
    if env.get(bstack11l1ll1_opy_ (u"ࠤࡆࡍࠧᳩ")) == bstack11l1ll1_opy_ (u"ࠥࡸࡷࡻࡥࠣᳪ") and bstack1ll1lll1l_opy_(env.get(bstack11l1ll1_opy_ (u"ࠦࡌࡏࡔࡍࡃࡅࡣࡈࡏࠢᳫ"))):
        return {
            bstack11l1ll1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᳬ"): bstack11l1ll1_opy_ (u"ࠨࡇࡪࡶࡏࡥࡧࠨ᳭"),
            bstack11l1ll1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᳮ"): env.get(bstack11l1ll1_opy_ (u"ࠣࡅࡌࡣࡏࡕࡂࡠࡗࡕࡐࠧᳯ")),
            bstack11l1ll1_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᳰ"): env.get(bstack11l1ll1_opy_ (u"ࠥࡇࡎࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣᳱ")),
            bstack11l1ll1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᳲ"): env.get(bstack11l1ll1_opy_ (u"ࠧࡉࡉࡠࡌࡒࡆࡤࡏࡄࠣᳳ"))
        }
    if env.get(bstack11l1ll1_opy_ (u"ࠨࡃࡊࠤ᳴")) == bstack11l1ll1_opy_ (u"ࠢࡵࡴࡸࡩࠧᳵ") and bstack1ll1lll1l_opy_(env.get(bstack11l1ll1_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࠦᳶ"))):
        return {
            bstack11l1ll1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᳷"): bstack11l1ll1_opy_ (u"ࠥࡆࡺ࡯࡬ࡥ࡭࡬ࡸࡪࠨ᳸"),
            bstack11l1ll1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ᳹"): env.get(bstack11l1ll1_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦᳺ")),
            bstack11l1ll1_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ᳻"): env.get(bstack11l1ll1_opy_ (u"ࠢࡃࡗࡌࡐࡉࡑࡉࡕࡇࡢࡐࡆࡈࡅࡍࠤ᳼")) or env.get(bstack11l1ll1_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࡣࡕࡏࡐࡆࡎࡌࡒࡊࡥࡎࡂࡏࡈࠦ᳽")),
            bstack11l1ll1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ᳾"): env.get(bstack11l1ll1_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡍࡌࡘࡊࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧ᳿"))
        }
    if bstack1ll1lll1l_opy_(env.get(bstack11l1ll1_opy_ (u"࡙ࠦࡌ࡟ࡃࡗࡌࡐࡉࠨᴀ"))):
        return {
            bstack11l1ll1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᴁ"): bstack11l1ll1_opy_ (u"ࠨࡖࡪࡵࡸࡥࡱࠦࡓࡵࡷࡧ࡭ࡴࠦࡔࡦࡣࡰࠤࡘ࡫ࡲࡷ࡫ࡦࡩࡸࠨᴂ"),
            bstack11l1ll1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᴃ"): bstack11l1ll1_opy_ (u"ࠣࡽࢀࡿࢂࠨᴄ").format(env.get(bstack11l1ll1_opy_ (u"ࠩࡖ࡝ࡘ࡚ࡅࡎࡡࡗࡉࡆࡓࡆࡐࡗࡑࡈࡆ࡚ࡉࡐࡐࡖࡉࡗ࡜ࡅࡓࡗࡕࡍࠬᴅ")), env.get(bstack11l1ll1_opy_ (u"ࠪࡗ࡞࡙ࡔࡆࡏࡢࡘࡊࡇࡍࡑࡔࡒࡎࡊࡉࡔࡊࡆࠪᴆ"))),
            bstack11l1ll1_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᴇ"): env.get(bstack11l1ll1_opy_ (u"࡙࡙ࠧࡔࡖࡈࡑࡤࡊࡅࡇࡋࡑࡍ࡙ࡏࡏࡏࡋࡇࠦᴈ")),
            bstack11l1ll1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᴉ"): env.get(bstack11l1ll1_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡎࡊࠢᴊ"))
        }
    if bstack1ll1lll1l_opy_(env.get(bstack11l1ll1_opy_ (u"ࠣࡃࡓࡔ࡛ࡋ࡙ࡐࡔࠥᴋ"))):
        return {
            bstack11l1ll1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᴌ"): bstack11l1ll1_opy_ (u"ࠥࡅࡵࡶࡶࡦࡻࡲࡶࠧᴍ"),
            bstack11l1ll1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᴎ"): bstack11l1ll1_opy_ (u"ࠧࢁࡽ࠰ࡲࡵࡳ࡯࡫ࡣࡵ࠱ࡾࢁ࠴ࢁࡽ࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࡽࢀࠦᴏ").format(env.get(bstack11l1ll1_opy_ (u"࠭ࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡗࡕࡐࠬᴐ")), env.get(bstack11l1ll1_opy_ (u"ࠧࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡄࡇࡈࡕࡕࡏࡖࡢࡒࡆࡓࡅࠨᴑ")), env.get(bstack11l1ll1_opy_ (u"ࠨࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡔࡗࡕࡊࡆࡅࡗࡣࡘࡒࡕࡈࠩᴒ")), env.get(bstack11l1ll1_opy_ (u"ࠩࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡇ࡛ࡉࡍࡆࡢࡍࡉ࠭ᴓ"))),
            bstack11l1ll1_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᴔ"): env.get(bstack11l1ll1_opy_ (u"ࠦࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣᴕ")),
            bstack11l1ll1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᴖ"): env.get(bstack11l1ll1_opy_ (u"ࠨࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢᴗ"))
        }
    if env.get(bstack11l1ll1_opy_ (u"ࠢࡂ࡜ࡘࡖࡊࡥࡈࡕࡖࡓࡣ࡚࡙ࡅࡓࡡࡄࡋࡊࡔࡔࠣᴘ")) and env.get(bstack11l1ll1_opy_ (u"ࠣࡖࡉࡣࡇ࡛ࡉࡍࡆࠥᴙ")):
        return {
            bstack11l1ll1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᴚ"): bstack11l1ll1_opy_ (u"ࠥࡅࡿࡻࡲࡦࠢࡆࡍࠧᴛ"),
            bstack11l1ll1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᴜ"): bstack11l1ll1_opy_ (u"ࠧࢁࡽࡼࡿ࠲ࡣࡧࡻࡩ࡭ࡦ࠲ࡶࡪࡹࡵ࡭ࡶࡶࡃࡧࡻࡩ࡭ࡦࡌࡨࡂࢁࡽࠣᴝ").format(env.get(bstack11l1ll1_opy_ (u"࠭ࡓ࡚ࡕࡗࡉࡒࡥࡔࡆࡃࡐࡊࡔ࡛ࡎࡅࡃࡗࡍࡔࡔࡓࡆࡔ࡙ࡉࡗ࡛ࡒࡊࠩᴞ")), env.get(bstack11l1ll1_opy_ (u"ࠧࡔ࡛ࡖࡘࡊࡓ࡟ࡕࡇࡄࡑࡕࡘࡏࡋࡇࡆࡘࠬᴟ")), env.get(bstack11l1ll1_opy_ (u"ࠨࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡏࡄࠨᴠ"))),
            bstack11l1ll1_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᴡ"): env.get(bstack11l1ll1_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡊࡆࠥᴢ")),
            bstack11l1ll1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᴣ"): env.get(bstack11l1ll1_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡌࡈࠧᴤ"))
        }
    if any([env.get(bstack11l1ll1_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦᴥ")), env.get(bstack11l1ll1_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡖࡊ࡙ࡏࡍࡘࡈࡈࡤ࡙ࡏࡖࡔࡆࡉࡤ࡜ࡅࡓࡕࡌࡓࡓࠨᴦ")), env.get(bstack11l1ll1_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡘࡕࡕࡓࡅࡈࡣ࡛ࡋࡒࡔࡋࡒࡒࠧᴧ"))]):
        return {
            bstack11l1ll1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᴨ"): bstack11l1ll1_opy_ (u"ࠥࡅ࡜࡙ࠠࡄࡱࡧࡩࡇࡻࡩ࡭ࡦࠥᴩ"),
            bstack11l1ll1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᴪ"): env.get(bstack11l1ll1_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡒࡘࡆࡑࡏࡃࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦᴫ")),
            bstack11l1ll1_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᴬ"): env.get(bstack11l1ll1_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧᴭ")),
            bstack11l1ll1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᴮ"): env.get(bstack11l1ll1_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠢᴯ"))
        }
    if env.get(bstack11l1ll1_opy_ (u"ࠥࡦࡦࡳࡢࡰࡱࡢࡦࡺ࡯࡬ࡥࡐࡸࡱࡧ࡫ࡲࠣᴰ")):
        return {
            bstack11l1ll1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᴱ"): bstack11l1ll1_opy_ (u"ࠧࡈࡡ࡮ࡤࡲࡳࠧᴲ"),
            bstack11l1ll1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᴳ"): env.get(bstack11l1ll1_opy_ (u"ࠢࡣࡣࡰࡦࡴࡵ࡟ࡣࡷ࡬ࡰࡩࡘࡥࡴࡷ࡯ࡸࡸ࡛ࡲ࡭ࠤᴴ")),
            bstack11l1ll1_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᴵ"): env.get(bstack11l1ll1_opy_ (u"ࠤࡥࡥࡲࡨ࡯ࡰࡡࡶ࡬ࡴࡸࡴࡋࡱࡥࡒࡦࡳࡥࠣᴶ")),
            bstack11l1ll1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᴷ"): env.get(bstack11l1ll1_opy_ (u"ࠦࡧࡧ࡭ࡣࡱࡲࡣࡧࡻࡩ࡭ࡦࡑࡹࡲࡨࡥࡳࠤᴸ"))
        }
    if env.get(bstack11l1ll1_opy_ (u"ࠧ࡝ࡅࡓࡅࡎࡉࡗࠨᴹ")) or env.get(bstack11l1ll1_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘ࡟ࡎࡃࡌࡒࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡔࡖࡄࡖ࡙ࡋࡄࠣᴺ")):
        return {
            bstack11l1ll1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᴻ"): bstack11l1ll1_opy_ (u"࡙ࠣࡨࡶࡨࡱࡥࡳࠤᴼ"),
            bstack11l1ll1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᴽ"): env.get(bstack11l1ll1_opy_ (u"࡛ࠥࡊࡘࡃࡌࡇࡕࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢᴾ")),
            bstack11l1ll1_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᴿ"): bstack11l1ll1_opy_ (u"ࠧࡓࡡࡪࡰࠣࡔ࡮ࡶࡥ࡭࡫ࡱࡩࠧᵀ") if env.get(bstack11l1ll1_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘ࡟ࡎࡃࡌࡒࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡔࡖࡄࡖ࡙ࡋࡄࠣᵁ")) else None,
            bstack11l1ll1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᵂ"): env.get(bstack11l1ll1_opy_ (u"࡙ࠣࡈࡖࡈࡑࡅࡓࡡࡊࡍ࡙ࡥࡃࡐࡏࡐࡍ࡙ࠨᵃ"))
        }
    if any([env.get(bstack11l1ll1_opy_ (u"ࠤࡊࡇࡕࡥࡐࡓࡑࡍࡉࡈ࡚ࠢᵄ")), env.get(bstack11l1ll1_opy_ (u"ࠥࡋࡈࡒࡏࡖࡆࡢࡔࡗࡕࡊࡆࡅࡗࠦᵅ")), env.get(bstack11l1ll1_opy_ (u"ࠦࡌࡕࡏࡈࡎࡈࡣࡈࡒࡏࡖࡆࡢࡔࡗࡕࡊࡆࡅࡗࠦᵆ"))]):
        return {
            bstack11l1ll1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᵇ"): bstack11l1ll1_opy_ (u"ࠨࡇࡰࡱࡪࡰࡪࠦࡃ࡭ࡱࡸࡨࠧᵈ"),
            bstack11l1ll1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᵉ"): None,
            bstack11l1ll1_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᵊ"): env.get(bstack11l1ll1_opy_ (u"ࠤࡓࡖࡔࡐࡅࡄࡖࡢࡍࡉࠨᵋ")),
            bstack11l1ll1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᵌ"): env.get(bstack11l1ll1_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡍࡉࠨᵍ"))
        }
    if env.get(bstack11l1ll1_opy_ (u"࡙ࠧࡈࡊࡒࡓࡅࡇࡒࡅࠣᵎ")):
        return {
            bstack11l1ll1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᵏ"): bstack11l1ll1_opy_ (u"ࠢࡔࡪ࡬ࡴࡵࡧࡢ࡭ࡧࠥᵐ"),
            bstack11l1ll1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᵑ"): env.get(bstack11l1ll1_opy_ (u"ࠤࡖࡌࡎࡖࡐࡂࡄࡏࡉࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣᵒ")),
            bstack11l1ll1_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᵓ"): bstack11l1ll1_opy_ (u"ࠦࡏࡵࡢࠡࠥࡾࢁࠧᵔ").format(env.get(bstack11l1ll1_opy_ (u"࡙ࠬࡈࡊࡒࡓࡅࡇࡒࡅࡠࡌࡒࡆࡤࡏࡄࠨᵕ"))) if env.get(bstack11l1ll1_opy_ (u"ࠨࡓࡉࡋࡓࡔࡆࡈࡌࡆࡡࡍࡓࡇࡥࡉࡅࠤᵖ")) else None,
            bstack11l1ll1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᵗ"): env.get(bstack11l1ll1_opy_ (u"ࠣࡕࡋࡍࡕࡖࡁࡃࡎࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥᵘ"))
        }
    if bstack1ll1lll1l_opy_(env.get(bstack11l1ll1_opy_ (u"ࠤࡑࡉ࡙ࡒࡉࡇ࡛ࠥᵙ"))):
        return {
            bstack11l1ll1_opy_ (u"ࠥࡲࡦࡳࡥࠣᵚ"): bstack11l1ll1_opy_ (u"ࠦࡓ࡫ࡴ࡭࡫ࡩࡽࠧᵛ"),
            bstack11l1ll1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᵜ"): env.get(bstack11l1ll1_opy_ (u"ࠨࡄࡆࡒࡏࡓ࡞ࡥࡕࡓࡎࠥᵝ")),
            bstack11l1ll1_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᵞ"): env.get(bstack11l1ll1_opy_ (u"ࠣࡕࡌࡘࡊࡥࡎࡂࡏࡈࠦᵟ")),
            bstack11l1ll1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᵠ"): env.get(bstack11l1ll1_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡌࡈࠧᵡ"))
        }
    if bstack1ll1lll1l_opy_(env.get(bstack11l1ll1_opy_ (u"ࠦࡌࡏࡔࡉࡗࡅࡣࡆࡉࡔࡊࡑࡑࡗࠧᵢ"))):
        return {
            bstack11l1ll1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᵣ"): bstack11l1ll1_opy_ (u"ࠨࡇࡪࡶࡋࡹࡧࠦࡁࡤࡶ࡬ࡳࡳࡹࠢᵤ"),
            bstack11l1ll1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᵥ"): bstack11l1ll1_opy_ (u"ࠣࡽࢀ࠳ࢀࢃ࠯ࡢࡥࡷ࡭ࡴࡴࡳ࠰ࡴࡸࡲࡸ࠵ࡻࡾࠤᵦ").format(env.get(bstack11l1ll1_opy_ (u"ࠩࡊࡍ࡙ࡎࡕࡃࡡࡖࡉࡗ࡜ࡅࡓࡡࡘࡖࡑ࠭ᵧ")), env.get(bstack11l1ll1_opy_ (u"ࠪࡋࡎ࡚ࡈࡖࡄࡢࡖࡊࡖࡏࡔࡋࡗࡓࡗ࡟ࠧᵨ")), env.get(bstack11l1ll1_opy_ (u"ࠫࡌࡏࡔࡉࡗࡅࡣࡗ࡛ࡎࡠࡋࡇࠫᵩ"))),
            bstack11l1ll1_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᵪ"): env.get(bstack11l1ll1_opy_ (u"ࠨࡇࡊࡖࡋ࡙ࡇࡥࡗࡐࡔࡎࡊࡑࡕࡗࠣᵫ")),
            bstack11l1ll1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᵬ"): env.get(bstack11l1ll1_opy_ (u"ࠣࡉࡌࡘࡍ࡛ࡂࡠࡔࡘࡒࡤࡏࡄࠣᵭ"))
        }
    if env.get(bstack11l1ll1_opy_ (u"ࠤࡆࡍࠧᵮ")) == bstack11l1ll1_opy_ (u"ࠥࡸࡷࡻࡥࠣᵯ") and env.get(bstack11l1ll1_opy_ (u"࡛ࠦࡋࡒࡄࡇࡏࠦᵰ")) == bstack11l1ll1_opy_ (u"ࠧ࠷ࠢᵱ"):
        return {
            bstack11l1ll1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᵲ"): bstack11l1ll1_opy_ (u"ࠢࡗࡧࡵࡧࡪࡲࠢᵳ"),
            bstack11l1ll1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᵴ"): bstack11l1ll1_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࡾࢁࠧᵵ").format(env.get(bstack11l1ll1_opy_ (u"࡚ࠪࡊࡘࡃࡆࡎࡢ࡙ࡗࡒࠧᵶ"))),
            bstack11l1ll1_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᵷ"): None,
            bstack11l1ll1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᵸ"): None,
        }
    if env.get(bstack11l1ll1_opy_ (u"ࠨࡔࡆࡃࡐࡇࡎ࡚࡙ࡠࡘࡈࡖࡘࡏࡏࡏࠤᵹ")):
        return {
            bstack11l1ll1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᵺ"): bstack11l1ll1_opy_ (u"ࠣࡖࡨࡥࡲࡩࡩࡵࡻࠥᵻ"),
            bstack11l1ll1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᵼ"): None,
            bstack11l1ll1_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᵽ"): env.get(bstack11l1ll1_opy_ (u"࡙ࠦࡋࡁࡎࡅࡌࡘ࡞ࡥࡐࡓࡑࡍࡉࡈ࡚࡟ࡏࡃࡐࡉࠧᵾ")),
            bstack11l1ll1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᵿ"): env.get(bstack11l1ll1_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧᶀ"))
        }
    if any([env.get(bstack11l1ll1_opy_ (u"ࠢࡄࡑࡑࡇࡔ࡛ࡒࡔࡇࠥᶁ")), env.get(bstack11l1ll1_opy_ (u"ࠣࡅࡒࡒࡈࡕࡕࡓࡕࡈࡣ࡚ࡘࡌࠣᶂ")), env.get(bstack11l1ll1_opy_ (u"ࠤࡆࡓࡓࡉࡏࡖࡔࡖࡉࡤ࡛ࡓࡆࡔࡑࡅࡒࡋࠢᶃ")), env.get(bstack11l1ll1_opy_ (u"ࠥࡇࡔࡔࡃࡐࡗࡕࡗࡊࡥࡔࡆࡃࡐࠦᶄ"))]):
        return {
            bstack11l1ll1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᶅ"): bstack11l1ll1_opy_ (u"ࠧࡉ࡯࡯ࡥࡲࡹࡷࡹࡥࠣᶆ"),
            bstack11l1ll1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᶇ"): None,
            bstack11l1ll1_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᶈ"): env.get(bstack11l1ll1_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤᶉ")) or None,
            bstack11l1ll1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᶊ"): env.get(bstack11l1ll1_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡌࡈࠧᶋ"), 0)
        }
    if env.get(bstack11l1ll1_opy_ (u"ࠦࡌࡕ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤᶌ")):
        return {
            bstack11l1ll1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᶍ"): bstack11l1ll1_opy_ (u"ࠨࡇࡰࡅࡇࠦᶎ"),
            bstack11l1ll1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᶏ"): None,
            bstack11l1ll1_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᶐ"): env.get(bstack11l1ll1_opy_ (u"ࠤࡊࡓࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢᶑ")),
            bstack11l1ll1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᶒ"): env.get(bstack11l1ll1_opy_ (u"ࠦࡌࡕ࡟ࡑࡋࡓࡉࡑࡏࡎࡆࡡࡆࡓ࡚ࡔࡔࡆࡔࠥᶓ"))
        }
    if env.get(bstack11l1ll1_opy_ (u"ࠧࡉࡆࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠥᶔ")):
        return {
            bstack11l1ll1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᶕ"): bstack11l1ll1_opy_ (u"ࠢࡄࡱࡧࡩࡋࡸࡥࡴࡪࠥᶖ"),
            bstack11l1ll1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᶗ"): env.get(bstack11l1ll1_opy_ (u"ࠤࡆࡊࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣᶘ")),
            bstack11l1ll1_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᶙ"): env.get(bstack11l1ll1_opy_ (u"ࠦࡈࡌ࡟ࡑࡋࡓࡉࡑࡏࡎࡆࡡࡑࡅࡒࡋࠢᶚ")),
            bstack11l1ll1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᶛ"): env.get(bstack11l1ll1_opy_ (u"ࠨࡃࡇࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦᶜ"))
        }
    return {bstack11l1ll1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᶝ"): None}
def get_host_info():
    return {
        bstack11l1ll1_opy_ (u"ࠣࡪࡲࡷࡹࡴࡡ࡮ࡧࠥᶞ"): platform.node(),
        bstack11l1ll1_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࠦᶟ"): platform.system(),
        bstack11l1ll1_opy_ (u"ࠥࡸࡾࡶࡥࠣᶠ"): platform.machine(),
        bstack11l1ll1_opy_ (u"ࠦࡻ࡫ࡲࡴ࡫ࡲࡲࠧᶡ"): platform.version(),
        bstack11l1ll1_opy_ (u"ࠧࡧࡲࡤࡪࠥᶢ"): platform.architecture()[0]
    }
def bstack1llllllll_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack111l111111l_opy_():
    if bstack11lll111l_opy_.get_property(bstack11l1ll1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧᶣ")):
        return bstack11l1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ᶤ")
    return bstack11l1ll1_opy_ (u"ࠨࡷࡱ࡯ࡳࡵࡷ࡯ࡡࡪࡶ࡮ࡪࠧᶥ")
def bstack111l11lll11_opy_(driver):
    info = {
        bstack11l1ll1_opy_ (u"ࠩࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨᶦ"): driver.capabilities,
        bstack11l1ll1_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠧᶧ"): driver.session_id,
        bstack11l1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬᶨ"): driver.capabilities.get(bstack11l1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪᶩ"), None),
        bstack11l1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᶪ"): driver.capabilities.get(bstack11l1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᶫ"), None),
        bstack11l1ll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪᶬ"): driver.capabilities.get(bstack11l1ll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠨᶭ"), None),
        bstack11l1ll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᶮ"):driver.capabilities.get(bstack11l1ll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᶯ"), None),
    }
    if bstack111l111111l_opy_() == bstack11l1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫᶰ"):
        if bstack1ll11ll11_opy_():
            info[bstack11l1ll1_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺࠧᶱ")] = bstack11l1ll1_opy_ (u"ࠧࡢࡲࡳ࠱ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ᶲ")
        elif driver.capabilities.get(bstack11l1ll1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᶳ"), {}).get(bstack11l1ll1_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡴࡥࡤࡰࡪ࠭ᶴ"), False):
            info[bstack11l1ll1_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࠫᶵ")] = bstack11l1ll1_opy_ (u"ࠫࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥࠨᶶ")
        else:
            info[bstack11l1ll1_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹ࠭ᶷ")] = bstack11l1ll1_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨᶸ")
    return info
def bstack1ll11ll11_opy_():
    if bstack11lll111l_opy_.get_property(bstack11l1ll1_opy_ (u"ࠧࡢࡲࡳࡣࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ᶹ")):
        return True
    if bstack1ll1lll1l_opy_(os.environ.get(bstack11l1ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩᶺ"), None)):
        return True
    return False
def bstack111l111ll1l_opy_(bstack111l1l1ll11_opy_, url, response, headers=None, data=None):
    bstack11l1ll1_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࡅࡹ࡮ࡲࡤࠡࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡲ࡯ࡨࠢࡳࡥࡷࡧ࡭ࡦࡶࡨࡶࡸࠦࡦࡰࡴࠣࡶࡪࡷࡵࡦࡵࡷ࠳ࡷ࡫ࡳࡱࡱࡱࡷࡪࠦ࡬ࡰࡩࡪ࡭ࡳ࡭ࠊࠡࠢࠣࠤࡆࡸࡧࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡷ࡫ࡱࡶࡧࡶࡸࡤࡺࡹࡱࡧ࠽ࠤࡍ࡚ࡔࡑࠢࡰࡩࡹ࡮࡯ࡥࠢࠫࡋࡊ࡚ࠬࠡࡒࡒࡗ࡙࠲ࠠࡦࡶࡦ࠲࠮ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡶࡴ࡯࠾ࠥࡘࡥࡲࡷࡨࡷࡹࠦࡕࡓࡎ࠲ࡩࡳࡪࡰࡰ࡫ࡱࡸࠏࠦࠠࠡࠢࠣࠤࠥࠦࡲࡦࡵࡳࡳࡳࡹࡥ࠻ࠢࡕࡩࡸࡶ࡯࡯ࡵࡨࠤࡴࡨࡪࡦࡥࡷࠤ࡫ࡸ࡯࡮ࠢࡵࡩࡶࡻࡥࡴࡶࡶࠎࠥࠦࠠࠡࠢࠣࠤࠥ࡮ࡥࡢࡦࡨࡶࡸࡀࠠࡓࡧࡴࡹࡪࡹࡴࠡࡪࡨࡥࡩ࡫ࡲࡴࠢࡲࡶࠥࡔ࡯࡯ࡧࠍࠤࠥࠦࠠࠡࠢࠣࠤࡩࡧࡴࡢ࠼ࠣࡖࡪࡷࡵࡦࡵࡷࠤࡏ࡙ࡏࡏࠢࡧࡥࡹࡧࠠࡰࡴࠣࡒࡴࡴࡥࠋࠢࠣࠤࠥࡘࡥࡵࡷࡵࡲࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࡦ࡬ࡧࡹࡀࠠࡇࡱࡵࡱࡦࡺࡴࡦࡦࠣࡰࡴ࡭ࠠ࡮ࡧࡶࡷࡦ࡭ࡥࠡࡹ࡬ࡸ࡭ࠦࡲࡦࡳࡸࡩࡸࡺࠠࡢࡰࡧࠤࡷ࡫ࡳࡱࡱࡱࡷࡪࠦࡤࡢࡶࡤࠎࠥࠦࠠࠡࠤࠥࠦᶻ")
    bstack1111lll1ll1_opy_ = {
        bstack11l1ll1_opy_ (u"ࠥ࡬ࡪࡧࡤࡦࡴࡶࠦᶼ"): headers,
        bstack11l1ll1_opy_ (u"ࠦࡲ࡫ࡴࡩࡱࡧࠦᶽ"): bstack111l1l1ll11_opy_.upper(),
        bstack11l1ll1_opy_ (u"ࠧࡧࡧࡦࡰࡷࠦᶾ"): None,
        bstack11l1ll1_opy_ (u"ࠨࡥ࡯ࡦࡳࡳ࡮ࡴࡴࠣᶿ"): url,
        bstack11l1ll1_opy_ (u"ࠢ࡫ࡵࡲࡲࠧ᷀"): data
    }
    try:
        bstack111l1111l11_opy_ = response.json()
    except Exception:
        bstack111l1111l11_opy_ = response.text
    bstack111l1l1l11l_opy_ = {
        bstack11l1ll1_opy_ (u"ࠣࡤࡲࡨࡾࠨ᷁"): bstack111l1111l11_opy_,
        bstack11l1ll1_opy_ (u"ࠤࡶࡸࡦࡺࡵࡴࡅࡲࡨࡪࠨ᷂"): response.status_code
    }
    return {
        bstack11l1ll1_opy_ (u"ࠥࡶࡪࡷࡵࡦࡵࡷࠦ᷃"): bstack1111lll1ll1_opy_,
        bstack11l1ll1_opy_ (u"ࠦࡷ࡫ࡳࡱࡱࡱࡷࡪࠨ᷄"): bstack111l1l1l11l_opy_
    }
def bstack111l11l1ll_opy_(bstack111l1l1ll11_opy_, url, data, config):
    headers = config.get(bstack11l1ll1_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭᷅"), None)
    proxies = bstack11l1lll111_opy_(config, url)
    auth = config.get(bstack11l1ll1_opy_ (u"࠭ࡡࡶࡶ࡫ࠫ᷆"), None)
    response = requests.request(
            bstack111l1l1ll11_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    try:
        log_message = bstack111l111ll1l_opy_(bstack111l1l1ll11_opy_, url, response, headers, data)
        bstack11llll111_opy_.debug(json.dumps(log_message, separators=(bstack11l1ll1_opy_ (u"ࠧ࠭ࠩ᷇"), bstack11l1ll1_opy_ (u"ࠨ࠼ࠪ᷈"))))
    except Exception as e:
        logger.debug(bstack11l1ll1_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠ࡭ࡱࡪ࡫࡮ࡴࡧࠡࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡸࡥࡲࡷࡨࡷࡹࡀࠠࡼࡿࠥ᷉").format(e))
    return response
def bstack11l1l1l1l1_opy_(bstack1ll11l111l_opy_, size):
    bstack1llll1l111_opy_ = []
    while len(bstack1ll11l111l_opy_) > size:
        bstack1l11llllll_opy_ = bstack1ll11l111l_opy_[:size]
        bstack1llll1l111_opy_.append(bstack1l11llllll_opy_)
        bstack1ll11l111l_opy_ = bstack1ll11l111l_opy_[size:]
    bstack1llll1l111_opy_.append(bstack1ll11l111l_opy_)
    return bstack1llll1l111_opy_
def bstack111l1l11l11_opy_(message, bstack111ll111lll_opy_=False):
    os.write(1, bytes(message, bstack11l1ll1_opy_ (u"ࠪࡹࡹ࡬࠭࠹᷊ࠩ")))
    os.write(1, bytes(bstack11l1ll1_opy_ (u"ࠫࡡࡴࠧ᷋"), bstack11l1ll1_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫ᷌")))
    if bstack111ll111lll_opy_:
        with open(bstack11l1ll1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࠳࡯࠲࠳ࡼ࠱ࠬ᷍") + os.environ[bstack11l1ll1_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉ᷎࠭")] + bstack11l1ll1_opy_ (u"ࠨ࠰࡯ࡳ࡬᷏࠭"), bstack11l1ll1_opy_ (u"ࠩࡤ᷐ࠫ")) as f:
            f.write(message + bstack11l1ll1_opy_ (u"ࠪࡠࡳ࠭᷑"))
def bstack1l1l1111ll1_opy_():
    return os.environ[bstack11l1ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧ᷒")].lower() == bstack11l1ll1_opy_ (u"ࠬࡺࡲࡶࡧࠪᷓ")
def bstack1ll1llll11_opy_():
    return bstack11111lllll_opy_().replace(tzinfo=None).isoformat() + bstack11l1ll1_opy_ (u"࡚࠭ࠨᷔ")
def bstack111l111l11l_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack11l1ll1_opy_ (u"࡛ࠧࠩᷕ"))) - datetime.datetime.fromisoformat(start.rstrip(bstack11l1ll1_opy_ (u"ࠨ࡜ࠪᷖ")))).total_seconds() * 1000
def bstack111l11l1l1l_opy_(timestamp):
    return bstack1111llllll1_opy_(timestamp).isoformat() + bstack11l1ll1_opy_ (u"ࠩ࡝ࠫᷗ")
def bstack111l1ll11ll_opy_(bstack111l1lllll1_opy_):
    date_format = bstack11l1ll1_opy_ (u"ࠪࠩ࡞ࠫ࡭ࠦࡦࠣࠩࡍࡀࠥࡎ࠼ࠨࡗ࠳ࠫࡦࠨᷘ")
    bstack111lll11111_opy_ = datetime.datetime.strptime(bstack111l1lllll1_opy_, date_format)
    return bstack111lll11111_opy_.isoformat() + bstack11l1ll1_opy_ (u"ࠫ࡟࠭ᷙ")
def bstack111l111lll1_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack11l1ll1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᷚ")
    else:
        return bstack11l1ll1_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ᷛ")
def bstack1ll1lll1l_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack11l1ll1_opy_ (u"ࠧࡵࡴࡸࡩࠬᷜ")
def bstack111l1l11lll_opy_(val):
    return val.__str__().lower() == bstack11l1ll1_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧᷝ")
def error_handler(bstack1111llll1l1_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack1111llll1l1_opy_ as e:
                print(bstack11l1ll1_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡨࡸࡲࡨࡺࡩࡰࡰࠣࡿࢂࠦ࠭࠿ࠢࡾࢁ࠿ࠦࡻࡾࠤᷞ").format(func.__name__, bstack1111llll1l1_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack111lll1111l_opy_(bstack111l11ll111_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack111l11ll111_opy_(cls, *args, **kwargs)
            except bstack1111llll1l1_opy_ as e:
                print(bstack11l1ll1_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡩࡹࡳࡩࡴࡪࡱࡱࠤࢀࢃࠠ࠮ࡀࠣࡿࢂࡀࠠࡼࡿࠥᷟ").format(bstack111l11ll111_opy_.__name__, bstack1111llll1l1_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack111lll1111l_opy_
    else:
        return decorator
def bstack1l1l1111l1_opy_(bstack1lllll1ll1l_opy_):
    if os.getenv(bstack11l1ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧᷠ")) is not None:
        return bstack1ll1lll1l_opy_(os.getenv(bstack11l1ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨᷡ")))
    if bstack11l1ll1_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᷢ") in bstack1lllll1ll1l_opy_ and bstack111l1l11lll_opy_(bstack1lllll1ll1l_opy_[bstack11l1ll1_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫᷣ")]):
        return False
    if bstack11l1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᷤ") in bstack1lllll1ll1l_opy_ and bstack111l1l11lll_opy_(bstack1lllll1ll1l_opy_[bstack11l1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫᷥ")]):
        return False
    return True
def bstack1l1l1l1l1l_opy_():
    try:
        from pytest_bdd import reporting
        bstack111lll1l111_opy_ = os.environ.get(bstack11l1ll1_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡘࡗࡊࡘ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠥᷦ"), None)
        return bstack111lll1l111_opy_ is None or bstack111lll1l111_opy_ == bstack11l1ll1_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠣᷧ")
    except Exception as e:
        return False
def bstack1l1l111ll_opy_(hub_url, CONFIG):
    if bstack1l1lll1l_opy_() <= version.parse(bstack11l1ll1_opy_ (u"ࠬ࠹࠮࠲࠵࠱࠴ࠬᷨ")):
        if hub_url:
            return bstack11l1ll1_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢᷩ") + hub_url + bstack11l1ll1_opy_ (u"ࠢ࠻࠺࠳࠳ࡼࡪ࠯ࡩࡷࡥࠦᷪ")
        return bstack111ll1l1l_opy_
    if hub_url:
        return bstack11l1ll1_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࠥᷫ") + hub_url + bstack11l1ll1_opy_ (u"ࠤ࠲ࡻࡩ࠵ࡨࡶࡤࠥᷬ")
    return bstack1lll1111l_opy_
def bstack111ll1l1l1l_opy_():
    return isinstance(os.getenv(bstack11l1ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓ࡝࡙ࡋࡓࡕࡡࡓࡐ࡚ࡍࡉࡏࠩᷭ")), str)
def bstack11l1lll1_opy_(url):
    return urlparse(url).hostname
def bstack1ll1l111_opy_(hostname):
    for bstack11l111ll1_opy_ in bstack1ll1111l_opy_:
        regex = re.compile(bstack11l111ll1_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack111l1lll111_opy_(bstack111l1llll11_opy_, file_name, logger):
    bstack11l1l111ll_opy_ = os.path.join(os.path.expanduser(bstack11l1ll1_opy_ (u"ࠫࢃ࠭ᷮ")), bstack111l1llll11_opy_)
    try:
        if not os.path.exists(bstack11l1l111ll_opy_):
            os.makedirs(bstack11l1l111ll_opy_)
        file_path = os.path.join(os.path.expanduser(bstack11l1ll1_opy_ (u"ࠬࢄࠧᷯ")), bstack111l1llll11_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack11l1ll1_opy_ (u"࠭ࡷࠨᷰ")):
                pass
            with open(file_path, bstack11l1ll1_opy_ (u"ࠢࡸ࠭ࠥᷱ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack1l111l1111_opy_.format(str(e)))
def bstack111l11l1l11_opy_(file_name, key, value, logger):
    file_path = bstack111l1lll111_opy_(bstack11l1ll1_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨᷲ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1l1ll1lll_opy_ = json.load(open(file_path, bstack11l1ll1_opy_ (u"ࠩࡵࡦࠬᷳ")))
        else:
            bstack1l1ll1lll_opy_ = {}
        bstack1l1ll1lll_opy_[key] = value
        with open(file_path, bstack11l1ll1_opy_ (u"ࠥࡻ࠰ࠨᷴ")) as outfile:
            json.dump(bstack1l1ll1lll_opy_, outfile)
def bstack1ll1111l1_opy_(file_name, logger):
    file_path = bstack111l1lll111_opy_(bstack11l1ll1_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ᷵"), file_name, logger)
    bstack1l1ll1lll_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack11l1ll1_opy_ (u"ࠬࡸࠧ᷶")) as bstack11ll1l11l1_opy_:
            bstack1l1ll1lll_opy_ = json.load(bstack11ll1l11l1_opy_)
    return bstack1l1ll1lll_opy_
def bstack111lllll11_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack11l1ll1_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡦࡨࡰࡪࡺࡩ࡯ࡩࠣࡪ࡮ࡲࡥ࠻᷷ࠢࠪ") + file_path + bstack11l1ll1_opy_ (u"᷸ࠧࠡࠩ") + str(e))
def bstack1l1lll1l_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack11l1ll1_opy_ (u"ࠣ࠾ࡑࡓ࡙࡙ࡅࡕࡀ᷹ࠥ")
def bstack1ll111ll1l_opy_(config):
    if bstack11l1ll1_opy_ (u"ࠩ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨ᷺") in config:
        del (config[bstack11l1ll1_opy_ (u"ࠪ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩ᷻")])
        return False
    if bstack1l1lll1l_opy_() < version.parse(bstack11l1ll1_opy_ (u"ࠫ࠸࠴࠴࠯࠲ࠪ᷼")):
        return False
    if bstack1l1lll1l_opy_() >= version.parse(bstack11l1ll1_opy_ (u"ࠬ࠺࠮࠲࠰࠸᷽ࠫ")):
        return True
    if bstack11l1ll1_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭᷾") in config and config[bstack11l1ll1_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉ᷿ࠧ")] is False:
        return False
    else:
        return True
def bstack1ll11l1l_opy_(args_list, bstack111l111ll11_opy_):
    index = -1
    for value in bstack111l111ll11_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
def bstack11l1ll111ll_opy_(a, b):
  for k, v in b.items():
    if isinstance(v, dict) and k in a and isinstance(a[k], dict):
        bstack11l1ll111ll_opy_(a[k], v)
    else:
        a[k] = v
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack1111llll1l_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack1111llll1l_opy_ = bstack1111llll1l_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack11l1ll1_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨḀ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack11l1ll1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩḁ"), exception=exception)
    def bstack1llll11111l_opy_(self):
        if self.result != bstack11l1ll1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪḂ"):
            return None
        if isinstance(self.exception_type, str) and bstack11l1ll1_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࠢḃ") in self.exception_type:
            return bstack11l1ll1_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࡆࡴࡵࡳࡷࠨḄ")
        return bstack11l1ll1_opy_ (u"ࠨࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠢḅ")
    def bstack111l1l1l111_opy_(self):
        if self.result != bstack11l1ll1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧḆ"):
            return None
        if self.bstack1111llll1l_opy_:
            return self.bstack1111llll1l_opy_
        return bstack111ll1l1l11_opy_(self.exception)
def bstack111ll1l1l11_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack111l1l111l1_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack111ll1l1_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack1ll1ll1l1l_opy_(config, logger):
    try:
        import playwright
        bstack111lll111l1_opy_ = playwright.__file__
        bstack111l1ll1lll_opy_ = os.path.split(bstack111lll111l1_opy_)
        bstack111ll11l1ll_opy_ = bstack111l1ll1lll_opy_[0] + bstack11l1ll1_opy_ (u"ࠨ࠱ࡧࡶ࡮ࡼࡥࡳ࠱ࡳࡥࡨࡱࡡࡨࡧ࠲ࡰ࡮ࡨ࠯ࡤ࡮࡬࠳ࡨࡲࡩ࠯࡬ࡶࠫḇ")
        os.environ[bstack11l1ll1_opy_ (u"ࠩࡊࡐࡔࡈࡁࡍࡡࡄࡋࡊࡔࡔࡠࡊࡗࡘࡕࡥࡐࡓࡑ࡛࡝ࠬḈ")] = bstack11l11lll1l_opy_(config)
        with open(bstack111ll11l1ll_opy_, bstack11l1ll1_opy_ (u"ࠪࡶࠬḉ")) as f:
            bstack1l1l1ll1_opy_ = f.read()
            bstack111l1lll11l_opy_ = bstack11l1ll1_opy_ (u"ࠫ࡬ࡲ࡯ࡣࡣ࡯࠱ࡦ࡭ࡥ࡯ࡶࠪḊ")
            bstack111ll1lll1l_opy_ = bstack1l1l1ll1_opy_.find(bstack111l1lll11l_opy_)
            if bstack111ll1lll1l_opy_ == -1:
              process = subprocess.Popen(bstack11l1ll1_opy_ (u"ࠧࡴࡰ࡮ࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣ࡫ࡱࡵࡢࡢ࡮࠰ࡥ࡬࡫࡮ࡵࠤḋ"), shell=True, cwd=bstack111l1ll1lll_opy_[0])
              process.wait()
              bstack111ll111111_opy_ = bstack11l1ll1_opy_ (u"࠭ࠢࡶࡵࡨࠤࡸࡺࡲࡪࡥࡷࠦࡀ࠭Ḍ")
              bstack1111llll1ll_opy_ = bstack11l1ll1_opy_ (u"ࠢࠣࠤࠣࡠࠧࡻࡳࡦࠢࡶࡸࡷ࡯ࡣࡵ࡞ࠥ࠿ࠥࡩ࡯࡯ࡵࡷࠤࢀࠦࡢࡰࡱࡷࡷࡹࡸࡡࡱࠢࢀࠤࡂࠦࡲࡦࡳࡸ࡭ࡷ࡫ࠨࠨࡩ࡯ࡳࡧࡧ࡬࠮ࡣࡪࡩࡳࡺࠧࠪ࠽ࠣ࡭࡫ࠦࠨࡱࡴࡲࡧࡪࡹࡳ࠯ࡧࡱࡺ࠳ࡍࡌࡐࡄࡄࡐࡤࡇࡇࡆࡐࡗࡣࡍ࡚ࡔࡑࡡࡓࡖࡔ࡞࡙ࠪࠢࡥࡳࡴࡺࡳࡵࡴࡤࡴ࠭࠯࠻ࠡࠤࠥࠦḍ")
              bstack111l11l1ll1_opy_ = bstack1l1l1ll1_opy_.replace(bstack111ll111111_opy_, bstack1111llll1ll_opy_)
              with open(bstack111ll11l1ll_opy_, bstack11l1ll1_opy_ (u"ࠨࡹࠪḎ")) as f:
                f.write(bstack111l11l1ll1_opy_)
    except Exception as e:
        logger.error(bstack11lllll1ll_opy_.format(str(e)))
def bstack111ll11lll_opy_():
  try:
    bstack111l1lll1ll_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1ll1_opy_ (u"ࠩࡲࡴࡹ࡯࡭ࡢ࡮ࡢ࡬ࡺࡨ࡟ࡶࡴ࡯࠲࡯ࡹ࡯࡯ࠩḏ"))
    bstack111l1ll1l11_opy_ = []
    if os.path.exists(bstack111l1lll1ll_opy_):
      with open(bstack111l1lll1ll_opy_) as f:
        bstack111l1ll1l11_opy_ = json.load(f)
      os.remove(bstack111l1lll1ll_opy_)
    return bstack111l1ll1l11_opy_
  except:
    pass
  return []
def bstack1llll1111_opy_(bstack11lllllll1_opy_):
  try:
    bstack111l1ll1l11_opy_ = []
    bstack111l1lll1ll_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1ll1_opy_ (u"ࠪࡳࡵࡺࡩ࡮ࡣ࡯ࡣ࡭ࡻࡢࡠࡷࡵࡰ࠳ࡰࡳࡰࡰࠪḐ"))
    if os.path.exists(bstack111l1lll1ll_opy_):
      with open(bstack111l1lll1ll_opy_) as f:
        bstack111l1ll1l11_opy_ = json.load(f)
    bstack111l1ll1l11_opy_.append(bstack11lllllll1_opy_)
    with open(bstack111l1lll1ll_opy_, bstack11l1ll1_opy_ (u"ࠫࡼ࠭ḑ")) as f:
        json.dump(bstack111l1ll1l11_opy_, f)
  except:
    pass
def bstack11ll11ll1l_opy_(logger, bstack111ll11llll_opy_ = False):
  try:
    test_name = os.environ.get(bstack11l1ll1_opy_ (u"ࠬࡖ࡙ࡕࡇࡖࡘࡤ࡚ࡅࡔࡖࡢࡒࡆࡓࡅࠨḒ"), bstack11l1ll1_opy_ (u"࠭ࠧḓ"))
    if test_name == bstack11l1ll1_opy_ (u"ࠧࠨḔ"):
        test_name = threading.current_thread().__dict__.get(bstack11l1ll1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡃࡦࡧࡣࡹ࡫ࡳࡵࡡࡱࡥࡲ࡫ࠧḕ"), bstack11l1ll1_opy_ (u"ࠩࠪḖ"))
    bstack111l1111111_opy_ = bstack11l1ll1_opy_ (u"ࠪ࠰ࠥ࠭ḗ").join(threading.current_thread().bstackTestErrorMessages)
    if bstack111ll11llll_opy_:
        bstack11ll11l1ll_opy_ = os.environ.get(bstack11l1ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫḘ"), bstack11l1ll1_opy_ (u"ࠬ࠶ࠧḙ"))
        bstack1ll11l1l11_opy_ = {bstack11l1ll1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫḚ"): test_name, bstack11l1ll1_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ḛ"): bstack111l1111111_opy_, bstack11l1ll1_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧḜ"): bstack11ll11l1ll_opy_}
        bstack111ll1lll11_opy_ = []
        bstack111ll111l11_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1ll1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡳࡴࡵࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶ࠱࡮ࡸࡵ࡮ࠨḝ"))
        if os.path.exists(bstack111ll111l11_opy_):
            with open(bstack111ll111l11_opy_) as f:
                bstack111ll1lll11_opy_ = json.load(f)
        bstack111ll1lll11_opy_.append(bstack1ll11l1l11_opy_)
        with open(bstack111ll111l11_opy_, bstack11l1ll1_opy_ (u"ࠪࡻࠬḞ")) as f:
            json.dump(bstack111ll1lll11_opy_, f)
    else:
        bstack1ll11l1l11_opy_ = {bstack11l1ll1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩḟ"): test_name, bstack11l1ll1_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫḠ"): bstack111l1111111_opy_, bstack11l1ll1_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬḡ"): str(multiprocessing.current_process().name)}
        if bstack11l1ll1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷࠫḢ") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack1ll11l1l11_opy_)
  except Exception as e:
      logger.warn(bstack11l1ll1_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺ࡯ࡳࡧࠣࡴࡾࡺࡥࡴࡶࠣࡪࡺࡴ࡮ࡦ࡮ࠣࡨࡦࡺࡡ࠻ࠢࡾࢁࠧḣ").format(e))
def bstack1l1l11111_opy_(error_message, test_name, index, logger):
  try:
    from filelock import FileLock
  except ImportError:
    logger.debug(bstack11l1ll1_opy_ (u"ࠩࡩ࡭ࡱ࡫࡬ࡰࡥ࡮ࠤࡳࡵࡴࠡࡣࡹࡥ࡮ࡲࡡࡣ࡮ࡨ࠰ࠥࡻࡳࡪࡰࡪࠤࡧࡧࡳࡪࡥࠣࡪ࡮ࡲࡥࠡࡱࡳࡩࡷࡧࡴࡪࡱࡱࡷࠬḤ"))
    try:
      bstack111l1111l1l_opy_ = []
      bstack1ll11l1l11_opy_ = {bstack11l1ll1_opy_ (u"ࠪࡲࡦࡳࡥࠨḥ"): test_name, bstack11l1ll1_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪḦ"): error_message, bstack11l1ll1_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫḧ"): index}
      bstack111l11llll1_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1ll1_opy_ (u"࠭ࡲࡰࡤࡲࡸࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧḨ"))
      if os.path.exists(bstack111l11llll1_opy_):
          with open(bstack111l11llll1_opy_) as f:
              bstack111l1111l1l_opy_ = json.load(f)
      bstack111l1111l1l_opy_.append(bstack1ll11l1l11_opy_)
      with open(bstack111l11llll1_opy_, bstack11l1ll1_opy_ (u"ࠧࡸࠩḩ")) as f:
          json.dump(bstack111l1111l1l_opy_, f)
    except Exception as e:
      logger.warn(bstack11l1ll1_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺ࡯ࡳࡧࠣࡶࡴࡨ࡯ࡵࠢࡩࡹࡳࡴࡥ࡭ࠢࡧࡥࡹࡧ࠺ࠡࡽࢀࠦḪ").format(e))
    return
  bstack111l1111l1l_opy_ = []
  bstack1ll11l1l11_opy_ = {bstack11l1ll1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧḫ"): test_name, bstack11l1ll1_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩḬ"): error_message, bstack11l1ll1_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪḭ"): index}
  bstack111l11llll1_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1ll1_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴ࠯࡬ࡶࡳࡳ࠭Ḯ"))
  lock_file = bstack111l11llll1_opy_ + bstack11l1ll1_opy_ (u"࠭࠮࡭ࡱࡦ࡯ࠬḯ")
  try:
    with FileLock(lock_file, timeout=10):
      if os.path.exists(bstack111l11llll1_opy_):
          with open(bstack111l11llll1_opy_, bstack11l1ll1_opy_ (u"ࠧࡳࠩḰ")) as f:
              content = f.read().strip()
              if content:
                  bstack111l1111l1l_opy_ = json.load(open(bstack111l11llll1_opy_))
      bstack111l1111l1l_opy_.append(bstack1ll11l1l11_opy_)
      with open(bstack111l11llll1_opy_, bstack11l1ll1_opy_ (u"ࠨࡹࠪḱ")) as f:
          json.dump(bstack111l1111l1l_opy_, f)
  except Exception as e:
    logger.warn(bstack11l1ll1_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡴࡰࡴࡨࠤࡷࡵࡢࡰࡶࠣࡪࡺࡴ࡮ࡦ࡮ࠣࡨࡦࡺࡡࠡࡹ࡬ࡸ࡭ࠦࡦࡪ࡮ࡨࠤࡱࡵࡣ࡬࡫ࡱ࡫࠿ࠦࡻࡾࠤḲ").format(e))
def bstack11ll1l11_opy_(bstack1l11ll1l1_opy_, name, logger):
  try:
    bstack1ll11l1l11_opy_ = {bstack11l1ll1_opy_ (u"ࠪࡲࡦࡳࡥࠨḳ"): name, bstack11l1ll1_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪḴ"): bstack1l11ll1l1_opy_, bstack11l1ll1_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫḵ"): str(threading.current_thread()._name)}
    return bstack1ll11l1l11_opy_
  except Exception as e:
    logger.warn(bstack11l1ll1_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡸࡴࡸࡥࠡࡤࡨ࡬ࡦࡼࡥࠡࡨࡸࡲࡳ࡫࡬ࠡࡦࡤࡸࡦࡀࠠࡼࡿࠥḶ").format(e))
  return
def bstack111ll1llll1_opy_():
    return platform.system() == bstack11l1ll1_opy_ (u"ࠧࡘ࡫ࡱࡨࡴࡽࡳࠨḷ")
def bstack11lll1llll_opy_(bstack111ll1111l1_opy_, config, logger):
    bstack111lll111ll_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack111ll1111l1_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack11l1ll1_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡫࡯࡬ࡵࡧࡵࠤࡨࡵ࡮ࡧ࡫ࡪࠤࡰ࡫ࡹࡴࠢࡥࡽࠥࡸࡥࡨࡧࡻࠤࡲࡧࡴࡤࡪ࠽ࠤࢀࢃࠢḸ").format(e))
    return bstack111lll111ll_opy_
def bstack111ll11l1l1_opy_(bstack111ll1l111l_opy_, bstack1111lllllll_opy_):
    bstack111ll1l1ll1_opy_ = version.parse(bstack111ll1l111l_opy_)
    bstack111lll1l11l_opy_ = version.parse(bstack1111lllllll_opy_)
    if bstack111ll1l1ll1_opy_ > bstack111lll1l11l_opy_:
        return 1
    elif bstack111ll1l1ll1_opy_ < bstack111lll1l11l_opy_:
        return -1
    else:
        return 0
def bstack11111lllll_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack1111llllll1_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
def bstack111lll11lll_opy_(framework):
    from browserstack_sdk._version import __version__
    return str(framework) + str(__version__)
def bstack11l1l1ll1l_opy_(options, framework, config, bstack1l1l11l11_opy_={}):
    if options is None:
        return
    if getattr(options, bstack11l1ll1_opy_ (u"ࠩࡪࡩࡹ࠭ḹ"), None):
        caps = options
    else:
        caps = options.to_capabilities()
    bstack1l11l11l_opy_ = caps.get(bstack11l1ll1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫḺ"))
    bstack111ll11ll1l_opy_ = True
    bstack11l1lll1l_opy_ = os.environ[bstack11l1ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩḻ")]
    bstack1l1llll1lll_opy_ = config.get(bstack11l1ll1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬḼ"), False)
    if bstack1l1llll1lll_opy_:
        bstack1ll1l11llll_opy_ = config.get(bstack11l1ll1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ḽ"), {})
        bstack1ll1l11llll_opy_[bstack11l1ll1_opy_ (u"ࠧࡢࡷࡷ࡬࡙ࡵ࡫ࡦࡰࠪḾ")] = os.getenv(bstack11l1ll1_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ḿ"))
        bstack11l1l111l11_opy_ = json.loads(os.getenv(bstack11l1ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪṀ"), bstack11l1ll1_opy_ (u"ࠪࡿࢂ࠭ṁ"))).get(bstack11l1ll1_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬṂ"))
    if bstack111l1l11lll_opy_(caps.get(bstack11l1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡺࡹࡥࡘ࠵ࡆࠫṃ"))) or bstack111l1l11lll_opy_(caps.get(bstack11l1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡻࡳࡦࡡࡺ࠷ࡨ࠭Ṅ"))):
        bstack111ll11ll1l_opy_ = False
    if bstack1ll111ll1l_opy_({bstack11l1ll1_opy_ (u"ࠢࡶࡵࡨ࡛࠸ࡉࠢṅ"): bstack111ll11ll1l_opy_}):
        bstack1l11l11l_opy_ = bstack1l11l11l_opy_ or {}
        bstack1l11l11l_opy_[bstack11l1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪṆ")] = bstack111lll11lll_opy_(framework)
        bstack1l11l11l_opy_[bstack11l1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫṇ")] = bstack1l1l1111ll1_opy_()
        bstack1l11l11l_opy_[bstack11l1ll1_opy_ (u"ࠪࡸࡪࡹࡴࡩࡷࡥࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭Ṉ")] = bstack11l1lll1l_opy_
        bstack1l11l11l_opy_[bstack11l1ll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭ṉ")] = bstack1l1l11l11_opy_
        if bstack1l1llll1lll_opy_:
            bstack1l11l11l_opy_[bstack11l1ll1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬṊ")] = bstack1l1llll1lll_opy_
            bstack1l11l11l_opy_[bstack11l1ll1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ṋ")] = bstack1ll1l11llll_opy_
            bstack1l11l11l_opy_[bstack11l1ll1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧṌ")][bstack11l1ll1_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩṍ")] = bstack11l1l111l11_opy_
        if getattr(options, bstack11l1ll1_opy_ (u"ࠩࡶࡩࡹࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵࡻࠪṎ"), None):
            options.set_capability(bstack11l1ll1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫṏ"), bstack1l11l11l_opy_)
        else:
            options[bstack11l1ll1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬṐ")] = bstack1l11l11l_opy_
    else:
        if getattr(options, bstack11l1ll1_opy_ (u"ࠬࡹࡥࡵࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸࡾ࠭ṑ"), None):
            options.set_capability(bstack11l1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧṒ"), bstack111lll11lll_opy_(framework))
            options.set_capability(bstack11l1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨṓ"), bstack1l1l1111ll1_opy_())
            options.set_capability(bstack11l1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡵࡧࡶࡸ࡭ࡻࡢࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪṔ"), bstack11l1lll1l_opy_)
            options.set_capability(bstack11l1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪṕ"), bstack1l1l11l11_opy_)
            if bstack1l1llll1lll_opy_:
                options.set_capability(bstack11l1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩṖ"), bstack1l1llll1lll_opy_)
                options.set_capability(bstack11l1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪṗ"), bstack1ll1l11llll_opy_)
                options.set_capability(bstack11l1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶ࠲ࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬṘ"), bstack11l1l111l11_opy_)
        else:
            options[bstack11l1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧṙ")] = bstack111lll11lll_opy_(framework)
            options[bstack11l1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨṚ")] = bstack1l1l1111ll1_opy_()
            options[bstack11l1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡵࡧࡶࡸ࡭ࡻࡢࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪṛ")] = bstack11l1lll1l_opy_
            options[bstack11l1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪṜ")] = bstack1l1l11l11_opy_
            if bstack1l1llll1lll_opy_:
                options[bstack11l1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩṝ")] = bstack1l1llll1lll_opy_
                options[bstack11l1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪṞ")] = bstack1ll1l11llll_opy_
                options[bstack11l1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫṟ")][bstack11l1ll1_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧṠ")] = bstack11l1l111l11_opy_
    return options
def bstack111ll1l1111_opy_(bstack111l111l1l1_opy_, framework):
    bstack1l1l11l11_opy_ = bstack11lll111l_opy_.get_property(bstack11l1ll1_opy_ (u"ࠢࡑࡎࡄ࡝࡜ࡘࡉࡈࡊࡗࡣࡕࡘࡏࡅࡗࡆࡘࡤࡓࡁࡑࠤṡ"))
    if bstack111l111l1l1_opy_ and len(bstack111l111l1l1_opy_.split(bstack11l1ll1_opy_ (u"ࠨࡥࡤࡴࡸࡃࠧṢ"))) > 1:
        ws_url = bstack111l111l1l1_opy_.split(bstack11l1ll1_opy_ (u"ࠩࡦࡥࡵࡹ࠽ࠨṣ"))[0]
        if bstack11l1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭Ṥ") in ws_url:
            from browserstack_sdk._version import __version__
            bstack111l11lllll_opy_ = json.loads(urllib.parse.unquote(bstack111l111l1l1_opy_.split(bstack11l1ll1_opy_ (u"ࠫࡨࡧࡰࡴ࠿ࠪṥ"))[1]))
            bstack111l11lllll_opy_ = bstack111l11lllll_opy_ or {}
            bstack11l1lll1l_opy_ = os.environ[bstack11l1ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪṦ")]
            bstack111l11lllll_opy_[bstack11l1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧṧ")] = str(framework) + str(__version__)
            bstack111l11lllll_opy_[bstack11l1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨṨ")] = bstack1l1l1111ll1_opy_()
            bstack111l11lllll_opy_[bstack11l1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡵࡧࡶࡸ࡭ࡻࡢࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪṩ")] = bstack11l1lll1l_opy_
            bstack111l11lllll_opy_[bstack11l1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪṪ")] = bstack1l1l11l11_opy_
            bstack111l111l1l1_opy_ = bstack111l111l1l1_opy_.split(bstack11l1ll1_opy_ (u"ࠪࡧࡦࡶࡳ࠾ࠩṫ"))[0] + bstack11l1ll1_opy_ (u"ࠫࡨࡧࡰࡴ࠿ࠪṬ") + urllib.parse.quote(json.dumps(bstack111l11lllll_opy_))
    return bstack111l111l1l1_opy_
def bstack11ll111l1l_opy_():
    global bstack1lll1l1l11_opy_
    from playwright._impl._browser_type import BrowserType
    bstack1lll1l1l11_opy_ = BrowserType.connect
    return bstack1lll1l1l11_opy_
def bstack11ll111l_opy_(framework_name):
    global bstack11l1lllll_opy_
    bstack11l1lllll_opy_ = framework_name
    return framework_name
def bstack1ll1l1l1l_opy_(self, *args, **kwargs):
    global bstack1lll1l1l11_opy_
    try:
        global bstack11l1lllll_opy_
        if bstack11l1ll1_opy_ (u"ࠬࡽࡳࡆࡰࡧࡴࡴ࡯࡮ࡵࠩṭ") in kwargs:
            kwargs[bstack11l1ll1_opy_ (u"࠭ࡷࡴࡇࡱࡨࡵࡵࡩ࡯ࡶࠪṮ")] = bstack111ll1l1111_opy_(
                kwargs.get(bstack11l1ll1_opy_ (u"ࠧࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷࠫṯ"), None),
                bstack11l1lllll_opy_
            )
    except Exception as e:
        logger.error(bstack11l1ll1_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪࡨࡲࠥࡶࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡖࡈࡐࠦࡣࡢࡲࡶ࠾ࠥࢁࡽࠣṰ").format(str(e)))
    return bstack1lll1l1l11_opy_(self, *args, **kwargs)
def bstack111ll111ll1_opy_(bstack111l111l1ll_opy_, proxies):
    proxy_settings = {}
    try:
        if not proxies:
            proxies = bstack11l1lll111_opy_(bstack111l111l1ll_opy_, bstack11l1ll1_opy_ (u"ࠤࠥṱ"))
        if proxies and proxies.get(bstack11l1ll1_opy_ (u"ࠥ࡬ࡹࡺࡰࡴࠤṲ")):
            parsed_url = urlparse(proxies.get(bstack11l1ll1_opy_ (u"ࠦ࡭ࡺࡴࡱࡵࠥṳ")))
            if parsed_url and parsed_url.hostname: proxy_settings[bstack11l1ll1_opy_ (u"ࠬࡶࡲࡰࡺࡼࡌࡴࡹࡴࠨṴ")] = str(parsed_url.hostname)
            if parsed_url and parsed_url.port: proxy_settings[bstack11l1ll1_opy_ (u"࠭ࡰࡳࡱࡻࡽࡕࡵࡲࡵࠩṵ")] = str(parsed_url.port)
            if parsed_url and parsed_url.username: proxy_settings[bstack11l1ll1_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡛ࡳࡦࡴࠪṶ")] = str(parsed_url.username)
            if parsed_url and parsed_url.password: proxy_settings[bstack11l1ll1_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡢࡵࡶࠫṷ")] = str(parsed_url.password)
        return proxy_settings
    except:
        return proxy_settings
def bstack11111l11_opy_(bstack111l111l1ll_opy_):
    bstack111ll1l11ll_opy_ = {
        bstack11l11l11l11_opy_[bstack111ll1ll11l_opy_]: bstack111l111l1ll_opy_[bstack111ll1ll11l_opy_]
        for bstack111ll1ll11l_opy_ in bstack111l111l1ll_opy_
        if bstack111ll1ll11l_opy_ in bstack11l11l11l11_opy_
    }
    bstack111ll1l11ll_opy_[bstack11l1ll1_opy_ (u"ࠤࡳࡶࡴࡾࡹࡔࡧࡷࡸ࡮ࡴࡧࡴࠤṸ")] = bstack111ll111ll1_opy_(bstack111l111l1ll_opy_, bstack11lll111l_opy_.get_property(bstack11l1ll1_opy_ (u"ࠥࡴࡷࡵࡸࡺࡕࡨࡸࡹ࡯࡮ࡨࡵࠥṹ")))
    bstack111l1llllll_opy_ = [element.lower() for element in bstack11l111l11ll_opy_]
    bstack111ll11111l_opy_(bstack111ll1l11ll_opy_, bstack111l1llllll_opy_)
    return bstack111ll1l11ll_opy_
def bstack111ll11111l_opy_(d, keys):
    for key in list(d.keys()):
        if key.lower() in keys:
            d[key] = bstack11l1ll1_opy_ (u"ࠦ࠯࠰ࠪࠫࠤṺ")
    for value in d.values():
        if isinstance(value, dict):
            bstack111ll11111l_opy_(value, keys)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    bstack111ll11111l_opy_(item, keys)
def bstack1l11ll1ll1l_opy_():
    bstack111ll11l111_opy_ = [os.environ.get(bstack11l1ll1_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡏࡌࡆࡕࡢࡈࡎࡘࠢṻ")), os.path.join(os.path.expanduser(bstack11l1ll1_opy_ (u"ࠨࡾࠣṼ")), bstack11l1ll1_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧṽ")), os.path.join(bstack11l1ll1_opy_ (u"ࠨ࠱ࡷࡱࡵ࠭Ṿ"), bstack11l1ll1_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩṿ"))]
    for path in bstack111ll11l111_opy_:
        if path is None:
            continue
        try:
            if os.path.exists(path):
                logger.debug(bstack11l1ll1_opy_ (u"ࠥࡊ࡮ࡲࡥࠡࠩࠥẀ") + str(path) + bstack11l1ll1_opy_ (u"ࠦࠬࠦࡥࡹ࡫ࡶࡸࡸ࠴ࠢẁ"))
                if not os.access(path, os.W_OK):
                    logger.debug(bstack11l1ll1_opy_ (u"ࠧࡍࡩࡷ࡫ࡱ࡫ࠥࡶࡥࡳ࡯࡬ࡷࡸ࡯࡯࡯ࡵࠣࡪࡴࡸࠠࠨࠤẂ") + str(path) + bstack11l1ll1_opy_ (u"ࠨࠧࠣẃ"))
                    os.chmod(path, 0o777)
                else:
                    logger.debug(bstack11l1ll1_opy_ (u"ࠢࡇ࡫࡯ࡩࠥ࠭ࠢẄ") + str(path) + bstack11l1ll1_opy_ (u"ࠣࠩࠣࡥࡱࡸࡥࡢࡦࡼࠤ࡭ࡧࡳࠡࡶ࡫ࡩࠥࡸࡥࡲࡷ࡬ࡶࡪࡪࠠࡱࡧࡵࡱ࡮ࡹࡳࡪࡱࡱࡷ࠳ࠨẅ"))
            else:
                logger.debug(bstack11l1ll1_opy_ (u"ࠤࡆࡶࡪࡧࡴࡪࡰࡪࠤ࡫࡯࡬ࡦࠢࠪࠦẆ") + str(path) + bstack11l1ll1_opy_ (u"ࠥࠫࠥࡽࡩࡵࡪࠣࡻࡷ࡯ࡴࡦࠢࡳࡩࡷࡳࡩࡴࡵ࡬ࡳࡳ࠴ࠢẇ"))
                os.makedirs(path, exist_ok=True)
                os.chmod(path, 0o777)
            logger.debug(bstack11l1ll1_opy_ (u"ࠦࡔࡶࡥࡳࡣࡷ࡭ࡴࡴࠠࡴࡷࡦࡧࡪ࡫ࡤࡦࡦࠣࡪࡴࡸࠠࠨࠤẈ") + str(path) + bstack11l1ll1_opy_ (u"ࠧ࠭࠮ࠣẉ"))
            return path
        except Exception as e:
            logger.debug(bstack11l1ll1_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࠦࡵࡱࠢࡩ࡭ࡱ࡫ࠠࠨࡽࡳࡥࡹ࡮ࡽࠨ࠼ࠣࠦẊ") + str(e) + bstack11l1ll1_opy_ (u"ࠢࠣẋ"))
    logger.debug(bstack11l1ll1_opy_ (u"ࠣࡃ࡯ࡰࠥࡶࡡࡵࡪࡶࠤ࡫ࡧࡩ࡭ࡧࡧ࠲ࠧẌ"))
    return None
@measure(event_name=EVENTS.bstack11l11l11ll1_opy_, stage=STAGE.bstack11lll1l1l1_opy_)
def bstack1ll1l1l1l11_opy_(binary_path, bstack1ll11lll111_opy_, bs_config):
    logger.debug(bstack11l1ll1_opy_ (u"ࠤࡆࡹࡷࡸࡥ࡯ࡶࠣࡇࡑࡏࠠࡑࡣࡷ࡬ࠥ࡬࡯ࡶࡰࡧ࠾ࠥࢁࡽࠣẍ").format(binary_path))
    bstack1111lllll11_opy_ = bstack11l1ll1_opy_ (u"ࠪࠫẎ")
    bstack111ll1lllll_opy_ = {
        bstack11l1ll1_opy_ (u"ࠫࡸࡪ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩẏ"): __version__,
        bstack11l1ll1_opy_ (u"ࠧࡵࡳࠣẐ"): platform.system(),
        bstack11l1ll1_opy_ (u"ࠨ࡯ࡴࡡࡤࡶࡨ࡮ࠢẑ"): platform.machine(),
        bstack11l1ll1_opy_ (u"ࠢࡤ࡮࡬ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧẒ"): bstack11l1ll1_opy_ (u"ࠨ࠲ࠪẓ"),
        bstack11l1ll1_opy_ (u"ࠤࡶࡨࡰࡥ࡬ࡢࡰࡪࡹࡦ࡭ࡥࠣẔ"): bstack11l1ll1_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪẕ")
    }
    bstack1111lll1l11_opy_(bstack111ll1lllll_opy_)
    try:
        if binary_path:
            if bstack111ll1llll1_opy_():
                bstack111ll1lllll_opy_[bstack11l1ll1_opy_ (u"ࠫࡨࡲࡩࡠࡸࡨࡶࡸ࡯࡯࡯ࠩẖ")] = subprocess.check_output([binary_path, bstack11l1ll1_opy_ (u"ࠧࡼࡥࡳࡵ࡬ࡳࡳࠨẗ")]).strip().decode(bstack11l1ll1_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬẘ"))
            else:
                bstack111ll1lllll_opy_[bstack11l1ll1_opy_ (u"ࠧࡤ࡮࡬ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬẙ")] = subprocess.check_output([binary_path, bstack11l1ll1_opy_ (u"ࠣࡸࡨࡶࡸ࡯࡯࡯ࠤẚ")], stderr=subprocess.DEVNULL).strip().decode(bstack11l1ll1_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨẛ"))
        response = requests.request(
            bstack11l1ll1_opy_ (u"ࠪࡋࡊ࡚ࠧẜ"),
            url=bstack11l1l1ll11_opy_(bstack11l11l111ll_opy_),
            headers=None,
            auth=(bs_config[bstack11l1ll1_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ẝ")], bs_config[bstack11l1ll1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨẞ")]),
            json=None,
            params=bstack111ll1lllll_opy_
        )
        data = response.json()
        if response.status_code == 200 and bstack11l1ll1_opy_ (u"࠭ࡵࡳ࡮ࠪẟ") in data.keys() and bstack11l1ll1_opy_ (u"ࠧࡶࡲࡧࡥࡹ࡫ࡤࡠࡥ࡯࡭ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭Ạ") in data.keys():
            logger.debug(bstack11l1ll1_opy_ (u"ࠣࡐࡨࡩࡩࠦࡴࡰࠢࡸࡴࡩࡧࡴࡦࠢࡥ࡭ࡳࡧࡲࡺ࠮ࠣࡧࡺࡸࡲࡦࡰࡷࠤࡧ࡯࡮ࡢࡴࡼࠤࡻ࡫ࡲࡴ࡫ࡲࡲ࠿ࠦࡻࡾࠤạ").format(bstack111ll1lllll_opy_[bstack11l1ll1_opy_ (u"ࠩࡦࡰ࡮ࡥࡶࡦࡴࡶ࡭ࡴࡴࠧẢ")]))
            if bstack11l1ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅࡍࡓࡇࡒ࡚ࡡࡘࡖࡑ࠭ả") in os.environ:
                logger.debug(bstack11l1ll1_opy_ (u"ࠦࡘࡱࡩࡱࡲ࡬ࡲ࡬ࠦࡢࡪࡰࡤࡶࡾࠦࡤࡰࡹࡱࡰࡴࡧࡤࠡࡣࡶࠤࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆࡎࡔࡁࡓ࡛ࡢ࡙ࡗࡒࠠࡪࡵࠣࡷࡪࡺࠢẤ"))
                data[bstack11l1ll1_opy_ (u"ࠬࡻࡲ࡭ࠩấ")] = os.environ[bstack11l1ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡉࡏࡃࡕ࡝ࡤ࡛ࡒࡍࠩẦ")]
            bstack111ll11l11l_opy_ = bstack1111lllll1l_opy_(data[bstack11l1ll1_opy_ (u"ࠧࡶࡴ࡯ࠫầ")], bstack1ll11lll111_opy_)
            bstack1111lllll11_opy_ = os.path.join(bstack1ll11lll111_opy_, bstack111ll11l11l_opy_)
            os.chmod(bstack1111lllll11_opy_, 0o777) # bstack111l11l1111_opy_ permission
            return bstack1111lllll11_opy_
    except Exception as e:
        logger.debug(bstack11l1ll1_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡤࡰࡹࡱࡰࡴࡧࡤࡪࡰࡪࠤࡳ࡫ࡷࠡࡕࡇࡏࠥࢁࡽࠣẨ").format(e))
    return binary_path
def bstack1111lll1l11_opy_(bstack111ll1lllll_opy_):
    try:
        if bstack11l1ll1_opy_ (u"ࠩ࡯࡭ࡳࡻࡸࠨẩ") not in bstack111ll1lllll_opy_[bstack11l1ll1_opy_ (u"ࠪࡳࡸ࠭Ẫ")].lower():
            return
        if os.path.exists(bstack11l1ll1_opy_ (u"ࠦ࠴࡫ࡴࡤ࠱ࡲࡷ࠲ࡸࡥ࡭ࡧࡤࡷࡪࠨẫ")):
            with open(bstack11l1ll1_opy_ (u"ࠧ࠵ࡥࡵࡥ࠲ࡳࡸ࠳ࡲࡦ࡮ࡨࡥࡸ࡫ࠢẬ"), bstack11l1ll1_opy_ (u"ࠨࡲࠣậ")) as f:
                bstack111l1llll1l_opy_ = {}
                for line in f:
                    if bstack11l1ll1_opy_ (u"ࠢ࠾ࠤẮ") in line:
                        key, value = line.rstrip().split(bstack11l1ll1_opy_ (u"ࠣ࠿ࠥắ"), 1)
                        bstack111l1llll1l_opy_[key] = value.strip(bstack11l1ll1_opy_ (u"ࠩࠥࡠࠬ࠭Ằ"))
                bstack111ll1lllll_opy_[bstack11l1ll1_opy_ (u"ࠪࡨ࡮ࡹࡴࡳࡱࠪằ")] = bstack111l1llll1l_opy_.get(bstack11l1ll1_opy_ (u"ࠦࡎࡊࠢẲ"), bstack11l1ll1_opy_ (u"ࠧࠨẳ"))
        elif os.path.exists(bstack11l1ll1_opy_ (u"ࠨ࠯ࡦࡶࡦ࠳ࡦࡲࡰࡪࡰࡨ࠱ࡷ࡫࡬ࡦࡣࡶࡩࠧẴ")):
            bstack111ll1lllll_opy_[bstack11l1ll1_opy_ (u"ࠧࡥ࡫ࡶࡸࡷࡵࠧẵ")] = bstack11l1ll1_opy_ (u"ࠨࡣ࡯ࡴ࡮ࡴࡥࠨẶ")
    except Exception as e:
        logger.debug(bstack11l1ll1_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥ࡭ࡥࡵࠢࡧ࡭ࡸࡺࡲࡰࠢࡲࡪࠥࡲࡩ࡯ࡷࡻࠦặ") + e)
@measure(event_name=EVENTS.bstack11l11l1111l_opy_, stage=STAGE.bstack11lll1l1l1_opy_)
def bstack1111lllll1l_opy_(bstack111l11111l1_opy_, bstack111lll11l11_opy_):
    logger.debug(bstack11l1ll1_opy_ (u"ࠥࡈࡴࡽ࡮࡭ࡱࡤࡨ࡮ࡴࡧࠡࡕࡇࡏࠥࡨࡩ࡯ࡣࡵࡽࠥ࡬ࡲࡰ࡯࠽ࠤࠧẸ") + str(bstack111l11111l1_opy_) + bstack11l1ll1_opy_ (u"ࠦࠧẹ"))
    zip_path = os.path.join(bstack111lll11l11_opy_, bstack11l1ll1_opy_ (u"ࠧࡪ࡯ࡸࡰ࡯ࡳࡦࡪࡥࡥࡡࡩ࡭ࡱ࡫࠮ࡻ࡫ࡳࠦẺ"))
    bstack111ll11l11l_opy_ = bstack11l1ll1_opy_ (u"࠭ࠧẻ")
    with requests.get(bstack111l11111l1_opy_, stream=True) as response:
        response.raise_for_status()
        with open(zip_path, bstack11l1ll1_opy_ (u"ࠢࡸࡤࠥẼ")) as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        logger.debug(bstack11l1ll1_opy_ (u"ࠣࡈ࡬ࡰࡪࠦࡤࡰࡹࡱࡰࡴࡧࡤࡦࡦࠣࡷࡺࡩࡣࡦࡵࡶࡪࡺࡲ࡬ࡺ࠰ࠥẽ"))
    with zipfile.ZipFile(zip_path, bstack11l1ll1_opy_ (u"ࠩࡵࠫẾ")) as zip_ref:
        bstack111l1l1l1l1_opy_ = zip_ref.namelist()
        if len(bstack111l1l1l1l1_opy_) > 0:
            bstack111ll11l11l_opy_ = bstack111l1l1l1l1_opy_[0] # bstack111l1l1l1ll_opy_ bstack11l111111l1_opy_ will be bstack111l1ll1111_opy_ 1 file i.e. the binary in the zip
        zip_ref.extractall(bstack111lll11l11_opy_)
        logger.debug(bstack11l1ll1_opy_ (u"ࠥࡊ࡮ࡲࡥࡴࠢࡶࡹࡨࡩࡥࡴࡵࡩࡹࡱࡲࡹࠡࡧࡻࡸࡷࡧࡣࡵࡧࡧࠤࡹࡵࠠࠨࠤế") + str(bstack111lll11l11_opy_) + bstack11l1ll1_opy_ (u"ࠦࠬࠨỀ"))
    os.remove(zip_path)
    return bstack111ll11l11l_opy_
def get_cli_dir():
    bstack111ll1ll111_opy_ = bstack1l11ll1ll1l_opy_()
    if bstack111ll1ll111_opy_:
        bstack1ll11lll111_opy_ = os.path.join(bstack111ll1ll111_opy_, bstack11l1ll1_opy_ (u"ࠧࡩ࡬ࡪࠤề"))
        if not os.path.exists(bstack1ll11lll111_opy_):
            os.makedirs(bstack1ll11lll111_opy_, mode=0o777, exist_ok=True)
        return bstack1ll11lll111_opy_
    else:
        raise FileNotFoundError(bstack11l1ll1_opy_ (u"ࠨࡎࡰࠢࡺࡶ࡮ࡺࡡࡣ࡮ࡨࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠࡢࡸࡤ࡭ࡱࡧࡢ࡭ࡧࠣࡪࡴࡸࠠࡵࡪࡨࠤࡘࡊࡋࠡࡤ࡬ࡲࡦࡸࡹ࠯ࠤỂ"))
def bstack1ll111lll11_opy_(bstack1ll11lll111_opy_):
    bstack11l1ll1_opy_ (u"ࠢࠣࠤࡊࡩࡹࠦࡴࡩࡧࠣࡴࡦࡺࡨࠡࡨࡲࡶࠥࡺࡨࡦࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡕࡇࡏࠥࡨࡩ࡯ࡣࡵࡽࠥ࡯࡮ࠡࡣࠣࡻࡷ࡯ࡴࡢࡤ࡯ࡩࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹ࠯ࠤࠥࠦể")
    bstack111l111l111_opy_ = [
        os.path.join(bstack1ll11lll111_opy_, f)
        for f in os.listdir(bstack1ll11lll111_opy_)
        if os.path.isfile(os.path.join(bstack1ll11lll111_opy_, f)) and f.startswith(bstack11l1ll1_opy_ (u"ࠣࡤ࡬ࡲࡦࡸࡹ࠮ࠤỄ"))
    ]
    if len(bstack111l111l111_opy_) > 0:
        return max(bstack111l111l111_opy_, key=os.path.getmtime) # get bstack111l11l11l1_opy_ binary
    return bstack11l1ll1_opy_ (u"ࠤࠥễ")
def bstack11l1l11l11l_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1l1l1lllll1_opy_(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = bstack1l1l1lllll1_opy_(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack1lll1l111l_opy_(data, keys, default=None):
    bstack11l1ll1_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࡗࡦ࡬ࡥ࡭ࡻࠣ࡫ࡪࡺࠠࡢࠢࡱࡩࡸࡺࡥࡥࠢࡹࡥࡱࡻࡥࠡࡨࡵࡳࡲࠦࡡࠡࡦ࡬ࡧࡹ࡯࡯࡯ࡣࡵࡽࠥࡵࡲࠡ࡮࡬ࡷࡹ࠴ࠊࠡࠢࠣࠤ࠿ࡶࡡࡳࡣࡰࠤࡩࡧࡴࡢ࠼ࠣࡘ࡭࡫ࠠࡥ࡫ࡦࡸ࡮ࡵ࡮ࡢࡴࡼࠤࡴࡸࠠ࡭࡫ࡶࡸࠥࡺ࡯ࠡࡶࡵࡥࡻ࡫ࡲࡴࡧ࠱ࠎࠥࠦࠠࠡ࠼ࡳࡥࡷࡧ࡭ࠡ࡭ࡨࡽࡸࡀࠠࡂࠢ࡯࡭ࡸࡺࠠࡰࡨࠣ࡯ࡪࡿࡳ࠰࡫ࡱࡨ࡮ࡩࡥࡴࠢࡵࡩࡵࡸࡥࡴࡧࡱࡸ࡮ࡴࡧࠡࡶ࡫ࡩࠥࡶࡡࡵࡪ࠱ࠎࠥࠦࠠࠡ࠼ࡳࡥࡷࡧ࡭ࠡࡦࡨࡪࡦࡻ࡬ࡵ࠼࡚ࠣࡦࡲࡵࡦࠢࡷࡳࠥࡸࡥࡵࡷࡵࡲࠥ࡯ࡦࠡࡶ࡫ࡩࠥࡶࡡࡵࡪࠣࡨࡴ࡫ࡳࠡࡰࡲࡸࠥ࡫ࡸࡪࡵࡷ࠲ࠏࠦࠠࠡࠢ࠽ࡶࡪࡺࡵࡳࡰ࠽ࠤ࡙࡮ࡥࠡࡸࡤࡰࡺ࡫ࠠࡢࡶࠣࡸ࡭࡫ࠠ࡯ࡧࡶࡸࡪࡪࠠࡱࡣࡷ࡬࠱ࠦ࡯ࡳࠢࡧࡩ࡫ࡧࡵ࡭ࡶࠣ࡭࡫ࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥ࠰ࠍࠤࠥࠦࠠࠣࠤࠥỆ")
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
def bstack111ll1111_opy_(bstack111l1ll1ll1_opy_, key, value):
    bstack11l1ll1_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࡘࡺ࡯ࡳࡧࠣࡇࡑࡏࠠࡦࡰࡹ࡭ࡷࡵ࡮࡮ࡧࡱࡸࠥࡼࡡࡳ࡫ࡤࡦࡱ࡫ࡳࠡ࡯ࡤࡴࡵ࡯࡮ࡨࠢ࡬ࡲࠥࡺࡨࡦࠢࡳࡶࡴࡼࡩࡥࡧࡧࠤࡩ࡯ࡣࡵ࡫ࡲࡲࡦࡸࡹ࠯ࠌࠣࠤࠥࠦࡁࡳࡩࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡣ࡭࡫ࡢࡩࡳࡼ࡟ࡷࡣࡵࡷࡤࡳࡡࡱ࠼ࠣࡈ࡮ࡩࡴࡪࡱࡱࡥࡷࡿࠠࡵࡱࠣࡷࡹࡵࡲࡦࠢࡨࡲࡻ࡯ࡲࡰࡰࡰࡩࡳࡺࠠࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠢࡰࡥࡵࡶࡩ࡯ࡩࡶࠎࠥࠦࠠࠡࠢࠣࠤࠥࡱࡥࡺ࠼ࠣࡏࡪࡿࠠࡧࡴࡲࡱࠥࡉࡌࡊࡡࡆࡅࡕ࡙࡟ࡕࡑࡢࡇࡔࡔࡆࡊࡉࠍࠤࠥࠦࠠࠡࠢࠣࠤࡻࡧ࡬ࡶࡧ࠽ࠤ࡛ࡧ࡬ࡶࡧࠣࡪࡷࡵ࡭ࠡࡥࡲࡱࡲࡧ࡮ࡥࠢ࡯࡭ࡳ࡫ࠠࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠍࠤࠥࠦࠠࠣࠤࠥệ")
    if key in bstack1ll11lll11_opy_:
        bstack1ll1llll1_opy_ = bstack1ll11lll11_opy_[key]
        if isinstance(bstack1ll1llll1_opy_, list):
            for env_name in bstack1ll1llll1_opy_:
                bstack111l1ll1ll1_opy_[env_name] = value
        else:
            bstack111l1ll1ll1_opy_[bstack1ll1llll1_opy_] = value