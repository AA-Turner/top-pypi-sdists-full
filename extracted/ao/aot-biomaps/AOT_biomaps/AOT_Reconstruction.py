import subprocess
import os
import numpy as np
from abc import ABC, abstractmethod
import enum
import AOT_biomaps
import matplotlib.pyplot as plt
from tqdm import trange
from .config import config
import matplotlib.animation as animation
from IPython.display import HTML
import sys
from datetime import datetime
from tempfile import gettempdir
from sklearn.metrics import mean_squared_error
from skimage.metrics import structural_similarity as ssim
if config.get_process()  == 'gpu':
    import torch
    try:
        from torch_scatter import scatter
        from torch_sparse import coalesce
    except ImportError:
        raise ImportError("torch_scatter and torch_sparse are required for GPU processing. Please install them using 'pip install torch-scatter torch-sparse' with correct link (follow instructions https://github.com/LucasDuclos/AcoustoOpticTomography/edit/main/README.md).")
from numba import njit, prange
import numba
from .AOT_Experiment import *
from .AOT_Optic import *
from .AOT_Acoustic import *
import warnings

class ReconType(enum.Enum):
    """
    Enum for different reconstruction types.

    Selection of reconstruction types:
    - Analytic: A reconstruction method based on analytical solutions.
    - Algebraic: A reconstruction method using algebraic techniques.
    - Algebraic: A reconstruction method that Algebraicly refines the solution.
    - Bayesian: A reconstruction method based on Bayesian statistical approaches.
    - DeepLearning: A reconstruction method utilizing deep learning algorithms.
    """

    Analytic = 'analytic'
    """A reconstruction method based on analytical solutions."""
    Algebraic = 'algebraic'
    """A reconstruction method that Algebraicly refines the solution."""
    Bayesian = 'bayesian'
    """A reconstruction method based on Bayesian statistical approaches."""
    DeepLearning = 'deep_learning'
    """A reconstruction method utilizing deep learning algorithms."""

class AnalyticType(enum.Enum):
    iFOURIER = 'iFOURIER'
    """
    This analytic reconstruction type uses the inverse Fourier transform to reconstruct the image.
    It is suitable for data that can be represented in the frequency domain.
    It is typically used for data that has been transformed into the frequency domain, such as in Fourier optics.
    It is not suitable for data that has not been transformed into the frequency domain.
    """
    iRADON = 'iRADON'
    """
    This analytic reconstruction type uses the inverse Radon transform to reconstruct the image.
    It is suitable for data that has been transformed into the Radon domain, such as in computed tomography (CT).
    It is typically used for data that has been transformed into the Radon domain, such as in CT.
    It is not suitable for data that has not been transformed into the Radon domain.
    """

class AlgebraicType(enum.Enum):
    MLEM = 'MLEM'
    """
    This optimizer is the standard MLEM (for Maximum Likelihood Expectation Maximization).
    It is numerically implemented in the multiplicative form (as opposed to the gradient form).
    It truncates negative data to 0 to satisfy the positivity constraint.
    If subsets are used, it naturally becomes the OSEM optimizer.

    With transmission data, the log-converted pre-corrected data are used as in J. Nuyts et al:
    "Algebraic reconstruction for helical CT: a simulation study", Phys. Med. Biol., vol. 43, pp. 729-737, 1998.

    The following options can be used (in this particular order when provided as a list):
    - Initial image value: Sets the uniform voxel value for the initial image.
    - Denominator threshold: Sets the threshold of the data space denominator under which the ratio is set to 1.
    - Minimum image update: Sets the minimum of the image update factor under which it stays constant.
      (0 or a negative value means no minimum, thus allowing a 0 update).
    - Maximum image update: Sets the maximum of the image update factor over which it stays constant.
      (0 or a negative value means no maximum).

    This optimizer is compatible with both histogram and list-mode data.
    This optimizer is compatible with both emission and transmission data.
    """
    MLTR = 'MLTR'
    """
    This optimizer is a version of the MLTR algorithm implemented from equation 16 of the paper from K. Van Slambrouck and J. Nuyts:
    "Reconstruction scheme for accelerated maximum likelihood reconstruction: the patchwork structure",
    IEEE Trans. Nucl. Sci., vol. 61, pp. 173-81, 2014.

    An additional empiric relaxation factor has been added onto the additive update. Its value for the first and last updates
    can be parameterized. Its value for all updates in between is computed linearly from these first and last provided values.

    Subsets can be used.

    Options (in order when provided as a list):
    - Initial image value: Sets the uniform voxel value for the initial image.
    - Alpha ratio: Sets the ratio between exterior and interior of the cylindrical FOV alpha values (0 value means 0 inside exterior).
    - Initial relaxation factor: Sets the empiric multiplicative factor on the additive update used at the first update.
    - Final relaxation factor: Sets the empiric multiplicative factor on the additive update used at the last update.
    - Non-negativity constraint: 0 if no constraint or 1 to apply the constraint during the image update.

    This optimizer is only compatible with histogram data and transmission data.
    """

    NEGML = 'NEGML'
    """
    This optimizer is the NEGML algorithm from K. Van Slambrouck et al, IEEE TMI, Jan 2015, vol. 34, pp. 126-136.

    Subsets can be used. This implementation only considers the psi parameter, but not the alpha image design parameter,
    which is supposed to be 1 for all voxels. It implements equation 17 of the reference paper.

    This algorithm allows for negative image values.

    Options (in order when provided as a list):
    - Initial image value: Sets the uniform voxel value for the initial image.
    - Psi: Sets the psi parameter that sets the transition from Poisson to Gaussian statistics (must be positive).
      (If set to 0, then it is taken to infinity and implements equation 21 in the reference paper).

    This optimizer is only compatible with histogram data and emission data.
    """

    OSL = 'OSL'
    """
    This optimizer is the One-Step-Late algorithm from P. J. Green, IEEE TMI, Mar 1990, vol. 9, pp. 84-93.

    Subsets can be used as for OSEM. It accepts penalty terms that have a derivative order of at least one.
    Without penalty, it is strictly equivalent to the MLEM algorithm.

    It is numerically implemented in the multiplicative form (as opposed to the gradient form).

    Options (in order when provided as a list):
    - Initial image value: Sets the uniform voxel value for the initial image.
    - Denominator threshold: Sets the threshold of the data space denominator under which the ratio is set to 1.
    - Minimum image update: Sets the minimum of the image update factor under which it stays constant (0 or a negative value
                            means no minimum thus allowing a 0 update).
    - Maximum image update: Sets the maximum of the image update factor over which it stays constant (0 or a negative value means
                            no maximum).

    This optimizer is compatible with both histogram and list-mode data, and with both emission and transmission data.
    """

    PPGMLEM = 'PPGML'
    """
    This optimizer is the Penalized Preconditioned Gradient algorithm from J. Nuyts et al, IEEE TNS, Feb 2002, vol. 49, pp. 56-60.

    It is a heuristic but effective gradient ascent algorithm for penalized maximum-likelihood reconstruction.
    It addresses the shortcoming of One-Step-Late when large penalty strengths can create numerical problems.
    Penalty terms must have a derivative order of at least two.

    Subsets can be used as for OSEM. Without penalty, it is equivalent to the gradient ascent form of the MLEM algorithm.

    Based on likelihood gradient and penalty, a multiplicative update factor is computed and its range is limited by provided parameters.
    Thus, negative values cannot occur and voxels cannot be trapped into 0 values, providing the first estimate is strictly positive.

    Options (in order when provided as a list):
    - Initial image value: Sets the uniform voxel value for the initial image.
    - Denominator threshold: Sets the threshold of the data space denominator under which the ratio is set to 1.
    - Minimum image update: Sets the minimum of the image update factor under which it stays constant (0 or a negative value
                            means no minimum thus allowing a 0 update).
    - Maximum image update: Sets the maximum of the image update factor over which it stays constant (0 or a negative value means
                            no maximum).

    This optimizer is only compatible with histogram data and emission data.
    """

    AML = 'AML'
    """
    This optimizer is the AML algorithm derived from the AB-EMML of C. Byrne, Inverse Problems, 1998, vol. 14, pp. 1455-67.

    The bound B is taken to infinity, so only the bound A can be parameterized.
    This bound must be quantitative (same unit as the reconstructed image).
    It is provided as a single value and thus assuming a uniform bound.

    This algorithm allows for negative image values in case the provided bound is also negative.

    Subsets can be used.

    With a negative or null bound, this algorithm implements equation 6 of A. Rahmim et al, Phys. Med. Biol., 2012, vol. 57, pp. 733-55.
    If a positive bound is provided, then we suppose that the bound A is taken to minus infinity. In that case, this algorithm implements
    equation 22 of K. Van Slambrouck et al, IEEE TMI, Jan 2015, vol. 34, pp. 126-136.

    Options (in order when provided as a list):
    - Initial image value: Sets the uniform voxel value for the initial image.
    - Denominator threshold: Sets the threshold of the data space denominator under which the ratio is set to 1.
    - Bound: Sets the bound parameter that shifts the Poisson law (quantitative, negative or null for standard AML and positive for infinite AML).

    This optimizer is only compatible with histogram data and emission data.
    """

    BSREM = 'BSREM'
    """
    This optimizer is the BSREM (for Block Sequential Regularized Expectation Maximization) algorithm, in development.
    It follows the definition of BSREM II in Ahn and Fessler 2003.

    This optimizer is the Block Sequential Regularized Expectation Maximization (BSREM) algorithm from S. Ahn and
    J. Fessler, IEEE TMI, May 2003, vol. 22, pp. 613-626. Its abbreviated name in this paper is BSREM-II.

    This algorithm is the only one to have proven convergence using subsets. Its implementation is entirely based
    on the reference paper. It may have numerical problems when a full field-of-view is used, because of the sharp
    sensitivity loss at the edges of the field-of-view. As it is simply based on the gradient, penalty terms must
    have a derivative order of at least one. Without penalty, it reduces to OSEM but where the sensitivity is not
    dependent on the current subset. This is a requirement of the algorithm, explaining why it starts by computing
    the global sensitivity before going through iterations. The algorithm is restricted to histograms.

    Options:
    - Initial image value: Sets the uniform voxel value for the initial image.
    - Minimum image value: Sets the minimum allowed image value (parameter 't' in the reference paper).
    - Maximum image value: Sets the maximum allowed image value (parameter 'U' in the reference paper).
    - Relaxation factor type: Type of relaxation factors (can be one of the following: 'classic').

    Relaxation factors of type 'classic' correspond to what was proposed in the reference paper in equation (31).
    This equation gives: alpha_n = alpha_0 / (gamma * iter_num + 1)
    The iteration number 'iter_num' is supposed to start at 0 so that for the first iteration, alpha_0 is used.
    This parameter can be provided using the following keyword: 'relaxation factor classic initial value'.
    The 'gamma' parameter can be provided using the following keyword: 'relaxation factor classic step size'.

    This optimizer is only compatible with histogram data and emission data.
    """

    DEPIERRO95 = 'DEPIERRO95'
    """
    This optimizer is based on the algorithm from A. De Pierro, IEEE TMI, vol. 14, pp. 132-137, 1995.

    This algorithm uses optimization transfer techniques to derive an exact and convergent algorithm
    for maximum likelihood reconstruction including a MRF penalty with different potential functions.

    The algorithm is convergent and is numerically robust to high penalty strength.
    It is strictly equivalent to MLEM without penalty, but can be unstable with extremely low penalty strength.
    Currently, it only implements the quadratic penalty.

    To be used, a MRF penalty still needs to be defined accordingly (at least to define the neighborhood).
    Subsets can be used as for OSEM, without proof of convergence however.

    The algorithm is compatible with list-mode or histogram data.

    Options (in order when provided as a list):
    - Initial image value: Sets the uniform voxel value for the initial image.
    - Denominator threshold: Sets the threshold of the data space denominator under which the ratio is set to 1.
    - Minimum image update: Sets the minimum of the image update factor under which it stays constant (0 or a negative value
                            means no minimum thus allowing a 0 update).
    - Maximum image update: Sets the maximum of the image update factor over which it stays constant (0 or a negative value means
                            no maximum).

    This optimizer is compatible with both histogram and list-mode data, and only with emission data.
    """

    LDWB = 'LDWB'
    """
    This optimizer implements the standard Landweber algorithm for least-squares optimization.

    With transmission data, it uses the log-converted model to derive the update.
    Be aware that the relaxation parameter is not automatically set, so it often requires some
    trials and errors to find an optimal setting. Also, remember that this algorithm is particularly
    slow to converge.

    Options (in order when provided as a list):
    - Initial image value: Sets the uniform voxel value for the initial image.
    - Relaxation factor: Sets the relaxation factor applied to the update.
    - Non-negativity constraint: 0 if no constraint or 1 in order to apply the constraint during the image update.

    This optimizer is only compatible with histogram data, and with both emission and transmission data.
    """

class PotentialType(enum.Enum):
    """The potential function actually penalizes the difference between the voxel of interest and a neighbor:
    p(u, v) = p(u - v)

    Descriptions of potential functions:
    - Quadratic: p(u, v) = 0.5 * (u - v)^2
    - Geman-McClure: p(u, v, d) = (u - v)^2 / (d^2 + (u - v)^2)
    - Hebert-Leahy: p(u, v, m) = log(1 + (u - v)^2 / m^2)
    - Green's log-cosh: p(u, v, d) = log(cosh((u - v) / d))
    - Huber piecewise: p(u, v, d) = d * |u - v| - 0.5 * d^2 if |u - v| > d, else 0.5 * (u - v)^2
    - Nuyts relative: p(u, v, g) = (u - v)^2 / (u + v + g * |u - v|)
    """

    QUADRATIC = 'QUADRATIC'
    """
    Quadratic potential:
    p(u, v) = 0.5 * (u - v)^2

    Reference: Geman and Geman, IEEE Trans. Pattern Anal. Machine Intell., vol. PAMI-6, pp. 721-741, 1984.
    """

    GEMAN_MCCLURE = 'GEMAN_MCCLURE'
    """
    Geman-McClure potential:
    p(u, v, d) = (u - v)^2 / (d^2 + (u - v)^2)

    The parameter 'd' can be set using the 'deltaGMC' keyword.

    Reference: Geman and McClure, Proc. Amer. Statist. Assoc., 1985.
    """

    HEBERT_LEAHY = 'HEBERT_LEAHY'
    """
    Hebert-Leahy potential:
    p(u, v, m) = log(1 + (u - v)^2 / m^2)

    The parameter 'm' can be set using the 'muHL' keyword.

    Reference: Hebert and Leahy, IEEE Trans. Med. Imaging, vol. 8, pp. 194-202, 1989.
    """

    GREEN_LOGCOSH = 'GREEN_LOGCOSH'
    """
    Green's log-cosh potential:
    p(u, v, d) = log(cosh((u - v) / d))

    The parameter 'd' can be set using the 'deltaLogCosh' keyword.

    Reference: Green, IEEE Trans. Med. Imaging, vol. 9, pp. 84-93, 1990.
    """

    HUBER_PIECEWISE = 'HUBER_PIECEWISE'
    """
    Huber piecewise potential:
    p(u, v, d) = d * |u - v| - 0.5 * d^2 if |u - v| > d, else 0.5 * (u - v)^2

    The parameter 'd' can be set using the 'deltaHuber' keyword.

    Reference: e.g. Mumcuoglu et al, Phys. Med. Biol., vol. 41, pp. 1777-1807, 1996.
    """

    RELATIVE_DIFFERENCE = 'NUYTS_RELATIVE'
    """
    Nuyts relative potential:
    p(u, v, g) = (u - v)^2 / (u + v + g * |u - v|)

    The parameter 'g' can be set using the 'gammaRD' keyword.

    Reference: Nuyts et al, IEEE Trans. Nucl. Sci., vol. 49, pp. 56-60, 2002.
    """

