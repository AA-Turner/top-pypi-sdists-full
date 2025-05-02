# /*******************************************************************************
#  * Copyright (c) 2019 - 2022 Cambridge Semantics Incorporated.
#  * All rights reserved.
#  * 
#  * Contributors:
#  *     Cambridge Semantics Incorporated
#  *******************************************************************************/

import unittest
import time
import os

from pyanzo import (
    AnzoClient,
    QuadStore
)

from pyanzo.orchestration_wrapper import (
    OrchestrationWrapper,
    IngestionComponentStatus,
)

from .test_common import (
    GRAPHMART,
    DOMAIN,
    PORT,
    USERNAME,
    PASSWORD,
    log_while_running_tests,
)

# log_while_running_tests()

class TestOrchestrationWrapper(unittest.TestCase):
    im_uri = "http://cambridgesemantics.com/service/devIngestManager"

    def setUp(self) -> None:
        self.anzo_client = AnzoClient(
            domain=DOMAIN, username=USERNAME, password=PASSWORD, port=PORT
        )

    @unittest.skip("Integration Test")
    def test_orchestration_wrapper(self):
        osm = OrchestrationWrapper(self.anzo_client, self.im_uri, [])

        osm.start()
        run_status = osm.block_until_complete(2000)

    def test_ingestion_component_status_construction1(self) -> None:

        ing_comp_trig = """
            @prefix ns1: <urn://etl/> .
            @prefix ns2: <http://openanzo.org/ontologies/2008/07/ASDL/IngestManager#> .

            ns1:4f558d33-dadd-4cdb-b4a4-7d94e069423f {
                   ns1:4f558d33-dadd-4cdb-b4a4-7d94e069423f a ns2:IngestionComponent ;
                       ns2:componentDescription "NULL" ;
                       ns2:componentLoadService <http://cambridgesemantics.com/Project/6bdebd2d-a585-480c-31d2-ff1c39eb3130/6bdebd2d-a585-480c-31d2-ff1c39eb3130/7696237e-1c7b-c488-6a6d-       9bdd6bdfb6b2/Job/919fb444-80e7-19b5-25a5-63b6903a2ba1> ;
                       ns2:componentName "Load sample" ;
                       ns2:componentStatus "STARTING" .
             }
             """  # noqa
        uri = "urn://etl/4f558d33-dadd-4cdb-b4a4-7d94e069423f"

        ing_comp_qs = QuadStore.from_trig_string(ing_comp_trig)
        ics = IngestionComponentStatus.from_quadstore(ing_comp_qs, uri)
        ics2 = IngestionComponentStatus(
            uri, "Load sample", "STARTING", False, "", "", "", ""
        )

        self.assertEqual(ics, ics2)

    def test_ingestion_component_status_construction2(self):

        ing_comp_trig = """
            @prefix ns1: <urn://etl/> .
            @prefix ns2: <http://openanzo.org/ontologies/2008/07/ASDL/IngestManager#> .
            @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

            ns1:d4f6d003-0545-4039-87ae-4da95fafca06 {
                ns1:d4f6d003-0545-4039-87ae-4da95fafca06 a ns2:IngestionComponent,
                        <http://openanzo.org/ontologies/2008/07/ASDL/IngestManager/EtlLoadService#StructuredIngestionComponent> ;
                    ns2:componentDescription "Job began at 2021-04-27T14:32:56.071Z and ended at 2021-04-27T14:33:02.039Z." ;
                    ns2:componentLoadService <http://cambridgesemantics.com/Project/6bdebd2d-a585-480c-31d2-ff1c39eb3130/6bdebd2d-a585-480c-31d2-ff1c39eb3130/7696237e-1c7b-c488-6a6d-9bdd6bdfb6b2/Job/919fb444-80e7-19b5-25a5-63b6903a2ba1> ;
                    #ns2:componentName "ETL ingestion component: Loadsample_sample" ;
                    ns2:componentName "" ;
                    ns2:componentStatus "success" ;
                    ns2:componentSucceeded true ;
                    ns2:contextGraph <http://cambridgesemantics.com/Project/6bdebd2d-a585-480c-31d2-ff1c39eb3130/6bdebd2d-a585-480c-31d2-ff1c39eb3130/7696237e-1c7b-c488-6a6d-9bdd6bdfb6b2/Job/919fb444-80e7-19b5-25a5-63b6903a2ba1/6> ;
                    ns2:index "1"^^xsd:int ;
                    ns2:ingestEndTime "2021-04-27T14:33:02.409000+00:00"^^xsd:dateTime ;
                    ns2:ingestStartTime "2021-04-27T14:32:49.129000+00:00"^^xsd:dateTime ;
                    ns2:newFldsUri <http://csi.com/FileBasedLinkedDataSet/faf590ddadf853e4d213b8ac823eb194> ;
                    ns2:percentComplete 1e+00 ;
                    ns2:previousFldsUri <http://csi.com/FileBasedLinkedDataSet/faf590ddadf853e4d213b8ac823eb194> .
            }

            """  # noqa
        uri = "urn://etl/4f558d33-dadd-4cdb-b4a4-7d94e069423f"

        ing_comp_qs = QuadStore.from_trig_string(ing_comp_trig)
        ics = IngestionComponentStatus.from_quadstore(ing_comp_qs, uri)
        ics2 = IngestionComponentStatus(
            uri, "", "success", True, "2021-04-27T14:32:49.129000+00:00",
            "2021-04-27T14:33:02.409000+00:00", "1", "1.0"
        )

        self.assertEqual(ics, ics2)
