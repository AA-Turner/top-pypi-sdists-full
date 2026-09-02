# import pytest
# 
# from novita_sandbox.core import Sandbox
# 
# 
# @pytest.mark.skip_debug()
# def test_commit_instance_method(template):
#     """Test commit using instance method"""
#     sbx = Sandbox.create(template, timeout=300)
#     try:
#         result_template = sbx.commit()
#         print(result_template)
# 
#         assert result_template is not None
#         assert hasattr(result_template, "template_id")
#         assert result_template.template_id is not None
# 
#     finally:
#         sbx.kill()
# 
# 
# @pytest.mark.skip_debug()
# def test_commit_static_method(template):
#     """Test commit using static method"""
#     sbx = Sandbox.create(template, timeout=300)
#     try:
#         result_template = Sandbox.commit(sbx.sandbox_id, alias="test-commit-static")
# 
#         assert result_template is not None
#         assert hasattr(result_template, "template_id")
#         assert result_template.template_id is not None
# 
#     finally:
#         sbx.kill()
# 
# 
# @pytest.mark.skip_debug()
# def test_commit_without_alias(template):
#     """Test commit without providing an alias"""
#     sbx = Sandbox.create(template, timeout=300)
#     try:
#         result_template = sbx.commit()
# 
#         assert result_template is not None
#         assert hasattr(result_template, "template_id")
#         assert result_template.template_id is not None
# 
#     finally:
#         sbx.kill()
# 
# 
# @pytest.mark.skip_debug()
# def test_commit_nonexistent_sandbox():
#     """Test commit with a non-existent sandbox ID"""
#     from novita_sandbox.core.exceptions import NotFoundException
# 
#     with pytest.raises(NotFoundException):
#         Sandbox.commit("nonexistent-sandbox-id")
