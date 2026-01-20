def count_no_of_replacements(arr):
    count = 0
    n = len(arr)
    uniq_arr = list(set(sorted(arr)))
    n = len(uniq_arr)
    l, r = 0, 0
    max_con_len = 1
    while(r<n-1):
        if uniq_arr[r+1] - uniq_arr[r] == 1:
            max_con_len = max(max_con_len, r-l+1)
        else:
            l=r
        r += 1
    return n - max_con_len
    sorted