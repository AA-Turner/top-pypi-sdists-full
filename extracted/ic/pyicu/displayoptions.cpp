/* ====================================================================
 * Copyright (c) 2022-2024 Open Source Applications Foundation.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a
 * copy of this software and associated documentation files (the "Software"),
 * to deal in the Software without restriction, including without limitation
 * the rights to use, copy, modify, merge, publish, distribute, sublicense,
 * and/or sell copies of the Software, and to permit persons to whom the
 * Software is furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included
 * in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
 * OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
 * DEALINGS IN THE SOFTWARE.
 * ====================================================================
 */

#include "common.h"
#include "structmember.h"

#include "bases.h"
#include "locale.h"
#include "format.h"
#include "displayoptions.h"
#include "macros.h"

#include "arg.h"

#if U_ICU_VERSION_HEX >= VERSION_HEX(72, 0, 0)

DECLARE_CONSTANTS_TYPE(UDisplayOptionsGrammaticalCase)
DECLARE_CONSTANTS_TYPE(UDisplayOptionsNounClass)
DECLARE_CONSTANTS_TYPE(UDisplayOptionsPluralCategory)
DECLARE_CONSTANTS_TYPE(UDisplayOptionsCapitalization)
DECLARE_CONSTANTS_TYPE(UDisplayOptionsNameStyle)
DECLARE_CONSTANTS_TYPE(UDisplayOptionsDisplayLength)
DECLARE_CONSTANTS_TYPE(UDisplayOptionsSubstituteHandling)


using DisplayOptionsBuilder = DisplayOptions::Builder;

/* DisplayOptionsBuilder */

class t_displayoptionsbuilder : public _wrapper {
public:
    DisplayOptionsBuilder *object;
};

static PyObject *t_displayoptionsbuilder_setGrammaticalCase(t_displayoptionsbuilder *self, PyObject *arg);
static PyObject *t_displayoptionsbuilder_setNounClass(t_displayoptionsbuilder *self, PyObject *arg);
static PyObject *t_displayoptionsbuilder_setPluralCategory(t_displayoptionsbuilder *self, PyObject *arg);
static PyObject *t_displayoptionsbuilder_setCapitalization(t_displayoptionsbuilder *self, PyObject *arg);
static PyObject *t_displayoptionsbuilder_setNameStyle(t_displayoptionsbuilder *self, PyObject *arg);
static PyObject *t_displayoptionsbuilder_setDisplayLength(t_displayoptionsbuilder *self, PyObject *arg);
static PyObject *t_displayoptionsbuilder_setSubstituteHandling(t_displayoptionsbuilder *self, PyObject *arg);
static PyObject *t_displayoptionsbuilder_build(t_displayoptionsbuilder *self);

static PyMethodDef t_displayoptionsbuilder_methods[] = {
    DECLARE_METHOD(t_displayoptionsbuilder, setGrammaticalCase, METH_O),
    DECLARE_METHOD(t_displayoptionsbuilder, setNounClass, METH_O),
    DECLARE_METHOD(t_displayoptionsbuilder, setPluralCategory, METH_O),
    DECLARE_METHOD(t_displayoptionsbuilder, setCapitalization, METH_O),
    DECLARE_METHOD(t_displayoptionsbuilder, setNameStyle, METH_O),
    DECLARE_METHOD(t_displayoptionsbuilder, setDisplayLength, METH_O),
    DECLARE_METHOD(t_displayoptionsbuilder, setSubstituteHandling, METH_O),
    DECLARE_METHOD(t_displayoptionsbuilder, build, METH_NOARGS),
    { NULL, NULL, 0, NULL }
};

DECLARE_BY_VALUE_TYPE(DisplayOptionsBuilder, t_displayoptionsbuilder, UMemory,
                      DisplayOptionsBuilder, abstract_init)

/* DisplayOptions */

static PyObject *t_displayoptions_builder(PyTypeObject *type);
static PyObject *t_displayoptions_copyToBuilder(t_displayoptions *self);
static PyObject *t_displayoptions_getGrammaticalCase(t_displayoptions *self);
static PyObject *t_displayoptions_getNounClass(t_displayoptions *self);
static PyObject *t_displayoptions_getPluralCategory(t_displayoptions *self);
static PyObject *t_displayoptions_getCapitalization(t_displayoptions *self);
static PyObject *t_displayoptions_getNameStyle(t_displayoptions *self);
static PyObject *t_displayoptions_getDisplayLength(t_displayoptions *self);
static PyObject *t_displayoptions_getSubstituteHandling(t_displayoptions *self);

