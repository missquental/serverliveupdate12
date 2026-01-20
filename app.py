# File: main_app.py (untuk aplikasi utama)
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
        # Decode dan parse tokens
        decoded_tokens = urllib.parse.unquote(tokens_json)
        tokens = json.loads(decoded_tokens)
        st.session_state['youtube_tokens'] = tokens
        st.success("✅ Successfully connected to YouTube!")
        
        # HAPUS parameter tokens dari URL untuk mencegah loop
        st.query_params.clear()
        
        # Refresh halaman untuk membersihkan URL
        st.components.v1.html("""
            <script>
                setTimeout(function() {
                    window.location.href = window.location.pathname;
                }, 2000);
            </script>
        """, height=0)
        
    except Exception as e:
        st.error(f"❌ Failed to process token: {str(e)}")

# Tampilkan tombol auth jika belum terautentikasi
if 'youtube_tokens' not in st.session_state:
    st.subheader("🔐 YouTube Authentication")
    
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
    
    # Fallback: input manual
    if not current_app_url:
        user_url = st.text_input("Enter your app URL", 
                               placeholder="serverliveupdate12.streamlit.app")
        if user_url:
            user_url = user_url.replace('https://', '').replace('http://', '').split('/')[0]
            current_app_url = f"https://{user_url}"
    
    if current_app_url:
        # Bersihkan URL
        clean_host = current_app_url.replace('https://', '').replace('http://', '').split('/')[0]
        current_app_url = f"https://{clean_host}"
        
        st.info(f"App URL: {current_app_url}")
        
        # Generate auth URL dengan state parameter
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
        ### Authentication Steps:
        1. Click the button below to authorize
        2. Login to your YouTube account  
        3. Grant app access
        4. You'll be redirected back automatically
        
        [🔐 Authorize YouTube]({auth_url})
        """)
    else:
        st.warning("📝 Enter your app URL to continue")
else:
    st.success("✅ Already authenticated!")
    
    # Tampilkan token info (untuk debugging)
    with st.expander("🔧 Token Info"):
        st.json(st.session_state['youtube_tokens'])
    
    if st.button("🔄 Logout"):
        # Hapus session state
        keys_to_delete = ['youtube_tokens']
        for key in keys_to_delete:
            if key in st.session_state:
                del st.session_state[key]
        # Bersihkan URL
        st.query_params.clear()
        st.rerun()

# Konten utama
st.markdown("---")
st.header("📺 Streaming Content")
st.write("YouTube Live Streaming platform is ready!")
