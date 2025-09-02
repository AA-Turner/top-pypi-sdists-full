import copy
import importlib.resources
import json
import logging
import os
import re
import shutil
import sys
from dataclasses import dataclass
from datetime import datetime

from lxml import etree

from pendingai.exceptions import HtmlGenerationError

# Conditionally import Traversable from the correct location based on the Python version
if sys.version_info < (3, 11):
    from importlib.abc import Traversable
else:
    from importlib.resources.abc import Traversable

from pathlib import Path
from typing import Any, Dict, Final, List, Match, Optional, Set, Type, TypeVar

from jinja2 import Environment, PackageLoader, Template, TemplateError, select_autoescape
from rdkit import Chem
from rdkit.Chem.Draw import MolDraw2DSVG, rdMolDraw2D

from pendingai.utils.logger import Logger

# TypeVars
T_Node = TypeVar("T_Node", bound="Node")
T_Job = TypeVar("T_Job", bound="Job")
T_Route = TypeVar("T_Route", bound="Route")

# Module constants
TEMPLATES_PACKAGE: Final[str] = "pendingai.html_templates"
# Content of the jobs overview html page for single jobs (forwards to single job html)
REDIRECT_INDEX_HTML_CONTENT: Final[str] = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Redirecting...</title>
    <meta http-equiv="refresh" content="0; url=./job_%%JOB_ID%%/index.html" />
</head>
<body>
    <p>
        There is only one job in this report.
        If you are not redirected automatically,
        <a href="./job_%%JOB_ID%%/index.html">click here to view the job</a>.
    </p>
</body>
</html>"""


# module vars
logger: logging.Logger = Logger().get_logger()


# --- Data Structures ---
class Node:
    """Represents a single molecule node in the synthesis tree."""

    def __init__(self, smiles: str, step_number: int) -> None:
        self._smiles: str = smiles
        self._children: List["Node"] = []
        self._parent: Optional["Node"] = None
        self._step_numbers: Set[int] = set()
        # add the single step number provided as an argument to the set of step numbers
        self._step_numbers.add(step_number)

    @property
    def smiles(self) -> str:
        return self._smiles

    @property
    def children(self) -> List["Node"]:
        """Returns a copy of the list of children."""
        return list(self._children)

    @property
    def parent(self) -> Optional["Node"]:
        return self._parent

    @property
    def step_numbers(self) -> Set[int]:
        """Returns a copy of the set of step numbers associated with this node."""
        return set(self._step_numbers)

    def add_step_numbers(self, step_numbers: Set[int]) -> None:
        """Adds a set of new step numbers to the node.

        This method validates that the new step numbers are not already
        associated with the node before adding them to the internal set.

        Args:
            step_numbers: A set of new integer step numbers to associate with
                this node.

        Raises:
            ValueError: If any of the provided step numbers already exist in the
                node's current set of step numbers.
        """
        if not self._step_numbers.isdisjoint(step_numbers):
            raise ValueError(
                f"One or more of the step numbers {step_numbers} to be added to this node "
                f"already exist in the set of step numbers {self._step_numbers} associated with this node."
            )
        self._step_numbers.update(step_numbers)

    def add_child(self, child: "Node") -> "Node":
        """Adds a child to this node, sets the child's parent, and returns self for chaining."""
        if child not in self._children:
            self._children.append(child)
            child._parent = self
        return self

    def remove_child(self, child: "Node") -> None:
        """Removes a child from this node and unsets its parent reference."""
        if child in self._children:
            self._children.remove(child)
            child._parent = None

    def replace_child(self, old_child: "Node", new_child: "Node") -> None:
        """Replaces an existing child with a new child, updating parent references."""
        if old_child not in self._children:
            raise ValueError("The node to be replaced is not a child of this node.")

        child_index: int = self._children.index(old_child)
        self._children[child_index] = new_child
        old_child._parent = None
        new_child._parent = self


