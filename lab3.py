import math

INF = math.inf

# Матриця ваг для (вершини a, b, c, d, e, f)
# Індекси: 0:a, 1:b, 2:c, 3:d, 4:e, 5:f
C = [
    [0,   3,   INF, INF, INF, 9],
    [INF, 0,   INF, 2,   INF, 5],
    [4,   INF, 0,   12,  9,   INF],
    [INF, INF, INF, 0,   4,   INF],
    [INF, INF, INF, INF, 0,   INF],
    [INF, INF, INF, INF, INF, 0]
]

vertex_names = ['a', 'b', 'c', 'd', 'e', 'f']

def dijkstra(matrix, start_idx):
    n = len(matrix)
    dist = [matrix[start_idx][i] for i in range(n)]
    visited = {start_idx}
    paths = {i: [start_idx, i] if matrix[start_idx][i] != INF else [] for i in range(n)}
    paths[start_idx] = [start_idx]

    for _ in range(n - 1):
        # Вибір вершини з мінімальною відстанню серед невідвіданих
        min_dist = INF
        u = -1
        for i in range(n):
            if i not in visited and dist[i] < min_dist:
                min_dist = dist[i]
                u = i
                
        if u == -1:
            break
            
        visited.add(u)
        
        # Оновлення відстаней
        for v in range(n):
            if v not in visited and matrix[u][v] != INF:
                new_dist = dist[u] + matrix[u][v]
                if new_dist < dist[v]:
                    dist[v] = new_dist
                    paths[v] = paths[u] + [v]
                    
    return dist, paths

def floyd_warshall(matrix):
    n = len(matrix)
    # Створення копії матриці
    A = [[matrix[i][j] for j in range(n)] for i in range(n)]
    
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if A[i][k] + A[k][j] < A[i][j]:
                    A[i][j] = A[i][k] + A[k][j]
    return A

if __name__ == "__main__":
    print("=== 1. АЛГОРИТМ ДЕЙКСТРИ (від вершини 'a') ===")
    dist, paths = dijkstra(C, 0) # 0 відповідає вершині 'a'
    for i in range(1, len(vertex_names)):
        target = vertex_names[i]
        d = dist[i]
        if d == INF:
            print(f"до вершини {target}: шляху не існує")
        else:
            path_str = " -> ".join([vertex_names[node] for node in paths[i]])
            print(f"до вершини {target}: {path_str}, довжина шляху {d}")
            
    print("\n=== 2. АЛГОРИТМ ФЛОЙДА (найкоротші шляхи між усіма парами) ===")
    A_final = floyd_warshall(C)
    
    print("    " + "    ".join(vertex_names))
    for i in range(len(A_final)):
        row_strs = []
        for val in A_final[i]:
            row_strs.append(f"{val:<4}" if val != INF else "INF ")
        print(f"{vertex_names[i]} | " + " ".join(row_strs))