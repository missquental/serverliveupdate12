# File: main_app.py (untuk livenews2x.streamlit.app)
import streamlit as st
import requests
import json
import urllib.parse

st.set_page_config(page_title="YouTube Live Streaming", layout="wide")

# Fungsi untuk generate auth URL dengan referer
def generate_auth_url(client_config, referer_url):
    import urllib.parse
    scopes = ['https://www.googleapis.com/auth/youtube.force-ssl']
    # Tambahkan parameter referer ke redirect URI
    redirect_with_referer = f"{client_config['redirect_uris'][0]}?referer={urllib.parse.quote(referer_url)}"
    
    auth_url = (
        f"{client_config['auth_uri']}?"
        f"client_id={client_config['client_id']}&"
        f"redirect_uri={urllib.parse.quote(client_config['redirect_uris'][0])}&"
        f"scope={urllib.parse.quote(' '.join(scopes))}&"
        f"response_type=code&"
        f"access_type=offline&"
        f"prompt=consent"
    )
    return auth_url

# Konfigurasi OAuth
PREDEFINED_OAUTH_CONFIG = {
    "web": {
        "client_id": "1086578184958-hin4d45sit9ma5psovppiq543eho41sl.apps.googleusercontent.com",
        "project_id": "anjelikakozme",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": "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",
        "redirect_uris": ["https://redirect1x.streamlit.app"]
    }
}

st.title("🎥 YouTube Live Streaming Platform")

# Cek apakah ada token yang dikirim dari redirect app
if 'tokens' in st.query_params:
    tokens_json = st.query_params['tokens']
    try:
        tokens = json.loads(tokens_json)
        st.session_state['youtube_tokens'] = tokens
        st.success("✅ Berhasil terhubung ke YouTube!")
        st.query_params.clear()  # Bersihkan URL
    except:
        st.error("❌ Gagal memproses token")

# Tampilkan tombol auth jika belum terautentikasi
if 'youtube_tokens' not in st.session_state:
    st.subheader("🔐 Autentikasi YouTube")
    
    # Dapatkan URL aplikasi saat ini
    current_app_url = "https://redirect1x.streamlit.app"  # Bisa juga dideteksi otomatis
    
    # Generate auth URL dengan referer
    auth_url = generate_auth_url(PREDEFINED_OAUTH_CONFIG['web'], current_app_url)
    
    st.markdown(f"""
    ### Langkah Autentikasi:
    1. Klik tombol di bawah untuk membuka halaman otorisasi
    2. Login ke akun YouTube Anda
    3. Izinkan akses ke aplikasi
    4. Anda akan dialihkan ke aplikasi redirect
    5. Token akan dikirim kembali ke sini secara otomatis
    
    [🔐 Klik untuk Otorisasi YouTube]({auth_url})
    """)
    
    st.info("Setelah otorisasi selesai, Anda akan otomatis kembali ke halaman ini dengan token yang sudah diproses.")

else:
    st.success("✅ Sudah terautentikasi!")
    if st.button("🔄 Logout"):
        del st.session_state['youtube_tokens']
        st.rerun()

# Konten utama aplikasi
st.markdown("---")
st.header("📺 Konten Streaming")
# ... (konten aplikasi utama Anda)
