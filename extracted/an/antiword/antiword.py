from argparse import ArgumentParser
from pathlib import Path
from tempfile import TemporaryDirectory
from subprocess import run


def main():
    parser = ArgumentParser()
    parser.add_argument("IN", type=Path)
    args = parser.parse_args()

    with TemporaryDirectory() as d:
        cmd = [
            "libreoffice",
            "--convert-to",
            "txt",
            "--outdir",
            d,
            str(args.IN.resolve()),
        ]
        r = run(cmd)
        with (Path(d) / f"{args.IN.stem}.txt").open() as f:
            for line in f:
                print(line, end="")


if __name__ == "__main__":
    main()
