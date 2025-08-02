"""Pretty printing utilities.

This module provides a pretty printing utility for the IR nodes and other
objects in the compiler.

The pretty printing utility is implemented using the visitor pattern. The
[`Printable`][kirin.print.Printable] class is the base class for all objects that can be pretty printed.

The [`Printer`][kirin.print.Printer] class is the visitor that traverses the object and prints the
object to a string. The [`Printer`][kirin.print.Printer] class provides methods for printing different
types of objects.
"""

from kirin.print.printer import Printer as Printer
from kirin.print.printable import Printable as Printable
