import os
import mm.parsehelp as parsehelp
import mm.util as util
import mm.config as config
from mm.exceptions import *
from mm.basecommand import Command

debug = config.logger.debug

class GetApexClassesAndObjectsCommand(Command):
    """
        Returns list of Apex classes (standard and custom) and custom objects
    """
    def execute(self):
        objects = []
        if config.project != None and config.project.location != None:
            if config.connection.get_plugin_client_setting('mm_use_org_metadata_for_completions', False):
                if os.path.isfile(os.path.join(config.project.location,"config",".org_metadata")): #=> parse org metadata, looking for object names
                    jsonData = util.parse_json_from_file(os.path.join(config.project.location,"config",".org_metadata"))
                    for metadata_type in jsonData:
                        if 'xmlName' in metadata_type and metadata_type['xmlName'] == 'CustomObject':
                            for object_type in metadata_type['children']:
                                objects.append({
                                    'type' : 'CustomObject',
                                    'name' : object_type['text']
                                })

        custom_apex_classes = []
        if config.project != None and config.project.location != None:
            if os.path.isdir(os.path.join(config.project.location,"config",".symbols")): #=> get list of classes
                for (dirpath, dirnames, filenames) in os.walk(os.path.join(config.project.location,"config",".symbols")):
                    for f in filenames:
                        if '-meta.xml' in f: continue
                        class_name = f.replace(".json", "")
                        custom_apex_classes.append({
                            'type' : 'Custom Apex Class',
                            'name' : class_name
                        })
            
        standard_apex_classes = []
        apex_completions = util.parse_json_from_file(os.path.join(config.base_path, config.support_dir, "sforce", "metadata", "apex.json"))
        for top_level_class_name in apex_completions["publicDeclarations"]["System"].keys():
            standard_apex_classes.append({
                'type' : 'Standard Apex Class',
                'name' : top_level_class_name
            })

        response = {
            'standard' : standard_apex_classes,
            'custom' : custom_apex_classes,
            'objects' : objects
        }

        return util.generate_success_response(response, "string")

