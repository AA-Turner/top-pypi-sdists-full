import os
import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field

@dataclass
class ProjectMetadata:
    build_tool: str = "unknown"
    build_tool_version: str = "unknown"
    java_version: str = "unknown"
    spring_boot_version: str = "unknown"
    group_id: str = ""
    artifact_id: str = ""
    project_version: str = ""
    dependencies: list[dict] = field(default_factory=list)

def get_project_info(project_root: str) -> str:
    """
    Parse pom.xml (Maven) or build.gradle (Gradle) to extract
    Java version, Spring Boot version, build tool, and all dependencies.
    """
    pom_path = _find_file(project_root, "pom.xml")
    gradle_path = _find_file(project_root, "build.gradle")
    gradle_kts_path = _find_file(project_root, "build.gradle.kts")

    if pom_path:
        meta = _parse_maven(pom_path)
    elif gradle_path:
        meta = _parse_gradle(gradle_path)
    elif gradle_kts_path:
        meta = _parse_gradle(gradle_kts_path)
    else:
        return "No pom.xml or build.gradle found in the project root."

    return _format_output(meta)

def _find_file(root: str, filename: str) -> str | None:
    """Search for a file starting from root, return first match."""
    for dirpath, _, files in os.walk(root):
        if filename in files:
            return os.path.join(dirpath, filename)
        depth = len(os.path.relpath(dirpath, root).split(os.sep))
        if depth > 5:
            break
    return None

def _parse_maven(pom_path: str) -> ProjectMetadata:
    meta = ProjectMetadata(build_tool="Maven")
    try:
        tree = ET.parse(pom_path)
        root = tree.getroot()

        ns = ""
        if root.tag.startswith("{"):
            ns = root.tag.split("}")[0] + "}"

        def find(tag):
            return root.find(f"{ns}{tag}")

        def findtext(tag, default="unknown"):
            el = find(tag)
            return el.text.strip() if el is not None and el.text else default

        meta.group_id = findtext("groupId")
        meta.artifact_id = findtext("artifactId")
        meta.project_version = findtext("version")

        props = find("properties")
        if props is not None:
            java_el = props.find(f"{ns}java.version") or props.find(f"{ns}maven.compiler.source")
            if java_el is not None and java_el.text:
                meta.java_version = java_el.text.strip()

        parent = find("parent")
        if parent is not None:
            parent_artifact = parent.find(f"{ns}artifactId")
            parent_version = parent.find(f"{ns}version")
            if parent_artifact is not None and "spring-boot" in (parent_artifact.text or ""):
                if parent_version is not None and parent_version.text:
                    meta.spring_boot_version = parent_version.text.strip()

        wrapper_props = os.path.join(
            os.path.dirname(pom_path), ".mvn", "wrapper", "maven-wrapper.properties"
        )
        if os.path.exists(wrapper_props):
            with open(wrapper_props) as f:
                content = f.read()
            version_match = re.search(r'apache-maven-([\d.]+)', content)
            if version_match:
                meta.build_tool_version = version_match.group(1)

        deps_el = root.find(f".//{ns}dependencies")
        if deps_el:
            for dep in deps_el.findall(f"{ns}dependency"):
                g = dep.findtext(f"{ns}groupId") or ""
                a = dep.findtext(f"{ns}artifactId") or ""
                v = dep.findtext(f"{ns}version") or "managed"
                scope = dep.findtext(f"{ns}scope") or "compile"
                meta.dependencies.append({
                    "group": g,
                    "artifact": a,
                    "version": v,
                    "scope": scope,
                })

    except Exception as e:
        return ProjectMetadata(build_tool=f"Maven (parse error: {e})")

    return meta

def _parse_gradle(gradle_path: str) -> ProjectMetadata:
    meta = ProjectMetadata(build_tool="Gradle")
    try:
        with open(gradle_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        java_match = re.search(r'(?:sourceCompatibility|javaVersion)\s*[=:]\s*["\']?([\d.]+)["\']?', content)
        if java_match:
            meta.java_version = java_match.group(1)

        sb_match = re.search(r'spring-boot["\'].*?version\s+["\']([^"\']+)["\']', content)
        if sb_match:
            meta.spring_boot_version = sb_match.group(1)

        wrapper_props = os.path.join(
            os.path.dirname(gradle_path), "gradle", "wrapper", "gradle-wrapper.properties"
        )
        if os.path.exists(wrapper_props):
            with open(wrapper_props) as f:
                wrapper_content = f.read()
            version_match = re.search(r'gradle-([\d.]+)-', wrapper_content)
            if version_match:
                meta.build_tool_version = version_match.group(1)

        dep_pattern = re.compile(
            r'(implementation|testImplementation|compileOnly|runtimeOnly|api|annotationProcessor)'
            r'\s+["\']([^"\']+)["\']'
        )
        for match in dep_pattern.finditer(content):
            scope = match.group(1)
            coords = match.group(2)
            parts = coords.split(":")
            if len(parts) >= 2:
                meta.dependencies.append({
                    "group": parts[0],
                    "artifact": parts[1],
                    "version": parts[2] if len(parts) > 2 else "managed",
                    "scope": scope,
                })

    except Exception as e:
        return ProjectMetadata(build_tool=f"Gradle (parse error: {e})")

    return meta

def _format_output(meta: ProjectMetadata) -> str:
    lines = [
        "=== Project Metadata ===",
        f"  Project       : {meta.group_id}:{meta.artifact_id} v{meta.project_version}",
        f"  Build tool    : {meta.build_tool} {meta.build_tool_version}",
        f"  Java version  : {meta.java_version}",
        f"  Spring Boot   : {meta.spring_boot_version}",
        "",
        f"=== Dependencies ({len(meta.dependencies)} total) ===",
    ]

    by_scope: dict[str, list] = {}
    for dep in meta.dependencies:
        by_scope.setdefault(dep["scope"], []).append(dep)

    for scope, deps in sorted(by_scope.items()):
        lines.append(f"\n  [{scope}]")
        for dep in sorted(deps, key=lambda d: d["artifact"]):
            lines.append(f"    {dep['group']}:{dep['artifact']}  ({dep['version']})")

    return "\n".join(lines)