# Note: Equality for this class is value-based, but since the 'tree' attribute is a mutable Node
# object without a custom __eq__, two Route objects will only be equal if their 'tree' attributes
# refer to the exact same Node instance in memory.
@dataclass(frozen=True)
class Route:
    """Represents a single synthesis route with read-only attributes."""

    route_number: int
    num_steps: int
    num_building_blocks: int
    tree: Node

    @classmethod
    def from_json(
        cls: Type[T_Route], route_data_json: Dict[str, Any], route_number: int
    ) -> T_Route:
        """
        Creates an instance of this class from a JSON representation of a reaction synthesis route.

        This method processes synthesized reaction data in JSON format and constructs a
        synthesis tree. It ensures the integrity of the data by validating steps,
        relationships between building blocks, products, and the query structure. It
        organizes reaction nodes hierarchically to align a query SMILES with its
        connected reactants in the synthesis tree.

        Args:
            route_data_json (Dict[str, Any]): The JSON data of the reaction synthesis route.
            route_number (int): The numerical identifier for the route being processed.

        Returns:
            T_Route: An instance of the class constructed from the provided data.

        Raises:
            ValueError: Raised when the input JSON lacks reaction steps, when reactants in
                the final step are inconsistent with known building blocks, or when the
                root node of the synthesis tree mismatches the query SMILES.
        """
        # Extract the query SMILES from the 'summary' section
        query_smiles: str = _extract_product_from_reaction_smiles(
            route_data_json["summary"]
        )

        # Compile a list of building blocks
        building_blocks: List[str] = [
            building_block["smiles"]
            for building_block in route_data_json["building_blocks"]
        ]

        # Compile a list that holds all products and all building blocks.
        # The list contains all reaction components that take the role of reactant for one
        # of the reactions in the synthesis tree. In addition, it also contains the query structure.
        products: List[str] = [
            _extract_product_from_reaction_smiles(step["reaction_smiles"])
            for step in route_data_json["steps"]
        ]
        products_and_building_blocks: List[str] = sorted(
            building_blocks + products, key=len
        )

        # Create a sub-tree for each reaction step
        reaction_step_nodes: List[Node] = []
        for route_index, step in enumerate(route_data_json["steps"]):
            reaction_smiles = step["reaction_smiles"]
            product_smiles: str = _extract_product_from_reaction_smiles(reaction_smiles)
            reactant_smiles_list: List[str] = (
                cls._extract_reactants_from_reaction_smiles(
                    reaction_smiles, products_and_building_blocks
                )
            )

            product_node: Node = Node(product_smiles, route_index)
            for reactant_smiles in reactant_smiles_list:
                reactant_node: Node = Node(reactant_smiles, route_index)
                product_node.add_child(reactant_node)

            reaction_step_nodes.append(product_node)

        # Validation: There must be at least one reaction step
        if not reaction_step_nodes:
            raise ValueError(
                f"Route Number {route_number}: There are not reaction steps."
            )
        # Validation: reaction steps must be ordered bottom-to-top (building blocks at top, query at bottom)
        for child in reaction_step_nodes[0].children:
            if child.smiles not in building_blocks:
                raise ValueError(
                    f"Route Number {route_number}: Reactant '{child.smiles}' in the last step is not a known building block."
                )
        if reaction_step_nodes[-1].smiles != query_smiles:
            raise ValueError(
                f"Route Number {route_number}: The root node of the last step '{reaction_step_nodes[0].smiles}' does not match the query SMILES '{query_smiles}'."
            )

        # Assemble the full tree from the list of step nodes
        tree_root_node: Node = cls._generate_tree_from_step_nodes(reaction_step_nodes)

        return cls(
            route_number=route_number,
            num_steps=len(reaction_step_nodes),
            num_building_blocks=len(building_blocks),
            tree=tree_root_node,
        )

    @staticmethod
    def _extract_reactants_from_reaction_smiles(
        reaction_smiles: str, products_and_building_blocks: List[str]
    ) -> List[str]:
        """Identifies molecules on the reactant side of a reaction SMILES.

        This function deconstructs the reactant side of a reaction string
        (left of '>>') by iteratively matching and removing all molecules
        provided in the `products_and_building_blocks` list.

        To ensure correct matching when one molecule is a substring of another,
        the list of known components is sorted by length in descending order
        before matching. The entire reactant string must be fully deconstructed
        by the provided components, otherwise an error is raised.

        Args:
            reaction_smiles: The reaction SMILES string, expected to be in the
                format 'REACTANTS>>PRODUCTS'.
            products_and_building_blocks: A list of all known SMILES strings
                (e.g., products, building blocks, intermediates) that could
                potentially be found on the reactant side.

        Returns:
            A list of SMILES strings from the `products_and_building_blocks`
            that were successfully found on the reactant side.

        Raises:
            ValueError: If `products_and_building_blocks` is empty, if the
                `reaction_smiles` has an invalid format, or if any part of the
                reactant string cannot be accounted for by the provided list
                of known molecules.
        """
        if not products_and_building_blocks:
            raise ValueError("The list of products and building blocks cannot be empty.")

        parts: List[str] = reaction_smiles.split(">>")
        if len(parts) != 2:
            raise ValueError(
                f"Invalid reaction SMILES format: '{reaction_smiles}', must contain exactly one '>>'."
            )

        reactants_string: str = parts[0]

        # Sort known components by length, descending, to match longer strings first.
        # This is crucial for correctness if some components are substrings of others.
        products_and_building_blocks_sorted_desc: List[str] = sorted(
            products_and_building_blocks, key=len, reverse=True
        )

        reactants_list: List[str] = []

        # Iteratively find and remove all known components from the reactants string.
        for component in products_and_building_blocks_sorted_desc:
            escaped_component: str = re.escape(component)

            # First, try to remove the component when it appears in the middle of the string.
            # In this case, we replace ".component." with a single "." to keep the string valid.
            # Example: "A.B.C" with component "B" becomes "A.C".
            reactants_string, hits = re.subn(
                f"\\.{escaped_component}\\.", ".", reactants_string, count=1
            )
            if hits:
                reactants_list.append(component)
                continue

            # If it's not in the middle, it must be at an edge (start/end) or be the entire string.
            # This single, more concise regex handles all of these cases.
            # The replacement is an empty string.
            # Example: "A.B", component "A" -> "B"
            # Example: "A.B", component "B" -> "A"
            # Example: "A",   component "A" -> ""
            edge_pattern = f"(^{escaped_component}\\.?)|(\\.?{escaped_component}$)"
            reactants_string, hits = re.subn(edge_pattern, "", reactants_string, count=1)
            if hits:
                reactants_list.append(component)
                continue

        # After checking all known components, the reactant string should be empty.
        if reactants_string:
            raise ValueError(
                f"Unknown compound(s) '{reactants_string}' left on LHS of reaction smiles '{reaction_smiles}'."
            )

        return reactants_list

    @staticmethod
    def _generate_tree_from_step_nodes(reaction_step_nodes: List[Node]) -> Node:
        """
        Generates a synthesis tree from a list of reaction step nodes.

        This method processes a series of reaction step nodes and assembles them into a single connected
        synthesis tree. Each node in the input list represents a step in a reaction sequence. The method
        iteratively connects product nodes as children of reactant nodes in other reaction steps,
        thereby forming a tree structure. It ensures no cycles are introduced during this process and
        validates that the final tree is a single, connected synthesis tree.

        Args:
            reaction_step_nodes (List[Node]): A list of `Node` objects, each representing a
                reaction step in a synthesis sequence.

        Returns:
            Node: The root node of the fully assembled synthesis tree.

        Raises:
            ValueError: If the input list of nodes is empty or if it's not possible to assemble
                a single connected synthesis tree due to unconnected sub-trees or cycles.
        """
        if not reaction_step_nodes:
            raise ValueError(
                "Cannot generate a tree from an empty list of reaction steps."
            )

        # Keep track of subtrees that have not been connected to a parent yet.
        # Initially, this list contains the root of every step's sub-tree.
        subtrees_without_parents: List[Node] = list(reaction_step_nodes)

        # Outer loop: Iterate over each sub-tree, treating its root as a potential product
        # that needs to be connected to a parent tree.
        for product_node in reaction_step_nodes:
            product_smiles: str = product_node.smiles
            parent_found: bool = (
                False  # used to break out of nested loops if parent has been found
            )

            # Inner loop: Iterate over all sub-trees again, treating them as potential parents.
            for parent_subtree_root in reaction_step_nodes:
                if parent_subtree_root is product_node:
                    continue  # A node cannot be its own parent.

                # Inner-most loop: Check the children of the potential parent.
                # These children are the reactant nodes.
                for child in list(parent_subtree_root.children):
                    # If a reactant node (child) matches the product and hasn't been connected yet
                    # (i.e., it's still a leaf node with no children of its own), we've found its parent.
                    if not child.children and child.smiles == product_smiles:
                        # Before connecting, check if doing so would create a cycle.
                        # A cycle occurs if the product_node is already an ancestor of the parent_subtree_root.
                        is_cycle: bool = False
                        current_node: Optional[Node] = parent_subtree_root
                        while current_node:
                            if current_node is product_node:
                                is_cycle = True
                                break
                            current_node = current_node.parent

                        # If a cycle would be created, skip this connection and try the next child.
                        if is_cycle:
                            continue

                        # Replace the placeholder reactant node with the actual product sub-tree.
                        parent_subtree_root.replace_child(child, product_node)

                        # Per the algorithm, merge step number information.
                        # Note: This assumes stepNumbers are populated on the nodes beforehand.
                        product_node.add_step_numbers(parent_subtree_root.step_numbers)

                        # The product_node has been connected, so it's no longer a root of the forest.
                        if product_node in subtrees_without_parents:
                            subtrees_without_parents.remove(product_node)

                        # Continue to the next product_node in the outer loop.
                        parent_found = True
                        break  # Exit the children loop

                if parent_found:
                    break  # Exit the parent sub-tree loop

        # After the loops, only one tree should remain in the list of roots.
        # If not, the steps did not form a single, connected synthesis tree.
        if len(subtrees_without_parents) != 1:
            raise ValueError(
                f"Could not assemble a single synthesis tree. "
                f"Found {len(subtrees_without_parents)} unconnected sub-trees at the end."
            )

        return subtrees_without_parents[0]


