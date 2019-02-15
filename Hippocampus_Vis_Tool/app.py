# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import numpy as np

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash('visualize-hippocampus', external_stylesheets=external_stylesheets)
server = app.server

#df = pd.read_csv('pointclouds_col.csv')
df = pd.read_pickle('pointclouds_col.pkl')
print('Done loading pointcloud file')

def add_markers( figure_data, point_data, plot_type = 'scatter3d' ):
    indices = []
    point_data = figure_data[0]
    for pd in point_data:
        hover_text = figure_data['Status']
        for i in range(len(hover_text)):
            if pd == hover_text[i]:
                indices.append(i)

    traces = []
    for point_number in indices:
        trace = dict(
            x = [ figure_data['x'][point_number] ],
            y = [ figure_data['y'][point_number] ],
            z = [ figure_data['z'][point_number] ],
            marker = {
                'size': 15,
                'opacity': 0.6,
                'color': figure_data['color_val'],          # set color according to distance from mean as calculated above
                'colorscale': 'Cividis',
                'cmin': df['color_val'].min(),
                'cmax': df['color_val'].max(),
                'colorbar': {
                    'title': 'Distance<br>from mean'
                }
            },
            type = plot_type
        )

        traces.append(trace)

    return traces


def scatter_plot_3d(
        data = df,
        x = df['x'],
        y = df['y'],
        z = df['z'],
        xlabel = 'x',
        ylabel = 'y',
        zlabel = 'z',
        plot_type = 'scatter3d',
        markers = [] ):

    def axis_template_3d( title, type='linear' ):
        return dict(
            showbackground = True,
            backgroundcolor = BACKGROUND,
            gridcolor = 'rgb(255, 255, 255)',
            title = title,
            type = type,
            zerolinecolor = 'rgb(255, 255, 255)'
        )

    data = [ dict(
        x = x,
        y = y,
        z = z,
        mode = 'markers',
        type = plot_type,
        marker = {
                'size': 15,
                'opacity': 0.6,
                'color': df['color_val'],          # set color according to distance from mean as calculated above
                'colorscale': 'Cividis',
                'cmin': df['color_val'].min(),
                'cmax': df['color_val'].max(),
                'colorbar': {
                    'title': 'Distance<br>from mean'
                }
        }

    ) ]

    layout = dict(
        font = dict( family = 'Raleway' ),
        hovermode = 'closest',
        uirevision='same',
        margin = dict( r=20, t=0, l=0, b=0 ),
        showlegend = False,
        scene = dict(
            xaxis = axis_template_3d( xlabel ),
            yaxis = axis_template_3d( ylabel ),
            zaxis = axis_template_3d( zlabel ),
            camera = dict(
                up=dict(x=0, y=0, z=1),
                center=dict(x=0, y=0, z=0),
                eye=dict(x=0.08, y=2.2, z=0.08)
            )
        )
    )

    if len(markers) > 0:
        data = data + add_markers( data, markers, plot_type = plot_type )

    return dict( data=data, layout = layout)


# create layout
BACKGROUND = 'rgb(230, 230, 230)'

FIGURE = scatter_plot_3d()

app.layout = html.Div(children=[

    html.H1(children='Visualization Tool', style={'color': 'midnightblue', 'font-weight': 'bold'}),

    html.Div(children=[
        html.P('''A visualization tool for viewing the generated point clouds of the hippocampus
        for healthy controls and Alzhemeirs Disease patients using two''', style={'font-style': 'italic'}),
        html.P('''dimensions z0 and z1 for the generation.''', style={'font-style': 'italic'})
    ]),

    # set up graph radio buttons and marker size option
    html.Div(children = [

        # seting up the graph
        html.Div([
            dcc.Graph(
                id='graph',
                figure = FIGURE
            )
        ], className="six columns"),

        # seting up dropdown to pick marker size
        html.Div(children = [
                html.Div(children='''Change marker size''', style={'margin-top': 20}, className='one row'),

                html.Div([
                    dcc.Dropdown(
                        id='marker-size',
                        options=[
                                {'label': '5', 'value': 5},
                                {'label': '10', 'value': 10},
                                {'label': '15', 'value': 15},
                                {'label': '20', 'value': 20},
                                {'label': '25', 'value': 25}
                            ],
                        value=15
                    )
                    ], className='four rows', style={'margin-bottom': 20, 'width':'40%'}),

                # radio item to choose between healthy subject or AD patient
                html.Div(children='''Type of subject''', style={'margin-top': 10}, className='one row'),

                html.Div([
                        dcc.RadioItems(
                            id = 'choose_healthy_non',
                            options=[
                                    { 'label': 'HC', 'value': 'HC'},
                                    { 'label': 'AD', 'value': 'AD'},
                            ],
                            value='HC'
                        )
                ], className="two rows")

        ], className='two columns')

    ], className="row"),

    # set up sliders

    html.Div(children = [

        html.Div([
            dcc.Slider(
                id='z0-continuous-slider',
                min=df['z0'].min() - 2,
                max=df['z0'].max() - 2,
                marks={i: '{}'.format(i) for i in range(-2,3)},
                value=df['z0'].mean() -2,
                step=0.1
            )
        ], style={'width': '50%'}, className="seven columns"),

        html.Div([
            html.Div(id = 'z0-value', children='''z0 = 0''', style={ 'textAlign': 'left', 'color': 'midnightblue', 'font-weight': 'bold'})
        ], className="one column")

    ], className=" one row", style={'padding': 10}),

    html.Div(children = [

        html.Div([
            dcc.Slider(
                id='z1-continuous-slider',
                min=df['z1'].min() - 2,
                max=df['z1'].max() - 2,
                marks={i: '{}'.format(i) for i in range(-2,3)},
                value=df['z1'].mean() - 2,
                step=0.1
            )
        ], style={'width': '50%'}, className="seven columns"),

        html.Div([
            html.Div(id = 'z1-value', children='''z1 = 0''', style={ 'textAlign': 'left', 'color': 'midnightblue', 'font-weight': 'bold'})
        ], className="one column")

    ], className=" one row", style={'padding': 10})

], style = {'display': 'inline-block', 'width': '100%'})


