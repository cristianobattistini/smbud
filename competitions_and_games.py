import pandas as pd

# Load the datasets
competitions_df = pd.read_csv('competitions')
games_df = pd.read_csv('games')
game_events_df = pd.read_csv('game_events')

# Define the columns to keep for competitions and games
competitions_columns = ["competition_id", "name", "sub_type", "type", "country_id", "country_name", "domestic_league_code", "confederation"]
games_columns = ["game_id", "competition_id", "season", "round", "date", "home_club_id", "away_club_id", "home_club_goals", "away_club_goals", "home_club_position", "away_club_position", "home_club_manager_name", "away_club_manager_name", "stadium", "attendance", "referee", "home_club_name", "away_club_name", "aggregate"]

# Raggruppa game_events_df per 'game_id' e trasforma in lista di dizionari
events_grouped = game_events_df.groupby('game_id').apply(lambda x: x.to_dict('records')).reset_index(name='events')

# Unisci games_df con events_grouped
games_with_events_df = pd.merge(games_df, events_grouped, on='game_id', how='left')

# Seleziona solo le colonne desiderate per games
games_with_events_df = games_with_events_df[games_columns]

# Raggruppa games_with_events_df per 'competition_id'
games_grouped = games_with_events_df.groupby('competition_id').apply(lambda x: x.to_dict('records')).reset_index(name='games')

# Seleziona solo le colonne desiderate per competitions
competitions_df = competitions_df[competitions_columns]

# Unisci competitions_df con games_grouped
competitions_with_games_df = pd.merge(competitions_df, games_grouped, on='competition_id', how='left')

# Esporta in JSON
competitions_with_games_df.to_json('competitions_with_games_and_events.json', orient='records', lines=True)
