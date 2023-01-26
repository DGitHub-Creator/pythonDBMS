import os
import re
import warnings

import pandas as pd
from openpyxl import *

import delete as dl
import select as sl

warnings.filterwarnings("ignore")


def up_equal(operator, lim, table, data):
    '''
    更新：条件：等于的
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
        # test = table[~((table[limleft]).astype('str').isin([limright]))]
        test = table[(table[limleft] == limright)]
        test[data[0]] = data[1]
        table_copy = table[(table[limleft] != limright)]
        new_table = pd.concat([table_copy, test])
    except:
        print('[!]语法错误!：没有找到', limleft, '列，请检查输入是否正确！')
        return
    return new_table


def up_not_equal(operator, lim, table, data):
    '''
    更新：条件：不等于的
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
        # test = table[((table[limleft]).astype('str').isin([limright]))]
        test = table[(table[limleft] != limright)]
        test[data[0]] = data[1]
        table_copy = table[(table[limleft] == limright)]
        new_table = pd.concat([table_copy, test])
    except:
        print('[!]语法错误!：没有找到', limleft, '列，请检查输入是否正确！')
        return
    return new_table


def up_less(operator, lim, table, data):
    '''
    更新：条件：小于的
    :param operator: 操作符
    :param lim: 限制条件
    :param table: 现在要操作的数据表
    :return:
    '''
    limleft = lim[0]
    limright = lim[2]
    # limright = int(limright)
    try:
        limright = int(limright)
    except:
        try:
            limright = float(limright)
        except:
            limright = limright
    try:
        test = table[(table[limleft] < limright)]
        test[data[0]] = data[1]
        table_copy = table[~(table[limleft] < limright)]
        new_table = pd.concat([table_copy, test])
    except:
        print('[!]语法错误!：没有找到', limleft, '列，请检查输入是否正确！')
        return
    return new_table


