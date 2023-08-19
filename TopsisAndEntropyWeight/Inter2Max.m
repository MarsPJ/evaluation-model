function [X]=Inter2Max(x,low,up)
    M=max([low-min(x),max(x)-up]);
    xRows=size(x,1);
    X=zeros(xRows,1);
    for i=1:xRows
        if x(i)<low
            X(i)=1-(low-x(i))/M;
        elseif x(i)>up
            X(i)=1-(x(i)-up)/M;
        else
            X(i)=1;
        end
    end
end