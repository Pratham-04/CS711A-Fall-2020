numTrials = 50;
numCells = 4;
patchA = 20;
patchB = 12;
util1 = zeros(numTrials, numCells);
util2 = zeros(numTrials, numCells);
mu1 = zeros(numTrials, numCells);
mu2 = zeros(numTrials, numCells);
rew = zeros(numTrials, 2);
sigma = 2;
decay = 0.95; growth = 1.05;
epsilon = 0.1;
e1 = [1 1 1 1]; e2 = [1 1 1 1];
s1 = [1 1 1 1]; s2 = [1 1 1 1];
k1 = [0 0 0 0]; k2 = [0 0 0 0];
chosen_idx = zeros(numTrials, 2);

for i = 1:numTrials
    
    if i > 1
        if chosen_idx(i,1) == 1
            z1 = (rew(i,1) - e1(i-1,1))/s1(i-1,1);
            z2 = (rew(i,1) - e1(i-1,2))/s1(i-1,2);
            if z1 >= z2
                [s1 e1 k1] = kalman(rew(:,1), sigma, s1, e1, k1, i, 2);
                %k_update e1, s1, k1, 2
            else
                [s1 e1 k1] = kalman(rew(:,1), sigma, s1, e1, k1, i, 1);
                %k_update e1, s1, k1, 1
            end
        else
            z1 = (rew(i,1) - e1(i-1,3))/s1(i-1,3);
            z2 = (rew(i,1) - e1(i-1,4))/s1(i-1,4);
            if z1 >= z2
                [s1 e1 k1] = kalman(rew(:,1), sigma, s1, e1, k1, i, 4);
                %k_update e1, s1, k1, 4
            else
                [s1 e1 k1] = kalman(rew(:,1), sigma, s1, e1, k1, i, 3);
                %k_update e1, s1, k1, 3
            end
        end
        
        if chosen_idx(i,2) == 1
            z1 = (rew(i,2) - e2(i-1,1))/s2(i-1,1);
            z2 = (rew(i,2) - e2(i-1,3))/s2(i-1,3);
            if z1 >= z2
                [s2 e2 k2] = kalman(rew(:,2), sigma, s2, e2, k2, i, 1);
                %k_update e2, s2, k2, 1
            else
                [s2 e2 k2] = kalman(rew(:,2), sigma, s2, e2, k2, i, 3);
                %k_update e2, s2, k2, 3
            end
        else
            z1 = (rew(i,2) - e2(i-1,2))/s2(i-1,2);
            z2 = (rew(i,2) - e2(i-1,4))/s2(i-1,4);
            if z1 >= z2
                [s2 e2 k2] = kalman(rew(:,2), sigma, s2, e2, k2, i, 4);
                %k_update e2, s2, k2 4
            else
                [s2 e2 k2] = kalman(rew(:,2), sigma, s2, e2, k2, i, 2);
                %k_update e2, s2, k2, 2
            end
        end
    end
    
    [mu1(i,:) mu2(i,:)] = make_reward(patchA, patchB);
    util1(i,:) = normrnd(mu1(i,:), sigma); 
    util2(i,:) = normrnd(mu2(i,:), sigma);
    p = rand;
    if p < epsilon
        [chosen_idx(i,:)] = ceil(2*rand(1,2));
    else
        %[chosen_idx(i,:)] = greedy(blah);
        [chosen_idx(i,:)] = greedy(e1(i,:), e2(i,:), chosen_idx, i);
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
end