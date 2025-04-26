//$$FILE$$
//$$VERSION$$
//$$DATE$$
//$$LICENSE$$


/*!
** \file DictParentChild.C
**
** \brief Implementation file for DictParentChild class.
*/


#include <string>
#include <vector>
#include <algorithm>

#include "GenString.h"
#include "GenCont.h"
#include "CifString.h"
#include "ISTable.h"
#include "TableFile.h"
#include "DictParentChild.h"


using std::string;
using std::vector;
using std::cout;
using std::endl;
using std::sort;


DictParentChild::DictParentChild(const DictObjCont& dictObjCont,
  DictDataInfo& dictDataInfo) : ParentChild(), _dictObjCont(dictObjCont),
  _dictDataInfo(dictDataInfo)
{
    FillGroupTable(*_groupTableP);
    FillGroupListTable(*_groupListTableP, *_groupTableP);

    // Add one more column to the group table, that will tell the parent
    // category of the group.
    AddParentCategoryToItemLinkedGroup(*_groupTableP, *_groupListTableP);

    // Now create relations
    CreateAllRelations(*_groupTableP, *_groupListTableP);

    // TRACE
    // cout << "Tables" << endl;
    // cout << (*_groupTableP) << endl;
    // cout << (*_groupListTableP) << endl;
}


DictParentChild::~DictParentChild()
{

}


const DictObjCont& DictParentChild::GetDictObjCont()
{
    return (_dictObjCont);
}


void DictParentChild::GetParentCifItems(vector<string>& parCifItems,
  const string& cifItemName)
{
    _dictDataInfo.GetParentCifItems(parCifItems, cifItemName);
}


void DictParentChild::FillGroupTable(ISTable& groupTable)
{
    vector<string> cats = _dictDataInfo.GetCatNames();

    sort(cats.begin(), cats.end());

    for (unsigned int catI = 0; catI < cats.size(); ++catI)
    {
        const vector<string>& linkGroupId = _dictDataInfo.GetCatAttribute(
          cats[catI], CifString::CIF_DDL_CATEGORY_PDBX_ITEM_LINKED_GROUP,
          CifString::CIF_DDL_ITEM_LINK_GROUP_ID);

        const vector<string>& label = _dictDataInfo.GetCatAttribute(
          cats[catI], CifString::CIF_DDL_CATEGORY_PDBX_ITEM_LINKED_GROUP,
          CifString::CIF_DDL_ITEM_LABEL);

        const vector<string>& context = _dictDataInfo.GetCatAttribute(
          cats[catI], CifString::CIF_DDL_CATEGORY_PDBX_ITEM_LINKED_GROUP,
          CifString::CIF_DDL_ITEM_CONTEXT);

        const vector<string>& conditionId = _dictDataInfo.GetCatAttribute(
          cats[catI], CifString::CIF_DDL_CATEGORY_PDBX_ITEM_LINKED_GROUP,
          CifString::CIF_DDL_ITEM_CONDITION_ID);

        for (unsigned int numI = 0; numI < linkGroupId.size(); ++numI)
        {
            vector<string> newGroupRow;
            newGroupRow.push_back(cats[catI]);
            newGroupRow.push_back(linkGroupId[numI]);
            newGroupRow.push_back(label[numI]);
            newGroupRow.push_back(context[numI]);
            newGroupRow.push_back(conditionId[numI]);
            groupTable.AddRow(newGroupRow);
        } // for (every group in category)
    } // for (every category acting as a child)
}


