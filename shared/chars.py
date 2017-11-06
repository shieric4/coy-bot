a = '⑀'
# ⑁
# ⑂
# ⑃
# ⑄
# ⑅
# ⑆
# ⑇
# ⑈
# ⑉
# ⑊

def reduceClusters(s, c):
    while c+c in s:
        s = s.replace(c+c, c)
    return s

chinese = r'[\u4e00-\u9fff]'
korean = r'[가-힣]'