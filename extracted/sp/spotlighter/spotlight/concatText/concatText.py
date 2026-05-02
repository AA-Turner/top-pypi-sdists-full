# 231213 : 하위폴더 순환하도록 구현
# 231213 : 마지막에 LF를 포함하지 않는 경우 강제로 추가하여 개행하도록 수정

# 전역선언부
import os
import glob
import tqdm
import spotlight.common.myFileDialog as myfd

# 함수부
class ConcatText:
    liTgt:list    
    filenameNew:str
    encodingOld:str
    encodingNew:str
    bHeader:bool

    def run(cls): #HANDLER        
        cls.getFiles()
        cls.filenameNew = input("new file name(result.txt)>>") or 'result.txt'                
        cls.encodingOld = input("encodingOld(cp949)>>") or 'cp949'
        cls.encodingNew = input("encodingNew(utf8)>>") or 'utf8'

        flag = input("헤더가 포함되어 있습니까?(기본값 Y). Y인 경우 첫번째 파일만 포함함)>>") or 'Y'
        if flag == 'Y': cls.bHeader = True
        else: cls.bHeader = False

        cls.concat(cls.bHeader)
        print("DONE")

    #231213: 하위폴더 순환하도록 변경
    def getFiles(cls, msg:str = "합칠 텍스트 파일이 있는 경로명(하위폴더 포함)"): 
        path = myfd.askdirectory(msg)        
        ext = input("확장자(tsv)>>") or 'tsv'        
        strContain = input("특정 문자열을 포함하는 파일만 포함하고자 하는 경우 입력하세요.(기본값 None. None인 경우 모두 포함함)>>") or None #포함할 문자열
        #cls.liTgt = glob.glob(path + '/*.'+ext)    #result.txt 생성 앞에 해야함
        cls.liTgt = []
        for dirpath, dirname, filenames in os.walk(path):
            for file in filenames:
                path = "%s/%s"%(dirpath,file)
                path = path.replace('\\','/').replace('//','/')

                if strContain != None:
                    if (path.split(".")[-1] == ext) and (strContain in path): cls.liTgt.append(path)
                elif strContain == None:
                    if path.split(".")[-1] == ext: cls.liTgt.append(path)

    def concat(cls, bHeader:bool): #bHeader가 True면 헤더 포함
        # 합산파일 생성
        fileNew = open(cls.filenameNew,'wt', encoding=cls.encodingNew)
        fileNew.close()

        # 파일 하나씩 append        
        fileNew = open(cls.filenameNew,'at', encoding=cls.encodingNew)        
        print("총",len(cls.liTgt),"개")
        pbar = tqdm.tqdm(total=len(cls.liTgt) , desc="순환")
        totalj = 0
        i = 0 #i = File
        for file in cls.liTgt:    
            bContainLF = cls.checkLF(file, cls.encodingOld) #파일을 열 때, 해당 파일 마지막에 LF를 포함하는지 확인한다.           

            j = 0 #j = Line           
            fileOld = open(file, 'rt', encoding=cls.encodingOld)
            for line in fileOld:                
                if bHeader and i!=0 and j==0: pass #헤더가 True이고, 첫번째 파일이 아닌 다른 파일인 경우, 첫번째 줄이면 생략함
                else: tmp = fileNew.write(line) #to speed up, set return
                j+=1
                
            fileOld.close(); i+=1
            if not bContainLF: fileNew.write('\n'); print("ADDED LF AFTER :", file) #when not contain LF, add LR (NOT CRLF)
            totalj += j
            msg = str(file)+":"+str(totalj)
            pbar.desc = msg; pbar.update(1) #pbar update

        fileNew.close()
        pbar.close()

    def checkLF(self, filename:str, encoding:str) -> bool:
        f = open(filename, mode='rb')
        f.seek(-1, os.SEEK_END)
        tmp = f.read(1) #read 1 byte)
        f.close()

        return str(tmp, encoding=encoding) == '\n' #마지막 Byte가 LF인지를 확인하여 반환         

def runConcatText():
    ConcatText().run()

if(__name__ == "__main__"):
    runConcatText()