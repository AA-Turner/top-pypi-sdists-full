from datetime import datetime
import json
import os
import sys
import click

class Log:
    DEBUG = False

    def is_debug():
        return Log.DEBUG

    def debug(s: None):
        if Log.DEBUG:
            Log.log2(f'DEBUG {s}')

    def log(s = None):
        # want to print empty line for False or empty collection
        if s == None:
            print()
        else:
            click.echo(s)

    def log2(s = None):
        if s:
            click.echo(s, err=True)
        else:
            print(file=sys.stderr)

    def log_to_file(config: dict[any, any]):
        try:
            base = f"/tmp/logs"
            os.makedirs(base, exist_ok=True)

            now = datetime.now()
            timestamp_str = now.strftime("%Y%m%d-%H%M%S")
            filename = f"{base}/login.{timestamp_str}.txt"
            with open(filename, 'w') as f:
                if isinstance(config, dict):
                    try:
                        json.dump(config, f, indent=4)
                    except:
                        f.write(config)
                else:
                        f.write(config)
        except:
            pass