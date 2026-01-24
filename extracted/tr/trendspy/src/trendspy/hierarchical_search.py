from typing import Dict, List, Optional
import re

def flatten_tree(node, parent_id='', result=None, join_ids=True):
    """
    Recursively transforms a tree structure into a flat list.
    
    Args:
        node (dict): Tree node with 'name', 'id' and optional 'children' keys
        parent_id (str): Parent node ID
        result (list): Accumulated result
        join_ids (bool): Whether to join IDs with parent (True for geo, False for categories)
        
    Returns:
        list: List of dictionaries with name and id
    """
    if result is None:
        result = []
    
    current_id = node['id']
    # Join IDs only for geographical data
    if join_ids and parent_id:
        full_id = f"{parent_id}-{current_id}"
    else:
        full_id = current_id
    
    result.append({
        'name': node['name'],
        'id': full_id
    })
    
    if 'children' in node:
        for child in node['children']:
            flatten_tree(child, full_id if join_ids else '', result, join_ids)
    
    return result

class HierarchicalIndex:
    """
    An index for efficient searches in hierarchical Google Trends data structures.

    This class provides fast lookups for hierarchical data like locations and categories,
    supporting both exact and partial matching of names.

    Examples:
        - Geographical hierarchies (Country -> Region -> City)
        - Category hierarchies (Main category -> Subcategory)

    Methods:
        add_item(item): Add an item to the index
        exact_search(name): Find exact match for name
        partial_search(query): Find items containing the query
        id_search(id_query): Find by ID (supports both exact and partial matching)
    """
    
    def __init__(self, items: List[dict], partial_id_search: bool = True):
        """
        Initialize the search index.
        
        Args:
            items (List[dict]): List of dictionaries with 'name' and 'id'
            partial_id_search (bool): Whether to allow partial ID matches 
                (True for geo locations, False for categories)
        """
        # Main storage: dict with lowercase name as key
        self.name_to_item: Dict[str, dict] = {}
        
        # Inverted index for partial matching
        self.word_index: Dict[str, List[str]] = {}
        
        # Store search mode
        self.partial_id_search = partial_id_search
        
        # Build indexes
        for item in items:
            self.add_item(item)
    
    def add_item(self, item: dict) -> None:
        """
        Add a single item to the index.
        
        Args:
            item (dict): Dictionary with 'name' and 'id'
        """
        name = item['name'].lower()
        
        # Add to main storage
        self.name_to_item[name] = item
        
        # Split name into words and add to inverted index
        words = set(re.split(r'\W+', name))
        for word in words:
            if word:
                if word not in self.word_index:
                    self.word_index[word] = []
                self.word_index[word].append(name)
    
    def exact_search(self, name: str) -> Optional[dict]:
        """
        Perform exact name search (case-insensitive).
        
        Args:
            name (str): Name to search for
            
        Returns:
            Optional[dict]: Item dictionary if found, None otherwise
        """
        return self.name_to_item.get(name.lower())
    
    def partial_search(self, query: str) -> List[dict]:
        """
        Perform partial name search (case-insensitive).
        
        Args:
            query (str): Search query string
            
        Returns:
            List[dict]: List of matching item dictionaries
        """
        query = query.lower()
        results = set()
        
        # Search for partial matches in word index
        for word, items in self.word_index.items():
            if query in word:
                results.update(items)
        
        # Also check if query matches any part of full names
        for name in self.name_to_item:
            if query in name:
                results.add(name)
        
        # Return found items
        return [self.name_to_item[name] for name in results]
    
    def id_search(self, id_query: str) -> List[dict]:
        """
        Search by ID.
        
        Args:
            id_query (str): ID or partial ID to search for
            
        Returns:
            List[dict]: List of matching item dictionaries
        """
        if self.partial_id_search:
            # For geo data - allow partial matches
            return [item for item in self.name_to_item.values() 
                   if id_query in item['id']]
        else:
            # For categories - only exact matches
            return [item for item in self.name_to_item.values() 
                   if item['id'] == id_query]

def create_hierarchical_index(tree_data: dict, join_ids: bool = True) -> HierarchicalIndex:
    """
    Create a complete search system from a hierarchical tree structure.
    
    Args:
        tree_data (dict): Original tree structure
        join_ids (bool): Whether to join IDs with parent 
            (True for geo locations, False for categories)
        
    Returns:
        HierarchicalIndex: Initialized search system
    """
    # First flatten the tree
    flat_items = flatten_tree(tree_data, join_ids=join_ids)
    # Then create and return the search index
    return HierarchicalIndex(flat_items, partial_id_search=join_ids)