import heapq

def dijkstra(graph, start, end):
    # Inicialização
    queue = [(0, start)]  # Fila de prioridade: (distância acumulada, nó atual)
    distances = {node: float('inf') for node in graph}  # Distâncias iniciais infinitas
    distances[start] = 0
    visited = {}

    while queue:
        current_distance, current_node = heapq.heappop(queue)

        # Ignorar nós já visitados
        if current_node in visited:
            continue

        # Marcar como visitado
        visited[current_node] = current_distance

        # Checar os vizinhos
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(queue, (distance, neighbor))

    return distances, visited
