
### 因子评价
* XGB 树分裂的参考
   * 信息增益 
* 线性回归的参考
### 因子处理函数
* def neutralize(): 中性化
* def winsorize(): 去极值
* def winsorize_med(): 中位数去极值
* def standrlize(): 标准化
### 具体事项
* [回测报告](https://github.com/AutoAlpha2022/AutoAlpha/issues/1)
* ST剔除，结果保存在NAS/output中。3000+ => 2100 (2018-2022)
### 因子生成
* 可选因子：流动性、波动率和不平衡性。以及其他基础指标
  * 分钟级，流动性，不平衡性
  * 根据分钟级的曲线，来提取特征，实现因子
  * 预测？下一日的流动性
  * R^Squared
  * 流动性转化为收益率
  * 流动性的变化率
* [可选变换](https://github.com/AutoAlpha2022/AutoAlpha/issues/2)：min max 普通运算 rank
### 股票选择：
* 根据因子值的大小排序，选择股票
* 根据quantile分组
* 选股去掉涨停
* 行业，大盘指数
* twap均价。作为成交的价格。成交时间：一天？五天？
* PnL (未完成) 
* 数量选择：
    * 等权重配置
    * 组合风险最小化（最小化组合方差）；组合总权重限制为90%到100%；组合年化收益率目标下限为10%
    * 组合夏普比率最大化；每只标的权重不超过10%
### 问题
* 如何访问到docker里面的文件。pycharm 只能download 不能upload吗？
* ~~如何一行一行运行？~~
* Debug

![image](https://user-images.githubusercontent.com/121123877/209524199-c230df48-d9ad-4f14-84e9-dcd096833183.png)


</br> </hr>
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
* [Kaggle HFT Orderbook Features Ext](https://www.kaggle.com/code/luiscl/hft-orderbook-features-ext)
* [Wavelet](https://github.com/AutoAlpha2022/AutoAlpha/issues/4)
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
