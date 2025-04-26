//$$FILE$$
//$$VERSION$$
//$$DATE$$
//$$LICENSE$$


/*!
** \file DictObjContInfo.C
**
** \brief Implementation file for ObjContInfo, DictObjContInfo, CatObjContInfo,
**   SubcatObjContInfo and ItemObjContInfo classes.
*/


#include <iostream>

#include "Exceptions.h"
#include "rcsb_types.h"
#include "Serializer.h"
#include "DictObjContInfo.h"


using std::string;
using std::pair;
using std::map;
using std::make_pair;


ObjContInfo::ObjContInfo()
{
    _cats.clear();

    _catMap.clear();
}


void ObjContInfo::AddCat(const string& catName)
{
    AddCat(catName, string());
}


void ObjContInfo::AddCat(const string& catName, const string& col1,
  const bool nonDefaultValue, const bool inheritance)
{
    Cat cat;

    cat.catName = catName;
    cat.col1 = col1;
    cat.nonDefaultValue = nonDefaultValue;
    cat.inheritance = inheritance;
 
    _cats.push_back(cat);

    currCat = _cats.end() - 1;
}


void ObjContInfo::AddItem(const string& descr, const string& itemName)
{
    Item item;

    item.descr = descr;
    item.itemName = itemName;

    (*currCat).items.push_back(item);

    unsigned int currElemIndex = _cats.size() - 1;
    unsigned int currSubElemIndex = (*currCat).items.size() - 1;

    map<pair<string, string>, pair<unsigned int, unsigned int> >::value_type
      valType(make_pair(string((*currCat).catName),
      string(itemName)), make_pair(currElemIndex, currSubElemIndex));

    _catMap.insert(valType);
}


unsigned int ObjContInfo::GetItemIndex(const string& catName,
  const string& itemName) const
{
    map<pair<string, string>, pair<unsigned int, unsigned int> >::\
      const_iterator pos = _catMap.find(make_pair(catName, itemName));
    if (pos != _catMap.end())
    {
        // Found
        return((pos->second).first);
    }

    throw NotFoundException("Index not found", "ObjContInfo::GetItemIndex");

}


pair<unsigned int, unsigned int> ObjContInfo::GetItemIndices(
  const string& catName, const string& itemName) const
{
    map<pair<string, string>, pair<unsigned int, unsigned int> >::
      const_iterator pos = _catMap.find(make_pair(catName, itemName));
    if (pos != _catMap.end())
    {
        // Found
        return(pos->second);
    }

    throw NotFoundException("Indices not found",
      "ObjContInfo::GetItemIndices");

}


ObjContInfo::~ObjContInfo()
{
    _cats.clear();

    _catMap.clear();
}


DictObjContInfo& DictObjContInfo::GetInstance()
{
    static DictObjContInfo dictObjContInfo;
 
    return (dictObjContInfo);
}


