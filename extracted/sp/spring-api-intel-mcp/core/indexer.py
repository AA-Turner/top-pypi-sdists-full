import os
import re
from dataclasses import dataclass, field
from typing import List, Optional
from .extract_method_body_static import _extract_method_body_static
@dataclass
class EndpointInfo:
    http_method: str
    path: str
    controller_class: str
    method_name: str
    file_path: str
    line_number: int
    calls_service: list[str] = field(default_factory=list)

@dataclass
class ClassInfo:
    class_name: str
    file_path: str
    annotations: list[str] = field(default_factory=list)
    methods: list[str] = field(default_factory=list)
    dependencies: list[str] = field(default_factory=list)


class CodeIndex:
    def __init__(self):
        self.endpoints: list[EndpointInfo] = []
        self.classes: dict[str, ClassInfo] = {}
        self.file_contents: dict[str, str] = {}

    
    def build(self, project_root: str):
        self.endpoints.clear()
        self.classes.clear()
        self.file_contents.clear()
        for dirpath, _, filenames in os.walk(project_root):
            for fname in filenames:
                if fname.endswith(".java"):
                    fpath = os.path.join(dirpath, fname)
                    try:
                        with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                            source = f.read()
                        self.file_contents[fpath] = source
                        self._index_file(fpath, source)
                    except Exception:
                        pass

    def _index_file(self, fpath: str, source: str):
        class_name = self._extract_class_name(source)
        if not class_name:
            return

        annotations = re.findall(r'@(\w+)', source)
        methods = re.findall(r'(?:public|private|protected)\s+\w[\w<>,\s]*\s+(\w+)\s*\(', source)
        dependencies = re.findall(
            r'(?:'
            r'@Autowired\s+(?:public\s+)?\w+\s*\([^)]*?(\w+(?:Service|Repository|Component|Manager))\s+\w+'
            r'|private\s+(?:final\s+)?(\w+(?:Service|Repository|Component|Manager))\s+\w+\s*;'
            r')',
            source
        )
        dependencies = [d for pair in dependencies for d in pair if d]

        self.classes[class_name] = ClassInfo(
            class_name=class_name,
            file_path=fpath,
            annotations=list(set(annotations)),
            methods=methods,
            dependencies=list(set(dependencies)),
        )

        if "@RestController" not in source and "@Controller" not in source:
            return

        base_path = ""
        base_match = re.search(
            r'@RequestMapping\s*\('
            r'(?:[^)]*?)'                          
            r'(?:value\s*=\s*)?["\']([^"\']+)["\']',
            source,
            re.DOTALL
        )
        if base_match:
            base_path = base_match.group(1).rstrip("/")

        old_style_map = {
            "GET":    r'RequestMethod\.GET',
            "POST":   r'RequestMethod\.POST',
            "PUT":    r'RequestMethod\.PUT',
            "DELETE": r'RequestMethod\.DELETE',
            "PATCH":  r'RequestMethod\.PATCH',
        }

        for http_method, method_pattern in old_style_map.items():
            pattern = (
                r'@RequestMapping\s*\('
                r'(?=[^)]*' + method_pattern + r')'
                r'[^)]*?(?:value\s*=\s*)?["\']([^"\']+)["\']'
                r'[^)]*\)'
            )
            for match in re.finditer(pattern, source, re.DOTALL):
                sub_path = match.group(1).strip("/")
                full_path = base_path + "/" + sub_path if sub_path else base_path or "/"
                line_no = source[:match.start()].count("\n") + 1

                after_annotation = source[match.end():]
                method_match = re.search(
                    r'(?:public|private|protected)\s+\S+\s+(\w+)\s*\(',
                    after_annotation
                )
                method_name = method_match.group(1) if method_match else "unknown"
                method_body = _extract_method_body_static(source, method_name)
                service_calls = []
                if method_body:
                    service_calls = re.findall(
                        r'(\w+(?:Service|Repository))\.\w+\s*\(', method_body
                    )
                self.endpoints.append(EndpointInfo(
                    http_method=http_method,
                    path=full_path,
                    controller_class=class_name,
                    method_name=method_name,
                    file_path=fpath,
                    line_number=line_no,
                    calls_service=list(set(service_calls)),
                ))

        http_annotations = {
            "GET":    "GetMapping",
            "POST":   "PostMapping",
            "PUT":    "PutMapping",
            "DELETE": "DeleteMapping",
            "PATCH":  "PatchMapping",
        }

        for http_method, annotation in http_annotations.items():
            bare_pattern = rf'@{annotation}\s*(?!\s*\()'
            for match in re.finditer(bare_pattern, source):
                
                after = source[match.end():match.end()+20].lstrip()
                if after.startswith("("):
                    continue 
                line_no = source[:match.start()].count("\n") + 1
                after_annotation = source[match.end():]
                method_match = re.search(
                    r'(?:public|private|protected)\s+\S+\s+(\w+)\s*\(',
                    after_annotation
                )
                method_name = method_match.group(1) if method_match else "unknown"
                method_body = _extract_method_body_static(source, method_name)
                service_calls = []
                if method_body:
                    service_calls = re.findall(
                        r'(\w+(?:Service|Repository))\.\w+\s*\(', method_body
                    )
                self.endpoints.append(EndpointInfo(
                    http_method=http_method,
                    path=base_path or "/",
                    controller_class=class_name,
                    method_name=method_name,
                    file_path=fpath,
                    line_number=line_no,
                    calls_service=list(set(service_calls)),
                ))

            paren_pattern = rf'@{annotation}\s*\(([^)]*)\)'
            for match in re.finditer(paren_pattern, source, re.DOTALL):
                inner = match.group(1)  # everything inside the parens

                paths_found = re.findall(r'["\']([^"\']*)["\']', inner)

                paths_found = [
                    p for p in paths_found
                    if p.startswith("/") or p == ""
                ]

                
                if not paths_found:
                    paths_found = [""]

                line_no = source[:match.start()].count("\n") + 1
                after_annotation = source[match.end():]
                method_match = re.search(
                    r'(?:public|private|protected)\s+\S+\s+(\w+)\s*\(',
                    after_annotation
                )
                method_name = method_match.group(1) if method_match else "unknown"
                method_body = _extract_method_body_static(source, method_name)
                service_calls = []
                if method_body:
                    service_calls = re.findall(
                        r'(\w+(?:Service|Repository))\.\w+\s*\(', method_body
                    )

                for sub_path in paths_found:
                    sub_path = sub_path.strip("/")
                    full_path = base_path + "/" + sub_path if sub_path else base_path or "/"
                    self.endpoints.append(EndpointInfo(
                        http_method=http_method,
                        path=full_path,
                        controller_class=class_name,
                        method_name=method_name,
                        file_path=fpath,
                        line_number=line_no,
                        calls_service=list(set(service_calls)),
                    ))


    def _extract_class_name(self, source: str) -> Optional[str]:
        match = re.search(r'(?:public\s+)?(?:class|interface|enum)\s+(\w+)', source)
        return match.group(1) if match else None


    def get_class_source(self, class_name: str) -> Optional[str]:
        info = self.classes.get(class_name)
        if info:
            return self.file_contents.get(info.file_path)
        return None