@dataclass(frozen=True)
class Job:
    """
    Represents the entire results of a Job query, including the job parameters and all routes in a tree data structure.
    """

    query_smiles: str
    query_svg: str
    job_id: str
    submission_date: str
    engine: str
    processing_time: int
    building_block_libraries: List[str]
    maximum_no_of_routes: int
    building_block_limit: int
    reaction_limit: int
    routes: List[Route]

    @classmethod
    def from_json(
        cls: Type[T_Job],
        result_json: Dict[str, Any],
    ) -> T_Job:
        """
        Parses and validates a JSON dictionary representing a job instance and returns an initialized object.

        Args:
            result_json (Dict[str, Any]): A dictionary containing job data.

        Returns:
            T_Job: An initialized instance of the class populated with data from the input JSON.

        Raises:
            ValueError: If the input JSON is missing required keys, has inconsistencies in the query structure
                across routes or fields do not match expected formats or values.
        """
        # data validation: make sure all necessary data is present in JSON
        json_keys_root: List[str] = ["id", "query", "created", "parameters"]
        json_keys_parameters: List[str] = [
            "retrosynthesis_engine",
            "building_block_libraries",
            "number_of_routes",
            "processing_time",
            "reaction_limit",
            "building_block_limit",
        ]
        for key in json_keys_root:
            if key not in result_json:
                raise ValueError(f"JSON Error: Missing key '.{key}'.")
        for key in json_keys_parameters:
            if key not in result_json["parameters"]:
                raise ValueError(f"JSON Error: Missing key '.parameters.{key}'.")

        # data validation: make sure all routes have the same query structure
        # we use the query of the first route as a reference and make sure that all other routes have the same query
        if not result_json["routes"]:
            raise ValueError("JSON Error: List of routes must not be empty .")

        query_smiles_first_route: str = _extract_product_from_reaction_smiles(
            result_json["routes"][0]["summary"]
        )
        for index, route in enumerate(result_json["routes"][1:]):
            query_smiles_current_route: str = _extract_product_from_reaction_smiles(
                route["summary"]
            )
            if query_smiles_current_route != query_smiles_first_route:
                raise ValueError(
                    f"JSON Error: All routes are expected to have the same query structure. Route 1 has '{query_smiles_first_route}' and Route {index + 2} has '{query_smiles_current_route}'."
                )

        # data validation: make sure that the value of the key query is identical to the query of all routes
        query_smiles: str = result_json["query"]
        if not query_smiles == query_smiles_first_route:
            raise ValueError(
                f"JSON Error: Value of .query '{query_smiles}' does not match query SMILES '{query_smiles_first_route}' at RHS of .routes[0].summary."
            )

        # Parse an ISO-like datetime string YYYY-mm-ddThh:mm:ss.ssssss (e.g., 2025-06-24T07:23:48.438000) in UTC,
        # validate its format, and convert yo a standard ISO 8601 UTC format with 'Z'.
        created_datetime: str = result_json["created"]
        try:
            # Step 1: Parse the string to create a naive datetime object.
            if isinstance(created_datetime, datetime):
                datetime_instance: datetime = created_datetime
            else:
                datetime_instance = datetime.strptime(
                    created_datetime, "%Y-%m-%dT%H:%M:%S.%f"
                )
            # Step 2: Format the datetime object back to an ISO string.
            datetime_iso_string: str = datetime_instance.isoformat(
                timespec="milliseconds"
            )
            # Step 3: Append 'Z', the ISO 8601 designator for UTC, to the string.
            datetime_iso_string += "Z"
        except ValueError:
            # If strptime fails, catch the ValueError and re-raise it with a more descriptive error message.
            raise ValueError(
                f"JSON Error: The value of .created '{created_datetime}' does not match the expected format 'YYYY-mm-ddTHH:MM:SS.ffffff'"
            )

        # extract all routes from retro api json
        routes: List[Route] = cls._get_routes_from_json(result_json["routes"])

        return cls(
            query_smiles=result_json["query"],
            # generate the SVG for the query smiles
            query_svg=_smiles_to_svg(result_json["query"])[0],
            job_id=result_json["id"],
            submission_date=datetime_iso_string,
            engine=result_json["parameters"]["retrosynthesis_engine"],
            processing_time=result_json["parameters"]["processing_time"],
            building_block_libraries=result_json["parameters"][
                "building_block_libraries"
            ],
            maximum_no_of_routes=result_json["parameters"]["number_of_routes"],
            building_block_limit=result_json["parameters"]["building_block_limit"],
            reaction_limit=result_json["parameters"]["reaction_limit"],
            routes=routes,
        )

    @staticmethod
    def _get_routes_from_json(
        retro_api_json_routes_only: List[Dict[str, Any]],
    ) -> List[Route]:
        routes: List[Route] = []

        for index, retro_api_json_route in enumerate(retro_api_json_routes_only):
            route: Route = Route.from_json(retro_api_json_route, index + 1)
            routes.append(route)

        return routes


