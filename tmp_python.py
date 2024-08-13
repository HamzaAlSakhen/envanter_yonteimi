
import tkinter as tk
from tkinter import messagebox

class EnvanterYonetimi(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title('Envanter Yönetimi')
        self.master.geometry("650x450")
        self.grid()
        
        self.urunler = []
        self.widget_olustur()

    def widget_olustur(self):
        self.arama_widget_olustur()
        self.envanter_gorunum_olustur()
        self.urun_giris_widget_olustur()
        self.islem_butonlari_olustur()

    def arama_widget_olustur(self):
        tk.Label(self, text='Arama (Ürün Numarası): ').grid(row=0, column=1, padx=6, pady=20, sticky=tk.E)

        self.arama_var = tk.StringVar()
        self.arama_giris = tk.Entry(self, width=20, textvariable=self.arama_var)
        self.arama_giris.grid(row=0, column=2, padx=8, pady=20, sticky=tk.W)

        tk.Button(self, text='Ara', command=self.envanter_ara).grid(row=0, column=3, padx=8, pady=20, sticky=tk.W)
        tk.Button(self, text='Sıfırla', command=self.aramayi_temizle).grid(row=0, column=4, padx=4, pady=20, sticky=tk.W)

    def envanter_gorunum_olustur(self):
        self.kaydirma = tk.Scrollbar(self)
        self.kaydirma.grid(row=3, column=4, sticky='ns')
        
        self.envanter_gorunum = tk.Text(self, width=60, height=10, wrap=tk.WORD, yscrollcommand=self.kaydirma.set)
        self.envanter_gorunum.grid(row=3, column=0, columnspan=5, padx=20, pady=20)
        self.kaydirma.config(command=self.envanter_gorunum.yview)

        self.urun_sayisi_etiketi = tk.Label(self, text=f"Ürün Sayısı: {len(self.urunler)}")
        self.urun_sayisi_etiketi.grid(row=4, column=0, pady=5, sticky=tk.N)

        self.envanter_gorunumunu_guncelle()

    def urun_giris_widget_olustur(self):
        alanlar = [('Ürün Numarası', '_urun_numarasi'), ('Ürün Adı', '_urun_adi'), 
                   ('Stok Miktarı', '_stok_miktari'), ('Fiyat', '_fiyat')]

        for i, (etiket, attr) in enumerate(alanlar):
            tk.Label(self, text=etiket).grid(row=6 + (i // 2) * 4, column=i % 2 * 2, padx=6, pady=6, sticky=tk.E)
            setattr(self, attr, tk.StringVar())
            tk.Entry(self, width=20, textvariable=getattr(self, attr)).grid(row=6 + (i // 2) * 4, column=i % 2 * 2 + 1, padx=8, pady=10, sticky=tk.E)

    def islem_butonlari_olustur(self):
        islemler = [('Ürün Ekle', self.urun_ekle), ('Ürün Düzenle', self.urun_duzenle), ('Ürün Sil', self.urun_sil)]

        for i, (metin, komut) in enumerate(islemler):
            tk.Button(self, text=metin, command=komut).grid(row=11, column=i+1, padx=5, pady=20, sticky=tk.W)

    def envanter_gorunumunu_guncelle(self):
        self.envanter_gorunum.config(state=tk.NORMAL)
        self.envanter_gorunum.delete(1.0, tk.END)
        self.envanter_gorunum.insert(tk.END, 'Ürün Numarası\t\tÜrün Adı\t\tStok Miktarı\t\tFiyat\n')
        self.envanter_gorunum.insert(tk.END, '-' * 100 + '\n')

        for urun in self.urunler:
            self.envanter_gorunum.insert(tk.END, f"{urun['numara']}\t\t{urun['ad']}\t\t{urun['stok']}\t\t{urun['fiyat']}\n")

        self.envanter_gorunum.config(state=tk.DISABLED)
        self.urun_sayisi_etiketi.config(text=f"Ürün Sayısı: {len(self.urunler)}")

    def urun_ekle(self):
        urun = {
            'numara': self._urun_numarasi.get(),
            'ad': self._urun_adi.get(),
            'stok': self._stok_miktari.get(),
            'fiyat': self._fiyat.get()
        }

        if all(urun.values()):
            self.urunler.append(urun)
            self.envanter_gorunumunu_guncelle()
            self.giris_alanlarini_temizle()
            messagebox.showinfo("Başarılı", "Ürün başarıyla eklendi.")
        else:
            messagebox.showerror("Hata", "Tüm alanlar doldurulmalıdır.")

    def envanter_ara(self):
        arama_degeri = self.arama_var.get()
        bulunan_urunler = [urun for urun in self.urunler if urun['numara'] == arama_degeri]

        if bulunan_urunler:
            self.envanter_gorunum.config(state=tk.NORMAL)
            self.envanter_gorunum.delete(1.0, tk.END)
            self.envanter_gorunum.insert(tk.END, 'Ürün Numarası\t\tÜrün Adı\t\tStok Miktarı\t\tFiyat\n')
            self.envanter_gorunum.insert(tk.END, '-' * 60 + '\n')

            for urun in bulunan_urunler:
                self.envanter_gorunum.insert(tk.END, f"{urun['numara']}\t\t{urun['ad']}\t\t{urun['stok']}\t\t{urun['fiyat']}\n")

            self.envanter_gorunum.config(state=tk.DISABLED)
        else:
            messagebox.showinfo("Arama Sonucu", "Bu numaraya sahip bir ürün bulunamadı.")

    def aramayi_temizle(self):
        self.arama_var.set('')
        self.envanter_gorunumunu_guncelle()

    def urun_duzenle(self):
        arama_degeri = self.arama_var.get()
        for i, urun in enumerate(self.urunler):
            if urun['numara'] == arama_degeri:
                self._urun_numarasi.set(urun['numara'])
                self._urun_adi.set(urun['ad'])
                self._stok_miktari.set(urun['stok'])
                self._fiyat.set(urun['fiyat'])
                self.arama_var.set('')
                
                def guncelle():
                    yeni_urun = {
                        'numara': self._urun_numarasi.get(),
                        'ad': self._urun_adi.get(),
                        'stok': self._stok_miktari.get(),
                        'fiyat': self._fiyat.get()
                    }
                    if all(yeni_urun.values()):
                        self.urunler[i] = yeni_urun
                        self.envanter_gorunumunu_guncelle()
                        self.giris_alanlarini_temizle()
                        messagebox.showinfo("Başarılı", "Ürün başarıyla güncellendi.")
                        guncelle_butonu.destroy()
                    else:
                        messagebox.showerror("Hata", "Tüm alanlar doldurulmalıdır.")

                guncelle_butonu = tk.Button(self, text="Güncelle", command=guncelle)
                guncelle_butonu.grid(row=12, column=2, padx=5, pady=20, sticky=tk.W)
                return
        messagebox.showinfo("Ürün Düzenle", "Bu numaraya sahip bir ürün bulunamadı.")

    def urun_sil(self):
        arama_degeri = self.arama_var.get()
        for urun in self.urunler:
            if urun['numara'] == arama_degeri:
                self.urunler.remove(urun)
                self.envanter_gorunumunu_guncelle()
                self.arama_var.set('')
                messagebox.showinfo("Ürün Sil", "Ürün başarıyla silindi.")
                return
        messagebox.showinfo("Ürün Sil", "Bu numaraya sahip bir ürün bulunamadı.")

    def giris_alanlarini_temizle(self):
        for attr in ['_urun_numarasi', '_urun_adi', '_stok_miktari', '_fiyat']:
            getattr(self, attr).set('')

def main():
    root = tk.Tk()
    app = EnvanterYonetimi(master=root)
    app.mainloop()

if __name__ == "__main__":
    main()