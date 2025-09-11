"""
compare_utils.py
Part of the abstract_utilities package

This script provides utility functions for comparing strings and objects. These functions include methods for calculating string similarity and comparing the lengths of objects.

Author: putkoff
Date: 05/31/2023
Version: 0.1.2
"""
import string
from ..type_utils import is_number,make_list
def get_comp(string:str, string_2:str):
    """
    Calculates the similarity between two strings.

    Args:
        string (str): The first string.
        string_2 (str): The second string.

    Returns:
        float: The similarity score between the two strings, calculated by comparing overlapping sequences of characters.
    """
    ls = [['']]
    for k in range(len(get_lower(string, string_2))):
        if string[k] in st2:
            if len(ls) == 0 or ls[-1][0] + string[k] in string_2:
                ls[-1].append(string[k])
            else:
                ls.append([string[k]])
        elif len(string) > 1:
            string = string[1:]
    for k in range(len(ls)):
        ls[k] = len(ls[k])
    ls.sort()
    if float(0) in [float(ls[0]),float(len(string_2))]:
        return float(0)
    return float(ls[0] / len(string_2))

def get_lower(obj, obj2):
    """
    Compares the lengths of two objects or their string representations and returns the shorter one. If an object isn't a string, it's compared using its natural length.

    Args:
        obj: The first object to compare.
        obj2: The second object to compare.

    Returns:
        any: The shorter of the two objects, based on their length or string representation length.
    """
    lowest = [obj, 0]
    if type(obj) == str:
        lowest = [len(obj), 0]
    if type(obj2) == str:
        return obj2 if len(obj2) > lowest[0] else obj
    return obj2 if obj2 > lowest[0] else obj
def is_in_list(obj: any, ls: list = []):
    """
    Checks if the given object is present in the list.

    Args:
        obj (any): The object to search for.
        ls (list, optional): The list in which to search. Defaults to an empty list.

    Returns:
        bool: True if the object is in the list, False otherwise.
    """
    if obj in ls:
        return True
def safe_len(obj: str = ''):
    """
    Safely gets the length of the string representation of the given object.

    Args:
        obj (str, optional): The object whose string length is to be determined. Defaults to an empty string.

    Returns:
        int: The length of the string representation of the object. Returns 0 if any exceptions are encountered.
    """
    try:
        length = len(str(obj))
    except:
        length = 0
    return length
def line_contains(string: str = None, compare: str = None, start: int = 0, length: int = None):
    """
    Determines if the substring `compare` is present at the beginning of a section of `string` starting at the index `start` and having length `length`.

    Args:
        string (str, optional): The main string to search within. Defaults to None.
        compare (str, optional): The substring to search for. Defaults to None.
        start (int, optional): The index to start the search from. Defaults to 0.
        length (int, optional): The length of the section to consider for the search. If not specified, the length is determined safely.

    Returns:
        bool: True if the substring is found at the specified position, False otherwise.
    """
    if is_in_list(None,[string,compare]):
        return False
    if length == None:
        length = safe_len(string)
    string = string[start:length]
    if safe_len(compare)>safe_len(string):
        return False
    if string[:safe_len(compare)]==compare:
        return True
    return False

def count_slashes(url: str) -> int:
    """
    Count the number of slashes in a given URL.

    Parameters:
    url (str): The URL string in which slashes will be counted.

    Returns:
    int: The count of slashes in the URL.
    """
    return url.count('/')
def get_letters() -> list:
    """
    Get a list of lowercase letters from 'a' to 'z'.

    Returns:
    list: A list of lowercase letters.
    """

    return 'a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z'.split(',')
def get_numbers() -> list:
    """
    Get a list of numeric digits from 0 to 9.

    Returns:
    list: A list of numeric digits.
    """
    return '0,1,2,3,4,5,6,7,8,9'.split(',')

