"""

Help Menu

    Help menu object containing body of help content.
    For printing with formatting

"""

from spotlib.statics import PACKAGE, PACKAGE_CLI
from spotlib.variables import c, bbc, bdwt, bdcy, rst


ACCENT = c.ORANGE               # orange accent highlight color
bdacct = c.ORANGE + c.BOLD      # bold orange
lbrct = bbc + ' [ ' + rst        # left bracket
rbrct = bbc + ' ] ' + rst        # right bracket
vdiv = bbc + ' | ' + rst
tab = '\t'.expandtabs(24)

menu_title = '\n' + bdwt + tab + PACKAGE_CLI + rst + ' command help'

synopsis_cmd = (
        ACCENT + 'spotcli' + rst + ' --start <value> ' + '--end <value>' + vdiv +
        '--duration-days'
    )

url_doc = c.URL + 'http://spotlib.readthedocs.io' + rst
url_sc = c.URL + 'https://github.com/fstab50/spotlib' + rst


menu_body = menu_title + bdwt + """

  DESCRIPTION""" + rst + """

            Command line interface to """ + PACKAGE + """ to retrieve Amazon
            EC2 Spot Instance Pricing and associated metadata.

            Source Code Repo: """ + url_sc + """
    """ + bdwt + """
  SYNOPSIS""" + rst + """

        $ """ + synopsis_cmd + """

                        -r, --region <value>
                       [-s, --start  <value>  ]
                       [-e, --end    <value>  ]
                       [-d, --duration-days   <value>  ]
                       [-p, --profile  <value>  ]
                       [-d, --debug    ]
                       [-h, --help     ]
                       [-V, --version  ]
    """ + bdwt + """
  OPTIONS
    """ + bdwt + """
        -D, --duration-days""" + rst + """ <value>: Number of days of price data
            history to retrieve ending at midnight on present day.
    """ + bdwt + """
        -d, --debug""" + rst + """:  Print out additional  debugging information
    """ + bdwt + """
        -s, --start""" + rst + """ <value>:  Datetime of start of price sampling
            period (example: 2019-09-03T00:00:00). See --end.
    """ + bdwt + """
        -e, --end""" + rst + """ <value>:  Datetime of end of the price sampling
            period (example: 2019-09-04T23:59:59). See --start.
    """ + bdwt + """
        -h, --help""" + rst + """: Show this help message, symbol legend, & exit
    """ + bdwt + """
        -p, --profile""" + rst + """: Access the AWS api using specified profile
            from the local awscli configuration.
    """ + bdwt + """
        -r, --region""" + rst + """:  AWS region code (e.g. us-east-1) for which
            you wish to retrieve EC2 spot price data.
    """ + bdwt + """
        -V, --version""" + rst + """: Print version, license, and copyright info
    """