DictObjContInfo::DictObjContInfo()
{
    _objContInfoDescr = "dictionary";

    AddCat(CifString::CIF_DDL_CATEGORY_DICTIONARY);
    AddItem("Title", CifString::CIF_DDL_ITEM_TITLE);
    AddItem("Version", CifString::CIF_DDL_ITEM_VERSION);

    AddCat(CifString::CIF_DDL_CATEGORY_DATABLOCK);
    AddItem("Description", CifString::CIF_DDL_ITEM_DESCRIPTION);

    AddCat(CifString::CIF_DDL_CATEGORY_DICTIONARY_HISTORY);
    AddItem("HistoryVersion", CifString::CIF_DDL_ITEM_VERSION);
    AddItem("HistoryUpdate", CifString::CIF_DDL_ITEM_UPDATE);
    AddItem("HistoryRevision", CifString::CIF_DDL_ITEM_REVISION);

    AddCat(CifString::CIF_DDL_CATEGORY_CATEGORY);
    AddItem("Categories", CifString::CIF_DDL_ITEM_ID);

    AddCat(CifString::CIF_DDL_CATEGORY_SUB_CATEGORY);
    AddItem("SubCategories", CifString::CIF_DDL_ITEM_ID);

    AddCat(CifString::CIF_DDL_CATEGORY_ITEM);
    AddItem("Items", CifString::CIF_DDL_ITEM_NAME);

    AddCat(CifString::CIF_DDL_CATEGORY_DATABLOCK_METHODS);
    AddItem("MethodsDB", CifString::CIF_DDL_ITEM_DATABLOCK_ID);
    AddItem("MethodsID", CifString::CIF_DDL_ITEM_METHOD_ID);

    AddCat(CifString::CIF_DDL_CATEGORY_METHOD_LIST);
    AddItem("MethodsList", CifString::CIF_DDL_ITEM_ID);
    AddItem("MethodsListDetail", CifString::CIF_DDL_ITEM_DETAIL);
    AddItem("MethodsListInline", CifString::CIF_DDL_ITEM_INLINE);
    AddItem("MethodsListCode", CifString::CIF_DDL_ITEM_CODE);
    AddItem("MethodsListLanguage", CifString::CIF_DDL_ITEM_LANGUAGE);

    AddCat(CifString::CIF_DDL_CATEGORY_CATEGORY_GROUP_LIST);
    AddItem("CategoryGroupList", CifString::CIF_DDL_ITEM_ID);
    AddItem("CategoryGroupListParents", CifString::CIF_DDL_ITEM_PARENT_ID);
    AddItem("CategoryGroupListDescription",
      CifString::CIF_DDL_ITEM_DESCRIPTION);

    AddCat(CifString::CIF_DDL_CATEGORY_ITEM_STRUCTURE_LIST);
    AddItem("ItemStructureListCode", CifString::CIF_DDL_ITEM_CODE);
    AddItem("ItemStructureListIndex", CifString::CIF_DDL_ITEM_INDEX);
    AddItem("ItemStructureListDimension", CifString::CIF_DDL_ITEM_DIMENSION);

    AddCat(CifString::CIF_DDL_CATEGORY_ITEM_TYPE_LIST);
    AddItem("ItemTypeListCode", CifString::CIF_DDL_ITEM_CODE);
    AddItem("ItemTypeListPrimitiveCode",
      CifString::CIF_DDL_ITEM_PRIMITIVE_CODE);
    AddItem("ItemTypeListConstruct", CifString::CIF_DDL_ITEM_CONSTRUCT);
    AddItem("ItemTypeListDetail", CifString::CIF_DDL_ITEM_DETAIL);

    AddCat(CifString::CIF_DDL_CATEGORY_ITEM_UNITS_LIST);
    AddItem("ItemUnitsListCode", CifString::CIF_DDL_ITEM_CODE);
    AddItem("ItemUnitsListDetail", CifString::CIF_DDL_ITEM_DETAIL);

    AddCat(CifString::CIF_DDL_CATEGORY_ITEM_UNITS_CONVERSION);
    AddItem("ItemUnitsConversionOperator", CifString::CIF_DDL_ITEM_OPERATOR);
    AddItem("ItemUnitsConversionFactor", CifString::CIF_DDL_ITEM_FACTOR);
    AddItem("ItemUnitsConversionFromCode", CifString::CIF_DDL_ITEM_FROM_CODE);
    AddItem("ItemUnitsConversionToCode", CifString::CIF_DDL_ITEM_TO_CODE);
}


DictObjContInfo::~DictObjContInfo()
{

}


CatObjContInfo& CatObjContInfo::GetInstance()
{
    static CatObjContInfo catObjContInfo;
 
    return (catObjContInfo);
}


CatObjContInfo::CatObjContInfo()
{
    _objContInfoDescr = "category";

    AddCat(CifString::CIF_DDL_CATEGORY_CATEGORY, CifString::CIF_DDL_ITEM_ID);
    AddItem("Description", CifString::CIF_DDL_ITEM_DESCRIPTION);
    AddItem("Mandatory Code", CifString::CIF_DDL_ITEM_MANDATORY_CODE);

    AddCat(CifString::CIF_DDL_CATEGORY_NDB_CATEGORY_DESCRIPTION,
      CifString::CIF_DDL_ITEM_ID);
    AddItem("NDB Description", CifString::CIF_DDL_ITEM_DESCRIPTION);

    AddCat(CifString::CIF_DDL_CATEGORY_CATEGORY_KEY,
      CifString::CIF_DDL_ITEM_ID);
    AddItem("Keys", CifString::CIF_DDL_ITEM_NAME);

    AddCat(CifString::CIF_DDL_CATEGORY_CATEGORY_EXAMPLES,
      CifString::CIF_DDL_ITEM_ID);
    AddItem("ExamplesCase", CifString::CIF_DDL_ITEM_CASE);
    AddItem("ExamplesDetail", CifString::CIF_DDL_ITEM_DETAIL);

    AddCat(CifString::CIF_DDL_CATEGORY_NDB_CATEGORY_EXAMPLES,
      CifString::CIF_DDL_ITEM_ID);
    AddItem("ExamplesCase NDB", CifString::CIF_DDL_ITEM_CASE);
    AddItem("ExamplesDetail NDB", CifString::CIF_DDL_ITEM_DETAIL);

    AddCat(CifString::CIF_DDL_CATEGORY_CATEGORY_GROUP,
      CifString::CIF_DDL_ITEM_CATEGORY_ID);
    AddItem("CategoryGroups", CifString::CIF_DDL_ITEM_ID);

    AddCat(CifString::CIF_DDL_CATEGORY_CATEGORY_METHODS,
      CifString::CIF_DDL_ITEM_CATEGORY_ID);
    AddItem("CategoryMethods", CifString::CIF_DDL_ITEM_METHOD_ID);

    AddCat(CifString::CIF_DDL_CATEGORY_PDBX_ITEM_LINKED_GROUP,
      CifString::CIF_DDL_ITEM_CATEGORY_ID);
    AddItem("Link group Id", CifString::CIF_DDL_ITEM_LINK_GROUP_ID);
    AddItem("Label", CifString::CIF_DDL_ITEM_LABEL);
    AddItem("Label", CifString::CIF_DDL_ITEM_CONTEXT);
    AddItem("Label", CifString::CIF_DDL_ITEM_CONDITION_ID);
}


