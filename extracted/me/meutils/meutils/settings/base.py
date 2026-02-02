from pydantic import BaseSettings as _BaseSettings

from meutils.pipe import *


class BaseSetting(_BaseSettings):
    class Config:
        env_file = os.getenv("EVN_FILE")
        env_file_encoding = 'utf-8'


if __name__ == '__main__':
    print(BaseSetting())
