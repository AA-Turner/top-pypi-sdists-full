import pytest

from novita_sandbox.core import AsyncTemplate


@pytest.mark.skip_debug()
@pytest.mark.asyncio
async def test_async_list_default():
    """Test async list templates with default parameters"""
    templates = await AsyncTemplate.list()

    assert templates is not None
    assert hasattr(templates, "items")
    assert hasattr(templates, "total")
    assert hasattr(templates, "page")
    assert hasattr(templates, "limit")
    assert hasattr(templates, "total_pages")

    assert templates.page == 1
    assert templates.limit == 20
    assert templates.total >= 0
    assert templates.total_pages >= 0

    assert isinstance(templates.items, list)
    assert len(templates) == len(templates.items)


@pytest.mark.skip_debug()
@pytest.mark.asyncio
async def test_async_list_template_build():
    """Test async list template_build templates"""
    templates = await AsyncTemplate.list(template_type="template_build")

    assert templates is not None
    assert templates.page == 1

    for template in templates.items:
        assert hasattr(template, "template_id")
        assert hasattr(template, "aliases")
        assert hasattr(template, "envd_version")


@pytest.mark.skip_debug()
@pytest.mark.asyncio
async def test_async_list_snapshot_template():
    """Test async list snapshot_template templates"""
    templates = await AsyncTemplate.list(template_type="snapshot_template")

    assert templates is not None
    assert templates.page == 1

    for template in templates.items:
        assert hasattr(template, "template_id")
        assert hasattr(template, "build_id")
        assert hasattr(template, "cpu_count")
        assert hasattr(template, "memory_mb")
        assert hasattr(template, "disk_size_mb")


@pytest.mark.skip_debug()
@pytest.mark.asyncio
async def test_async_list_with_pagination():
    """Test async list templates with custom pagination"""
    templates = await AsyncTemplate.list(page=1, limit=5)

    assert templates is not None
    assert templates.page == 1
    assert templates.limit == 5
    assert len(templates.items) <= 5


@pytest.mark.skip_debug()
@pytest.mark.asyncio
async def test_async_list_iteration():
    """Test iterating over async template list"""
    templates = await AsyncTemplate.list(limit=10)

    count = 0
    for template in templates:
        count += 1
        assert hasattr(template, "template_id")

    assert count == len(templates.items)


@pytest.mark.skip_debug()
@pytest.mark.asyncio
async def test_async_list_indexing():
    """Test indexing async template list"""
    templates = await AsyncTemplate.list(limit=10)

    if len(templates) > 0:
        first_template = templates[0]
        assert hasattr(first_template, "template_id")

        last_template = templates[-1]
        assert hasattr(last_template, "template_id")


@pytest.mark.skip_debug()
@pytest.mark.asyncio
async def test_async_template_info_properties():
    """Test TemplateInfo properties in async context"""
    templates = await AsyncTemplate.list(limit=1)

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


@pytest.mark.asyncio
async def test_async_list_invalid_limit():
    """Test async list with invalid limit"""
    with pytest.raises(ValueError, match="limit must be between 1 and 100"):
        await AsyncTemplate.list(limit=0)

    with pytest.raises(ValueError, match="limit must be between 1 and 100"):
        await AsyncTemplate.list(limit=101)


@pytest.mark.asyncio
async def test_async_list_invalid_page():
    """Test async list with invalid page"""
    with pytest.raises(ValueError, match="page must be >= 1"):
        await AsyncTemplate.list(page=0)


@pytest.mark.asyncio
async def test_async_list_invalid_template_type():
    """Test async list with invalid template_type"""
    with pytest.raises(ValueError, match="template_type must be"):
        await AsyncTemplate.list(template_type="invalid_type")


@pytest.mark.skip_debug()
@pytest.mark.asyncio
async def test_async_template_list_repr():
    """Test TemplateList string representation in async context"""
    templates = await AsyncTemplate.list(limit=5)

    repr_str = repr(templates)
    assert "TemplateList" in repr_str
    assert "total=" in repr_str
    assert "page=" in repr_str


@pytest.mark.skip_debug()
@pytest.mark.asyncio
async def test_async_template_info_repr():
    """Test TemplateInfo string representation in async context"""
    templates = await AsyncTemplate.list(limit=1)

    if len(templates) > 0:
        template = templates[0]
        repr_str = repr(template)
        assert "TemplateInfo" in repr_str
        assert "template_id=" in repr_str
