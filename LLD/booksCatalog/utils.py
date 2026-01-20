from typing import List

def compute_all_prefixes(value: str) -> List[str]:
    return [value[:i+1].lower() for i in range(len(value))]
