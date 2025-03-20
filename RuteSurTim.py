from collections import deque  # Mengimpor deque untuk antrian, tapi tidak digunakan di sini
import tkinter as tk  # Mengimpor tkinter untuk membuat GUI
from tkinter import ttk  # Mengimpor ttk untuk widget modern seperti Combobox
import networkx as nx  # Mengimpor networkx untuk membuat dan menggambar graf
import matplotlib.pyplot as plt  # Mengimpor matplotlib untuk visualisasi graf dan plot
import heapq  # Mengimpor heapq untuk priority queue dalam BFS berbobot

def bfs_berbobot(graf, awal, tujuan):  # Fungsi BFS berbobot untuk mencari rute terpendek
    queue = [(0, awal, [awal])]  # Inisialisasi priority queue dengan (jarak_total, simpul, jalur)
    dikunjungi = {}  # Dictionary untuk menyimpan simpul yang sudah dikunjungi dan jaraknya

    while queue:  # Looping selama queue tidak kosong
        jarak, simpul, jalur = heapq.heappop(queue)  # Ambil elemen dengan jarak terkecil dari queue
        
        if simpul in dikunjungi and dikunjungi[simpul] <= jarak:  # Cek jika simpul sudah dikunjungi dengan jarak lebih kecil
            continue  # Skip jika ada jalur lebih pendek sebelumnya
        
        dikunjungi[simpul] = jarak  # Simpan jarak terpendek ke simpul ini

        if simpul == tujuan:  # Jika simpul adalah tujuan
            return jalur, jarak  # Kembalikan jalur dan total jarak
    
        for tetangga, bobot in graf.get(simpul, {}).items():  # Iterasi tetangga dari simpul saat ini
            heapq.heappush(queue, (jarak + bobot, tetangga, jalur + [tetangga]))  # Tambah tetangga ke queue dengan jarak baru

    return None, float('inf')  # Kembalikan None dan infinity jika tidak ada jalur


def gambar_graf(graf, rute_terpendek):  # Fungsi untuk menggambar graf dan rute terpendek
    G = nx.DiGraph()  # Buat objek graf berarah dengan networkx
    for simpul, tetangga in graf.items():  # Iterasi setiap simpul dan tetangganya di graf
        for tujuan, jarak in tetangga.items():  # Iterasi tetangga dan jaraknya
            G.add_edge(simpul, tujuan, weight=jarak)  # Tambah sisi ke graf dengan bobot
    
    posisi = {  # Dictionary posisi koordinat untuk tata letak graf
        'Gubeng': (8, 6), 'Gunung Anyar': (10, 3),
        'Mulyorejo': (10.5, 6.5),'Rungkut': (10, 4),'Sukolilo': (10, 5), 
        'Tambaksari': (8, 7), 'Tenggilis Mejoyo': (8, 4),
    }

    def koordinat():  # Fungsi untuk menggambar scatter plot koordinat
        x_values = [pos[0] for pos in posisi.values()]  # Ambil nilai x dari posisi
        y_values = [pos[1] for pos in posisi.values()]  # Ambil nilai y dari posisi
        plt.figure(figsize=(8, 6))  # Buat figure baru dengan ukuran 8x6
        plt.scatter(x_values, y_values, color='blue', marker='o')  # Gambar titik koordinat
        for kecamatan, (x, y) in posisi.items():  # Iterasi kecamatan dan koordinatnya
            plt.text(x, y, kecamatan, fontsize=9, verticalalignment='bottom', horizontalalignment='right')  # Tambah label kecamatan
        plt.xlabel("Koordinat X")  # Label sumbu x
        plt.ylabel("Koordinat Y")  # Label sumbu y
        plt.title("Visualisasi Posisi Kecamatan dalam Grafik Cartesian")  # Judul plot
        plt.grid(True)  # Tampilkan grid
        plt.show()  # Tampilkan scatter plot
    
    koordinat()  # Panggil fungsi koordinat untuk menggambar scatter plot
    
    plt.figure(figsize=(12, 10))  # Buat figure baru untuk graf dengan ukuran 12x10
    nx.draw(G, posisi, with_labels=True, node_color='lightblue', node_size=2000, font_size=10)  # Gambar graf dengan label dan styling
    nx.draw_networkx_edge_labels(G, posisi, edge_labels={(u, v): d['weight'] for u, v, d in G.edges(data=True)})  # Tambah label bobot pada sisi
    
    if rute_terpendek:  # Jika ada rute terpendek
        jalur = [(rute_terpendek[i], rute_terpendek[i+1]) for i in range(len(rute_terpendek)-1)]  # Buat daftar pasangan simpul untuk jalur
        nx.draw_networkx_edges(G, posisi, edgelist=jalur, edge_color='red', width=1, style='dashed')  # Gambar jalur dengan warna merah dan gaya putus-putus
    plt.show()  # Tampilkan graf

