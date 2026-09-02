# import pytest
# 
# from novita_sandbox.core import AsyncSandbox
# 
# 
# @pytest.mark.skip_debug()
# @pytest.mark.asyncio
# async def test_async_commit_instance_method(template):
#     """Test async commit using instance method"""
#     sbx = await AsyncSandbox.create(template, timeout=300)
#     try:
#         result_template = await sbx.commit(alias="test-async-commit-alias")
# 
#         assert result_template is not None
#         assert hasattr(result_template, "template_id")
#         assert hasattr(result_template, "aliases")
# 
#         if result_template.aliases:
#             assert "test-async-commit-alias" in result_template.aliases
# 
#     finally:
#         await sbx.kill()
# 
# 
# @pytest.mark.skip_debug()
# @pytest.mark.asyncio
# async def test_async_commit_static_method(template):
#     """Test async commit using static method"""
#     sbx = await AsyncSandbox.create(template, timeout=300)
#     try:
#         result_template = await AsyncSandbox.commit(sbx.sandbox_id, alias="test-async-commit-static")
# 
#         assert result_template is not None
#         assert hasattr(result_template, "template_id")
#         assert result_template.template_id is not None
# 
#     finally:
#         await sbx.kill()
# 
# 
# @pytest.mark.skip_debug()
# @pytest.mark.asyncio
# async def test_async_commit_without_alias(template):
#     """Test async commit without providing an alias"""
#     sbx = await AsyncSandbox.create(template, timeout=300)
#     try:
#         result_template = await sbx.commit()
# 
#         assert result_template is not None
#         assert hasattr(result_template, "template_id")
#         assert result_template.template_id is not None
# 
#     finally:
#         await sbx.kill()
# 
# 
# @pytest.mark.skip_debug()
# @pytest.mark.asyncio
# async def test_async_commit_nonexistent_sandbox():
#     """Test async commit with a non-existent sandbox ID"""
#     from novita_sandbox.core.exceptions import NotFoundException
# 
#     with pytest.raises(NotFoundException):
#         await AsyncSandbox.commit("nonexistent-sandbox-id")
