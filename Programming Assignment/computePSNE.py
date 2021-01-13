import numpy as np
def computePSNE(file_name):
    index = [0]                                                                        # Index for entering the utility values into the matrix; initialised as a 1x1 array to be universally mutable
    def setGame(mat, strat, N, k, u, tup):
        if k == 0:
            for i in range(0,N):
                mat[tup+(i,)] = u[index[0]]                                            # Assigning the index-th entry of the utility list into the matrix at (strategy_tuple, player_number)
                index[0] += 1                                                          # Moving to the next number in the utilities list
            return
        
        for i in range(0,strat[k-1]):
            setGame(mat, strat, N, k-1, u, (i,) + tup)                                 # Recursive call with i being added to the tuple in the front to match the order of the .nfg file
    
    
    f = open(file_name, "r")
    line1 = f.readline()
    line2 = f.readline()
    line3 = f.readline()
    
    data = line2.split(" ")                                                           # Line 2 is important since it contains the number of players and their respective startegies
    data = data[data.index("{") + 1: data.index("}\n")]
    data = data[data.index("{") + 1:]
    num_players = len(data)                                                           # Number of players
    strategies = list(map(int, data))                                                 # Number of strategies of each player
    
    utilities = line3.split(" ")
    for i in range(0,len(utilities)):
        utilities[i] = int(utilities[i])                                              # Saving the utilities in one long 1D list
    
    utilities = np.array(utilities, dtype=int)                                        # Converting list to numpy array
    
    matrix = np.zeros(tuple(strategies)+(num_players,))                               # If number of players are 2 and their strategies are (4,3), we will need a matrix of dimensions 4x3x2 to save all the utilities once all the strategies are chosen
    
    setGame(matrix, tuple(strategies), num_players, num_players, utilities, ())       # Enters the utilities recursively into the utility matrix
    # Parsing of .nfg file ends here

    psne = []
    def addPsne(tup, strat, N):
        psneTup = []
        for i in range(0,N):
            for j in range(0,strat[i]):
                if tup[i] == j:
                    psneTup.append(1)
                else:
                    psneTup.append(0)
        psne.append(psneTup)
    
    def checkPsne(mat, strat, tup, p, util):
        k = 0
        for i in range(0,strat[p]):
            tup = list(tup)
            tup[p] = i
            tup = tuple(tup)
            if util >= mat[tup]:
                k += 1
        if k == strat[p]:
            return 1                                                                  # No unilateral deviation for player p, could be a PSNE
        else:
            return 0                                                                  # Unilateral deviation for player p is possible, hence this strategy set is not PSNE
    
    def setPsne(mat, N, strat, k, tup):
        if k == 0:                                                                    # By this point, all the players have a fixed strategy
            count = 0
            for i in range(0,N):
                count += checkPsne(mat, strat, tup+(i,), i, mat[tup+(i,)])            # Checks if i-th player unilaterally deviates from the strategy set given by tup
            
            if count == N:                                                            # If there is no unilateral deviation for all players, strategy set 'tup' is a psne
                addPsne(tup, strat, N)                                                # If the certain strategy set is a psne, add the strategy_tuple to the psne list of lists
            return
        
        for i in range(0,strat[N-k]):
            setPsne(mat, N, strat, k-1, tup+(i,))
    
    setPsne(matrix, num_players, strategies, num_players, ())
    
    return psne