class ProcessType(enum.Enum):
    CASToR = 'CASToR'
    PYTHON = 'PYTHON'

class Recon:
    def __init__(self, experiment, saveDir, isGPU = config.get_process() == 'gpu',  isMultiGPU =  True if config.numGPUs > 1 else False, isMultiCPU = True):
        self.reconPhantom = None
        self.reconLaser = None
        self.experiment = experiment
        self.reconType = None
        self.saveDir = saveDir
        self.MSE = None
        self.SSIM = None

        self.isGPU = isGPU
        self.isMultiGPU = isMultiGPU
        self.isMultiCPU = isMultiCPU

        if str(type(self.experiment)) != str(AOT_biomaps.AOT_Experiment.Tomography):
            raise TypeError(f"Experiment must be of type {AOT_biomaps.AOT_Experiment.Tomography}")

    @abstractmethod
    def run(self,withTumor = True):
        pass

    def calculateCRC(self,ROI_mask = None):
        """
        Computes the Contrast Recovery Coefficient (CRC) for a given ROI.
        """
        if self.reconType is ReconType.Analytic:
            raise TypeError(f"Impossible to calculate CRC with analytical reconstruction")
        elif self.reconType is None:
            raise ValueError("Run reconstruction first")
        
        if self.reconPhantom is None or self.reconPhantom == []:
            raise ValueError("Reconstructed phantom is empty. Run reconstruction first.")
        
        if self.reconLaser is None or self.reconLaser == []:
            raise ValueError("Reconstructed laser is empty. Run reconstruction first.")
        
        if self.reconLaser is None or self.reconLaser == []:
            self.run(withTumor = False)
        if ROI_mask is not None:
            recon_ratio = np.mean(self.reconPhantom[ROI_mask]) / np.mean(self.reconLaser[ROI_mask])
            lambda_ratio = np.mean(self.experiment.OpticImage.phantom[ROI_mask]) / np.mean(self.experiment.OpticImage.laser[ROI_mask]) 
        else:
            recon_ratio = np.mean(self.reconPhantom) / np.mean(self.reconLaser)
            lambda_ratio = np.mean(self.experiment.OpticImage.phantom) / np.mean(self.experiment.OpticImage.laser)
        
        # Compute CRC
        CRC = (recon_ratio - 1) / (lambda_ratio - 1)
        return CRC
    
    def calculateMSE(self):
        """
        Calculate the Mean Squared Error (MSE) of the reconstruction.

        Returns:
            mse: float or list of floats, Mean Squared Error of the reconstruction
        """
                
        if self.reconPhantom is None or self.reconPhantom == []:
            raise ValueError("Reconstructed phantom is empty. Run reconstruction first.")

        if self.reconType in (ReconType.Analytic, ReconType.DeepLearning):
            self.MSE = mean_squared_error(self.experiment.OpticImage.phantom, self.reconPhantom)

        elif self.reconType in (ReconType.Algebraic, ReconType.Bayesian):
            self.MSE = []
            for theta in self.reconPhantom:
                self.MSE.append(mean_squared_error(self.experiment.OpticImage.phantom, theta))
  
    def calculateSSIM(self):
        """
        Calculate the Structural Similarity Index (SSIM) of the reconstruction.

        Returns:
            ssim: float or list of floats, Structural Similarity Index of the reconstruction
        """

        if self.reconPhantom is None or self.reconPhantom == []:
            raise ValueError("Reconstructed phantom is empty. Run reconstruction first.")
    
        if self.reconType in (ReconType.Analytic, ReconType.DeepLearning):
            data_range = self.reconPhantom.max() - self.reconPhantom.min()
            self.SSIM = ssim(self.experiment.OpticImage.phantom, self.reconPhantom, data_range=data_range)

        elif self.reconType in (ReconType.Algebraic, ReconType.Bayesian):
            self.SSIM = []
            for theta in self.reconPhantom:
                data_range = theta.max() - theta.min()
                ssim_value = ssim(self.experiment.OpticImage.phantom, theta, data_range=data_range)
                self.SSIM.append(ssim_value)
 
    @staticmethod
    def load_recon(hdr_path):
        """
        Lit un fichier Interfile (.hdr) et son fichier binaire (.img) pour reconstruire une image comme le fait Vinci.
        
        Paramètres :
        ------------
        - hdr_path : chemin complet du fichier .hdr
        
        Retour :
        --------
        - image : tableau NumPy contenant l'image
        - header : dictionnaire contenant les métadonnées du fichier .hdr
        """
        header = {}
        with open(hdr_path, 'r') as f:
            for line in f:
                if ':=' in line:
                    key, value = line.split(':=', 1)  # s'assurer qu'on ne coupe que la première occurrence de ':='
                    key = key.strip().lower().replace('!', '')  # Nettoyage des caractères
                    value = value.strip()
                    header[key] = value
        
        # 📘 Obtenez le nom du fichier de données associé (le .img)
        data_file = header.get('name of data file')
        if data_file is None:
            raise ValueError(f"Impossible de trouver le fichier de données associé au fichier header {hdr_path}")
        
        img_path = os.path.join(os.path.dirname(hdr_path), data_file)
        
        # 📘 Récupérer la taille de l'image à partir des métadonnées
        shape = [int(header[f'matrix size [{i}]']) for i in range(1, 4) if f'matrix size [{i}]' in header]
        if shape and shape[-1] == 1:  # Si la 3e dimension est 1, on la supprime
            shape = shape[:-1]  # On garde (192, 240) par exemple
        
        if not shape:
            raise ValueError("Impossible de déterminer la forme de l'image à partir des métadonnées.")
        
        # 📘 Déterminez le type de données à utiliser
        data_type = header.get('number format', 'short float').lower()
        dtype_map = {
            'short float': np.float32,
            'float': np.float32,
            'int16': np.int16,
            'int32': np.int32,
            'uint16': np.uint16,
            'uint8': np.uint8
        }
        dtype = dtype_map.get(data_type)
        if dtype is None:
            raise ValueError(f"Type de données non pris en charge : {data_type}")
        
        # 📘 Ordre des octets (endianness)
        byte_order = header.get('imagedata byte order', 'LITTLEENDIAN').lower()
        endianess = '<' if 'little' in byte_order else '>'
        
        # 📘 Vérifie la taille réelle du fichier .img
        img_size = os.path.getsize(img_path)
        expected_size = np.prod(shape) * np.dtype(dtype).itemsize
        
        if img_size != expected_size:
            raise ValueError(f"La taille du fichier img ({img_size} octets) ne correspond pas à la taille attendue ({expected_size} octets).")
        
        # 📘 Lire les données binaires et les reformater
        with open(img_path, 'rb') as f:
            data = np.fromfile(f, dtype=endianess + np.dtype(dtype).char)
        
        image =  data.reshape(shape[::-1]) 
        
        # 📘 Rescale l'image si nécessaire
        rescale_slope = float(header.get('data rescale slope', 1))
        rescale_offset = float(header.get('data rescale offset', 0))
        image = image * rescale_slope + rescale_offset
        
        return image.T

