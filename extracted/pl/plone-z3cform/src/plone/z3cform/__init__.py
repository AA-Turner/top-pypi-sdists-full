from plone.z3cform.patch import apply_patch

import zope.i18nmessageid


MessageFactory = zope.i18nmessageid.MessageFactory("plone.z3cform")


apply_patch()
