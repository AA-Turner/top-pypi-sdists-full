from typing import overload
from enum import IntEnum
import typing

import QuantConnect
import QuantConnect.Interfaces
import QuantConnect.Packets
import QuantConnect.Storage
import System
import System.Collections.Generic
import System.Text
import pandas

QuantConnect_Storage__EventContainer_Callable = typing.TypeVar("QuantConnect_Storage__EventContainer_Callable")
QuantConnect_Storage__EventContainer_ReturnType = typing.TypeVar("QuantConnect_Storage__EventContainer_ReturnType")
QuantConnect_Storage_ObjectStore_ReadJson_T = typing.TypeVar("QuantConnect_Storage_ObjectStore_ReadJson_T")
QuantConnect_Storage_ObjectStore_ReadXml_T = typing.TypeVar("QuantConnect_Storage_ObjectStore_ReadXml_T")
QuantConnect_Storage_ObjectStore_SaveJson_T = typing.TypeVar("QuantConnect_Storage_ObjectStore_SaveJson_T")
QuantConnect_Storage_ObjectStore_SaveXml_T = typing.TypeVar("QuantConnect_Storage_ObjectStore_SaveXml_T")


class _Typed_ObjectStore_ReadJson(typing.Generic[QuantConnect_Storage_ObjectStore_ReadJson_T]):
    """"""

    @overload
    def __call__(self, path: str, encoding: System.Text.Encoding = None, settings: typing.Any = None) -> QuantConnect_Storage_ObjectStore_ReadJson_T:
        """
        Returns the JSON deserialized object data for the specified path
        
        :param path: The object path
        :param encoding: The string encoding used
        :param settings: The settings used by the JSON deserializer
        :returns: An object containing the data.
        """
        ...


class _ObjectStore_ReadJson:
    """"""

    def __getitem__(self, type: typing.Type[QuantConnect_Storage_ObjectStore_ReadJson_T]) -> QuantConnect.Storage._Typed_ObjectStore_ReadJson[QuantConnect_Storage_ObjectStore_ReadJson_T]:
        ...


class _Typed_ObjectStore_ReadXml(typing.Generic[QuantConnect_Storage_ObjectStore_ReadXml_T]):
    """"""

    @overload
    def __call__(self, path: str, encoding: System.Text.Encoding = None) -> QuantConnect_Storage_ObjectStore_ReadXml_T:
        """
        Returns the XML deserialized object data for the specified path
        
        :param path: The object path
        :param encoding: The string encoding used
        :returns: An object containing the data.
        """
        ...


class _ObjectStore_ReadXml:
    """"""

    def __getitem__(self, type: typing.Type[QuantConnect_Storage_ObjectStore_ReadXml_T]) -> QuantConnect.Storage._Typed_ObjectStore_ReadXml[QuantConnect_Storage_ObjectStore_ReadXml_T]:
        ...


class _Typed_ObjectStore_SaveJson(typing.Generic[QuantConnect_Storage_ObjectStore_SaveJson_T]):
    """"""

    @overload
    def __call__(self, path: str, obj: QuantConnect_Storage_ObjectStore_SaveJson_T, encoding: System.Text.Encoding = None, settings: typing.Any = None) -> bool:
        """
        Saves the object data in JSON format for the specified path
        
        :param path: The object key: english letters, numbers, spaces and the characters '.', '/', '\\', '_', '#', '-', '$' and '=', never '..', e.g. 'folder/trade_log-2024.v2.csv'. Other characters are replaced by '_'
        :param obj: The object to be saved
        :param encoding: The string encoding used
        :param settings: The settings used by the JSON serializer
        :returns: True if the object was saved successfully.
        """
        ...


class _ObjectStore_SaveJson:
    """"""

    def __getitem__(self, type: typing.Type[QuantConnect_Storage_ObjectStore_SaveJson_T]) -> QuantConnect.Storage._Typed_ObjectStore_SaveJson[QuantConnect_Storage_ObjectStore_SaveJson_T]:
        ...