class GetApexClassCompletionsCommand(Command):
    """
        Returns list of completions given a string of Apex
    """
    def execute(self):
        text_buffer = self.params.get("buffer", None)
        point = self.params.get("point", None)
        word = self.params.get("word", None)
        file_name = self.params.get("file_name", None)
        
        # example of data:
        #
        # public with sharing class AUTOTEST {

        #     String someString;
        #     public String myPublicString { get; set; }

        #     public AUTOTEST(String foo , Boolean bar) {
        #         ApexPages.StandardController c;
        #         c.cancel();
        #         String s = 'foo';
        #         s.

        # if data == None:
        #     raise MMException('Please provide data')
        # if file_name == None:
        #     raise MMException('Please provide file_name')

        apex_completions = util.parse_json_from_file(os.path.join(config.base_path, config.support_dir, "sforce", "metadata", "apex.json"))
        
        # point passed
        lines = text_buffer.split('\n')
        substr = ''
        for i, val in enumerate(lines):
            if i <= point[0]:
                substr += val

        debug(substr)
        typedef = parsehelp.get_type_definition(substr)
        
        debug('autocomplete type definition: ')
        debug(typedef)

        if '<' not in typedef[2] and '[' not in typedef[2]:
            if '.' in typedef[2] and '<' not in typedef[2]:
                type_parts = typedef[2].split('.')
                typedef_class = type_parts[0] #e.g. ApexPages
                typedef_class_lower = typedef_class.lower()
                typedef_class_extra = type_parts[1] #e.g. StandardController
                typedef_class_extra_lower = typedef_class_extra.lower()
            else:
                typedef_class = typedef[2] #e.g. ApexPages
                typedef_class_lower = typedef_class.lower()
                typedef_class_extra = typedef[4].replace('.','') #e.g. StandardController
                typedef_class_extra_lower = typedef_class_extra.lower()

            if '<' in typedef_class:
                typedef_class_lower = re.sub('\<.*?\>', '', typedef_class_lower)
                typedef_class_lower = re.sub('\<', '', typedef_class_lower)
                typedef_class_lower = re.sub('\>', '', typedef_class_lower)
                typedef_class       = re.sub('\<.*?\>', '', typedef_class)
                typedef_class       = re.sub('\<', '', typedef_class)
                typedef_class       = re.sub('\>', '', typedef_class)

            if '[' in typedef_class:
                typedef_class_lower = re.sub('\[.*?\]', '', typedef_class_lower)
                typedef_class       = re.sub('\[.*?\]', '', typedef_class)
        else:
            if '<' in typedef[2]:
                typedef_class = typedef[2].split('<')[0]
            elif '[' in typedef[2]:
                typedef_class = typedef[2].split('[')[0]
            typedef_class_lower = typedef_class.lower()
            typedef_class_extra = ''
            typedef_class_extra_lower = ''


        debug('autocomplete type: ')
        debug(typedef_class) #String
        debug('autocomplete type extra: ')
        debug(typedef_class_extra) #String

        if word != None and word == 'Page' and os.path.isdir(os.path.join(config.project.location,"src","pages")):
            for (dirpath, dirnames, filenames) in os.walk(os.path.join(config.project.location,"src","pages")):
                for f in filenames:
                    if '-meta.xml' in f: continue
                    base_page_name = f.replace(".page", "")
                    completions.append({
                        'type' : "Visualforce Page",
                        'name' : base_page_name
                    })
            
            return util.generate_success_response(completions, 'array')

        if len(typedef[4]) > 1 and '.' in typedef[4]:
            #deeply nested, need to look for properties
            #TODO 
            return util.generate_success_response([], 'array')

        # 
        # Is typedef_class a STANDARD Apex class?
        # 
        apex_class_key = typedef_class
        if apex_class_key == 'DateTime':
            apex_class_key = 'Datetime'

        if apex_class_key in apex_completions["publicDeclarations"] and typedef_class_extra_lower == '':
            apex_class_key = word
            if apex_class_key == 'DateTime':
                apex_class_key = 'Datetime'
            comp_def = apex_completions["publicDeclarations"].get(apex_class_key)
            for i in comp_def:
                completions.append(i)
            return util.generate_success_response(sorted(completions), 'array')

        elif apex_completions["publicDeclarations"].get(apex_class_key) != None:
            top_level = apex_completions["publicDeclarations"].get(typedef_class)
            sub_def = top_level.get(word)
            if sub_def == None:
                sub_def = top_level.get(typedef_class_extra)
            completions = get_symbol_table_completions(sub_def)
            return util.generate_success_response(sorted(completions), 'array')

        elif apex_class_key in apex_completions["publicDeclarations"]["System"]:
            if typedef_class == 'DateTime':
                typedef_class = 'Datetime'
            if word == typedef_class: #static
                comp_def = apex_completions["publicDeclarations"]["System"].get(apex_class_key)
            else: #instance
                comp_def = apex_completions["publicDeclarations"]["System"].get(typedef_class)
            completions = get_symbol_table_completions(comp_def)
            return util.generate_success_response(sorted(completions), 'array')

        # 
        # Is typedef_class a CUSTOM Apex class?
        # 

        # HANDLE CUSTOM APEX CLASS STATIC METHODS 
        # e.g. ===> MyCustomClass.doSomethingCool
        elif word != None and os.path.isfile(os.path.join(config.project.location,"src","classes",word+".cls")):
            try:
                completions = get_apex_completions(word) 
                return util.generate_success_response(sorted(completions), 'array')

            except:
                return util.generate_success_response([], 'array')

        if typedef_class_lower == None:
            return util.generate_success_response([], 'array')

        # HANDLE CUSTOM APEX INSTANCE METHOD ## 
        # MyClass foo = new MyClass()
        # e.g. ===> foo.??  

        # TODO: do we still need this given the existence of symbol tables, i don't think so?
        # clazz = parsehelp.extract_class(data)
        # inheritance = parsehelp.extract_inheritance(data, clazz)
        # if inheritance != None:
        #     if os.path.isfile(os.path.join(config.project.location,"src","classes",inheritance+".cls")): #=> apex classes
        #         completions = util.get_apex_completions(inheritance, typedef_class)
        #         return sorted(completions)
        
        # get symbol table for the seed file
        symbol_table = get_symbol_table(file_name)
        
        if symbol_table != None and "innerClasses" in symbol_table and type(symbol_table["innerClasses"] is list and len(symbol_table["innerClasses"]) > 0):
            for ic in symbol_table["innerClasses"]:
                if ic["name"].lower() == typedef_class_lower:
                    completions = get_completions_for_inner_class(ic)
                    return util.generate_success_response(sorted(completions), 'array')

        if os.path.isfile(os.path.join(config.project.location,"src","classes",typedef_class+".cls")): #=> apex classes
            completions = get_apex_completions(typedef_class, typedef_class_extra)
            return util.generate_success_response(sorted(completions), 'array')


        
        
        #TODO: finish
        return util.generate_success_response([], 'array')

        if typedef_class.endswith('__r'):
            typedef_class = typedef_class.replace('__r', '__c')
        if os.path.isfile(os.path.join(config.project.location,"src","objects",typedef_class+".object")): #=> object fields from src directory (more info on field metadata, so is primary)
            object_dom = parse(os.path.join(config.project.location,"src","objects",typedef_class+".object"))
            for node in object_dom.getElementsByTagName('fields'):
                field_name = ''
                field_type = ''
                for child in node.childNodes:                            
                    if child.nodeName != 'fullName' and child.nodeName != 'type': continue
                    if child.nodeName == 'fullName':
                        field_name = child.firstChild.nodeValue
                    elif child.nodeName == 'type':
                        field_type = child.firstChild.nodeValue
                completions.append((field_name+" \t"+field_type, field_name))
            return sorted(completions)
        elif os.path.isfile(os.path.join(config.project.location,"config",".org_metadata")) and settings.get('mm_use_org_metadata_for_completions', False): #=> parse org metadata, looking for object fields
            jsonData = util.parse_json_from_file(os.path.join(config.project.location,"config",".org_metadata"))
            for metadata_type in jsonData:
                if 'xmlName' in metadata_type and metadata_type['xmlName'] == 'CustomObject':
                    for object_type in metadata_type['children']:
                        if 'text' in object_type and object_type['text'].lower() == typedef_class_lower:
                            for attr in object_type['children']:
                                if 'text' in attr and attr['text'] == 'fields':
                                    for field in attr['children']:
                                        completions.append((field['text'], field['text']))
            if len(completions) == 0 and '__c' in typedef_class_lower:
                try:
                    #need to index custom objects here, because it couldnt be found
                    if len(ThreadTracker.get_pending_mm_panel_threads(sublime.active_window())) == 0:
                        params = {
                            'metadata_types' : ['CustomObject']
                        }
                        mm.call('refresh_metadata_index', False, params=params)
                except:
                    debug('Failed to index custom object metadata')
            else:
                completions.append(('Id', 'Id'))
                return (sorted(completions), completion_flags)
        else:
            return []

