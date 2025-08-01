# import pytest
#
#
# class TestSomeModuleTestCase:
#
#     @pytest.fixture(autouse=True)
#     def context(self):
#         print("SETUP")
#         try:
#             yield
#         finally:
#             print("TEARDOWN")
#
#     def test_one(self):
#         print("    one")
#         assert True
#         print("    one after")
#
#     @pytest.mark.skip()
#     def test_two(self):
#         print("    two")
#         assert False
#         print("    two after")
