//$$FILE$$
//$$VERSION$$
//$$DATE$$
//$$LICENSE$$


/*!
** \file DictObjFileSelectiveReader.C
**
** \brief Implementation file for the DictObjFileSelectiveReader application.
*/


#include <iostream>

#include "DictObjFile.h"
#include "DictObjCont.h"


using std::cout;
using std::cerr;
using std::endl;


int main(int argc, char ** argv)
{
  if (argc != 3)
  {
    cerr << "Usage: " << argv[0] 
	 << " <object filename> <datablock name>" << endl;
    return(1);
  }

  DictObjFile dictObjFile(argv[1]);

  dictObjFile.Read();

  cout << "Get everthing ... individually ..." << endl << endl;

  DictObjCont& dictObjCont = dictObjFile.GetDictObjCont(argv[2]);

  const vector<string>& title = dictObjCont.GetAttribute(
    CifString::CIF_DDL_CATEGORY_DICTIONARY,
    CifString::CIF_DDL_ITEM_TITLE);

  const vector<string>& version = dictObjCont.GetAttribute(
    CifString::CIF_DDL_CATEGORY_DICTIONARY,
    CifString::CIF_DDL_ITEM_VERSION);

  const vector<string>& description = dictObjCont.GetAttribute(
    CifString::CIF_DDL_CATEGORY_DATABLOCK,
    CifString::CIF_DDL_ITEM_DESCRIPTION);


  const vector<string>& historyVersion = dictObjCont.GetAttribute(
    CifString::CIF_DDL_CATEGORY_DICTIONARY_HISTORY,
    CifString::CIF_DDL_ITEM_VERSION);

  const vector<string>& historyUpdate = dictObjCont.GetAttribute(
    CifString::CIF_DDL_CATEGORY_DICTIONARY_HISTORY,
    CifString::CIF_DDL_ITEM_UPDATE);

  const vector<string>& historyRevision = dictObjCont.GetAttribute(
    CifString::CIF_DDL_CATEGORY_DICTIONARY_HISTORY,
    CifString::CIF_DDL_ITEM_REVISION);

  const vector<string>& subcategories = dictObjCont.GetAttribute(
    CifString::CIF_DDL_CATEGORY_SUB_CATEGORY,
    CifString::CIF_DDL_ITEM_ID);

  const vector<string>& categories = dictObjCont.GetAttribute(
    CifString::CIF_DDL_CATEGORY_CATEGORY,
    CifString::CIF_DDL_ITEM_ID);

  const vector<string>& items = dictObjCont.GetAttribute(
    CifString::CIF_DDL_CATEGORY_ITEM, CifString::CIF_DDL_ITEM_NAME);

  const vector<string>& methods = dictObjCont.GetAttribute(
    CifString::CIF_DDL_CATEGORY_DATABLOCK_METHODS,
    CifString::CIF_DDL_ITEM_DATABLOCK_ID);

  const vector<string>& methodsId = dictObjCont.GetAttribute(
    CifString::CIF_DDL_CATEGORY_DATABLOCK_METHODS,
    CifString::CIF_DDL_ITEM_METHOD_ID);

  const vector<string>& methodsList = dictObjCont.GetAttribute(
    CifString::CIF_DDL_CATEGORY_METHOD_LIST,
    CifString::CIF_DDL_ITEM_ID);

  const vector<string>& methodsListDetail = dictObjCont.GetAttribute(
    CifString::CIF_DDL_CATEGORY_METHOD_LIST,
    CifString::CIF_DDL_ITEM_DETAIL);

  const vector<string>& methodsListInline = dictObjCont.GetAttribute(
    CifString::CIF_DDL_CATEGORY_METHOD_LIST,
    CifString::CIF_DDL_ITEM_INLINE);

  const vector<string>& methodsListCode = dictObjCont.GetAttribute(
    CifString::CIF_DDL_CATEGORY_METHOD_LIST,
    CifString::CIF_DDL_ITEM_CODE);

  const vector<string>& methodsListLanguage = dictObjCont.GetAttribute(
    CifString::CIF_DDL_CATEGORY_METHOD_LIST,
    CifString::CIF_DDL_ITEM_LANGUAGE);

  const vector<string>& categoryGroupList = dictObjCont.GetAttribute(
    CifString::CIF_DDL_CATEGORY_CATEGORY_GROUP_LIST,
    CifString::CIF_DDL_ITEM_ID);

  const vector<string>& categoryGroupListParents = dictObjCont.GetAttribute(
    CifString::CIF_DDL_CATEGORY_CATEGORY_GROUP_LIST,
    CifString::CIF_DDL_ITEM_PARENT_ID);

  const vector<string>& categoryGroupListDescription = dictObjCont.GetAttribute(
    CifString::CIF_DDL_CATEGORY_CATEGORY_GROUP_LIST,
    CifString::CIF_DDL_ITEM_DESCRIPTION);

  const vector<string>& itemStructureListCode = dictObjCont.GetAttribute(
    CifString::CIF_DDL_CATEGORY_ITEM_STRUCTURE_LIST,
    CifString::CIF_DDL_ITEM_CODE);

  const vector<string>& itemStructureListIndex = dictObjCont.GetAttribute(
    CifString::CIF_DDL_CATEGORY_ITEM_STRUCTURE_LIST,
    CifString::CIF_DDL_ITEM_INDEX);

  const vector<string>& itemStructureListDimension  = dictObjCont.GetAttribute(
    CifString::CIF_DDL_CATEGORY_ITEM_STRUCTURE_LIST,
    CifString::CIF_DDL_ITEM_DIMENSION);

  const vector<string>& itemTypeListCode = dictObjCont.GetAttribute(
    CifString::CIF_DDL_CATEGORY_ITEM_TYPE_LIST,
    CifString::CIF_DDL_ITEM_CODE);

  const vector<string>& itemTypeListPrimitiveCode = dictObjCont.GetAttribute(
    CifString::CIF_DDL_CATEGORY_ITEM_TYPE_LIST,
    CifString::CIF_DDL_ITEM_PRIMITIVE_CODE);

  const vector<string>& itemTypeListConstruct = dictObjCont.GetAttribute(
    CifString::CIF_DDL_CATEGORY_ITEM_TYPE_LIST,
    CifString::CIF_DDL_ITEM_CONSTRUCT);

  const vector<string>& itemTypeListDetail = dictObjCont.GetAttribute(
    CifString::CIF_DDL_CATEGORY_ITEM_TYPE_LIST,
    CifString::CIF_DDL_ITEM_DETAIL);

  const vector<string>& itemUnitsListCode = dictObjCont.GetAttribute(
    CifString::CIF_DDL_CATEGORY_ITEM_UNITS_LIST,
    CifString::CIF_DDL_ITEM_CODE);

  const vector<string>& itemUnitsListDetail = dictObjCont.GetAttribute(
    CifString::CIF_DDL_CATEGORY_ITEM_UNITS_LIST,
    CifString::CIF_DDL_ITEM_DETAIL);

  const vector<string>& itemUnitsConversionOperator = dictObjCont.GetAttribute(
    CifString::CIF_DDL_CATEGORY_ITEM_UNITS_CONVERSION,
    CifString::CIF_DDL_ITEM_OPERATOR);

  const vector<string>& itemUnitsConversionFactor = dictObjCont.GetAttribute(
    CifString::CIF_DDL_CATEGORY_ITEM_UNITS_CONVERSION,
    CifString::CIF_DDL_ITEM_FACTOR);

  const vector<string>& itemUnitsConversionFromCode = dictObjCont.GetAttribute(
    CifString::CIF_DDL_CATEGORY_ITEM_UNITS_CONVERSION,
    CifString::CIF_DDL_ITEM_FROM_CODE);

  const vector<string>& itemUnitsConversionToCode = dictObjCont.GetAttribute(
    CifString::CIF_DDL_CATEGORY_ITEM_UNITS_CONVERSION,
    CifString::CIF_DDL_ITEM_TO_CODE);

  vector<string> regexes;
  for (unsigned int itemI = 0; itemI < items.size(); itemI++)
  {
    const ObjCont& itemObjCont = dictObjCont.GetObjCont(items[itemI],
      ItemObjContInfo::GetInstance());

    const vector<string>& tmp = itemObjCont.GetAttribute(
      CifString::CIF_DDL_CATEGORY_ITEM_TYPE_LIST,
      CifString::CIF_DDL_ITEM_CONSTRUCT);

    if (!tmp.empty())
    {
        regexes.push_back(tmp[0]);
    }
    else
    {
        regexes.push_back(string());
    }

    if (regexes[itemI].empty())
    {
        cout << itemI << ": " << "(null)" << endl;
    }
    else
    {
        cout << itemI << ": " << regexes[itemI] << endl;
    }
  }

  cout << "Title: " << title[0] << endl;
  cout << "Version: " << version[0] << endl;
  if (description[0].empty())
  {
      cout << "Description: " << "(null)" << endl;
  }
  else
  {
      cout << "Description: " << description[0] << endl;
  }
  cout << "HistoryVersion: (" << historyVersion.size() << ")" << endl;
  for (unsigned int i = 0; i < historyVersion.size(); i++) {
    cout << "  #" << i << " : " << historyVersion[i] << endl;
  }
  cout << "HistoryUpdate: (" << historyUpdate.size() << ")" << endl;
  for (unsigned int i = 0; i < historyUpdate.size(); i++) { 
    cout << "  #" << i << " : " << historyUpdate[i] << endl;
  }
  cout << "HistoryRevision: (" << historyRevision.size() << ")" << endl;
  for (unsigned int i = 0; i < historyRevision.size(); i++) {
    cout << "  #" << i << " : " << historyRevision[i] << endl;
  }

  cout << "Categories: (" << categories.size() << ")" << endl;
  for (unsigned int i = 0; i < categories.size(); i++) {
    cout << "  #" << i << " : " << categories[i] << endl;
  }
  cout << "SubCategories: (" << subcategories.size() << ")" << endl;
  for (unsigned int i = 0; i < subcategories.size(); i++) {
    cout << "  #" << i << " : " << subcategories[i] << endl;
  }
  cout << "Items: (" << items.size() << ")" << endl;
  for (unsigned int i = 0; i < items.size(); i++) {
    cout << "  #" << i << " : " << items[i] << endl;
  }
  cout << "MethodsDB: (" << methods.size() << ")" << endl;
  for (unsigned int i = 0; i < methods.size(); i++)
    cout << "  #" << i << " : " << methods[i] << endl;
  cout << "MethodsID: (" << methodsId.size() << ")" << endl;
  for (unsigned int i = 0; i < methodsId.size(); i++)
    cout << "  #" << i << " : " << methodsId[i] << endl;
  cout << "MethodsList: (" << methodsList.size() << ")" << endl;
  for (unsigned int i = 0; i < methodsList.size(); i++)
    cout << "  #" << i << " : " << methodsList[i] << endl;
  cout << "MethodsListDetail: (" << methodsListDetail.size() << ")" << endl;
  for (unsigned int i = 0; i < methodsListDetail.size(); i++)
    cout << "  #" << i << " : " << methodsListDetail[i] << endl;
  cout << "MethodsListInline: (" << methodsListInline.size() << ")" << endl;
  for (unsigned int i = 0; i < methodsListInline.size(); i++)
    cout << "  #" << i << " : " << methodsListInline[i] << endl;
  cout << "MethodsListCode: (" << methodsListCode.size() << ")" << endl;
  for (unsigned int i = 0; i < methodsListCode.size(); i++)
    cout << "  #" << i << " : " << methodsListCode[i] << endl;
  cout << "MethodsListLanguage: (" << methodsListLanguage.size() << ")" << endl;
  for (unsigned int i = 0; i < methodsListLanguage.size(); i++)
    cout << "  #" << i << " : " << methodsListLanguage[i] << endl;

  cout << "CategoryGroupList: (" << categoryGroupList.size() << ")" << endl;
  for (unsigned int i = 0; i < categoryGroupList.size(); i++)
    cout << "  #" << i << " : " << categoryGroupList[i] << endl;

  cout << "CategoryGroupListParents: (" << categoryGroupListParents.size() << ")" << endl;
  for (unsigned int i = 0; i < categoryGroupListParents.size(); i++)
    cout << "  #" << i << " : " << categoryGroupListParents[i] << endl;

  cout << "CategoryGroupListDescription: (" << categoryGroupListDescription.size() << ")" << endl;
  for (unsigned int i = 0; i < categoryGroupListDescription.size(); i++)
    cout << "  #" << i << " : " << categoryGroupListDescription[i] << endl;

  cout << "ItemStructureListCode: (" << itemStructureListCode.size() << ")" << endl;
  for (unsigned int i = 0; i < itemStructureListCode.size(); i++)
    cout << "  #" << i << " : " << itemStructureListCode[i] << endl;
  cout << "ItemStructureListIndex: (" << itemStructureListIndex.size() << ")" << endl;
  for (unsigned int i = 0; i < itemStructureListIndex.size(); i++)
    cout << "  #" << i << " : " << itemStructureListIndex[i] << endl;
  cout << "ItemStructureListDimension: (" << itemStructureListDimension.size() << ")" << endl;
  for (unsigned int i = 0; i < itemStructureListDimension.size(); i++)
    cout << "  #" << i << " : " << itemStructureListDimension[i] << endl;

  cout << "ItemTypeListCode: (" << itemTypeListCode.size() << ")" << endl;
  for (unsigned int i = 0; i < itemTypeListCode.size(); i++)
    cout << "  #" << i << " : " << itemTypeListCode[i] << endl;
  cout << "ItemTypeListPrimitiveCode: (" << itemTypeListPrimitiveCode.size() << ")" << endl;
  for (unsigned int i = 0; i < itemTypeListPrimitiveCode.size(); i++)
    cout << "  #" << i << " : " << itemTypeListPrimitiveCode[i] << endl;
  cout << "ItemTypeListConstruct: (" << itemTypeListConstruct.size() << ")" << endl;
  for (unsigned int i = 0; i < itemTypeListConstruct.size(); i++)
    cout << "  #" << i << " : " << itemTypeListConstruct[i] << endl;
  cout << "ItemTypeListDetail: (" << itemTypeListDetail.size() << ")" << endl;
  for (unsigned int i = 0; i < itemTypeListDetail.size(); i++)
    cout << "  #" << i << " : " << itemTypeListDetail[i] << endl;

  cout << "ItemUnitsListCode: (" << itemUnitsListCode.size() << ")" << endl;
  for (unsigned int i = 0; i < itemUnitsListCode.size(); i++)
    cout << "  #" << i << " : " << itemUnitsListCode[i] << endl;
  cout << "ItemUnitsListDetail: (" << itemUnitsListDetail.size() << ")" << endl;
  for (unsigned int i = 0; i < itemUnitsListDetail.size(); i++)
    cout << "  #" << i << " : " << itemUnitsListDetail[i] << endl;

  cout << "ItemUnitsConversionOperator: (" << itemUnitsConversionOperator.size() << ")" << endl;
  for (unsigned int i = 0; i < itemUnitsConversionOperator.size(); i++)
    cout << "  #" << i << " : " << itemUnitsConversionOperator[i] << endl;
  cout << "ItemUnitsConversionFactor: (" << itemUnitsConversionFactor.size() << ")" << endl;
  if (!itemUnitsConversionFactor.empty())
    for (unsigned int i = 0; i < itemUnitsConversionFactor.size(); i++)
      if (!itemUnitsConversionFactor[i].empty())
        cout << "  #" << i << " : " << itemUnitsConversionFactor[i] << endl;

  cout << "ItemUnitsConversionFromCode: (" << itemUnitsConversionFromCode.size() << ")" << endl;
   if (!itemUnitsConversionFromCode.empty())
     for (unsigned int i = 0; i < itemUnitsConversionFromCode.size(); i++)
      if (!itemUnitsConversionFromCode[i].empty())
        cout << "  #" << i << " : " << itemUnitsConversionFromCode[i] << endl;

  cout << "ItemUnitsConversionToCode: (" << itemUnitsConversionToCode.size() << ")" << endl;
   if (!itemUnitsConversionToCode.empty())
     for (unsigned int i = 0; i < itemUnitsConversionToCode.size(); i++)
      if (!itemUnitsConversionToCode[i].empty())
        cout << "  #" << i << " : " << itemUnitsConversionToCode[i] << endl;


  cout << "Done!" << endl;

}

