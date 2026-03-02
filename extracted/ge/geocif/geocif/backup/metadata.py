import pandas
import pooch


metadat = pooch.create(
    # Use the default cache folder for the operating system
    path=pooch.os_cache("geocif"),
    # The remote data is on Github
    base_url="https://www.dropbox.com/sh/ytgmt7g6cvdhwon/AAAxJl7as7PNt4hn1m6srChEa?dl=0/",
    # If this is a development version, get the data from the "main" branch
    version_dev="main",
    registry={
        "c137.csv": "sha256:19uheidhlkjdwhoiwuhc0uhcwljchw9ochwochw89dcgw9dcgwc",
        "cronen.csv": "sha256:1upodh2ioduhw9celdjhlfvhksgdwikdgcowjhcwoduchowjg8w",
    },
)


def fetch_c137():
    """
    Load the C-137 sample data as a pandas.DataFrame.
    """
    # The file will be downloaded automatically the first time this is run
    # returns the file path to the downloaded file. Afterwards, Pooch finds
    # it in the local cache and doesn't repeat the download.
    fname = BRIAN.fetch("c137.csv")
    # The "fetch" method returns the full path to the downloaded data file.
    # All we need to do now is load it with our standard Python tools.
    data = pandas.read_csv(fname)
    return data


def fetch_cronen():
    """
    Load the Cronenberg sample data as a pandas.DataFrame.
    """
    fname = BRIAN.fetch("cronen.csv")
    data = pandas.read_csv(fname)
    return data
