def clean(selftext):
    selftext = selftext.replace('\n', ' ')
    selftext = selftext.replace('\r', ' ')
    selftext = selftext.replace('\t', ' ')
    while ('  ' in selftext):
        selftext = selftext.replace('  ', ' ')
    return selftext

def do(session, sub='jakeandamir', slimit=200, climit = 500):
    caughtObj = []
    caughtTxt = []
    for submission in session.subreddit(sub).new(limit=slimit):
            caughtObj.append(submission)
            caughtTxt.append(clean(submission.selftext))
            if not str(submission.selftext) == str(submission.title):
                caughtObj.append(submission)
                caughtTxt.append(clean(submission.title))
    for comment in session.subreddit(sub).comments(limit=climit):
            caughtObj.append(comment)
            caughtTxt.append(clean(comment.body))
    return caughtObj, caughtTxt