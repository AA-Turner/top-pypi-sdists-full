//$$FILE$$
//$$VERSION$$
//$$DATE$$
//$$LICENSE$$


/*!
** \file DictObjFileCreator.C
**
** \brief Implementation file for the DictObjFileCreator application.
*/


#include <string.h>
#include <string>
#include <iostream>

#include "DictObjFile.h"
#include "DictObjCont.h"


using std::cout;
using std::cerr;
using std::endl;


void usage(string name)
{
    cerr << "Usage: " << name << endl;
    cerr << "               -dictSdbFile <dictionary SDB filename> (input dictionary file)"
      << endl;
    cerr << "               -o <destination filename> (output object file)" <<
      endl;
    cerr << "               -v  (verbose flag)" << endl;
}


int main(int argc, char** argv)
{
    bool verbose = false;
    const string version = "8.0";
    string dictSdbFileName;
    string outputfile;

    if (argc < 5)
    {
        usage(argv[0]);
        return(1);
    }

    for (int i = 1; i < argc; i++)
    {
        if (argv[i][0] == '-')
        {
            if (!strcmp(argv[i], "-dictSdbFile"))
            {
	        i++;
	        dictSdbFileName = argv[i];
            }
            else if (!strcmp(argv[i], "-o"))
            {
	        i++;
	        outputfile = argv[i];
            }
            else if (!strcmp(argv[i], "-v"))
            {
	        verbose = true;
            }
            else
            {
	        usage(argv[0]);
	        return(1);
            }
        }
        else
        {
            usage(argv[0]);
            return(1);
        }
    }

    if (dictSdbFileName.empty() || outputfile.empty())
    {
        usage(argv[0]);
        return(1);
    }

    cout << endl;
    cout << "DictObjFileCreator Version " << version << endl;
    cout << endl;
    cout << "Dictionary SDB filename: " << dictSdbFileName << endl;
    cout << "Object filename:     " << outputfile << endl;
    cout << endl;

    DictObjFile dictObjFile(outputfile, CREATE_MODE, verbose, dictSdbFileName);

    dictObjFile.Build();

    dictObjFile.Write();
}

