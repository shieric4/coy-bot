from shared.drive import pickles as pkl
from shared.drive import drive as drv

listBlank = []
dictBlank = {}

dMain = 'data'
dProcesses = 'processes'
dArchive = 'archive'
drv.confirmDir(dMain)
drv.confirmDir(dProcesses)
drv.confirmDir(dArchive)

fDataframe = dArchive + '/dataframe.pkl'
fPassword = dMain + '/password.pkl'

fReplied = dProcesses + '/replied.pkl'
fChecked = dProcesses + '/checked.pkl'
fQuality = dMain + '/quality.pkl'
pkl.confirm(fReplied, listBlank)
pkl.confirm(fChecked, listBlank)
pkl.confirm(fQuality, dictBlank)