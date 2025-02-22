import heapq

def dijkstra(graph, start, end):
    # Inicialização
    queue = [(0, start)]  # Fila de prioridade: (distância acumulada, nó atual)
    distances = {node: float('inf') for node in graph}  # Distâncias iniciais infinitas
    distances[start] = 0  # Distância do ponto inicial é 0
    visited = set()

    while queue:
        current_distance, current_node = heapq.heappop(queue)

        # Ignorar nós já visitados
        if current_node in visited:
            continue

        # Marcar como visitado
        visited.add(current_node)

        # Checar os vizinhos
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(queue, (distance, neighbor))

    # Retorna a distância final
    return distances[end]
