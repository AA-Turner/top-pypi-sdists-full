"""Allow ``python -m scrapy_ingest`` when the ``scrapy-ingest.exe`` shim is blocked."""
import sys

from scrapy_ingest.cli import main

if __name__ == "__main__":
    sys.exit(main())
