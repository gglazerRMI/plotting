import numpy as np
import pandas as pd
import pickle
import os
import pandas.io.formats.excel
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.io as pio
import requests
import scipy
import xlsxwriter
from plotly import tools
from pdfrw import PdfReader, PdfWriter

pd.set_option('display.max_columns', 100)
path = str(os.path.dirname(os.path.realpath(__file__)))
fig_path = path + '/figs/'
if not os.path.exists(fig_path):
    os.mkdir(fig_path)


def load_pickle(name):
    """ Function to load an object from a pickle """
    with open(str(name) + '.pkl', 'rb') as f:
        temp = pickle.load(f)
    return temp


def save_pickle(contents, name):
    """ Function to save to an object as a pickle """
    with open(str(name) + '.pkl', 'wb') as output:
        pickle.dump(contents, output, pickle.HIGHEST_PROTOCOL)

# def make_var_width(self, x, y, df, title):
#     fig = tools.make_subplots(rows=df.shape[0], cols=1, suplot_titles = )

# df_learningrates = pd.read_excel('/Users/gglazer/OneDrive - Rocky Mountain Institute/supplycurvemain.xlsx',
#                          sheet_name='SummaryOutputs')
# save_pickle(df_learningrates, 'learning_rates')
# df_learningrates = load_pickle('learning_rates')


# df_dsm = pd.read_excel('/Users/gglazer/Downloads/DSM_20190614_1910.xlsx', sheet_name='SummaryOutputs')
# save_pickle(df_dsm, 'dsm')
df_dsm = load_pickle('dsm')


#------SETTINGS------####
df1 = df_dsm  # can be df_dsm or df_learning rates
ttl = 'Net'  # NPV, LCOE, or Net
key = 'NGCC'  # NGCC or NGCT
scenario = '0main'  # can be any scenario in the df 4aNoDSM
export = True
#-------------------#####

xcol = 'Data\nCaseInfo\nCapacity (MW)'
xlabel = 'Cumulative Capacity\n(MW)'
if ttl == 'NPV':
    ycol = 'Cost\nComp\nBAU - CEP (000)'
    ylabel = 'CEP Cost Savings\n($000)'
elif ttl == 'LCOE':
    ycol = 'Cost\nComp\nBAU - CEP ($/MWh)'
    ylabel = 'BAU NPV - CEP NPV\n($/MWh)'
elif ttl == 'Net':
    df1['Net Cost Diff'] = (df1['Cost\nBAU\nTotal (000)'] - df1['Cost\nCEP\nNet Cost (000)']) / 1000000
    ycol = 'Net Cost Diff'
    ylabel = 'CEP Net Cost Savings\n($B)'

df_main = df1.loc[(df1['Scenario'] == scenario), :]
df_main = df_main.sort_values(by=[ycol])
df_main.reset_index(inplace=True)
if export:
    df_main.to_csv('df_'+scenario+'.csv')
regions = sorted(list(set(df_main.loc[:, 'Data\nCaseInfo\nRegion'].values.tolist())))
reg_colors = {'Northeast': '#005289',
                  'Midwest': '#004c4a',
                  'Southeast': '#ab0326',
                  'Texas': '#fbab18',
                  'Northcentral': '#507c1d',
                  'Southwest': '#5e0215',
                  'West': '#DB6F11'}
col = 'Data\nCaseInfo\nType'
screens = {'col': col, 'key': key}

if key != 'All':
    df_main = df_main[df_main[screens['col']] == screens['key']]


fig = go.Figure()
inc = 0 # increment: previous plant's capacity
o_x = 0 # old x
# x has to be numeric, refer to center point of each var-width bar
# x tells it where to put center of bar, w tells how wide each bar should be
for row in list(df_main.index):
    cap = df_main.loc[row, xcol]   # cap = current plant's capacity, x refers to the column type you want to use as var width
    n_x = o_x + inc/2 + cap/2
    df_main.loc[row, 'for_var_x'] = n_x
    o_x = n_x
    inc = cap
for reg in regions:
    df2 = df_main[df_main['Data\nCaseInfo\nRegion'] == reg]
    fig.add_trace(go.Bar(y=df2.loc[:, ycol],
                         x=df2.loc[:, 'for_var_x'].values.tolist(),
                         width=df2.loc[:, xcol].values.tolist(), showlegend=True,
                         name=reg, marker=dict(color=reg_colors[reg],
                                               line=dict(color='rgb(255,255,255)', width=0.125))))

title = 'CEP vs BAU Supply Curve, ' + scenario + ', ' + screens['key'] + ', ' + ttl
height = 100 + 250

# data = [trace0]
# fig1 = go.Figure(data=data)
fig['layout'].update(title=title, height=height, yaxis=dict(title=ylabel, tickformat='$,0'), xaxis=dict(title=xlabel))
pio.write_image(fig, fig_path + 'supply_curve_'+scenario+'_'+screens['key']+'_'+ttl+'.png')
# files = []
# for filename in os.listdir(fig_path):
#     if filename.endswith('.pdf'):
#         files.append(fig_path + filename)
#     files.sort(key=str.lower)
#
#     writer = PdfWriter()
#     for inpfn in files:
#         writer.addpages(PdfReader(inpfn).pages)
#     writer.write(fig_path+'pdfs/')