import os
import re

import pandas as pd
from openpyxl import *

import check as ch
import select as sl


def insert(using_dbname, table_name, columns=None, columns_value=None, sltag=False, sltable=None):
    """
    数据表的插入操作
    :param using_dbname: 数据库的名称
    :param table_name: 数据表的名称
    :param columns: 列名
    :param columns_value:对应列的值
    :param sltag:是否子查询的标记
    :param sltable:子查询得到的表
    :return:
    """
    if using_dbname == '':  # 如果数据库名字为空，就报错
        print('[!]请选择一个数据库！')
        return
    else:
        using_db = pd.read_excel('data/' + using_dbname + '.xlsx', sheet_name=None)
    if sltable is None:
        sltable = []
    if columns_value is None:
        columns_value = []
    if columns is None:
        columns = []
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
    if sltag is False:
        len_columns = len(table.columns)  # 读取列数
        if len(columns) == 0:  # 如果没有指定列名，默认添加全部列数据
            columns = table.columns
        value_type = columns_value[0:]  # 创建数据类型列表
        for i in range(len(columns_value)):  # 对数据类型列表进行赋值：有双引号的为string,没有双引号的为int
            if columns_value[i][0] == '\'' and columns_value[i][-1] == '\'':  # 前后都有单引号就是string
                value_type[i] = 'string'
                columns_value[i] = columns_value[i][1:-1]
            else:
                value_type[i] = 'int'  # 其他的是int
        # 记得检查约束
        dic_type = dict(map(lambda x, y: [x, y], columns, value_type))  # 创建列名与数据类型对应的字典
        if ch.check_Constraint(using_dbname, dic_type, table_name) is False:  # 检查约束
            return
        if len(columns_value) < len_columns:  # 不够列数的补全空值
            for i in range(len(columns_value), len_columns):
                columns_value.append('NULL')
        dic = dict(map(lambda x, y: [x, y], columns, columns_value))  # 创建列名与数据对应的字典
        print(dic)
        new_table = table.append(dic, ignore_index=True)  # 按照列名添加到数据表中
    else:
        new_table = pd.concat([table, sltable])
    # print(test)
    print("[*]插入成功！插入了", new_table.shape[0] - old_table.shape[0], "个元组")
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
    print(table_name, '表插入操作完成！')  # 显示 提示信息
    pass


def sql_Analysis(using_dbname, sql, tag=''):
    sql = sql.strip()
    sql_word = sql.split(' ')  # 分割sql语句
    if len(sql_word) < 2:
        print('[!]语法错误')
        return
    operate = sql_word[0].lower()  # 操作名
    # INSERT INTO Student(Sno,Sname,Ssex,Sdept,Sage) VALUES('201215128','张成民','男','IS',18)
    if operate == 'insert':  # 如果是插入
        if sql_word[1].lower() == 'into':  # 后面要跟INTO
            pos_select = -1  # 标记select位置 -1 就是无
            # print(operate.upper())  # 显示 打印操作符大写
            # print(sql_word[1], end=' ')  # 显示 打印INTO
            table_name_info = sql_word[2]  # 处理数据表的名称与要插入的列的名称
            # print(table_name_info)  # 显示 待处理的信息
            # 处理INTO数据
            columns = []  # 用于存放列名称
            if '(' in table_name_info:  # 如果表名称后面有括号，就用正则表达式提取出数据表的名称和要插入列的名称
                table_name = re.findall('(.*)\(', table_name_info)[0]  # 提取表名
                columns = re.findall('\((.*)\)', table_name_info)[0].split(',')  # 提取列名称
            else:
                table_name = table_name_info  # 如果没有括号，INTO数据就是表名
            # print(table_name, end=' ')  # 显示 数据表名
            # print(columns)  # 显示 列名
            Asql_word = [x.upper() for x in sql_word]  # 新建大写列表，方便后面定位index
            try:
                pos_select = Asql_word.index('SELECT')  # 定位SELECT的位置
            except:
                pos_select = -1
            # print(pos_select)  # 显示 SELECT的位置
            # 处理VALUES 和 子查询
            if pos_select == -1:  # 如果没有SELECT，没有子查询
                try:
                    value_info = sql_word[3]  # 获取需要插入的值的信息
                    # print(value_info)  # 显示 值的信息
                except:
                    print('[!]语法错误!：VALUES错误！没有输入VALUES值！')  # 显示 报错信息
                    return
                if '(' in value_info:  # 获取VALUES()括号包裹的需要插入的值
                    value_op = re.findall('(.*)\(', value_info)[0]  # 获取VALUES这个标记
                    if value_op.lower() != 'values':  # 检查VALUES这个标记
                        print('[!]语法错误!：VALUES错误！缺失VALUES标记！')  # 如果没有就是语法错误
                        return
                    columns_value = re.findall('\((.*)\)', value_info)[0].split(',')  # 通过正则表达式获取()括号中包裹着的需要插入的值
                    # print(columns_value)  # 显示 需要插入的值
                else:
                    print('[!]语法错误!：VALUES错误！没有输入需要插入的值！')  # 显示 报错信息
                    return
                if len(columns) > 0:  # 判断列名与值是否对称，是否多输入了列或者是多输入了值
                    if len(columns) != len(columns_value):  # 如果列名的数量与值的数量不一样
                        print('[!]语法错误!：VALUES错误！列与值不对称！')  # 显示 报错信息
                        return
                insert(using_dbname, table_name, columns=columns, columns_value=columns_value)  # 插入
            else:
                # INSERT INTO Dept_age(Sdept,Avg_age) SELECT Sdept,AVG(Sage) FROM Student GROUP BY Sdept
                select_sql_list = sql_word[pos_select:]
                # print(select_sql_list)
                sql_select = ' '.join(select_sql_list)
                # print(sql_select)
                print('select start----------------------------------------------------------------')
                sss = sl.sql_Analysis(using_dbname, sql_select, 'return')
                print('select end------------------------------------------------------------------')
                # print(sss)
                # print(columns)
                insert(using_dbname, table_name, sltag=True, sltable=sss)  # 插入


# INSERT INTO Sheet1(Sno,Sname) SELECT Sno,Sname FROM Student WHERE Sage<20
if __name__ == '__main__':
    for i in range(10):
        # using_db = pd.read_excel('data/' + using_dbname + '.xlsx', sheet_name=None)
        using_dbname = 'S-T'
        sql = input('[!][' + str(i) + ']>> ')
        sql_Analysis(using_dbname, sql)
