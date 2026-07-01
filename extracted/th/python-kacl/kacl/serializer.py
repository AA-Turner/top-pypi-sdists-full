import yaml

from kacl.changes import KACLChanges
from kacl.document import KACLDocument
from kacl.element import KACLElement
from kacl.version import KACLVersion


class KACLMarkdownSerializer:
    def __init__(self):
        pass

    def serialize(self, document):
        data = []
        link_references = []
        if isinstance(document, KACLDocument):
            serialized_metadata = self.__serialize_metadata(document.metadata())
            if serialized_metadata:
                data.extend(serialized_metadata)

            data.append(self.__serialize_header(document.header()))
            # check if the body starts with a newline. if not add one
            if document.header().body().startswith("\n"):
                data.append(document.header().body())
            else:
                data.append("\n" + document.header().body())

            for version in document.versions():
                data.extend([self.__serialize_version(version), ""])
                if version.has_link_reference():
                    link_references.append(self.__serialize_link_reference(version))

        elif isinstance(document, KACLVersion):
            data.extend([self.__serialize_version(document), ""])

            if document.has_link_reference():
                link_references.append(self.__serialize_link_reference(document))

        elif isinstance(document, dict):
            # Validate that the dict contains KACLChanges objects (from version.sections())
            if document and all(isinstance(v, KACLChanges) for v in document.values()):
                data.extend([self.__serialize_sections(document), ""])
            else:
                raise TypeError(
                    "Dict input must contain KACLChanges objects (from version.sections())"
                )

        data.extend(link_references)

        if data[-1] != "":
            data.append("")

        return "\n".join(data)

    def __serialize_metadata(self, metadata):
        if not metadata:
            return None

        metadata_lines = ["---"]
        metadata_lines.extend(yaml.dump(metadata).rstrip().split("\n"))

        metadata_lines.append("---")

        return metadata_lines

    def __serialize_header(self, obj):
        if isinstance(obj, KACLChanges):
            return f"### {obj.title()}"
        elif isinstance(obj, KACLVersion):
            version_decorator_left = ""
            version_decorator_right = ""
            if obj.has_link_reference():
                version_decorator_left = "["
                version_decorator_right = "]"
            if obj.date():
                return f"## {version_decorator_left}{obj.version()}{version_decorator_right} - {obj.date()}"
            else:
                return f"## {version_decorator_left}{obj.version()}{version_decorator_right}"
        elif isinstance(obj, KACLElement):
            return f"# {obj.title()}"

    def __serialize_version(self, obj):
        lines = [self.__serialize_header(obj), ""]
        lines.append(self.__serialize_sections(obj.sections()))
        return "\n".join(lines).strip()

    def __serialize_sections(self, sections_dict):
        """Serialize a dictionary of section title -> KACLChanges.

        Used by both __serialize_version (for full version with header)
        and for standalone sections (for --no-header output).
        """
        lines = []
        for title, changes in sections_dict.items():
            lines.extend(
                [
                    self.__serialize_header(changes),
                    "",
                    self.__serialize_list(changes.items()),
                    "",
                ]
            )
        return "\n".join(lines).strip()

    def __serialize_list(self, obj):
        lines = [f"- {x}" for x in obj]
        return "\n".join(lines)

    def __serialize_link_reference(self, obj):
        return f"[{obj.version()}]: {obj.link()}"
