# /*******************************************************************************
#  * Copyright (c) 2019 - 2022 Cambridge Semantics Incorporated.
#  * All rights reserved.
#  * 
#  * Contributors:
#  *     Cambridge Semantics Incorporated
#  *******************************************************************************/

TYPE_PRED = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
ALL_NAMED_GRAPHS_URI = "http://openanzo.org/namedGraphs/reserved/graphs/ALL"
SYSTEM_DATASOURCE_URI = "http://openanzo.org/datasource/systemDatasource"

NAMESPACE = {
    "anzo":             "http://openanzo.org/ontologies/2008/07/Anzo#",
    "cs-ds":            "http://cambridgesemantics.com/datasets/",
    "cs-ld":            "http://cambridgesemantics.com/ontologies/2009/05/LinkedData#",
    "dc":               "http://purl.org/dc/elements/1.1/",
    "du-ls":            "http://openanzo.org/ontologies/2008/07/ASDL/IngestManager/DistributedUnstructuredLoadService#",
    "etl-ls":           "http://openanzo.org/ontologies/2008/07/ASDL/IngestManager/EtlLoadService#",
    "gm-ls":            "http://openanzo.org/ontologies/2008/07/ASDL/IngestManager/GraphmartLoadService#",
    "im":               "http://openanzo.org/ontologies/2008/07/ASDL/IngestManager#",
    "lds":              "http://cambridgesemantics.com/LinkedDataSet/",
    "orch":             "http://openanzo.org/ontologies/2008/07/ASDL/Orchestration#",
    "reg":              "http://cambridgesemantics.com/registries/",
    "registries":       "http://openanzo.org/registries/",
    "remoteconnection": "http://openanzo.org/ontologies/2008/07/RemoteConnection#",
    "role":             "http://openanzo.org/Role/",
    "ss":               "http://openanzo.org/ontologies/2008/07/SemanticService#",
    "svc":              "http://cambridgesemantics.com/service/",
    "system":           "http://openanzo.org/ontologies/2008/07/System#"
}

DNG_PRED = NAMESPACE["anzo"] + "defaultNamedGraph"
NG_TYPE = NAMESPACE["anzo"] + "NamedGraph"