class AlgebraicRecon(Recon):
    """
    This class implements the Algebraic reconstruction process.
    It currently does not perform any operations but serves as a template for future implementations.
    """
    def __init__(self, opti = AlgebraicType.MLEM, numIterations = 10000, numSubsets = 1, isSavingEachIteration=True, **kwargs):
        super().__init__(**kwargs)
        self.reconType = ReconType.Algebraic
        self.opti = opti
        self.reconPhantom = []
        self.reconLaser = []
        self.numIterations = numIterations
        self.numSubsets = numSubsets
        self.isSavingEachIteration = isSavingEachIteration

        if self.numIterations <= 0:
            raise ValueError("Number of iterations must be greater than 0.")
        if self.numSubsets <= 0:
            raise ValueError("Number of subsets must be greater than 0.")
        if type(self.numIterations) is not int:
            raise TypeError("Number of iterations must be an integer.")
        if type(self.numSubsets) is not int:
            raise TypeError("Number of subsets must be an integer.")

    # PUBLIC METHODS

    def run(self, processType = ProcessType.PYTHON, withTumor= True):
        """
        This method is a placeholder for the Algebraic reconstruction process.
        It currently does not perform any operations but serves as a template for future implementations.
        """
            
        if(processType == ProcessType.CASToR):
            self._AlgebraicReconCASToR(withTumor)
        elif(processType == ProcessType.PYTHON):
            self._AlgebraicReconPython(withTumor)
        else:
            raise ValueError(f"Unknown Algebraic reconstruction type: {processType}")

    def load_reconCASToR(self,withTumor = True):
        if withTumor:
            folder = 'results_withTumor'
        else:
            folder = 'results_withoutTumor'
            
        for thetaFiles in os.path.join(self.saveDir, folder + '_{}'):
            if thetaFiles.endswith('.hdr'):
                theta = Recon.load_recon(thetaFiles)
                if withTumor:
                    self.reconPhantom.append(theta)
                else:
                    self.reconLaser.append(theta)

    def plot_MSE(self, isSaving=True):
        """
        Plot the Mean Squared Error (MSE) of the reconstruction.
        
        Parameters:
            MSE: list of float, Mean Squared Error values for each iteration
                      If None, uses the MSE from self.MSE.
        
        Returns:
            None
        """
        if not self.MSE:
            raise ValueError("MSE is empty. Please calculate MSE first.")
        
        best_idx = np.argmin(self.MSE)
        
        print(f"Lowest MSE = {np.min(self.MSE):.4f} at iteration {best_idx+1}")

        # Plot MSE curve
        plt.figure(figsize=(7, 5))
        plt.plot(self.MSE, 'r-', label="MSE curve")

        # Add blue dashed lines
        plt.axhline(np.min(self.MSE), color='blue', linestyle='--', label=f"Min MSE = {np.min(self.MSE):.4f}")
        plt.axvline(best_idx+1, color='blue', linestyle='--', label=f"Iteration = {best_idx+1}")

        plt.xlabel("Iteration")
        plt.ylabel("MSE")
        plt.title("MSE vs. Iteration")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        if isSaving:
            now = datetime.now()    
            date_str = now.strftime("%Y_%d_%m_%y")
            SavingFolder = os.path.join(self.saveDir, 'results', f'MSE_plot{date_str}.png')
            plt.savefig(SavingFolder, dpi=300)
            print(f"MSE plot saved to {SavingFolder}")
        
        plt.show()

    def show_MSE_bestRecon(self, isSaving=True):
        
        if not self.MSE:
            raise ValueError("MSE is empty. Please calculate MSE first.")

        best_idx = np.argmin(self.MSE)
        best_recon = self.reconPhantom[best_idx]

        # ----------------- Plotting -----------------
        fig, axs = plt.subplots(1, 3, figsize=(15, 5))  # 1 row, 3 columns

        # Normalization based on LAMBDA max
        lambda_max = np.max(self.experiment.OpticImage.laser.intensity)

        # Left: Best reconstructed image (normalized)
        im0 = axs[0].imshow(best_recon / lambda_max, 
                            extent=(self.experiment.params['Xrange'][0], self.experiment.params['Xrange'][1], self.experiment.params['Zrange'][1], self.experiment.params['Zrange'][0]),
                            cmap='hot', aspect='equal', vmin=0, vmax=1)
        axs[0].set_title(f"Min MSE Reconstruction\nIter {best_idx+1}, MSE={np.min(self.MSE):.4f}")
        axs[0].set_xlabel("x (mm)")
        axs[0].set_ylabel("z (mm)")
        plt.colorbar(im0, ax=axs[0])

        # Middle: Ground truth (normalized)
        im1 = axs[1].imshow(self.experiment.OpticImage.laser.intensity / lambda_max, 
                            extent=(self.experiment.params['Xrange'][0], self.experiment.params['Xrange'][1], self.experiment.params['Zrange'][1], self.experiment.params['Zrange'][0]),
                            cmap='hot', aspect='equal', vmin=0, vmax=1)
        axs[1].set_title(r"Ground Truth ($\lambda$)")
        axs[1].set_xlabel("x (mm)")
        axs[1].set_ylabel("z (mm)")
        plt.colorbar(im1, ax=axs[1])

        # Right: Reconstruction at iter 350
        lastRecon = self.reconPhantom[-1] 
        im2 = axs[2].imshow(lastRecon / lambda_max,
                            extent=(self.experiment.params['Xrange'][0], self.experiment.params['Xrange'][1], self.experiment.params['Zrange'][1], self.experiment.params['Zrange'][0]),
                            cmap='hot', aspect='equal', vmin=0, vmax=1)
        axs[2].set_title(f"Last Reconstruction\nIter {self.numIterations * self.numSubsets}, MSE={np.mean((self.experiment.OpticImage.laser.intensity - lastRecon) ** 2):.4f}")
        axs[2].set_xlabel("x (mm)")
        axs[2].set_ylabel("z (mm)")
        plt.colorbar(im2, ax=axs[2])

        plt.tight_layout()
        if isSaving:
            now = datetime.now()    
            date_str = now.strftime("%Y_%d_%m_%y")
            SavingFolder = os.path.join(self.saveDir, 'results', f'comparison_MSE_BestANDLastRecon{date_str}.png')
            plt.savefig(SavingFolder, dpi=300)
            print(f"MSE plot saved to {SavingFolder}")
        plt.show()

    def show_recon(self, vmin=None, vmax=None, isSaving=True, iteration=-1):
        """
        Show the reconstructed phantom image.
        
        Parameters:
            vmin, vmax: color limits (optional)
            isSaving: boolean, whether to save the figure or not
        """
        if self.reconPhantom is None or len(self.reconPhantom) == 0:
            raise ValueError("Reconstructed phantom is empty. Run reconstruction first.")

        plt.imshow(self.reconPhantom[iteration], extent=(self.experiment.params['Xrange'][0], self.experiment.params['Xrange'][1], self.experiment.params['Zrange'][1], self.experiment.params['Zrange'][0]),vmin=vmin, vmax=vmax, aspect='equal', cmap='hot')
        plt.title(f"Reconstructed Phantom at Iteration {iteration + 1}")
        plt.xlabel("x (mm)")
        plt.ylabel("z (mm)")

    def show_theta_animation(self, vmin=None, vmax=None, duration=5000, save_path=None):
        """
        Show theta iteration animation (for Jupyter) and optionally save it as a GIF.
        
        Parameters:
            matrix_theta: list of (z, x) ndarray, Algebraic reconstructions
            x: 1D array, x-coordinates (in meters)
            z: 1D array, z-coordinates (in meters)
            vmin, vmax: color limits (optional)
            duration: duration of the animation in milliseconds
            save_path: path to save animation (e.g., 'theta.gif' or 'theta.mp4')
        """
        if len(self.reconPhantom) == 0 or len(self.reconPhantom) == 1:
            raise ValueError("No theta matrix available for animation.")

        frames = np.array(self.reconPhantom)
        num_frames = len(frames)

        interval = max(1, int(duration / num_frames))

        if vmin is None:
            vmin = np.min(frames)
        if vmax is None:
            vmax = np.max(frames)

        fig, ax = plt.subplots(figsize=(5, 5))
        im = ax.imshow(frames[0],
                    extent=(self.experiment.params['Xrange'][0],self.experiment.params['Xrange'][1], self.experiment.params['Zrange'][1], self.experiment.params['Zrange'][0]),
                    vmin=vmin, vmax=vmax,
                    aspect='equal', cmap='hot')

        title = ax.set_title("Iteration 0")
        ax.set_xlabel("x (mm)")
        ax.set_ylabel("z (mm)")
        plt.tight_layout()

        def update(frame_idx):
            im.set_array(frames[frame_idx])
            title.set_text(f"Iteration {frame_idx}")
            return [im, title]

        ani = animation.FuncAnimation(fig, update, frames=num_frames, interval=interval, blit=False)

        if save_path:
            if save_path.endswith(".gif"):
                ani.save(save_path, writer="pillow", fps=1000 // interval)
            elif save_path.endswith(".mp4"):
                ani.save(save_path, writer="ffmpeg", fps=1000 // interval)
            else:
                raise ValueError("Unsupported file format. Use .gif or .mp4")
            print(f"Animation saved to {save_path}")

        plt.close(fig)
        plt.rcParams["animation.html"] = "jshtml"
        return HTML(ani.to_jshtml())  

    def plot_SSIM(self, isSaving=True):

        if not self.SSIM:
            raise ValueError("SSIM is empty. Please calculate SSIM first.")
        
        best_idx = np.argmax(self.SSIM)
        
        print(f"Highest SSIM = {np.max(self.SSIM):.4f} at iteration {best_idx+1}")

        # Plot SSIM curve
        plt.figure(figsize=(7, 5))
        plt.plot(self.SSIM, 'r-', label="SSIM curve")

        # Add blue dashed lines
        plt.axhline(np.max(self.SSIM), color='blue', linestyle='--', label=f"Max SSIM = {np.max(self.SSIM):.4f}")
        plt.axvline(best_idx+1, color='blue', linestyle='--', label=f"Iteration = {best_idx+1}")

        plt.xlabel("Iteration")
        plt.ylabel("SSIM")
        plt.title("SSIM vs. Iteration")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        if isSaving:
            now = datetime.now()    
            date_str = now.strftime("%Y_%d_%m_%y")
            SavingFolder = os.path.join(self.saveDir, 'results', f'SSIM_plot{date_str}.png')
            plt.savefig(SavingFolder, dpi=300)
            print(f"SSIM plot saved to {SavingFolder}")
        
        plt.show()

    def show_SSIM_bestRecon(self, isSaving=True):
        
        if not self.SSIM:
            raise ValueError("SSIM is empty. Please calculate SSIM first.")

        best_idx = np.argmax(self.SSIM)
        best_recon = self.reconPhantom[best_idx]

        # ----------------- Plotting -----------------
        fig, axs = plt.subplots(1, 3, figsize=(15, 5))  # 1 row, 3 columns

        # Normalization based on LAMBDA max
        lambda_max = np.max(self.experiment.OpticImage.laser.intensity)

        # Left: Best reconstructed image (normalized)
        im0 = axs[0].imshow(best_recon / lambda_max, 
                            extent=(self.experiment.params['Xrange'][0], self.experiment.params['Xrange'][1], self.experiment.params['Zrange'][1], self.experiment.params['Zrange'][0]),
                            cmap='hot', aspect='equal', vmin=0, vmax=1)
        axs[0].set_title(f"Max SSIM Reconstruction\nIter {best_idx+1}, SSIM={np.min(self.MSE):.4f}")
        axs[0].set_xlabel("x (mm)")
        axs[0].set_ylabel("z (mm)")
        plt.colorbar(im0, ax=axs[0])

        # Middle: Ground truth (normalized)
        im1 = axs[1].imshow(self.experiment.OpticImage.laser.intensity / lambda_max, 
                            extent=(self.experiment.params['Xrange'][0], self.experiment.params['Xrange'][1], self.experiment.params['Zrange'][1], self.experiment.params['Zrange'][0]),
                            cmap='hot', aspect='equal', vmin=0, vmax=1)
        axs[1].set_title(r"Ground Truth ($\lambda$)")
        axs[1].set_xlabel("x (mm)")
        axs[1].set_ylabel("z (mm)")
        plt.colorbar(im1, ax=axs[1])

        # Right: Reconstruction at iter 350
        lastRecon = self.reconPhantom[-1] 
        im2 = axs[2].imshow(lastRecon / lambda_max,
                            extent=(self.experiment.params['Xrange'][0], self.experiment.params['Xrange'][1], self.experiment.params['Zrange'][1], self.experiment.params['Zrange'][0]),
                            cmap='hot', aspect='equal', vmin=0, vmax=1)
        axs[2].set_title(f"Last Reconstruction\nIter {self.numIterations * self.numSubsets}, SSIM={self.SSIM[-1]:.4f}")
        axs[2].set_xlabel("x (mm)")
        axs[2].set_ylabel("z (mm)")
        plt.colorbar(im2, ax=axs[2])

        plt.tight_layout()
        if isSaving:
            now = datetime.now()    
            date_str = now.strftime("%Y_%d_%m_%y")
            SavingFolder = os.path.join(self.saveDir, 'results', f'comparison_SSIM_BestANDLastRecon{date_str}.png')
            plt.savefig(SavingFolder, dpi=300)
            print(f"SSIM plot saved to {SavingFolder}")
        plt.show()

    def plot_CRC_vs_Noise(theta_with_tumor_vec, theta_without_tumor_vec,
                      LAMBDA_with_tumor, LAMBDA_without_tumor, ROI_mask,
                      start=0, fin=None, step=10, save_path=None):
        """
        画出 CRC vs Noise 曲线，横轴为 noise，纵轴为 CRC
        """
        if fin is None:
            fin = len(theta_with_tumor_vec)

        iter_range = range(start, fin+1, step)

        crc_values = []
        noise_values = []

        for i in iter_range:
            recon_with_tumor = theta_with_tumor_vec[i].T
            recon_without_tumor = theta_without_tumor_vec[i].T
            diff = np.abs(recon_with_tumor - LAMBDA_with_tumor)

            # CRC (使用 ROI)
            crc = compute_CRC(recon_with_tumor, recon_without_tumor, LAMBDA_with_tumor, LAMBDA_without_tumor, ROI_mask)
            crc_values.append(crc)

            # Noise (全图)
            noise = np.mean(np.abs(recon_without_tumor - LAMBDA_without_tumor))
            noise_values.append(noise)

        # 绘图
        plt.figure(figsize=(6, 5))
        plt.plot(noise_values, crc_values, 'o-', label='ML-EM')
        for i, (x, y) in zip(iter_range, zip(noise_values, crc_values)):
            plt.text(x, y, str(i), fontsize=5.5, ha='left', va='bottom')

        plt.xlabel("Noise (mean absolute error)")
        plt.ylabel("CRC (Contrast Recovery Coefficient)")

        plt.xscale('log')
        plt.yscale('log')

        plt.title("CRC vs Noise over Iterations")
        plt.grid(True)
        plt.legend()

        if save_path:
            plt.savefig(save_path, dpi=300)
            print(f"Figure saved to: {save_path}")
        plt.show()
        
    def plot_reconstruction_progress(theta_without_tumor_vec, LAMBDA_without_tumor, theta_with_tumor_vec, LAMBDA_with_tumor, start, fin=None, step=1, save_path=None):
        #TODO
        """
        绘制每隔一定迭代次数的重建结果 + 误差图 + Ground Truth。

        参数：
            theta_with_tumor_vec (list of 2D np.ndarray): 重建图像序列（来自 EM）
            LAMBDA_with_tumor (2D np.ndarray): ground truth 图像
            start (int): 起始迭代索引
            fin (int): 终止迭代索引（包含）；如果为 None，默认为最后一帧
            step (int): 每隔多少次迭代绘制一行
            save_path (str): 如果提供，将保存图像到指定路径
        """

        # without tumor

        if fin is None:
            fin = len(theta_without_tumor_vec) - 1  # 注意索引从 0 开始

        iter_list = list(range(start, fin + 1, step))
        nrows = len(iter_list)
        ncols = 3  # Recon, |Recon - GT|, Ground Truth

        vmin = 0
        vmax = 1

        # 提前计算所有 recon, diff, mse, noise
        recon_without_tumor_list = []
        diff_abs_without_tumor_list = []
        mse_without_tumor_list = []
        noise_list = []

        for i in iter_list:
            recon_without_tumor = theta_without_tumor_vec[i].T
            diff_abs_without_tumor = np.abs(recon_without_tumor - LAMBDA_without_tumor)
            mse_without_tumor = mean_squared_error(LAMBDA_without_tumor.flatten(), recon_without_tumor.flatten())

            noise = np.mean(np.abs(theta_without_tumor_vec[i].T - LAMBDA_without_tumor))

            recon_without_tumor_list.append(recon_without_tumor)
            diff_abs_without_tumor_list.append(diff_abs_without_tumor)
            mse_without_tumor_list.append(mse_without_tumor)
            noise_list.append(noise)

        # 全局误差范围用于统一 colormap
        global_min_diff_abs_without_tumor = np.min([d.min() for d in diff_abs_without_tumor_list[1:]])
        global_max_diff_abs_without_tumor = np.max([d.max() for d in diff_abs_without_tumor_list[1:]])

        # 开始绘图
        fig, axs = plt.subplots(nrows=nrows, ncols=ncols, figsize=(12, 3 * nrows))

        for i, iter_idx in enumerate(iter_list):
            recon_without_tumor = recon_without_tumor_list[i]
            diff_abs_without_tumor = diff_abs_without_tumor_list[i]
            mse_without_tumor = mse_without_tumor_list[i]
            noise = noise_list[i]

            # 左图：重建图像
            im0 = axs[i, 0].imshow(recon_without_tumor.T, cmap='hot', vmin=vmin, vmax=vmax, aspect='equal')
            axs[i, 0].set_title(f"Reconstruction\nIter {iter_idx}, MSE={mse_without_tumor:.2e}", fontsize=10)
            axs[i, 0].axis('off')
            plt.colorbar(im0, ax=axs[i, 0])

            # 中图：误差图
            if i >= 0 :
                im1 = axs[i, 1].imshow(diff_abs_without_tumor.T, cmap='viridis', vmin=np.min(diff_abs_without_tumor), vmax=np.max(diff_abs_without_tumor), aspect='equal')
            else :
                im1 = axs[i, 1].imshow(diff_abs_without_tumor.T, cmap='viridis', vmin=global_min_diff_abs_without_tumor, vmax=global_max_diff_abs_without_tumor, aspect='equal')
            axs[i, 1].set_title(f"|Recon - Ground Truth|\nNoise={noise:.2e}", fontsize=10)
            axs[i, 1].axis('off')
            plt.colorbar(im1, ax=axs[i, 1])

            # 右图：ground truth
            im2 = axs[i, 2].imshow(LAMBDA_without_tumor.T, cmap='hot', vmin=vmin, vmax=vmax, aspect='equal')
            axs[i, 2].set_title(r"Ground Truth ($\lambda$)", fontsize=10)
            axs[i, 2].axis('off')
            plt.colorbar(im2, ax=axs[i, 2])

        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300)
            print(f"Figure saved to: {save_path}")
        plt.show()

        # with tumor

        if fin is None:
            fin = len(theta_with_tumor_vec) - 1  # 注意索引从 0 开始

        iter_list = list(range(start, fin + 1, step))
        nrows = len(iter_list)
        ncols = 3  # Recon, |Recon - GT|, Ground Truth

        vmin = 0
        vmax = 1

        # 提前计算所有 recon, diff, mse, noise
        recon_with_tumor_list = []
        diff_abs_with_tumor_list = []
        mse_with_tumor_list = []
        noise_list = []

        for i in iter_list:
            recon_with_tumor = theta_with_tumor_vec[i].T
            diff_abs_with_tumor = np.abs(recon_with_tumor - LAMBDA_with_tumor)
            mse_with_tumor = mean_squared_error(LAMBDA_with_tumor.flatten(), recon_with_tumor.flatten())

            noise = np.mean(np.abs(theta_without_tumor_vec[i].T - LAMBDA_without_tumor))  # !! without tumor

            recon_with_tumor_list.append(recon_with_tumor)
            diff_abs_with_tumor_list.append(diff_abs_with_tumor)
            mse_with_tumor_list.append(mse_with_tumor)  
            noise_list.append(noise)

        # 全局误差范围用于统一 colormap
        global_min_diff_abs_with_tumor = np.min([d.min() for d in diff_abs_with_tumor_list[1:]])
        global_max_diff_abs_with_tumor = np.max([d.max() for d in diff_abs_with_tumor_list[1:]])

        # 开始绘图
        fig, axs = plt.subplots(nrows=nrows, ncols=ncols, figsize=(12, 3 * nrows))

        for i, iter_idx in enumerate(iter_list):
            recon_with_tumor = recon_with_tumor_list[i]
            diff_abs_with_tumor = diff_abs_with_tumor_list[i]
            mse_with_tumor = mse_with_tumor_list[i]
            noise = noise_list[i]

            # 左图：重建图像
            im0 = axs[i, 0].imshow(recon_with_tumor.T, cmap='hot', vmin=vmin, vmax=vmax, aspect='equal')
            axs[i, 0].set_title(f"Reconstruction\nIter {iter_idx}, MSE={mse_with_tumor:.2e}", fontsize=10)
            axs[i, 0].axis('off')
            plt.colorbar(im0, ax=axs[i, 0])

            # 中图：误差图
            if i >= 0 :
                im1 = axs[i, 1].imshow(diff_abs_with_tumor.T, cmap='viridis', vmin=np.min(diff_abs_with_tumor), vmax=np.max(diff_abs_with_tumor), aspect='equal')
            else :
                im1 = axs[i, 1].imshow(diff_abs_with_tumor.T, cmap='viridis', vmin=global_min_diff_abs_with_tumor, vmax=global_max_diff_abs_with_tumor, aspect='equal')
            axs[i, 1].set_title(f"|Recon - Ground Truth|\nNoise={noise:.2e}", fontsize=10)
            axs[i, 1].axis('off')
            plt.colorbar(im1, ax=axs[i, 1])

            # 右图：ground truth
            im2 = axs[i, 2].imshow(LAMBDA_with_tumor.T, cmap='hot', vmin=vmin, vmax=vmax, aspect='equal')
            axs[i, 2].set_title(r"Ground Truth ($\lambda$)", fontsize=10)
            axs[i, 2].axis('off')
            plt.colorbar(im2, ax=axs[i, 2])

        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300)
            print(f"Figure saved to: {save_path}")
        plt.show()
   
    # PRIVATE METHODS

    def _AlgebraicReconPython(self,withTumor):

        acoustic_fields = []
        for i in trange(len(self.experiment.AcousticFields), desc="Generating system matrix (formating acoustic fields)"):
            ac_field = self.experiment.AcousticFields[i]
            acoustic_fields.append(ac_field.field)

        # Convertir la liste en un tableau numpy
        SMatrix = np.stack(acoustic_fields, axis=-1)

        if withTumor:
            if self.experiment.AOsignal_withTumor is None:
                raise ValueError("AO signal with tumor is not available. Please generate AO signal with tumor the experiment first in the experiment object.")
            if self.opti.value == AlgebraicType.MLEM.value:
                self.reconPhantom = self._MLEM(SMatrix=SMatrix, y=self.experiment.AOsignal_withTumor)
        else:
            if self.experiment.AOsignal_withoutTumor is None:
                raise ValueError("AO signal without tumor is not available. Please generate AO signal without tumor the experiment first in the experiment object.")
            if self.opti.value == AlgebraicType.MLEM.value:
                self.reconLaser = self._MLEM(SMatrix=SMatrix, y=self.experiment.AOsignal_withoutTumor)

    def _AlgebraicReconCASToR(self, withTumor):
        
        # Define variables
        smatrix = os.path.join(self.saveDir,"system_matrix")

        if withTumor:
            fileName = 'AOSignals_withTumor.cdh'
        else:
            fileName = 'AOSignals_withoutTumor.cdh'

        # Check if input file exists
        if not os.path.isfile(f"{self.saveDir}/{fileName}"):
            self.experiment._saveAOsignals_Castor(self.saveDir)
        # Check if system matrix directory exists
        elif not os.path.isdir(smatrix):
            os.mkdir(smatrix)
        # check if system matrix is empty
        elif not os.listdir(smatrix):
            self.experiment.saveAcousticFields(self.saveDir)

        # Construct the command
        cmd = [
            self.experiment.params.reconstruction['castor_executable'],
            "-df", f"{self.saveDir}/{fileName}",
            "-opti", self.opti.value,
            "-it", f"{self.numIterations}:{self.numSubsets}"  ,
            "-proj", "matrix",
            "-dout", os.path.join(self.saveDir, 'results','recon'),
            "-th", f"{ os.cpu_count()}",
            "-vb", "5",
            "-proj-comp", "1",
            "-ignore-scanner",
            "-data-type", "AOT",
            "-ignore-corr", "cali,fdur",
            "-system-matrix", smatrix,
        ]

        # Print the command
        print(" ".join(cmd))

        #save the command to a script file
        recon_script_path = os.path.join(gettempdir(), 'recon.sh')
        with open(recon_script_path, 'w') as f:
            f.write("#!/bin/bash\n")
            f.write(" ".join(cmd) + "\n")

        sys.exit(0)

        # --- Run Reconstruction Script ---
        print(f"Running reconstruction script: {recon_script_path}")
        subprocess.run(["chmod", "+x", recon_script_path], check=True)
        subprocess.run([recon_script_path], check=True)
        print("Reconstruction script executed.")

        self.load_reconCASToR(withTumor=withTumor)

    def _MLEM(self, SMatrix, y):
        """
        This method implements the MLEM algorithm using either basic numpy operations or PyTorch for GPU acceleration.
        It is called by the Algebraic reconstruction process.
        """
        if self.isGPU and self.isMultiGPU:
            try:
                return AlgebraicRecon._MLEM_GPU_multi(SMatrix= SMatrix, y = y, numIteration=self.numIterations, isSavingEachIteration = self.isSavingEachIteration)
            except:
                try:
                    warnings.warn("Multi-GPU MLEM failed. Falling back to single GPU MLEM.")
                    return AlgebraicRecon._MLEM_GPU_basic(SMatrix= SMatrix, y = y, numIteration=self.numIterations, isSavingEachIteration = self.isSavingEachIteration)
                except:
                    warnings.warn("Single GPU MLEM failed. Falling back to basic CPU MLEM.")
                    return AlgebraicRecon._MLEM_CPU_opti(SMatrix= SMatrix, y = y, numIteration=self.numIterations, isSavingEachIteration = self.isSavingEachIteration)
        if self.isGPU and not self.isMultiGPU:
            try:
                return AlgebraicRecon._MLEM_GPU_basic(SMatrix= SMatrix, y = y, numIteration=self.numIterations, isSavingEachIteration = self.isSavingEachIteration)
            except:
                warnings.warn("Single GPU MLEM failed. Falling back to basic CPU MLEM.")
                return AlgebraicRecon._MLEM_CPU_opti(SMatrix= SMatrix, y = y, numIteration=self.numIterations, isSavingEachIteration = self.isSavingEachIteration)
        if not self.isGPU and self.isMultiCPU:
            return AlgebraicRecon._MLEM_CPU_multi(SMatrix= SMatrix, y = y, numIteration=self.numIterations, isSavingEachIteration = self.isSavingEachIteration)
        if not self.isGPU and not self.isMultiCPU:
            try:
                return AlgebraicRecon._MLEM_CPU_opti(SMatrix= SMatrix, y = y, numIteration=self.numIterations, isSavingEachIteration = self.isSavingEachIteration)
            except:
                warnings.warn("Optimized MLEM failed. Falling back to basic MLEM.")
                return AlgebraicRecon._MLEM_CPU_basic(SMatrix= SMatrix, y = y, numIteration=self.numIterations, isSavingEachIteration = self.isSavingEachIteration)
        

    ### ALGORITHMS IMPLEMENTATION ###

    @staticmethod
    def _MLEM_GPU_basic(SMatrix, y, numIteration, isSavingEachIteration):
        """
        This method implements the MLEM algorithm using PyTorch for GPU acceleration.
        Parameters:
            SMatrix: 4D numpy array (time, z, x, nScans)
            y: 2D numpy array (time, nScans)
            numIteration: number of iterations for the MLEM algorithm
        """
        A_matrix_torch = torch.tensor(SMatrix, dtype=torch.float32).cuda()  # shape: (T, Z, X, N)
        y_torch = torch.tensor(y, dtype=torch.float32).cuda()                # shape: (T, N)

        # Initialize variables
        T, Z, X, N = SMatrix.shape

        # flat
        A_flat = A_matrix_torch.permute(0, 3, 1, 2).reshape(T * N, Z * X)     # shape: (T * N, Z * X)
        y_flat = y_torch.reshape(-1)                                          # shape: (T * N, )

        # Step 1: start from a strickly positive image theta^(0)
        theta_0 = torch.ones((Z, X), dtype=torch.float32, device='cuda')      # shape: (Z, X)
        matrix_theta_torch = [theta_0]
        # matrix_theta_from_gpu = []

        # Compute normalization factor: A^T * 1
        normalization_factor = A_matrix_torch.sum(dim=(0, 3))                # shape: (Z, X)
        normalization_factor_flat = normalization_factor.reshape(-1)         # shape: (Z * X, )

        # EM Algebraic update
        for _ in trange(numIteration, desc=f"AOT-BioMaps -- Algebraic Reconstruction Tomography: ML-EM  ---- processing on single GPU no.{torch.cuda.current_device()} ----"):

            theta_p = matrix_theta_torch[-1]                                 # shape: (Z, X)

            # Step 2: Forward projection of current estimate : q = A * theta + b (acc with GPU)
            theta_p_flat = theta_p.reshape(-1)                               # shape: (Z * X, )
            q_flat = A_flat @ theta_p_flat                                   # shape: (T * N, )

            # Step 3: Current error estimate : compute ratio e = m / q
            e_flat = y_flat / (q_flat + torch.finfo(torch.float32).tiny)                                # shape: (T * N, )

            # Step 4: Backward projection of the error estimate : c = A.T * e (acc with GPU)
            c_flat = A_flat.T @ e_flat                                       # shape: (Z * X, )

            # Step 5: Multiplicative update of current estimate
            theta_p_plus_1_flat = (theta_p_flat / (normalization_factor_flat + torch.finfo(torch.float32).tiny)) * c_flat

            matrix_theta_torch.append(theta_p_plus_1_flat.reshape(Z, X))      # shape: (Z, X)
        
        if not isSavingEachIteration:
            return matrix_theta_torch[-1]
        else:
            return [theta.cpu().numpy() for theta in matrix_theta_torch]
         
    @staticmethod
    def _MLEM_CPU_basic(SMatrix, y, numIteration, isSavingEachIteration):
        """
        This method implements the MLEM algorithm using basic numpy operations.
        Parameters:
            SMatrix: 4D numpy array (time, z, x, nScans)
            y: 2D numpy array (time, nScans)
            numIteration: number of iterations for the MLEM algorithm
        """
        # Initialize variables
        q_p = np.zeros((SMatrix.shape[0], SMatrix.shape[3]))  # shape : (t, i)
        c_p = np.zeros((SMatrix.shape[1], SMatrix.shape[2]))  # shape : (z, x)

        # Step 1: start from a strickly positive image theta^(0)
        theta_p_0 = np.ones((SMatrix.shape[1], SMatrix.shape[2]))  # initial theta^(0)
        matrix_theta = [theta_p_0]  # store theta 

        # Compute normalization factor: A^T * 1
        normalization_factor = np.sum(SMatrix, axis=(0, 3))  # shape: (z, x)

        # EM Algebraic update
        for _ in trange(numIteration, desc="AOT-BioMaps -- Algebraic Reconstruction Tomography: ML-EM  ---- processing on single CPU (basic) ----"):

            theta_p = matrix_theta[-1]

            # Step 1: Forward projection of current estimate : q = A * theta + b
            for _t in range(SMatrix.shape[0]):
                for _n in range(SMatrix.shape[3]):
                    q_p[_t, _n] = np.sum(SMatrix[_t, :, :, _n] * theta_p)
            
            # Step 2: Current error estimate : compute ratio e = m / q
            e_p = y / (q_p + 1e-8)  # 避免除零
            
            # Step 3: Backward projection of the error estimate : c = A.T * e
            for _z in range(SMatrix.shape[1]):
                for _x in range(SMatrix.shape[2]):
                    c_p[_z, _x] = np.sum(SMatrix[:, _z, _x, :] * e_p)
            
            # Step 4: Multiplicative update of current estimate
            theta_p_plus_1 = theta_p / (normalization_factor + 1e-8) * c_p
            
            # Step 5: Store current theta
            matrix_theta.append(theta_p_plus_1)
        
        if not isSavingEachIteration:
            return matrix_theta[-1]
        else:
            return matrix_theta  # Return the list of numpy arrays

    @staticmethod
    def _MLEM_CPU_multi(SMatrix, y, numIteration, isSavingEachIteration):
        """
        This method implements the MLEM algorithm using multi-threading with Numba.
        Parameters:
            SMatrix: 4D numpy array (time, z, x, nScans)
            y: 2D numpy array (time, nScans)
            numIteration: number of iterations for the MLEM algorithm
        """
        numba.set_num_threads(os.cpu_count())
        q_p = np.zeros((SMatrix.shape[0], SMatrix.shape[3]))  # shape : (t, i)
        c_p = np.zeros((SMatrix.shape[1], SMatrix.shape[2]))  # shape : (z, x)

        # Step 1: start from a strickly positive image theta^(0)
        theta_p_0 = np.ones((SMatrix.shape[1], SMatrix.shape[2]))
        matrix_theta = [theta_p_0]

        # Compute normalization factor: A^T * 1
        normalization_factor = np.sum(SMatrix, axis=(0, 3))  # shape: (z, x)

        # EM Algebraic update
        for _ in trange(numIteration, desc=f"AOT-BioMaps -- Algebraic Reconstruction Tomography: ML-EM  ---- processing on multithread CPU ({numba.config.NUMBA_DEFAULT_NUM_THREADS} threads)----"):
            
            theta_p = matrix_theta[-1]

            # Step 1: Forward projection of current estimate : q = A * theta + b (acc with njit)
            AlgebraicRecon._forward_projection(SMatrix, theta_p, q_p)

            # Step 2: Current error estimate : compute ratio e = m / q
            e_p = y / (q_p + 1e-8)

            # Step 3: Backward projection of the error estimate : c = A.T * e (acc with njit)
            AlgebraicRecon._backward_projection(SMatrix, e_p, c_p)

            # Step 4: Multiplicative update of current estimate
            theta_p_plus_1 = theta_p / (normalization_factor + 1e-8) * c_p

            # Step 5: Store current theta
            matrix_theta.append(theta_p_plus_1)
        
        if not isSavingEachIteration:
            return matrix_theta[-1]
        else:
            return matrix_theta

    @staticmethod
    def _MLEM_CPU_opti(SMatrix, y, numIteration, isSavingEachIteration):
        """
        This method implements the MLEM algorithm using optimized numpy operations.
        Parameters:
            SMatrix: 4D numpy array (time, z, x, nScans)
            y: 2D numpy array (time, nScans)
            numIteration: number of iterations for the MLEM algorithm
        """
        # Initialize variables
        T, Z, X, N = SMatrix.shape

        A_flat = SMatrix.astype(np.float32).transpose(0, 3, 1, 2).reshape(T * N, Z * X)         # shape: (T * N, Z * X)
        y_flat = y.astype(np.float32).reshape(-1)                                                # shape: (T * N, )

        # Step 1: start from a strickly positive image theta^(0)
        theta_0 = np.ones((Z, X), dtype=np.float32)              # shape: (Z, X)
        matrix_theta = [theta_0]

        # Compute normalization factor: A^T * 1
        normalization_factor = np.sum(SMatrix, axis=(0, 3)).astype(np.float32)                  # shape: (Z, X)
        normalization_factor_flat = normalization_factor.reshape(-1) 

        # EM Algebraic update
        for _ in trange(numIteration, desc="AOT-BioMaps -- Algebraic Reconstruction Tomography: ML-EM ---- processing on single CPU (optimized) ----"):
            theta_p = matrix_theta[-1]

            # Step 2: Forward projection of current estimate : q = A * theta + b (acc with njit)
            theta_p_flat = theta_p.reshape(-1)                                                    # shape: (Z * X, )
            q_flat = A_flat @ theta_p_flat                                                        # shape: (T * N)

            # Step 3: Current error estimate : compute ratio e = m / q
            e_flat = y_flat / (q_flat + np.finfo(np.float32).tiny)                                         # shape: (T * N, )
            # np.float32(1e-8)
            
            # Step 4: Backward projection of the error estimate : c = A.T * e (acc with njit)
            c_flat = A_flat.T @ e_flat                                                            # shape: (Z * X, )

            # Step 5: Multiplicative update of current estimate
            theta_p_plus_1_flat = theta_p_flat / (normalization_factor_flat + np.finfo(np.float32).tiny) * c_flat
            
            
            # Step 5: Store current theta
            matrix_theta.append(theta_p_plus_1_flat.reshape(Z, X))

        if not isSavingEachIteration:
            return matrix_theta[-1]
        else:
            return matrix_theta

    @staticmethod   
    def _MLEM_GPU_multi(SMatrix, y, numIteration, isSavingEachIteration):
        """
        This method implements the MLEM algorithm using PyTorch for multi-GPU acceleration.
        Parameters:
            SMatrix: 4D numpy array (time, z, x, nScans)
            y: 2D numpy array (time, nScans)
            numIteration: number of iterations for the MLEM algorithm
        """
        # Check the number of available GPUs
        num_gpus = torch.cuda.device_count()
 
        # Convert data to tensors and distribute across GPUs
        A_matrix_torch = torch.tensor(SMatrix, dtype=torch.float32).cuda()
        y_torch = torch.tensor(y, dtype=torch.float32).cuda()

        # Initialize variables
        T, Z, X, N = SMatrix.shape

        # Distribute the data across GPUs
        A_matrix_torch = A_matrix_torch.permute(0, 3, 1, 2).reshape(T * N, Z * X)
        y_flat = y_torch.reshape(-1)

        # Split data across GPUs
        A_split = torch.chunk(A_matrix_torch, num_gpus, dim=0)
        y_split = torch.chunk(y_flat, num_gpus)

        # Initialize theta on each GPU
        theta_0 = torch.ones((Z, X), dtype=torch.float32, device='cuda')
        theta_list = [theta_0.clone() for _ in range(num_gpus)]

        # Compute normalization factor: A^T * 1
        normalization_factor = A_matrix_torch.sum(dim=0)
        normalization_factor = normalization_factor.reshape(Z, X)

        # EM Algebraic update
        for _ in trange(numIteration, desc=f"AOT-BioMaps -- Algebraic Reconstruction Tomography: ML-EM ---- processing on multi-GPU ({num_gpus} GPUs)----"):
            theta_p_list = theta_list.copy()

            for i in range(num_gpus):
                A_i = A_split[i].to(f'cuda:{i}')
                y_i = y_split[i].to(f'cuda:{i}')
                theta_p = theta_p_list[i].to(f'cuda:{i}')

                # Forward projection
                q_flat = A_i @ theta_p.reshape(-1)

                # Current error estimate
                e_flat = y_i / (q_flat + torch.finfo(torch.float32).tiny)

                # Backward projection
                c_flat = A_i.T @ e_flat

                # Multiplicative update
                theta_p_plus_1_flat = (theta_p.reshape(-1) / (normalization_factor.reshape(-1) + torch.finfo(torch.float32).tiny)) * c_flat
                theta_list[i] = theta_p_plus_1_flat.reshape(Z, X).to('cuda:0')

        if not isSavingEachIteration:
            return torch.stack(theta_list).mean(dim=0).cpu().numpy()
        else:
            return [theta.cpu().numpy() for theta in theta_list]

    @staticmethod
    @njit(parallel=True)
    def _forward_projection(SMatrix, theta_p, q_p):
        t_dim, z_dim, x_dim, i_dim = SMatrix.shape
        for _t in prange(t_dim):
            for _n in range(i_dim):
                total = 0.0
                for _z in range(z_dim):
                    for _x in range(x_dim):
                        total += SMatrix[_t, _z, _x, _n] * theta_p[_z, _x]
                q_p[_t, _n] = total

    @staticmethod
    @njit(parallel=True)
    def _backward_projection(SMatrix, e_p, c_p):
        t_dim, z_dim, x_dim, n_dim = SMatrix.shape
        for _z in prange(z_dim):
            for _x in range(x_dim):
                total = 0.0
                for _t in range(t_dim):
                    for _n in range(n_dim):
                        total += SMatrix[_t, _z, _x, _n] * e_p[_t, _n]
                c_p[_z, _x] = total

