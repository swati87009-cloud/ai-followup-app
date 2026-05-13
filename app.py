# =========================================================
# FREELANCER COMMAND CENTER - FINAL PROFESSIONAL VERSION
# =========================================================

import streamlit as st
import json
import os
import time
from datetime import date

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Freelancer Command Center",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# DATABASE
# =========================================================

DATA_FILE = "freelancer_data.json"

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({}, f)

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

data = load_data()

# =========================================================
# SESSION
# =========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_id" not in st.session_state:
    st.session_state.user_id = ""

# =========================================================
# PREMIUM BLUE CSS
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"]{
    font-family:'Inter',sans-serif;
}

/* MAIN */

.stApp{
    background:
    radial-gradient(
    circle at top left,
    #1e3a8a,
    #0f172a 45%
    );

    color:white;
}

/* HIDE */

#MainMenu{
    visibility:hidden;
}

footer{
    visibility:hidden;
}

/* SIDEBAR */

section[data-testid="stSidebar"]{

    background:
    rgba(15,23,42,0.98);

    border-right:
    1px solid rgba(255,255,255,0.08);

    backdrop-filter:blur(20px);
}

section[data-testid="stSidebar"] *{
    color:white !important;
}

/* WIDTH */

.block-container{
    max-width:1450px;
    padding-top:2rem;
    padding-left:2rem;
    padding-right:2rem;
}

/* HERO CARD */

.hero-card{

    background:
    linear-gradient(
    135deg,
    rgba(255,255,255,0.10),
    rgba(255,255,255,0.04)
    );

    border:
    1px solid rgba(255,255,255,0.08);

    border-radius:32px;

    padding:45px;

    margin-bottom:25px;

    backdrop-filter:blur(20px);

    box-shadow:
    0 10px 40px rgba(0,0,0,0.30);
}

/* METRIC CARD */

.metric-card{

    background:
    linear-gradient(
    135deg,
    rgba(255,255,255,0.10),
    rgba(255,255,255,0.04)
    );

    border:
    1px solid rgba(255,255,255,0.08);

    border-radius:26px;

    padding:28px;

    text-align:center;

    backdrop-filter:blur(20px);

    box-shadow:
    0 10px 35px rgba(0,0,0,0.20);

    transition:0.3s;
}

.metric-card:hover{

    transform:translateY(-5px);

    box-shadow:
    0 15px 35px rgba(99,102,241,0.30);
}

/* CLIENT CARD */

.client-card{

    background:
    linear-gradient(
    135deg,
    rgba(255,255,255,0.10),
    rgba(255,255,255,0.04)
    );

    border:
    1px solid rgba(255,255,255,0.08);

    border-radius:28px;

    padding:30px;

    margin-bottom:24px;

    backdrop-filter:blur(20px);

    box-shadow:
    0 10px 35px rgba(0,0,0,0.20);
}

/* INPUTS */

.stTextInput input,
.stTextArea textarea,
.stDateInput input{

    background:
    rgba(17,24,39,0.95) !important;

    color:white !important;

    border:
    1px solid rgba(255,255,255,0.08) !important;

    border-radius:18px !important;

    min-height:55px !important;

    padding-left:15px !important;

    font-size:16px !important;
}

/* SELECT BOX */

.stSelectbox > div > div{

    background:
    rgba(17,24,39,0.95) !important;

    color:white !important;

    border:
    1px solid rgba(255,255,255,0.08) !important;

    border-radius:18px !important;

    min-height:55px !important;
}

/* BUTTON */

.stButton button{

    width:100%;

    border:none;

    border-radius:18px;

    padding:14px;

    font-size:16px;

    font-weight:700;

    color:white;

    background:
    linear-gradient(
    135deg,
    #6366f1,
    #8b5cf6,
    #06b6d4
    );

    transition:0.3s;
}

.stButton button:hover{

    transform:scale(1.02);

    box-shadow:
    0 12px 35px rgba(99,102,241,0.35);
}

