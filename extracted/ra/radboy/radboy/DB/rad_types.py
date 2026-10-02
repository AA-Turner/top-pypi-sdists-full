from decimal import Decimal as TDecimal,getcontext
import string,random,re
from colored import Fore,Back,Style

def index_inList(x,b):
    return (x <= -1 and x in list(range(-1,-(len(b)+1),-1))) or (x >= 0 and\
 x in range((len(b))))

class decc(TDecimal):
    ''' defines a decimal of 'cf\''''
    def __new__(self,value,cf=3):
        '''you can set the floating precision of a value in curly braces {value:.3f} by doing {value:{three}f} where three is he variable containting the value 3
        used for precision
        
        value=1.234
        cf=2
        result=1.23
        for the below assignment.

        value=f"{value:.{cf}f}"
        print(value)
        '''
        #print(value,type(value))
        if isinstance(value,str):
            scientific=re.findall(r'[-+]?[0-9]+\.?[0-9]*[Ee](?:\ *[-+]?\ *[0-9]+)?',value)
            if len(scientific) < 1:
                try:
                    whole,part=value.split(".")
                except Exception as e:
                    whole,part=value,"0"*cf
                if len(part) > cf:
                    part=part[:cf-1]
                    value=f"{whole}.{part}"
                    #print(value)
            else:
                pass
            
        else:
            value=f"{value:.{cf}f}"
        return super().__new__(self,value)

class dec3(TDecimal):
    ''' defines a decimal of .3f'''
    def __new__(self,value):
        value=f"{value:.3f}"
        return super().__new__(self,value)

class dec2(TDecimal):
    ''' defines a decimal of .2f'''
    def __new__(self,value):
        value=f"{value:.3f}"
        return super().__new__(self,value)

class dec1(TDecimal):
    ''' defines a decimal of .1f'''
    def __new__(self,value):
        value=f"{value:.3f}"
        return super().__new__(self,value)

def chunker(l,size):
    return [l[i:i+size] for i in range(0,len(l),int(size))]

class stre(str):
    '''String Extended to include operators for some useful functionality.'''
    def __invert__(self):
        '''Generate a 512 Hex Digest for self'''
        hl=hashlib.sha512()
        hl.update(self.encode())
        return str(hl.hexdigest())

    def __sub__(self,other):
        '''remove this many characters from the string, where a positive removes from the right and a negative removes from the left'''
        if isinstance(other,int) or isinstance(other,float):
            #print(other<0)
            if other < 0:
                return self[:other]
            elif other > 0:
                m=[self[i:i+1] for i in range(0,len(self),int(1))]
                for i in range(0,other):
                    popped=m.pop(0)
                return ''.join(m)
        else:
            raise NotImplemented

    def __truediv__(self,other):
        '''return a list broken into chunks of other'''
        if isinstance(other,int) or isinstance(other,float):
            return [self[i:i+other] for i in range(0,len(self),int(other))]
        else:
            raise NotImplemented

    def __mod__(self,other):
        #return the number of chunks
        if isinstance(other,int) or isinstance(other,float):

            return len([self[i:i+other] for i in range(0,len(self),int(other))])
        else:
            raise NotImplemented

    def __floordiv__(self,other):
        '''reverse of __truediv__'''
        if isinstance(other,int) or isinstance(other,float):

            return [ii for ii in reversed([self[i:i+other] for i in range(0,len(self),int(other))])]

        else:
            raise NotImplemented

    def __pow__(self,other):
        '''generate a random string from self of length other.'''

        if isinstance(other,int) or isinstance(other,float):

            src=[self[i:i+1] for i in range(0,len(self),int(1))]
            end=''.join(random.choices(src,k=int(abs(other))))[:int(abs(other))]
            while (len(end) < other) or (len(end) > other):
                end=''.join(random.choices(src,k=int(abs(other))))[:int(abs(other))]
            return end
        else:
            raise NotImplemented
            
def std_colorize(m,n,c,start=f'',end=''):
    #start=f"[Prompt]{Back.black}{Fore.pale_turquoise_1} Start {'*'*(os.get_terminal_size().columns-(len(Fore.pale_turquoise_1)+(len(Fore.grey_27)*2)+len(Style.reset)))}{Style.reset}\n",end=f"\n{Back.black}{Fore.dark_red_1}{'-'*(os.get_terminal_size().columns-(len(Fore.dark_red_1)+(len(Fore.grey_50)*2)+len(Style.reset)))} Stop {Style.reset}"):
        if ((n % 2) != 0) and n > 0:
            msg=f'{start}{Fore.cyan}i{n}/{Fore.light_yellow}L{n+1}{Fore.light_red} of {c}T {Fore.dark_goldenrod}{m}{Style.reset}{end}'
        else:
            msg=f'{start}{Fore.light_cyan}i{n}/{Fore.green_yellow}L{n+1}{Fore.orange_red_1} of {c}T {Fore.light_salmon_1}{m}{Style.reset}{end}'
        return msg
