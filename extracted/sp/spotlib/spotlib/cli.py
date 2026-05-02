"""

ec2 spotprice retriever, GPL v3 License

Copyright (c) 2018-2019 Blake Huber

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the 'Software'), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""
import os
import sys
import datetime
import json
import inspect
import argparse
import subprocess
import boto3
from botocore.exceptions import ClientError
from libtools import stdout_message
from libtools.js import export_iterobject
from spotlib import SpotPrices, UtcConversion
from spotlib.help_menu import menu_body
from spotlib import about, logger
from spotlib.variables import acct, bd, bdwt, bbc, bl, bbl, btext, fs, rst


try:
    from libtools.oscodes_unix import exit_codes
    os_type = 'Linux'
    user_home = os.getenv('HOME')
    splitchar = '/'                                   # character for splitting paths (linux)

except Exception:
    from libtools.oscodes_win import exit_codes         # non-specific os-safe codes
    os_type = 'Windows'
    user_home = os.getenv('username')
    splitchar = '\\'                                  # character for splitting paths (windows)


# globals
container = []
module = os.path.basename(__file__)
iloc = os.path.abspath(os.path.dirname(__file__))     # installed location of modules


def _debug_output(*args):
    """additional verbose information output"""
    for arg in args:
        if os.path.isfile(arg):
            print('Filename {}'.format(arg.strip(), 'lower'))
        elif str(arg):
            print('String {} = {}'.format(getattr(arg.strip(), 'title'), arg))


def default_endpoints(duration_days=1):
    """
    Supplies the default start and end datetime objects in absence
    of user supplied endpoints which frames time period from which
    to begin and end retrieving spot price data from Amazon APIs.

    Returns:  TYPE: tuple, containing:
        - start (datetime), midnight yesterday
        - end (datetime) midnight, current day

    """
    # end datetime calcs
    dt_date = datetime.datetime.today().date()
    dt_time = datetime.datetime.min.time()
    end = datetime.datetime.combine(dt_date, dt_time)

    # start datetime calcs
    duration = datetime.timedelta(days=duration_days)
    start = end - duration
    return start, end


def help_menu():
    """Print help menu options"""
    print(menu_body)


def local_awsregion(profile):
    """Determines AWS region code local to user"""
    if os.environ.get('AWS_DEFAULT_REGION'):
        return os.environ['AWS_DEFAULT_REGION']
    cmd = 'aws configure get {}.region'.format(profile)
    return subprocess.getoutput(cmd).strip()


def source_environment(env_variable):
    """
    Sources all environment variables
    """
    return {
        'duration_days': read_env_variable('default_duration'),
        'page_size': read_env_variable('page_size', 500),
        'bucket': read_env_variable('S3_BUCKET', None)
    }.get(env_variable, None)


def modules_location():
    """Filsystem location of Python3 modules"""
    return os.path.split(os.path.abspath(__file__))[0]


def options(parser, help_menu=False):
    """
    Summary:
        parse cli parameter options

    Returns:
        TYPE: argparse object, parser argument set

    """
    # default datetime objects when no custom datetimes supplied
    start_dt, end_dt = default_endpoints()

    parser.add_argument("-C", "--configure", dest='configure', action='store_true', required=False)
    parser.add_argument("-d", "--debug", dest='debug', action='store_true', default=False, required=False)
    parser.add_argument("-e", "--end", dest='end', nargs=1, default=end_dt, required=False)
    parser.add_argument("-h", "--help", dest='help', action='store_true', required=False)
    parser.add_argument("-p", "--profile", dest='profile', nargs=1, default='default', required=False)
    parser.add_argument("-r", "--region", dest='region', nargs='*', default=[], required=False)
    parser.add_argument("-D", "--duration-days", dest='duration', nargs='*', default=None, required=False)
    parser.add_argument("-s", "--start", dest='start', nargs=1, default=start_dt, required=False)
    parser.add_argument("-V", "--version", dest='version', action='store_true', required=False)
    return parser.parse_known_args()


def package_version():
    """
    Prints package version and requisite PACKAGE info
    """
    print(about.about_object)
    sys.exit(exit_codes['EX_OK']['Code'])


def precheck(debug, region):
    """
    Runtime Dependency Checks: postinstall artifacts, environment
    """
    if region == 'noregion':
        return False
    return True

    try:

        home_dir = os.expanduser('~')
        config_file = os.path.join(home_dir, '.spotlib.json')

        if os.path.exists(config_file):
            with open(config_file, 'r') as f1:
                defaults = json.loads(f1.read())
        else:
            from spotlib.defaults import defaults

        _debug_output(home_dir, config_file)

    except OSError:
        fx = inspect.stack()[0][3]
        logger.exception('{}: Problem installing user config files. Exit'.format(fx))
        return False
    return defaults


def writeout_data(key, jsonobject, filename):
    """
        Persists json data to local filesystem

    Returns:
        Success | Failure, TYPE: bool

    """
    tab = '\t'.expandtabs(13)

    if export_iterobject({key: jsonobject}, filename):
        success = f'Wrote {bbl + filename + rst}\n{tab}successfully to local filesystem.'
        if isinstance(jsonobject, list):
            qty = bd + str(len(jsonobject)) + rst
            ancillary_msg = f'\n{tab}{qty} unique instance types utilised for spot in region.'
        stdout_message(success + ancillary_msg, prefix='OK')
        return True
    else:
        failure = f'Problem writing {bbl + filename + rst} to local filesystem.'
        stdout_message(failure, prefix='WARN')
        return False


def writeout_status(key, region, filename, finished):
    """Display current status message to user"""
    fregion = fs + region + '/' + rst       # formatted region
    ffname = bbl + filename + rst              # formtted filename
    tab = '\t'.expandtabs(13)
    success = f'Wrote {fregion + ffname}\n{tab}successfully to local filesystem'
    failure = f'Problem writing {key} to local filesystem.'
    stdout_message(success, prefix='OK') if finished else stdout_message(failure, prefix='WARN')


def init():
    """
    Initialize spot price operations; process command line parameters
    """
    parser = argparse.ArgumentParser(add_help=False)

    try:

        args, unknown = options(parser)

    except Exception as e:
        help_menu()
        stdout_message(str(e), 'ERROR')
        sys.exit(exit_codes['EX_BADARG']['Code'])

    if len(sys.argv) == 1 or args.help:
        help_menu()
        sys.exit(exit_codes['EX_OK']['Code'])

    elif args.version:
        package_version()

    elif (args.start and args.end) or args.duration:
        args.profile = args.profile[0] if isinstance(args.profile, list) else args.profile

        # set local region
        args.region = [local_awsregion(args.profile)] if not args.region else args.region

        # validate prerun conditions
        defaults = precheck(args.debug, args.region)

        sp = SpotPrices(profile=args.profile)

        if args.duration and isinstance(int(args.duration[0]), int):
            start, end = sp.set_endpoints(duration=int(args.duration[0]))
        else:
            start, end = sp.set_endpoints(args.start[0], args.end[0])

        # global container for ec2 instance size types
        instance_sizes = []

        for region in args.region:

            fname = '_'.join(
                        [
                            start.strftime('%Y-%m-%dT%H:%M:%SZ'),
                            end.strftime('%Y-%m-%dT%H:%M:%SZ'),
                            'all-instance-spot-prices.json'
                        ]
                    )

            prices = sp.generate_pricedata(regions=[region])

            # conversion of datetime obj => utc strings
            uc = UtcConversion(prices)

            # write to file on local filesystem
            key = os.path.join(region, fname)
            os.makedirs(region) if not os.path.exists(region) else True
            _completed = export_iterobject(prices, key)

            # user status message
            writeout_status(key, region, fname, _completed)

            # build unique collection of instances for this region
            regional_sizes = list(set([x['InstanceType'] for x in prices['SpotPriceHistory']]))
            instance_sizes.extend(regional_sizes)

        # instance sizes across analyzed regions
        instance_sizes = list(set(instance_sizes))
        instance_sizes.sort()
        key = 'instanceTypes'
        date = sp.end.strftime("%Y-%m-%d")
        return writeout_data(key, instance_sizes, date + '_spot-instanceTypes.json')

    else:
        stdout_message(
            'Dependency check fail %s' % json.dumps(args, indent=4),
            prefix='AUTH',
            severity='WARNING'
            )
        sys.exit(exit_codes['EX_DEPENDENCY']['Code'])

    failure = """ : Check of runtime parameters failed for unknown reason.
    Please ensure you have both read and write access to local filesystem. """
    logger.warning(failure + 'Exit. Code: %s' % sys.exit(exit_codes['EX_MISC']['Code']))
    print(failure)
    return sys.exit(exit_codes['EX_BADARG']['Code'])
