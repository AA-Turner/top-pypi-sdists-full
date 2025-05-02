# /*******************************************************************************
#  * Copyright (c) 2019 - 2022 Cambridge Semantics Incorporated.
#  * All rights reserved.
#  * 
#  * Contributors:
#  *     Cambridge Semantics Incorporated
#  *******************************************************************************/

import logging
import time
import uuid
from typing import List
import pandas as pd
import urllib.parse

from .anzo_client import AnzoClient
from .quad_store import Quad, QuadStore
from .uris import (
    NAMESPACE,
    TYPE_PRED,
    DNG_PRED,
    NG_TYPE
)

logger = logging.getLogger(__name__)


class LDSManager:
    """Class for managing the state of an Anzo LinkedDataSet
    (i.e "local volume" dataset, "journal" dataset)

    The class can be used to perform operations like
    creating and deleting an Anzo LDS, as well as adding and
    clearing data from an LDS.

    All operations within this class assume that the LDS graph is itself also
        the "Dataset" graph. If this is not the case, then do not use this
        class for LDS management.

    Attributes:
        anzo_client: An AnzoClient object pointing to the Anzo
            with the LDS
        lds_uri: URI of the LDS to manage

    Usage:
        from pyanzo import AnzoClient, LDSManager
        anzo_client = AnzoClient("localhost", "8443")
        lds_uri = "http://cambridgesemantics.com/dataset/123"
        lds_manager = LDSManager(anzo_client, lds_uri)

        from pyanzo import AnzoClient, LDSManager
        anzo_client = AnzoClient("localhost", "8443")
        lds_title = "my test LDS"
        lds_manager = LDSManager.create_lds(anzo_client=anzo_client,
                                            title=lds_title)
    """

    SLEEP_TIME = 3  # need a long sleep time for dataset operations

    def __init__(self, anzo_client: AnzoClient, lds_uri: str):
        """Constructs an LDSManager for managing the state of
        an Anzo LinkedDataSet.

        As with other operations within this class, it is assumed the LDS graph
            is itself also the "Dataset" graph.

        Args:
            anzo_client: An AnzoClient object used for interacting with an Anzo
                server.
            lds_uri: The URI of the LDS. It's assumed that the
                LDS is on the server underlying the anzo client object.

        Returns:
            An LDSManager object
        """
        self.anzo_client = anzo_client
        self.lds_uri = lds_uri

    @classmethod
    def create_lds(cls, anzo_client: AnzoClient, title: str,
                   statements: QuadStore = None,
                   ontologies: List[str] = None) -> 'LDSManager':
        """Creates an LDS on Anzo with the given title.
        Adds the statements in the given quad store to the LDS, if applicable.
        Adds references from the LDS to the given ontologies, if applicable.

        As is assumed with other operations within this class, the LDS graph
            is itself also the "Dataset" graph.

        Args:
            anzo_client: An AnzoClient object used for interacting with an Anzo
                server.
            title: Title to give the LDS that is created.
            statements: (optional) QuadStore of statements to add to the LDS
                once it's creatd
            ontologies: (optional) Ontology URIs that the LDS will reference
                when created via the ld:ontology predicate.


        Returns:
            LDSManager that manages the created LDS
        """

        lds_uri = NAMESPACE["lds"] + str(uuid.uuid1())
        cls._add_lds_graph(anzo_client, lds_uri,
                           title, ontologies)
        cls._register_lds_graph(anzo_client, lds_uri)
        lds_mananger = cls(anzo_client, lds_uri)
        if statements:
            lds_mananger.add_to_lds(statements)
        time.sleep(cls.SLEEP_TIME)
        return lds_mananger

    def add_to_lds(self, statements: QuadStore):
        """Adds the statements in the provided QuadStore to the managed LDS.
        This operation takes care of all that's needed to properly add the
        statements to the LDS; specifically, it adds anzo:defaultNamedGraph
        references from the LDS to the named graphs of the statements

        Args:
            statements: QuadStore of statements to add to the LDS.
                The statements must be quads (they must contain a NamedGraph).

        """
        qs = QuadStore()
        df = pd.DataFrame.from_dict(statements.as_record_dictionaries())
        for g in df['g'].unique():
            qs.add(Quad(self.lds_uri, DNG_PRED, g, self.lds_uri))
        for stmt in statements:
            qs.add(stmt)
        self.anzo_client.add(qs)

    def overwrite_lds(self, statements: QuadStore):
        """Clears the managed LDS of all existing named graphs and statements,
        and then adds the statements in the provided QuadStore to the LDS.
        This is simply a utility method that first executes clear_lds(),
        and then add_to_lds(QuadStore).

        Args:
            statements: QuadStore of statements to add to the LDS.
                The statements must be quads (they must contain a NamedGraph).
        """
        self.clear_lds()
        self.add_to_lds(statements)

    def clear_lds(self):
        """Removes all of the managed LDS's named graphs and their contents
        from the journal. This leaves you with an "empty" LDS - the LDS graph
        itself remains, but it points to nothing.
        """

        # populate quad store with magic triples from all LDS graphs
        to_remove = QuadStore()
        res = self.anzo_client.query_journal("select distinct ?g where { <%s> <%s> ?g . }" % (self.lds_uri, DNG_PRED)).as_table_results().as_list()
        for r in res:
            graph_uri = r.pop()
            # in case LDS references itself, do not delete
            if r != self.lds_uri:
                to_remove.add(Quad(self.lds_uri, DNG_PRED,
                                   graph_uri, self.lds_uri))
                to_remove.add(magic_triple(graph_uri))

        # remove magic triples
        if len(to_remove) > 0:
            self.anzo_client.remove(to_remove)

    def delete_lds(self):
        """Clears the managed LDS of its contents (if applicable) and then
        deletes/deregisters the LDS itself. This method first performs a
        clear_lds() operation, then performs the necessary LDS deregistration.
        """

        self.clear_lds()
        self._deregister_lds_graph(self.anzo_client, self.lds_uri)
        self.anzo_client.remove(QuadStore({magic_triple(self.lds_uri)}))

    @classmethod
    def _add_lds_graph(cls, anzo_client: AnzoClient, lds_uri: str,
                       title: str, ontologies: List[str] = None):

        LDS_TYPE = NAMESPACE["cs-ld"] + "LinkedDataSet"
        DS_TYPE = NAMESPACE["cs-ld"] + "Dataset"
        DS_PRED = NAMESPACE["cs-ld"] + "dataset"
        ONTO_PRED = NAMESPACE["cs-ld"] + "ontology"
        DC_TITLE = NAMESPACE["dc"] + "title"

        qs = QuadStore()
        qs.add(Quad(lds_uri, TYPE_PRED, LDS_TYPE, lds_uri))
        qs.add(Quad(lds_uri, TYPE_PRED, DS_TYPE, lds_uri))
        qs.add(Quad(lds_uri, DC_TITLE, title, lds_uri, obj_type="literal"))
        qs.add(Quad(lds_uri, DS_PRED, lds_uri, lds_uri))

        if ontologies:
            for onto in ontologies:
                qs.add(Quad(lds_uri, ONTO_PRED, onto, lds_uri))

        anzo_client.add(qs)

    @classmethod
    def _register_lds_graph(cls, anzo_client: AnzoClient, lds_uri: str):
        qs = cls._lds_registry_statements(lds_uri)
        anzo_client.add(qs)

    @classmethod
    def _deregister_lds_graph(cls, anzo_client: AnzoClient, lds_uri: str):
        qs = cls._lds_registry_statements(lds_uri)
        anzo_client.remove(qs)

    @staticmethod
    def _lds_registry_statements(lds_uri: str) -> QuadStore:
        LDS_REG_URI = "http://cambridgesemantics.com/registries/LinkedDataSets"  # noqa
        DS_REG_URI = "http://cambridgesemantics.com/registries/DataSets"

        qs = QuadStore()
        qs.add(Quad(LDS_REG_URI, DNG_PRED, lds_uri, LDS_REG_URI))
        qs.add(Quad(DS_REG_URI, DNG_PRED, lds_uri, DS_REG_URI))
        return qs


def magic_triple(graph_uri: str) -> Quad:
    """Utility method to construct a Quad representing the "magic triple" for
    the given graph URI.

    Args:
        graph_uri: URI of the graph

    Returns:
        Quad representing the "magic triple" for the given graph URI
    """
    return Quad(graph_uri, TYPE_PRED, NG_TYPE,
                md_graph(graph_uri))


def md_graph(graph_uri: str) -> str:
    """Utility method to construct the metadata graph URI for the given graph URI.

    Args:
        graph_uri: URI of the graph

    Returns:
        The metadata graph URI for the given graph URI
    """
    encoded = urllib.parse.quote(graph_uri, safe="")
    return "http://openanzo.org/metadataGraphs(%s)" % encoded
