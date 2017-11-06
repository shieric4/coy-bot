import catch
import downloader as dwn
import files as fln
import login
import reply
import revise
import shared.console.font as fnt
from shared.drive import pickles as pkl

def goRogueOnSub(session, df, subreddit ='test', submission_limit = 100, comment_limit = 300, wordmin = 5, charmin = 12, scoremax = 1, replymax = 0):
    caughtObj, caughtTxt = catch.do(session, subreddit, submission_limit, comment_limit)
    print(fnt.bS + 'New posts recorded for /r/%s.' % (subreddit) + fnt.End)
    reply.do(session, df, caughtObj, caughtTxt, wordmin, charmin, scoremax, replymax)
    print(fnt.bS + 'Finished replies on /r/%s.' % (subreddit) + fnt.End)

def run(infiniteLoop):
    pkl.println(fln.fQuality)
    session = login.do()
    print(fnt.bS + 'Login successful.' + fnt.End)
    revise.do(session, 50)
    print(fnt.bS + 'Self-revision complete.' + fnt.End)
    df = dwn.init()
    print(fnt.bS + 'Archive initialized.' + fnt.End)

    x = True

    while x == True:
        ext = input('Type \'exit\' to make this the final loop: ')
        goRogueOnSub(session, df, subreddit='jakeandamir', submission_limit=50, comment_limit=300, wordmin=5, charmin=5, scoremax=0, replymax=0)
        goRogueOnSub(session, df, subreddit='headgum', submission_limit=50, comment_limit=200, wordmin=5, charmin=5, scoremax=0, replymax=0)
        goRogueOnSub(session, df, subreddit='twinnovation', submission_limit=50, comment_limit=200, wordmin=5, charmin=5, scoremax=0, replymax=0)
        #goRogueOnSub(session, df, subreddit='all', submission_limit=0, comment_limit=500, wordmin=5, charmin=5, scoremax=0, replymax=10)
        if ext == 'exit':
            x = False
        x = infiniteLoop

    print(fnt.bS + 'Run successful.' + fnt.End)

run(infiniteLoop=False)