class GetVisualforceTagsListCommand(Command):
    """
        Returns list of Visualforce Tags
    """
    def execute(self):
        import mm.vf as vf 
        return util.generate_success_response(vf.tag_list, "array")

class GetVisualforceAttributeListCommand(Command):
    """
        Returns list of Visualforce Tags
    """
    def execute(self):
        tag = self.params.get("tag", None) #tag should be formatted like: apex:tagname or flow:interview or support:caseFeed, etc.
        if tag == None:
            raise MMException('Please provide tag')
        
        import mm.vf as vf
        completions = [] 
        if tag in vf.tag_defs:
            def_entry = vf.tag_defs[tag]

            for key, value in def_entry['attribs'].items():
                definition = {
                    'attribute' : key,
                    'type' : value['type']
                }
                
                if 'values' in value:
                    definition['values'] = value['values']

                completions.append(definition)

        return util.generate_success_response(completions, "array")

class GetApexTypeDefinitionCommand(Command):
    """
        Attempts to parse Apex class to get the type definition for a variable declaration (will be replaced by official Apex parser when it's released)
    """
    def execute(self):
        data = self.params.get("data", None)
        
        # example of data:
        #
        # public with sharing class AUTOTEST {

        #     String someString;
        #     public String myPublicString { get; set; }

        #     public AUTOTEST(String foo , Boolean bar) {
        #         ApexPages.StandardController c;
        #         c.cancel();
        #         String s = 'foo';
        #         s.

        if data == None:
            raise MMException('Please provide data')

        typedef = parsehelp.get_type_definition(data)

        return util.generate_success_response(list(typedef), "array")

