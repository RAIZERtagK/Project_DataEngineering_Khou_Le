import json
import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objs as go
import plotly.express as px

with open('data.json', 'r') as file:
    data = json.load(file)



# Graph Gain ---------------------------------------------------
equipes = [team['Equipe'] for team in data]
gains = [int(team['Gain'].replace(" ", "")) for team in data]

# Triez les données par ordre croissant de gains
equipes_gains_sorted, gains_sorted = zip(*sorted(zip(equipes, gains), key=lambda x: x[1]))

# Créer l'histogramme avec Plotly en utilisant les données triées
fig_gains = px.bar(x=equipes_gains_sorted, y=gains_sorted, labels={'x': 'Équipes', 'y': 'Gains'},
                   title='Histogramme des Gains par Équipe')



# Graph réussites/échecs ---------------------------------------------------
reussites = []
echecs = []
for team in data:
    toutes_reussites = sum([categorie.count("Reussite") for categorie in team['Reussites'].values()])
    tous_echecs = sum([categorie.count("Echec") for categorie in team['Reussites'].values()])
    reussites.append(toutes_reussites)
    echecs.append(tous_echecs)

# Créer le graphique des réussites/échecs avec Plotly
fig_reussites_echecs = go.Figure(data=[
    go.Bar(name='Réussites', x=equipes, y=reussites),
    go.Bar(name='Échecs', x=equipes, y=echecs)
])
fig_reussites_echecs.update_layout(barmode='group', title='Réussites et Échecs par Équipe')



# Graph Moy Réussite ---------------------------------------------------
data_triage = data.copy()

# Triez la nouvelle variable par ordre croissant de réussite moyenne
data_triage.sort(key=lambda team: sum(len(reussites) for reussites in team['Reussites'].values()) / len(team['Reussites']))

fig_avg_successes = px.bar(
    x=[team['Equipe'] for team in data_triage],
    y=[sum(len(reussites) for reussites in team['Reussites'].values()) / len(team['Reussites']) for team in data_triage],
    labels={'x': 'Équipe', 'y': 'Nombre Moyen de Réussites'},
    title='Nombre Moyen de Réussites par Équipe'
)

# Graph Temps ---------------------------------------------------

def time_to_minutes(time_list):
    return time_list[0] * 60 + time_list[1]

# Extraction des noms des équipes et de leur temps respectif
teams = [team['Equipe'] for team in data]
times = [time_to_minutes(team['Temps']) for team in data]

# Tri des données par temps en ordre décroissant
teams_sorted, times_sorted = zip(*sorted(zip(teams, times), key=lambda x: x[1], reverse=True))

# Création d'un graphique en barres avec Plotly
fig_time = px.bar(x=teams_sorted, y=times_sorted, labels={'x': 'Équipes', 'y': 'Temps Total (seconde)'},
                  title="Temps Total (en seconde) par Équipe dans l'épreuve final")


# Application Dash ---------------------------------------------------

app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

couleur_principale = '#2f2f2f'
couleur_secondaire = '#404040'
couleur_texte = '#ffffff'

Tab_Style = {'backgroundColor': couleur_principale, 'color': couleur_texte}
Content_Style = {'height': '100%','backgroundColor':couleur_secondaire,'color': couleur_texte,'margin': '0','padding': '0','text-align': 'left'}
Main_Style = {'height': '100%','backgroundColor':couleur_principale,'width': '90%', 'float': 'left','margin': '0','padding': '0','color': couleur_texte,'text-align': 'center'}

# Définition du layout de l'application
app.layout = html.Div([
    # Barre de navigation à gauche avec des onglets pour sélectionner les graphiques
    html.Div([
        dcc.Tabs(id="tabs", value='tab-1', children=[
            dcc.Tab(label="Introductio", value='tab-start', style=Tab_Style),
            dcc.Tab(label="L'équipe la plus riche", value='tab-1', style=Tab_Style),
            dcc.Tab(label='Taux échecs et réussites', value='tab-2', style=Tab_Style),
            dcc.Tab(label="L'équipe la plus victorieuse", value='tab-3', style=Tab_Style),
            dcc.Tab(label="L'équipe ayant le plus de temps", value='tab-4', style=Tab_Style),
        ], vertical=True, style={'height': '100vh'}),
    ], style={'width': '10%', 'float': 'left', 'backgroundColor':couleur_principale}),

    # Contenu principal qui change en fonction de l'onglet sélectionné
    html.H3('Projet KHOU_LE : Analyse des équipes de Fort Boyard', style= Main_Style),
    html.Div(id='tabs-content', style=Main_Style),
])

@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.H3('Quelle équipe à gagner le plus?'),
            dcc.Graph(id='graph-gains', figure=fig_gains),
            html.P("Fort Boyard calcule les gains d'une équipe avec 'L'épreuve final' dans lequelle une pluie de pièce d'or tombe dans une cage. Chaques membres doit récupérer à la main les pièces qui augmente le gain final obtenue. ", style={'padding': '20px'})
        ], style=Content_Style )
    elif tab == 'tab-2':
        return html.Div([
            html.H3('Comparaison de réussites/échec de chaques équipes'),
            # Contenu pour Graph 2
            dcc.Graph(id='graph-reussites-echecs', figure=fig_reussites_echecs),
            html.P('Analyse en texte ici...', style={'padding': '20px'}),
        ],style=Content_Style )
    elif tab == 'tab-3':
        return html.Div([
            html.H3("Quelle équipe à eu le plus de réussites?"),
            # Contenu pour Graph 3
            dcc.Graph(id='graph-moy-réusite', figure=fig_avg_successes),
            html.P("En observant les données extraites sur le site, on remarque que l'équipe ayant réussit le plus d'épreuves est l'équipe ARSEP, ce qui n'est pas étonnant étant donnée qu'il y a des membres expérimentés à Fort Boyard comme Vianney avec 3 participations aux jeux, Laura BOULLEAU avec aussi 3 participations et Maeva COUCKE avec 5 participations!", style={'padding': '20px'}),
        ],style=Content_Style )
    elif tab == 'tab-4':
        return html.Div([
            html.H3("Quelle équipe a eu le plus de temps dans l'épreuve final?"),
            # Contenu pour Graph 2
            dcc.Graph(id='graph-time', figure=fig_time),
            html.P("L'épreuve final de Fort Boyard est une épreuve limité en temps, ce temps accordé aux équipes différe en fonction du nombre de bonnes réponses fournie lors de l'épreuve du conseil.", style={'padding': '20px'}),
        ],style=Content_Style )
    elif tab == 'tab-start':
        return html.Div([
            html.H3("Introduction "),
            html.P("Ce projet va analyser des données extraites du site Fort Boyard sur les équipes ayant participé pendant 2019 à 2023. ", style={'padding': '20px'}),
        ],style=Content_Style )



# Lance l'application  ---------------------------------------------------
def create_dashboard():
    return app

# Pour tester localement
# if __name__ == '__main__':
#     app.run_server(debug=True)
