from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

app = Dash(__name__)

# ===============================================================================
# import and clean data

df = pd.read_csv("dailyActivity_merged1.csv")
df.drop(columns=['TrackerDistance'], inplace=True)
df['TotalTime'] = (df['VeryActiveMinutes'] + df['FairlyActiveMinutes'] +
                   df['LightlyActiveMinutes'] + df['SedentaryMinutes'])
df['SpeedMilePerMinute'] = df['TotalDistance'] / df['TotalTime']

# ===============================================================================
# App layout
app.layout = html.Div([
    # header
    html.Div([
        html.H1('IoT device is FitBit Fitness Tracker',
                className="header-title"),
        html.Br(),
        html.P("Analyze the weight lost by fitBit user"
               "and there daily activity distance, time, and Calories lost",
               className='header-description'),
    ],
        className="header"),

    # -----------------------------------------
    # Dropdown
    html.Div([
        html.Div([
            html.H2("select user number "),
            dcc.Dropdown(
                options=df['Id'].unique(),
                value=df['Id'].unique()[0],
                id="user_number",
            )],
            style={'width': '40%', 'display': 'inline-block',
                   "text-align": "center", "margin": "auto"}),

    ], style={"text-align": "center"}),
    html.Br(),

    # -----------------------------------------------
    # main gragh
    html.Div([
        dcc.Graph(
            id='user_plot',
            figure={},
            clickData=None,
            hoverData=None,
        ),
        dcc.Graph(
            id='calore_scater_plot',
            figure={},
            clickData=None,
            hoverData=None,
        )
    ],
        style={'width': '60%',
               'display': 'inline-block',
               'padding': '0 20',
               'justify-content': 'space-between',
               'margin-left': '15px',
               'margin-right': '10px'
               }
    ),

    # --------------------------------------------------
    # pie chart
    html.Div([
        dcc.Graph(id='active_distance', figure={}),

        dcc.Graph(id='active_minutes', figure={}),
    ],
        style={'display': 'inline-block',
               'width': '37%',
               'margin-right': '10px',
               'justify-content': 'space-between'
               }),

])

# ===============================================================================
# callback
@app.callback(
    Output(component_id="user_plot", component_property="figure"),
    [Input(component_id="user_number", component_property='value')]
)
def update_graph(option_slctd):
    dff = df.copy()
    dff = dff[dff["Id"] == option_slctd]
    # Plotly Express
    fig = px.bar(
        data_frame=dff,
        x='ActivityDate',
        y=['TotalSteps','Calories'],
        text_auto='.2s',
        # hover_data=['Calories','TotalSteps'],
        title="bar chart of the user activity"
    )
    return fig

# --------------------------------------------------------
# plot the relation between the speed and the calories lost
@app.callback(
    Output(component_id="calore_scater_plot", component_property="figure"),
    [Input(component_id="user_number", component_property='value')]
)
def update_scater_plot(option_slctd):
    dff = df.copy()
    dff = dff[dff["Id"] == option_slctd]
    # Plotly Express
    fig = px.scatter(
        data_frame=dff,
        x="Calories",
        y="SpeedMilePerMinute",
        trendline="ols",
        title="The relation between the user sped and calories lost"
    )
    return fig