class ExtractApexClassCommand(Command):
    def execute(self):
        data = self.params.get("data", None)
        
        # example of data:
        #
        # public with sharing class AUTOTEST {

        #     public class MyClass {
        #         public String foo;
        #         public String bar;
        #     }

        #     public AUTOTEST(String foo, Boolean bar) {
        #         MyClass foo = new MyClass();
        #         foo.

        if data == None:
            raise MMException('Please provide data')

        class_def = parsehelp.extract_class(data)

        return util.generate_success_response(list(class_def), "array")

        # ## HANDLE CUSTOM APEX INSTANCE METHOD ## 
        # ## MyClass foo = new MyClass()
        # ## foo.??  
        # symbol_table = util.get_symbol_table(file_name)
        # clazz = parsehelp.extract_class(data)

def get_field_completions(object_name):
    completions = []
    if os.path.isfile(os.path.join(config.project.location,"src","objects",object_name+".object")): #=> object fields from src directory (more info on field metadata, so is primary)
        object_dom = parse(os.path.join(config.project.location,"src","objects",object_name+".object"))
        for node in object_dom.getElementsByTagName('fields'):
            field_name = ''
            field_type = ''
            for child in node.childNodes:                            
                if child.nodeName != 'fullName' and child.nodeName != 'type': continue
                if child.nodeName == 'fullName':
                    field_name = child.firstChild.nodeValue
                elif child.nodeName == 'type':
                    field_type = child.firstChild.nodeValue
            completions.append((field_name+" \t"+field_type, field_name))
        return sorted(completions)
    elif os.path.isfile(os.path.join(config.project.location,"config",".org_metadata")): #=> parse org metadata, looking for object fields
        jsonData = util.parse_json_from_file(os.path.join(config.project.location,"config",".org_metadata"))
        for metadata_type in jsonData:
            if 'xmlName' in metadata_type and metadata_type['xmlName'] == 'CustomObject':
                for object_type in metadata_type['children']:
                    if 'text' in object_type and object_type['text'].lower() == object_name.lower():
                        for attr in object_type['children']:
                            if 'text' in attr and attr['text'] == 'fields':
                                for field in attr['children']:
                                    completions.append((field['text'], field['text']))
    return completions

def get_symbol_table(class_name):
    try:
        if os.path.exists(os.path.join(config.project.location, 'config', '.symbols')):
            class_name_json = os.path.basename(class_name).replace(".cls","json")
            if os.path.exists(os.path.join(config.project.location, 'config', '.symbols', class_name_json+".json")):
                return util.parse_json_from_file(os.path.join(config.project.location, "config", ".symbols", class_name_json+".json"))

        if not os.path.exists(os.path.join(config.project.location, 'config', '.apex_file_properties')):
            return None

        apex_props = util.parse_json_from_file(os.path.join(config.project.location, "config", ".apex_file_properties"))
        for p in apex_props.keys():
            if p == class_name+".cls" and 'symbolTable' in apex_props[p]:
                return apex_props[p]['symbolTable']
        return None
    except:
        return None

