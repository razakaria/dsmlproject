# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown', 
                                options=[{'label':'All Sites', 'value':'All Sites'}, {'label':'CCAFS LC-40', 'value':'CCAFS LC-40'}, {'label':'VAFB SLC-4E', 'value':'VAFB SLC-4E'}, {'label':'KSC LC-39A', 'value':'KSC LC-39A'}, {'label':'CCAFS SLC-40', 'value':'CCAFS SLC-40'}], 
                                value='All Sites', placeholder='Select a Launch Site here', searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider', 
                                min=0, max=10000, step=1000,
                                marks={0:'0', 2500:'2500', 5000:'5000', 7500:'7500', 10000:'10000'}, 
                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'), 
Input(component_id='site-dropdown', component_property='value'))

def get_graph(entered_site):
    if entered_site == 'All Sites':
        g1 = spacex_df.groupby(['Launch Site'])['class'].sum().reset_index()
        fig1 = px.pie(g1, values='class', names='Launch Site', title='Total Success Launches By Site')
        fig1.update_layout()
        return fig1
    else:
        df = spacex_df[spacex_df['Launch Site']==entered_site]
        g2 = df.groupby(['class'])['Launch Site'].count().reset_index()
        fig2 = px.pie(g2, values='Launch Site', names='class', title='Total Success Launches for site '+ str(entered_site))
        fig2.update_layout()
        return fig2

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'), 
[Input(component_id='site-dropdown', component_property='value'), 
Input(component_id="payload-slider", component_property="value")])

def get_scatter(entered_site, entered_payload):
    g3 = spacex_df[(spacex_df['Payload Mass (kg)'] >= entered_payload[0]) & (spacex_df['Payload Mass (kg)'] <= entered_payload[1])]
    if entered_site == 'All Sites':
        fig3 = px.scatter(g3, x='Payload Mass (kg)', y='class', color='Booster Version Category', title='Correlation between Payload and Success for all Sites')
        fig3.update_layout()
        return fig3
    else:
        g4 = g3[g3['Launch Site']==entered_site]
        fig4 = px.scatter(g4, x='Payload Mass (kg)', y='class', color='Booster Version Category', title='Correlation between Payload and Success for '+str(entered_site))
        fig4.update_layout()
        return fig4

# Run the app
if __name__ == '__main__':
    app.run_server()

