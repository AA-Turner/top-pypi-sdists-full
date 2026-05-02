import hashlib
import logging
import os
from pathlib import Path
from typing import Optional, List

from neo4j import GraphDatabase

from ghostcoder import FileRepository
from ghostcoder.codeblocks import CodeBlock
from ghostcoder.schema import File, Folder, Project, Dependency
from ghostcoder.utils import count_tokens


def get_parent_path(path):
    parent_path = os.path.dirname(path)
    return "/" if parent_path == '' or parent_path == path else parent_path


logger = logging.getLogger(__name__)


class GraphStore:

    def __init__(
        self,
        username: str,
        password: str,
        url: str,
        repository: str,
        database: str = "neo4j"
    ) -> None:
        try:
            import neo4j
        except ImportError:
            raise ImportError("Please install neo4j: pip install neo4j")
        try:
            self._driver = GraphDatabase.driver(url, auth=(username, password))
        except Exception as e:
            logger.error("Failed to create the driver:", e)

        self._database = database
        self._repository = repository

        self._create_constraint("Project", "project_id")
        self._create_constraint("Dependency", "dependency_id")
        self._create_constraint("Folder", "folder_id")
        self._create_constraint("File", "file_id")
        self._create_constraint("Dependency", "dependency_id")

    def _query(self, query, parameters=None):
        assert self._driver is not None, "Driver not initialized!"

        with self._driver.session(database=self._database) as session:
            try:
                response = list(session.run(query, parameters))
            except Exception as e:
                logger.warning(f"Query with parameters {parameters} failed:", e)
                raise
        return response

    def _create_constraint(self, label, property):
        with self._driver.session() as session:
            session.run(f"CREATE CONSTRAINT {label}_{property} IF NOT EXISTS FOR (n:{label}) REQUIRE n.{property} IS UNIQUE")

    def reset(self):
        query = """MATCH (n)
WHERE n.repository = $repository
DETACH DELETE n"""

        response = self._query(query, parameters={
            "repository": self._repository
        })

        logger.info(f"Deleted codeblocks from repository '{self._repository}': {response}")

    def read_incoming_relations(self, file_path: str, block_path: List[str]):
        repository_id = f"{self._repository}"
        block_id = f"{repository_id}|{file_path}|{'.'.join(block_path)}"

        query = """
        MATCH (codeblock {block_id: $block_id})
        OPTIONAL MATCH (relatedIn)-[incoming]->(codeblock)
        RETURN codeblock, 
               collect({type: type(incoming), direction: 'incoming', related_node: relatedIn}) as incomingRelations
        """

        result = self._query(query, parameters={
            "block_id": block_id
        })

        if result:
            record = result[0]
            codeblock_info = record['codeblock']
            relations = {
                "incoming": record['incomingRelations']
            }
            return {
                "codeblock": codeblock_info,
                "relations": relations
            }
        else:
            return {"codeblock": None, "relations": {"outgoing": [], "incoming": []}}

    def create_project(self, project: Project):
        project_id = f"{self._repository}|{project.name}"
        logger.debug(f"Creating project [{project_id}]")

        query = """
        MERGE (repository:Repository {name: $repository})

        CREATE (project:Project {project_id: $project_id, name: $name, repository: $repository, version: $version, created_at: timestamp()})
        """

        self._query(query, parameters={
            "name": project.name,
            "version": project.version,
            "project_id": project_id,
            "repository": self._repository
        })

    def create_dependency(self, project: Project, dependency: Dependency):
        dependency_id = f"{self._repository}|{dependency.name}"
        logger.debug(f"Creating dependency [{dependency_id}]")
        project_id = f"{self._repository}|{project.name}"

        query = """
        CREATE (dependency:Dependency {dependency_id: $dependency_id, name: $name, repository: $repository, version: $version, scope: $scope, created_at: timestamp()})

        WITH dependency
        MATCH (project:Project {project_id: $project_id})
        MERGE (project)-[:DEPENDS_ON]->(dependency)
        """

        self._query(query, parameters={
            "dependency_id": dependency_id,
            "name": dependency.name,
            "version": dependency.version,
            "scope": dependency.scope,
            "project_id": project_id,
            "repository": self._repository,
        })

    def create_folder(self, folder: Folder):
        folder_id = f"{self._repository}|{folder.path}"
        logger.debug(f"Creating folder [{folder_id}]")

        query = """      
        CREATE (folder:Folder {folder_id: $folder_id, name: $name, path: $path, repository: $repository, created_at: timestamp()})

        WITH folder
        MATCH (repository:Repository {name: $repository})        
        MERGE (folder)-[:STORED_IN]->(repository)
        """

        self._query(query, parameters={
            "folder_id": folder_id,
            "name": folder.name,
            "path": folder.path,
            "repository": self._repository
        })

    def create_file(self, file: File):
        file_id = f"{self._repository}|{file.path}"
        logger.debug(f"Creating file [{file_id}]")

        query = """
        CREATE (file:File {file_id: $file_id, name: $name, path: $path, hash: $hash, repository: $repository, created_at: timestamp()})

        WITH file
        MATCH (repository:Repository {name: $repository})        
        MERGE (file)-[:STORED_IN]->(repository)
        """

        self._query(query, parameters={
            "name": file.name,
            "path": file.path,
            "hash": file.hash,
            "repository": self._repository,
            "file_id": file_id
        })

    def create_codeblock(self, codeblock: CodeBlock):
        file_path = codeblock.root().file_path
        if not file_path:
            logger.error(f"Codeblock missing file_path: {codeblock.path_string()}")
            return

        block_path = codeblock.path_string()
        block_id = f"{self._repository}|{file_path}|{block_path}"
        logger.debug(f"Upsert codeblock [{block_id}]")

        file_id = f"{self._repository}|{file_path}"

        contents = codeblock.to_string()
        tokens = count_tokens(contents)  # TODO: Move to CodeBlock
        hash = hashlib.sha256(contents.encode("utf-8")).hexdigest()  # TODO: Move to CodeBlock

        if codeblock.identifier:
            block_name = codeblock.identifier
        else:
            block_name = f"<{file_path.split('/')[-1]}>"

        query = f"""
           CREATE (codeblock:{codeblock.type.value} {{
               block_id: $block_id,
               block_path: $block_path,
               name: $block_name,
               hash: $block_hash,
               tokens: $block_tokens,
               repository: $repository,
               created_at: timestamp()
           }})

           WITH codeblock
           MATCH (file:File {{file_id: $file_id}})
           MERGE (codeblock)-[:PART_OF]->(file)
           """

        if codeblock.parent:
            parent_block_path = ".".join(codeblock.parent.full_path())
            parent_block_id = f"{self._repository}|{file_path}|{parent_block_path}"

            query += f"""
        FOREACH (ignoreMe IN CASE WHEN $parent_block_id IS NOT NULL THEN [1] ELSE [] END |
            MERGE (parent:{codeblock.parent.type.value} {{block_id: $parent_block_id}})
            MERGE (parent)-[:HAS]->(codeblock)
        )
        """
        else:
            parent_block_id = None

        self._query(query, parameters={
            "repository": self._repository,
            "file_id": file_id,
            "block_name": block_name,
            "block_path": codeblock.path_string(),
            "block_hash": hash,
            "block_tokens": tokens,
            "block_id": block_id,
            "parent_block_id": parent_block_id,
        })

    def upsert_project(self, project: Project):
        project_id = f"{self._repository}|{project.name}"
        logger.debug(f"Upserting project [{project_id}]")

        query = """
        MERGE (repository:Repository {name: $repository})
        
        MERGE (project:Project {project_id: $project_id})
        ON CREATE SET
            project.name = $name,
            project.repository = $repository,
            project.created_at = timestamp()
        SET
            project.version = $version,
            project.last_updated_at = timestamp()

        MERGE (project)-[rel:ASSOCIATED_WITH]->(repository)
        ON CREATE SET
            rel.created_at = timestamp()
        ON MATCH SET
            rel.last_updated_at = timestamp()
        """

        self._query(query, parameters={
            "name": project.name,
            "version": project.version,
            "project_id": project_id,
            "repository": self._repository
        })

    def upsert_dependency(self, project: Project, dependency: Dependency):
        dependency_id = f"{self._repository}|{dependency.name}"
        logger.debug(f"Upserting dependency [{dependency_id}]")
        project_id = f"{self._repository}|{project.name}"

        query = """
        MERGE (dependency:Dependency {dependency_id: $dependency_id})
        ON CREATE SET
            dependency.name = $name,
            dependency.repository = $repository,
            dependency.created_at = timestamp()
        SET
            dependency.version = $version,
            dependency.scope = $scope,
            dependency.last_updated_at = timestamp()
        
        WITH dependency
        MATCH (project:Project {project_id: $project_id})
        MERGE (project)-[rel:DEPENDS_ON]->(dependency)
        ON CREATE SET
            rel.scope = $scope,
            rel.created_at = timestamp()
        ON MATCH SET
            rel.scope = $scope,
            rel.last_updated_at = timestamp()
        """

        self._query(query, parameters={
            "dependency_id": dependency_id,
            "name": dependency.name,
            "version": dependency.version,
            "scope": dependency.scope,
            "project_id": project_id,
            "repository": self._repository,
        })

    def upsert_folder(self, folder: Folder):
        folder_id = f"{self._repository}|{folder.path}"
        logger.debug(f"Upsert folder [{folder_id}]")

        parent_folder_path = get_parent_path(folder.path)
        parent_folder_id = f"{self._repository}|{parent_folder_path}"

        query = """      
        MERGE (folder:Folder {folder_id: $folder_id})
        ON CREATE SET
            folder.name = $name,
            folder.path = $path,
            folder.repository = $repository,
            folder.created_at = timestamp()
        SET
            folder.last_updated_at = timestamp()
        
        WITH folder
        OPTIONAL MATCH (parent:Folder {folder_id: $parent_folder_id})
        FOREACH (p IN CASE WHEN parent IS NOT NULL THEN [1] ELSE [] END |
            MERGE (parent)-[:CONTAINS]->(folder)
        )

        WITH folder
        MATCH (repository:Repository {name: $repository})        
        MERGE (folder)-[:STORED_IN]->(repository)
        """

        self._query(query, parameters={
                "parent_folder_id": parent_folder_id,
                "folder_id": folder_id,
                "name": folder.name,
                "path": folder.path,
                "repository": self._repository
        })

    def upsert_file(self, file: File):
        file_id = f"{self._repository}|{file.path}"
        logger.debug(f"Upsert file [{file_id}]")

        folder_id = f"{self._repository}|{get_parent_path(file.path)}"

        query = """
        MERGE (file:File {
            file_id: $file_id
        })
        ON CREATE SET
            file.name = $name,
            file.path = $path,
            file.hash = $hash,
            file.repository = $repository,
            file.created_at = timestamp()
        SET
            file.hash = $hash,
            file.last_updated_at = timestamp()
        
        WITH file
        MATCH (repository:Repository {name: $repository})        
        MERGE (file)-[:STORED_IN]->(repository)
        
        WITH file
        MATCH (folder:Folder {folder_id: $folder_id})
        MERGE (folder)-[:CONTAINS]->(file)
        """

        self._query(query, parameters={
            "name": file.name,
            "path": file.path,
            "hash": file.hash,
            "repository": self._repository,
            "file_id": file_id,
            "folder_id": folder_id,
        })

    def upsert_codeblock(self, codeblock: CodeBlock):
        file_path = codeblock.root().file_path
        if not file_path:
            logger.error(f"Codeblock missing file_path: {codeblock.path_string()}")
            return

        block_path = codeblock.path_string()
        block_id = f"{self._repository}|{file_path}|{block_path}"
        logger.debug(f"Upsert codeblock [{block_id}]")

        file_id = f"{self._repository}|{file_path}"

        contents = codeblock.to_string()
        tokens = count_tokens(contents)  # TODO: Move to CodeBlock
        hash = hashlib.sha256(contents.encode("utf-8")).hexdigest()  # TODO: Move to CodeBlock

        query = f"""
        MERGE (codeblock:{codeblock.type.value} {{
            block_id: $block_id
        }})
        ON CREATE SET
            codeblock.block_path = $block_path,
            codeblock.name = $block_name,
            codeblock.hash = $block_hash,
            codeblock.tokens = $block_tokens,
            codeblock.repository = $repository
        
        WITH codeblock
        MATCH (file:File {{file_id: $file_id}})
        MERGE (codeblock)-[:PART_OF]->(file)
        """

        if codeblock.parent:
            parent_block_path = ".".join(codeblock.parent.full_path())
            parent_block_id = f"{self._repository}|{file_path}|{parent_block_path}"

            query += f"""
        FOREACH (ignoreMe IN CASE WHEN $parent_block_id IS NOT NULL THEN [1] ELSE [] END |
            MERGE (parent:{codeblock.parent.type.value} {{block_id: $parent_block_id}})
            MERGE (parent)-[:HAS]->(codeblock)
        )
        """
        else:
            parent_block_id = None

        self._query(query, parameters={
            "repository": self._repository,
            "file_id": file_id,
            "block_name": codeblock.identifier or "<no name>",
            "block_path": codeblock.path_string(),
            "block_hash": hash,
            "block_tokens": tokens,
            "block_id": block_id,
            "parent_block_id": parent_block_id,
        })

    def upsert_relationship(self,
                            relationship: str,
                            from_block: CodeBlock,
                            to_block: CodeBlock):

        from_block_id = f"{self._repository}|{from_block.root().file_path}|{from_block.path_string()}"
        to_block_id = f"{self._repository}|{to_block.root().file_path}|{to_block.path_string()}"
        logger.debug(f"Inserting relationship {relationship} from {from_block_id} to {to_block_id}")

        query = f"""
        MATCH (fromBlock:{from_block.type.value} {{block_id: $from_block_id}})
        MATCH (toBlock:{to_block.type.value} {{block_id: $to_block_id}})
        
        MERGE (fromBlock)-[rel:{relationship}]->(toBlock)
        ON CREATE SET
            rel.created_at = timestamp()
        ON MATCH SET
            rel.last_updated_at = timestamp()        
        """

        self._query(query, parameters={
            "repository": self._repository,
            "from_block_id": from_block_id,
            "to_block_id": to_block_id,
        })

    def upsert_dependency_relationship(self,
                            relationship: str,
                            from_block: CodeBlock,
                            dependency: str):

        from_block_id = f"{self._repository}|{from_block.root().file_path}|{from_block.path_string()}"
        to_dependency_id = f"{self._repository}|{dependency}"

        print(f"Inserting relationship {relationship} from {from_block_id} to dependency {to_dependency_id}")

        query = f"""
        MATCH (fromBlock:{from_block.type.value} {{block_id: $from_block_id}})
        MATCH (toDependency:Dependency {{to_dependency_id: $to_dependency_id}})

        MERGE (fromBlock)-[rel:{relationship}]->(toDependency)
        ON CREATE SET
            rel.created_at = timestamp()
        ON MATCH SET
            rel.last_updated_at = timestamp()        
        """

        self._query(query, parameters={
            "repository": self._repository,
            "from_block_id": from_block_id,
            "to_dependency_id": to_dependency_id,
        })
