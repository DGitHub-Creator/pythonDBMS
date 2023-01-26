# # import pandas as pd
# #
# # using_dbname = 'S-T'
# # table_name = 'Sheet1'
# #
# # from openpyxl import *
# #
# # using_db = pd.read_excel('S-T.xlsx', sheet_name=None)
# #
# # book = load_workbook('S-T.xlsx')
# # writer = pd.ExcelWriter('S-T.xlsx')
# # writer.book = book
# #
# # table = using_db[table_name]
# # table.to_excel(writer, sheet_name=table_name, index=False)
# #
# # writer.save()
# #
# # wb = load_workbook('S-T.xlsx')
# # del wb[table_name]
# # for sheet in wb:
# #     if sheet.title == table_name + '1':
# #         sheet.title = table_name
# #         break
# # wb.save('S-T.xlsx')
# # import hashlib
# #
# # print(hashlib.md5('root'.encode('utf-8')).hexdigest())
# # import os
# #
# # import pandas as pd
# #
# # using_dbname = 'S-T'
# # table_name = 'IS_Student'
# # using_db = pd.read_excel('data/' + using_dbname + '.xlsx', sheet_name=None)
# # if table_name in using_db.keys():
# #     print('1-------------------')
# # elif os.path.exists('data/view/' + using_dbname + '/' + table_name + '.xlsx'):
# #     print('2-------------------')
# #     view_db = pd.read_excel('data/view/' + using_dbname + '/' + table_name + '.xlsx', sheet_name=None)  # 获取数据表
# #     table = view_db[table_name]
# # else:
# #     print('[!]查无此表！', table_name, '表没有找到')
# # # print(view_db)
# # print(table)
# '''
#
# '''
# # import pandas as pd
# #
# #
# # def check_Constraint(using_dbname, dic_type, table_name):
# #     """
# #     插入时检查实体完整性约束，包括主码不为空，主码唯一，各数据对应的类型一致
# #     :param using_dbname: 数据库名称
# #     :param dic_type: 字典类型，{列名：数据类型}
# #     :param table_name:数据表的名称
# #     :return:
# #     """
# #     db_info = pd.read_excel('data/table_information.xlsx', sheet_name=None)  # 读入数据表的信息
# #     table_info = db_info[using_dbname]  # 查找到对应的数据库的信息表
# #     tablene = table_info[table_info['table'] == table_name]  # 查找到对应的数据表的信息
# #     # tablepk = tablene[(tablene['primary_key']) == '1']  # 查找主码，主码为primary_key标记为1，这个1可能是字符类型也可能是数字类型
# #     # if tablepk.empty:  # 如果没有查找到字符类型的标记，就查找数字类型的标记
# #     #     tablepk = tablene[(tablene['primary_key']) == 1]
# #     # print(tablepk)  # 显示 主码，可能为空
# #     # try:
# #     #     pkname = tablepk['column_name'].tolist()  # 获取主码
# #     #     print(pkname)  # 显示主码
# #     # except:
# #     #     print(table_name, '表中没有查询到主码，请检查主码设置')  # 报错 没有主码
# #     #     return False
# #     # print(table_name, '表的主码(pk)为：', pkname)
# #     # try:
# #     #     for pk in pkname:
# #     #         if dic_type[pk] is None:  # 要插入的值中主码为空
# #     #             print('[!]语法错误!：主码为空！')
# #     #             return False
# #     # except:
# #     #     print('[!]语法错误!：缺失主码！')  # 要插入的值中缺失主码
# #     #     return False
# #     print('-----------------------------------------')  # 显示 分隔符
# #     # print(tablene)
# #     # 将信息表里面的列名和类型打包成字典
# #     ne_name = tablene['column_name'].values.tolist()  # 列名转化为列表
# #     # print(ne_name)
# #     ne_type = tablene['type'].values.tolist()  # 类型转化为列表
# #     # print(ne_type)
# #     ne_dic = dict(map(lambda x, y: [x, y], ne_name, ne_type))  # 按对应关系打包
# #     # print(ne_dic)
# #     column_dic = dic_type.keys()  # 获取要插入数据的列名
# #     print(column_dic)
# #     for key in column_dic:
# #         # print(dic_type[key],'==',ne_dic[key])
# #         if dic_type[key] != ne_dic[key]:  # 检查要插入的类型与信息表里面的类型是够对称
# #             print('[!]数据类型错误!：', key, '的数据类型是', ne_dic[key], '而不是', dic_type[key])
# #             return False
# #     print('实体完整性检查约束成功！')  # 显示 检查完成
# #     return True
# #
# #
# # using_dbname = 'S-T'
# # table_name = 'Student'
# # date = ['Sage', '22']
# # # print(date)
# # if date[1][0] == '\'' and date[1][-1] == '\'':  # 前后都有单引号就是string
# #     value_type = 'string'
# #     date[1] = date[1][1:-1]
# # else:
# #     value_type = 'int'  # 其他的是int
# # dic_type = {date[0]: value_type}
# # # print(dic_type)
# # if check_Constraint(using_dbname, dic_type, table_name) is False:
# #     print('ERROR----------------------------')
# # else:
# #     print('SUCCESS----------------------------')
# ''''''
#
# # import re
# #
# # info = ['刘去', '出纳', '终端', '董.志121新', 'DB_Design']
# #
# # col = 'DB\_Design'
# # # wc_str = col.replace('%', '(.*)').replace('_', '(.)').replace('\(.*)', '%').replace('\(.)', '_')
# # wc_str = '董.(.*)'
# # # print(wc_str)
# # for i in info:
# #     s = re.search(wc_str, i)
# #     try:
# #         print(s[0])
# #     except:
# #         ''
#
# # df = pd.read_excel('data/S-T.xlsx', sheet_name=None)
# # table = df['Student']
# # print(table)
# # name_list = ['刘晨', '王敏', '张立', '马中']
# # new_table = table[table['Sname'].isin(name_list)]
# # print(new_table)
# # i = 0
# # while True:
# #     if input() == '0':
# #         break
# #     i = i + 1
# # print(i)
# # import pandas as pd
# # df = pd.read_excel('data/S-T.xlsx', sheet_name=None)
# # df1 = df['Student']
# # df2 = df['Sheet1']
# # df3 = pd.concat([df1,df2],axis=1)
# # print(df3)
# # print(df3.info())
# # print(df3['Sno'])
#
# # limright = '99.9'
# # try:
# #     limright = int(limright)
# # except:
# #     try:
# #         limright = float(limright)
# #     except:
# #         limright = limright
# #
# # print(limright)
# # print(type(limright))
# # import sys
# # print(sys.version)
# import pip  # needed to use the pip functions
#
# # for i in pip.get_installed_distributions(local_only=True):
# #     print(i)
#
# import hashlib
# import os
# import re
# import numpy
#
# print(os.__version__)
# print(re.__version__)
# print(hashlib.__version__)
# print(numpy.__version__)

Asql_word= ['UNION','A','UNION','V','V','A']
try:  # 获取UNIOM位置
    pos_union = Asql_word.index('UNION')
except:
    pos_union = -4
print(pos_union)