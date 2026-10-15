import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

df = pd.read_csv("historical_automobile_sales.csv")

app = Dash(__name__)

app.layout = html.Div([
    html.H1(
        "Automobile Sales Statistics Dashboard",
        style={'textAlign': 'center', 'color': '#503D36', 'fontSize': 24}
    ),

    html.Div([
        html.Label("Select Report type:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=[
                {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
                {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
            ],
            placeholder='Select a report type',
            value=None,
            style={'width': '80%', 'padding': '3px', 'fontSize': '20px'}
        )
    ]),

    html.Div([
        html.Label("Select Year:"),
        dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in range(1980, 2014)],
            placeholder='Select year',
            value=None,
            disabled=True
        )
    ]),

    html.Div(
        id='output-container',
        className='chart-grid',
        style={'display': 'flex', 'flexDirection': 'column'}
    )
])


@app.callback(
    Output('select-year', 'disabled'),
    Input('dropdown-statistics', 'value')
)
def update_input_container(selected_statistics):
    return selected_statistics != 'Yearly Statistics'


@app.callback(
    Output('output-container', 'children'),
    [
        Input('dropdown-statistics', 'value'),
        Input('select-year', 'value')
    ]
)
def update_output_container(selected_statistics, input_year):

    if selected_statistics == 'Recession Period Statistics':

        recession_data = df[df['Recession'] == 1]

        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(
                yearly_rec,
                x='Year',
                y='Automobile_Sales',
                title='Average Automobile Sales During Recession'
            )
        )

        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(
            figure=px.bar(
                average_sales,
                x='Vehicle_Type',
                y='Automobile_Sales',
                title='Average Vehicles Sold by Vehicle Type During Recession'
            )
        )

        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.pie(
                exp_rec,
                values='Advertising_Expenditure',
                names='Vehicle_Type',
                title='Advertising Expenditure Share During Recession'
            )
        )

        unemp_data = recession_data.groupby(
            ['unemployment_rate', 'Vehicle_Type']
        )['Automobile_Sales'].mean().reset_index()

        R_chart4 = dcc.Graph(
            figure=px.bar(
                unemp_data,
                x='unemployment_rate',
                y='Automobile_Sales',
                color='Vehicle_Type',
                labels={
                    'unemployment_rate': 'Unemployment Rate',
                    'Automobile_Sales': 'Average Automobile Sales'
                },
                title='Effect of Unemployment Rate on Vehicle Type and Sales'
            )
        )

        return [
            html.Div(
                children=[R_chart1, R_chart2],
                style={'display': 'flex', 'width': '100%'}
            ),
            html.Div(
                children=[R_chart3, R_chart4],
                style={'display': 'flex', 'width': '100%'}
            )
        ]

    elif selected_statistics == 'Yearly Statistics' and input_year is not None:

        yearly_data = df[df['Year'] == input_year]

        yas = df.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(
            figure=px.line(
                yas,
                x='Year',
                y='Automobile_Sales',
                title='Yearly Automobile Sales'
            )
        )

        mas = yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(
            figure=px.line(
                mas,
                x='Month',
                y='Automobile_Sales',
                title='Total Monthly Automobile Sales in {}'.format(input_year)
            )
        )

        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(
            figure=px.bar(
                avr_vdata,
                x='Vehicle_Type',
                y='Automobile_Sales',
                title='Average Vehicles Sold by Vehicle Type in {}'.format(input_year)
            )
        )

        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(
            figure=px.pie(
                exp_data,
                values='Advertising_Expenditure',
                names='Vehicle_Type',
                title='Total Advertisement Expenditure for Each Vehicle in {}'.format(input_year)
            )
        )

        return [
            html.Div(
                children=[Y_chart1, Y_chart2],
                style={'display': 'flex', 'width': '100%'}
            ),
            html.Div(
                children=[Y_chart3, Y_chart4],
                style={'display': 'flex', 'width': '100%'}
            )
        ]

    return html.Div("Select a report type to display the charts.")


if __name__ == '__main__':
    app.run(debug=True)
