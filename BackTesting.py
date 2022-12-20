import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import time
import copy
import pyecharts.options as opts
from pyecharts.charts import Bar, Line
# TODO implement the EquityData() for high-frequency-alpha

#%%日期转换函数
def date_format(date):
    """
    将格式为yyyymmdd的字符串转变为yyyy-mm-dd的格式
    """
    strlist = list(date)
    strlist.insert(4,'-')
    strlist.insert(7,'-')
    date = ''.join(strlist)
    return date


#%%回测函数
def Backtesting(weight,bench_code):
    '''    

    Parameters
    ----------
    weight : DataFrame
        所有股票在（start_date,end_date）下的持仓权重
        column 为 date asset weight
    bench_code : Str
        基准资产代码 例如：000905.SH
    start_date : Str YYYYMMDD
        回测起始日期
    end_date : Str YYYYMMDD
        回测截止日期

    Returns
    -------
    Result : Dict
         'Performance': DataFrame
         列为：date ,PtfRet, BenchRet, AbRet, NetValue, MaxDrawDown
         'Assess': Series
         值为： Annualized Returns, Max Drawdown, Sharpe Ratio,Volatility,Turnover,WinRate
    '''    
    Dates = weight['date'].sort_values().unique().tolist()
    start_date = Dates[0].replace('-','')
    end_date = Dates[-1].replace('-','')
    pctchange = EquityData().get_stocks_price(start_date,end_date,fields=['n_pctChange'])
    pctchange.columns=['asset','date','n_pctChange']
    weights = weight.pivot(index = 'date',\
                           columns = 'asset',\
                           values = 'weight')
    cal_weights = weight.pivot(index = 'date',\
                           columns = 'asset',\
                           values = 'weight').shift(2).dropna()
    weights = weights.shift(2).dropna().unstack().reset_index()#调整日期
    df = pd.merge(weights,pctchange,on=['date','asset'])
    df.columns = ['asset', 'date', 'weight', 'ret']
    df['ret'] = df['weight']*df['ret']
    ret = df.groupby('date').sum()['ret'].rename('PtfRet')
    bench_ret = EquityData().get_index_daily_price(bench_code,start_date,end_date,fields=['n_pctChange'])
    bench_ret.columns = ['asset', 'date','ret']
    bench_ret = bench_ret.groupby('date').sum()['ret'].rename('BenchRet')
    Ret = pd.concat([ret,bench_ret],axis=1,sort = False).dropna()
    Ret['PtfRet'] = Ret['PtfRet']/100
    Ret['BenchRet'] = Ret['BenchRet']/100    
    Ret["AbRet"] = Ret["PtfRet"]-Ret["BenchRet"]  
    Ret["NetValue"] = np.cumprod(Ret["AbRet"]+1)
    Ret["MaxDrawDown"] = 1-Ret["NetValue"]/(Ret["NetValue"].cummax())        
    #计算策略评价指标
    result = pd.Series(index = ["Annualized Returns","Max Drawdown","Sharpe Ratio","Volatility","Turnover","WinRate"],name="value")
    lenth = len(Ret)    
    result.loc["Annualized Returns"] = (Ret["NetValue"][-1])**(250/lenth)-1
    result.loc["Max Drawdown"] = Ret["MaxDrawDown"].max()
    result.loc["Sharpe Ratio"] = Ret["AbRet"].mean()/Ret["AbRet"].std()*np.sqrt(250)
    result.loc["Volatility"] = Ret["AbRet"].std()*np.sqrt(250)
    result.loc["Turnover"] = (cal_weights.T.diff(1,axis=1).abs().sum()/2).mean()    
    result.loc["WinRate"] = (Ret["AbRet"]>0).sum()/Ret["AbRet"].count()
    Result = {}
    Result['Performance'] = Ret
    Result['Assess'] = result
    return Result

#%%回测展示
def BacktestingShow(data,html_name):
    '''
    描绘回测结果，三条净值曲线，组合净值，基准净值，相对强弱
    柱形图：每日最大回撤
    Parameters
    ----------
    data : DataFrame
        Columns：BenchRet NetValue PtfRet MaxDrawDown
    html_name : Str
        网页的名称，导出名字为 html_name.html

    Returns
    -------
    None.

    '''
    x_data = data.index.tolist()
    benchvalue = np.cumprod(data["BenchRet"]+1)
    netvalue = data['NetValue']
    ptfvalue = np.cumprod(data['PtfRet']+1)
    drawdown = data['MaxDrawDown']*100
    bar= (
         Bar()
        .add_xaxis(xaxis_data=x_data)
        .add_yaxis(
            series_name="最大回撤%",
            y_axis=drawdown.tolist(),
            yaxis_index=0,
            label_opts=opts.LabelOpts(is_show=False),
            
        )

    )    
    line = (
        Line(init_opts=opts.InitOpts(width="1600px", height="800px"))
        .add_xaxis(xaxis_data=x_data)
        .add_yaxis(
            series_name="相对强弱",
            yaxis_index=1,
            y_axis=netvalue,
            label_opts=opts.LabelOpts(is_show=False),
        )
        .add_yaxis(
            series_name="策略",
            yaxis_index=1,
            y_axis=ptfvalue,
            label_opts=opts.LabelOpts(is_show=False),
        )
        .add_yaxis(
            series_name="指数",
            yaxis_index=1,
            y_axis=benchvalue,
            label_opts=opts.LabelOpts(is_show=False),
        )
        .extend_axis(
            yaxis=opts.AxisOpts(
                name="净值",
                type_="value",
                )
        )
        
        .set_global_opts(
            tooltip_opts=opts.TooltipOpts(
                is_show=True, trigger="axis", axis_pointer_type="cross"
            ),
            xaxis_opts=opts.AxisOpts(
                type_="category",
                axispointer_opts=opts.AxisPointerOpts(is_show=True, type_="shadow"),
            ),
            yaxis_opts=opts.AxisOpts(
                name="最大回撤%",
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
                axislabel_opts=opts.LabelOpts(formatter="{value}%"),
                min_ = 0,
                max_ = 15,
            ),
            datazoom_opts=[
                opts.DataZoomOpts(range_start=20, range_end=100),
                opts.DataZoomOpts(type_="inside", range_start=20, range_end=100)
            ],
        )

    )
    
    line.overlap(bar).render(html_name+'.html')