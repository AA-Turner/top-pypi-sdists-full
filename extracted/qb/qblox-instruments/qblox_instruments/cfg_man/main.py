# ----------------------------------------------------------------------------
# Description    : Helper functions for updating using a legacy cfg_man
# Git repository : https://gitlab.com/qblox/packages/software/qblox_instruments.git
# Copyright (C) Qblox BV (2021)
# ----------------------------------------------------------------------------


# -- include -----------------------------------------------------------------

import argparse
import io
import json
import os
import sys
from collections.abc import Iterable
from textwrap import dedent
from typing import BinaryIO, Optional, TextIO, Union

from qblox_instruments.cfg_man import log
from qblox_instruments.cfg_man.const import VERSION
from qblox_instruments.cfg_man.legacy_connection import LegacyConnection
from qblox_instruments.cfg_man.pnp_connection import PnpConnection
from qblox_instruments.cfg_man.probe import (
    ConnectionInfo,
    connection_info_to_json,
    pprint_connection_info,
    probe_device,
    represent_address,
    represent_connection,
    represent_device,
)
from qblox_instruments.cfg_man.scpi_connection import ScpiConnection
from qblox_instruments.cfg_man.update_file import UpdateFile
from qblox_instruments.pnp import CMM_SLOT_INDEX, AddressInfo, PlugAndPlay

# -- class -------------------------------------------------------------------


