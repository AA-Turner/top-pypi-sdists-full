# /*******************************************************************************
#  * Copyright (c) 2019 - 2022 Cambridge Semantics Incorporated.
#  * All rights reserved.
#  * 
#  * Contributors:
#  *     Cambridge Semantics Incorporated
#  *******************************************************************************/

from typing import List, Set, Dict, Any
import rdflib

from .uris import NAMESPACE


def semantic_type_to_python_object(val: str, val_datatype: str) -> any:
    """
    Returns val as the python type specified by val_datatype. For example,
    if val_datatype is xsd:int, then val parsed as an int will be returned.

    Args:
        val: The value to parse
        val_datatype: The datatype of val, used to inform the parsing

    Returns: val parsed as a python object; parsed as indicated
        by the val_datatype
    """

    mapping = {
        "http://www.w3.org/2001/XMLSchema#int": int,
        "http://www.w3.org/2001/XMLSchema#integer": int,
        "http://www.w3.org/2001/XMLSchema#long": int,
        "http://www.w3.org/2001/XMLSchema#float": float,
        "http://www.w3.org/2001/XMLSchema#double": float,
        "http://www.w3.org/2001/XMLSchema#decimal": float,
    }

    if val_datatype in mapping:
        func = mapping[val_datatype]
        return func(val)
    return val


class Quad:
    NAMED_GRAPH_URI_KEY = "namedGraphUri"
    SUBJECT_KEY = "subject"
    VALUE_KEY = "value"
    OBJECT_KEY = "object"
    PREDICATE_KEY = "predicate"
    TYPE_KEY = "objectType"
    DATA_TYPE_KEY = "dataType"

    def __init__(self, sub, pred, obj, graph, sub_type="", obj_type="", obj_data_type=""):
        self.sub = sub
        self.pred = pred
        self.obj = obj
        self.graph = graph

        self.sub_type = sub_type if sub_type else "uri"

        # obj_type is typically either uri or literal
        self.obj_type = obj_type if obj_type else "uri"

        # obj_data_type is only non-empty if obj_type
        # is a literal, and it will be the type of literal,
        # like an xsd:int or xsd:float.
        self.obj_data_type = obj_data_type

    @staticmethod
    def from_anzo_json_dict(item: Dict[str, Any]):
        try:
            sub = item[Quad.SUBJECT_KEY][Quad.VALUE_KEY]
            sub_type = item[Quad.SUBJECT_KEY][Quad.TYPE_KEY]

            pred = item[Quad.PREDICATE_KEY]

            obj = item[Quad.OBJECT_KEY][Quad.VALUE_KEY]
            obj_type = item[Quad.OBJECT_KEY][Quad.TYPE_KEY]

            obj_data_type = item[Quad.OBJECT_KEY].get(Quad.DATA_TYPE_KEY, "")

        except (KeyError, TypeError, AttributeError) as e:
            raise RuntimeError(f"The JSON object {item} is not suited to"
                               " be transformed into a Quad. ") from e

        graph = item.get(Quad.NAMED_GRAPH_URI_KEY, "")
        return Quad(sub, pred, obj, graph, sub_type, obj_type, obj_data_type)

    def as_anzo_json_dict(self) -> dict:

        object_dict = dict()

        object_dict = {
            self.VALUE_KEY: self.obj,
            self.TYPE_KEY: self.obj_type
        }

        if self.obj_data_type:
            object_dict[self.DATA_TYPE_KEY] = self.obj_data_type

        return {
            self.NAMED_GRAPH_URI_KEY: self.graph,
            self.SUBJECT_KEY: {
                self.VALUE_KEY: self.sub,
                self.TYPE_KEY: self.sub_type
            },
            self.PREDICATE_KEY: self.pred,
            self.OBJECT_KEY: object_dict,
        }

    def as_record_dict(self):
        ret = {
            's': semantic_type_to_python_object(self.sub, self.sub_type),
            'p': self.pred,
            'o': semantic_type_to_python_object(self.obj, self.obj_data_type)
        }

        # Only add the graph if it exists
        if self.graph:
            ret['g'] = self.graph
        return ret

    def verbosify(self) -> str:
        """Returns a verbose string describing the quad. For a less
        verbose serialization, use str()
        """

        return (
            f"<Quad sub={self.sub}, sub_type={self.sub_type} "
            f"pred={self.pred}, "
            f"obj={self.obj}, obj_type={self.obj_type}, "
            f"obj_data_type={self.obj_data_type}, graph={self.graph}>"
        )

    def __eq__(self, other):
        return self.sub == other.sub and self.pred == other.pred and \
            self.obj == other.obj and self.graph == other.graph and \
            self.sub_type == other.sub_type and self.obj_type == other.obj_type \
            and self.obj_data_type == other.obj_data_type

    def __str__(self) -> str:
        return (
            f"<Quad sub={self.sub}, pred={self.pred}, "
            f"obj={self.obj}, graph={self.graph} "
            f"sub_type={self.sub_type}, obj_type={self.obj_type}, "
            f"obj_data_type={self.obj_data_type}>"
        )

    def __hash__(self):
        return hash((
            self.sub, self.sub_type, self.pred,
            self.obj, self.obj_type, self.obj_data_type,
            self.graph
        ))

    def __repr__(self):
        return str(self)

    def __lt__(self, other):
        return str(self.verbosify()) < str(other.verbosify())


