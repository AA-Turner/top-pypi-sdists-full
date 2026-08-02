from textual.app import App, ComposeResult
from textual.widgets import Static
from textual import events
import math,os

class NXWelcome(App):
    BINDINGS = [("ctrl+c", "quit", "Quit"), ("ctrl+q", "quit", "Quit")]

    CSS = """
    Screen {
        background: #050505;
        color: #b89a5e;
    }
    #panel {
        width: 100%;
        border: solid #c8a44a;
        background: #050505;
    }
    #inner {
        layout: horizontal;
        height: 16;
        width: 100%;
    }
    #left {
        width: 28;
        border-right: solid #c8a44a;
        padding: 1 2;
    }
    #right {
        width: 1fr;
        padding: 1 2;
    }
    #stars {
        border-top: solid #c8a44a;
        border-bottom: solid #c8a44a;
        height: 3;
        padding: 0 1;
    }
    #meta {
        height: 5;
        padding: 1 2;
    }
    #auth {
        width: 100%;
        padding: 1 0 0 0;
    }
    """

    TIPS = [
        [("Type your task directly to start","dim"),("/help  /mode  /model  /council  /exit","gold"),("Sessions saved automatically","dim")],
        [("Use /model to switch models","dim"),("BYOK or use Nexplora credits","dim"),("Plan First for complex tasks","gold")],
        [("Route across every world instantly","dim"),("Autonomous execution, reviewable","dim"),("$council — 3 models debate hard calls","gold")],
    ]

    @staticmethod
    def _live_caps():
        """Real worlds/tiers/skills counts — never fabricated. Safe fallbacks."""
        worlds = tiers = skills = 0
        try:
            import nx_routing as _r
            worlds = len(_r.WORLD_CONFIG)
            tiers = len(_r.TIERS_BY_PROVIDER.get(_r.PRIMARY_PROVIDER, {}))
        except Exception:
            pass
        try:
            import nx_skills_import as _s
            skills = int((_s.skills_summary() or {}).get("total", 0) or 0)
        except Exception:
            pass
        return worlds, tiers, skills

    def __init__(self, cfg=None):
        super().__init__()
        self.cfg = cfg or {}
        self._t = 0
        self._sf = 0
        self._tip_set = 0
        self._tip_tick = 0
        self._selected = 0  # 0 = OAuth, 1 = API key
        self.choice = None

    def compose(self) -> ComposeResult:
        with Static(id="panel"):
            with Static(id="inner"):
                yield Static(self._logo(0), id="left")
                yield Static(self._right(), id="right")
            yield Static(self._stars(0), id="stars")
            yield Static(self._meta(), id="meta")
        yield Static(self._auth(), id="auth")

    def on_mount(self):
        self.set_interval(0.055, self._tick)

    def _tick(self):
        self._t += 1
        self._sf = (self._sf + 1) % 60
        self._tip_tick += 1
        if self._tip_tick >= 140:
            self._tip_tick = 0
            self._tip_set = (self._tip_set + 1) % len(self.TIPS)
            self.query_one("#right", Static).update(self._right())
        self.query_one("#left", Static).update(self._logo(self._t))
        self.query_one("#stars", Static).update(self._stars(self._sf))

    def on_key(self, event: events.Key):
        if event.key == "ctrl+c":
            event.stop()
            self.choice = None
            self.exit()
        elif event.key in ("up", "down", "tab"):
            self._selected = 1 - self._selected
            self.query_one("#auth", Static).update(self._auth())
        elif event.key in ("enter", "space"):
            self.choice = "oauth" if self._selected == 0 else "apikey"
            self.exit()
        elif event.key == "1":
            self.choice = "oauth"
            self.exit()
        elif event.key == "2":
            self.choice = "apikey"
            self.exit()
        elif event.key in ("q", "escape", "ctrl+c"):
            self.choice = None
            self.exit()

    def _logo(self, T):
        from rich.text import Text
        version=self.cfg.get("_version","0.3.50")
        W,H=20,10; cx,cy=9,5
        grid=[[" "]*W for _ in range(H)]
        br=[[0.0]*W for _ in range(H)]
        SPD=0.025; TLEN=22

        def lemnH(t):
            s,c=math.sin(t),math.cos(t); d=1+s*s
            return cx+8*c/d, cy+4*s*c/d

        def lemnV(t):
            s,c=math.sin(t),math.cos(t); d=1+s*s
            return cx+3*s*c/d, cy+8*c/d

        paths=[(lemnH,0,SPD),(lemnH,math.pi,SPD),(lemnV,math.pi/2,SPD*0.85),(lemnV,math.pi*1.5,SPD*0.85)]

        for pfn,ph,sp in paths:
            head=ph+T*sp
            for i in range(TLEN,0,-1):
                x,y=pfn(head-i*0.09)
                xi,yi=int(round(x)),int(round(y))
                b2=((TLEN-i)/TLEN)**1.3*0.9
                if 0<=yi<H and 0<=xi<W and b2>br[yi][xi]:
                    br[yi][xi]=b2; grid[yi][xi]="·"

        NL=cx-3; NT=1; NH=H-2; BAR=1; NW=6
        for row in range(NT,NT+NH):
            if 0<=row<H:
                if 0<=NL<W: grid[row][NL]="▌"; br[row][NL]=-1
                if 0<=NL+NW<W: grid[row][NL+NW]="▐"; br[row][NL+NW]=-1
        for step in range(NH):
            row=NT+step; col=NL+int(NW*step/NH)
            if 0<=row<H and 0<=col<W: grid[row][col]="░"; br[row][col]=-2
            if 0<=row<H and 0<=col+1<W: grid[row][col+1]="░"; br[row][col+1]=-2

        for pfn,ph,sp in paths:
            hx,hy=pfn(ph+T*sp)
            xi,yi=int(round(hx)),int(round(hy))
            if 0<=yi<H and 0<=xi<W: grid[yi][xi]="✦"; br[yi][xi]=1.0

        out=Text()
        for r in range(H):
            for c in range(W):
                ch=grid[r][c]; b2=br[r][c]
                if ch==" ": out.append(" ")
                elif b2==-1: out.append(ch,style="rgb(18,14,6)")
                elif b2==-2: out.append(ch,style="rgb(28,22,8)")
                else:
                    gr=int(45+155*b2); gg=int(35+129*b2); gb=int(15+59*b2)
                    out.append(ch,style=f"rgb({gr},{gg},{gb})")
            out.append("\n")

        who=self.cfg.get("account","")
        out.append("\n")
        if who:
            out.append("Welcome back\n",style="rgb(120,98,44)")
            out.append(f"{who}\n",style="#c8a44a bold")
        else:
            out.append("Nexplora\n",style="#c8a44a bold")
        out.append(f"NX v{version}",style="rgb(80,62,22)")
        return out

    def _right(self):
        from rich.text import Text
        out=Text()
        out.append("TIPS\n",style="#c8a44a bold")
        tips=self.TIPS[self._tip_set]
        for text,style in tips:
            if style=="gold":
                out.append(f"  {text}\n",style="#c8a44a")
            else:
                out.append(f"  {text}\n",style="rgb(100,78,28)")
        out.append("\n")
        worlds, tiers, skills = self._live_caps()
        out.append("WHAT'S LIVE\n",style="#c8a44a bold")
        out.append("  " + str(worlds),style="#c8a44a bold")
        out.append(" worlds  ·  ",style="rgb(100,78,28)")
        out.append(str(tiers),style="#c8a44a bold")
        out.append(" model tiers\n",style="rgb(100,78,28)")
        if skills > 0:
            out.append("  " + f"{skills:,}",style="#c8a44a bold")
            out.append(" skills loaded\n",style="rgb(100,78,28)")
        out.append("  ",style="rgb(100,78,28)")
        out.append("Plan First",style="#c8a44a bold")
        out.append(" — autonomous, reviewable\n",style="rgb(100,78,28)")
        out.append("  BYOK or Nexplora credits",style="rgb(100,78,28)")
        return out

    def _stars(self,frame):
        from rich.text import Text
        SLOTS=58; TR=["✦","✧","·"," "]; BR=[1.0,0.65,0.35,0.0]
        orb=[" "]*SLOTS; brt=[0.0]*SLOTS
        for s in range(3):
            h=(frame+s*(SLOTS//3))%SLOTS
            for t,ch in enumerate(TR):
                p=(h-t)%SLOTS; orb[p]=ch; brt[p]=BR[t]
        out=Text()
        for i in range(SLOTS):
            ch=orb[i]; b2=brt[i]
            if ch==" " or b2==0: out.append(" ")
            else:
                r=int(5+195*b2); g=int(5+159*b2); b=int(5+69*b2)
                out.append(ch,style=f"rgb({r},{g},{b})")
        return out

    def _meta(self):
        from rich.text import Text
        version=self.cfg.get("_version","0.3.50")
        out=Text()
        for label,val in [("Model    ","Nexplora model layer"),("Version  ",f"NX v{version}"),("Directory",os.getcwd())]:
            out.append(f"  {label}  ",style="rgb(80,62,22)")
            out.append(f"{val}\n",style="#c8a44a")
        return out

    def _auth(self):
        from rich.text import Text
        out=Text()
        out.append("  Sign in to your Nexplora account\n",style="#c8a44a bold")
        out.append("  ↑ ↓ to select   Enter to confirm\n\n",style="rgb(60,46,14)")
        if self._selected == 0:
            out.append("  ❯ Browser sign-in (OAuth)\n",style="#c8a44a bold")
            out.append("    Paste API key\n",style="rgb(60,46,14)")
        else:
            out.append("    Browser sign-in (OAuth)\n",style="rgb(60,46,14)")
            out.append("  ❯ Paste API key\n",style="#c8a44a bold")
        return out

if __name__=="__main__":
    app=NXWelcome()
    app.run()
    print(f"choice: {app.choice}")