static PyMethodDef t_displayoptions_methods[] = {
    DECLARE_METHOD(t_displayoptions, builder, METH_CLASS | METH_NOARGS),
    DECLARE_METHOD(t_displayoptions, copyToBuilder, METH_NOARGS),
    DECLARE_METHOD(t_displayoptions, getGrammaticalCase, METH_NOARGS),
    DECLARE_METHOD(t_displayoptions, getNounClass, METH_NOARGS),
    DECLARE_METHOD(t_displayoptions, getPluralCategory, METH_NOARGS),
    DECLARE_METHOD(t_displayoptions, getCapitalization, METH_NOARGS),
    DECLARE_METHOD(t_displayoptions, getNameStyle, METH_NOARGS),
    DECLARE_METHOD(t_displayoptions, getDisplayLength, METH_NOARGS),
    DECLARE_METHOD(t_displayoptions, getSubstituteHandling, METH_NOARGS),
    { NULL, NULL, 0, NULL }
};

DECLARE_BY_VALUE_TYPE(DisplayOptions, t_displayoptions, UMemory,
                      DisplayOptions, abstract_init)


/* DisplayOptionsBuilder */

#define DEFINE_DISPLAY_OPTIONS_SETTER(name)                         \
    static PyObject *t_displayoptionsbuilder_set##name(             \
        t_displayoptionsbuilder *self, PyObject *arg)               \
{                                                                   \
    UDisplayOptions##name option;                                   \
                                                                    \
    if (!parseArg(arg, arg::Enum<UDisplayOptions##name>(&option)))  \
    {                                                               \
        self->object->set##name(option);                            \
        Py_RETURN_SELF();                                           \
    }                                                               \
                                                                    \
    return PyErr_SetArgsError((PyObject *) self, "set"#name, arg);  \
}

DEFINE_DISPLAY_OPTIONS_SETTER(GrammaticalCase)
DEFINE_DISPLAY_OPTIONS_SETTER(NounClass)
DEFINE_DISPLAY_OPTIONS_SETTER(PluralCategory)
DEFINE_DISPLAY_OPTIONS_SETTER(Capitalization)
DEFINE_DISPLAY_OPTIONS_SETTER(NameStyle)
DEFINE_DISPLAY_OPTIONS_SETTER(DisplayLength)
DEFINE_DISPLAY_OPTIONS_SETTER(SubstituteHandling)

static PyObject *t_displayoptionsbuilder_build(t_displayoptionsbuilder *self)
{
    return wrap_DisplayOptions(self->object->build());
}

/* DisplayOptions */

static PyObject *t_displayoptions_builder(PyTypeObject *type)
{
    return wrap_DisplayOptionsBuilder(DisplayOptions::builder());
}

static PyObject *t_displayoptions_copyToBuilder(t_displayoptions *self)
{
    return wrap_DisplayOptionsBuilder(self->object->copyToBuilder());
}

#define DEFINE_DISPLAY_OPTIONS_GETTER(name)                         \
static PyObject *t_displayoptions_get##name(t_displayoptions *self) \
{                                                                   \
    UDisplayOptions##name option = self->object->get##name();       \
    return PyInt_FromLong(option);                                  \
}

DEFINE_DISPLAY_OPTIONS_GETTER(GrammaticalCase)
DEFINE_DISPLAY_OPTIONS_GETTER(NounClass)
DEFINE_DISPLAY_OPTIONS_GETTER(PluralCategory)
DEFINE_DISPLAY_OPTIONS_GETTER(Capitalization)
DEFINE_DISPLAY_OPTIONS_GETTER(NameStyle)
DEFINE_DISPLAY_OPTIONS_GETTER(DisplayLength)
DEFINE_DISPLAY_OPTIONS_GETTER(SubstituteHandling)

#endif  // ICU >= 72

void _init_displayoptions(PyObject *m)
{
#if U_ICU_VERSION_HEX >= VERSION_HEX(72, 0, 0)
    INSTALL_STRUCT(DisplayOptionsBuilder, m);
    INSTALL_STRUCT(DisplayOptions, m);

    PyDict_SetItemString(DisplayOptionsType_.tp_dict, "Builder",
                         (PyObject *) &DisplayOptionsBuilderType_);

    INSTALL_CONSTANTS_TYPE(UDisplayOptionsGrammaticalCase, m);
    INSTALL_ENUM(UDisplayOptionsGrammaticalCase, "UNDEFINED", UDISPOPT_GRAMMATICAL_CASE_UNDEFINED);
    INSTALL_ENUM(UDisplayOptionsGrammaticalCase, "ABLATIVE", UDISPOPT_GRAMMATICAL_CASE_ABLATIVE);
    INSTALL_ENUM(UDisplayOptionsGrammaticalCase, "ACCUSATIVE", UDISPOPT_GRAMMATICAL_CASE_ACCUSATIVE);
    INSTALL_ENUM(UDisplayOptionsGrammaticalCase, "COMITATIVE", UDISPOPT_GRAMMATICAL_CASE_COMITATIVE);
    INSTALL_ENUM(UDisplayOptionsGrammaticalCase, "DATIVE", UDISPOPT_GRAMMATICAL_CASE_DATIVE);
    INSTALL_ENUM(UDisplayOptionsGrammaticalCase, "ERGATIVE", UDISPOPT_GRAMMATICAL_CASE_ERGATIVE);
    INSTALL_ENUM(UDisplayOptionsGrammaticalCase, "GENITIVE", UDISPOPT_GRAMMATICAL_CASE_GENITIVE);
    INSTALL_ENUM(UDisplayOptionsGrammaticalCase, "INSTRUMENTAL", UDISPOPT_GRAMMATICAL_CASE_INSTRUMENTAL);
    INSTALL_ENUM(UDisplayOptionsGrammaticalCase, "LOCATIVE", UDISPOPT_GRAMMATICAL_CASE_LOCATIVE);
    INSTALL_ENUM(UDisplayOptionsGrammaticalCase, "LOCATIVE_COPULATIVE", UDISPOPT_GRAMMATICAL_CASE_LOCATIVE_COPULATIVE);
    INSTALL_ENUM(UDisplayOptionsGrammaticalCase, "NOMINATIVE", UDISPOPT_GRAMMATICAL_CASE_NOMINATIVE);
    INSTALL_ENUM(UDisplayOptionsGrammaticalCase, "OBLIQUE", UDISPOPT_GRAMMATICAL_CASE_OBLIQUE);
    INSTALL_ENUM(UDisplayOptionsGrammaticalCase, "PREPOSITIONAL", UDISPOPT_GRAMMATICAL_CASE_PREPOSITIONAL);
    INSTALL_ENUM(UDisplayOptionsGrammaticalCase, "SOCIATIVE", UDISPOPT_GRAMMATICAL_CASE_SOCIATIVE);
    INSTALL_ENUM(UDisplayOptionsGrammaticalCase, "VOCATIVE", UDISPOPT_GRAMMATICAL_CASE_VOCATIVE);

    INSTALL_CONSTANTS_TYPE(UDisplayOptionsNounClass, m);
    INSTALL_ENUM(UDisplayOptionsNounClass, "UNDEFINED", UDISPOPT_NOUN_CLASS_UNDEFINED);
    INSTALL_ENUM(UDisplayOptionsNounClass, "OTHER", UDISPOPT_NOUN_CLASS_OTHER);
    INSTALL_ENUM(UDisplayOptionsNounClass, "NEUTER", UDISPOPT_NOUN_CLASS_NEUTER);
    INSTALL_ENUM(UDisplayOptionsNounClass, "FEMININE", UDISPOPT_NOUN_CLASS_FEMININE);
    INSTALL_ENUM(UDisplayOptionsNounClass, "MASCULINE", UDISPOPT_NOUN_CLASS_MASCULINE);
    INSTALL_ENUM(UDisplayOptionsNounClass, "ANIMATE", UDISPOPT_NOUN_CLASS_ANIMATE);
    INSTALL_ENUM(UDisplayOptionsNounClass, "INANIMATE", UDISPOPT_NOUN_CLASS_INANIMATE);
    INSTALL_ENUM(UDisplayOptionsNounClass, "PERSONAL", UDISPOPT_NOUN_CLASS_PERSONAL);
    INSTALL_ENUM(UDisplayOptionsNounClass, "COMMON", UDISPOPT_NOUN_CLASS_COMMON);

    INSTALL_CONSTANTS_TYPE(UDisplayOptionsPluralCategory, m);
    INSTALL_ENUM(UDisplayOptionsPluralCategory, "UNDEFINED", UDISPOPT_PLURAL_CATEGORY_UNDEFINED);
    INSTALL_ENUM(UDisplayOptionsPluralCategory, "ZERO", UDISPOPT_PLURAL_CATEGORY_ZERO);
    INSTALL_ENUM(UDisplayOptionsPluralCategory, "ONE", UDISPOPT_PLURAL_CATEGORY_ONE);
    INSTALL_ENUM(UDisplayOptionsPluralCategory, "TWO", UDISPOPT_PLURAL_CATEGORY_TWO);
    INSTALL_ENUM(UDisplayOptionsPluralCategory, "FEW", UDISPOPT_PLURAL_CATEGORY_FEW);
    INSTALL_ENUM(UDisplayOptionsPluralCategory, "MANY", UDISPOPT_PLURAL_CATEGORY_MANY);
    INSTALL_ENUM(UDisplayOptionsPluralCategory, "OTHER", UDISPOPT_PLURAL_CATEGORY_OTHER);

    INSTALL_CONSTANTS_TYPE(UDisplayOptionsCapitalization, m);
    INSTALL_ENUM(UDisplayOptionsCapitalization, "UNDEFINED", UDISPOPT_CAPITALIZATION_UNDEFINED);
    INSTALL_ENUM(UDisplayOptionsCapitalization, "BEGINNING_OF_SENTENCE", UDISPOPT_CAPITALIZATION_BEGINNING_OF_SENTENCE);
    INSTALL_ENUM(UDisplayOptionsCapitalization, "MIDDLE_OF_SENTENCE", UDISPOPT_CAPITALIZATION_MIDDLE_OF_SENTENCE);
    INSTALL_ENUM(UDisplayOptionsCapitalization, "STANDALONE", UDISPOPT_CAPITALIZATION_STANDALONE);
    INSTALL_ENUM(UDisplayOptionsCapitalization, "UI_LIST_OR_MENU", UDISPOPT_CAPITALIZATION_UI_LIST_OR_MENU);
    
    INSTALL_CONSTANTS_TYPE(UDisplayOptionsNameStyle, m);
    INSTALL_ENUM(UDisplayOptionsNameStyle, "UNDEFINED", UDISPOPT_NAME_STYLE_UNDEFINED);
    INSTALL_ENUM(UDisplayOptionsNameStyle, "STANDARD_NAMES", UDISPOPT_NAME_STYLE_STANDARD_NAMES);
    INSTALL_ENUM(UDisplayOptionsNameStyle, "DIALECT_NAMES", UDISPOPT_NAME_STYLE_DIALECT_NAMES);
    
    INSTALL_CONSTANTS_TYPE(UDisplayOptionsDisplayLength, m);
    INSTALL_ENUM(UDisplayOptionsDisplayLength, "UNDEFINED", UDISPOPT_DISPLAY_LENGTH_UNDEFINED);
    INSTALL_ENUM(UDisplayOptionsDisplayLength, "FULL", UDISPOPT_DISPLAY_LENGTH_FULL);
    INSTALL_ENUM(UDisplayOptionsDisplayLength, "SHORT", UDISPOPT_DISPLAY_LENGTH_SHORT);

    INSTALL_CONSTANTS_TYPE(UDisplayOptionsSubstituteHandling, m);
    INSTALL_ENUM(UDisplayOptionsSubstituteHandling, "UNDEFINED", UDISPOPT_SUBSTITUTE_HANDLING_UNDEFINED);
    INSTALL_ENUM(UDisplayOptionsSubstituteHandling, "SUBSTITUTE", UDISPOPT_SUBSTITUTE_HANDLING_SUBSTITUTE);
    INSTALL_ENUM(UDisplayOptionsSubstituteHandling, "NO_SUBSTITUTE", UDISPOPT_SUBSTITUTE_HANDLING_NO_SUBSTITUTE);
    
#endif  // ICU >= 72
}
