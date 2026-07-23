from AOT_biomaps.AOT_Recon.AOT_Preconditioner._mainPreconditioner import Preconditioner
from AOT_biomaps.AOT_Recon.AOT_Preconditioner.PreconditionerEnums import PreconditionerType

class DiagPreconditioner(Preconditioner):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.diagonal = None
        self.precondType = PreconditionerType.DIAGONAL
    
    def get_name(self):
        return "Diagonal Preconditioner"

    def build(self):

        xp = self.get_array_module()
        self.diagonal = self.SMatrix.compute_hessian_diagonal().astype(xp.float32)
        eps = xp.maximum(xp.median(self.diagonal)*1e-6, xp.float32(1e-12))
        self.diagonal = xp.maximum(self.diagonal, eps)

    def apply_inverse(self, x):

        return x / self.diagonal