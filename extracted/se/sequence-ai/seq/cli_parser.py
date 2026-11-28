"""
The open `seq` command tree: `seq init`, `seq serve` and `seq weights get`, their arguments and their help -
`build_parser()`, which seq/cli.py's `main` parses argv with (seq/cli.py keeps the dispatch). sequence-cloud, GS's
client for its platform, mounts the platform's commands - deploy, eval, policy, gpu, account and the rest - on the same
tree through the `seq.commands` entry point (sequence_ai/_core/plugins.py), its overview with them; without it, typing
one of their names says where it is.
Building the parser stays cheap: a command's heavy imports live inside the command, so `seq --help` loads neither numpy
nor mujoco.
"""
from __future__ import annotations

import argparse
from typing import Any

from sequence_ai._core.plugins import loaded, needs_cloud
from sequence_ai.engine.compiled import tensorrt_install as _tensorrt_install


class _DescFromHelp(argparse._SubParsersAction):
    """A subcommand's own --help should say what it does, not list its arguments alone. A command added with a one-line
    `help=` (what the parent's command list shows) and no `description=` gets that help as its description too, so `seq
    <cmd> --help` opens with it; a command that gives a fuller `description=` of its own keeps it. The help stays as the
    parent's list wants it (lower-case, to read after the command name); its description leads a page of its own, so its
    first letter is upper-cased - a description reads as a sentence, and the hand-written ones already begin capital.
    
"""

    def add_parser(self, name, **kwargs):
        help_text = kwargs.get("help")
        if help_text and not kwargs.get("description"):
            kwargs["description"] = help_text[0].upper() + help_text[1:]
        return super().add_parser(name, **kwargs)





_ELSEWHERE: dict = {}

_SAME = {"delete": "rm", "remove": "rm", "list": "ls"}




_CLOUD_COMMANDS = frozenset(("deploy eval policy robot key benchmark adapter volume secret login logout profile "
                             "audit models gpus gpu account billing storage usage").split())


def _meant(prog: str, value: str, choices: list[str]) -> list[str]:
    """The one or two commands `prog value` most likely meant: another name for one of `choices`, a command elsewhere
    the word names, else the nearest spellings among `choices`; none when nothing is near."""
    import difflib

    if _SAME.get(value) in choices:
        return [f"{prog} {_SAME[value]}"]
    if value in _ELSEWHERE:
        return list(_ELSEWHERE[value])
    return [f"{prog} {c}" for c in difflib.get_close_matches(value, choices, n=2, cutoff=0.6)]



def _tolerance(text: str):
    """--tolerance: a number, or max_abs=...,mean_abs=...,cosine=... (sequence_ai.engine.optimize's tolerance)."""
    try:
        return float(text)
    except ValueError:
        pass
    out = {}
    for part in text.split(","):
        name, eq, value = part.partition("=")
        try:
            out[name.strip()] = float(value)
        except ValueError:
            raise argparse.ArgumentTypeError(f"{text!r}: a number, or max_abs=...,mean_abs=...,cosine=...") from None
        if not eq:
            raise argparse.ArgumentTypeError(f"{text!r}: a number, or max_abs=...,mean_abs=...,cosine=...")
    return out


class _Parser(argparse.ArgumentParser):
    """seq's parser, its subcommands' too (argparse makes those of the parent's class): a command it does not have is
    said in one line with the one or two it most likely meant (_meant), where argparse printed its usage and every
    command at that level - a usage error still, ended as argparse ends one, exit 2.
"""

    def _check_value(self, action: argparse.Action, value: Any) -> None:
        if isinstance(action, argparse._SubParsersAction) and value not in action.choices:
            if self.prog == "seq" and value in _CLOUD_COMMANDS:

                self.exit(2, f"error[invalid_request]: {needs_cloud(f'`seq {value}`')}\n")
            meant = _meant(self.prog, value, list(action.choices))
            said = (f"did you mean {' or '.join(f'`{m}`' for m in meant)}?" if meant
                    else f"`{self.prog} --help` lists them")

            self.exit(2, f"error[invalid_request]: `{self.prog} {value}` is no command: {said}\n")
        super()._check_value(action, value)


