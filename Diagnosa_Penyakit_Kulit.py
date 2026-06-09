import streamlit as st
from typing import List, Dict
from collections import defaultdict

GEJALA = {
    "G01": "Gatal",
    "G02": "Kemerahan",
    "G03": "Pembengkakan",
    "G04": "Lepuhan berisi cairan",
    "G05": "Kulit kering",
    "G06": "Kulit pecah-pecah",
    "G07": "Bercak merah",
    "G08": "Sisik putih keperakan",
    "G09": "Kulit menebal",
    "G11": "Perubahan kuku",
    "G12": "Bercak merah melingkar",
    "G13": "Kulit bersisik",
    "G14": "Bercak melebar",
    "G15": "Tepi bercak lebih merah",
    "G16": "Gatal hebat malam hari",
    "G17": "Ruam merah",
    "G18": "Lesi pada sela jari",
    "G19": "Mudah menular",
    "G20": "Anggota keluarga ikut gatal",
    "G21": "Komedo (whitehead/blackhead)",
    "G24": "Papula",
    "G25": "Pustula",
    "G26": "Kulit berminyak",
    "G27": "Bentol merah (wheal)",
    "G28": "Muncul tiba-tiba",
    "G29": "Hilang timbul",
}

AREA = {
    "A01": "Wajah",
    "A02": "Kulit Kepala",
    "A03": "Tangan & Kaki",
    "A04": "Badan",
    "A05": "Seluruh Tubuh",
}

AREA_KODE = {v: k for k, v in AREA.items()}

GEJALA_AREA = {
    "Wajah": ["G01","G02","G03","G07","G08","G21","G24","G25","G26","G27","G28","G29"],
    "Kulit Kepala": ["G01","G07","G08","G09","G11","G12","G13","G14","G15"],
    "Tangan & Kaki": ["G01","G02","G04","G06","G16","G17","G18","G19","G20","G27","G28","G29"],
    "Badan": ["G01","G02","G03","G04","G05","G06","G07","G08","G09","G11","G12","G13","G14","G15","G16","G17","G18","G19","G20","G27","G28","G29"],
    "Seluruh Tubuh": list(GEJALA.keys()),
}

RULES = [
    {"id": "R01_inti", "penyakit": "P01", "conditions": ["G01","G02"], "inti": True, "deskripsi": "Gatal + Kemerahan (gejala inti)"},
    {"id": "R02", "penyakit": "P01", "conditions": ["G01","G02","G03"], "inti": False, "deskripsi": "+ Pembengkakan"},
    {"id": "R03", "penyakit": "P01", "conditions": ["G01","G02","G04"], "inti": False, "deskripsi": "+ Lepuhan berisi cairan"},
    {"id": "R04", "penyakit": "P01", "conditions": ["G01","G02","G05"], "inti": False, "deskripsi": "+ Kulit kering"},
    {"id": "R05", "penyakit": "P01", "conditions": ["G01","G02","G06"], "inti": False, "deskripsi": "+ Kulit pecah-pecah"},
    
    {"id": "R06_inti", "penyakit": "P02", "conditions": ["G07","G08"], "inti": True, "deskripsi": "Bercak merah + Sisik putih keperakan (inti)"},
    {"id": "R07", "penyakit": "P02", "conditions": ["G07","G08","G01"], "inti": False, "deskripsi": "+ Gatal"},
    {"id": "R08", "penyakit": "P02", "conditions": ["G07","G08","G09"], "inti": False, "deskripsi": "+ Kulit menebal"},
    {"id": "R09", "penyakit": "P02", "conditions": ["G07","G08","G06"], "inti": False, "deskripsi": "+ Kulit pecah-pecah"},
    {"id": "R10", "penyakit": "P02", "conditions": ["G07","G08","G11"], "inti": False, "deskripsi": "+ Perubahan kuku"},
    
    {"id": "R11_inti", "penyakit": "P03", "conditions": ["G12","G15"], "inti": True, "deskripsi": "Bercak melingkar + Tepi bercak lebih merah (inti)"},
    {"id": "R12", "penyakit": "P03", "conditions": ["G12","G15","G01"], "inti": False, "deskripsi": "+ Gatal"},
    {"id": "R13", "penyakit": "P03", "conditions": ["G12","G15","G13"], "inti": False, "deskripsi": "+ Kulit bersisik"},
    {"id": "R14", "penyakit": "P03", "conditions": ["G12","G15","G14"], "inti": False, "deskripsi": "+ Bercak melebar"},
    
    {"id": "R15_inti", "penyakit": "P04", "conditions": ["G16","G18"], "inti": True, "deskripsi": "Gatal malam hebat + Lesi sela jari (inti)"},
    {"id": "R16", "penyakit": "P04", "conditions": ["G16","G18","G17"], "inti": False, "deskripsi": "+ Ruam merah"},
    {"id": "R17", "penyakit": "P04", "conditions": ["G16","G18","G19"], "inti": False, "deskripsi": "+ Mudah menular"},
    {"id": "R18", "penyakit": "P04", "conditions": ["G16","G18","G20"], "inti": False, "deskripsi": "+ Keluarga ikut gatal"},
    
    {"id": "R19_inti", "penyakit": "P05", "conditions": ["G21","G26"], "inti": True, "deskripsi": "Komedo + Kulit berminyak (inti)"},
    {"id": "R20", "penyakit": "P05", "conditions": ["G21","G26","G24"], "inti": False, "deskripsi": "+ Papula"},
    {"id": "R21", "penyakit": "P05", "conditions": ["G21","G26","G25"], "inti": False, "deskripsi": "+ Pustula"},
    
    {"id": "R22_inti", "penyakit": "P06", "conditions": ["G27","G28"], "inti": True, "deskripsi": "Bentol merah + Muncul tiba-tiba (inti)"},
    {"id": "R23", "penyakit": "P06", "conditions": ["G27","G28","G01"], "inti": False, "deskripsi": "+ Gatal"},
    {"id": "R24", "penyakit": "P06", "conditions": ["G27","G28","G29"], "inti": False, "deskripsi": "+ Hilang timbul"},
    {"id": "R25", "penyakit": "P06", "conditions": ["G27","G28","G03"], "inti": False, "deskripsi": "+ Pembengkakan"},
]

