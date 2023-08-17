function [X] = ForCV(x,type,col)
    if type==1
        disp(['第',num2str(col),'列是极小型，正在进行正向化...']);
        X=Min2Max(x);
        disp(['第',num2str(col),'列正向化成功结束！']);
    elseif type==2
         best=input('请输入中间型最佳的值：');
         disp(['第',num2str(col),'列是中间型，正在进行正向化...']);
         X=Mid2Max(x,best);
         disp(['第',num2str(col),'列正向化成功结束！']);
    elseif type==3
         low=input('请输入区间型最佳范围的最小值：');
         up=input('请输入区间型最佳范围的最大值：');
         disp(['第',num2str(col),'列是区间型，正在进行正向化...']);
         X=Inter2Max(x,low,up);
         disp(['第',num2str(col),'列正向化成功结束！']);
    else
        disp(['没有对应代号',num2str(type),'的指标类型！']);
    end
end