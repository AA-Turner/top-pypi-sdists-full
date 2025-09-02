import logging

# Configure logging
logging.basicConfig(level=logging.INFO)  # Change to INFO or higher to suppress DEBUG logs
logger = logging.getLogger(__name__)
from src.abstract_paths.content_utils.src.find_content import findContentAndEdit
from src.abstract_paths import read_any_file
diff = """-interface Props {
-  setInfodata?: any; // optional
-  setLoading?: any;
-};
+interface Props {
+  setInfoData?: (v: any) => void; // canonical
+  setLoading?: (v: boolean) => void;
+}

 ...
-  const onSubmit = async (e: FormEvent<HTMLFormElement>) => {
+  const onSubmit = async (e: FormEvent<HTMLFormElement>) => {
     e.preventDefault();
-    const { setInfodata, setLoading } = props; // Destructure for safety
+    const { setInfoData, setLoading } = props;
     setLocalLoading(true);
     alertit(urlInput)
     try {
       await VideoSubmit({
         e,
         urlInput,
         setLoading: setLoading || setLocalLoading,
-        setInfodata, // Pass directly
+        setInfoData, // ✅ correct name
         setResponse: (msg: string) => console.log(msg)
       });
"""
def get_sub_add(diffs,all_difs):
    if diffs:
        sub_diffs = diffs[-1].get('sub')
        if sub_diffs:    
            all_difs.append(sub_diffs)
    diffs.append({"sub":[],"add":[],"content":None})
    return diffs,all_difs
diffs = []
endiff = True
all_difs = []
def elimComments(string):
    if '//' in string:
        for i in range(len(string)):
            if str(string[-i])+str(string[-i+1]) == '//':
                return eatOuter(string[:-i],' ')
                
    return string
for dif in diff.split('\n'):
    
    if dif.startswith('-'):
        if endiff:
            diffs,all_difs = get_sub_add(diffs,all_difs)
            endiff=False
        diffs[-1]["sub"].append(dif[1:])
        
    elif dif.startswith('+'):
        diffs[-1]["add"].append(dif[1:])
    else:
        if endiff==False:
            if diffs:
                content = findContentAndEdit(
                    directory='/var/www/html/clownworld/bolshevid',
                    exclude_dirs='node_modules',
                    strings=diffs[-1].get('sub'),
                    edit_lines=False,
                    diffs = True
                )
                
                diffs[-1]["content"] = content
            endiff = True
last_loaded=None
for diff in diffs:
    subs = diff.get("sub")
    adds = diff.get('add')
    contents = diff.get('content')
    
    for content in contents:
        file_path = content.get('file_path')
        if file_path != last_loaded:
            if last_loaded != None:
                new_content = '\n'.join(ogLines)
                
            last_loaded=file_path
            og_content = read_any_file(file_path)
            ogLines = og_content.split('\n')
            input('\n'.join(ogLines))
        for j,line in enumerate(content.get('lines')):
            i = line.get('line')
            add = None
            print(line)
            if adds:
                add = adds.pop()
            if add:
                ogLines[i-1]= add
    
input('\n'.join(ogLines))
  

