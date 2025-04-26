from simple_ddl_parser import DDLParser

ddl = """
CREATE TABLE `table_notes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `notes` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
);"""
result = DDLParser(ddl, debug=True).run(group_by_type=True, 
                            output_mode="mysql",
                            )

import pprint

pprint.pprint(result)