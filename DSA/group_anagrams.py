from collections import defaultdict

def getWordCount(string):
    word_count = [0]*26
    for ch in string:
        key = ord(ch) - 97
        word_count[key] += 1
    ans = ''
    for count in word_count:
        ans += str(count)
    set()
    return ans

def groupAnagrams(strs):
    group = defaultdict(list)
    for eachStr in strs:
        anagram = getWordCount(eachStr)
        group[anagram].append(eachStr)

    return list(group.values())

