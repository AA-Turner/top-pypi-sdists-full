import getopt
import sys
import os
from .main import Main


def getOptionVal(options, key):
    for optKey, optVal in options:
        if optKey == key:
            return optVal
    return None


def main():
    try:
        opts, args = getopt.gnu_getopt(
            sys.argv[1:],
            "hvd:j:t:p:D:k:P",
            [
                "help",
                "version",
                "dir=",
                "java=",
                "type=",
                "packging=",
                "dependencies=",
                "keepZip",
                "packageName"
            ],
        )
    except getopt.GetoptError as e:
        print("获取参数信息出错，错误提示：", e.msg)
        exit()
    mainProcess = Main()
    params: dict = {}
    if len(opts) == 0:
        mainProcess.generate_spring_project()
        return
    else:
        for opt in opts:
            argKey = opt[0]
            argVal = opt[1]
            if argKey == "--help" or argKey == "-h":
                mainProcess.printHelp()
                return
            elif argKey == "--version" or argKey == "-v":
                mainProcess.printVersion()
                return
            elif argKey == "--dir" or argKey == "-d":
                params["dirName"] = argVal
            elif argKey == "--java" or argKey == "-j":
                params["javaVersion"] = argVal
            elif argKey == "--type" or argKey == "-t":
                params["type"] = argVal
            elif argKey == "--packging" or argKey == "-p":
                params["packging"] = argVal
            elif argKey == "--dependencies" or argKey == "-D":
                params["dependencies"] = argVal
            elif argKey == "--keepZip" or argKey == "-k":
                params["removeZip"] = False
            elif argKey == "--packageName" or argKey == "-P":
                params["packageName"] = argVal
            else:
                pass
        mainProcess.generate_spring_project(**params)
        return


if __name__ == "__main__":
    main()
