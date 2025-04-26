//$$FILE$$
//$$VERSION$$
//$$DATE$$
//$$LICENSE$$


/*!
** \file DictObjCont.C
**
** \brief Implementation file for ObjCont, ItemObjCont and DictObjCont classes.
*/


#include <string>
#include <algorithm>

#include "ISTable.h"
#include "DictObjContInfo.h"
#include "DictObjCont.h"


using std::make_pair;
using std::cout;
using std::endl;
using std::sort;


ObjCont::ObjCont(Serializer& ser, DicFile& dicFile,
  const string& blockName, const string& id, const ObjContInfo& objContInfo) :
  _ser(ser), _dicFile(dicFile), _objContInfo(objContInfo)
{
  Init();

  // VLAD - IMPROVE
  // Throw exception here and everywhere regarding empty blockName or id or
  // maybe something else.

  _blockName = blockName;
  _id = id;  

  _verbose = false;
}


ObjCont::~ObjCont()
{
  _blockName.clear();
  _id.clear();

  _index.clear();

  _itemsStore.clear();

}


void ObjCont::Init()
{
  _blockName.clear();
  _id.clear();

  _index.clear();

  _itemsStore.clear();

  vector<string> tmp1;
  vector<vector<string> > tmp2;

  for (unsigned int i = 0; i < _objContInfo._cats.size(); ++i)
  {
    tmp2.clear();
    for (unsigned int j = 0; j < _objContInfo._cats[i].items.size();
      ++j)
    {
      tmp2.push_back(tmp1);
    }
    _itemsStore.push_back(tmp2);
  }

}


const string& ObjCont::GetName() const
{

    return(_id);

}


const vector<string>& ObjCont::GetAttribute(const string& catName,
  const string& itemName) const
{

    pair<unsigned int, unsigned int> indexPair =
      _objContInfo.GetItemIndices(catName, itemName);

    return(_itemsStore[indexPair.first][indexPair.second]);

}


void ObjCont::Print() const
{
    cout << endl;
    cout << "Dictionary/Datablock Name: " << _blockName << endl;
    cout << "Id: " << _id << endl;

    pair<unsigned int, unsigned int> indexPair;

    for (unsigned int i = 0; i < _objContInfo._cats.size(); ++i)
    {
        for (unsigned int j = 0; j < _objContInfo._cats[i].\
          items.size(); ++j)
        {
            indexPair = _objContInfo.GetItemIndices(_objContInfo.\
              _cats[i].catName.c_str(),
            _objContInfo._cats[i].items[j].itemName.c_str());
            cout << _objContInfo._cats[i].items[j].descr << ": (" <<
              _itemsStore[indexPair.first][indexPair.second].size() << ")" << endl;

            for (unsigned int ii = 0; ii < _itemsStore[indexPair.first]\
              [indexPair.second].size(); ii++) 
                cout << "  #" << ii << " : " << _itemsStore[indexPair.first]\
                  [indexPair.second][ii] << endl;
        }
    }

}


UInt32 ObjCont::Write()
{
    // Write items
    for (unsigned int i = 0; i < _itemsStore.size(); ++i)
    {
        for (unsigned int j = 0; j < _itemsStore[i].size(); ++j)
        {
            if (!_itemsStore[i][j].empty())
                _index.push_back(_ser.WriteStrings(_itemsStore[i][j]));
            else
                _index.push_back(0);
        }
    }

    return (_ser.WriteUInt32s(_index));
}


void ObjCont::Read(UInt32 which, unsigned int Index)
{
/*
-------------------------------------------------------------------------------
  Read() calls all of the private Get methods so that the entire object
  can be retrieved from memory. The object# must be specified.
-------------------------------------------------------------------------------
*/

  _index.clear();
  _ser.ReadUInt32s(_index, which); 

  pair<unsigned int, unsigned int> indexPair;

  // Get complex items
  for (unsigned int i = 0; i < _objContInfo._cats.size(); ++i)
  {
    for (unsigned int j = 0; j < _objContInfo._cats[i].items.size(); ++j)
    {
      indexPair = _objContInfo.GetItemIndices(_objContInfo._cats[i].catName,
        _objContInfo._cats[i].items[j].itemName);

      ReadItem(indexPair, Index);
      ++Index;
    }
  }

}


