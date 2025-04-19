# EVALUATION METRICES
import numpy as np
from sklearn.metrics import precision_score, recall_score

def recall_at_k(relevant_items, recommended_items, k=3):
    """Calculating Recall@K"""
    if not relevant_items:
        return 0.0
    recommended_at_k = set(recommended_items[:k])
    relevant_set = set(relevant_items)
    return len(recommended_at_k.intersection(relevant_set)) / len(relevant_set)

def mean_average_precision(relevant_items, recommended_items, k=3):
    """Calculating MAP@K"""
    if not relevant_items:
        return 0.0
    
    relevant_set = set(relevant_items)
    sum_precision = 0.0
    num_hits = 0
    
    for i, item in enumerate(recommended_items[:k]):
        if item in relevant_set:
            num_hits += 1
            precision_at_i = num_hits / (i + 1)
            sum_precision += precision_at_i
    
    return sum_precision / min(k, len(relevant_set))