# --------------------------------------------------------
# pie chart the active distance
@app.callback(
    Output(component_id="active_distance", component_property="figure"),
    [Input(component_id="user_plot", component_property='hoverData'),
     Input(component_id="user_number", component_property='value')]
)
def update_side_graph_distance(hov_data, option_slctd):
    if hov_data is None:
        dff2 = df.copy()
        dff2 = dff2[dff2["Id"] == option_slctd]
        # get the total activities Distance
        tot_dis = dff2.loc[dff2['ActivityDate'] == dff2["ActivityDate"].unique()[0],
                           'TotalDistance'].reset_index(drop=True)[0]
        # creat a dataframe for the activities Distance
        random_date_distance = dff2.loc[dff2['ActivityDate'] == dff2['ActivityDate'].unique()[0],
                                        ['LoggedActivitiesDistance',
                                         'VeryActiveDistance',
                                         'ModeratelyActiveDistance',
                                         'LightActiveDistance',
                                         'SedentaryActiveDistance']]
        # chang it to a columns dataframe
        random_date_distance = random_date_distance.T
        # # get the non_zeros values only
        dff2 = random_date_distance.loc[
            random_date_distance[random_date_distance.columns[0]] > 0]
        # Plotly Express
        fig2 = px.pie(data_frame=dff2,
                      values=dff2.columns[0],
                      names=dff2.index,
                      title=f'activity distance: {round(tot_dis,3)} mile -> for: {df["ActivityDate"].unique()[0]}')
        return fig2
    else:
        dff2 = df.copy()
        dff2 = dff2[dff2["Id"] == option_slctd]
        # get the date using the hoverData function
        hov_date_v = hov_data['points'][0]['x']
        # get the total activities Distance
        tot_dis = dff2.loc[dff2['ActivityDate'] == hov_date_v, 'TotalDistance'].reset_index(drop=True)[0]
        # create a dataframe for the activities Distance
        random_date_distance = dff2.loc[dff2['ActivityDate'] == hov_date_v,
                                        ['LoggedActivitiesDistance',
                                         'VeryActiveDistance',
                                         'ModeratelyActiveDistance',
                                         'LightActiveDistance',
                                         'SedentaryActiveDistance']]
        # chang it to a columns dataframe
        random_date_distance = random_date_distance.T
        # get the non_zeros values only
        dff2 = random_date_distance.loc[
            random_date_distance[random_date_distance.columns[0]] > 0]
        # Plotly Express
        fig2 = px.pie(data_frame=dff2,
                      values=dff2.columns[0],
                      names=dff2.index,
                      title=f'activity distance: {round(tot_dis,3)} mile -> for: {hov_date_v}')
        return fig2

# --------------------------------------------------------
# pie chart the active minutes
@app.callback(
    Output(component_id="active_minutes", component_property="figure"),
    [Input(component_id="user_plot", component_property='hoverData'),
     Input(component_id="user_number", component_property='value')]
)
def update_side_graph_minutes(hov_data, option_slctd):
    if hov_data is None:
        dff3 = df.copy()
        dff3 = dff3[dff3["Id"] == option_slctd]
        # get the total minute
        tot_min = dff3.loc[dff3['ActivityDate'] == dff3["ActivityDate"].unique()[0],
                           'TotalTime'].reset_index(drop=True)[0]
        # create a dataframe for the activities Distance
        random_date_minutes = dff3.loc[dff3['ActivityDate'] == dff3['ActivityDate'].unique()[0],
                                       ['VeryActiveMinutes',
                                        'FairlyActiveMinutes',
                                        'LightlyActiveMinutes',
                                        'SedentaryMinutes']]
        # chang it to a columns dataframe
        random_date_minutes = random_date_minutes.T
        # get the non_zeros values only
        dff3 = random_date_minutes.loc[
            random_date_minutes[random_date_minutes.columns[0]] > 0]

        # Plotly Express
        fig3 = px.pie(data_frame=dff3,
                      values=dff3.columns[0],
                      names=dff3.index,
                      title=f'activity time: {tot_min} min -> for: {df["ActivityDate"].unique()[0]}')
        return fig3
    else:
        dff3 = df.copy()
        dff3 = dff3[dff3["Id"] == option_slctd]
        # get the date using the hoverData function
        hov_date_v = hov_data['points'][0]['x']
        # get the total minute
        tot_min = dff3.loc[dff3['ActivityDate'] == hov_date_v, 'TotalTime'].reset_index(drop=True)[0]
        # create a dataframe for the activities Distance
        random_date_minutes = dff3.loc[dff3['ActivityDate'] == hov_date_v,
                                       ['VeryActiveMinutes',
                                        'FairlyActiveMinutes',
                                        'LightlyActiveMinutes',
                                        'SedentaryMinutes']]
        # chang it to a columns dataframe
        random_date_minutes = random_date_minutes.T
        # get the non_zeros values only
        dff3 = random_date_minutes.loc[
            random_date_minutes[random_date_minutes.columns[0]] > 0]

        # Plotly Express
        fig3 = px.pie(data_frame=dff3,
                      values=dff3.columns[0],
                      names=dff3.index,
                      title=f'activity time: {tot_min} min -> for: {hov_date_v}  ')
        return fig3

# ===============================================================================
if __name__ == '__main__':
    app.run_server(debug=True)