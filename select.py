import os
import re
import warnings

import pandas as pd

warnings.filterwarnings("ignore")


def print_dict(dicc):
    for grouped_key, grouped_value in dicc.items():
        print(grouped_key, ':')
        print(grouped_value)


def sl_equal(operator, lim, table):
    '''
    选择：条件：等于的
    :param operator: 操作符
    :param lim: 限制条件
    :param table: 现在要操作的数据表
    :return:
    '''
    limleft = lim[0]
    limright = re.split(r'[\']', lim[2])
    limright = [item for item in filter(lambda x: x != '', limright)][0]
    # print(type(limright))
    # print(limleft, operator, limright)
    try:
        limright = int(limright)
    except:
        try:
            limright = float(limright)
        except:
            limright = limright
    try:
        test = table[(table[limleft] == limright)]
    except:
        print('[!]语法错误!：没有找到', limleft, '列，请检查输入是否正确！')
        return
    return test


def sl_not_equal(operator, lim, table):
    '''
    选择：条件：不等于的
    :param operator: 操作符
    :param lim: 限制条件
    :param table: 现在要操作的数据表
    :return:
    '''
    limleft = lim[0]
    limright = re.split(r'[\']', lim[2])
    limright = [item for item in filter(lambda x: x != '', limright)][0]
    # limright = limright[0]
    # print(type(limright))
    # print(limleft, operator, limright)
    try:
        limright = int(limright)
    except:
        try:
            limright = float(limright)
        except:
            limright = limright
    try:
        # test = table[((table[limleft]).astype(str).isin([limright]))]
        test = table[(table[limleft] != limright)]
    except:
        print('[!]语法错误!：没有找到', limleft, '列，请检查输入是否正确！')
        return
    return test


def sl_less(operator, lim, table):
    '''
    选择：条件：小于的
    :param operator: 操作符
    :param lim: 限制条件
    :param table: 现在要操作的数据表
    :return:
    '''
    limleft = lim[0]
    limright = lim[2]
    # limright = int(limright)
    # print(limleft, operator, limright)
    try:
        limright = int(limright)
    except:
        try:
            limright = float(limright)
        except:
            limright = limright
    test = table[(table[limleft] < limright)]
    # try:
    #     test = table[(table[limleft] < limright)]
    # except:
    #     print('[!]语法错误!：没有找到', limleft, '列，请检查输入是否正确！')
    #     return
    return test


def sl_more(operator, lim, table):
    '''
    选择：条件：大于的
    :param operator: 操作符
    :param lim: 限制条件
    :param table: 现在要操作的数据表
    :return:
    '''

    limleft = lim[0]
    limright = lim[2]
    # limright = int(limright)
    # print(limleft, operator, limright)
    try:
        limright = int(limright)
    except:
        try:
            limright = float(limright)
        except:
            limright = limright
    try:
        test = table[(table[limleft] > limright)]
    except:
        print('[!]语法错误!：没有找到', limleft, '列，请检查输入是否正确！')
        return
    return test


def sl_less_equal(operator, lim, table):
    '''
    选择：条件：小于等于的
    :param operator: 操作符
    :param lim: 限制条件
    :param table: 现在要操作的数据表
    :return:
    '''

    limleft = lim[0]
    limright = lim[2]
    # limright = int(limright)
    # print(limleft, operator, limright)
    try:
        limright = int(limright)
    except:
        try:
            limright = float(limright)
        except:
            limright = limright
    try:
        test = table[(table[limleft] <= limright)]
    except:
        print('[!]语法错误!：没有找到', limleft, '列，请检查输入是否正确！')
        return
    return test


def sl_more_equal(operator, lim, table):
    '''
    选择：条件：大于等于的
    :param operator: 操作符
    :param lim: 限制条件
    :param table: 现在要操作的数据表
    :return:
    '''
    limleft = lim[0]
    limright = lim[2]
    # limright = int(limright)
    # print(limleft, operator, limright)
    try:
        limright = int(limright)
    except:
        try:
            limright = float(limright)
        except:
            limright = limright
    try:
        test = table[(table[limleft] >= limright)]
    except:
        print('[!]语法错误!：没有找到', limleft, '列，请检查输入是否正确！')
        return
    return test


def agg_fun(Agg_list, columns, ed_table):
    """
    计算聚集函数
    :param Agg_list: 聚集函数名组成的列表(它和columns是对应的，
    对于没有聚集函数的列名对应的位置为''，有聚集函数的列名对应的位置为聚集函数名)
    :param columns: 数据表列名的列表
    :param ed_table: 要进行聚集函数运算的数据表
    :return: 1、用于存放聚集函数的得到的信息，格式如下：[列名，聚集函数名，聚集后的值]；2、用于存放聚集后的值
    """
    agg_col = [''] * len(columns)  # 创建一个与列名列表长度一致的列表，用于存放聚集函数的得到的信息，格式如下：[列名，聚集函数名，聚集后的值]
    agg_value = []  # 创建一个空列表，用于存放聚集后的值
    for i in range(len(Agg_list)):  # 循环查找用于聚集函数的列
        fg = Agg_list[i]  # 提取聚集函数的名称
        # print(fg)
        if fg == '':  # 如果没有聚集函数，就打断这次循环
            continue
        if fg == '*':  # 如果是*号，则说明是COUNT(*)，计算表中元组的数量，即有多少行
            countfg = ed_table.shape[0]  # 获取数据表的行数
            agg_col[i] = [columns[i], fg, countfg]  # 存放
            agg_value.append(countfg)  # 存放
            # print(columns[i], 'COUNT:', countfg)
            continue  # 打断循环，寻找下一个
        if fg == 'COUNT':  # 如果是COUNT,就是计算某一列的数量
            countfg = ed_table[columns[i]].count()  # 调用count函数
            agg_col[i] = [columns[i], fg, countfg]  # 存放
            agg_value.append(countfg)  # 存放
            # print(columns[i], 'COUNT:', countfg)
            continue  # 打断循环，寻找下一个
        if fg == 'SUM':  # 如果是SUM,就是计算某一列的和
            countfg = ed_table[columns[i]].sum()  # 调用sum函数
            agg_col[i] = [columns[i], fg, countfg]  # 存放
            agg_value.append(countfg)  # 存放
            # print(columns[i], 'SUM:', countfg)
            continue  # 打断循环，寻找下一个
        if fg == 'AVG':  # 如果是AVG,就是计算某一列的平均
            countfg = ed_table[columns[i]].mean()  # 调用mean函数
            agg_col[i] = [columns[i], fg, countfg]  # 存放
            agg_value.append(countfg)  # 存放
            # print(columns[i], 'AVG:', countfg)
            continue  # 打断循环，寻找下一个
        if fg == 'MAX':  # 如果是MAX,就是计算某一列的最大值
            countfg = ed_table[columns[i]].max()  # 调用max函数
            agg_col[i] = [columns[i], fg, countfg]  # 存放
            agg_value.append(countfg)  # 存放
            # print(columns[i], 'MAX:', countfg)
            continue  # 打断循环，寻找下一个
        if fg == 'MIN':  # 如果是MIN,就是计算某一列的最小值
            countfg = ed_table[columns[i]].min()  # 调用min函数
            agg_col[i] = [columns[i], fg, countfg]  # 存放
            agg_value.append(countfg)  # 存放
            # print(columns[i], 'MIN:', countfg)
            continue  # 打断循环，寻找下一个
    return agg_col, agg_value  # 返回存放的列表，到时候需要哪个用哪个


