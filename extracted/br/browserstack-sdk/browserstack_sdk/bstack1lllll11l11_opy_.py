# coding: UTF-8
import sys
bstack1lllll_opy_ = sys.version_info [0] == 2
bstack1l1ll1_opy_ = 2048
bstack1lllll1l_opy_ = 7
def bstack1111_opy_ (bstack1l11ll1_opy_):
    global bstack1l_opy_
    bstack11lll1l_opy_ = ord (bstack1l11ll1_opy_ [-1])
    bstack1llll1_opy_ = bstack1l11ll1_opy_ [:-1]
    bstack111ll11_opy_ = bstack11lll1l_opy_ % len (bstack1llll1_opy_)
    bstack1111l_opy_ = bstack1llll1_opy_ [:bstack111ll11_opy_] + bstack1llll1_opy_ [bstack111ll11_opy_:]
    if bstack1lllll_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    return eval (bstack1llll11_opy_)
bstack1111_opy_ (u"ࠨࠢࠣࠌࡓࡽࡹ࡫ࡳࡵࠢࡷࡩࡸࡺࠠࡤࡱ࡯ࡰࡪࡩࡴࡪࡱࡱࠤ࡭࡫࡬ࡱࡧࡵࠤࡺࡹࡩ࡯ࡩࠣࡨ࡮ࡸࡥࡤࡶࠣࡴࡾࡺࡥࡴࡶࠣ࡬ࡴࡵ࡫ࡴ࠰ࠍࠦࠧࠨᄖ")
import pytest
import io
import os
from contextlib import redirect_stdout, redirect_stderr
import subprocess
import sys
def bstack1llll1ll1l1_opy_(bstack1llll1ll1ll_opy_=None, bstack1lllll11111_opy_=None):
    bstack1111_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࡄࡱ࡯ࡰࡪࡩࡴࠡࡲࡼࡸࡪࡹࡴࠡࡶࡨࡷࡹࡹࠠࡶࡵ࡬ࡲ࡬ࠦࡰࡺࡶࡨࡷࡹ࠭ࡳࠡ࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠣࡅࡕࡏࡳ࠯ࠌࠣࠤࠥࠦࡁࡳࡩࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡴࡦࡵࡷࡣࡦࡸࡧࡴࠢࠫࡰ࡮ࡹࡴ࠭ࠢࡲࡴࡹ࡯࡯࡯ࡣ࡯࠭࠿ࠦࡃࡰ࡯ࡳࡰࡪࡺࡥࠡ࡮࡬ࡷࡹࠦ࡯ࡧࠢࡳࡽࡹ࡫ࡳࡵࠢࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠥ࡯࡮ࡤ࡮ࡸࡨ࡮ࡴࡧࠡࡲࡤࡸ࡭ࡹࠠࡢࡰࡧࠤ࡫ࡲࡡࡨࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࡙ࡧ࡫ࡦࡵࠣࡴࡷ࡫ࡣࡦࡦࡨࡲࡨ࡫ࠠࡰࡸࡨࡶࠥࡺࡥࡴࡶࡢࡴࡦࡺࡨࡴࠢ࡬ࡪࠥࡨ࡯ࡵࡪࠣࡥࡷ࡫ࠠࡱࡴࡲࡺ࡮ࡪࡥࡥ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡹ࡫ࡳࡵࡡࡳࡥࡹ࡮ࡳࠡࠪ࡯࡭ࡸࡺࠠࡰࡴࠣࡷࡹࡸࠬࠡࡱࡳࡸ࡮ࡵ࡮ࡢ࡮ࠬ࠾࡚ࠥࡥࡴࡶࠣࡪ࡮ࡲࡥࠩࡵࠬ࠳ࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠨࡪࡧࡶ࠭ࠥࡺ࡯ࠡࡥࡲࡰࡱ࡫ࡣࡵࠢࡩࡶࡴࡳ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡆࡥࡳࠦࡢࡦࠢࡤࠤࡸ࡯࡮ࡨ࡮ࡨࠤࡵࡧࡴࡩࠢࡶࡸࡷ࡯࡮ࡨࠢࡲࡶࠥࡲࡩࡴࡶࠣࡳ࡫ࠦࡰࡢࡶ࡫ࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡊࡩࡱࡳࡷ࡫ࡤࠡ࡫ࡩࠤࡹ࡫ࡳࡵࡡࡤࡶ࡬ࡹࠠࡪࡵࠣࡴࡷࡵࡶࡪࡦࡨࡨ࠳ࠐࠠࠡࠢࠣࡖࡪࡺࡵࡳࡰࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡤࡪࡥࡷ࠾ࠥࡉ࡯࡭࡮ࡨࡧࡹ࡯࡯࡯ࠢࡵࡩࡸࡻ࡬ࡵࡵࠣࡻ࡮ࡺࡨࠡ࡭ࡨࡽࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡴࡷࡦࡧࡪࡹࡳࠡࠪࡥࡳࡴࡲࠩࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡥࡲࡹࡳࡺࠠࠩ࡫ࡱࡸ࠮ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦ࡮ࡰࡦࡨ࡭ࡩࡹࠠࠩ࡮࡬ࡷࡹ࠯ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡵࡧࡶࡸࡤ࡬ࡩ࡭ࡧࡶࠤ࠭ࡲࡩࡴࡶࠬࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡪࡸࡲࡰࡴࠣࠬࡸࡺࡲࠪࠌࠣࠤࠥࠦࠢࠣࠤᄗ")
    try:
        bstack1llll1ll11l_opy_ = os.getenv(bstack1111_opy_ (u"ࠣࡒ࡜ࡘࡊ࡙ࡔࡠࡅࡘࡖࡗࡋࡎࡕࡡࡗࡉࡘ࡚ࠢᄘ")) is not None
        if bstack1llll1ll1ll_opy_ is not None:
            args = list(bstack1llll1ll1ll_opy_)
        elif bstack1lllll11111_opy_ is not None:
            if isinstance(bstack1lllll11111_opy_, str):
                args = [bstack1lllll11111_opy_]
            elif isinstance(bstack1lllll11111_opy_, list):
                args = list(bstack1lllll11111_opy_)
            else:
                args = [bstack1111_opy_ (u"ࠤ࠱ࠦᄙ")]
        else:
            args = [bstack1111_opy_ (u"ࠥ࠲ࠧᄚ")]
        if bstack1llll1ll11l_opy_:
            return _1lllll111ll_opy_(args)
        bstack1llll1lll1l_opy_ = args + [
            bstack1111_opy_ (u"ࠦ࠲࠳ࡣࡰ࡮࡯ࡩࡨࡺ࠭ࡰࡰ࡯ࡽࠧᄛ"),
            bstack1111_opy_ (u"ࠧ࠳࠭ࡲࡷ࡬ࡩࡹࠨᄜ")
        ]
        class bstack1llll1llll1_opy_:
            bstack1111_opy_ (u"ࠨࠢࠣࡒࡼࡸࡪࡹࡴࠡࡲ࡯ࡹ࡬࡯࡮ࠡࡶ࡫ࡥࡹࠦࡣࡢࡲࡷࡹࡷ࡫ࡳࠡࡥࡲࡰࡱ࡫ࡣࡵࡧࡧࠤࡹ࡫ࡳࡵࠢ࡬ࡸࡪࡳࡳ࠯ࠤࠥࠦᄝ")
            def __init__(self):
                self.bstack1llll1lll11_opy_ = []
                self.test_files = set()
                self.bstack1lllll1111l_opy_ = None
            def pytest_collection_finish(self, session):
                bstack1111_opy_ (u"ࠢࠣࠤࡋࡳࡴࡱࠠࡤࡣ࡯ࡰࡪࡪࠠࡢࡨࡷࡩࡷࠦࡣࡰ࡮࡯ࡩࡨࡺࡩࡰࡰࠣ࡭ࡸࠦࡦࡪࡰ࡬ࡷ࡭࡫ࡤ࠯ࠤࠥࠦᄞ")
                try:
                    for item in session.items:
                        nodeid = item.nodeid
                        self.bstack1llll1lll11_opy_.append(nodeid)
                        if bstack1111_opy_ (u"ࠣ࠼࠽ࠦᄟ") in nodeid:
                            file_path = nodeid.split(bstack1111_opy_ (u"ࠤ࠽࠾ࠧᄠ"), 1)[0]
                            if file_path.endswith(bstack1111_opy_ (u"ࠪ࠲ࡵࡿࠧᄡ")):
                                self.test_files.add(file_path)
                except Exception as e:
                    self.bstack1lllll1111l_opy_ = str(e)
        collector = bstack1llll1llll1_opy_()
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            exit_code = pytest.main(bstack1llll1lll1l_opy_, plugins=[collector])
        if collector.bstack1lllll1111l_opy_:
            return {bstack1111_opy_ (u"ࠦࡸࡻࡣࡤࡧࡶࡷࠧᄢ"): False, bstack1111_opy_ (u"ࠧࡩ࡯ࡶࡰࡷࠦᄣ"): 0, bstack1111_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࡹࠢᄤ"): [], bstack1111_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡩ࡭ࡧࡶࠦᄥ"): [], bstack1111_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢᄦ"): bstack1111_opy_ (u"ࠤࡆࡳࡱࡲࡥࡤࡶ࡬ࡳࡳࠦࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠤᄧ").format(collector.bstack1lllll1111l_opy_)}
        return {
            bstack1111_opy_ (u"ࠥࡷࡺࡩࡣࡦࡵࡶࠦᄨ"): True,
            bstack1111_opy_ (u"ࠦࡨࡵࡵ࡯ࡶࠥᄩ"): len(collector.bstack1llll1lll11_opy_),
            bstack1111_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࡸࠨᄪ"): collector.bstack1llll1lll11_opy_,
            bstack1111_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫࡯࡬ࡦࡵࠥᄫ"): sorted(collector.test_files),
            bstack1111_opy_ (u"ࠢࡦࡺ࡬ࡸࡤࡩ࡯ࡥࡧࠥᄬ"): exit_code
        }
    except Exception as e:
        return {bstack1111_opy_ (u"ࠣࡵࡸࡧࡨ࡫ࡳࡴࠤᄭ"): False, bstack1111_opy_ (u"ࠤࡦࡳࡺࡴࡴࠣᄮ"): 0, bstack1111_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࡶࠦᄯ"): [], bstack1111_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩ࡭ࡱ࡫ࡳࠣᄰ"): [], bstack1111_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦᄱ"): bstack1111_opy_ (u"ࠨࡕ࡯ࡧࡻࡴࡪࡩࡴࡦࡦࠣࡩࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡺࡥࡴࡶࠣࡧࡴࡲ࡬ࡦࡥࡷ࡭ࡴࡴ࠺ࠡࡽࢀࠦᄲ").format(e)}
