# https://leetcode.com/problems/unique-paths-ii/?envType=problem-list-v2&envId=array


def uniquePathRecursion(i, j, n, m, obsMap):
        if i == n-1 and j == m-1:
            return int(not obsMap.get((n-1, m-1)))
        if (i < 0 or i >= n) or (j< 0 or j >= m) or obsMap.get((i, j)):
            return 0
        count = uniquePathRecursion(i+1, j, n, m, obsMap)
        count += uniquePathRecursion(i, j+1, n, m, obsMap)
        return count
        

def uniquePathsWithObstacles(obstacleGrid) -> int:
    obsCellSet = {}
    n, m = len(obstacleGrid), len(obstacleGrid[0])
    for i in range(n):
        for j in range(m):
            if obstacleGrid[i][j] == 1:
                obsCellSet[(i, j)] = 1
    return uniquePathRecursion(0, 0, n, m, obsCellSet)


# Compute TLE reson for this