def percent_integer_of_string(obj: str, object_compare: str = "numbers") -> float:
    """
    Calculate the percentage of characters in a string that are either letters or numbers.

    Parameters:
    obj (str): The input string to analyze.
    object_compare (str, optional): The type of characters to compare against ('letters' or 'numbers').
                                    Defaults to 'numbers' if not specified.

    Returns:
    float: The percentage of characters in the string that match the specified character type.
    """
    if len(obj) == 0:
        return 0
    if object_compare.lower() not in ["number","numbers"]:
        object_compare = get_letters()
    else:
        object_compare = get_numbers()
    count = sum(1 for char in obj if char in object_compare)
    if float(0) in [float(count),float(len(obj))]:
        return 0
    return float(count) / len(obj)
def return_obj_excluded(list_obj:str, exclude:str, substitute="*"):
    """
    Replace all occurrences of a specified substring with a substitute string in a given list_obj.

    Args:
        list_obj (str): The original string in which to perform substitutions.
        exclude (str): The substring to be replaced.
        substitute (str, optional): The string to substitute for the excluded substring. Defaults to "*".

    Returns:
        str: The modified string with substitutions.
    """
    count = 0
    length_exclude = len(exclude)
    return_obj = ''
    found = False
    while count < len(list_obj):
        if list_obj[count:count+length_exclude] == exclude and not found:
            count += length_exclude
            return_obj += substitute * length_exclude
            found = True
        else:
            return_obj += list_obj[count]
            count += 1
    return return_obj

def determine_closest(string_comp:str, list_obj:str):
    """
    Find the closest consecutive substrings from 'comp' in 'list_obj'.

    Args:
        string_comp (str): The substring to search for.
        list_obj (str): The string in which to search for consecutive substrings.

    Returns:
        dict: A dictionary containing the found consecutive substrings ('comp_list') and the remaining string ('excluded_obj').
    """
    comp_list = []
    while string_comp:
        found = False
        for i in range(len(string_comp), 0, -1):
            sub = string_comp[:i]
            if sub in list_obj:
                list_obj = return_obj_excluded(list_obj=list_obj, exclude=sub)
                comp_list.append(sub)
                string_comp = string_comp[i:]
                found = True
                break
        if not found:
            break
    return {"comp_list": comp_list, "excluded_obj": list_obj}

def longest_consecutive(list_cons:list):
    """
    Calculate the length of the longest consecutive non-empty elements in a list of strings.

    Args:
        list_cons (list): A list of strings.

    Returns:
        int: The length of the longest consecutive non-empty substring.
    """
    highest = 0
    current_length = 0
    for each in list_cons:
        if len(each) > 0:
            current_length += 1
            highest = max(highest, current_length)
        else:
            current_length = 0
    return highest

def combined_list_len(list_cons:list):
    """
    Calculate the total length of a list of strings by summing their individual lengths.

    Args:
        list_cons (list): A list of strings.

    Returns:
        int: The total length of all the strings in the list.
    """
    return sum(len(each) for each in list_cons)

def percent_obj(list_cons:list, list_obj:str):
    """
    Calculate the percentage of the combined length of a list of strings relative to the length of a target string.

    Args:
        list_cons (list): A list of strings.
        list_obj (str): The target string.

    Returns:
        float: The percentage of the combined length relative to the length of the target string.
    """
    return float(combined_list_len(list_cons) / len(list_obj))
def get_highest(obj,obj_2):
    def determine_highest(highest,key,value):
        if is_number(value):
            if None in highest:
                highest=[key,value]
            else:
                if float(value) > float(highest[1]):
                    highest=[key,value]
        return highest
    highest=[None,None]
    if obj_2 != None:
        highest=determine_highest(highest,obj,obj)
        highest=determine_highest(highest,obj_2,obj_2)
        highest = highest[1]
    elif isinstance(obj,dict):
        for key,value in obj:
            highest = determine_highest(highest,key,float(value))
        
    elif isinstance(obj,list):
        for i,item in enumerate(obj):
            highest = determine_highest(highest,i,float(value))
    return highest
