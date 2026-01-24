# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later

"""
This is an internal PyTango module.
"""


__all__ = ("AttrData",)

__docformat__ = "restructuredtext"

import inspect

from tango._tango import Except, CmdArgType, AttrDataFormat, AttrWriteType
from tango._tango import DispLevel, UserDefaultAttrProp, UserDefaultFwdAttrProp
from tango._tango import Attr, SpectrumAttr, ImageAttr, FwdAttr
from tango.utils import is_non_str_seq, is_pure_str


class AttrData:
    """A helper class that contains the same information one of the items in
    DeviceClass.attr_list but in object form"""

    def __init__(self, name, class_name, attr_info=None):
        self.class_name = class_name
        self.attr_name = name
        self.attr_type = CmdArgType.DevVoid
        self.attr_format = AttrDataFormat.SCALAR
        self.attr_write = AttrWriteType.READ
        self.dim_x = 1
        self.dim_y = 0
        self.display_level = DispLevel.OPERATOR
        self.polling_period = -1
        self.memorized = False
        self.hw_memorized = False
        self.alarm_event_implemented = False
        self.alarm_event_detect = True
        self.archive_event_implemented = False
        self.archive_event_detect = True
        self.change_event_implemented = False
        self.change_event_detect = True
        self.data_ready_event_implemented = False
        if name is None:
            self.read_method_name = None
            self.write_method_name = None
            self.is_allowed_name = None
        else:
            self.read_method_name = "read_" + name
            self.write_method_name = "write_" + name
            self.is_allowed_name = "is_" + name + "_allowed"
        self.attr_class = None
        self.attr_args = None
        self.att_prop = None
        self.forward = False
        self.has_dtype_kword = False
        self.has_size_kword = False
        if attr_info is not None:
            self.from_attr_info(attr_info)

    @classmethod
    def from_dict(cls, attr_dict):
        attr_dict = dict(attr_dict)
        name = attr_dict.pop("name", None)
        class_name = attr_dict.pop("class_name", None)
        self = cls(name, class_name)
        self.build_from_dict(attr_dict)
        return self

    def build_from_dict(self, attr_dict):
        self.forward = attr_dict.pop("forwarded", False)
        if not self.forward:
            self.has_dtype_kword = "dtype" in attr_dict
            self.attr_type = attr_dict.pop("dtype", CmdArgType.DevDouble)
            self.attr_format = attr_dict.pop("dformat", AttrDataFormat.SCALAR)
            self.has_size_kword = "max_dim_x" in attr_dict or "max_dim_y" in attr_dict
            self.dim_x = attr_dict.pop("max_dim_x", 1)
            self.dim_y = attr_dict.pop("max_dim_y", 0)
            self.display_level = attr_dict.pop("display_level", DispLevel.OPERATOR)
            self.polling_period = attr_dict.pop("polling_period", -1)
            self.memorized = attr_dict.pop("memorized", False)
            self.hw_memorized = attr_dict.pop("hw_memorized", False)

            is_access_explicit = "access" in attr_dict
            if is_access_explicit:
                self.attr_write = attr_dict.pop("access")
            else:
                # access is defined by which methods were defined
                r_explicit = "fread" in attr_dict or "fget" in attr_dict
                w_explicit = "fwrite" in attr_dict or "fset" in attr_dict
                if r_explicit and w_explicit:
                    self.attr_write = AttrWriteType.READ_WRITE
                elif r_explicit:
                    self.attr_write = AttrWriteType.READ
                elif w_explicit:
                    self.attr_write = AttrWriteType.WRITE
                else:
                    self.attr_write = AttrWriteType.READ

            fread = attr_dict.pop("fget", attr_dict.pop("fread", None))
            if fread is not None:
                if is_pure_str(fread):
                    self.read_method_name = fread
                elif inspect.isroutine(fread):
                    self.read_method_name = fread.__name__
            fwrite = attr_dict.pop("fset", attr_dict.pop("fwrite", None))
            if fwrite is not None:
                if is_pure_str(fwrite):
                    self.write_method_name = fwrite
                elif inspect.isroutine(fwrite):
                    self.write_method_name = fwrite.__name__
            fisallowed = attr_dict.pop("fisallowed", None)
            if fisallowed is not None:
                if is_pure_str(fisallowed):
                    self.is_allowed_name = fisallowed
                elif inspect.isroutine(fisallowed):
                    self.is_allowed_name = fisallowed.__name__
            self.attr_class = attr_dict.pop("klass", None)
        else:
            self.attr_class = FwdAttr
            self.attr_args = [self.attr_name]

        self.alarm_event_implemented = attr_dict.pop("alarm_event_implemented", False)
        self.alarm_event_detect = attr_dict.pop("alarm_event_detect", True)
        self.archive_event_implemented = attr_dict.pop(
            "archive_event_implemented", False
        )
        self.archive_event_detect = attr_dict.pop("archive_event_detect", True)
        self.change_event_implemented = attr_dict.pop("change_event_implemented", False)
        self.change_event_detect = attr_dict.pop("change_event_detect", True)
        self.data_ready_event_implemented = attr_dict.pop(
            "data_ready_event_implemented", False
        )

        if self.forward:
            self.att_prop = self.__create_user_default_fwdattr_prop(attr_dict)
        elif len(attr_dict):
            self.att_prop = self.__create_user_default_attr_prop(attr_dict)
        return self

    def _set_name(self, name):
        old_name = self.attr_name
        self.attr_name = name
        if self.attr_args is None:
            self.attr_args = [name]
        else:
            self.attr_args[0] = name
        if old_name is None:
            if self.read_method_name is None:
                self.read_method_name = "read_" + name
            if self.write_method_name is None:
                self.write_method_name = "write_" + name
            if self.is_allowed_name is None:
                self.is_allowed_name = "is_" + name + "_allowed"

    def __throw_exception(self, msg, meth="create_attribute()"):
        Except.throw_exception("PyDs_WrongAttributeDefinition", msg, meth)

    def __create_user_default_fwdattr_prop(self, extra_info):
        """for internal usage only"""
        p = UserDefaultFwdAttrProp()
        if "label" in extra_info:
            p.set_label(extra_info["label"])
        return p

    def __create_user_default_attr_prop(self, extra_info):
        """for internal usage only"""
        p = UserDefaultAttrProp()

        doc = extra_info.pop("doc", None)
        if doc is not None:
            extra_info["description"] = doc

        for k, v in extra_info.items():
            k_lower = k.lower()
            method_name = f"set_{k_lower.replace(' ', '_')}"
            if hasattr(p, method_name):
                method = getattr(p, method_name)
                if method_name == "set_enum_labels":
                    method(v)
                else:
                    method(str(v))
            elif k == "delta_time":
                p.set_delta_t(str(v))
            elif k_lower not in ("display level", "polling period", "memorized"):
                msg = (
                    f"Wrong definition of attribute. "
                    f"The object extra information '{k}' "
                    f"is not recognized!"
                )
                Except.throw_exception(
                    "PyDs_WrongAttributeDefinition",
                    msg,
                    "create_user_default_attr_prop()",
                )
        return p

    def from_attr_info(self, attr_info):
        self.has_dtype_kword = True
        self.has_size_kword = True

        name = self.class_name
        attr_name = self.attr_name
        throw_ex = self.__throw_exception
        # check for well defined attribute info

        # check parameter
        if not is_non_str_seq(attr_info):
            throw_ex(
                f"Wrong data type for value for describing attribute {attr_name} in "
                f"class {name}\nMust be a sequence with 1 or 2 elements"
            )

        if len(attr_info) < 1 or len(attr_info) > 2:
            throw_ex(
                f"Wrong number of argument for describing attribute {attr_name} in "
                f"class {name}\nMust be a sequence with 1 or 2 elements"
            )

        extra_info = {}
        if len(attr_info) == 2:
            # attr_info[1] must be a dictionary
            # extra_info = attr_info[1], with all the keys lowercase
            for k, v in attr_info[1].items():
                extra_info[k.lower()] = v

        attr_info = attr_info[0]

        attr_info_len = len(attr_info)
        # check parameter
        if not is_non_str_seq(attr_info) or attr_info_len < 3 or attr_info_len > 5:
            throw_ex(
                f"Wrong data type for describing mandatory information for "
                f"attribute {attr_name} in class {name}\nMust be a sequence with 3, 4 "
                f"or 5 elements"
            )

        # get data type
        try:
            self.attr_type = CmdArgType(attr_info[0])
        except Exception:
            throw_ex(
                f"Wrong data type in attribute argument for attribute {attr_name} "
                f"in class {name}\nAttribute data type (first element in first "
                f"sequence) must be a tango.CmdArgType"
            )

        # get format
        try:
            self.attr_format = AttrDataFormat(attr_info[1])
        except Exception:
            throw_ex(
                f"Wrong data format in attribute argument for attribute {attr_name} "
                f"in class {name}\nAttribute data format (second element in "
                f"first sequence) must be a tango.AttrDataFormat"
            )

        if self.attr_format == AttrDataFormat.SCALAR:
            if attr_info_len != 3:
                throw_ex(
                    f"Wrong data type in attribute argument for attribute "
                    f"{attr_name} in class {name}\nSequence describing mandatory "
                    f"attribute parameters for scalar attribute must have "
                    f"3 elements"
                )
        elif self.attr_format == AttrDataFormat.SPECTRUM:
            if attr_info_len != 4:
                throw_ex(
                    f"Wrong data type in attribute argument for attribute "
                    f"{attr_name} in class {name}\nSequence describing mandatory "
                    f"attribute parameters for spectrum attribute must "
                    f"have 4 elements"
                )
            try:
                self.dim_x = int(attr_info[3])
            except Exception:
                throw_ex(
                    f"Wrong data type in attribute argument for attribute "
                    f"{attr_name} in class {name}\n4th element in sequence describing "
                    f"mandatory dim_x attribute parameter for spectrum "
                    f"attribute must be an integer"
                )
        elif self.attr_format == AttrDataFormat.IMAGE:
            if attr_info_len != 5:
                throw_ex(
                    f"Wrong data type in attribute argument for attribute "
                    f"{attr_name} in class {name}\nSequence describing mandatory "
                    f"attribute parameters for image attribute must have "
                    f"5 elements"
                )
            try:
                self.dim_x = int(attr_info[3])
            except Exception:
                throw_ex(
                    f"Wrong data type in attribute argument for attribute "
                    f"{attr_name} in class {name}\n4th element in sequence describing "
                    f"mandatory dim_x attribute parameter for image "
                    f"attribute must be an integer"
                )
            try:
                self.dim_y = int(attr_info[4])
            except Exception:
                throw_ex(
                    f"Wrong data type in attribute argument for attribute "
                    f"{attr_name} in class {name}\n5th element in sequence desribing "
                    f"mandatory dim_y attribute parameter for image "
                    f"attribute must be an integer"
                )
        else:
            assert False, "Unsupported AttrDataFormat {attr_format}."

        # get write type
        try:
            self.attr_write = AttrWriteType(attr_info[2])
        except Exception:
            throw_ex(
                f"Wrong data write type in attribute argument for "
                f"attribute {attr_name} in class {name}\nAttribute write type (third "
                f"element in first sequence) must be a "
                f"tango.AttrWriteType"
            )
        try:
            self.display_level = DispLevel(
                extra_info.get("display level", DispLevel.OPERATOR)
            )
        except Exception:
            throw_ex(
                f"Wrong display level in attribute information for "
                f"attribute {attr_name} in class {name}\nAttribute information for "
                f"display level is not a tango.DispLevel"
            )
        try:
            self.polling_period = int(extra_info.get("polling period", -1))
        except Exception:
            throw_ex(
                f"Wrong polling period in attribute information for "
                f"attribute {attr_name} in class {name}\nAttribute information for "
                f"polling period is not an integer"
            )

        memorized = extra_info.get("memorized", "false").lower()

        if memorized not in ("true", "true_without_hard_applied", "false"):
            throw_ex(
                f"Wrong memorized value for attribute {attr_name} in class {name}."
                f'Allowed valued are the strings "true", "false" and '
                f'"true_without_hard_applied" (case insensitive)'
            )

        if memorized == "true":
            self.memorized = True
            self.hw_memorized = True
        elif memorized == "true_without_hard_applied":
            self.memorized = True
        else:
            self.memorized = False

        self.alarm_event_implemented = extra_info.get("alarm_event_implemented", False)
        self.alarm_event_detect = extra_info.get("alarm_event_detect", True)
        self.archive_event_implemented = extra_info.get(
            "archive_event_implemented", False
        )
        self.archive_event_detect = extra_info.get("archive_event_detect", True)
        self.change_event_implemented = extra_info.get(
            "change_event_implemented", False
        )
        self.change_event_detect = extra_info.get("change_event_detect", True)
        self.data_ready_event_implemented = extra_info.get(
            "data_ready_event_implemented", False
        )

        if self.attr_type == CmdArgType.DevEnum:
            if "enum_labels" not in extra_info:
                throw_ex(
                    f"Missing 'enum_labels' key in attr_list definition "
                    f"for enum attribute {attr_name} in class {name}"
                )
            self.enum_labels = extra_info["enum_labels"]

        self.attr_class = extra_info.get("klass", None)

        att_prop = None
        if extra_info:
            att_prop = self.__create_user_default_attr_prop(extra_info)
        self.att_prop = att_prop

    def set_enum_labels_to_attr_prop(self, enum_labels):
        if self.att_prop:
            self.att_prop.set_enum_labels(enum_labels)
        else:
            self.att_prop = self.__create_user_default_attr_prop(
                {"enum_labels": enum_labels}
            )

    def to_attr(self):
        if self.attr_args is None:
            attr_args = [self.attr_name, self.attr_type, self.attr_write]
            if not self.attr_format == AttrDataFormat.SCALAR:
                attr_args.append(self.dim_x)
                if not self.attr_format == AttrDataFormat.SPECTRUM:
                    attr_args.append(self.dim_y)
        else:
            attr_args = self.attr_args

        if self.attr_class is None:
            klass = self.DftAttrClassMap[self.attr_format]
        else:
            klass = self.attr_class

        attr = klass(*attr_args)
        if self.att_prop is not None:
            attr.set_default_properties(self.att_prop)
        attr.set_disp_level(self.display_level)
        if self.memorized:
            attr.set_memorized()
            attr.set_memorized_init(self.hw_memorized)
        if self.polling_period > 0:
            attr.set_polling_period(self.polling_period)
        return attr

    DftAttrClassMap = {
        AttrDataFormat.SCALAR: Attr,
        AttrDataFormat.SPECTRUM: SpectrumAttr,
        AttrDataFormat.IMAGE: ImageAttr,
    }
