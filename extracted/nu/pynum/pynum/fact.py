class factorial:
    def find_fact(self,n):
        res = 1
        if n < 0:
            return -1

        elif n == 0:
            return 1
        else:
            for i in range(1,n+1):
                res = res*i
        return res
