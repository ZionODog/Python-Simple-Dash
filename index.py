import dash
import os
from app import *
from dash import html, dcc, Input, Output, State
from dash_bootstrap_templates import ThemeSwitchAIO
from modules.datamanager import DataManager
from modules.graphs import create_bar_chart, create_donut_chart

# Configuração do caminho do arquivo de dados
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data', 'us-population-2010-2019-reshaped.csv')

# Inicialização do DataManager
file_path = os.path.join(DATA_DIR)
dm = DataManager(file_path)
dm.load_data()

# Extração para o Dropdown
available_years = sorted(dm.data['year'].dt.year.unique())

# # Temas para o ThemeSwitchAIO
# url_theme1 = dbc.themes.FLATLY
# url_theme2 = dbc.themes.DARKLY

# Definição do layout do dashboard
tab_card = {'height': '100%'} # Garantir que o card ocupe toda a altura disponível
config_graph = {"displayModeBar": False, "showTips": False} # Configurações para o gráfico (remover barra de ferramentas e dicas)
app.layout = dbc.Container(children=[
    # Linha de Cabeçalho
    dbc.Row([
        dbc.Col([
            html.H1("US Population", className="text-dark mt-4 mb-3 fw-bold"),
            html.Hr()
        ], width=12)
    ]),

    # Linha de Filtros e KPIs Rápidos
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6("Filtros", className="card-subtitle text-muted"),
                    html.Label("Selecione o Ano:", className="mt-2"),
                    dcc.Dropdown(id='year-dropdown', options=[{'label': str(year), 'value': year} for year in available_years], value=available_years[0]) # Seu dropdown aqui
                ])
            ], className="shadow-sm mb-4")
        ], width=3),

        # KPI 1: População Total
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Span("População Total", className="text-muted small"),
                    html.H3(id="kpi-total-pop", className="text-primary fw-bold"),
                    html.I(className="fa fa-users text-light-gray position-absolute end-0 top-0 m-3 opacity-25", style={"font-size": "2rem"})
                ])
            ], className="shadow-sm border-0 border-start border-primary border-4")
        ], sm=12, md=3),

        # KPI 2: Média por Estado
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Span("Média por Estado", className="text-muted small"),
                    html.H3(id="kpi-avg-pop", className="text-success fw-bold"),
                    html.I(className="fa fa-chart-line text-light-gray position-absolute end-0 top-0 m-3 opacity-25", style={"font-size": "2rem"})
                ])
            ], className="shadow-sm border-0 border-start border-success border-4")
        ], sm=12, md=3) 
    ], className="g-2 my-3"),

    # Linha do Gráfico
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(id='graph-barras-pop', config=config_graph)
                        ], sm=12, md=7),
                        dbc.Col([
                            dcc.Graph(id='graph-pizza', className='dbc', config=config_graph)
                        ], sm=12, lg=5)
                    ])   
                ])
            ], className="shadow-sm")
        ], width=12)
    ], className="g-2 my-3")
    
], fluid=True, className="bg-light pb-5")


# Callback para atualizar o gráfico com base no ano selecionado e tema
@app.callback(
    [
        Output("kpi-total-pop", "children"),
        Output("kpi-avg-pop", "children"),
        Output("graph-barras-pop", "figure"), 
        Output("graph-pizza", "figure"), 
    ],
    [
        Input("year-dropdown", "value"),
        # Input(ThemeSwitchAIO.ids.switch("theme"), "value") # Comentado até você reativar o Switch
    ]
)
def update_all_components(selected_year):
    # Tratamento de segurança
    if selected_year is None:
        selected_year = available_years[0]

    # Cálculo dos Dados para os KPIs
    stats = dm.get_stats(year=selected_year)
    
    # Formatação
    if stats:
        total_pop = f"{stats['total_population']:.2f} M"
        avg_pop = f"{stats['average_population']:.2f} M"
    else:
        total_pop, avg_pop = "N/A", "N/A"

    # Preparação do Gráfico (Para o próximo passo)
    df_filtered = dm.filter_data(year=selected_year)
    fig = create_bar_chart(df_filtered, selected_year)
    fig_pizza = create_donut_chart(df_filtered, selected_year)

    return total_pop, avg_pop, fig, fig_pizza


if __name__ == '__main__':
    app.run(debug=False)