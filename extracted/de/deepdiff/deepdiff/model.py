import logging
from collections.abc import Mapping
from copy import copy
from deepdiff.helper import (
    RemapDict, strings, notpresent, get_type, numpy_numbers, np, literal_eval_extended,
    dict_, SetOrdered)
from deepdiff.path import stringify_element

logger = logging.getLogger(__name__)

FORCE_DEFAULT = 'fake'
UP_DOWN = {'up': 'down', 'down': 'up'}

REPORT_KEYS = {
    "type_changes",
    "dictionary_item_added",
    "dictionary_item_removed",
    "values_changed",
    "unprocessed",
    "iterable_item_added",
    "iterable_item_removed",
    "iterable_item_moved",
    "attribute_added",
    "attribute_removed",
    "set_item_removed",
    "set_item_added",
    "repetition_change",
}

CUSTOM_FIELD = "__internal:custom:extra_info"


class DoesNotExist(Exception):
    pass


class ResultDict(RemapDict):

    def remove_empty_keys(self):
        """
        Remove empty keys from this object. Should always be called after the result is final.
        :return:
        """
        empty_keys = [k for k, v in self.items() if not isinstance(v, (int)) and not v]

        for k in empty_keys:
            del self[k]


class TreeResult(ResultDict):
    def __init__(self):
        for key in REPORT_KEYS:
            self[key] = SetOrdered()

    def mutual_add_removes_to_become_value_changes(self):
        """
        There might be the same paths reported in the results as removed and added.
        In such cases they should be reported as value_changes.

        Note that this function mutates the tree in ways that causes issues when report_repetition=True
        and should be avoided in that case.

        This function should only be run on the Tree Result.
        """
        iterable_item_added = self.get('iterable_item_added')
        iterable_item_removed = self.get('iterable_item_removed')
        if iterable_item_added is not None and iterable_item_removed is not None:
            added_paths = {i.path(): i for i in iterable_item_added}
            removed_paths = {i.path(): i for i in iterable_item_removed}
            mutual_paths = set(added_paths) & set(removed_paths)

            if mutual_paths and 'values_changed' not in self or self['values_changed'] is None:
                self['values_changed'] = SetOrdered()
            for path in mutual_paths:
                level_before = removed_paths[path]
                iterable_item_removed.remove(level_before)
                level_after = added_paths[path]
                iterable_item_added.remove(level_after)
                level_before.t2 = level_after.t2
                self['values_changed'].add(level_before)  # type: ignore
                level_before.report_type = 'values_changed'
        if 'iterable_item_removed' in self and not iterable_item_removed:
            del self['iterable_item_removed']
        if 'iterable_item_added' in self and not iterable_item_added:
            del self['iterable_item_added']

    def __getitem__(self, item):
        if item not in self:
            self[item] = SetOrdered()
        return self.get(item)

    def __len__(self):
        length = 0
        for value in self.values():
            if isinstance(value, SetOrdered):
                length += len(value)
            elif isinstance(value, int):
                length += 1
        return length


