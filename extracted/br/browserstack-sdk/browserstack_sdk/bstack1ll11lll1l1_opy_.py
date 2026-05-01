# coding: UTF-8
import sys
bstack1l11_opy_ = sys.version_info [0] == 2
bstack11_opy_ = 2048
bstackl_opy_ = 7
def bstack111ll_opy_ (bstack1ll1ll1_opy_):
    global bstack1ll111_opy_
    bstack1l11l1l_opy_ = ord (bstack1ll1ll1_opy_ [-1])
    bstack1llll_opy_ = bstack1ll1ll1_opy_ [:-1]
    bstack1l1lll_opy_ = bstack1l11l1l_opy_ % len (bstack1llll_opy_)
    bstack1_opy_ = bstack1llll_opy_ [:bstack1l1lll_opy_] + bstack1llll_opy_ [bstack1l1lll_opy_:]
    if bstack1l11_opy_:
        bstack11l1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    else:
        bstack11l1lll_opy_ = str () .join ([chr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    return eval (bstack11l1lll_opy_)
bstack111ll_opy_ (u"ࠦࠧࠨࠊࡑࡻࡷࡩࡸࡺࠠࡵࡧࡶࡸࠥࡩ࡯࡭࡮ࡨࡧࡹ࡯࡯࡯ࠢ࡫ࡩࡱࡶࡥࡳࠢࡸࡷ࡮ࡴࡧࠡࡦ࡬ࡶࡪࡩࡴࠡࡲࡼࡸࡪࡹࡴࠡࡪࡲࡳࡰࡹ࠮ࠋࠤࠥࠦፄ")
import pytest
import io
import os
from contextlib import redirect_stdout, redirect_stderr
import subprocess
import sys
def bstack1ll11ll1ll1_opy_(bstack1ll11llll11_opy_=None, bstack1ll11llll1l_opy_=None):
    bstack111ll_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࡉ࡯࡭࡮ࡨࡧࡹࠦࡰࡺࡶࡨࡷࡹࠦࡴࡦࡵࡷࡷࠥࡻࡳࡪࡰࡪࠤࡵࡿࡴࡦࡵࡷࠫࡸࠦࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠡࡃࡓࡍࡸ࠴ࠊࠡࠢࠣࠤࡆࡸࡧࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡹ࡫ࡳࡵࡡࡤࡶ࡬ࡹࠠࠩ࡮࡬ࡷࡹ࠲ࠠࡰࡲࡷ࡭ࡴࡴࡡ࡭ࠫ࠽ࠤࡈࡵ࡭ࡱ࡮ࡨࡸࡪࠦ࡬ࡪࡵࡷࠤࡴ࡬ࠠࡱࡻࡷࡩࡸࡺࠠࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠣ࡭ࡳࡩ࡬ࡶࡦ࡬ࡲ࡬ࠦࡰࡢࡶ࡫ࡷࠥࡧ࡮ࡥࠢࡩࡰࡦ࡭ࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡗࡥࡰ࡫ࡳࠡࡲࡵࡩࡨ࡫ࡤࡦࡰࡦࡩࠥࡵࡶࡦࡴࠣࡸࡪࡹࡴࡠࡲࡤࡸ࡭ࡹࠠࡪࡨࠣࡦࡴࡺࡨࠡࡣࡵࡩࠥࡶࡲࡰࡸ࡬ࡨࡪࡪ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡷࡩࡸࡺ࡟ࡱࡣࡷ࡬ࡸࠦࠨ࡭࡫ࡶࡸࠥࡵࡲࠡࡵࡷࡶ࠱ࠦ࡯ࡱࡶ࡬ࡳࡳࡧ࡬ࠪ࠼ࠣࡘࡪࡹࡴࠡࡨ࡬ࡰࡪ࠮ࡳࠪ࠱ࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽ࠭࡯ࡥࡴࠫࠣࡸࡴࠦࡣࡰ࡮࡯ࡩࡨࡺࠠࡧࡴࡲࡱ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡄࡣࡱࠤࡧ࡫ࠠࡢࠢࡶ࡭ࡳ࡭࡬ࡦࠢࡳࡥࡹ࡮ࠠࡴࡶࡵ࡭ࡳ࡭ࠠࡰࡴࠣࡰ࡮ࡹࡴࠡࡱࡩࠤࡵࡧࡴࡩࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡏࡧ࡯ࡱࡵࡩࡩࠦࡩࡧࠢࡷࡩࡸࡺ࡟ࡢࡴࡪࡷࠥ࡯ࡳࠡࡲࡵࡳࡻ࡯ࡤࡦࡦ࠱ࠎࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡩ࡯ࡣࡵ࠼ࠣࡇࡴࡲ࡬ࡦࡥࡷ࡭ࡴࡴࠠࡳࡧࡶࡹࡱࡺࡳࠡࡹ࡬ࡸ࡭ࠦ࡫ࡦࡻࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡹࡵࡤࡥࡨࡷࡸࠦࠨࡣࡱࡲࡰ࠮ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡣࡰࡷࡱࡸࠥ࠮ࡩ࡯ࡶࠬࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡳࡵࡤࡦ࡫ࡧࡷࠥ࠮࡬ࡪࡵࡷ࠭ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡺࡥࡴࡶࡢࡪ࡮ࡲࡥࡴࠢࠫࡰ࡮ࡹࡴࠪࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡨࡶࡷࡵࡲࠡࠪࡶࡸࡷ࠯ࠊࠡࠢࠣࠤࠧࠨࠢፅ")
    try:
        bstack1ll11lllll1_opy_ = os.getenv(bstack111ll_opy_ (u"ࠨࡐ࡚ࡖࡈࡗ࡙ࡥࡃࡖࡔࡕࡉࡓ࡚࡟ࡕࡇࡖࡘࠧፆ")) is not None
        if bstack1ll11llll11_opy_ is not None:
            args = list(bstack1ll11llll11_opy_)
        elif bstack1ll11llll1l_opy_ is not None:
            if isinstance(bstack1ll11llll1l_opy_, str):
                args = [bstack1ll11llll1l_opy_]
            elif isinstance(bstack1ll11llll1l_opy_, list):
                args = list(bstack1ll11llll1l_opy_)
            else:
                args = [bstack111ll_opy_ (u"ࠢ࠯ࠤፇ")]
        else:
            args = [bstack111ll_opy_ (u"ࠣ࠰ࠥፈ")]
        if bstack1ll11lllll1_opy_:
            return _1ll11llllll_opy_(args)
        bstack1ll11ll1l1l_opy_ = args + [
            bstack111ll_opy_ (u"ࠤ࠰࠱ࡨࡵ࡬࡭ࡧࡦࡸ࠲ࡵ࡮࡭ࡻࠥፉ"),
            bstack111ll_opy_ (u"ࠥ࠱࠲ࡷࡵࡪࡧࡷࠦፊ")
        ]
        class bstack1ll11lll11l_opy_:
            bstack111ll_opy_ (u"ࠦࠧࠨࡐࡺࡶࡨࡷࡹࠦࡰ࡭ࡷࡪ࡭ࡳࠦࡴࡩࡣࡷࠤࡨࡧࡰࡵࡷࡵࡩࡸࠦࡣࡰ࡮࡯ࡩࡨࡺࡥࡥࠢࡷࡩࡸࡺࠠࡪࡶࡨࡱࡸ࠴ࠢࠣࠤፋ")
            def __init__(self):
                self.bstack1ll11lll111_opy_ = []
                self.test_files = set()
                self.bstack1ll1l111111_opy_ = None
            def pytest_collection_finish(self, session):
                bstack111ll_opy_ (u"ࠧࠨࠢࡉࡱࡲ࡯ࠥࡩࡡ࡭࡮ࡨࡨࠥࡧࡦࡵࡧࡵࠤࡨࡵ࡬࡭ࡧࡦࡸ࡮ࡵ࡮ࠡ࡫ࡶࠤ࡫࡯࡮ࡪࡵ࡫ࡩࡩ࠴ࠢࠣࠤፌ")
                try:
                    for item in session.items:
                        nodeid = item.nodeid
                        self.bstack1ll11lll111_opy_.append(nodeid)
                        if bstack111ll_opy_ (u"ࠨ࠺࠻ࠤፍ") in nodeid:
                            file_path = nodeid.split(bstack111ll_opy_ (u"ࠢ࠻࠼ࠥፎ"), 1)[0]
                            if file_path.endswith(bstack111ll_opy_ (u"ࠨ࠰ࡳࡽࠬፏ")):
                                self.test_files.add(file_path)
                except Exception as e:
                    self.bstack1ll1l111111_opy_ = str(e)
        collector = bstack1ll11lll11l_opy_()
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            exit_code = pytest.main(bstack1ll11ll1l1l_opy_, plugins=[collector])
        if collector.bstack1ll1l111111_opy_:
            return {bstack111ll_opy_ (u"ࠤࡶࡹࡨࡩࡥࡴࡵࠥፐ"): False, bstack111ll_opy_ (u"ࠥࡧࡴࡻ࡮ࡵࠤፑ"): 0, bstack111ll_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࡷࠧፒ"): [], bstack111ll_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪ࡮ࡲࡥࡴࠤፓ"): [], bstack111ll_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧፔ"): bstack111ll_opy_ (u"ࠢࡄࡱ࡯ࡰࡪࡩࡴࡪࡱࡱࠤࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠢፕ").format(collector.bstack1ll1l111111_opy_)}
        return {
            bstack111ll_opy_ (u"ࠣࡵࡸࡧࡨ࡫ࡳࡴࠤፖ"): True,
            bstack111ll_opy_ (u"ࠤࡦࡳࡺࡴࡴࠣፗ"): len(collector.bstack1ll11lll111_opy_),
            bstack111ll_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࡶࠦፘ"): collector.bstack1ll11lll111_opy_,
            bstack111ll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩ࡭ࡱ࡫ࡳࠣፙ"): sorted(collector.test_files),
            bstack111ll_opy_ (u"ࠧ࡫ࡸࡪࡶࡢࡧࡴࡪࡥࠣፚ"): exit_code
        }
    except Exception as e:
        return {bstack111ll_opy_ (u"ࠨࡳࡶࡥࡦࡩࡸࡹࠢ፛"): False, bstack111ll_opy_ (u"ࠢࡤࡱࡸࡲࡹࠨ፜"): 0, bstack111ll_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࡴࠤ፝"): [], bstack111ll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧ࡫࡯ࡩࡸࠨ፞"): [], bstack111ll_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤ፟"): bstack111ll_opy_ (u"࡚ࠦࡴࡥࡹࡲࡨࡧࡹ࡫ࡤࠡࡧࡵࡶࡴࡸࠠࡪࡰࠣࡸࡪࡹࡴࠡࡥࡲࡰࡱ࡫ࡣࡵ࡫ࡲࡲ࠿ࠦࡻࡾࠤ፠").format(e)}
def _1ll11llllll_opy_(args):
    bstack111ll_opy_ (u"ࠧࠨࠢࡊࡵࡲࡰࡦࡺࡥࡥࠢࡦࡳࡱࡲࡥࡤࡶ࡬ࡳࡳࠦࡥࡹࡧࡦࡹࡹ࡫ࡤࠡ࡫ࡱࠤࡦࠦࡳࡦࡲࡤࡶࡦࡺࡥࠡࡒࡼࡸ࡭ࡵ࡮ࠡࡲࡵࡳࡨ࡫ࡳࡴࠢࡷࡳࠥࡧࡶࡰ࡫ࡧࠤࡳ࡫ࡳࡵࡧࡧࠤࡵࡿࡴࡦࡵࡷࠤ࡮ࡹࡳࡶࡧࡶ࠲ࠧࠨࠢ፡")
    bstack1ll11lll1ll_opy_ = [sys.executable, bstack111ll_opy_ (u"ࠨ࠭࡮ࠤ።"), bstack111ll_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺࠢ፣"), bstack111ll_opy_ (u"ࠣ࠯࠰ࡧࡴࡲ࡬ࡦࡥࡷ࠱ࡴࡴ࡬ࡺࠤ፤"), bstack111ll_opy_ (u"ࠤ࠰࠱ࡶࡻࡩࡦࡶࠥ፥")]
    bstack1ll11ll1lll_opy_ = [a for a in args if a not in (bstack111ll_opy_ (u"ࠥ࠱࠲ࡩ࡯࡭࡮ࡨࡧࡹ࠳࡯࡯࡮ࡼࠦ፦"), bstack111ll_opy_ (u"ࠦ࠲࠳ࡱࡶ࡫ࡨࡸࠧ፧"), bstack111ll_opy_ (u"ࠧ࠳ࡱࠣ፨"))]
    cmd = bstack1ll11lll1ll_opy_ + bstack1ll11ll1lll_opy_
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, env=os.environ.copy())
        stdout = proc.stdout.splitlines()
        bstack1ll11lll111_opy_ = []
        test_files = set()
        for line in stdout:
            line = line.strip()
            if not line or bstack111ll_opy_ (u"ࠨࠠࡤࡱ࡯ࡰࡪࡩࡴࡦࡦࠥ፩") in line.lower():
                continue
            if bstack111ll_opy_ (u"ࠢ࠻࠼ࠥ፪") in line:
                bstack1ll11lll111_opy_.append(line)
                file_path = line.split(bstack111ll_opy_ (u"ࠣ࠼࠽ࠦ፫"), 1)[0]
                if file_path.endswith(bstack111ll_opy_ (u"ࠩ࠱ࡴࡾ࠭፬")):
                    test_files.add(file_path)
        success = proc.returncode in (0, 5)
        return {
            bstack111ll_opy_ (u"ࠥࡷࡺࡩࡣࡦࡵࡶࠦ፭"): success,
            bstack111ll_opy_ (u"ࠦࡨࡵࡵ࡯ࡶࠥ፮"): len(bstack1ll11lll111_opy_),
            bstack111ll_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࡸࠨ፯"): bstack1ll11lll111_opy_,
            bstack111ll_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫࡯࡬ࡦࡵࠥ፰"): sorted(test_files),
            bstack111ll_opy_ (u"ࠢࡦࡺ࡬ࡸࡤࡩ࡯ࡥࡧࠥ፱"): proc.returncode,
            bstack111ll_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢ፲"): None if success else bstack111ll_opy_ (u"ࠤࡖࡹࡧࡶࡲࡰࡥࡨࡷࡸࠦࡣࡰ࡮࡯ࡩࡨࡺࡩࡰࡰࠣࡪࡦ࡯࡬ࡦࡦࠣࠬࡪࡾࡩࡵࠢࡾࢁ࠮ࠨ፳").format(proc.returncode)
        }
    except Exception as e:
        return {bstack111ll_opy_ (u"ࠥࡷࡺࡩࡣࡦࡵࡶࠦ፴"): False, bstack111ll_opy_ (u"ࠦࡨࡵࡵ࡯ࡶࠥ፵"): 0, bstack111ll_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࡸࠨ፶"): [], bstack111ll_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫࡯࡬ࡦࡵࠥ፷"): [], bstack111ll_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨ፸"): bstack111ll_opy_ (u"ࠣࡕࡸࡦࡵࡸ࡯ࡤࡧࡶࡷࠥࡩ࡯࡭࡮ࡨࡧࡹ࡯࡯࡯ࠢࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠧ፹").format(e)}