import numpy as np

def score_to_probability(score: float) -> float:
    return float(1 / (1 + np.exp(-score)))