def get_completions_for_inner_class(symbol_table):
    return get_symbol_table_completions(symbol_table)

def get_symbol_table_completions(symbol_table):
    completions = []
    if 'constructors' in symbol_table:
        for c in symbol_table['constructors']:
            params = []
            if not 'visibility' in c:
                c['visibility'] = 'PUBLIC'
            if 'parameters' in c and type(c['parameters']) is list and len(c['parameters']) > 0:
                for p in c['parameters']:
                    params.append(p["type"] + " " + p["name"])
                paramStrings = []
                for i, p in enumerate(params):
                    paramStrings.append("${"+str(i+1)+":"+params[i]+"}")
                paramString = ", ".join(paramStrings)
                completions.append(c)
            else:
                completions.append(c)
    if 'properties' in symbol_table:
        for c in symbol_table['properties']:
            if not 'visibility' in c:
                c['visibility'] = 'PUBLIC'
            if "type" in c and c["type"] != None and c["type"] != "null":
                completions.append(c)
            else:
                completions.append(c)
    if 'methods' in symbol_table:
        for c in symbol_table['methods']:
            params = []
            if not 'visibility' in c:
                c['visibility'] = 'PUBLIC'
            completions.append(c)
    if 'innerClasses' in symbol_table:
        for c in symbol_table["innerClasses"]:
            if 'constructors' in c and len(c['constructors']) > 0:
                for con in c['constructors']:
                    if not 'visibility' in con:
                        con['visibility'] = 'PUBLIC'
                    params = []
                    if 'parameters' in con and type(con['parameters']) is list and len(con['parameters']) > 0:
                        for p in con['parameters']:
                            params.append(p["type"] + " " + p["name"])
                        paramStrings = []
                        for i, p in enumerate(params):
                            paramStrings.append("${"+str(i+1)+":"+params[i]+"}")
                        paramString = ", ".join(paramStrings)
                        completions.append(c)
                    else:
                        completions.append(c)
            else:
                completions.append(c)
    return sorted(completions) 

#returns suggestions based on tooling api symbol table
def get_apex_completions(search_name, search_name_extra=None):
    debug('Attempting to get completions')
    debug('search_name: ',search_name)
    debug('search_name_extra: ',search_name_extra)

    if os.path.exists(os.path.join(config.project.location, 'config', '.symbols')):
        #class_name_json = os.path.basename(class_name).replace(".cls","json")
        if os.path.exists(os.path.join(config.project.location, 'config', '.symbols', search_name+".json")):
            symbol_table = util.parse_json_from_file(os.path.join(config.project.location, "config", ".symbols", search_name+".json"))
            if search_name_extra == None or search_name_extra == '':
                return get_symbol_table_completions(symbol_table)
            elif 'innerClasses' in symbol_table and len(symbol_table['innerClasses']) > 0:
                for inner in symbol_table['innerClasses']:
                    if inner["name"] == search_name_extra:
                        return get_completions_for_inner_class(inner)

    if not os.path.exists(os.path.join(config.project.location, 'config', '.apex_file_properties')):
        return []

    apex_props = util.parse_json_from_file(os.path.join(config.project.location, "config", ".apex_file_properties"))

    for p in apex_props.keys():
        if p == search_name+".cls" and 'symbolTable' in apex_props[p] and apex_props[p]["symbolTable"] != None:
            symbol_table = apex_props[p]['symbolTable']
            if search_name_extra == None or search_name_extra == '':
                return get_symbol_table_completions(symbol_table)
            elif 'innerClasses' in symbol_table and len(symbol_table['innerClasses']) > 0:
                for inner in symbol_table['innerClasses']:
                    if inner["name"] == search_name_extra:
                        return get_completions_for_inner_class(inner)
    
    debug('no symbol table found for '+search_name)
