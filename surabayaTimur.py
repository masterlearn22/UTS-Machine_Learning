import tkinter as tk
from tkinter import ttk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
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

# Posisi koordinat untuk tata letak peta
posisi = {
    'Gubeng': (8, 6), 'Gunung Anyar': (10, 3),
    'Mulyorejo': (10.5, 6.5), 'Rungkut': (10, 4), 'Sukolilo': (10, 5), 
    'Tambaksari': (8, 7), 'Tenggilis Mejoyo': (8, 4),
}

# Warna untuk visualisasi
WARNA_KECAMATAN = '#3498db'  # Biru
WARNA_AWAL = '#2ecc71'       # Hijau
WARNA_TUJUAN = '#e74c3c'     # Merah
WARNA_JALUR = '#f39c12'      # Oranye
WARNA_BOBOT = '#ffffff'      # Putih untuk label bobot

class AplikasiRuteSurabaya:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualisasi Rute Kecamatan Surabaya")
        self.root.geometry("900x600")
        self.root.configure(bg="#2c3e50")
        
        # Judul aplikasi
        judul = tk.Label(root, text="Visualisasi Rute Kecamatan Surabaya", 
                         font=("Arial", 16, "bold"), bg="#2c3e50", fg="white")
        judul.pack(pady=10)
        
        # Frame utama
        main_frame = tk.Frame(root, bg="#2c3e50")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Frame kiri untuk visualisasi
        self.frame_kiri = tk.Frame(main_frame, bg="#2c3e50", width=600)
        self.frame_kiri.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Frame kanan untuk kontrol dan hasil
        frame_kanan = tk.Frame(main_frame, bg="#34495e", width=300)
        frame_kanan.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10, pady=10)
        
        # Bagian pencarian jalur
        pencarian_label = tk.Label(frame_kanan, text="Pencarian Jalur Terpendek", 
                                  font=("Arial", 12, "bold"), bg="#34495e", fg="white")
        pencarian_label.pack(pady=(10, 5), anchor="w")
        
        # Dropdown untuk kecamatan awal
        tk.Label(frame_kanan, text="Pilih Kecamatan Awal:", bg="#34495e", fg="white").pack(anchor="w")
        self.dropdown_awal = ttk.Combobox(frame_kanan, values=list(graf.keys()), width=25)
        self.dropdown_awal.pack(pady=(0, 10), fill="x")
        
        # Dropdown untuk kecamatan tujuan
        tk.Label(frame_kanan, text="Pilih Kecamatan Tujuan:", bg="#34495e", fg="white").pack(anchor="w")
        self.dropdown_tujuan = ttk.Combobox(frame_kanan, values=list(graf.keys()), width=25)
        self.dropdown_tujuan.pack(pady=(0, 10), fill="x")
        
        # Tombol cari rute
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 10, "bold"))
        self.tombol_cari = ttk.Button(frame_kanan, text="Cari Rute Terpendek", command=self.tampilkan_rute)
        self.tombol_cari.pack(pady=10, fill="x")
        
        # Hasil pencarian
        tk.Label(frame_kanan, text="Hasil Pencarian:", font=("Arial", 12, "bold"), 
                bg="#34495e", fg="white").pack(pady=(10, 5), anchor="w")
        
        self.hasil_frame = tk.Frame(frame_kanan, bg="#2c3e50", bd=1, relief=tk.SUNKEN)
        self.hasil_frame.pack(fill="x", pady=5)
        
        self.jalur_label = tk.Label(self.hasil_frame, text="Jalur Terpendek:", 
                                   bg="#2c3e50", fg="white", justify=tk.LEFT, wraplength=280)
        self.jalur_label.pack(anchor="w", padx=5, pady=5)
        
        self.jarak_label = tk.Label(self.hasil_frame, text="Total Jarak: -", 
                                   bg="#2c3e50", fg="white")
        self.jarak_label.pack(anchor="w", padx=5, pady=5)
        
        # Keterangan
        tk.Label(frame_kanan, text="Keterangan", font=("Arial", 12, "bold"), 
                bg="#34495e", fg="white").pack(pady=(15, 5), anchor="w")
        
        # Frame untuk legenda
        legenda_frame = tk.Frame(frame_kanan, bg="#34495e")
        legenda_frame.pack(fill="x")
        
        # Legenda dengan kotak warna
        self.buat_legenda(legenda_frame, WARNA_AWAL, "Kecamatan Awal")
        self.buat_legenda(legenda_frame, WARNA_KECAMATAN, "Kecamatan Lain")
        self.buat_legenda(legenda_frame, WARNA_TUJUAN, "Kecamatan Tujuan")
        self.buat_legenda(legenda_frame, WARNA_JALUR, "Jalur")
        self.buat_legenda(legenda_frame, WARNA_BOBOT, "Bobot (km)")
        
        # Informasi tambahan
        tk.Label(frame_kanan, text="Informasi Jalur", font=("Arial", 12, "bold"), 
                bg="#34495e", fg="white").pack(pady=(15, 5), anchor="w")
        
        self.info_text = tk.Text(frame_kanan, height=6, width=30, bg="#2c3e50", fg="white", 
                                wrap=tk.WORD, bd=0)
        self.info_text.pack(fill="x", pady=5)
        self.info_text.insert(tk.END, "Pilih kecamatan awal dan tujuan untuk melihat informasi jalur.")
        self.info_text.config(state=tk.DISABLED)
        
        # Inisialisasi visualisasi peta
        self.gambar_peta()
    
    def buat_legenda(self, parent, warna, teks):
        frame = tk.Frame(parent, bg="#34495e", pady=2)
        frame.pack(fill="x")
        
        kotak = tk.Canvas(frame, width=15, height=15, bg=warna, bd=0, highlightthickness=0)
        kotak.pack(side=tk.LEFT, padx=5)
        
        label = tk.Label(frame, text=teks, bg="#34495e", fg="white")
        label.pack(side=tk.LEFT, padx=5, anchor="w")
    
    def gambar_peta(self, jalur_terpendek=None):
        # Hapus canvas lama jika ada
        for widget in self.frame_kiri.winfo_children():
            widget.destroy()
        
        # Buat figure dan axes baru
        fig, ax = plt.subplots(figsize=(6, 5), facecolor="#2c3e50")
        ax.set_facecolor("#2c3e50")
        
        # Buat graf tidak berarah untuk visualisasi
        G_visual = nx.Graph()
        
        # Tambahkan semua node
        for kecamatan in graf.keys():
            G_visual.add_node(kecamatan)
        
        # Tambahkan edge dengan memeriksa bobot dua arah
        edge_sudah_ditambahkan = set()
        
        for simpul, tetangga in graf.items():
            for tujuan, bobot in tetangga.items():
                # Periksa apakah edge ini sudah ditambahkan
                if (simpul, tujuan) in edge_sudah_ditambahkan or (tujuan, simpul) in edge_sudah_ditambahkan:
                    continue
                
                # Periksa apakah ada edge balik dengan bobot yang sama
                bobot_balik = graf.get(tujuan, {}).get(simpul, None)
                
                if bobot_balik is not None and bobot == bobot_balik:
                    # Jika bobot sama di kedua arah, tambahkan satu edge tidak berarah
                    G_visual.add_edge(simpul, tujuan, weight=bobot, is_bidirectional=True)
                else:
                    # Jika bobot berbeda atau tidak ada edge balik, tambahkan edge berarah
                    G_visual.add_edge(simpul, tujuan, weight=bobot, is_bidirectional=False)
                
                # Tandai edge ini sudah ditambahkan
                edge_sudah_ditambahkan.add((simpul, tujuan))
        
        # Gambar semua node (kecamatan)
        node_colors = [WARNA_KECAMATAN] * len(G_visual.nodes())
        
        # Jika ada jalur terpendek, atur warna node awal dan tujuan
        if jalur_terpendek and len(jalur_terpendek) > 0:
            awal = jalur_terpendek[0]
            tujuan = jalur_terpendek[-1]
            
            # Ubah warna node berdasarkan posisinya dalam jalur
            for i, node in enumerate(G_visual.nodes()):
                if node == awal:
                    node_colors[i] = WARNA_AWAL
                elif node == tujuan:
                    node_colors[i] = WARNA_TUJUAN
        
        # Gambar node
        nx.draw_networkx_nodes(G_visual, posisi, node_size=700, node_color=node_colors, 
                              edgecolors="white", ax=ax)
        nx.draw_networkx_labels(G_visual, posisi, font_color="white", font_weight="bold", ax=ax)
        
        # Gambar semua edge dengan warna abu-abu
        nx.draw_networkx_edges(G_visual, posisi, width=1.5, edge_color="#95a5a6", ax=ax)
        
        # Jika ada jalur terpendek, gambar jalur dengan warna oranye
        if jalur_terpendek and len(jalur_terpendek) > 1:
            jalur_edges = []
            for i in range(len(jalur_terpendek)-1):
                # Cari edge yang sesuai dengan jalur (bisa dalam urutan mana saja)
                u, v = jalur_terpendek[i], jalur_terpendek[i+1]
                if G_visual.has_edge(u, v):
                    jalur_edges.append((u, v))
                elif G_visual.has_edge(v, u):
                    jalur_edges.append((v, u))
            
            nx.draw_networkx_edges(G_visual, posisi, edgelist=jalur_edges, width=3, 
                                  edge_color=WARNA_JALUR, ax=ax)
        
        # Gambar label bobot edge dengan posisi yang tepat di tengah
        for (u, v, d) in G_visual.edges(data=True):
            # Ambil posisi node
            x1, y1 = posisi[u]
            x2, y2 = posisi[v]
            
            # Hitung posisi tengah edge dengan tepat
            x_mid = (x1 + x2) / 2
            y_mid = (y1 + y2) / 2
            
            # Buat lingkaran kecil sebagai latar belakang
            circle = plt.Circle((x_mid, y_mid), 0.15, color='#34495e', alpha=0.7)
            ax.add_patch(circle)
            
            # Tambahkan teks bobot
            ax.text(x_mid, y_mid, str(d['weight']), fontsize=9, color=WARNA_BOBOT, 
                   ha='center', va='center', fontweight='bold')
        
        # Hapus axis
        ax.set_axis_off()
        
        # Tambahkan canvas ke frame kiri
        canvas = FigureCanvasTkAgg(fig, master=self.frame_kiri)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def tampilkan_rute(self):
        awal = self.dropdown_awal.get()
        tujuan = self.dropdown_tujuan.get()
        
        if not awal or not tujuan:
            self.update_hasil("Silakan pilih kecamatan awal dan tujuan!", "")
            return
            
        if awal == tujuan:
            self.update_hasil("Kecamatan awal dan tujuan tidak boleh sama!", "")
            return
        
        # Cari jalur terpendek
        jalur, jarak = bfs_berbobot(graf, awal, tujuan)
        
        if jalur:
            # Update hasil
            jalur_text = " → ".join(jalur)
            jarak_text = f"{jarak} km"
            self.update_hasil(jalur_text, jarak_text)
            
            # Update informasi
            self.update_info(awal, tujuan, jalur, jarak)
            
            # Gambar ulang peta dengan jalur terpendek
            self.gambar_peta(jalur)
        else:
            self.update_hasil("Tidak ada rute yang tersedia", "")
    
    def update_hasil(self, jalur_text, jarak_text):
        self.jalur_label.config(text=f"Jalur Terpendek:\n{jalur_text}")
        self.jarak_label.config(text=f"Total Jarak: {jarak_text}")
    
    def update_info(self, awal, tujuan, jalur, jarak):
        # Enable text widget untuk update
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        
        # Tambahkan informasi
        info = f"{awal}: titik awal\n"
        info += f"{tujuan}: titik tujuan\n"
        info += f"Jumlah kecamatan yang dilalui: {len(jalur)}\n"
        info += f"Total jarak: {jarak} km\n"
        
        # Tambahkan informasi tentang jalur alternatif jika ada
        alt_routes = []
        for k in graf.keys():
            if k != awal and k != tujuan and k not in jalur:
                alt_routes.append(k)
        
        if alt_routes:
            info += f"Kecamatan yang tidak dilalui: {', '.join(alt_routes)}"
        
        self.info_text.insert(tk.END, info)
        self.info_text.config(state=tk.DISABLED)

# Jalankan aplikasi
if __name__ == "__main__":
    root = tk.Tk()
    app = AplikasiRuteSurabaya(root)
    
    # Konfigurasi style untuk combobox
    style = ttk.Style()
    style.theme_use('clam')
    style.configure('TCombobox', fieldbackground='#34495e', background='#2c3e50', foreground='white')
    style.map('TCombobox', fieldbackground=[('readonly', '#34495e')], 
              selectbackground=[('readonly', '#2c3e50')], 
              selectforeground=[('readonly', 'white')])
    
    root.mainloop()

