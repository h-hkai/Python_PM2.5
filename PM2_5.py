'''
    中国五大城市PM2.5数据分析
    任务：
        - 五城市污染状态
        - 五城市每个区空气质量的月度差
        - 统计每个城市的平均PM2.5的数值
        - 基于天数对比中国环保部和美国驻华大使馆统计的污染状态
    参考博客：
        https://blog.csdn.net/zbrj12345/article/details/81174653
        https://blog.csdn.net/zbrj12345/article/details/81183746
        https://blog.csdn.net/qq_42535601/article/details/86523689
        https://blog.csdn.net/weixin_38664232/article/details/97259159
        https://blog.csdn.net/suixuejie/article/details/82383192
        ...
'''

import os
import csv
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import config


def load_data(data_file, usecols):
    '''
        函数功能：
            读取数据文件，加在数据
        参数：
            ：data_file：文件路径
            ：useclos：所使用的列
            ：return：data_arr：    数据的多问数组表示
    '''
    data = []
    with open(data_file, 'r') as csvfile:
        data_reader = csv.DictReader(csvfile)
        # ===数据处理===
        for row in data_reader:
            # 取出每行数据，组合为一个列表放入数据列表中
            row_data = []
            # usecols = config.common_cols + [col for col in cols]
            # usecols中包含本次要用到的列('year', 'month', 'day', 'PM_US Post', '每个城市的各个区')
            # csv模块读入的数据全部为字符串类型
            for col in usecols:
                str_val = row[col]
                # 将数据转换为float，如果是'NA'，则返回nan
                if str_val == 'NA':
                    str_val = np.nan
                row_data.append(float(str_val))
            # 如果行数据中不包含nan才保存该行数据
            if not any(np.isnan(row_data)):
                data.append(row_data)
    # 将data转换成ndarray
    data_arr = np.array(data)
    return data_arr


def get_polluted_perc(data_arr):
    '''
        获取各个城市每个区污染占比的小时数
            规则：
                heavy:      PM2.5 > 150
                medium:     75 < PM2.5 <= 150
                light:      35 < PM2.5 <= 75
                good:       PM2.5 <= 35
        :param data_arr:    数据的多维数组表示
        :return:            polluted_perc_list: 污染小时数百分比列表
    '''
    # data_arr 是load_data中返回的数据其中包含的列有['year', 'month', 'day', 'PM_US Post'] + [每个城市的各个区]
    # 对各个区的污染指数求平均值
    # data_arr[:,4:]表示从第四列开始的所有列
    # axis = 1 表示对行进行操作
    hour_val = np.mean(data_arr[:, 4:], axis=1)
    # shape[0]代表统计行数
    n_hours = hour_val.shape[0]
    # 对数组运用条件表达式进行过滤
    n_heavy_hours = hour_val[hour_val > 150].shape[0]
    # 条件表达式中的与操作用&进行表示
    n_medium_hours = hour_val[(hour_val > 75) & (hour_val <= 150)].shape[0]
    n_light_hours = hour_val[(hour_val > 35) & (hour_val <= 75)].shape[0]
    n_good_hours = hour_val[hour_val <= 35].shape[0]
    polluted_perc_list = [n_heavy_hours / n_hours, n_medium_hours /
                          n_hours, n_light_hours / n_hours, n_good_hours / n_hours]
    # 返回不同污染状态所占的百分比
    return polluted_perc_list


def get_avg_pm_per_month(data_arr):
    '''
        获取每个区每月的平均PM值
        :data_arr: 需要处理的数据的数组表示
        :return:   results_arr：多维数组结果
    '''
    results = []
    # 对于一维数组或者列表，unique函数去除其中重复的元素，
    # 并按元素由大到小返回一个新的无元素重复的元组或者列表
    years = np.unique(data_arr[:, 0])
    for year in years:
        # 同一年中的数据
        year_data_arr = data_arr[data_arr[:, 0] == year]
        # 合并出月列表
        month_list = np.unique(year_data_arr[:, 1])

        for month in month_list:
            # 同一个月中的数据
            month_data_arr = year_data_arr[year_data_arr[:, 1] == month]
            # 计算当前月份的PM均值，先转换成列表方便之后的列表拼接
            mean_vals = np.mean(month_data_arr[:, 4:], axis=0).tolist()
            row_data = ['{:.0f}-{:02.0f}'.format(year, month)] + mean_vals
            results.append(row_data)
    # 将列表转换为数组
    results_arr = np.array(results)
    return results_arr