class TextResult(ResultDict):
    ADD_QUOTES_TO_STRINGS = True

    def __init__(self, tree_results=None, verbose_level=1):
        self.verbose_level = verbose_level
        # TODO: centralize keys
        self.update({
            "type_changes": dict_(),
            "dictionary_item_added": self.__set_or_dict(),
            "dictionary_item_removed": self.__set_or_dict(),
            "values_changed": dict_(),
            "unprocessed": [],
            "iterable_item_added": dict_(),
            "iterable_item_removed": dict_(),
            "iterable_item_moved": dict_(),
            "attribute_added": self.__set_or_dict(),
            "attribute_removed": self.__set_or_dict(),
            "set_item_removed": SetOrdered(),
            "set_item_added": SetOrdered(),
            "repetition_change": dict_()
        })

        if tree_results:
            self._from_tree_results(tree_results)

    def __set_or_dict(self):
        return {} if self.verbose_level >= 2 else SetOrdered()

    def _from_tree_results(self, tree):
        """
        Populate this object by parsing an existing reference-style result dictionary.
        :param tree: A TreeResult
        :return:
        """
        self._from_tree_type_changes(tree)
        self._from_tree_default(tree, 'dictionary_item_added')
        self._from_tree_default(tree, 'dictionary_item_removed')
        self._from_tree_value_changed(tree)
        self._from_tree_unprocessed(tree)
        self._from_tree_default(tree, 'iterable_item_added')
        self._from_tree_default(tree, 'iterable_item_removed')
        self._from_tree_iterable_item_moved(tree)
        self._from_tree_default(tree, 'attribute_added')
        self._from_tree_default(tree, 'attribute_removed')
        self._from_tree_set_item_removed(tree)
        self._from_tree_set_item_added(tree)
        self._from_tree_repetition_change(tree)
        self._from_tree_deep_distance(tree)
        self._from_tree_custom_results(tree)

    def _from_tree_default(self, tree, report_type, ignore_if_in_iterable_opcodes=False):
        if report_type in tree:
                
            for change in tree[report_type]:  # report each change
                # When we convert from diff to delta result, we care more about opcodes than iterable_item_added or removed
                if (
                    ignore_if_in_iterable_opcodes
                    and report_type in {"iterable_item_added", "iterable_item_removed"}
                    and change.up.path(force=FORCE_DEFAULT) in self["_iterable_opcodes"]
                ):
                    continue
                # determine change direction (added or removed)
                # Report t2 (the new one) whenever possible.
                # In cases where t2 doesn't exist (i.e. stuff removed), report t1.
                if change.t2 is not notpresent:
                    item = change.t2
                else:
                    item = change.t1

                # do the reporting
                report = self[report_type]
                if isinstance(report, SetOrdered):
                    report.add(change.path(force=FORCE_DEFAULT))
                elif isinstance(report, dict):
                    report[change.path(force=FORCE_DEFAULT)] = item
                elif isinstance(report, list):  # pragma: no cover
                    # we don't actually have any of those right now, but just in case
                    report.append(change.path(force=FORCE_DEFAULT))
                else:  # pragma: no cover
                    # should never happen
                    raise TypeError("Cannot handle {} report container type.".
                                    format(report))

    def _from_tree_type_changes(self, tree):
        if 'type_changes' in tree:
            for change in tree['type_changes']:
                path = change.path(force=FORCE_DEFAULT)
                if type(change.t1) is type:
                    include_values = False
                    old_type = change.t1
                    new_type = change.t2
                else:
                    include_values = True
                    old_type = get_type(change.t1)
                    new_type = get_type(change.t2)
                remap_dict = RemapDict({
                    'old_type': old_type,
                    'new_type': new_type,
                })
                if self.verbose_level > 1:
                    new_path = change.path(use_t2=True, force=FORCE_DEFAULT)
                    if path != new_path:
                        remap_dict['new_path'] = new_path
                self['type_changes'][path] = remap_dict
                if self.verbose_level and include_values:
                    remap_dict.update(old_value=change.t1, new_value=change.t2)

    def _from_tree_value_changed(self, tree):
        if 'values_changed' in tree and self.verbose_level > 0:
            for change in tree['values_changed']:
                path = change.path(force=FORCE_DEFAULT)
                the_changed = {'new_value': change.t2, 'old_value': change.t1}
                if self.verbose_level > 1:
                    new_path = change.path(use_t2=True, force=FORCE_DEFAULT)
                    if path != new_path:
                        the_changed['new_path'] = new_path
                self['values_changed'][path] = the_changed
                if 'diff' in change.additional:
                    the_changed.update({'diff': change.additional['diff']})

    def _from_tree_iterable_item_moved(self, tree):
        if 'iterable_item_moved' in tree and self.verbose_level > 1:

            for change in tree['iterable_item_moved']:
                the_changed = {'new_path': change.path(use_t2=True, reporting_move=True), 'value': change.t2}
                self['iterable_item_moved'][change.path(
                    force=FORCE_DEFAULT, use_t2=False, reporting_move=True)] = the_changed

    def _from_tree_unprocessed(self, tree):
        if 'unprocessed' in tree:
            for change in tree['unprocessed']:
                self['unprocessed'].append("{}: {} and {}".format(change.path(
                    force=FORCE_DEFAULT), change.t1, change.t2))

    def _from_tree_set_item_added_or_removed(self, tree, key):
        if key in tree:
            set_item_info = self[key]
            is_dict = isinstance(set_item_info, Mapping)
            for change in tree[key]:
                path = change.up.path(
                )  # we want't the set's path, the added item is not directly accessible
                item = change.t2 if key == 'set_item_added' else change.t1
                if self.ADD_QUOTES_TO_STRINGS and isinstance(item, strings):
                    item = "'%s'" % item
                if is_dict:
                    if path not in set_item_info:
                        set_item_info[path] = set()  # type: ignore
                    set_item_info[path].add(item)
                else:
                    set_item_info.add("{}[{}]".format(path, str(item)))
                    # this syntax is rather peculiar, but it's DeepDiff 2.x compatible)

    def _from_tree_set_item_added(self, tree):
        self._from_tree_set_item_added_or_removed(tree, key='set_item_added')

    def _from_tree_set_item_removed(self, tree):
        self._from_tree_set_item_added_or_removed(tree, key='set_item_removed')

    def _from_tree_repetition_change(self, tree):
        if 'repetition_change' in tree:
            for change in tree['repetition_change']:
                path = change.path(force=FORCE_DEFAULT)
                self['repetition_change'][path] = RemapDict(
                    change.additional['repetition']
                )
                self['repetition_change'][path]['value'] = change.t1

    def _from_tree_deep_distance(self, tree):
        if 'deep_distance' in tree:
            self['deep_distance'] = tree['deep_distance']

    def _from_tree_custom_results(self, tree):
        for k, _level_list in tree.items():
            if k not in REPORT_KEYS:
                if not isinstance(_level_list, SetOrdered):
                    continue

                # if len(_level_list) == 0:
                #     continue
                #
                # if not isinstance(_level_list[0], DiffLevel):
                #     continue

                # _level_list is a list of DiffLevel
                _custom_dict = {}
                for _level in _level_list:
                    _custom_dict[_level.path(
                        force=FORCE_DEFAULT)] = _level.additional.get(CUSTOM_FIELD, {})
                self[k] = _custom_dict


