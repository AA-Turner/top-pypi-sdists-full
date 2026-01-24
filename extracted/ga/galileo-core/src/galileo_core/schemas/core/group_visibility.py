from enum import Enum


class GroupVisibility(str, Enum):
    public = "public"
    private = "private"
    hidden = "hidden"
    protected = "protected"
