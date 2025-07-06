"""Run the Brian Spiral Healer API via uvicorn."""

import uvicorn
from tsal.api import app


def main() -> None:
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
