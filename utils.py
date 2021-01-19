BLANK = [' ', '\r', '\n', '\t']
QUOT = ['\'', '\"']

def n_increase(cur_n, increase):
    """docstring for n_increase"""
    return cur_n, cur_n+increase



def remove_quot(s):
    """docstring for remove_quot"""
    if s[0] in QUOT and s[0] == s[-1]:
        s = s[1:-1]
    return s
