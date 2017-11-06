import re

def cleanScript(script):
    script = re.sub(r'\[.*?\]', '', script)
    script = re.sub(r'\(.*?\)', '', script)
    script = re.sub(r'<.*?>', '', script)
    while '  ' in script:
        script = script.replace('  ', ' ')
    while len(script)>=1 and (' ' in script[-1:]):
        script = script[:-1]
    return script

def reduceClustersAndAddQuestionMark(s, c, escape=False, any=False):
    while c+c in s:
       s = s.replace(c+c, c)
    d = ''
    if escape == True:
        d = '\\'
    c2 = c
    if any == True:
        c2 = '.'
    s = s.replace(c, d+c2+'?')
    return s

def getRegex(query):
    reg = query.replace('?', '？')
    reg = reg.replace('.', '。')
    reg = reduceClustersAndAddQuestionMark(reg, ',', False, True)
    reg = reduceClustersAndAddQuestionMark(reg, '-', False, True)
    reg = reduceClustersAndAddQuestionMark(reg, '\"', False, True)
    reg = reduceClustersAndAddQuestionMark(reg, '\'', False, True)
    reg = reduceClustersAndAddQuestionMark(reg, ':', False, True)
    reg = reduceClustersAndAddQuestionMark(reg, '=', False, True)
    reg = reduceClustersAndAddQuestionMark(reg, '+', False, True)
    reg = reduceClustersAndAddQuestionMark(reg, '。', False, True)
    reg = reduceClustersAndAddQuestionMark(reg, '!', False, True)
    reg = reduceClustersAndAddQuestionMark(reg, '？', False, True)
    reg = reduceClustersAndAddQuestionMark(reg, '⋯', False, True)
    reg = reg.replace('。', '.')
    reg = reg.replace('？', '?')
    return r'(%s.)' % reg

def do(df, query):

    titles, links, scripts = [], [], []
    reg = getRegex(query)

    for i, script in enumerate(df['Script']):
        script = cleanScript(script)
        script = re.sub(reg, r'\1'+'⑀', script, flags=re.IGNORECASE)
        subs = script.split('⑀')
        for sub in subs[1:]:
            title = df['Title'][i]
            link = df['Link'][i]
            titles.append(title)
            links.append(link)
            scripts.append(sub)

    results = list(zip(titles, links, scripts))

    return results
