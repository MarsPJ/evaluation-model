import gurobipy
import pandas as pd

# 分页显示数据, 设置为 False 不允许分页
pd.set_option('display.expand_frame_repr', False)

# 最多显示的列数, 设置为 None 显示全部列
pd.set_option('display.max_columns', None)

# 最多显示的行数, 设置为 None 显示全部行
pd.set_option('display.max_rows', None)


class DEA(object):
    def __init__(self, DMUs_Name, X, Y, AP=False):
        self.m1, self.m1_name, self.m2, self.m2_name, self.AP = X.shape[1], X.columns.tolist(), Y.shape[
            1], Y.columns.tolist(), AP
        self.DMUs, self.X, self.Y = gurobipy.multidict(
            {DMU: [X.loc[DMU].tolist(), Y.loc[DMU].tolist()] for DMU in DMUs_Name})
        print(f'DEA(AP={AP}) MODEL RUNING...')

    def __CCR(self):
        for k in self.DMUs:
            MODEL = gurobipy.Model()
            OE, lambdas, s_negitive, s_positive = MODEL.addVar(), MODEL.addVars(self.DMUs), MODEL.addVars(
                self.m1), MODEL.addVars(self.m2)
            MODEL.update()
            MODEL.setObjectiveN(OE, index=0, priority=1)
            MODEL.setObjectiveN(-(sum(s_negitive) + sum(s_positive)), index=1, priority=0)
            MODEL.addConstrs(
                gurobipy.quicksum(lambdas[i] * self.X[i][j] for i in self.DMUs if i != k or not self.AP) + s_negitive[
                    j] == OE * self.X[k][j] for j in range(self.m1))
            MODEL.addConstrs(
                gurobipy.quicksum(lambdas[i] * self.Y[i][j] for i in self.DMUs if i != k or not self.AP) - s_positive[
                    j] == self.Y[k][j] for j in range(self.m2))
            MODEL.setParam('OutputFlag', 0)
            MODEL.optimize()
            self.Result.at[k, ('效益分析', '综合技术效益(CCR)')] = MODEL.objVal
            self.Result.at[k, ('规模报酬分析',
                               '有效性')] = '非 DEA 有效' if MODEL.objVal < 1 else 'DEA 弱有效' if s_negitive.sum().getValue() + s_positive.sum().getValue() else 'DEA 强有效'
            self.Result.at[k, ('规模报酬分析',
                               '类型')] = '规模报酬固定' if lambdas.sum().getValue() == 1 else '规模报酬递增' if lambdas.sum().getValue() < 1 else '规模报酬递减'
            for m in range(self.m1):
                self.Result.at[k, ('差额变数分析', f'{self.m1_name[m]}')] = s_negitive[m].X
                self.Result.at[k, ('投入冗余率', f'{self.m1_name[m]}')] = 'N/A' if self.X[k][m] == 0 else s_negitive[m].X / \
                                                                                                     self.X[k][m]
            for m in range(self.m2):
                self.Result.at[k, ('差额变数分析', f'{self.m2_name[m]}')] = s_positive[m].X
                self.Result.at[k, ('产出不足率', f'{self.m2_name[m]}')] = 'N/A' if self.Y[k][m] == 0 else s_positive[m].X / \
                                                                                                     self.Y[k][m]
        return self.Result

    def __BCC(self):
        for k in self.DMUs:
            MODEL = gurobipy.Model()
            TE, lambdas = MODEL.addVar(), MODEL.addVars(self.DMUs)
            MODEL.update()
            MODEL.setObjective(TE, sense=gurobipy.GRB.MINIMIZE)
            MODEL.addConstrs(
                gurobipy.quicksum(lambdas[i] * self.X[i][j] for i in self.DMUs if i != k or not self.AP) <= TE *
                self.X[k][j] for j in range(self.m1))
            MODEL.addConstrs(
                gurobipy.quicksum(lambdas[i] * self.Y[i][j] for i in self.DMUs if i != k or not self.AP) >= self.Y[k][j]
                for j in range(self.m2))
            MODEL.addConstr(gurobipy.quicksum(lambdas[i] for i in self.DMUs if i != k or not self.AP) == 1)
            MODEL.setParam('OutputFlag', 0)
            MODEL.optimize()
            self.Result.at[
                k, ('效益分析', '技术效益(BCC)')] = MODEL.objVal if MODEL.status == gurobipy.GRB.Status.OPTIMAL else 'N/A'
        return self.Result

    def dea(self):
        columns_Page = ['效益分析'] * 3 + ['规模报酬分析'] * 2 + ['差额变数分析'] * (self.m1 + self.m2) + ['投入冗余率'] * self.m1 + [
            '产出不足率'] * self.m2
        columns_Group = ['技术效益(BCC)', '规模效益(CCR/BCC)', '综合技术效益(CCR)', '有效性', '类型'] + (self.m1_name + self.m2_name) * 2
        self.Result = pd.DataFrame(index=self.DMUs, columns=[columns_Page, columns_Group])
        self.__CCR()
        self.__BCC()
        self.Result.loc[:, ('效益分析', '规模效益(CCR/BCC)')] = self.Result.loc[:, ('效益分析', '综合技术效益(CCR)')] / self.Result.loc[:,
                                                                                                      ('效益分析',
                                                                                                       '技术效益(BCC)')]
        return self.Result

    def analysis(self, file_name=None):
        Result = self.dea()
        file_name = 'DEA 数据包络分析报告.xlsx' if file_name is None else f'\\{file_name}.xlsx'
        Result.to_excel(file_name, 'DEA 数据包络分析报告')



if __name__ == '__main__':
    data = pd.read_excel('test.xlsx')

    # 将 'year' 列设置为索引
    data.set_index('year', inplace=True)

    # 提取年份和数据字段
    years = data.index
    inputs = data[['财政收入', '环保投入', '科技人员']]
    outputs = data[['人均GDP', '城市环境质量']]

    # 创建DEA实例
    my_dea = DEA(DMUs_Name=years, X=inputs, Y=outputs)

    # 进行数据包络分析
    # my_dea.analysis()
    print(my_dea.dea())