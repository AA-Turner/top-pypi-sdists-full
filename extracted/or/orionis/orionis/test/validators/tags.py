from orionis.test.exceptions import OrionisTestValueError

class __ValidTags:

    def __call__(self, tags):
        """
        Validator that ensures the `tags` parameter is a non-empty list of non-empty strings.

        Parameters
        ----------
        tags : Any
            The value to be validated as a list of non-empty strings.

        Returns
        -------
        list
            The validated and stripped list of tags.

        Raises
        ------
        OrionisTestValueError
            If `tags` is not a non-empty list of non-empty strings.
        """

        if tags is not None:

            if (not isinstance(tags, list) or not tags or not all(isinstance(tag, str) and tag.strip() for tag in tags)):
                raise OrionisTestValueError(
                    f"Invalid tags: Expected a non-empty list of non-empty strings, got '{tags}' ({type(tags).__name__})."
                )

            return [str(tag).strip() for tag in tags]

        return None

# Exported singleton instance
ValidTags = __ValidTags()