class _Typed_ObjectStore_SaveXml(typing.Generic[QuantConnect_Storage_ObjectStore_SaveXml_T]):
    """"""

    @overload
    def __call__(self, path: str, obj: QuantConnect_Storage_ObjectStore_SaveXml_T, encoding: System.Text.Encoding = None) -> bool:
        """
        Saves the object data in XML format for the specified path
        
        :param path: The object key: english letters, numbers, spaces and the characters '.', '/', '\\', '_', '#', '-', '$' and '=', never '..', e.g. 'folder/trade_log-2024.v2.csv'. Other characters are replaced by '_'
        :param obj: The object to be saved
        :param encoding: The string encoding used
        :returns: True if the object was saved successfully.
        """
        ...


class _ObjectStore_SaveXml:
    """"""

    def __getitem__(self, type: typing.Type[QuantConnect_Storage_ObjectStore_SaveXml_T]) -> QuantConnect.Storage._Typed_ObjectStore_SaveXml[QuantConnect_Storage_ObjectStore_SaveXml_T]:
        ...


class ObjectStore(System.Object, QuantConnect.Interfaces.IObjectStore, typing.Iterable[System.Collections.Generic.KeyValuePair[str, typing.List[int]]]):
    """
    Helper class for easier access to IObjectStore methods. A key that does not follow the key
    format (english letters, numbers, spaces and the characters '.', '/', '\\', '_', '#', '-', '$' and '=', never
    two '.' in a row, e.g. 'folder/trade_log-2024.v2.csv') is saved under its sanitized version, then found and
    listed by either name, with a warning the first time it happens. An object already stored under an unsupported name
    is read as is until a save through that name creates the sanitized one
    """

    @property
    def max_size(self) -> int:
        """Gets the maximum storage limit in bytes"""
        ...

    @property
    def max_files(self) -> int:
        """Gets the maximum number of files allowed"""
        ...

    @property
    def error_raised(self) -> _EventContainer[typing.Callable[[System.Object, QuantConnect.Interfaces.ObjectStoreErrorRaisedEventArgs], typing.Any], typing.Any]:
        """Event raised each time there's an error"""
        ...

    @error_raised.setter
    def error_raised(self, value: _EventContainer[typing.Callable[[System.Object, QuantConnect.Interfaces.ObjectStoreErrorRaisedEventArgs], typing.Any], typing.Any]) -> None:
        ...

    @property
    def keys(self) -> System.Collections.Generic.ICollection[str]:
        """
        Returns the file paths present in the object store. This is specially useful not to load the object store into memory.
        An unsupported key saved in this run is listed next to the sanitized name its object is stored under.
        The store is listed on first use, and Contains finds a key the way contains_key does, without listing it
        """
        ...

    @property
    def read_json(self) -> QuantConnect.Storage._ObjectStore_ReadJson:
        ...

    @property
    def read_xml(self) -> QuantConnect.Storage._ObjectStore_ReadXml:
        ...

    @property
    def save_json(self) -> QuantConnect.Storage._ObjectStore_SaveJson:
        ...

    @property
    def save_xml(self) -> QuantConnect.Storage._ObjectStore_SaveXml:
        ...

    def __init__(self, store: QuantConnect.Interfaces.IObjectStore, warn: typing.Callable[[str], typing.Any] = None) -> None:
        """
        Initializes a new instance of the ObjectStore class
        
        :param store: The IObjectStore instance to wrap
        :param warn: Receives the warnings about sanitized keys, the engine log by default
        """
        ...

    def __iter__(self) -> typing.Iterator[System.Collections.Generic.KeyValuePair[str, typing.List[int]]]:
        ...

    def clear(self) -> None:
        """Will clear the object store state cache. This is useful when the object store is used concurrently by nodes which want to share information"""
        ...

    def contains_key(self, path: str) -> bool:
        """
        Determines whether the store contains data for the specified path
        
        :param path: The object path
        :returns: True if the key was found.
        """
        ...

    def delete(self, path: str) -> bool:
        """
        Deletes the object data for the specified path
        
        :param path: The object path
        :returns: True if the delete operation was successful.
        """
        ...

    def dispose(self) -> None:
        """Performs application-defined tasks associated with freeing, releasing, or resetting unmanaged resources."""
        ...

    def get_enumerator(self) -> System.Collections.Generic.IEnumerator[System.Collections.Generic.KeyValuePair[str, typing.List[int]]]:
        """
        Returns an enumerator that iterates through the collection.
        
        :returns: A System.Collections.Generic.IEnumerator`1 that can be used to iterate through the collection.
        """
        ...

    def get_file_path(self, path: str) -> str:
        """
        Returns the file path for the specified path
        
        :param path: The object path
        :returns: The path for the file.
        """
        ...

    def initialize(self, user_id: int, project_id: int, user_token: str, controls: QuantConnect.Packets.Controls, algorithm_mode: QuantConnect.AlgorithmMode) -> None:
        """
        Initializes the object store
        
        :param user_id: The user id
        :param project_id: The project id
        :param user_token: The user token
        :param controls: The job controls instance
        :param algorithm_mode: The algorithm mode
        """
        ...

    def read(self, path: str, encoding: System.Text.Encoding = None) -> str:
        """
        Returns the string object data for the specified path
        
        :param path: The object path
        :param encoding: The string encoding used
        :returns: A string containing the data.
        """
        ...

    def read_bytes(self, path: str) -> typing.List[int]:
        """
        Returns the object data for the specified path
        
        :param path: The object path
        :returns: A byte array containing the data.
        """
        ...

    def read_string(self, path: str, encoding: System.Text.Encoding = None) -> str:
        """
        Returns the string object data for the specified path
        
        :param path: The object path
        :param encoding: The string encoding used
        :returns: A string containing the data.
        """
        ...

    def read_text(self, path: str, encoding: System.Text.Encoding = None) -> str:
        """
        Returns the object data for the specified path as a string. Alias of read(string, Encoding)
        
        :param path: The object path
        :param encoding: The string encoding used, Encoding.UTF8 by default
        :returns: A string containing the data.
        """
        ...

    @overload
    def save(self, path: str) -> bool:
        """
        Saves the data from a local file path associated with the specified path
        
        :param path: The object key: english letters, numbers, spaces and the characters '.', '/', '\\', '_', '#', '-', '$' and '=', never '..', e.g. 'folder/trade_log-2024.v2.csv'. Other characters are replaced by '_'
        :returns: True if the object was saved successfully.
        """
        ...

    @overload
    def save(self, path: str, text: str, encoding: System.Text.Encoding = None) -> bool:
        """
        Saves the object data in text format for the specified path
        
        :param path: The object key: english letters, numbers, spaces and the characters '.', '/', '\\', '_', '#', '-', '$' and '=', never '..', e.g. 'folder/trade_log-2024.v2.csv'. Other characters are replaced by '_'
        :param text: The string object to be saved
        :param encoding: The string encoding used, Encoding.UTF8 by default
        :returns: True if the object was saved successfully.
        """
        ...

    def save_bytes(self, path: str, contents: typing.List[int]) -> bool:
        """
        Saves the object data for the specified path
        
        :param path: The object key: english letters, numbers, spaces and the characters '.', '/', '\\', '_', '#', '-', '$' and '=', never '..', e.g. 'folder/trade_log-2024.v2.csv'. Other characters are replaced by '_'
        :param contents: The object data
        :returns: True if the save operation was successful.
        """
        ...

    def save_string(self, path: str, text: str, encoding: System.Text.Encoding = None) -> bool:
        """
        Saves the object data in text format for the specified path
        
        :param path: The object key: english letters, numbers, spaces and the characters '.', '/', '\\', '_', '#', '-', '$' and '=', never '..', e.g. 'folder/trade_log-2024.v2.csv'. Other characters are replaced by '_'
        :param text: The string object to be saved
        :param encoding: The string encoding used
        :returns: True if the object was saved successfully.
        """
        ...

    def save_text(self, path: str, text: str, encoding: System.Text.Encoding = None) -> bool:
        """
        Saves the object data in text format for the specified path.
        Alias of save(string, string, Encoding)
        
        :param path: The object key: english letters, numbers, spaces and the characters '.', '/', '\\', '_', '#', '-', '$' and '=', never '..', e.g. 'folder/trade_log-2024.v2.csv'. Other characters are replaced by '_'
        :param text: The string object to be saved
        :param encoding: The string encoding used, Encoding.UTF8 by default
        :returns: True if the object was saved successfully.
        """
        ...


