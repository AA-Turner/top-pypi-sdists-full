import os

class JHIDatabricksEnvironment:
  # constructor method runs when object is instantiated. Checks for all variables
  def __init__(self):
    self.env_suffix = self.checkEnvironment('env_suffix')
    self.env_name = self.checkEnvironment('env_name')
    self.env_code = self.checkEnvironment('env_code')
 
  # check/validation method used in constructor
  def checkEnvironment(self, input):
    try:
       return os.getenv(input).strip()
    except:
      raise ValueError("Exception in library jhidatabricksenv -> Environment Variable Key 'env_suffix', 'env_code' & 'env_name' values set as '" + str(os.getenv(input)) + "' on this cluster. Please set a VALID Value for Environment Variable Keys.")
  
  # getter functions
  
  def getSuffix(self):
    if self.env_suffix[:1] == '_' or self.env_suffix == '':
      return self.env_suffix
    else:
      raise ValueError("Exception in library jhidatabricksenv -> Environment Variable 'env_suffix' = '" + str(self.env_suffix) + "' Key Value must be prefixed with an underscore '_" + str(self.env_suffix) +"' or should be an empty string. Please set a VALID Key Value for Environment Variable 'env_suffix'.")
  
  def getName(self):
    return self.env_name
  
  def getCode(self):
      return self.env_code