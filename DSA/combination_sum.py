#https://leetcode.com/problems/combination-sum/

# Approach 1
class Solution:
    def cmRecursion(self, i, n, candidates, target, curr_pos, ans):
        if target < 0:
            return
        if target == 0:
            ans.append(curr_pos)
            return 
        for idx in range(i, n):
            curr_copy = list(curr_pos)
            curr_copy.append(candidates[idx])
            self.cmRecursion(
                idx, n, candidates, target - candidates[idx], curr_copy, ans
            )
        return 

    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        n = len(candidates)
        all_poss = []
        self.cmRecursion(0, len(candidates), candidates, target, [], all_poss)
        return all_poss

# Approach 2
class Solution2:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:

        candidates.sort()
        res = []
        path = []

        def dfs(start, remain):
            if remain == 0 :
                res.append(path.copy())

            for i in range(start, len(candidates)):
                x = candidates[i]
                if x > remain:
                    break
                
                path.append(x)
                dfs(i, remain-x)
                path.pop()


        dfs(0, target)
        return res
