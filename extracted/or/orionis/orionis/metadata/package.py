import requests
from orionis.metadata.framework import API

class PypiOrionisPackage:
    """
    Provides an interface for retrieving and accessing metadata about the Orionis package from PyPI.

    This class automatically fetches metadata from the PyPI JSON API for the Orionis package upon initialization.
    The metadata includes information such as package name, version, author, description, license, classifiers,
    required Python version, keywords, and project URLs. The metadata is stored internally and can be accessed
    through dedicated methods.

    Attributes
    ----------
    _baseUrl : str
        The base URL for the PyPI API endpoint used to fetch package metadata.
    _info : dict
        A dictionary containing the metadata retrieved from the PyPI API.

    Notes
    -----
    The metadata is retrieved using the PyPI JSON API and stored in the `_info` attribute.
    If the request fails or the response structure is invalid, an exception will be raised during initialization.
    """

    def __init__(self) -> None:
        """
        Initialize the PypiOrionisPackage instance.

        This constructor sets up the base URL for the Orionis PyPI package, initializes the internal
        information dictionary, and immediately fetches all available package metadata from PyPI.

        Parameters
        ----------
        None

        Returns
        -------
        None
            This method does not return any value. It initializes instance attributes and populates
            the `_info` dictionary with package metadata.

        Notes
        -----
        The metadata is retrieved using the PyPI JSON API and stored in the `_info` attribute.
        If the request fails, an exception will be raised during initialization.
        """
        self._baseUrl = API  # Set the base URL for the PyPI API endpoint
        self._info = {}      # Initialize the dictionary to store package metadata
        self.getAllData()    # Fetch and populate metadata from PyPI

    def getAllData(self) -> dict:
        """
        Fetch and update package metadata from the PyPI API.

        This method sends a GET request to the PyPI JSON API endpoint specified by `self._baseUrl`.
        If the request is successful (HTTP status code 200), it parses the JSON response and updates
        the internal `_info` attribute with the value associated with the "info" key. If the "info"
        key is missing or the request fails, an exception is raised.

        Parameters
        ----------
        None

        Returns
        -------
        dict
            A dictionary containing the package metadata retrieved from PyPI. This dictionary is also
            stored in the instance's `_info` attribute.

        Raises
        ------
        Exception
            If the request to the PyPI API fails, returns a non-200 status code, or the response
            structure is invalid (missing the "info" key).

        Notes
        -----
        The method uses a timeout of 10 seconds for the HTTP request to avoid hanging indefinitely.
        """
        try:
            # Send a GET request to the PyPI API endpoint
            response = requests.get(self._baseUrl, timeout=10)

            # Raise an error for non-200 status codes
            response.raise_for_status()

            # Parse the JSON response
            data: dict = response.json()

            # Extract the 'info' section containing package metadata
            self._info = data.get("info", {})

            # Raise an error if 'info' key is missing or empty
            if not self._info:
                raise ValueError("No 'info' key found in PyPI response.")

            # Return the package metadata dictionary
            return self._info

        except requests.RequestException as e:

            # Handle network or HTTP errors
            raise Exception(
                f"Error fetching data from PyPI: {e}. "
                "Please check your internet connection or try again later."
            )
        except ValueError as ve:

            # Handle invalid response structure
            raise Exception(
                f"Invalid response structure from PyPI: {ve}"
            )

    def getName(self) -> str:
        """
        Retrieve the package name from the internal metadata dictionary.

        This method accesses the '_info' attribute, which contains metadata fetched from the PyPI API,
        and returns the value associated with the 'name' key. The package name uniquely identifies the
        Python package as registered on PyPI.

        Returns
        -------
        str
            The name of the package as specified in the PyPI metadata.

        Notes
        -----
        The '_info' dictionary must be populated before calling this method, typically during initialization.
        If the 'name' key is missing, a KeyError will be raised.
        """

        # Return the package name from the metadata dictionary
        return self._info['name']

    def getVersion(self) -> str:
        """
        Retrieve the version information of the Orionis framework from the internal metadata dictionary.

        This method accesses the '_info' attribute, which contains metadata fetched from the PyPI API,
        and returns the value associated with the 'version' key. The version string uniquely identifies
        the current release of the package as registered on PyPI.

        Returns
        -------
        str
            The version string of the Orionis framework as specified in the PyPI metadata.

        Notes
        -----
        The '_info' dictionary must be populated before calling this method, typically during initialization.
        If the 'version' key is missing, a KeyError will be raised.
        """

        # Return the version string from the metadata dictionary
        return self._info['version']

    def getAuthor(self) -> str:
        """
        Retrieve the author's name from the internal metadata dictionary.

        This method accesses the '_info' attribute, which contains metadata fetched from the PyPI API,
        and returns the value associated with the 'author' key. The author's name identifies the individual
        or organization responsible for maintaining the Orionis framework package.

        Returns
        -------
        str
            The author's name as specified in the PyPI metadata. If the 'author' key is missing, a KeyError will be raised.

        Notes
        -----
        The '_info' dictionary must be populated before calling this method, typically during initialization.
        """

        # Return the author's name from the metadata dictionary
        return self._info['author']

    def getAuthorEmail(self) -> str:
        """
        Retrieve the author's email address from the internal metadata dictionary.

        This method accesses the '_info' attribute, which contains metadata fetched from the PyPI API,
        and returns the value associated with the 'author_email' key. The author's email address is useful
        for contacting the maintainer of the Orionis framework package.

        Returns
        -------
        str
            The email address of the author as specified in the PyPI metadata. If the 'author_email' key
            is missing, a KeyError will be raised.

        Notes
        -----
        The '_info' dictionary must be populated before calling this method, typically during initialization.
        """

        # Return the author's email address from the metadata dictionary
        return self._info['author_email']

    def getDescription(self) -> str:
        """
        Retrieve the summary description of the Orionis framework package.

        This method accesses the internal `_info` dictionary, which contains metadata fetched from the PyPI API,
        and returns the value associated with the 'summary' key. The summary provides a brief description of the
        package as registered on PyPI.

        Returns
        -------
        str
            The summary description of the Orionis framework package, as stored in the '_info' dictionary under the 'summary' key.

        Notes
        -----
        The '_info' dictionary must be populated before calling this method, typically during initialization.
        If the 'summary' key is missing, a KeyError will be raised.
        """

        # Return the summary description from the metadata dictionary
        return self._info['summary']

    def getUrl(self) -> str:
        """
        Retrieve the homepage URL of the Orionis framework package from PyPI metadata.

        This method accesses the internal `_info` dictionary, which contains metadata fetched from the PyPI API,
        and extracts the homepage URL from the 'project_urls' sub-dictionary under the 'Homepage' key. The homepage
        URL typically points to the main website or documentation for the Orionis framework.

        Returns
        -------
        str
            The homepage URL of the Orionis framework package as specified in the PyPI metadata under
            `_info['project_urls']['Homepage']`.

        Notes
        -----
        The `_info` dictionary must be populated before calling this method, typically during initialization.
        If the 'Homepage' key is missing in the 'project_urls' dictionary, a KeyError will be raised.
        """

        # Access the 'project_urls' dictionary and return the 'Homepage' URL
        return self._info['project_urls']['Homepage']

    def getLongDescription(self) -> str:
        """
        Retrieve the long description of the Orionis framework package.

        This method accesses the internal `_info` dictionary, which contains metadata fetched from the PyPI API,
        and returns the value associated with the 'description' key. The long description typically provides
        a detailed overview of the package, including features, usage, and other relevant information as
        registered on PyPI.

        Returns
        -------
        str
            The long description text of the Orionis framework package, as stored in the '_info' dictionary
            under the 'description' key.

        Notes
        -----
        The '_info' dictionary must be populated before calling this method, typically during initialization.
        If the 'description' key is missing, a KeyError will be raised.
        """

        # Return the long description from the metadata dictionary
        return self._info['description']

    def getDescriptionContentType(self) -> str:
        """
        Retrieve the content type of the package description from the internal metadata dictionary.

        This method accesses the `_info` attribute, which contains metadata fetched from the PyPI API,
        and returns the value associated with the 'description_content_type' key. The content type
        indicates the format of the package's long description, such as 'text/markdown' or 'text/plain'.

        Returns
        -------
        str
            The content type of the package description (e.g., 'text/markdown', 'text/plain') as specified
            in the PyPI metadata under the 'description_content_type' key.

        Notes
        -----
        The `_info` dictionary must be populated before calling this method, typically during initialization.
        If the 'description_content_type' key is missing, a KeyError will be raised.
        """

        # Return the content type of the description from the metadata dictionary
        return self._info['description_content_type']

    def getLicense(self) -> str:
        """
        Retrieve the license type specified in the framework metadata.

        This method accesses the internal `_info` dictionary, which contains metadata fetched from the PyPI API,
        and returns the value associated with the 'license' key. If the license information is not set or is an
        empty string, the method defaults to returning "MIT".

        Returns
        -------
        str
            The license type as specified in the PyPI metadata under the 'license' key. If the license is not set,
            returns "MIT".

        Notes
        -----
        The `_info` dictionary must be populated before calling this method, typically during initialization.
        If the 'license' key is missing, a KeyError will be raised.
        """

        # Return the license type from the metadata dictionary, defaulting to "MIT" if not set
        return self._info['license'] or "MIT"

    def getClassifiers(self) -> list:
        """
        Retrieve the list of classifiers associated with the Orionis framework package.

        This method accesses the internal `_info` dictionary, which contains metadata fetched from the PyPI API,
        and returns the value associated with the 'classifiers' key. Classifiers are standardized strings used
        by PyPI to categorize the package (e.g., supported Python versions, intended audience, license, etc.).

        Returns
        -------
        list of str
            A list of classifier strings as specified in the PyPI metadata under the 'classifiers' key.
            Each string describes a category or property of the package.

        Notes
        -----
        The `_info` dictionary must be populated before calling this method, typically during initialization.
        If the 'classifiers' key is missing, a KeyError will be raised.
        """

        # Return the list of classifiers from the metadata dictionary
        return self._info['classifiers']

    def getPythonVersion(self) -> str:
        """
        Retrieve the required Python version specification from the package metadata.

        This method accesses the internal `_info` dictionary, which contains metadata fetched from the PyPI API,
        and returns the value associated with the 'requires_python' key. The returned string specifies the Python
        version(s) required to use the Orionis framework package, as defined in its PyPI metadata.

        Returns
        -------
        str
            The Python version specification required by the framework, as defined in the '_info' dictionary
            under the 'requires_python' key. For example, it may return a string like '>=3.7'.

        Notes
        -----
        The `_info` dictionary must be populated before calling this method, typically during initialization.
        If the 'requires_python' key is missing, a KeyError will be raised.
        """

        # Return the required Python version specification from the metadata dictionary
        return self._info['requires_python']

    def getKeywords(self) -> list:
        """
        Retrieve the list of keywords associated with the Orionis framework package.

        This method accesses the internal `_info` dictionary, which contains metadata fetched from the PyPI API,
        and returns the value associated with the 'keywords' key. Keywords are typically used to describe the
        package's functionality, domain, or relevant search terms on PyPI.

        Returns
        -------
        list of str
            A list of keywords describing the Orionis framework package, as specified in the PyPI metadata
            under the 'keywords' key.

        Notes
        -----
        The `_info` dictionary must be populated before calling this method, typically during initialization.
        If the 'keywords' key is missing, a KeyError will be raised.
        """

        # Return the list of keywords from the metadata dictionary
        return self._info['keywords']