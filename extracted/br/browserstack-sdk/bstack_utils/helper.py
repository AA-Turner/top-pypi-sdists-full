# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack1l1lll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack1l1l1l1_opy_ (bstack1111l11_opy_):
    global bstack11l111_opy_
    bstack11ll1l_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1l111_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l11l_opy_ = bstack11ll1l_opy_ % len (bstack1l111_opy_)
    bstack1ll11l_opy_ = bstack1l111_opy_ [:bstack1l11l_opy_] + bstack1l111_opy_ [bstack1l11l_opy_:]
    if bstack11llll_opy_:
        bstack1lll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    else:
        bstack1lll1_opy_ = str () .join ([chr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    return eval (bstack1lll1_opy_)
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
from bstack_utils.constants import (bstack11ll1l111ll_opy_, bstack1l11ll11ll_opy_, bstack1lll11ll1_opy_, bstack1ll11llll1_opy_,
                                    bstack11ll111111l_opy_, bstack11ll111l111_opy_, bstack11l1ll1l1l1_opy_, bstack11ll11l1111_opy_)
from bstack_utils.measure import measure
from bstack_utils.messages import bstack1llll11ll_opy_, bstack1llll1ll11_opy_
from bstack_utils.proxy import bstack11ll11l1_opy_, bstack11l1111ll1_opy_
from bstack_utils.constants import *
from bstack_utils import bstack1llll1l111_opy_
from bstack_utils.bstack1l1l1l11l1_opy_ import bstack111l1ll1_opy_
from browserstack_sdk._version import __version__
bstack11lll11111_opy_ = Config.bstack1ll11lll_opy_()
logger = bstack1llll1l111_opy_.get_logger(__name__, bstack1llll1l111_opy_.bstack1llll11l111_opy_())
def bstack11ll1lll11l_opy_(config):
    return config[bstack1l1l1l1_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭᪑")]
def bstack11ll1l1llll_opy_(config):
    return config[bstack1l1l1l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ᪒")]
def bstack1l1lll11_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack111lllllll1_opy_(obj):
    values = []
    bstack11l1111l1l1_opy_ = re.compile(bstack1l1l1l1_opy_ (u"ࡸࠢ࡟ࡅࡘࡗ࡙ࡕࡍࡠࡖࡄࡋࡤࡢࡤࠬࠦࠥ᪓"), re.I)
    for key in obj.keys():
        if bstack11l1111l1l1_opy_.match(key):
            values.append(obj[key])
    return values
def bstack11l11l1l111_opy_(config):
    tags = []
    tags.extend(bstack111lllllll1_opy_(os.environ))
    tags.extend(bstack111lllllll1_opy_(config))
    return tags
def bstack11l1l11llll_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack111llll1111_opy_(bstack11l11l11ll1_opy_):
    if not bstack11l11l11ll1_opy_:
        return bstack1l1l1l1_opy_ (u"ࠧࠨ᪔")
    return bstack1l1l1l1_opy_ (u"ࠣࡽࢀࠤ࠭ࢁࡽࠪࠤ᪕").format(bstack11l11l11ll1_opy_.name, bstack11l11l11ll1_opy_.email)
def bstack11lll1l111l_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack11l1l111l11_opy_ = repo.common_dir
        info = {
            bstack1l1l1l1_opy_ (u"ࠤࡶ࡬ࡦࠨ᪖"): repo.head.commit.hexsha,
            bstack1l1l1l1_opy_ (u"ࠥࡷ࡭ࡵࡲࡵࡡࡶ࡬ࡦࠨ᪗"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack1l1l1l1_opy_ (u"ࠦࡧࡸࡡ࡯ࡥ࡫ࠦ᪘"): repo.active_branch.name,
            bstack1l1l1l1_opy_ (u"ࠧࡺࡡࡨࠤ᪙"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack1l1l1l1_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡺࡥࡳࠤ᪚"): bstack111llll1111_opy_(repo.head.commit.committer),
            bstack1l1l1l1_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺࡴࡦࡴࡢࡨࡦࡺࡥࠣ᪛"): repo.head.commit.committed_datetime.isoformat(),
            bstack1l1l1l1_opy_ (u"ࠣࡣࡸࡸ࡭ࡵࡲࠣ᪜"): bstack111llll1111_opy_(repo.head.commit.author),
            bstack1l1l1l1_opy_ (u"ࠤࡤࡹࡹ࡮࡯ࡳࡡࡧࡥࡹ࡫ࠢ᪝"): repo.head.commit.authored_datetime.isoformat(),
            bstack1l1l1l1_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡢࡱࡪࡹࡳࡢࡩࡨࠦ᪞"): repo.head.commit.message,
            bstack1l1l1l1_opy_ (u"ࠦࡷࡵ࡯ࡵࠤ᪟"): repo.git.rev_parse(bstack1l1l1l1_opy_ (u"ࠧ࠳࠭ࡴࡪࡲࡻ࠲ࡺ࡯ࡱ࡮ࡨࡺࡪࡲࠢ᪠")),
            bstack1l1l1l1_opy_ (u"ࠨࡣࡰ࡯ࡰࡳࡳࡥࡧࡪࡶࡢࡨ࡮ࡸࠢ᪡"): bstack11l1l111l11_opy_,
            bstack1l1l1l1_opy_ (u"ࠢࡸࡱࡵ࡯ࡹࡸࡥࡦࡡࡪ࡭ࡹࡥࡤࡪࡴࠥ᪢"): subprocess.check_output([bstack1l1l1l1_opy_ (u"ࠣࡩ࡬ࡸࠧ᪣"), bstack1l1l1l1_opy_ (u"ࠤࡵࡩࡻ࠳ࡰࡢࡴࡶࡩࠧ᪤"), bstack1l1l1l1_opy_ (u"ࠥ࠱࠲࡭ࡩࡵ࠯ࡦࡳࡲࡳ࡯࡯࠯ࡧ࡭ࡷࠨ᪥")]).strip().decode(
                bstack1l1l1l1_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪ᪦")),
            bstack1l1l1l1_opy_ (u"ࠧࡲࡡࡴࡶࡢࡸࡦ࡭ࠢᪧ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack1l1l1l1_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡹ࡟ࡴ࡫ࡱࡧࡪࡥ࡬ࡢࡵࡷࡣࡹࡧࡧࠣ᪨"): repo.git.rev_list(
                bstack1l1l1l1_opy_ (u"ࠢࡼࡿ࠱࠲ࢀࢃࠢ᪩").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack111llll11l1_opy_ = []
        for remote in remotes:
            bstack11l1111ll11_opy_ = {
                bstack1l1l1l1_opy_ (u"ࠣࡰࡤࡱࡪࠨ᪪"): remote.name,
                bstack1l1l1l1_opy_ (u"ࠤࡸࡶࡱࠨ᪫"): remote.url,
            }
            bstack111llll11l1_opy_.append(bstack11l1111ll11_opy_)
        bstack11l11l1l11l_opy_ = {
            bstack1l1l1l1_opy_ (u"ࠥࡲࡦࡳࡥࠣ᪬"): bstack1l1l1l1_opy_ (u"ࠦ࡬࡯ࡴࠣ᪭"),
            **info,
            bstack1l1l1l1_opy_ (u"ࠧࡸࡥ࡮ࡱࡷࡩࡸࠨ᪮"): bstack111llll11l1_opy_
        }
        bstack11l11l1l11l_opy_ = bstack11l111ll1l1_opy_(bstack11l11l1l11l_opy_)
        return bstack11l11l1l11l_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack1l1l1l1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡯ࡱࡷ࡯ࡥࡹ࡯࡮ࡨࠢࡊ࡭ࡹࠦ࡭ࡦࡶࡤࡨࡦࡺࡡࠡࡹ࡬ࡸ࡭ࠦࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠤ᪯").format(err))
        return {}
def bstack11l111ll1l1_opy_(bstack11l11l1l11l_opy_):
    bstack11l1l111111_opy_ = bstack11l111ll1ll_opy_(bstack11l11l1l11l_opy_)
    if bstack11l1l111111_opy_ and bstack11l1l111111_opy_ > bstack11ll111111l_opy_:
        bstack111llll111l_opy_ = bstack11l1l111111_opy_ - bstack11ll111111l_opy_
        bstack111lllll1ll_opy_ = bstack11l11l1lll1_opy_(bstack11l11l1l11l_opy_[bstack1l1l1l1_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺ࡟࡮ࡧࡶࡷࡦ࡭ࡥࠣ᪰")], bstack111llll111l_opy_)
        bstack11l11l1l11l_opy_[bstack1l1l1l1_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡠ࡯ࡨࡷࡸࡧࡧࡦࠤ᪱")] = bstack111lllll1ll_opy_
        logger.info(bstack1l1l1l1_opy_ (u"ࠤࡗ࡬ࡪࠦࡣࡰ࡯ࡰ࡭ࡹࠦࡨࡢࡵࠣࡦࡪ࡫࡮ࠡࡶࡵࡹࡳࡩࡡࡵࡧࡧ࠲࡙ࠥࡩࡻࡧࠣࡳ࡫ࠦࡣࡰ࡯ࡰ࡭ࡹࠦࡡࡧࡶࡨࡶࠥࡺࡲࡶࡰࡦࡥࡹ࡯࡯࡯ࠢ࡬ࡷࠥࢁࡽࠡࡍࡅࠦ᪲")
                    .format(bstack11l111ll1ll_opy_(bstack11l11l1l11l_opy_) / 1024))
    return bstack11l11l1l11l_opy_
def bstack11l111ll1ll_opy_(bstack111l1l11_opy_):
    try:
        if bstack111l1l11_opy_:
            bstack11l11ll1ll1_opy_ = json.dumps(bstack111l1l11_opy_)
            bstack11l11111lll_opy_ = sys.getsizeof(bstack11l11ll1ll1_opy_)
            return bstack11l11111lll_opy_
    except Exception as e:
        logger.debug(bstack1l1l1l1_opy_ (u"ࠥࡗࡴࡳࡥࡵࡪ࡬ࡲ࡬ࠦࡷࡦࡰࡷࠤࡼࡸ࡯࡯ࡩࠣࡻ࡭࡯࡬ࡦࠢࡦࡥࡱࡩࡵ࡭ࡣࡷ࡭ࡳ࡭ࠠࡴ࡫ࡽࡩࠥࡵࡦࠡࡌࡖࡓࡓࠦ࡯ࡣ࡬ࡨࡧࡹࡀࠠࡼࡿࠥ᪳").format(e))
    return -1
def bstack11l11l1lll1_opy_(field, bstack11l111111ll_opy_):
    try:
        bstack11l111l11ll_opy_ = len(bytes(bstack11ll111l111_opy_, bstack1l1l1l1_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪ᪴")))
        bstack11l1l11l11l_opy_ = bytes(field, bstack1l1l1l1_opy_ (u"ࠬࡻࡴࡧ࠯࠻᪵ࠫ"))
        bstack11l1111l11l_opy_ = len(bstack11l1l11l11l_opy_)
        bstack11l11llll11_opy_ = ceil(bstack11l1111l11l_opy_ - bstack11l111111ll_opy_ - bstack11l111l11ll_opy_)
        if bstack11l11llll11_opy_ > 0:
            bstack111llll1ll1_opy_ = bstack11l1l11l11l_opy_[:bstack11l11llll11_opy_].decode(bstack1l1l1l1_opy_ (u"࠭ࡵࡵࡨ࠰࠼᪶ࠬ"), errors=bstack1l1l1l1_opy_ (u"ࠧࡪࡩࡱࡳࡷ࡫᪷ࠧ")) + bstack11ll111l111_opy_
            return bstack111llll1ll1_opy_
    except Exception as e:
        logger.debug(bstack1l1l1l1_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡴࡳࡷࡱࡧࡦࡺࡩ࡯ࡩࠣࡪ࡮࡫࡬ࡥ࠮ࠣࡲࡴࡺࡨࡪࡰࡪࠤࡼࡧࡳࠡࡶࡵࡹࡳࡩࡡࡵࡧࡧࠤ࡭࡫ࡲࡦ࠼ࠣࡿࢂࠨ᪸").format(e))
    return field
def bstack1l1l1ll11_opy_():
    env = os.environ
    if (bstack1l1l1l1_opy_ (u"ࠤࡍࡉࡓࡑࡉࡏࡕࡢ࡙ࡗࡒ᪹ࠢ") in env and len(env[bstack1l1l1l1_opy_ (u"ࠥࡎࡊࡔࡋࡊࡐࡖࡣ࡚ࡘࡌ᪺ࠣ")]) > 0) or (
            bstack1l1l1l1_opy_ (u"ࠦࡏࡋࡎࡌࡋࡑࡗࡤࡎࡏࡎࡇࠥ᪻") in env and len(env[bstack1l1l1l1_opy_ (u"ࠧࡐࡅࡏࡍࡌࡒࡘࡥࡈࡐࡏࡈࠦ᪼")]) > 0):
        return {
            bstack1l1l1l1_opy_ (u"ࠨ࡮ࡢ࡯ࡨ᪽ࠦ"): bstack1l1l1l1_opy_ (u"ࠢࡋࡧࡱ࡯࡮ࡴࡳࠣ᪾"),
            bstack1l1l1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ᪿࠦ"): env.get(bstack1l1l1l1_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡗࡕࡐᫀࠧ")),
            bstack1l1l1l1_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ᫁"): env.get(bstack1l1l1l1_opy_ (u"ࠦࡏࡕࡂࡠࡐࡄࡑࡊࠨ᫂")),
            bstack1l1l1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵ᫃ࠦ"): env.get(bstack1l1l1l1_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖ᫄ࠧ"))
        }
    if env.get(bstack1l1l1l1_opy_ (u"ࠢࡄࡋࠥ᫅")) == bstack1l1l1l1_opy_ (u"ࠣࡶࡵࡹࡪࠨ᫆") and bstack1lll1l1lll_opy_(env.get(bstack1l1l1l1_opy_ (u"ࠤࡆࡍࡗࡉࡌࡆࡅࡌࠦ᫇"))):
        return {
            bstack1l1l1l1_opy_ (u"ࠥࡲࡦࡳࡥࠣ᫈"): bstack1l1l1l1_opy_ (u"ࠦࡈ࡯ࡲࡤ࡮ࡨࡇࡎࠨ᫉"),
            bstack1l1l1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬᫊ࠣ"): env.get(bstack1l1l1l1_opy_ (u"ࠨࡃࡊࡔࡆࡐࡊࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤ᫋")),
            bstack1l1l1l1_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᫌ"): env.get(bstack1l1l1l1_opy_ (u"ࠣࡅࡌࡖࡈࡒࡅࡠࡌࡒࡆࠧᫍ")),
            bstack1l1l1l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᫎ"): env.get(bstack1l1l1l1_opy_ (u"ࠥࡇࡎࡘࡃࡍࡇࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࠨ᫏"))
        }
    if env.get(bstack1l1l1l1_opy_ (u"ࠦࡈࡏࠢ᫐")) == bstack1l1l1l1_opy_ (u"ࠧࡺࡲࡶࡧࠥ᫑") and bstack1lll1l1lll_opy_(env.get(bstack1l1l1l1_opy_ (u"ࠨࡔࡓࡃ࡙ࡍࡘࠨ᫒"))):
        return {
            bstack1l1l1l1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ᫓"): bstack1l1l1l1_opy_ (u"ࠣࡖࡵࡥࡻ࡯ࡳࠡࡅࡌࠦ᫔"),
            bstack1l1l1l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ᫕"): env.get(bstack1l1l1l1_opy_ (u"ࠥࡘࡗࡇࡖࡊࡕࡢࡆ࡚ࡏࡌࡅࡡ࡚ࡉࡇࡥࡕࡓࡎࠥ᫖")),
            bstack1l1l1l1_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ᫗"): env.get(bstack1l1l1l1_opy_ (u"࡚ࠧࡒࡂࡘࡌࡗࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢ᫘")),
            bstack1l1l1l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ᫙"): env.get(bstack1l1l1l1_opy_ (u"ࠢࡕࡔࡄ࡚ࡎ࡙࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨ᫚"))
        }
    if env.get(bstack1l1l1l1_opy_ (u"ࠣࡅࡌࠦ᫛")) == bstack1l1l1l1_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ᫜") and env.get(bstack1l1l1l1_opy_ (u"ࠥࡇࡎࡥࡎࡂࡏࡈࠦ᫝")) == bstack1l1l1l1_opy_ (u"ࠦࡨࡵࡤࡦࡵ࡫࡭ࡵࠨ᫞"):
        return {
            bstack1l1l1l1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ᫟"): bstack1l1l1l1_opy_ (u"ࠨࡃࡰࡦࡨࡷ࡭࡯ࡰࠣ᫠"),
            bstack1l1l1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ᫡"): None,
            bstack1l1l1l1_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ᫢"): None,
            bstack1l1l1l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ᫣"): None
        }
    if env.get(bstack1l1l1l1_opy_ (u"ࠥࡆࡎ࡚ࡂࡖࡅࡎࡉ࡙ࡥࡂࡓࡃࡑࡇࡍࠨ᫤")) and env.get(bstack1l1l1l1_opy_ (u"ࠦࡇࡏࡔࡃࡗࡆࡏࡊ࡚࡟ࡄࡑࡐࡑࡎ࡚ࠢ᫥")):
        return {
            bstack1l1l1l1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ᫦"): bstack1l1l1l1_opy_ (u"ࠨࡂࡪࡶࡥࡹࡨࡱࡥࡵࠤ᫧"),
            bstack1l1l1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ᫨"): env.get(bstack1l1l1l1_opy_ (u"ࠣࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡌࡏࡔࡠࡊࡗࡘࡕࡥࡏࡓࡋࡊࡍࡓࠨ᫩")),
            bstack1l1l1l1_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ᫪"): None,
            bstack1l1l1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ᫫"): env.get(bstack1l1l1l1_opy_ (u"ࠦࡇࡏࡔࡃࡗࡆࡏࡊ࡚࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨ᫬"))
        }
    if env.get(bstack1l1l1l1_opy_ (u"ࠧࡉࡉࠣ᫭")) == bstack1l1l1l1_opy_ (u"ࠨࡴࡳࡷࡨࠦ᫮") and bstack1lll1l1lll_opy_(env.get(bstack1l1l1l1_opy_ (u"ࠢࡅࡔࡒࡒࡊࠨ᫯"))):
        return {
            bstack1l1l1l1_opy_ (u"ࠣࡰࡤࡱࡪࠨ᫰"): bstack1l1l1l1_opy_ (u"ࠤࡇࡶࡴࡴࡥࠣ᫱"),
            bstack1l1l1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ᫲"): env.get(bstack1l1l1l1_opy_ (u"ࠦࡉࡘࡏࡏࡇࡢࡆ࡚ࡏࡌࡅࡡࡏࡍࡓࡑࠢ᫳")),
            bstack1l1l1l1_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ᫴"): None,
            bstack1l1l1l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ᫵"): env.get(bstack1l1l1l1_opy_ (u"ࠢࡅࡔࡒࡒࡊࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧ᫶"))
        }
    if env.get(bstack1l1l1l1_opy_ (u"ࠣࡅࡌࠦ᫷")) == bstack1l1l1l1_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ᫸") and bstack1lll1l1lll_opy_(env.get(bstack1l1l1l1_opy_ (u"ࠥࡗࡊࡓࡁࡑࡊࡒࡖࡊࠨ᫹"))):
        return {
            bstack1l1l1l1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᫺"): bstack1l1l1l1_opy_ (u"࡙ࠧࡥ࡮ࡣࡳ࡬ࡴࡸࡥࠣ᫻"),
            bstack1l1l1l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ᫼"): env.get(bstack1l1l1l1_opy_ (u"ࠢࡔࡇࡐࡅࡕࡎࡏࡓࡇࡢࡓࡗࡍࡁࡏࡋ࡝ࡅ࡙ࡏࡏࡏࡡࡘࡖࡑࠨ᫽")),
            bstack1l1l1l1_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ᫾"): env.get(bstack1l1l1l1_opy_ (u"ࠤࡖࡉࡒࡇࡐࡉࡑࡕࡉࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢ᫿")),
            bstack1l1l1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᬀ"): env.get(bstack1l1l1l1_opy_ (u"ࠦࡘࡋࡍࡂࡒࡋࡓࡗࡋ࡟ࡋࡑࡅࡣࡎࡊࠢᬁ"))
        }
    if env.get(bstack1l1l1l1_opy_ (u"ࠧࡉࡉࠣᬂ")) == bstack1l1l1l1_opy_ (u"ࠨࡴࡳࡷࡨࠦᬃ") and bstack1lll1l1lll_opy_(env.get(bstack1l1l1l1_opy_ (u"ࠢࡈࡋࡗࡐࡆࡈ࡟ࡄࡋࠥᬄ"))):
        return {
            bstack1l1l1l1_opy_ (u"ࠣࡰࡤࡱࡪࠨᬅ"): bstack1l1l1l1_opy_ (u"ࠤࡊ࡭ࡹࡒࡡࡣࠤᬆ"),
            bstack1l1l1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᬇ"): env.get(bstack1l1l1l1_opy_ (u"ࠦࡈࡏ࡟ࡋࡑࡅࡣ࡚ࡘࡌࠣᬈ")),
            bstack1l1l1l1_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᬉ"): env.get(bstack1l1l1l1_opy_ (u"ࠨࡃࡊࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦᬊ")),
            bstack1l1l1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᬋ"): env.get(bstack1l1l1l1_opy_ (u"ࠣࡅࡌࡣࡏࡕࡂࡠࡋࡇࠦᬌ"))
        }
    if env.get(bstack1l1l1l1_opy_ (u"ࠤࡆࡍࠧᬍ")) == bstack1l1l1l1_opy_ (u"ࠥࡸࡷࡻࡥࠣᬎ") and bstack1lll1l1lll_opy_(env.get(bstack1l1l1l1_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡎࡍ࡙ࡋࠢᬏ"))):
        return {
            bstack1l1l1l1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᬐ"): bstack1l1l1l1_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡰ࡯ࡴࡦࠤᬑ"),
            bstack1l1l1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᬒ"): env.get(bstack1l1l1l1_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢᬓ")),
            bstack1l1l1l1_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᬔ"): env.get(bstack1l1l1l1_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡍࡌࡘࡊࡥࡌࡂࡄࡈࡐࠧᬕ")) or env.get(bstack1l1l1l1_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡎࡍ࡙ࡋ࡟ࡑࡋࡓࡉࡑࡏࡎࡆࡡࡑࡅࡒࡋࠢᬖ")),
            bstack1l1l1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᬗ"): env.get(bstack1l1l1l1_opy_ (u"ࠨࡂࡖࡋࡏࡈࡐࡏࡔࡆࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣᬘ"))
        }
    if bstack1lll1l1lll_opy_(env.get(bstack1l1l1l1_opy_ (u"ࠢࡕࡈࡢࡆ࡚ࡏࡌࡅࠤᬙ"))):
        return {
            bstack1l1l1l1_opy_ (u"ࠣࡰࡤࡱࡪࠨᬚ"): bstack1l1l1l1_opy_ (u"ࠤ࡙࡭ࡸࡻࡡ࡭ࠢࡖࡸࡺࡪࡩࡰࠢࡗࡩࡦࡳࠠࡔࡧࡵࡺ࡮ࡩࡥࡴࠤᬛ"),
            bstack1l1l1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᬜ"): bstack1l1l1l1_opy_ (u"ࠦࢀࢃࡻࡾࠤᬝ").format(env.get(bstack1l1l1l1_opy_ (u"࡙࡙ࠬࡔࡖࡈࡑࡤ࡚ࡅࡂࡏࡉࡓ࡚ࡔࡄࡂࡖࡌࡓࡓ࡙ࡅࡓࡘࡈࡖ࡚ࡘࡉࠨᬞ")), env.get(bstack1l1l1l1_opy_ (u"࠭ࡓ࡚ࡕࡗࡉࡒࡥࡔࡆࡃࡐࡔࡗࡕࡊࡆࡅࡗࡍࡉ࠭ᬟ"))),
            bstack1l1l1l1_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᬠ"): env.get(bstack1l1l1l1_opy_ (u"ࠣࡕ࡜ࡗ࡙ࡋࡍࡠࡆࡈࡊࡎࡔࡉࡕࡋࡒࡒࡎࡊࠢᬡ")),
            bstack1l1l1l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᬢ"): env.get(bstack1l1l1l1_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡊࡆࠥᬣ"))
        }
    if bstack1lll1l1lll_opy_(env.get(bstack1l1l1l1_opy_ (u"ࠦࡆࡖࡐࡗࡇ࡜ࡓࡗࠨᬤ"))):
        return {
            bstack1l1l1l1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᬥ"): bstack1l1l1l1_opy_ (u"ࠨࡁࡱࡲࡹࡩࡾࡵࡲࠣᬦ"),
            bstack1l1l1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᬧ"): bstack1l1l1l1_opy_ (u"ࠣࡽࢀ࠳ࡵࡸ࡯࡫ࡧࡦࡸ࠴ࢁࡽ࠰ࡽࢀ࠳ࡧࡻࡩ࡭ࡦࡶ࠳ࢀࢃࠢᬨ").format(env.get(bstack1l1l1l1_opy_ (u"ࠩࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣ࡚ࡘࡌࠨᬩ")), env.get(bstack1l1l1l1_opy_ (u"ࠪࡅࡕࡖࡖࡆ࡛ࡒࡖࡤࡇࡃࡄࡑࡘࡒ࡙ࡥࡎࡂࡏࡈࠫᬪ")), env.get(bstack1l1l1l1_opy_ (u"ࠫࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡐࡓࡑࡍࡉࡈ࡚࡟ࡔࡎࡘࡋࠬᬫ")), env.get(bstack1l1l1l1_opy_ (u"ࠬࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠩᬬ"))),
            bstack1l1l1l1_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᬭ"): env.get(bstack1l1l1l1_opy_ (u"ࠢࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦᬮ")),
            bstack1l1l1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᬯ"): env.get(bstack1l1l1l1_opy_ (u"ࠤࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥᬰ"))
        }
    if env.get(bstack1l1l1l1_opy_ (u"ࠥࡅ࡟࡛ࡒࡆࡡࡋࡘ࡙ࡖ࡟ࡖࡕࡈࡖࡤࡇࡇࡆࡐࡗࠦᬱ")) and env.get(bstack1l1l1l1_opy_ (u"࡙ࠦࡌ࡟ࡃࡗࡌࡐࡉࠨᬲ")):
        return {
            bstack1l1l1l1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᬳ"): bstack1l1l1l1_opy_ (u"ࠨࡁࡻࡷࡵࡩࠥࡉࡉ᬴ࠣ"),
            bstack1l1l1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᬵ"): bstack1l1l1l1_opy_ (u"ࠣࡽࢀࡿࢂ࠵࡟ࡣࡷ࡬ࡰࡩ࠵ࡲࡦࡵࡸࡰࡹࡹ࠿ࡣࡷ࡬ࡰࡩࡏࡤ࠾ࡽࢀࠦᬶ").format(env.get(bstack1l1l1l1_opy_ (u"ࠩࡖ࡝ࡘ࡚ࡅࡎࡡࡗࡉࡆࡓࡆࡐࡗࡑࡈࡆ࡚ࡉࡐࡐࡖࡉࡗ࡜ࡅࡓࡗࡕࡍࠬᬷ")), env.get(bstack1l1l1l1_opy_ (u"ࠪࡗ࡞࡙ࡔࡆࡏࡢࡘࡊࡇࡍࡑࡔࡒࡎࡊࡉࡔࠨᬸ")), env.get(bstack1l1l1l1_opy_ (u"ࠫࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡋࡇࠫᬹ"))),
            bstack1l1l1l1_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᬺ"): env.get(bstack1l1l1l1_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡍࡉࠨᬻ")),
            bstack1l1l1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᬼ"): env.get(bstack1l1l1l1_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡏࡄࠣᬽ"))
        }
    if any([env.get(bstack1l1l1l1_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠢᬾ")), env.get(bstack1l1l1l1_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡒࡆࡕࡒࡐ࡛ࡋࡄࡠࡕࡒ࡙ࡗࡉࡅࡠࡘࡈࡖࡘࡏࡏࡏࠤᬿ")), env.get(bstack1l1l1l1_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡔࡑࡘࡖࡈࡋ࡟ࡗࡇࡕࡗࡎࡕࡎࠣᭀ"))]):
        return {
            bstack1l1l1l1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᭁ"): bstack1l1l1l1_opy_ (u"ࠨࡁࡘࡕࠣࡇࡴࡪࡥࡃࡷ࡬ࡰࡩࠨᭂ"),
            bstack1l1l1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᭃ"): env.get(bstack1l1l1l1_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡕ࡛ࡂࡍࡋࡆࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒ᭄ࠢ")),
            bstack1l1l1l1_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᭅ"): env.get(bstack1l1l1l1_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠣᭆ")),
            bstack1l1l1l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᭇ"): env.get(bstack1l1l1l1_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠥᭈ"))
        }
    if env.get(bstack1l1l1l1_opy_ (u"ࠨࡢࡢ࡯ࡥࡳࡴࡥࡢࡶ࡫࡯ࡨࡓࡻ࡭ࡣࡧࡵࠦᭉ")):
        return {
            bstack1l1l1l1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᭊ"): bstack1l1l1l1_opy_ (u"ࠣࡄࡤࡱࡧࡵ࡯ࠣᭋ"),
            bstack1l1l1l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᭌ"): env.get(bstack1l1l1l1_opy_ (u"ࠥࡦࡦࡳࡢࡰࡱࡢࡦࡺ࡯࡬ࡥࡔࡨࡷࡺࡲࡴࡴࡗࡵࡰࠧ᭍")),
            bstack1l1l1l1_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ᭎"): env.get(bstack1l1l1l1_opy_ (u"ࠧࡨࡡ࡮ࡤࡲࡳࡤࡹࡨࡰࡴࡷࡎࡴࡨࡎࡢ࡯ࡨࠦ᭏")),
            bstack1l1l1l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ᭐"): env.get(bstack1l1l1l1_opy_ (u"ࠢࡣࡣࡰࡦࡴࡵ࡟ࡣࡷ࡬ࡰࡩࡔࡵ࡮ࡤࡨࡶࠧ᭑"))
        }
    if env.get(bstack1l1l1l1_opy_ (u"࡙ࠣࡈࡖࡈࡑࡅࡓࠤ᭒")) or env.get(bstack1l1l1l1_opy_ (u"ࠤ࡚ࡉࡗࡉࡋࡆࡔࡢࡑࡆࡏࡎࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡗ࡙ࡇࡒࡕࡇࡇࠦ᭓")):
        return {
            bstack1l1l1l1_opy_ (u"ࠥࡲࡦࡳࡥࠣ᭔"): bstack1l1l1l1_opy_ (u"ࠦ࡜࡫ࡲࡤ࡭ࡨࡶࠧ᭕"),
            bstack1l1l1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ᭖"): env.get(bstack1l1l1l1_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘ࡟ࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥ᭗")),
            bstack1l1l1l1_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ᭘"): bstack1l1l1l1_opy_ (u"ࠣࡏࡤ࡭ࡳࠦࡐࡪࡲࡨࡰ࡮ࡴࡥࠣ᭙") if env.get(bstack1l1l1l1_opy_ (u"ࠤ࡚ࡉࡗࡉࡋࡆࡔࡢࡑࡆࡏࡎࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡗ࡙ࡇࡒࡕࡇࡇࠦ᭚")) else None,
            bstack1l1l1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ᭛"): env.get(bstack1l1l1l1_opy_ (u"ࠦ࡜ࡋࡒࡄࡍࡈࡖࡤࡍࡉࡕࡡࡆࡓࡒࡓࡉࡕࠤ᭜"))
        }
    if any([env.get(bstack1l1l1l1_opy_ (u"ࠧࡍࡃࡑࡡࡓࡖࡔࡐࡅࡄࡖࠥ᭝")), env.get(bstack1l1l1l1_opy_ (u"ࠨࡇࡄࡎࡒ࡙ࡉࡥࡐࡓࡑࡍࡉࡈ࡚ࠢ᭞")), env.get(bstack1l1l1l1_opy_ (u"ࠢࡈࡑࡒࡋࡑࡋ࡟ࡄࡎࡒ࡙ࡉࡥࡐࡓࡑࡍࡉࡈ࡚ࠢ᭟"))]):
        return {
            bstack1l1l1l1_opy_ (u"ࠣࡰࡤࡱࡪࠨ᭠"): bstack1l1l1l1_opy_ (u"ࠤࡊࡳࡴ࡭࡬ࡦࠢࡆࡰࡴࡻࡤࠣ᭡"),
            bstack1l1l1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ᭢"): None,
            bstack1l1l1l1_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ᭣"): env.get(bstack1l1l1l1_opy_ (u"ࠧࡖࡒࡐࡌࡈࡇ࡙ࡥࡉࡅࠤ᭤")),
            bstack1l1l1l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ᭥"): env.get(bstack1l1l1l1_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡉࡅࠤ᭦"))
        }
    if env.get(bstack1l1l1l1_opy_ (u"ࠣࡕࡋࡍࡕࡖࡁࡃࡎࡈࠦ᭧")):
        return {
            bstack1l1l1l1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᭨"): bstack1l1l1l1_opy_ (u"ࠥࡗ࡭࡯ࡰࡱࡣࡥࡰࡪࠨ᭩"),
            bstack1l1l1l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ᭪"): env.get(bstack1l1l1l1_opy_ (u"࡙ࠧࡈࡊࡒࡓࡅࡇࡒࡅࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦ᭫")),
            bstack1l1l1l1_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥ᭬ࠣ"): bstack1l1l1l1_opy_ (u"ࠢࡋࡱࡥࠤࠨࢁࡽࠣ᭭").format(env.get(bstack1l1l1l1_opy_ (u"ࠨࡕࡋࡍࡕࡖࡁࡃࡎࡈࡣࡏࡕࡂࡠࡋࡇࠫ᭮"))) if env.get(bstack1l1l1l1_opy_ (u"ࠤࡖࡌࡎࡖࡐࡂࡄࡏࡉࡤࡐࡏࡃࡡࡌࡈࠧ᭯")) else None,
            bstack1l1l1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ᭰"): env.get(bstack1l1l1l1_opy_ (u"ࠦࡘࡎࡉࡑࡒࡄࡆࡑࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨ᭱"))
        }
    if bstack1lll1l1lll_opy_(env.get(bstack1l1l1l1_opy_ (u"ࠧࡔࡅࡕࡎࡌࡊ࡞ࠨ᭲"))):
        return {
            bstack1l1l1l1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ᭳"): bstack1l1l1l1_opy_ (u"ࠢࡏࡧࡷࡰ࡮࡬ࡹࠣ᭴"),
            bstack1l1l1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ᭵"): env.get(bstack1l1l1l1_opy_ (u"ࠤࡇࡉࡕࡒࡏ࡚ࡡࡘࡖࡑࠨ᭶")),
            bstack1l1l1l1_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ᭷"): env.get(bstack1l1l1l1_opy_ (u"ࠦࡘࡏࡔࡆࡡࡑࡅࡒࡋࠢ᭸")),
            bstack1l1l1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ᭹"): env.get(bstack1l1l1l1_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡏࡄࠣ᭺"))
        }
    if bstack1lll1l1lll_opy_(env.get(bstack1l1l1l1_opy_ (u"ࠢࡈࡋࡗࡌ࡚ࡈ࡟ࡂࡅࡗࡍࡔࡔࡓࠣ᭻"))):
        return {
            bstack1l1l1l1_opy_ (u"ࠣࡰࡤࡱࡪࠨ᭼"): bstack1l1l1l1_opy_ (u"ࠤࡊ࡭ࡹࡎࡵࡣࠢࡄࡧࡹ࡯࡯࡯ࡵࠥ᭽"),
            bstack1l1l1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ᭾"): bstack1l1l1l1_opy_ (u"ࠦࢀࢃ࠯ࡼࡿ࠲ࡥࡨࡺࡩࡰࡰࡶ࠳ࡷࡻ࡮ࡴ࠱ࡾࢁࠧ᭿").format(env.get(bstack1l1l1l1_opy_ (u"ࠬࡍࡉࡕࡊࡘࡆࡤ࡙ࡅࡓࡘࡈࡖࡤ࡛ࡒࡍࠩᮀ")), env.get(bstack1l1l1l1_opy_ (u"࠭ࡇࡊࡖࡋ࡙ࡇࡥࡒࡆࡒࡒࡗࡎ࡚ࡏࡓ࡛ࠪᮁ")), env.get(bstack1l1l1l1_opy_ (u"ࠧࡈࡋࡗࡌ࡚ࡈ࡟ࡓࡗࡑࡣࡎࡊࠧᮂ"))),
            bstack1l1l1l1_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᮃ"): env.get(bstack1l1l1l1_opy_ (u"ࠤࡊࡍ࡙ࡎࡕࡃࡡ࡚ࡓࡗࡑࡆࡍࡑ࡚ࠦᮄ")),
            bstack1l1l1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᮅ"): env.get(bstack1l1l1l1_opy_ (u"ࠦࡌࡏࡔࡉࡗࡅࡣࡗ࡛ࡎࡠࡋࡇࠦᮆ"))
        }
    if env.get(bstack1l1l1l1_opy_ (u"ࠧࡉࡉࠣᮇ")) == bstack1l1l1l1_opy_ (u"ࠨࡴࡳࡷࡨࠦᮈ") and env.get(bstack1l1l1l1_opy_ (u"ࠢࡗࡇࡕࡇࡊࡒࠢᮉ")) == bstack1l1l1l1_opy_ (u"ࠣ࠳ࠥᮊ"):
        return {
            bstack1l1l1l1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᮋ"): bstack1l1l1l1_opy_ (u"࡚ࠥࡪࡸࡣࡦ࡮ࠥᮌ"),
            bstack1l1l1l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᮍ"): bstack1l1l1l1_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࢁࡽࠣᮎ").format(env.get(bstack1l1l1l1_opy_ (u"࠭ࡖࡆࡔࡆࡉࡑࡥࡕࡓࡎࠪᮏ"))),
            bstack1l1l1l1_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᮐ"): None,
            bstack1l1l1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᮑ"): None,
        }
    if env.get(bstack1l1l1l1_opy_ (u"ࠤࡗࡉࡆࡓࡃࡊࡖ࡜ࡣ࡛ࡋࡒࡔࡋࡒࡒࠧᮒ")):
        return {
            bstack1l1l1l1_opy_ (u"ࠥࡲࡦࡳࡥࠣᮓ"): bstack1l1l1l1_opy_ (u"࡙ࠦ࡫ࡡ࡮ࡥ࡬ࡸࡾࠨᮔ"),
            bstack1l1l1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᮕ"): None,
            bstack1l1l1l1_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᮖ"): env.get(bstack1l1l1l1_opy_ (u"ࠢࡕࡇࡄࡑࡈࡏࡔ࡚ࡡࡓࡖࡔࡐࡅࡄࡖࡢࡒࡆࡓࡅࠣᮗ")),
            bstack1l1l1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᮘ"): env.get(bstack1l1l1l1_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣᮙ"))
        }
    if any([env.get(bstack1l1l1l1_opy_ (u"ࠥࡇࡔࡔࡃࡐࡗࡕࡗࡊࠨᮚ")), env.get(bstack1l1l1l1_opy_ (u"ࠦࡈࡕࡎࡄࡑࡘࡖࡘࡋ࡟ࡖࡔࡏࠦᮛ")), env.get(bstack1l1l1l1_opy_ (u"ࠧࡉࡏࡏࡅࡒ࡙ࡗ࡙ࡅࡠࡗࡖࡉࡗࡔࡁࡎࡇࠥᮜ")), env.get(bstack1l1l1l1_opy_ (u"ࠨࡃࡐࡐࡆࡓ࡚ࡘࡓࡆࡡࡗࡉࡆࡓࠢᮝ"))]):
        return {
            bstack1l1l1l1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᮞ"): bstack1l1l1l1_opy_ (u"ࠣࡅࡲࡲࡨࡵࡵࡳࡵࡨࠦᮟ"),
            bstack1l1l1l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᮠ"): None,
            bstack1l1l1l1_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᮡ"): env.get(bstack1l1l1l1_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧᮢ")) or None,
            bstack1l1l1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᮣ"): env.get(bstack1l1l1l1_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡏࡄࠣᮤ"), 0)
        }
    if env.get(bstack1l1l1l1_opy_ (u"ࠢࡈࡑࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧᮥ")):
        return {
            bstack1l1l1l1_opy_ (u"ࠣࡰࡤࡱࡪࠨᮦ"): bstack1l1l1l1_opy_ (u"ࠤࡊࡳࡈࡊࠢᮧ"),
            bstack1l1l1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᮨ"): None,
            bstack1l1l1l1_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᮩ"): env.get(bstack1l1l1l1_opy_ (u"ࠧࡍࡏࡠࡌࡒࡆࡤࡔࡁࡎࡇ᮪ࠥ")),
            bstack1l1l1l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶ᮫ࠧ"): env.get(bstack1l1l1l1_opy_ (u"ࠢࡈࡑࡢࡔࡎࡖࡅࡍࡋࡑࡉࡤࡉࡏࡖࡐࡗࡉࡗࠨᮬ"))
        }
    if env.get(bstack1l1l1l1_opy_ (u"ࠣࡅࡉࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࠨᮭ")):
        return {
            bstack1l1l1l1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᮮ"): bstack1l1l1l1_opy_ (u"ࠥࡇࡴࡪࡥࡇࡴࡨࡷ࡭ࠨᮯ"),
            bstack1l1l1l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ᮰"): env.get(bstack1l1l1l1_opy_ (u"ࠧࡉࡆࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦ᮱")),
            bstack1l1l1l1_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ᮲"): env.get(bstack1l1l1l1_opy_ (u"ࠢࡄࡈࡢࡔࡎࡖࡅࡍࡋࡑࡉࡤࡔࡁࡎࡇࠥ᮳")),
            bstack1l1l1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ᮴"): env.get(bstack1l1l1l1_opy_ (u"ࠤࡆࡊࡤࡈࡕࡊࡎࡇࡣࡎࡊࠢ᮵"))
        }
    return {bstack1l1l1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ᮶"): None}
def get_host_info():
    return {
        bstack1l1l1l1_opy_ (u"ࠦ࡭ࡵࡳࡵࡰࡤࡱࡪࠨ᮷"): platform.node(),
        bstack1l1l1l1_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࠢ᮸"): platform.system(),
        bstack1l1l1l1_opy_ (u"ࠨࡴࡺࡲࡨࠦ᮹"): platform.machine(),
        bstack1l1l1l1_opy_ (u"ࠢࡷࡧࡵࡷ࡮ࡵ࡮ࠣᮺ"): platform.version(),
        bstack1l1l1l1_opy_ (u"ࠣࡣࡵࡧ࡭ࠨᮻ"): platform.architecture()[0]
    }
def bstack11l11l11l1_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack11l11lll1ll_opy_():
    if bstack11lll11111_opy_.get_property(bstack1l1l1l1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࠪᮼ")):
        return bstack1l1l1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩᮽ")
    return bstack1l1l1l1_opy_ (u"ࠫࡺࡴ࡫࡯ࡱࡺࡲࡤ࡭ࡲࡪࡦࠪᮾ")
def bstack111llll1lll_opy_(driver):
    info = {
        bstack1l1l1l1_opy_ (u"ࠬࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᮿ"): driver.capabilities,
        bstack1l1l1l1_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࠪᯀ"): driver.session_id,
        bstack1l1l1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨᯁ"): driver.capabilities.get(bstack1l1l1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ᯂ"), None),
        bstack1l1l1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫᯃ"): driver.capabilities.get(bstack1l1l1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᯄ"), None),
        bstack1l1l1l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࠭ᯅ"): driver.capabilities.get(bstack1l1l1l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠫᯆ"), None),
        bstack1l1l1l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᯇ"):driver.capabilities.get(bstack1l1l1l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩᯈ"), None),
    }
    if bstack11l11lll1ll_opy_() == bstack1l1l1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧᯉ"):
        if bstack1lll1111_opy_():
            info[bstack1l1l1l1_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࠪᯊ")] = bstack1l1l1l1_opy_ (u"ࠪࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦࠩᯋ")
        elif driver.capabilities.get(bstack1l1l1l1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᯌ"), {}).get(bstack1l1l1l1_opy_ (u"ࠬࡺࡵࡳࡤࡲࡷࡨࡧ࡬ࡦࠩᯍ"), False):
            info[bstack1l1l1l1_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺࠧᯎ")] = bstack1l1l1l1_opy_ (u"ࠧࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨࠫᯏ")
        else:
            info[bstack1l1l1l1_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࠩᯐ")] = bstack1l1l1l1_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫᯑ")
    return info
def bstack1lll1111_opy_():
    if bstack11lll11111_opy_.get_property(bstack1l1l1l1_opy_ (u"ࠪࡥࡵࡶ࡟ࡢࡷࡷࡳࡲࡧࡴࡦࠩᯒ")):
        return True
    if bstack1lll1l1lll_opy_(os.environ.get(bstack1l1l1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬᯓ"), None)):
        return True
    return False
def bstack1l1llll1ll_opy_(bstack11l11l1l1l1_opy_, url, data, config):
    headers = config.get(bstack1l1l1l1_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭ᯔ"), None)
    proxies = bstack11ll11l1_opy_(config, url)
    auth = config.get(bstack1l1l1l1_opy_ (u"࠭ࡡࡶࡶ࡫ࠫᯕ"), None)
    response = requests.request(
            bstack11l11l1l1l1_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack11lll11l11_opy_(bstack11lll1lll_opy_, size):
    bstack11l1l11l1_opy_ = []
    while len(bstack11lll1lll_opy_) > size:
        bstack1l1ll1l111_opy_ = bstack11lll1lll_opy_[:size]
        bstack11l1l11l1_opy_.append(bstack1l1ll1l111_opy_)
        bstack11lll1lll_opy_ = bstack11lll1lll_opy_[size:]
    bstack11l1l11l1_opy_.append(bstack11lll1lll_opy_)
    return bstack11l1l11l1_opy_
def bstack11l1l11l1ll_opy_(message, bstack11l111lll11_opy_=False):
    os.write(1, bytes(message, bstack1l1l1l1_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭ᯖ")))
    os.write(1, bytes(bstack1l1l1l1_opy_ (u"ࠨ࡞ࡱࠫᯗ"), bstack1l1l1l1_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨᯘ")))
    if bstack11l111lll11_opy_:
        with open(bstack1l1l1l1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠰ࡳ࠶࠷ࡹ࠮ࠩᯙ") + os.environ[bstack1l1l1l1_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡉࡃࡖࡌࡊࡊ࡟ࡊࡆࠪᯚ")] + bstack1l1l1l1_opy_ (u"ࠬ࠴࡬ࡰࡩࠪᯛ"), bstack1l1l1l1_opy_ (u"࠭ࡡࠨᯜ")) as f:
            f.write(message + bstack1l1l1l1_opy_ (u"ࠧ࡝ࡰࠪᯝ"))
def bstack1l1lll11ll1_opy_():
    return os.environ[bstack1l1l1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫᯞ")].lower() == bstack1l1l1l1_opy_ (u"ࠩࡷࡶࡺ࡫ࠧᯟ")
def bstack1lllll1l1l_opy_():
    return bstack111ll111l1_opy_().replace(tzinfo=None).isoformat() + bstack1l1l1l1_opy_ (u"ࠪ࡞ࠬᯠ")
def bstack11l11ll11l1_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack1l1l1l1_opy_ (u"ࠫ࡟࠭ᯡ"))) - datetime.datetime.fromisoformat(start.rstrip(bstack1l1l1l1_opy_ (u"ࠬࡠࠧᯢ")))).total_seconds() * 1000
def bstack11l1111l111_opy_(timestamp):
    return bstack11l11l11l11_opy_(timestamp).isoformat() + bstack1l1l1l1_opy_ (u"࡚࠭ࠨᯣ")
def bstack11l11l111l1_opy_(bstack11l1l111lll_opy_):
    date_format = bstack1l1l1l1_opy_ (u"࡛ࠧࠦࠨࡱࠪࡪࠠࠦࡊ࠽ࠩࡒࡀࠥࡔ࠰ࠨࡪࠬᯤ")
    bstack11l11lll111_opy_ = datetime.datetime.strptime(bstack11l1l111lll_opy_, date_format)
    return bstack11l11lll111_opy_.isoformat() + bstack1l1l1l1_opy_ (u"ࠨ࡜ࠪᯥ")
def bstack11l11ll11ll_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack1l1l1l1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥ᯦ࠩ")
    else:
        return bstack1l1l1l1_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᯧ")
def bstack1lll1l1lll_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack1l1l1l1_opy_ (u"ࠫࡹࡸࡵࡦࠩᯨ")
def bstack11l111l111l_opy_(val):
    return val.__str__().lower() == bstack1l1l1l1_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫᯩ")
def bstack111ll11111_opy_(bstack111llllll11_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack111llllll11_opy_ as e:
                print(bstack1l1l1l1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࡼࡿࠣ࠱ࡃࠦࡻࡾ࠼ࠣࡿࢂࠨᯪ").format(func.__name__, bstack111llllll11_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack111llll11ll_opy_(bstack11l11l1ll11_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack11l11l1ll11_opy_(cls, *args, **kwargs)
            except bstack111llllll11_opy_ as e:
                print(bstack1l1l1l1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠡࡽࢀࠤ࠲ࡄࠠࡼࡿ࠽ࠤࢀࢃࠢᯫ").format(bstack11l11l1ll11_opy_.__name__, bstack111llllll11_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack111llll11ll_opy_
    else:
        return decorator
def bstack11l1l1l1_opy_(bstack1111ll11ll_opy_):
    if os.getenv(bstack1l1l1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫᯬ")) is not None:
        return bstack1lll1l1lll_opy_(os.getenv(bstack1l1l1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠬᯭ")))
    if bstack1l1l1l1_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᯮ") in bstack1111ll11ll_opy_ and bstack11l111l111l_opy_(bstack1111ll11ll_opy_[bstack1l1l1l1_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᯯ")]):
        return False
    if bstack1l1l1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᯰ") in bstack1111ll11ll_opy_ and bstack11l111l111l_opy_(bstack1111ll11ll_opy_[bstack1l1l1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᯱ")]):
        return False
    return True
def bstack11lll111l1_opy_():
    try:
        from pytest_bdd import reporting
        bstack11l1l11111l_opy_ = os.environ.get(bstack1l1l1l1_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡕࡔࡇࡕࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑ᯲ࠢ"), None)
        return bstack11l1l11111l_opy_ is None or bstack11l1l11111l_opy_ == bstack1l1l1l1_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨ᯳ࠧ")
    except Exception as e:
        return False
def bstack11l111llll_opy_(hub_url, CONFIG):
    if bstack11lll1l11l_opy_() <= version.parse(bstack1l1l1l1_opy_ (u"ࠩ࠶࠲࠶࠹࠮࠱ࠩ᯴")):
        if hub_url:
            return bstack1l1l1l1_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦ᯵") + hub_url + bstack1l1l1l1_opy_ (u"ࠦ࠿࠾࠰࠰ࡹࡧ࠳࡭ࡻࡢࠣ᯶")
        return bstack1lll11ll1_opy_
    if hub_url:
        return bstack1l1l1l1_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࠢ᯷") + hub_url + bstack1l1l1l1_opy_ (u"ࠨ࠯ࡸࡦ࠲࡬ࡺࡨࠢ᯸")
    return bstack1ll11llll1_opy_
def bstack11l11l11lll_opy_():
    return isinstance(os.getenv(bstack1l1l1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐ࡚ࡖࡈࡗ࡙ࡥࡐࡍࡗࡊࡍࡓ࠭᯹")), str)
def bstack1l1lll111_opy_(url):
    return urlparse(url).hostname
def bstack1l11lll1l_opy_(hostname):
    for bstack111ll111l_opy_ in bstack1l11ll11ll_opy_:
        regex = re.compile(bstack111ll111l_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack11l1l1l1111_opy_(bstack11l11111111_opy_, file_name, logger):
    bstack11l1llll_opy_ = os.path.join(os.path.expanduser(bstack1l1l1l1_opy_ (u"ࠨࢀࠪ᯺")), bstack11l11111111_opy_)
    try:
        if not os.path.exists(bstack11l1llll_opy_):
            os.makedirs(bstack11l1llll_opy_)
        file_path = os.path.join(os.path.expanduser(bstack1l1l1l1_opy_ (u"ࠩࢁࠫ᯻")), bstack11l11111111_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack1l1l1l1_opy_ (u"ࠪࡻࠬ᯼")):
                pass
            with open(file_path, bstack1l1l1l1_opy_ (u"ࠦࡼ࠱ࠢ᯽")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack1llll11ll_opy_.format(str(e)))
def bstack11l111l1l11_opy_(file_name, key, value, logger):
    file_path = bstack11l1l1l1111_opy_(bstack1l1l1l1_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ᯾"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1lllll1ll1_opy_ = json.load(open(file_path, bstack1l1l1l1_opy_ (u"࠭ࡲࡣࠩ᯿")))
        else:
            bstack1lllll1ll1_opy_ = {}
        bstack1lllll1ll1_opy_[key] = value
        with open(file_path, bstack1l1l1l1_opy_ (u"ࠢࡸ࠭ࠥᰀ")) as outfile:
            json.dump(bstack1lllll1ll1_opy_, outfile)
def bstack11ll1l111l_opy_(file_name, logger):
    file_path = bstack11l1l1l1111_opy_(bstack1l1l1l1_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨᰁ"), file_name, logger)
    bstack1lllll1ll1_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack1l1l1l1_opy_ (u"ࠩࡵࠫᰂ")) as bstack1111l1l1l_opy_:
            bstack1lllll1ll1_opy_ = json.load(bstack1111l1l1l_opy_)
    return bstack1lllll1ll1_opy_
def bstack111ll11l_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack1l1l1l1_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡪࡥ࡭ࡧࡷ࡭ࡳ࡭ࠠࡧ࡫࡯ࡩ࠿ࠦࠧᰃ") + file_path + bstack1l1l1l1_opy_ (u"ࠫࠥ࠭ᰄ") + str(e))
def bstack11lll1l11l_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack1l1l1l1_opy_ (u"ࠧࡂࡎࡐࡖࡖࡉ࡙ࡄࠢᰅ")
def bstack111l1l1l1_opy_(config):
    if bstack1l1l1l1_opy_ (u"࠭ࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬᰆ") in config:
        del (config[bstack1l1l1l1_opy_ (u"ࠧࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ᰇ")])
        return False
    if bstack11lll1l11l_opy_() < version.parse(bstack1l1l1l1_opy_ (u"ࠨ࠵࠱࠸࠳࠶ࠧᰈ")):
        return False
    if bstack11lll1l11l_opy_() >= version.parse(bstack1l1l1l1_opy_ (u"ࠩ࠷࠲࠶࠴࠵ࠨᰉ")):
        return True
    if bstack1l1l1l1_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪᰊ") in config and config[bstack1l1l1l1_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫᰋ")] is False:
        return False
    else:
        return True
def bstack11l1ll1l_opy_(args_list, bstack11l11111l11_opy_):
    index = -1
    for value in bstack11l11111l11_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
def bstack11lll11lll1_opy_(a, b):
  for k, v in b.items():
    if isinstance(v, dict) and k in a and isinstance(a[k], dict):
        bstack11lll11lll1_opy_(a[k], v)
    else:
        a[k] = v
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack111lll1ll1_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack111lll1ll1_opy_ = bstack111lll1ll1_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack1l1l1l1_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᰌ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack1l1l1l1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᰍ"), exception=exception)
    def bstack11111l11ll_opy_(self):
        if self.result != bstack1l1l1l1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᰎ"):
            return None
        if isinstance(self.exception_type, str) and bstack1l1l1l1_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࠦᰏ") in self.exception_type:
            return bstack1l1l1l1_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࡊࡸࡲࡰࡴࠥᰐ")
        return bstack1l1l1l1_opy_ (u"࡙ࠥࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠦᰑ")
    def bstack11l111ll11l_opy_(self):
        if self.result != bstack1l1l1l1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᰒ"):
            return None
        if self.bstack111lll1ll1_opy_:
            return self.bstack111lll1ll1_opy_
        return bstack11l111l1l1l_opy_(self.exception)
def bstack11l111l1l1l_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack11l11l1l1ll_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack111l1ll1l_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack11l1l1ll1_opy_(config, logger):
    try:
        import playwright
        bstack111llll1l11_opy_ = playwright.__file__
        bstack11l111lll1l_opy_ = os.path.split(bstack111llll1l11_opy_)
        bstack111lllll1l1_opy_ = bstack11l111lll1l_opy_[0] + bstack1l1l1l1_opy_ (u"ࠬ࠵ࡤࡳ࡫ࡹࡩࡷ࠵ࡰࡢࡥ࡮ࡥ࡬࡫࠯࡭࡫ࡥ࠳ࡨࡲࡩ࠰ࡥ࡯࡭࠳ࡰࡳࠨᰓ")
        os.environ[bstack1l1l1l1_opy_ (u"࠭ࡇࡍࡑࡅࡅࡑࡥࡁࡈࡇࡑࡘࡤࡎࡔࡕࡒࡢࡔࡗࡕࡘ࡚ࠩᰔ")] = bstack11l1111ll1_opy_(config)
        with open(bstack111lllll1l1_opy_, bstack1l1l1l1_opy_ (u"ࠧࡳࠩᰕ")) as f:
            bstack1lll11l1ll_opy_ = f.read()
            bstack11l11llll1l_opy_ = bstack1l1l1l1_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬࠮ࡣࡪࡩࡳࡺࠧᰖ")
            bstack11l11111l1l_opy_ = bstack1lll11l1ll_opy_.find(bstack11l11llll1l_opy_)
            if bstack11l11111l1l_opy_ == -1:
              process = subprocess.Popen(bstack1l1l1l1_opy_ (u"ࠤࡱࡴࡲࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡨ࡮ࡲࡦࡦࡲ࠭ࡢࡩࡨࡲࡹࠨᰗ"), shell=True, cwd=bstack11l111lll1l_opy_[0])
              process.wait()
              bstack11l1l111l1l_opy_ = bstack1l1l1l1_opy_ (u"ࠪࠦࡺࡹࡥࠡࡵࡷࡶ࡮ࡩࡴࠣ࠽ࠪᰘ")
              bstack11l1111lll1_opy_ = bstack1l1l1l1_opy_ (u"ࠦࠧࠨࠠ࡝ࠤࡸࡷࡪࠦࡳࡵࡴ࡬ࡧࡹࡢࠢ࠼ࠢࡦࡳࡳࡹࡴࠡࡽࠣࡦࡴࡵࡴࡴࡶࡵࡥࡵࠦࡽࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࠬ࡭࡬ࡰࡤࡤࡰ࠲ࡧࡧࡦࡰࡷࠫ࠮ࡁࠠࡪࡨࠣࠬࡵࡸ࡯ࡤࡧࡶࡷ࠳࡫࡮ࡷ࠰ࡊࡐࡔࡈࡁࡍࡡࡄࡋࡊࡔࡔࡠࡊࡗࡘࡕࡥࡐࡓࡑ࡛࡝࠮ࠦࡢࡰࡱࡷࡷࡹࡸࡡࡱࠪࠬ࠿ࠥࠨࠢࠣᰙ")
              bstack11l111llll1_opy_ = bstack1lll11l1ll_opy_.replace(bstack11l1l111l1l_opy_, bstack11l1111lll1_opy_)
              with open(bstack111lllll1l1_opy_, bstack1l1l1l1_opy_ (u"ࠬࡽࠧᰚ")) as f:
                f.write(bstack11l111llll1_opy_)
    except Exception as e:
        logger.error(bstack1llll1ll11_opy_.format(str(e)))
def bstack1ll1l1lll_opy_():
  try:
    bstack11l11ll1l1l_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1l1l1_opy_ (u"࠭࡯ࡱࡶ࡬ࡱࡦࡲ࡟ࡩࡷࡥࡣࡺࡸ࡬࠯࡬ࡶࡳࡳ࠭ᰛ"))
    bstack11l111l1ll1_opy_ = []
    if os.path.exists(bstack11l11ll1l1l_opy_):
      with open(bstack11l11ll1l1l_opy_) as f:
        bstack11l111l1ll1_opy_ = json.load(f)
      os.remove(bstack11l11ll1l1l_opy_)
    return bstack11l111l1ll1_opy_
  except:
    pass
  return []
def bstack11lll111_opy_(bstack1l11lll11_opy_):
  try:
    bstack11l111l1ll1_opy_ = []
    bstack11l11ll1l1l_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1l1l1_opy_ (u"ࠧࡰࡲࡷ࡭ࡲࡧ࡬ࡠࡪࡸࡦࡤࡻࡲ࡭࠰࡭ࡷࡴࡴࠧᰜ"))
    if os.path.exists(bstack11l11ll1l1l_opy_):
      with open(bstack11l11ll1l1l_opy_) as f:
        bstack11l111l1ll1_opy_ = json.load(f)
    bstack11l111l1ll1_opy_.append(bstack1l11lll11_opy_)
    with open(bstack11l11ll1l1l_opy_, bstack1l1l1l1_opy_ (u"ࠨࡹࠪᰝ")) as f:
        json.dump(bstack11l111l1ll1_opy_, f)
  except:
    pass
def bstack1ll1ll11ll_opy_(logger, bstack111llllll1l_opy_ = False):
  try:
    test_name = os.environ.get(bstack1l1l1l1_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕࡡࡗࡉࡘ࡚࡟ࡏࡃࡐࡉࠬᰞ"), bstack1l1l1l1_opy_ (u"ࠪࠫᰟ"))
    if test_name == bstack1l1l1l1_opy_ (u"ࠫࠬᰠ"):
        test_name = threading.current_thread().__dict__.get(bstack1l1l1l1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡇࡪࡤࡠࡶࡨࡷࡹࡥ࡮ࡢ࡯ࡨࠫᰡ"), bstack1l1l1l1_opy_ (u"࠭ࠧᰢ"))
    bstack11l111111l1_opy_ = bstack1l1l1l1_opy_ (u"ࠧ࠭ࠢࠪᰣ").join(threading.current_thread().bstackTestErrorMessages)
    if bstack111llllll1l_opy_:
        bstack1ll111l111_opy_ = os.environ.get(bstack1l1l1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨᰤ"), bstack1l1l1l1_opy_ (u"ࠩ࠳ࠫᰥ"))
        bstack1ll11ll1_opy_ = {bstack1l1l1l1_opy_ (u"ࠪࡲࡦࡳࡥࠨᰦ"): test_name, bstack1l1l1l1_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᰧ"): bstack11l111111l1_opy_, bstack1l1l1l1_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫᰨ"): bstack1ll111l111_opy_}
        bstack11l11ll1lll_opy_ = []
        bstack11l11l111ll_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1l1l1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡰࡱࡲࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬᰩ"))
        if os.path.exists(bstack11l11l111ll_opy_):
            with open(bstack11l11l111ll_opy_) as f:
                bstack11l11ll1lll_opy_ = json.load(f)
        bstack11l11ll1lll_opy_.append(bstack1ll11ll1_opy_)
        with open(bstack11l11l111ll_opy_, bstack1l1l1l1_opy_ (u"ࠧࡸࠩᰪ")) as f:
            json.dump(bstack11l11ll1lll_opy_, f)
    else:
        bstack1ll11ll1_opy_ = {bstack1l1l1l1_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᰫ"): test_name, bstack1l1l1l1_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨᰬ"): bstack11l111111l1_opy_, bstack1l1l1l1_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩᰭ"): str(multiprocessing.current_process().name)}
        if bstack1l1l1l1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴࠨᰮ") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack1ll11ll1_opy_)
  except Exception as e:
      logger.warn(bstack1l1l1l1_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡳࡷ࡫ࠠࡱࡻࡷࡩࡸࡺࠠࡧࡷࡱࡲࡪࡲࠠࡥࡣࡷࡥ࠿ࠦࡻࡾࠤᰯ").format(e))
def bstack11l1ll11_opy_(error_message, test_name, index, logger):
  try:
    bstack111llll1l1l_opy_ = []
    bstack1ll11ll1_opy_ = {bstack1l1l1l1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᰰ"): test_name, bstack1l1l1l1_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ᰱ"): error_message, bstack1l1l1l1_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧᰲ"): index}
    bstack11l1l1111l1_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1l1l1_opy_ (u"ࠩࡵࡳࡧࡵࡴࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰࠪᰳ"))
    if os.path.exists(bstack11l1l1111l1_opy_):
        with open(bstack11l1l1111l1_opy_) as f:
            bstack111llll1l1l_opy_ = json.load(f)
    bstack111llll1l1l_opy_.append(bstack1ll11ll1_opy_)
    with open(bstack11l1l1111l1_opy_, bstack1l1l1l1_opy_ (u"ࠪࡻࠬᰴ")) as f:
        json.dump(bstack111llll1l1l_opy_, f)
  except Exception as e:
    logger.warn(bstack1l1l1l1_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡶࡲࡶࡪࠦࡲࡰࡤࡲࡸࠥ࡬ࡵ࡯ࡰࡨࡰࠥࡪࡡࡵࡣ࠽ࠤࢀࢃࠢᰵ").format(e))
def bstack1l1ll1llll_opy_(bstack1lll11lll1_opy_, name, logger):
  try:
    bstack1ll11ll1_opy_ = {bstack1l1l1l1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᰶ"): name, bstack1l1l1l1_opy_ (u"࠭ࡥࡳࡴࡲࡶ᰷ࠬ"): bstack1lll11lll1_opy_, bstack1l1l1l1_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭᰸"): str(threading.current_thread()._name)}
    return bstack1ll11ll1_opy_
  except Exception as e:
    logger.warn(bstack1l1l1l1_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺ࡯ࡳࡧࠣࡦࡪ࡮ࡡࡷࡧࠣࡪࡺࡴ࡮ࡦ࡮ࠣࡨࡦࡺࡡ࠻ࠢࡾࢁࠧ᰹").format(e))
  return
def bstack11l11llllll_opy_():
    return platform.system() == bstack1l1l1l1_opy_ (u"࡚ࠩ࡭ࡳࡪ࡯ࡸࡵࠪ᰺")
def bstack11l1l111l1_opy_(bstack11l111ll111_opy_, config, logger):
    bstack111llllllll_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack11l111ll111_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack1l1l1l1_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡪ࡮ࡷࡩࡷࠦࡣࡰࡰࡩ࡭࡬ࠦ࡫ࡦࡻࡶࠤࡧࡿࠠࡳࡧࡪࡩࡽࠦ࡭ࡢࡶࡦ࡬࠿ࠦࡻࡾࠤ᰻").format(e))
    return bstack111llllllll_opy_
def bstack11l1l111ll1_opy_(bstack11l11l1ll1l_opy_, bstack11l1111111l_opy_):
    bstack11l111l1111_opy_ = version.parse(bstack11l11l1ll1l_opy_)
    bstack11l11l11l1l_opy_ = version.parse(bstack11l1111111l_opy_)
    if bstack11l111l1111_opy_ > bstack11l11l11l1l_opy_:
        return 1
    elif bstack11l111l1111_opy_ < bstack11l11l11l1l_opy_:
        return -1
    else:
        return 0
def bstack111ll111l1_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack11l11l11l11_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
def bstack11l1l1l111l_opy_(framework):
    from browserstack_sdk._version import __version__
    return str(framework) + str(__version__)
def bstack1ll1l1llll_opy_(options, framework, config, bstack11l111l1_opy_={}):
    if options is None:
        return
    if getattr(options, bstack1l1l1l1_opy_ (u"ࠫ࡬࡫ࡴࠨ᰼"), None):
        caps = options
    else:
        caps = options.to_capabilities()
    bstack111lllll_opy_ = caps.get(bstack1l1l1l1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭᰽"))
    bstack11l11l1llll_opy_ = True
    bstack1lll11lll_opy_ = os.environ[bstack1l1l1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ᰾")]
    bstack1ll111lllll_opy_ = config.get(bstack1l1l1l1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ᰿"), False)
    if bstack1ll111lllll_opy_:
        bstack1lll1l11ll1_opy_ = config.get(bstack1l1l1l1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ᱀"), {})
        bstack1lll1l11ll1_opy_[bstack1l1l1l1_opy_ (u"ࠩࡤࡹࡹ࡮ࡔࡰ࡭ࡨࡲࠬ᱁")] = os.getenv(bstack1l1l1l1_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨ᱂"))
        bstack11ll1llll11_opy_ = json.loads(os.getenv(bstack1l1l1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬ᱃"), bstack1l1l1l1_opy_ (u"ࠬࢁࡽࠨ᱄"))).get(bstack1l1l1l1_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ᱅"))
    if bstack11l111l111l_opy_(caps.get(bstack1l1l1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡵࡴࡧ࡚࠷ࡈ࠭᱆"))) or bstack11l111l111l_opy_(caps.get(bstack1l1l1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡶࡵࡨࡣࡼ࠹ࡣࠨ᱇"))):
        bstack11l11l1llll_opy_ = False
    if bstack111l1l1l1_opy_({bstack1l1l1l1_opy_ (u"ࠤࡸࡷࡪ࡝࠳ࡄࠤ᱈"): bstack11l11l1llll_opy_}):
        bstack111lllll_opy_ = bstack111lllll_opy_ or {}
        bstack111lllll_opy_[bstack1l1l1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬ᱉")] = bstack11l1l1l111l_opy_(framework)
        bstack111lllll_opy_[bstack1l1l1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭᱊")] = bstack1l1lll11ll1_opy_()
        bstack111lllll_opy_[bstack1l1l1l1_opy_ (u"ࠬࡺࡥࡴࡶ࡫ࡹࡧࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨ᱋")] = bstack1lll11lll_opy_
        bstack111lllll_opy_[bstack1l1l1l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨ᱌")] = bstack11l111l1_opy_
        if bstack1ll111lllll_opy_:
            bstack111lllll_opy_[bstack1l1l1l1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᱍ")] = bstack1ll111lllll_opy_
            bstack111lllll_opy_[bstack1l1l1l1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨᱎ")] = bstack1lll1l11ll1_opy_
            bstack111lllll_opy_[bstack1l1l1l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩᱏ")][bstack1l1l1l1_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ᱐")] = bstack11ll1llll11_opy_
        if getattr(options, bstack1l1l1l1_opy_ (u"ࠫࡸ࡫ࡴࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷࡽࠬ᱑"), None):
            options.set_capability(bstack1l1l1l1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭᱒"), bstack111lllll_opy_)
        else:
            options[bstack1l1l1l1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ᱓")] = bstack111lllll_opy_
    else:
        if getattr(options, bstack1l1l1l1_opy_ (u"ࠧࡴࡧࡷࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡹࠨ᱔"), None):
            options.set_capability(bstack1l1l1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩ᱕"), bstack11l1l1l111l_opy_(framework))
            options.set_capability(bstack1l1l1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪ᱖"), bstack1l1lll11ll1_opy_())
            options.set_capability(bstack1l1l1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷࡩࡸࡺࡨࡶࡤࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬ᱗"), bstack1lll11lll_opy_)
            options.set_capability(bstack1l1l1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬ᱘"), bstack11l111l1_opy_)
            if bstack1ll111lllll_opy_:
                options.set_capability(bstack1l1l1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ᱙"), bstack1ll111lllll_opy_)
                options.set_capability(bstack1l1l1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬᱚ"), bstack1lll1l11ll1_opy_)
                options.set_capability(bstack1l1l1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠴ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᱛ"), bstack11ll1llll11_opy_)
        else:
            options[bstack1l1l1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩᱜ")] = bstack11l1l1l111l_opy_(framework)
            options[bstack1l1l1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᱝ")] = bstack1l1lll11ll1_opy_()
            options[bstack1l1l1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷࡩࡸࡺࡨࡶࡤࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬᱞ")] = bstack1lll11lll_opy_
            options[bstack1l1l1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬᱟ")] = bstack11l111l1_opy_
            if bstack1ll111lllll_opy_:
                options[bstack1l1l1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᱠ")] = bstack1ll111lllll_opy_
                options[bstack1l1l1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬᱡ")] = bstack1lll1l11ll1_opy_
                options[bstack1l1l1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ᱢ")][bstack1l1l1l1_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᱣ")] = bstack11ll1llll11_opy_
    return options
def bstack111lll1llll_opy_(bstack11l11l1111l_opy_, framework):
    bstack11l111l1_opy_ = bstack11lll11111_opy_.get_property(bstack1l1l1l1_opy_ (u"ࠤࡓࡐࡆ࡟ࡗࡓࡋࡊࡌ࡙ࡥࡐࡓࡑࡇ࡙ࡈ࡚࡟ࡎࡃࡓࠦᱤ"))
    if bstack11l11l1111l_opy_ and len(bstack11l11l1111l_opy_.split(bstack1l1l1l1_opy_ (u"ࠪࡧࡦࡶࡳ࠾ࠩᱥ"))) > 1:
        ws_url = bstack11l11l1111l_opy_.split(bstack1l1l1l1_opy_ (u"ࠫࡨࡧࡰࡴ࠿ࠪᱦ"))[0]
        if bstack1l1l1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨᱧ") in ws_url:
            from browserstack_sdk._version import __version__
            bstack11l1l11l1l1_opy_ = json.loads(urllib.parse.unquote(bstack11l11l1111l_opy_.split(bstack1l1l1l1_opy_ (u"࠭ࡣࡢࡲࡶࡁࠬᱨ"))[1]))
            bstack11l1l11l1l1_opy_ = bstack11l1l11l1l1_opy_ or {}
            bstack1lll11lll_opy_ = os.environ[bstack1l1l1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬᱩ")]
            bstack11l1l11l1l1_opy_[bstack1l1l1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩᱪ")] = str(framework) + str(__version__)
            bstack11l1l11l1l1_opy_[bstack1l1l1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᱫ")] = bstack1l1lll11ll1_opy_()
            bstack11l1l11l1l1_opy_[bstack1l1l1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷࡩࡸࡺࡨࡶࡤࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬᱬ")] = bstack1lll11lll_opy_
            bstack11l1l11l1l1_opy_[bstack1l1l1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬᱭ")] = bstack11l111l1_opy_
            bstack11l11l1111l_opy_ = bstack11l11l1111l_opy_.split(bstack1l1l1l1_opy_ (u"ࠬࡩࡡࡱࡵࡀࠫᱮ"))[0] + bstack1l1l1l1_opy_ (u"࠭ࡣࡢࡲࡶࡁࠬᱯ") + urllib.parse.quote(json.dumps(bstack11l1l11l1l1_opy_))
    return bstack11l11l1111l_opy_
def bstack1111l1l1_opy_():
    global bstack1ll11111ll_opy_
    from playwright._impl._browser_type import BrowserType
    bstack1ll11111ll_opy_ = BrowserType.connect
    return bstack1ll11111ll_opy_
def bstack11l1ll1111_opy_(framework_name):
    global bstack11l11llll1_opy_
    bstack11l11llll1_opy_ = framework_name
    return framework_name
def bstack11llll111l_opy_(self, *args, **kwargs):
    global bstack1ll11111ll_opy_
    try:
        global bstack11l11llll1_opy_
        if bstack1l1l1l1_opy_ (u"ࠧࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷࠫᱰ") in kwargs:
            kwargs[bstack1l1l1l1_opy_ (u"ࠨࡹࡶࡉࡳࡪࡰࡰ࡫ࡱࡸࠬᱱ")] = bstack111lll1llll_opy_(
                kwargs.get(bstack1l1l1l1_opy_ (u"ࠩࡺࡷࡊࡴࡤࡱࡱ࡬ࡲࡹ࠭ᱲ"), None),
                bstack11l11llll1_opy_
            )
    except Exception as e:
        logger.error(bstack1l1l1l1_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬ࡪࡴࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡘࡊࡋࠡࡥࡤࡴࡸࡀࠠࡼࡿࠥᱳ").format(str(e)))
    return bstack1ll11111ll_opy_(self, *args, **kwargs)
def bstack11l1111l1ll_opy_(bstack11l1l11lll1_opy_, proxies):
    proxy_settings = {}
    try:
        if not proxies:
            proxies = bstack11ll11l1_opy_(bstack11l1l11lll1_opy_, bstack1l1l1l1_opy_ (u"ࠦࠧᱴ"))
        if proxies and proxies.get(bstack1l1l1l1_opy_ (u"ࠧ࡮ࡴࡵࡲࡶࠦᱵ")):
            parsed_url = urlparse(proxies.get(bstack1l1l1l1_opy_ (u"ࠨࡨࡵࡶࡳࡷࠧᱶ")))
            if parsed_url and parsed_url.hostname: proxy_settings[bstack1l1l1l1_opy_ (u"ࠧࡱࡴࡲࡼࡾࡎ࡯ࡴࡶࠪᱷ")] = str(parsed_url.hostname)
            if parsed_url and parsed_url.port: proxy_settings[bstack1l1l1l1_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡰࡴࡷࠫᱸ")] = str(parsed_url.port)
            if parsed_url and parsed_url.username: proxy_settings[bstack1l1l1l1_opy_ (u"ࠩࡳࡶࡴࡾࡹࡖࡵࡨࡶࠬᱹ")] = str(parsed_url.username)
            if parsed_url and parsed_url.password: proxy_settings[bstack1l1l1l1_opy_ (u"ࠪࡴࡷࡵࡸࡺࡒࡤࡷࡸ࠭ᱺ")] = str(parsed_url.password)
        return proxy_settings
    except:
        return proxy_settings
def bstack11ll111lll_opy_(bstack11l1l11lll1_opy_):
    bstack11l11lll11l_opy_ = {
        bstack11ll11l1111_opy_[bstack11l1l11ll1l_opy_]: bstack11l1l11lll1_opy_[bstack11l1l11ll1l_opy_]
        for bstack11l1l11ll1l_opy_ in bstack11l1l11lll1_opy_
        if bstack11l1l11ll1l_opy_ in bstack11ll11l1111_opy_
    }
    bstack11l11lll11l_opy_[bstack1l1l1l1_opy_ (u"ࠦࡵࡸ࡯ࡹࡻࡖࡩࡹࡺࡩ࡯ࡩࡶࠦᱻ")] = bstack11l1111l1ll_opy_(bstack11l1l11lll1_opy_, bstack11lll11111_opy_.get_property(bstack1l1l1l1_opy_ (u"ࠧࡶࡲࡰࡺࡼࡗࡪࡺࡴࡪࡰࡪࡷࠧᱼ")))
    bstack11l111lllll_opy_ = [element.lower() for element in bstack11l1ll1l1l1_opy_]
    bstack11l11l11111_opy_(bstack11l11lll11l_opy_, bstack11l111lllll_opy_)
    return bstack11l11lll11l_opy_
def bstack11l11l11111_opy_(d, keys):
    for key in list(d.keys()):
        if key.lower() in keys:
            d[key] = bstack1l1l1l1_opy_ (u"ࠨࠪࠫࠬ࠭ࠦᱽ")
    for value in d.values():
        if isinstance(value, dict):
            bstack11l11l11111_opy_(value, keys)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    bstack11l11l11111_opy_(item, keys)
def bstack1l1l1llllll_opy_():
    bstack11l11ll1111_opy_ = [os.environ.get(bstack1l1l1l1_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡊࡎࡈࡗࡤࡊࡉࡓࠤ᱾")), os.path.join(os.path.expanduser(bstack1l1l1l1_opy_ (u"ࠣࢀࠥ᱿")), bstack1l1l1l1_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩᲀ")), os.path.join(bstack1l1l1l1_opy_ (u"ࠪ࠳ࡹࡳࡰࠨᲁ"), bstack1l1l1l1_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫᲂ"))]
    for path in bstack11l11ll1111_opy_:
        if path is None:
            continue
        try:
            if os.path.exists(path):
                logger.debug(bstack1l1l1l1_opy_ (u"ࠧࡌࡩ࡭ࡧࠣࠫࠧᲃ") + str(path) + bstack1l1l1l1_opy_ (u"ࠨࠧࠡࡧࡻ࡭ࡸࡺࡳ࠯ࠤᲄ"))
                if not os.access(path, os.W_OK):
                    logger.debug(bstack1l1l1l1_opy_ (u"ࠢࡈ࡫ࡹ࡭ࡳ࡭ࠠࡱࡧࡵࡱ࡮ࡹࡳࡪࡱࡱࡷࠥ࡬࡯ࡳࠢࠪࠦᲅ") + str(path) + bstack1l1l1l1_opy_ (u"ࠣࠩࠥᲆ"))
                    os.chmod(path, 0o777)
                else:
                    logger.debug(bstack1l1l1l1_opy_ (u"ࠤࡉ࡭ࡱ࡫ࠠࠨࠤᲇ") + str(path) + bstack1l1l1l1_opy_ (u"ࠥࠫࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡨࡢࡵࠣࡸ࡭࡫ࠠࡳࡧࡴࡹ࡮ࡸࡥࡥࠢࡳࡩࡷࡳࡩࡴࡵ࡬ࡳࡳࡹ࠮ࠣᲈ"))
            else:
                logger.debug(bstack1l1l1l1_opy_ (u"ࠦࡈࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡦࡪ࡮ࡨࠤࠬࠨᲉ") + str(path) + bstack1l1l1l1_opy_ (u"ࠧ࠭ࠠࡸ࡫ࡷ࡬ࠥࡽࡲࡪࡶࡨࠤࡵ࡫ࡲ࡮࡫ࡶࡷ࡮ࡵ࡮࠯ࠤᲊ"))
                os.makedirs(path, exist_ok=True)
                os.chmod(path, 0o777)
            logger.debug(bstack1l1l1l1_opy_ (u"ࠨࡏࡱࡧࡵࡥࡹ࡯࡯࡯ࠢࡶࡹࡨࡩࡥࡦࡦࡨࡨࠥ࡬࡯ࡳࠢࠪࠦ᲋") + str(path) + bstack1l1l1l1_opy_ (u"ࠢࠨ࠰ࠥ᲌"))
            return path
        except Exception as e:
            logger.debug(bstack1l1l1l1_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࠡࡷࡳࠤ࡫࡯࡬ࡦࠢࠪࡿࡵࡧࡴࡩࡿࠪ࠾ࠥࠨ᲍") + str(e) + bstack1l1l1l1_opy_ (u"ࠤࠥ᲎"))
    logger.debug(bstack1l1l1l1_opy_ (u"ࠥࡅࡱࡲࠠࡱࡣࡷ࡬ࡸࠦࡦࡢ࡫࡯ࡩࡩ࠴ࠢ᲏"))
    return None
@measure(event_name=EVENTS.bstack11ll1111lll_opy_, stage=STAGE.bstack1l1lll1lll_opy_)
def bstack1lll1l1llll_opy_(binary_path, bstack1lll1lll1l1_opy_, bs_config):
    logger.debug(bstack1l1l1l1_opy_ (u"ࠦࡈࡻࡲࡳࡧࡱࡸࠥࡉࡌࡊࠢࡓࡥࡹ࡮ࠠࡧࡱࡸࡲࡩࡀࠠࡼࡿࠥᲐ").format(binary_path))
    bstack11l1l1l11l1_opy_ = bstack1l1l1l1_opy_ (u"ࠬ࠭Ბ")
    bstack11l11111ll1_opy_ = {
        bstack1l1l1l1_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫᲒ"): __version__,
        bstack1l1l1l1_opy_ (u"ࠢࡰࡵࠥᲓ"): platform.system(),
        bstack1l1l1l1_opy_ (u"ࠣࡱࡶࡣࡦࡸࡣࡩࠤᲔ"): platform.machine(),
        bstack1l1l1l1_opy_ (u"ࠤࡦࡰ࡮ࡥࡶࡦࡴࡶ࡭ࡴࡴࠢᲕ"): bstack1l1l1l1_opy_ (u"ࠪ࠴ࠬᲖ"),
        bstack1l1l1l1_opy_ (u"ࠦࡸࡪ࡫ࡠ࡮ࡤࡲ࡬ࡻࡡࡨࡧࠥᲗ"): bstack1l1l1l1_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬᲘ")
    }
    bstack11l1111llll_opy_(bstack11l11111ll1_opy_)
    try:
        if binary_path:
            bstack11l11111ll1_opy_[bstack1l1l1l1_opy_ (u"࠭ࡣ࡭࡫ࡢࡺࡪࡸࡳࡪࡱࡱࠫᲙ")] = subprocess.check_output([binary_path, bstack1l1l1l1_opy_ (u"ࠢࡷࡧࡵࡷ࡮ࡵ࡮ࠣᲚ")]).strip().decode(bstack1l1l1l1_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧᲛ"))
        response = requests.request(
            bstack1l1l1l1_opy_ (u"ࠩࡊࡉ࡙࠭Ნ"),
            url=bstack111l1ll1_opy_(bstack11l1llll1ll_opy_),
            headers=None,
            auth=(bs_config[bstack1l1l1l1_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬᲝ")], bs_config[bstack1l1l1l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧᲞ")]),
            json=None,
            params=bstack11l11111ll1_opy_
        )
        data = response.json()
        if response.status_code == 200 and bstack1l1l1l1_opy_ (u"ࠬࡻࡲ࡭ࠩᲟ") in data.keys() and bstack1l1l1l1_opy_ (u"࠭ࡵࡱࡦࡤࡸࡪࡪ࡟ࡤ࡮࡬ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᲠ") in data.keys():
            logger.debug(bstack1l1l1l1_opy_ (u"ࠢࡏࡧࡨࡨࠥࡺ࡯ࠡࡷࡳࡨࡦࡺࡥࠡࡤ࡬ࡲࡦࡸࡹ࠭ࠢࡦࡹࡷࡸࡥ࡯ࡶࠣࡦ࡮ࡴࡡࡳࡻࠣࡺࡪࡸࡳࡪࡱࡱ࠾ࠥࢁࡽࠣᲡ").format(bstack11l11111ll1_opy_[bstack1l1l1l1_opy_ (u"ࠨࡥ࡯࡭ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭Ტ")]))
            if bstack1l1l1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡌࡒࡆࡘ࡙ࡠࡗࡕࡐࠬᲣ") in os.environ:
                logger.debug(bstack1l1l1l1_opy_ (u"ࠥࡗࡰ࡯ࡰࡱ࡫ࡱ࡫ࠥࡨࡩ࡯ࡣࡵࡽࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠠࡢࡵࠣࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅࡍࡓࡇࡒ࡚ࡡࡘࡖࡑࠦࡩࡴࠢࡶࡩࡹࠨᲤ"))
                data[bstack1l1l1l1_opy_ (u"ࠫࡺࡸ࡬ࠨᲥ")] = os.environ[bstack1l1l1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇࡏࡎࡂࡔ࡜ࡣ࡚ࡘࡌࠨᲦ")]
            bstack11l11lll1l1_opy_ = bstack111lllll11l_opy_(data[bstack1l1l1l1_opy_ (u"࠭ࡵࡳ࡮ࠪᲧ")], bstack1lll1lll1l1_opy_)
            bstack11l1l1l11l1_opy_ = os.path.join(bstack1lll1lll1l1_opy_, bstack11l11lll1l1_opy_)
            os.chmod(bstack11l1l1l11l1_opy_, 0o777) # bstack11l1111ll1l_opy_ permission
            return bstack11l1l1l11l1_opy_
    except Exception as e:
        logger.debug(bstack1l1l1l1_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࡩ࡯ࡩࠣࡲࡪࡽࠠࡔࡆࡎࠤࢀࢃࠢᲨ").format(e))
    return binary_path
def bstack11l1111llll_opy_(bstack11l11111ll1_opy_):
    try:
        if bstack1l1l1l1_opy_ (u"ࠨ࡮࡬ࡲࡺࡾࠧᲩ") not in bstack11l11111ll1_opy_[bstack1l1l1l1_opy_ (u"ࠩࡲࡷࠬᲪ")].lower():
            return
        if os.path.exists(bstack1l1l1l1_opy_ (u"ࠥ࠳ࡪࡺࡣ࠰ࡱࡶ࠱ࡷ࡫࡬ࡦࡣࡶࡩࠧᲫ")):
            with open(bstack1l1l1l1_opy_ (u"ࠦ࠴࡫ࡴࡤ࠱ࡲࡷ࠲ࡸࡥ࡭ࡧࡤࡷࡪࠨᲬ"), bstack1l1l1l1_opy_ (u"ࠧࡸࠢᲭ")) as f:
                bstack111lllll111_opy_ = {}
                for line in f:
                    if bstack1l1l1l1_opy_ (u"ࠨ࠽ࠣᲮ") in line:
                        key, value = line.rstrip().split(bstack1l1l1l1_opy_ (u"ࠢ࠾ࠤᲯ"), 1)
                        bstack111lllll111_opy_[key] = value.strip(bstack1l1l1l1_opy_ (u"ࠨࠤ࡟ࠫࠬᲰ"))
                bstack11l11111ll1_opy_[bstack1l1l1l1_opy_ (u"ࠩࡧ࡭ࡸࡺࡲࡰࠩᲱ")] = bstack111lllll111_opy_.get(bstack1l1l1l1_opy_ (u"ࠥࡍࡉࠨᲲ"), bstack1l1l1l1_opy_ (u"ࠦࠧᲳ"))
        elif os.path.exists(bstack1l1l1l1_opy_ (u"ࠧ࠵ࡥࡵࡥ࠲ࡥࡱࡶࡩ࡯ࡧ࠰ࡶࡪࡲࡥࡢࡵࡨࠦᲴ")):
            bstack11l11111ll1_opy_[bstack1l1l1l1_opy_ (u"࠭ࡤࡪࡵࡷࡶࡴ࠭Ჵ")] = bstack1l1l1l1_opy_ (u"ࠧࡢ࡮ࡳ࡭ࡳ࡫ࠧᲶ")
    except Exception as e:
        logger.debug(bstack1l1l1l1_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡬࡫ࡴࠡࡦ࡬ࡷࡹࡸ࡯ࠡࡱࡩࠤࡱ࡯࡮ࡶࡺࠥᲷ") + e)
@measure(event_name=EVENTS.bstack11l1lll1ll1_opy_, stage=STAGE.bstack1l1lll1lll_opy_)
def bstack111lllll11l_opy_(bstack11l11lllll1_opy_, bstack11l1l11ll11_opy_):
    logger.debug(bstack1l1l1l1_opy_ (u"ࠤࡇࡳࡼࡴ࡬ࡰࡣࡧ࡭ࡳ࡭ࠠࡔࡆࡎࠤࡧ࡯࡮ࡢࡴࡼࠤ࡫ࡸ࡯࡮࠼ࠣࠦᲸ") + str(bstack11l11lllll1_opy_) + bstack1l1l1l1_opy_ (u"ࠥࠦᲹ"))
    zip_path = os.path.join(bstack11l1l11ll11_opy_, bstack1l1l1l1_opy_ (u"ࠦࡩࡵࡷ࡯࡮ࡲࡥࡩ࡫ࡤࡠࡨ࡬ࡰࡪ࠴ࡺࡪࡲࠥᲺ"))
    bstack11l11lll1l1_opy_ = bstack1l1l1l1_opy_ (u"ࠬ࠭᲻")
    with requests.get(bstack11l11lllll1_opy_, stream=True) as response:
        response.raise_for_status()
        with open(zip_path, bstack1l1l1l1_opy_ (u"ࠨࡷࡣࠤ᲼")) as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        logger.debug(bstack1l1l1l1_opy_ (u"ࠢࡇ࡫࡯ࡩࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࡥࡥࠢࡶࡹࡨࡩࡥࡴࡵࡩࡹࡱࡲࡹ࠯ࠤᲽ"))
    with zipfile.ZipFile(zip_path, bstack1l1l1l1_opy_ (u"ࠨࡴࠪᲾ")) as zip_ref:
        bstack11l1l11l111_opy_ = zip_ref.namelist()
        if len(bstack11l1l11l111_opy_) > 0:
            bstack11l11lll1l1_opy_ = bstack11l1l11l111_opy_[0] # bstack11l111l11l1_opy_ bstack11l1ll1l11l_opy_ will be bstack11l11ll111l_opy_ 1 file i.e. the binary in the zip
        zip_ref.extractall(bstack11l1l11ll11_opy_)
        logger.debug(bstack1l1l1l1_opy_ (u"ࠤࡉ࡭ࡱ࡫ࡳࠡࡵࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࡱࡿࠠࡦࡺࡷࡶࡦࡩࡴࡦࡦࠣࡸࡴࠦࠧࠣᲿ") + str(bstack11l1l11ll11_opy_) + bstack1l1l1l1_opy_ (u"ࠥࠫࠧ᳀"))
    os.remove(zip_path)
    return bstack11l11lll1l1_opy_
def get_cli_dir():
    bstack11l111l1lll_opy_ = bstack1l1l1llllll_opy_()
    if bstack11l111l1lll_opy_:
        bstack1lll1lll1l1_opy_ = os.path.join(bstack11l111l1lll_opy_, bstack1l1l1l1_opy_ (u"ࠦࡨࡲࡩࠣ᳁"))
        if not os.path.exists(bstack1lll1lll1l1_opy_):
            os.makedirs(bstack1lll1lll1l1_opy_, mode=0o777, exist_ok=True)
        return bstack1lll1lll1l1_opy_
    else:
        raise FileNotFoundError(bstack1l1l1l1_opy_ (u"ࠧࡔ࡯ࠡࡹࡵ࡭ࡹࡧࡢ࡭ࡧࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࠦࡡࡷࡣ࡬ࡰࡦࡨ࡬ࡦࠢࡩࡳࡷࠦࡴࡩࡧࠣࡗࡉࡑࠠࡣ࡫ࡱࡥࡷࡿ࠮ࠣ᳂"))
def bstack1llll1l1lll_opy_(bstack1lll1lll1l1_opy_):
    bstack1l1l1l1_opy_ (u"ࠨࠢࠣࡉࡨࡸࠥࡺࡨࡦࠢࡳࡥࡹ࡮ࠠࡧࡱࡵࠤࡹ࡮ࡥࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡔࡆࡎࠤࡧ࡯࡮ࡢࡴࡼࠤ࡮ࡴࠠࡢࠢࡺࡶ࡮ࡺࡡࡣ࡮ࡨࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿ࠮ࠣࠤࠥ᳃")
    bstack11l1l1111ll_opy_ = [
        os.path.join(bstack1lll1lll1l1_opy_, f)
        for f in os.listdir(bstack1lll1lll1l1_opy_)
        if os.path.isfile(os.path.join(bstack1lll1lll1l1_opy_, f)) and f.startswith(bstack1l1l1l1_opy_ (u"ࠢࡣ࡫ࡱࡥࡷࡿ࠭ࠣ᳄"))
    ]
    if len(bstack11l1l1111ll_opy_) > 0:
        return max(bstack11l1l1111ll_opy_, key=os.path.getmtime) # get bstack11l11ll1l11_opy_ binary
    return bstack1l1l1l1_opy_ (u"ࠣࠤ᳅")
def bstack11ll1lll1l1_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1ll11lll111_opy_(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = bstack1ll11lll111_opy_(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack111l111l_opy_(data, keys, default=None):
    bstack1l1l1l1_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࡖࡥ࡫࡫࡬ࡺࠢࡪࡩࡹࠦࡡࠡࡰࡨࡷࡹ࡫ࡤࠡࡸࡤࡰࡺ࡫ࠠࡧࡴࡲࡱࠥࡧࠠࡥ࡫ࡦࡸ࡮ࡵ࡮ࡢࡴࡼࠤࡴࡸࠠ࡭࡫ࡶࡸ࠳ࠐࠠࠡࠢࠣ࠾ࡵࡧࡲࡢ࡯ࠣࡨࡦࡺࡡ࠻ࠢࡗ࡬ࡪࠦࡤࡪࡥࡷ࡭ࡴࡴࡡࡳࡻࠣࡳࡷࠦ࡬ࡪࡵࡷࠤࡹࡵࠠࡵࡴࡤࡺࡪࡸࡳࡦ࠰ࠍࠤࠥࠦࠠ࠻ࡲࡤࡶࡦࡳࠠ࡬ࡧࡼࡷ࠿ࠦࡁࠡ࡮࡬ࡷࡹࠦ࡯ࡧࠢ࡮ࡩࡾࡹ࠯ࡪࡰࡧ࡭ࡨ࡫ࡳࠡࡴࡨࡴࡷ࡫ࡳࡦࡰࡷ࡭ࡳ࡭ࠠࡵࡪࡨࠤࡵࡧࡴࡩ࠰ࠍࠤࠥࠦࠠ࠻ࡲࡤࡶࡦࡳࠠࡥࡧࡩࡥࡺࡲࡴ࠻࡙ࠢࡥࡱࡻࡥࠡࡶࡲࠤࡷ࡫ࡴࡶࡴࡱࠤ࡮࡬ࠠࡵࡪࡨࠤࡵࡧࡴࡩࠢࡧࡳࡪࡹࠠ࡯ࡱࡷࠤࡪࡾࡩࡴࡶ࠱ࠎࠥࠦࠠࠡ࠼ࡵࡩࡹࡻࡲ࡯࠼ࠣࡘ࡭࡫ࠠࡷࡣ࡯ࡹࡪࠦࡡࡵࠢࡷ࡬ࡪࠦ࡮ࡦࡵࡷࡩࡩࠦࡰࡢࡶ࡫࠰ࠥࡵࡲࠡࡦࡨࡪࡦࡻ࡬ࡵࠢ࡬ࡪࠥࡴ࡯ࡵࠢࡩࡳࡺࡴࡤ࠯ࠌࠣࠤࠥࠦࠢࠣࠤ᳆")
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