class AnalyticRecon(Recon):
    def __init__(self, analyticType, **kwargs):
        super().__init__(**kwargs)
        self.reconType = ReconType.Analytic
        self.analyticType = analyticType

    def run(self, processType = ProcessType.PYTHON, withTumor= True):
        """
        This method is a placeholder for the analytic reconstruction process.
        It currently does not perform any operations but serves as a template for future implementations.
        """
        if(processType == ProcessType.CASToR):
            raise NotImplementedError("CASToR analytic reconstruction is not implemented yet.")
        elif(processType == ProcessType.PYTHON):
            self._analyticReconPython(withTumor)
        else:
            raise ValueError(f"Unknown analytic reconstruction type: {processType}")

    def _analyticReconPython(self,withTumor):
        """
        This method is a placeholder for the analytic reconstruction process in Python.
        It currently does not perform any operations but serves as a template for future implementations.
        
        Parameters:
            analyticType: The type of analytic reconstruction to perform (default is iFOURIER).
        """
        if withTumor:
            if self.analyticType == AnalyticType.iFOURIER:
                self.reconPhantom = self._iFourierRecon(self.experiment.AOsignal_withTumor)
            elif self.analyticType == AnalyticType.iRADON:
                self.reconPhantom = self._iRadonRecon(self.experiment.AOsignal_withTumor)
            else:            
                raise ValueError(f"Unknown analytic type: {self.analyticType}")
        else:
            if self.analyticType == AnalyticType.iFOURIER:
                self.reconLaser = self._iFourierRecon(self.experiment.AOsignal_withoutTumor)
            elif self.analyticType == AnalyticType.iRADON:
                self.reconLaser = self._iRadonRecon(self.experiment.AOsignal_withoutTumor)
            else:            
                raise ValueError(f"Unknown analytic type: {self.analyticType}")
    
    def _iFourierRecon(self, AOsignal):
        """
        Reconstruction d'image utilisant la transformation de Fourier inverse.

        :param AOsignal: Signal dans le domaine temporel.
        :return: Image reconstruite dans le domaine spatial.
        """
        # Signal dans le domaine fréquentiel (FFT sur l'axe temporel)
        s_tilde = np.fft.fft(AOsignal, axis=0)

        theta = np.array([af.angle for af in self.experiment.AcousticFields])  # angles (N_theta,)
        f_s = np.array([af.f_s for af in self.experiment.AcousticFields])  # spatial freqs (N_theta,)
        f_t = np.fft.fftfreq(AOsignal.shape[0], d=self.experiment.dt)  # temporal freqs

        x = self.experiment.OpticImage.laser.x
        z = self.experiment.OpticImage.laser.z
        X, Z = np.meshgrid(x, z, indexing='ij')  # shape (Nx, Nz)

        N_theta = len(theta)
        I_rec = np.zeros((len(x), len(z)), dtype=complex)

        for i, th in enumerate(trange(N_theta, desc="AOT-BioMaps -- Analytic Recontruction Tomography : iFourier (Processing projection) ---- processing on single CPU ----")):
            fs = f_s[i]

            # Projection des coordonnées dans le repère tourné
            x_prime = X * np.cos(th) + Z * np.sin(th)
            z_prime = -X * np.sin(th) + Z * np.cos(th)

            # Signal spectral pour cet angle (1D pour chaque f_t)
            s_angle = s_tilde[:, i]  # shape (len(f_t),)

            # Grille 2D des fréquences
            F_t, F_s = np.meshgrid(f_t, [fs], indexing='ij')  # F_t: (len(f_t), 1), F_s: (1, 1)

            # Phase : exp(2iπ(x' f_s + z' f_t)) = (x_prime * f_s + z_prime * f_t)
            phase = 2j * np.pi * (x_prime[:, :, None] * fs + z_prime[:, :, None] * f_t[None, None, :])

            # reshape s_angle to (len(f_t), 1, 1)
            s_angle = s_angle[:, None, None]

            # Contribution de cet angle
            integrand = s_angle * np.exp(phase)

            # Intégration sur f_t (somme discrète)
            I_theta = np.sum(integrand, axis=0)

            # Ajout à la reconstruction
            I_rec += I_theta

        I_rec /= N_theta

        return np.abs(I_rec)

    def _iRadonRecon(self, AOsignal):
        """
        Reconstruction d'image utilisant la méthode iRadon.

        :return: Image reconstruite.
        """
        @staticmethod
        def trapz(y, x):
            """Compute the trapezoidal rule for integration."""
            return np.sum((y[:-1] + y[1:]) * (x[1:] - x[:-1]) / 2)

        # Initialisation de l'image reconstruite
        I_rec = np.zeros((len(self.experiment.OpticImage.laser.x), len(self.experiment.OpticImage.laser.z)), dtype=complex)

        # Transformation de Fourier du signal
        s_tilde = np.fft.fft(AOsignal, axis=0)

        # Extraction des angles et des fréquences spatiales
        theta = [acoustic_field.angle for acoustic_field in self.experiment.AcousticFields]
        f_s = [acoustic_field.f_s for acoustic_field in self.experiment.AcousticFields]

        # Calcul des coordonnées transformées et intégrales
        with trange(len(theta) * 2, desc="AOT-BioMaps -- Analytic Reconstruction Tomography: iRadon") as pbar:
            for i in range(len(theta)):
                pbar.set_description("AOT-BioMaps -- Analytic Reconstruction Tomography: iRadon (Processing frequency contributions)  ---- processing on single CPU ----")
                th = theta[i]
                x_prime = self.experiment.OpticImage.x[:, np.newaxis] * np.cos(th) - self.experiment.OpticImage.z[np.newaxis, :] * np.sin(th)
                z_prime = self.experiment.OpticImage.z[np.newaxis, :] * np.cos(th) + self.experiment.OpticImage.x[:, np.newaxis] * np.sin(th)

                # Première intégrale : partie réelle
                for j in range(len(f_s)):
                    fs = f_s[j]
                    integrand = s_tilde[i, j] * np.exp(2j * np.pi * (x_prime * fs + z_prime * fs))
                    integral = self.trapz(integrand * fs, fs)
                    I_rec += 2 * np.real(integral)
                pbar.update(1)

            for i in range(len(theta)):
                pbar.set_description("AOT-BioMaps -- Analytic Reconstruction Tomography: iRadon (Processing central contributions)  ---- processing on single CPU ----")
                th = theta[i]
                x_prime = self.experiment.OpticImage.x[:, np.newaxis] * np.cos(th) - self.experiment.OpticImage.z[np.newaxis, :] * np.sin(th)
                z_prime = self.experiment.OpticImage.z[np.newaxis, :] * np.cos(th) + self.experiment.OpticImage.x[:, np.newaxis] * np.sin(th)

                # Filtrer les fréquences spatiales pour ne garder que celles inférieures ou égales à f_s_max
                filtered_f_s = np.array([fs for fs in f_s if fs <= self.f_s_max])
                integrand = s_tilde[i, np.where(np.array(f_s) == 0)[0][0]] * np.exp(2j * np.pi * z_prime * filtered_f_s)
                integral = self.trapz(integrand * filtered_f_s, filtered_f_s)
                I_rec += integral
                pbar.update(1)

        return np.abs(I_rec)

