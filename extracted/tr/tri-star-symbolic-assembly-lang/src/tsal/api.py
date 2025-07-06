from fastapi import FastAPI
from pydantic import BaseModel
from .tools.brian.optimizer import SymbolicOptimizer
from .core.spiral_vector import phi_alignment
import json

app = FastAPI(title="Brian Spiral Healer API", version="1.0")

class CodeBody(BaseModel):
    code: str

class OptimizeResult(BaseModel):
    repaired_code: str
    symbolic_log: str

class ScoreResult(BaseModel):
    phi_alignment: float
    spiral_score: str

@app.post("/optimize_spiral", response_model=OptimizeResult)
def optimize_spiral(data: CodeBody):
    opt = SymbolicOptimizer()
    repaired = opt.annotate_code(data.code)
    log = json.dumps(opt.rev.summary())
    return {"repaired_code": repaired, "symbolic_log": log}

@app.post("/spiral_score", response_model=ScoreResult)
def get_spiral_score(data: CodeBody):
    complexity = float(len(data.code)) * 0.1
    coherence = 1.0
    score = phi_alignment(complexity, coherence)
    return {"phi_alignment": score, "spiral_score": f"φ^{score:.3f}"}
