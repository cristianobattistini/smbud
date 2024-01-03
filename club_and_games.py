import pandas as pd
# Carica i dataset

currentPath ="Old_DB/"
clubs_df = pd.read_csv(currentPath+'clubs')
club_games_df = pd.read_csv(currentPath+'club_games')
game_events_df = pd.read_csv(currentPath+'game_events')

# Define the columns to keep for clubs
clubs_columns = ["club_id", "club_code", "name", "domestic_competition_id", "total_market_value", "squad_size", "average_age", "foreigners_number", "foreigners_percentage", "national_team_players", "stadium_name", "stadium_seats", "net_transfer_record", "coach_name", "last_season"]

# Raggruppa game_events_df per 'game_id' e trasforma in una lista di dizionari e rimuove il game_id e dal club_id

events_grouped = game_events_df.groupby('game_id').apply(lambda x: x.drop(columns=['club_id', 'game_id']).to_dict('records')).reset_index(name='events')

# Unisci club_games_df con events_grouped creando i subdocuments
club_games_with_events_df = pd.merge(club_games_df, events_grouped, on='game_id', how='left')


# Seleziona solo le colonne desiderate per club
clubs_df = clubs_df[clubs_columns]

# Raggruppa club_games_with_events_df per 'club_id'e lo rimuove all'interno dei games
club_games_grouped = club_games_with_events_df.groupby('club_id').apply(lambda x: x.drop(columns=['club_id']).to_dict('records')).reset_index(name='games')

# Unisci clubs_df con club_games_grouped creando i subdocuments
clubs_with_games_df = pd.merge(clubs_df, club_games_grouped, left_on='club_id', right_on='club_id', how='left')


# Esporta il DataFrame unificato in JSON con orientamento 'records'
clubs_with_games_df.to_json('DB_gen/clubs_with_games_and_events.json', orient='records', lines=True)
