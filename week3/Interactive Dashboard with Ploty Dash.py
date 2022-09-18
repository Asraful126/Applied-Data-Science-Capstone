# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objs as go

# Read the airline data into pandas dataframe
df = pd.read_csv("data.csv")
max_payload = df['Payload Mass (kg)'].max()
min_payload = df['Payload Mass (kg)'].min()



# Create a dash application
app = dash.Dash(__name__)
#
# Create an app layout
app.layout = html.Div([
    html.H1('Space Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),

        dcc.Dropdown(id='site-dropdown',
                 options=[
                    {'label': 'All Launch Sites', 'value': 'All'},
                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                          ], value='ALL',
                             placeholder='Select a Launch Site here',
                            searchable=True
                 ),

        dcc.Graph(id='success-pie-chart'),

        html.Br(),

        dcc.RangeSlider(id='payload-slider',
                    min=0, max=10000, step=1000,
                    marks={0: '0',
                           2500: '2500',
                           5000:'5000',
                           7500:'7500'},
                    value=[min_payload, max_payload]),

        dcc.Graph(id='success-payload-scatter-chart')
])

@app.callback(
        Output('success-pie-chart', 'figure'),
        [Input('site-dropdown','value')]
    )

def get_pie_chart(selected_site):
     df_class_1 = df[df['class']==1]
     df_selected_site = df[df['Launch Site']==selected_site]
     if selected_site == 'All':
         fig = px.pie(df_class_1, values='class',
                        names='Launch Site',
                        title='Total Success Launches By Site')
         return fig
     else:
         fig = px.pie(df_selected_site, #values='class',
                      names='class',
                      title='Total Success Launches for site ' + selected_site)
         return fig


# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

@app.callback(Output('success-payload-scatter-chart', 'figure'),
              [Input('payload-slider', 'value'),
               Input('site-dropdown', 'value')])

def scatter(selected_mass, selected_site):

    df_filtered = df[(df['Payload Mass (kg)'] <= selected_mass[-1])
                     & (df['Payload Mass (kg)'] >= selected_mass[0])]
    df_site_filtered = df_filtered[df_filtered['Launch Site']==selected_site]
    if selected_site == 'All':
        fig = px.scatter(df_filtered, x= 'Payload Mass (kg)',
                                     y= 'class',
                                     color = 'Booster Version Category')


    else:
         fig = px.scatter(df_site_filtered, x= 'Payload Mass (kg)',
                                     y= 'class',
                                     color = 'Booster Version Category')

    return fig




# Run the app
if __name__ == '__main__':
    app.run_server()