void ObjCont::ReadItem(const pair<unsigned int, unsigned int>& indexPair,
  unsigned int Index)
{
    if (_index.empty())
    {
        throw EmptyValueException("Empty index vector",
          "ObjCont::ReadItem");
    }
 
    if (!_itemsStore[indexPair.first][indexPair.second].empty())
    {
        for (UInt32 i = 0; i < _itemsStore[indexPair.first][indexPair.second].\
          size(); i++) 
          _itemsStore[indexPair.first][indexPair.second][i].clear();
        _itemsStore[indexPair.first][indexPair.second].clear();
    }

    if (_index[Index] == 0)
        _itemsStore[indexPair.first][indexPair.second].clear();
    else
        _ser.ReadStrings(_itemsStore[indexPair.first][indexPair.second],
          _index[Index]);
}


void ObjCont::SetVerbose(bool verbose)
{
    _verbose = verbose;
}


void ObjCont::Build()
{

    for (unsigned int i = 0; i < _objContInfo._cats.size(); ++i)
    {
        BuildItems(_itemsStore[i], i);
    }

}


void ObjCont::BuildItems(vector<vector<string> >& combo,
  const unsigned int configIndex)
{
    ObjCont::BuildItems(combo, configIndex, _id);    
}


void ObjCont::BuildItems(vector<vector<string> >& combo,
  const unsigned int configIndex, const string& value)
{
    if (_id.empty() || _blockName.empty())
    {
        return;
    }
 
    Block& block = _dicFile.GetBlock(_blockName);

    ISTable* tbl = block.GetTablePtr(_objContInfo._cats[configIndex].catName);
    if (tbl == NULL)
    {
        return;
    }

    vector<string> ColumnNames;
    ColumnNames.push_back(_objContInfo._cats[configIndex].col1);

    vector<string> values;
    if (_objContInfo._cats[configIndex].nonDefaultValue)
    {
        unsigned int valIndex =
          _objContInfo.GetItemIndex(CifString::CIF_DDL_CATEGORY_ITEM_TYPE,
          CifString::CIF_DDL_ITEM_CODE);

        vector<string> tmp1;
        vector<vector<string> > valueVector;

        for (unsigned int j = 0; j < _objContInfo._cats[valIndex].\
          items.size(); ++j)
        {
            valueVector.push_back(tmp1);
        }

        BuildItems(valueVector, valIndex);

        if (valueVector[0].empty())
            return;

        values.push_back(valueVector[0][0]); 

        if (_itemsStore[valIndex][0].empty())
            _itemsStore[valIndex][0].push_back(valueVector[0][0]);
    }
    else
    {
        values.push_back(value); 
    }

    tbl->SetFlags(_objContInfo._cats[configIndex].col1, ISTable::DT_STRING |
      ISTable::CASE_INSENSE);

    vector<unsigned int> listOut;
    tbl->Search(listOut, values, ColumnNames);
    if (listOut.empty())
    {
        return;
    }

    vector<string> columnNames;

    for (unsigned int ind = 0; ind < _objContInfo.\
      _cats[configIndex].items.size(); ++ind)
    {
        if (tbl->IsColumnPresent(_objContInfo._cats[configIndex].\
          items[ind].itemName))
        {
            columnNames.push_back(_objContInfo._cats[configIndex].\
              items[ind].itemName);
        }
        else
        {
#ifdef VLAD_REVERSE_ENG
            std::cerr << "ODB ERROR: Attribute: \"" <<
              _objContInfo._cats[configIndex].items[ind].itemName << "\" "\
              "not in cat: \"" << _objContInfo._cats[configIndex].catName <<
              "\"" << endl;
#endif
            columnNames.push_back(string());
        }
    }

#ifdef VLAD_REVERSE_ENG
    if (listOut.size() > 1)
        std::cerr << "ODB ERROR: listOut.size() is: " << listOut.size() <<
          " for category: " << _objContInfo._cats[configIndex].catName <<
          " column " << _objContInfo._cats[configIndex].col1 <<
          " and value " << values[0] << endl;
#endif

    for (unsigned int i = 0; i < listOut.size(); ++i)
    {
        for (unsigned int ind = 0; ind < _objContInfo.\
          _cats[configIndex].items.size(); ++ind)
        {
            string cell;
            if (!columnNames[ind].empty())
            {
                cell = (*tbl)(listOut[i], columnNames[ind]);
            }
            combo[ind].push_back(cell);
        }
    }
}


