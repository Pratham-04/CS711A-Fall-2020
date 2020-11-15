function [s, e, k] = kalman(rew, sigma, s, e, k, i, t1)
    k(i,:) = (s(i-1,:) + sigma^2)./(s(i-1,:) + sigma^2);
    
    e(i,:) = e(i-1,:);
    e(i,t1) = e(i,t1) + k(i,t1)*(rew(i) - e(i-1,t1));
    
    s(i,:) = s(i-1,:);
    s(i,t1) = (1 - k(i,t1))*(s(i-1,t1) + sigma^2);
end