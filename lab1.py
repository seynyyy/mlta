# =====================================================================
# ДОПОМІЖНІ ФУНКЦІЇ ДЛЯ ВИВОДУ
# =====================================================================
def print_matrix(matrix, title):
    print(f"--- {title} ---")
    for row in matrix:
        # Форматуємо для рівного відображення (вирівнювання по ширині 3 символи)
        print(" ".join(f"{val:>3}" for val in row))
    print()

def print_list(lst, title):
    print(f"--- {title} ---")
    if isinstance(lst, dict):
        for k, v in lst.items():
            print(f"Вершина {k}: {v}")
    else:
        for edge in lst:
            print(edge)
    print()

# =====================================================================
# ЧАСТИНА 2: ФУНКЦІЇ ПЕРЕТВОРЕННЯ (КОНВЕРТАЦІЇ)
# =====================================================================
# 1. За заданою матрицею суміжності побудувати матрицю інцидентності
def adj_to_inc(adj, is_directed=False):
    n = len(adj)
    inc = [[] for _ in range(n)]

    for i in range(n):
        start_j = 0 if is_directed else i
        for j in range(start_j, n):
            if adj[i][j] > 0:
                for row_idx in range(n):
                    inc[row_idx].append(0)
                col_idx = len(inc[0]) - 1

                if i == j: # Петля
                    inc[i][col_idx] = 2
                else:
                    if is_directed:
                        inc[i][col_idx] = 1   # Виходить
                        inc[j][col_idx] = -1  # Входить
                    else:
                        inc[i][col_idx] = 1
                        inc[j][col_idx] = 1
    return inc

# 2. За заданою матрицею інцидентності побудувати список ребер
def inc_to_edge(inc, is_directed=False):
    edges = []
    if not inc or not inc[0]: return edges
    n_vertices = len(inc)
    n_edges = len(inc[0])

    for e in range(n_edges):
        u, v = -1, -1
        for i in range(n_vertices):
            if inc[i][e] == 2:
                u, v = i, i
                break
            elif inc[i][e] == 1:
                if is_directed:
                    u = i
                else:
                    if u == -1: u = i
                    else: v = i
            elif inc[i][e] == -1 and is_directed:
                v = i
        edges.append((u, v))
    return edges

# 3. За заданою матрицею суміжності побудувати список суміжності
def adj_to_adj_list(adj):
    adj_list = {}
    for i in range(len(adj)):
        adj_list[i] = []
        for j in range(len(adj[i])):
            if adj[i][j] > 0:
                adj_list[i].append(j)
    return adj_list

# 4. За заданою матрицею інцидентності побудувати матрицю суміжності
def inc_to_adj(inc, is_directed=False):
    n = len(inc)
    adj = [[0] * n for _ in range(n)]
    if not inc or not inc[0]: return adj
    n_edges = len(inc[0])

    for e in range(n_edges):
        u, v = -1, -1
        for i in range(n):
            if inc[i][e] == 2:
                u, v = i, i
                break
            elif inc[i][e] == 1:
                if is_directed: u = i
                else:
                    if u == -1: u = i
                    else: v = i
            elif inc[i][e] == -1 and is_directed:
                v = i

        if u != -1 and v != -1:
            adj[u][v] = 1
            if not is_directed and u != v:
                adj[v][u] = 1
    return adj

# 5. За заданою матрицею суміжності побудувати список ребер
def adj_to_edge(adj, is_directed=False):
    edges = []
    n = len(adj)
    for i in range(n):
        start_j = 0 if is_directed else i
        for j in range(start_j, n):
            if adj[i][j] > 0:
                edges.append((i, j))
    return edges

# 6. За заданою матрицею інцидентності побудувати список суміжності
def inc_to_adj_list(inc, is_directed=False):
    n = len(inc)
    adj_list = {i: [] for i in range(n)}
    if not inc or not inc[0]: return adj_list
    n_edges = len(inc[0])

    for e in range(n_edges):
        u, v = -1, -1
        for i in range(n):
            if inc[i][e] == 2:
                u, v = i, i
                break
            elif inc[i][e] == 1:
                if is_directed: u = i
                else:
                    if u == -1: u = i
                    else: v = i
            elif inc[i][e] == -1 and is_directed:
                v = i

        if u != -1 and v != -1:
            adj_list[u].append(v)
            if not is_directed and u != v:
                adj_list[v].append(u)
    return adj_list