ItemObjCont::ItemObjCont(Serializer& ser, DicFile& dicFile,
  const string& blockName, const string& itemName) :
  ObjCont(ser, dicFile, blockName, itemName, ItemObjContInfo::GetInstance())
{
    GetItemDecendency();
}


ItemObjCont::~ItemObjCont()
{
    _decendency.clear();
}


void ItemObjCont::Build()
{

    for (unsigned int i = 0; i < _objContInfo._cats.size(); ++i)
    {
        if (_objContInfo._cats[i].inheritance)
            BuildItems(_itemsStore[i], i);
        else
            ObjCont::BuildItems(_itemsStore[i], i);
    }

}


void ItemObjCont::GetItemDecendency()
/* -------------------------------------------------------------------------
   GetItemDecendency(): creates and returns a complete Family for the item
   pointed to by blockName, categoryName, and itemKeyword.  The number of
   decendents in the Family is returned in the reference numD.
   ------------------------------------------------------------------------- */
{
    _decendency.clear();

    if (_blockName.empty())
        return;

    Block& block = _dicFile.GetBlock(_blockName);

    ISTable *tbl = block.GetTablePtr(CifString::CIF_DDL_CATEGORY_ITEM_LINKED);
    if(tbl == NULL)
        return;

    vector<string> ColumnNamesCh;
    ColumnNamesCh.push_back(CifString::CIF_DDL_ITEM_CHILD_NAME);

    vector<string> values;
    values.push_back(_id);   

    tbl->SetFlags(CifString::CIF_DDL_ITEM_CHILD_NAME, ISTable::DT_STRING |
      ISTable::CASE_INSENSE);

    vector<unsigned int> listOut;
    tbl->Search(listOut, values, ColumnNamesCh);
    if (listOut.empty())
        return;
  
    vector<unsigned int> parentList = listOut;

    for (unsigned int totalCount = 0; totalCount < parentList.size();
      ++totalCount)
    {
         const string& cell = (*tbl)(parentList[totalCount],
           CifString::CIF_DDL_ITEM_PARENT_NAME);

	 values.clear();
	 values.push_back(cell);

         tbl->Search(listOut, values, ColumnNamesCh);

         for (unsigned int i = 0; i < listOut.size(); ++i)
         {
             parentList.push_back(listOut[i]);
         }
    }

    for (unsigned int i = 0; i < parentList.size(); ++i)
    {
         const string& cell = (*tbl)(parentList[i],
           CifString::CIF_DDL_ITEM_PARENT_NAME);

         _decendency.push_back(cell);
    }
 
}


void ItemObjCont::BuildItems(vector<vector<string> >& combo,
  const unsigned int configIndex)
{
    if (_id.empty() || _blockName.empty())
        return;

    ObjCont::BuildItems(combo, configIndex);

    if (combo[0].empty())
    {
        for (unsigned int i = 0; i < _decendency.size(); i++)
        {
            ObjCont::BuildItems(combo, configIndex, _decendency[i]);
            if (!combo[0].empty())
                break;
        }
    }
}


DictObjCont::DictObjCont(Serializer& ser, DicFile& dicFile,
  const string& blockName) : ObjCont(ser, dicFile, blockName, blockName,
  DictObjContInfo::GetInstance())
{

}


DictObjCont::~DictObjCont()
{
    for (unsigned int itemI = 0; itemI < _items.size(); ++itemI)
    {
        string name = _items.get_name(itemI);
        if (_items.is_read(name))
        {
            ObjCont* objContP = &(_items[itemI]);
            if (objContP != NULL)
            {
                delete (objContP);
            }
        }
    }

    _items.clear();

    for (unsigned int subCatI = 0; subCatI < _subcategories.size(); ++subCatI)
    {
        string name = _subcategories.get_name(subCatI);
        if (_subcategories.is_read(name))
        {
            ObjCont* objContP = &(_subcategories[subCatI]);
            if (objContP != NULL)
            {
                delete (objContP);
            }
        }
    }

    _subcategories.clear();

    for (unsigned int catI = 0; catI < _categories.size(); ++catI)
    {
        string name = _categories.get_name(catI);
        if (_categories.is_read(name))
        {
            ObjCont* objContP = &(_categories[catI]);
            if (objContP != NULL)
            {
                delete (objContP);
            }
        }
    }

    _categories.clear();
}


