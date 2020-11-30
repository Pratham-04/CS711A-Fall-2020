#!/usr/bin/env python
# coding: utf-8

# In[56]:


import numpy as np
import os
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

def readData(filename):
    strats = []
    rewards = []
    f = open(filename, "r")
    for i in range(30):
        line1 = f.readline()
        line2 = f.readline()
        
        data1 = line1.split(" ")
        data2 = line2.split(" ")
        data1[1] = data1[1].rstrip()
        data2[1] = data2[1].rstrip()
        data1 = [int(i) for i in data1]
        data2 = [float(i) for i in data2]
        
        strats.append(data1)
        rewards.append(data2)
    fin = f.readline()
    final = fin.split()
    final = [float(i) for i in final]
    return strats, rewards, final

def regret(strats, rewards):
    TRIALS = 30
    MEANREW = [20,12]
    DECAY = 0.95
    GROWTH = 1.05
    rew = MEANREW

    regret1 = 0
    regret2 = 0
    for i in range(0,TRIALS):
        gameMat = [[[rew[0]/2,rew[0]/2], [rew[0],rew[1]]],
                   [[rew[1],rew[0]], [rew[1]/2,rew[1]/2]]]
        
        max1 = max(gameMat[0][0][0],gameMat[0][1][0],gameMat[1][0][0],gameMat[1][1][0])
        max2 = max(gameMat[0][0][1],gameMat[0][1][1],gameMat[1][0][1],gameMat[1][1][1])

        choice1 = rewards[i][0]
        choice2 = rewards[i][1]

        r1 = (max1 - choice1)
        r2 = (max2 - choice2)
        regret1 += r1
        regret2 += r2

        if strats[i][0] == strats[i][1]:
            rew[strats[i][0]] *= DECAY*DECAY
            rew[1-strats[i][0]] *= GROWTH
        else:
            rew[strats[i][0]] *= DECAY
            rew[strats[i][1]] *= DECAY
        
        
    
    return regret1, regret2

directory = os.fsencode("Choices and Rewards")

regrets = []
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    strats, rewards, final = readData(r"Choices and Rewards\\"+str(filename))
    reg1, reg2 = regret(strats, rewards)
    regrets.append(reg1)
    regrets.append(reg2)

regrets = np.array(regrets)
# print(regrets)
MEAN = np.mean(regrets)
STD = np.std(regrets)
print(MEAN, STD)
print()



for i in range(28):
    if regrets[i] > MEAN+STD:
        print(i+1, np.round(regrets[i],2), "GREATER")
    elif regrets[i] < MEAN-STD:
        print(i+1, np.round(regrets[i],2), "LESSER")
    else:
        print(i+1, np.round(regrets[i],2))

plt.boxplot(regrets)
plt.show()
#regrets

