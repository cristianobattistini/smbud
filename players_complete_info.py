import pandas as pd

# player_id,first_name,last_name,name,last_season,current_club_id,country_of_birth,city_of_birth,
# country_of_citizenship,date_of_birth,sub_position,position,foot,height_in_cm,market_value_in_eur,highest_market_value_in_eur,
#contract_expiration_date,agent_name,image_url,url,current_club_domestic_competition_id,current_club_name

currentPath ="Old_DB/"
# Load the datasets
players_df = pd.read_csv(currentPath+'players')
player_valuation_df = pd.read_csv(currentPath+'player_valuations')
appearances_df = pd.read_csv(currentPath+'appearances')

# Define the columns to keep for valuations and appearances
valuation_columns = ['player_id', 'last_season', 'market_value_in_eur', 'current_club_id']
appearances_columns = ['player_id', 'game_id', 'date', 'competition_id', 'yellow_cards', 'red_cards', 'goals', 'assists', 'minutes_played']

# Select the desired columns for players
players_columns = ['player_id', 'first_name', 'last_name', 'name', 'last_season', 'current_club_id', 'country_of_birth',
                   'city_of_birth', 'country_of_citizenship', 'date_of_birth', 'sub_position', 'position', 'foot',
                   'height_in_cm', 'market_value_in_eur', 'contract_expiration_date', 'agent_name', 'current_club_name']

# Select only the desired columns for players
players_df = players_df[players_columns]

# Funzione per rimuovere 'player_id' dai record
def remove_player_id(records):
    return [{k: v for k, v in record.items() if k != 'player_id'} for record in records]

# Raggruppa per 'player_id' e rimuovi 'player_id' dai record
players_df['valuations'] = players_df['player_id'].map(player_valuation_df[valuation_columns].groupby('player_id').apply(lambda x: remove_player_id(x.to_dict('records'))).to_dict())
players_df['appearances'] = players_df['player_id'].map(appearances_df[appearances_columns].groupby('player_id').apply(lambda x: remove_player_id(x.to_dict('records'))).to_dict())

# Esporta il DataFrame unificato in JSON
players_df.to_json('DB_gen/players_merged.json', orient='records', lines=True)


