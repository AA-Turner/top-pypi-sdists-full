import sys,shutil,os
sys.path.insert(-2, "D:\\workspace\\spring-initializer\\src")
# from spring_initializer.main import Main
from spring_initializer.__main__ import main
# main = Main()
# 删除测试目录
testDir = "D:\\workspace\\spring-initializer\\tests\\spring_demo"
if os.path.exists(testDir):
    shutil.rmtree(testDir)
# main.generate_spring_project(javaVersion="17",packging="war",removeZip=False)
# main.printHelp()
# main.printVersion()
main()



