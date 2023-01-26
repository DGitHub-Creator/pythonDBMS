import hashlib
import os
import re

import pandas as pd


def md5_pwd(pwd):
    """
    为了防止解密，hashlib.md5时加入了自己的字段
    将密码转为md5形式
    :param pwd: 密码铭文
    :return: 加密的结果
    """
    for i in range(pwd.shape[0]):
        values = pwd.iloc[i, 0]
        hash = hashlib.md5(bytes('dzx', encoding='utf8'))
        hash.update(bytes(values, encoding='utf8'))
        res = hash.hexdigest()
        pwd.iloc[i, 0] = res
    return pwd


def sql_Analysis(using_dbname, sql, tag=''):
    sql = sql.strip()
    sql_word = sql.split(' ')  # 分割sql语句
    print(sql_word)
    if len(sql_word) < 2:
        print('[!]语法错误')
        return
    operate = sql_word[0].lower()  # 操作名
    if operate == 'create':
        if sql_word[1].lower() == 'index' or sql_word[2].lower() == 'index':
            Asql_word = [x.upper() for x in sql_word]  # 全变大写，方便查找
            try:  # 获取WHERE位置
                pos_index = Asql_word.index('INDEX')
            except:
                pos_index = -1
                print('[!]语法错误!：没有INDEX')
                return
            index_name = sql_word[pos_index + 1]
            table_name = re.findall('(.*)\(', sql_word[pos_index + 3])[0]
            columns = re.findall('\((.*)\)', sql)[0].split(',')
            columns = [x.split(' ') for x in columns]
            # print(index_name)
            # print(table_name)
            # print(columns)
            ind_df = pd.read_excel('data/' + using_dbname + '.xlsx', sheet_name=None)
            ind_tb = ind_df[table_name]

            reality_col = [x[0] for x in columns]
            # print(reality_col)

            asc_list = []  # 保存是升序还是降序的列表
            for lim in columns:  # 循环判断是否是升序降序
                if len(lim) == 1 or lim[1].upper() == 'ASC':  # 如果只有一个元素就是默认是升序，或者如果是ASC就是升序
                    asc_list.append(1)  # 升序排序存入1
                    continue
                if lim[1].upper() == 'DESC':  # 如果是DESC就是降序
                    asc_list.append(0)  # 降序排序存入0
                    continue
            # print(asc_list)

            sorted_ind_table = ind_tb.sort_values(by=reality_col,
                                                  ascending=asc_list)  # 按照by_list(根据排序的列)和asc_list(排序顺序)排序
            # print(sorted_ind_table)

            ind_table = sorted_ind_table[[reality_col[0]]]
            for i in range(1, len(columns)):
                ind_test = sorted_ind_table[[reality_col[i]]]
                ind_table = pd.concat([ind_table, ind_test], axis=1)
            ind_table['ind_sum'] = ind_table[reality_col[0]]
            for i in range(1, len(reality_col)):
                ind_table['ind_sum'] = ind_table['ind_sum'].astype(str) + ind_table[reality_col[i]].astype(str)
            ind_table['hash_value'] = md5_pwd(ind_table[['ind_sum']])
            ind_table['pos_value'] = ind_table.index

            # print(ind_table)
            new_table = pd.DataFrame(ind_table['hash_value'])
            new_table = pd.concat([new_table, ind_table['pos_value']], axis=1)
            for col in reality_col:
                new_table = pd.concat([new_table, ind_table[col]], axis=1)
            # print(new_table)
            if not os.path.exists('data/view'):
                os.mkdir('data/view')
            if not os.path.exists('data/view/' + using_dbname):
                os.mkdir('data/view/' + using_dbname)
            new_table.to_excel('data/view/' + using_dbname + '/' + index_name + '.xlsx',index=False)
            pass


# CREATE UNQUE INDEX Stusno ON Student(Sno,Cno)
# CREATE UNQUE INDEX SCno ON SC(Sno ASC,Cno DESC)
if __name__ == '__main__':
    for i in range(10):
        using_dbname = 'S-T'
        # using_db = pd.read_excel('data/' + using_dbname + '.xlsx', sheet_name=None)
        sql = input('[!][' + str(i) + ']>> ')
        sql_Analysis(using_dbname, sql)
