# 数据可视化——中国五大城市PM2.5数据分析
## 数据字典
No：记录编号，整型
year：年份，整型
month：月份，整型
day：日期，整型
hour：小时，整型
season：季度，整型
PM2.5：中国环保部发布的PM2.5指数（ug/m3），浮点型
PM_US：美国驻华大使馆发布的PM2.5指数（ug/m3），浮点型
DEWP：露点温度（摄氏度）
TEMP：温度（摄氏度）
HUMI：湿度（%）
PRES：气压（hpa）
cbwd：合成风向
Iws：合成风速（m/s）
Precipitation：每小时降水量（mm）
Iprec：累积降水量（mm）

## 任务
- 分析五城市污染状态
- 五城市每个区空气质量的月度差异
- 统计每个城市每天的平均PM2.5的数值
- 基于天数对比中国环保部和美国驻华大使馆统计的污染状态

## 该项目通过分析中国五大城市PM2.5的数据实例，巩固了python的进阶技巧及NumPy、pandas 库的使用：
- 字典遍历
- CSV数据读写操作
- numpy的使用
- 列表推导式的使用
- 条件表达式的使用
- 数据清洗
- 向量化字符串操作
- 分组与聚合操作

## 分析结果
<div style="align: center">
<img src="https://github.com/h-hkai/Python_PM2.5/blob/master/%E5%9F%BA%E4%BA%8E%E5%A4%A9%E6%95%B0%E5%AF%B9%E4%B8%AD%E7%BE%8E%E4%B8%A4%E5%9B%BD%E7%9A%84%E6%95%B0%E6%8D%AE%E8%BF%9B%E8%A1%8C%E5%AF%B9%E6%AF%94.png"/>
</div>
<div style="align: center">
<img src="https://github.com/h-hkai/Python_PM2.5/blob/master/%E6%AF%8F%E4%B8%AA%E5%9F%8E%E5%B8%82%E7%9A%84%E6%B1%A1%E6%9F%93%E7%8A%B6%E5%86%B5.png"/>
</div>