# here z0 is fixed and we need to calculate interpolation for z1 only
def calc_z1_interpolaton(df, z0, z1, sub_type):
    z1_floor = np.floor(z1)
    z1_ceil = np.ceil(z1)

    df_type = df[df['Status'] == sub_type]
    df_type = df_type[df_type['z0'] == z0]
    filtered_floor = df_type[df_type['z1'] == z1_floor]
    filtered_ceil = df_type[df_type['z1'] == z1_ceil]

    x = (z1_ceil - z1)*filtered_floor['x'].reset_index(drop=True) + (z1 - z1_floor)*filtered_ceil['x'].reset_index(drop=True)
    y = (z1_ceil - z1)*filtered_floor['y'].reset_index(drop=True) + (z1 - z1_floor)*filtered_ceil['y'].reset_index(drop=True)
    z = (z1_ceil - z1)*filtered_floor['z'].reset_index(drop=True) + (z1 - z1_floor)*filtered_ceil['z'].reset_index(drop=True)
    col = (z1_ceil - z1)*filtered_floor['color_val'].reset_index(drop=True) + (z1 - z1_floor)*filtered_ceil['color_val'].reset_index(drop=True)

    interp_df = pd.DataFrame(sub_type, index = np.arange(1024), columns=['Status'])
    interp_df['x'] = x
    interp_df['y'] = y
    interp_df['z'] = z
    interp_df['color_val'] = col

    return interp_df


# here z1 is fixed and we need to calculate interpolation for z0 only
def calc_z0_interpolaton(df, z0, z1, sub_type):
    z0_floor = np.floor(z0)
    z0_ceil = np.ceil(z0)

    df_type = df[df['Status'] == sub_type]
    df_type = df_type[df_type['z1'] == z1]
    filtered_floor = df_type[df_type['z0'] == z0_floor]
    filtered_ceil = df_type[df_type['z0'] == z0_ceil]

    x = (z0_ceil - z0)*filtered_floor['x'].reset_index(drop=True) + (z0 - z0_floor)*filtered_ceil['x'].reset_index(drop=True)
    y = (z0_ceil - z0)*filtered_floor['y'].reset_index(drop=True) + (z0 - z0_floor)*filtered_ceil['y'].reset_index(drop=True)
    z = (z0_ceil - z0)*filtered_floor['z'].reset_index(drop=True) + (z0 - z0_floor)*filtered_ceil['z'].reset_index(drop=True)
    col = (z0_ceil - z0)*filtered_floor['color_val'].reset_index(drop=True) + (z0 - z0_floor)*filtered_ceil['color_val'].reset_index(drop=True)

    interp_df = pd.DataFrame(sub_type, index = np.arange(1024), columns=['Status'])
    interp_df['x'] = x
    interp_df['y'] = y
    interp_df['z'] = z
    interp_df['color_val'] = col

    return interp_df


