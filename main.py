import streamlit as st
from dijkstra import dijkstra
from maps_api import GoogleMapsAPI

# Configuração da API do Google Maps
API_KEY = "teste"
maps_api = GoogleMapsAPI(API_KEY)

# Interface do Streamlit
st.title("Planejador de Rotas com Dijkstra e Google Maps")
st.sidebar.header("Configurações")

# Pontos fixos para depuração
st.write("### Pontos Fixos para Depuração:")
origin = "Av. Paulista, São Paulo"
point1 = "Rua Augusta, São Paulo"
point2 = "Praça da Sé, São Paulo"
destination = "Parque Ibirapuera, São Paulo"

st.write(f"- **Origem**: {origin}")
st.write(f"- **Ponto Intermediário 1**: {point1}")
st.write(f"- **Ponto Intermediário 2**: {point2}")
st.write(f"- **Destino**: {destination}")

# Obter matriz de distâncias
points = [origin, point1, point2, destination]
response = maps_api.get_distance_matrix(points, points)

# Depuração da resposta da API
st.write("### Debug da Resposta da API:")
st.json(response)

# Construir grafo a partir da resposta
graph = {}
for i, origin in enumerate(points):
    graph[origin] = {}
    for j, destination in enumerate(points):
        try:
            element = response["rows"][i]["elements"][j]
            distance = element.get("distance", {}).get("value", float('inf'))
            graph[origin][destination] = distance
        except KeyError:
            st.error(f"Erro ao processar a distância entre {origin} e {destination}.")

# Exibir o grafo construído
st.write("### Grafo de Distâncias:")
st.json(graph)

# Calcular rota com Dijkstra
start_point = origin
end_point = destination

if end_point in graph:
    distances, visited = dijkstra(graph, start_point, end_point)
    total_distance = distances.get(end_point, float('inf'))
    st.write("### Resultado:")
    st.write(f"**Distância Total:** {total_distance} metros")
else:
    st.error("Destino não encontrado no grafo.")