#!/usr/bin/env python3
import readline


def historyLength():
    """get current length of history"""
    return readline.get_current_history_length()


def getHistory(lineNumbers=False, n=None, newLine="\n"):
    """Get History

    Method that allows one to get the (whole) history of currently used Python shell

    Args:
        lineNumbers (bool): print line numbers in history? (default: `False`)
        n (int): number of latest history entries to show (default: `None`)
        newLine (str): which new line character(s) should be used on join of the history? (default: `\\n`)
    """
    historyItemCount = historyLength()
    if n == None or n > historyItemCount:
        n = historyItemCount

    if lineNumbers:
        preWidth = len(str(n))
        formatstring = f"{{0:{preWidth}d}}" + " " * 2 + "{1!s}"
    else:
        formatstring = "{1!s}"

    start = historyItemCount - n

    result = []
    for i in range(start + 1, start + n + 1):
        result.append(formatstring.format(i - start, readline.get_history_item(i)))

    return newLine.join(result)


def printHistory(lineNumbers=False, n=None, newLine="\n"):
    """Print History

    Method that allows one to print the (whole) history of currently used Python shell

    Args:
        lineNumbers (bool): print line numbers in history? (default: `False`)
        n (int): number of latest history entries to show (default: `None`)
        newLine (str): which new line character(s) should be used on join of the history? (default: `\\n`)
    """
    print(getHistory(lineNumbers, n, newLine))


def saveHistory(filePath, lineNumbers=False, n=None, newLine="\n"):
    """Save History

    Method that allows one to stor the (whole) history of currently used Python shell into a file

    Args:
        filePath (str): path of destination file
        lineNumbers (bool): print line numbers in history? (default: `False`)
        n (int): number of latest history entries to show (default: `None`)
        newLine (str): which new line character(s) should be used on join of the history? (default: `\\n`)
    """
    with open(filePath, "w") as file:
        file.write(getHistory(lineNumbers, n, newLine))
        file.close()
