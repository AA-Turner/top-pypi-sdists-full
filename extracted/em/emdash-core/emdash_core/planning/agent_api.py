"""Graph traversal API for AI agents."""

from typing import Optional

from ..graph.connection import KuzuConnection, get_connection
from ..utils.logger import log


class AgentAPI:
    """Graph traversal API for AI coding agents."""

    def __init__(self, connection: Optional[KuzuConnection] = None):
        """Initialize agent API.

        Args:
            connection: Neo4j connection. If None, uses global connection.
        """
        self.connection = connection or get_connection()

    def get_file_dependencies(self, file_path: str) -> dict:
        """Get files that import/are imported by this file.

        Args:
            file_path: Path to the file

        Returns:
            Dictionary with imports and imported_by lists
        """
        with self.connection.session() as session:
            # Get files this file imports
            imports_result = session.run("""
                MATCH (f:File)-[:IMPORTS]->(m:Module)
                WHERE f.path ENDS WITH $file_path
                RETURN m.name as module_name,
                       m.is_external as is_external
            """, file_path=file_path)
            imports = [dict(r) for r in imports_result]

            # Get files that import modules from this file
            # Query functions and classes separately (Kuzu doesn't support | in rel types)
            func_result = session.run("""
                MATCH (f:File)-[:CONTAINS_FUNCTION]->(entity:Function)
                WHERE f.path ENDS WITH $file_path
                WITH entity.qualified_name as qn
                MATCH (other:File)-[:IMPORTS]->(m:Module)
                WHERE m.name CONTAINS qn OR m.import_path CONTAINS qn
                RETURN DISTINCT other.path as file_path
            """, file_path=file_path)

            class_result = session.run("""
                MATCH (f:File)-[:CONTAINS_CLASS]->(entity:Class)
                WHERE f.path ENDS WITH $file_path
                WITH entity.qualified_name as qn
                MATCH (other:File)-[:IMPORTS]->(m:Module)
                WHERE m.name CONTAINS qn OR m.import_path CONTAINS qn
                RETURN DISTINCT other.path as file_path
            """, file_path=file_path)

            imported_by = list(set(
                [r["file_path"] for r in func_result] +
                [r["file_path"] for r in class_result]
            ))

            return {
                "file_path": file_path,
                "imports": imports,
                "imported_by": imported_by,
            }

    def get_function_callers(self, qualified_name: str) -> list[dict]:
        """Find all functions that call this function.

        Args:
            qualified_name: Qualified name of the function

        Returns:
            List of calling functions with metadata
        """
        with self.connection.session() as session:
            result = session.run("""
                MATCH (caller:Function)-[:CALLS]->(f:Function {qualified_name: $qualified_name})
                RETURN caller.name as name,
                       caller.qualified_name as qualified_name,
                       caller.file_path as file_path,
                       caller.is_method as is_method
                ORDER BY caller.name
            """, qualified_name=qualified_name)

            return [dict(r) for r in result]

    def get_function_callees(self, qualified_name: str) -> list[dict]:
        """Find all functions called by this function.

        Args:
            qualified_name: Qualified name of the function

        Returns:
            List of called functions with metadata
        """
        with self.connection.session() as session:
            result = session.run("""
                MATCH (f:Function {qualified_name: $qualified_name})-[:CALLS]->(callee:Function)
                RETURN callee.name as name,
                       callee.qualified_name as qualified_name,
                       callee.file_path as file_path,
                       callee.is_method as is_method
                ORDER BY callee.name
            """, qualified_name=qualified_name)

            return [dict(r) for r in result]

    def get_class_hierarchy(self, class_name: str) -> dict:
        """Get inheritance tree for a class.

        Args:
            class_name: Name or qualified name of the class

        Returns:
            Dictionary with parents and children
        """
        with self.connection.session() as session:
            # Get parent classes
            parents_result = session.run("""
                MATCH (c:Class)-[:INHERITS_FROM]->(parent:Class)
                WHERE c.name = $class_name OR c.qualified_name = $class_name
                RETURN parent.name as name,
                       parent.qualified_name as qualified_name,
                       parent.file_path as file_path
            """, class_name=class_name)
            parents = [dict(r) for r in parents_result]

            # Get child classes
            children_result = session.run("""
                MATCH (child:Class)-[:INHERITS_FROM]->(c:Class)
                WHERE c.name = $class_name OR c.qualified_name = $class_name
                RETURN child.name as name,
                       child.qualified_name as qualified_name,
                       child.file_path as file_path
            """, class_name=class_name)
            children = [dict(r) for r in children_result]

            return {
                "class_name": class_name,
                "parents": parents,
                "children": children,
            }

    def get_file_history(self, file_path: str, limit: int = 10) -> dict:
        """Get recent commits that modified this file.

        Args:
            file_path: Path to the file
            limit: Maximum number of commits to return

        Returns:
            Dictionary with file_path and commits list
        """
        with self.connection.session() as session:
            result = session.run("""
                MATCH (c:GitCommit)-[mod:COMMIT_MODIFIES]->(f:File)
                WHERE f.path ENDS WITH $file_path
                RETURN c.sha as sha,
                       c.message as message,
                       c.author_name as author,
                       c.timestamp as timestamp,
                       mod.change_type as change_type,
                       mod.insertions as insertions,
                       mod.deletions as deletions
                ORDER BY c.timestamp DESC
                LIMIT $limit
            """, file_path=file_path, limit=limit)

            commits = [dict(r) for r in result]

            return {
                "file_path": file_path,
                "commits": commits,
            }

    def get_community_overview(self, community_id: int) -> dict:
        """Get summary of a code community.

        Args:
            community_id: The community ID

        Returns:
            Dictionary with community summary
        """
        with self.connection.session() as session:
            # Get member counts by type
            result = session.run("""
                MATCH (n)
                WHERE n.community = $community_id
                AND (n:Class OR n:Function)
                WITH label(n) as type, n
                RETURN type,
                       count(n) as count,
                       collect(n.name)[0:10] as sample_names
            """, community_id=community_id)

            members_by_type = {r["type"]: {"count": r["count"], "samples": r["sample_names"]}
                              for r in result}

            # Get files in this community (separate queries for Kuzu compatibility)
            func_files = session.run("""
                MATCH (f:File)-[:CONTAINS_FUNCTION]->(n:Function)
                WHERE n.community = $community_id
                RETURN DISTINCT f.path as file_path
                LIMIT 10
            """, community_id=community_id)

            class_files = session.run("""
                MATCH (f:File)-[:CONTAINS_CLASS]->(n:Class)
                WHERE n.community = $community_id
                RETURN DISTINCT f.path as file_path
                LIMIT 10
            """, community_id=community_id)

            files = list(set(
                [r["file_path"] for r in func_files] +
                [r["file_path"] for r in class_files]
            ))[:10]

            return {
                "community_id": community_id,
                "members_by_type": members_by_type,
                "sample_files": files,
            }

    def get_author_expertise(self, email: str) -> dict:
        """Get files and areas an author has worked on.

        Args:
            email: Author's email

        Returns:
            Dictionary with author expertise summary
        """
        with self.connection.session() as session:
            # Get author info
            author_result = session.run("""
                MATCH (a:Author {email: $email})
                RETURN a.name as name,
                       a.total_commits as total_commits,
                       a.total_lines_added as lines_added,
                       a.total_lines_deleted as lines_deleted
            """, email=email)
            author = author_result.single()

            if not author:
                return {"error": f"Author not found: {email}"}

            # Get most modified files
            files_result = session.run("""
                MATCH (a:Author {email: $email})<-[:AUTHORED_BY]-(c:GitCommit)-[:COMMIT_MODIFIES]->(f:File)
                WITH f.path as file_path, count(c) as commit_count
                RETURN file_path, commit_count
                ORDER BY commit_count DESC
                LIMIT 10
            """, email=email)
            top_files = [dict(r) for r in files_result]

            # Get communities the author has worked in (separate queries for Kuzu)
            func_communities = session.run("""
                MATCH (a:Author {email: $email})<-[:AUTHORED_BY]-(c:GitCommit)-[:COMMIT_MODIFIES]->(f:File)
                MATCH (f)-[:CONTAINS_FUNCTION]->(entity:Function)
                WHERE entity.community IS NOT NULL
                WITH entity.community as community_id, count(DISTINCT c) as commit_count
                RETURN community_id, commit_count
                ORDER BY commit_count DESC
                LIMIT 5
            """, email=email)

            class_communities = session.run("""
                MATCH (a:Author {email: $email})<-[:AUTHORED_BY]-(c:GitCommit)-[:COMMIT_MODIFIES]->(f:File)
                MATCH (f)-[:CONTAINS_CLASS]->(entity:Class)
                WHERE entity.community IS NOT NULL
                WITH entity.community as community_id, count(DISTINCT c) as commit_count
                RETURN community_id, commit_count
                ORDER BY commit_count DESC
                LIMIT 5
            """, email=email)

            # Combine and deduplicate by community_id, keeping highest commit_count
            community_map = {}
            for r in list(func_communities) + list(class_communities):
                cid = r["community_id"]
                cc = r["commit_count"]
                if cid not in community_map or cc > community_map[cid]:
                    community_map[cid] = cc
            communities = [
                {"community_id": cid, "commit_count": cc}
                for cid, cc in sorted(community_map.items(), key=lambda x: -x[1])[:5]
            ]

            return {
                "email": email,
                "name": author["name"],
                "total_commits": author["total_commits"],
                "lines_added": author["lines_added"],
                "lines_deleted": author["lines_deleted"],
                "top_files": top_files,
                "communities": communities,
            }

    def expand_from_files(
        self,
        file_paths: list[str],
        hops: int = 1,
    ) -> dict:
        """Expand to related files within N relationship hops.

        Args:
            file_paths: Starting file paths
            hops: Number of relationship hops to follow

        Returns:
            Dictionary with expanded file set and relationships
        """
        with self.connection.session() as session:
            # Get directly related files (via imports, function calls)
            result = session.run("""
                UNWIND $file_paths as fp
                MATCH (f:File)
                WHERE f.path ENDS WITH fp

                // Follow imports
                OPTIONAL MATCH (f)-[:IMPORTS]->(m:Module)<-[:IMPORTS]-(related:File)
                WHERE related.path <> f.path

                // Follow function calls
                OPTIONAL MATCH (f)-[:CONTAINS_FUNCTION]->(func:Function)-[:CALLS]->(called:Function)<-[:CONTAINS_FUNCTION]-(related2:File)
                WHERE related2.path <> f.path

                WITH collect(DISTINCT related.path) + collect(DISTINCT related2.path) as related_paths
                UNWIND related_paths as rp
                WITH rp WHERE rp IS NOT NULL
                RETURN DISTINCT rp as file_path
                LIMIT 20
            """, file_paths=file_paths)

            related_files = [r["file_path"] for r in result]

            return {
                "starting_files": file_paths,
                "hops": hops,
                "related_files": related_files,
                "total_files": len(file_paths) + len(related_files),
            }

    def get_impact_analysis(self, file_path: str) -> dict:
        """Analyze potential impact of changing a file.

        Args:
            file_path: Path to the file

        Returns:
            Dictionary with impact analysis
        """
        with self.connection.session() as session:
            # Get functions in this file and their callers
            callers_result = session.run("""
                MATCH (f:File)-[:CONTAINS_FUNCTION]->(func:Function)
                WHERE f.path ENDS WITH $file_path
                OPTIONAL MATCH (caller:Function)-[:CALLS]->(func)
                RETURN func.name as function_name,
                       func.qualified_name as qualified_name,
                       collect(DISTINCT caller.qualified_name) as called_by
            """, file_path=file_path)

            functions_impact = []
            total_callers = set()
            for r in callers_result:
                callers = [c for c in r["called_by"] if c is not None]
                total_callers.update(callers)
                functions_impact.append({
                    "name": r["function_name"],
                    "qualified_name": r["qualified_name"],
                    "caller_count": len(callers),
                })

            # Get files that import from this file (separate queries for Kuzu)
            func_names = session.run("""
                MATCH (f:File)-[:CONTAINS_FUNCTION]->(entity:Function)
                WHERE f.path ENDS WITH $file_path
                RETURN DISTINCT entity.name as name
            """, file_path=file_path)

            class_names = session.run("""
                MATCH (f:File)-[:CONTAINS_CLASS]->(entity:Class)
                WHERE f.path ENDS WITH $file_path
                RETURN DISTINCT entity.name as name
            """, file_path=file_path)

            exported_names = [r["name"] for r in func_names] + [r["name"] for r in class_names]

            # Find files that import these names
            dependent_files = []
            if exported_names:
                dependents_result = session.run("""
                    MATCH (other:File)-[:IMPORTS]->(m:Module)
                    WHERE any(name IN $exported_names WHERE m.name CONTAINS name)
                    RETURN DISTINCT other.path as file_path
                """, exported_names=exported_names)
                dependent_files = [r["file_path"] for r in dependents_result]

            return {
                "file_path": file_path,
                "functions": functions_impact,
                "total_callers": len(total_callers),
                "dependent_files": dependent_files,
                "risk_level": "high" if len(total_callers) > 10 else "medium" if len(total_callers) > 3 else "low",
            }
