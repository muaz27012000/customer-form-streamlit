import streamlit as st
import pandas as pd
import os

db_file = r"C:\KANTOR\data baru\database_customer.xlsx"

st.title("Customer Profile Form")

# --- Bagian Utama ---
nama = st.text_input("Nama Perusahaan / Individu")
email = st.text_input("Email Perusahaan")
payment_terms = st.text_input("Terms of Payment")
payment_delivery = st.text_input("Payment Delivery")
alamat_pengiriman = st.text_area("Alamat Pengiriman Barang")

# --- Bagian Lampiran ---
st.subheader("Lampiran")
lampiran = {}
for item in ["NPWP atau KTP", "NIB", "Ket Rekening", "KTP Penanggung Jawab", "Share Location Alamat Pengiriman Barang"]:
    cek = st.checkbox(item)
    link = st.text_input(f"Link {item}")
    lampiran[item] = {"ceklist": cek, "link": link}

if st.button("Simpan"):
    data = {
        "Nama Perusahaan": nama,
        "Email Perusahaan": email,
        "Terms of Payment": payment_terms,
        "Payment Delivery": payment_delivery,
        "Alamat Pengiriman": alamat_pengiriman
    }
    # tambahkan lampiran ke data
    for item, val in lampiran.items():
        data[item] = "Ya" if val["ceklist"] else "Tidak"
        data[item + " Link"] = val["link"]

    # Simpan ke Excel
    if not os.path.exists(db_file):
        df = pd.DataFrame([data])
        df.to_excel(db_file, index=False)
    else:
        df = pd.read_excel(db_file)
        df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
        df.to_excel(db_file, index=False)

    st.success("Data berhasil disimpan!")