CatObjContInfo::~CatObjContInfo()
{

}


SubcatObjContInfo& SubcatObjContInfo::GetInstance()
{
    static SubcatObjContInfo subCatObjContInfo;
 
    return (subCatObjContInfo);
}


SubcatObjContInfo::SubcatObjContInfo()
{
    _objContInfoDescr = "subcategory";

    AddCat(CifString::CIF_DDL_CATEGORY_SUB_CATEGORY,
      CifString::CIF_DDL_ITEM_ID);
    AddItem("Description", CifString::CIF_DDL_ITEM_DESCRIPTION);

    AddCat(CifString::CIF_DDL_CATEGORY_SUB_CATEGORY_EXAMPLES,
      CifString::CIF_DDL_ITEM_NAME);
    AddItem("ExamplesCase", CifString::CIF_DDL_ITEM_CASE);
    AddItem("ExamplesDetail", CifString::CIF_DDL_ITEM_DETAIL);

    AddCat(CifString::CIF_DDL_CATEGORY_SUB_CATEGORY_METHODS,
      CifString::CIF_DDL_ITEM_SUB_CATEGORY_ID);
    AddItem("SubcategoryMethods", CifString::CIF_DDL_ITEM_METHOD_ID);
}


SubcatObjContInfo::~SubcatObjContInfo()
{

}


ItemObjContInfo& ItemObjContInfo::GetInstance()
{
    static ItemObjContInfo itemObjContInfo;
 
    return (itemObjContInfo);
}


