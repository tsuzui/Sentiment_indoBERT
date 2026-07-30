import streamlit as st

from ui_helpers import metric_row


def render() -> None:
    st.header("🎯 Kesimpulan")
    st.caption("Rangkuman jawaban rumusan masalah penelitian, berdasarkan Bab 5 skripsi.")

    tab_kesimpulan, tab_keterbatasan, tab_saran = st.tabs(["Kesimpulan", "Keterbatasan Penelitian", "Saran"])

    with tab_kesimpulan:
        st.subheader("Perbandingan Sentimen — Fase Awal (MSIB Setara vs Magang Berdampak)")
        metric_row([
            ("Netral MSIB Setara", "75,2%"),
            ("Netral Magang Berdampak", "52,0%"),
            ("Negatif Magang Berdampak", "28,3%", None, "Lebih tinggi dari MSIB Setara (12,9%)"),
            ("Positif Magang Berdampak", "19,7%", None, "Lebih tinggi dari MSIB Setara (11,9%)"),
        ])
        st.write(
            "Kedua program sama-sama didominasi sentimen netral, namun Magang Berdampak "
            "menunjukkan opini publik yang jauh lebih beragam dan kritis pada fase awal peluncurannya."
        )

        st.subheader("Perbandingan Sentimen — Fase Matang (MSIB Matang vs Magang Berdampak)")
        metric_row([
            ("Netral MSIB Matang", "52,3%"),
            ("Netral Magang Berdampak", "52,0%"),
            ("Pos/Neg MSIB Matang", "23,9% / 23,8%", None, "Distribusi lebih seimbang"),
            ("Kecenderungan Magang Berdampak", "Negatif > Positif"),
        ])
        st.write(
            "Pada fase matang, proporsi netral kedua program relatif serupa, tetapi MSIB Matang "
            "memiliki distribusi positif-negatif yang jauh lebih seimbang, sedangkan Magang Berdampak "
            "tetap condong ke sentimen negatif."
        )

        st.subheader("Performa Model Fine-Tuned IndoBERT")
        metric_row([
            ("Skenario Terbaik", "Random Oversampling"),
            ("Accuracy", "0,69"),
            ("Macro F1-Score", "0,59"),
            ("F1 Kelas Positif", "0,10 → 0,39", None, "Baseline → Random Oversampling"),
        ])
        st.write(
            "Model paling akurat pada kelas Netral (kelas mayoritas), namun masih terbatas pada kelas "
            "Positif karena data latih yang sedikit (87 data sebelum oversampling) — bukan karena "
            "keterbatasan arsitektur IndoBERT. Model dinilai cukup efektif untuk tujuan eksploratif "
            "penelitian ini dalam mengungkap pola dan kecenderungan sentimen publik pada kedua program."
        )

    with tab_keterbatasan:
        st.markdown(
            """
1. **Distribusi kelas tidak seimbang** — data kelas Positif jauh lebih sedikit dari Netral dan Negatif, sehingga performa model pada kelas Positif belum optimal meski sudah memakai Random Oversampling.
2. **Inferensi memakai data yang sudah dipelajari model** — hasil inferensi ke seluruh dataset (MSIB Setara, Magang Berdampak, MSIB Matang) memakai model yang sama dengan yang dilatih/diuji, termasuk data training/testing. Ini dipilih karena tujuannya untuk melihat gambaran distribusi sentimen secara utuh, bukan mengukur ulang performa model — tapi berpotensi membuat hasil sedikit bias ke performa model pada data yang sudah dikenalnya.
3. **Sumber data terbatas** — hanya dari X (Twitter) dan YouTube, belum tentu merepresentasikan opini publik di platform lain.
            """
        )

    with tab_saran:
        st.markdown(
            """
1. Memperbanyak data kelas Positif (tambah periode/kata kunci scraping) agar distribusi kelas lebih seimbang.
2. Mencoba teknik penanganan imbalance lain di luar Random Oversampling dan Class Weight, misalnya data augmentation berbasis teks (back-translation, paraphrasing).
3. Mengeksplorasi varian model lain (IndoBERT-large atau transformer berbahasa Indonesia lainnya) untuk perbandingan performa.
4. Bagi pengelola Program MSIB dan Magang Berdampak: hasil ini bisa jadi bahan evaluasi kebijakan, khususnya menindaklanjuti proporsi sentimen negatif yang relatif tinggi pada Magang Berdampak.
5. Memperluas sumber data ke platform lain seperti Instagram atau TikTok untuk gambaran opini publik yang lebih komprehensif.
            """
        )
