"""Template/rules management endpoints."""

from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(prefix="/rules", tags=["rules"])


class TemplateInfo(BaseModel):
    """Information about a template."""
    name: str
    source: str  # built-in, global, local
    path: Optional[str] = None
    description: Optional[str] = None


class TemplateContent(BaseModel):
    """Template content."""
    name: str
    content: str
    source: str


class CreateRuleRequest(BaseModel):
    """Request to create a new rule file."""

    name: str
    description: str = ""
    content: str = ""


class CreateRuleResponse(BaseModel):
    """Response after creating a rule."""

    success: bool
    name: str
    path: str


def _scan_custom_rules() -> list[TemplateInfo]:
    """Scan .emdash-rules/ for custom rule/template files."""
    from pathlib import Path

    templates = []

    for rules_dir in [Path.cwd() / ".emdash-rules", Path.home() / ".emdash-rules"]:
        if not rules_dir.exists():
            continue
        source = "local" if rules_dir.parent == Path.cwd() else "global"
        for f in sorted(rules_dir.iterdir()):
            if f.suffix in (".md", ".template") or f.name.endswith(".md.template"):
                name = f.stem
                if name.endswith(".md"):
                    name = name[:-3]
                # Read first line as description
                desc = ""
                try:
                    first_line = f.read_text().split("\n", 1)[0].strip()
                    if first_line.startswith("#"):
                        desc = first_line.lstrip("# ").strip()
                except Exception:
                    pass
                templates.append(
                    TemplateInfo(
                        name=name,
                        source=source,
                        path=str(f),
                        description=desc or f"Custom rule: {name}",
                    )
                )

    return templates


@router.get("/list")
async def list_templates():
    """List all templates and their active sources."""
    templates = [
        TemplateInfo(
            name="spec",
            source="built-in",
            description="Feature specification template",
        ),
        TemplateInfo(
            name="tasks",
            source="built-in",
            description="Implementation tasks template",
        ),
        TemplateInfo(
            name="project",
            source="built-in",
            description="PROJECT.md template",
        ),
        TemplateInfo(
            name="focus",
            source="built-in",
            description="Team focus template",
        ),
        TemplateInfo(
            name="pr-review",
            source="built-in",
            description="PR review template",
        ),
    ]

    # Scan for custom templates in .emdash-rules
    templates.extend(_scan_custom_rules())

    return {"templates": templates}


@router.get("/{template_name}", response_model=TemplateContent)
async def get_template(template_name: str):
    """Get a template's content."""
    try:
        from ..templates import load_template as get_template

        content = get_template(template_name)
        if not content:
            raise HTTPException(status_code=404, detail=f"Template {template_name} not found")

        return TemplateContent(
            name=template_name,
            content=content,
            source="built-in",  # TODO: Detect actual source
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("", response_model=CreateRuleResponse)
async def create_rule(request: CreateRuleRequest):
    """Create a new rule file in .emdash-rules/."""
    from pathlib import Path
    import re

    # Validate name
    if not re.match(r"^[a-zA-Z0-9_-]+$", request.name):
        raise HTTPException(
            status_code=400,
            detail="Rule name must contain only alphanumeric characters, hyphens, and underscores.",
        )

    rules_dir = Path.cwd() / ".emdash-rules"
    rules_dir.mkdir(parents=True, exist_ok=True)

    rule_file = rules_dir / f"{request.name}.md"
    if rule_file.exists():
        raise HTTPException(
            status_code=409,
            detail=f"Rule '{request.name}' already exists at {rule_file}",
        )

    content = request.content or f"# {request.name}\n\n{request.description}\n"
    rule_file.write_text(content)

    return CreateRuleResponse(
        success=True,
        name=request.name,
        path=str(rule_file),
    )


@router.post("/init")
async def init_templates(global_templates: bool = False, force: bool = False):
    """Initialize custom templates in .emdash-rules."""
    try:
        from pathlib import Path

        # Determine target directory
        if global_templates:
            target = Path.home() / ".emdash-rules"
        else:
            target = Path.cwd() / ".emdash-rules"

        if target.exists() and not force:
            raise HTTPException(
                status_code=400,
                detail=f"Templates already exist at {target}. Use force=true to overwrite."
            )

        target.mkdir(parents=True, exist_ok=True)

        # Copy built-in templates
        from ..templates.loader import get_defaults_dir, copy_templates_to_dir, TEMPLATE_NAMES

        templates_copied = copy_templates_to_dir(target, overwrite=force)

        return {
            "success": True,
            "path": str(target),
            "templates": templates_copied,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
