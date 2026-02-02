"""
ChEMBL API Tools

This module provides tools for accessing the ChEMBL database:
- ChEMBLTool: Specialized tool for similarity search
- ChEMBLRESTTool: Generic REST API tool for ChEMBL endpoints
"""

import requests
from urllib.parse import quote
from typing import Any, Dict

# from rdkit import Chem
from .base_tool import BaseTool
from .tool_registry import register_tool
from .http_utils import request_with_retry
from indigo import Indigo


@register_tool("ChEMBLRESTTool")
class ChEMBLRESTTool(BaseTool):
    """
    Generic ChEMBL REST API tool.
    Wrapper for ChEMBL API endpoints defined in chembl_tools.json.
    Supports all ChEMBL data resources: molecules, targets, assays, activities, drugs, etc.
    """

    def __init__(self, tool_config: Dict):
        super().__init__(tool_config)
        self.base_url = "https://www.ebi.ac.uk/chembl/api/data"
        self.session = requests.Session()
        self.session.headers.update(
            {"Accept": "application/json", "User-Agent": "ToolUniverse/1.0"}
        )
        self.timeout = 30

    def _build_url(self, args: Dict[str, Any]) -> str:
        """Build URL from endpoint template and arguments"""
        endpoint_template = self.tool_config.get("fields", {}).get("endpoint", "")
        tool_name = self.tool_config.get("name", "")

        if endpoint_template:
            url = endpoint_template
            # Replace placeholders in URL
            for k, v in args.items():
                url = url.replace(f"{{{k}}}", str(v))
            # If URL doesn't start with http, prepend base_url
            if not url.startswith("http"):
                url = self.base_url + url
            return url

        # Build URL based on tool name patterns
        if tool_name.startswith("ChEMBL_get_molecule"):
            chembl_id = args.get("chembl_id", "")
            if chembl_id:
                return f"{self.base_url}/molecule/{chembl_id}.json"
        elif tool_name.startswith("ChEMBL_get_target"):
            target_id = args.get("target_chembl_id", "")
            if target_id:
                return f"{self.base_url}/target/{target_id}.json"
        elif tool_name.startswith("ChEMBL_get_assay"):
            assay_id = args.get("assay_chembl_id", "")
            if assay_id:
                return f"{self.base_url}/assay/{assay_id}.json"
        elif tool_name.startswith("ChEMBL_get_activity"):
            activity_id = args.get("activity_id", "")
            if activity_id:
                return f"{self.base_url}/activity/{activity_id}.json"
        elif tool_name.startswith("ChEMBL_get_drug"):
            drug_id = args.get("drug_chembl_id", "")
            if drug_id:
                return f"{self.base_url}/drug/{drug_id}.json"

        return self.base_url

    def _build_params(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Build query parameters for ChEMBL API"""
        params = {}
        self.tool_config.get("name", "")

        # ChEMBL API uses query parameters for filtering
        # Common parameters: limit, offset, format, ordering
        if "limit" in args:
            params["limit"] = args["limit"]
        if "offset" in args:
            params["offset"] = args["offset"]
        if "format" in args:
            params["format"] = args["format"]
        else:
            params["format"] = "json"
        # Optional field projection to reduce payload size on heavy endpoints.
        # ChEMBL supports projection via the `only` query parameter.
        # We accept ToolUniverse argument name `fields` and map it to `only`.
        # Power users can also pass `only` directly.
        only_value = args.get("only", None)
        fields_value = args.get("fields", None)
        projection_value = only_value if only_value is not None else fields_value
        if projection_value is not None:
            if isinstance(projection_value, (list, tuple)):
                params["only"] = ",".join(str(f) for f in projection_value)
            else:
                params["only"] = str(projection_value)
        if "ordering" in args:
            params["ordering"] = args["ordering"]

        # Add any filter parameters (ChEMBL uses field__filter syntax)
        # e.g., molecule_chembl_id__exact, pref_name__contains
        for key, value in args.items():
            if (
                key
                not in [
                    "limit",
                    "offset",
                    "format",
                    "fields",
                    "only",
                    "ordering",
                    "chembl_id",
                    "target_chembl_id",
                    "assay_chembl_id",
                    "activity_id",
                    "drug_chembl_id",
                ]
                and value is not None
            ):
                params[key] = value

        return params

    def run(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the ChEMBL API call"""
        try:
            url = self._build_url(arguments)
            params = self._build_params(arguments)
            response = request_with_retry(
                self.session,
                "GET",
                url,
                params=params,
                timeout=self.timeout,
                max_attempts=3,
                backoff_seconds=0.5,
            )
            response.raise_for_status()

            data = response.json()

            response_data = {
                "status": "success",
                "data": data,
                "url": response.url,
            }

            # Extract count if available (ChEMBL pagination)
            if isinstance(data, dict):
                if "page_meta" in data:
                    response_data["page_meta"] = data["page_meta"]
                if "page" in data:
                    response_data["pagination"] = data["page"]

            # Count results if it's a list or has a results key
            if isinstance(data, list):
                response_data["count"] = len(data)
            elif isinstance(data, dict):
                # ChEMBL often returns data in a key matching the resource name
                for key in [
                    "molecules",
                    "targets",
                    "assays",
                    "activities",
                    "drugs",
                    "mechanisms",
                    "indications",
                    "binding_sites",
                ]:
                    if key in data and isinstance(data[key], list):
                        response_data["count"] = len(data[key])
                        break

            return response_data

        except requests.exceptions.HTTPError as e:
            resp = e.response
            status_code = getattr(resp, "status_code", None)
            detail = None
            if getattr(resp, "text", None):
                # Include a short preview of the response body for debugging,
                # but avoid returning huge payloads.
                detail = resp.text[:500]
            return {
                "status": "error",
                "error": f"ChEMBL API returned HTTP {status_code}",
                "url": getattr(resp, "url", url if "url" in locals() else None),
                "status_code": status_code,
                "detail": detail,
            }
        except requests.exceptions.RequestException as e:
            return {
                "status": "error",
                "error": f"ChEMBL API request failed: {str(e)}",
                "url": url if "url" in locals() else None,
                "detail": repr(e),
            }
        except Exception as e:
            return {
                "status": "error",
                "error": f"Unexpected error: {str(e)}",
                "url": url if "url" in locals() else None,
                "detail": repr(e),
            }


@register_tool("ChEMBLTool")
class ChEMBLTool(BaseTool):
    """
    Tool to search for molecules similar to a given compound name or SMILES using the ChEMBL Web Services API.

    Note: This tool is designed for small molecule compounds only. Biologics (antibodies, proteins,
    oligonucleotides, etc.) do not have SMILES structures and cannot be used for structure-based
    similarity search. The tool will provide detailed error messages when biologics are queried,
    explaining the reason and suggesting alternative tools.
    """

    def __init__(self, tool_config, base_url="https://www.ebi.ac.uk/chembl/api/data"):
        super().__init__(tool_config)
        self.base_url = base_url
        self.indigo = Indigo()

    def run(self, arguments):
        query = arguments.get("query")
        similarity_threshold = arguments.get("similarity_threshold", 80)
        max_results = arguments.get("max_results", 20)

        if not query:
            return {"error": "`query` parameter is required."}
        return self._search_similar_molecules(query, similarity_threshold, max_results)

    def get_chembl_id_by_name(self, compound_name):
        """
        Search ChEMBL for a compound by name and return the ChEMBL ID of the first match.
        """
        headers = {"Accept": "application/json"}
        search_url = f"{self.base_url}/molecule/search.json?q={quote(compound_name)}"
        print(search_url)
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()
        results = response.json().get("molecules", [])
        if not results or not isinstance(results, list):
            return {"error": "No valid results found for the compound name."}
        if not results:
            return {"error": "No results found for the compound name."}
        top_molecules = results[:3]  # Get the top 3 results
        chembl_ids = [
            molecule.get("molecule_chembl_id")
            for molecule in top_molecules
            if molecule.get("molecule_chembl_id")
        ]
        if not chembl_ids:
            return {"error": "No ChEMBL IDs found for the compound name."}
        return {"chembl_ids": chembl_ids}

    def get_smiles_pref_name_by_chembl_id(self, query):
        """
        Given a ChEMBL ID, return a dict with canonical SMILES and preferred name.
        """
        headers = {"Accept": "application/json"}
        if query.upper().startswith("CHEMBL"):
            molecule_url = f"{self.base_url}/molecule/{quote(query)}.json"
            response = requests.get(molecule_url, headers=headers)
            response.raise_for_status()
            molecule = response.json()
            if not molecule or not isinstance(molecule, dict):
                return {"error": "No valid molecule found for the given ChEMBL ID."}
            molecule_structures = molecule.get("molecule_structures")
            if not molecule_structures or not isinstance(molecule_structures, dict):
                return {
                    "error": "Molecule structures not found or invalid for the ChEMBL ID."
                }
            smiles = molecule_structures.get("canonical_smiles")
            pref_name = molecule.get("pref_name")
            if not smiles:
                return {"error": "SMILES not found for the given ChEMBL ID."}
            return {"smiles": smiles, "pref_name": pref_name}
        else:
            return None

    def get_chembl_smiles_pref_name_id_by_name(self, compound_name):
        """
        Search ChEMBL for a compound by name and return a list of dicts with ChEMBL ID, canonical SMILES, and preferred name for the top 5 matches.
        """
        headers = {"Accept": "application/json"}
        search_url = f"{self.base_url}/molecule/search.json?q={quote(compound_name)}"
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()
        results = response.json().get("molecules", [])
        if not results or not isinstance(results, list):
            return {"error": "No valid results found for the compound name."}
        top_molecules = results[:5]
        output = []
        molecules_without_smiles = []
        for molecule in top_molecules:
            chembl_id = molecule.get("molecule_chembl_id", None)
            molecule_structures = molecule.get("molecule_structures", {})
            molecule_type = molecule.get("molecule_type", "Unknown")
            if molecule_structures is not None:
                smiles = molecule_structures.get("canonical_smiles", None)
            else:
                smiles = None
            pref_name = molecule.get("pref_name")
            if chembl_id and smiles:
                output.append(
                    {"chembl_id": chembl_id, "smiles": smiles, "pref_name": pref_name}
                )
            elif chembl_id and not smiles:
                smiles_pre_name_dict = self.get_smiles_pref_name_by_chembl_id(chembl_id)
                if (
                    isinstance(smiles_pre_name_dict, dict)
                    and "error" not in smiles_pre_name_dict
                ):
                    output.append(
                        {
                            "chembl_id": chembl_id,
                            "smiles": smiles_pre_name_dict["smiles"],
                            "pref_name": smiles_pre_name_dict.get("pref_name"),
                        }
                    )
                else:
                    # Store info about molecules found but without SMILES
                    molecules_without_smiles.append(
                        {
                            "chembl_id": chembl_id,
                            "pref_name": pref_name,
                            "molecule_type": molecule_type,
                        }
                    )
        if not output:
            # Provide detailed error message with reason and alternative tools
            error_msg = "No ChEMBL IDs or SMILES found for the compound name."
            if molecules_without_smiles:
                molecule_types = set(
                    [
                        m.get("molecule_type")
                        for m in molecules_without_smiles
                        if m.get("molecule_type")
                    ]
                )
                if any(
                    mt in ["Antibody", "Protein", "Oligonucleotide", "Oligosaccharide"]
                    for mt in molecule_types
                ):
                    error_msg = (
                        f"The compound '{compound_name}' was found in ChEMBL but does not have a SMILES structure. "
                        f"This tool is designed for small molecule compounds only. "
                        f"The found molecule(s) are of type(s): {', '.join(molecule_types)}. "
                        f"Biologics (antibodies, proteins, etc.) do not have SMILES representations. "
                        f"For searching similar biologics, consider using: "
                        f"PDB_search_similar_structures (for structure/sequence similarity search using PDB ID or sequence), "
                        f"BLAST_protein_search (for protein/antibody sequence similarity search, requires amino acid sequence), "
                        f"or UniProt_search (for searching proteins in UniProt database). "
                        f"For small molecule similarity search, use: PubChem_search_compounds_by_similarity (requires SMILES input)."
                    )
                else:
                    error_msg = (
                        f"The compound '{compound_name}' was found in ChEMBL (ChEMBL ID(s): "
                        f"{', '.join([m.get('chembl_id') for m in molecules_without_smiles[:3]])}) "
                        f"but does not have a SMILES structure available. "
                        f"This tool requires SMILES for similarity search. "
                        f"For searching similar small molecules, consider using: "
                        f"PubChem_search_compounds_by_similarity (requires SMILES input)."
                    )
            return {"error": error_msg}
        return output

    def _search_similar_molecules(self, query, similarity_threshold, max_results):
        headers = {"Accept": "application/json"}

        smiles_info_list = []

        # If the query looks like a ChEMBL ID, fetch its SMILES and pref_name
        if isinstance(query, str) and query.upper().startswith("CHEMBL"):
            result = self.get_smiles_pref_name_by_chembl_id(query)
            if isinstance(result, dict) and "error" in result:
                return result
            smiles_info_list.append(
                {
                    "chembl_id": query,
                    "smiles": result["smiles"],
                    "pref_name": result.get("pref_name"),
                }
            )

        # If not a ChEMBL ID, use get_chembl_smiles_pref_name_id_by_name to get info
        if len(smiles_info_list) == 0 and isinstance(query, str):
            results = self.get_chembl_smiles_pref_name_id_by_name(query)
            if isinstance(results, dict) and "error" in results:
                return results
            for item in results:
                smiles_info_list.append(item)

        if len(smiles_info_list) == 0:
            # Check if the compound exists in ChEMBL but without SMILES
            if isinstance(query, str) and not query.upper().startswith("CHEMBL"):
                # Try to get molecule info to provide better error message
                headers = {"Accept": "application/json"}
                search_url = f"{self.base_url}/molecule/search.json?q={quote(query)}"
                try:
                    response = requests.get(search_url, headers=headers)
                    response.raise_for_status()
                    results = response.json().get("molecules", [])
                    if results and len(results) > 0:
                        molecule = results[0]
                        molecule_type = molecule.get("molecule_type", "Unknown")
                        chembl_id = molecule.get("molecule_chembl_id")
                        if molecule_type in [
                            "Antibody",
                            "Protein",
                            "Oligonucleotide",
                            "Oligosaccharide",
                        ]:
                            return {
                                "error": (
                                    f"The compound '{query}' was found in ChEMBL (ChEMBL ID: {chembl_id}) "
                                    f"but is a {molecule_type.lower()}, not a small molecule. "
                                    f"This tool is designed for small molecule compounds only. "
                                    f"Biologics (antibodies, proteins, etc.) do not have SMILES representations "
                                    f"and cannot be used for structure-based similarity search. "
                                    f"For searching similar biologics, consider using: "
                                    f"PDB_search_similar_structures (for structure/sequence similarity search using PDB ID or sequence), "
                                    f"BLAST_protein_search (for protein/antibody sequence similarity search, requires amino acid sequence), "
                                    f"or UniProt_search (for searching proteins in UniProt database). "
                                    f"For small molecule similarity search, use: PubChem_search_compounds_by_similarity (requires SMILES input)."
                                )
                            }
                except Exception:
                    pass
            return {
                "error": (
                    f"SMILES representation not found for the compound '{query}'. "
                    f"This tool requires SMILES structure for similarity search. "
                    f"If you have a SMILES string, you can use it directly as the query. "
                    f"Alternatively, consider using PubChem_search_compounds_by_similarity "
                    f"(requires SMILES input) for similarity search."
                )
            }

        results_list = []
        for info in smiles_info_list:
            smiles = info["smiles"]
            pref_name = info.get("pref_name")
            chembl_id = info.get("chembl_id")
            mol = self.indigo.loadMolecule(smiles)
            if mol is None:
                return {"error": "Failed to load molecule with Indigo."}

            encoded_smiles = quote(smiles)
            similarity_url = f"{self.base_url}/similarity/{encoded_smiles}/{similarity_threshold}.json?limit={max_results}"
            sim_response = requests.get(similarity_url, headers=headers)
            sim_response.raise_for_status()
            sim_results = sim_response.json().get("molecules", [])
            similar_molecules = []
            for mol in sim_results:
                sim_chembl_id = mol.get("molecule_chembl_id")
                sim_pref_name = mol.get("pref_name", "N/A")
                mol_structures = mol.get("molecule_structures", {})
                if mol_structures is None:
                    continue
                mol_smiles = mol_structures.get("canonical_smiles", "N/A")
                similarity = mol.get("similarity", "N/A")
                similar_molecules.append(
                    {
                        "chembl_id": sim_chembl_id,
                        "pref_name": sim_pref_name,
                        "smiles": mol_smiles,
                        "similarity": similarity,
                    }
                )
            if len(similar_molecules) == 0:
                continue
            results_list.append(
                {
                    "chembl_id": chembl_id,
                    "pref_name": pref_name,
                    "smiles": smiles,
                    "similar_molecules": similar_molecules,
                }
            )

        return results_list
