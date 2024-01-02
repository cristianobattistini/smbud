import pandas as pd

# Carica i dataset
players_df = pd.read_csv('players')
appearances_df = pd.read_csv('appearances')

# Pre-elaborazione dei DataFrame
appearances_grouped = appearances_df.groupby('player_id').apply(lambda x: x.to_dict('records')).reset_index(name='appearances')


merged_df = pd.merge(players_df, appearances_grouped, on='player_id', how='left')


# Esporta in JSON senza colonne duplicate
merged_df.to_json('players_appearances.json', orient='records', lines=True)