void DictObjCont::Build()
{
    ObjCont::Build();

    unsigned int index =
      DictObjContInfo::GetInstance().GetItemIndex(
      CifString::CIF_DDL_CATEGORY_CATEGORY,
      CifString::CIF_DDL_ITEM_ID);
    sort(_itemsStore[index][0].begin(), _itemsStore[index][0].end());

    index =
      DictObjContInfo::GetInstance().GetItemIndex(
      CifString::CIF_DDL_CATEGORY_SUB_CATEGORY, CifString::CIF_DDL_ITEM_ID);
    sort(_itemsStore[index][0].begin(), _itemsStore[index][0].end());

    index =
      DictObjContInfo::GetInstance().GetItemIndex(
      CifString::CIF_DDL_CATEGORY_ITEM, CifString::CIF_DDL_ITEM_NAME);
    sort(_itemsStore[index][0].begin(), _itemsStore[index][0].end());
}


UInt32 DictObjCont::Write()
{
    pair<unsigned int, unsigned int> indexPair =
      DictObjContInfo::GetInstance().GetItemIndices(
      CifString::CIF_DDL_CATEGORY_ITEM, CifString::CIF_DDL_ITEM_NAME);

    vector<UInt32> itemsIndices;

    for (unsigned int i = 0; i < _itemsStore[indexPair.first]\
      [indexPair.second].size(); i++)
    {
        ItemObjCont* ilo = new ItemObjCont(_ser, _dicFile, _blockName,
          _itemsStore[indexPair.first][indexPair.second][i]);
        ilo->Build();
        if (_verbose) ilo->Print();
        itemsIndices.push_back(ilo->Write());
        delete ilo;
    }

    indexPair = DictObjContInfo::GetInstance().GetItemIndices(
      CifString::CIF_DDL_CATEGORY_SUB_CATEGORY, CifString::CIF_DDL_ITEM_ID);

    vector<UInt32> subcategoriesIndices;

    for (unsigned int i = 0; i < _itemsStore[indexPair.first]\
      [indexPair.second].size(); i++)
    {
        ObjCont* slo = new ObjCont(_ser, _dicFile, _blockName,
          _itemsStore[indexPair.first][indexPair.second][i],
          SubcatObjContInfo::GetInstance());
        slo->Build();
        if (_verbose) slo->Print();
        subcategoriesIndices.push_back(slo->Write());
        delete slo;
    }

    indexPair = DictObjContInfo::GetInstance().GetItemIndices(
      CifString::CIF_DDL_CATEGORY_CATEGORY, CifString::CIF_DDL_ITEM_ID);

    vector<UInt32> categoriesIndices;

    for (unsigned int i = 0; i < _itemsStore[indexPair.first]\
      [indexPair.second].size(); i++)
    {
        ObjCont* clo = new ObjCont(_ser, _dicFile, _blockName,
          _itemsStore[indexPair.first][indexPair.second][i],
          CatObjContInfo::GetInstance());
        clo->Build();
        if (_verbose) clo->Print();
        categoriesIndices.push_back(clo->Write());
        delete clo;
    }

    _index.push_back(WriteContLocations(itemsIndices));
    _index.push_back(WriteContLocations(subcategoriesIndices));
    _index.push_back(WriteContLocations(categoriesIndices));

    return(ObjCont::Write());
}


void DictObjCont::Read(UInt32 which, unsigned int Index)
{
    // HARDCODED - VLAD - FORMAT DEPENDENT
    ObjCont::Read(which, 3);

    // HARDCODED - VLAD - FORMAT DEPENDENT
    BuildContainers(0, CifString::CIF_DDL_CATEGORY_ITEM,
      CifString::CIF_DDL_ITEM_NAME, _items);
    BuildContainers(1, CifString::CIF_DDL_CATEGORY_SUB_CATEGORY,
      CifString::CIF_DDL_ITEM_ID, _subcategories);
    BuildContainers(2, CifString::CIF_DDL_CATEGORY_CATEGORY,
      CifString::CIF_DDL_ITEM_ID, _categories);
}


