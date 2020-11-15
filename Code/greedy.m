function choose = greedy(e1, e2, chosen_idx, i)
    choose = zeros(1,2);
    n1 = sum(chosen_idx(:,2) == 1);
    v11 = n1 * e1(1) + (i - n1) * e1(2);
    v12 = n1 * e1(3) + (i - n1) * e1(4);
    if v11 > v12
        choose(1) = 1;
    else
        choose(1) = 2;
    end
    
    n2 = sum(chosen_idx(:,1) == 1);
    v21 = n2 * e2(1) + (i - n2) * e2(2);
    v22 = n2 * e2(2) + (i - n2) * e2(4);
    if v21 > v22
        choose(2) = 1;
    else
        choose(2) = 2;
    end
end