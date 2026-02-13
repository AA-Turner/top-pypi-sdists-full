# coding: UTF-8
import sys
bstack111ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack11l11_opy_ (bstack1lll1ll_opy_):
    global bstack11l11l_opy_
    bstack11111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1l11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack11111l1_opy_ = bstack11111l_opy_ % len (bstack1l11_opy_)
    bstack1lll1l_opy_ = bstack1l11_opy_ [:bstack11111l1_opy_] + bstack1l11_opy_ [bstack11111l1_opy_:]
    if bstack111ll11_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    return eval (bstack1l1l1_opy_)
bstack11l11_opy_ (u"ࠨࠢࠣࠌࡓࡽࡹ࡫ࡳࡵࠢࡷࡩࡸࡺࠠࡤࡱ࡯ࡰࡪࡩࡴࡪࡱࡱࠤ࡭࡫࡬ࡱࡧࡵࠤࡺࡹࡩ࡯ࡩࠣࡨ࡮ࡸࡥࡤࡶࠣࡴࡾࡺࡥࡴࡶࠣ࡬ࡴࡵ࡫ࡴ࠰ࠍࠦࠧࠨᄈ")
import pytest
import io
import os
from contextlib import redirect_stdout, redirect_stderr
import subprocess
import sys
def bstack1llll1ll1l1_opy_(bstack1llll1llll1_opy_=None, bstack1llll1ll1ll_opy_=None):
    bstack11l11_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࡄࡱ࡯ࡰࡪࡩࡴࠡࡲࡼࡸࡪࡹࡴࠡࡶࡨࡷࡹࡹࠠࡶࡵ࡬ࡲ࡬ࠦࡰࡺࡶࡨࡷࡹ࠭ࡳࠡ࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠣࡅࡕࡏࡳ࠯ࠌࠣࠤࠥࠦࡁࡳࡩࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡴࡦࡵࡷࡣࡦࡸࡧࡴࠢࠫࡰ࡮ࡹࡴ࠭ࠢࡲࡴࡹ࡯࡯࡯ࡣ࡯࠭࠿ࠦࡃࡰ࡯ࡳࡰࡪࡺࡥࠡ࡮࡬ࡷࡹࠦ࡯ࡧࠢࡳࡽࡹ࡫ࡳࡵࠢࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠥ࡯࡮ࡤ࡮ࡸࡨ࡮ࡴࡧࠡࡲࡤࡸ࡭ࡹࠠࡢࡰࡧࠤ࡫ࡲࡡࡨࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࡙ࡧ࡫ࡦࡵࠣࡴࡷ࡫ࡣࡦࡦࡨࡲࡨ࡫ࠠࡰࡸࡨࡶࠥࡺࡥࡴࡶࡢࡴࡦࡺࡨࡴࠢ࡬ࡪࠥࡨ࡯ࡵࡪࠣࡥࡷ࡫ࠠࡱࡴࡲࡺ࡮ࡪࡥࡥ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡹ࡫ࡳࡵࡡࡳࡥࡹ࡮ࡳࠡࠪ࡯࡭ࡸࡺࠠࡰࡴࠣࡷࡹࡸࠬࠡࡱࡳࡸ࡮ࡵ࡮ࡢ࡮ࠬ࠾࡚ࠥࡥࡴࡶࠣࡪ࡮ࡲࡥࠩࡵࠬ࠳ࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠨࡪࡧࡶ࠭ࠥࡺ࡯ࠡࡥࡲࡰࡱ࡫ࡣࡵࠢࡩࡶࡴࡳ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡆࡥࡳࠦࡢࡦࠢࡤࠤࡸ࡯࡮ࡨ࡮ࡨࠤࡵࡧࡴࡩࠢࡶࡸࡷ࡯࡮ࡨࠢࡲࡶࠥࡲࡩࡴࡶࠣࡳ࡫ࠦࡰࡢࡶ࡫ࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡊࡩࡱࡳࡷ࡫ࡤࠡ࡫ࡩࠤࡹ࡫ࡳࡵࡡࡤࡶ࡬ࡹࠠࡪࡵࠣࡴࡷࡵࡶࡪࡦࡨࡨ࠳ࠐࠠࠡࠢࠣࡖࡪࡺࡵࡳࡰࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡤࡪࡥࡷ࠾ࠥࡉ࡯࡭࡮ࡨࡧࡹ࡯࡯࡯ࠢࡵࡩࡸࡻ࡬ࡵࡵࠣࡻ࡮ࡺࡨࠡ࡭ࡨࡽࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡴࡷࡦࡧࡪࡹࡳࠡࠪࡥࡳࡴࡲࠩࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡥࡲࡹࡳࡺࠠࠩ࡫ࡱࡸ࠮ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦ࡮ࡰࡦࡨ࡭ࡩࡹࠠࠩ࡮࡬ࡷࡹ࠯ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡵࡧࡶࡸࡤ࡬ࡩ࡭ࡧࡶࠤ࠭ࡲࡩࡴࡶࠬࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡪࡸࡲࡰࡴࠣࠬࡸࡺࡲࠪࠌࠣࠤࠥࠦࠢࠣࠤᄉ")
    try:
        bstack1llll1lll1l_opy_ = os.getenv(bstack11l11_opy_ (u"ࠣࡒ࡜ࡘࡊ࡙ࡔࡠࡅࡘࡖࡗࡋࡎࡕࡡࡗࡉࡘ࡚ࠢᄊ")) is not None
        if bstack1llll1llll1_opy_ is not None:
            args = list(bstack1llll1llll1_opy_)
        elif bstack1llll1ll1ll_opy_ is not None:
            if isinstance(bstack1llll1ll1ll_opy_, str):
                args = [bstack1llll1ll1ll_opy_]
            elif isinstance(bstack1llll1ll1ll_opy_, list):
                args = list(bstack1llll1ll1ll_opy_)
            else:
                args = [bstack11l11_opy_ (u"ࠤ࠱ࠦᄋ")]
        else:
            args = [bstack11l11_opy_ (u"ࠥ࠲ࠧᄌ")]
        if bstack1llll1lll1l_opy_:
            return _1llll1l1lll_opy_(args)
        bstack1llll1l11ll_opy_ = args + [
            bstack11l11_opy_ (u"ࠦ࠲࠳ࡣࡰ࡮࡯ࡩࡨࡺ࠭ࡰࡰ࡯ࡽࠧᄍ"),
            bstack11l11_opy_ (u"ࠧ࠳࠭ࡲࡷ࡬ࡩࡹࠨᄎ")
        ]
        class bstack1llll1lll11_opy_:
            bstack11l11_opy_ (u"ࠨࠢࠣࡒࡼࡸࡪࡹࡴࠡࡲ࡯ࡹ࡬࡯࡮ࠡࡶ࡫ࡥࡹࠦࡣࡢࡲࡷࡹࡷ࡫ࡳࠡࡥࡲࡰࡱ࡫ࡣࡵࡧࡧࠤࡹ࡫ࡳࡵࠢ࡬ࡸࡪࡳࡳ࠯ࠤࠥࠦᄏ")
            def __init__(self):
                self.bstack1llll1l1l11_opy_ = []
                self.test_files = set()
                self.bstack1llll1l1ll1_opy_ = None
            def pytest_collection_finish(self, session):
                bstack11l11_opy_ (u"ࠢࠣࠤࡋࡳࡴࡱࠠࡤࡣ࡯ࡰࡪࡪࠠࡢࡨࡷࡩࡷࠦࡣࡰ࡮࡯ࡩࡨࡺࡩࡰࡰࠣ࡭ࡸࠦࡦࡪࡰ࡬ࡷ࡭࡫ࡤ࠯ࠤࠥࠦᄐ")
                try:
                    for item in session.items:
                        nodeid = item.nodeid
                        self.bstack1llll1l1l11_opy_.append(nodeid)
                        if bstack11l11_opy_ (u"ࠣ࠼࠽ࠦᄑ") in nodeid:
                            file_path = nodeid.split(bstack11l11_opy_ (u"ࠤ࠽࠾ࠧᄒ"), 1)[0]
                            if file_path.endswith(bstack11l11_opy_ (u"ࠪ࠲ࡵࡿࠧᄓ")):
                                self.test_files.add(file_path)
                except Exception as e:
                    self.bstack1llll1l1ll1_opy_ = str(e)
        collector = bstack1llll1lll11_opy_()
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            exit_code = pytest.main(bstack1llll1l11ll_opy_, plugins=[collector])
        if collector.bstack1llll1l1ll1_opy_:
            return {bstack11l11_opy_ (u"ࠦࡸࡻࡣࡤࡧࡶࡷࠧᄔ"): False, bstack11l11_opy_ (u"ࠧࡩ࡯ࡶࡰࡷࠦᄕ"): 0, bstack11l11_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࡹࠢᄖ"): [], bstack11l11_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡩ࡭ࡧࡶࠦᄗ"): [], bstack11l11_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢᄘ"): bstack11l11_opy_ (u"ࠤࡆࡳࡱࡲࡥࡤࡶ࡬ࡳࡳࠦࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠤᄙ").format(collector.bstack1llll1l1ll1_opy_)}
        return {
            bstack11l11_opy_ (u"ࠥࡷࡺࡩࡣࡦࡵࡶࠦᄚ"): True,
            bstack11l11_opy_ (u"ࠦࡨࡵࡵ࡯ࡶࠥᄛ"): len(collector.bstack1llll1l1l11_opy_),
            bstack11l11_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࡸࠨᄜ"): collector.bstack1llll1l1l11_opy_,
            bstack11l11_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫࡯࡬ࡦࡵࠥᄝ"): sorted(collector.test_files),
            bstack11l11_opy_ (u"ࠢࡦࡺ࡬ࡸࡤࡩ࡯ࡥࡧࠥᄞ"): exit_code
        }
    except Exception as e:
        return {bstack11l11_opy_ (u"ࠣࡵࡸࡧࡨ࡫ࡳࡴࠤᄟ"): False, bstack11l11_opy_ (u"ࠤࡦࡳࡺࡴࡴࠣᄠ"): 0, bstack11l11_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࡶࠦᄡ"): [], bstack11l11_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩ࡭ࡱ࡫ࡳࠣᄢ"): [], bstack11l11_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦᄣ"): bstack11l11_opy_ (u"ࠨࡕ࡯ࡧࡻࡴࡪࡩࡴࡦࡦࠣࡩࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡺࡥࡴࡶࠣࡧࡴࡲ࡬ࡦࡥࡷ࡭ࡴࡴ࠺ࠡࡽࢀࠦᄤ").format(e)}
