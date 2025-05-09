#
# @file    TestKineticLaw.py
# @brief   SBML KineticLaw unit tests
#
# @author  Akiya Jouraku (Python conversion)
# @author  Ben Bornstein 
# 
# ====== WARNING ===== WARNING ===== WARNING ===== WARNING ===== WARNING ======
#
# DO NOT EDIT THIS FILE.
#
# This file was generated automatically by converting the file located at
# src/sbml/test/TestKineticLaw.c
# using the conversion program dev/utilities/translateTests/translateTests.pl.
# Any changes made here will be lost the next time the file is regenerated.
#
# -----------------------------------------------------------------------------
# This file is part of libSBML.  Please visit http://sbml.org for more
# information about SBML, and the latest version of libSBML.
#
# Copyright 2005-2010 California Institute of Technology.
# Copyright 2002-2005 California Institute of Technology and
#                     Japan Science and Technology Corporation.
# 
# This library is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation.  A copy of the license agreement is provided
# in the file named "LICENSE.txt" included with this software distribution
# and also available online as http://sbml.org/software/libsbml/license.html
# -----------------------------------------------------------------------------

import sys
import unittest
import libsbml


class TestKineticLaw(unittest.TestCase):

  global kl
  kl = None

  def setUp(self):
    self.kl = libsbml.KineticLaw(2,4)
    if (self.kl == None):
      pass    
    pass  

  def tearDown(self):
    _dummyList = [ self.kl ]; _dummyList[:] = []; del _dummyList
    pass  

  def test_KineticLaw_addParameter(self):
    p = libsbml.Parameter(2,4)
    p.setId( "p")
    self.kl.addParameter(p)
    self.assertTrue( self.kl.getNumParameters() == 1 )
    _dummyList = [ p ]; _dummyList[:] = []; del _dummyList
    pass  

  def test_KineticLaw_create(self):
    self.assertTrue( self.kl.getTypeCode() == libsbml.SBML_KINETIC_LAW )
    self.assertTrue( self.kl.getMetaId() == "" )
    self.assertTrue( self.kl.getNotes() == None )
    self.assertTrue( self.kl.getAnnotation() == None )
    self.assertTrue( self.kl.getFormula() == "" )
    self.assertTrue( self.kl.getMath() == None )
    self.assertTrue( self.kl.getTimeUnits() == "" )
    self.assertTrue( self.kl.getSubstanceUnits() == "" )
    self.assertEqual( False, self.kl.isSetFormula() )
    self.assertEqual( False, self.kl.isSetMath() )
    self.assertEqual( False, self.kl.isSetTimeUnits() )
    self.assertEqual( False, self.kl.isSetSubstanceUnits() )
    self.assertTrue( self.kl.getNumParameters() == 0 )
    pass  

  def test_KineticLaw_createWithNS(self):
    xmlns = libsbml.XMLNamespaces()
    xmlns.add( "http://www.sbml.org", "testsbml")
    sbmlns = libsbml.SBMLNamespaces(2,1)
    sbmlns.addNamespaces(xmlns)
    object = libsbml.KineticLaw(sbmlns)
    self.assertTrue( object.getTypeCode() == libsbml.SBML_KINETIC_LAW )
    self.assertTrue( object.getMetaId() == "" )
    self.assertTrue( object.getNotes() == None )
    self.assertTrue( object.getAnnotation() == None )
    self.assertTrue( object.getLevel() == 2 )
    self.assertTrue( object.getVersion() == 1 )
    self.assertTrue( object.getNamespaces() != None )
    self.assertTrue( object.getNamespaces().getLength() == 2 )
    _dummyList = [ object ]; _dummyList[:] = []; del _dummyList
    pass  

  def test_KineticLaw_free_NULL(self):
    _dummyList = [ None ]; _dummyList[:] = []; del _dummyList
    pass  

  def test_KineticLaw_getParameter(self):
    k1 = libsbml.Parameter(2,4)
    k2 = libsbml.Parameter(2,4)
    k1.setId( "k1")
    k2.setId( "k2")
    k1.setValue(3.14)
    k2.setValue(2.72)
    self.kl.addParameter(k1)
    self.kl.addParameter(k2)
    _dummyList = [ k1 ]; _dummyList[:] = []; del _dummyList
    _dummyList = [ k2 ]; _dummyList[:] = []; del _dummyList
    self.assertTrue( self.kl.getNumParameters() == 2 )
    k1 = self.kl.getParameter(0)
    k2 = self.kl.getParameter(1)
    self.assertTrue((  "k1" == k1.getId() ))
    self.assertTrue((  "k2" == k2.getId() ))
    self.assertTrue( k1.getValue() == 3.14 )
    self.assertTrue( k2.getValue() == 2.72 )
    pass  

  def test_KineticLaw_getParameterById(self):
    k1 = libsbml.Parameter(2,4)
    k2 = libsbml.Parameter(2,4)
    k1.setId( "k1")
    k2.setId( "k2")
    k1.setValue(3.14)
    k2.setValue(2.72)
    self.kl.addParameter(k1)
    self.kl.addParameter(k2)
    _dummyList = [ k1 ]; _dummyList[:] = []; del _dummyList
    _dummyList = [ k2 ]; _dummyList[:] = []; del _dummyList
    self.assertTrue( self.kl.getNumParameters() == 2 )
    k1 = self.kl.getParameter( "k1")
    k2 = self.kl.getParameter( "k2")
    self.assertTrue((  "k1" == k1.getId() ))
    self.assertTrue((  "k2" == k2.getId() ))
    self.assertTrue( k1.getValue() == 3.14 )
    self.assertTrue( k2.getValue() == 2.72 )
    pass  

  def test_KineticLaw_removeParameter(self):
    o1 = self.kl.createParameter()
    o2 = self.kl.createParameter()
    o3 = self.kl.createParameter()
    o3.setId("test")
    self.assertTrue( self.kl.removeParameter(0) == o1 )
    self.assertTrue( self.kl.getNumParameters() == 2 )
    self.assertTrue( self.kl.removeParameter(0) == o2 )
    self.assertTrue( self.kl.getNumParameters() == 1 )
    self.assertTrue( self.kl.removeParameter("test") == o3 )
    self.assertTrue( self.kl.getNumParameters() == 0 )
    _dummyList = [ o1 ]; _dummyList[:] = []; del _dummyList
    _dummyList = [ o2 ]; _dummyList[:] = []; del _dummyList
    _dummyList = [ o3 ]; _dummyList[:] = []; del _dummyList
    pass  

  def test_KineticLaw_setBadFormula(self):
    formula =  "k1 X0";
    self.kl.setFormula(formula)
    self.assertEqual( False, self.kl.isSetFormula() )
    self.assertEqual( False, self.kl.isSetMath() )
    pass  

  def test_KineticLaw_setFormula(self):
    formula =  "k1*X0";
    self.kl.setFormula(formula)
    self.assertTrue(( formula == self.kl.getFormula() ))
    self.assertEqual( True, self.kl.isSetFormula() )
    if (self.kl.getFormula() == formula):
      pass    
    self.kl.setFormula(self.kl.getFormula())
    self.assertTrue(( formula == self.kl.getFormula() ))
    self.kl.setFormula("")
    self.assertEqual( False, self.kl.isSetFormula() )
    if (self.kl.getFormula() != None):
      pass    
    pass  

  def test_KineticLaw_setFormulaFromMath(self):
    math = libsbml.parseFormula("k1 * X0")
    self.assertEqual( False, self.kl.isSetMath() )
    self.assertEqual( False, self.kl.isSetFormula() )
    self.kl.setMath(math)
    self.assertEqual( True, self.kl.isSetMath() )
    self.assertEqual( True, self.kl.isSetFormula() )
    self.assertTrue((  "k1 * X0" == self.kl.getFormula() ))
    _dummyList = [ math ]; _dummyList[:] = []; del _dummyList
    pass  

  def test_KineticLaw_setMath(self):
    math = libsbml.parseFormula("k3 / k2")
    self.kl.setMath(math)
    math1 = self.kl.getMath()
    self.assertTrue( math1 != None )
    formula = libsbml.formulaToString(math1)
    self.assertTrue( formula != None )
    self.assertTrue((  "k3 / k2" == formula ))
    self.assertTrue( self.kl.getMath() != math )
    self.assertEqual( True, self.kl.isSetMath() )
    self.kl.setMath(self.kl.getMath())
    math1 = self.kl.getMath()
    self.assertTrue( math1 != None )
    formula = libsbml.formulaToString(math1)
    self.assertTrue( formula != None )
    self.assertTrue((  "k3 / k2" == formula ))
    self.assertTrue( self.kl.getMath() != math )
    self.kl.setMath(None)
    self.assertEqual( False, self.kl.isSetMath() )
    if (self.kl.getMath() != None):
      pass    
    _dummyList = [ math ]; _dummyList[:] = []; del _dummyList
    pass  

  def test_KineticLaw_setMathFromFormula(self):
    formula =  "k3 / k2";
    self.assertEqual( False, self.kl.isSetMath() )
    self.assertEqual( False, self.kl.isSetFormula() )
    self.kl.setFormula(formula)
    self.assertEqual( True, self.kl.isSetMath() )
    self.assertEqual( True, self.kl.isSetFormula() )
    formula = libsbml.formulaToString(self.kl.getMath())
    self.assertTrue((  "k3 / k2" == formula ))
    pass  

def suite():
  suite = unittest.TestSuite()
  suite.addTest(unittest.TestLoader.loadTestsFromTestCase(TestKineticLaw))

  return suite

if __name__ == "__main__":
  if unittest.TextTestRunner(verbosity=1).run(suite()).wasSuccessful() :
    sys.exit(0)
  else:
    sys.exit(1)
