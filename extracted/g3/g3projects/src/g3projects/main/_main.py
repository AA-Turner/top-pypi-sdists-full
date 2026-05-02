import argparse
import logging

from ..logical import generate_logical_files
from ..physical import generate_physical_files


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            'Create a G3 Project PLC files from a SystemConfig.json file.'
            )
        )
    parser.add_argument(
        'system_config',
        type=str,
        help='Path to the SystemConfig.json file'
        )
    parser.add_argument(
        '--gen-physical',
        required=False,
        action='store_true',
        help=(
            'Generate physical files only. If both --gen-physical and '
            '--gen-logical are provided or neither are provided, both '
            'physical and logical files will be generated.'
            )
        )
    parser.add_argument(
        '--gen-logical',
        required=False,
        action='store_true',
        help=(
            'Generate logical files only. If both --gen-logical and '
            '--gen-physical are provided or neither are provided, both '
            'logical and physical files will be generated.'
            )
        )
    parser.add_argument(
        '--gen-test',
        required=False,
        action='store_true',
        help=(
            'Generate test devices in logical files. Such devices act as '
            'digital twins for testing purposes and are directly connected '
            'to the control devices. This option requires --gen-logical.'
            )
        )
    parser.add_argument(
        "--ftp1-pswd-hash",
        type=str,
        required=True,
        help="'ftp' user password hash for PLC FTP server",
        )
    parser.add_argument(
        "--ftp2-pswd-hash",
        type=str,
        required=True,
        help="'ellmaster' user password hash for PLC FTP server",
        )
    parser.add_argument(
        "--sfdomain_pswd_hash",
        type=str,
        required=True,
        help="SafeDomain password hash",
        )
    parser.add_argument(
        '--log-level',
        type=str,
        required=False,
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help='Set the logging level.'
        )
    args = parser.parse_args()
    if not args.gen_physical and not args.gen_logical:
        args.gen_physical = True
        args.gen_logical = True
    if not args.gen_logical and args.gen_test:
        parser.error('--gen-test requires --gen-logical')
    return args


def generate_project_files(
    system_config_path: str,
    gen_physical: bool = True,
    gen_logical: bool = True,
    gen_test: bool = False,
    ftp1_pswd_hash: str = '',
    ftp2_pswd_hash: str = '',
    sfdomain_pswd_hash: str = ''
) -> None:
    if gen_logical:
        generate_logical_files(system_config_path, gen_test)
    if gen_physical:
        generate_physical_files(system_config_path, ftp1_pswd_hash, ftp2_pswd_hash, sfdomain_pswd_hash)


def main() -> None:
    args = parse_arguments()
    logging.basicConfig(
        level=args.log_level,
        format='[%(name)s] %(levelname)s:%(message)s'
        )
    generate_project_files(
        args.system_config, args.gen_physical, args.gen_logical, args.gen_test, args.ftp1_pswd_hash, args.ftp2_pswd_hash, args.sfdomain_pswd_hash
        )
