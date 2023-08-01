import pandas as pd
from plotly.offline import plot
import plotly.graph_objects as go
from .models import *

# 메인화면 데이터 시각화 start
def data_visualization():
    df_item = pd.DataFrame(list(Item.objects.all().values()))
    filt_1 = ((df_item['item_price'] >= 100000) & (df_item['item_price'] < 450000))
    filt_2 = ((df_item['item_price'] >= 450000) & (df_item['item_price'] < 800000))
    filt_3 = ((df_item['item_price'] >= 800000) & (df_item['item_price'] < 1600000))
    df_item_1 = df_item[filt_1]
    df_item_2 = df_item[filt_2]
    df_item_3 = df_item[filt_3]

    labels = ['10만원~45만원', '45만원~80만원', '80만원~160만원']
    values = [len(df_item_1['item_price']), len(df_item_2['item_price']),len(df_item_3['item_price'])]

    fig = go.Pie(labels=labels, values=values, hoverinfo='percent+label', insidetextorientation='radial', hole=.3)

    graphs2 = []
    graphs2.append(fig)

    layout_pie = {'title': '지금 이만큼이나 거래 중이에요 :0',
                    'height': 480,
                    'width': 1270,}
                    
    fig_div = plot({'data':graphs2, 'layout' : layout_pie}, output_type='div')
    

    df_trade = pd.DataFrame(list(Trade.objects.all().values()))
   
    Filt_1 = ((df_trade['item_price'] >= 100000) & (df_trade['item_price'] < 450000))
    Filt_2 = ((df_trade['item_price'] >= 450000) & (df_trade['item_price'] < 800000))
    Filt_3 = ((df_trade['item_price'] >= 800000) & (df_trade['item_price'] < 1600000))
    df_trade_1 = df_trade[Filt_1]
    df_trade_2 = df_trade[Filt_2]
    df_trade_3 = df_trade[Filt_3]
    x1 = df_trade_1['item_date']
    x2 = df_trade_2['item_date']
    x3 = df_trade_3['item_date']

    def get_counts(seq):
        counts={}
        for x in seq:
            if x in counts:
                counts[x] += 1
            else : 
                counts[x] = 1
        return counts

    count_1 = get_counts(x1)
    count_2 = get_counts(x2)
    count_3 = get_counts(x3)

    x1 = list(count_1.keys())
    x2 = list(count_2.keys())
    x3 = list(count_3.keys())
    y1 = []
    y2 = []
    y3 = []

    for i in list(count_1.keys()):
        y1.append(count_1[i])
    for i in list(count_2.keys()):
        y2.append(count_2[i])  
    for i in list(count_3.keys()):
        y3.append(count_3[i])      

    graphs1 = []
    graphs1.append(go.Bar(x=x1, y=y1, name="10만원~45만원",))
    graphs1.append(go.Bar(x=x2, y=y2, name="45만원~80만원",))
    graphs1.append(go.Bar(x=x3, y=y3, name="80만원~160만원",))
   
    

    layout_graph = {
        'title': '최근 이만큼이나 거래됐어요! :)',
        'xaxis_title': 'Date',
        'yaxis_title': '수량 (개)',
        'height': 480,
        'width': 1270,}

    plot_div = plot({'data': graphs1, 'layout': layout_graph}, 
                    output_type='div')
    
    context = dict()
    context['plot_div'] = plot_div
    context['fig_div'] = fig_div 

    return context
# 메인화면 데이터 시각화 end