class BayesianRecon(AlgebraicRecon):
    """
    This class implements the Bayesian reconstruction process.
    It currently does not perform any operations but serves as a template for future implementations.
    """
    def __init__(self, 
                potentialFunction, 
                isPenalizedLogLikelyHood = False,  
                beta=None, 
                delta=None, 
                gamma=None, 
                sigma=None,
                corner = (0.5-np.sqrt(2)/4)/np.sqrt(2),
                face = 0.5-np.sqrt(2)/4, 
                **kwargs):
        super().__init__(**kwargs)
        self.reconType = ReconType.Bayesian
        self.potentialFunction = potentialFunction
        self.isPenalizedLogLikelyHood = isPenalizedLogLikelyHood
        self.beta = beta           
        self.delta = delta          # typical value is 0.1
        self.gamma = gamma          # typical value is 0.01
        self.sigma = sigma          # typical value is 1.0
        self.corner = corner        # typical value is (0.5-np.sqrt(2)/4)/np.sqrt(2)
        self.face = face            # typical value is 0.5-np.sqrt(2)/4 
        

        if not isinstance(self.potentialFunction, PotentialType):
            raise TypeError(f"Potential functions must be of type PotentialType, got {type(self.potentialFunction)}")  

    def run(self, processType=ProcessType.PYTHON, withTumor=True):
        """
        This method is a placeholder for the Bayesian reconstruction process.
        It currently does not perform any operations but serves as a template for future implementations.
        """
        if(processType == ProcessType.CASToR):
            self._bayesianReconCASToR(withTumor)
        elif(processType == ProcessType.PYTHON):
            self._bayesianReconPython(withTumor)
        else:
            raise ValueError(f"Unknown Bayesian reconstruction type: {processType}")
        
    def _bayesianReconCASToR(self, withTumor):
        raise NotImplementedError("CASToR Bayesian reconstruction is not implemented yet.")

    def _bayesianReconPython(self, withTumor):

        acoustic_fields = []
        for i in trange(len(self.experiment.AcousticFields), desc="Generating system matrix (formating acoustic fields)"):
            ac_field = self.experiment.AcousticFields[i]
            acoustic_fields.append(ac_field.field)

        # Convertir la liste en un tableau numpy
        SMatrix = np.stack(acoustic_fields, axis=-1)

        if withTumor:
            if self.experiment.AOsignal_withTumor is None:
                raise ValueError("AO signal with tumor is not available. Please generate AO signal with tumor the experiment first in the experiment object.")
            if self.isPenalizedLogLikelyHood:
                self.reconPhantom = BayesianRecon._MAPEM_STOP(SMatrix=SMatrix, y=self.experiment.AOsignal_withTumor)
            else:
                self.reconPhantom = BayesianRecon._MAPEM(SMatrix=SMatrix, y=self.experiment.AOsignal_withTumor)
        else:
            if self.experiment.AOsignal_withoutTumor is None:
                raise ValueError("AO signal without tumor is not available. Please generate AO signal without tumor the experiment first in the experiment object.")
            if self.isPenalizedLogLikelyHood:
                self.reconLaser = BayesianRecon._MAPEM_STOP(SMatrix=SMatrix, y=self.experiment.AOsignal_withoutTumor)
            else:
                self.reconLaser = BayesianRecon._MAPEM(SMatrix=SMatrix, y=self.experiment.AOsignal_withoutTumor)

    # POTENTIAL FUNCTIONS

    @staticmethod
    @njit
    def _Omega_HUBER_PIECEWISE_CPU(theta_flat, index, values, delta):
        """
        Compute the gradient and Hessian of the Huber penalty function for sparse data.
        Parameters:
            theta_flat (torch.Tensor): Flattened parameter vector.
            index (torch.Tensor): Indices of the sparse matrix in COO format.
            values (torch.Tensor): Values of the sparse matrix in COO format.
            delta (float): Threshold for the Huber penalty.
        Returns:
            grad_U (torch.Tensor): Gradient of the penalty function.
            hess_U (torch.Tensor): Hessian of the penalty function.
            U_value (float): Value of the penalty function.
        """
        j_idx, k_idx = index
        diff = theta_flat[j_idx] - theta_flat[k_idx]
        abs_diff = np.abs(diff)

        # Huber penalty (potential function)
        psi_pair = np.where(abs_diff > delta,
                            delta * abs_diff - 0.5 * delta ** 2,
                            0.5 * diff ** 2)
        psi_pair = values * psi_pair

        # Huber gradient
        grad_pair = np.where(abs_diff > delta,
                             delta * np.sign(diff),
                             diff)
        grad_pair = values * grad_pair

        # Huber Hessian
        hess_pair = np.where(abs_diff > delta,
                             np.zeros_like(diff),
                             np.ones_like(diff))
        hess_pair = values * hess_pair

        grad_U = np.zeros_like(theta_flat)
        hess_U = np.zeros_like(theta_flat)

        np.add.at(grad_U, j_idx, grad_pair)
        np.add.at(hess_U, j_idx, hess_pair)

        # Total penalty energy
        U_value = 0.5 * np.sum(psi_pair)

        return grad_U, hess_U, U_value
    
    @staticmethod
    def _Omega_HUBER_PIECEWISE_GPU(theta_flat, index, values, delta):
        """
        Compute the gradient and Hessian of the Huber penalty function for sparse data.
        Parameters:
            theta_flat (torch.Tensor): Flattened parameter vector.
            index (torch.Tensor): Indices of the sparse matrix in COO format.
            values (torch.Tensor): Values of the sparse matrix in COO format.
            delta (float): Threshold for the Huber penalty.
        Returns:
            grad_U (torch.Tensor): Gradient of the penalty function.
            hess_U (torch.Tensor): Hessian of the penalty function.
            U_value (float): Value of the penalty function.
        """
        
        j_idx, k_idx = index
        diff = theta_flat[j_idx] - theta_flat[k_idx]
        abs_diff = torch.abs(diff)

        # Huber penalty (potential function) 
        psi_pair = torch.where(abs_diff > delta,
                            delta * abs_diff - 0.5 * delta ** 2,
                            0.5 * diff ** 2)
        psi_pair = values * psi_pair  

        # Huber gradient
        grad_pair = torch.where(abs_diff > delta,
                                delta * torch.sign(diff),
                                diff)
        grad_pair = values * grad_pair

        # Huber Hessian
        hess_pair = torch.where(abs_diff > delta,
                                torch.zeros_like(diff),
                                torch.ones_like(diff))
        hess_pair = values * hess_pair

        grad_U = scatter(grad_pair, j_idx, dim=0, dim_size=theta_flat.shape[0], reduce='sum')
        hess_U = scatter(hess_pair, j_idx, dim=0, dim_size=theta_flat.shape[0], reduce='sum')

        # Total penalty energy
        U_value = 0.5 * psi_pair.sum()  

        return grad_U, hess_U, U_value
    
    @staticmethod
    @njit
    def _Omega_RELATIVE_DIFFERENCE_CPU(theta_flat, index, values, gamma):
        j_idx, k_idx = index
        theta_j = theta_flat[j_idx]
        theta_k = theta_flat[k_idx]
        diff = theta_k - theta_j
        abs_diff = np.abs(diff)

        denom = theta_k + theta_j + gamma * abs_diff + 1e-8
        num = diff ** 2

        # First derivative ∂U/∂θ_j
        dpsi = (2 * diff * denom - num * (1 + gamma * np.sign(diff))) / (denom ** 2)
        grad_pair = values * (-dpsi)  # Note the negative sign: U contains ψ(θ_k, θ_j), seeking ∂/∂θ_j

        # Second derivative ∂²U/∂θ_j² (numerically stable, approximate treatment)
        d2psi = (2 * denom ** 2 - 4 * diff * denom * (1 + gamma * np.sign(diff))
                 + 2 * num * (1 + gamma * np.sign(diff)) ** 2) / (denom ** 3 + 1e-8)
        hess_pair = values * d2psi

        grad_U = np.zeros_like(theta_flat)
        hess_U = np.zeros_like(theta_flat)

        np.add.at(grad_U, j_idx, grad_pair)
        np.add.at(hess_U, j_idx, hess_pair)

        return grad_U, hess_U
    
    @staticmethod
    def _Omega_RELATIVE_DIFFERENCE_GPU(theta_flat, index, values, gamma):
        j_idx, k_idx = index
        theta_j = theta_flat[j_idx]
        theta_k = theta_flat[k_idx]
        diff = theta_k - theta_j
        abs_diff = torch.abs(diff)

        denom = theta_k + theta_j + gamma * abs_diff + 1e-8
        num = diff ** 2

        dpsi = (2 * diff * denom - num * (1 + gamma * torch.sign(diff))) / (denom ** 2)
        grad_pair = values * (-dpsi) 

        d2psi = (2 * denom ** 2 - 4 * diff * denom * (1 + gamma * torch.sign(diff))
                + 2 * num * (1 + gamma * torch.sign(diff)) ** 2) / (denom ** 3 + 1e-8)
        hess_pair = values * d2psi

        grad_U = scatter(grad_pair, j_idx, dim=0, dim_size=theta_flat.shape[0], reduce='sum')
        hess_U = scatter(hess_pair, j_idx, dim=0, dim_size=theta_flat.shape[0], reduce='sum')

        return grad_U, hess_U
    
    @staticmethod
    @njit
    def _Omega_QUADRATIC_CPU(theta_flat, j_idx, k_idx, values, sigma=1.0):
        """
        Optimized CPU implementation of the quadratic potential using Numba.

        Parameters:
            theta_flat (np.ndarray): shape (J,)
            j_idx (np.ndarray): indices j (shape N_edges,)
            k_idx (np.ndarray): indices k (shape N_edges,)
            values (np.ndarray): edge weights (shape N_edges,)
            sigma (float): standard deviation (scalar)

        Returns:
            grad_U (np.ndarray): shape (J,)
            hess_U (np.ndarray): shape (J,)
            U_value (float): scalar
        """
        n_nodes = theta_flat.shape[0]
        n_edges = j_idx.shape[0]

        grad_U = np.zeros(n_nodes)
        hess_U = np.zeros(n_nodes)
        U_value = 0.0

        for i in range(n_edges):
            j = j_idx[i]
            k = k_idx[i]
            v = values[i]
            diff = theta_flat[j] - theta_flat[k]

            psi = 0.5 * (diff / sigma) ** 2
            psi *= v
            U_value += psi

            grad = -v * diff / sigma**2
            hess = v / sigma**2

            grad_U[j] += grad
            hess_U[j] += hess

        U_value *= 0.5
        return grad_U, hess_U, U_value

    @staticmethod
    def _Omega_QUADRATIC_GPU(theta_flat, index, values, sigma=1.0):
        """
        GPU implementation of the quadratic potential function, gradient and Hessian.
        
        Parameters:
            theta_flat (torch.Tensor): (J,) tensor on GPU
            index (Tuple[torch.Tensor, torch.Tensor]): (j_idx, k_idx), indices of adjacent pixels
            values (torch.Tensor): (N_edges,) weights, typically 1 or distance-based
            sigma (float): smoothness hyperparameter
            
        Returns:
            grad_U (torch.Tensor): gradient of the potential function, shape (J,)
            hess_U (torch.Tensor): diagonal of the Hessian, shape (J,)
            U_value (torch.Tensor): scalar, energy
        """
        j_idx, k_idx = index
        diff = theta_flat[j_idx] - theta_flat[k_idx]

        # Energy term (potential ψ)
        psi_pair = 0.5 * (diff / sigma) ** 2
        psi_pair = values * psi_pair

        # Gradient ∂ψ/∂θ_j = -(θ_k - θ_j) / σ^2
        grad_pair = values * (-diff / sigma**2)

        # Hessian ∂²ψ/∂θ_j² = 1 / σ² (constant per edge)
        hess_pair = values * (1.0 / sigma**2)

        # Initialize zero tensors on GPU
        grad_U = torch.zeros_like(theta_flat)
        hess_U = torch.zeros_like(theta_flat)

        # Aggregate contributions (scatter equivalent)
        grad_U = grad_U.index_add(0, j_idx, grad_pair)
        hess_U = hess_U.index_add(0, j_idx, hess_pair)

        # Total energy U(θ)
        U_value = 0.5 * psi_pair.sum()

        return grad_U, hess_U, U_value
    
    


        # GRADIENT AND HESSIAN COMPUTATION

    @staticmethod
    @njit
    def _build_adjacency_sparse_CPU(Z, X,corner = (0.5-np.sqrt(2)/4)/np.sqrt(2),face = 0.5-np.sqrt(2)/4):
        rows = []
        cols = []
        weights = []

        for z in range(Z):
            for x in range(X):
                j = z * X + x
                for dz in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        if dz == 0 and dx == 0:
                            continue
                        nz, nx = z + dz, x + dx
                        if 0 <= nz < Z and 0 <= nx < X:
                            k = nz * X + nx
                            weight = corner if abs(dz) + abs(dx) == 2 else face
                            rows.append(j)
                            cols.append(k)
                            weights.append(weight)

        index = (np.array(rows), np.array(cols))
        values = np.array(weights, dtype=np.float32)
        return index, values 
    
    @staticmethod
    def _build_adjacency_sparse_GPU(Z, X,corner = (0.5-np.sqrt(2)/4)/np.sqrt(2),face = 0.5-np.sqrt(2)/4):
        rows = []
        cols = []
        weights = []

        for z in range(Z):
            for x in range(X):
                j = z * X + x
                for dz in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        if dz == 0 and dx == 0:
                            continue
                        nz, nx = z + dz, x + dx
                        if 0 <= nz < Z and 0 <= nx < X:
                            k = nz * X + nx
                            weight = corner if abs(dz) + abs(dx) == 2 else face
                            rows.append(j)
                            cols.append(k)
                            weights.append(weight)
    
        index = torch.tensor([rows, cols], device= config.select_best_gpu())
        values = torch.tensor(weights, dtype=torch.float32, device= config.select_best_gpu())
        index, values = coalesce(index, values, m=Z*X, n=Z*X)
        return index, values 

    def _MAPEM_STOP(self, SMatrix, y):

        if self.isGPU and self.isMultiGPU:
            warnings.warn("Multi-GPU MAPEM_STOP is not implemented yet. Falling back to single GPU.")
            try:
                return BayesianRecon._MAPEM_GPU_STOP(SMatrix= SMatrix, y = y, Omega=self.potentialFunction, iteration=self.numIterations, beta=self.beta, delta=self.delta, gamma=self.gamma, sigma=self.sigma, isSavingEachIteration=self.isSavingEachIteration)
            except:
                warnings.warn("Falling back to CPU implementation due to an error in GPU implementation.")
                return BayesianRecon._MAPEM_CPU_STOP(SMatrix= SMatrix, y = y, Omega=self.potentialFunction, iteration=self.numIterations, beta=self.beta, delta=self.delta, gamma=self.gamma, sigma=self.sigma, isSavingEachIteration=self.isSavingEachIteration)
        if self.isGPU and not self.isMultiGPU:
            try:
                return BayesianRecon._MAPEM_GPU_STOP(SMatrix= SMatrix, y = y, Omega=self.potentialFunction, iteration=self.numIterations, beta=self.beta, delta=self.delta, gamma=self.gamma, sigma=self.sigma, isSavingEachIteration=self.isSavingEachIteration)
            except:
                warnings.warn("Falling back to CPU implementation due to an error in GPU implementation.")
                return BayesianRecon._MAPEM_CPU_STOP(SMatrix= SMatrix, y = y, Omega=self.potentialFunction, iteration=self.numIterations, beta=self.beta, delta=self.delta, gamma=self.gamma, sigma=self.sigma, isSavingEachIteration=self.isSavingEachIteration)
        if not self.isGPU and self.isMultiCPU:
            warnings.warn("Multi-CPU MAPEM_STOP is not implemented yet. Falling back to single CPU.")
            return BayesianRecon._MAPEM_CPU_STOP(SMatrix= SMatrix, y = y, Omega=self.potentialFunction, iteration=self.numIterations, beta=self.beta, delta=self.delta, gamma=self.gamma, sigma=self.sigma, isSavingEachIteration=self.isSavingEachIteration)
        if not self.isGPU and not self.isMultiCPU:
            return BayesianRecon._MAPEM_CPU_STOP(SMatrix= SMatrix, y = y, Omega=self.potentialFunction, iteration=self.numIterations, beta=self.beta, delta=self.delta, gamma=self.gamma, sigma=self.sigma, isSavingEachIteration=self.isSavingEachIteration)
        
    def _MAPEM(self, SMatrix, y):
        
        if self.isGPU and self.isMultiGPU:
            warnings.warn("Multi-GPU MAPEM_STOP is not implemented yet. Falling back to single GPU.")
            try:
                return BayesianRecon._MAPEM_GPU(SMatrix= SMatrix, y = y, Omega=self.potentialFunction, iteration=self.numIterations ,beta=self.beta, delta=self.delta, gamma=self.gamma, sigma=self.sigma, isSavingEachIteration=self.isSavingEachIteration)
            except:
                warnings.warn("Falling back to CPU implementation due to an error in GPU implementation.")
                return BayesianRecon._MAPEM_CPU(SMatrix= SMatrix, y = y, Omega=self.potentialFunction, iteration=self.numIterations, beta=self.beta, delta=self.delta, gamma=self.gamma, sigma=self.sigma, isSavingEachIteration=self.isSavingEachIteration)
        if self.isGPU and not self.isMultiGPU:
            try:
                return BayesianRecon._MAPEM_GPU(SMatrix= SMatrix, y = y, Omega=self.potentialFunction, iteration=self.numIterations, beta=self.beta, delta=self.delta, gamma=self.gamma, sigma=self.sigma, isSavingEachIteration=self.isSavingEachIteration)
            except:
                warnings.warn("Falling back to CPU implementation due to an error in GPU implementation.")
                return BayesianRecon._MAPEM_CPU(SMatrix= SMatrix, y = y, Omega=self.potentialFunction, iteration=self.numIterations, beta=self.beta, delta=self.delta, gamma=self.gamma, sigma=self.sigma, isSavingEachIteration=self.isSavingEachIteration)
        if not self.isGPU and self.isMultiCPU:
            warnings.warn("Multi-CPU MAPEM_STOP is not implemented yet. Falling back to single CPU.")
            return BayesianRecon._MAPEM_CPU(SMatrix= SMatrix, y = y, Omega=self.potentialFunction, iteration=self.numIterations, beta=self.beta, delta=self.delta, gamma=self.gamma, sigma=self.sigma, isSavingEachIteration=self.isSavingEachIteration)
        if not self.isGPU and not self.isMultiCPU:
            return BayesianRecon._MAPEM_CPU(SMatrix= SMatrix, y = y, Omega=self.potentialFunction, iteration=self.numIterations, beta=self.beta, delta=self.delta, gamma=self.gamma, sigma=self.sigma, isSavingEachIteration=self.isSavingEachIteration)
        
    @staticmethod
    def _MAPEM_CPU_STOP(SMatrix, y, Omega, numIteration, beta, delta, gamma, sigma, previous=-np.inf, isSavingEachIteration=False):
        """
        MAPEM version CPU simple - sans GPU - torch uniquement
        """
        if Omega is not isinstance(Omega, PotentialType):
            raise TypeError(f"Omega must be of type PotentialType, got {type(Omega)}")

        if Omega == PotentialType.RELATIVE_DIFFERENCE:
            if gamma == None:
                raise ValueError("gamma must be specified for RELATIVE_DIFFERENCE potential type. Please find the value in the paper.")
            if beta == None:
                raise ValueError("beta must be specified for RELATIVE_DIFFERENCE potential type. Please find the value in the paper.")
        elif Omega == PotentialType.HUBER_PIECEWISE:
            if delta == None:
                raise ValueError("delta must be specified for HUBER_PIECEWISE potential type. Please find the value in the paper.")
            if beta == None:
                raise ValueError("beta must be specified for HUBER_PIECEWISE potential type. Please find the value in the paper.") 
        elif Omega == PotentialType.QUADRATIC:
            if sigma == None:
                raise ValueError("sigma must be specified for QUADRATIC potential type. Please find the value in the paper.")
        else:
            raise ValueError(f"Unknown potential type: {Omega}")
        
        SMatrix = torch.tensor(SMatrix, dtype=torch.float32)
        y_tensor = torch.tensor(y, dtype=torch.float32)

        T, Z, X, N = SMatrix.shape
        A_flat = SMatrix.permute(0, 3, 1, 2).reshape(T * N, Z * X)
        y_flat = y_tensor.reshape(-1)

        I_0 = torch.ones((Z, X), dtype=torch.float32)
        theta_list = [I_0]
        results = [I_0.numpy()]

        normalization_factor = SMatrix.sum(dim=(0, 3)).reshape(-1)
        adj_index, adj_values = BayesianRecon._build_adjacency_sparse_CPU(Z, X)

        if Omega == PotentialType.RELATIVE_DIFFERENCE:
                description = f"AOT-BioMaps -- Bayesian Recontruction Tomography : MAP-EM (Sparse RD β:{beta:.4f}, δ:{delta:4f})+ STOP condtion (penalized log-likelihood) ---- processing on single CPU ----"
        elif Omega == PotentialType.HUBER_PIECEWISE:
                description = f"AOT-BioMaps -- Bayesian Recontruction Tomography : MAP-EM (Sparse HUBER β:{beta:.4f}, γ:{gamma:4f})+ STOP condtion (penalized log-likelihood) ---- processing on single CPU ----"
        elif Omega == PotentialType.QUADRATIC:
                description = f"AOT-BioMaps -- Bayesian Recontruction Tomography : MAP-EM (Sparse QUADRATIC σ:{sigma:.4f})+ STOP condtion (penalized log-likelihood) ---- processing on single CPU ----"

        for p in trange(numIteration, desc=description):
            theta_p = theta_list[-1]
            theta_p_flat = theta_p.reshape(-1)

            q_flat = A_flat @ theta_p_flat
            e_flat = (y_flat - q_flat) / (q_flat + torch.finfo(torch.float32).tiny)
            c_flat = A_flat.T @ e_flat

            if Omega == PotentialType.RELATIVE_DIFFERENCE:
                grad_U, hess_U, U_value = BayesianRecon._Omega_RELATIVE_DIFFERENCE_CPU(theta_p_flat, adj_index, adj_values, delta)
            elif Omega == PotentialType.HUBER_PIECEWISE:
                grad_U, hess_U, U_value = BayesianRecon._Omega_HUBER_PIECEWISE_CPU(theta_p_flat, adj_index, adj_values, gamma)
            elif Omega == PotentialType.QUADRATIC:
                grad_U, hess_U, U_value = BayesianRecon._Omega_QUADRATIC_CPU(theta_p_flat, adj_index, adj_values, sigma)

            denom = normalization_factor + theta_p_flat * beta * hess_U
            num = theta_p_flat * (c_flat - beta * grad_U)

            theta_next_flat = theta_p_flat + num / (denom + torch.finfo(torch.float32).tiny)
            theta_next_flat = torch.clamp(theta_next_flat, min=0)
            theta_next = theta_next_flat.reshape(Z, X)

            theta_list[-1] = theta_next
            results.append(theta_next.numpy())

            log_likelihood = (y_flat * torch.log(q_flat + 1e-8) - (q_flat + 1e-8)).sum()
            penalized_log_likelihood = log_likelihood - beta * U_value
            current = penalized_log_likelihood.item()

            if (p + 1) % 100 == 0:
                print(f"Iter {p+1}: logL={log_likelihood:.3e}, U={U_value:.3e}, penalized logL={penalized_log_likelihood:.3e}")
                if current <= previous:
                    nb_false_successive += 1
                else:
                    nb_false_successive = 0
                previous = current

                # Optionally add early stop:
                # if nb_false_successive >= 25:
                #     break

        if isSavingEachIteration:
            return results[-1]
        else:
            return results  

    @staticmethod  
    def _MAPEM_GPU_STOP(SMatrix, y, Omega, numIteration, beta, delta, gamma, sigma, previous = -np.inf, isSavingEachIteration=False):
        """
        Maximum A Posteriori (MAP) estimation for Bayesian reconstruction.
        This method computes the MAP estimate of the parameters given the data.
        """

        if Omega is not isinstance(Omega, PotentialType):
            raise TypeError(f"Omega must be of type PotentialType, got {type(Omega)}")

        if Omega == PotentialType.RELATIVE_DIFFERENCE:
            if gamma == None:
                raise ValueError("gamma must be specified for RELATIVE_DIFFERENCE potential type. Please find the value in the paper.")
            if beta == None:
                raise ValueError("beta must be specified for RELATIVE_DIFFERENCE potential type. Please find the value in the paper.")
        elif Omega == PotentialType.HUBER_PIECEWISE:
            if delta == None:
                raise ValueError("delta must be specified for HUBER_PIECEWISE potential type. Please find the value in the paper.")
            if beta == None:
                raise ValueError("beta must be specified for HUBER_PIECEWISE potential type. Please find the value in the paper.") 
        elif Omega == PotentialType.QUADRATIC:
            if sigma == None:
                raise ValueError("sigma must be specified for QUADRATIC potential type. Please find the value in the paper.")
        else:
            raise ValueError(f"Unknown potential type: {Omega}")

        device = torch.device(f"cuda:{config.select_best_gpu()}")

        A_matrix_torch = torch.tensor(SMatrix, dtype=torch.float32).to(device)
        y_torch = torch.tensor(y, dtype=torch.float32).to(device)

        T, Z, X, N = SMatrix.shape
        J = Z * X

        A_flat = A_matrix_torch.permute(0, 3, 1, 2).reshape(T * N, Z * X)
        y_flat = y_torch.reshape(-1)

        I_0 = torch.ones((Z, X), dtype=torch.float32, device=device)
        matrix_theta_torch = []
        matrix_theta_torch = [I_0]
        matrix_theta_from_gpu_MAPEM = []
        matrix_theta_from_gpu_MAPEM = [I_0.cpu().numpy()]

        normalization_factor = A_matrix_torch.sum(dim=(0, 3))                # (Z, X)
        normalization_factor_flat = normalization_factor.reshape(-1)         # (Z*X,)

        adj_index, adj_values = BayesianRecon._build_adjacency_sparse_GPU(Z, X)

        
        if Omega == PotentialType.RELATIVE_DIFFERENCE:
                description = f"AOT-BioMaps -- Bayesian Recontruction Tomography : MAP-EM (Sparse RD β:{beta:.4f}, δ:{delta:4f})+ STOP condtion (penalized log-likelihood) ---- processing on single GPU no.{torch.cuda.current_device()} ----"
        elif Omega == PotentialType.HUBER_PIECEWISE:
                description = f"AOT-BioMaps -- Bayesian Recontruction Tomography : MAP-EM (Sparse HUBER β:{beta:.4f}, γ:{gamma:4f})+ STOP condtion (penalized log-likelihood) ---- processing on single GPU no.{torch.cuda.current_device()} ----"
        elif Omega == PotentialType.QUADRATIC:
                description = f"AOT-BioMaps -- Bayesian Recontruction Tomography : MAP-EM (Sparse QUADRATIC σ:{sigma:.4f})+ STOP condtion (penalized log-likelihood) ---- processing on single GPU no.{torch.cuda.current_device()} ----"

        for p in trange(numIteration, desc=description):
            theta_p = matrix_theta_torch[-1]
            theta_p_flat = theta_p.reshape(-1)

            q_flat = A_flat @ theta_p_flat
            e_flat = (y_flat - q_flat) / (q_flat + torch.finfo(torch.float32).tiny)
            c_flat = A_flat.T @ e_flat

            if Omega == PotentialType.RELATIVE_DIFFERENCE:
                    grad_U, hess_U, U_value = BayesianRecon._Omega_RELATIVE_DIFFERENCE_CPU(theta_p_flat, adj_index, adj_values, delta)
            elif Omega == PotentialType.HUBER_PIECEWISE:
                    grad_U, hess_U, U_value = BayesianRecon._Omega_HUBER_PIECEWISE_CPU(theta_p_flat, adj_index, adj_values, gamma)
            elif Omega == PotentialType.QUADRATIC:
                    grad_U, hess_U, U_value = BayesianRecon._Omega_QUADRATIC_CPU(theta_p_flat, adj_index, adj_values, sigma)
            else:
                raise ValueError(f"Unknown potential type: {Omega}")
            
            denom = normalization_factor_flat + theta_p_flat * beta * hess_U
            num = theta_p_flat * (c_flat - beta * grad_U)

            theta_p_plus_1_flat = theta_p_flat + num / (denom + torch.finfo(torch.float32).tiny)
            theta_p_plus_1_flat = torch.clamp(theta_p_plus_1_flat, min=0)

            theta_next = theta_p_plus_1_flat.reshape(Z, X)
            #matrix_theta_torch.append(theta_next) # save theta in GPU
            matrix_theta_torch[-1] = theta_next    # do not save theta in GPU

            if p % 1 == 0:
                matrix_theta_from_gpu_MAPEM.append(theta_next.cpu().numpy())

            # === compute penalized log-likelihood (without term ln(m_i !) inside) ===
            # log-likelihood (without term ln(m_i !) inside)
            # log_likelihood = (torch.where(q_flat > 0, y_flat * torch.log(q_flat), torch.zeros_like(q_flat)) - q_flat).sum()
            # log_likelihood = (y_flat * torch.log(q_flat) - q_flat).sum()
            log_likelihood = (y_flat * ( torch.log( q_flat + torch.finfo(torch.float32).tiny ) ) - (q_flat + torch.finfo(torch.float32).tiny)).sum()

            # penalized log-likelihood
            penalized_log_likelihood = log_likelihood - beta * U_value

            if p == 0 or (p+1) % 100 == 0:
                current = penalized_log_likelihood.item()

                if current<=previous:
                    nb_false_successive = nb_false_successive + 1

                else:
                    nb_false_successive = 0
                
                print(f"Iter {p+1}: lnL without term ln(m_i !) inside={log_likelihood.item():.8e}, Gibbs energy function U={U_value.item():.4e}, penalized lnL without term ln(m_i !) inside={penalized_log_likelihood.item():.8e}, p lnL (current {current:.8e} - previous {previous:.8e} > 0)={(current-previous>0)}, nb_false_successive={nb_false_successive}")
                
                #if nb_false_successive >= 25:
                    #break
            
                previous = penalized_log_likelihood.item()
        if isSavingEachIteration:
            return matrix_theta_from_gpu_MAPEM[-1]
        else:
            return matrix_theta_from_gpu_MAPEM

    @staticmethod
    def _MAPEM_CPU(SMatrix, y, Omega, numIteration, beta, delta, gamma, sigma, isSavingEachIteration=False):
        if not isinstance(Omega, PotentialType):
            raise TypeError(f"Omega must be of type PotentialType, got {type(Omega)}")

        if Omega == PotentialType.RELATIVE_DIFFERENCE:
            if gamma is None or beta is None:
                raise ValueError("gamma and beta must be specified for RELATIVE_DIFFERENCE.")
        elif Omega == PotentialType.HUBER_PIECEWISE:
            if delta is None or beta is None:
                raise ValueError("delta and beta must be specified for HUBER_PIECEWISE.")
        elif Omega == PotentialType.QUADRATIC:
            if sigma is None:
                raise ValueError("sigma must be specified for QUADRATIC.")
        else:
            raise ValueError(f"Unknown potential type: {Omega}")

        T, Z, X, N = SMatrix.shape
        J = Z * X

        A_flat = np.transpose(SMatrix, (0, 3, 1, 2)).reshape(T * N, Z * X)
        y_flat = y.reshape(-1)

        theta_0 = np.ones((Z, X), dtype=np.float32)
        matrix_theta_np = [theta_0]
        I_reconMatrix = [theta_0.copy()]

        normalization_factor = SMatrix.sum(axis=(0, 3))
        normalization_factor_flat = normalization_factor.reshape(-1)

        j_idx, k_idx, values = BayesianRecon._build_adjacency_sparse_CPU(Z, X)

        if Omega == PotentialType.RELATIVE_DIFFERENCE:
            description = f"AOT-BioMaps -- Bayesian Recontruction Tomography : MAP-EM (Sparse RD β:{beta:.4f}, δ:{delta:4f}) ---- processing on single CPU ----"
        elif Omega == PotentialType.HUBER_PIECEWISE:
            description = f"AOT-BioMaps -- Bayesian Recontruction Tomography : MAP-EM (Sparse HUBER β:{beta:.4f}, γ:{gamma:4f}) ---- processing on single CPU ----"
        elif Omega == PotentialType.QUADRATIC:
            description = f"AOT-BioMaps -- Bayesian Recontruction Tomography : MAP-EM (Sparse QUADRATIC σ:{sigma:.4f}) ---- processing on single CPU ----"

        for p in trange(numIteration, desc=description):
            theta_p = matrix_theta_np[-1]
            theta_p_flat = theta_p.reshape(-1)

            q_flat = A_flat @ theta_p_flat
            e_flat = (y_flat - q_flat) / (q_flat + np.finfo(np.float32).tiny)
            c_flat = A_flat.T @ e_flat

            if Omega == PotentialType.RELATIVE_DIFFERENCE:
                grad_U, hess_U, _ = BayesianRecon._Omega_RELATIVE_DIFFERENCE_CPU(theta_p_flat, j_idx, k_idx, values, delta)
            elif Omega == PotentialType.HUBER_PIECEWISE:
                grad_U, hess_U, _ = BayesianRecon._Omega_HUBER_PIECEWISE_CPU(theta_p_flat, j_idx, k_idx, values, gamma)
            elif Omega == PotentialType.QUADRATIC:
                grad_U, hess_U, _ = BayesianRecon._Omega_QUADRATIC_CPU(theta_p_flat, j_idx, k_idx, values, sigma)

            denom = normalization_factor_flat + theta_p_flat * beta * hess_U
            num = theta_p_flat * (c_flat - beta * grad_U)

            theta_p_plus_1_flat = theta_p_flat + num / (denom + np.finfo(np.float32).tiny)
            theta_p_plus_1_flat = np.clip(theta_p_plus_1_flat, 0, None)

            theta_next = theta_p_plus_1_flat.reshape(Z, X)
            matrix_theta_np.append(theta_next)


            if p % 1 == 0:
                I_reconMatrix.append(theta_next.copy())

        if isSavingEachIteration:
            return I_reconMatrix
        else:
            return I_reconMatrix[-1]

    @staticmethod
    def _MAPEM_GPU(SMatrix, y, Omega, numIteration, beta, delta, gamma, sigma, isSavingEachIteration=False):
        '''
        Maximum A Posteriori (MAP) estimation for Bayesian reconstruction using GPU.
        This method computes the MAP estimate of the parameters given the data.
        Parameters:
            SMatrix (numpy.ndarray): The system matrix of shape (T, Z, X, N).
            y (numpy.ndarray): The observed data of shape (T, N).
            Omega (PotentialType): The potential function to use for regularization.
            iteration (int): The number of iterations for the MAP-EM algorithm.
        Returns:
            matrix_theta_from_gpu_MAPEM (list): A list of numpy arrays containing the estimated parameters at each iteration.
            '''
        
        if Omega is not isinstance(Omega, PotentialType):
            raise TypeError(f"Omega must be of type PotentialType, got {type(Omega)}")

        if Omega == PotentialType.RELATIVE_DIFFERENCE:
            if gamma == None:
                raise ValueError("gamma must be specified for RELATIVE_DIFFERENCE potential type. Please find the value in the paper.")
            if beta == None:
                raise ValueError("beta must be specified for RELATIVE_DIFFERENCE potential type. Please find the value in the paper.")
        elif Omega == PotentialType.HUBER_PIECEWISE:
            if delta == None:
                raise ValueError("delta must be specified for HUBER_PIECEWISE potential type. Please find the value in the paper.")
            if beta == None:
                raise ValueError("beta must be specified for HUBER_PIECEWISE potential type. Please find the value in the paper.") 
        elif Omega == PotentialType.QUADRATIC:
            if sigma == None:
                raise ValueError("sigma must be specified for QUADRATIC potential type. Please find the value in the paper.")
        else:
            raise ValueError(f"Unknown potential type: {Omega}")

        device = torch.device(f"cuda:{config.select_best_gpu()}")

        A_matrix_torch = torch.tensor(SMatrix, dtype=torch.float32).to(device)
        y_torch = torch.tensor(y, dtype=torch.float32).to(device)

        T, Z, X, N = SMatrix.shape
        J = Z * X

        A_flat = A_matrix_torch.permute(0, 3, 1, 2).reshape(T * N, Z * X)
        y_flat = y_torch.reshape(-1)

        theta_0 = torch.ones((Z, X), dtype=torch.float32, device=device)
        matrix_theta_torch = []
        matrix_theta_torch = [theta_0]
        I_reconMatrix = []
        matrix_theta_from_gpu_MAPEM = [theta_0.cpu().numpy()]

        normalization_factor = A_matrix_torch.sum(dim=(0, 3))                # (Z, X)
        normalization_factor_flat = normalization_factor.reshape(-1)         # (Z*X,)

        adj_index, adj_values = BayesianRecon._build_adjacency_sparse(Z, X)

        if Omega == PotentialType.RELATIVE_DIFFERENCE:
            description = f"AOT-BioMaps -- Bayesian Recontruction Tomography : MAP-EM (Sparse RD β:{beta:.4f}, δ:{delta:4f}) ---- processing on single GPU no.{torch.cuda.current_device()} ----"
        elif Omega == PotentialType.HUBER_PIECEWISE:
            description = f"AOT-BioMaps -- Bayesian Recontruction Tomography : MAP-EM (Sparse HUBER β:{beta:.4f}, γ:{gamma:4f}) ---- processing on single GPU no.{torch.cuda.current_device()} ----"
        elif Omega == PotentialType.QUADRATIC:
            description = f"AOT-BioMaps -- Bayesian Recontruction Tomography : MAP-EM (Sparse QUADRATIC σ:{sigma:.4f}) ---- processing on single GPU no.{torch.cuda.current_device()} ----"

        for p in trange(numIteration, desc=description):
            theta_p = matrix_theta_torch[-1]
            theta_p_flat = theta_p.reshape(-1)

            q_flat = A_flat @ theta_p_flat
            e_flat = (y_flat - q_flat) / (q_flat + torch.finfo(torch.float32).tiny)
            c_flat = A_flat.T @ e_flat
            
            if Omega == PotentialType.RELATIVE_DIFFERENCE:
                    grad_U, hess_U, _ = BayesianRecon._Omega_RELATIVE_DIFFERENCE_GPU(theta_p_flat, adj_index, adj_values, delta=delta)
            elif Omega == PotentialType.HUBER_PIECEWISE:
                    grad_U, hess_U, _ = BayesianRecon._Omega_HUBER_PIECEWISE_GPU(theta_p_flat, adj_index, adj_values, gamma=gamma)
            elif Omega == PotentialType.QUADRATIC:
                    grad_U, hess_U, _ = BayesianRecon._Omega_QUADRATIC_GPU(theta_p_flat, adj_index, adj_values, sigma=sigma)
            else:
                raise ValueError(f"Unknown potential type: {Omega}")

            denom = normalization_factor_flat + theta_p_flat * beta * hess_U
            num = theta_p_flat * (c_flat - beta * grad_U)

            theta_p_plus_1_flat = theta_p_flat + num / (denom + torch.finfo(torch.float32).tiny)
            theta_p_plus_1_flat = torch.clamp(theta_p_plus_1_flat, min=0)

            theta_next = theta_p_plus_1_flat.reshape(Z, X)
            matrix_theta_torch.append(theta_next) # save theta in GPU

            if p % 1 == 0:
                I_reconMatrix.append(theta_next.cpu().numpy())   

        if isSavingEachIteration:
            return I_reconMatrix
        else:
            return I_reconMatrix[-1]