const ObjCont& DictObjCont::GetObjCont(const string& contName,
  const ObjContInfo& objContInfo) const
{
    if (objContInfo._objContInfoDescr == "item")
    {
        return(GetContainers(contName, _items, objContInfo));
    }
    else if (objContInfo._objContInfoDescr == "subcategory")
    {
        return(GetContainers(contName, _subcategories, objContInfo));
    }
    else if (objContInfo._objContInfoDescr == "category")
    {
        return(GetContainers(contName, _categories, objContInfo));
    }
    else
    {
        throw NotFoundException("Container type not found",
          "DictObjCont::GetObjCont");
    }

    throw NotFoundException("Container type not found",
      "DictObjCont::GetObjCont");
}


void DictObjCont::Print()
{
    PrintContainers(CifString::CIF_DDL_CATEGORY_CATEGORY,
      CifString::CIF_DDL_ITEM_ID, CatObjContInfo::GetInstance());
    PrintContainers(CifString::CIF_DDL_CATEGORY_SUB_CATEGORY,
      CifString::CIF_DDL_ITEM_ID, SubcatObjContInfo::GetInstance());
    PrintContainers(CifString::CIF_DDL_CATEGORY_ITEM,
      CifString::CIF_DDL_ITEM_NAME, ItemObjContInfo::GetInstance());

    ObjCont::Print();
}


void DictObjCont::PrintContainers(const string& catName,
  const string& itemName, const ObjContInfo& objContInfo)
{
    pair<unsigned int, unsigned int> indexPair =
      DictObjContInfo::GetInstance().GetItemIndices(catName, itemName);

    for (unsigned int i = 0; i < _itemsStore[indexPair.first]\
      [indexPair.second].size(); ++i)
    {
        const ObjCont& objCont = GetObjCont(_itemsStore[indexPair.first]\
          [indexPair.second][i], objContInfo);
        try
        {
            objCont.Print();
        }
        catch (NotFoundException& exc)
        {
            cout << "Failed to load " << objContInfo._objContInfoDescr <<
              " " << _itemsStore[indexPair.first][indexPair.second][i] <<
              endl;
        }
    }
}


UInt32 DictObjCont::WriteContLocations(const vector<UInt32>& indices)
{
    if (indices.empty())
    {
        // If indices vector is empty, it will not be serialized in order
        // to save space in the file. Return of 0 will indicate no-write
        // condition, since no user data is written to index 0.
        return(0);
    }
    else
    {
        return (_ser.WriteUInt32s(indices));
    }
}


void DictObjCont::BuildContainers(unsigned int index,
  const string& catName, const string& itemName,
  mapped_ptr_vector<ObjCont>& containers)
{
    if (_index[index] == 0)
    {
        // Value 0 indicates that nothing was written. Just clear.
        containers.clear();
        return;
    }

    pair<unsigned int, unsigned int> indexPair =
      DictObjContInfo::GetInstance().GetItemIndices(catName, itemName);

    vector<UInt32> ddlContIndices;
    _ser.ReadUInt32s(ddlContIndices, _index[index]);

    containers.push_back(_itemsStore[indexPair.first][indexPair.second],
      ddlContIndices);
}


void DictObjCont::BuildItems(vector<vector<string> >& combo,
  const unsigned int configIndex)
{
    if (_blockName.empty())
    {
        return;
    }

    Block& block = _dicFile.GetBlock(_blockName);

    ISTable* catTableP = block.GetTablePtr(DictObjContInfo::GetInstance().\
      _cats[configIndex].catName);
    if (catTableP == NULL)
    {
        return;
    }

    vector<string> attribsNames;

    for (unsigned int ind = 0; ind < DictObjContInfo::GetInstance().\
      _cats[configIndex].items.size(); ++ind)
    {
        attribsNames.push_back(DictObjContInfo::GetInstance().\
          _cats[configIndex].items[ind].itemName);
    }
  
    for (unsigned int ind = 0; ind < DictObjContInfo::GetInstance().\
      _cats[configIndex].items.size(); ++ind)
    {
        catTableP->GetColumn(combo[ind], attribsNames[ind]);
    }
}


ObjCont& DictObjCont::GetContainers(const string& contName,
  mapped_ptr_vector<ObjCont>& containers, const ObjContInfo& objContInfo) const
{
    unsigned int index = containers.find(contName);
    if (index == containers.size())
    {
        throw NotFoundException("Container \"" + contName + "\" not found",
          "DictObjCont::GetContainers");
    }

    if (containers.is_read(contName))
        return(containers[index]);

    containers.set(new ObjCont(_ser, _dicFile, _blockName,
      contName, objContInfo));

    containers.read(contName);

    return(containers[index]);
}

