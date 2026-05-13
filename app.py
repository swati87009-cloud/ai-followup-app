# =========================================================
# 🚀 FREELANCER GROWTH OPERATING SYSTEM
# Ultimate Streamlit CRM
# =========================================================

import streamlit as st
import pandas as pd
import numpy as np
import hashlib
import os
from datetime import date, datetime

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Freelancer Growth Operating System",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM PREMIUM UI
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
}

/* MAIN APP */
.stApp {
    background:
    radial-gradient(circle at top left, #124EAF 0%, transparent 30%),
    radial-gradient(circle at bottom right, #00C6FF 0%, transparent 25%),
    linear-gradient(135deg,#06152E,#081F44,#0D2B63);
    color: white;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: rgba(5,10,25,0.75);
    border-right: 1px solid rgba(255,255,255,0.08);
}

/* GLASS */
.glass-card {
    background: rgba(255,255,255,0.07);
    border-radius: 24px;
    padding: 24px;
    backdrop-filter: blur(18px);
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 8px 32px rgba(0,0,0,0.25);
}

/* METRIC */
.metric-card {
    background: rgba(255,255,255,0.07);
    padding: 22px;
    border-radius: 22px;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.08);
    transition: 0.3s;
}

.metric-card:hover {
    transform: translateY(-4px);
}

/* FEATURE */
.feature-card {
    background: rgba(255,255,255,0.06);
    border-radius: 20px;
    padding: 18px;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.08);
}

/* BUTTON */
.stButton > button {
    width: 100%;
    border: none;
    border-radius: 14px;
    padding: 0.8rem;
    background: linear-gradient(90deg,#00C6FF,#0072FF);
    color: white;
    font-weight: 700;
    transition: 0.3s;
}

.stButton > button:hover {
    transform: scale(1.02);
    background: linear-gradient(90deg,#0072FF,#00C6FF);
}

/* INPUTS */
.stTextInput input,
.stSelectbox div,
.stDateInput input,
.stTextArea textarea,
.stNumberInput input {
    border-radius: 14px !important;
}

/* LOGIN */
.login-box {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(16px);
    border-radius: 30px;
    padding: 45px;
    border: 1px solid rgba(255,255,255,0.08);
}

/* TITLES */
h1,h2,h3,h4,h5,p,label {
    color: white !important;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# FILES
# =========================================================

USERS_FILE = "users.csv"

# =========================================================
# INIT USERS FILE
# =========================================================

if not os.path.exists(USERS_FILE):

    pd.DataFrame(columns=[
        "username",
        "password",
        "goal"
    ]).to_csv(USERS_FILE, index=False)

# =========================================================
# HELPERS
# =========================================================

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    return pd.read_csv(USERS_FILE)

def save_users(df):
    df.to_csv(USERS_FILE, index=False)

def user_file(username):
    return f"{username}_clients.csv"

def init_client_file(username):

    file = user_file(username)

    if not os.path.exists(file):

        pd.DataFrame(columns=[
            "Client Name",
            "WhatsApp Number",
            "Business Name",
            "City",
            "Website",
            "Lead Source",
            "Pitch Angle",
            "Client Niche",
            "Money Signal",
            "Followup Date",
            "Status",
            "Reply"
        ]).to_csv(file, index=False)

def load_clients(username):

    init_client_file(username)

    return pd.read_csv(user_file(username))

def save_clients(username, df):
    df.to_csv(user_file(username), index=False)

# =========================================================
# SESSION
# =========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# =========================================================
# LOGIN PAGE
# =========================================================

if not st.session_state.logged_in:

    st.markdown("<br>", unsafe_allow_html=True)

    left, center, right = st.columns([1,2,1])

    with center:

        st.markdown("""
        <div class="login-box">

        <h1 style="text-align:center;font-size:48px;">
        🚀 Freelancer Growth Operating System
        </h1>

        <p style="text-align:center;font-size:18px;color:#d6e3ff;">
        Smart CRM + Outreach Tracking + Followup System +
        Freelancer Productivity Dashboard
        </p>

        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        f1,f2,f3,f4 = st.columns(4)

        with f1:
            st.markdown("""
            <div class='feature-card'>
            <h4>📋 CRM</h4>
            <p>Client management</p>
            </div>
            """, unsafe_allow_html=True)

        with f2:
            st.markdown("""
            <div class='feature-card'>
            <h4>📅 Followups</h4>
            <p>Reminder tracking</p>
            </div>
            """, unsafe_allow_html=True)

        with f3:
            st.markdown("""
            <div class='feature-card'>
            <h4>📈 Analytics</h4>
            <p>Reply & conversion</p>
            </div>
            """, unsafe_allow_html=True)

        with f4:
            st.markdown("""
            <div class='feature-card'>
            <h4>🎯 Goals</h4>
            <p>Monthly targets</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["🔐 Login", "📝 Signup"])

        # =================================================
        # LOGIN
        # =================================================

        with tab1:

            login_user = st.text_input("Username")

            login_pass = st.text_input(
                "Password",
                type="password"
            )

            if st.button("Login To Workspace"):

                users = load_users()

                user = users[
                    (users["username"] == login_user) &
                    (users["password"] == hash_password(login_pass))
                ]

                if not user.empty:

                    st.session_state.logged_in = True
                    st.session_state.username = login_user

                    st.success("Login Successful")
                    st.rerun()

                else:
                    st.error("Invalid Credentials")

        # =================================================
        # SIGNUP
        # =================================================

        with tab2:

            new_user = st.text_input("Create Username")

            new_pass = st.text_input(
                "Create Password",
                type="password"
            )

            goal = st.number_input(
                "Monthly Goal",
                1,
                500,
                10
            )

            if st.button("Create Workspace"):

                users = load_users()

                if new_user in users["username"].values:

                    st.error("Username Already Exists")

                else:

                    new_data = pd.DataFrame([{
                        "username": new_user,
                        "password": hash_password(new_pass),
                        "goal": goal
                    }])

                    users = pd.concat(
                        [users,new_data],
                        ignore_index=True
                    )

                    save_users(users)

                    init_client_file(new_user)

                    st.session_state.logged_in = True
                    st.session_state.username = new_user

                    st.success("Workspace Created")
                    st.rerun()

# =========================================================
# MAIN APP
# =========================================================

else:

    username = st.session_state.username

    users = load_users()

    user_data = users[
        users["username"] == username
    ].iloc[0]

    goal = int(user_data["goal"])

    clients = load_clients(username)

    # =====================================================
    # SIDEBAR
    # =====================================================

    st.sidebar.title("🚀 Navigation")

    page = st.sidebar.radio(
        "Menu",
        [
            "Dashboard",
            "Add Client",
            "Manage Clients",
            "Analytics"
        ]
    )

    st.sidebar.markdown("---")

    st.sidebar.success(f"👤 {username}")

    st.sidebar.info(f"👥 Total Users : {len(users)}")

    if st.sidebar.button("Logout"):

        st.session_state.logged_in = False
        st.session_state.username = ""

        st.rerun()

    # =====================================================
    # DASHBOARD
    # =====================================================

    if page == "Dashboard":

        st.title("📊 Growth Dashboard")

        total_clients = len(clients)

        closed = len(
            clients[clients["Status"] == "Deal Closed"]
        )

        pending = len(
            clients[clients["Status"] == "Pending"]
        )

        cancelled = len(
            clients[clients["Status"] == "Cancelled"]
        )

        progress = min(closed / goal, 1.0)

        c1,c2,c3,c4 = st.columns(4)

        with c1:
            st.metric(
                "👥 Total Clients",
                total_clients
            )

        with c2:
            st.metric(
                "✅ Deal Closed",
                closed
            )

        with c3:
            st.metric(
                "⏳ Pending",
                pending
            )

        with c4:
            st.metric(
                "❌ Cancelled",
                cancelled
            )

        st.markdown("---")

        st.subheader("🎯 Monthly Goal Progress")

        st.progress(progress)

        st.write(f"{closed} / {goal} Deals Closed")

        if progress >= 1:
            st.success("🔥 Goal Completed")

        elif progress >= 0.7:
            st.info("🚀 You're close to goal")

        else:
            st.warning("💪 Keep going")

        st.markdown("---")

        st.subheader("📅 Today's Followups")

        today = str(date.today())

        due = clients[
            clients["Followup Date"].astype(str) == today
        ]

        if len(due) > 0:

            st.dataframe(
                due,
                use_container_width=True
            )

        else:
            st.success("No Followups Today")

    # =====================================================
    # ADD CLIENT
    # =====================================================

    elif page == "Add Client":

        st.title("➕ Add Client")

        with st.form("client_form"):

            col1,col2 = st.columns(2)

            with col1:

                client_name = st.text_input("Client Name")

                whatsapp = st.text_input(
                    "WhatsApp Number"
                )

                business = st.text_input(
                    "Business Name"
                )

                city = st.text_input("City")

                website = st.text_input("Website")

                niche = st.text_input(
                    "Client Niche"
                )

            with col2:

                lead_source = st.selectbox(
                    "Lead Source",
                    [
                        "Instagram",
                        "LinkedIn",
                        "Facebook",
                        "Cold Email",
                        "Referral",
                        "Other"
                    ]
                )

                pitch = st.text_input(
                    "Pitch Angle"
                )

                money_signal = st.selectbox(
                    "Money Signal",
                    [
                        "Low",
                        "Medium",
                        "High"
                    ]
                )

                followup = st.date_input(
                    "Followup Date"
                )

                status = st.selectbox(
                    "Status",
                    [
                        "Pending",
                        "Deal Closed",
                        "Cancelled"
                    ]
                )

            submit = st.form_submit_button(
                "Add Client"
            )

            if submit:

                new_client = pd.DataFrame([{
                    "Client Name": client_name,
                    "WhatsApp Number": whatsapp,
                    "Business Name": business,
                    "City": city,
                    "Website": website,
                    "Lead Source": lead_source,
                    "Pitch Angle": pitch,
                    "Client Niche": niche,
                    "Money Signal": money_signal,
                    "Followup Date": followup,
                    "Status": status,
                    "Reply": np.random.choice(
                        ["Yes","No"]
                    )
                }])

                clients = pd.concat(
                    [clients,new_client],
                    ignore_index=True
                )

                save_clients(
                    username,
                    clients
                )

                st.success(
                    "Client Added Successfully"
                )

    # =====================================================
    # MANAGE CLIENTS
    # =====================================================

    elif page == "Manage Clients":

        st.title("👥 Manage Clients")

        search = st.text_input(
            "🔍 Search Client"
        )

        filtered = clients.copy()

        if search:

            filtered = filtered[
                filtered["Client Name"].str.contains(
                    search,
                    case=False,
                    na=False
                )
            ]

        st.dataframe(
            filtered,
            use_container_width=True
        )

        st.markdown("---")

        if len(filtered) > 0:

            selected = st.selectbox(
                "Select Client",
                filtered["Client Name"].tolist()
            )

            idx = filtered[
                filtered["Client Name"] == selected
            ].index[0]

            row = clients.loc[idx]

            st.subheader("✏ Edit Client")

            new_status = st.selectbox(
                "Status",
                [
                    "Pending",
                    "Deal Closed",
                    "Cancelled"
                ],
                index=[
                    "Pending",
                    "Deal Closed",
                    "Cancelled"
                ].index(row["Status"])
            )

            new_followup = st.date_input(
                "Followup Date",
                pd.to_datetime(
                    row["Followup Date"]
                )
            )

            c1,c2,c3 = st.columns(3)

            with c1:

                if st.button("Update Client"):

                    clients.at[
                        idx,
                        "Status"
                    ] = new_status

                    clients.at[
                        idx,
                        "Followup Date"
                    ] = new_followup

                    save_clients(
                        username,
                        clients
                    )

                    st.success(
                        "Client Updated"
                    )

                    st.rerun()

            with c2:

                number = str(
                    row["WhatsApp Number"]
                )

                if number != "nan":

                    wa = f"https://wa.me/{number}"

                    st.markdown(
                        f"""
                        <a href="{wa}" target="_blank">
                        <button style="
                        background:#25D366;
                        color:white;
                        border:none;
                        padding:10px 18px;
                        border-radius:12px;
                        width:100%;
                        ">
                        Open WhatsApp
                        </button>
                        </a>
                        """,
                        unsafe_allow_html=True
                    )

            with c3:

                if st.button(
                    "Delete Client"
                ):

                    clients = clients.drop(idx)

                    save_clients(
                        username,
                        clients
                    )

                    st.success(
                        "Client Deleted"
                    )

                    st.rerun()

    # =====================================================
    # ANALYTICS
    # =====================================================

    elif page == "Analytics":

        st.title("📈 Smart Analytics")

        if len(clients) == 0:

            st.warning("No Data Available")

        else:

            st.subheader(
                "🏆 Best Lead Sources"
            )

            source = clients[
                "Lead Source"
            ].value_counts()

            st.bar_chart(source)

            st.subheader(
                "🎯 Best Niches"
            )

            niches = clients[
                "Client Niche"
            ].value_counts()

            st.bar_chart(niches)

            st.subheader(
                "💰 Money Signal Analytics"
            )

            money = clients[
                "Money Signal"
            ].value_counts()

            st.bar_chart(money)

            st.subheader(
                "📊 Status Analytics"
            )

            status_data = clients[
                "Status"
            ].value_counts()

            st.bar_chart(status_data)

            replies = len(
                clients[
                    clients["Reply"] == "Yes"
                ]
            )

            reply_rate = (
                replies / len(clients)
            ) * 100

            closed = len(
                clients[
                    clients["Status"] == "Deal Closed"
                ]
            )

            conversion = (
                closed / len(clients)
            ) * 100

            a1,a2 = st.columns(2)

            with a1:

                st.metric(
                    "📩 Reply Rate",
                    f"{reply_rate:.1f}%"
                )

            with a2:

                st.metric(
                    "🔥 Conversion Rate",
                    f"{conversion:.1f}%"
                )

            st.markdown("---")

            st.subheader("🧠 Smart Insights")

            best_source = source.idxmax()

            best_niche = niches.idxmax()

            st.success(
                f"Best Lead Source : {best_source}"
            )

            st.success(
                f"Best Performing Niche : {best_niche}"
            )

            if conversion > 50:

                st.info(
                    "Excellent sales performance"
                )

            else:

                st.warning(
                    "Improve followups & outreach"
                )

# =========================================================
# END
# =========================================================