def _version() -> str:


    from sequence_ai import __version__

    return __version__



_OVERVIEW = """\
Start from a template and serve its policy from this machine's GPU; a robot connects with
connect("http://<this machine>:8000").

  init <template> [dir]     start from a policy template (seq init --list)
  serve [folder]            serve the folder's @seq.policy from this machine's GPU, a template's weights downloaded
                            with your key
  weights get <template>    download one version of a template's weights, with your key
  check <url|name>          what is on, and what is not, between this machine and a policy server, or a deployment
                            on GS's platform by its name
  teleop serve              pair a robot and the consoles that drive it, from this machine
  data export <recording>   a robot's recordings as a LeRobot v3.0 dataset, or JSON lines

`seq <command> --help` tells more.
"""


def _group(ap: argparse.ArgumentParser, sub: Any, name: str, description: str) -> Any:
    """A category: `seq <name> <command>`. Kept on the parser so a bare `seq <name>` can print its commands."""
    p = sub.add_parser(name, description=description)
    ap.seq_groups[name] = p
    return p.add_subparsers(dest=f"{name}_cmd", metavar="<command>", action=_DescFromHelp)



def _overview() -> str:
    """`seq --help`'s overview."""
    return _OVERVIEW



def build_parser() -> argparse.ArgumentParser:
    """The `seq` command tree: init, serve and weights get, and every command sequence-cloud mounts (its register(ap,
    sub), the `seq.commands` entry point). Exposed (not inlined into `main`) so tests can drive it."""
    ap = _Parser(prog="seq", description=_overview(), formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.seq_groups = {}
    ap.add_argument("--version", action="version", version=f"seq {_version()}")

    ap.add_argument("--base-url", default=None, help=argparse.SUPPRESS)
    ap.add_argument("--json", action="store_true", help="print what the command read as JSON, for scripts")
    sub = ap.add_subparsers(dest="cmd", metavar="<command>", help="one of the commands above", action=_DescFromHelp)








    p = sub.add_parser("init", description="Start from a template: a policy or an adapter, from the platform. The "
                                           "benchmarks are ours: an eval runs any of their tasks as they are, `seq "
                                           "eval run <policy> --task <id> ...` - nothing to start from or build.")
    p.add_argument("template", nargs="?",
                   help="a template, its version the one `seq init --list` shows (pi05-droid), or an exact version "
                        "(pi05-droid@v12)")
    p.add_argument("dest", nargs="?", default=None,
                   help="the directory to create (default: the template's name): a policy deploys under it; an "
                        "adapter keeps the name its file gives, which the next step names")
    p.add_argument("--list", action="store_true", dest="list_only", help="list the templates, by kind")
    p.add_argument("--no-source", action="store_true", dest="no_source",
                   help="do not download a template's large upstream sources (third_party/SOURCES.json) - the image "
                        "installs them from their official packages either way")

    p = sub.add_parser("serve", description="Serve a folder's @seq.policy, or an official template's by its name, from "
                                            "this machine until Ctrl-C: the class "
                                            "built as the platform builds it - its init= filled, a template's weights "
                                            "downloaded with your key into ~/.cache/sequence-ai/weights and checked by "
                                            "their sha256 - a @seq.concurrent policy's acts batched in its sizes as the "
                                            "platform batches them. A robot connects with sequence_ai.connect("
                                            "\"http://<this machine>:<port>\"). What the folder's code imports must be "
                                            "installed here, as its image installs it (requirements-policy.lock).")


    p.add_argument("folder", nargs="?", default=".",
                   help="the folder `seq init` made, one .py file holding the policy, or an official template's name "
                        "(pi05-droid, pi05-droid@v12), whose code is kept in ~/.cache/sequence-ai/templates as `seq "
                        "init` writes it; a folder here of that name is served instead (default: this folder)")
    p.add_argument("--name", default=None, help="the policy to serve, when the folder holds several")
    p.add_argument("--port", type=int, default=8000, help="the port it listens on (default 8000)")
    p.add_argument("--host", default=None,
                   help="the address it listens on (default: every address of this machine; 127.0.0.1: this one only)")
    p.add_argument("--weights", action="append", default=None, metavar="[PART=]DIR",
                   help="a folder holding the weights, read instead of downloading them; PART=DIR for a named part "
                        "(repeat it for each)")
    p.add_argument("--token", default=None,
                   help="a token each robot must send (sequence_ai.connect(url, token=...))")
    p.add_argument("--no-cuda-graphs", action="store_const", const=False, dest="cuda_graphs", default=None,
                   help="do not replay the policy's modules from CUDA graphs (tried by default on a PyTorch policy, "
                        "kept where the answers stay the same, bit for bit, on its sample episode, and acts are at "
                        "least 10%% faster)")
    p.add_argument("--cuda-graphs", action="store_const", const=True, dest="cuda_graphs",
                   help="try them on a JAX policy too, as XLA's command buffers (not tried on one by default)")
    p.add_argument("--no-whole-graph", action="store_const", const=False, dest="whole_graph", default=None,
                   help="do not replay an act's whole call into the model as one CUDA graph (tried by default on a "
                        "PyTorch policy, kept where the answers stay the same, bit for bit, and acts are at least "
                        "10%% faster)")
    p.add_argument("--whole-graph", action="store_const", const=True, dest="whole_graph",
                   help="try it on a JAX policy too, its loops in XLA's command buffers (not tried on one by default)")
    p.add_argument("--torch-compile", action="store_true", dest="torch_compile",
                   help="try torch.compile on the modules acts spend their time in (changes the answers: needs "
                        "--tolerance)")
    p.add_argument("--fused-kernels", action="store_true", dest="fused_kernels",
                   help="try fused kernels for their norms, gated activations and rotary embeddings (needs --tolerance)")
    p.add_argument("--tensorrt", action="store_true",
                   help="try TensorRT on those modules, TF32 off; needs --tolerance, and TensorRT: "
                        + _tensorrt_install())
    p.add_argument("--precision", choices=["fp32", "fp16", "fp8"], default=None,
                   help="try those modules in float16 or float32, or their linear layers in fp8 on a GPU of compute "
                        "capability 8.9 or later (needs --tolerance; by default the model keeps its own dtype)")
    p.add_argument("--cfg-parallel", action="store_true", dest="cfg_parallel",
                   help="on a server of two processes (torchrun --nproc-per-node 2), try running the half of each "
                        "guidance batch on each (needs --tolerance)")
    p.add_argument("--pipeline-parallel", action="store_true", dest="pipeline_parallel",
                   help="on a server of two processes or more (torchrun --nproc-per-node N), try splitting the "
                        "model's blocks into one stage each, its calls passed through them in parts (needs "
                        "--tolerance)")
    p.add_argument("--tolerance", type=_tolerance, default=None, metavar="LIMIT",
                   help="the difference from eager mode's answers you accept for the switches above: a number (the "
                        "largest absolute difference), or max_abs=...,mean_abs=...,cosine=...")

    wsub = _group(ap, sub, "weights", "An official template's weights on this machine, each file checked by its sha256: "
                                      "what `seq serve` reads.")
    p = wsub.add_parser("get", help="download one version of a template's weights, with your key",
                        description="Download one version of an official template's weights - the latest, or the "
                                    "version @vN names - with your key, into ~/.cache/sequence-ai/weights/<template>/"
                                    "<version> or --dir, each file checked by its sha256. Files already there are kept, "
                                    "so a run again downloads what is missing alone. Prints the folder.")
    p.add_argument("template", help="the template, and a version if you name one (pi05-libero, pi05-libero@v1)")
    p.add_argument("--dir", default=None, help="the folder to download into")

    tsub = _group(ap, sub, "teleop", "A person drives a robot from a console, connected straight to it: this machine "
                                     "pairs the two.")
    p = tsub.add_parser("serve", help="pair a robot and the consoles that drive it, from this machine, until Ctrl-C",
                        description="Pair a robot and the consoles that drive it, from this machine, until Ctrl-C - "
                                    "the platform's pairing, with no account. The robot connects with "
                                    "sequence_ai.connect(\"http://<this machine>:8200\", token=...), a console with "
                                    "sequence_ai.teleop(\"http://<this machine>:8200\", token=...) or the page served "
                                    "at that address; then the two talk to each other straight, past this machine. "
                                    "Needs sequence-ai[teleop] on the robot and on a Python console.")
    p.add_argument("--port", type=int, default=8200, help="the port it listens on (default 8200)")
    p.add_argument("--host", default=None,
                   help="the address it listens on (default: every address of this machine; 127.0.0.1: this one only)")
    p.add_argument("--token", default=None,
                   help="the token the robot and each console must send (default: $SEQ_TELEOP_TOKEN, else one made "
                        "for this run and printed once; \"\" for none)")
    p.add_argument("--robot", default=None, help="the name its robot goes by (default: this machine's name)")
    p.add_argument("--record", action="store_true",
                   help="turn the robot's Record on: it writes its steps to a file on its own machine, which "
                        "`seq data export` turns into a dataset")
    p.add_argument("--turn", action="append", default=None, metavar="URL",
                   help="a TURN server the robot and its consoles may relay through where they cannot meet directly "
                        "(turn:host:3478); repeat it for each")
    p.add_argument("--turn-secret", default=None,
                   help="that server's shared secret (coturn's static-auth-secret), which each side's credentials "
                        "are made with (default: $SEQ_TELEOP_TURN_SECRET)")
    p.add_argument("--turn-ttl", type=float, default=None, metavar="SECONDS",
                   help="how long each side's credentials are good for (default 12 hours)")
    p.add_argument("--moq-port", type=int, default=None, metavar="PORT",
                   help="serve a MoQ relay on this UDP port for the people watching the robot: it uploads once, "
                        "however many watch with sequence_ai.teleop(..., via=\"moq\"); needs sequence-ai[moq] here "
                        "and on the robot")
    p.add_argument("--moq", default=None, metavar="URL",
                   help="a MoQ relay of your own for them instead (moq-relay 0.17): https://HOST:PORT/, or http:// "
                        "for one that made its own certificate")

    dsub = _group(ap, sub, "data", "A robot's recordings on this machine as a dataset.")
    p = dsub.add_parser("export", help="a robot's recordings as a LeRobot v3.0 dataset, or JSON lines",
                        description="Write the recordings named - .msgpack files, or folders of them, that a robot's "
                                    "Record wrote (seq teleop serve --record) or `seq robot record` wrote - as one "
                                    "LeRobot v3.0 dataset: a frame for every step observed, each camera an image "
                                    "column, every other number an array, the action each step was given, who drove "
                                    "it, each episode's instruction its task and its label next.success. --format "
                                    "jsonl writes every item as a line of JSON instead, a file a recording. The "
                                    "LeRobot format needs pyarrow: pip install 'sequence-ai[data]'.")
    p.add_argument("recordings", nargs="+", help="the recordings: .msgpack files, or folders holding them")
    p.add_argument("-o", "--out", required=True, help="the folder to write the dataset to")
    p.add_argument("--format", choices=["lerobot", "jsonl"], default="lerobot", help="lerobot (default) or jsonl")
    p.add_argument("--fps", type=float, default=None,
                   help="the dataset's frame rate (default: the pace its robots observed at)")




    from sequence_ai import check as _check

    _check.add_arguments(sub.add_parser("check", description=_check.DESCRIPTION))

    for plugin in loaded("seq.commands"):
        plugin.register(ap, sub)
    return ap
