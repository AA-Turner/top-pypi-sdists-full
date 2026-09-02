import pytest

from novita_sandbox.core import Template


@pytest.mark.skip_debug()
def test_list_default():
    """Test list templates with default parameters"""
    templates = Template.list(template_type="snapshot_template")
    print(templates)
    for template in templates.items:
        print(template.to_dict())


@pytest.mark.skip_debug()
def test_list_template_build():
    """Test list template_build templates"""
    templates = Template.list(template_type="template_build")

    assert templates is not None
    assert templates.page == 1

    for template in templates.items:
        assert hasattr(template, "template_id")
        assert hasattr(template, "aliases")
        assert hasattr(template, "envd_version")


@pytest.mark.skip_debug()
def test_list_snapshot_template():
    """Test list snapshot_template templates"""
    templates = Template.list(template_type="snapshot_template")
    print("\n")
    for template in templates.items:
        print(template)

    assert templates is not None
    assert templates.page == 1

    for template in templates.items:
        assert hasattr(template, "template_id")
        assert hasattr(template, "build_id")
        assert hasattr(template, "cpu_count")
        assert hasattr(template, "memory_mb")
        assert hasattr(template, "disk_size_mb")


@pytest.mark.skip_debug()
def test_list_with_pagination():
    """Test list templates with custom pagination"""
    templates = Template.list(page=1, limit=10, template_type="snapshot_template")
    print("\n")
    print(templates.total_pages, templates.total, templates.limit, templates.page)
    for template in templates.items:
        print(template)


@pytest.mark.skip_debug()
def test_list_iteration():
    """Test iterating over template list"""
    templates = Template.list(limit=10)

    count = 0
    for template in templates:
        count += 1
        assert hasattr(template, "template_id")

    assert count == len(templates.items)


@pytest.mark.skip_debug()
def test_list_indexing():
    """Test indexing template list"""
    templates = Template.list(limit=10)

    if len(templates) > 0:
        first_template = templates[0]
        assert hasattr(first_template, "template_id")

        last_template = templates[-1]
        assert hasattr(last_template, "template_id")


@pytest.mark.skip_debug()
def test_template_info_properties():
    """Test TemplateInfo properties"""
    templates = Template.list(limit=1)

    if len(templates) > 0:
        template = templates[0]

        assert isinstance(template.template_id, str)
        assert isinstance(template.build_id, str)
        assert isinstance(template.cpu_count, int)
        assert isinstance(template.memory_mb, int)
        assert isinstance(template.disk_size_mb, int)
        assert isinstance(template.envd_version, str)
        assert isinstance(template.public, bool)
        assert isinstance(template.aliases, list)
        assert isinstance(template.spawn_count, int)
        assert isinstance(template.build_count, int)


def test_list_invalid_limit():
    """Test list with invalid limit"""
    with pytest.raises(ValueError, match="limit must be between 1 and 100"):
        Template.list(limit=0)

    with pytest.raises(ValueError, match="limit must be between 1 and 100"):
        Template.list(limit=101)


def test_list_invalid_page():
    """Test list with invalid page"""
    with pytest.raises(ValueError, match="page must be >= 1"):
        Template.list(page=0)


def test_list_invalid_template_type():
    """Test list with invalid template_type"""
    with pytest.raises(ValueError, match="template_type must be"):
        Template.list(template_type="invalid_type")


@pytest.mark.skip_debug()
def test_template_list_repr():
    """Test TemplateList string representation"""
    templates = Template.list(limit=5)

    repr_str = repr(templates)
    assert "TemplateList" in repr_str
    assert "total=" in repr_str
    assert "page=" in repr_str


@pytest.mark.skip_debug()
def test_template_info_repr():
    """Test TemplateInfo string representation"""
    templates = Template.list(limit=1)

    if len(templates) > 0:
        template = templates[0]
        repr_str = repr(template)
        assert "TemplateInfo" in repr_str
        assert "template_id=" in repr_str
