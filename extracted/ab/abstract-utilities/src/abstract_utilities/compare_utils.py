"""
compare_utils.py
Part of the abstract_utilities package

This script provides utility functions for comparing strings and objects. These functions include methods for calculating string similarity and comparing the lengths of objects.

Author: putkoff
Date: 05/31/2023
Version: 0.1.2
"""
import string
from .type_utils import is_number
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
def get_closest_match_from_list(comp_str:str, total_list:list,case_sensative:bool=True):
    """
    Find the closest match from a list of strings based on various criteria.

    Args:
        comp_str (str): The target string to find the closest match for.
        total_list (list): A list of strings to search for a match.

    Returns:
        str or None: The string from the 'total_list' that best matches the 'comp_str' based on criteria
                     such as longest consecutive substring, combined length of consecutive substrings,
                     and percentage of combined length relative to the length of the 'comp_str'.
                     Returns None if no match is found.
    """
    def get_highest(highest,result,list_obj):
        if highest is None:
            highest = {
                "longest_consecutive": longest_consecutive(result["comp_list"]),
                "combined_length": combined_list_len(result["comp_list"]),
                "per_obj": percent_obj(result["comp_list"], list_obj),
                "list_obj": list_obj,
            }
        else:
            current = {
                "longest_consecutive": longest_consecutive(result["comp_list"]),
                "combined_length": combined_list_len(result["comp_list"]),
                "per_obj": percent_obj(result["comp_list"], list_obj),
                "list_obj": list_obj,
            }
            if current["per_obj"] > highest["per_obj"]:
                highest = current
        return highest
    def untuple(obj):
        if isinstance(obj,tuple):
            obj=obj[0]
        return obj
    def make_list(obj):
        if isinstance(obj,(set,tuple)):
            obj=list(obj)
        else:
            obj=[obj]
        return obj
    best_match = None
    best_match_score = {"longest_consecutive": 0, "combined_length": 0, "per_obj": 0, "total_score": 0}
    highest = None
    all_score={}

    
    comp_strs=make_list(comp_str)
    for comp_str in comp_strs:
        for list_obj in total_list:
            comp_comp_str = untuple(comp_str)
            comp_list_obj=list_obj
            if case_sensative:
                comp_comp_str = comp_comp_str.lower()
                comp_list_obj=comp_list_obj.lower()
            result = determine_closest(comp_comp_str, comp_list_obj)
            if len(result["comp_list"]) != 0:
                if len(comp_str) <= len(list_obj):
                    highest = get_highest(highest,result,list_obj)
        all_score[comp_str]=highest
    highest=None
    for key,value in all_score.items():
        if highest == None:
            highest = value
        else:
            if value["per_obj"] > value["per_obj"]:
                highest = value
    if highest is None:
        return None
    return highest["list_obj"]

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
def get_closest_match_from_list(comp_str:str, total_list:list,case_sensative:bool=True):
    """
    Find the closest match from a list of strings based on various criteria.

    Args:
        comp_str (str): The target string to find the closest match for.
        total_list (list): A list of strings to search for a match.

    Returns:
        str or None: The string from the 'total_list' that best matches the 'comp_str' based on criteria
                     such as longest consecutive substring, combined length of consecutive substrings,
                     and percentage of combined length relative to the length of the 'comp_str'.
                     Returns None if no match is found.
    """
    def get_highest(highest,result,list_obj):
        if highest is None:
            highest = {
                "longest_consecutive": longest_consecutive(result["comp_list"]),
                "combined_length": combined_list_len(result["comp_list"]),
                "per_obj": percent_obj(result["comp_list"], list_obj),
                "list_obj": list_obj,
            }
        else:
            current = {
                "longest_consecutive": longest_consecutive(result["comp_list"]),
                "combined_length": combined_list_len(result["comp_list"]),
                "per_obj": percent_obj(result["comp_list"], list_obj),
                "list_obj": list_obj,
            }
            if current["per_obj"] > highest["per_obj"]:
                highest = current
        return highest
    def untuple(obj):
        if isinstance(obj,tuple):
            obj=obj[0]
        return obj
    best_match = None
    best_match_score = {"longest_consecutive": 0, "combined_length": 0, "per_obj": 0, "total_score": 0}
    highest = None
    all_score={}
    if isinstance(comp_str,(dict,set,tuple)):
        comp_strs=list(comp_str)
    else:
        comp_strs=[comp_str]

    comp_strs=comp_str if isinstance(comp_str,list) else [comp_str] 
    for comp_str in comp_strs:
        for list_obj in total_list:
            comp_comp_str = untuple(comp_str)
            comp_list_obj=list_obj
            if case_sensative:
                comp_comp_str = comp_comp_str.lower()
                comp_list_obj=comp_list_obj.lower()
            result = determine_closest(comp_comp_str, comp_list_obj)
            if len(result["comp_list"]) != 0:
                if len(comp_str) <= len(list_obj):
                    highest = get_highest(highest,result,list_obj)
        all_score[comp_str]=highest
    highest=None
    for key,value in all_score.items():
        if highest == None:
            highest = value
        else:
            if value["per_obj"] > value["per_obj"]:
                highest = value
    if highest is None:
        return None
    return highest["list_obj"]
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
