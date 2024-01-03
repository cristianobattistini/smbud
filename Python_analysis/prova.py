"""
python -m venv myenv                                                                                                                               
source myenv/bin/activate
pip install pymongo matplotlib
"""

import pymongo
import matplotlib.pyplot as plt

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
db = myclient.football
collection = db.players

# Definisci la query di aggregazione
query = [
    { "$match": { "agent_name": { "$ne": None } } },
    { "$group": { "_id": "$agent_name", "numberOfPlayers": { "$sum": 1 } } },
    { "$sort": { "numberOfPlayers": -1 } }
]
"""
result = collection.aggregate(query)

# Stampa i risultati
for i in range(10):
    try:
        document = next(result)
        print(document)
    except StopIteration:
        print("Nessun documento trovato.")

print(type(result))
"""

# Esegui la query
result = collection.aggregate(query)

# Prepara i dati per il grafico
agent_names = []
player_counts = []
for i in range (20):
    record = next(result)
    agent_names.append(record['_id'])
    player_counts.append(record['numberOfPlayers'])

# Creazione del grafico a barre
plt.figure(figsize=(10, 6))
plt.bar(agent_names, player_counts, color='blue')
plt.xlabel('Nome Agente')
plt.ylabel('Numero di Giocatori')
plt.title('Numero di Giocatori per Agente')
plt.xticks(rotation=45)
plt.show()