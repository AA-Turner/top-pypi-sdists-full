import pprint
import asyncio
from collections.abc import Callable
import pandas as pd
import numpy as np
from lxml import etree
from ..exceptions import ComponentError, DataNotFound
from ..utils import cPrint
from .flow import FlowComponent


pp = pprint.PrettyPrinter(indent=2)


class XMLToPandas(FlowComponent):
    """
    XMLToPandas.

    Transform an XML list structure to Pandas

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          XMLToPandas:
          # attributes here
        ```
    """
    _version = "1.0.0"

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        """Init Method."""
        self.data = None
        self.infer_types: bool = False
        self.to_string: bool = True
        self.as_dict: bool = False
        self.as_objects: bool = False
        self._dtypes: dict = {}
        super(XMLToPandas, self).__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs):
        """
        start.

            Get if directory exists
        """
        if self.previous:
            if not isinstance(self.input, list):
                raise ComponentError(
                    f"XMLtoPandas requires a List as input, get {type(self.input)}"
                )
            try:
                if not etree.iselement(self.input[0]):
                    raise ComponentError("Invalid XML tree")
            except Exception as exc:
                raise ComponentError(
                    f"Error validating XML tree, error: {exc}"
                ) from exc
            #  if is valid:
            self.data = self.input
        else:
            raise ComponentError("Requires an *OpenXML* previous component")

    async def close(self):
        """
        close.

            close method
        """

    def set_datatypes(self):
        if hasattr(self, "datatypes"):
            dtypes = {}
            for field, dtype in self.datatypes.items():
                if dtype == "uint8":
                    dtypes[field] = np.uint8
                elif dtype == "uint16":
                    dtypes[field] = np.uint16
                elif dtype == "uint32":
                    dtypes[field] = np.uint32
                elif dtype == "int8":
                    dtypes[field] = np.int8
                elif dtype == "int16":
                    dtypes[field] = np.int16
                elif dtype == "int32":
                    dtypes[field] = np.int32
                elif dtype == "float":
                    dtypes[field] = float
                elif dtype == "float32":
                    dtypes[field] = float
                elif dtype in ("string", "varchar", "str"):
                    dtypes[field] = str
                else:
                    # invalid datatype
                    self._logger.warning(
                        f"Invalid DataType value: {field} for field {dtype}"
                    )
                    continue
            if dtypes:
                self._dtypes["dtype"] = dtypes

    async def get_dataframe(self, result):
        self.set_datatypes()
        print(self._dtypes)
        try:
            if self.as_objects is True:
                df = pd.DataFrame(result, dtype=object)
            else:
                df = pd.DataFrame(result, **self._dtypes)
        except Exception as err:
            self._logger.exception(err, stack_info=True)
        # Attempt to infer better dtypes for object columns.
        if self.infer_types is True:
            df.infer_objects()
            df = df.convert_dtypes(convert_string=self.to_string)
        if self._debug is True:
            cPrint("Data Types:")
            print(df.dtypes)
        if hasattr(self, "drop_empty"):
            df.dropna(axis=1, how="all", inplace=True)
            df.dropna(axis=0, how="all", inplace=True)
        if hasattr(self, "dropna"):
            df.dropna(subset=self.dropna, how="all", inplace=True)
        if (
            hasattr(self, "clean_strings")
            and getattr(self, "clean_strings", False) is True
        ):
            u = df.select_dtypes(include=["object", "string"])
            df[u.columns] = u.fillna("")
        return df

    def get_childs(self, element, id, parent: dict, name: str = None):
        odata = {}
        dr = {}
        for other in element.iterchildren():
            if name is not None:
                k = name
            else:
                k = other.tag.split("}")[1] if "}" in other.tag else other.tag
            oid = ""
            dr = {}
            if not k in odata.keys():
                odata[k] = []
            for a in other.attrib:
                if a == "id":
                    nw = "{}{}".format(k, a.capitalize())
                    oid = nw
                else:
                    nw = a
                dr[nw] = other.attrib[a]
                if hasattr(self, "add_previous"):
                    if id:
                        dr[id] = parent[id]
                # also we can add other columns too
                if hasattr(self, "add_parent"):
                    for col in self.add_parent:
                        if col in parent:
                            dr[col] = parent[col]
            # can we make recursive?
            # recursive: true
            if hasattr(self, "recursive") and self.recursive:
                if list(other):
                    # print(list(other))
                    self.get_childs(other, oid, dr)
            else:
                if hasattr(self, "process_child") and self.process_child:
                    child = other.find(self.process_child)
                    if child is not None:
                        if list(child):
                            # every child gets this name
                            self.get_childs(
                                child, oid, parent=dr, name=self.process_child
                            )
            odata[k].append(dr)
        # have all children on the structure
        result = []
        for key, item in odata.items():
            if key in self._result:
                result = self._result[key]
            self._result[key] = result + item

    async def run(self):
        """
        run.

            Transform the XML list into a Pandas Dataframe
        """
        self._result = None
        oresult = []
        if self.data:
            for item in self.data:
                obj = {}
                for child_element in item.iterchildren():
                    column_name = child_element.tag
                    column_value = child_element.text
                    obj[column_name] = column_value
                oresult.append(obj)
            #     if hasattr(self, 'childs') and self.childs is True:
            #         # elements to build List come from child elements
            #         key = ''
            #         data = []
            #         for element in item.iterchildren():
            #             # Remove namespace prefix
            #             key = element.tag.split('}')[1] if '}' in element.tag else element.tag
            #             d = {}
            #             _id = ''
            #             for att in element.attrib:
            #                 if att == 'id':
            #                     name = '{}{}'.format(key, att.capitalize())
            #                     _id = name
            #                 else:
            #                     name = att
            #                 d[name] = element.attrib[att]
            #             # recursive: true
            #             if hasattr(self, 'recursive'):
            #                 if list(element):
            #                     self.get_childs(element, _id, parent=d)
            #             # processing categories
            #             data.append(d)
            #         # append to result
            #         self._result[key] = data
            #     else:
            #         # need to process all items one by one
            #         key = item.tag.split('}')[1] if '}' in item.tag else item.tag
            #         print('KEY > ', key)
            #         data = {}
            #         _id = ''
            #         for att in item.attrib:
            #             print('ATTR >', att)
            #             if att == 'id':
            #                 name = '{}{}'.format(key, att.capitalize())
            #                 _id = name
            #             else:
            #                 name = att
            #             data[name] = item.attrib[att]
            #         if hasattr(self, 'recursive'):
            #             if list(item):
            #                 self.get_childs(item, _id, parent=data)
            #         else:
            #             # item has childs, but I need to recurse
            #             if hasattr(self, 'process_child'):
            #                 child = item.find(self.process_child)
            #                 if list(child):
            #                     # every child gets this name
            #                     self.get_childs(child, _id, parent=data, name=self.process_child)
            #         oresult.append(data)
            # # check oresult
            if oresult:
                self._result = oresult
            if self._result:
                df = await self.get_dataframe(result=self._result)
                if self._debug is True:
                    print("== DATA PREVIEW ==")
                    print(df)
                    print()
                    numrows = len(df.index)
                    self.add_metric("NUMROWS", numrows)
                    self.add_metric("COLUMNS", df.shape[1])
                if isinstance(df, pd.DataFrame):
                    if not df.empty:
                        self._result = df
                    else:
                        raise DataNotFound(f"Empty Dataframe for -{self.data}-")
                return self._result
            else:
                self._result = []
                return False
        else:
            # nothing
            return False
