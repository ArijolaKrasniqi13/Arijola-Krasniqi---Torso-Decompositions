"""Undirected graph representation and ESA edge-list input handling."""

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


# Përfaqëson një graf të thjeshtë e të padrejtuar me kulme të numëruara nga 0.
@dataclass(frozen=True)
class Graph:
    """A simple undirected graph whose vertices are numbered 0 through n-1."""

    adjacency: tuple[frozenset[int], ...]

    # Kthen numrin e kulmeve të ruajtura në graf.
    @property
    def vertex_count(self) -> int:
        return len(self.adjacency)

    # Ndërton fqinjësinë duke ruajtur simetrinë e çdo brinje.
    @classmethod
    def from_edges(cls, edges: Iterable[tuple[int, int]], vertex_count: int | None = None) -> "Graph":
        edge_list = list(edges)
        if vertex_count is None:
            if not edge_list:
                raise ValueError("vertex_count is required for a graph without edges")
            vertex_count = max(max(u, v) for u, v in edge_list) + 1
        if vertex_count < 1:
            raise ValueError("a graph must contain at least one vertex")

        neighbors = [set() for _ in range(vertex_count)]
        for u, v in edge_list:
            if not (0 <= u < vertex_count and 0 <= v < vertex_count):
                raise ValueError(f"edge ({u}, {v}) has a vertex outside 0..{vertex_count - 1}")
            if u == v:
                raise ValueError("self-loops are not allowed in a simple graph")
            neighbors[u].add(v)
            neighbors[v].add(u)
        return cls(tuple(frozenset(row) for row in neighbors))


# Lexon çiftet e kulmeve nga skedari dhe ndërton grafikun përkatës.
def read_edge_list(path: str | Path) -> Graph:
    """Read whitespace-separated endpoint pairs, one edge per non-empty line."""
    edges: list[tuple[int, int]] = []
    largest_vertex = -1
    with Path(path).open("r", encoding="utf-8") as source:
        for line_number, line in enumerate(source, start=1):
            # Injoron rreshtat bosh dhe komentet para se të lexojë brinjën.
            content = line.split("#", 1)[0].strip()
            if not content:
                continue
            parts = content.split()
            if len(parts) != 2:
                raise ValueError(f"line {line_number}: expected exactly two vertex IDs")
            try:
                u, v = (int(part) for part in parts)
            except ValueError as error:
                raise ValueError(f"line {line_number}: vertex IDs must be integers") from error
            if u < 0 or v < 0:
                raise ValueError(f"line {line_number}: vertex IDs must be non-negative")
            edges.append((u, v))
            largest_vertex = max(largest_vertex, u, v)
    if largest_vertex < 0:
        raise ValueError("edge-list file contains no edges")
    return Graph.from_edges(edges, largest_vertex + 1)