def up_more(operator, lim, table, data):
    '''
    更新：条件：大于的
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
        test[data[0]] = data[1]
        table_copy = table[~(table[limleft] > limright)]
        new_table = pd.concat([table_copy, test])
    except:
        print('[!]语法错误!：没有找到', limleft, '列，请检查输入是否正确！')
        return
    return new_table


def up_less_equal(operator, lim, table, data):
    '''
    更新：条件：小于等于的
    :param operator: 操作符
    :param lim: 限制条件
    :param table: 现在要操作的数据表
    :return:
    '''

    limleft = lim[0]
    limright = lim[2]
    limright = int(limright)
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
        test[data[0]] = data[1]
        table_copy = table[~(table[limleft] <= limright)]
        new_table = pd.concat([table_copy, test])
    except:
        print('[!]语法错误!：没有找到', limleft, '列，请检查输入是否正确！')
        return
    return new_table


def up_more_equal(operator, lim, table, data):
    '''
    更新：条件：大于等于的
    :param operator: 操作符
    :param lim: 限制条件
    :param table: 现在要操作的数据表
    :return:
    '''
    limleft = lim[0]
    limright = lim[2]
    limright = int(limright)
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
        test[data[0]] = data[1]
        table_copy = table[~(table[limleft] >= limright)]
        new_table = pd.concat([table_copy, test])
    except:
        print('[!]语法错误!：没有找到', limleft, '列，请检查输入是否正确！')
        return
    return new_table


def update(using_dbname, table_name, updata, condition, fag):
    if using_dbname == '':  # 如果数据库名字为空，就报错
        print('[!]请选择一个数据库！')
        return
    else:
        using_db = pd.read_excel('data/' + using_dbname + '.xlsx', sheet_name=None)
        pass
    if table_name in using_db.keys():
        try:
            table = using_db[table_name]  # 获取数据表
        except:
            print('[!]查无此表！', table_name, '表没有找到')
            return
    elif os.path.exists('data/view/' + using_dbname + '/' + table_name + '.xlsx'):
        try:
            view_db = pd.read_excel('data/view/' + using_dbname + '/' + table_name + '.xlsx', sheet_name=None)  # 获取数据表
            table = view_db[table_name]
        except:
            print('[!]查无此表！', table_name, '表没有找到')
            return
    else:
        print('[!]查无此表！', table_name, '表没有找到')
        return
    old_table = table
    new_table = table
    if fag == 1:
        con_limit = re.split(r'(\+|\-|\*|\/)', updata[1])
        # print(con_limit)
        try:
            value = int(con_limit[2])
        except:
            try:
                if con_limit[1] == '+':
                    table[updata[0]] = table[con_limit[0]].astype(int) + table[con_limit[2]].astype(int)
                if con_limit[1] == '-':
                    table[updata[0]] = table[con_limit[0]].astype(int) - table[con_limit[2]].astype(int)
                if con_limit[1] == '*':
                    table[updata[0]] = table[con_limit[0]].astype(int) * table[con_limit[2]].astype(int)
                if con_limit[1] == '/':
                    table[updata[0]] = table[con_limit[0]].astype(int) / table[con_limit[2]].astype(int)
            except:
                print('[!]语法错误!：请检查输入的列名是否在表中！')
                return
        else:
            if con_limit[1] == '+':
                table[updata[0]] = table[con_limit[0]].astype(int) + value
            if con_limit[1] == '-':
                table[updata[0]] = table[con_limit[0]].astype(int) - value
            if con_limit[1] == '*':
                table[updata[0]] = table[con_limit[0]].astype(int) * value
            if con_limit[1] == '/':
                table[updata[0]] = table[con_limit[0]].astype(int) / value
        new_table = table
        # print(new_table)
    elif fag == 2:
        con_limit = condition
        predicate = con_limit[-1]
        # predicate = ' ',AND,OR,IN,NOTIN,BETWEENAND,NOTBETWEENAND.LIKE,NOTLIKE
        # print('predicate:', predicate)
        # new_table = ''
        # UPDATE Student SET Sage=22 WHERE Sno='201215121'
        if predicate == ' ':
            limit = con_limit[:-1]
            # print(limit)
            # 更新 =条件
            for lim in limit:
                operator = lim[1]
                # UPDATE Student SET Sage=22 WHERE Sage=18
                if operator == '=':
                    new_table = up_equal(operator, lim, table, updata)
                # UPDATE Student SET Sage=22 WHERE Sage<18
                if operator == '<':
                    new_table = up_less(operator, lim, table, updata)
                # UPDATE Student SET Sage=22 WHERE Sage>18
                if operator == '>':
                    new_table = up_more(operator, lim, table, updata)
                # UPDATE Student SET Sage=22 WHERE Sage<=18
                if operator == '<=':
                    new_table = up_less_equal(operator, lim, table, updata)
                # UPDATE Student SET Sage=22 WHERE Sage>=18
                if operator == '>=':
                    new_table = up_more_equal(operator, lim, table, updata)
                # UPDATE Student SET Sage=22 WHERE Sage<>18
                if operator == '!=' or operator == '<>':
                    new_table = up_not_equal(operator, lim, table, updata)
        # UPDATE Student SET Sage=22 WHERE Sage=20 OR Ssex='男'
        if predicate == 'OR':
            limit = con_limit[:-1]
            # print(limit)
            # 更新 =条件
            table_copy = table
            for lim in limit:
                operator = lim[1]
                if operator == '=':
                    table_copy = up_equal(operator, lim, table_copy, updata)
                if operator == '<':
                    table_copy = up_less(operator, lim, table_copy, updata)
                if operator == '>':
                    table_copy = up_more(operator, lim, table_copy, updata)
                if operator == '<=':
                    table_copy = up_less_equal(operator, lim, table_copy, updata)
                if operator == '>=':
                    table_copy = up_more_equal(operator, lim, table_copy, updata)
                if operator == '!=' or operator == '<>':
                    table_copy = up_not_equal(operator, lim, table_copy, updata)
            new_table = table_copy
        # UPDATE Student SET Sage=22 WHERE Sage=20 AND Ssex='男'
        # UPDATE Student SET Sage=22 Student WHERE Sage<20 AND Ssex='女'
        # UPDATE Student SET Sage=22 WHERE Sage=20 AND Sdept='IS'
        if predicate == 'AND':
            limit = con_limit[:-1]
            # print(limit)
            # 更新 =条件
            table_copy = table
            for lim in limit:
                operator = lim[1]
                if operator == '=':
                    table_copy = dl.dl_not_equal(operator, lim, table_copy)
                if operator == '<':
                    table_copy = dl.dl_more(operator, lim, table_copy)
                if operator == '>':
                    table_copy = dl.dl_less(operator, lim, table_copy)
                if operator == '<=':
                    table_copy = dl.dl_more_equal(operator, lim, table_copy)
                if operator == '>=':
                    table_copy = dl.dl_less_equal(operator, lim, table_copy)
                if operator == '!=' or operator == '<>':
                    table_copy = dl.dl_equal(operator, lim, table_copy)
            if table_copy is None:
                return
            # print(list(table_copy.index))
            test_table = table.drop(index=list(table_copy.index))
            table_copy[updata[0]] = updata[1]
            new_table = pd.concat([test_table, table_copy])
        # UPDATE Student SET Sage=22 Student WHERE Sdept in ('CS','MA')
        if predicate == 'IN':
            column = con_limit[0]
            # print(column, end=' ')
            limit = con_limit[1]
            # print(limit)
            try:
                test_table = table[~table[column].isin(limit)]
                table_copy = table[table[column].isin(limit)]
                table_copy[updata[0]] = updata[1]
                new_table = pd.concat([test_table, table_copy])
            except:
                print('[!]语法错误!：没有找到', column, '列，请检查输入是否正确！')
                return
            # print(new_table)
        # UPDATE Student SET Sage=22 Student WHERE Sdept not in ('CS','MA')
        if predicate == 'NOTIN':
            column = con_limit[0]
            # print(column, end=' ')
            limit = con_limit[1]
            # print(limit)
            try:
                test_table = table[table[column].isin(limit)]
                table_copy = table[~table[column].isin(limit)]
                table_copy[updata[0]] = updata[1]
                new_table = pd.concat([test_table, table_copy])
            except:
                print('[!]语法错误!：没有找到', column, '列，请检查输入是否正确！')
                return
            # print(new_table)
        # UPDATE Student SET Sage=22 Student WHERE Sage between 18 and 19
        if predicate == 'BETWEENAND':
            column = con_limit[0]
            minn = int(con_limit[1][0])
            maxx = int(con_limit[1][1])
            limit = list(range(minn, maxx + 1))
            # print(limit)
            try:
                test_table = table[~table[column].isin(limit)]
                table_copy = table[table[column].isin(limit)]
                table_copy[updata[0]] = updata[1]
                new_table = pd.concat([test_table, table_copy])
            except:
                print('[!]语法错误!：没有找到', column, '列，请检查输入是否正确！')
                return
            # print(new_table)
        # UPDATE Student SET Sage=22 Student WHERE Sage not between 18 and 19
        if predicate == 'NOTBETWEENAND':
            column = con_limit[0]
            minn = int(con_limit[1][0])
            maxx = int(con_limit[1][1])
            limit = list(range(minn, maxx + 1))
            # print(limit)
            try:
                test_table = table[table[column].isin(limit)]
                table_copy = table[~table[column].isin(limit)]
                table_copy[updata[0]] = updata[1]
                new_table = pd.concat([test_table, table_copy])
            except:
                print('[!]语法错误!：没有找到', column, '列，请检查输入是否正确！')
                return
        # UPDATE Student SET Sage=22 Student WHERE Sname LIKE '刘%'
        if predicate == 'LIKE':  # 如果谓词是LIKE
            column = con_limit[0]
            limit = con_limit[1]
            if con_limit[2] != 'LIKE':  # 不是LIKE就是通配符
                escape = con_limit[2][-2]
                wc_str = limit[0].replace('%', '(.*)').replace('_', '(.)').replace(escape + '(.*)', '%').replace(
                    escape + '(.)', '_')
            else:
                wc_str = limit[0].replace('%', '(.*)').replace('_', '(.)')  # print(wc_str)
            try:
                col_list = table[column].tolist()
            except:
                print('[!]语法错误!：没有找到', column, '列')
                return
            name_list = []
            for i in col_list:
                s = re.search(wc_str, i)
                try:
                    name_list.append(s[0])
                except:
                    ''
            # new_table = table[table[column].isin(name_list)]
            try:
                test_table = table[~table[column].isin(name_list)]  # 不like的
                table_copy = table[table[column].isin(name_list)]  # like的
                table_copy[updata[0]] = updata[1]  # 修改like的
                new_table = pd.concat([test_table, table_copy])  # 拼起来
            except:
                print('[!]语法错误!：没有找到', column, '列，请检查输入是否正确！')
                return
            # pint(new_table)
        # print(new_table)
    elif fag == 3:
        # 子查询
        sql_select = ' '.join(condition[1])
        # print(sql_select)
        print('select start----------------------------------------------------------------')
        sss = sl.sql_Analysis(using_dbname, sql_select, 'return')
        print('select end------------------------------------------------------------------')
        # print(sss)
        lim_con = sss[condition[0]].tolist()
        # print(lim_con)
        new_condition = [condition[0], lim_con, 'IN']
        # print(table_name)
        # print(updata)
        # print(new_condition)
        update(using_dbname, table_name, updata, new_condition, fag=2)
        return
    else:
        print('[!]语法错误!：fag超限！')
        return
    # print(old_table)
    # print(new_table)
    test_table = new_table.append(old_table).append(old_table).drop_duplicates(keep=False)
    # print(test_table)
    print("[*]更新成功！更新了", test_table.shape[0], "个元组")
    # 保存
    book = load_workbook('data/' + using_dbname + '.xlsx')
    writer = pd.ExcelWriter('data/' + using_dbname + '.xlsx')
    writer.book = book
    # 保存操作 保存修改后的表
    new_table.to_excel(writer, sheet_name=table_name, index=False)
    writer.save()
    # 因为pandas没有办法覆盖数据表，它会新建一个数据表，并在你所设置的名字后面加一个1，
    # 这样此数据表的名称变为:table_name1,所以要重新读入，删除旧的表并且把新的表改名
    wb = load_workbook('data/' + using_dbname + '.xlsx')  # 读入数据库
    del wb[table_name]  # 删除掉旧的表
    for sheet in wb:  # 循环查找table_name1，改成table_name
        if sheet.title == table_name + '1':
            sheet.title = table_name
            break
    wb.save('data/' + using_dbname + '.xlsx')  # 把修改后的数据表保存
    print(table_name, '表更新操作完成！')
    pass


def sql_Analysis(using_dbname, sql, tag=''):
    sql = sql.strip()
    sql_word = sql.split(' ')  # 分割sql语句
    if len(sql_word) < 2:
        print('[!]语法错误')
        return
    operate = sql_word[0].lower()  # 操作名
    # UPDATE Student SET Sbron=Syear-Sage
    # UPDATE Student SET Sage=22 WHERE Sno='201215121'
    # UPDATE Student SET Sage=99 WHERE Ssex='男'
    # UPDATE Student SET Sage=Sage+1
    # UPDATE SC SET Grade=0 WHERE Sno IN (SELECT Sno FROM Student WHERE Sdept='CS')
    if operate == 'update':  # 如果是更新
        # print(sql_word)
        uptable = sql_word[1]
        pos_select = -1  # 标记select位置 -1 就是无
        # print(operate.upper(), end=' ')  # 显示 打印操作符大写
        # print(uptable)  # 显示 打印要更新的表名
        upset = sql_word[2]  # SET
        # print(upset)  # 显示 待处理的信息
        date = sql_word[3].split('=')
        # print(date)
        Asql_word = [x.upper() for x in sql_word]  # 新建大写列表，方便后面定位index
        try:
            pos_where = Asql_word.index('WHERE')  # 定位SELECT的位置
        except:
            pos_where = -1
        try:
            pos_select = Asql_word.index('(SELECT')  # 定位SELECT的位置
        except:
            pos_select = -1
        fag = 1  # 什么也没有
        condition = []  # where条件
        if pos_where != -1 and pos_select == -1:  # 如果只有where
            fag = 2  # 只有where
            limit_where = sql_word[pos_where + 1:]
            con_limit = []  # 分割限制条件
            # AND
            # UPDATE Student SET Sage=22 WHERE Sdept='CS' AND Sage<=20
            if 'BETWEEN' not in Asql_word and 'AND' in Asql_word:
                subqueries = 'AND'
                for i in range(0, len(limit_where), 2):
                    con_limit.append(re.split(r'(>=|<=|!=|<>|!>|!<|=|<|>)', limit_where[i]))
                con_limit.append('AND')
            # OR
            # UPDATE Student SET Sage=22 WHERE Sdept='CS' or Sage<=20
            if 'OR' in Asql_word:
                subqueries = 'OR'
                for i in range(0, len(limit_where), 2):
                    con_limit.append(re.split(r'(>=|<=|!=|<>|!>|!<|=|<|>)', limit_where[i]))
                con_limit.append('OR')
            # IN
            # UPDATE Student SET Sage=22 WHERE Sdept in ('CS','MA','IS')
            if 'NOT' not in Asql_word and 'IN' in Asql_word:
                subqueries = 'IN'
                con_1 = limit_where[0]
                con_2 = re.split(r'[(|)|\'|,]', limit_where[2])
                con_2 = [item for item in filter(lambda x: x != '', con_2)]
                con_limit.append(con_1)
                con_limit.append(con_2)
                con_limit.append('IN')
            # NOT IN
            # UPDATE Student SET Sage=22 WHERE Sdept not in ('CS','MA','IS')
            if 'NOT' in Asql_word and 'IN' in Asql_word:
                subqueries = 'NOTIN'
                con_1 = limit_where[0]
                con_2 = re.split(r'[(|)|\'|,]', limit_where[3])
                con_2 = [item for item in filter(lambda x: x != '', con_2)]
                con_limit.append(con_1)
                con_limit.append(con_2)
                con_limit.append('NOTIN')
            # BETWEEN AND
            # UPDATE Student SET Sage=22 WHERE Sage between 20 and 23
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
            # NOT BETWEEN AND
            # UPDATE Student SET Sage=22 WHERE Sage not between 20 and 23
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
            # LIKE
            # UPDATE Student SET Sage=22 WHERE Sname LIKE '刘%'
            if 'NOT' not in Asql_word and 'LIKE' in Asql_word:
                subqueries = 'LIKE'
                con_1 = limit_where[0]
                con_2 = re.split(r'[(|)|\'|,]', limit_where[2])
                con_2 = [item for item in filter(lambda x: x != '', con_2)]
                con_limit.append(con_1)
                con_limit.append(con_2)
                con_limit.append('LIKE')
            # NOT LIKE
            # UPDATE Student SET Sage=22 WHERE Sname NOT LIKE '刘%'
            if 'NOT' in Asql_word and 'LIKE' in Asql_word:
                subqueries = 'NOTLIKE'
                con_1 = limit_where[0]
                con_2 = re.split(r'[(|)|\'|,]', limit_where[3])
                con_2 = [item for item in filter(lambda x: x != '', con_2)]
                con_limit.append(con_1)
                con_limit.append(con_2)
                con_limit.append('NOTLIKE')
            # IS NULL
            # UPDATE Student SET Sage=22 WHERE Sname IS NULL
            if 'IS' in Asql_word and 'NOT' not in Asql_word and 'NULL' in Asql_word:
                subqueries = 'ISNULL'
                con_1 = limit_where[0]
                con_limit.append(con_1)
                con_limit.append('ISNULL')
            # IS NOT NULL
            # UPDATE Student SET Sage=22 WHERE Sname IS NOT NULL
            if 'IS' in Asql_word and 'NOT' in Asql_word and 'NULL' in Asql_word:
                subqueries = 'ISNOTNULL'
                con_1 = limit_where[0]
                con_limit.append(con_1)
                con_limit.append('ISNOTNULL')
            if len(con_limit) == 0:
                for i in range(0, len(limit_where), 2):
                    con_limit.append(re.split(r'(>=|<=|!=|<>|!>|!<|=|<|>)', limit_where[i]))
                con_limit.append(' ')
            condition = con_limit
            # print(condition)
        elif pos_where != -1 and pos_select != -1:  # 如果有where和select
            column = sql_word[5]
            condition.append(column)
            subselect = re.findall('\((.*)\)', sql)[0].split(' ')
            condition.append(subselect)
            fag = 3  # 有where和select
            # print(condition)
        # print(date)
        # print(condition)
        update(using_dbname, uptable, date, condition, fag)


if __name__ == '__main__':
    for i in range(10):
        using_dbname = 'S-T'
        # using_db = pd.read_excel('data/' + using_dbname + '.xlsx', sheet_name=None)
        sql = input('[!][' + str(i) + ']>> ')
        sql_Analysis(using_dbname, sql)
