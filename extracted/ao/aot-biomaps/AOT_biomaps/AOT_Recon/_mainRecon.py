from AOT_biomaps.Config import config
from AOT_biomaps.AOT_Experiment.Tomography import Tomography
from .ReconEnums import ReconType
from .ReconTools import mse
from skimage.metrics import structural_similarity as ssim

import os
import numpy as np
from abc import ABC, abstractmethod
from tqdm import trange
import matplotlib.pyplot as plt

    


class Recon(ABC):
    def __init__(self, experiment, saveDir = None, isGPU = config.get_process() == 'gpu', isMultiCPU = True):
        self.reconPhantom = None
        self.reconLaser = None
        self.experiment = experiment
        self.reconType = None
        self.saveDir = saveDir
        self.MSE = None
        self.SSIM = None
        self.CRC = None

        self.isGPU = isGPU
        self.isMultiCPU = isMultiCPU

        if str(type(self.experiment)) != str(Tomography):
            raise TypeError(f"[AOT-biomaps] Experiment must be of type {Tomography}")

    @abstractmethod
    def run(self,withTumor = True):
        pass

    def save(self, withTumor=True, overwrite=False, date=None, show_logs=True):
        """
        Save the reconstruction results (reconPhantom is with tumor, reconLaser is without tumor) and indices of the saved recon results, in numpy format.

        Args:
            withTumor (bool): If True, saves reconPhantom. If False, saves reconLaser. Default is True.
            overwrite (bool): If False, does not save if the file already exists. Default is False.

        Warnings:
            reconPhantom and reconLaser are lists of 2D numpy arrays, each array corresponding to one iteration.
        """
        isExisting, filepath = self.check_existing_file(date=date, withTumor=withTumor)
        if isExisting and not overwrite:
            return
        
        filename = 'reconPhantom.npy' if withTumor else 'reconLaser.npy'
        filepathRecon = os.path.join(filepath, filename)

        if withTumor:
            if not self.reconPhantom or len(self.reconPhantom) == 0:
                raise ValueError("[AOT-biomaps] Reconstructed phantom is empty. Run reconstruction first.")
            np.save(filepathRecon, np.array(self.reconPhantom))
        else:
            if not self.reconLaser or len(self.reconLaser) == 0:
                raise ValueError("[AOT-biomaps] Reconstructed laser is empty. Run reconstruction first.")
            np.save(filepathRecon, np.array(self.reconLaser))

        if self.indices is not None and len(self.indices) > 0:
            filepathIndices = os.path.join(filepath, f"indices_{'withTumor' if withTumor else 'withoutTumor'}.npy")
            np.save(filepathIndices, np.array(self.indices))

        if show_logs:
            print(f"[AOT-biomaps] Reconstruction results saved to {os.path.dirname(filepath)}")

    @abstractmethod
    def check_existing_file(self, date=None, withTumor=True):
        pass

    def _gt(self, withTumor=True):
        """Ground truth cropped to the effective SMatrix geometry (handles virtual/physical truncation)."""
        optic = self.experiment.OpticImage
        if optic is None:
            return None
        gt = optic.phantom if withTumor else optic.laser.intensity
        S = getattr(self, 'SMatrix', None)
        if S is not None and hasattr(S, 'crop_to_effective'):
            return S.crop_to_effective(gt)
        return gt

    def _crop_mask(self, mask):
        """Crop a full-size (Z, X) mask/label array to the effective SMatrix geometry."""
        S = getattr(self, 'SMatrix', None)
        if S is not None and hasattr(S, 'crop_to_effective'):
            return S.crop_to_effective(mask)
        return mask
    
    def _eff_extent(self, scale=1e3):
        """imshow extent [x0, x1, z1, z0] in mm, matching the effective SMatrix geometry."""
        g = self.experiment.params.general
        Xrange = [g['Xrange'][0] * scale, g['Xrange'][1] * scale]
        Zrange = [g['Zrange'][0] * scale, g['Zrange'][1] * scale]
        S = getattr(self, 'SMatrix', None)
        if S is not None and hasattr(S, 'effective_extent'):
            return S.effective_extent(Xrange, Zrange)
        return [Xrange[0], Xrange[1], Zrange[1], Zrange[0]]

    def calculate_CRC(self, use_ROI=True, per_tumor=False):
        """
        Computes the Contrast Recovery Coefficient (CRC).

        CRC = (recon_ratio - 1) / (lambda_ratio - 1)
        where recon_ratio = mean(reconPhantom) / mean(reconLaser) over the ROI, and lambda_ratio is the same ratio on the ground truths.

        Ground truths and ROI masks are cropped to the effective SMatrix geometry.

        Args:
            use_ROI: If True, restrict the computation to the phantom ROIs (one mask per absorber). If False, compute a single global CRC over the whole image.
            per_tumor: If True (requires use_ROI), compute ONE CRC per absorber/tumor and return a dictionary {absorber_name: CRC}. If False, compute a single averaged CRC over the union of all ROIs.

        Returns:
            - Analytic recon: scalar CRC (or dict {name: CRC} if per_tumor).
            - Iterative recon: list of CRC per iteration; if per_tumor, a list of dict {absorber_name: CRC_per_iteration} — i.e. self.CRC = [{name: crc_it}, ...].
        """
        if self.reconType is None:
            raise ValueError("[AOT-biomaps] Run reconstruction first")

        if self.reconLaser is None or self.reconLaser == []:
            raise ValueError("[AOT-biomaps] Reconstructed laser is empty. Run reconstruction first.")
        if self.reconPhantom is None or self.reconPhantom == []:
            raise ValueError("[AOT-biomaps] Reconstructed phantom is empty. Run reconstruction first.")

        if per_tumor and not use_ROI:
            raise ValueError("[AOT-biomaps] per_tumor=True requires use_ROI=True (tumor masks are needed).")

        # Effective ground truths (cropped to the reconstruction geometry)
        gt_phantom = self._gt(withTumor=True)
        gt_laser = self._gt(withTumor=False)

        # --- Masks ---
        mask_dict = None   # {absorber_name: cropped_mask} si per_tumor
        global_mask = None
        if use_ROI:
            self.experiment.OpticImage.find_ROI()
            absorbers = self.experiment.OpticImage.absorbers
            masks = [self._crop_mask(m) for m in self.experiment.OpticImage.maskList]

            # Absorber names ↔ masks, dans le même ordre (find_ROI itère sur absorbers)
            # Gère les noms dupliqués en suffixant.
            mask_dict = {}
            name_count = {}
            for absorber, m in zip(absorbers, masks):
                name = getattr(absorber, 'name', None) or f"absorber_{len(mask_dict)}"
                if name in mask_dict:
                    name_count[name] = name_count.get(name, 0) + 1
                    name = f"{name}_{name_count[name]}"
                mask_dict[name] = m
                if m is not None and np.any(m):
                    mask_dict[name] = m
                else:
                    print(f"[AOT-biomaps] Warning: empty mask for absorber '{name}' after cropping.")

            global_mask = np.logical_or.reduce(masks)
            if global_mask is None or np.count_nonzero(global_mask) == 0:
                print("[AOT-biomaps] No ROIs found in the phantom. Computing global CRC instead.")
                use_ROI = False
                per_tumor = False

        # --- CRC for one (or several) mask(s) ---
        def _crc_from_mask(recon_ph, recon_laser, mask):
            if mask is None:  # global (whole image)
                recon_ratio = np.mean(recon_ph) / np.mean(recon_laser)
            else:
                if not np.any(mask):
                    return np.nan
                recon_ratio = np.mean(recon_ph[mask]) / np.mean(recon_laser[mask])
            return recon_ratio

        lambda_ratio = {}
        if use_ROI:
            for name, m in mask_dict.items():
                lambda_ratio[name] = (np.mean(gt_phantom[m]) / np.mean(gt_laser[m])) if np.any(m) else np.nan
        global_lambda_ratio = (np.mean(gt_phantom[global_mask]) / np.mean(gt_laser[global_mask])) if use_ROI \
            else (np.mean(gt_phantom) / np.mean(gt_laser))

        def _finalize(recon_ratio, lam_ratio):
            denom = lam_ratio - 1
            return (recon_ratio - 1) / denom if denom != 0 else np.nan

        # ================= Analytic reconstruction =================
        if self.reconType is ReconType.Analytic:
            if per_tumor:
                self.CRC = {
                    name: _finalize(_crc_from_mask(self.reconPhantom, self.reconLaser, m), lambda_ratio[name])
                    for name, m in mask_dict.items()
                }
            elif use_ROI:
                self.CRC = _finalize(_crc_from_mask(self.reconPhantom, self.reconLaser, global_mask), global_lambda_ratio)
            else:
                self.CRC = _finalize(_crc_from_mask(self.reconPhantom, self.reconLaser, None), global_lambda_ratio)

        # ================= Iterative reconstruction =================
        else:
            iterations = range(np.min([len(self.reconPhantom), len(self.reconLaser)]))

            if per_tumor:
                # Liste de dictionnaires : CRC[t] = {tumor_name: CRC à l'itération t}
                crc_list = []
                for it in iterations:
                    crc_it = {}
                    for name, m in mask_dict.items():
                        crc_it[name] = _finalize(_crc_from_mask(self.reconPhantom[it], self.reconLaser[it], m), lambda_ratio[name])
                    crc_list.append(crc_it)
                self.CRC = crc_list
            else:
                crc_list = []
                for it in iterations:
                    mask = global_mask if use_ROI else None
                    crc_list.append(_finalize(_crc_from_mask(self.reconPhantom[it], self.reconLaser[it], mask), global_lambda_ratio))
                self.CRC = crc_list

    def calculate_MSE(self, withTumor=True, ground_truth=None):
        """
        Calculate the Mean Squared Error (MSE) of the reconstruction,
        against the ground truth cropped to the effective geometry.
        """
        if withTumor and self._is_empty(self.reconPhantom):
            raise ValueError("[AOT-biomaps] Reconstructed phantom is empty. Run reconstruction first.")
        if not withTumor and self._is_empty(self.reconLaser):
            raise ValueError("[AOT-biomaps] Reconstructed laser is empty. Run reconstruction first.")

        if ground_truth is not None:
            gt = ground_truth
        else:
            gt = self._gt(withTumor=withTumor)

        if self.reconType in (ReconType.Analytic, ReconType.DeepLearning):
            self.MSE = mse(None, gt, self.reconPhantom)

        elif self.reconType == ReconType.Algebraic:
            self.MSE = []
            if withTumor:
                for theta in self.reconPhantom:
                    self.MSE.append(mse(self.SMatrix, gt, theta))
            else:
                for theta in self.reconLaser:
                    self.MSE.append(mse(self.SMatrix, gt, theta))

    def calculate_SSIM(self, withTumor=True, show_log=False):
        """
        Calculate SSIM without normalizing images, using original data_range.
        Reference image is cropped to the effective geometry.
        """
        if self.reconPhantom is None or self.reconPhantom == []:
            raise ValueError("[AOT-biomaps] Reconstructed phantom is empty. Run reconstruction first.")

        ref_img = self._gt(withTumor=withTumor)

        ref_min, ref_max = ref_img.min(), ref_img.max()
        data_range = ref_max - ref_min

        if self.reconType in (ReconType.Analytic, ReconType.DeepLearning):
            recon = self.reconPhantom
            self.SSIM = ssim(ref_img, recon, data_range=data_range)

        else:
            self.SSIM = []
            recon_list = self.reconPhantom if withTumor else self.reconLaser

            iteration = trange(len(recon_list), desc=f"Calculating SSIM {'with' if withTumor else 'without'} tumor") if show_log else range(len(recon_list))

            for i in iteration:
                theta = recon_list[i]
                theta_min, theta_max = theta.min(), theta.max()
                current_data_range = max(data_range, theta_max - theta_min)
                self.SSIM.append(ssim(ref_img, theta, data_range=current_data_range))

    def _is_empty(self, x):
        """Check if a variable is empty (None or has zero length)."""
        return x is None or (hasattr(x, '__len__') and len(x) == 0)