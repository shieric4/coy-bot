import praw
import files as fln
import shared.drive.pickles as pkl
import shared.drive.drive as drv

username = 'Coy-Bot'
client_id = 'ZluO_Nx3bRQIxg'
client_secret = 'c9Xfr07tsvApD-QFOYp_ZItYtmA'
user_agent = 'Python Jake and Amir Quote-Completer Bot (by /u/ShiEric)'

def do():
    if drv.exists(fln.fPassword):
        password = pkl.load(fln.fPassword)
    else:
        password = input('Password:')
        pkl.save(fln.fPassword, password)
    session = praw.Reddit(
            username = username,
            password = password,
            client_id = client_id,
            client_secret = client_secret,
            user_agent = user_agent
            )
    return session