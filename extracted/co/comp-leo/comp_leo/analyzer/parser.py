"""Leo source code parser and AST builder."""

import re
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class LeoFunction:
    """Represents a Leo function/transition."""
    name: str
    is_transition: bool = False
    is_async: bool = False
    is_finalize: bool = False
    parameters: List[Dict[str, str]] = field(default_factory=list)
    visibility: str = "private"  # public, private
    body: str = ""
    line_start: int = 0
    line_end: int = 0
    
    # Analysis flags
    has_assertions: bool = False
    has_mappings: bool = False
    has_external_calls: bool = False
    modifies_state: bool = False


@dataclass
class LeoStruct:
    """Represents a Leo struct."""
    name: str
    fields: List[Dict[str, str]] = field(default_factory=list)
    line_number: int = 0


@dataclass
class LeoMapping:
    """Represents a Leo mapping (on-chain state)."""
    name: str
    key_type: str
    value_type: str
    line_number: int = 0


@dataclass
class LeoProgram:
    """Parsed Leo program AST."""
    name: str
    file_path: str
    
    structs: List[LeoStruct] = field(default_factory=list)
    mappings: List[LeoMapping] = field(default_factory=list)
    functions: List[LeoFunction] = field(default_factory=list)
    transitions: List[LeoFunction] = field(default_factory=list)
    
    imports: List[str] = field(default_factory=list)
    
    # Raw source
    source_lines: List[str] = field(default_factory=list)
    source_code: str = ""