# --- Report Generation ---
def _extract_product_from_reaction_smiles(reaction_smiles: str) -> str:
    """Extracts the product SMILES from a reaction SMILES string.

    The function parses a standard reaction SMILES string, which separates
    reactants from products with '>>', and returns only the product portion.

    Args:
        reaction_smiles: The reaction SMILES string, expected to be in the
            format 'REACTANTS>>PRODUCT'.

    Returns:
        The SMILES string representing the product of the reaction.

    Raises:
        ValueError: If the input `reaction_smiles` does not contain
            exactly one '>>' separator, indicating an invalid format.
    """
    parts: List[str] = reaction_smiles.split(">>")
    if len(parts) != 2:
        raise ValueError(
            f"Invalid reaction SMILES format: '{reaction_smiles}'. It must contain exactly one '>>'."
        )
    return parts[1]


def _crop_svg(svg_content: str, padding: int = 5) -> tuple[str, int, int]:
    """
    Adjusts the viewBox of an SVG to fit its content using lxml and regex,
    and returns the cropped SVG along with its new dimensions.

    Args:
        svg_content: A string containing the SVG to be processed.
        padding: Padding in pixels to add around the bounding box.

    Returns:
        A tuple containing the modified SVG string, its width, and its height.
        If processing fails, it returns the original SVG and its original dimensions.
    """
    try:
        # Use lxml to parse the SVG XML. It's robust and handles various encodings.
        # The 'recover' mode helps with potentially malformed XML fragments.
        parser: etree.XMLParser = etree.XMLParser(recover=True, encoding="utf-8")
        tree = etree.fromstring(svg_content.encode("utf-8"), parser=parser)

        # Define the SVG namespace to properly find elements using xpath.
        ns: dict[str, str] = {"svg": "http://www.w3.org/2000/svg"}
        all_x: list[float] = []
        all_y: list[float] = []

        # We find all path elements, as they contain the molecule's drawing data.
        for path in tree.xpath("//svg:path[@d]", namespaces=ns):
            d_attr: str = path.get("d")
            # This regex finds all numbers (integers or floats) in the path's 'd' attribute.
            coords: list[float] = [
                float(c) for c in re.findall(r"[-+]?\d*\.\d+|[-+]?\d+", d_attr)
            ]
            # Coordinates in SVG paths are typically ordered as (x, y) pairs.
            all_x.extend(coords[0::2])
            all_y.extend(coords[1::2])

        if not all_x or not all_y:
            raise ValueError("No coordinates found in SVG paths.")

        # Determine the exact bounding box of the drawing.
        min_x: int = round(min(all_x))
        max_x: int = round(max(all_x))
        min_y: int = round(min(all_y))
        max_y: int = round(max(all_y))

        # Calculate the final width and height with padding.
        width: int = max_x - min_x + (2 * padding)
        height: int = max_y - min_y + (2 * padding)

        if width <= 0 or height <= 0:
            raise ValueError("Invalid bounding box dimensions.")

        # CRITICAL FIX: Set viewBox, width, and height using only integers.
        tree.set(
            "viewBox",
            f"{min_x - padding} {min_y - padding} {width} {height}",
        )
        tree.set("width", f"{width}px")
        tree.set("height", f"{height}px")

        # Remove the 'xml:space' attribute if it exists, as it's not needed.
        if "{http://www.w3.org/XML/1998/namespace}space" in tree.attrib:
            del tree.attrib["{http://www.w3.org/XML/1998/namespace}space"]

        # Serialize the modified XML back to a UTF-8 string.
        return etree.tostring(tree, pretty_print=True).decode("utf-8"), width, height

    except Exception as e:
        logger.warning(f"Could not crop SVG, falling back to original. Reason: {e}")
        # Fallback to extracting dimensions from the original SVG string.
        width_match: Optional[Match[str]] = re.search(
            r"width=['\"]([\d.]+)px['\"]", svg_content
        )
        height_match: Optional[Match[str]] = re.search(
            r"height=['\"]([\d.]+)px['\"]", svg_content
        )
        original_width: int = round(float(width_match.group(1))) if width_match else 150
        original_height: int = (
            round(float(height_match.group(1))) if height_match else 100
        )
        return svg_content, original_width, original_height


