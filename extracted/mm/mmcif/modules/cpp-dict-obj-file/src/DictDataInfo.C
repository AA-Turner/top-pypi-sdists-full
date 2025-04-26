//$$FILE$$
//$$VERSION$$
//$$DATE$$
//$$LICENSE$$


#include <string>
#include <vector>

#include "GenCont.h"
#include "DictObjCont.h"
#include "DictObjContInfo.h"
#include "DictDataInfo.h"


using std::string;
using std::vector;


#ifdef VLAD_INTRODUCE_LATER
bool IsNullRow(const vector<string>& row);
#endif


DictDataInfo::DictDataInfo(const DictObjCont& dictObjCont) :
  _dictObjCont(dictObjCont)
{

}


DictDataInfo::~DictDataInfo()
{

}


void DictDataInfo::GetVersion(string& version)
{
    _GetDictVersion(version);
}


const vector<string>& DictDataInfo::GetCatNames()
{
    return(_dictObjCont.GetAttribute(CifString::CIF_DDL_CATEGORY_CATEGORY,
      CifString::CIF_DDL_ITEM_ID));
}


const vector<string>& DictDataInfo::GetItemsNames()
{
    return(_dictObjCont.GetAttribute(CifString::CIF_DDL_CATEGORY_ITEM,
      CifString::CIF_DDL_ITEM_NAME));
}


bool DictDataInfo::IsCatDefined(const string& catName) const
{
    return(_isDictCategory(catName));
}


bool DictDataInfo::IsItemDefined(const string& itemName)
{
    const vector<string>& items =
      _dictObjCont.GetAttribute(CifString::CIF_DDL_CATEGORY_ITEM,
      CifString::CIF_DDL_ITEM_NAME);

    return(GenCont::IsInVector(itemName, items));
}


const vector<string>& DictDataInfo::GetCatKeys(const string& catName)
{
    const ObjCont& catCont = _dictObjCont.GetObjCont(catName,
      CatObjContInfo::GetInstance());

    return(catCont.GetAttribute(CifString::CIF_DDL_CATEGORY_CATEGORY_KEY,
      CifString::CIF_DDL_ITEM_NAME));
}


const vector<string>& DictDataInfo::GetCatAttribute(const string& catName,
  const string& refCatName, const string& refAttrName)
{
    const ObjCont& catCont = _dictObjCont.GetObjCont(catName,
      CatObjContInfo::GetInstance());

    return(catCont.GetAttribute(refCatName, refAttrName));
}


const vector<string>& DictDataInfo::GetItemAttribute(const string& itemName,
  const string& refCatName, const string& refAttrName)
{
    const ObjCont& itemCont = _dictObjCont.GetObjCont(itemName,
      ItemObjContInfo::GetInstance());

    return(itemCont.GetAttribute(refCatName, refAttrName));
}


#ifdef VLAD_INTRODUCE_LATER
bool IsNullRow(const vector<string>& row)
{
    for (unsigned int i = 0; i < row.size(); ++i)
    {
        if (!CifString::IsUnknownValue(row[i]))
        {
            return(false);
        }
    }

    return(true);
}
#endif


void DictDataInfo::_GetDictVersion(string& dictVer)
{

    dictVer.clear();

    const vector<string>& dictVersion =
      _dictObjCont.GetAttribute(CifString::CIF_DDL_CATEGORY_DICTIONARY,
      CifString::CIF_DDL_ITEM_VERSION);

    if (dictVersion.empty())
    {
        return;
    }

    if (dictVersion[0].empty())
    {
        return;
    }

    dictVer = dictVersion[0];

}


bool DictDataInfo::_isDictCategory(const string& category) const
{
    const vector<string>& dictCategories  = _dictObjCont.GetAttribute(
      CifString::CIF_DDL_CATEGORY_CATEGORY, CifString::CIF_DDL_ITEM_ID);

    return (GenCont::IsInVector(category, dictCategories));
}


void DictDataInfo::GetCatItemsNames(vector<string>& itemsNames,
  const string& catName)
{
    itemsNames.clear();

    // Get all items of a category
    const vector<string>& allItemsNames = 
      _dictObjCont.GetAttribute(CifString::CIF_DDL_CATEGORY_ITEM,
      CifString::CIF_DDL_ITEM_NAME);

    for (unsigned int itemI = 0; itemI < allItemsNames.size(); ++itemI)
    {
        string itemCatName;
        CifString::GetCategoryFromCifItem(itemCatName, allItemsNames[itemI]);

        if (itemCatName == catName)
            itemsNames.push_back(allItemsNames[itemI]);
    }
}


void DictDataInfo::GetParentCifItems(vector<string>& parCifItems,
  const string& cifItemName)
{
    parCifItems.clear();

    const ObjCont& itemCont = _dictObjCont.GetObjCont(cifItemName,
      ItemObjContInfo::GetInstance());

    parCifItems =
      itemCont.GetAttribute(CifString::CIF_DDL_CATEGORY_ITEM_LINKED,
        CifString::CIF_DDL_ITEM_PARENT_NAME);
}

