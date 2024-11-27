import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import numpy as np
from scipy import integrate

app = dash.Dash(__name__)

app.index_string = """
<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Calculadora MRUV</title>

    <link href="https://cdn.jsdelivr.net/npm/daisyui@4.12.14/dist/full.min.css" rel="stylesheet" type="text/css" />
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="min-h-screen bg-slate-50">
    {%app_entry%}
    <footer>
        {%config%}
        {%scripts%}
        {%renderer%}
    </footer>
</body>
</html>
"""

# Layout da aplicação
app.layout = html.Div(
    className='min-h-screen flex flex-col items-center justify-center p-8 bg-slate-50',
    children=[
        html.Div(
            className='flex flex-col gap-4 w-full max-w-4xl bg-red-200 rounded-lg p-4 shadow-2xl',
            children=[
                html.H1(
                    'Calculadora de Movimento Retilíneo Uniformemente Variado (MRUV)',
                    className='text-lg font-bold',
                ),
                html.Div(
                    className='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-2',
                    children=[
                        html.Label(
                            children=[
                                html.Span(['S', html.Sub('0')]),
                                dcc.Input(
                                    id='s0',
                                    type='number',
                                    value=0,
                                    className='grow',
                                ),
                            ],
                            className='input input-bordered flex items-center gap-2',
                        ),
                        html.Label(
                            children=[
                                html.Span(['V', html.Sub('0')]),
                                dcc.Input(
                                    id='v0',
                                    type='number',
                                    value=0,
                                    className='grow',
                                ),
                            ],
                            className='input input-bordered flex items-center gap-2',
                        ),
                        html.Label(
                            children=[
                                html.Span('a'),
                                dcc.Input(
                                    id='a',
                                    type='number',
                                    value=2,
                                    className='grow',
                                ),
                            ],
                            className='input input-bordered flex items-center gap-2',
                        ),
                        html.Label(
                            children=[
                                html.Span(['t', html.Sub('0')]),
                                dcc.Input(
                                    id='t0',
                                    type='number',
                                    value=0,
                                    className='grow',
                                ),
                            ],
                            className='input input-bordered flex items-center gap-2',
                        ),
                        html.Label(
                            children=[
                                html.Span('t'),
                                dcc.Input(
                                    id='t',
                                    type='number',
                                    value=20,
                                    className='grow',
                                ),
                            ],
                            className='input input-bordered flex items-center gap-2',
                        ),
                    ],
                ),
                # Botão de cálculo
                html.Button(
                    'Calcular',
                    id='calculate-button',
                    n_clicks=0,
                    className='btn bg-red-400 border-red-500 w-full text-lg font-bold',
                ),
                # Gráficos
                dcc.Graph(id='velocity-graph'),
                dcc.Graph(id='total-space-graph'),
                dcc.Graph(id='space-graph'),
            ],
        )
    ],
)

# Callback para calcular e atualizar os gráficos
@app.callback(
    [
        Output('velocity-graph', 'figure'),
        Output('total-space-graph', 'figure'),
        Output('space-graph', 'figure'),
    ],
    [
        Input('s0', 'value'),
        Input('v0', 'value'),
        Input('a', 'value'),
        Input('t0', 'value'),
        Input('t', 'value'),
    ],
)
def update_graphs(s0, v0, a, t0, t):
    if None in {s0, v0, a, t0, t}:
        return {}, {}, {}

    time_points = np.linspace(t0, t, 10_000)
    velocity_points = [v0 + a * time for time in time_points]
    space_points = s0 + v0 * time_points + (a / 2) * time_points ** 2
    total_space_points = integrate.cumulative_trapezoid(
        velocity_points, time_points
    )

    velocity_fig = go.Figure(
        data=[
            go.Scatter(
                x=time_points,
                y=velocity_points,
                mode='lines',
                name='Velocidade',
            )
        ],
        layout=go.Layout(
            title='Velocidade x Tempo',
            xaxis=dict(title='Tempo (s)'),
            yaxis=dict(title='Velocidade (m/s)'),
        ),
    )

    # Gráfico de Espaço Total Percorrido
    total_space_fig = go.Figure(
        data=[
            go.Scatter(
                x=time_points,
                y=total_space_points,
                mode='lines',
                name='Espaço Total Percorrido',
            )
        ],
        layout=go.Layout(
            title='Espaço Total Percorrido x Tempo',
            xaxis=dict(title='Tempo (s)'),
            yaxis=dict(title='Espaço Total (m)'),
        ),
    )

    # Gráfico de Espaço
    space_fig = go.Figure(
        data=[
            go.Scatter(
                x=time_points,
                y=space_points,
                mode='lines',
                name='Espaço',
            )
        ],
        layout=go.Layout(
            title='Espaço x Tempo',
            xaxis=dict(title='Tempo (s)'),
            yaxis=dict(title='Espaço (m)'),
        ),
    )

    return velocity_fig, total_space_fig, space_fig


if __name__ == '__main__':
    app.run_server(debug=True)