def _1lllll111ll_opy_(args):
    bstack1111_opy_ (u"ࠢࠣࠤࡌࡷࡴࡲࡡࡵࡧࡧࠤࡨࡵ࡬࡭ࡧࡦࡸ࡮ࡵ࡮ࠡࡧࡻࡩࡨࡻࡴࡦࡦࠣ࡭ࡳࠦࡡࠡࡵࡨࡴࡦࡸࡡࡵࡧࠣࡔࡾࡺࡨࡰࡰࠣࡴࡷࡵࡣࡦࡵࡶࠤࡹࡵࠠࡢࡸࡲ࡭ࡩࠦ࡮ࡦࡵࡷࡩࡩࠦࡰࡺࡶࡨࡷࡹࠦࡩࡴࡵࡸࡩࡸ࠴ࠢࠣࠤᄳ")
    bstack1llll1lllll_opy_ = [sys.executable, bstack1111_opy_ (u"ࠣ࠯ࡰࠦᄴ"), bstack1111_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵࠤᄵ"), bstack1111_opy_ (u"ࠥ࠱࠲ࡩ࡯࡭࡮ࡨࡧࡹ࠳࡯࡯࡮ࡼࠦᄶ"), bstack1111_opy_ (u"ࠦ࠲࠳ࡱࡶ࡫ࡨࡸࠧᄷ")]
    bstack1lllll111l1_opy_ = [a for a in args if a not in (bstack1111_opy_ (u"ࠧ࠳࠭ࡤࡱ࡯ࡰࡪࡩࡴ࠮ࡱࡱࡰࡾࠨᄸ"), bstack1111_opy_ (u"ࠨ࠭࠮ࡳࡸ࡭ࡪࡺࠢᄹ"), bstack1111_opy_ (u"ࠢ࠮ࡳࠥᄺ"))]
    cmd = bstack1llll1lllll_opy_ + bstack1lllll111l1_opy_
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, env=os.environ.copy())
        stdout = proc.stdout.splitlines()
        bstack1llll1lll11_opy_ = []
        test_files = set()
        for line in stdout:
            line = line.strip()
            if not line or bstack1111_opy_ (u"ࠣࠢࡦࡳࡱࡲࡥࡤࡶࡨࡨࠧᄻ") in line.lower():
                continue
            if bstack1111_opy_ (u"ࠤ࠽࠾ࠧᄼ") in line:
                bstack1llll1lll11_opy_.append(line)
                file_path = line.split(bstack1111_opy_ (u"ࠥ࠾࠿ࠨᄽ"), 1)[0]
                if file_path.endswith(bstack1111_opy_ (u"ࠫ࠳ࡶࡹࠨᄾ")):
                    test_files.add(file_path)
        success = proc.returncode in (0, 5)
        return {
            bstack1111_opy_ (u"ࠧࡹࡵࡤࡥࡨࡷࡸࠨᄿ"): success,
            bstack1111_opy_ (u"ࠨࡣࡰࡷࡱࡸࠧᅀ"): len(bstack1llll1lll11_opy_),
            bstack1111_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࡳࠣᅁ"): bstack1llll1lll11_opy_,
            bstack1111_opy_ (u"ࠣࡶࡨࡷࡹࡥࡦࡪ࡮ࡨࡷࠧᅂ"): sorted(test_files),
            bstack1111_opy_ (u"ࠤࡨࡼ࡮ࡺ࡟ࡤࡱࡧࡩࠧᅃ"): proc.returncode,
            bstack1111_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤᅄ"): None if success else bstack1111_opy_ (u"ࠦࡘࡻࡢࡱࡴࡲࡧࡪࡹࡳࠡࡥࡲࡰࡱ࡫ࡣࡵ࡫ࡲࡲࠥ࡬ࡡࡪ࡮ࡨࡨࠥ࠮ࡥࡹ࡫ࡷࠤࢀࢃࠩࠣᅅ").format(proc.returncode)
        }
    except Exception as e:
        return {bstack1111_opy_ (u"ࠧࡹࡵࡤࡥࡨࡷࡸࠨᅆ"): False, bstack1111_opy_ (u"ࠨࡣࡰࡷࡱࡸࠧᅇ"): 0, bstack1111_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࡳࠣᅈ"): [], bstack1111_opy_ (u"ࠣࡶࡨࡷࡹࡥࡦࡪ࡮ࡨࡷࠧᅉ"): [], bstack1111_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣᅊ"): bstack1111_opy_ (u"ࠥࡗࡺࡨࡰࡳࡱࡦࡩࡸࡹࠠࡤࡱ࡯ࡰࡪࡩࡴࡪࡱࡱࠤࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠢᅋ").format(e)}