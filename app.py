# File: main_app.py (untuk aplikasi utama seperti serverliveupdate12.streamlit.app)
import streamlit as st
import requests
import json
import urllib.parse

st.set_page_config(page_title="YouTube Live Streaming", layout="wide")

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

REDIRECT_APP_URL = "https://redirect1x.streamlit.app"

st.title("🎥 YouTube Live Streaming Platform")

# Cek apakah ada token yang dikirim dari redirect app
if 'tokens' in st.query_params:
    tokens_json = st.query_params['tokens']
    try:
        tokens = json.loads(urllib.parse.unquote(tokens_json))
        st.session_state['youtube_tokens'] = tokens
        st.success("✅ Berhasil terhubung ke YouTube!")
        # Hapus parameter tokens dari URL
        st.query_params.clear()
        st.rerun()  # Refresh untuk membersihkan URL
    except Exception as e:
        st.error(f"❌ Gagal memproses token: {str(e)}")

# Tampilkan tombol auth jika belum terautentikasi
if 'youtube_tokens' not in st.session_state:
    st.subheader("🔐 Autentikasi YouTube")
    
    # Dapatkan URL aplikasi saat ini
    try:
        import os
        host = os.environ.get('HOST', '')
        if host:
            current_app_url = f"https://{host}"
        else:
            current_app_url = f"https://{st.context.headers.get('Host', '')}" if hasattr(st, 'context') and hasattr(st.context, 'headers') else ''
    except:
        current_app_url = ''
    
    # Method fallback: input manual
    if not current_app_url:
        user_url = st.text_input("Masukkan URL aplikasi ini", 
                               placeholder="serverliveupdate12.streamlit.app",
                               help="Contoh: serverliveupdate12.streamlit.app")
        if user_url:
            user_url = user_url.replace('https://', '').replace('http://', '').split('/')[0]
            current_app_url = f"https://{user_url}"
    
    if current_app_url:
        # Bersihkan URL
        clean_host = current_app_url.replace('https://', '').replace('http://', '').split('/')[0]
        current_app_url = f"https://{clean_host}"
        
        st.info(f"URL aplikasi: {current_app_url}")
        
        # Gunakan parameter state untuk membawa URL aplikasi
        scopes = ['https://www.googleapis.com/auth/youtube.force-ssl']
        encoded_state = urllib.parse.quote(current_app_url)
        
        auth_url = (
            f"{PREDEFINED_OAUTH_CONFIG['web']['auth_uri']}?"
            f"client_id={PREDEFINED_OAUTH_CONFIG['web']['client_id']}&"
            f"redirect_uri={urllib.parse.quote(PREDEFINED_OAUTH_CONFIG['web']['redirect_uris'][0])}&"
            f"scope={urllib.parse.quote(' '.join(scopes))}&"
            f"response_type=code&"
            f"access_type=offline&"
            f"prompt=consent&"
            f"state={encoded_state}"
        )
        
        st.markdown(f"""
        ### Langkah Autentikasi:
        1. Klik tombol di bawah untuk otorisasi
        2. Login ke akun YouTube Anda  
        3. Izinkan akses aplikasi
        4. Anda akan otomatis kembali ke sini
        
        [🔐 Otorisasi YouTube]({auth_url})
        """)
    else:
        st.warning("📝 Masukkan URL aplikasi Anda")
else:
    st.success("✅ Sudah terautentikasi!")
    
    # Tampilkan info token untuk debugging
    with st.expander("🔧 Token Info"):
        st.json(st.session_state['youtube_tokens'])
    
    if st.button("🔄 Logout"):
        keys_to_delete = ['youtube_tokens']
        for key in keys_to_delete:
            if key in st.session_state:
                del st.session_state[key]
        st.query_params.clear()
        st.rerun()

# Konten utama
st.markdown("---")
st.header("📺 Konten Streaming")
st.write("Platform streaming YouTube Live siap digunakan!")
