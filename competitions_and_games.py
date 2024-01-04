import pandas as pd

currentPath ="Old_DB/"
# Load the datasets
competitions_df = pd.read_csv(currentPath+'competitions')
competition_games_df = pd.read_csv(currentPath+'games')
game_events_df = pd.read_csv(currentPath+'game_events')

# Define the columns to keep for competitions and games
competitions_columns = ["competition_id", "name", "sub_type", "type", "country_id", "country_name", "domestic_league_code", "confederation"]
games_columns = ["game_id", "competition_id", "season", "round", "date", "home_club_id", "away_club_id", "home_club_goals", "away_club_goals", "home_club_position", "away_club_position", "home_club_manager_name", "away_club_manager_name", "stadium", "attendance", "referee", "home_club_name", "away_club_name", "aggregate"]

# Raggruppa game_events_df per 'game_id' e trasforma in una lista di dizionari e rimuove il game_id e dal club_id

events_grouped = game_events_df.groupby('game_id').apply(lambda x: x.drop(columns=['game_id']).to_dict('records')).reset_index(name='events')

# Unisci club_games_df con events_grouped creando i subdocuments
competition_games_with_events_df = pd.merge(competition_games_df, events_grouped, on='game_id', how='left')

# Seleziona solo le colonne desiderate
competitions_df = competitions_df[competitions_columns]
competition_games_df = competition_games_df[games_columns]

# Raggruppa e trasforma game_events_df in una lista di dizionari, rimuovendo 'game_id'
events_grouped = game_events_df.groupby('game_id').apply(lambda x: x.drop(columns=['game_id']).to_dict('records')).reset_index(name='events')

# Unisci competition_games_df con events_grouped
competition_games_with_events_df = pd.merge(competition_games_df, events_grouped, on='game_id', how='left')

# Raggruppa per 'competition_id' mantenendo 'competition_id' nei giochi
competition_games_grouped = competition_games_with_events_df.groupby('competition_id').apply(lambda x: x.drop(columns=['competition_id']).to_dict('records')).reset_index(name='games')

# Unisci competitions_df con competition_games_grouped
competitions_with_games_df = pd.merge(competitions_df, competition_games_grouped, on='competition_id', how='left')

# Esporta il DataFrame unificato in JSON
competitions_with_games_df.to_json('DB_gen/competitions_with_games_and_events.json', orient='records', lines=True)

