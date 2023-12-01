from dash import dcc, html
import plotly.express as px

# Fonction pour créer un graphique de nuage de points
def create_scatter_plot(df):
    return px.scatter(df, x='X', y='Y', title='Nuage de points')

# Fonction pour créer un histogramme
def create_histogram(df):
    return px.histogram(df, x='Y', title='Histogramme')

# Fonction générique pour créer le contenu d'une page
def create_page_content(title, text, chart_function, df):
    content_style = {
        'backgroundColor': '#004080',  # Couleur de fond bleue légèrement plus claire
        'color': '#fff',
        'borderRadius': '10px',  # Contour arrondi
        'padding': '20px',  # Marge intérieure
        'margin': '20px'  # Marge extérieure
    }

    content = [
        html.H2(title, style={'textAlign': 'center', 'color': '#fff'}),
        html.P(text, style={'color': '#fff'})
    ]

    if chart_function:
        content.append(dcc.Graph(id='graph', figure=chart_function(df)))

    return html.Div(content, style=content_style)

# Fonction pour créer la mise en page du dashboard
def layout():
    return html.Div(
        style={'backgroundColor': '#001f3f', 'color': '#fff', 'height': '100vh', 'margin': '20px 20px 20px 20px'},
        children=[
            html.H1("Dashboard sur Fort Boyard", style={'textAlign': 'center', 'color': '#fff'}),

            # Sélection du graphique
            dcc.Dropdown(
                id='dropdown-chart',
                options=[
                    {'label': 'Accueil', 'value': 'home'},
                    {'label': 'Page 1', 'value': 'pg1'},
                    {'label': 'Page 2', 'value': 'pg2'}
                ],
                value='home',
                style={'width': '50%', 'color': '#000', 'margin': '20px auto'}
            ),

            # Contenu de la page d'accueil
            html.Div(id='home-content'),

            # Autres composants modulables peuvent être ajoutés ici
        ]
    )

# Fonction générique pour créer le contenu en fonction de la sélection du menu déroulant
def update_content(selected_chart, df):
    if selected_chart == 'home':
        return create_page_content(
            "Bienvenue sur le Dashboard sur Fort Boyard",
            "Cette page est la page d'accueil par défaut. Vous pouvez sélectionner d'autres pages dans le menu déroulant.",
            None,
            None
        )
    elif selected_chart == 'pg1':
        return create_page_content(
            "Page 1",
            "Contenu spécifique à la page 1",
            create_scatter_plot,
            df
        )
    elif selected_chart == 'pg2':
        return create_page_content(
            "Page 2",
            "Contenu spécifique à la page 2",
            create_histogram,
            df
        )
    else:
        return []
