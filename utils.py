def merge_str(s1: str, s2: str) -> str:
    '''return longer string'''
    return s1 if len(s1) >= len(s2) else s2

def merge_list(l1: list, l2: list) -> list:
    '''return l1 union l2 and remove duplicate'''
    union = l1 + l2
    if all(isinstance(item, dict) for item in union):
        seen = set([tuple(sorted(d.items())) for d in l1])
        
        for d in l2:
            t = tuple(sorted(d.items()))
            if t not in seen:
                seen.add(t)
                l1.append(d)
    else:
        l1 = list(set(union))
    return l1

def merge_dict(d1: dict, d2: dict) -> dict:
    '''merge d2 to d1, return d1'''
    for key, val in d2.items():
        if key not in d1:
            d1[key] = val
        elif isinstance(val, str) and isinstance(d1[key], str):
            d1[key] = merge_str(d1[key], val)
        elif isinstance(val, dict) and isinstance(d1[key], dict):
            d1[key] = merge_dict(d1[key], val)
        elif isinstance(val, list) and isinstance(d1[key], list):
            d1[key] = merge_list(d1[key], val)
    
    return d1
