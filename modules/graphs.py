import plotly.express as px
import plotly.graph_objects as go

def create_bar_chart(df, year):
    # Filtrando e ordenando para pegar os 10 maiores
    df_sorted = df.sort_values(by='population', ascending=True).tail(10)
    
    fig = px.bar(
        df_sorted,
        x='population',
        y='states',
        orientation='h',
        text='population', # Exibe o valor na barra
        title=f'Top 10 Estados mais Populosos - {year}',
        template='plotly_white'
    )

    # Estilização Sênior: Limpando o visual
    fig.update_traces(
        texttemplate='%{text:.2f}M', 
        textposition='outside',
        marker_color='rgb(26, 118, 255)', # Um azul profissional
        marker_line_color='rgb(8, 48, 107)',
        marker_line_width=1.5,
        opacity=0.7
    )

    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, title=""),
        margin=dict(l=20, r=20, t=50, b=20),
    )
    
    return fig

# Gráfico de Pizza dos 10 maiores estados
def create_donut_chart(df, year):
    # Filtrando e ordenando para pegar os 10 maiores
    df_sorted = df.sort_values(by='population', ascending=False).head(5)
    
    fig = px.pie(
        df_sorted,
        values='population',
        names='states',
        title=f'Distribuição da População - {year}',
        template='plotly_white',
        hole=.5
    )

    fig.update_traces(
        textposition='inside',      # Coloca o texto dentro das fatias 
        textinfo='percent+label',  # Mostra porcentagem e nome da fatia
        marker=dict(
            # Paleta de cores sóbria e profissional
            colors=['#34495e', '#e67e22', '#1abc9c', '#c0392b', '#95a5a6', '#7f8c8d'],
            line=dict(color='#ffffff', width=2) # Linha branca separando as fatias
        )
    )

    fig.update_layout(
        margin=dict(l=10, r=10, t=50, b=10),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )

    return fig