def main():
    print("Hello from hgx!")

import hypernetx as hnx
data = { 0: ('A', 'B'), 1: ('B', 'C'), 2: ('D', 'A', 'E'), 3: ('F', 'G', 'H', 'D') }
H = hnx.Hypergraph(data)
list(H.nodes)
['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
list(H.edges)
[0, 1, 2, 3]
H.shape
(8, 4)


if __name__ == "__main__":
    main()