label{
    color:white !important;
    font-weight:600 !important;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# LOGIN PAGE
# =========================================================

if not st.session_state.logged_in:

    st.markdown("""
<div class="hero-card">

<h3 style="
color:#60a5fa;
font-size:24px;
font-weight:700;
">
📈 Add More Leads Daily
</h3>

<p style="
color:#94a3b8;
font-size:16px;
line-height:1.7;
">
Consistency builds pipeline.
Try adding 2-3 new leads every day.
</p>

</div>
""", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    # =====================================================
    # CREATE ACCOUNT
    # =====================================================

    with col1:

        st.markdown("""
        <div class="hero-card">
        <h2>✨ Create Account</h2>
        </div>
        """, unsafe_allow_html=True)

        full_name = st.text_input("👤 Full Name")

        username = st.text_input("🆔 Username")

        client_goal = st.number_input(
            "🎯 Monthly Client Goal",
            min_value=1,
            max_value=1000,
            value=10
        )

        if st.button("🚀 Create Account"):

            username = username.lower().strip()

            if username == "" or full_name == "":

                st.warning("Fill all fields")

            elif username in data:

                st.error("Username already exists")

            else:

                data[username] = {

                    "name": full_name,

                    "goal": client_goal,

                    "clients": []

                }

                save_data(data)

                st.session_state.logged_in = True

                st.session_state.user_id = username

                st.success("Account Created Successfully 🚀")

                time.sleep(1)

                st.rerun()

    # =====================================================
    # LOGIN
    # =====================================================

    with col2:

        st.markdown("""
        <div class="hero-card">
        <h2>🔐 Login</h2>
        </div>
        """, unsafe_allow_html=True)

        login_user = st.text_input("Enter Username")

        if st.button("✨ Open Dashboard"):

            login_user = login_user.lower().strip()

            if login_user in data:

                st.session_state.logged_in = True

                st.session_state.user_id = login_user

                st.rerun()

            else:

                st.error("User not found")

# =========================================================
# MAIN APP
# =========================================================

else:

    user_id = st.session_state.user_id

    user_data = data[user_id]

    clients = user_data.get("clients", [])

    # =====================================================
    # SIDEBAR
    # =====================================================

    st.sidebar.title("🚀 Command Center")

    st.sidebar.success(f"👤 {user_data['name']}")

    st.sidebar.info(f"🌍 Total Users: {len(data)}")

    page = st.sidebar.radio(
        "Navigation",
        [
            "Dashboard",
            "Add Client",
            "Profile"
        ]
    )

    if st.sidebar.button("🚪 Logout"):

        st.session_state.logged_in = False

        st.rerun()

    # =====================================================
    # DASHBOARD
    # =====================================================

    if page == "Dashboard":

        total_clients = len(clients)

        closed = len([
            c for c in clients
            if c.get("status") == "Deal Closed"
        ])

        pending = len([
            c for c in clients
            if c.get("status") == "No Response"
        ])

        cancelled = len([
            c for c in clients
            if c.get("status") == "Cancelled"
        ])

        # HERO

        st.markdown(f"""
        <div class="hero-card">

        <h1 style="
        font-size:58px;
        font-weight:800;
        ">
        Welcome Back, {user_data['name']} 👋
        </h1>

        <p style="
        font-size:20px;
        color:#94a3b8;
        ">
        Manage leads and close more deals professionally.
        </p>

        </div>
        """, unsafe_allow_html=True)

        # METRICS

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.markdown(f"""
            <div class="metric-card">
            <h1>{total_clients}</h1>
            <p>👥 Total Clients</p>
            </div>
            """, unsafe_allow_html=True)

        with c2:
            st.markdown(f"""
            <div class="metric-card">
            <h1 style="color:#22c55e;">{closed}</h1>
            <p>🔥 Closed Deals</p>
            </div>
            """, unsafe_allow_html=True)

        with c3:
            st.markdown(f"""
            <div class="metric-card">
            <h1 style="color:#eab308;">{pending}</h1>
            <p>⏳ Pending</p>
            </div>
            """, unsafe_allow_html=True)

        with c4:
            st.markdown(f"""
            <div class="metric-card">
            <h1 style="color:#ef4444;">{cancelled}</h1>
            <p>❌ Cancelled</p>
            </div>
            """, unsafe_allow_html=True)

        # =====================================================
        # GOAL PROGRESS
        # =====================================================

        goal = user_data.get("goal", 10)

        progress = min(total_clients / goal, 1.0)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(f"""
        <div class="hero-card">

        <h2>
        🎯 Client Goal Progress
        </h2>

        <p style="
        color:#94a3b8;
        ">
        {total_clients} / {goal} Clients Added
        </p>

        </div>
        """, unsafe_allow_html=True)

        st.progress(progress)

        if total_clients >= goal:

            st.success("🔥 Goal Completed!")

        elif total_clients >= goal * 0.7:

            st.info("⚡ You are close to your goal")

        elif total_clients >= goal * 0.4:

            st.warning("🚀 Keep pushing consistently")

        else:

            st.error("📈 Add more leads daily")

        # =====================================================
        # SEARCH
        # =====================================================

        search = st.text_input(
            "🔎 Search Client",
            placeholder="Search client..."
        )

        filtered_clients = []

        for client in clients:

            if search.lower() in client.get(
                "client_name",""
            ).lower():

                filtered_clients.append(client)

        # =====================================================
        # CLIENT CARDS
        # =====================================================

        for index, client in enumerate(filtered_clients):

            st.markdown(f"""
            <div class="client-card">

            <h2>
            👤 {client.get('client_name','')}
            </h2>

            <p>📱 {client.get('phone','Not Added')}</p>

            <p>🌍 Source: {client.get('lead_source','')}</p>

            <p>✉ Pitch: {client.get('pitch_type','')}</p>

            <p>🏢 Niche: {client.get('client_niche','')}</p>

            <p>📅 Followup: {client.get('date','')}</p>

            <p>💬 {client.get('last_message','No Message')}</p>

            <p>📌 Status: {client.get('status','No Response')}</p>

            </div>
            """, unsafe_allow_html=True)

            # WHATSAPP BUTTON

            if client.get("phone","") != "":

                phone = client["phone"]

                whatsapp_url = f"https://wa.me/{phone}"

                st.markdown(
                    f"""
                    <a href="{whatsapp_url}" target="_blank">

                        <button style="
                        width:100%;
                        padding:14px;
                        border:none;
                        border-radius:16px;
                        background:#25D366;
                        color:white;
                        font-weight:700;
                        font-size:16px;
                        cursor:pointer;
                        margin-bottom:20px;
                        ">

                        💬 Open WhatsApp

                        </button>

                    </a>
                    """,
                    unsafe_allow_html=True
                )

            b1, b2, b3, b4 = st.columns(4)

            with b1:

                if st.button(f"🔥 Close {index}"):

                    clients[index]["status"] = "Deal Closed"

                    save_data(data)

                    st.rerun()

            with b2:

                if st.button(f"❌ Cancel {index}"):

                    clients[index]["status"] = "Cancelled"

                    save_data(data)

                    st.rerun()

            with b3:

                if st.button(f"✏ Edit {index}"):

                    st.session_state["edit_client"] = index

            with b4:

                if st.button(f"🗑 Delete {index}"):

                    clients.pop(index)

                    save_data(data)

                    st.rerun()

        # =====================================================
        # EDIT CLIENT
        # =====================================================

        if "edit_client" in st.session_state:

            edit_index = st.session_state["edit_client"]

            if edit_index < len(clients):

                edit_client = clients[edit_index]

                st.markdown("""
                <div class="hero-card">
                <h1>✏ Edit Client</h1>
                </div>
                """, unsafe_allow_html=True)

                new_name = st.text_input(
                    "Client Name",
                    value=edit_client.get(
                        "client_name",""
                    )
                )

                new_phone = st.text_input(
                    "Phone Number",
                    value=edit_client.get(
                        "phone",""
                    )
                )

                new_message = st.text_area(
                    "Last Message",
                    value=edit_client.get(
                        "last_message",""
                    )
                )

                if st.button("💾 Save Changes"):

                    clients[edit_index]["client_name"] = new_name

                    clients[edit_index]["phone"] = new_phone

                    clients[edit_index]["last_message"] = new_message

                    save_data(data)

                    del st.session_state["edit_client"]

                    st.success("Client Updated 🚀")

                    time.sleep(1)

                    st.rerun()

    # =====================================================
    # ADD CLIENT
    # =====================================================

    elif page == "Add Client":

        st.markdown("""
        <div class="hero-card">
        <h1>➕ Add New Client</h1>
        </div>
        """, unsafe_allow_html=True)

        client_name = st.text_input("👤 Client Name")

        client_phone = st.text_input(
            "📱 WhatsApp Number (Optional)"
        )

        last_message = st.text_area(
            "💬 Last Message"
        )

        lead_source = st.selectbox(
            "🌍 Lead Source",
            [
                "Twitter",
                "LinkedIn",
                "Instagram",
                "Referral",
                "Cold Outreach"
            ]
        )

        pitch_type = st.selectbox(
            "✉ Pitch Angle",
            [
                "Short Pitch",
                "Detailed Pitch",
                "Custom Proposal"
            ]
        )

        client_niche = st.selectbox(
            "🏢 Client Niche",
            [
                "AI",
                "SaaS",
                "Agency",
                "Ecommerce",
                "Personal Brand"
            ]
        )

        followup_date = st.date_input(
            "📅 Followup Date",
            value=date.today()
        )

        if st.button("🚀 Save Client"):

            clients.append({

                "client_name": client_name,

                "phone": client_phone,

                "last_message": last_message,

                "lead_source": lead_source,

                "pitch_type": pitch_type,

                "client_niche": client_niche,

                "date": str(followup_date),

                "status": "No Response"

            })

            save_data(data)

            st.success("Client Added Successfully 🚀")

            st.balloons()

            time.sleep(1)

            st.rerun()

    # =====================================================
    # PROFILE
    # =====================================================

    elif page == "Profile":

        st.markdown(f"""
        <div class="hero-card">

        <h1>
        👤 {user_data['name']}
        </h1>

        <p>
        Username: @{user_id}
        </p>

        <p>
        🎯 Goal: {user_data.get('goal',10)}
        </p>

        <p>
        👥 Total Clients: {len(clients)}
        </p>

        </div>
        """, unsafe_allow_html=True)