PENYAKIT = {
    "P01": {
        "nama": "Dermatitis (Eksim)",
        "deskripsi": "Dermatitis atau eksim adalah kondisi peradangan pada kulit yang menyebabkan kulit menjadi merah, gatal, dan kering. Kondisi ini bersifat kronis dan dapat kambuh secara periodik.",
        "penyebab": "Kombinasi faktor genetik, disfungsi sistem imun, dan faktor lingkungan. Pemicu umum termasuk iritan (sabun, deterjen), alergen (debu, serbuk sari), stres, dan perubahan suhu ekstrem.",
        "penanganan_awal": [
            "Hindari pemicu (sabun keras, deterjen, bahan iritan lainnya)",
            "Gunakan pelembab secara teratur (minimal 2 kali sehari)",
            "Kompres dingin untuk mengurangi gatal",
            "Mandi dengan air hangat (bukan panas) selama 10-15 menit",
            "Gunakan sabun lembut dan bebas pewangi",
            "Hindari menggaruk area yang gatal"
        ],
        "sumber": "National Eczema Association, American Academy of Dermatology"
    },
    "P02": {
        "nama": "Psoriasis",
        "deskripsi": "Psoriasis adalah penyakit autoimun kronis yang menyebabkan percepatan siklus hidup sel kulit. Sel kulit menumpuk dengan cepat di permukaan kulit membentuk sisik tebal berwarna putih keperakan dan bercak merah yang terkadang terasa gatal atau nyeri.",
        "penyebab": "Disfungsi sistem imun yang menyebabkan sel T menyerang sel kulit sehat. Faktor genetik berperan penting. Pemicu termasuk infeksi, cedera kulit, stres, merokok, konsumsi alkohol, dan obat-obatan tertentu.",
        "penanganan_awal": [
            "Jaga kelembaban kulit dengan pelembab tebal",
            "Hindari menggaruk atau menggosok kulit",
            "Kelola stres dengan baik (meditasi, olahraga ringan)",
            "Hindari alkohol dan rokok",
            "Ekspos sinar matahari pagi secara terbatas (10-15 menit)",
            "Mandi dengan garam epsom atau oatmeal koloid"
        ],
        "sumber": "American Academy of Dermatology, Mayo Clinic, CDC"
    },
    "P03": {
        "nama": "Tinea (Kurap / Ringworm)",
        "deskripsi": "Tinea atau kurap adalah infeksi jamur pada kulit yang membentuk bercak melingkar seperti cincin dengan tepi yang lebih merah dan kulit bersisik di bagian tengah. Sangat menular dan dapat menyebar ke bagian tubuh lain.",
        "penyebab": "Infeksi jamur dermatofita (Trichophyton, Microsporum, Epidermophyton). Penularan melalui kontak langsung dengan manusia, hewan (kucing, anjing), atau benda yang terkontaminasi (handuk, pakaian, lantai kolam renang).",
        "penanganan_awal": [
            "Jaga kebersihan dan kekeringan kulit (jamur menyukai tempat lembab)",
            "Ganti pakaian, handuk, dan seprai setiap hari",
            "Hindari berbagi barang pribadi dengan orang lain",
            "Cuci tangan setelah menyentuh area yang terinfeksi",
            "Hindari menggaruk agar tidak menyebar ke area lain"
        ],
        "sumber": "CDC, WHO, Mayo Clinic"
    },
    "P04": {
        "nama": "Skabies (Kudis)",
        "deskripsi": "Skabies adalah infeksi kulit yang disebabkan oleh tungau Sarcoptes scabiei. Tungau menggali terowongan di bawah permukaan kulit dan bertelur, menyebabkan gatal hebat terutama pada malam hari.",
        "penyebab": "Infeksi tungau Sarcoptes scabiei var hominis. Penularan melalui kontak kulit langsung yang lama (minimal 10-15 menit) atau berbagi pakaian, handuk, dan tempat tidur dengan orang yang terinfeksi.",
        "penanganan_awal": [
            "Konsultasi dokter untuk mendapatkan pengobatan yang tepat",
            "Cuci semua pakaian, handuk, dan seprai dengan air panas (>60°C)",
            "Semua anggota keluarga harus diperiksa bersamaan",
            "Hindari kontak fisik langsung sampai pengobatan selesai",
            "Vakum lantai dan furnitur untuk menghilangkan tungau"
        ],
        "sumber": "CDC, WHO, American Academy of Dermatology"
    },
    "P05": {
        "nama": "Acne Vulgaris (Jerawat)",
        "deskripsi": "Acne vulgaris adalah kondisi kulit umum yang terjadi ketika folikel rambut tersumbat oleh minyak (sebum) dan sel kulit mati, menyebabkan komedo, papula, pustula, atau nodul.",
        "penyebab": "Produksi sebum berlebih, penyumbatan folikel rambut, bakteri Propionibacterium acnes, peradangan, perubahan hormon (pubertas, menstruasi, kehamilan), faktor genetik, stres.",
        "penanganan_awal": [
            "Cuci wajah 2 kali sehari dengan pembersih lembut",
            "Gunakan produk perawatan kulit non-komedogenik",
            "Hindari memencet atau menyentuh jerawat",
            "Hindari produk berbasis minyak (oil-based)",
            "Kurangi konsumsi makanan manis dan berlemak"
        ],
        "sumber": "American Academy of Dermatology, Mayo Clinic"
    },
    "P06": {
        "nama": "Urtikaria (Biduran / Kaligata)",
        "deskripsi": "Urtikaria atau biduran adalah reaksi alergi yang menyebabkan bentol merah (wheal) yang gatal pada kulit. Bentol dapat muncul tiba-tiba, berubah bentuk, dan hilang dalam beberapa jam.",
        "penyebab": "Reaksi alergi terhadap makanan (kerang, kacang, telur), obat-obatan, gigitan serangga, lateks, infeksi, stres, paparan panas/dingin, tekanan pada kulit, atau cahaya matahari.",
        "penanganan_awal": [
            "Identifikasi dan hindari pemicu alergi",
            "Kompres dingin untuk mengurangi gatal",
            "Mandi dengan air hangat (bukan panas)",
            "Kenakan pakaian longgar dan berbahan lembut",
            "Hindari alkohol dan makanan pemicu alergi"
        ],
        "sumber": "American Academy of Dermatology, Mayo Clinic"
    }
}

