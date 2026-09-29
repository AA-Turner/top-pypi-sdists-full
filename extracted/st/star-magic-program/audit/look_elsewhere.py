"""Look-elsewhere density for UQFF primitive-combination formulas.
Enumerate products of primitives with small integer exponents (|e|<=2 per primitive,
<=3 primitives with non-zero exponent, optional prefactor 1,2,1/2,pi,4pi,sqrt) and count
how densely the resulting numbers cover the dimensionless line (per decade).
Then: for random dimensionless targets in [1e-3,1e3], what fraction land within 0.5/1/2/5%?"""
import itertools, math, random
P = {'D_PHYS':4,'SO_5':10,'D_CRIT':26,'D_BSFG':6,'A_5':60,'BETA_I':0.6029,'F_TRZ':0.1,'SSQ':0.57,
     'K_MEX':25/12,'PHI_RES':5/6,'PHI_RES_R':0.84}
names=list(P); vals=[P[n] for n in names]
pref={'1':1,'2':2,'1/2':0.5,'pi':math.pi,'4pi':4*math.pi,'sqrt2':2**0.5,'e':math.e,'3':3,'1/3':1/3}
exps=[-2,-1,0,1,2]
S=set(); forms=[]
# combinations of up to 3 primitives with non-zero exponent
for k in (1,2,3):
    for idx in itertools.combinations(range(len(names)),k):
        for es in itertools.product([-2,-1,1,2],repeat=k):
            v=1.0
            for i,e in zip(idx,es): v*=vals[i]**e
            for pn,pv in pref.items():
                x=pv*v
                for root in (1,0.5):   # allow a sqrt of the whole thing
                    y=x**root
                    S.add(round(math.log10(y),6)); forms.append(y)
                # also sums of two terms are common (a + b) -- skip: keep conservative
vals_sorted=sorted(set(forms))
n=len(vals_sorted); print('distinct expressions:',n)
import bisect
def frac_within(tol,N=20000,lo=-3,hi=3):
    random.seed(1); hit=0
    for _ in range(N):
        t=10**random.uniform(lo,hi)
        i=bisect.bisect_left(vals_sorted,t)
        best=min(abs(vals_sorted[j]/t-1) for j in (i-1,i) if 0<=j<n)
        hit+= best<=tol
    return hit/N
for tol in (0.001,0.005,0.01,0.02,0.05):
    print(f'within {tol*100:.1f}%: {frac_within(tol)*100:.1f}% of random targets in [1e-3,1e3]')
# density per decade in [0.1,100]
dec=[v for v in vals_sorted if 0.1<=v<=100]; print('expressions per decade in [0.1,100]:',len(dec)/3)
# restricted vocabulary: no prefactors, <=2 primitives, |e|<=1 (the 'natural' UQFF family)
S2=set()
for k in (1,2,3):
    for idx in itertools.combinations(range(len(names)),k):
        for es in itertools.product([-1,1],repeat=k):
            v=1.0
            for i,e in zip(idx,es): v*=vals[i]**e
            S2.add(v)
S2=sorted(S2); n2=len(S2); print('restricted vocabulary (<=3 primitives, exp +-1, no prefactor):',n2)
def frac2(tol,N=20000):
    random.seed(2); hit=0
    for _ in range(N):
        t=10**random.uniform(-2,2)
        i=bisect.bisect_left(S2,t)
        best=min(abs(S2[j]/t-1) for j in (i-1,i) if 0<=j<n2)
        hit+= best<=tol
    return hit/N
for tol in (0.005,0.01,0.02,0.05):
    print(f'  restricted, within {tol*100:.1f}%: {frac2(tol)*100:.1f}% of random targets in [1e-2,1e2]')
