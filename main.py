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

# Função para obter endereço formatado da API Geocoding
def get_address_from_api(address, api_key):
    geocode_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": address, "key": api_key}
    response = requests.get(geocode_url, params=params).json()

    if response["status"] == "OK":
        return response["results"][0]["formatted_address"]
    else:
        st.error(f"Erro ao buscar o endereço: {response['status']}")
        return None

# Função para obter grafo de distâncias
def get_distance_matrix(addresses, api_key):
    url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    params = {
        "origins": "|".join(addresses),
        "destinations": "|".join(addresses),
        "key": api_key
    }
    response = requests.post(url, params=params).json()

    if response["status"] != "OK":
        st.error("Erro ao obter a matriz de distâncias.")
        return None

    graph = {}
    for i, origin_address in enumerate(response["origin_addresses"]):
        graph[origin_address] = {}
        for j, destination_address in enumerate(response["destination_addresses"]):
            element = response["rows"][i]["elements"][j]
            distance = element.get("distance", {}).get("value", float('inf'))
            if distance != float('inf') and i != j:
                graph[origin_address][destination_address] = distance
    return graph

# Configuração da página
st.title("Calculador de Rota com Dijkstra")
st.write("Insira os endereços e encontre a rota mais curta.")

# Configurações da API
api_key = st.text_input("Insira sua chave da API do Google Maps:", type="password")

# Entradas do usuário
start_point = st.text_input("Ponto de Partida:")
intermediate_point_1 = st.text_input("Ponto Intermediário 1:")
intermediate_point_2 = st.text_input("Ponto Intermediário 2:")
end_point = st.text_input("Ponto de Chegada:")

if st.button("Calcular Rota"):
    if not all([api_key, start_point, intermediate_point_1, intermediate_point_2, end_point]):
        st.warning("Por favor, insira todos os endereços e a chave da API.")
    else:
        # Obter endereços formatados
        addresses = [
            get_address_from_api(start_point, api_key),
            get_address_from_api(intermediate_point_1, api_key),
            get_address_from_api(intermediate_point_2, api_key),
            get_address_from_api(end_point, api_key)
        ]

        if None in addresses:
            st.error("Erro ao processar os endereços. Verifique os valores inseridos.")
        else:
            # Construir o grafo com a matriz de distâncias
            graph = get_distance_matrix(addresses, api_key)
            if graph:
                # Calcular todas as rotas possíveis
                routes = list(permutations(addresses))
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
