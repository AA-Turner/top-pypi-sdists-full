import requests
from typing import Dict, Any, Optional
from .base_tool import BaseTool
from .tool_registry import register_tool


class GWASRESTTool(BaseTool):
    """Base class for GWAS Catalog REST API tools."""

    def __init__(self, tool_config):
        super().__init__(tool_config)
        self.base_url = "https://www.ebi.ac.uk/gwas/rest/api"
        self.endpoint = ""  # Will be set by subclasses

    def _make_request(
        self, endpoint: str, params: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Make a request to the GWAS Catalog API."""
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}

    def _extract_embedded_data(
        self, data: Dict[str, Any], data_type: str
    ) -> Dict[str, Any]:
        """Extract data from the _embedded structure and add metadata."""
        if "error" in data:
            return data

        result: Dict[str, Any] = {"data": [], "metadata": {}}
        metadata: Dict[str, Any] = {}

        # Extract the main data from _embedded
        if "_embedded" in data and data_type in data["_embedded"]:
            result["data"] = data["_embedded"][data_type]

        # Extract pagination metadata
        if "page" in data:
            metadata["pagination"] = data["page"]

        # Extract links metadata
        if "_links" in data:
            metadata["links"] = data["_links"]

        if metadata:
            result["metadata"] = metadata

        # If no _embedded structure, return the original data
        if not result["data"]:
            result["data"] = data

        return result

    def run(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the tool with given arguments."""
        return self._make_request(self.endpoint, arguments)


@register_tool("GWASAssociationSearch")
class GWASAssociationSearch(GWASRESTTool):
    """Search for GWAS associations by various criteria."""

    def __init__(self, tool_config):
        super().__init__(tool_config)
        self.endpoint = "/v2/associations"

    def run(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Search for associations with optional filters."""
        params = {}

        # Handle various search parameters based on examples
        if "efo_trait" in arguments:
            params["efo_trait"] = arguments["efo_trait"]
        if "rs_id" in arguments:
            params["rs_id"] = arguments["rs_id"]
        if "accession_id" in arguments:
            params["accession_id"] = arguments["accession_id"]
        if "sort" in arguments:
            params["sort"] = arguments["sort"]
        if "direction" in arguments:
            params["direction"] = arguments["direction"]
        if "size" in arguments:
            params["size"] = arguments["size"]
        if "page" in arguments:
            params["page"] = arguments["page"]

        data = self._make_request(self.endpoint, params)
        return self._extract_embedded_data(data, "associations")


@register_tool("GWASStudySearch")
class GWASStudySearch(GWASRESTTool):
    """Search for GWAS studies by various criteria."""

    def __init__(self, tool_config):
        super().__init__(tool_config)
        self.endpoint = "/v2/studies"

    def run(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Search for studies with optional filters."""
        params = {}

        if "efo_trait" in arguments:
            params["efo_trait"] = arguments["efo_trait"]
        if "disease_trait" in arguments:
            params["disease_trait"] = arguments["disease_trait"]
        if "cohort" in arguments:
            params["cohort"] = arguments["cohort"]
        if "gxe" in arguments:
            params["gxe"] = arguments["gxe"]
        if "full_pvalue_set" in arguments:
            params["full_pvalue_set"] = arguments["full_pvalue_set"]
        if "size" in arguments:
            params["size"] = arguments["size"]
        if "page" in arguments:
            params["page"] = arguments["page"]

        data = self._make_request(self.endpoint, params)
        return self._extract_embedded_data(data, "studies")


@register_tool("GWASSNPSearch")
class GWASSNPSearch(GWASRESTTool):
    """Search for GWAS single nucleotide polymorphisms (SNPs)."""

    def __init__(self, tool_config):
        super().__init__(tool_config)
        self.endpoint = "/v2/single-nucleotide-polymorphisms"

    def run(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Search for SNPs with optional filters."""
        params = {}

        if "rs_id" in arguments:
            params["rs_id"] = arguments["rs_id"]
        if "mapped_gene" in arguments:
            params["mapped_gene"] = arguments["mapped_gene"]
        if "size" in arguments:
            params["size"] = arguments["size"]
        if "page" in arguments:
            params["page"] = arguments["page"]

        data = self._make_request(self.endpoint, params)
        return self._extract_embedded_data(data, "snps")


# Get by ID tools
@register_tool("GWASAssociationByID")
class GWASAssociationByID(GWASRESTTool):
    """Get a specific GWAS association by its ID."""

    def __init__(self, tool_config):
        super().__init__(tool_config)
        self.endpoint = "/v2/associations"

    def run(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Get association by ID."""
        if "association_id" not in arguments:
            return {"error": "association_id is required"}

        association_id = arguments["association_id"]
        return self._make_request(f"{self.endpoint}/{association_id}")


@register_tool("GWASStudyByID")
class GWASStudyByID(GWASRESTTool):
    """Get a specific GWAS study by its ID."""

    def __init__(self, tool_config):
        super().__init__(tool_config)
        self.endpoint = "/v2/studies"

    def run(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Get study by ID."""
        if "study_id" not in arguments:
            return {"error": "study_id is required"}

        study_id = arguments["study_id"]
        return self._make_request(f"{self.endpoint}/{study_id}")


@register_tool("GWASSNPByID")
class GWASSNPByID(GWASRESTTool):
    """Get a specific GWAS SNP by its rs ID."""

    def __init__(self, tool_config):
        super().__init__(tool_config)
        self.endpoint = "/v2/single-nucleotide-polymorphisms"

    def run(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Get SNP by rs ID."""
        if "rs_id" not in arguments:
            return {"error": "rs_id is required"}

        rs_id = arguments["rs_id"]
        return self._make_request(f"{self.endpoint}/{rs_id}")


# Specialized search tools based on common use cases from examples
@register_tool("GWASVariantsForTrait")
class GWASVariantsForTrait(GWASRESTTool):
    """Get all variants associated with a specific trait."""

    def __init__(self, tool_config):
        super().__init__(tool_config)
        self.endpoint = "/v2/associations"

    def run(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Get variants for a trait with pagination support."""
        if "efo_trait" not in arguments:
            return {"error": "efo_trait is required"}

        params = {
            "efo_trait": arguments["efo_trait"],
            "size": arguments.get("size", 200),
            "page": arguments.get("page", 0),
        }

        data = self._make_request(self.endpoint, params)
        return self._extract_embedded_data(data, "associations")


@register_tool("GWASAssociationsForTrait")
class GWASAssociationsForTrait(GWASRESTTool):
    """Get all associations for a specific trait, sorted by p-value."""

    def __init__(self, tool_config):
        super().__init__(tool_config)
        self.endpoint = "/v2/associations"

    def run(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Get associations for a trait, sorted by significance."""
        if "efo_trait" not in arguments:
            return {"error": "efo_trait is required"}

        params = {
            "efo_trait": arguments["efo_trait"],
            "sort": "p_value",
            "direction": "asc",
            "size": arguments.get("size", 40),
            "page": arguments.get("page", 0),
        }

        data = self._make_request(self.endpoint, params)
        return self._extract_embedded_data(data, "associations")


@register_tool("GWASAssociationsForSNP")
class GWASAssociationsForSNP(GWASRESTTool):
    """Get all associations for a specific SNP."""

    def __init__(self, tool_config):
        super().__init__(tool_config)
        self.endpoint = "/v2/associations"

    def run(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Get associations for a SNP."""
        if "rs_id" not in arguments:
            return {"error": "rs_id is required"}

        params = {
            "rs_id": arguments["rs_id"],
            "size": arguments.get("size", 200),
            "page": arguments.get("page", 0),
        }

        if "sort" in arguments:
            params["sort"] = arguments["sort"]
        if "direction" in arguments:
            params["direction"] = arguments["direction"]

        data = self._make_request(self.endpoint, params)
        return self._extract_embedded_data(data, "associations")


@register_tool("GWASStudiesForTrait")
class GWASStudiesForTrait(GWASRESTTool):
    """Get studies for a specific trait with optional filters."""

    def __init__(self, tool_config):
        super().__init__(tool_config)
        self.endpoint = "/v2/studies"

    def run(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Get studies for a trait with optional filters."""
        if "efo_trait" not in arguments and "disease_trait" not in arguments:
            return {"error": "efo_trait or disease_trait is required"}

        params = {
            "size": arguments.get("size", 200),
            "page": arguments.get("page", 0),
        }

        if "efo_trait" in arguments:
            params["efo_trait"] = arguments["efo_trait"]
        if "disease_trait" in arguments:
            params["disease_trait"] = arguments["disease_trait"]
        if "cohort" in arguments:
            params["cohort"] = arguments["cohort"]
        if "gxe" in arguments:
            params["gxe"] = arguments["gxe"]
        if "full_pvalue_set" in arguments:
            params["full_pvalue_set"] = arguments["full_pvalue_set"]

        data = self._make_request(self.endpoint, params)
        return self._extract_embedded_data(data, "studies")


@register_tool("GWASSNPsForGene")
class GWASSNPsForGene(GWASRESTTool):
    """Get SNPs mapped to a specific gene."""

    def __init__(self, tool_config):
        super().__init__(tool_config)
        self.endpoint = "/v2/single-nucleotide-polymorphisms"

    def run(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Get SNPs for a gene."""
        if "mapped_gene" not in arguments:
            return {"error": "mapped_gene is required"}

        params = {
            "mapped_gene": arguments["mapped_gene"],
            "size": arguments.get("size", 10000),
            "page": arguments.get("page", 0),
        }

        data = self._make_request(self.endpoint, params)
        return self._extract_embedded_data(data, "snps")


@register_tool("GWASAssociationsForStudy")
class GWASAssociationsForStudy(GWASRESTTool):
    """Get all associations for a specific study."""

    def __init__(self, tool_config):
        super().__init__(tool_config)
        self.endpoint = "/v2/associations"

    def run(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Get associations for a study."""
        if "accession_id" not in arguments:
            return {"error": "accession_id is required"}

        params = {
            "accession_id": arguments["accession_id"],
            "sort": "p_value",
            "direction": "asc",
            "size": arguments.get("size", 200),
            "page": arguments.get("page", 0),
        }

        data = self._make_request(self.endpoint, params)
        return self._extract_embedded_data(data, "associations")
