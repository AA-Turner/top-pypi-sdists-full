from .file_filters import *
from .reader_utils import *
from .find_collect import *
STOP_SEARCH = False

def request_find_console_stop():
    global STOP_SEARCH
    STOP_SEARCH = True

def reset_find_console_stop():
    global STOP_SEARCH
    STOP_SEARCH = False

def get_contents(
    full_path=None,
    parse_lines=False,
    content=None
    ):
    if full_path:
        content = content or read_any_file(full_path)
    if content:
        if parse_lines:
            content = str(content).split('\n')
        return make_list(content)
    return []

def _normalize(s: str, strip_comments=True, collapse_ws=True, lower=True):
    if s is None:
        return ""
    if strip_comments:
        s = s.split('//', 1)[0]
    if collapse_ws:
        s = re.sub(r'\s+', ' ', s)
    if lower:
        s = s.lower()
    return s.strip()

def stringInContent(content, strings, total_strings=False, normalize=False):
    if not content:
        return False
    if normalize:
        c = _normalize(str(content))
        
        found = [s for s in strings if _normalize(s) and _normalize(s) in c]
    else:
        c = str(content)
        found = [s for s in strings if s and s in c]
    if not found:
        return False
    return len(found) == len(strings) if total_strings else True
def find_file(content, spec_line, strings, total_strings=False):
    lines = content.split('\n')
    if 1 <= spec_line <= len(lines):
        return stringInContent(lines[spec_line - 1], strings, total_strings=total_strings)
    return False
def find_lines(content, strings, total_strings=False, normalize=True, any_per_line=True):
    lines = content.split('\n')
    hits = []
    for i, line in enumerate(lines):
        # match one line either if ANY string matches or if ALL match (configurable)
        if any_per_line:
            match = stringInContent(line, strings, total_strings=False, normalize=normalize)
        else:
            match = stringInContent(line, strings, total_strings=True,  normalize=normalize)
        if match:
            hits.append({"line": i+1, "content": line})
    return hits
def getPaths(files, strings):
    tot_strings = strings
    nu_files, found_paths = [], []
    if isinstance(strings,list):
        if len(strings) >1:
            tot_strings = '\n'.join(strings)
        else:
            if len(strings) == 0:
                return nu_files, found_paths
            tot_strings = strings[0]
    
    
    for file_path in files:
        try:
            og_content = read_any_file(file_path)
            if tot_strings not in og_content:
                continue
            if file_path not in nu_files:
                nu_files.append(file_path)
            ogLines = og_content.split('\n')
            # find all occurrences of the block
            for m in re.finditer(re.escape(tot_strings), og_content):
                start_line = og_content[:m.start()].count('\n') + 1  # 1-based
                curr = {'file_path': file_path, 'lines': []}
                for j in range(len(strings)):
                    ln = start_line + j
                    curr['lines'].append({'line': ln, 'content': ogLines[ln - 1]})
                found_paths.append(curr)
        except Exception as e:
            print(f"{e}")
    return nu_files, found_paths

def findContent(
    *args,
    strings: list=[],
    total_strings=True,
    parse_lines=False,
    spec_line=False,
    get_lines=True,
    diffs=False,
    **kwargs
):
    global STOP_SEARCH
    kwargs["directories"] = ensure_directories(*args,**kwargs)

    found_paths = []

    dirs, files = get_files_and_dirs(
        **kwargs
    )
    nu_files, found_paths = getPaths(files, strings)

    if diffs and found_paths:
        return found_paths

    for file_path in nu_files:
        if STOP_SEARCH:
            return found_paths   # early exit

        if file_path:
            og_content = read_any_file(file_path)
            contents = get_contents(
                file_path,
                parse_lines=parse_lines,
                content=og_content
            )
            found = False
            for content in contents:
                if STOP_SEARCH:
                    return found_paths  # bail out cleanly

                if stringInContent(content, strings, total_strings=True, normalize=True):
                    found = True
                    if spec_line:
                        found = find_file(og_content, spec_line, strings, total_strings=True)
                    if found:
                        if get_lines:
                            lines = find_lines(
                                og_content,
                                strings=strings,
                                total_strings=False,
                                normalize=True,
                                any_per_line=True
                            )
                            if lines:
                                file_path = {"file_path": file_path, "lines": lines}
                        found_paths.append(file_path)
                        break
    return found_paths
def return_function(start_dir=None,preferred_dir=None,basenames=None,functionName=None):
    if basenames:
        basenames = make_list(basenames)
        abstract_file_finder = AbstractFileFinderImporter(start_dir=start_dir,preferred_dir=preferred_dir)
        paths = abstract_file_finder.find_paths(basenames)
        func = abstract_file_finder.import_function_from_path(paths[0], functionName)
        return func
def getLineNums(file_path):
    lines=[]
    if file_path and isinstance(file_path,dict):
        lines = file_path.get('lines')
        file_path = file_path.get('file_path')
    return file_path,lines
def get_line_content(obj):
    line,content=None,None
    if obj and isinstance(obj,dict):
        line=obj.get('line')
        content = obj.get('content')
    #print(f"line: {line}\ncontent: {content}")
    return line,content
def get_edit(file_path):
    if file_path and os.path.isfile(file_path):
        os.system(f"code {file_path}")
        input()
def editLines(file_paths):
    for file_path in file_paths:
        file_path,lines = getLineNums(file_path)
        for obj in lines:
            line,content = get_line_content(obj)
        get_edit(file_path)
def findContentAndEdit(*args,
    strings: list=[],
    total_strings=True,
    parse_lines=False,
    spec_line=False,
    get_lines=True,
    edit_lines=False,
    diffs=False,
    **kwargs
    ):
    file_paths = findContent(
        *args,
        strings=strings,
        total_strings=total_strings,
        parse_lines=parse_lines,
        spec_line=spec_line,
        get_lines=get_lines,
        diffs=diffs,
        **kwargs
        )
    if edit_lines:
        editLines(file_paths)
    return file_paths

