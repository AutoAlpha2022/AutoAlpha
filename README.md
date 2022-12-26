* [回测报告](https://github.com/AutoAlpha2022/AutoAlpha/issues/1)
* ST剔除，结果保存在NAS/output中。3000+ => 2100 (2018-2022)

* 如何访问到docker里面的文件。pycharm 只能download 不能upload吗？
* 如何一行一行运行？

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

(2) 因子开发的格式
因子名称: Liquidity_DeltaTurnover
一级分类: PriceVolume
二级分类: Liquidity
因子编号: Factor01040009
因子含义: 
因子说明:
因子算法:
因子来源：海通证券《选股因子系列研究 *****》

工厂方法生成因子类

```python
class StockFactor(object):
    def __init__(self, name,category,description):
        """
        初始化因子
        :param name: 因子名称
        """
        self.name = name
        self.category = category
        self.description = description

    def name(self):
        return self.name

    @abstractmethod
    def compute(self, start_date, end_date):
        """
        计算指定周期内的因子值
        :param start_date:  开始时间
        :param end_date:  结束时间
        """
        pass
```



(3)继续研究高频语境下的orderflow imbalance和volatility。看了两篇论文，约了组里的同学明天开会讨论一下。

(4)数据预处理

* 剔除上市时间不满60天的新股

* 采用MAD法侦测单变量的异常值,将均值和标准差换成稳健的统计量,均值用样本中位数代替,标准差用样本MAD代替,缺失值不作处理
* ？？？存疑：加入行业因素
* ？？？存疑： 对规模和行业进行中性化处理





</hr></br>

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
