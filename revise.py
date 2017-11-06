import random
import files as fln
import login as l
import shared.console.font as fnt
from shared.drive import pickles as pkl

goodbot = ["I just want to do shit that makes me smile of you."]
badbot = ["I knew this would happen. I knew as soon as I went off and did something cute and subjective, you would turn it into this, this, this, this, this, this nuclear bomb of me!", "Don't taint my ideas with your negative shit feedback... Christ!", "We should come up with a ratings system. So instead of you saying, like, \"this is good, this is bad\", you'll be like \"this is amber, this is taupe\".", "I'm so serious, man. Oppa leads, like, a Halloween-style Gangnam life and you have no love for it? Like... how is that good for Oppa?", "Y'all are gonna have to bind and gag me if you want peace and quiet around here. And good luck, because I'm got going quietly.", "Okay, well I'm sorry I'm not good with wordplay right now, but I'm kinda... I'm bleeding out, man.","Tell that to my dad, man.", "The good news is it don't matter, cause we don't care.", "Okay, okay. You've made your point. Relax. You'll-- you'll make a martyr of me.", "Uhh, yeah. I went for it, didn't get it. That's... that's gonna happen. Dane Cook even tells jokes that sometimes don't get laughs.", "Laugh! Laugh at that! Okay? I don't make a lot of good jokes, I'm the first to admit it. But when I do, you gotta give me some taps. You gotta gimme that atta boy."]
coybot = ["Excuse?", "Hey, cutie. Want to see me tonight? Go to livecamgirlwhores.co.nz and enter your billing info."]

goodsig_template = "\n___\n*^Thank ^you ^for ^voting ^for ^me. ^I ^am ^currently ^ranked [^%s] (https://goodbot-badbot.herokuapp.com/all_filter) ^among ^%s ^Reddit ^bots.*"
badsig = "\n___\n*^Please ^downvote ^my ^bad ^comments ^instead ^of ^reporting ^me ^as ^a ^'bad ^bot.' ^This ^way ^I ^can ^improve."

def getRank():
    import downloader as d
    import login as l
    url = "https://goodbot-badbot.herokuapp.com/all_filter"
    sub = '/'+l.username + '\"'
    soup = d.getSoup(url)
    rankinfo = []
    table = soup.findAll("tr")
    for row in table:
        if str(sub).lower() in str(row).lower():
            for cell in row.findAll("td"):
                rankinfo.append(str(cell.text))
            rankinfo.append(str(int(len(table)-1)))
    return rankinfo

def getKarma(comment):
    return (comment.ups - comment.downs)

def quality(comment, min=1):
    dict = pkl.load(fln.fQuality)
    karma = getKarma(comment)
    if (karma < min):
        body = str(comment.body)
        if '\n' in body:
            key = body.split('\n')[0]
        else:
            key = body
        print(fnt.colorRed + body + fnt.End)
        if str(comment.subreddit) == 'jakeandamir':
            if key in dict:
                dict[key] += 1
            else:
                dict[key] = 1
            print('\tRecorded quality score.')
        comment.delete()
        print("\tDeleted.")
    pkl.save(fln.fQuality, dict)

def replies(comment, goodsig):
    replied = pkl.load(fln.fReplied)
    comment.refresh()
    if len(comment.replies) > 0:
        for reply in comment.replies:
            r = str(reply.body)
            if not (comment.id in replied):
                if 'good bot' in r.lower():
                    reply.upvote()
                    line = random.choice(goodbot)
                    replytext = line + goodsig
                    reply.reply(replytext)
                    print('\t'+line)
                    replied.append(comment.id)
                elif 'bad bot' in r.lower():
                    reply.downvote()
                    line = random.choice(badbot)
                    replytext = line + badsig
                    reply.reply(replytext)
                    print('\t'+line)
                    replied.append(comment.id)
                elif 'coy bot' in r.lower() or 'coy-bot' in r.lower():
                    reply.upvote()
                    replytext = random.choice(coybot)
                    reply.reply(replytext)
                    print('\t'+replytext)
                    replied.append(comment.id)
    pkl.save(fln.fReplied, replied)

def goodSig():
    rankinfo = getRank()
    rank = rankinfo[0]
    bots = rankinfo[5]
    return goodsig_template % (str(rank) , str(bots))

def do(session, limit=None):
    user = session.redditor(l.username)
    goodsig = goodSig()
    for comment in user.comments.new(limit=limit):
        quality(comment, 1)
    for comment in user.comments.new(limit=limit):
        replies(comment, goodsig)