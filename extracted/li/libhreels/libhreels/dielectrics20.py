# Testing dielectric models and their surface loss function
import matplotlib.pyplot as plt
import numpy as np
from scipy import constants
from scipy.integrate import cumulative_trapezoid

def plasmaFrequency(n,eps_inf=1, m=1): 
    # Returns the plasma frequency in cm^-1 for a given charge carrier density n in e/m³
    # and a polarisable medium described by eps_infinity 
    # and a band mass m in units of electron mass in vacuum.
    eps_0 = constants.value("vacuum electric permittivity")
    e = constants.value('elementary charge')
    m_e = constants.value('electron mass')
    # Careful: There is a factor of 2 pi between omega and nue:
    # If the plasma oscillates in a polarisable medium eps_infinity will reduce the restoring fields
    w_P = np.sqrt(n*e*e/(eps_0*eps_inf*m_e*m))        #
    nue_P = w_P /1E+12 * 33.35641 /2 /np.pi   #Hz -> THz -> cm^-1
    return nue_P        # in units of cm-1

def chargeDensitySTO(x):
    # Calculates the charge density per m^3 for SrTi_(1-x)Nb_xO_3 
    # assuming doping by one electron per Nb atom 
    vol = 3.91*3.91*3.91 * 1E-30    # unit cell volume in m^3 
    return x/vol
    
def plasmaFrequencySTO(x,eps_inf=5.14,m=15):
    # Calculates the plasma frequency in cm^-1 for SrTi_(1-x)Nb_xO_3 
    # assuming doping by one electron per Nb atom 
    # and an effective mass m=15
    vol = 3.91*3.91*3.91 * 1E-30    # unit cell volume in m^3 
    return plasmaFrequency(x/vol,eps_inf, m=m)
    

def loss(eps):
    '''Returns the loss function for a given eps'''
    return np.imag(-1/eps) 

def surfaceLoss(eps):
    '''Returns the surface loss function for a given eps'''
    return np.imag(-1/(1+eps)) #HHE changed former sign, according to Phd of FSc

def reflectivity(eps):  # IR reflectivity
    '''Returns the reflectivity for a given eps'''
    sq = np.sqrt(eps)
    a = np.abs((sq-1)/(sq+1))
    return a*a

def sigma(eps,w):       
    '''Returns the complex conductivity for a given eps'''
    return (eps-1)*w/1j

def int_sigma(eps,w):       
    from scipy.integrate import cumulative_trapezoid
    '''Cumulatively integrates the optical conductivity for a given eps'''
    # Note that one value less is returned than the number of w values.
    # The following factor depends on the unit cell volume:
    fac = 0.67e-06
    xx = w
    return fac*cumulative_trapezoid(np.real(sigma(eps,w)), x=xx)

def plotDielectrics(x,eps, title=" ", plot_show=True):
    '''This method plots a given (x,eps)-dataset as Re/Im(eps), SurfaceLoss and Reflectivity 
    '''
    fig, axs = plt.subplots(3, 1, sharex=True)
    fig.suptitle(str(title), fontsize=16)
    axs[0].plot(x, np.imag(eps), label='Im( $\epsilon (\omega )$ )')
    axs[0].plot(x, np.real(eps), label='Re( $\epsilon (\omega )$ )')
    axs[0].legend()
    axs[0].set_ylabel('Dielectric Function')

    axs[1].plot(x, surfaceLoss(eps), linestyle='-', label='Loss function')    
    axs[1].set_ylabel('Surface Loss Function')
    axs[1].set_ylim([-0.10,None])

    axs[2].plot(x, reflectivity(eps))
    axs[2].set_ylabel('Reflectivity')
    axs[2].set_xlabel('Frequency')
    axs[2].set_ylim([0.0,1])
    axs[0].set_xlim(left=0, right=max(x))

    if plot_show==True:
        plt.show()

class oscillator:
    '''This defines epsilon of an oscillator with a given (wTO, gTO, wLO, gLO)
    '''
    def __init__(self, wTO=177., gTO=20., wLO=184., gLO=20.):
        self.wTO = wTO
        self.wLO = wLO
        self.gammaTO = gTO
        self.gammaLO = gLO

    def eps(self,w):
        nom = self.wLO*self.wLO - w*w - 1j*w*self.gammaLO   #sign changed according to gervais paper, formular 2 -> neg im(eps), therefore changed back to lambins kurosawa
        denom = self.wTO*self.wTO - w*w - 1j*w*self.gammaTO #sign changed according to gervais paper, formular 2 -> neg im(eps), therefore changed back to lambins kurosawa
        return nom/denom

    def __call__(self, w):
        return self.eps(w)

class drude:
    '''This defines an additive Drude component to a dielectric function: 
    eps_drude = drude2(omega_p, gamma_p, gamma_0)
    ... eps(omega) + eps_drude(omega)
    '''
    def __init__(self, omega_p, gamma_p, gamma_0):

        self.omega_p = omega_p
        self.gamma_p = gamma_p
        self.gamma_0 = gamma_0

        #print("called drude with w_P, g_P, g_0:", omega_p, gamma_p, gamma_0)
        

    def eps(self,w):
        newW = np.where(w==0, 0.000567894, w)   # Avoid zeros to avoid devision by zero 
        w = newW
        #print("Drude (x,y): ", w, -((self.omega_p**2 + 1j*w*(self.gamma_0-self.gamma_p))/(w*w + 1j*w*self.gamma_0)))

        nom = self.omega_p**2 + 1j*w*(self.gamma_0-self.gamma_p)
        denom = w*w + 1j*w*self.gamma_0 #sign changed according to Lambin notation

        return -(nom/denom) #HHE changed 

    def __call__(self, w):
        return self.eps(w)

    