def _smiles_to_svg(smiles: str) -> tuple[str, int, int]:
    """
    Generates a cropped SVG representation of a molecule based on a provided SMILES string.
    The function uses RDKit to parse the SMILES string and generate the SVG. The SVG
    is then cropped to the content by adjusting the viewbox. A default placeholder
    SVG is provided for invalid SMILES strings.

    Args:
        smiles: A string representing a molecule in SMILES format.

    Returns:
        A tuple containing the cropped SVG content as a string, the width, and the height.
    """
    mol = Chem.MolFromSmiles(smiles)
    if not mol:
        return (
            '<svg width="100" height="30" xmlns="http://www.w3.org/2000/svg"><text x="10" y="20" fill="red">Invalid SMILES</text></svg>',
            100,
            30,
        )

    # We accept that RDKit will generate an SVG with whitespace.
    drawer: MolDraw2DSVG = rdMolDraw2D.MolDraw2DSVG(-1, -1)
    options = drawer.drawOptions()
    options.fixedBondLength = 12
    options.fixedFontSize = 12
    options.clearBackground = False
    drawer.DrawMolecule(mol)
    drawer.FinishDrawing()
    svg: str = drawer.GetDrawingText()

    # Crop the SVG to the bounding box of its contents.
    cropped_svg, width, height = _crop_svg(svg)

    # Rounding the dimensions to the nearest integer avoids subpixel rendering issues.
    return cropped_svg, width, height