def forward_chaining(fakta: List[str]) -> Dict[str, List[Dict]]:
    hasil = defaultdict(list)
    for rule in RULES:
        if all(kondisi in fakta for kondisi in rule["conditions"]):
            hasil[rule["penyakit"]].append(rule)
    return dict(hasil)

def format_fakta(fakta: List[str]) -> str:
    nama = []
    for f in fakta:
        if f in GEJALA:
            nama.append(GEJALA[f])
        else:
            nama.append(f)
    return ", ".join(nama)

def get_gejala_dari_fakta(fakta: List[str]) -> List[str]:
    return [f for f in fakta if f in GEJALA]

def load_css():
    st.markdown("""
    <style>
        .main { padding: 0rem 1rem; }
        .hero {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            padding: 2rem;
            border-radius: 20px;
            margin-bottom: 2rem;
            color: white;
            text-align: center;
        }
        .step-card {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 1.5rem;
            border-radius: 15px;
            text-align: center;
            margin: 0.5rem;
            transition: transform 0.3s;
        }
        .step-card:hover { transform: translateY(-5px); }
        .step-number {
            background: #2a5298;
            color: white;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            margin-bottom: 1rem;
        }
        .area-card {
            background: white;
            border: 2px solid #e0e0e0;
            border-radius: 12px;
            padding: 1rem;
            text-align: center;
            transition: all 0.3s;
            margin: 0.5rem;
        }
        .area-card:hover {
            border-color: #2a5298;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .result-card {
            background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
            padding: 1.5rem;
            border-radius: 15px;
            margin: 1rem 0;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        .disease-card {
            background: white;
            border-radius: 15px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
            border-left: 5px solid #2a5298;
        }
        .rule-item {
            background: #f0f2f6;
            padding: 0.75rem;
            border-radius: 8px;
            margin: 0.5rem 0;
            font-family: monospace;
        }
        .badge {
            background: #2a5298;
            color: white;
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.8rem;
            display: inline-block;
            margin: 0.25rem;
        }
        .badge-inti {
            background: #28a745;
        }
        .sumber {
            font-size: 0.8rem;
            color: #666;
            font-style: italic;
            margin-top: 1rem;
            padding-top: 0.5rem;
            border-top: 1px solid #eee;
        }
        .diagnose-btn {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            border: none;
            padding: 0.75rem 2rem;
            border-radius: 30px;
            font-weight: bold;
            width: 100%;
            margin-top: 1rem;
        }
        hr { margin: 2rem 0; }
        .forward-chain {
            background: #e8f4f8;
            padding: 1rem;
            border-radius: 10px;
            margin: 1rem 0;
            border-left: 4px solid #2a5298;
        }
        .area-info {
            background: #d4edda;
            padding: 0.5rem 1rem;
            border-radius: 10px;
            margin-bottom: 1rem;
        }
    </style>
    """, unsafe_allow_html=True)

