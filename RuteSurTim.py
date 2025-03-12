
from collections import deque
import tkinter as tk
from tkinter import ttk
import networkx as nx
import matplotlib.pyplot as plt
import heapq  # Untuk priority queue

def bfs_berbobot(graf, awal, tujuan):
    queue = [(0, awal, [awal])]  # (jarak_total, simpul, jalur)
    dikunjungi = {}

    while queue:
        jarak, simpul, jalur = heapq.heappop(queue)

        if simpul in dikunjungi and dikunjungi[simpul] <= jarak:
            continue  # Skip jika sudah ditemukan jalur lebih pendek sebelumnya
        
        dikunjungi[simpul] = jarak

        if simpul == tujuan:
            return jalur, jarak  # Kembalikan jalur dan total jarak

        for tetangga, bobot in graf.get(simpul, {}).items():
            heapq.heappush(queue, (jarak + bobot, tetangga, jalur + [tetangga]))

    return None, float('inf')  # Jika tidak ditemukan jalur


# Data graf berbasis jaringan kecamatan Surabaya
graf = {
    'Gubeng': { 'Mulyorejo': 4, 'Sukolilo': 3, 'Tambaksari': 3,'Tenggilis Mejoyo':9,},
    'Gunung Anyar': {'Rungkut': 3, 'Tenggilis Mejoyo': 2},
    'Mulyorejo': {'Gubeng': 4, 'Sukolilo': 2, 'Tambaksari': 3},
    'Rungkut': {'Gunung Anyar': 3, 'Sukolilo': 4, 'Tenggilis Mejoyo': 2},
    'Sukolilo': {'Gubeng': 3, 'Mulyorejo': 2, 'Rungkut': 4},
    'Tambaksari': { 'Gubeng':2, 'Mulyorejo': 3},
    'Tenggilis Mejoyo': {'Gunung Anyar': 2, 'Rungkut': 2,'Gubeng':5}
}
