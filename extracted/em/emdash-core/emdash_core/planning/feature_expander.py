"""Feature graph expansion using AST relationships."""

from dataclasses import dataclass, field
from typing import Optional

from ..graph.connection import KuzuConnection, get_connection
from ..utils.logger import log


@dataclass
class FeatureGraph:
    """Complete AST graph for a feature."""

    root_node: dict = field(default_factory=dict)
    functions: list[dict] = field(default_factory=list)
    classes: list[dict] = field(default_factory=list)
    files: list[dict] = field(default_factory=list)
    call_graph: list[dict] = field(default_factory=list)
    inheritance: list[dict] = field(default_factory=list)
    imports: list[dict] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "root_node": self.root_node,
            "functions": self.functions,
            "classes": self.classes,
            "files": self.files,
            "call_graph": self.call_graph,
            "inheritance": self.inheritance,
            "imports": self.imports,
        }

    def to_context_string(self) -> str:
        """Convert to a readable string for LLM context."""
        lines = []

        # Root node
        lines.append(f"## Root: {self.root_node.get('name', 'Unknown')}")
        lines.append(f"Type: {self.root_node.get('type', 'Unknown')}")
        if self.root_node.get('docstring'):
            lines.append(f"Description: {self.root_node['docstring'][:200]}")
        lines.append("")

        # Call graph
        if self.call_graph:
            lines.append("## Call Graph")
            for call in self.call_graph[:20]:
                lines.append(f"  {call['caller']} -> {call['callee']}")
            lines.append("")

        # Classes
        if self.classes:
            lines.append("## Classes")
            for cls in self.classes[:10]:
                lines.append(f"  - {cls['name']}: {cls.get('docstring', 'No description')[:100]}")
            lines.append("")

        # Functions
        if self.functions:
            lines.append("## Functions")
            for func in self.functions[:15]:
                lines.append(f"  - {func['name']}: {func.get('docstring', 'No description')[:100]}")
            lines.append("")

        # Inheritance
        if self.inheritance:
            lines.append("## Inheritance")
            for inh in self.inheritance[:10]:
                lines.append(f"  {inh['child']} extends {inh['parent']}")
            lines.append("")

        # Files
        if self.files:
            lines.append("## Files")
            for f in self.files[:10]:
                lines.append(f"  - {f.get('path', f.get('name', 'Unknown'))}")

        return "\n".join(lines)