class ConfigurationManager:
    """
    Class that provides configuration management functionality.
    """

    __slots__ = ["_ci", "_conn"]

    # ------------------------------------------------------------------------
    def __init__(self, identifier: Union[str, AddressInfo, ConnectionInfo]) -> None:
        """
        Creates a configuration management interface object for the given
        device. Use close() when you're done with the object, or a ``with``
        clause::

            with cfg_man(...) as cm:
                # do stuff with cm here
                pass

        .. note::
            Depending on the software running on the device and the
            connectivity to the device, not all features may be available.
            See :meth:`get_protocol()`.

            .. list-table:: Feature availability
                :widths: 25 25 25 25
                :header-rows: 1

                * - Feature
                  - ``scpi``
                  - ``legacy``
                  - ``pnp``
                * - ``set_name``
                  - Yes
                  - No
                  - Yes
                * - ``download_log``
                  - Yes
                  - tgz only
                  - No
                * - ``set_ip_config``
                  - Yes
                  - ``192.168.x.x/24`` only
                  - Yes
                * - ``update``
                  - Yes
                  - Yes
                  - No
                * - ``rollback``
                  - Yes
                  - Yes
                  - No
                * - ``reboot``
                  - Yes
                  - Yes
                  - Yes

            ``scpi`` will be used if available, but:

             - devices running an old software version may not support it, in
               which case ``legacy`` will be used; and
             - if the embedded software version is new enough but the device
               IP configuration is incompatible with your network settings,
               ``pnp`` will be used.

        Parameters
        ----------
        identifier: Union[str, AddressInfo, ConnectionInfo]
            Instrument identifier. See :func:`~qblox_instruments.resolve()`.

        Raises
        ------
        Exception
            If we can't connect.
        """
        super().__init__()

        self._ci = probe_device(identifier)

        if self._ci.protocol == "legacy":
            self._conn = LegacyConnection(self._ci)
        elif self._ci.protocol == "scpi":
            self._conn = ScpiConnection(self._ci)
        elif self._ci.protocol == "pnp":
            self._conn = PnpConnection(self._ci)
        else:
            assert False

    # ------------------------------------------------------------------------
    def close(self) -> None:
        """
        Closes the underlying connection. The object must not be used anymore
        after this call.
        """
        if hasattr(self, "_conn") and self._conn is not None:
            self._conn.close()
            self._conn = None

    # ------------------------------------------------------------------------
    def __del__(self) -> None:
        self.close()

    # ------------------------------------------------------------------------
    def __enter__(self) -> "ConfigurationManager":
        return self

    # ------------------------------------------------------------------------
    def __exit__(self, exc_type, exc_value, traceback) -> Optional[bool]:
        self.close()

    # ------------------------------------------------------------------------
    def get_connection_info(self) -> ConnectionInfo:
        """
        Returns the connection information object.

        Returns
        -------
        ConnectionInfo
            The connection information object.
        """
        return self._ci

    # ------------------------------------------------------------------------
    def get_protocol(self) -> str:
        """
        Returns the protocol used for this connection.

        Returns
        -------
        str
            The protocol, either ``"scpi"``, ``"legacy"``, or ``"pnp"``.
        """
        return self._ci.protocol

    # ------------------------------------------------------------------------
    def has_capability(self, cmd: str) -> bool:
        """
        Returns whether our connection type supports the given command.

        Parameters
        ----------
        cmd: str
            The command name.

        Returns
        -------
        bool
            Whether the command is supported. Note that some commands are only
            partially supported; in this case, this still reports True.
        """
        return hasattr(self._conn, cmd) and not self._ci.device.is_extended_instrument

    # ------------------------------------------------------------------------
    def _check_capability(self, cmd: str) -> None:
        """
        Raises a NotImplementedError if the given command is not supported by
        our connection type.

        Parameters
        ----------
        cmd: str
            The command name.

        Raises
        ------
        NotImplementedError
            If the given command is not supported by our connection type.
        """
        if not self.has_capability(cmd):
            raise NotImplementedError(
                f"{cmd}() is not implemented for {self._ci.protocol} connections"
            )

    # ------------------------------------------------------------------------
    def describe(self, as_json: bool = False) -> None:
        """
        Prints information about the device being connected to stdout.

        Parameters
        ----------
        as_json: bool
            If set to True, the structure is dumped in a machine-friendly
            JSON format rather than a pretty-printed table.
        """
        if as_json:
            print(json.dumps(connection_info_to_json(self._ci), indent=4))
        else:
            pprint_connection_info(self._ci, print)
            print()

    # ------------------------------------------------------------------------
    def download_log(
        self,
        source: str = "app",
        fmt: Union[str, int] = "tail",
        file: Union[str, BinaryIO, TextIO] = sys.stdout,
        tail: int = 100,
    ) -> None:
        """
        Downloads log data from the device.

        Parameters
        ----------
        source: str
            The log source. Currently this must be ``"app"`` (default),
            ``"system"``, or ``"cfg_man"``, or the device will return an
            error.

        fmt: Union[str, int]
            File format:

             - If ``"tail"`` (default): return the latest <tail> messages in
               plaintext.
             - If a positive integer: return the latest <fmt> messages in
               plaintext.
             - If ``"txt"`` or zero: return the log file currently in rotation
               in plaintext.
             - If ``"tgz"`` or a negative integer: return all log files in
               rotation in a tar.gz archive.

        file: Union[str, BinaryIO, TextIO]
            The file object to write to. For textual formats, the file may be
            opened in either binary or unicode mode (in the latter case, the
            contents will be buffered in memory first); for tgz, it must be
            open in binary mode. If a string, this is a pattern for the
            filename to write to; the file will be opened internally. The
            following substitutions are made for convenience:

             - ``%s`` -> device serial number;
             - ``%n`` -> device name (be careful, device names are not
               necessarily valid filenames);
             - ``%i`` -> address of the device we're connecting to (usually
               IP+port, but will be the serial number when this is a
               plug & play connection).

        tail: int
            If fmt is ``"tail"``, this specifies the number of lines returned.
            Unused otherwise.

        Raises
        ------
        NotImplementedError
            If the underlying protocol we're connecting with does not support
            this command.
        Exception
            If the command failed.
        """
        self._check_capability("download_log")

        # Convert format mnemonics to integers.
        if not isinstance(fmt, int):
            fmt = {"tail": tail, "txt": 0, "tgz": -1}.get(fmt)
            if fmt is None:
                raise ValueError(f"invalid log format {fmt!r}")

        # Handle the different options for file.
        if isinstance(file, str):
            fname = file.replace(
                "%s",
                (self._ci.device.serial if self._ci.device.serial is not None else "unknown"),
            )
            fname = fname.replace("%n", self._ci.device.name)
            fname = fname.replace("%i", represent_address(self._ci))
            with open(fname, "wb") as f:
                return self._conn.download_log(source, fmt, f)

        elif isinstance(file, io.TextIOBase):
            # Buffer in memory; download_log may write in chunks not aligned
            # to UTF-8 boundaries.
            with io.BytesIO() as bin_file:
                self._conn.download_log(source, fmt, bin_file)
                bin_file.seek(0)
                file.write(bin_file.read().decode("utf-8", errors="ignore"))

        else:
            self._conn.download_log(source, fmt, file)

    # ------------------------------------------------------------------------
    def set_name(self, name: str) -> None:
        """
        Renames the device. The name change will be processed immediately.

        Parameters
        ----------
        name: str
            The new name. Names may not contain newlines, backslashes, or
            double-quotes.

        Raises
        ------
        NotImplementedError
            If the underlying protocol we're connecting with does not support
            this command.
        Exception
            If the command failed.
        """
        self._check_capability("set_name")

        if "\n" in name or "\\" in name or '"' in name:
            raise ValueError("Device names may not include newlines, backslashes, or double-quotes")
        return self._conn.set_name(name)

    # ------------------------------------------------------------------------
    def set_ip_config(self, config: str) -> None:
        """
        Reconfigures the IP configuration of the device. Changes will only go
        into effect after the device is rebooted.

        .. note::
            If this is a plug & play connection, this will also reboot the
            device immediately.

        Parameters
        ----------
        config: str
            The IP configuration. Must be one of:

             - a static IPv4 address including prefix length;
             - a static IPv6 address including prefix length;
             - "dhcp" to get an IPv4 address via DHCP;
             - a combination of an IPv4 and IPv6 configuration separated by
               a semicolon.

        Raises
        ------
        NotImplementedError
            If the underlying protocol we're connecting with does not support
            this command.
        Exception
            If the command failed.
        """
        self._check_capability("set_ip_config")
        self._conn.set_ip_config(config)

    # ------------------------------------------------------------------------
    def update(
        self,
        package: Union[str, UpdateFile],
        included_slots: Union[None, Iterable[int]] = None,
        excluded_slots: Union[None, Iterable[int]] = None,
    ) -> None:
        """
        Updates the device with the given update file. The changes will only
        go into effect once the device is rebooted.

        Parameters
        ----------
        package: Union[str, UpdateFile]
            The update package.

        Raises
        ------
        NotImplementedError
            If the underlying protocol we're connecting with does not support
            this command.
        Exception
            If the command failed.
        """
        self._check_capability("update")

        if isinstance(package, str):
            package = UpdateFile(package)
        with package.load(self._ci, included_slots, excluded_slots) as file:
            return self._conn.update(file, included_slots, excluded_slots)

    # ------------------------------------------------------------------------
    def rollback(self) -> None:
        """
        Instructs the device to attempt a rollback to the previous version. The
        changes will only go into effect once the device is rebooted.

        Raises
        ------
        NotImplementedError
            If the underlying protocol we're connecting with does not support
            this command.
        Exception
            If the command failed.
        """
        self._check_capability("rollback")
        self._conn.rollback()

    # ------------------------------------------------------------------------
    def reboot(self) -> None:
        """
        Instructs the device to reboot.

        Raises
        ------
        NotImplementedError
            If the underlying protocol we're connecting with does not support
            this command.
        Exception
            If the command failed.
        """
        self._check_capability("reboot")
        self._conn.reboot()

    # ------------------------------------------------------------------------
    @staticmethod
    def cmd_line(*args: Iterable[str]) -> None:
        """
        Runs the configuration manager with the given command-line arguments.

        Parameters
        ----------
        *args: Iterable[str]
            The command-line arguments.

        Raises
        ------
        RuntimeError
            If the command-line tool returns a nonzero exit status.
        """

        # This version is intended to be called from within a script or
        # notebook, so catch sys.exit() calls, and enable tracebacks.
        code = 0
        try:
            _main(*args)
        except SystemExit as e:
            code = e.code
        if code != 0:
            raise RuntimeError(f"exit with status {code}")


