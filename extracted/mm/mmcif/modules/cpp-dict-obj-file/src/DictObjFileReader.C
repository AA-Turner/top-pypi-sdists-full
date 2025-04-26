//$$FILE$$
//$$VERSION$$
//$$DATE$$
//$$LICENSE$$


/*!
** \file DictObjFileReader.C
**
** \brief Implementation file for the DictObjFileReader application.
*/


#include <iostream>

#include "DictObjFile.h"
#include "DictObjCont.h"


using std::cout;
using std::cerr;
using std::endl;


int main(int argc, char** argv)
{
    if (argc != 3)
    {
        cerr << "Usage: " << argv[0] << " <object filename> <datablock name>"
          << endl;
        return(0);
    }

    DictObjFile dictObjFile(argv[1]);

    dictObjFile.Read();

    DictObjCont& dictObjCont = dictObjFile.GetDictObjCont(argv[2]);

    cout << "Get the all the dictionaries in one sweep ... " << endl << endl;

    dictObjCont.Print();

    cout << "Done!" << endl;

}