def select(using_dbname, columns, table_name, limit_where, con_limit, limit_group, limit_order, tag, having_limit=None):
    '''
    选择函数
    :param having_limit:HAVING限制条件
    :param using_dbname: 正在使用的数据库名称
    :param columns: select的列名
    :param table_name: 数据表名称
    :param limit_where: where限制条件(没啥用，之前写错了，现在用来判断有没有where限制条件)
    :param con_limit: where限制条件(这个是已经分割好的where限制条件)
    :param limit_group:group限制条件
    :param limit_order:order限制条件
    :param tag:返回标记符，目前未设置
    写于2021/1111/0516
    更新2021/1204/2034
    :return:
    '''
    if having_limit is None:
        having_limit = []
    if using_dbname == '':  # 如果数据库名字为空，就报错
        print('[!]请选择一个数据库！')
        return
    else:
        using_db = pd.read_excel('data/' + using_dbname + '.xlsx', sheet_name=None)
        pass
    pd.set_option('display.max_rows', None)
    pd.set_option('max_colwidth', 200)
    if isinstance(table_name, pd.DataFrame):
        table = table_name
    else:
        table_name = table_name[0]
        if table_name in using_db.keys():  # 选择表
            try:
                table = using_db[table_name]  # 获取数据表
            except:
                print('[!]查无此表！', table_name, '表没有找到')
                return
        elif os.path.exists('data/view/' + using_dbname + '/' + table_name + '.xlsx'):  # 选择视图
            try:
                view_db = pd.read_excel('data/view/' + using_dbname + '/' + table_name + '.xlsx',
                                        sheet_name=None)  # 获取数据表
                table = view_db[table_name]
            except:
                print('[!]查无此表！', table_name, '表没有找到')
                return
        else:
            print('[!]查无此表！', table_name, '表没有找到')
            return
    # print(columns)  # 输出一下列名
    allfg = False  # *(选择全部的)标记
    aggfg = False  # 聚集函数标记
    if columns[0] == '*':  # 如果第一个是*，就是全选，一般全选后面也不会有其他的列名了
        allfg = True  # 标记为全部
    Agg_list = [''] * len(columns)  # 创建一个与columns等长的列表，是由聚集函数名组成的列表
    columns_copy = columns[0:]  # 创建一个列名列表的拷贝，用于存放清洗掉聚集函数的列名，也就是纯列名，变化如下：MAX(Sage)->Sage
    for i in range(len(columns)):  # 聚集函数，遍历列名，寻找存在聚集函数的列
        count_col = re.search('COUNT\((.*)\)|count\((.*)\)', columns[i])  # 查找COUNT函数
        # print('count_col:', count_col)
        if count_col is None:  # 如果没有查到就赋值为''
            Agg_list[i] = ''
        elif count_col[0] == '*':  # 如果是*，就是全选得到意思
            columns_copy[i] = count_col[0][6:-1]  # 提取列名
            Agg_list[i] = '*'  # 标记*
            allfg = True  # 选择全部的标记
            aggfg = True  # 拥有聚集函数的标记
            continue  # 打断这次循环
        else:  # COUNT函数
            columns_copy[i] = count_col[0][6:-1]  # 提取列名
            Agg_list[i] = 'COUNT'  # 标记COUNT
            aggfg = True  # 拥有聚集函数的标记
            continue  # 打断这次循环
        sum_col = re.search('SUM\((.*)\)|sum\((.*)\)', columns[i])  # 查找SUM函数
        if sum_col is None:  # 如果没有查到就赋值为''
            Agg_list[i] = ''
        else:  # SUM函数
            columns_copy[i] = sum_col[0][4:-1]  # 提取列名
            Agg_list[i] = 'SUM'  # 标记SUM
            aggfg = True  # 拥有聚集函数的标记
            continue  # 打断这次循环
        avg_col = re.search('AVG\((.*)\)|avg\((.*)\)', columns[i])  # 查找AVG函数
        if avg_col is None:  # 如果没有查到就赋值为''
            Agg_list[i] = ''
        else:  # AVG函数
            columns_copy[i] = avg_col[0][4:-1]  # 提取列名
            Agg_list[i] = 'AVG'  # 标记AVG
            aggfg = True  # 拥有聚集函数的标记
            continue  # 打断这次循环
        max_col = re.search('MAX\((.*)\)|max\((.*)\)', columns[i])
        if max_col is None:  # 如果没有查到就赋值为''
            Agg_list[i] = ''
        else:  # MAX函数
            columns_copy[i] = max_col[0][4:-1]  # 提取列名
            Agg_list[i] = 'MAX'  # 标记MAX
            aggfg = True  # 拥有聚集函数的标记
            continue  # 打断这次循环
        min_col = re.search('MIN\((.*)\)|min\((.*)\)', columns[i])
        if min_col is None:  # 如果没有查到就赋值为''
            Agg_list[i] = ''
        else:  # MIN函数
            columns_copy[i] = min_col[0][4:-1]  # 提取列名
            Agg_list[i] = 'MIN'  # 标记MIN
            aggfg = True  # 拥有聚集函数的标记
            continue  # 打断这次循环
    # print(columns_copy)  # 输出一下纯列名
    # print(Agg_list)  # 输出一下聚集函数标记列表
    if len(limit_where) == 0:  # 如果没有WHERE限制
        new_table = table  # 这个表就是新表
    else:  # 有WHERE限制
        predicate = con_limit[-1]  # 获取谓词，也就是连接词，如果没有是空格' ',支持的所有谓词如下：
        # predicate = ' ',AND,OR,IN,NOTIN,BETWEENAND,NOTBETWEENAND.LIKE,NOTLIKE
        # print('predicate:', predicate)  # 打印，显示谓词
        new_table = table  # 新表，为空
        # SELECT Sno,Sname FROM Student WHERE Sdept='CS'
        # SELECT Sno,Sname FROM Student WHERE Sdept='CS' AND Sage<20 group by Sno order by Sname
        if predicate == ' ':  # 如果没有谓词，也就是说WHERE只有一个限制条件

            limit = con_limit[:-1]  # 获取where限制条件，去掉谓词标记，谓词标记是列表的最后一个
            # print(limit)  # 输出一下
            # 选择 ' '条件
            print(limit)
            for lim in limit:  # 循环选择限制条件，其实限制条件就一个，之前写的，也没啥影响，就没改
                print(lim)
                operator = lim[1]  # lim格式为[列名,操作符,值]
                print(operator)  # 提取出新表
                if operator == '=':
                    new_table = sl_equal(operator, lim, table)
                if operator == '<':
                    new_table = sl_less(operator, lim, table)
                if operator == '>':
                    new_table = sl_more(operator, lim, table)
                if operator == '<=':
                    new_table = sl_less_equal(operator, lim, table)
                if operator == '>=':
                    new_table = sl_more_equal(operator, lim, table)
                if operator == '!=' or operator == '<>':
                    new_table = sl_not_equal(operator, lim, table)
        # SELECT Sno,Sname FROM Student WHERE Sdept='CS' OR Sage<19
        if predicate == 'OR':  # 如果谓词是OR
            limit = con_limit[:-1]  # 获取where限制条件，去掉谓词标记，谓词标记是列表的最后一个
            # print(limit)  # 输出一下
            # 选择 OR条件
            # 因为OR是成立一个条件就行，所以把每个条件都选择出来一个结果表，存到table_list中，然后最后拼接到一起
            table_list = []  # 用于存放选择后的表，
            table_copy = table  # 复制一下表
            for lim in limit:  # 循环选择限制条件
                operator = lim[1]  # lim格式为[列名,操作符,值]
                # 提取出新表
                if operator == '=':
                    table_copy = sl_equal(operator, lim, table)
                if operator == '<':
                    table_copy = sl_less(operator, lim, table)
                if operator == '>':
                    table_copy = sl_more(operator, lim, table)
                if operator == '<=':
                    table_copy = sl_less_equal(operator, lim, table)
                if operator == '>=':
                    table_copy = sl_more_equal(operator, lim, table)
                if operator == '!=' or operator == '<>':
                    table_copy = sl_not_equal(operator, lim, table)
                table_list.append(table_copy)  # 然后把每个新表都添加到table_list中
            if len(table_list) > 0:  # 新表的数量大于1
                new_table = table_list[0]  # 选择第一个作为基准表，后面的表都要拼接到这个表中
            for i in range(1, len(table_list)):  # 循环读取新表
                new_table = pd.concat([new_table, table_list[i]])  # 把每个新表拼接到基准表new_table中
        # SELECT Sno,Sname FROM Student WHERE Sage=20 AND Ssex='男'
        # SELECT Sno,Sname FROM Student WHERE Sage<20 AND Ssex='女'
        if predicate == 'AND':  # 如果谓词是AND
            limit = con_limit[:-1]
            # print(limit)
            # 选择 AND条件
            # 按顺序提取新表，然后下一个条件再在第一次的新表中提取一个新新表，如此循环
            table_copy = table  # 复制一下表
            for lim in limit:  # 循环选择限制条件
                operator = lim[1]  # lim格式为[列名,操作符,值]
                if operator == '=':
                    table_copy = sl_equal(operator, lim, table_copy)
                if operator == '<':
                    table_copy = sl_less(operator, lim, table_copy)
                if operator == '>':
                    table_copy = sl_more(operator, lim, table_copy)
                if operator == '<=':
                    table_copy = sl_less_equal(operator, lim, table_copy)
                if operator == '>=':
                    table_copy = sl_more_equal(operator, lim, table_copy)
                if operator == '!=' or operator == '<>':
                    table_copy = sl_not_equal(operator, lim, table_copy)
            new_table = table_copy  # 获取最后的新表
            # print(new_table)
        # SELECT Sno,Sname FROM Student WHERE Sdept in ('CS','MA')
        if predicate == 'IN':  # 如果谓词是IN
            column = con_limit[0]  # 提取列名
            # print(column, end=' ')  # 输出一下
            limit = con_limit[1]  # 提取信息
            # print(limit)  # 输出信息
            try:
                new_table = table[table[column].isin(limit)]  # 提取新表
            except:
                print('[!]语法错误!：没有找到', column, '列，请检查输入是否正确！')
                return
            # print(new_table)
        # SELECT Sno,Sname FROM Student WHERE Sdept not in ('CS','MA')
        if predicate == 'NOTIN':  # 如果谓词是NOTIN
            column = con_limit[0]  # 提取列名
            # print(column, end=' ')  # 输出一下
            limit = con_limit[1]  # 提取信息
            # print(limit)  # 输出信息
            try:
                new_table = table[~table[column].isin(limit)]  # 提取新表
            except:
                print('[!]语法错误!：没有找到', column, '列，请检查输入是否正确！')
                return
            # print(new_table)
        # SELECT Sno,Sname FROM Student WHERE Sage between 18 and 19
        if predicate == 'BETWEENAND':  # 如果谓词是BETWEENAND
            column = con_limit[0]  # 提取列名
            minn = int(con_limit[1][0])  # 提取min值
            maxx = int(con_limit[1][1])  # 提取max值
            limit = list(range(minn, maxx + 1))  # min到max的所有整数值
            # print(limit)  # 输出信息
            try:
                new_table = table[table[column].isin(limit)]  # 提取新表
            except:
                print('[!]语法错误!：没有找到', column, '列，请检查输入是否正确！')
                return
            # print(new_table)
        # SELECT Sno,Sname FROM Student WHERE Sage not between 18 and 19
        if predicate == 'NOTBETWEENAND':  # 如果谓词是NOTBETWEENAND
            column = con_limit[0]  # 提取列名
            minn = int(con_limit[1][0])  # 提取min值
            maxx = int(con_limit[1][1])  # 提取max值
            limit = list(range(minn, maxx + 1))  # min到max的所有整数值
            # print(limit)
            try:
                new_table = table[~table[column].isin(limit)]  # 提取新表
            except:
                print('[!]语法错误!：没有找到', column, '列，请检查输入是否正确！')
                return
        # SELECT Sname,Sno,Ssex FROM Student WHERE Sname LIKE '刘%'
        # SELECT Cno,Ccredit FROM Course WHERE Cname LIKE 'DB\_Design' ESPCAPE'\'
        if predicate == 'LIKE':  # 如果谓词是LIKE
            column = con_limit[0]  # 获取列名
            limit = con_limit[1]  # 获取限制条件
            if con_limit[2] != 'LIKE':  # 不是LIKE就是拥有通配符
                escape = con_limit[2][-2]  # 获取通配符
                # print(escape)
                wc_str = limit[0].replace('%', '(.*)').replace('_', '(.)').replace(escape + '(.*)', '%').replace(
                    escape + '(.)', '_')  # 进行替换，构造正则中的模式字符串
            else:  # 没有通配符
                wc_str = limit[0].replace('%', '(.*)').replace('_', '(.)')  # 进行替换，构造正则中的模式字符串
            try:  # 获取对应列的数据构造成列表
                col_list = table[column].tolist()
            except:  # 输出报错
                print('[!]语法错误!：没有找到', column, '列')
                return
            name_list = []  # 用于存放符合LIKE的数据的列表
            for i in col_list:  # 循环匹配正则
                s = re.search(wc_str, i)  # 匹配正则
                try:  # 匹配到了存入列表
                    name_list.append(s[0])
                except:  # 匹配不到就抛出
                    ''
            try:  # 选择符合LIKE条件的表
                new_table = table[table[column].isin(name_list)]
            except:  # 报错，抛出异常
                print('[!]语法错误!：没有找到', column, '列，请检查输入是否正确！')
                return
            # print(new_table)
    # print(new_table)  # 输出一下选择后的新表
    # print(limit_order)  # 打印一下order排序限制条件
    # 处理排序条件
    if len(limit_order) != 0:  # 如果有排序限制条件
        # table.sort_values(by=['Sage', 'Sno'], ascending=[1, 0])
        by_list = [x[0] for x in limit_order]  # 提取需要排序的的列名
        # print(by_list)  # 输出一下
        asc_list = []  # 保存是升序还是降序的列表
        for lim in limit_order:  # 循环判断是否是升序降序
            if len(lim) == 1 or lim[1].upper() == 'ASC':  # 如果只有一个元素就是默认是升序，或者如果是ASC就是升序
                asc_list.append(1)  # 升序排序存入1
                continue
            if lim[1].upper() == 'DESC':  # 如果是DESC就是降序
                asc_list.append(0)  # 降序排序存入0
                continue
        # print(asc_list)  # 输出一下列表
        sorted_table = new_table.sort_values(by=by_list, ascending=asc_list)  # 按照by_list(根据排序的列)和asc_list(排序顺序)排序
        # print(sorted_table)  # 输出一下
        new_table = sorted_table  # 将排好序的表复制给new_table
    # print(allfg)  # 输出是否全选的标记
    if allfg:  # 如果是要全选，就是输入的*
        lim_table = new_table  # 就把新表给限制表
    else:  # 如果选择了列，就是不需要全选
        try:
            # print(len(columns_copy))  # 输出一下列名
            lim_table = new_table[[columns_copy[0]]]  # 用第一列做基准表，以后其他的都要拼接到这个表上，用两层中括号就是为了把Serise类型转化为DataFrame格式，方便后面拼接
            for i in range(1, len(columns_copy)):  # 从1开始循环，开始拼接
                lim_table = pd.concat([lim_table, new_table[columns_copy[i]]], axis=1)  # 按列拼接
        except:
            print('[!]拼接错误！：可能出现意外的列名！')
            return
    # 输出lim_table
    # print('lim_table:')
    # print(lim_table)  # 输出lim_table
    # print(limit_group)  # 输出group限制条件
    Agg_value = []  # 把聚集函数的列表中的空值('')去掉
    for i in Agg_list:  # 循环遍历
        if i != '':  # 非空放入
            Agg_value.append(i)
    # Agg_value = [x if x != '' else  for x in Agg_list]
    columns_agg = []  # 把拥有聚集函数的列名保存下来
    for i in range(len(Agg_list)):  # 遍历循环
        if Agg_list[i] == '':  # 如果是空就是跳出，留下非空的
            continue
        columns_agg.append(columns[i])  # 把对应的列名(带聚集函数的列名)存入
    # print(Agg_value)  # 输出聚集函数list
    # print(columns_agg)  # 输出聚集函数的列名的list
    grouped_list = []  # 存储分组后表的列表
    grouped_index = []  # 存储分组的列的信息
    # 处理分组条件
    if len(limit_group) != 0:  # 如果存在分组条件
        grouped_lim_table = lim_table.groupby(limit_group)  # 调用函数分组
        # 判断分组的条件列名是否属于列表类型，如果是就转化为元组，因为DataFrame不允许列表做列名
        if isinstance(limit_group, list) and len(limit_group) == 1:  # 列表元素只有1个，取出来就行
            lim_group = limit_group[0]
        elif isinstance(limit_group, list) and len(limit_group) > 1:  # 列表元素大于1个，转化为元组
            lim_group = tuple(limit_group)
        else:
            return
        columns_agg.insert(0, lim_group)  # 把转换好的列名插入到存在聚集函数的列名中
        # print(grouped_lim_table.size().index)  # 输出分组条件的列的值
        for index in grouped_lim_table.size().index:  # 循环提取分组条件的列的值
            grouped_index.append(index)  # 把分组条件的列的值加入到list中
            grouped_list.append(grouped_lim_table.get_group(index))  # 把分好的表添加到list中
        grouped_dict = dict(map(lambda x, y: [x, y], grouped_index, grouped_list))  # 把两个列表组成字典
        # 显示一下分组的信息
        # for grouped_key, grouped_value in grouped_dict.items():
        #     print(grouped_key, ':')
        #     print(grouped_value)
        # 如果有聚集函数标记
        if aggfg:
            aggfg_list = []  # 存放分组后每个组的信息的list[[分组依据的值,对应的聚集函数的值],[]]
            for grouped_key, grouped_value in grouped_dict.items():  # 循环遍历
                try:
                    fg_list, fg_value = agg_fun(Agg_list, columns_copy, grouped_value)  # 获取值
                    fg_value.insert(0, grouped_key)  # 将分组的条件的值与聚集后的值插在一起
                except:
                    return
                aggfg_list.append(fg_value)  # 把每个组的信息放到list中
            # print(columns_agg)  # 输出，查看列名
            # print(aggfg_list)  # 输出，其应该是二维列表
            grouped_df = pd.DataFrame(aggfg_list)  # 转化为DataFrame格式，转化完后没有列名，所以下面要重命名列名
            col_ind = []  # 用于存放id，即默认列名为：0，1，2，3，
            for i in range(len(columns_agg)):  # 按照列名的数量创建一个id列表
                col_ind.append(i)
            name_dicts = dict(map(lambda x, y: [x, y], col_ind, columns_agg))  # id列表和真正的列名列表合并成一个字典
            grouped_df.rename(columns=name_dicts, inplace=True)  # 重命名列名并生效
            # print(grouped_df)  # 输出显示
            # print(having_limit)
            # SELECT Sno FROM SC GROUP BY Sno HAVING COUNT(*)>2
            # SELECT Sno,AVG(Grade) FROM SC GROUP BY Sno HAVING AVG(Grade)>=90
            if len(having_limit) != 0:
                grouped_df_copy = grouped_df
                having_limit = having_limit[0]
                if having_limit[0] in grouped_df.columns:
                    operator = having_limit[1]
                    lim = having_limit
                    if operator == '=':
                        grouped_df_copy = sl_equal(operator, lim, grouped_df)
                    if operator == '<':
                        grouped_df_copy = sl_less(operator, lim, grouped_df)
                    if operator == '>':
                        grouped_df_copy = sl_more(operator, lim, grouped_df)
                    if operator == '<=':
                        grouped_df_copy = sl_less_equal(operator, lim, grouped_df)
                    if operator == '>=':
                        grouped_df_copy = sl_more_equal(operator, lim, grouped_df)
                    if operator == '!=' or operator == '<>':
                        grouped_df_copy = sl_not_equal(operator, lim, grouped_df)
                    return grouped_df_copy
                elif having_limit[0] == 'COUNT(*)' or having_limit[0] == 'count(*)':
                    df_keys = []
                    df_rows = []
                    for grouped_key, grouped_value in grouped_dict.items():
                        df_keys.append(grouped_key)
                        df_rows.append(grouped_value.shape[0])
                    keys_rows = dict(map(lambda x, y: [x, y], df_keys, df_rows))
                    # print(keys_rows)
                    grouped_dict_copy = grouped_dict
                    operator = having_limit[1]
                    limright = having_limit[2]
                    try:
                        limright = int(limright)
                    except:
                        limright = limright
                    # print(limright)
                    if operator == '=':
                        for i in range(len(df_rows)):
                            if df_rows[i] != limright:
                                del grouped_dict_copy[df_keys[i]]
                    if operator == '<':
                        for i in range(len(df_rows)):
                            if df_rows[i] >= limright:
                                del grouped_dict_copy[df_keys[i]]
                    if operator == '>':
                        for i in range(len(df_rows)):
                            if df_rows[i] <= limright:
                                del grouped_dict_copy[df_keys[i]]
                    if operator == '<=':
                        for i in range(len(df_rows)):
                            if df_rows[i] > limright:
                                del grouped_dict_copy[df_keys[i]]
                    if operator == '>=':
                        for i in range(len(df_rows)):
                            if df_rows[i] < limright:
                                del grouped_dict_copy[df_keys[i]]
                    if operator == '!=' or operator == '<>':
                        for i in range(len(df_rows)):
                            if df_rows[i] == limright:
                                del grouped_dict_copy[df_keys[i]]
                    print_dict(grouped_dict_copy)
                    if len(grouped_dict_copy) == 0:
                        print('[*]没有查询到结果')
                        return
                    # return grouped_dict_copy
                else:
                    print('[!]语法错误!:HAVING语法错误，请检查后再次输入！')
                    return
            else:
                return grouped_df  # 返回DataFarme类型的表(数据表)
        else:  # 如果没有聚集函数存在
            print(having_limit)
            if len(having_limit) != 0:
                having_limit = having_limit[0]
                if having_limit[0] == 'COUNT(*)' or having_limit[0] == 'count(*)':
                    df_keys = []
                    df_rows = []
                    for grouped_key, grouped_value in grouped_dict.items():
                        df_keys.append(grouped_key)
                        df_rows.append(grouped_value.shape[0])
                    keys_rows = dict(map(lambda x, y: [x, y], df_keys, df_rows))
                    print(keys_rows)
                    grouped_dict_copy = grouped_dict
                    operator = having_limit[1]
                    limright = having_limit[2]
                    try:
                        limright = int(limright)
                    except:
                        limright = limright
                    print(limright)
                    if operator == '=':
                        for i in range(len(df_rows)):
                            if df_rows[i] != limright:
                                del grouped_dict_copy[df_keys[i]]
                    if operator == '<':
                        for i in range(len(df_rows)):
                            if df_rows[i] >= limright:
                                del grouped_dict_copy[df_keys[i]]
                    if operator == '>':
                        for i in range(len(df_rows)):
                            if df_rows[i] <= limright:
                                del grouped_dict_copy[df_keys[i]]
                    if operator == '<=':
                        for i in range(len(df_rows)):
                            if df_rows[i] > limright:
                                del grouped_dict_copy[df_keys[i]]
                    if operator == '>=':
                        for i in range(len(df_rows)):
                            if df_rows[i] < limright:
                                del grouped_dict_copy[df_keys[i]]
                    if operator == '!=' or operator == '<>':
                        for i in range(len(df_rows)):
                            if df_rows[i] == limright:
                                del grouped_dict_copy[df_keys[i]]
                    print_dict(grouped_dict_copy)
                    if len(grouped_dict_copy) == 0:
                        print('[*]没有查询到结果')
                        return
                else:
                    print('[!]语法错误!:HAVING语法错误，请检查后再次输入！')
                    return
                # return grouped_dict_copy
            else:
                print_dict(grouped_dict)
                return grouped_dict  # 这是一个字典类型，其中key是分组的值，value是依据此分组的表(DataFrame格式)
    else:  # 如果没有分组限制条件
        if aggfg:  # 如果有聚集函数存在
            fg_list, fg_value = agg_fun(Agg_list, columns_copy, lim_table)  # 获取值
            # print(fg_value)
            fg_df = pd.DataFrame(fg_value)  # 转换为DataFrame格式
            fg_df = fg_df.T  # 转置
            # 对表进行重命名
            col_ind = []  # 用于存放id，即默认列名为：0，1，2，3，
            for i in range(len(columns_agg)):  # 按照列名的数量创建一个id列表
                col_ind.append(i)
            name_dicts = dict(map(lambda x, y: [x, y], col_ind, columns_agg))  # id列表和真正的列名列表合并成一个字典
            fg_df.rename(columns=name_dicts, inplace=True)  # 重命名列名并生效
            # print(fg_df)  # 输出显示
            columns_notagg = []  # 用于存放没有聚集函数的列名
            for i in range(len(Agg_list)):  # 循环遍历
                if Agg_list[i] == '':  # 是空就加入
                    columns_notagg.append(columns[i])
            try:
                notagg_table = lim_table[[columns_notagg[0]]]  # 设定一个基准表
                for i in range(1, len(columns_notagg)):  # 从1开始循环，开始拼接
                    notagg_table = pd.concat([notagg_table, lim_table[columns_notagg[i]]], axis=1)  # 按列拼接
                # print(notagg_table)
                return fg_df, notagg_table  # 返回聚集函数值和普通的列的select表(数据表)
            except:
                return fg_df  # 返回聚集函数的值(数据表)
        else:  # 如果没有聚集函数存在
            return lim_table  # 直接返回表(数据表)
    # SELECT Sdept,AVG(Sage),MAX(Sbron) FROM Student GROUP BY Sdept
    # SELECT AVG(Grade) FROM SC WHERE Cno='1'
    # SELECT Sno,Sname FROM Student WHERE Sage<20 group by Sno
    # SELECT Sdept,AVG(Sage) FROM Student GROUP BY Sdept
    # SELECT Student.Sno,Sname FROM Student,SC WHERE Student.Sno=SC.Sno AND SC.Cno='2' AND SC.Grade>90
    # SELECT Cno,COUNT(Sno) FROM SC GROUP BY Cno HAVING COUNT(*)>3


