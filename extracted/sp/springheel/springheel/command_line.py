import springheel, asyncio

"""Run Springheel command line scripts."""


def cbuild():
    """
    Generate a Springheel site.

    Run with ``--logging`` to enable logging to ``springheel.log``.
    """

    loop = asyncio.get_event_loop()
    task = loop.create_task(springheel.build())
    loop.run_until_complete(task)
    loop.close()


def cinit():
    """Initialize a Springheel project."""

    loop = asyncio.get_event_loop()
    task = loop.create_task(springheel.init())
    loop.run_until_complete(task)
    loop.close()


def cversion():
    """Print version information."""
    springheel.version()


def caddimg():
    """
    Create a .meta file for a new strip.

    Requires Pillow. All parameters are command-line arguments to be
    passed to ``springheel-addimg``.

    Parameters
    ----------
    input : str
        Relative path to the image file in input/. Short: "-i".
    conf : str
        Filename of the .conf file for the strip's category. Short:
        "-c".
    title : str
        The title of the strip. Short: "-t".
    num : str
        The strip's page number. Short: "-n".
    chapter : str, optional
        The chapter number if a strip is part of a chapter. "False" if
        it is not. Short: "-k" (for "Kapitel", as C and H were already
        taken).
    alt : str, optional
        Extra text that displays below the strip. Despite the
        name, is not really used as alt text. A more accessible
        version of the title text some comics have. Short: "-a".
    source : str, optional
        If not empty, the URL of an original work on which this strip is
        based. For translations, freely-licensed comics, etc. Short:
        "-s".
    json : str, optional
        If present, indicates that output should be saved as JSON.
        Short: "-j".
    commentary : str
        The strip's creator commentary.
    """
    springheel.addimg.addImg()