# -- command-line tool -------------------------------------------------------


def _main(args: Union[None, Iterable[str]] = None) -> None:
    """
    Runs the configuration manager.

    Parameters
    ----------
    args: Union[None, Iterable[str]]
        When None, this will run the configuration manager as if called from
        the command line. Arguments are taken from ``sys.argv``, and
        ``sys.exit()`` is called when complete. When this is an iterable of
        strings, these strings are interpreted as ``sys.argv[1:]``, exceptions
        will never be caught, and the logging module won't be (re)configured.
    """

    def strictly_positive_int(x) -> int:
        x = int(x)
        if x < 1:
            raise ValueError("value must be positive")
        return x

    def positive_int(x) -> int:
        x = int(x)
        if x < 0:
            raise ValueError("value must be positive")
        return x

    title = f"Qblox Configuration Manager version {'.'.join(map(str, VERSION))}"

    if args is not None:
        usage = "cfg_man.main([options], <device>, [commands...])"
    else:
        usage = f"{os.path.basename(sys.argv[0])} [options] <device> [commands...]"

    description = dedent(
        f"""
    {title}

    <device> must be one of the following, resolved in the given order (use
    ip:// or pnp:// prefixes to disambiguate if necessary):
      all                   Apply commands to all devices on the network,
                            discovered via plug & play.
      [ip://]<ip-address>   Connect to the device at the given IP address.
      [pnp://]<name>        A customer-specified device name, resolved via
                            plug & play.
      [pnp://]<serial>      A device serial number, resolved via plug & play.
      [ip://]<hostname>     A hostname, resolved via DNS.
      <...>/<slot>          For clusters, access (only) the given slot where
                            applicable. 0 selects the CMM, 1-20 selects one of
                            the module slots. <...> can be any of the above
                            except "all".

    [commands...] can be a sequence of the following, executed sequentially
                  for each device (commands marked with an * are not available
                   for "all"):
      describe              Describe the device(s) and the qblox-cfg connection
                            to it/them in a human-readable way on stdout. Add
                            -j/--json to print in a machine-readable JSON
                            format instead. If multiple devices are queried, a
                            different table/JSON object will be printed for
                            each.
    * set-name <name>       Rename the device.
      sys-log               Download the system log. one of -g, -x, or -l must
                            be specified to set the format. See also -f.
      app-log               Download the application log, same as sys-log
                            otherwise.
      cfg-log               Download the configuration manager log, same as
                            sys-log otherwise.
    * set-ip <192.168.x.y>  Configure the device to use the given static IPv4
                            address with subnet 192.168.x.255 (prefix length
                            24).
    * set-ip <172.x.y.z>    Configure the device to use the given static IPv4
                            address with subnet 172.x.255.255 (prefix length
                            16).
    * set-ip <10.x.y.z>     Configure the device to use the given static IPv4
                            address with subnet 10.255.255.255 (prefix length
                            8).
    * set-ip <ipv4>/<pre>   Configure the device to use the given static IPv4
                            address and custom prefix length.
      set-ip dhcp           Configure the device(s) to determine their IPv4
                            address via DHCP.
    * set-ip <ipv6>/<pre>   Configure the device to use the given static IPv6
                            address and custom prefix length. Can be combined
                            with any of the IPv4 options above using a comma
                            as separator, for example "dhcp,1:2::3:4/64".
      update <fname>        Updates the device(s) with the given update
                            package.
      rollback              Rolls back the device(s) to their previous version
                            if possible.
      reboot                Reboots the device(s). This is implicit when
                            set-ip, update, or rollback are in the sequence.
                            It must be the last entry in the sequence if
                            used.
    """
    )

    epilog = dedent(
        """
    Regardless of whether a command is specified, information gathered about
    the connection and device will be logged with "info" level. Use -v to make
    it visible, or read the log file that's generated
    (unless you specified -n).
    """
    )

    parser = argparse.ArgumentParser(
        description=description,
        usage=usage,
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "identifier",
        metavar="<device>",
        nargs="?",
        help=("Configures which device to connect to. Various formats are allowed; see above."),
    )
    parser.add_argument(
        "commands",
        metavar="[command]",
        nargs="*",
        help=("List of commands to execute. Various patterns are allowed; see above."),
    )
    parser.add_argument(
        "-V",
        "--version",
        action="store_true",
        help="Only print the version, then exit.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Increase verbosity to info, or debug if given twice.",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="count",
        default=0,
        help=("Reduce verbosity to errors, or don't print anything if given twice."),
    )
    parser.add_argument(
        "-t",
        "--tee",
        metavar="<fname>",
        action="store",
        default="cfg_man_client.log",
        help=(
            "In addition to the terminal, also log to the given file with at "
            'least info level. Defaults to "cfg_man_client.log".'
        ),
    )
    parser.add_argument(
        "-r",
        "--traceback",
        action="store_true",
        help=("Don't catch Python exceptions, so the full traceback is shown on error."),
    )
    parser.add_argument(
        "-n",
        "--no-tee",
        action="store_true",
        help="Don't write a log file; only print to the terminal.",
    )
    parser.add_argument(
        "-g",
        "--log-tgz",
        action="store_true",
        help=("For log retrieval commands, retrieve all available data as tar.gz archive."),
    )
    parser.add_argument(
        "-x",
        "--log-txt",
        action="store_true",
        help=(
            "For log retrieval commands, retrieve the contents of the "
            "current log file in rotation in plaintext."
        ),
    )
    parser.add_argument(
        "-l",
        "--log-tail",
        metavar="<N>",
        action="store",
        type=strictly_positive_int,
        default=None,
        help=("For log retrieval commands, retrieve the latest <N> messages in plaintext."),
    )
    parser.add_argument(
        "-f",
        "--log-fname",
        metavar="<pat>",
        action="store",
        default="%s-%x.%f",
        help=(
            "For log retrieval commands, sets the pattern for the output "
            "filenames. %%s is replaced with the serial number, %%n with the "
            "name (will fail if device names are not valid filenames, use "
            "with caution!), %%i with the IP address, %%x with the log type "
            "(sys, app, or cfg), and %%f with the format extension (txt or "
            'tgz). Defaults to "%%s-%%x.%%f".'
        ),
    )
    parser.add_argument(
        "-j",
        "--json",
        action="store_true",
        help=(
            "For the describe command, print the connection/device description "
            "using machine-readable JSON rather than a human-readable table."
        ),
    )
    slot_selection_group = parser.add_mutually_exclusive_group()
    slot_selection_group.add_argument(
        "-e",
        "--exclude_slots",
        metavar="<slot#>",
        nargs="+",
        type=positive_int,
        help=(
            "For the update command, exclude a set of slots even when they are disabled / shut-down"
        ),
    )
    slot_selection_group.add_argument(
        "-i",
        "--include_slots",
        metavar="<slot#>",
        nargs="+",
        type=positive_int,
        help="For the update command, only update the given slots",
    )
    parser.add_argument(
        "-y",
        "--yes",
        action="store_true",
        help='Batch mode: automatically respond "yes" to all queries.',
    )
    parser.add_argument(
        "-k",
        "--keep-going",
        action="store_true",
        help=(
            "If there is a problem executing the commands for one of the "
            "devices, continue processing the other devices anyway."
        ),
    )

    if args is not None:
        args = parser.parse_args(args)
        from_script = True
    else:
        args = parser.parse_args()
        from_script = False

    def query_user(message: str) -> None:
        """
        Queries the user whether they want to continue.

        Parameters
        ----------
        message: str
            Message printed to indicate the questionable condition.

        Raises
        ------
        KeyboardInterrupt
            If the user cancelled the operation.
        """
        if args.yes:
            log.warn("%s", message)
            log.warn("Assuming that's okay (-y is active).")
        else:
            log.always("%s", message)
            log.always("Do you want to continue? [Y/N]")
            response = input()
            while response not in "yYnN":
                response = input("Please enter Y or N. ")
            if response in "nN":
                raise KeyboardInterrupt

    # Handle exceptions thrown in the program.
    try:
        # Track whether we should fail at the end. We usually fail immediately
        # when something goes wrong, but -k/args.keep_going overrides this.
        failed = False

        # Print version and exit if requested.
        if args.version:
            print(".".join(map(str, VERSION)))
            sys.exit(0)

        # If no device identifier is specified, show help.
        if args.identifier is None:
            parser.print_help()
            sys.exit(2)
        identifier = args.identifier

        # Configure logging, unless we're called from within a script.
        if not from_script:
            log.configure(args.verbose - args.quiet, None if args.no_tee else args.tee)

        # Print header in the logfile.
        log.note("")
        log.note("--- %s ---", title)
        log.note("")

        # Print the argument list as parsed by argparse.
        log.debug("Called with arguments:")
        for name, value in vars(args).items():
            log.debug("%s", f"  {name:<25}: {value}")
        log.debug("")

        # Parse the command list.
        address_all = identifier == "all"
        command_list = []
        commands_used = {}
        making_changes = False
        try:
            it = iter(args.commands)
            while True:
                # Get command name.
                try:
                    cmd = next(it)
                except StopIteration:
                    break

                # Make sure no commands follow a reboot.
                if "reboot" in commands_used:
                    raise ValueError("Cannot queue commands after reboot")

                # Handle the available command types.
                reuse_key = cmd
                if cmd == "describe":
                    # Print information about device(s).
                    command_list.append(("describe", [], {"as_json": args.json}))

                elif cmd == "set-name":
                    # Name configuration command.
                    if address_all:
                        raise ValueError('set-name command cannot be combined with "all"')
                    name = next(it)
                    if "\n" in name or "\\" in name or '"' in name:
                        raise ValueError(
                            "Device names may not include newlines, backslashes, or double-quotes"
                        )
                    command_list.append(("set_name", [name], {}))
                    making_changes = True

                elif cmd.endswith("-log"):
                    # Log download command. These don't conflict with anything.
                    reuse_key = None

                    # Expand filename pattern (for as far as the configuration
                    # manager class doesn't do it).
                    log_fname = args.log_fname

                    # Determine log source.
                    log_type = cmd.rsplit("-", maxsplit=1)[0]
                    log_fname = log_fname.replace("%x", log_type)
                    source = {"app": "app", "sys": "system", "cfg": "cfg_man"}.get(log_type)
                    if source is None:
                        raise ValueError(f'Unknown log type "{log_type}"')

                    # Determine file format.
                    if args.log_tgz:
                        fmt = -1
                        log_fname = log_fname.replace("%f", "tgz")
                    elif args.log_txt:
                        fmt = 0
                        log_fname = log_fname.replace("%f", "txt")
                    elif args.log_tail is not None:
                        fmt = args.log_tail
                        log_fname = log_fname.replace("%f", "txt")
                    else:
                        raise ValueError("Missing log format option")

                    # Queue command.
                    command_list.append(("download_log", [source, fmt, log_fname], {}))

                elif cmd == "set-ip":
                    # IP configuration command.
                    config = next(it)

                    # Don't allow users to set all devices to the same static
                    # IP address...
                    if config != "dhcp" and address_all:
                        raise ValueError('set-ip command cannot be combined with "all"')

                    # Do some desugaring of the IP addresses, since I'm
                    # betting most people don't know what a "prefix length"
                    # is. Also use commas for separation on the command line,
                    # since semicolons are a PITA.
                    configs = config.split(",")
                    for i in range(len(configs)):
                        if configs[i] == "dhcp":
                            continue
                        if "/" not in configs[i]:
                            if configs[i].startswith("192.168."):
                                configs[i] += "/24"
                            elif configs[i].startswith("172."):
                                configs[i] += "/16"
                            elif configs[i].startswith("10."):
                                configs[i] += "/8"
                            else:
                                raise ValueError(f"Missing prefix length for {configs[i]}")

                    # There's certainly potential for more error checking here,
                    # but just leave that to the device.
                    config = ";".join(configs)
                    command_list.append(("set_ip_config", [config], {}))
                    making_changes = True

                elif cmd == "update":
                    # Update command.
                    command_list.append(
                        (
                            "update",
                            [next(it)],
                            {
                                "included_slots": args.include_slots,
                                "excluded_slots": args.exclude_slots,
                            },
                        )
                    )
                    making_changes = True

                elif cmd == "rollback":
                    # Rollback command. Conflicts with update and vice-versa,
                    # so use update as the command reuse checking key.
                    reuse_key = "update"
                    command_list.append(("rollback", [], {}))
                    making_changes = True

                elif cmd == "reboot":
                    # Reboot command.
                    command_list.append(("reboot", [], {}))

                else:
                    raise ValueError(f'Unsupported command "{cmd}"')

                # Most commands cannot be reused, or conflict with other
                # commands. Check for that.
                if reuse_key is not None:
                    if reuse_key in commands_used:
                        raise ValueError(
                            f"{cmd} command conflicts with earlier "
                            f"{commands_used[reuse_key]} command"
                        )
                    commands_used[reuse_key] = cmd

        except StopIteration:
            raise ValueError("Unexpected end of command list")

        # Append reboot command implicitly if needed.
        if "set-ip" in commands_used and "reboot" not in commands_used:
            command_list.append(("reboot", (), {}))

        if "update" in commands_used and "reboot" not in commands_used:
            if (
                # Included slots are already rebooted by CMM and CMM itself isn't included in update
                args.include_slots is not None and CMM_SLOT_INDEX not in args.include_slots
            ) or (
                # OR CMM is excluded from update, so do not reboot whole cluster
                args.exclude_slots is not None and CMM_SLOT_INDEX in args.exclude_slots
            ):
                pass

            elif (
                (
                    # CMM is also updated so just reboot everything
                    args.include_slots is not None and CMM_SLOT_INDEX in args.include_slots
                )
                or (
                    # OR CMM is not excluded from update, so reboot everything
                    args.exclude_slots is not None and CMM_SLOT_INDEX not in args.exclude_slots
                )
                or (
                    # OR A standard whole-cluster update happens
                    args.include_slots is None and args.exclude_slots is None
                )
            ):
                command_list.append(("reboot", (), {}))

        # If we have an update command, open the file and print information
        # about it.
        update_file_inst = None
        for cmd, cmd_args, cmd_kwargs in command_list:
            if cmd == "update":
                log.note('Parsing update file "%s"...', cmd_args[0])
                update_file_inst = UpdateFile(cmd_args[0])
                log.note("Found %s", update_file_inst.summarize())
                update_file_inst.pprint(lambda msg: log.info(f"  {msg}"))
                log.note("")
                confirm = update_file_inst.needs_confirmation()
                if confirm is not None:
                    query_user(confirm)
                cmd_args[0] = update_file_inst

        # Perform plug & play discovery to get a list of all devices if
        # requested.
        if address_all:
            log.note("Performing plug & play discovery...")
            with PlugAndPlay() as p:
                identifiers = list(p.list_devices())
            if not identifiers:
                raise RuntimeError("Failed to find any devices via plug & play")
            elif len(identifiers) == 1:
                log.note("Discovered 1 device.")
            else:
                log.note("Discovered %d devices.", len(identifiers))
            log.note("")
        else:
            identifiers = [identifier]

        # Configure all connections.
        connections = []
        for identifier in identifiers:
            log.note(f'Trying to connect to "{identifier}"...')
            try:
                ci = probe_device(identifier)
                log.note(f'"{identifier}" is reachable via {represent_connection(ci)}')
                pprint_connection_info(ci, lambda msg: log.info(f"  {msg}"))
                log.note("")
                connections.append(ci)
            except Exception as e:
                if args.keep_going:
                    log.error(f"{type(e).__name__}: {e!s}")
                    log.warn("Failed to connect, but --keep-going is active. Will fail at the end.")
                    failed = True
                else:
                    raise

        # If we have nothing to do at this point, exit.
        if not command_list or not connections:
            log.note("Nothing left to do.")
            if failed:
                log.error("Failing with nonzero exit status due to earlier errors.")
                sys.exit(1)
            else:
                sys.exit(0)

        # Print what we're about to do, and ask for confirmation if we're
        # making any persistent changes.
        printer = log.note if args.yes or not making_changes else log.always
        printer("Operations to be performed:")
        for cmd, cmd_args, cmd_kwargs in command_list:
            arg_strs = [repr(arg) for arg in cmd_args]
            arg_strs += [f"{key}={value!r}" for key, value in cmd_kwargs.items()]
            printer(" - %s(%s)", cmd, ", ".join(arg_strs))
        printer("")
        printer("On the following devices:")
        for ci in connections:
            printer(" - %s", represent_device(ci))
        if not args.no_tee and (args.verbose - args.quiet) < 1:
            printer("")
            printer("More information is available in the log file (%s).", args.tee)
        if making_changes:
            query_user("")
        else:
            printer("")
            printer("No changes are made; proceeding without query.")
        printer("")

        # Execute the commands.
        for ci in connections:
            log.note("Proceeding with %s...", represent_device(ci))
            try:
                cm = ConfigurationManager(ci)
                res = 0
                for cmd, cmd_args, cmd_kwargs in command_list:
                    # If res is a positive integer, skip that many next commands
                    # (e.g. if res == 1 then skip the next command)
                    # Used when calling an invalid update command, i.e. skipping
                    # the only module present.
                    # This will prevent the cluster from rebooting unnecessarily.
                    # Commands are expected to return None with the only exception now being
                    # update() if invalid
                    if res in (None, 0):
                        # Normal command execution
                        log.note("Calling %s on %s...", cmd, represent_address(ci))
                        res = getattr(cm, cmd)(*cmd_args, **cmd_kwargs)
                    else:
                        # Some previous command told us to skip this one
                        log.note("Skipping %s on %s...", cmd, represent_address(ci))
                        res -= 1

                log.note("Done with %s.", represent_address(ci))
            except Exception as e:
                if args.keep_going:
                    log.error(f"{type(e).__name__}: {e!s}")
                    log.warn(
                        "Failed to apply all steps to %s, but --keep-going is "
                        "active. Will fail at the end.",
                        represent_address(ci),
                    )
                    failed = True
                else:
                    raise
            log.note("")

        # Print completion message.
        if failed:
            log.error("Failing with nonzero exit status due to earlier errors.")
        else:
            log.note("Completed successfully.")

    except KeyboardInterrupt:
        log.error("Interrupted")
        pass
    except Exception as e:
        log.error(f"{type(e).__name__}: {e!s}")
        if args.traceback or from_script:
            raise
        sys.exit(1)


# ------------------------------------------------------------------------------


def main(*args: Iterable[str]) -> None:
    """
    Runs the configuration manager with the given command-line arguments.

    Parameters
    ----------
    *args: Iterable[str]
        The command-line arguments.

    Raises
    ------
    RuntimeError
        If the command-line tool returns a nonzero exit status.
    """

    # This version is intended to be called from within a script or notebook,
    # so catch sys.exit() calls, and enable tracebacks.
    code = 0
    try:
        _main(*args)
    except SystemExit as e:
        code = e.code
    if code != 0:
        raise RuntimeError(f"exit with status {code}")


# - main -----------------------------------------------------------------------

if __name__ == "__main__":
    _main()
