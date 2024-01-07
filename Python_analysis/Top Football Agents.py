import matplotlib.pyplot as plt
import pymongo
import numpy as np
from collections import defaultdict

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client.football
collection = db.players

# Query Definition
query = [
    { "$match": { "agent_name": { "$ne": None } } },
    { "$group": { "_id": "$agent_name", "numberOfPlayers": { "$sum": 1 } } },
    { "$sort": { "numberOfPlayers": -1 } }
]
# Query Execution
result = collection.aggregate(query)

# Range of visualization
ranges = [(10, 14), (15, 19), (20, 29), (30, 39), (40, 49), (50, 59), (60, 69), (70, 79), (80, 89), (90, 99)]

grouped_agents = defaultdict(int)
grouped_players = defaultdict(int)
sumOfTopTen = 0 #Sum of players of top ten agents

#Agent clustering
for i,record in enumerate(result):
    players = record['numberOfPlayers']

    if i < 10: #Top Ten
        grouped_agents[record['_id']] += 1
        grouped_players[record['_id']] += players
        sumOfTopTen += players

    elif players < 10: #Few players clustering
        grouped_agents[str(players)] += 1
        grouped_players[str(players)] += players

    elif players >= 100:#Many players clustering
        grouped_agents["100+"] += 1
        grouped_players["100+"] += players

    else: #Range clustering
        for r in ranges:
            if r[0] <= players <= r[1]:
                key = f'{r[0]}-{r[1]}'
                grouped_agents[key] += 1
                grouped_players[key] += players
                break

# Histogram of number of agent per cluster
            
categories_bar = list(grouped_agents.keys())
agents_count = list(grouped_agents.values())

plt.figure(figsize=(12, 6))
plt.bar(categories_bar, agents_count, color='blue')
plt.xlabel(' Cluster Name')
plt.ylabel('Agents Number')
plt.title('Number of agents for each cluster')
plt.xticks(rotation=90)
plt.show()

#Pie chart of the percentage of players on the total for each cluster

categories_pie = list(grouped_players.keys())
total_players_pie = list(grouped_players.values())

plt.figure(figsize=(10, 10))
plt.pie(total_players_pie, labels=categories_pie, autopct='%1.1f%%', startangle=140)
plt.title('Percentage Distribution of Players by Agent Cluster')
plt.show()


# Text Output and Top Ten Analysis

summary_text = "Summary of Agent and Player Distribution:\n\n"
summary_text += "Percentage Distribution of Aget by group:\n"

summary_text += "- Top 10 : 10 Agents\n"
i=0
for range, count in grouped_agents.items():
    if(i>9):
        summary_text += f"- {range:<6} Category: {count:<5} Agents\n"
    i+=1

summary_text += "\nPercentage Distribution of player by Agent group:\n"
total_players_count = sum(grouped_players.values())
sumOfTopTenPerc= (sumOfTopTen / total_players_count) * 100
summary_text += f"- Top 10 Agents  : {sumOfTopTen:<5} Players {sumOfTopTenPerc:<6.2f}% of Total Player: \n"
i=0
for range, player_count in grouped_players.items():
    if(i>9):
        percentage = (player_count / total_players_count) * 100
        summary_text += f"- {range:<6} Category: {player_count:<5} Players {percentage:<6.2f}% of Total Player: \n"
    i+=1

summary_text += f"\n Top 10 Agents (Total: {sumOfTopTenPerc:.2f}%):\n"
i=0
for range, player_count in grouped_players.items():
    if(i<10):
        percentage = (player_count / total_players_count) * 100
        summary_text += f"- {range:<20} : {player_count:<5} Players {percentage:<6.2f}% of Total Player: \n"
    else: break
    i+=1

print(summary_text)