class _PythonObjectStore_ReadJson(QuantConnect.Storage._ObjectStore_ReadJson):
    """"""

    @overload
    def __call__(self, path: str) -> typing.Any:
        """
        Returns the JSON deserialized object data for the specified path as Python objects
        
        :param path: The object path
        :returns: The deserialized Python object.
        """
        ...


class _PythonObjectStore_SaveJson(QuantConnect.Storage._ObjectStore_SaveJson):
    """"""

    @overload
    def __call__(self, path: str, obj: typing.Any) -> bool:
        """
        Saves the given Python dictionary, list, tuple or .NET object in JSON format for the specified path,
        tolerating nested types the standard json module rejects: datetime/date/time, pandas Timestamp and
        numpy datetime64 are stored in ISO-8601 format, timedelta and timedelta64 as ISO-8601 durations,
        Decimal and numpy numbers as numbers, NaN, infinity and NaT as null, .NET objects (Symbol included)
        as the C# ObjectStore.SaveJson{T} overload writes them (a NaN inside one is Newtonsoft's "NaN"
        string) and non-string dictionary keys as strings. pandas DataFrames and Series are rejected, use
        SaveDataframe, and so is any other type that would not round trip. A top-level Python
        str, int, float or bool is not accepted, use ObjectStore.save_text for text
        
        :param path: The object key: english letters, numbers, spaces and the characters '.', '/', '\\', '_', '#', '-', '$' and '=', never '..', e.g. 'folder/trade_log-2024.v2.csv'. Other characters are replaced by '_'
        :param obj: The Python object to be saved
        :returns: True if the object was saved successfully.
        """
        ...