class FeatureExpander:
    """Expands from a starting node to full feature graph."""

    def __init__(self, connection: Optional[KuzuConnection] = None):
        """Initialize feature expander.

        Args:
            connection: Neo4j connection. If None, uses global connection.
        """
        self.connection = connection or get_connection()

    def expand_from_function(
        self,
        qualified_name: str,
        max_hops: int = 2
    ) -> FeatureGraph:
        """Expand from a function node.

        Traverses:
        - Callers (who calls this function?)
        - Callees (what does this function call?)
        - Parent class (if method)
        - Containing file
        - Sibling functions in same file

        Args:
            qualified_name: Function's qualified name
            max_hops: Maximum relationship depth to traverse

        Returns:
            FeatureGraph with expanded context
        """
        log.debug(f"Expanding from function: {qualified_name}")

        with self.connection.session() as session:
            # Get the root function and immediate relationships
            result = session.run("""
                MATCH (f:Function {qualified_name: $qualified_name})
                OPTIONAL MATCH (f)<-[:CALLS]-(caller:Function)
                OPTIONAL MATCH (f)-[:CALLS]->(callee:Function)
                OPTIONAL MATCH (c:Class)-[:HAS_METHOD]->(f)
                OPTIONAL MATCH (file:File)-[:CONTAINS_FUNCTION]->(f)
                RETURN f as func,
                       collect(DISTINCT caller) as callers,
                       collect(DISTINCT callee) as callees,
                       c as parent_class,
                       file
            """, qualified_name=qualified_name)

            record = result.single()
            if not record or not record["func"]:
                return FeatureGraph()

            func = dict(record["func"])
            callers = [dict(c) for c in (record["callers"] or []) if c]
            callees = [dict(c) for c in (record["callees"] or []) if c]
            parent_class = dict(record["parent_class"]) if record["parent_class"] else None
            file_node = dict(record["file"]) if record["file"] else None

            # Build root node
            root_node = {
                "type": "Function",
                "name": func.get("name"),
                "qualified_name": func.get("qualified_name"),
                "file_path": func.get("file_path"),
                "docstring": func.get("docstring"),
                "line_start": func.get("line_start"),
                "line_end": func.get("line_end"),
            }

            # Build call graph
            call_graph = []
            for caller in callers:
                call_graph.append({
                    "caller": caller.get("name"),
                    "caller_qualified": caller.get("qualified_name"),
                    "callee": func.get("name"),
                    "callee_qualified": func.get("qualified_name"),
                })
            for callee in callees:
                call_graph.append({
                    "caller": func.get("name"),
                    "caller_qualified": func.get("qualified_name"),
                    "callee": callee.get("name"),
                    "callee_qualified": callee.get("qualified_name"),
                })

            # Collect functions (callers + callees + root)
            functions = [root_node]
            for c in callers + callees:
                functions.append({
                    "name": c.get("name"),
                    "qualified_name": c.get("qualified_name"),
                    "file_path": c.get("file_path"),
                    "docstring": c.get("docstring"),
                })

            # If max_hops > 1, expand further
            if max_hops > 1:
                expanded = self._expand_call_graph(session, qualified_name, max_hops)
                existing_qns = {f.get("qualified_name") for f in functions}
                for func in expanded.get("functions", []):
                    if func.get("qualified_name") not in existing_qns:
                        functions.append(func)
                        existing_qns.add(func.get("qualified_name"))
                call_graph.extend(expanded.get("calls", []))

            # Collect classes
            classes = []
            if parent_class:
                classes.append({
                    "name": parent_class.get("name"),
                    "qualified_name": parent_class.get("qualified_name"),
                    "file_path": parent_class.get("file_path"),
                    "docstring": parent_class.get("docstring"),
                })

                # Get class hierarchy
                inheritance = self._get_class_hierarchy(session, parent_class.get("qualified_name"))
            else:
                inheritance = []

            # Collect files
            files = []
            if file_node:
                files.append({
                    "path": file_node.get("path"),
                    "name": file_node.get("name"),
                })

            # Get sibling functions from same file
            if file_node:
                siblings = self._get_file_functions(session, file_node.get("path"))
                for sib in siblings:
                    if sib.get("qualified_name") != qualified_name:
                        if sib not in functions:
                            functions.append(sib)

            return FeatureGraph(
                root_node=root_node,
                functions=functions,
                classes=classes,
                files=files,
                call_graph=call_graph,
                inheritance=inheritance,
                imports=[],
            )

    def expand_from_class(
        self,
        qualified_name: str,
        max_hops: int = 2
    ) -> FeatureGraph:
        """Expand from a class node.

        Traverses:
        - Methods (HAS_METHOD)
        - Parent classes (INHERITS_FROM)
        - Child classes (reverse INHERITS_FROM)
        - Containing file
        - Method call graphs

        Args:
            qualified_name: Class's qualified name
            max_hops: Maximum relationship depth to traverse

        Returns:
            FeatureGraph with expanded context
        """
        log.debug(f"Expanding from class: {qualified_name}")

        with self.connection.session() as session:
            # Get the root class and relationships
            result = session.run("""
                MATCH (c:Class {qualified_name: $qualified_name})
                OPTIONAL MATCH (c)-[:HAS_METHOD]->(m:Function)
                OPTIONAL MATCH (c)-[:INHERITS_FROM]->(parent:Class)
                OPTIONAL MATCH (child:Class)-[:INHERITS_FROM]->(c)
                OPTIONAL MATCH (file:File)-[:CONTAINS_CLASS]->(c)
                RETURN c as cls,
                       collect(DISTINCT m) as methods,
                       collect(DISTINCT parent) as parents,
                       collect(DISTINCT child) as children,
                       file
            """, qualified_name=qualified_name)

            record = result.single()
            if not record or not record["cls"]:
                return FeatureGraph()

            cls = dict(record["cls"])
            methods = [dict(m) for m in (record["methods"] or []) if m]
            parents = [dict(p) for p in (record["parents"] or []) if p]
            children = [dict(c) for c in (record["children"] or []) if c]
            file_node = dict(record["file"]) if record["file"] else None

            # Build root node
            root_node = {
                "type": "Class",
                "name": cls.get("name"),
                "qualified_name": cls.get("qualified_name"),
                "file_path": cls.get("file_path"),
                "docstring": cls.get("docstring"),
            }

            # Build classes list
            classes = [root_node]
            for p in parents:
                classes.append({
                    "name": p.get("name"),
                    "qualified_name": p.get("qualified_name"),
                    "file_path": p.get("file_path"),
                    "docstring": p.get("docstring"),
                })
            for c in children:
                classes.append({
                    "name": c.get("name"),
                    "qualified_name": c.get("qualified_name"),
                    "file_path": c.get("file_path"),
                    "docstring": c.get("docstring"),
                })

            # Build inheritance
            inheritance = []
            for p in parents:
                inheritance.append({
                    "child": cls.get("name"),
                    "child_qualified": cls.get("qualified_name"),
                    "parent": p.get("name"),
                    "parent_qualified": p.get("qualified_name"),
                })
            for c in children:
                inheritance.append({
                    "child": c.get("name"),
                    "child_qualified": c.get("qualified_name"),
                    "parent": cls.get("name"),
                    "parent_qualified": cls.get("qualified_name"),
                })

            # Build functions list from methods
            functions = []
            for m in methods:
                functions.append({
                    "name": m.get("name"),
                    "qualified_name": m.get("qualified_name"),
                    "file_path": m.get("file_path"),
                    "docstring": m.get("docstring"),
                })

            # Get method call graphs
            call_graph = []
            for m in methods:
                method_calls = self._get_function_calls(session, m.get("qualified_name"))
                call_graph.extend(method_calls)

            # Collect files
            files = []
            if file_node:
                files.append({
                    "path": file_node.get("path"),
                    "name": file_node.get("name"),
                })

            return FeatureGraph(
                root_node=root_node,
                functions=functions,
                classes=classes,
                files=files,
                call_graph=call_graph,
                inheritance=inheritance,
                imports=[],
            )

    def expand_from_file(
        self,
        file_path: str,
        max_hops: int = 2
    ) -> FeatureGraph:
        """Expand from a file node.

        Traverses:
        - All classes and functions (CONTAINS)
        - Imports (IMPORTS)
        - Files that import this file

        Args:
            file_path: File path
            max_hops: Maximum relationship depth to traverse

        Returns:
            FeatureGraph with expanded context
        """
        log.debug(f"Expanding from file: {file_path}")

        with self.connection.session() as session:
            # Get the file and its contents
            result = session.run("""
                MATCH (f:File)
                WHERE f.path ENDS WITH $file_path OR f.path = $file_path
                OPTIONAL MATCH (f)-[:CONTAINS_CLASS]->(cls:Class)
                OPTIONAL MATCH (f)-[:CONTAINS_FUNCTION]->(func:Function)
                OPTIONAL MATCH (f)-[:IMPORTS]->(m:Module)
                RETURN f as file,
                       collect(DISTINCT cls) as classes,
                       collect(DISTINCT func) as functions,
                       collect(DISTINCT m) as imports
            """, file_path=file_path)

            record = result.single()
            if not record or not record["file"]:
                return FeatureGraph()

            file_node = dict(record["file"])
            file_classes = [dict(c) for c in (record["classes"] or []) if c]
            file_functions = [dict(f) for f in (record["functions"] or []) if f]
            file_imports = [dict(m) for m in (record["imports"] or []) if m]

            # Build root node
            root_node = {
                "type": "File",
                "name": file_node.get("name"),
                "path": file_node.get("path"),
            }

            # Build classes list
            classes = []
            for c in file_classes:
                classes.append({
                    "name": c.get("name"),
                    "qualified_name": c.get("qualified_name"),
                    "file_path": c.get("file_path"),
                    "docstring": c.get("docstring"),
                })

            # Build functions list
            functions = []
            for f in file_functions:
                functions.append({
                    "name": f.get("name"),
                    "qualified_name": f.get("qualified_name"),
                    "file_path": f.get("file_path"),
                    "docstring": f.get("docstring"),
                })

            # Build imports list
            imports = []
            for m in file_imports:
                imports.append({
                    "module": m.get("name"),
                    "is_external": m.get("is_external", False),
                })

            # Get call graph for all functions in file
            call_graph = []
            for f in file_functions:
                calls = self._get_function_calls(session, f.get("qualified_name"))
                call_graph.extend(calls)

            # Get inheritance for all classes
            inheritance = []
            for c in file_classes:
                inh = self._get_class_hierarchy(session, c.get("qualified_name"))
                inheritance.extend(inh)

            # Files list
            files = [{
                "path": file_node.get("path"),
                "name": file_node.get("name"),
            }]

            return FeatureGraph(
                root_node=root_node,
                functions=functions,
                classes=classes,
                files=files,
                call_graph=call_graph,
                inheritance=inheritance,
                imports=imports,
            )

    def _expand_call_graph(self, session, qualified_name: str, max_hops: int) -> dict:
        """Expand call graph to multiple hops.

        Uses Kuzu-compatible syntax (no startNode/endNode/relationships functions).

        Returns:
            Dict with 'functions' list and 'calls' list
        """
        calls = []
        functions = []
        seen_funcs = set()
        seen_calls = set()

        # Get the starting function
        seen_funcs.add(qualified_name)

        # Iteratively expand the call graph up to max_hops
        current_functions = {qualified_name}

        for hop in range(max_hops):
            if not current_functions:
                break

            # Find all calls from/to current set of functions
            # Outgoing calls
            out_result = session.run("""
                MATCH (caller:Function)-[:CALLS]->(callee:Function)
                WHERE caller.qualified_name IN $func_names
                RETURN caller.name as caller_name,
                       caller.qualified_name as caller_qualified,
                       callee.name as callee_name,
                       callee.qualified_name as callee_qualified,
                       callee.file_path as callee_file,
                       callee.docstring as callee_docstring
            """, func_names=list(current_functions))

            next_functions = set()
            for record in out_result:
                call_key = (record["caller_qualified"], record["callee_qualified"])
                if call_key not in seen_calls:
                    seen_calls.add(call_key)
                    calls.append({
                        "caller": record["caller_name"],
                        "caller_qualified": record["caller_qualified"],
                        "callee": record["callee_name"],
                        "callee_qualified": record["callee_qualified"],
                    })

                callee_qn = record["callee_qualified"]
                if callee_qn and callee_qn not in seen_funcs:
                    seen_funcs.add(callee_qn)
                    next_functions.add(callee_qn)
                    functions.append({
                        "name": record["callee_name"],
                        "qualified_name": callee_qn,
                        "file_path": record["callee_file"],
                        "docstring": record["callee_docstring"],
                    })

            # Incoming calls
            in_result = session.run("""
                MATCH (caller:Function)-[:CALLS]->(callee:Function)
                WHERE callee.qualified_name IN $func_names
                RETURN caller.name as caller_name,
                       caller.qualified_name as caller_qualified,
                       caller.file_path as caller_file,
                       caller.docstring as caller_docstring,
                       callee.name as callee_name,
                       callee.qualified_name as callee_qualified
            """, func_names=list(current_functions))

            for record in in_result:
                call_key = (record["caller_qualified"], record["callee_qualified"])
                if call_key not in seen_calls:
                    seen_calls.add(call_key)
                    calls.append({
                        "caller": record["caller_name"],
                        "caller_qualified": record["caller_qualified"],
                        "callee": record["callee_name"],
                        "callee_qualified": record["callee_qualified"],
                    })

                caller_qn = record["caller_qualified"]
                if caller_qn and caller_qn not in seen_funcs:
                    seen_funcs.add(caller_qn)
                    next_functions.add(caller_qn)
                    functions.append({
                        "name": record["caller_name"],
                        "qualified_name": caller_qn,
                        "file_path": record["caller_file"],
                        "docstring": record["caller_docstring"],
                    })

            current_functions = next_functions

        return {"functions": functions, "calls": calls}

    def _get_class_hierarchy(self, session, qualified_name: str) -> list[dict]:
        """Get inheritance hierarchy for a class."""
        # Get ancestors (classes this class inherits from)
        result = session.run("""
            MATCH (c:Class {qualified_name: $qualified_name})
            OPTIONAL MATCH (c)-[:INHERITS_FROM*1..3]->(ancestor:Class)
            WITH c, collect(DISTINCT ancestor) as ancestors
            UNWIND ancestors as a
            RETURN c.name as child, a.name as parent
        """, qualified_name=qualified_name)

        inheritance = []
        for record in result:
            if record["child"] and record["parent"]:
                inheritance.append({
                    "child": record["child"],
                    "parent": record["parent"],
                })

        # Get descendants (classes that inherit from this class)
        result = session.run("""
            MATCH (c:Class {qualified_name: $qualified_name})
            OPTIONAL MATCH (descendant:Class)-[:INHERITS_FROM*1..3]->(c)
            WITH c, collect(DISTINCT descendant) as descendants
            UNWIND descendants as d
            RETURN d.name as child, c.name as parent
        """, qualified_name=qualified_name)

        for record in result:
            if record["child"] and record["parent"]:
                inheritance.append({
                    "child": record["child"],
                    "parent": record["parent"],
                })

        return inheritance

    def _get_function_calls(self, session, qualified_name: str) -> list[dict]:
        """Get call relationships for a function."""
        calls = []

        # Get functions this function calls (outgoing)
        result = session.run("""
            MATCH (f:Function {qualified_name: $qualified_name})-[:CALLS]->(callee:Function)
            RETURN f.name as caller, callee.name as callee
        """, qualified_name=qualified_name)

        for record in result:
            if record["caller"] and record["callee"]:
                calls.append({
                    "caller": record["caller"],
                    "callee": record["callee"],
                })

        # Get functions that call this function (incoming)
        result = session.run("""
            MATCH (caller:Function)-[:CALLS]->(f:Function {qualified_name: $qualified_name})
            RETURN caller.name as caller, f.name as callee
        """, qualified_name=qualified_name)

        for record in result:
            if record["caller"] and record["callee"]:
                calls.append({
                    "caller": record["caller"],
                    "callee": record["callee"],
                })

        return calls

    def _get_file_functions(self, session, file_path: str) -> list[dict]:
        """Get all functions in a file."""
        result = session.run("""
            MATCH (f:File {path: $file_path})-[:CONTAINS_FUNCTION]->(func:Function)
            RETURN func.name as name,
                   func.qualified_name as qualified_name,
                   func.file_path as file_path,
                   func.docstring as docstring
        """, file_path=file_path)

        functions = []
        for record in result:
            functions.append({
                "name": record["name"],
                "qualified_name": record["qualified_name"],
                "file_path": record["file_path"],
                "docstring": record["docstring"],
            })
        return functions