def main():
    st.set_page_config(
        page_title="Sistem Pakar Diagnosa Penyakit Kulit - Forward Chaining",
        layout="wide"
    )
    load_css()

    st.markdown("""
    <div class="hero">
        <h1>SISTEM PAKAR DIAGNOSA PENYAKIT KULIT</h1>
        <p style="font-size: 1.2rem; margin-top: 1rem;">
            Metode <strong>Forward Chaining</strong> | IF-THEN Rules | Rule-Based Expert System
        </p>
        <p style="margin-top: 0.5rem; opacity: 0.9;">
            Sistem ini hanya untuk tujuan edukasi dan diagnosis awal, bukan pengganti konsultasi dengan dokter spesialis kulit.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="step-card">
            <div class="step-number">1</div>
            <h3>Pilih Area Tubuh</h3>
            <p>Pilih area yang mengalami keluhan</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="step-card">
            <div class="step-number">2</div>
            <h3>Pilih Gejala</h3>
            <p>Pilih semua gejala yang dialami</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="step-card">
            <div class="step-number">3</div>
            <h3>Forward Chaining</h3>
            <p>Mesin inferensi mencocokkan dengan rule base</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    if 'selected_area' not in st.session_state:
        st.session_state.selected_area = None
    if 'selected_gejala' not in st.session_state:
        st.session_state.selected_gejala = []

    st.subheader("STEP 1: Pilih Area Tubuh")
    st.markdown("Pilih area yang paling sesuai dengan keluhan Anda (gejala akan difilter sesuai area):")

    area_list = ["Wajah", "Kulit Kepala", "Tangan & Kaki", "Badan", "Seluruh Tubuh"]
    cols = st.columns(3)
    for idx, area in enumerate(area_list):
        col_idx = idx % 3
        with cols[col_idx]:
            is_selected = st.session_state.selected_area == area
            if st.button(f"{area}", key=f"area_{area}", use_container_width=True):
                st.session_state.selected_area = area
                st.session_state.selected_gejala = []
                st.rerun()
            if is_selected:
                st.caption("✓ Terpilih")

    st.markdown("<hr>", unsafe_allow_html=True)

    st.subheader("STEP 2: Pilih Gejala yang Dialami")

    if st.session_state.selected_area:
        st.markdown(f"""
        <div class="area-info">
            Area terpilih: <strong>{st.session_state.selected_area}</strong><br>
            Menampilkan gejala yang relevan untuk area tersebut.
        </div>
        """, unsafe_allow_html=True)

        gejala_relevan_kode = GEJALA_AREA.get(st.session_state.selected_area, [])
        gejala_relevan = [(k, GEJALA[k]) for k in gejala_relevan_kode if k in GEJALA]

        cols = st.columns(3)
        selected_gejala = []
        for idx, (kode, nama) in enumerate(gejala_relevan):
            col_idx = idx % 3
            with cols[col_idx]:
                if st.checkbox(f"{kode} - {nama}", key=f"gejala_{kode}", value=kode in st.session_state.selected_gejala):
                    selected_gejala.append(kode)
        st.session_state.selected_gejala = selected_gejala

        if st.session_state.selected_gejala:
            st.info(f"✓ {len(st.session_state.selected_gejala)} gejala dipilih untuk area {st.session_state.selected_area}")
        else:
            st.warning("Belum ada gejala yang dipilih. Silakan pilih gejala yang Anda alami.")
    else:
        st.info("Silakan pilih area tubuh terlebih dahulu untuk melihat daftar gejala yang relevan.")

    st.markdown("<hr>", unsafe_allow_html=True)

    st.subheader("STEP 3: Forward Chaining - Proses Diagnosa")

    col_btn, col_reset = st.columns([3, 1])
    with col_btn:
        diagnose_clicked = st.button("🩺 JALANKAN FORWARD CHAINING", use_container_width=True, type="primary")
    with col_reset:
        if st.button("Reset Semua", use_container_width=True):
            st.session_state.selected_area = None
            st.session_state.selected_gejala = []
            st.rerun()

    if diagnose_clicked:
        if not st.session_state.selected_area:
            st.error("Silakan pilih area tubuh terlebih dahulu.")
        elif not st.session_state.selected_gejala:
            st.error("Silakan pilih setidaknya satu gejala terlebih dahulu sebelum melakukan diagnosa.")
        else:
            fakta = st.session_state.selected_gejala
            hasil_raw = forward_chaining(fakta)

            with st.expander("🔍 Trace Forward Chaining (Proses Pencocokan Rule)", expanded=False):
                st.markdown("""
                <div class="forward-chain">
                    <b>Alur Forward Chaining:</b><br>
                    Fakta (Gejala) → Cocokkan dengan Rule Base → Rule Terpenuhi → Kesimpulan
                </div>
                """, unsafe_allow_html=True)
                st.markdown(f"**Fakta yang diketahui:** {format_fakta(fakta)}")
                st.markdown("**Penelusuran semua rule (✓ terpenuhi, ✗ tidak):**")
                for rule in RULES:
                    kondisi_terpenuhi = all(k in fakta for k in rule["conditions"])
                    status = "✓" if kondisi_terpenuhi else "✗"
                    kondisi_str = " ∧ ".join([GEJALA.get(k, k) for k in rule["conditions"]])
                    inti_tag = " [INTI]" if rule.get("inti", False) else ""
                    st.markdown(f"{status} **{rule['id']}**{inti_tag}: IF {kondisi_str} THEN {PENYAKIT[rule['penyakit']]['nama']}")

            hasil_filter = {}
            for kode_penyakit, rules in hasil_raw.items():
                if any(r.get("inti", False) for r in rules):
                    hasil_filter[kode_penyakit] = rules

            if hasil_filter:
                sorted_hasil = sorted(hasil_filter.items(), key=lambda x: len(x[1]), reverse=True)

                st.markdown("""
                <div class="result-card">
                    <h2 style="color: #1e3c72; margin:0;">✓ HASIL DIAGNOSA</h2>
                    <p style="color: #1e3c72;">Berdasarkan fakta yang dipilih, berikut kemungkinan penyakit dengan gejala inti terpenuhi:</p>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"**Area Keluhan:** {st.session_state.selected_area}")

                for penyakit_kode, rules in sorted_hasil:
                    penyakit = PENYAKIT[penyakit_kode]
                    
                    st.markdown(f"""
                    <div class="disease-card">
                        <h2>{penyakit['nama']}</h2>
                        <div><span class="badge">{len(rules)} rule terpenuhi</span></div>
                    """, unsafe_allow_html=True)
                    
                    st.info(f"**Deskripsi:** {penyakit['deskripsi']}")
                    st.warning(f"**Penyebab:** {penyakit['penyebab']}")
                    st.success(f"**Penanganan Awal:**\n" + "\n".join([f"- {p}" for p in penyakit['penanganan_awal']]))
                    
                    st.markdown("""
                        <div style="background-color: #f5f5f5; padding: 0.75rem; border-radius: 8px; border-left: 3px solid #999; margin: 1rem 0;">
                            <p style="font-size: 0.75rem; color: #555; margin: 0;">
                                ⚠️ <strong>DISCLAIMER PENTING</strong><br>
                                Sistem ini hanya memberikan diagnosis awal berdasarkan gejala yang dipilih.<br>
                                Diagnosis ini <strong>bukan pengganti konsultasi dengan dokter spesialis kulit (dermatovenereologist)</strong>.<br>
                                Silakan konsultasikan hasil ini dengan tenaga medis profesional.
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    gejala_terpilih = get_gejala_dari_fakta(fakta)
                    st.markdown("**Gejala yang Dipilih:**")
                    for g in gejala_terpilih:
                        st.markdown(f"- ✓ {GEJALA[g]}")
                    
                    st.markdown("**Rule yang Terpenuhi (IF-THEN):**")
                    for rule in rules:
                        kondisi_str = " ∧ ".join([GEJALA.get(k, k) for k in rule["conditions"]])
                        inti_badge = '<span class="badge badge-inti" style="background:#28a745;">INTI</span> ' if rule.get("inti", False) else ''
                        st.markdown(f"""
                        <div class="rule-item">
                            <b>{rule['id']}</b> {inti_badge}<br>
                            <code>IF {kondisi_str} THEN {penyakit['nama']}</code><br>
                            <span style="font-size:0.85rem;">{rule['deskripsi']}</span>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div class="sumber">
                         Sumber: {penyakit['sumber']}
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)

                if len(sorted_hasil) > 1:
                    st.info(" **Catatan:** Beberapa kemungkinan diagnosis ditemukan. Urutan di atas berdasarkan jumlah rule yang terpenuhi (semakin banyak rule, semakin kuat kecocokan). Konsultasikan dengan dokter untuk diagnosis pasti.")
            else:
                st.markdown("""
                <div style="background: #fff3cd; border-left: 5px solid #ffc107; padding: 1.5rem; border-radius: 10px; margin: 1rem 0;">
                    <h3 style="color: #856404; margin:0;">⚠️ Belum Ditemukan Penyakit dengan Gejala Inti</h3>
                    <p style="color: #856404; margin-top: 0.5rem;">Tidak ada penyakit yang memenuhi gejala inti berdasarkan fakta yang dipilih.</p>
                </div>
                """, unsafe_allow_html=True)
                st.markdown(f" **Area Keluhan:** {st.session_state.selected_area}")
                with st.expander(" Lihat Gejala yang Dipilih", expanded=True):
                    gejala_fakta = [f"{k} - {GEJALA[k]}" for k in st.session_state.selected_gejala]
                    for g in gejala_fakta:
                        st.markdown(f"- {g}")
                    st.info("💡 **Saran:** Konsultasikan gejala yang Anda alami dengan dokter spesialis kulit.")

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p> <strong>Sistem Pakar Diagnosa Penyakit Kulit</strong> | Metode <strong>Forward Chaining</strong> | IF-THEN Rule Base</p>
        <p> Referensi: WHO, CDC, Mayo Clinic, American Academy of Dermatology (AAD), National Eczema Association</p>
        <p>© 2026 - Sistem Pakar - KELOMPOK 3</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
