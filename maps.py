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
types = ['NGCC', 'NGCT']
# print(dfp.loc[(dfp['Data\nCaseInfo\nType'] == types[1]), 'Data\nCaseInfo\nLatitude'])
colors = ['rgb(0,0,128)', 'rgb(0,255,255)']
scale = 50
# fig = go.Figure()
plants = []
print(range(len(types)))
for i in range(len(types)):
    print(colors[i])
    print(types[i])
    dft = dfp.loc[(dfp['Data\nCaseInfo\nType'] == types[i])]
    type = go.Scattergeo(
            locationmode='USA-states',
            lat=dft['Data\nCaseInfo\nLatitude'],
            lon=dft['Data\nCaseInfo\nLongitude'],
            # text=dfp['Case'],
            marker=go.scattergeo.Marker(
                size=dfp['Data\nCaseInfo\nCapacity (MW)']/scale,
                color=colors[i],
                line=go.scattergeo.marker.Line(
                    width=0.5, color='rgb(25,25,112)'
                ),
            # name=types[i]
            )
        )
    # fig.add_trace(type)
    plants.append(type)

# fig.add_trace(plants)
layout = go.Layout(
    title=go.layout.Title(
        text='Announced Planned Gas Plants as of June 2019'
    ),
    showlegend=True,
    geo=go.layout.Geo(
        scope='usa',
        projection=go.layout.geo.Projection(
            type='albers usa'
        ),
        showland=True,
        landcolor='rgb(217,217,217)',
        subunitwidth=1,
        countrywidth=1,
        subunitcolor="rgb(225,225,225)",
        countrycolor="rgb(225,225,225)"
    )
)
# fig['layout'].update(title=go.layout.Title(
#         text='Announced Planned Gas Plants as of June 2019'
#     ),
#     showlegend=True,
#     geo=go.layout.Geo(
#         scope='usa',
#         projection=go.layout.geo.Projection(
#             type='albers usa'
#         ),
#         showland=True,
#         landcolor='rgb(217,217,217)',
#         subunitwidth=1,
#         countrywidth=1,
#         subunitcolor="rgb(225,225,225)",
#         countrycolor="rgb(225,225,225)"
#     ))
fig = go.Figure(data=plants, layout=layout)
pio.write_image(fig, fig_path + 'scatter_map.png')