def tampilkan_rute():  # Fungsi untuk menampilkan rute di GUI
    awal = dropdown_awal.get()  # Ambil nilai dari dropdown awal
    tujuan = dropdown_tujuan.get()  # Ambil nilai dari dropdown tujuan
    if awal == tujuan:  # Cek jika awal dan tujuan sama
        hasil_label.config(text="Kecamatan awal dan tujuan tidak boleh sama!")  # Tampilkan pesan error
        return  # Keluar dari fungsi
    rute, jarak = bfs_berbobot(graf, awal, tujuan)  # Cari rute dan jarak dengan BFS berbobot
    if rute:  # Jika rute ditemukan
        hasil_label.config(text=f"Rute tercepat: {' -> '.join(rute)}\nTotal jarak: {jarak} km")  # Tampilkan rute dan jarak di label
        gambar_graf(graf, rute)  # Gambar graf dengan rute terpendek
    else:  # Jika rute tidak ditemukan
        hasil_label.config(text="Tidak ada rute yang tersedia")  # Tampilkan pesan tidak ada rute
        
graf = {  # Struktur graf sebagai dictionary dengan simpul dan tetangga beserta bobot
    'Gubeng': { 'Mulyorejo': 4, 'Sukolilo': 3, 'Tambaksari': 3,'Tenggilis Mejoyo':9,},
    'Gunung Anyar': {'Rungkut': 3, 'Tenggilis Mejoyo': 2},
    'Mulyorejo': {'Gubeng': 4, 'Sukolilo': 2, 'Tambaksari': 3},
    'Rungkut': {'Gunung Anyar': 3, 'Sukolilo': 4, 'Tenggilis Mejoyo': 2},
    'Sukolilo': {'Gubeng': 3, 'Mulyorejo': 2, 'Rungkut': 4},
    'Tambaksari': { 'Gubeng':2, 'Mulyorejo': 3},
    'Tenggilis Mejoyo': {'Gunung Anyar': 2, 'Rungkut': 2,'Gubeng':5}
}

root = tk.Tk()  # Buat jendela utama GUI
root.title("Visualisasi Rute BFS")  # Atur judul jendela
root.geometry("400x250")  # Atur ukuran jendela menjadi 400x250 piksel

kecamatan_list = list(graf.keys())  # Buat daftar kecamatan dari kunci graf
tk.Label(root, text="Pilih Kecamatan Awal:").pack()  # Tambah label untuk dropdown awal
dropdown_awal = ttk.Combobox(root, values=kecamatan_list)  # Buat dropdown untuk memilih kecamatan awal
dropdown_awal.pack()  # Tempatkan dropdown awal di jendela

tk.Label(root, text="Pilih Kecamatan Tujuan:").pack()  # Tambah label untuk dropdown tujuan
dropdown_tujuan = ttk.Combobox(root, values=kecamatan_list)  # Buat dropdown untuk memilih kecamatan tujuan
dropdown_tujuan.pack()  # Tempatkan dropdown tujuan di jendela

button = tk.Button(root, text="Tampilkan Rute", command=tampilkan_rute)  # Buat tombol untuk menampilkan rute
button.pack()  # Tempatkan tombol di jendela

hasil_label = tk.Label(root, text="")  # Buat label kosong untuk menampilkan hasil
hasil_label.pack()  # Tempatkan label di jendela

root.mainloop()  # Jalankan loop utama GUI