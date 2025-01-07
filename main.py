import streamlit as st
import requests
import json
from itertools import permutations
from dijkstra import dijkstra

# Função para salvar dados em JSON
def save_to_json(data, filename):
    """Salva os dados no formato JSON."""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Função para calcular a distância total de uma rota
def calculate_total_distance(graph, route):
    total_distance = 0
    for i in range(len(route) - 1):
        origin = route[i]
        destination = route[i + 1]
        total_distance += graph[origin][destination]
    return total_distance

# Configuração da página
st.title("Algoritmo de Rota com Menor Distância")
st.write("Selecione até 3 pontos e encontre a rota mais curta.")

# Pontos fixos
addresses = [
    "Av. Paulista, São Paulo - SP, Brazil",
    "R. Augusta, São Paulo - SP, Brazil",
    "Praça da Sé, São Paulo - SP, Brazil",
    "Ibirapuera Park - Av. Pedro Álvares Cabral - Vila Mariana, São Paulo - SP, 04094-050, Brazil"
]

# Configurações da API
api_key = "AIzaSyA_SBl7x_oJ7flj6e_6lvSZA0livUPD7R4"  # Substitua pela sua chave de API do Google Maps
url = "https://maps.googleapis.com/maps/api/distancematrix/json"

params = {
    "origins": "|".join(addresses),
    "destinations": "|".join(addresses),
    "key": api_key
}

# Obter resposta da API
response = requests.post(url, params=params).json()

# Salvar resposta no arquivo response.json
save_to_json(response, "response.json")

st.write("Resposta da API salva no arquivo 'response.json'.")

# Construir grafo a partir da resposta da API
graph = {}
for i, origin_address in enumerate(response["origin_addresses"]):
    graph[origin_address] = {}
    for j, destination_address in enumerate(response["destination_addresses"]):
        element = response["rows"][i]["elements"][j]
        distance = element.get("distance", {}).get("value", float('inf'))
        if distance != float('inf') and i != j:
            graph[origin_address][destination_address] = distance

# Salvar grafo no arquivo graph.json
save_to_json(graph, "graph.json")

st.write("Grafo salvo no arquivo 'graph.json'.")

# Seleção de múltiplos pontos
selected_points = st.multiselect("Selecione até 3 pontos:", addresses, default=addresses[:2])

if len(selected_points) < 2:
    st.warning("Selecione pelo menos 2 pontos para formar uma rota.")
else:
    # Calcular todas as rotas possíveis
    routes = list(permutations(selected_points))
    shortest_route = None
    shortest_distance = float('inf')

    for route in routes:
        total_distance = calculate_total_distance(graph, route)
        if total_distance < shortest_distance:
            shortest_distance = total_distance
            shortest_route = route

    # Exibir os resultados
    st.write("### Melhor Rota:")
    st.write(" -> ".join(shortest_route))
    st.write(f"**Distância Total:** {shortest_distance} metros")
