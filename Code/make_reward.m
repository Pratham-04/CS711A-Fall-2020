function [u1 u2] = make_reward(patchA, patchB)
    u1 = [patchA/2 patchA patchB patchB/2];
    u2 = [patchA/2 patchB patchA patchA/2];
end