def _tree_to_cytoscape_elements(synthesis_tree: Node) -> list:
    """
    Converts a tree structure into a list of elements suitable for rendering in Cytoscape.
    Each node in the tree is represented as a Cytoscape node, and parent-child relationships
    in the tree are represented as Cytoscape edges.

    The function processes each node in the tree, ensuring that no node is processed more
    than once, even if multiple parent nodes reference the same child node. It generates
    SVG content for each node and extracts dimensions for visualization purposes. The resulting
    Cytoscape elements include data for node and edge visualization, such as identifiers, labels,
    and dimensions.

    Args:
        synthesis_tree (Node): The root node of the tree structure to be converted into Cytoscape
            elements. Each node in the tree must have a `smiles` attribute representing
            its unique identifier and a `children` attribute listing its child nodes.

    Returns:
        list: A list of dictionaries representing the Cytoscape elements, including nodes
            and edges, generated from the input tree structure.
    """
    elements: List[dict] = []
    nodes_to_process: List[Node] = [synthesis_tree]
    processed_smiles: Set[str] = set()

    while nodes_to_process:
        node: Node = nodes_to_process.pop(0)
        if node.smiles in processed_smiles:
            continue
        processed_smiles.add(node.smiles)

        node_id: str = node.smiles

        # Generate SVG and get its dimensions
        svg_content, width, height = _smiles_to_svg(node.smiles)

        elements.append(
            {
                "group": "nodes",
                "data": {
                    "id": node_id,
                    "label": node_id,
                    "svg": svg_content,
                    "width": width,  # Pass width to Cytoscape
                    "height": height,  # Pass height to Cytoscape
                },
            }
        )

        for child in node.children:
            child_id: str = child.smiles
            elements.append(
                {
                    "group": "edges",
                    "data": {
                        "id": f"{node_id}_to_{child_id}",
                        "source": node_id,  # Parent is now the source
                        "target": child_id,  # Child is now the target
                    },
                }
            )
            nodes_to_process.append(child)

    return elements


