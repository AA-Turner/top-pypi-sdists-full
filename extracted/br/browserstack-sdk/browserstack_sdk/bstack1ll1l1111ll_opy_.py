# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack111ll11_opy_ (bstack1111l1_opy_):
    global bstack1llll11_opy_
    bstack1ll11l1_opy_ = ord (bstack1111l1_opy_ [-1])
    bstack11ll_opy_ = bstack1111l1_opy_ [:-1]
    bstack1llll1_opy_ = bstack1ll11l1_opy_ % len (bstack11ll_opy_)
    bstack1ll1_opy_ = bstack11ll_opy_ [:bstack1llll1_opy_] + bstack11ll_opy_ [bstack1llll1_opy_:]
    if bstack11llll_opy_:
        bstack1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1l1_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1l1_opy_)
bstack111ll11_opy_ (u"ࠦࠧࠨࠊࡑࡻࡷࡩࡸࡺࠠࡵࡧࡶࡸࠥࡩ࡯࡭࡮ࡨࡧࡹ࡯࡯࡯ࠢ࡫ࡩࡱࡶࡥࡳࠢࡸࡷ࡮ࡴࡧࠡࡦ࡬ࡶࡪࡩࡴࠡࡲࡼࡸࡪࡹࡴࠡࡪࡲࡳࡰࡹ࠮ࠋࠤࠥࠦጶ")
import pytest
import io
import os
from contextlib import redirect_stdout, redirect_stderr
import subprocess
import sys
def bstack1ll11lllll1_opy_(bstack1ll11llllll_opy_=None, bstack1ll11lll1ll_opy_=None):
    bstack111ll11_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࡉ࡯࡭࡮ࡨࡧࡹࠦࡰࡺࡶࡨࡷࡹࠦࡴࡦࡵࡷࡷࠥࡻࡳࡪࡰࡪࠤࡵࡿࡴࡦࡵࡷࠫࡸࠦࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠡࡃࡓࡍࡸ࠴ࠊࠡࠢࠣࠤࡆࡸࡧࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡹ࡫ࡳࡵࡡࡤࡶ࡬ࡹࠠࠩ࡮࡬ࡷࡹ࠲ࠠࡰࡲࡷ࡭ࡴࡴࡡ࡭ࠫ࠽ࠤࡈࡵ࡭ࡱ࡮ࡨࡸࡪࠦ࡬ࡪࡵࡷࠤࡴ࡬ࠠࡱࡻࡷࡩࡸࡺࠠࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠣ࡭ࡳࡩ࡬ࡶࡦ࡬ࡲ࡬ࠦࡰࡢࡶ࡫ࡷࠥࡧ࡮ࡥࠢࡩࡰࡦ࡭ࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡗࡥࡰ࡫ࡳࠡࡲࡵࡩࡨ࡫ࡤࡦࡰࡦࡩࠥࡵࡶࡦࡴࠣࡸࡪࡹࡴࡠࡲࡤࡸ࡭ࡹࠠࡪࡨࠣࡦࡴࡺࡨࠡࡣࡵࡩࠥࡶࡲࡰࡸ࡬ࡨࡪࡪ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡷࡩࡸࡺ࡟ࡱࡣࡷ࡬ࡸࠦࠨ࡭࡫ࡶࡸࠥࡵࡲࠡࡵࡷࡶ࠱ࠦ࡯ࡱࡶ࡬ࡳࡳࡧ࡬ࠪ࠼ࠣࡘࡪࡹࡴࠡࡨ࡬ࡰࡪ࠮ࡳࠪ࠱ࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽ࠭࡯ࡥࡴࠫࠣࡸࡴࠦࡣࡰ࡮࡯ࡩࡨࡺࠠࡧࡴࡲࡱ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡄࡣࡱࠤࡧ࡫ࠠࡢࠢࡶ࡭ࡳ࡭࡬ࡦࠢࡳࡥࡹ࡮ࠠࡴࡶࡵ࡭ࡳ࡭ࠠࡰࡴࠣࡰ࡮ࡹࡴࠡࡱࡩࠤࡵࡧࡴࡩࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡏࡧ࡯ࡱࡵࡩࡩࠦࡩࡧࠢࡷࡩࡸࡺ࡟ࡢࡴࡪࡷࠥ࡯ࡳࠡࡲࡵࡳࡻ࡯ࡤࡦࡦ࠱ࠎࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡩ࡯ࡣࡵ࠼ࠣࡇࡴࡲ࡬ࡦࡥࡷ࡭ࡴࡴࠠࡳࡧࡶࡹࡱࡺࡳࠡࡹ࡬ࡸ࡭ࠦ࡫ࡦࡻࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡹࡵࡤࡥࡨࡷࡸࠦࠨࡣࡱࡲࡰ࠮ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡣࡰࡷࡱࡸࠥ࠮ࡩ࡯ࡶࠬࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡳࡵࡤࡦ࡫ࡧࡷࠥ࠮࡬ࡪࡵࡷ࠭ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡺࡥࡴࡶࡢࡪ࡮ࡲࡥࡴࠢࠫࡰ࡮ࡹࡴࠪࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡨࡶࡷࡵࡲࠡࠪࡶࡸࡷ࠯ࠊࠡࠢࠣࠤࠧࠨࠢጷ")
    try:
        bstack1ll11llll1l_opy_ = os.getenv(bstack111ll11_opy_ (u"ࠨࡐ࡚ࡖࡈࡗ࡙ࡥࡃࡖࡔࡕࡉࡓ࡚࡟ࡕࡇࡖࡘࠧጸ")) is not None
        if bstack1ll11llllll_opy_ is not None:
            args = list(bstack1ll11llllll_opy_)
        elif bstack1ll11lll1ll_opy_ is not None:
            if isinstance(bstack1ll11lll1ll_opy_, str):
                args = [bstack1ll11lll1ll_opy_]
            elif isinstance(bstack1ll11lll1ll_opy_, list):
                args = list(bstack1ll11lll1ll_opy_)
            else:
                args = [bstack111ll11_opy_ (u"ࠢ࠯ࠤጹ")]
        else:
            args = [bstack111ll11_opy_ (u"ࠣ࠰ࠥጺ")]
        if bstack1ll11llll1l_opy_:
            return _1ll1l111l11_opy_(args)
        bstack1ll11llll11_opy_ = args + [
            bstack111ll11_opy_ (u"ࠤ࠰࠱ࡨࡵ࡬࡭ࡧࡦࡸ࠲ࡵ࡮࡭ࡻࠥጻ"),
            bstack111ll11_opy_ (u"ࠥ࠱࠲ࡷࡵࡪࡧࡷࠦጼ")
        ]
        class bstack1ll11lll1l1_opy_:
            bstack111ll11_opy_ (u"ࠦࠧࠨࡐࡺࡶࡨࡷࡹࠦࡰ࡭ࡷࡪ࡭ࡳࠦࡴࡩࡣࡷࠤࡨࡧࡰࡵࡷࡵࡩࡸࠦࡣࡰ࡮࡯ࡩࡨࡺࡥࡥࠢࡷࡩࡸࡺࠠࡪࡶࡨࡱࡸ࠴ࠢࠣࠤጽ")
            def __init__(self):
                self.bstack1ll1l1111l1_opy_ = []
                self.test_files = set()
                self.bstack1ll1l111111_opy_ = None
            def pytest_collection_finish(self, session):
                bstack111ll11_opy_ (u"ࠧࠨࠢࡉࡱࡲ࡯ࠥࡩࡡ࡭࡮ࡨࡨࠥࡧࡦࡵࡧࡵࠤࡨࡵ࡬࡭ࡧࡦࡸ࡮ࡵ࡮ࠡ࡫ࡶࠤ࡫࡯࡮ࡪࡵ࡫ࡩࡩ࠴ࠢࠣࠤጾ")
                try:
                    for item in session.items:
                        nodeid = item.nodeid
                        self.bstack1ll1l1111l1_opy_.append(nodeid)
                        if bstack111ll11_opy_ (u"ࠨ࠺࠻ࠤጿ") in nodeid:
                            file_path = nodeid.split(bstack111ll11_opy_ (u"ࠢ࠻࠼ࠥፀ"), 1)[0]
                            if file_path.endswith(bstack111ll11_opy_ (u"ࠨ࠰ࡳࡽࠬፁ")):
                                self.test_files.add(file_path)
                except Exception as e:
                    self.bstack1ll1l111111_opy_ = str(e)
        collector = bstack1ll11lll1l1_opy_()
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            exit_code = pytest.main(bstack1ll11llll11_opy_, plugins=[collector])
        if collector.bstack1ll1l111111_opy_:
            return {bstack111ll11_opy_ (u"ࠤࡶࡹࡨࡩࡥࡴࡵࠥፂ"): False, bstack111ll11_opy_ (u"ࠥࡧࡴࡻ࡮ࡵࠤፃ"): 0, bstack111ll11_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࡷࠧፄ"): [], bstack111ll11_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪ࡮ࡲࡥࡴࠤፅ"): [], bstack111ll11_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧፆ"): bstack111ll11_opy_ (u"ࠢࡄࡱ࡯ࡰࡪࡩࡴࡪࡱࡱࠤࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠢፇ").format(collector.bstack1ll1l111111_opy_)}
        return {
            bstack111ll11_opy_ (u"ࠣࡵࡸࡧࡨ࡫ࡳࡴࠤፈ"): True,
            bstack111ll11_opy_ (u"ࠤࡦࡳࡺࡴࡴࠣፉ"): len(collector.bstack1ll1l1111l1_opy_),
            bstack111ll11_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࡶࠦፊ"): collector.bstack1ll1l1111l1_opy_,
            bstack111ll11_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩ࡭ࡱ࡫ࡳࠣፋ"): sorted(collector.test_files),
            bstack111ll11_opy_ (u"ࠧ࡫ࡸࡪࡶࡢࡧࡴࡪࡥࠣፌ"): exit_code
        }
    except Exception as e:
        return {bstack111ll11_opy_ (u"ࠨࡳࡶࡥࡦࡩࡸࡹࠢፍ"): False, bstack111ll11_opy_ (u"ࠢࡤࡱࡸࡲࡹࠨፎ"): 0, bstack111ll11_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࡴࠤፏ"): [], bstack111ll11_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧ࡫࡯ࡩࡸࠨፐ"): [], bstack111ll11_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤፑ"): bstack111ll11_opy_ (u"࡚ࠦࡴࡥࡹࡲࡨࡧࡹ࡫ࡤࠡࡧࡵࡶࡴࡸࠠࡪࡰࠣࡸࡪࡹࡴࠡࡥࡲࡰࡱ࡫ࡣࡵ࡫ࡲࡲ࠿ࠦࡻࡾࠤፒ").format(e)}