# =====================================================================
# ФУНКЦІЯ ДЛЯ ЗАПУСКУ ВСІХ ЗАВДАНЬ ДЛЯ ОДНОГО ГРАФА
# =====================================================================
def run_all_tasks(current_adj, current_inc, is_directed, graph_name):
    print(f"\n{'='*60}")
    print(f"ТЕСТУВАННЯ: {graph_name.upper()}")
    print(f"{'='*60}\n")

    print("=== ЗАВДАННЯ 1: ПРЕДСТАВЛЕННЯ ГРАФА ===\n")
    print_matrix(current_adj, "а) Матриця суміжності (задана)")
    print_matrix(current_inc, "б) Матриця інцидентності (задана)")

    edges_repr = adj_to_edge(current_adj, is_directed)
    print_list(edges_repr, "в) Список ребер (згенерований)")

    adj_list_repr = adj_to_adj_list(current_adj)
    print_list(adj_list_repr, "г) Список суміжності (згенерований)")

    print("\n=== ЗАВДАННЯ 2: ПЕРЕВІРКА КОНВЕРТАЦІЙ ===\n")

    # 2.1 Матриця суміжності -> Матриця інцидентності
    t1 = adj_to_inc(current_adj, is_directed)
    print_matrix(t1, "Матр. суміжності -> Матр. інцидентності")

    # 2.2 Матриця інцидентності -> Список ребер (ВИКОРИСТОВУЄТЬСЯ ЗАДАНА)
    t2 = inc_to_edge(current_inc, is_directed)
    print_list(t2, "Матр. інцидентності (задана) -> Список ребер")

    # 2.3 Матриця суміжності -> Список суміжності
    t3 = adj_to_adj_list(current_adj)
    print_list(t3, "Матр. суміжності -> Список суміжності")

    # 2.4 Матриця інцидентності -> Матриця суміжності (ВИКОРИСТОВУЄТЬСЯ ЗАДАНА)
    t4 = inc_to_adj(current_inc, is_directed)
    print_matrix(t4, "Матр. інцидентності (задана) -> Матриця суміжності")

    # 2.5 Матриця суміжності -> Список ребер
    t5 = adj_to_edge(current_adj, is_directed)
    print_list(t5, "Матр. суміжності -> Список ребер")

    # 2.6 Матриця інцидентності -> Список суміжності (ВИКОРИСТОВУЄТЬСЯ ЗАДАНА)
    t6 = inc_to_adj_list(current_inc, is_directed)
    print_list(t6, "Матр. інцидентності (задана) -> Список суміжності")

# =====================================================================
# ГОЛОВНИЙ БЛОК: СТВОРЕННЯ МАТРИЦЬ ТА ТЕСТУВАННЯ
# =====================================================================
if __name__ == "__main__":
    # --- ЗАВЧАСНО ЗАДАНІ МАТРИЦІ ---

    # 1. Неорієнтований граф
    undirected_adj = [
        [0, 1, 1, 0, 1, 0],
        [1, 0, 0, 1, 1, 0],
        [1, 0, 1, 1, 0, 1],
        [0, 1, 1, 1, 0, 1],
        [1, 1, 0, 0, 0, 0],
        [0, 0, 1, 1, 0, 0]
    ]
    undirected_inc = [
        [1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 1, 1, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 1, 1, 0, 2, 0],
        [0, 0, 0, 1, 0, 1, 0, 1, 0, 2],
        [0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 1, 0, 0]
    ]

    # 2. Орієнтований граф
    directed_adj = [
        [1, 0, 0, 0, 0, 1],
        [1, 1, 0, 1, 0, 1],
        [1, 0, 0, 1, 1, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0]
    ]
    directed_inc = [
        [ 2,  1, -1,  0,  0,  0, -1,  0,  0,  0],
        [ 0,  0,  1,  2,  1,  1,  0,  0,  0,  0],
        [ 0,  0,  0,  0,  0,  0,  1,  1,  1,  0],
        [ 0,  0,  0,  0, -1,  0,  0, -1,  0,  1],
        [ 0,  0,  0,  0,  0,  0,  0,  0, -1, -1],
        [ 0, -1,  0,  0,  0, -1,  0,  0,  0,  0]
    ]

    # Запускаємо перевірки послідовно
    run_all_tasks(undirected_adj, undirected_inc, is_directed=False, graph_name="Неорієнтований граф")
    run_all_tasks(directed_adj, directed_inc, is_directed=True, graph_name="Орієнтований граф")
