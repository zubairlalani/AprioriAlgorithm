
from collections import defaultdict
from itertools import combinations

ITEM_DELIM = ';'

def apriori(input_file, output_file, min_supp):
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
    
    singleton_items = get_singleton_items(input_file)
    prune_candidates(singleton_items, min_supp)
    frequent_patterns = []
    frequent_patterns.extend(singleton_items.items())
    export_frequent_patterns(frequent_patterns, "output/patterns1.txt")
    frequent_k_itemsets = [set(k) for k in singleton_items.keys()]
    k = 2
    while frequent_k_itemsets:
        candidates = generate_candidates(frequent_k_itemsets, k)
        support_vals = get_supports(input_file, candidates)
        prune_candidates(support_vals, min_supp)
        
        frequent_patterns.extend(support_vals.items())
        frequent_k_itemsets = [set(k) for k in support_vals.keys()]
        k = k + 1
    
    export_frequent_patterns(frequent_patterns, output_file)
    
def generate_candidates(frequent_prev_candidates, k):
    candidates = set()
    for i in range(0, len(frequent_prev_candidates)):
        for j in range(i+1, len(frequent_prev_candidates)):
            itemset1 = frequent_prev_candidates[i]
            itemset2 = frequent_prev_candidates[j]
            union_set = itemset1.union(itemset2)
            if len(union_set) == k and check_apriori_property(union_set, frequent_prev_candidates, k):
                
                candidates.add(tuple(sorted(union_set)))
    return candidates
                    
                    
def check_apriori_property(candidate, frequent_k_minus_1, k):
    subsets = list(map(set, combinations(candidate, k-1)))
    for s in subsets:
        if s not in frequent_k_minus_1:
            return False
    return True 

def get_singleton_items(file):
    singleton_items = defaultdict(int)
    
    with open(file, "r") as f:
        for line in f:
            transaction = line.strip()
            items = transaction.split(ITEM_DELIM)
            for item in items:
                singleton_items[tuple([item])] += 1
        
    return singleton_items

def get_supports(file, candidates):
    supports = defaultdict(int) # key will be a tuple representing a pattern
    
    with open(file, "r") as f:
        for line in f:
            transaction = line.strip()
            items = set(transaction.split(ITEM_DELIM))
            for candidate in candidates:
                if set(candidate).issubset(items):
                    supports[candidate] += 1
    
    return supports
                
def prune_candidates(candidates, min_supp):
    for item in list(candidates.keys()):
        support = candidates[item]
        if support <= min_supp:
            del candidates[item]
            
def export_frequent_patterns(frequent_patterns, file):
    with open(file, "w+") as f:
        for pattern, support in frequent_patterns:
            categories = ";".join(pattern)
            f.write(f"{support}:{categories}\n")
        
apriori("data/categories.txt",  "output/patterns.txt", 771) 
        
        
