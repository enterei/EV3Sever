from SystemHandler import SystemHandler
sh=SystemHandler("buh")

loop = False

while not loop:
    x= sh.findWay()
    if x == True:
        break
    if x == None:
        break
    sh.doMove(x)
