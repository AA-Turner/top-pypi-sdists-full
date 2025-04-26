//$$FILE$$
//$$VERSION$$
//$$DATE$$
//$$LICENSE$$


/*!
** \file DictObjFile.C
**
** \brief Implementation file for DictObjFile class.
*/


#include <string>
#include <algorithm>

#include "RcsbFile.h"
#include "ISTable.h"
#include "CifFileUtil.h"
#include "DictObjFile.h"


using std::make_pair;
using std::cout;
using std::endl;
using std::sort;


string OdbFileVersion("V1");


DictObjFile::DictObjFile(const string& persStorFileName,
  const eFileMode fileMode, const bool verbose, const string& dictSdbFileName)
  : _verbose(verbose), _dicFileP(NULL),
  _ser(*(new Serializer(persStorFileName, fileMode, verbose))),
  _currDictObjContP(NULL)
{
    if ((fileMode != READ_MODE) && (fileMode != CREATE_MODE))
    {
        throw FileModeException("Dictionary object file not in read or "\
          "create mode", "DictObjFile::DictObjFile()");
    }

    if (fileMode == READ_MODE)
    {
        if (!dictSdbFileName.empty())
        {
            throw InvalidStateException("Non-empty dictionary file name "\
              "in read mode", "DictObjFile::DictObjFile()");
        }
    }

    if (fileMode == CREATE_MODE)
    {
        if (dictSdbFileName.empty())
        {
            throw EmptyValueException("Empty dictionary file name in "\
              "create mode", "DictObjFile::DictObjFile()");
        }
    }

    _fileMode = fileMode;
    _dictSdbFileName = dictSdbFileName;
}


DictObjFile::~DictObjFile()
{
    _dictSdbFileName.clear();

    delete (_dicFileP);

    delete &(_ser);

    if (!_dictionaries.empty())
    {
      for (unsigned int j = 0; j < _dictionaries.size(); ++j)
      {
        string name = _dictionaries.get_name(j);
        if (_dictionaries.is_read(name))
        {
            DictObjCont* dictObjContP = &(_dictionaries[j]);
            if (dictObjContP != NULL)
            {
                delete (dictObjContP);
            }
        }
      }

      _dictionaries.clear();
    }

}


void DictObjFile::Build()
{
    if (_fileMode != CREATE_MODE)
    {
        throw FileModeException("Dictionary object file not in create mode",
          "DictObjFile::Build()");
    }

    _dicFileP = GetDictFile(NULL, string(), _dictSdbFileName);

    vector<string> dictNames;
    _dicFileP->GetBlockNames(dictNames);

    _dictionaries.push_back(dictNames);
}


void DictObjFile::Write()
{

    if (_fileMode != CREATE_MODE)
    {
        throw FileModeException("Dictionary object file not in create mode",
          "DictObjFile::Write()");
    }

    vector<string> blockNames;
    GetDictionaryNames(blockNames);

    cout << "Number of dictionary datablocks: " << blockNames.size() << endl;

    // Write ODB file version
    // HARDCODED - VLAD - FORMAT DEPENDENT
    _ser.WriteString(OdbFileVersion);
    _ser.WriteUInt32(23);

    sort(blockNames.begin(), blockNames.end());

    vector<UInt32> list;
    for (unsigned int i = 0; i < blockNames.size(); i++)
    {
        DictObjCont* dictObjContP = new DictObjCont(_ser, *_dicFileP,
          blockNames[i]);

        dictObjContP->SetVerbose(_verbose);

        cout << "Building dictionary object: " << blockNames[i] << endl;
        dictObjContP->Build();

        if (_verbose)
        {
            cout << "Printing dictionary object: " << blockNames[i] << endl;
            dictObjContP->Print();
        }

        cout << "Writing dictionary object: " << blockNames[i] << endl;
        UInt32 ret = dictObjContP->Write();

        if (ret > 0)
        {
            list.push_back(ret);
        }
        else
        {
            cout << "Write dictionary object error code  = " << ret << endl;
            list.push_back(0);
        }
        delete dictObjContP;
    }

    UInt32 ret = _ser.WriteUInt32s(list);

    _ser.UpdateUInt32(ret, 1);

    cout << "Last index = " << ret << endl;

    _ser.WriteStrings(blockNames);

    cout << "Return code = " << 0 << endl;

}


void DictObjFile::Read()
{

    if (_fileMode != READ_MODE)
    {
        throw FileModeException("Dictionary object file not in read mode",
          "DictObjFile::Read()");
    }

    string firstString;
    // HARDCODED - VLAD - FORMAT DEPENDENT
    _ser.ReadString(firstString, 0);
    if (firstString != OdbFileVersion)
    {
        throw VersionMismatchException("Cannot read old versions of "\
          "dictionary object file!", "DictObjFile::Read");
    }

    // HARDCODED - VLAD - FORMAT DEPENDENT
    // Location of the dictionary indices in the file.
    UInt32 location = _ser.ReadUInt32(1);

    if (location == 0)
        // VLAD - ERROR HANDLING return BUILD_LIST_ERROR;
        return;

    vector<UInt32> dictIndices;
    _ser.ReadUInt32s(dictIndices, location);

    vector<string> dictNames;
    // HARDCODED - VLAD - FORMAT DEPENDENT
    _ser.ReadStrings(dictNames, location + 1);

    if (dictIndices.size() != dictNames.size())
        return;
        // return BUILD_LIST_ERROR;

    _dictionaries.push_back(dictNames, dictIndices);

}


unsigned int DictObjFile::GetNumDictionaries()
{
    return(_dictionaries.size());
}


void DictObjFile::GetDictionaryNames(vector<string>& dictNames)
{
    dictNames.clear();

    if (!_dictSdbFileName.empty())
    {
        _dicFileP->GetBlockNames(dictNames);
    }
    else
    {
        for (unsigned int index = 0; index < _dictionaries.size(); ++index)
        {
            dictNames.push_back(_dictionaries[index].GetName());
        }
    }
}


DictObjCont& DictObjFile::GetDictObjCont(const string& dictName)
{

    if (_currDictObjContP != NULL)
    {
        if (_currDictObjContP->GetName() == dictName)
        {
            return(*_currDictObjContP);
        }
    }

    unsigned int l = _dictionaries.find(dictName);
    if (l == _dictionaries.size())
    {
        throw NotFoundException("Dictionary \"" + dictName + "\" not found.",
          "DictObjFile::GetDictObjCont");
    }

    if (!_dictionaries.is_read(dictName))
    {
        _dictionaries.set(new DictObjCont(_ser, *_dicFileP, dictName));
        _dictionaries.read(dictName);
    }

    _currDictObjContP = &(_dictionaries[l]);

    return(*_currDictObjContP);

}


void DictObjFile::Print()
{
    for (unsigned int dictI = 0; dictI < _dictionaries.size(); ++dictI)
    {
        DictObjCont& dictObjCont = GetDictObjCont(_dictionaries[dictI].\
          GetName());

        dictObjCont.Print();    
    }
}

