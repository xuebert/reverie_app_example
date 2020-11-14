import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#delaney_dataset= pd.read_csv('~/repos/reverie_axue/delaney-processed.csv', index_col="Compound ID")
delaney_dataset= pd.read_csv('delaney-processed.csv', index_col="Compound ID")
labels = delaney_dataset["measured log solubility in mols per litre"].values
calculated_properties = delaney_dataset[["Molecular Weight", "Number of H-Bond Donors", "Number of Rings", "Number of Rotatable Bonds", "Polar Surface Area"]]


import plotly.express as px
plotly_df = calculated_properties
plotly_df['solubility'] = labels
molecule_names = calculated_properties.index.tolist()

fig = px.scatter_matrix(calculated_properties.drop(columns='solubility')
  , dimensions= ['Molecular Weight', 'Number of H-Bond Donors', 'Number of Rings',
       'Number of Rotatable Bonds', 'Polar Surface Area']
  , hover_name = pd.Series(calculated_properties.index)
  , color = calculated_properties['solubility'])


fig.update_layout(
    dragmode='select',
    width=1200,
    height=1200,
    hovermode='closest',
)


import plotly.graph_objs as go
fig2 = go.FigureWidget(px.scatter(calculated_properties, x= 'Molecular Weight', y='Number of H-Bond Donors'))
scatter = fig2.data[0]
colors = ['#a3a7e4'] * 100
scatter.marker.color = colors
scatter.marker.size = [10] * 100
fig2.layout.hovermode = 'closest'

# create our callback function
def update_point(trace, points, selector):
    c = list(scatter.marker.color)
    s = list(scatter.marker.size)
    for i in points.point_inds:
        c[i] = '#bae2be'
        s[i] = 20
        scatter.marker.color = c
        scatter.marker.size = s
scatter.on_click(update_point)

app.layout = html.Div(children=[
    html.H1(children='Scatterplot matrix with molecule upon click'),

    html.Div(children='''
        Idea: click the point and the molecule shows up underneath the plot. Doesn't work :(
    '''),

    dcc.Graph(
        id='splom',
        figure=fig
    ),
    html.Img(src=app.get_asset_url('how_do_i_dash.png')),
    #html.Img(
    #    id="image",
    #    className="quick_meme",
    #    src='~/repos/test/how_do_i_dash.png'
    #)
    #dcc.Graph(
    #    id='molecule',
    #    figure=fig2
    #)
])


if __name__ == '__main__':
    app.run_server(debug=True)
