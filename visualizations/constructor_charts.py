import plotly.express as px
from sklearn.cluster import KMeans

# 1. Average Driver Points by Constructor
def plot_avg_driver_points(df):
    grouped = df.groupby(['constructor_name', 'driver_name'])['points'].mean().reset_index()
    top_pairs = grouped.sort_values('points', ascending=False).head(20)
    fig = px.bar(
        top_pairs,
        x='points',
        y='driver_name',
        color='constructor_name',
        orientation='h',
        title='Top 20 Constructor–Driver Pairings (Avg Points per Race)',
        labels={'points': 'Avg Points'},
        hover_data=['constructor_name']
    )
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    return fig

# 2. Total Points by Constructor–Driver Pair
def plot_total_pair_points(df):
    pair_points = df.groupby(['constructor_name', 'driver_name'])['points'].sum().reset_index()
    top_pairings = pair_points.sort_values('points', ascending=False).head(20)
    fig = px.bar(
        top_pairings,
        x='points',
        y='driver_name',
        color='constructor_name',
        orientation='h',
        title='Top 20 Constructor–Driver Pairings by Total Points',
        labels={'points': 'Total Points'}
    )
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    return fig

# 3. Constructor Win Rate Over Seasons
def plot_win_rate_by_year(df):
    win_rate = df.groupby(['year', 'constructor_name'])['win'].mean().reset_index()
    fig = px.line(
        win_rate,
        x='year',
        y='win',
        color='constructor_name',
        title='Constructor Win Rate per Season',
        labels={'win': 'Win Rate'}
    )
    return fig

# 4. Average DNF Rate by Constructor
def plot_dnf_rate(df):
    dnf_rate = df.groupby('constructor_name')['dnf_flag'].mean().reset_index().sort_values('dnf_flag', ascending=False)
    fig = px.bar(
        dnf_rate,
        x='constructor_name',
        y='dnf_flag',
        title='Average DNF Rate by Constructor',
        labels={'dnf_flag': 'DNF Rate'}
    )
    fig.update_layout(xaxis={'categoryorder': 'total descending'})
    return fig

# 5. Average Constructor Points Per Season
def plot_team_points_by_season(df):
    avg_team_pts = df.groupby(['year', 'constructor_name'])['points'].mean().reset_index()
    fig = px.line(
        avg_team_pts,
        x='year',
        y='points',
        color='constructor_name',
        title='Average Constructor Points per Season',
        labels={'points': 'Avg Points'}
    )
    return fig

# 6. K-Means Clustering of Constructors
def plot_constructor_tiers(df):
    cluster_df = df.groupby('constructor_name')[['points', 'win']].mean().reset_index()
    cluster_data = cluster_df[['points', 'win']]
    kmeans = KMeans(n_clusters=3, random_state=42)
    cluster_df['tier'] = kmeans.fit_predict(cluster_data)
    fig = px.scatter(
        cluster_df,
        x='points',
        y='win',
        color='tier',
        hover_name='constructor_name',
        title='Constructor Performance Tiers (Clustered)',
        labels={'points': 'Avg Points', 'win': 'Win Rate'}
    )
    return fig

# 7. Best Driver–Team Pairings by Total Points
def plot_best_driver_team_pairings(df):
    pair_points = df.groupby(['driver_name', 'constructor_name'])['points'].sum().reset_index()
    top_pairings = pair_points.sort_values('points', ascending=False).head(15)
    fig = px.bar(
        top_pairings,
        x='points',
        y='driver_name',
        color='constructor_name',
        orientation='h',
        title='Best Driver–Team Pairings by Total Points',
        labels={'points': 'Total Points'}
    )
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    return fig