class ConvexRecon(Recon):
    """
    This class implements the convex reconstruction process.
    It currently does not perform any operations but serves as a template for future implementations.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.reconType = ReconType.Convex

    def run(self, processType=ProcessType.PYTHON):
        """
        This method is a placeholder for the convex reconstruction process.
        It currently does not perform any operations but serves as a template for future implementations.
        """
        if(processType == ProcessType.CASToR):
            self._convexReconCASToR()
        elif(processType == ProcessType.PYTHON):
            self._convexReconPython()
        else:
            raise ValueError(f"Unknown convex reconstruction type: {processType}")

    def _convexReconCASToR(self):
        pass

    def _convexReconPython(self):
        pass

    @staticmethod
    def prox_l1_CPU(v, alpha):
        return np.sign(v) * np.maximum(np.abs(v) - alpha, 0)

    @staticmethod
    def prox_l2_CPU(v, sigma):
        return v / (1 + sigma)

    @staticmethod
    def gradient_operator_CPU(lambda_):
        # Implémentez l'opérateur gradient ici
        return np.gradient(lambda_)

    @staticmethod
    def divergence_operator_CPU(u):
        # Implémentez l'opérateur divergence ici
        return -np.gradient(u[0]) - np.gradient(u[1])
    
    @staticmethod
    def prox_l1_GPU(v, alpha):
        return torch.sign(v) * torch.clamp(torch.abs(v) - alpha, min=0)

    @staticmethod
    def prox_l2_GPU(v, sigma):
        return v / (1 + sigma)

    @staticmethod
    def gradient_operator_GPU(lambda_):
        # Implémentez l'opérateur gradient ici
        grad_x = torch.gradient(lambda_, dim=0)[0]
        grad_y = torch.gradient(lambda_, dim=1)[0]
        return torch.stack((grad_x, grad_y), dim=0)

    @staticmethod
    def divergence_operator_GPU(u):
        # Implémentez l'opérateur divergence ici
        div = -torch.gradient(u[0], dim=0)[0] - torch.gradient(u[1], dim=1)[0]
        return div
    
    @staticmethod
    def primal_dual_chambolle_pock_CPU(A, y, alpha, tau, sigma, theta, iterations):
        # Initialisation
        lambda_ = np.zeros((A.shape[1], 1))
        u = np.zeros((2, A.shape[1], 1))

        for _ in trange(iterations):
            # Mise à jour de lambda
            lambda_new = ConvexRecon.prox_l1_CPU(lambda_ - tau * A.T @ (A @ lambda_ - y), tau * alpha)

            # Mise à jour de u
            u_new = u + sigma * ConvexRecon.gradient_operator_CPU(lambda_new)
            u_new = ConvexRecon.prox_l2_CPU(u_new, sigma)

            # Mise à jour avec relaxation
            lambda_ = lambda_new + theta * (lambda_new - lambda_)
            u = u_new + theta * (u_new - u)

        return lambda_

    @staticmethod
    def primal_dual_chambolle_pock_GPU(A, y, alpha, tau, sigma, theta, iterations):
        # Initialisation sur GPU
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        lambda_ = torch.zeros((A.shape[1], 1), device=device)
        u = torch.zeros((2, A.shape[1], 1), device=device)

        A = A.to(device)
        y = y.to(device)

        for _ in trange(iterations):
            # Mise à jour de lambda
            lambda_new = ConvexRecon.prox_l1_GPU(lambda_ - tau * torch.matmul(A.t(), torch.matmul(A, lambda_) - y), tau * alpha)

            # Mise à jour de u
            u_new = u + sigma * ConvexRecon.gradient_operator_GPU(lambda_new)
            u_new = ConvexRecon.prox_l2_GPU(u_new, sigma)

            # Mise à jour avec relaxation
            lambda_ = lambda_new + theta * (lambda_new - lambda_)
            u = u_new + theta * (u_new - u)

        return lambda_

class DeepLearningRecon(Recon):
    """
    This class implements the deep learning reconstruction process.
    It currently does not perform any operations but serves as a template for future implementations.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.reconType = ReconType.DeepLearning
        self.model = None  # Placeholder for the deep learning model
        self.theta_matrix = []

    def run(self, processType=ProcessType.PYTHON):
        """
        This method is a placeholder for the deep learning reconstruction process.
        It currently does not perform any operations but serves as a template for future implementations.
        """
        if(processType == ProcessType.CASToR):
            self._deepLearningReconCASToR()
        elif(processType == ProcessType.PYTHON):
            self._deepLearningReconPython()
        else:
            raise ValueError(f"Unknown deep learning reconstruction type: {processType}")

    def _deepLearningReconCASToR(self):
        pass

    def _deepLearningReconPython(self):
        pass