class PythonObjectStore(QuantConnect.Storage.ObjectStore):
    """
    The ObjectStore of Python algorithms and notebooks: adds the save and read methods that take
    and return Python objects, such as dictionaries and pandas DataFrames
    """

    @property
    def read_json(self) -> QuantConnect.Storage._PythonObjectStore_ReadJson:
        ...

    @property
    def save_json(self) -> QuantConnect.Storage._PythonObjectStore_SaveJson:
        ...

    def __init__(self, store: QuantConnect.Interfaces.IObjectStore, warn: typing.Callable[[str], typing.Any] = None) -> None:
        """
        Initializes a new instance of the PythonObjectStore class
        
        :param store: The IObjectStore instance to wrap
        :param warn: Receives the warnings about sanitized keys, the engine log by default
        """
        ...

    def read_dataframe(self, path: str) -> pandas.DataFrame:
        """
        Returns the object data for the specified path as a pandas DataFrame, read as JSON if the path has
        a '.json' extension and as CSV otherwise, so a save_dataframe round trip restores the frame.
        A CSV index in ISO-8601 format is restored as a time index. A saved Series comes back as a
        one-column DataFrame, call squeeze() on it to get the Series
        
        :param path: The object path
        :returns: The pandas DataFrame.
        """
        ...

    def save_dataframe(self, path: str, data_frame: typing.Any) -> bool:
        """
        Saves the given pandas DataFrame (or Series) for the specified path, in JSON format if the
        path has a '.json' extension and as CSV otherwise
        
        :param path: The object key: english letters, numbers, spaces and the characters '.', '/', '\\', '_', '#', '-', '$' and '=', never '..', e.g. 'folder/trade_log-2024.v2.csv'. Other characters are replaced by '_'
        :param data_frame: The pandas DataFrame or Series to be saved
        :returns: True if the object was saved successfully.
        """
        ...


class _EventContainer(typing.Generic[QuantConnect_Storage__EventContainer_Callable, QuantConnect_Storage__EventContainer_ReturnType]):
    """This class is used to provide accurate autocomplete on events and cannot be imported."""

    def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> QuantConnect_Storage__EventContainer_ReturnType:
        """Fires the event."""
        ...

    def __iadd__(self, item: QuantConnect_Storage__EventContainer_Callable) -> typing.Self:
        """Registers an event handler."""
        ...

    def __isub__(self, item: QuantConnect_Storage__EventContainer_Callable) -> typing.Self:
        """Unregisters an event handler."""
        ...


