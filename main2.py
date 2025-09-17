import streamlit as st
import pandas as pd
import os

# Nama file database
db_file = "database_customer.xlsx"

st.title("📋 Customer Profile Form")

# --- Bagian Utama ---
st.subheader("Informasi Utama")
nama = st.text_input("1. Nama Perusahaan / Individu")
email = st.text_input("2. Email Perusahaan")
payment_terms = st.text_input("3. Terms Of Payment")
payment_delivery = st.text_input("4. Payment Delivery")

# --- Bagian Gudang ---
st.subheader("Informasi Gudang")
pic_gudang = st.text_input("5. PIC Gudang")
email_gudang = st.text_input("6. Email Gudang")
telp_gudang = st.text_input("7. No. Telp Gudang")
alamat_pengiriman = st.text_area("8. Alamat Pengiriman Barang")
hari_jam_operasional = st.text_input("9. Hari & Jam Operational Gudang")
dokumen_pengiriman = st.text_input(
    "10. Dokumen Pengiriman (3 Rangkap / 5 Rangkap Surat Jalan & Invoice)"
)

# --- Bagian Finance ---
st.subheader("Informasi Finance")
pic_finance = st.text_input("11. PIC Finance")
email_finance = st.text_input("12. Email Finance")
telp_finance = st.text_input("13. No. Telp Finance")
alamat_tukar_faktur = st.text_area("14. Alamat Tukar Faktur")
dokumen_tukar_faktur = st.text_input("15. Dokumen Tukar Faktur (Yang Diperlukan)")
jadwal_tukar_faktur = st.text_input("16. Jadwal Tukar Faktur")

# --- Bagian Purchasing ---
st.subheader("Informasi Purchasing")
pic_purchasing = st.text_input("17. PIC Purchasing")
email_purchasing = st.text_input("18. Email Purchasing")
telp_purchasing = st.text_input("19. No. Telp Purchasing")

# --- Bagian Lampiran ---
st.subheader("Lampiran (Checklist + Link Drive)")
lampiran = {}
for item in [
    "NPWP atau KTP",
    "NIB",
    "Ket Rekening",
    "KTP Penanggung Jawab",
    "Share Location Alamat Pengiriman Barang"
]:
    cek = st.checkbox(item)
    link = st.text_input(f"Link {item}")
    lampiran[item] = {"ceklist": cek, "link": link}

# --- Tombol Simpan ---
if st.button("💾 Simpan"):
    data = {
        # Utama
        "Nama Perusahaan": nama,
        "Email Perusahaan": email,
        "Terms Of Payment": payment_terms,
        "Payment Delivery": payment_delivery,

        # Gudang
        "PIC Gudang": pic_gudang,
        "Email Gudang": email_gudang,
        "No. Telp Gudang": telp_gudang,
        "Alamat Pengiriman": alamat_pengiriman,
        "Hari & Jam Operasional Gudang": hari_jam_operasional,
        "Dokumen Pengiriman": dokumen_pengiriman,

        # Finance
        "PIC Finance": pic_finance,
        "Email Finance": email_finance,
        "No. Telp Finance": telp_finance,
        "Alamat Tukar Faktur": alamat_tukar_faktur,
        "Dokumen Tukar Faktur": dokumen_tukar_faktur,
        "Jadwal Tukar Faktur": jadwal_tukar_faktur,

        # Purchasing
        "PIC Purchasing": pic_purchasing,
        "Email Purchasing": email_purchasing,
        "No. Telp Purchasing": telp_purchasing,
    }

    # Tambahkan lampiran ke data
    for item, val in lampiran.items():
        data[item] = "Ya" if val["ceklist"] else "Tidak"
        data[item + " Link"] = val["link"]

    # Simpan ke Excel
    if not os.path.exists(db_file):
        df = pd.DataFrame([data])
    else:
        df = pd.read_excel(db_file)
        df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)

    df.to_excel(db_file, index=False)
    st.success("✅ Data berhasil disimpan!")

# --- Tombol Download Database ---
if os.path.exists(db_file):
    with open(db_file, "rb") as f:
        st.download_button(
            label="⬇️ Download Database Customer",
            data=f,
            file_name="database_customer.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