def _1llll1l1lll_opy_(args):
    bstack11l11_opy_ (u"ࠢࠣࠤࡌࡷࡴࡲࡡࡵࡧࡧࠤࡨࡵ࡬࡭ࡧࡦࡸ࡮ࡵ࡮ࠡࡧࡻࡩࡨࡻࡴࡦࡦࠣ࡭ࡳࠦࡡࠡࡵࡨࡴࡦࡸࡡࡵࡧࠣࡔࡾࡺࡨࡰࡰࠣࡴࡷࡵࡣࡦࡵࡶࠤࡹࡵࠠࡢࡸࡲ࡭ࡩࠦ࡮ࡦࡵࡷࡩࡩࠦࡰࡺࡶࡨࡷࡹࠦࡩࡴࡵࡸࡩࡸ࠴ࠢࠣࠤᄥ")
    bstack1llll1ll11l_opy_ = [sys.executable, bstack11l11_opy_ (u"ࠣ࠯ࡰࠦᄦ"), bstack11l11_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵࠤᄧ"), bstack11l11_opy_ (u"ࠥ࠱࠲ࡩ࡯࡭࡮ࡨࡧࡹ࠳࡯࡯࡮ࡼࠦᄨ"), bstack11l11_opy_ (u"ࠦ࠲࠳ࡱࡶ࡫ࡨࡸࠧᄩ")]
    bstack1llll1l1l1l_opy_ = [a for a in args if a not in (bstack11l11_opy_ (u"ࠧ࠳࠭ࡤࡱ࡯ࡰࡪࡩࡴ࠮ࡱࡱࡰࡾࠨᄪ"), bstack11l11_opy_ (u"ࠨ࠭࠮ࡳࡸ࡭ࡪࡺࠢᄫ"), bstack11l11_opy_ (u"ࠢ࠮ࡳࠥᄬ"))]
    cmd = bstack1llll1ll11l_opy_ + bstack1llll1l1l1l_opy_
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, env=os.environ.copy())
        stdout = proc.stdout.splitlines()
        bstack1llll1l1l11_opy_ = []
        test_files = set()
        for line in stdout:
            line = line.strip()
            if not line or bstack11l11_opy_ (u"ࠣࠢࡦࡳࡱࡲࡥࡤࡶࡨࡨࠧᄭ") in line.lower():
                continue
            if bstack11l11_opy_ (u"ࠤ࠽࠾ࠧᄮ") in line:
                bstack1llll1l1l11_opy_.append(line)
                file_path = line.split(bstack11l11_opy_ (u"ࠥ࠾࠿ࠨᄯ"), 1)[0]
                if file_path.endswith(bstack11l11_opy_ (u"ࠫ࠳ࡶࡹࠨᄰ")):
                    test_files.add(file_path)
        success = proc.returncode in (0, 5)
        return {
            bstack11l11_opy_ (u"ࠧࡹࡵࡤࡥࡨࡷࡸࠨᄱ"): success,
            bstack11l11_opy_ (u"ࠨࡣࡰࡷࡱࡸࠧᄲ"): len(bstack1llll1l1l11_opy_),
            bstack11l11_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࡳࠣᄳ"): bstack1llll1l1l11_opy_,
            bstack11l11_opy_ (u"ࠣࡶࡨࡷࡹࡥࡦࡪ࡮ࡨࡷࠧᄴ"): sorted(test_files),
            bstack11l11_opy_ (u"ࠤࡨࡼ࡮ࡺ࡟ࡤࡱࡧࡩࠧᄵ"): proc.returncode,
            bstack11l11_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤᄶ"): None if success else bstack11l11_opy_ (u"ࠦࡘࡻࡢࡱࡴࡲࡧࡪࡹࡳࠡࡥࡲࡰࡱ࡫ࡣࡵ࡫ࡲࡲࠥ࡬ࡡࡪ࡮ࡨࡨࠥ࠮ࡥࡹ࡫ࡷࠤࢀࢃࠩࠣᄷ").format(proc.returncode)
        }
    except Exception as e:
        return {bstack11l11_opy_ (u"ࠧࡹࡵࡤࡥࡨࡷࡸࠨᄸ"): False, bstack11l11_opy_ (u"ࠨࡣࡰࡷࡱࡸࠧᄹ"): 0, bstack11l11_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࡳࠣᄺ"): [], bstack11l11_opy_ (u"ࠣࡶࡨࡷࡹࡥࡦࡪ࡮ࡨࡷࠧᄻ"): [], bstack11l11_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣᄼ"): bstack11l11_opy_ (u"ࠥࡗࡺࡨࡰࡳࡱࡦࡩࡸࡹࠠࡤࡱ࡯ࡰࡪࡩࡴࡪࡱࡱࠤࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠢᄽ").format(e)}