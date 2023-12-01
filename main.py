import dash
from dash import html
from dash.dependencies import Input, Output
import visualization
import pandas as pd

# Exemple de données
df = pd.DataFrame({
    'X': [1, 2, 3, 4, 5],
    'Y': [10, 11, 12, 13, 14]
})

# Initialiser l'application Dash
app = dash.Dash(__name__)

# Mise en page du dashboard avec l'appel à la fonction de visualisation
app.layout = visualization.layout

# Callback pour mettre à jour le contenu en fonction de la sélection
@app.callback(
    Output('home-content', 'children'),
    [Input('dropdown-chart', 'value')]
)
def update_content(selected_chart):
    if selected_chart == 'home':
        return visualization.create_page_content(
            "Bienvenue sur le Dashboard sur Fort Boyard",
            "Cette page est la page d'accueil par défaut. Vous pouvez sélectionner d'autres pages dans le menu déroulant.",
            None,
            None
        )
    elif selected_chart == 'pg1':
        return visualization.create_page_content(
            "Page 1",
            "Contenu spécifique à la page 1",
            visualization.create_scatter_plot,
            df
        )
    elif selected_chart == 'pg2':
        return visualization.create_page_content(
            "Page 2",
            "Contenu spécifique à la page 2",
            visualization.create_histogram,
            df
        )
    else:
        return []

# Exécutez l'application
if __name__ == '__main__':
    app.run_server(debug=True)
