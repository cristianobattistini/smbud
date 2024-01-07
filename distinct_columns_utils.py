import pandas as pd

# Load the players dataset
players_df = pd.read_csv('Old_DB/games')

# Get distinct values in the 'sub_position' column
#distinct_sub_positions = players_df['sub_position'].unique()

# Get distinct values in the 'position' column
description = players_df['round'].unique()

# Print distinct values
print("Distinct round:", description)
