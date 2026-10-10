from collections import deque

def dfs_traversal(adj_list, start_node=None):
    visited = set()
    order = []
    protocol = []
    stack = []
    dfs_counter = 1

    nodes = sorted(list(adj_list.keys()))
    start_nodes = [start_node] + [n for n in nodes if n != start_node] if start_node else nodes

    for root in start_nodes:
        if root not in visited:
            stack.append(root)
            visited.add(root)
            order.append(root)
            protocol.append((root, dfs_counter, list(stack), f"Старт/перехід на {root}"))
            dfs_counter += 1

            while stack:
                curr = stack[-1]
                neighbors = sorted([n for n in adj_list.get(curr, []) if n != curr])
                unvisited_found = False

                for nxt in neighbors:
                    if nxt not in visited:
                        visited.add(nxt)
                        order.append(nxt)
                        stack.append(nxt)
                        protocol.append((nxt, dfs_counter, list(stack), f"Ребро дерева ({curr} -> {nxt})"))
                        dfs_counter += 1
                        unvisited_found = True
                        break

                if not unvisited_found:
                    popped = stack.pop()
                    protocol.append(("-", "-", list(stack), f"Повернення з {popped}"))

    return order, protocol


def bfs_traversal(adj_list, start_node=None):
    visited = set()
    order = []
    protocol = []
    queue = deque()
    bfs_counter = 1

    nodes = sorted(list(adj_list.keys()))
    start_nodes = [start_node] + [n for n in nodes if n != start_node] if start_node else nodes

    for root in start_nodes:
        if root not in visited:
            visited.add(root)
            queue.append(root)
            order.append(root)
            protocol.append((root, bfs_counter, list(queue), f"Старт з {root}"))
            bfs_counter += 1

            while queue:
                curr = queue.popleft()
                protocol.append(("-", "-", list(queue), f"Обробка вершини {curr}"))
                neighbors = sorted([n for n in adj_list.get(curr, []) if n != curr])

                for nxt in neighbors:
                    if nxt not in visited:
                        visited.add(nxt)
                        queue.append(nxt)
                        order.append(nxt)
                        protocol.append((nxt, bfs_counter, list(queue), f"Додано {nxt}"))
                        bfs_counter += 1

    return order, protocol


def print_protocol(name, protocol):
    print(f"\n--- {name} ПРОТОКОЛ ---")
    print(f"{'Вершина':<10} | {'Номер':<6} | {'Стек / Черга':<25} | {'Подія'}")
    print("-" * 65)
    for v, num, state, desc in protocol:
        state_str = str(state)
        print(f"{str(v):<10} | {str(num):<6} | {state_str:<25} | {desc}")


if __name__ == "__main__":
    # 1. Неорієнтований граф (Варіант 1)
    undirected_graph = {
        'a': ['b', 'c', 'e'],
        'b': ['a', 'd', 'e'],
        'c': ['a', 'c', 'd', 'f'],
        'd': ['b', 'c', 'd', 'f'],
        'e': ['a', 'b'],
        'f': ['c', 'd']
    }

    print("================== НЕОРІЄНТОВАНИЙ ГРАФ ==================")
    dfs_order, dfs_proto = dfs_traversal(undirected_graph, start_node='a')
    print("DFS порядок:", " -> ".join(dfs_order))
    print_protocol("DFS", dfs_proto)

    bfs_order, bfs_proto = bfs_traversal(undirected_graph, start_node='a')
    print("\nBFS порядок:", " -> ".join(bfs_order))
    print_protocol("BFS", bfs_proto)

    # 2. Орієнтований граф (Варіант 1)
    directed_graph = {
        'a': ['a', 'f'],
        'b': ['a', 'b', 'd', 'f'],
        'c': ['a', 'd', 'e'],
        'd': ['e'],
        'e': [],
        'f': []
    }

    print("\n=================== ОРІЄНТОВАНИЙ ГРАФ ===================")
    dir_dfs_order, dir_dfs_proto = dfs_traversal(directed_graph, start_node='a')
    print("DFS порядок:", " -> ".join(dir_dfs_order))
    print_protocol("DFS", dir_dfs_proto)

    dir_bfs_order, dir_bfs_proto = bfs_traversal(directed_graph, start_node='a')
    print("\nBFS порядок:", " -> ".join(dir_bfs_order))
    print_protocol("BFS", dir_bfs_proto)