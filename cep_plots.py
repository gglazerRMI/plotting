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
df_learningrates = load_pickle('learning_rates')
# print(df_learningrates.head())

y1 = 'Cost\nComp\nBAU - CEP ($/MWh)'

df_main = df_learningrates.loc[(df_learningrates['Scenario'] == '0main'), :]
df_main = df_main.sort_values(by=[y1])
df_main.reset_index(inplace=True)

x = list(df_main.loc[:, 'Case'])
y = list(df_main.loc[:, y1])

inc = 0
o_x = 0
for row in list(df_main.index):
    cap = df_main.loc[row, x]


w = list(df_main.loc[:, 'Data\nCaseInfo\nCapacity (MW)'])

# x = ['Grant', 'Loves', 'Charts']
# y = [12, 3.2, 9.9]
# w = [1, 1, 1]

trace0 = go.Bar(
    x=x,
    y=y,
    width=w
)

title = 'Super Important Data'
height = 100 + 250 * len(y)

data = [trace0]
fig = go.Figure(data=data)
fig['layout'].update(title=title, height=height, yaxis=dict(title='Values', tickformat='$,0'), xaxis=dict(title='Cases'))
pio.write_image(fig, fig_path + 'supply_curve.jpg')
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