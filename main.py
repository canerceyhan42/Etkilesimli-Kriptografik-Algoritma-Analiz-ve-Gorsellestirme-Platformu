
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pyperclip

from algorithms.aes_module import AESVisualizer
from algorithms.galois_module import GaloisField
from algorithms.hash_module import HashVisualizer
from algorithms.hmac_module import HMACVisualizer
from algorithms.rbg_module import RandomBitGenerator
from algorithms.des_module import DESVisualizer
from algorithms.triple_des_module import TripleDESVisualizer


class CryptoVisualizer:

    def __init__(self, root):

        self.root = root
        self.root.title("CryptoVisualizer")
        self.root.geometry("1200x800")

        self.aes_engine = AESVisualizer()
        self.gf = GaloisField()
        self.hash_engine = HashVisualizer()
        self.hmac_engine = HMACVisualizer()
        self.rbg_engine = RandomBitGenerator()
        self.des_engine = DESVisualizer()
        self.triple_des_engine = TripleDESVisualizer()

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)

        self.create_home_tab()
        self.create_aes_tab()
        self.create_des_tab()
        self.create_3des_tab()
        self.create_hash_tab()
        self.create_hmac_tab()
        self.create_galois_tab()
        self.create_rbg_tab()

    # ==================================================
    # HOME
    # ==================================================

    def create_home_tab(self):

        tab = ttk.Frame(self.notebook)

        self.notebook.add(
            tab,
            text="Home"
        )

        title = tk.Label(
            tab,
            text="CryptoVisualizer",
            font=("Arial", 24, "bold")
        )

        title.pack(pady=20)

        info = """
Etkileşimli Kriptografik Algoritma Analiz ve Görselleştirme Platformu

Modüller

• AES
• DES
• 3DES
• SHA-256
• HMAC
• GF(2^8)
• Random Bit Generator

Kriptografi ve Uygulamaları Final Projesi
"""

        tk.Label(
            tab,
            text=info,
            font=("Arial", 14),
            justify="left"
        ).pack()

    # ==================================================
    # AES
    # ==================================================

    def create_aes_tab(self):

        tab = ttk.Frame(self.notebook)

        self.notebook.add(
            tab,
            text="AES"
        )

        tk.Label(
            tab,
            text="Plaintext"
        ).pack(pady=5)

        plaintext = tk.Entry(
            tab,
            width=60
        )

        plaintext.pack()

        # Dosya yükleme butonu
        def load_file():
            filename = filedialog.askopenfilename(
                title="Plaintext Dosyası Seç",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            if filename:
                try:
                    with open(filename, 'r', encoding='utf-8') as f:
                        content = f.read()
                        plaintext.delete(0, tk.END)
                        plaintext.insert(0, content)
                except Exception as e:
                    messagebox.showerror("Hata", f"Dosya okunamadı: {str(e)}")

        tk.Button(
            tab,
            text="📁 Dosyadan Yükle",
            command=load_file
        ).pack(pady=2)

        tk.Label(
            tab,
            text="Key"
        ).pack(pady=5)

        key = tk.Entry(
            tab,
            width=60
        )

        key.pack()

        # Adım kontrolü için frame
        control_frame = tk.Frame(tab)
        control_frame.pack(pady=5)

        step_label = tk.Label(
            control_frame,
            text="Adım: 0/5",
            font=("Arial", 10, "bold")
        )
        step_label.pack(side="left", padx=10)

        # Hız kontrolü
        tk.Label(
            control_frame,
            text="Otomatik Hız:"
        ).pack(side="left", padx=5)

        speed_var = tk.IntVar(value=2000)
        speed_scale = tk.Scale(
            control_frame,
            from_=500,
            to=5000,
            orient="horizontal",
            variable=speed_var,
            length=150
        )
        speed_scale.pack(side="left", padx=5)

        tk.Label(
            control_frame,
            text="ms"
        ).pack(side="left")

        output = tk.Text(
            tab,
            height=28
        )

        output.pack(
            fill="both",
            expand=True,
            pady=10
        )

        # Adım kontrolü için değişkenler
        current_step = [0]  # Liste kullanıyoruz ki nested fonksiyonlarda değiştirebilelim
        steps_data = [[]]  # Adımları saklamak için
        auto_play_running = [False]  # Otomatik oynatma durumu
        auto_play_id = [None]  # After callback id'si

        def show_step(step_index):
            """Belirli bir adımı göster"""
            if not steps_data[0]:
                return
                
            if 0 <= step_index < len(steps_data[0]):
                current_step[0] = step_index
                title, content = steps_data[0][step_index]
                
                output.delete("1.0", tk.END)
                output.insert(tk.END, "=" * 60 + "\n")
                output.insert(tk.END, f"{title}\n")
                output.insert(tk.END, "=" * 60 + "\n\n")
                output.insert(tk.END, content)
                
                step_label.config(text=f"Adım: {step_index + 1}/{len(steps_data[0])}")

        def prev_step():
            """Önceki adıma git"""
            stop_auto_play()
            if current_step[0] > 0:
                show_step(current_step[0] - 1)

        def next_step():
            """Sonraki adıma git"""
            stop_auto_play()
            if current_step[0] < len(steps_data[0]) - 1:
                show_step(current_step[0] + 1)

        def first_step():
            """İlk adıma git"""
            stop_auto_play()
            show_step(0)

        def last_step():
            """Son adıma git"""
            stop_auto_play()
            show_step(len(steps_data[0]) - 1)

        def stop_auto_play():
            """Otomatik oynatmayı durdur"""
            if auto_play_running[0] and auto_play_id[0]:
                self.root.after_cancel(auto_play_id[0])
                auto_play_running[0] = False

        def auto_play():
            """Otomatik olarak adımları göster"""
            if not steps_data[0]:
                return
            
            if auto_play_running[0]:
                # Durdur
                stop_auto_play()
                return
            
            # Başlat
            auto_play_running[0] = True
            
            def play_next():
                if not auto_play_running[0]:
                    return
                    
                if current_step[0] < len(steps_data[0]) - 1:
                    show_step(current_step[0] + 1)
                    auto_play_id[0] = self.root.after(speed_var.get(), play_next)
                else:
                    # Son adıma gelindi, durdur
                    auto_play_running[0] = False
            
            play_next()

        def encrypt_aes():

            output.delete(
                "1.0",
                tk.END
            )

            try:

                cipher = self.aes_engine.encrypt(
                    plaintext.get(),
                    key.get()
                )

                visual = self.aes_engine.visualize(
                    plaintext.get()
                )

                output.insert(
                    tk.END,
                    "AES ENCRYPTION\n"
                )

                output.insert(
                    tk.END,
                    "=" * 50 + "\n\n"
                )

                output.insert(
                    tk.END,
                    f"Cipher:\n{cipher}\n\n"
                )

                output.insert(
                    tk.END,
                    visual
                )

            except Exception as e:

                output.insert(
                    tk.END,
                    str(e)
                )

        def visualize_steps():
            """Adım adım görselleştirme başlat"""
            stop_auto_play()
            
            try:
                steps_data[0] = self.aes_engine.get_visualization_steps(
                    plaintext.get()
                )
                current_step[0] = 0
                show_step(0)
            except Exception as e:
                output.delete("1.0", tk.END)
                output.insert(tk.END, f"Hata: {str(e)}")

        def decrypt_aes():

            output.delete(
                "1.0",
                tk.END
            )

            try:

                decrypted = self.aes_engine.decrypt(
                    plaintext.get(),
                    key.get()
                )

                output.insert(
                    tk.END,
                    "AES DECRYPTION\n"
                )

                output.insert(
                    tk.END,
                    "=" * 50 + "\n\n"
                )

                output.insert(
                    tk.END,
                    f"Decrypted Text:\n{decrypted}\n"
                )

            except Exception as e:

                output.insert(
                    tk.END,
                    str(e)
                )

        def copy_output():
            try:
                content = output.get("1.0", tk.END)
                pyperclip.copy(content)
                messagebox.showinfo("Başarılı", "Çıktı panoya kopyalandı!")
            except Exception as e:
                messagebox.showerror("Hata", f"Kopyalama hatası: {str(e)}")

        def save_output():
            filename = filedialog.asksaveasfilename(
                title="Çıktıyı Kaydet",
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            if filename:
                try:
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(output.get("1.0", tk.END))
                    messagebox.showinfo("Başarılı", "Çıktı dosyaya kaydedildi!")
                except Exception as e:
                    messagebox.showerror("Hata", f"Kaydetme hatası: {str(e)}")

        # Ana butonlar
        button_frame1 = tk.Frame(tab)
        button_frame1.pack(pady=5)

        tk.Button(
            button_frame1,
            text="Encrypt",
            command=encrypt_aes,
            width=15
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame1,
            text="Decrypt",
            command=decrypt_aes,
            width=15
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame1,
            text="🎬 Adım Adım",
            command=visualize_steps,
            width=15,
            bg="#4CAF50",
            fg="white"
        ).pack(side="left", padx=5)

        # Adım kontrol butonları
        button_frame2 = tk.Frame(tab)
        button_frame2.pack(pady=5)

        tk.Button(
            button_frame2,
            text="⏮ İlk",
            command=first_step,
            width=8
        ).pack(side="left", padx=2)

        tk.Button(
            button_frame2,
            text="◀ Geri",
            command=prev_step,
            width=8
        ).pack(side="left", padx=2)

        tk.Button(
            button_frame2,
            text="▶ Otomatik",
            command=auto_play,
            width=12,
            bg="#2196F3",
            fg="white"
        ).pack(side="left", padx=2)

        tk.Button(
            button_frame2,
            text="İleri ▶",
            command=next_step,
            width=8
        ).pack(side="left", padx=2)

        tk.Button(
            button_frame2,
            text="Son ⏭",
            command=last_step,
            width=8
        ).pack(side="left", padx=2)

        # Dosya işlemleri
        button_frame3 = tk.Frame(tab)
        button_frame3.pack(pady=5)

        tk.Button(
            button_frame3,
            text="📋 Kopyala",
            command=copy_output,
            width=12
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame3,
            text="💾 Kaydet",
            command=save_output,
            width=12
        ).pack(side="left", padx=5)

    # ==================================================
    # DES
    # ==================================================

    def create_des_tab(self):

        tab = ttk.Frame(self.notebook)

        self.notebook.add(
            tab,
            text="DES"
        )

        tk.Label(
            tab,
            text="Plaintext"
        ).pack(pady=5)

        plaintext = tk.Entry(
            tab,
            width=60
        )

        plaintext.pack()

        tk.Label(
            tab,
            text="Key (8 karakter)"
        ).pack(pady=5)

        key = tk.Entry(
            tab,
            width=60
        )

        key.pack()

        output = tk.Text(
            tab,
            height=30
        )

        output.pack(
            fill="both",
            expand=True,
            pady=10
        )

        def encrypt_des():

            output.delete(
                "1.0",
                tk.END
            )

            try:

                cipher = self.des_engine.encrypt(
                    plaintext.get(),
                    key.get()
                )

                output.insert(
                    tk.END,
                    "DES ENCRYPTION\n\n"
                )

                output.insert(
                    tk.END,
                    f"Şifreli Metin (Hex):\n{cipher}\n"
                )

            except Exception as e:

                output.insert(
                    tk.END,
                    str(e)
                )

        def decrypt_des():

            output.delete(
                "1.0",
                tk.END
            )

            try:

                decrypted = self.des_engine.decrypt(
                    plaintext.get(),
                    key.get()
                )

                output.insert(
                    tk.END,
                    "DES DECRYPTION\n\n"
                )

                output.insert(
                    tk.END,
                    f"Çözülmüş Metin:\n{decrypted}\n"
                )

            except Exception as e:

                output.insert(
                    tk.END,
                    str(e)
                )

        def visualize_des():

            output.delete(
                "1.0",
                tk.END
            )

            try:

                visual = self.des_engine.visualize(
                    plaintext.get(),
                    key.get()
                )

                output.insert(
                    tk.END,
                    visual
                )

            except Exception as e:

                output.insert(
                    tk.END,
                    str(e)
                )

        button_frame = tk.Frame(tab)
        button_frame.pack(pady=10)

        tk.Button(
            button_frame,
            text="Encrypt",
            command=encrypt_des,
            width=15
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame,
            text="Decrypt",
            command=decrypt_des,
            width=15
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame,
            text="Visualize",
            command=visualize_des,
            width=15
        ).pack(side="left", padx=5)

    # ==================================================
    # 3DES
    # ==================================================

    def create_3des_tab(self):

        tab = ttk.Frame(self.notebook)

        self.notebook.add(
            tab,
            text="3DES"
        )

        tk.Label(
            tab,
            text="Plaintext"
        ).pack(pady=5)

        plaintext = tk.Entry(
            tab,
            width=60
        )

        plaintext.pack()

        tk.Label(
            tab,
            text="Key (24 karakter)"
        ).pack(pady=5)

        key = tk.Entry(
            tab,
            width=60
        )

        key.pack()

        output = tk.Text(
            tab,
            height=30
        )

        output.pack(
            fill="both",
            expand=True,
            pady=10
        )

        def encrypt_3des():

            output.delete(
                "1.0",
                tk.END
            )

            try:

                cipher = self.triple_des_engine.encrypt(
                    plaintext.get(),
                    key.get()
                )

                output.insert(
                    tk.END,
                    "3DES ENCRYPTION\n\n"
                )

                output.insert(
                    tk.END,
                    f"Şifreli Metin (Hex):\n{cipher}\n"
                )

            except Exception as e:

                output.insert(
                    tk.END,
                    str(e)
                )

        def decrypt_3des():

            output.delete(
                "1.0",
                tk.END
            )

            try:

                decrypted = self.triple_des_engine.decrypt(
                    plaintext.get(),
                    key.get()
                )

                output.insert(
                    tk.END,
                    "3DES DECRYPTION\n\n"
                )

                output.insert(
                    tk.END,
                    f"Çözülmüş Metin:\n{decrypted}\n"
                )

            except Exception as e:

                output.insert(
                    tk.END,
                    str(e)
                )

        def visualize_3des():

            output.delete(
                "1.0",
                tk.END
            )

            try:

                visual = self.triple_des_engine.visualize(
                    plaintext.get(),
                    key.get()
                )

                output.insert(
                    tk.END,
                    visual
                )

            except Exception as e:

                output.insert(
                    tk.END,
                    str(e)
                )

        button_frame = tk.Frame(tab)
        button_frame.pack(pady=10)

        tk.Button(
            button_frame,
            text="Encrypt",
            command=encrypt_3des,
            width=12
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame,
            text="Decrypt",
            command=decrypt_3des,
            width=12
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame,
            text="Visualize",
            command=visualize_3des,
            width=12
        ).pack(side="left", padx=5)

    # ==================================================
    # SHA256
    # ==================================================

    def create_hash_tab(self):

        tab = ttk.Frame(self.notebook)

        self.notebook.add(
            tab,
            text="SHA-256"
        )

        tk.Label(
            tab,
            text="Mesaj"
        ).pack(pady=5)

        message = tk.Entry(
            tab,
            width=70
        )

        message.pack()

        output = tk.Text(
            tab,
            height=10
        )

        output.pack(
            fill="x",
            padx=10,
            pady=10
        )

        def calculate_hash():

            output.delete(
                "1.0",
                tk.END
            )

            try:

                result = self.hash_engine.sha256(
                    message.get()
                )

                output.insert(
                    tk.END,
                    f"SHA-256:\n\n{result}"
                )

            except Exception as e:

                output.insert(
                    tk.END,
                    str(e)
                )

        tk.Button(
            tab,
            text="Hash Hesapla",
            command=calculate_hash
        ).pack(pady=5)

        # ==========================================
        # Hash Karşılaştırma
        # ==========================================

        tk.Label(
            tab,
            text="Algoritma Karşılaştırması",
            font=("Arial", 12, "bold")
        ).pack(pady=10)

        tk.Label(
            tab,
            text="Metin"
        ).pack()

        compare_msg = tk.Entry(
            tab,
            width=70
        )

        compare_msg.pack()

        compare_output = tk.Text(
            tab,
            height=15
        )

        compare_output.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        def compare_algos():

            compare_output.delete(
                "1.0",
                tk.END
            )

            try:

                result = self.hash_engine.compare_algorithms(
                    compare_msg.get()
                )

                compare_output.insert(
                    tk.END,
                    result
                )

            except Exception as e:

                compare_output.insert(
                    tk.END,
                    str(e)
                )

        tk.Button(
            tab,
            text="Algoritmaları Karşılaştır",
            command=compare_algos
        ).pack(pady=5)

        # ==========================================
        # Avalanche Effect
        # ==========================================

        tk.Label(
            tab,
            text="Avalanche Effect Analizi",
            font=("Arial", 12, "bold")
        ).pack(pady=10)

        tk.Label(
            tab,
            text="Mesaj 1"
        ).pack()

        msg1 = tk.Entry(
            tab,
            width=70
        )

        msg1.pack()

        tk.Label(
            tab,
            text="Mesaj 2"
        ).pack()

        msg2 = tk.Entry(
            tab,
            width=70
        )

        msg2.pack()

        avalanche_output = tk.Text(
            tab,
            height=12
        )

        avalanche_output.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        def run_avalanche():

            avalanche_output.delete(
                "1.0",
                tk.END
            )

            try:

                result = self.hash_engine.avalanche_effect(
                    msg1.get(),
                    msg2.get()
                )

                avalanche_output.insert(
                    tk.END,
                    f"Hash 1:\n{result['hash1']}\n\n"
                )

                avalanche_output.insert(
                    tk.END,
                    f"Hash 2:\n{result['hash2']}\n\n"
                )

                avalanche_output.insert(
                    tk.END,
                    f"Farklı Bit Sayısı: {result['different_bits']}\n"
                )

                avalanche_output.insert(
                    tk.END,
                    f"Değişim Oranı: %{result['percentage']}"
                )

            except Exception as e:

                avalanche_output.insert(
                    tk.END,
                    str(e)
                )

        tk.Button(
            tab,
            text="Avalanche Testi",
            command=run_avalanche
        ).pack(pady=5)

    # ==================================================
    # HMAC
    # ==================================================

    def create_hmac_tab(self):

        tab = ttk.Frame(self.notebook)

        self.notebook.add(
            tab,
            text="HMAC"
        )

        tk.Label(
            tab,
            text="Mesaj"
        ).pack(pady=5)

        message = tk.Entry(
            tab,
            width=60
        )

        message.pack()

        tk.Label(
            tab,
            text="Anahtar"
        ).pack(pady=5)

        key = tk.Entry(
            tab,
            width=60
        )

        key.pack()

        output = tk.Text(
            tab,
            height=20
        )

        output.pack(
            fill="both",
            expand=True,
            pady=10
        )

        def generate_hmac():

            output.delete(
                "1.0",
                tk.END
            )

            try:
                result = self.hmac_engine.generate(
                    message.get(),
                    key.get()
                )

                output.insert(
                    tk.END,
                    result
                )

            except Exception as e:

                output.insert(
                    tk.END,
                    str(e)
                )

        tk.Button(
            tab,
            text="HMAC Oluştur",
            command=generate_hmac
        ).pack(pady=10)

    # ==================================================
    # GF(2^8)
    # ==================================================

    def create_galois_tab(self):

        tab = ttk.Frame(self.notebook)

        self.notebook.add(
            tab,
            text="GF(2^8)"
        )

        tk.Label(
            tab,
            text="GF(2^8) Çarpma Görselleştirmesi",
            font=("Arial", 14, "bold")
        ).pack(pady=10)

        tk.Label(
            tab,
            text="Byte A (Hex)"
        ).pack()

        byte_a = tk.Entry(
            tab,
            width=20
        )

        byte_a.pack()

        tk.Label(
            tab,
            text="Byte B (Hex)"
        ).pack()

        byte_b = tk.Entry(
            tab,
            width=20
        )

        byte_b.pack()

        output = tk.Text(
            tab,
            height=25
        )

        output.pack(
            fill="both",
            expand=True,
            pady=10
        )

        def calculate():

            output.delete(
                "1.0",
                tk.END
            )

            try:

                result = self.gf.visualize_multiplication(
                    byte_a.get(),
                    byte_b.get()
                )

                output.insert(
                    tk.END,
                    result
                )

            except Exception as e:

                output.insert(
                    tk.END,
                    str(e)
                )

        tk.Button(
            tab,
            text="GF(2^8) Hesapla",
            command=calculate
        ).pack(pady=10)

    # ==================================================
    # RANDOM BIT GENERATOR
    # ==================================================

    def create_rbg_tab(self):

        tab = ttk.Frame(self.notebook)

        self.notebook.add(
            tab,
            text="RBG"
        )

        tk.Label(
            tab,
            text="Random Bit Generator",
            font=("Arial", 14, "bold")
        ).pack(pady=10)

        bits_var = tk.IntVar()
        bits_var.set(128)

        tk.Radiobutton(
            tab,
            text="128 Bit",
            variable=bits_var,
            value=128
        ).pack()

        tk.Radiobutton(
            tab,
            text="256 Bit",
            variable=bits_var,
            value=256
        ).pack()

        tk.Radiobutton(
            tab,
            text="512 Bit",
            variable=bits_var,
            value=512
        ).pack()

        output = tk.Text(
            tab,
            height=25
        )

        output.pack(
            fill="both",
            expand=True,
            pady=10
        )

        def generate():

            output.delete(
                "1.0",
                tk.END
            )

            try:

                result = self.rbg_engine.generate(
                    bits_var.get()
                )

                output.insert(
                    tk.END,
                    f"{bits_var.get()} Bit Rastgele Değer\n\n"
                )

                output.insert(
                    tk.END,
                    f"Hex: {result}\n"
                )

            except Exception as e:

                output.insert(
                    tk.END,
                    str(e)
                )

        def generate_with_analysis():

            output.delete(
                "1.0",
                tk.END
            )

            try:

                result = self.rbg_engine.generate_with_analysis(
                    bits_var.get()
                )

                output.insert(
                    tk.END,
                    result
                )

            except Exception as e:

                output.insert(
                    tk.END,
                    str(e)
                )

        def compare_prng():

            output.delete(
                "1.0",
                tk.END
            )

            try:

                result = self.rbg_engine.compare_prng_vs_csprng(100)

                output.insert(
                    tk.END,
                    result
                )

            except Exception as e:

                output.insert(
                    tk.END,
                    str(e)
                )

        button_frame = tk.Frame(tab)
        button_frame.pack(pady=10)

        tk.Button(
            button_frame,
            text="Üret",
            command=generate,
            width=15
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame,
            text="Analiz Et",
            command=generate_with_analysis,
            width=15
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame,
            text="PRNG vs CSPRNG",
            command=compare_prng,
            width=20
        ).pack(side="left", padx=5)


# ==================================================
# MAIN
# ==================================================

if __name__ == "__main__":
    
    print("Program başlatılıyor...")
    
    root = tk.Tk()

    app = CryptoVisualizer(root)

    root.mainloop()