def save_states_to_csv(results_arr, save_file, headers):
    '''
        将处理后的数据进行保存
        :results_arr:   处理后的结果数组
        :save_file:     文件保存位置的路径
        :headers:       csv表头
    '''
    with open(save_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # 先写入columns_name
        writer.writerow(headers)
        # 然后再将每一个月的数据写入对应的columns
        for row in results_arr.tolist():
            writer.writerow(row)


def preprocess_data(data_df, city_name):
    '''
        预处理数据
        参数：
            - data_df:      数据DataFrame
            - city_name:    城市名
        返回：
            - cln_data_df:  预处理后的数据集
    '''
    # 数据清洗，去掉存在空值的行
    cln_data_df = data_df.dropna()
    # 件处理后的数据的索引进行重新编号
    cln_data_df = cln_data_df.reset_index(drop=True)
    # 将城市名作为新的列加入数组中
    cln_data_df['city'] = city_name

    print('{}共有{}行数据，其中有效数据为{}行'.format(
        city_name, data_df.shape[0], cln_data_df.shape[0]))
    print('{}的前10行有效数据： '.format(city_name))
    print(cln_data_df.head())

    return cln_data_df


def get_china_us_pm_df(data_df, suburb_cols):
    '''
        函数功能：
            分别获取中国和美国获取的PM2.5的数值
        参数：
            data_df:        预处理之后的数据
            suburb_cols:    城市中的各个区
        返回值：
            proc_data_df:   本次处理后的数据
    '''
    pm_suburb_cols = [col for col in suburb_cols]
    # 将本城市各个区的PM2.5的值取平均后的值作为中国测量的PM2.5的值
    data_df['PM_China'] = data_df[pm_suburb_cols].mean(axis=1)
    proc_data_df = data_df[config.common_cols + ['city', 'PM_China']]

    print('处理后的数据预览： ')
    print(proc_data_df.head())

    return proc_data_df


def add_date_col_to_df(data_df):
    '''
        将'year', 'month', 'day'合并成字符串列'data'
    '''
    # 对原文件进行拷贝
    proc_data_df = data_df.copy()
    # 将年，月，日的数据类型作为字符串进行处理
    proc_data_df[['year', 'month', 'day']] = proc_data_df[[
        'year', 'month', 'day']].astype('str')
    # 对字符串进行拼接
    proc_data_df['date'] = proc_data_df['year'].str.cat(
        [proc_data_df['month'], proc_data_df['day']], sep='-')
    # 对复制文件中的年，月，日三列进行删除
    proc_data_df = proc_data_df.drop(['year', 'month', 'day'], axis=1)
    # 调整列的顺序
    proc_data_df = proc_data_df[['date', 'city', 'PM_China', 'PM_US Post']]
    return proc_data_df


def add_polluted_state_col_to_df(day_stats):
    '''
        根据每天的PM值，添加相关的污染状态
        参数：
            - day_stats:        数据DataFrame
        返回：
            - proc_day_stats:   处理后的数据集
    '''
    proc_day_stats = day_stats.copy()
    bins = [-np.inf, 35, 75, 150, np.inf]
    state_lablels = ['good', 'light', 'medium', 'heavy']

    '''
        pd.cut(x,bins,right=True,labels=None,retbins=False,precision=3,include_lowest=False)
        将数据进行离散化、将连续变量进行分段汇总
        x：一维数组
        bins：整数--将x划分为多少个等距的区间，序列--将x划分在指定序列中，若不在该序列中，则是Nan
        right：是否包含右端点
        labels：是否用标记来代替返回的bins
        precision：精度
        include_lowest：是否包含左端点
    '''
    proc_day_stats['Polluted State CH'] = pd.cut(
        proc_day_stats['PM_China'], bins=bins, labels=state_lablels)
    proc_day_stats['Polluted State US'] = pd.cut(
        proc_day_stats['PM_US Post'], bins=bins, labels=state_lablels)

    return proc_day_stats


def compare_state_by_day(day_stats):
    '''
        基于天数对比中国环保部和美国驻华大使馆统计的污染状态
    '''
    city_names = config.data_config_dict.keys()
    city_comparison_list = []
    for city_name in city_names:
        # 筛选指定城市的污染状态
        city_df = day_stats[day_stats['city'] == city_name]
        # 将数组转化为DataFrame格式
        city_polluted_days_count_ch = pd.value_counts(
            city_df['Polluted State CH']).to_frame(name=city_name + 'CH')
        city_polluted_days_count_us = pd.value_counts(
            city_df['Polluted State US']).to_frame(name=city_name + 'US')
        city_comparison_list.append(city_polluted_days_count_ch)
        city_comparison_list.append(city_polluted_days_count_us)

    # 对DataFrame元素进行连接，axis = 1表示对列进行操作
    comparison_result = pd.concat(city_comparison_list, axis=1)
    return comparison_result


def show1():
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    plt.rcParams['axes.unicode_minus'] = False
    city_names = config.data_config_dict.keys()
    file_path = os.path.join(config.output_path, 'polluted_percentage.csv')
    citys_perc = pd.read_csv(file_path)
    citys_perc.rename(index=citys_perc.city, inplace=True)
    status = citys_perc.columns.drop('city')
    colors = ['red', 'yellow', 'lightskyblue', 'yellowgreen']  # 每块颜色定义
    index = 1
    for city_name in city_names:
        city_perc = list(citys_perc.loc[city_name].drop('city'))
        plt.subplot(2, 3, index).set_title(city_name)
        plt.pie(city_perc, labels=status, colors=colors)
        index += 1
    plt.suptitle("每个城市的污染状况")
    plt.show()


def show2():
    # 基于天数对中美两国的数据进行对比
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    plt.rcParams['axes.unicode_minus'] = False
    file_path = os.path.join(config.output_path, 'comparison_result.csv')
    comparison_result = pd.read_csv(file_path)
    city_names = config.data_config_dict.keys()
    comparison_result.rename(columns={'Unnamed: 0': 'status'}, inplace=True)
    status = comparison_result['status']
    index = 1
    fig = plt.figure(figsize=(20, 10))
    for city_name in city_names:
        city1 = city_name+'CH'
        city2 = city_name+'US'
        axi = 'ax{}'.format(index)
        CHData = comparison_result[city1]
        USData = comparison_result[city2]
        data_dict = {'status': status, city1: CHData, city2: USData}
        data_df = pd.DataFrame(data_dict).set_index('status')
        axi = fig.add_subplot(2, 3, index)
        plt.subplot(2, 3, index).set_title(city_name)
        data_df.plot(kind='bar', title=city_name, ax=axi)
        index += 1
    plt.suptitle("基于天数对中美两国的数据进行对比")
    plt.show()


def main():
    '''
        任务一：
            - 五城市污染状态
            - 五城市每个区空气质量的月度差
    '''

    # 存储每个城市不同污染状况的列表
    polluted_state_list = []
    # 对每个城市分别进行操作处理
    for city_name, (filename, cols) in config.data_config_dict.items():
        '''
            os.path.join()函数：连接两个或更多的路径名组件
                1.如果各组件名首字母不包含’/’，则函数会自动加上
                2.如果有一个组件是一个绝对路径，则在它之前的所有组件均会被舍弃
                3.如果最后一个组件为空，则生成的路径以一个’/’分隔符结尾
        '''
        data_file = os.path.join(config.dataset_path, filename)
        # cols代表的是每个城市的各个区
        usecols = config.common_cols + [col for col in cols]
        # 生成本次操作所需要的数据
        data_arr = load_data(data_file, usecols)

        print('{}共有{}行有效数据'.format(city_name, data_arr.shape[0]))
        print('{}的前10行数据：'.format(city_name))
        print(data_arr[:10])

        polluted_perc_list = get_polluted_perc(data_arr)
        polluted_state_list.append([city_name] + polluted_perc_list)
        print('{}的污染小时数百分比{}'.format(city_name, polluted_perc_list))

        results_arr = get_avg_pm_per_month(data_arr)
        print('{}的每月平均PM值预览：'.format(city_name))
        print(results_arr[:10])

        save_filename = city_name + '_month_stats.csv'
        save_file = os.path.join(config.output_path, save_filename)
        save_states_to_csv(results_arr, save_file, headers=['month'] + cols)
        print('月度统计结果以保存至{}'.format(save_file))

    # 保存城市污染百分比文件
    save_file = os.path.join(config.output_path, 'polluted_percentage.csv')
    with open(save_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # 先写入columns_name
        writer.writerow(['city', 'heavy', 'medium', 'light', 'good'])
        for row in polluted_state_list:
            writer.writerow(row)
    print('污染状态结果已保存{}'.format(save_file))

    '''
        任务二：
            - 统计每个城市的平均PM2.5的数值
            - 基于天数对比中国环保部和美国驻华大使馆统计的污染状态
    '''
    city_data_list = []

    for city_name, (filename, suburb_cols) in config.data_config_dict.items():
        # 1. 数据获取
        data_file = os.path.join(config.dataset_path, filename)
        usecols = config.common_cols + [col for col in suburb_cols]
        # reading data
        data_df = pd.read_csv(data_file, usecols=usecols)

        # 2. data processing
        # Pretreatment
        cln_data_df = preprocess_data(data_df, city_name)

        # processing the data of PM from CN and US
        proc_data_df = get_china_us_pm_df(cln_data_df, suburb_cols)
        city_data_list.append(proc_data_df)

        all_data_df = pd.concat(city_data_list)

        all_data_df = add_date_col_to_df(all_data_df)

        # analysising data
        day_stats = all_data_df.groupby(['city', 'date'])[
            ['PM_China', 'PM_US Post']].mean()

        day_stats.reset_index(inplace=True)

        day_stats = add_polluted_state_col_to_df(day_stats)

        comparison_result = compare_state_by_day(day_stats)
        print(comparison_result)

        # showing the result
        all_data_df.to_csv(os.path.join(config.output_path,
                                        'all_cities_pm.csv'), index=False)
        day_stats.to_csv(os.path.join(config.output_path, 'day_stats.csv'))
        comparison_result.to_csv(os.path.join(
            config.output_path, 'comparison_result.csv'))


if __name__ == "__main__":
    main()
    show1()
    show2()