class DeltaResult(TextResult):
    ADD_QUOTES_TO_STRINGS = False

    def __init__(self, tree_results=None, ignore_order=None, always_include_values=False, _iterable_opcodes=None):
        self.ignore_order = ignore_order
        self.always_include_values = always_include_values

        self.update({
            "type_changes": dict_(),
            "dictionary_item_added": dict_(),
            "dictionary_item_removed": dict_(),
            "values_changed": dict_(),
            "iterable_item_added": dict_(),
            "iterable_item_removed": dict_(),
            "iterable_item_moved": dict_(),
            "attribute_added": dict_(),
            "attribute_removed": dict_(),
            "set_item_removed": dict_(),
            "set_item_added": dict_(),
            "iterable_items_added_at_indexes": dict_(),
            "iterable_items_removed_at_indexes": dict_(),
            "_iterable_opcodes": _iterable_opcodes or {},
        })

        if tree_results:
            self._from_tree_results(tree_results)

    def _from_tree_results(self, tree):
        """
        Populate this object by parsing an existing reference-style result dictionary.
        :param tree: A TreeResult
        :return:
        """
        self._from_tree_type_changes(tree)
        self._from_tree_default(tree, 'dictionary_item_added')
        self._from_tree_default(tree, 'dictionary_item_removed')
        self._from_tree_value_changed(tree)
        if self.ignore_order:
            self._from_tree_iterable_item_added_or_removed(
                tree, 'iterable_item_added', delta_report_key='iterable_items_added_at_indexes')
            self._from_tree_iterable_item_added_or_removed(
                tree, 'iterable_item_removed', delta_report_key='iterable_items_removed_at_indexes')
        else:
            self._from_tree_default(tree, 'iterable_item_added', ignore_if_in_iterable_opcodes=True)
            self._from_tree_default(tree, 'iterable_item_removed', ignore_if_in_iterable_opcodes=True)
            self._from_tree_iterable_item_moved(tree)
        self._from_tree_default(tree, 'attribute_added')
        self._from_tree_default(tree, 'attribute_removed')
        self._from_tree_set_item_removed(tree)
        self._from_tree_set_item_added(tree)
        self._from_tree_repetition_change(tree)

    def _from_tree_iterable_item_added_or_removed(self, tree, report_type, delta_report_key):
        if report_type in tree:
            for change in tree[report_type]:  # report each change
                # determine change direction (added or removed)
                # Report t2 (the new one) whenever possible.
                # In cases where t2 doesn't exist (i.e. stuff removed), report t1.
                if change.t2 is not notpresent:
                    item = change.t2
                else:
                    item = change.t1

                # do the reporting
                path, param, _ = change.path(force=FORCE_DEFAULT, get_parent_too=True)
                try:
                    iterable_items_added_at_indexes = self[delta_report_key][path]
                except KeyError:
                    iterable_items_added_at_indexes = self[delta_report_key][path] = dict_()
                iterable_items_added_at_indexes[param] = item

    def _from_tree_type_changes(self, tree):
        if 'type_changes' in tree:
            for change in tree['type_changes']:
                include_values = None
                if type(change.t1) is type:
                    include_values = False
                    old_type = change.t1
                    new_type = change.t2
                else:
                    old_type = get_type(change.t1)
                    new_type = get_type(change.t2)
                    include_values = True
                    try:
                        if new_type in numpy_numbers:
                            new_t1 = change.t1.astype(new_type)
                            include_values = not np.array_equal(new_t1, change.t2)
                        else:
                            new_t1 = new_type(change.t1)
                            # If simply applying the type from one value converts it to the other value,
                            # there is no need to include the actual values in the delta.
                            include_values = new_t1 != change.t2
                    except Exception:
                        pass

                path = change.path(force=FORCE_DEFAULT)
                new_path = change.path(use_t2=True, force=FORCE_DEFAULT)
                remap_dict = RemapDict({
                    'old_type': old_type,
                    'new_type': new_type,
                })
                if path != new_path:
                    remap_dict['new_path'] = new_path
                self['type_changes'][path] = remap_dict
                if include_values or self.always_include_values:
                    remap_dict.update(old_value=change.t1, new_value=change.t2)

    def _from_tree_value_changed(self, tree):
        if 'values_changed' in tree:
            for change in tree['values_changed']:
                path = change.path(force=FORCE_DEFAULT)
                new_path = change.path(use_t2=True, force=FORCE_DEFAULT)
                the_changed = {'new_value': change.t2, 'old_value': change.t1}
                if path != new_path:
                    the_changed['new_path'] = new_path
                self['values_changed'][path] = the_changed
                # If we ever want to store the difflib results instead of the new_value
                # these lines need to be uncommented and the Delta object needs to be able
                # to use them.
                # if 'diff' in change.additional:
                #     the_changed.update({'diff': change.additional['diff']})

    def _from_tree_repetition_change(self, tree):
        if 'repetition_change' in tree:
            for change in tree['repetition_change']:
                path, _, _ = change.path(get_parent_too=True)
                repetition = RemapDict(change.additional['repetition'])
                value = change.t1
                try:
                    iterable_items_added_at_indexes = self['iterable_items_added_at_indexes'][path]
                except KeyError:
                    iterable_items_added_at_indexes = self['iterable_items_added_at_indexes'][path] = dict_()
                for index in repetition['new_indexes']:
                    iterable_items_added_at_indexes[index] = value

    def _from_tree_iterable_item_moved(self, tree):
        if 'iterable_item_moved' in tree:
            for change in tree['iterable_item_moved']:
                if (
                    change.up.path(force=FORCE_DEFAULT, reporting_move=True) not in self["_iterable_opcodes"]
                ):
                    the_changed = {'new_path': change.path(use_t2=True, reporting_move=True), 'value': change.t2}
                    self['iterable_item_moved'][change.path(
                        force=FORCE_DEFAULT, reporting_move=True)] = the_changed


