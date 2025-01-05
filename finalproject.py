import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Load dataset
dataset = pd.read_csv("vijay modified project .csv")

# Ensure consistent data types for sorting
dataset['Year'] = dataset['Year'].astype(str)

# Initialize Dash app
app = dash.Dash(__name__)

# Layout of the dashboard
app.layout = html.Div([
    html.H1("Movie Dashboard", style={"text-align": "center", "color": "#00FF00", "font-family": "Verdana, sans-serif", "text-shadow": "2px 2px 4px #000000"}),

    # Dropdowns for Year and Language filters
    html.Div([
        html.Label("Select Year:", style={"font-weight": "bold", "color": "#00FF00"}),
        dcc.Dropdown(
            id="year-filter",
            options=[{"label": str(year), "value": year} for year in sorted(dataset['Year'].unique())],
            multi=True,
            placeholder="Filter by Year",
        ),
        html.Label("Select Language:", style={"font-weight": "bold", "color": "#00FF00", "margin-top": "10px"}),
        dcc.Dropdown(
            id="language-filter",
            options=[{"label": lang, "value": lang} for lang in sorted(dataset['Language'].unique())],
            multi=True,
            placeholder="Filter by Language",
        ),
        html.Label("Search Movie Name:", style={"font-weight": "bold", "color": "#00FF00", "margin-top": "10px"}),
        dcc.Input(
            id="movie-search",
            type="text",
            placeholder="Enter movie name",
            debounce=True,
        ),
    ], style={"margin-bottom": "20px", "padding": "15px", "background-color": "#000000", "border-radius": "10px", "box-shadow": "0 4px 6px rgba(0, 255, 0, 0.8)"}),

    # Graphs: Line Plot, Bar Graph, and Pie Chart
    html.Div([
        dcc.Graph(id="line-plot", style={"display": "inline-block", "width": "48%"}),
        dcc.Graph(id="bar-graph", style={"display": "inline-block", "width": "48%"}),
        dcc.Graph(id="pie-chart", style={"margin-top": "20px"}),
    ], style={"padding": "15px", "background-color": "#000000", "border-radius": "15px", "box-shadow": "0 4px 10px rgba(0, 255, 0, 0.9)"})
], style={"border": "5px solid #00FF00", "border-radius": "15px", "padding": "20px", "background": "linear-gradient(to bottom, #000000, #00FF00)"})

# Callback to update graphs based on filters
@app.callback(
    [Output("line-plot", "figure"),
     Output("bar-graph", "figure"),
     Output("pie-chart", "figure")],
    [Input("year-filter", "value"),
     Input("language-filter", "value"),
     Input("movie-search", "value")]
)
def update_graphs(selected_years, selected_languages, movie_search):
    # Filter data based on selected years and languages
    filtered_data = dataset.copy()
    if selected_years:
        filtered_data = filtered_data[filtered_data['Year'].isin(selected_years)]
    if selected_languages:
        filtered_data = filtered_data[filtered_data['Language'].isin(selected_languages)]
    if movie_search:
        filtered_data = filtered_data[filtered_data['Movie Name'].str.contains(movie_search, case=False, na=False)]

    # Line Plot: Movie Name vs Rating
    line_fig = px.line(
        filtered_data,
        x="Movie Name",
        y="Rating(10)",
        title="Movie Name vs Rating(10)",
        markers=True
    )
    # Change the line color to red
    line_fig.update_traces(line=dict(color='red'))

    # Bar Graph: Movie Name vs Timing
    bar_fig = px.bar(
        filtered_data,
        x="Movie Name",
        y="Timing(min)",
        title="Movie Name vs Timing(min)",
        barmode="group"
    )
    # Ensure all bars get unique colors by using a color scale
    bar_fig.update_traces(marker=dict(color=px.colors.qualitative.Alphabet))  # A color scale with distinct colors

    # Pie Chart: Genre Distribution
    if not filtered_data.empty:
        genre_counts = filtered_data['Genre'].value_counts().reset_index()
        genre_counts.columns = ['Genre', 'Count']
        pie_fig = px.pie(
            genre_counts,
            names="Genre",
            values="Count",
            title="Genre Distribution",
            hole=0.4
        )
    else:
        pie_fig = px.pie(
            values=[1],
            names=["No Data"],
            title="Genre Distribution (No Data Available)",
            hole=0.4
        )

    return line_fig, bar_fig, pie_fig

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True, port=8011)
