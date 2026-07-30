# Dashboard Analisis Sentimen — MSIB vs Magang Berdampak

Dashboard demo untuk sidang skripsi, menampilkan hasil analisis sentimen Fine-Tuned IndoBERT
terhadap Program MSIB dan Magang Berdampak.

## Cara Menjalankan

```
pip install -r requirements.txt
streamlit run app.py
```

## Isi Dashboard

1. **Distribusi Sentimen per Program** — grafik & tabel distribusi positif/netral/negatif untuk tiap dataset.
2. **Perbandingan Antar Program** — perbandingan fase awal (MSIB Setara vs Magang Berdampak) dan fase matang (MSIB Matang vs Magang Berdampak).
3. **Contoh Komentar** — jelajahi contoh komentar asli per program dan kelas sentimen.
4. **Evaluasi Model** — classification report dan confusion matrix model terbaik (Random Oversampling), persis dari Tabel 4.7 dan Gambar 4.4 skripsi.

## Sumber Data

Data dibaca langsung dari 3 file Excel hasil klasifikasi di:
`C:\Users\ekopr\OneDrive\KULIAH\SKRIPSI\Hasil klasifikasi\`

Angka classification report & confusion matrix di-hardcode di `constants.py` sesuai Tabel 4.7 / Gambar 4.4 skripsi (skenario Random Oversampling), karena tidak ada file terpisah yang merepresentasikan ulang metrik ini.
