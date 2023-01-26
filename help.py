import os

import pandas as pd


def sql_Analysis(using_dbname, sql, tag=''):
    sql = sql.strip()
    sql_word = sql.split(' ')  # 分割sql语句
    # print(sql_word)
    if len(sql_word) < 2:
        print('[!]语法错误')
        return
    operate = sql_word[0].lower()  # 操作名
    # print(operate)
    if operate == 'help':
        type_name = sql_word[1].lower()
        # print(type_name)
        if type_name.lower() == 'database':
            # 输出数据表信息
            print('table information:')
            u1_db = pd.read_excel('data/table_information.xlsx', sheet_name=None)
            try:
                u1_table = u1_db[using_dbname]
            except:
                print('[!]没有正在使用数据库！请选择一个数据库使用后再次尝试。')
                return
            list_1 = ['table', 'column_name']
            u1_table.drop_duplicates(subset=list_1, inplace=True, keep="first")
            print(u1_table)
            # 输出视图信息
            print('view information:')
            u2_db = pd.read_excel('data/view/view_sql_information.xlsx', sheet_name=None)
            u2_table = u2_db[using_dbname]
            list_2 = ['viewname', 'sql_view']
            pd.set_option('display.max_rows', None)
            pd.set_option('max_colwidth', 200)
            u2_table.drop_duplicates(subset=list_2, inplace=True, keep="first")
            print(u2_table)
            # 输出索引信息（待完善）
            print('index information:')
            index_names = os.listdir('data/index/' + using_dbname)
            # print(index_names)
            for index_name in index_names:
                print(index_name[:-5] + ':')
                u3_db = pd.read_excel('data/index/' + using_dbname + '/' + index_name)
                print(u3_db)
            pass
        elif type_name.lower() == 'table':
            # 输出数据表信息
            use_db = pd.read_excel('data/table_information.xlsx', sheet_name=None)
            use_table = use_db[using_dbname]
            u2_table = use_table[use_table['table'] == sql_word[2]]
            u2_table.drop_duplicates(subset="column_name", inplace=True, keep="first")
            print(u2_table)
            pass
        elif type_name.lower() == 'view':
            # 输出视图信息
            use_db = pd.read_excel('data/view/view_sql_information.xlsx', sheet_name=None)
            use_table = use_db[using_dbname]
            u2_table = use_table[use_table['viewname'] == sql_word[2]]
            print(u2_table.iloc[0, 0], end=' : ')
            print(u2_table.iloc[0, 1])
            pass
        elif type_name.lower() == 'index':
            use_db = pd.read_excel('data/index/' + using_dbname + '/' + sql_word[2] + '.xlsx')
            print(use_db)
            pass


# help database
# help table 表名
# help table Student
# help view 视图名
# help view IS_Student
# help index 索引名
# help index SCno
if __name__ == '__main__':
    for i in range(10):
        using_dbname = 'S-T'
        # using_db = pd.read_excel('data/' + using_dbname + '.xlsx', sheet_name=None)
        sql = input('[!][' + str(i) + ']>> ')
        sql_Analysis(using_dbname, sql)
