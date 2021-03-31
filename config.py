import os

# 指定数据集路径
dataset_path = './data'

# 结果保存路径
output_path = './output'

if not os.path.exists(output_path):
    os.mkdir(output_path)

# 公共列
common_cols = ['year', 'month', 'day', 'PM_US Post']

# 每个城市对应的文件名及所需分析的列名， 以字典的形式保存，如{城市：(文件名)}
data_config_dict = {'Beijing': ('BeijingPM20100101_20151231.csv', ['PM_Dongsi', 'PM_Dongsihuan', 'PM_Nongzhanguan']),
                    'Chengdu': ('ChengduPM20100101_20151231.csv', ['PM_Caotangsi', 'PM_Shahepu']),
                    'Guangzhou': ('GuangzhouPM20100101_20151231.csv', ['PM_City Station', 'PM_5th Middle School']),
                    'Shanghai': ('ShanghaiPM20100101_20151231.csv', ['PM_Jingan']),
                    'Shenyang': ('ShenyangPM20100101_20151231.csv', ['PM_Taiyuanjie'])}
