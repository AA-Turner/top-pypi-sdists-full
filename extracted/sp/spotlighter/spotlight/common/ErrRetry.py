#에러가 발생하면 반복하는 Decorator
class ErrRetry:
    def __init__(self,func):
        self.func = func
    def __call__(self,*arg,**kwarg):
        while True:
            try:
                return self.func(self, *arg, **kwarg)
            except Exception as e:
                print(e)
                input("RETRY>")        

        # return self.func(*arg, **kwarg) # TO DEBUG

def ErrRetryF(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(e)
    return wrapper

@ErrRetry
def Test():
    print("a")

