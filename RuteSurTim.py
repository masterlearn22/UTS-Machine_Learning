
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


# Fungsi untuk menggambar graf dan rute terpendek
def gambar_graf(graf, rute_terpendek):
    G = nx.DiGraph()
    for simpul, tetangga in graf.items():
        for tujuan, jarak in tetangga.items():
            G.add_edge(simpul, tujuan, weight=jarak)
    
    posisi = {  # Posisi koordinat untuk tata letak graf
        'Gubeng': (8, 6), 'Gunung Anyar': (10, 3),
        'Mulyorejo': (10.5, 6.5),'Rungkut': (10, 4),'Sukolilo': (10, 5), 
        'Tambaksari': (8, 7), 'Tenggilis Mejoyo': (8, 4),
       
    }

