clear;clc
%%  第一步：把数据复制到工作区，并将这个矩阵命名为X
load data_water_quality.mat
%%  第二步：判断是否需要正向化
[row,col]=size(X);
disp(['输入的数据一共有',num2str(row),'个对象',num2str(col),'个指标。']);
NeedForCV=input('是否需要对数据进行正向化处理（需要输入1，否则输入0）：');
if(NeedForCV==1)
    NeedCols=input('请输入需要进行正向化的数据的列数(如[1 2 3]):');
    Types=input('请输入这些列的指标类型（1-极小型；2-中间型；3-区间型），如[2 1 3]：');
    if(size(NeedCols,2)==size(Types,2))
        for i=1:size(NeedCols,2)
            X(:,NeedCols(i))=ForCV(X(:,NeedCols(i)),Types(i),NeedCols(i));
        end
        disp('正向化结果如下：');
        disp(X);
    else
        dis('输入的需要正向化的列数和指标类型总数不一致！');
    end
end
%% 第三步：对正向化后的矩阵进行标准化
% 每一列平方和开根号
SquSumCol=sum(X.^2).^0.5;
% 所有元素除以当前列的平方和
X=X./repmat(SquSumCol,size(X,1),1);
disp('标准化结果如下：');
disp(X);
%% 第四步：判断计算得分时是否需要考虑权重，用什么确定权重
NeedWei=input('计算得分时是否需要计算权重（0-否；1-是且采用熵权法确定权重；2-自行给定权重）：');
%% 第五步：计算与最大值的距离和最小值的距离，并算出得分
if NeedWei~=0
    if NeedWei==1
        existNeg=sum(X<0)>0;
        if existNeg==1
            disp("矩阵存在负数数据，现在重新进行标准化...");
            ColMin=min(X);
            ColMax=max(X);
            X=(X-ColMin)/(ColMax-ColMin);
            disp("重新标准化后结果如下：");
            disp(X);
        end
        % 熵权法求权重
        Weight=Entropy_Weight(X);
    else
        Weight=input('请输入各列指标的权重（如[0.2 0.3 0.5]）：');
        if  size(Weight,2)~=col
            disp('所给权重个数与指标个数不一致！');
            return;
        end
    end
    % 计算D-
    % 每列最小值
    MinCols=min(X);
    % 差的平方
    NeSubSqua=(X-repmat(MinCols,row,1)).^2;
    % 扩展权重
    Weights=repmat(Weight,row,1);
    % D-
    D_Neg=sum(NeSubSqua.*Weights,2).^0.5;

    % 计算D+
    % 每列最大值
    MaxCols=max(X);
    % 差的平方
    PoSubSqua=(X-repmat(MaxCols,row,1)).^2;
    % 扩展权重
    Weights=repmat(Weight,row,1);
    % D+
    D_Pos=sum(PoSubSqua.*Weights,2).^0.5;

    % 总得分
    Ret=D_Neg./(D_Pos+D_Neg);
    % 归一化
    Ret=Ret./sum(Ret);
    disp('总得分为：');
    disp(Ret);
    % 排序处理
    [SortedRet,Index]=sort(Ret,'descend');
    disp('排序后（降序）结果为：');
    disp(SortedRet);
    disp('索引如下：');
    disp(Index);
else
    % 计算D-
    % 每列最小值
    MinCols=min(X);
    % 差的平方
    NeSubSqua=(X-repmat(MinCols,row,1)).^2;
    % D-
    D_Neg=sum(NeSubSqua,2).^0.5;

    % 计算D+
    % 每列最大值
    MaxCols=max(X);
    % 差的平方
    PoSubSqua=(X-repmat(MaxCols,row,1)).^2;
    % D+
    D_Pos=sum(PoSubSqua,2).^0.5;

    % 总得分
    Ret=D_Neg./(D_Pos+D_Neg);
    % 归一化
    Ret=Ret./sum(Ret);
    disp('总得分为：');
    disp(Ret);
    % 排序处理
    [SortedRet,Index]=sort(Ret,'descend');
    disp('排序后（降序）结果为：');
    disp(SortedRet);
    disp('索引如下：');
    disp(Index);
end