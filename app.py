# File: main_app.py (untuk aplikasi utama seperti serverliveupdate12.streamlit.app)
import streamlit as st
import requests
import json
import urllib.parse

st.set_page_config(page_title="YouTube Live Streaming", layout="wide")

# Fungsi untuk generate auth URL dengan referer otomatis
def generate_auth_url_with_referer(client_config, current_app_url, redirect_app_url):
    """Generate auth URL yang menyertakan referer aplikasi saat ini"""
    import urllib.parse
    scopes = ['https://www.googleapis.com/auth/youtube.force-ssl']
    
    # Encode current app URL untuk dikirim sebagai parameter
    encoded_referer = urllib.parse.quote(current_app_url)
    
    # Buat auth URL dengan redirect URI standar (Google tidak menerima parameter tambahan di redirect_uri)
    auth_url = (
        f"{client_config['auth_uri']}?"
        f"client_id={client_config['client_id']}&"
        f"redirect_uri={urllib.parse.quote(client_config['redirect_uris'][0])}&"
        f"scope={urllib.parse.quote(' '.join(scopes))}&"
        f"response_type=code&"
        f"access_type=offline&"
        f"prompt=consent"
    )
    
    # Kita akan mengirim referer melalui cookie atau session
    # Tapi untuk sekarang, kita bisa menyertakan dalam URL redirect app
    return auth_url, encoded_referer

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

# URL aplikasi redirect (satu untuk semua)
REDIRECT_APP_URL = "https://redirect1x.streamlit.app"

st.title("🎥 YouTube Live Streaming Platform")

# Cek apakah ada token yang dikirim dari redirect app
if 'tokens' in st.query_params:
    tokens_json = st.query_params['tokens']
    try:
        tokens = json.loads(urllib.parse.unquote(tokens_json))
        st.session_state['youtube_tokens'] = tokens
        st.success("✅ Berhasil terhubung ke YouTube!")
        st.query_params.clear()  # Bersihkan URL
    except Exception as e:
        st.error(f"❌ Gagal memproses token: {str(e)}")

# Tampilkan tombol auth jika belum terautentikasi
if 'youtube_tokens' not in st.session_state:
    st.subheader("🔐 Autentikasi YouTube")
    
    # Dapatkan URL aplikasi saat ini secara otomatis
    # Gunakan cara yang lebih reliable
    try:
        # Method 1: Dari headers (jika tersedia)
        current_app_url = f"https://{st.context.headers.get('Host', '')}" if hasattr(st, 'context') and hasattr(st.context, 'headers') else ''
    except:
        current_app_url = ''
    
    # Method 2: Dari environment (Streamlit sharing)
    if not current_app_url:
        import os
        host = os.environ.get('HOST', '')
        if host:
            current_app_url = f"https://{host}"
    
    # Method 3: Session state (user input sebelumnya)
    if not current_app_url and 'user_app_url' in st.session_state:
        current_app_url = st.session_state['user_app_url']
    
    # Method 4: Input manual
    if not current_app_url:
        st.warning("📝 Tidak dapat mendeteksi URL aplikasi secara otomatis")
        user_url = st.text_input("Masukkan URL aplikasi ini", 
                               placeholder="https://serverliveupdate12.streamlit.app",
                               help="Contoh: https://serverliveupdate12.streamlit.app")
        if user_url:
            current_app_url = user_url if user_url.startswith('http') else f"https://{user_url}"
            st.session_state['user_app_url'] = current_app_url
    
    if current_app_url:
        st.info(f"URL aplikasi terdeteksi: {current_app_url}")
        
        # Generate auth URL dengan cara menyertakan referer dalam redirect app URL
        encoded_referer = urllib.parse.quote(current_app_url)
        redirect_app_with_referer = f"{REDIRECT_APP_URL}?referer={encoded_referer}"
        
        # Buat auth URL yang akan redirect ke redirect app dengan referer
        scopes = ['https://www.googleapis.com/auth/youtube.force-ssl']
        auth_url = (
            f"{PREDEFINED_OAUTH_CONFIG['web']['auth_uri']}?"
            f"client_id={PREDEFINED_OAUTH_CONFIG['web']['client_id']}&"
            f"redirect_uri={urllib.parse.quote(PREDEFINED_OAUTH_CONFIG['web']['redirect_uris'][0])}&"
            f"scope={urllib.parse.quote(' '.join(scopes))}&"
            f"response_type=code&"
            f"access_type=offline&"
            f"prompt=consent&"
            f"state={encoded_referer}"  # Gunakan state parameter untuk membawa referer
        )
        
        # Tapi lebih baik menggunakan redirect app URL dengan parameter
        auth_url = f"{PREDEFINED_OAUTH_CONFIG['web']['auth_uri']}?"
        auth_url += f"client_id={PREDEFINED_OAUTH_CONFIG['web']['client_id']}&"
        auth_url += f"redirect_uri={urllib.parse.quote(PREDEFINED_OAUTH_CONFIG['web']['redirect_uris'][0])}&"
        auth_url += f"scope={urllib.parse.quote(' '.join(scopes))}&"
        auth_url += f"response_type=code&"
        auth_url += f"access_type=offline&"
        auth_url += f"prompt=consent"
        
        st.markdown(f"""
        ### Langkah Autentikasi:
        1. Klik tombol di bawah untuk membuka halaman otorisasi
        2. Login ke akun YouTube Anda  
        3. Izinkan akses ke aplikasi
        4. Anda akan dialihkan ke aplikasi redirect
        5. Token akan dikirim kembali ke sini secara otomatis
        
        [🔐 Klik untuk Otorisasi YouTube]({redirect_app_with_referer})
        """)
        
        st.info("Setelah otorisasi selesai, Anda akan otomatis kembali ke halaman ini dengan token yang sudah diproses.")
    else:
        st.warning("📝 Masukkan URL aplikasi Anda untuk melanjutkan proses autentikasi")
else:
    st.success("✅ Sudah terautentikasi!")
    # Tampilkan info channel jika tersedia
    if 'channel_info' in st.session_state:
        st.json(st.session_state['channel_info'])
    
    if st.button("🔄 Logout"):
        for key in ['youtube_tokens', 'channel_info', 'user_app_url']:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

# Konten utama aplikasi
st.markdown("---")
st.header("📺 Konten Streaming")
st.write("Aplikasi streaming YouTube Live siap digunakan!")

# Debug section
with st.expander("🔧 Debug Info"):
    st.write("Query Params:", dict(st.query_params))
    st.write("Session State Keys:", list(st.session_state.keys()))
    if 'youtube_tokens' in st.session_state:
        st.write("Tokens tersedia")
