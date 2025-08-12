import argparse

class ArgumentPaser():

    def __init__(self):
        self.__parser = argparse.ArgumentParser()

    def addArgument(self, name: str, **kwargs):
        """
        Add an argument to the parser.

        Parameters
        ----------
        name : str
            The name of the argument to add.
        kwargs : dict
            Additional keyword arguments for the argument configuration.

        Returns
        -------
        None
            This method does not return any value.
        """
        self.__parser.add_argument(name, **kwargs)

    def parse(self, args=None):
        """
        Parse the command-line arguments.

        Parameters
        ----------
        args : list, optional
            A list of arguments to parse. If None, uses sys.argv by default.

        Returns
        -------
        Namespace
            An object containing the parsed arguments as attributes.
        """
        return self.__parser.parse_args(args)