function [X]=Mid2Max(x,best)
    M=max(abs(x-best));
    X=1-(abs(x-best)./M);
end