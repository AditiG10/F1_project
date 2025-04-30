import plotly.express as px

# 1. Average Finishing Position Per Season
def plot_avg_finish_per_season(df):
    fig = px.line(
        df,
        x='year',
        y='avg_finish_season',
        color='driver_name',
        markers=True,
        title='Average Finishing Position Per Season – Top Drivers',
        labels={'avg_finish_season': 'Avg Finish Position', 'year': 'Season'},
        hover_data=['constructor_name']
    )
    fig.update_yaxes(autorange='reversed')
    fig.update_layout(legend_title_text='Driver')
    return fig

# 2. Points Per Race

def plot_points_per_race(df):
    fig = px.scatter(
        df,
        x='year',
        y='points',
        color='driver_name',
        title='Points per Race by Season – Top Drivers',
        labels={'points': 'Race Points', 'year': 'Season'},
        hover_data=['constructor_name']
    )
    fig.update_layout(legend_title_text='Driver')
    return fig

# 3. Total Podium Count

def plot_podium_count(df):
    podium_counts = df[df['podium'] == 1].groupby('driver_name')['podium'].count().reset_index()
    podium_counts = podium_counts.sort_values('podium', ascending=False)

    fig = px.bar(
        podium_counts,
        x='driver_name',
        y='podium',
        title='Total Podium Finishes – Top Drivers',
        labels={'podium': 'Podium Count', 'driver_name': 'Driver'}
    )
    fig.update_layout(xaxis_title='Driver', yaxis_title='Number of Podiums')
    return fig

# 4. Avg Finish Position by Team
def plot_team_driver_performance(df, constructor_name):
    team_df = df[df['constructor_name'] == constructor_name]

    fig = px.line(
        team_df,
        x='year',
        y='avg_finish_season',
        color='driver_name',
        title=f'Average Finishing Position – {constructor_name} Drivers',
        labels={'avg_finish_season': 'Avg Finish Position', 'year': 'Season'}
    )
    fig.update_yaxes(autorange='reversed')
    return fig

# 5. Driver Comparison Year-by-Year
def plot_driver_comparison(df, driver1, driver2):
    compare_df = df[df['driver_name'].isin([driver1, driver2])]
    fig = px.line(
        compare_df,
        x='year',
        y='avg_finish_season',
        color='driver_name',
        markers=True,
        title=f'Avg Finish Comparison: {driver1} vs {driver2}',
        labels={'avg_finish_season': 'Avg Finish Position', 'year': 'Season'}
    )
    fig.update_yaxes(autorange='reversed')
    return fig
