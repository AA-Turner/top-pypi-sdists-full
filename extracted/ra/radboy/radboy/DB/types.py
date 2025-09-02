from decimal import Decimal as TDecimal,getcontext
import string,random
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
            