class QuadStore:
    """Holds a set of quads

    This class is for interactions with Anzo that require trig.
    It holds quads which can be serialized to json and used
    in a semantic service payload, or it can be used to capture
    the results of a construct query, or get, for example.

    Attributes:
        quads: A set of Quads

    Raises:
        RuntimeError: Calling the method from_json errors
            when the json that it is passed is not valid.
    """

    def __init__(self, quads=None) -> None:
        """Stores quads.

        This initialization sets up an empty set of
        of Quads that can be added to by other methods.

        """

        self.quads: Set[Quad] = quads if quads else set()
        self.namespace: Dict[str, str] = NAMESPACE

    @staticmethod
    def from_anzo_json_list(json_list: List[Dict[str, Any]]): # -> QuadStore:
        """Builds a QuadStore from a list of JSON objects.

        Iterates through the list of JSON objects, and for each
        one adds a coresponding Quad to the QuadStore.

        Args:
            json_list: A list of JSON objects.

        Returns: A QuadStore object

        Raises:
            RuntimeError: If the passed JSON objects do not have the following
            form: {
                   "namedGraphUri": <URI_1> ,
                   "subject":{
                       "objectType":<TYPE>,
                       "value":<URI_2>
                       },
                  "predicate":<URI_3>,
                  "object":{
                      "objectType":<TYPE>,
                      "value":<URI_4>
                      }
                  }
        """
        quads = set()
        for item in json_list:
            quads.add(Quad.from_anzo_json_dict(item))
        return QuadStore(quads)

    @staticmethod
    def from_rdflib_graph(rdflib_graph, include_graphs: bool = True):
        """Builds a QuadStore from an RDFLib Graph

        This method requires RDFLib to be installed. If RDFLib is not
        installed, a NotImplementedError is raised.

        Args:
            rdflib_graph: RdfLib Graph to use for building the QuadStore
            include_graphs (optional): If False, then the Graph of all Quads
                is set to None, otherwise, the value in the rdflib_graph
                object is used. Defaults to True.

        Returns: A QuadStore object
        """

        quads = set()
        for s in rdflib_graph.quads():

            if isinstance(s[0], rdflib.BNode):
                sub_type = "bnode"
            else:
                sub_type = "uri"

            obj_type = ""
            obj_data_type = ""

            if isinstance(s[2], rdflib.Literal) and s[2].datatype is not None:
                obj_type = "literal"
                obj_data_type = str(s[2].datatype)
            elif isinstance(s[2], rdflib.Literal) and s[2].datatype is None:
                obj_type = "literal"
            elif isinstance(s[2], rdflib.BNode):
                obj_type = "bnode"
            else:
                obj_type = "uri"

            if include_graphs:
                graph = str(s[3].identifier)
            else:
                graph = None

            quads.add(Quad(
                sub=str(s[0]),
                pred=str(s[1]),
                obj=str(s[2]),
                graph=graph,
                sub_type=sub_type,
                obj_type=obj_type,
                obj_data_type=obj_data_type
            ))

        return QuadStore(quads)

    @staticmethod
    def from_trig_file(filename: str) -> None:
        """Builds a QuadStore from a trig file

        This method requires RDFLib to be installed. If RDFLib is not
        installed, a NotImplementedError is raised.

        Args:
            filename: Name of the file to parse
        """

        return QuadStore.from_file(filename, "trig")

    @staticmethod
    def from_file(filename: str, file_format: str):
        """Builds a QuadStore from a file. If the file format must be
        specified. The file formats that are supported are those
        that are supported by rdflib, and additional file formats
        can be supported by installing additional rdflib serializers.

        This method requires RDFLib to be installed. If RDFLib is not
        installed, a NotImplementedError is raised.

        If RDFLib is installed, then supported file_format values are
        "trig", "trix", "ttl", and "n3". If RDFLib-JSONLD is
        installed, then "json-ld" is also valid.

        Args:
            filename: Name of the file to parse
            file_format: Format of the file to parse (e.g., trig)
        """

        g = rdflib.ConjunctiveGraph()
        g.parse(filename, format=file_format)

        without_graph_file_formats = ["ttl", "n3", "trix"]
        include_graphs = file_format not in without_graph_file_formats

        return QuadStore.from_rdflib_graph(g, include_graphs)

    def as_anzo_json_list(self) -> List:
        """Returns the quad store encoded as a list of statements, adhering
        to the Anzo statement json spec.
        """
        return [quad.as_anzo_json_dict() for quad in self.quads]

    def as_list(self) -> List:
        return list(self.quads)

    def as_rdflib_graph(self):
        """
        Returns the QuadStore as an RDFLIB Conjuctive Graph

        This method requires RDFLib to be installed. If RDFLib is not
        installed, a NotImplementedError is raised.
        """

        g = rdflib.ConjunctiveGraph()
        for prefix in self.namespace:
            g.namespace_manager.bind(prefix, rdflib.URIRef(self.namespace[prefix]))

        for stmt in self:

            # Create the rdflib subject. It depends on the type of the
            # type of the object as specified in the statement
            if stmt.sub_type == "uri":
                rdflib_sub = rdflib.URIRef(stmt.sub)
            elif stmt.sub_type == "bnode":
                rdflib_sub = rdflib.BNode(stmt.sub)
            else:
                raise ValueError(f"Invalid subject type: {stmt.sub_type}")

            # Create the rdflib object. It depends on the type of the
            # type of the object as specified in the statement
            if stmt.obj_type == "uri":
                rdflib_obj = rdflib.URIRef(stmt.obj)
            elif stmt.obj_type == "bnode":
                rdflib_obj = rdflib.BNode(stmt.obj)
            elif stmt.obj_type == "":
                rdflib_obj = rdflib.Literal(stmt.obj)
            elif stmt.obj_type == "literal" and stmt.obj_data_type:
                rdflib_obj = rdflib.Literal(stmt.obj,
                                            datatype=stmt.obj_data_type)
            else:
                rdflib_obj = rdflib.Literal(stmt.obj)

            g.add((
                rdflib_sub,
                rdflib.URIRef(stmt.pred),
                rdflib_obj,
                rdflib.URIRef(stmt.graph)
            ))
        return g

    def as_record_dictionaries(self) -> List[dict]:
        """
        Returns the quad store as a list of dictionaries.
        The return format is well suited to interface with
        pandas through the DataFrame from_dict or from_records methods.

        Returns:
            A list of dictionaries, each representing one quad.
        """

        return [quad.as_record_dict() for quad in self.quads]

    def write_to_file(self, filename: str, file_format: str) -> None:
        """
        Writes the QuadStore to a file in the specified format.

        This method requires RDFLib to be installed. If RDFLib is not
        installed, a NotImplementedError is raised.

        If RDFLib is installed, then supported file_format values are
        "trig", "trix", "ttl", and "n3". If RDFLib-JSONLD is
        installed, then "json-ld" is also valid.

        Args:
            filename: Name of the file to write to
            file_format: Format of the file (e.g., "trig")
        """

        self.as_rdflib_graph().serialize(
            destination=filename, format=file_format
        )

    def write_to_trig_file(self, filename: str) -> None:
        """
        Writes the QuadStore to a trig file.

        This method requires RDFLib to be installed. If RDFLib is not
        installed, a NotImplementedError is raised.

        Args:
            filename: Name of the file to write to
        """

        self.write_to_file(filename, "trig")

    @staticmethod
    def from_string(data: str, string_format: str) -> str:
        g = rdflib.ConjunctiveGraph()
        g.parse(data=data, format=string_format)
        without_graph_formats = ["ttl", "n3", "trix"]
        include_graphs = string_format not in without_graph_formats
        return QuadStore.from_rdflib_graph(g, include_graphs)

    @staticmethod
    def from_trig_string(data: str) -> str:
        return QuadStore.from_string(data, "trig")

    def add_prefixes(self, data: dict) -> dict:
        """
        Adds prefixes to the dict of prefixes in a QuadStore

        Args:
            data: A dictionary of prefixes and uris to add
        """
        for key, val in data.items():
            self.namespace[key] = val
        return self.namespace

    def to_string(self, string_format: str) -> str:
        return self.as_rdflib_graph().serialize(
            format=string_format
        )

    def to_trig_string(self) -> str:
        return self.to_string("trig")

    def filter(self,
               subject="",
               predicate="",
               statement_object="",
               graph=""):  # -> QuadStore:
        """Filters QuadStore on Search Terms.

        This generates a new QuadStore where the
        quads in that new store match the search
        terms provided conjunctively. Failing to
        provide a search term, or setting it to
        the empty string treats that as a wildcard
        search term. The filtering works as a
        series of gates on each quad in the store.
        Any quad that does not pass one of the
        gates will not be included in the result.

        Args:
            subject: A string. The subject that all quads in the result have.
            predicate: A string. The predicate that
                all quads in the result have.
            statement_object: A string. The object
                all quads in the result have.
            graph: A string. The graph all quads in the result have.

        Returns: A QuadStore that is the result of
            filtering conjunctively by all the args
            that were passed to it.
        """
        result = QuadStore()

        def check_match(filter_arg, quad_item):
            match = True
            if filter_arg:
                if not filter_arg == quad_item:
                    match = False
            return match

        for quad in self.quads:
            subject_matches = check_match(subject, quad.sub)
            if not subject_matches:
                continue
            predicate_matches = check_match(predicate, quad.pred)
            if not predicate_matches:
                continue
            object_matches = check_match(statement_object, quad.obj)
            if not object_matches:
                continue
            graph_matches = check_match(graph, quad.graph)
            if not graph_matches:
                continue
            result.quads.add(quad)
        return result

    def add(self, quad: Quad) -> bool:
        """ Add the given quad to a quad store.

        Args:
            quad: the quad to add

        Returns: True if the quad store did not already contain the given quad
        """
        if quad not in self.quads:
            self.quads.add(quad)
            return True
        return False

    def remove(self, quad: Quad) -> bool:
        """ Remove the given quad from a quad store.

        Args:
            quad: the quad to remove

        Returns: A boolean indicating whether the quad was found and removed
        """
        if quad in self.quads:
            self.quads.remove(quad)
            return True
        return False

    def set(self, quad: Quad) -> bool:
        """ Convenience method to "upsert" the given quad to the quad store.

        First removes any existing quads from the quad store that have the same
        graph/subject/predicate as the given quad.
        Then takes the given quad and add it to the quad store.

        Based on:
        https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html#rdflib.graph.Graph.set

        Args:
            quad: the quad to upsert
        Return:
            A boolean indicating whether any quads were removed
        """
        to_remove = self.filter(subject=quad.sub,
                                predicate=quad.pred, graph=quad.graph)
        for remove in to_remove:
            self.remove(remove)
        self.add(quad)
        return len(to_remove) > 0

    def prettify(self) -> str:
        str_list = []
        for quad in self.quads:
            str_list.append(str(quad))
        return "\n".join(str_list)

    def verbosify(self) -> str:
        str_list = []
        for quad in self.quads:
            str_list.append(quad.verbosify())
        return "\n".join(str_list)

    def __eq__(self, other_store) -> bool:
        return self.quads == other_store.quads

    def __iter__(self):
        return iter(self.quads)

    def __len__(self):
        return len(self.quads)
