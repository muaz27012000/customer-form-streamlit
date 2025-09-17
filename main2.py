from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import os
import streamlit as st

# Folder lampiran
lampiran_folder = "lampiran"
os.makedirs(lampiran_folder, exist_ok=True)

# Fungsi generate PDF
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


# --- Streamlit Form ---
st.title("📋 Customer Profile Form")

nama = st.text_input("Nama Perusahaan / Individu")
email = st.text_input("Email Perusahaan")

# Upload Lampiran
st.subheader("Lampiran")
lampiran_files = {}
for item in ["NPWP atau KTP", "NIB", "Ket Rekening"]:
    uploaded_file = st.file_uploader(f"Upload {item}", type=["jpg", "png"], key=item)
    if uploaded_file:
        file_path = os.path.join(lampiran_folder, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        lampiran_files[item] = uploaded_file.name
    else:
        lampiran_files[item] = ""

# Simpan & Generate PDF
if st.button("💾 Simpan"):
    data = {
        "Nama Perusahaan": nama,
        "Email Perusahaan": email,
    }

    pdf_file = generate_pdf(data, lampiran_files, "customer_form.pdf")
    with open(pdf_file, "rb") as f:
        st.download_button("⬇️ Download PDF", f, file_name="customer_form.pdf", mime="application/pdf")
