numTrials = 50;
numCells = 4;
patchA = 20;
patchB = 12;
util1 = zeros(numTrials, numCells);
util2 = zeros(numTrials, numCells);
mu1 = zeros(numTrials, numCells);
mu2 = zeros(numTrials, numCells);
rew = zeros(numTrials, 20;
sigma = 2;
decay = 0.95; growth = 1.05;
epsilon = 0.1;
e1 = [1 1 1 1]; e2 = [1 1 1 1];
s1 = [1 1 1 1]; s2 = [1 1 1 1];
k1 = [0 0 0 0]; k2 = [0 0 0 0];
chosen_idx = zeros(numTrials, 2);

for i = 1:numTrials
    
    [mu1(i,:) mu2(i,:)] = make_reward(patchA, patchB);
    util1(i,:) = normrnd(mu1(i,:), sigma); 
    util2(i,:) = normrnd(mu2(i,:), sigma);
    p = rand;
    if p < epsilon
        [chosen_idx(i,:)] = random(blah);
    else
        [chosen_idx(i,:)] = greedy(blah);
    end
    
    if chosen_idx(i,1) == chosen_idx(i,2)
        if chosen_idx(i,1) == 1
            rew(i,:) = [util1(i,1) util2(i,1)];
            patchA = (decay^2)*patchA;
            patchB = growth*patchB;
        else
            rew(i,:) = [util1(i,4) util2(i,4)];
            patchA = growth*patchA;
            patchB = (decay^2)*patchB;
        end
    else
        if chosen_idx(i,1) == 1
            rew(i,:) = [util1(i,2) util2(i,2)];
        else
            rew(i,:) = [util1(i,3) util2(i,3)];
        end
        patchA = decay*patchA;
        patchB = decay*patchB;
    end
    %[e1, e2, s1, s2, k1, k2] = k_update(e1, e2, s1, s2, k1, k2, sigma, util1, util2, chosen_idx, i);
    if chosen_idx(i,1) == 1
        z1 = (rew(i,1) - e1(i-1,1))/s1(i-1,1);
        z2 = (rew(i,1) - e1(i-1,2))/s1(i-1,2);
        if z1 >= z2
            %k_update e1, s1, k1, 2
        else
            %k_update e1, s1, k1, 1
        end
    else
        z1 = (rew(i,1) - e1(i-1,3))/s1(i-1,3);
        z2 = (rew(i,1) - e1(i-1,4))/s1(i-1,4);
        if z1 >= z2
            %k_update e2, s2, k2 4
        else
            %k_update e1, s1, k1, 3
        end
    end
    
    if chosen_idx(i,2) == 1
        z1 = (rew(i,2) - e2(i-1,1))/s2(i-1,1);
        z2 = (rew(i,2) - e2(i-1,3))/s2(i-1,3);
        if z1 >= z2
            %k_update e2, s2, k2, 1
        else
            %k_update e2, s2, k2, 3
        end
    else
        z1 = (rew(i,2) - e2(i-1,2))/s2(i-1,2);
        z2 = (rew(i,2) - e2(i-1,4))/s2(i-1,4);
        if z1 >= z2
            %k_update e2, s2, k2 4
        else
            %k_update e2, s2, k2, 2
        end
    end
    
    
end

            
    
    
