def _1ll1l111l11_opy_(args):
    bstack111ll11_opy_ (u"ࠧࠨࠢࡊࡵࡲࡰࡦࡺࡥࡥࠢࡦࡳࡱࡲࡥࡤࡶ࡬ࡳࡳࠦࡥࡹࡧࡦࡹࡹ࡫ࡤࠡ࡫ࡱࠤࡦࠦࡳࡦࡲࡤࡶࡦࡺࡥࠡࡒࡼࡸ࡭ࡵ࡮ࠡࡲࡵࡳࡨ࡫ࡳࡴࠢࡷࡳࠥࡧࡶࡰ࡫ࡧࠤࡳ࡫ࡳࡵࡧࡧࠤࡵࡿࡴࡦࡵࡷࠤ࡮ࡹࡳࡶࡧࡶ࠲ࠧࠨࠢፓ")
    bstack1ll1l11111l_opy_ = [sys.executable, bstack111ll11_opy_ (u"ࠨ࠭࡮ࠤፔ"), bstack111ll11_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺࠢፕ"), bstack111ll11_opy_ (u"ࠣ࠯࠰ࡧࡴࡲ࡬ࡦࡥࡷ࠱ࡴࡴ࡬ࡺࠤፖ"), bstack111ll11_opy_ (u"ࠤ࠰࠱ࡶࡻࡩࡦࡶࠥፗ")]
    bstack1ll11lll11l_opy_ = [a for a in args if a not in (bstack111ll11_opy_ (u"ࠥ࠱࠲ࡩ࡯࡭࡮ࡨࡧࡹ࠳࡯࡯࡮ࡼࠦፘ"), bstack111ll11_opy_ (u"ࠦ࠲࠳ࡱࡶ࡫ࡨࡸࠧፙ"), bstack111ll11_opy_ (u"ࠧ࠳ࡱࠣፚ"))]
    cmd = bstack1ll1l11111l_opy_ + bstack1ll11lll11l_opy_
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, env=os.environ.copy())
        stdout = proc.stdout.splitlines()
        bstack1ll1l1111l1_opy_ = []
        test_files = set()
        for line in stdout:
            line = line.strip()
            if not line or bstack111ll11_opy_ (u"ࠨࠠࡤࡱ࡯ࡰࡪࡩࡴࡦࡦࠥ፛") in line.lower():
                continue
            if bstack111ll11_opy_ (u"ࠢ࠻࠼ࠥ፜") in line:
                bstack1ll1l1111l1_opy_.append(line)
                file_path = line.split(bstack111ll11_opy_ (u"ࠣ࠼࠽ࠦ፝"), 1)[0]
                if file_path.endswith(bstack111ll11_opy_ (u"ࠩ࠱ࡴࡾ࠭፞")):
                    test_files.add(file_path)
        success = proc.returncode in (0, 5)
        return {
            bstack111ll11_opy_ (u"ࠥࡷࡺࡩࡣࡦࡵࡶࠦ፟"): success,
            bstack111ll11_opy_ (u"ࠦࡨࡵࡵ࡯ࡶࠥ፠"): len(bstack1ll1l1111l1_opy_),
            bstack111ll11_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࡸࠨ፡"): bstack1ll1l1111l1_opy_,
            bstack111ll11_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫࡯࡬ࡦࡵࠥ።"): sorted(test_files),
            bstack111ll11_opy_ (u"ࠢࡦࡺ࡬ࡸࡤࡩ࡯ࡥࡧࠥ፣"): proc.returncode,
            bstack111ll11_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢ፤"): None if success else bstack111ll11_opy_ (u"ࠤࡖࡹࡧࡶࡲࡰࡥࡨࡷࡸࠦࡣࡰ࡮࡯ࡩࡨࡺࡩࡰࡰࠣࡪࡦ࡯࡬ࡦࡦࠣࠬࡪࡾࡩࡵࠢࡾࢁ࠮ࠨ፥").format(proc.returncode)
        }
    except Exception as e:
        return {bstack111ll11_opy_ (u"ࠥࡷࡺࡩࡣࡦࡵࡶࠦ፦"): False, bstack111ll11_opy_ (u"ࠦࡨࡵࡵ࡯ࡶࠥ፧"): 0, bstack111ll11_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࡸࠨ፨"): [], bstack111ll11_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫࡯࡬ࡦࡵࠥ፩"): [], bstack111ll11_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨ፪"): bstack111ll11_opy_ (u"ࠣࡕࡸࡦࡵࡸ࡯ࡤࡧࡶࡷࠥࡩ࡯࡭࡮ࡨࡧࡹ࡯࡯࡯ࠢࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠧ፫").format(e)}