void DictParentChild::FillGroupListTable(ISTable& groupListTable,
  ISTable& groupTable)
{
    vector<string> cats = _dictDataInfo.GetCatNames();

    sort(cats.begin(), cats.end());

    for (unsigned int catI = 0; catI < cats.size(); ++catI)
    {
        const vector<string>& linkGroupId = _dictDataInfo.GetCatAttribute(
          cats[catI], CifString::CIF_DDL_CATEGORY_PDBX_ITEM_LINKED_GROUP,
          CifString::CIF_DDL_ITEM_LINK_GROUP_ID);

        unsigned int nextGroupInt = linkGroupId.size() + 1;

        vector<string> cifItemNames;
        _dictDataInfo.GetCatItemsNames(cifItemNames, cats[catI]);

        for (unsigned int childI = 0; childI < cifItemNames.size(); ++childI)
        {
            const vector<string>& parItemNames =
              _dictDataInfo.GetItemAttribute(cifItemNames[childI],
              CifString::CIF_DDL_CATEGORY_PDBX_ITEM_LINKED_GROUP_LIST,
              CifString::CIF_DDL_ITEM_PARENT_NAME);

            const vector<string>& parCatNames =
              _dictDataInfo.GetItemAttribute(cifItemNames[childI],
              CifString::CIF_DDL_CATEGORY_PDBX_ITEM_LINKED_GROUP_LIST,
              CifString::CIF_DDL_ITEM_PARENT_CATEGORY_ID);

            const vector<string>& linkGroupId =
              _dictDataInfo.GetItemAttribute(cifItemNames[childI],
              CifString::CIF_DDL_CATEGORY_PDBX_ITEM_LINKED_GROUP_LIST,
              CifString::CIF_DDL_ITEM_LINK_GROUP_ID);

            for (unsigned int parI = 0; parI < parItemNames.size(); ++parI)
            {
                if (!_dictDataInfo.IsItemDefined(parItemNames[parI]))
                {
                    cout << "Warning: Child category \"" << cats[catI] <<
                      "\", child item \"" << cifItemNames[childI] <<
                      "\", link group \"" << linkGroupId[parI] <<
                      "\" is associated with non-defined parent item \"" <<
                      parItemNames[parI] << "\" and this entry will be "\
                      "ignored and not stored in \"" <<
                      groupListTable.GetName() << "\" table." << endl;
                    continue;
                }

                vector<string> row;

                row.push_back(cats[catI]);

                const string& linkGroup = linkGroupId[parI];
                row.push_back(linkGroup);

                row.push_back(cifItemNames[childI]);

                row.push_back(parItemNames[parI]);
      
                row.push_back(parCatNames[parI]);

                groupListTable.AddRow(row);
            } // for (every row where child CIF item is present)
        } // for (all child items)

        vector<string> childSearchCol;
        childSearchCol.push_back("child_name");

        for (unsigned int childI = 0; childI < cifItemNames.size(); ++childI)
        {
            // Check if item has already been processed
            vector<string> childTarget;
            childTarget.push_back(cifItemNames[childI]);

            unsigned int childRow = groupListTable.FindFirst(childTarget,
              childSearchCol);

            if (childRow != groupListTable.GetNumRows())
            {
                continue;
            }

            const vector<string>& parCifItems =
              _dictDataInfo.GetItemAttribute(cifItemNames[childI],
              CifString::CIF_DDL_CATEGORY_ITEM_LINKED,
              CifString::CIF_DDL_ITEM_PARENT_NAME);

            for (unsigned int parI = 0; parI < parCifItems.size(); ++parI,
              ++nextGroupInt)
            {
                const string& parentItem = parCifItems[parI];

                string parCatName;
                CifString::GetCategoryFromCifItem(parCatName, parentItem);

                if (!_dictDataInfo.IsCatDefined(parCatName))
                {
                    cout << "Warning: Child item \"" << cifItemNames[childI] <<
                      "\" is associated, via item_linked, with non-defined "\
                      "parent item \"" << parentItem <<
                      "\" and this entry will be ignored." << endl;
                    continue;
                }

                cout << "Info: Creating a new group \"" <<
                  String::IntToString(nextGroupInt) << "\" for child "\
                  "category \"" << cats[catI] << "\" for child item \"" <<
                  cifItemNames[childI] << "\" and parent item \"" <<
                  parentItem << "\", from \"item_linked\" table, as these "\
                  "are not defined in group tables." << endl;

                vector<string> row;

                row.push_back(cats[catI]);

                row.push_back(String::IntToString(nextGroupInt));

                row.push_back(cifItemNames[childI]);

                row.push_back(parentItem);
  
                row.push_back(parCatName);

                groupListTable.AddRow(row);

                vector<string> newGroupRow;
                newGroupRow.push_back(cats[catI]);
                newGroupRow.push_back(String::IntToString(nextGroupInt));
                newGroupRow.push_back(cats[catI] + ":" + parCatName + ":" +
                  String::IntToString(nextGroupInt));
                newGroupRow.push_back(CifString::InapplicableValue);
                newGroupRow.push_back(CifString::InapplicableValue);
                groupTable.AddRow(newGroupRow);
            }
        } // for (all child items)
    }
}

