import math

def combination(n,r):
    # กรณีพิเศษ: C(n,0) และ C(n,n) เท่ากับ 1
    if r == 0 or r == n:
        return 1
    # ใช้สูตร combination(n,r) = combination(n-1,r) + combination(n-1,r-1)
    return combination(n-1,r) + combination(n-1,r-1)
class data:
    n = "n"
    r = "r"

