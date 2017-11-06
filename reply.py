import random
import shared.console.font as fnt
import warnings
import praw
import files as fln
import search as sch
from shared.drive import pickles as pkl
from titlecase import titlecase
import re

warnings.filterwarnings("ignore", 'This pattern has match groups')

sig = "\n___\n*^Down-vote ^comments ^that ^don't ^make ^sense ^and ^I ^will ^automatically ^delete ^them, ^and ^adjust ^my ^algorithm ^so ^that ^I ^can ^learn ^how ^to ^be ^funny. [^<PM ^My ^Creator>](https://www.reddit.com/message/compose/?to=ShiEric&subject=Coy-bot&message=This+is+ace.+Dinner+tonight?)* [**^Episode: ^%s**]"

def cleanQuery(query):
    query = query + ' '
    query = query.replace('(', '')
    query = query.replace(')', '')
    query = query.replace('[', '')
    query = query.replace(']', '')
    query = query.replace('{', '')
    query = query.replace('}', '')
    query = re.sub(r'http://.*? ', '', query)
    query = re.sub(r'https://.*? ', '', query)
    query = query.replace('*', '')
    query = query.replace('^', '')
    query = query.replace('<', '')
    query = query.replace('>', '')
    query = query.replace('|', '')
    query = query.replace('+', '')
    query = query.replace(':', '')
    query = query.replace('=', '')
    query = query.replace('...', '⋯')
    query = query.replace('..', '⋯')
    while '  ' in query:
        query = query.replace('  ', ' ')
    while len(query)>=1 and (' ' in query[-1:]):
        query = query[:-1]
    return query

def trimLine(line):
    if ':' in line[:13]:
        s = line.split(':')
        line = ':'.join(s[1:])
    while len(line)>=1 and (' ' in line[0] or '…' in line[0] or '.' in line[0] or '?' in line[0] or '!' in line[0]):
        line = line[1:]
    line = line.replace('⋯', '...')
    return line[:1].upper() + line[1:]

def getQualityScore(key):
    dictQS = pkl.load(fln.fQuality)
    score = 0
    if key in dictQS:
        score = int(dictQS[key])
    print('dictQS[\'%s\'] = ' % (key[0:32]+'...') + str(score))
    return score

def parseReplies(df, query, replymin, scoremax):
    print('\t...'+query)
    results = sch.do(df, query)
    titles = []
    links = []
    lines = []
    if (len(results) > 0):
        for result in results:
            title = result[0]
            link = result[1]
            script = result[2]
            script = re.sub(r'\[.*?\]', '', script)
            script = re.sub(r'\(.*?\)', '', script)
            scriptLines = script.split('\n')
            xs = [i for i, s in enumerate(scriptLines)]
            if (len(xs)>0):
                x = int(xs[0]) + 1
                line = ''
                while (x<len(scriptLines)) and ((len(line) < replymin) or (('--' in line) and len(line) < 40)):
                    line = str(scriptLines[x])
                    if (len(line)>= replymin):
                        line = trimLine(line)
                    x += 1
                if (len(line) >= replymin):
                    score = getQualityScore(line)
                    if score <= scoremax:
                        titles.append(title)
                        links.append(link)
                        lines.append(line)
                        print('\t' + str(len(lines)) + ': ' + fnt.uS + line + fnt.End)
    parsed = list(zip(titles, links, lines))
    return parsed

def cleanSig(text):
    text = text.replace('(', '')
    text = text.replace(')', '')
    text = text.replace('[', '')
    text = text.replace(']', '')
    text = text.replace('{', '')
    text = text.replace('}', '')
    return text

def assembleReply(subreddit, reply):
    title = reply[0].replace(' ', ' ^')
    title = cleanSig(title)
    title = titlecase(title)
    link = reply[1]
    link = cleanSig(link)
    line = reply[2]
    signature = sig % title + '(' + link + ')'
    text = line
    if subreddit == 'jakeandamir':
        text = text + signature
    return text

def do(session, df, caughtObj, caughtTxt, query_words=5, reply_char_min=12, scoremax=2, replymax=0):
    replied = pkl.load(fln.fReplied)
    checked = pkl.load(fln.fChecked)
    for post, text in zip(caughtObj, caughtTxt):
        text = text.replace(' bot', '')
        if (len(text) > 0) and (post.id not in checked):
            query = cleanQuery(text)
            if (post.id not in replied) and (post.author != session.user.me()):
                s = query.split(' ')
                if (len(s) >= query_words):
                    print(fnt.colorDarkGray + query + fnt.End)
                    query = ' '.join(s[-query_words:])
                    replycount = 0
                    if isinstance(post, praw.models.Submission):
                        replycount = len(post.comments)
                    elif isinstance(post, praw.models.Comment):
                        try:
                            post.refresh()
                            replycount = len(post.replies)
                        except:
                            replycount = 9999
                    if replycount <= replymax:
                        replies = parseReplies(df, query, reply_char_min, scoremax)
                        if (len(replies)>0):
                            reply = random.choice(replies)
                            subreddit = post.subreddit
                            replyText = assembleReply(subreddit, reply)
                            print('\t' + fnt.bS + reply[2] + fnt.End)
                            post.upvote()
                            post.reply(replyText)
                            replied.append(post.id)
                            pkl.save(fln.fReplied, replied)
            checked.append(post.id)
            pkl.save(fln.fChecked, checked)