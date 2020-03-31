import dash 
import dash_core_components as dcc 
import dash_html_components as html 
import plotly.graph_objs as go 
import numpy as np 
from dash.dependencies import Input, Output
import pandas as pd 
from scipy import stats

df = pd.read_csv('fantasy_data_pfr.csv')

app = dash.Dash()

app.layout = html.Div([
    dcc.Graph(
        id='plot'
    ),

    dcc.Dropdown(
        id='stat',
        options=[{'label': i, 'value': i} for i in df.columns],
        value='Fantasy_PPR'
    )
])

@app.callback(
    Output('plot', 'figure'),
    [Input('stat', 'value')]
)
def update_output_div(input_value):

    # Create dataframe of the stats to compare to the previous year
    df_temp = df.copy()
    df1 = df_temp[['Player', input_value, 'Year']]
    df2 = df1.copy()
    df2['Year'] = df2['Year'] - 1
    df3 = df1.merge(df2, on=['Player','Year'], how='inner', suffixes=['_y','_y-1'])
    df3.columns = ['Player', 'Stat_Y','Year','Stat_Y-1']

    # Create the regression line to fit the data
    x = np.arange(0, df3['Stat_Y-1'].max()+1)
    slope, intercept, r_value, p_value, std_err, = stats.linregress(df3['Stat_Y-1'], df3['Stat_Y'])
    line = slope*x+intercept
    r2 = round(r_value*r_value, 2)
    trace1 = {
        'x': df3['Stat_Y-1'],
        'y': df3['Stat_Y'],
        'mode':'markers',
        'text':df3['Player']
    }

    trace2 = {
        'x':x,
        'y':line,
        'mode':'lines',
        'marker': {'color':'rgb(31, 119, 180'}
    }

    return {'data':[trace1, trace2],
            'layout': dict(title=f'R^2 = {r2}',
                           hovermode='closest') }

if __name__ == '__main__':
    app.run_server(debug=True)