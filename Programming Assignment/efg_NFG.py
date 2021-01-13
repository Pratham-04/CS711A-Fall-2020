import numpy as np
def efg_NFG(file_name):
    f = open(file_name, "r")
    lines = []
    lines.append(f.readline())
    numLines = 0
    while lines[numLines] != "":
        lines.append(f.readline())
        numLines += 1
    
    for i in range(len(lines)):
        lines[i] = lines[i].replace('\n','')
    line1 = lines[0][:lines[0].index('" ')+1]
    line1 = 'N'+line1[1:4]+'1'+line1[5:]
    line2 = lines[0][lines[0].index('{'):]
    line2 = line2+' { '

    class node(object):
        def __init__(self, player, infosetnum, playername, name, par, act):
            self.player = player
            self.infosetnum = None
            self.givenNum = infosetnum
            self.playername = playername
            self.name = name
            self.parent = par
            self.action = act
            self.numActions = None
            self.utility = None
            self.actionSet = None
            self.children = []
        def add_child(self, obj):
            self.children.append(obj)
    
    gamename = lines[0][lines[0].index(' "') + 2: lines[0].index('" ')]
    names = lines[0][lines[0].index('{ ') + 2: lines[0].index(' }')]
    names = names.split('" "')
    for i in range(0,len(names)):
        names[i] = names[i].replace('"','')
#     print(names)
#     return
    num_players = len(names)
    
    root = node(None, None, None, None, None, None)
    for i in range(2,len(lines)-1):
        first = lines[i][:lines[i].index('{')]
        first = first.split()
        for fir in range(0,len(first)):
            first[fir] = first[fir].replace('"','')
        second = lines[i][lines[i].index('{') + 1: lines[i].index('}')]
        second = second.split('" "')
        for sec in range(0,len(second)):
            second[sec] = second[sec].replace(' "','')
            second[sec] = second[sec].replace('" ','')
            second[sec] = second[sec].replace('"','')
        lines[i] = first+second
#         print(lines[i])
#     return
    
    infosets = [None]*num_players
    for i in range(0,num_players):
        infosets[i] = []
    indices = [0]*num_players
    terminal = [1]
    ind = [2]
    decPts = [0]*num_players
    def setGame(root, lines):
        if ind[0] == len(lines)-1:
            return
        
        if lines[ind[0]][0] == 'p':
            playername = lines[ind[0]][1]
            player = int(lines[ind[0]][2])
            infosetnum = int(lines[ind[0]][3])
            name = lines[ind[0]][4]
            actions = lines[ind[0]][5:]
            numActions = len(actions)
            
            root.player = player
            root.givenNum = infosetnum
            if infosetnum in infosets[root.player - 1]:
                root.infosetnum = infosets[root.player - 1].index(infosetnum) + 1
            else:
                infosets[root.player - 1].append(infosetnum)
                indices[root.player - 1] += 1
                root.infosetnum = indices[root.player - 1]
            root.playername = playername
            root.name = name
            root.numActions = numActions
            root.actionSet = actions
            decPts[root.player - 1] = root.infosetnum
#             print(root.numActions)
            
            for j in range(0,len(actions)):
                new = node(None, None, None, None, root, actions[j])
                ind[0] += 1
                root.add_child(new)
                setGame(root.children[j], lines)
            
            return
        
        if lines[ind[0]][0] == 't':
            infosetnum = int(lines[ind[0]][2])
            root.givenNum = infosetnum
            terminal[0] += 1
            root.infosetnum = terminal[0]
            util = lines[ind[0]][4]
            util = util.split()
            for u in range(0,len(util)):
                util[u] = util[u].replace(',','')
                util[u] = int(util[u])
            root.utility = util
#             print(root.utility)
            
            return
    
    setGame(root, lines)
    infosets.clear()
    indices.clear()
    
    stratSet = [[None]*decPts[i] for i in range(0,num_players)]
    
    def setStratSet(root):
        if root.player == None:
            return
        
        stratSet[root.player - 1][root.infosetnum - 1] = root.actionSet
        for i in range(0,root.numActions):
            setStratSet(root.children[i])
    setStratSet(root)
    
    nfgStrats = [1]*num_players
    for p in range(0,num_players):
        for dp in range(0,len(stratSet[p])):
            nfgStrats[p] *= len(stratSet[p][dp])
    for nfgs in nfgStrats:
        line2 = line2+str(nfgs)+' '
    line2 = line2+'}'
    lineOut = [line1, line2]
    
    matrix = np.zeros(tuple(nfgStrats)+(num_players,),dtype=np.int)
    
    utilities = []
    def traverseTree(root, hist):
        if root.player == None:
            utilities.append(root.utility)
            return
        traverseTree(root.children[hist[root.player - 1][root.infosetnum - 1]], hist)
    
    def setDecPt(root, hist, p, dp):
        if p == num_players:
            traverseTree(root, hist)
            return
        
        if dp == len(stratSet[p]):
            setDecPt(root, hist, p+1, 0)
            return
            
        for i in range(0,len(stratSet[p][dp])):
            hist[p][dp] = i
            setDecPt(root, hist, p, dp+1)
    
    hist = [[None]*decPts[i] for i in range(0,num_players)]
    setDecPt(root, hist, 0, 0)
    
    ind = [0]
    def setMatrix(k, tup):
        if k == num_players:
            matrix[tup] = utilities[ind[0]]
            ind[0] += 1
            return
        
        for i in range(0,nfgStrats[k]):
            setMatrix(k+1, tup+(i,))
    setMatrix(0, ())
    
    l3 = []
    def traverseMat(k, tup):
        if k == 0:
            for i in range(num_players-k):
                l3.append(matrix[tup+(i,)])
            return
        for i in range(0,nfgStrats[k-1]):
            traverseMat(k-1, (i,)+tup)
    traverseMat(num_players, ())
    
    line3 = ''
    for c in l3:
        line3 = line3+str(c)+' '
    line3 = line3[:-1]
    lineOut.append(line3)
    
    return lineOut