class LeoParser:
    """
    Parser for Leo smart contract source code.
    
    Extracts program structure, functions, transitions, mappings, and structs
    for static analysis.
    """
    
    def __init__(self):
        self.program: Optional[LeoProgram] = None
    
    def parse_file(self, file_path: str) -> LeoProgram:
        """Parse a Leo source file."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Leo file not found: {file_path}")
        
        source = path.read_text()
        return self.parse_source(source, str(path))
    
    def parse_source(self, source: str, file_path: str = "<string>") -> LeoProgram:
        """Parse Leo source code."""
        lines = source.split("\n")
        
        # Extract program name
        program_name = self._extract_program_name(source)
        
        program = LeoProgram(
            name=program_name,
            file_path=file_path,
            source_lines=lines,
            source_code=source
        )
        
        # Parse top-level constructs
        program.imports = self._extract_imports(source)
        program.structs = self._extract_structs(source, lines)
        program.mappings = self._extract_mappings(source, lines)
        
        # Parse functions and transitions
        functions = self._extract_functions(source, lines)
        for func in functions:
            if func.is_transition:
                program.transitions.append(func)
            else:
                program.functions.append(func)
        
        self.program = program
        return program
    
    def _extract_program_name(self, source: str) -> str:
        """Extract program name from 'program NAME.aleo { ... }'."""
        match = re.search(r'program\s+(\w+)\.aleo', source)
        return match.group(1) if match else "unknown"
    
    def _extract_imports(self, source: str) -> List[str]:
        """Extract import statements."""
        imports = []
        for match in re.finditer(r'import\s+([^;]+);', source):
            imports.append(match.group(1).strip())
        return imports
    
    def _extract_structs(self, source: str, lines: List[str]) -> List[LeoStruct]:
        """Extract struct definitions."""
        structs = []
        pattern = r'struct\s+(\w+)\s*\{'
        
        for match in re.finditer(pattern, source):
            struct_name = match.group(1)
            line_num = source[:match.start()].count('\n') + 1
            
            # Extract fields
            fields = []
            start_pos = match.end()
            brace_count = 1
            pos = start_pos
            
            while pos < len(source) and brace_count > 0:
                if source[pos] == '{':
                    brace_count += 1
                elif source[pos] == '}':
                    brace_count -= 1
                pos += 1
            
            struct_body = source[start_pos:pos-1]
            
            # Parse fields with visibility modifiers
            for line in struct_body.split('\n'):
                line = line.strip()
                if not line or line.startswith('//'):
                    continue
                
                # Match: [public|private] name: type
                field_match = re.match(r'(public|private)?\s*(\w+)\s*:\s*([^,}]+)', line)
                if field_match:
                    visibility = field_match.group(1) if field_match.group(1) else "private"
                    field_name = field_match.group(2).strip()
                    field_type = field_match.group(3).strip().rstrip(',;')
                    
                    fields.append({
                        "name": field_name,
                        "type": field_type,
                        "visibility": visibility
                    })
            
            structs.append(LeoStruct(
                name=struct_name,
                fields=fields,
                line_number=line_num
            ))
        
        return structs
    
    def _extract_mappings(self, source: str, lines: List[str]) -> List[LeoMapping]:
        """Extract mapping definitions."""
        mappings = []
        pattern = r'mapping\s+(\w+)\s*:\s*(\w+)\s*=>\s*(\w+)\s*;'
        
        for match in re.finditer(pattern, source):
            mapping_name = match.group(1)
            key_type = match.group(2)
            value_type = match.group(3)
            line_num = source[:match.start()].count('\n') + 1
            
            mappings.append(LeoMapping(
                name=mapping_name,
                key_type=key_type,
                value_type=value_type,
                line_number=line_num
            ))
        
        return mappings
    
    def _extract_functions(self, source: str, lines: List[str]) -> List[LeoFunction]:
        """Extract function and transition definitions."""
        functions = []
        
        # Match both 'transition' and 'function' keywords
        pattern = r'(async\s+)?(transition|function)\s+(\w+)\s*\('
        
        for match in re.finditer(pattern, source):
            is_async = match.group(1) is not None
            func_type = match.group(2)
            func_name = match.group(3)
            
            line_start = source[:match.start()].count('\n') + 1
            
            # Extract parameters
            params = self._extract_parameters(source, match.end())
            
            # Extract body
            body, line_end = self._extract_function_body(source, match.end(), lines)
            
            # Detect visibility (public/private parameters)
            visibility = "private"
            if "public" in params or "public" in body[:100]:
                visibility = "public"
            
            # Analyze function body
            has_assertions = "assert" in body
            has_mappings = "Mapping::" in body
            modifies_state = "Mapping::set" in body or "Mapping::remove" in body
            has_external_calls = ".aleo/" in body  # External program calls
            
            # Check if finalize function
            is_finalize = func_name.startswith("finalize_")
            
            func = LeoFunction(
                name=func_name,
                is_transition=func_type == "transition",
                is_async=is_async,
                is_finalize=is_finalize,
                parameters=params,
                visibility=visibility,
                body=body,
                line_start=line_start,
                line_end=line_end,
                has_assertions=has_assertions,
                has_mappings=has_mappings,
                has_external_calls=has_external_calls,
                modifies_state=modifies_state
            )
            
            functions.append(func)
        
        return functions
    
    def _extract_parameters(self, source: str, start_pos: int) -> List[Dict[str, str]]:
        """Extract function parameters."""
        params = []
        
        # Find closing paren
        paren_count = 1
        pos = start_pos
        while pos < len(source) and paren_count > 0:
            if source[pos] == '(':
                paren_count += 1
            elif source[pos] == ')':
                paren_count -= 1
            pos += 1
        
        param_str = source[start_pos:pos-1]
        
        # Remove comments line by line first
        cleaned_lines = []
        for line in param_str.split('\n'):
            if '//' in line:
                line = line[:line.index('//')]
            cleaned_lines.append(line)
        param_str = '\n'.join(cleaned_lines)
        
        # Parse parameters
        if param_str.strip():
            for param in param_str.split(','):
                param = param.strip()
                if not param:
                    continue
                
                # Parse: [public|private] name: type
                visibility = "private"
                if param.startswith("public"):
                    visibility = "public"
                    param = param[6:].strip()
                elif param.startswith("private"):
                    param = param[7:].strip()
                
                # Split name and type
                if ':' in param:
                    name, param_type = param.split(':', 1)
                    params.append({
                        "name": name.strip(),
                        "type": param_type.strip(),
                        "visibility": visibility
                    })
        
        return params
    
    def _extract_function_body(self, source: str, start_pos: int, lines: List[str]) -> tuple[str, int]:
        """Extract function body between braces."""
        # Skip to opening brace
        pos = start_pos
        while pos < len(source) and source[pos] != '{':
            pos += 1
        
        if pos >= len(source):
            return "", 0
        
        # Extract body
        pos += 1  # Skip opening brace
        start = pos
        brace_count = 1
        
        while pos < len(source) and brace_count > 0:
            if source[pos] == '{':
                brace_count += 1
            elif source[pos] == '}':
                brace_count -= 1
            pos += 1
        
        body = source[start:pos-1]
        line_end = source[:pos].count('\n') + 1
        
        return body.strip(), line_end
