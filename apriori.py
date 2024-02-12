
from collections import defaultdict

ITEM_DELIM = ';'

def apriori(file, min_supp):
    # Scan DB for singelton items and their support values
    # Prune all items that are less than min_supp
    # Also determine max itemset size (to get how many pattern sizes need to go up to)
    
    # k = 1
    # Repeat:
        # Generate candidates of size (k+1) 
        # Prune invalid candidates (contains subpattern that is not a frequent size k pattern)
        # Scan DB to check for support values of the candidates
        # Prune candidates that have support less than min_supp
    
    # return: frequent candidates
    
    singleton_items = get_singleton_items(file)
    print(singleton_items)
    prune_candidates(singleton_items, min_supp)
    
    
    

def get_singleton_items(file):
    singleton_items = defaultdict(int)
    
    with open(file, "r") as f:
        for line in f:
            transaction = line.strip()
            items = transaction.split(ITEM_DELIM)
            for item in items:
                singleton_items[item] += 1
        
    return singleton_items

def get_supports(file, candidates):
    supports = defaultdict(int) # key will be a tuple representing a pattern
    
    with open(file, "r") as f:
        for line in f:
            transaction = line.strip()
            items = set(transaction.split(ITEM_DELIM))
            for candidate in candidates:
                if candidate.issubset(items):
                    supports[tuple(candidate)] += 1
    
    return supports
                
        

def prune_candidates(candidates, min_supp):
    for item in list(candidates.keys()):
        support = candidates[item]
        if support <= min_supp:
            del candidates[item]
            

def export_frequent_patterns(frequent_patterns):
    pass
    
apriori("data/test_s.txt", 0)

# apriori("data/categories.txt", 771) 
        
        
