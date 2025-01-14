import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc

import pandas as pd
import plotly.express as px

df=pd.read_csv('data/pollreport.csv')
df["ambito_trabajo"] = df["ambito_trabajo"].fillna("No especificado")


# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Dashboard de Estudiantes"

# Layout of the dashboard
app.layout = dbc.Container([
    html.H1("Dashboard de Estudiantes", className="text-center mt-3"),

    dbc.Row([
        dbc.Col([
            html.Label("Filtrar por Carrera:"),
            dcc.Dropdown(
                id="carrera-dropdown",
                options=[{"label": carrera, "value": carrera} for carrera in df["carrera"].unique()],
                value=df["carrera"].unique()[0],
                clearable=False
            )
        ], width=4),

        dbc.Col([
            html.Label("Filtrar por Ámbito de Trabajo:"),
            dcc.Dropdown(
                id="ambito-dropdown",
                options=[{"label": ambito, "value": ambito} for ambito in df["ambito_trabajo"].unique()],
                value=df["ambito_trabajo"].unique()[0],
                clearable=False
            )
        ], width=4),

        dbc.Col([
            html.Label("Rango de Edad:"),
            dcc.RangeSlider(
                id="edad-slider",
                min=df["Edad"].min(),
                max=df["Edad"].max(),
                step=1,
                marks={i: str(i) for i in range(df["Edad"].min(), df["Edad"].max() + 1)},
                value=[df["Edad"].min(), df["Edad"].max()]
            )
        ], width=4)
    ], className="mb-4"),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id="cursos-bar-chart")
        ], width=6),

        dbc.Col([
            dcc.Graph(id="promedio-scatter")
        ], width=6)
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id="ingresos-pie-chart")
        ], width=6),

        dbc.Col([
            dcc.Graph(id="modo-transporte-bar")
        ], width=6)
    ])
])


# Callback to update graphs
@app.callback(
    [
        Output("cursos-bar-chart", "figure"),
        Output("promedio-scatter", "figure"),
        Output("ingresos-pie-chart", "figure"),
        Output("modo-transporte-bar", "figure")
    ],
    [
        Input("carrera-dropdown", "value"),
        Input("ambito-dropdown", "value"),
        Input("edad-slider", "value")
    ]
)
def update_charts(selected_carrera, selected_ambito, selected_edad):
    filtered_df = df[
        (df["carrera"] == selected_carrera) &
        (df["ambito_trabajo"] == selected_ambito) &
        (df["Edad"] >= selected_edad[0]) &
        (df["Edad"] <= selected_edad[1])
        ]

    cursos_bar_chart = px.bar(
        filtered_df,
        x="cursos_aprobados",
        title="Distribución de Cursos Aprobados",
        labels={"cursos_aprobados": "Cursos Aprobados"}
    )

    promedio_scatter = px.scatter(
        filtered_df,
        x="promedio_ponderado",
        y="ingresos_despues_graduacion",
        title="Promedio vs Ingresos",
        labels={"promedio_ponderado": "Promedio Ponderado", "ingresos_despues_graduacion": "Ingresos"}
    )

    ingresos_pie_chart = px.pie(
        filtered_df,
        names="herramienta_ia_preferida",
        title="Herramientas de IA Preferidas",
        hole=0.4
    )

    modo_transporte_bar = px.bar(
        filtered_df,
        x="modo_transporte",
        title="Modo de Transporte Preferido",
        labels={"modo_transporte": "Modo de Transporte"}
    )

    return cursos_bar_chart, promedio_scatter, ingresos_pie_chart, modo_transporte_bar


if __name__ == "__main__":
    app.run_server(debug=True)