class DiffLevel:
    """
    An object of this class represents a single object-tree-level in a reported change.
    A double-linked list of these object describes a single change on all of its levels.
    Looking at the tree of all changes, a list of those objects represents a single path through the tree
    (which is just fancy for "a change").
    This is the result object class for object reference style reports.

    Example:

    >>> t1 = {2: 2, 4: 44}
    >>> t2 = {2: "b", 5: 55}
    >>> ddiff = DeepDiff(t1, t2, view='tree')
    >>> ddiff
    {'dictionary_item_added': {<DiffLevel id:4560126096, t1:None, t2:55>},
     'dictionary_item_removed': {<DiffLevel id:4560126416, t1:44, t2:None>},
     'type_changes': {<DiffLevel id:4560126608, t1:2, t2:b>}}

    Graph:

    <DiffLevel id:123, original t1,t2>          <DiffLevel id:200, original t1,t2>
                    ↑up                                         ↑up
                    |                                           |
                    | ChildRelationship                         | ChildRelationship
                    |                                           |
                    ↓down                                       ↓down
    <DiffLevel id:13, t1:None, t2:55>            <DiffLevel id:421, t1:44, t2:None>
    .path() = 'root[5]'                         .path() = 'root[4]'

    Note that the 2 top level DiffLevel objects are 2 different objects even though
    they are essentially talking about the same diff operation.


    A ChildRelationship object describing the relationship between t1 and it's child object,
    where t1's child object equals down.t1.

    Think about it like a graph:

    +---------------------------------------------------------------+
    |                                                               |
    |    parent                 difflevel                 parent    |
    |      +                          ^                     +       |
    +------|--------------------------|---------------------|-------+
           |                      |   | up                  |
           | Child                |   |                     | ChildRelationship
           | Relationship         |   |                     |
           |                 down |   |                     |
    +------|----------------------|-------------------------|-------+
    |      v                      v                         v       |
    |    child                  difflevel                 child     |
    |                                                               |
    +---------------------------------------------------------------+


    The child_rel example:

    # dictionary_item_removed is a set so in order to get an item from it:
    >>> (difflevel,) = ddiff['dictionary_item_removed'])
    >>> difflevel.up.t1_child_rel
    <DictRelationship id:456, parent:{2: 2, 4: 44}, child:44, param:4>

    >>> (difflevel,) = ddiff['dictionary_item_added'])
    >>> difflevel
    <DiffLevel id:4560126096, t1:None, t2:55>

    >>> difflevel.up
    >>> <DiffLevel id:4560154512, t1:{2: 2, 4: 44}, t2:{2: 'b', 5: 55}>

    >>> difflevel.up
    <DiffLevel id:4560154512, t1:{2: 2, 4: 44}, t2:{2: 'b', 5: 55}>

    # t1 didn't exist
    >>> difflevel.up.t1_child_rel

    # t2 is added
    >>> difflevel.up.t2_child_rel
    <DictRelationship id:4560154384, parent:{2: 'b', 5: 55}, child:55, param:5>

    """

    def __init__(self,
                 t1,
                 t2,
                 down=None,
                 up=None,
                 report_type=None,
                 child_rel1=None,
                 child_rel2=None,
                 additional=None,
                 verbose_level=1):
        """
        :param child_rel1: Either:
                            - An existing ChildRelationship object describing the "down" relationship for t1; or
                            - A ChildRelationship subclass. In this case, we will create the ChildRelationship objects
                              for both t1 and t2.
                            Alternatives for child_rel1 and child_rel2 must be used consistently.
        :param child_rel2: Either:
                            - An existing ChildRelationship object describing the "down" relationship for t2; or
                            - The param argument for a ChildRelationship class we shall create.
                           Alternatives for child_rel1 and child_rel2 must be used consistently.
        """

        # The current-level object in the left hand tree
        self.t1 = t1

        # The current-level object in the right hand tree
        self.t2 = t2

        # Another DiffLevel object describing this change one level deeper down the object tree
        self.down = down

        # Another DiffLevel object describing this change one level further up the object tree
        self.up = up

        self.report_type = report_type

        # If this object is this change's deepest level, this contains a string describing the type of change.
        # Examples: "set_item_added", "values_changed"

        # Note: don't use {} as additional's default value - this would turn out to be always the same dict object
        self.additional = dict_() if additional is None else additional

        # For some types of changes we store some additional information.
        # This is a dict containing this information.
        # Currently, this is used for:
        # - values_changed: In case the changes data is a multi-line string,
        #                   we include a textual diff as additional['diff'].
        # - repetition_change: additional['repetition']:
        #                      e.g. {'old_repeat': 2, 'new_repeat': 1, 'old_indexes': [0, 2], 'new_indexes': [2]}
        # the user supplied ChildRelationship objects for t1 and t2

        # A ChildRelationship object describing the relationship between t1 and it's child object,
        # where t1's child object equals down.t1.
        # If this relationship is representable as a string, str(self.t1_child_rel) returns a formatted param parsable python string,
        # e.g. "[2]", ".my_attribute"
        self.t1_child_rel = child_rel1

        # Another ChildRelationship object describing the relationship between t2 and it's child object.
        self.t2_child_rel = child_rel2

        # Will cache result of .path() per 'force' as key for performance
        self._path = dict_()

        self.verbose_level = verbose_level

    def __repr__(self):
        if self.verbose_level:
            from deepdiff.summarize import summarize

            if self.additional:
                additional_repr = summarize(self.additional, max_length=35)
                result = "<{} {}>".format(self.path(), additional_repr)
            else:
                t1_repr = summarize(self.t1, max_length=35)
                t2_repr = summarize(self.t2, max_length=35)
                result = "<{} t1:{}, t2:{}>".format(self.path(), t1_repr, t2_repr)
        else:
            result = "<{}>".format(self.path())
        return result

    def __setattr__(self, key, value):
        # Setting up or down, will set the opposite link in this linked list.
        if key in UP_DOWN and value is not None:
            self.__dict__[key] = value
            opposite_key = UP_DOWN[key]
            value.__dict__[opposite_key] = self
        else:
            self.__dict__[key] = value

    def __iter__(self):
        yield self.t1
        yield self.t2

    @property
    def repetition(self):
        return self.additional['repetition']

    def auto_generate_child_rel(self, klass, param, param2=None):
        """
        Auto-populate self.child_rel1 and self.child_rel2.
        This requires self.down to be another valid DiffLevel object.
        :param klass: A ChildRelationship subclass describing the kind of parent-child relationship,
                      e.g. DictRelationship.
        :param param: A ChildRelationship subclass-dependent parameter describing how to get from parent to child,
                      e.g. the key in a dict
        """
        if self.down.t1 is not notpresent:  # type: ignore
            self.t1_child_rel = ChildRelationship.create(
                klass=klass, parent=self.t1, child=self.down.t1, param=param)  # type: ignore
        if self.down.t2 is not notpresent:  # type: ignore
            self.t2_child_rel = ChildRelationship.create(
                klass=klass, parent=self.t2, child=self.down.t2, param=param if param2 is None else param2)  # type: ignore

    @property
    def all_up(self):
        """
        Get the root object of this comparison.
        (This is a convenient wrapper for following the up attribute as often as you can.)
        :rtype: DiffLevel
        """
        level = self
        while level.up:
            level = level.up
        return level

    @property
    def all_down(self):
        """
        Get the leaf object of this comparison.
        (This is a convenient wrapper for following the down attribute as often as you can.)
        :rtype: DiffLevel
        """
        level = self
        while level.down:
            level = level.down
        return level

    @staticmethod
    def _format_result(root, result):
        return None if result is None else "{}{}".format(root, result)

    def get_root_key(self, use_t2=False):
        """
        Get the path's root key value for this change

        For example if the path to the element that is reported to have a change in value is root['X'][0]
        then get_root_key should return 'X'
        """
        root_level = self.all_up
        if(use_t2):
            next_rel = root_level.t2_child_rel
        else:
            next_rel = root_level.t1_child_rel or root_level.t2_child_rel  # next relationship object to get a formatted param from

        if next_rel:
            return next_rel.param
        return notpresent

    def path(self, root="root", force=None, get_parent_too=False, use_t2=False, output_format='str', reporting_move=False):
        """
        A python syntax string describing how to descend to this level, assuming the top level object is called root.
        Returns None if the path is not representable as a string.
        This might be the case for example if there are sets involved (because then there's not path at all) or because
        custom objects used as dictionary keys (then there is a path but it's not representable).
        Example: root['ingredients'][0]
        Note: We will follow the left side of the comparison branch, i.e. using the t1's to build the path.
        Using t1 or t2 should make no difference at all, except for the last step of a child-added/removed relationship.
        If it does in any other case, your comparison path is corrupt.

        **Parameters**

        :param root: The result string shall start with this var name
        :param force: Bends the meaning of "no string representation".
                      If None:
                        Will strictly return Python-parsable expressions. The result those yield will compare
                        equal to the objects in question.
                      If 'yes':
                        Will return a path including '(unrepresentable)' in place of non string-representable parts.
                      If 'fake':
                        Will try to produce an output optimized for readability.
                        This will pretend all iterables are subscriptable, for example.
        :param output_format: The format of the output. The options are 'str' which is the default and produces a
                              string representation of the path or 'list' to produce a list of keys and attributes
                              that produce the path.

        :param reporting_move: This should be set to true if and only if we are reporting on iterable_item_moved.
                               All other cases should leave this set to False.
        """
        # TODO: We could optimize this by building on top of self.up's path if it is cached there
        cache_key = "{}{}{}{}".format(force, get_parent_too, use_t2, output_format)
        if cache_key in self._path:
            cached = self._path[cache_key]
            if get_parent_too:
                parent, param, result = cached
                return (self._format_result(root, parent), param, self._format_result(root, result))
            else:
                return self._format_result(root, cached)

        if output_format == 'str':
            result = parent = param = ""
        else:
            result = []

        level = self.all_up  # start at the root

        # traverse all levels of this relationship
        while level and level is not self:
            # get this level's relationship object
            if level.additional.get("moved") and not reporting_move:
                # To ensure we can properly replay items such as values_changed in items that may have moved, we
                # need to make sure that all paths are reported relative to t2 if a level has reported a move.
                # If we are reporting a move, the path is already correct and does not need to be swapped.
                # Additional context of "moved" is only ever set if using iterable_compare_func and a move has taken place.
                level_use_t2 = not use_t2
            else:
                level_use_t2 = use_t2

            if level_use_t2:
                next_rel = level.t2_child_rel or level.t1_child_rel
            else:
                next_rel = level.t1_child_rel or level.t2_child_rel  # next relationship object to get a formatted param from

            # t1 and t2 both are empty
            if next_rel is None:
                break

            # Build path for this level
            if output_format == 'str':
                item = next_rel.get_param_repr(force)
                if item:
                    parent = result
                    param = next_rel.param
                    result += item
                else:
                    # it seems this path is not representable as a string
                    result = None
                    break
            elif output_format == 'list':
                result.append(next_rel.param)  # type: ignore

            # Prepare processing next level
            level = level.down

        if output_format == 'str':
            if get_parent_too:
                self._path[cache_key] = (parent, param, result)  # type: ignore
                output = (self._format_result(root, parent), param, self._format_result(root, result))  # type: ignore
            else:
                self._path[cache_key] = result
                output = self._format_result(root, result)
        else:
            output = result
        return output

    def create_deeper(self,
                      new_t1,
                      new_t2,
                      child_relationship_class,
                      child_relationship_param=None,
                      child_relationship_param2=None,
                      report_type=None):
        """
        Start a new comparison level and correctly link it to this one.
        :rtype: DiffLevel
        :return: New level
        """
        level = self.all_down
        result = DiffLevel(
            new_t1, new_t2, down=None, up=level, report_type=report_type, verbose_level=self.verbose_level)
        level.down = result
        level.auto_generate_child_rel(
            klass=child_relationship_class, param=child_relationship_param, param2=child_relationship_param2)
        return result

    def branch_deeper(self,
                      new_t1,
                      new_t2,
                      child_relationship_class,
                      child_relationship_param=None,
                      child_relationship_param2=None,
                      report_type=None):
        """
        Branch this comparison: Do not touch this comparison line, but create a new one with exactly the same content,
        just one level deeper.
        :rtype: DiffLevel
        :return: New level in new comparison line
        """
        branch = self.copy()
        return branch.create_deeper(new_t1, new_t2, child_relationship_class,
                                    child_relationship_param, child_relationship_param2, report_type)

    def copy(self):
        """
        Get a deep copy of this comparision line.
        :return: The leaf ("downmost") object of the copy.
        """
        orig = self.all_up
        result = copy(orig)  # copy top level

        while orig is not None:
            result.additional = copy(orig.additional)

            if orig.down is not None:  # copy and create references to the following level
                # copy following level
                result.down = copy(orig.down)

                if orig.t1_child_rel is not None:
                    result.t1_child_rel = ChildRelationship.create(
                        klass=orig.t1_child_rel.__class__,
                        parent=result.t1,
                        child=result.down.t1,
                        param=orig.t1_child_rel.param)
                if orig.t2_child_rel is not None:
                    result.t2_child_rel = ChildRelationship.create(
                        klass=orig.t2_child_rel.__class__,
                        parent=result.t2,
                        child=result.down.t2,
                        param=orig.t2_child_rel.param)

            # descend to next level
            orig = orig.down
            if result.down is not None:
                result = result.down
        return result