ItemObjContInfo::ItemObjContInfo()
{
    _objContInfoDescr = "item";

    AddCat(CifString::CIF_DDL_CATEGORY_ITEM_DESCRIPTION,
      CifString::CIF_DDL_ITEM_NAME);
    AddItem("Description", CifString::CIF_DDL_ITEM_DESCRIPTION);

    AddCat(CifString::CIF_DDL_CATEGORY_NDB_ITEM_DESCRIPTION,
      CifString::CIF_DDL_ITEM_NAME);
    AddItem("Description NDB", CifString::CIF_DDL_ITEM_DESCRIPTION);

    AddCat(CifString::CIF_DDL_CATEGORY_ITEM_TYPE, CifString::CIF_DDL_ITEM_NAME);
    AddItem("Type", CifString::CIF_DDL_ITEM_CODE);

    AddCat(CifString::CIF_DDL_CATEGORY_ITEM_TYPE_LIST,
      CifString::CIF_DDL_ITEM_CODE, true);
    AddItem("PrimitiveCode", CifString::CIF_DDL_ITEM_PRIMITIVE_CODE);
    AddItem("Regular expression", CifString::CIF_DDL_ITEM_CONSTRUCT);

    AddCat(CifString::CIF_DDL_CATEGORY_ITEM, CifString::CIF_DDL_ITEM_NAME);
    AddItem("MandatoryCode", CifString::CIF_DDL_ITEM_MANDATORY_CODE);

    AddCat(CifString::CIF_DDL_CATEGORY_ITEM_DEFAULT,
      CifString::CIF_DDL_ITEM_NAME);
    AddItem("DefaultValue", CifString::CIF_DDL_ITEM_VALUE);

    AddCat(CifString::CIF_DDL_CATEGORY_ITEM_UNITS,
      CifString::CIF_DDL_ITEM_NAME);
    AddItem("Units", CifString::CIF_DDL_ITEM_CODE);

    AddCat(CifString::CIF_DDL_CATEGORY_ITEM_STRUCTURE,
      CifString::CIF_DDL_ITEM_NAME);
    AddItem("ItemStructure", CifString::CIF_DDL_ITEM_CODE);
    AddItem("ItemStructureOrganization",
      CifString::CIF_DDL_ITEM_ORGANIZATION);

    AddCat(CifString::CIF_DDL_CATEGORY_ITEM_RANGE,
      CifString::CIF_DDL_ITEM_NAME);
    AddItem("RangeMin", CifString::CIF_DDL_ITEM_MINIMUM);
    AddItem("RangeMax", CifString::CIF_DDL_ITEM_MAXIMUM);

    AddCat(CifString::CIF_DDL_CATEGORY_ITEM_ALIASES,
      CifString::CIF_DDL_ITEM_NAME);
    AddItem("Alias", CifString::CIF_DDL_ITEM_ALIAS_NAME);
    AddItem("Alias Dictionary", CifString::CIF_DDL_ITEM_DICTIONARY);
    AddItem("Alias Version", CifString::CIF_DDL_ITEM_VERSION);

    AddCat(CifString::CIF_DDL_CATEGORY_ITEM_DEPENDENT,
      CifString::CIF_DDL_ITEM_NAME, false, true);
    AddItem("Dependents", CifString::CIF_DDL_ITEM_DEPENDENT_NAME);

    AddCat(CifString::CIF_DDL_CATEGORY_ITEM_RELATED,
      CifString::CIF_DDL_ITEM_NAME);
    AddItem("Related", CifString::CIF_DDL_ITEM_RELATED_NAME);
    AddItem("RelatedFunctionCode", CifString::CIF_DDL_ITEM_FUNCTION_CODE);

    AddCat(CifString::CIF_DDL_CATEGORY_ITEM_SUB_CATEGORY,
      CifString::CIF_DDL_ITEM_NAME, false, true);
    AddItem("SubCategory", CifString::CIF_DDL_ITEM_ID);

    AddCat(CifString::CIF_DDL_CATEGORY_ITEM_LINKED,
      CifString::CIF_DDL_ITEM_PARENT_NAME);
    AddItem("Child", CifString::CIF_DDL_ITEM_CHILD_NAME);

    AddCat(CifString::CIF_DDL_CATEGORY_ITEM_LINKED,
      CifString::CIF_DDL_ITEM_CHILD_NAME);
    AddItem("Parent", CifString::CIF_DDL_ITEM_PARENT_NAME);

    AddCat(CifString::CIF_DDL_CATEGORY_ITEM_METHODS,
      CifString::CIF_DDL_ITEM_NAME);
    AddItem("Method", CifString::CIF_DDL_ITEM_METHOD_ID);

    AddCat(CifString::CIF_DDL_CATEGORY_ITEM_TYPE_CONDITIONS,
      CifString::CIF_DDL_ITEM_NAME);
    AddItem("TypeCondition", CifString::CIF_DDL_ITEM_CODE);

    AddCat(CifString::CIF_DDL_CATEGORY_ITEM_EXAMPLES,
      CifString::CIF_DDL_ITEM_NAME);
    AddItem("Case", CifString::CIF_DDL_ITEM_CASE);
    AddItem("Detail", CifString::CIF_DDL_ITEM_DETAIL);

    AddCat(CifString::CIF_DDL_CATEGORY_ITEM_ENUMERATION,
      CifString::CIF_DDL_ITEM_NAME);
    AddItem("Value", CifString::CIF_DDL_ITEM_VALUE);
    AddItem("Detail", CifString::CIF_DDL_ITEM_DETAIL);

    AddCat(CifString::CIF_DDL_CATEGORY_NDB_ITEM_EXAMPLES,
      CifString::CIF_DDL_ITEM_NAME);
    AddItem("Case", CifString::CIF_DDL_ITEM_CASE);
    AddItem("Detail", CifString::CIF_DDL_ITEM_DETAIL);

    AddCat(CifString::CIF_DDL_CATEGORY_NDB_ITEM_ENUMERATION,
      CifString::CIF_DDL_ITEM_NAME);
    AddItem("Value", CifString::CIF_DDL_ITEM_VALUE);
    AddItem("Detail", CifString::CIF_DDL_ITEM_DETAIL);

    AddCat(CifString::CIF_DDL_CATEGORY_PDBX_ITEM_LINKED_GROUP_LIST,
      CifString::CIF_DDL_ITEM_CHILD_NAME);
    AddItem("Child category Id", CifString::CIF_DDL_ITEM_CHILD_CATEGORY_ID);
    AddItem("Link group Id", CifString::CIF_DDL_ITEM_LINK_GROUP_ID);
    AddItem("Parent category Id", CifString::CIF_DDL_ITEM_PARENT_CATEGORY_ID);
    AddItem("Parent", CifString::CIF_DDL_ITEM_PARENT_NAME);
}


ItemObjContInfo::~ItemObjContInfo()
{

}

