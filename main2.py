import streamlit as st
import pandas as pd
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

# Nama file database
db_file = "database_customer.xlsx"
lampiran_folder = "lampiran"
os.makedirs(lampiran_folder, exist_ok=True)

# --- Fungsi generate PDF ---
def generate_pdf(data, lampiran_files, filename="customer_form.pdf"):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    # --- Kop Surat ---
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width/2, height-50, "PT. BAHAGIA INDO PERSADA")
    c.setFont("Helvetica-Oblique", 10)
    c.drawCentredString(width/2, height-65, "your plastic packaging partner")
    c.setFont("Helvetica", 9)
    c.drawCentredString(width/2, height-80,
        "Ruko Gading Kirana Blok D6 No 46, Kelapa Gading - Jakarta Utara 14240")
    c.drawCentredString(width/2, height-95,
        "Telp: (+62) 21 4585 3992 / (+62) 21 4585 4606")

    # --- Judul ---
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(width/2, height-130, "CUSTOMER PROFILE FORM")

    # --- Isi Data ---
    y = height - 160
    nomor = 1
    for key, value in data.items():
        c.setFont("Helvetica", 10)
        c.drawString(50, y, f"{nomor}. {key} : {value}")
        y -= 18
        nomor += 1
        if y < 120:
            c.showPage()
            y = height - 100

    # --- Tanda Tangan ---
    y -= 40
    c.setFont("Helvetica", 10)
    c.drawString(50, y, "Disetujui oleh,")
    c.drawString(width - 200, y, "Hormat kami,")

    y -= 80
    c.drawString(50, y, "(__________________)")
    c.drawString(width - 200, y, "(__________________)")

    # --- Halaman Lampiran ---
    c.showPage()
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(width/2, height-50, "LAMPIRAN DOKUMEN")

    y = height - 100
    for item, filename in lampiran_files.items():
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, y, f"{item}:")
        y -= 20

        if filename and filename.lower().endswith((".png", ".jpg", ".jpeg")):
            try:
                img_path = os.path.join(lampiran_folder, filename)
                img = ImageReader(img_path)
                c.drawImage(img, 50, y-200, width=300, height=200, preserveAspectRatio=True, mask='auto')
                y -= 220
            except:
                c.setFont("Helvetica", 9)
                c.drawString(60, y, "[Gagal memuat gambar]")
                y -= 20
        else:
            c.setFont("Helvetica", 9)
            c.drawString(60, y, filename if filename else "Tidak ada")
            y -= 20

        if y < 150:
            c.showPage()
            y = height - 100

    c.save()
    return filename


# --- FORM STREAMLIT ---
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
dokumen_pengiriman = st.text_input("10. Dokumen Pengiriman (3 Rangkap / 5 Rangkap Surat Jalan & Invoice)")

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
st.subheader("Lampiran (Upload File)")
lampiran_files = {}
for item in [
    "NPWP atau KTP",
    "NIB",
    "Ket Rekening",
    "KTP Penanggung Jawab",
    "Share Location Alamat Pengiriman Barang"
]:
    uploaded_file = st.file_uploader(f"Upload {item}", type=["pdf", "jpg", "png"], key=item)
    if uploaded_file:
        file_path = os.path.join(lampiran_folder, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        lampiran_files[item] = uploaded_file.name
    else:
        lampiran_files[item] = ""

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

    # Tambahkan lampiran
    for item, filename in lampiran_files.items():
        data[item] = filename if filename else "Tidak ada"

    # Simpan ke Excel
    if not os.path.exists(db_file):
        df = pd.DataFrame([data])
    else:
        df = pd.read_excel(db_file)
        df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    df.to_excel(db_file, index=False)

    st.success("✅ Data berhasil disimpan!")

    # Generate PDF
    pdf_file = generate_pdf(data, lampiran_files, "customer_form.pdf")
    with open(pdf_file, "rb") as f:
        st.download_button("⬇️ Download PDF Customer Form", f, file_name="customer_form.pdf", mime="application/pdf")

# --- Tombol Download Database ---
if os.path.exists(db_file):
    with open(db_file, "rb") as f:
        st.download_button(
            label="⬇️ Download Database Customer",
            data=f,
            file_name="database_customer.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