class ChildRelationship:
    """
    Describes the relationship between a container object (the "parent") and the contained
    "child" object.
    """

    # Format to a be used for representing param.
    # E.g. for a dict, this turns a formatted param param "42" into "[42]".
    param_repr_format = None

    # This is a hook allowing subclasses to manipulate param strings.
    # :param string: Input string
    # :return: Manipulated string, as appropriate in this context.
    quote_str = None

    @staticmethod
    def create(klass, parent, child, param=None):
        if not issubclass(klass, ChildRelationship):
            raise TypeError
        return klass(parent, child, param)

    def __init__(self, parent, child, param=None):
        # The parent object of this relationship, e.g. a dict
        self.parent = parent

        # The child object of this relationship, e.g. a value in a dict
        self.child = child

        # A subclass-dependent parameter describing how to get from parent to child, e.g. the key in a dict
        self.param = param

    def __repr__(self):
        from deepdiff.summarize import summarize

        name = "<{} parent:{}, child:{}, param:{}>"
        parent = summarize(self.parent, max_length=35)
        child = summarize(self.child, max_length=35)
        param = summarize(self.param, max_length=15)
        return name.format(self.__class__.__name__, parent, child, param)

    def get_param_repr(self, force=None):
        """
        Returns a formatted param python parsable string describing this relationship,
        or None if the relationship is not representable as a string.
        This string can be appended to the parent Name.
        Subclasses representing a relationship that cannot be expressed as a string override this method to return None.
        Examples: "[2]", ".attribute", "['mykey']"
        :param force: Bends the meaning of "no string representation".
              If None:
                Will strictly return partials of Python-parsable expressions. The result those yield will compare
                equal to the objects in question.
              If 'yes':
                Will return a formatted param including '(unrepresentable)' instead of the non string-representable part.

        """
        return self.stringify_param(force)

    def stringify_param(self, force=None):
        """
        Convert param to a string. Return None if there is no string representation.
        This is called by get_param_repr()
        :param force: Bends the meaning of "no string representation".
                      If None:
                        Will strictly return Python-parsable expressions. The result those yield will compare
                        equal to the objects in question.
                      If 'yes':
                        Will return '(unrepresentable)' instead of None if there is no string representation

        TODO: stringify_param has issues with params that when converted to string via repr,
        it is not straight forward to turn them back into the original object.
        Although repr is meant to be able to reconstruct the original object but for complex objects, repr
        often does not recreate the original object.
        Perhaps we should log that the repr reconstruction failed so the user is aware.
        """
        param = self.param
        if isinstance(param, strings):
            result = stringify_element(param, quote_str=self.quote_str)
        elif isinstance(param, tuple):  # Currently only for numpy ndarrays
            result = ']['.join(map(repr, param))
        elif hasattr(param, '__dataclass_fields__'):
            attrs_to_values = [f"{key}={value}" for key, value in [(i, getattr(param, i)) for i in param.__dataclass_fields__]]  # type: ignore
            result = f"{param.__class__.__name__}({','.join(attrs_to_values)})"
        else:
            candidate = repr(param)
            try:
                resurrected = literal_eval_extended(candidate)
                # Note: This will miss string-representable custom objects.
                # However, the only alternative I can currently think of is using eval() which is inherently dangerous.
            except (SyntaxError, ValueError) as err:
                logger.error(
                    f'stringify_param was not able to get a proper repr for "{param}". '
                    "This object will be reported as None. Add instructions for this object to DeepDiff's "
                    f"helper.literal_eval_extended to make it work properly: {err}")
                result = None
            else:
                result = candidate if resurrected == param else None

        if result:
            result = ':' if self.param_repr_format is None else self.param_repr_format.format(result)

        return result


class DictRelationship(ChildRelationship):
    param_repr_format = "[{}]"
    quote_str = "'{}'"


class NumpyArrayRelationship(ChildRelationship):
    param_repr_format = "[{}]"
    quote_str = None


class SubscriptableIterableRelationship(DictRelationship):
    pass


class InaccessibleRelationship(ChildRelationship):
    pass


# there is no random access to set elements
class SetRelationship(InaccessibleRelationship):
    pass


class NonSubscriptableIterableRelationship(InaccessibleRelationship):

    param_repr_format = "[{}]"

    def get_param_repr(self, force=None):
        if force == 'yes':
            result = "(unrepresentable)"
        elif force == 'fake' and self.param:
            result = self.stringify_param()
        else:
            result = None

        return result


class AttributeRelationship(ChildRelationship):
    param_repr_format = ".{}"