def sql_Analysis(using_dbname, sql, tag=''):
    '''
    select语义分析
    :param using_dbname: 数据库名称
    :param sql: sql语句
    :param tag: 是否返回
    :return: 返回查询的表
    '''
    pd.set_option('display.max_rows', None)
    pd.set_option('max_colwidth', 200)

    sql = sql.strip()
    sql_word = sql.split(' ')  # 分割sql语句
    if len(sql_word) < 2:  # 如果语句太短就不对
        print('[!]语法错误')
        return
    operate = sql_word[0].lower()  # 操作名
    # SELECT Sno,Sname,Sdept FROM Student WHERE Sdept IN (SELECT Sdept FROM Student WHERE Sname='刘晨')
    # SELECT Sno,Sname FROM Student WHERE Sdept='CS' AND Sage<20 group by Sno order by Sname ASC,Sno DESC
    if operate == 'select':  # 如果是选择
        pos_where = -1  # 标记where的位置
        pos_group = -2  # 标记group的位置
        pos_order = -3  # 标记order的位置
        pos_union = -4
        pos_intersect = -5
        pos_except = -6
        pos_having = -7
        # print(operate.upper(), end=' ')  # 输出 操作名
        columns = sql_word[1].split(',')  # 提取分割 列名
        # print(columns)  # 输出 列名
        # print(sql_word[2], end=' ')  # 输出FROM
        table_name = sql_word[3].split(',')  # 提取 数据表名称
        # print(table_name)  # 输出 数据表名称
        Asql_word = [x.upper() for x in sql_word]  # 全变大写，方便查找
        try:  # 获取WHERE位置
            pos_where = Asql_word.index('WHERE')
        except:
            pos_where = -1
        try:  # 获取GROUP位置
            pos_group = Asql_word.index('GROUP')
        except:
            pos_group = -2
        try:  # 获取ORDER位置
            pos_order = Asql_word.index('ORDER')
        except:
            pos_order = -3
        try:  # 获取UNIOM位置
            pos_union = Asql_word.index('UNION')
        except:
            pos_union = -4
        try:  # 获取INTERSECT位置
            pos_intersect = Asql_word.index('INTERSECT')
        except:
            pos_intersect = -5
        try:  # 获取EXCEPT位置
            pos_except = Asql_word.index('EXCEPT')
        except:
            pos_except = -6
        try:  # 获取EXCEPT位置
            pos_having = Asql_word.index('HAVING')
        except:
            pos_having = -7
        # print(pos_where)
        # print(pos_group)
        # print(pos_order)
        # where>group>order
        # SELECT Cno,COUNT(Sno) FROM SC GROUP BY Cno HAVING COUNT(*)>1
        # if pos_where!= -1 and pos_group != -2:
        #     print('[!]语法错误')
        #     return
        having_limit = []
        if pos_having != -7:
            having_limit.append(re.split(r'(>=|<=|!=|<>|!>|!<|=|<|>)', sql_word[pos_having + 1:][0]))
        # print(having_limit)
        # 集合查询
        # SELECT * FROM Student WHERE Sdept='CS' UNION SELECT * FROM Student WHERE Sage<=19
        if pos_union != -4:  # 并操作
            sql_sl1_list = sql_word[0:pos_union]
            sql_sl1 = ' '.join(sql_sl1_list)
            # print("sql1", sql_sl1)
            print('sql1 select start----------------------------------------------------------------')
            sl1 = sql_Analysis(using_dbname, sql_sl1, tag='return')
            print('sql1 select end------------------------------------------------------------------')
            sql_sl2_list = sql_word[pos_union + 1:]
            # print(sql_sl2_list)
            sql_sl2 = ' '.join(sql_sl2_list)
            # print("sql2", sql_sl2)
            print('sql2 select start----------------------------------------------------------------')
            sl2 = sql_Analysis(using_dbname, sql_sl2, tag='return')
            print('sql2 select end------------------------------------------------------------------')
            # print(sl1)
            # print(sl2)
            # pd.merge(df1,df2,on=['name', 'age', 'sex']))
            columns_sl1 = sl1.columns
            columns_sl2 = sl2.columns
            # print(columns_sl1)
            # print(columns_sl2)
            for cl1, cl2 in zip(columns_sl1, columns_sl2):
                if cl1 != cl2:
                    print('[!]两次查询的列不匹配')
                    return
            new_table = pd.merge(sl1, sl2, on=list(columns_sl1), how='outer')
            print("new ")
            print(new_table)
            return new_table
        # SELECT * FROM Student WHERE Sdept='CS' intersect SELECT * FROM Student WHERE Sage<=19
        if pos_intersect != -5:  # 交操作
            sql_sl1_list = sql_word[0:pos_intersect]
            sql_sl1 = ' '.join(sql_sl1_list)
            sql_sl2_list = sql_word[pos_intersect + 1:]
            sql_sl2 = ' '.join(sql_sl2_list)
            # print(sql_sl1)
            print('sql1 select start----------------------------------------------------------------')
            sl1 = sql_Analysis(using_dbname, sql_sl1, tag='return')
            print('sql1 select end------------------------------------------------------------------')
            # print(sql_sl2)
            print('sql2 select start----------------------------------------------------------------')
            sl2 = sql_Analysis(using_dbname, sql_sl2, tag='return')
            print('sql2 select end------------------------------------------------------------------')
            # print(sl1)
            # print(sl2)
            # pd.merge(df1,df2,on=['name', 'age', 'sex']))
            columns_sl1 = sl1.columns
            columns_sl2 = sl2.columns
            # print(columns_sl1)
            # print(columns_sl2)
            for cl1, cl2 in zip(columns_sl1, columns_sl2):
                if cl1 != cl2:
                    print('[!]两次查询的列不匹配')
                    return
            new_table = pd.merge(sl1, sl2, on=list(columns_sl1))
            print(new_table)
            return new_table
        # SELECT * FROM Student WHERE Sdept='CS' except SELECT * FROM Student WHERE Sage<=19
        if pos_except != -6:  # 差操作
            sql_sl1_list = sql_word[0:pos_except]
            sql_sl1 = ' '.join(sql_sl1_list)
            sql_sl2_list = sql_word[pos_except + 1:]
            sql_sl2 = ' '.join(sql_sl2_list)
            # print(sql_sl1)
            print('sql1 select start----------------------------------------------------------------')
            sl1 = sql_Analysis(using_dbname, sql_sl1, tag='return')
            print('sql1 select end------------------------------------------------------------------')
            # print(sql_sl2)
            print('sql2 select start----------------------------------------------------------------')
            sl2 = sql_Analysis(using_dbname, sql_sl2, tag='return')
            print('sql2 select end------------------------------------------------------------------')
            # print(sl1)
            # print(sl2)
            # pd.merge(df1,df2,on=['name', 'age', 'sex']))
            columns_sl1 = sl1.columns
            columns_sl2 = sl2.columns
            # print(columns_sl1)
            # print(columns_sl2)
            for cl1, cl2 in zip(columns_sl1, columns_sl2):
                if cl1 != cl2:
                    print('[!]两次查询的列不匹配')
                    return
            new_table = sl1.append(sl2).append(sl2).drop_duplicates(keep=False)
            # new_table = sl1.loc[sl1.index.difference(sl2.index)]  # 取差集
            print(new_table)
            return new_table
        con_limit = []  # 分割存储 where限制条件
        limit_where = []  # 存储 where限制条件
        limit_group = []  # 存储 group限制条件
        limit_order = []  # 存储 order限制条件
        if pos_where != -1:  # 如果存在where限制条件
            # 确定where限制条件最后的位置
            if pos_group != -2:
                pos_end = pos_group
            elif pos_order != -3:
                pos_end = pos_order
            else:
                pos_end = len(sql_word)
            # print(sql_word[4], end=' ')  # 输出WHERE
            limit_where = sql_word[pos_where + 1:pos_end]  # 存放WHERE限制条件
            # print(limit_where)  # 输出
            # 判断谓词，提取谓词
            # 提取AND信息
            if 'BETWEEN' not in Asql_word and 'AND' in Asql_word:
                subqueries = 'AND'
                for i in range(0, len(limit_where), 2):
                    con_limit.append(re.split(r'(>=|<=|!=|<>|!>|!<|=|<|>)', limit_where[i]))
                con_limit.append('AND')
            # 提取OR信息
            if 'OR' in Asql_word:
                subqueries = 'OR'
                for i in range(0, len(limit_where), 2):
                    con_limit.append(re.split(r'(>=|<=|!=|<>|!>|!<|=|<|>)', limit_where[i]))
                con_limit.append('OR')
            # 提取IN信息
            # select Sname,Ssex from Student where Sdept in ('CS','MA','IS')
            # SELECT Sno,Sname,Sdept FROM Student WHERE Sdept IN (SELECT Sdept FROM Student WHERE Sname='刘晨')
            # SELECT Sno,Sname FROM Student WHERE Sno IN (SELECT Sno FROM SC WHERE Cno IN (SELECT Cno FROM Course WHERE Cname='信息系统'))
            if 'NOT' not in Asql_word and 'IN' in Asql_word:
                subqueries = 'IN'
                con_1 = limit_where[0]
                # print('limwhe2', limit_where[2])
                limit_where_2 = limit_where[2:pos_end]
                # print(limit_where_2)
                if limit_where_2[0].upper() != '(SELECT':
                    con_2 = re.split(r'[(|)|\'|,]', limit_where[2])
                    # print('con2', con_2)
                    con_2 = [item for item in filter(lambda x: x != '', con_2)]
                    con_limit.append(con_1)
                    con_limit.append(con_2)
                    con_limit.append('IN')
                else:  # 嵌套查询(子查询)
                    sql_sel = ' '.join(limit_where_2)[1:-1]
                    # print(sql_sel)
                    print('select start----------------------------------------------------------------')
                    sss = sql_Analysis(using_dbname, sql_sel, tag='return')
                    print('select end------------------------------------------------------------------')
                    # print(sss)
                    con_2 = sss[limit_where_2[1]].tolist()
                    con_limit.append(con_1)
                    con_limit.append(con_2)
                    con_limit.append('IN')
                    # return
            # 提取NOT IN信息
            if 'NOT' in Asql_word and 'IN' in Asql_word:
                subqueries = 'NOTIN'
                con_1 = limit_where[0]
                con_2 = re.split(r'[(|)|\'|,]', limit_where[3])
                con_2 = [item for item in filter(lambda x: x != '', con_2)]
                con_limit.append(con_1)
                con_limit.append(con_2)
                con_limit.append('NOTIN')
            # 提取BETWEEN AND信息
            if 'NOT' not in Asql_word and 'BETWEEN' in Asql_word and 'AND' in Asql_word:
                subqueries = 'BETWEENAND'
                con_1 = limit_where[0]

                if int(limit_where[2]) <= int(limit_where[4]):
                    con_2 = [limit_where[2], limit_where[4]]
                else:
                    print('BETWEEN AND的MIN,MAX值错误')
                    return
                con_limit.append(con_1)
                con_limit.append(con_2)
                con_limit.append('BETWEENAND')
            # 提取NOT BETWEEN AND信息
            if 'NOT' in Asql_word and 'BETWEEN' in Asql_word and 'AND' in Asql_word:
                subqueries = 'NOTBETWEENAND'
                con_1 = limit_where[0]
                # con_2 = [limit_where[3], limit_where[5]]
                if int(limit_where[3]) <= int(limit_where[5]):
                    con_2 = [limit_where[3], limit_where[5]]
                else:
                    print('BETWEEN AND的MIN,MAX值错误')
                    return
                con_limit.append(con_1)
                con_limit.append(con_2)
                con_limit.append('NOTBETWEENAND')
            # 提取LIKE信息
            if 'NOT' not in Asql_word and 'LIKE' in Asql_word:
                subqueries = 'LIKE'
                # print(limit_where)
                con_1 = limit_where[0]
                con_2 = re.split(r'[(|)|\'|,]', limit_where[2])
                con_2 = [item for item in filter(lambda x: x != '', con_2)]
                con_limit.append(con_1)
                con_limit.append(con_2)
                try:
                    con_3 = limit_where[3]
                    con_limit.append(con_3)
                except:
                    ''
                con_limit.append('LIKE')
            # 提取NOT LIKE信息
            if 'NOT' in Asql_word and 'LIKE' in Asql_word:
                subqueries = 'NOTLIKE'
                con_1 = limit_where[0]
                con_2 = re.split(r'[(|)|\'|,]', limit_where[3])
                con_2 = [item for item in filter(lambda x: x != '', con_2)]
                con_limit.append(con_1)
                con_limit.append(con_2)
                con_limit.append('NOTLIKE')
            # 提取IS NULL信息
            if 'IS' in Asql_word and 'NOT' not in Asql_word and 'NULL' in Asql_word:
                subqueries = 'ISNULL'
                con_1 = limit_where[0]
                con_limit.append(con_1)
                con_limit.append('ISNULL')
            # 提取IS NOT NULL信息
            if 'IS' in Asql_word and 'NOT' in Asql_word and 'NULL' in Asql_word:
                subqueries = 'ISNOTNULL'
                con_1 = limit_where[0]
                con_limit.append(con_1)
                con_limit.append('ISNOTNULL')
            # 如果没有谓词，直接提取
            if len(con_limit) == 0:
                for i in range(0, len(limit_where), 2):
                    con_limit.append(re.split(r'(>=|<=|!=|<>|!>|!<|=|<|>)', limit_where[i]))
                con_limit.append(' ')  # 标记为' '
            # print(con_limit)  # 输出
        if pos_group != -2:  # 如果存在group限制条件
            # 确定group限制条件最后的位置
            if pos_order != -3:
                pos_end = pos_order
            else:
                pos_end = len(sql_word)
            # print(sql_word[pos_group].upper(), sql_word[pos_group + 1].upper(), end=' ')  # 输出信息
            limit_group = sql_word[pos_group + 1 + 1:pos_end]  # 存放gruop限制条件
            limit_group = limit_group[0].split(',')  # 分割条件
            # print(limit_group)  # 显示输出
        if pos_order != -3:  # 如果存在order限制条件
            # 确定order限制条件最后的位置
            pos_end = len(sql_word)
            # print(sql_word[pos_order].upper(), sql_word[pos_order + 1].upper(), end=' ')  # 输出信息
            limit_or = sql_word[pos_order + 1 + 1:pos_end]  # 存放order限制条件
            # print(limit_or)  # 输出显示
            lim_s = ' '.join(limit_or)  # 用空格(' ')拼接列表成为字符串
            lim_ss = lim_s.split(',')  # 重新分割
            lim_sss = [x.split(' ') for x in lim_ss]  # 分割每个子项
            limit_order = lim_sss  # 赋值
        # print(limit_where)
        # print(con_limit)
        if len(table_name) == 1:  # 单表查询，嵌套查询
            if tag == 'return':  # 是否决定返回信息，为以后子查询做标记
                return select(using_dbname, columns, table_name, limit_where, con_limit, limit_group, limit_order,
                              tag=tag, having_limit=having_limit)
            else:
                print(select(using_dbname, columns, table_name, limit_where, con_limit, limit_group, limit_order,
                             tag=tag, having_limit=having_limit))
        else:
            # SELECT Student.Sno,Sname FROM Student,SC WHERE Student.Sno=SC.Sno AND SC.Cno='2' AND SC.Grade>90
            print('--连接查询----------------------')
            # print(limit_where)
            # print(con_limit)
            if using_dbname == '':  # 如果数据库名字为空，就报错
                print('[!]请选择一个数据库！')
                return
            else:
                using_db = pd.read_excel('data/' + using_dbname + '.xlsx', sheet_name=None)
                pass
            # 连接查询
            table_list = []
            for table_na in table_name:
                try:
                    table = using_db[table_na]  # 获取数据表
                    table_list.append(table)
                except:
                    print('[!]查无此表！', table_na, '表没有找到')
                    return
            connect_col = []
            for lim in con_limit:
                if len(lim) == 3:
                    if lim[1] == '=':
                        left_col = re.findall('\.(.*)', lim[0])[0]
                        right_col = re.findall('\.(.*)', lim[2])[0]
                        if left_col == right_col:
                            connect_col.append(left_col)
                            break
            # print(connect_col)
            indj = []
            for i in range(len(con_limit)):
                if len(con_limit[i]) == 3 and isinstance(con_limit[i], list):
                    lll = con_limit[i][0].split('.')[-1]
                    rrr = con_limit[i][2].split('.')[-1]
                    if con_limit[i][1] == '=' and lll == rrr:
                        indj.append(i)
                    con_limit[i][0] = lll
                    con_limit[i][2] = rrr
            for i in indj:
                con_limit.pop(i)
            # print(con_limit)
            for i in range(len(columns)):
                columns[i] = columns[i].split('.')[-1]
            if len(connect_col) == 0:
                print('[!]语法错误!：没有找到连接的条件')
                return
            # print(connect_col)
            connect_table = table_list[0]
            for i in range(1, len(table_name)):
                connect_table = pd.merge(connect_table, table_list[i], on=connect_col[i - 1])
            # print(connect_table)
            if tag == 'return':  # 是否决定返回信息，为以后子查询做标记
                # print(having_limit)
                return select(using_dbname, columns, connect_table, limit_where, con_limit, limit_group, limit_order,
                              tag=tag, having_limit=having_limit)
            else:
                print(select(using_dbname, columns, connect_table, limit_where, con_limit, limit_group, limit_order,
                             tag=tag, having_limit=having_limit))


if __name__ == '__main__':
    for i in range(10):
        using_dbname = 'S-T'
        using_db = pd.read_excel('data/' + using_dbname + '.xlsx', sheet_name=None)
        sql = input('[!][' + str(i) + ']>> ')
        xss = sql_Analysis(using_dbname, sql, tag='return')
        print('--main---------------------------------------------------------------')
        if isinstance(xss, dict):
            print_dict(xss)
        else:
            print(xss)
    # INSERT INTO Sheet1(Sno,Sname) SELECT Sno,Sname FROM Student WHERE Sage<20
