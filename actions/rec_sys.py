import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import table

df = pd.read_csv('D:/new/ayush/rasa_beginner/actions/lap25.csv')
df2 = pd.read_csv('D:/new/ayush/rasa_beginner/actions/lap28.csv')
cols = ['brand', 'laptop_name', 'price', 'type', 'style', 'screen_size', 'cpu_type', 
        'gpu/vpu', 'memory', 'memory_speed', 'storage_spec', 'ssd', 'operating_system', 
        'resolution', 'dimensions_(w_x_d_h)', 'weight', 'date_first_available']

def get_rec(price, usecase=None, brand=None, screen_size_name=None):
    if screen_size_name:
        screen_size_dict = {"10 inch": [10.1, 10.5], "11 inch": [11.6], "12 inch": [12.3, 12.5],
                            "13 inch": [13., 13.3, 13.4, 13.5], "14 inch": [14.], "15 inch": [15., 15.6],
                            "16 inch": [16., 16.1], "17 inch": [17.3]} 
        screen_size = screen_size_dict[screen_size_name]
    if brand and usecase and screen_size_name:
        ind = df.index[(df['type'] == usecase) & (df['price'] >= (price - 10000)) & (df['price'] <= (price + 10000)) & (df['brand'] == brand) & (df['screen_size_score'].isin(screen_size))]
    elif brand and usecase:
        ind = df.index[(df['type'] == usecase) & (df['price'] >= (price - 10000)) & (df['price'] <= (price + 10000)) & (df['brand'] == brand)]
    elif brand and screen_size_name:
        ind = df.index[(df['price'] >= (price - 10000)) & (df['price'] <= (price + 10000)) & (df['brand'] == brand) & (df['screen_size_score'].isin(screen_size))]
    elif usecase and screen_size_name:
        ind = df.index[(df['type'] == usecase) & (df['price'] >= (price - 10000)) & (df['price'] <= (price + 10000)) & (df['screen_size_score'].isin(screen_size))]
    elif usecase:
        ind = df.index[(df['type'] == usecase) & (df['price'] >= (price - 10000)) & (df['price'] <= (price + 10000))]
    elif brand:
        ind = df.index[(df['brand'] == brand) & (df['price'] >= (price - 10000)) & (df['price'] <= (price + 10000))]
    elif screen_size_name:
        ind = df.index[(df['screen_size_score'].isin(screen_size)) & (df['price'] >= (price - 10000)) & (df['price'] <= (price + 10000))]
    else:
        ind = df.index[(df['price'] >= (price - 10000)) & (df['price'] <= (price + 10000))]
    
    ind2 = df2.loc[ind, 'total'].sort_values(ascending=False).index[:5]
    length = len(ind2)
    
    if length < 5:
        next = None
        if brand and usecase and screen_size_name:
            ind = df.index[((df['brand'] == brand) | (df['type'] == usecase) | (df['screen_size_score'].isin(screen_size))) & (df['price'] >= (price - 10000)) & (df['price'] <= (price + 10000))]
            next = 1
                    
        elif brand and usecase:
            ind = df.index[((df['type'] == usecase) | (df['brand'] == brand)) & (df['price'] >= (price - 10000)) & (df['price'] <= (price + 10000))]
            next = 1
            
        elif usecase and screen_size_name:
            ind = df.index[((df['type'] == usecase) | (df['screen_size_score'].isin(screen_size))) & (df['price'] >= (price - 10000)) & (df['price'] <= (price + 10000))]
            next = 1
            
        elif brand and screen_size_name:
            ind = df.index[((df['brand'] == brand) | (df['screen_size_score'].isin(screen_size))) & (df['price'] >= (price - 10000)) & (df['price'] <= (price + 10000))]
            next = 1
         
        if next:
            ind3 = ind[~ind.isin(ind2)]
            ind2 = ind2.append(df2.loc[ind3, 'total'].sort_values(ascending=False).index[:(5 - length)])
            length = len(ind2)
            
        if (length < 5) and (brand or usecase or screen_size_name):
            ind = df.index[(df['price'] >= (price - 10000)) & (df['price'] <= (price + 10000))]
            ind3 = ind[~ind.isin(ind2)]
            ind2 = ind2.append(df2.loc[ind3, 'total'].sort_values(ascending=False).index[:(5 - length)])
            length = len(ind2)
            
        if (length < 5) or (price and not(usecase or brand or screen_size_name)):
            ind = df.index[df['price'] <= (price + 10000)]
            ind3 = ind[~ind.isin(ind2)]
            ind2 = ind2.append(df2.loc[ind3, 'total'].sort_values(ascending=False).index[:(5 - length)])
            length = len(ind2)

        if length == 0:
            return "No laptop found that meets any of the entered criteria."
        
    ax = plt.subplot(111, frame_on=False) # no visible frame
    ax.xaxis.set_visible(False)  # hide the x axis
    ax.yaxis.set_visible(False)  # hide the y axis
    tb = table(ax, df.loc[ind2, cols])
    tb.auto_set_font_size(False)
    tb.set_fontsize(14)
    tb.auto_set_column_width(col=list(range(len(df.columns))))
    tb.scale(2, 2)
    plt.savefig('D:/new/ayush/rasa_beginner/actions/img/lap_rec.png', bbox_inches='tight')