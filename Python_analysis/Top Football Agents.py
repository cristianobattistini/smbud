"""
python -m venv myenv                                                                                                                               
source myenv/bin/activate
pip install pymongo matplotlib
"""


import matplotlib.pyplot as plt
import pymongo
import numpy as np
from collections import defaultdict
import copy

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client.football
collection = db.players

# Definisci la query di aggregazione
query = [
    { "$match": { "agent_name": { "$ne": None } } },
    { "$group": { "_id": "$agent_name", "numberOfPlayers": { "$sum": 1 } } },
    { "$sort": { "numberOfPlayers": -1 } }
]
# Esecuzione della query
result = collection.aggregate(query)
result_2 = collection.aggregate(query) #clonazione

# Estrazione dei primi 10 agenti e calcolo delle percentuali
top_10_agents = []
total_players_in_top_10 = 0
for i, record in enumerate(result_2):
    if i < 10:
        top_10_agents.append(record)
        total_players_in_top_10 += record['numberOfPlayers']
    else:
        break

# Calcolo della percentuale totale di giocatori coperta dai primi 10 agenti
total_players = collection.count_documents({})
percent_players_in_top_10 = (total_players_in_top_10 / total_players) * 100

# Creazione del testo per la percentuale di giocatori coperta dai primi 10 agenti
summary_text_top_10 = "Percentuale di giocatori coperta dai primi 10 agenti:\n"
summary_text_top_10 += f"Totale: {percent_players_in_top_10:.2f}% dei giocatori\n"

# Elencazione testuale della percentuale dei giocatori coperta da ogni agente tra i primi 10
for agent in top_10_agents:
    agent_percent = (agent['numberOfPlayers'] / total_players) * 100
    summary_text_top_10 += f"- Agente {agent['_id']}: {agent_percent:.2f}% dei giocatori, {agent['numberOfPlayers']} giocatori\n"

# Stampa del testo riassuntivo
print(summary_text_top_10)


# Definizione dei range di raggruppamento
ranges = [(10, 14), (15, 19), (20, 29), (30, 39), (40, 49), (50, 59), (60, 69), (70, 79), (80, 89), (90, 99)]
grouped_agents = defaultdict(int)
grouped_players = defaultdict(int)

# Raggruppamento degli agenti e calcolo dei giocatori per ogni range
for record in result:
    players = record['numberOfPlayers']
    if players < 10 or players > 100:
        grouped_agents[str(players)] += 1
        grouped_players[str(players)] += players
    else:
        for r in ranges:
            if r[0] <= players <= r[1]:
                key = f'{r[0]}-{r[1]}'
                grouped_agents[key] += 1
                grouped_players[key] += players
                break

# Preparazione dei dati per il grafico a barre
categories_bar = list(grouped_agents.keys())
agents_count = list(grouped_agents.values())

# Grafico a barre
plt.figure(figsize=(12, 6))
plt.bar(categories_bar, agents_count, color='blue')
plt.xlabel('Numero di Giocatori per Agente (Range)')
plt.ylabel('Numero di Agenti')
plt.title('Numero di Agenti per Range di Giocatori')
plt.xticks(rotation=90)
plt.show()

# Preparazione dei dati per il grafico a torta
categories_pie = list(grouped_players.keys())
total_players_pie = list(grouped_players.values())

# Grafico a torta
plt.figure(figsize=(10, 10))
plt.pie(total_players_pie, labels=categories_pie, autopct='%1.1f%%', startangle=140)
plt.title('Distribuzione Percentuale dei Giocatori per Categoria di Agenti')
plt.show()

# Creazione del testo riassuntivo
summary_text = "Riassunto della Distribuzione degli Agenti e dei Giocatori:\n\n"
summary_text += "Distribuzione degli Agenti per Range di Giocatori:\n"
for range, count in grouped_agents.items():
    summary_text += f"- {range} Giocatori: {count} agenti\n"

summary_text += "\nDistribuzione Percentuale dei Giocatori per Categoria di Agenti:\n"
total_players_count = sum(grouped_players.values())
for range, player_count in grouped_players.items():
    percentage = (player_count / total_players_count) * 100
    summary_text += f"- {range} Giocatori: {percentage:.2f}% dei giocatori\n"

# Stampa del testo riassuntivo
print(summary_text)