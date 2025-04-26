import json

import pytest

from tests.helpers import environ
from tinybird_cdk.cloud import gcp


class TestGCP:
  def setup_method(self):
    self.saved_environ = environ.save()
    environ.unset('GOOGLE_APPLICATION_CREDENTIALS')
    environ.unset('GOOGLE_APPLICATION_CREDENTIALS_JSON')
    environ.unset('GCP_PROJECT')

  def teardown_method(self):
    environ.restore(self.saved_environ)

  def json_credentials(self):
    with open(environ.get('TB_CDK_TEST_SUITE_GOOGLE_APPLICATION_CREDENTIALS')) as file:
      return file.read()

  def project_id(self):
    return json.loads(self.json_credentials())['project_id']

  def test_credentials_supports_GOOGLE_APPLICATION_CREDENTIALS(self):
    environ.copy('TB_CDK_TEST_SUITE_GOOGLE_APPLICATION_CREDENTIALS', 'GOOGLE_APPLICATION_CREDENTIALS')
    assert gcp.credentials().project_id == self.project_id()

  def test_credentials_supports_GOOGLE_APPLICATION_CREDENTIALS_JSON(self):
    environ.set('GOOGLE_APPLICATION_CREDENTIALS_JSON', self.json_credentials())
    assert gcp.credentials().project_id == self.project_id()

  def test_credentials_GOOGLE_APPLICATION_CREDENTIALS_JSON_has_higher_precedence(self):
    environ.set('GOOGLE_APPLICATION_CREDENTIALS_JSON', self.json_credentials())
    environ.set('GOOGLE_APPLICATION_CREDENTIALS', '/does/not/even/exist.json')
    assert gcp.credentials().project_id == self.project_id()

  def test_project_id_supports_GCP_PROJECT(self):
    environ.set('GCP_PROJECT', 'X' + self.project_id())
    assert gcp.project_id() == 'X' + self.project_id()

  def test_project_id_falls_back_to_the_credentials_attribute(self):
    environ.copy('TB_CDK_TEST_SUITE_GOOGLE_APPLICATION_CREDENTIALS', 'GOOGLE_APPLICATION_CREDENTIALS')
    assert gcp.project_id() == self.project_id()

  def test_raises_if_none_of_the_environment_variables_are_set(self):
    with pytest.raises(Exception) as error:
      gcp.credentials()
    assert 'GOOGLE_APPLICATION_CREDENTIALS' in str(error.value)
