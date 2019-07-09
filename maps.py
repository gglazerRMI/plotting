import cep_plots as cp
import plotly.graph_objs as go
import plotly.io as pio
import os
import plotly
import plotly.plotly as py

path = str(os.path.dirname(os.path.realpath(__file__)))
fig_path = path + '/figs/maps/'
if not os.path.exists(fig_path):
    os.mkdir(fig_path)

df_dsm = cp.load_pickle('dsm')

scenario = '0main'
df1 = df_dsm

dfp = df1.loc[(df1['Scenario'] == scenario), :]
count = dfp['Data\nCaseInfo\nLatitude'].isnull().sum()

fig = go.Figure()
map = go.Scattergeo(
        locationmode = 'USA-states',
        lat = dfp['Data\nCaseInfo\nLatitude'],
        lon = dfp['Data\nCaseInfo\nLongitude'],
        text = dfp['Case'],
        marker = go.scattergeo.Marker(
            size = dfp['Data\nCaseInfo\nCapacity (MW)']/100,
            color = 'rgb(10,20,30)'
        )
    )

fig.add_trace(map)
fig['layout'].update(geo=go.layout.Geo(scope='usa', projection=go.layout.geo.Projection(type='albers usa')))
pio.write_image(fig, fig_path + 'scatter_map.png')