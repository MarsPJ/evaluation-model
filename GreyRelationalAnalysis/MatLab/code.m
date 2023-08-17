clear;clc
%%  第一步：把数据复制到工作区，并将这个矩阵命名为X
load WaterData.mat
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
%% 第三步：对正向化后的矩阵进行预处理
% 求出均值
X_mean=mean(X);
% 得到预处理后的矩阵（子序列）
X=X./repmat(X_mean,size(X,1),1);
disp('预处理后的矩阵如下：');
disp(X);
%% 第四步：计算权重
% 先求出母序列
Y=max(X,[],2);
% 求子序列与母序列之差的绝对值
X_Y_Abs=abs(X-repmat(Y,1,size(X,2)));
% 求绝对值中最小值和最大值
Abs_Min=min(min(X_Y_Abs));
Abs_Max=max(max(X_Y_Abs));
% 计算gamma
rho = 0.5 % 分辨系数
gamma=(Abs_Min+rho *Abs_Max)./(X_Y_Abs+rho *Abs_Max);
% 计算各个指标对母序列的关联度
R=mean(gamma);
% 计算权重
Weight=R./sum(R);
disp('权重计算结果如下：');
disp(Weight);
%% 第五步：计算得分
Ret=X.*repmat(Weight,size(X,1),1);
Score=sum(Ret,2);
% 归一化
Score=Score./sum(Score);
disp('得分如下：')
disp(Score);
% 排序
[SortedScore,Index]=sort(Score,'descend');
disp('排序(降序)后得分结果为：');
disp(SortedScore);
disp('索引如下：');
disp(Index);