class cole_davidson:
    '''This defines an additive Cole-Davidson component to a dielectric function: 
    eps_cole_davidson = cole_davidson(omega_p, gamma_p, gamma_0)
    ... eps(omega) + eps_drude(omega)
    '''
    def __init__(self, omega_p, gamma_p, gamma_0, beta):

        self.omega_p = omega_p
        self.gamma_p = gamma_p
        self.gamma_0 = gamma_0
        self.beta = beta

        #print("called coledavidson with w_P, g_P, g_0, beta:", omega_p, gamma_p, gamma_0, beta)
    

    def eps(self,w):
        newW = np.where(w==0, 0.000567894, w)   # Avoid zeros to avoid devision by zero 
        w = newW
        #print("Drude (x,y): ", w, -((self.omega_p**2 + 1j*w*(self.gamma_0-self.gamma_p))/(w*w + 1j*w*self.gamma_0)))
        #return -((self.omega_p**2 + 1j*w*(self.gamma_0-self.gamma_p))/(w*w + 1j*w*self.gamma_0)) #HHE changed 
        
        #nom = self.omega_p**2 + 1j*w*(self.gamma_0-self.gamma_p) #very simple approach by just putting an exponent to denominator (works only for gamma_0=gamma_P)
        #denom = (w*w - 1j*w*self.gamma_0)**self.beta  #sign changed according to gervais paper, formular 7

        hilf = 1j * w * self.gamma_0 * (1-1j*w*(1/self.gamma_0))**(self.beta)

        nom = self.omega_p**2 - 1j*w*(self.gamma_p) - w*w + hilf #unfortunately also the nominator changes due to cole-davidson
        denom = hilf   #sign changed according to gervais paper, formular 7 -> did not match, changed back to lambin formularism


        return -(nom/denom)

    def __call__(self, w):
        return self.eps(w)

class cole_cole:
    '''This defines an additive Cole-Davidson component to a dielectric function: 
    eps_cole_cole = cole_cole(omega_p, gamma_p, gamma_0, beta)
    ... 
    '''
    def __init__(self, omega_p, gamma_p, gamma_0, beta):

        self.omega_p = omega_p
        self.gamma_p = gamma_p
        self.gamma_0 = gamma_0
        self.beta = beta

        #print("called colecole with w_P, g_P, g_0, beta:", omega_p, gamma_p, gamma_0, beta)

    def eps(self,w):
        newW = np.where(w==0, 0.000567894, w)   # Avoid zeros to avoid devision by zero 
        w = newW
        #nom = self.omega_p**2 + 1j*w*(self.gamma_0-self.gamma_p) #very simple approach by just putting an exponent to denominator (works only for gamma_0=gamma_P)
        #denom = w*w + w*(1j*self.gamma_0)**self.beta

        hilf = 1j**(self.beta+1) * w**(self.beta+1) * self.gamma_0**(1-self.beta)

        nom = self.omega_p**2 + 1j*w*(self.gamma_0-self.gamma_p) - w*w - hilf #unfortunately also the nominator changes due to cole-cole 
        denom = 1j*w*(self.gamma_0) - hilf   #sign changed according to lambin formularism

        return -(nom/denom)

    def __call__(self, w):
        return self.eps(w)


class simpleOscillator(oscillator):
    '''This defines epsilon of an oscillator with a given (wPl, Q and gTO)
    '''
    def __init__(self, wPl, Q, gTO=20):
        self.wPl = wPl
        self.Q = Q
        self.gammaTO = gTO

    def eps(self,w):
        nom = self.wPl*self.wPl*self.Q
        denom = self.wPl*self.wPl - w*w - 1j*self.gammaTO*w #HHE changed, wrong sign of Im
        return nom/denom

class simpleDrude:
    '''This defines epsilon of an oscillator with a given (wPl, gamma). gamma = gammaTO = gammaLO
    '''
    def __init__(self, wPL, gamma):
        self.wPL = wPL
        self.gamma = gamma

    def eps(self,w):
        return -(self.wPL*self.wPL)/(w*w-1j*w*self.gamma) #HHE changed 

    def __call__(self, w):
        return self.eps(w)



def myMain():
    # BaTiO3
    simple_data = [
        [178.6, 8.02, 3.09800E-02],
        [270.6, 24.00, 10.0800E-02],
        [522.9, 1.20, 6.97200E-02]]

    data = [
        [177.4 , 1.9262 , 184.003 , 9.718],
        [272.84 , 93.3091 , 470.972 ,  14.31 ],
        [506.379 , 42.60 , 739.651 , 33.044],
    ]  
        
    x = np.linspace(0,1000,num=1200)
    epsInfinity = 5.25

    simpleoscis = [simpleOscillator(TO, Q, f*TO) for (TO, Q, f) in simple_data]
    eps = epsInfinity
    for each in simpleoscis:
        eps += each(x) #sum
    plotDielectrics(x, eps, title="Eps of BaTiO calced with simpleOscillator", plot_show=False)

    oscis = [oscillator(wTO=a, wLO=c, gTO=b, gLO=d) for (a, b, c, d) in data]
    eps2 = epsInfinity
    for each in oscis:
        eps2 *= each(x) #kurosawa
    plotDielectrics(x, eps2, title="Eps of BaTiO calced with oscillator", plot_show=False)

    plt.show()

if __name__ == '__main__':
    myMain()
