import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def cos_similar(a, b):
    a=np.array(a).reshape(1, -1)
    b=np.array(b).reshape(1, -1)
    return cosine_similarity(a, b)[0][0]


def precision(retrievals):
    '''
    retrievals: dict of job_name:top_k_ids
    returns the average precision at k
    '''
    precision=0.0
    k = len(next(iter(retrievals.values())))
    for job_name,candidates in retrievals.items():
        relevant= sum([1 for candidate in candidates if candidate.startswith(job_name)])/k
        precision+=relevant
    return precision/len(retrievals)


def hit_rate(retrievals):
    """
    retrievals: 
                dict of job_name:top_k_ids
    returns:
                the hit rate at k
    
    - Measures the proportion of queries for which at least one relevant document
    is retrieved in the top k results.
    - Formula: HR@k = (Number of queries with at least one relevant document in top k) / |Q|
    
    """
    hits = 0
    
    k = len(next(iter(retrievals.values())))
    for job_name,candidates in retrievals.items():
        # at least one relevant doc in top k
        relevant= sum([1 for candidate in candidates if candidate.startswith(job_name)])/k
        if relevant>0:
            hits+=1        
            
    return hits / len(retrievals)