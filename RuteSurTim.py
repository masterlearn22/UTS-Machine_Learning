
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


    def koordinat():
        # Ekstrak koordinat
        x_values = [pos[0] for pos in posisi.values()]
        y_values = [pos[1] for pos in posisi.values()]

        # Plot titik-titik kecamatan
        plt.figure(figsize=(8, 6))
        plt.scatter(x_values, y_values, color='blue', marker='o')

        # Tambahkan label kecamatan di setiap titik
        for kecamatan, (x, y) in posisi.items():
            plt.text(x, y, kecamatan, fontsize=9, verticalalignment='bottom', horizontalalignment='right')

        # Label sumbu
        plt.xlabel("Koordinat X")
        plt.ylabel("Koordinat Y")
        plt.title("Visualisasi Posisi Kecamatan dalam Grafik Cartesian")

        # Tampilkan grid
        plt.grid(True)
        plt.show()
    
    koordinat()
    
    plt.figure(figsize=(12, 10))
    nx.draw(G, posisi, with_labels=True, node_color='lightblue',  node_size=2000, font_size=10)
    nx.draw_networkx_edge_labels(G, posisi, edge_labels={(u, v): d['weight'] for u, v, d in G.edges(data=True)})
    
    if rute_terpendek:
        jalur = [(rute_terpendek[i], rute_terpendek[i+1]) for i in range(len(rute_terpendek)-1)]
        nx.draw_networkx_edges(G, posisi, edgelist=jalur, edge_color='red', width=1, style='dashed')
    plt.show()

# Fungsi untuk menampilkan rute di GUI
def tampilkan_rute():
    awal = dropdown_awal.get()
    tujuan = dropdown_tujuan.get()
    if awal == tujuan:
        hasil_label.config(text="Kecamatan awal dan tujuan tidak boleh sama!")
        return
    rute, jarak = bfs_berbobot(graf, awal, tujuan)
    if rute:
        hasil_label.config(text=f"Rute tercepat: {' -> '.join(rute)}\nTotal jarak: {jarak} km")
        gambar_graf(graf, rute)
    else:
        hasil_label.config(text="Tidak ada rute yang tersedia")
        
graf = {
    'Gubeng': { 'Mulyorejo': 4, 'Sukolilo': 3, 'Tambaksari': 3,'Tenggilis Mejoyo':9,},
    'Gunung Anyar': {'Rungkut': 3, 'Tenggilis Mejoyo': 2},
    'Mulyorejo': {'Gubeng': 4, 'Sukolilo': 2, 'Tambaksari': 3},
    'Rungkut': {'Gunung Anyar': 3, 'Sukolilo': 4, 'Tenggilis Mejoyo': 2},
    'Sukolilo': {'Gubeng': 3, 'Mulyorejo': 2, 'Rungkut': 4},
    'Tambaksari': { 'Gubeng':2, 'Mulyorejo': 3},
    'Tenggilis Mejoyo': {'Gunung Anyar': 2, 'Rungkut': 2,'Gubeng':5}
   
}

# GUI dengan Tkinter
root = tk.Tk()
root.title("Visualisasi Rute BFS")
root.geometry("400x250")

# Dropdown untuk memilih kecamatan awal dan tujuan
kecamatan_list = list(graf.keys())
tk.Label(root, text="Pilih Kecamatan Awal:").pack()
dropdown_awal = ttk.Combobox(root, values=kecamatan_list)
dropdown_awal.pack()

tk.Label(root, text="Pilih Kecamatan Tujuan:").pack()
dropdown_tujuan = ttk.Combobox(root, values=kecamatan_list)
dropdown_tujuan.pack()

# Tombol untuk mencari rute
button = tk.Button(root, text="Tampilkan Rute", command=tampilkan_rute)
button.pack()

# Label untuk menampilkan hasil
hasil_label = tk.Label(root, text="")
hasil_label.pack()

root.mainloop()