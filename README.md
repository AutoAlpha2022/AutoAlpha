# 周二

(1) 今天参考了[alphalens](https://github.com/quantopian/alphalens), 并在此基础上开发回测框架，具体分为

time-IC 折线图
正态分布图
QQ图
热力图
Cumulative return 
Cumulative return by quantile

1D period forward return IC
2D period forward return IC(存疑)
5D period forward return IC(存疑)

(2) 整理因子开发的格式
因子名称: Liquidity_DeltaTurnover
一级分类: PriceVolume
二级分类: Liquidity
因子编号: Factor01040009
因子含义: 
因子说明:
因子算法:
因子来源：海通证券《选股因子系列研究 *****》


## 特征提取

* How and When are High-Frequency Stock Returns Predictable
* Feature Extraction, Performance Analysis and System Design Using the DU Mobility Dataset
* Feature Extraction Methods in Quantitative Structure–Activity Relationship Modeling: A Comparative Study
* [Automatic extraction of relevant features from time series](https://github.com/blue-yonder/tsfresh)
## 数据预处理
* 涨跌停
* ST去除
## 因子开发分类
* message data
* orderbook data(minute level)
## 因子开发逻辑
* 微观结构
* 高频因子
* 交易量
  * traded volume
  * limit order volume
* 波动率 
* Order flow imbalance
* 遗传算法因子挖掘
  * 基于遗传规划的选股因子挖掘
  * 时间无关性
## 因子测试框架
* IC
* rank IC
* 换手率
* 超额收益
* **图表**
## 生成投资组合
* 股票选择

## Barra 风险分析
