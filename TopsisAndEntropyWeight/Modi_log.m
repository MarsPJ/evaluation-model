function Y = Modi_log(X)
    cnt=size(X,1);
    Y=zeros(cnt,1);
    for i=1:cnt
        if X(i)==0
            Y(i)=0;
        else
            Y(i)=log(X(i));
        end
    end
end