def create_new_name(name=None,names_list=None,default=True,match_true=False,num=0):
    if name==None:
        if default==True:
            name = 'Default_name'
        else:
            print('create_new_name from abstract_utilities.compare_utils: name was not provided and default is False, returning None... Aborting')
    if names_list != None:
        if name in names_list:
            for i in range(len(names_list)+1):
                new_name = create_new_name(name=name,num=i)
                if new_name not in names_list:
                    return new_name
        elif match_true:
            return create_new_name(name=name,num=i)
        return name
    return f'{name}_{num}'
def get_last_comp_list(string,compare_list):
    result_compare=None
    for list_item in compare_list:
        if isinstance(list_item,str):
            if string in list_item:
                result_compare = list_item
    return result_compare
def is_list_obj_in_string(list_objs,string):
    found = []
    for list_obj in make_list(list_objs):
        if list_obj in string:
            found.append(list_obj)
    return found            
def get_longest_common_portion(string, compare_string):
    for i in range(len(string), 0, -1):
        if string[:i] in compare_string:
            return string[:i]
    return ''


def get_common_portions(str1, str2):
    if not str1 or not str2:
        return ""

    matrix = [[0] * (len(str2) + 1) for _ in range(len(str1) + 1)]
    longest, x_longest = 0, 0

    for x in range(1, len(str1) + 1):
        for y in range(1, len(str2) + 1):
            if str1[x - 1] == str2[y - 1]:
                matrix[x][y] = matrix[x - 1][y - 1] + 1
                if matrix[x][y] > longest:
                    longest = matrix[x][y]
                    x_longest = x
            else:
                matrix[x][y] = 0

    return str1[x_longest - longest: x_longest]
def find_max_beginning_match_length(comp_obj, common_portions):
    for portion in common_portions:
        if comp_obj.startswith(portion):
            return len(portion) / len(comp_obj)
    return 0
def get_portions(string,compare_string,comp_set):
    for i,char in enumerate(string):
        found = get_portion_in_string(string[i:],compare_string)
        if found:
            comp_set.add(found)
            #input(f"{found} from {string[i:]} found in {compare_string}")
    return comp_set
def get_portion_in_string(string,compare_string):
    found = ''

    for i,char in enumerate(string):
        
        if i == 0:
            curr_portion = string[0]
        elif i == len(string)-1:
            curr_portion = string
        else:
            curr_portion = string[:i]
        if curr_portion and curr_portion in compare_string:
            found = curr_portion
            
        elif curr_portion  and curr_portion not in compare_string:
            break

    return found
def get_closest_match_from_list(comp_obj:str, total_list:list,case_sensative:bool=True):
    if isinstance(comp_obj,str):
        total_list_i= [i for i in range(len(total_list)) if isinstance(total_list[i],(str))]
        if not case_sensative:
            pre_processed_list = [total_list[i] for i in total_list_i]
        else:
            comp_obj=str(comp_obj).lower()
            pre_processed_list= [str(total_list[i]).lower() for i in total_list_i]
    else:
        total_list_i= [i for i in range(len(total_list)) if isinstance(comp_obj,type(total_list[i]))]
        pre_processed_list= [str(total_list[i]).lower() for i in total_list_i]
    highest={}
    total_found=[]
    for i,obj in enumerate(pre_processed_list):
        if comp_obj==obj:
            return total_list[total_list_i[i]]
        found = get_portions(obj,comp_obj,set())
        if found:
            found_ls = [len(str(obj)) for obj in found]
            found_ls.sort()
            length = len(comp_obj)/len(obj)
            longest_found = found_ls[-1]
            characters_shared = get_common_portions(comp_obj,obj)
            comp_curr_js = {"obj":total_list[total_list_i[i]],"found":found,
                            "longest_found":longest_found,
                            "length":length,
                            "characters_shared":characters_shared}
            if length<=1:
                if comp_obj in found:
                    total_found.append(total_list[total_list_i[i]])
                highest = highest or comp_curr_js
                if comp_curr_js["longest_found"] == highest["longest_found"]:
                    if comp_curr_js["length"] > highest["length"]:
                        highest =comp_curr_js
                elif comp_curr_js["longest_found"] > highest["longest_found"]:
                    highest =comp_curr_js
    if total_found:
        return total_found[0]
    return highest.get('obj') 