# here we need to do a quadratic interpolation
def calc_quad_interpolaton(df, z0, z1, sub_type):
    # calculate the ceil and floor of the given z0,z1 values
    z0_floor = np.floor(z0)
    z0_ceil = np.ceil(z0)
    z1_floor = np.floor(z1)
    z1_ceil = np.ceil(z1)

    df_type = df[df['Status'] == sub_type]
    filtered_z0 = df_type[df_type['z0'] == z0_floor]
    filtered_z1 = df_type[df_type['z0'] == z0_ceil]

    filtered_00 = filtered_z0[filtered_z0['z1'] == z1_floor]
    filtered_01 = filtered_z0[filtered_z0['z1'] == z1_ceil]
    filtered_10 = filtered_z1[filtered_z1['z1'] == z1_floor]
    filtered_11 = filtered_z1[filtered_z1['z1'] == z1_ceil]

    x1 = (z0_ceil - z0) * filtered_00['x'].reset_index(drop=True) + (z0 - z0_floor) * filtered_01['x'].reset_index(drop=True)
    x2 = (z0_ceil - z0) * filtered_10['x'].reset_index(drop=True) + (z0 - z0_floor) * filtered_11['x'].reset_index(drop=True)
    x = (z1_ceil - z1) * x1 + (z1 - z1_floor) * x2

    y1 = (z0_ceil - z0) * filtered_00['y'].reset_index(drop=True) + (z0 - z0_floor) * filtered_01['y'].reset_index(drop=True)
    y2 = (z0_ceil - z0) * filtered_10['y'].reset_index(drop=True) + (z0 - z0_floor) * filtered_11['y'].reset_index(drop=True)
    y = (z1_ceil - z1) * y1 + (z1 - z1_floor) * y2

    zz1 = (z0_ceil - z0) * filtered_00['z'].reset_index(drop=True) + (z0 - z0_floor) * filtered_01['z'].reset_index(drop=True)
    z2 = (z0_ceil - z0) * filtered_10['z'].reset_index(drop=True) + (z0 - z0_floor) * filtered_11['z'].reset_index(drop=True)
    z = (z1_ceil - z1) * zz1 + (z1 - z1_floor) * z2

    col1 = (z0_ceil - z0) * filtered_00['color_val'].reset_index(drop=True) + (z0 - z0_floor) * filtered_01['color_val'].reset_index(drop=True)
    col2 = (z0_ceil - z0) * filtered_10['color_val'].reset_index(drop=True) + (z0 - z0_floor) * filtered_11['color_val'].reset_index(drop=True)
    col = (z1_ceil - z1) * col1 + (z1 - z1_floor) * col2

    interp_df = pd.DataFrame(sub_type, index = np.arange(1024), columns=['Status'])
    interp_df['x'] = x
    interp_df['y'] = y
    interp_df['z'] = z
    interp_df['color_val'] = col

    return interp_df

# update the z0 displayed value
@app.callback(
    dash.dependencies.Output('z0-value', 'children'),
    [dash.dependencies.Input('z0-continuous-slider', 'value')])
def update_z0_value(selected_z0):
    return 'z0 = ' + str(selected_z0)

# update the z1 displayed value
@app.callback(
    dash.dependencies.Output('z1-value', 'children'),
    [dash.dependencies.Input('z1-continuous-slider', 'value')])
def update_z1_value(selected_z1):
    return 'z1 = ' + str(selected_z1)


# create callback to update graph based on user selection
@app.callback(
    dash.dependencies.Output('graph', 'figure'),
    [dash.dependencies.Input('z0-continuous-slider', 'value'),
     dash.dependencies.Input('z1-continuous-slider', 'value'),
     dash.dependencies.Input('marker-size', 'value'),
     dash.dependencies.Input('choose_healthy_non', 'value')])
def update_graph(selected_z0, selected_z1, marker_size, selected_healthy_non):

    if type(selected_z0) == int and type(selected_z1) == int:
        # get the dataframe for the given parameters z0, z1, patient or healthy subject
        filtered_df = df[df['z0'] == round((selected_z0 + 2), 2)]
        filtered_df = filtered_df[filtered_df['z1'] == round((selected_z1 + 2), 2)]
        filtered_df = filtered_df[filtered_df['Status'] == selected_healthy_non]
    elif type(selected_z0) == int:
        filtered_df = calc_z1_interpolaton(df, (selected_z0+2), round((selected_z1+2), 2), selected_healthy_non)
    elif type(selected_z1) == int:
        filtered_df = calc_z0_interpolaton(df, round((selected_z0+2), 2), (selected_z1+2), selected_healthy_non)
    else:
        # values do not exist - calculate via interpolation
        filtered_df = calc_quad_interpolaton(df, round((selected_z0+2), 2), round((selected_z1+2), 2), selected_healthy_non)

    traces = []

    for i in filtered_df: # i here is the different columns of df
        traces.append(go.Scatter3d(
            x=filtered_df['x'], # all the column x
            y=filtered_df['y'],
            z=filtered_df['z'],
            text=filtered_df['Status'],
            mode='markers',
            opacity=0.7,
            name=i,
            marker={
                'size': marker_size,
                'color': filtered_df['color_val'],         # set color according to distance from mean as calculated above,
                'colorscale': 'Cividis',
                'cmin': df['color_val'].min(),
                'cmax': df['color_val'].max(),
                'colorbar': {
                    'title': 'Distance<br>from mean'
                }
            }
        ))

    return {
        'data': traces,
        'layout': go.Layout(
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            uirevision='same',
            hovermode='closest',
            showlegend=False
        )
    }

if __name__ == '__main__':
    app.run_server(debug=False, port=8060)