def _copy_static_directory(directory_name: str, output_dir: Path):
    """
    Copies a directory from the package's 'html_templates' folder to the
    output directory.
    """
    try:
        # Get a traversable reference to the source directory within the package
        source_dir_traversable: Traversable = importlib.resources.files(
            TEMPLATES_PACKAGE
        ).joinpath(directory_name)

        # Get a real file system path for the source directory so shutil can use it
        with importlib.resources.as_file(source_dir_traversable) as source_dir_path:
            destination_path: Path = output_dir / directory_name
            # Copy the entire directory tree, allowing it to exist already
            shutil.copytree(source_dir_path, destination_path, dirs_exist_ok=True)
            logger.debug(
                f"Copied static directory from '{source_dir_path}' to '{destination_path}'"
            )

    except (ModuleNotFoundError, FileNotFoundError) as exception:
        raise HtmlGenerationError(
            f"Could not find or access the required static directory: '{directory_name}'"
        ) from exception


def generate_html_report(output_dir: Path, *json_results: Dict[str, Any]) -> None:
    """
    Generates a set of HTML files from one or more job objects using Jinja2 templates.

    Args:
        output_dir: Generated files are written to this directory.
        json_results: One or more job results in JSON format.

    Raises:
        HtmlGenerationError:
    """
    if not json_results:
        raise HtmlGenerationError("No job results provided to generate report.")

    try:
        jobs: List[Job] = [Job.from_json(result) for result in json_results]

        # Create the main output directory
        output_dir.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Created html output directory '{output_dir}'")

        # Copy static asset directories
        _copy_static_directory("css", output_dir)
        _copy_static_directory("scripts", output_dir)

        # Set up Jinja2 environment to load templates from the 'templates' directory
        env: Environment = Environment(
            loader=PackageLoader("pendingai", "html_templates"),
            autoescape=select_autoescape(["html", "xml"]),
        )

        # 1. Generate pages for each job
        job_template: Template = env.get_template("job_template.html")
        route_template: Template = env.get_template("route_template.html")

        for i, job in enumerate(jobs):
            job_dir: Path = output_dir / f"job_{job.job_id}"
            job_dir.mkdir(parents=True, exist_ok=True)
            logger.debug(
                f"Created output directory '{job_dir}' for job with id '{job.job_id}'"
            )

            # Determine previous and next job IDs for navigation
            prev_job_id = jobs[i - 1].job_id if i > 0 else None
            next_job_id = jobs[i + 1].job_id if i < len(jobs) - 1 else None

            # Generate the job-specific overview page that lists all routes
            job_overview_html: str = job_template.render(
                job=job,
                total_jobs=len(jobs),
                job_index=i,
                prev_job_id=prev_job_id,
                next_job_id=next_job_id,
            )
            job_overview_filepath: str = os.path.join(job_dir, "index.html")
            with open(job_overview_filepath, "w", encoding="utf-8") as f:
                f.write(job_overview_html)
                logger.debug(
                    f"Wrote html document '{job_overview_filepath}' for job with id '{job.job_id}'"
                )

            # Generate each route page for the job
            for route in job.routes:
                cytoscape_elements = _tree_to_cytoscape_elements(route.tree)
                template_vars = {
                    "job_id": job.job_id,
                    "route": route,
                    "total_routes": len(job.routes),
                    "cytoscape_elements": cytoscape_elements,
                }
                route_html: str = route_template.render(**template_vars)
                route_filename = f"route_{route.route_number}.html"
                route_filepath: str = os.path.join(job_dir, route_filename)
                with open(route_filepath, "w", encoding="utf-8") as f:
                    f.write(route_html)
                    logger.debug(
                        f"Wrote html document '{route_filepath}' for route of the job with id '{job.job_id}'"
                    )

        # 2. Generate the main index.html based on the number of jobs
        overview_filepath: Path = output_dir / "index.html"
        # For a single job, create a redirect to the job's index page.
        if len(jobs) == 1:
            job = jobs[0]
            redirect_html = REDIRECT_INDEX_HTML_CONTENT.replace("%%JOB_ID%%", job.job_id)
            with open(overview_filepath, "w", encoding="utf-8") as f:
                f.write(redirect_html)
                logger.debug(
                    f"Wrote html document '{overview_filepath}' for job overview of single job"
                )
        else:
            # For multiple jobs, generate the jobs overview page.
            jobs_overview_template: Template = env.get_template(
                "jobs_overview_template.html"
            )
            generation_date: str = datetime.now().strftime("%Y-%m-%d at %H:%M:%S")
            overview_html: str = jobs_overview_template.render(
                jobs=jobs, generation_date=generation_date
            )
            with open(overview_filepath, "w", encoding="utf-8") as f:
                f.write(overview_html)
                logger.debug(
                    f"Wrote html document '{overview_filepath}' for job overview of {len(jobs)} jobs"
                )

    # re-raise any exception we expect downstream as HtmlGenerationError
    except (OSError, TemplateError, KeyError, ValueError) as exception:
        raise HtmlGenerationError from exception


