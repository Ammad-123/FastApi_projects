import streamlit as st
import requests
import base64
import urllib.parse
from datetime import datetime
from PIL import Image
import io

# Page configuration
st.set_page_config(
    page_title="Simple Social",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .card {
        background: white;
        padding: 1.2rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
        border: 1px solid #e0e0e0;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    }
    .user-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .post-media-container {
        border-radius: 8px;
        overflow: hidden;
        margin: 0.8rem 0;
        text-align: center;
    }
    .post-image {
        max-width: 100%;
        max-height: 400px;
        border-radius: 8px;
        object-fit: contain;
    }
    .post-video {
        max-width: 100%;
        max-height: 400px;
        border-radius: 8px;
    }
    .stButton button {
        border-radius: 6px;
        font-weight: 500;
        font-size: 0.9rem;
        transition: all 0.2s ease;
    }
    .stButton button:hover {
        transform: translateY(-1px);
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    .success-message {
        background: #d4edda;
        color: #155724;
        padding: 10px;
        border-radius: 6px;
        border: 1px solid #c3e6cb;
        margin: 8px 0;
        font-size: 0.9rem;
    }
    .error-message {
        background: #f8d7da;
        color: #721c24;
        padding: 10px;
        border-radius: 6px;
        border: 1px solid #f5c6cb;
        margin: 8px 0;
        font-size: 0.9rem;
    }
    .caption-text {
        font-size: 14px;
        line-height: 1.4;
        margin: 8px 0;
        padding: 8px 12px;
        background: #f8f9fa;
        border-radius: 6px;
        border-left: 3px solid #667eea;
    }
    .user-info {
        font-size: 1rem;
        font-weight: 600;
        color: #333;
        margin-bottom: 0.2rem;
    }
    .timestamp {
        font-size: 0.8rem;
        color: #666;
        margin-bottom: 0.5rem;
    }
    .post-actions {
        margin-top: 0.5rem;
        padding-top: 0.5rem;
        border-top: 1px solid #f0f0f0;
    }
    .preview-container {
        border: 2px dashed #ddd;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        margin: 15px 0;
        background: #fafafa;
    }
    .preview-image {
        max-width: 100%;
        max-height: 300px;
        border-radius: 8px;
        margin: 10px auto;
    }
    .file-info {
        background: #e9ecef;
        padding: 8px 12px;
        border-radius: 6px;
        font-size: 0.9rem;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'token' not in st.session_state:
    st.session_state.token = None
if 'user' not in st.session_state:
    st.session_state.user = None
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None

def get_headers():
    """Get authorization headers with token"""
    if st.session_state.token:
        return {"Authorization": f"Bearer {st.session_state.token}"}
    return {}

def display_file_preview(uploaded_file):
    """Display preview of the uploaded file"""
    if uploaded_file is None:
        return
    
    st.markdown("### 📸 Preview")
    
    # File information
    file_size = len(uploaded_file.getvalue()) / 1024  # Size in KB
    st.markdown(f'<div class="file-info">📁 {uploaded_file.name} | 🗂️ {uploaded_file.type} | 📊 {file_size:.1f} KB</div>', unsafe_allow_html=True)
    
    # Display preview based on file type
    if uploaded_file.type.startswith('image/'):
        try:
            # Display image preview
            image = Image.open(uploaded_file)
            st.image(image, caption="Image Preview", use_container_width=False, width=400)
            
            # Reset file pointer to beginning for upload
            uploaded_file.seek(0)
        except Exception as e:
            st.error(f"Error previewing image: {str(e)}")
    
    elif uploaded_file.type.startswith('video/'):
        # Display video preview
        st.video(uploaded_file.getvalue())
        st.info("🎥 Video file selected - preview will play after upload")
        
        # Reset file pointer to beginning for upload
        uploaded_file.seek(0)
    
    else:
        st.warning("⚠️ File type preview not supported")

def upload_page():
    st.markdown('<h1 class="main-header">📸 Share Your Moment</h1>', unsafe_allow_html=True)
    
    with st.container():
        col1, col2 = st.columns([2, 1])
        
        with col1:
            with st.form("upload_form", clear_on_submit=True):
                st.markdown("### Create New Post")
                
                uploaded_file = st.file_uploader(
                    "📁 Choose media file", 
                    type=['png', 'jpg', 'jpeg', 'mp4', 'avi', 'mov', 'mkv', 'webm'],
                    help="Supported formats: Images (PNG, JPG, JPEG) and Videos (MP4, AVI, MOV, MKV, WEBM)",
                    key="file_uploader"
                )
                
                # Show preview if file is selected
                if uploaded_file is not None:
                    display_file_preview(uploaded_file)
                
                caption = st.text_area(
                    "💭 Caption", 
                    placeholder="What's happening? Share your thoughts...",
                    height=80,
                    key="upload_caption"
                )
                
                submit_btn = st.form_submit_button(
                    "🚀 Share Post", 
                    type="primary",
                    use_container_width=True
                )
                
                if submit_btn and uploaded_file:
                    with st.spinner("Uploading your post..."):
                        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                        data = {"caption": caption}
                        
                        try:
                            response = requests.post(
                                "http://localhost:8000/upload", 
                                files=files, 
                                data=data, 
                                headers=get_headers(),
                                timeout=30
                            )

                            if response.status_code == 200:
                                st.markdown('<div class="success-message">✅ Post shared successfully!</div>', unsafe_allow_html=True)
                                st.balloons()
                                # Clear the file uploader after successful upload
                                st.session_state.file_uploader = None
                                st.rerun()
                            else:
                                error_msg = response.json().get('detail', 'Upload failed')
                                st.markdown(f'<div class="error-message">❌ Upload failed: {error_msg}</div>', unsafe_allow_html=True)
                        except requests.exceptions.RequestException as e:
                            st.markdown(f'<div class="error-message">❌ Network error: {str(e)}</div>', unsafe_allow_html=True)
                
                elif submit_btn and not uploaded_file:
                    st.markdown('<div class="error-message">⚠️ Please select a file to upload</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown("### 📋 Upload Guidelines")
            st.info("""
            **Supported Formats:**
            - **Images:** PNG, JPG, JPEG
            - **Videos:** MP4, AVI, MOV, MKV, WEBM
            
            **Tips:**
            - Use high-quality media
            - Add engaging captions
            - Keep file size reasonable
            - Max file size: 200MB
            """)
            
            # Quick tips
            st.markdown("### 💡 Quick Tips")
            st.markdown("""
            - **Images:** Best results with square or 4:3 ratio
            - **Videos:** Keep under 2 minutes for best engagement
            - **Captions:** Add context to your media
            - **Hashtags:** Use relevant hashtags in captions
            """)

def feed_page():
    st.markdown('<h1 class="main-header">🏠 Your Feed</h1>', unsafe_allow_html=True)
    
    # Refresh button
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🔄 Refresh Feed", use_container_width=True):
            st.rerun()
    
    # Load posts
    with st.spinner("Loading your feed..."):
        try:
            response = requests.get("http://localhost:8000/feed", headers=get_headers(), timeout=10)
            
            if response.status_code == 200:
                posts = response.json()["posts"]

                if not posts:
                    st.markdown("""
                    <div style='text-align: center; padding: 3rem;'>
                        <h3>📭 No posts yet!</h3>
                        <p>Be the first to share something amazing with your community.</p>
                        <p>👉 Go to the <strong>Upload</strong> page to create your first post!</p>
                    </div>
                    """, unsafe_allow_html=True)
                    return

                # Create a centered container for posts
                with st.container():
                    # Display posts in reverse chronological order (newest first)
                    for post in posts:
                        display_post(post)
                    
            else:
                st.markdown('<div class="error-message">❌ Failed to load feed. Please try again later.</div>', unsafe_allow_html=True)
                
        except requests.exceptions.RequestException as e:
            st.markdown(f'<div class="error-message">❌ Network error: {str(e)}</div>', unsafe_allow_html=True)

def display_post(post):
    """Display a single post with proper formatting"""
    with st.container():
        # Use columns to center the card
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            
            # Post header - User info and timestamp
            st.markdown(f'<div class="user-info">👤 {post["email"]}</div>', unsafe_allow_html=True)
            created_time = datetime.fromisoformat(post['created_at'].replace('Z', '+00:00'))
            st.markdown(f'<div class="timestamp">🕒 {created_time.strftime("%B %d, %Y at %I:%M %p")}</div>', unsafe_allow_html=True)
            
            # Display caption first (above media)
            caption = post.get('caption', '')
            if caption and caption.strip():
                st.markdown(f'<div class="caption-text">💬 {caption}</div>', unsafe_allow_html=True)
            
            # Media content with proper sizing
            st.markdown('<div class="post-media-container">', unsafe_allow_html=True)
            if post['file_type'] == 'image':
                # Display image with controlled size
                st.image(
                    post['url'], 
                    use_container_width=False,  # Don't use full container width
                    width=400,  # Set fixed width
                    caption=""
                )
            else:
                # Display video with controlled size
                st.video(post['url'])
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Delete button (only for post owner)
            if post.get('is_owner', False):
                st.markdown('<div class="post-actions">', unsafe_allow_html=True)
                if st.button("🗑️ Delete Post", key=f"delete_{post['id']}", use_container_width=True):
                    with st.spinner("Deleting post..."):
                        try:
                            response = requests.delete(
                                f"http://localhost:8000/posts/{post['id']}", 
                                headers=get_headers(),
                                timeout=10
                            )
                            if response.status_code == 200:
                                st.success("✅ Post deleted successfully!")
                                st.rerun()
                            else:
                                st.error("❌ Failed to delete post!")
                        except requests.exceptions.RequestException:
                            st.error("❌ Network error while deleting post")
                st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

def login_page():
    # Header Section
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<h1 class="main-header">🚀 Simple Social</h1>', unsafe_allow_html=True)
        st.markdown("### Connect, Share, and Discover")
    
    # Login Card
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            with st.form("login_form"):
                st.markdown("### Welcome Back! 👋")
                
                email = st.text_input(
                    "📧 Email Address",
                    placeholder="Enter your email address",
                    key="login_email"
                )
                
                password = st.text_input(
                    "🔒 Password", 
                    type="password",
                    placeholder="Enter your password",
                    key="login_password"
                )
                
                col1, col2 = st.columns(2)
                
                with col1:
                    login_btn = st.form_submit_button(
                        "🚀 Login", 
                        use_container_width=True,
                        type="primary"
                    )
                
                with col2:
                    signup_btn = st.form_submit_button(
                        "📝 Sign Up", 
                        use_container_width=True,
                        type="secondary"
                    )
                
                if login_btn and email and password:
                    with st.spinner("Signing you in..."):
                        login_data = {"username": email, "password": password}
                        response = requests.post("http://localhost:8000/auth/jwt/login", data=login_data)

                        if response.status_code == 200:
                            token_data = response.json()
                            st.session_state.token = token_data["access_token"]

                            # Get user info
                            user_response = requests.get("http://localhost:8000/users/me", headers=get_headers())
                            if user_response.status_code == 200:
                                st.session_state.user = user_response.json()
                                st.markdown('<div class="success-message">✅ Login successful! Redirecting...</div>', unsafe_allow_html=True)
                                st.rerun()
                            else:
                                st.markdown('<div class="error-message">❌ Failed to get user info</div>', unsafe_allow_html=True)
                        else:
                            st.markdown('<div class="error-message">❌ Invalid email or password!</div>', unsafe_allow_html=True)
                
                if signup_btn and email and password:
                    with st.spinner("Creating your account..."):
                        signup_data = {"email": email, "password": password}
                        response = requests.post("http://localhost:8000/auth/register", json=signup_data)

                        if response.status_code == 201:
                            st.markdown('<div class="success-message">🎉 Account created successfully! Please login.</div>', unsafe_allow_html=True)
                        else:
                            error_detail = response.json().get("detail", "Registration failed")
                            st.markdown(f'<div class="error-message">❌ Registration failed: {error_detail}</div>', unsafe_allow_html=True)

def sidebar_content():
    """Render sidebar content"""
    st.sidebar.markdown("""
    <div style='text-align: center; padding: 1rem;'>
        <h2>🚀 Simple Social</h2>
        <p>Connect with your community</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    
    if st.session_state.user:
        # User info card
        st.sidebar.markdown(f"""
        <div class="user-card">
            <h4>👋 Welcome back!</h4>
            <p><strong>{st.session_state.user['email']}</strong></p>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation
        st.sidebar.markdown("### 🧭 Navigation")
        page_options = {
            "🏠 Feed": "View all posts from your community",
            "📸 Upload": "Share a new post with your followers"
        }
        
        selected_page = st.sidebar.radio(
            "Go to:",
            options=list(page_options.keys()),
            index=0 if st.session_state.get('current_page', 'Feed') == 'Feed' else 1,
            key="nav_radio"
        )
        
        # Show page description
        page_desc = page_options[selected_page]
        st.sidebar.info(f"**{page_desc}**")
        
        st.sidebar.markdown("---")
        
        # Stats (optional - you can add actual stats later)
        st.sidebar.markdown("### 📊 Quick Stats")
        st.sidebar.metric("Posts Today", "12")
        st.sidebar.metric("Active Users", "47")
        
        st.sidebar.markdown("---")
        
        # Logout button
        if st.sidebar.button("🚪 Logout", use_container_width=True, type="secondary"):
            st.session_state.user = None
            st.session_state.token = None
            st.session_state.current_page = None
            st.rerun()
        
        return selected_page.replace("🏠 ", "").replace("📸 ", "")
    
    return None

# Main app logic
if st.session_state.user is None:
    login_page()
else:
    # Get current page from sidebar
    current_page = sidebar_content()
    
    # Route to appropriate page
    if current_page == "Feed":
        st.session_state.current_page = "Feed"
        feed_page()
    elif current_page == "Upload":
        st.session_state.current_page = "Upload"
        upload_page()