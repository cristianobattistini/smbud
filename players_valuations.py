import pandas as pd

# Carica i dataset
players_df = pd.read_csv('players')
player_valuations_df = pd.read_csv('player_valuations')

# Pre-elaborazione dei DataFrame
valuations_grouped = player_valuations_df.groupby('player_id').apply(lambda x: x.to_dict('records')).reset_index(name='valuations')


# Unisci players_df con valuations_grouped e appearances_grouped
merged_df = pd.merge(players_df, valuations_grouped, on='player_id', how='left')

# Esporta in JSON senza colonne duplicate
merged_df.to_json('players_valuations', orient='records', lines=True)