# --- Helper method for functionality implemented in method _main ---
def _convert_mentor_core_to_retro_api_format(
    mentor_core_json: List[Dict[str, Any]],
    job_id: str,
    submission_date: str,
    engine: str,
    processing_time: int,
    building_block_libraries: List[str],
    maximum_no_of_routes: int,
    building_block_limit: int,
    reaction_limit: int,
) -> Dict[str, Any]:
    """
    Converts a list of routes from the mentor-core format to the retro-api format.

    Args:
        mentor_core_json (list): A list of routes in the mentor-core format.

    Returns:
        dict: A dictionary containing the routes in retro-api format.

    Raises:
        HtmlGenerationError: If the source data is invalid."""
    if not mentor_core_json:
        raise HtmlGenerationError("Source JSON must contain at least one route.")

    # convert routes data
    converted_routes: List[Dict[str, Any]] = []
    for source_route in mentor_core_json:
        if not source_route.get("overview"):
            raise HtmlGenerationError(
                "Source route is missing the 'overview' key or it is empty."
            )
        if not source_route.get("buildingblocks"):
            raise HtmlGenerationError(
                "Source route is missing the 'buildingblocks' key or it is empty."
            )
        if not source_route.get("steps"):
            raise HtmlGenerationError(
                "Source route is missing the 'steps' key or it is empty."
            )

        building_blocks = [
            {"smiles": smiles} for smiles in source_route["buildingblocks"]
        ]
        steps = [
            {
                "order": i + 1,
                "reaction_smiles": step["reaction"],
            }
            for i, step in enumerate(source_route["steps"])
        ]
        converted_routes.append(
            {
                "summary": source_route["overview"],
                "building_blocks": building_blocks,
                "steps": steps,
            }
        )

    # add job metadata to retro api json
    return {
        "id": job_id,
        # extract the query smiles from the first route of the mentor core JSON
        "query": _extract_product_from_reaction_smiles(mentor_core_json[0]["overview"]),
        "created": submission_date,
        "routes": converted_routes,
        "parameters": {
            "retrosynthesis_engine": engine,
            "building_block_libraries": building_block_libraries,
            "number_of_routes": maximum_no_of_routes,
            "processing_time": processing_time,
            "reaction_limit": building_block_limit,
            "building_block_limit": reaction_limit,
        },
    }


def _main(argv: List[str]) -> None:
    # Check if a JSON file path is provided as a command-line argument
    if len(argv) <= 1:
        print(f"Usage: {argv[0]} INPUT_FILE REPEATS", file=sys.stderr)
        sys.exit(1)

    json_file_path: str = argv[1]
    print(f"Attempting to load routes from {json_file_path}...")

    try:
        with open(json_file_path, "r", encoding="utf-8") as input_file:
            mentor_core_json_raw = json.load(input_file)
    except FileNotFoundError:
        print(f"Error: JSON file not found at '{json_file_path}'.", file=sys.stderr)
        sys.exit(1)

    # convert mentor core json to retro api json
    retro_api_json: Dict[str, Any] = _convert_mentor_core_to_retro_api_format(
        mentor_core_json_raw,
        # add required mock data
        "685a528401a400cf79e2f047",
        datetime.now().isoformat(),
        "eng_5be6fab0bbd28b40da7f523effaedfc53fdc6208f2f777a20165d043",
        120,
        [
            "Allspice",
            "Basil",
            "Cinnamon",
            "Dill",
            "Epazote",
            "Fenugreek",
            "Ginger",
            "Horseradish",
        ],
        20,
        3,
        3,
    )
    number_of_routes: int = len(retro_api_json["routes"])
    print(
        f"Successfully loaded and converted {number_of_routes} routes from {json_file_path}"
    )

    # repeat the same json to have data to test the jobs overview page
    number_repeats: int = 1 if len(argv) < 3 else int(argv[2])
    retro_api_json_list: List[Dict[str, Any]] = [retro_api_json]
    for i in range(1, number_repeats):
        retro_api_json_deepcopy: Dict[str, Any] = copy.deepcopy(retro_api_json)
        retro_api_json_deepcopy["id"] = hex(int(retro_api_json_deepcopy["id"], 16) + i)
        retro_api_json_list.append(retro_api_json_deepcopy)

    # Generate the HTML report using the loaded data
    # wrap the single json in a list to match
    generate_html_report(Path("out"), *retro_api_json_list)
    print("Successfully generated html")


if __name__ == "__main__":
    # poetry run python src/pendingai/cli/retro/generate_html.py result.json
    _main(sys.argv)
