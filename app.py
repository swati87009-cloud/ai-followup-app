import streamlit as st
import json
import os
import time
from datetime import date

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Freelancer Command Center",
    page_icon="🚀",
    layout="wide"
)

# =========================
# CUSTOM CSS
# =========================

st.markdown("""
<style>

html, body, [class*="css"] {
    background: #0f172a;
    color: white;
    font-family: 'Poppins', sans-serif;
}

.main {
    background: #0f172a;
}

h1,h2,h3,h4 {
    color: white;
}

.stTextInput input,
.stTextArea textarea,
.stDateInput input {
    background: #111827 !important;
    color: white !important;
    border-radius: 12px !important;
    border: 1px solid #374151 !important;
}

.stButton button {
    width: 100%;
    border: none;
    border-radius: 12px;
    padding: 12px;
    font-weight: bold;
    background: linear-gradient(90deg,#2563eb,#7c3aed);
    color: white;
    transition: 0.3s;
}

.stButton button:hover {
    transform: scale(1.02);
}

.metric-card {
    background: linear-gradient(135deg,#111827,#1e293b);
    padding: 20px;
    border-radius: 18px;
    text-align: center;
    border: 1px solid #374151;
}

.client-card {
    background: #111827;
    padding: 20px;
    border-radius: 18px;
    margin-bottom: 20px;
    border: 1px solid #1f2937;
}

.goal-box {
    background: linear-gradient(135deg,#1e293b,#111827);
    padding: 30px;
    border-radius: 20px;
    text-align:center;
    border: 1px solid #374151;
}

.footer {
    text-align:center;
    margin-top:50px;
    color:#9ca3af;
}

</style>
""", unsafe_allow_html=True)

# =========================
# DATA FILE
# =========================

DATA_FILE = "freelancer_data.json"

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({}, f)

# =========================
# FUNCTIONS
# =========================

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

data = load_data()

# =========================
# SESSION
# =========================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_id" not in st.session_state:
    st.session_state.user_id = ""

# =========================
# LOGIN / CREATE ACCOUNT
# =========================

if not st.session_state.logged_in:

    st.title("🚀 Freelancer Command Center")

    st.markdown("""
    ### Manage clients, track followups & close more deals.
    """)

    col1, col2 = st.columns(2)

    # =========================
    # CREATE ACCOUNT
    # =========================

    with col1:

        st.subheader("🆕 Create Account")

        st.markdown("""
        <div class="goal-box">
        Build your freelance workflow smarter 🚀
        </div>
        """, unsafe_allow_html=True)

        create_name = st.text_input(
            "👤 Your Name",
            placeholder="Enter your name"
        )

        create_user_id = st.text_input(
            "🆔 Create User ID",
            placeholder="Choose unique ID"
        )

        if st.button("🚀 Create Account"):

            create_name = create_name.strip()
            create_user_id = create_user_id.strip().lower()

            if create_name == "" or create_user_id == "":

                st.warning("⚠ Please fill all fields.")

            elif create_user_id in data:

                st.error("❌ User already exists.")

            else:

                data[create_user_id] = {
                    "name": create_name,
                    "target": 0,
                    "completed_targets": 0,
                    "clients": []
                }

                save_data(data)

                st.session_state.logged_in = True
                st.session_state.user_id = create_user_id

                st.success(
                    f"✅ Welcome {create_name}! Dashboard Ready 🚀"
                )

                st.balloons()

                time.sleep(1)

                st.rerun()

    # =========================
    # LOGIN
    # =========================

    with col2:

        st.subheader("🔐 Login")

        login_user_id = st.text_input(
            "Enter User ID",
            placeholder="Your user ID"
        )

        if st.button("✨ Open Dashboard"):

            login_user_id = login_user_id.strip().lower()

            if login_user_id in data:

                st.session_state.logged_in = True
                st.session_state.user_id = login_user_id

                st.success("✅ Welcome Back!")

                time.sleep(1)

                st.rerun()

            else:

                st.error("❌ User not found.")

# =========================
# DASHBOARD
# =========================

else:

    user_id = st.session_state.user_id

    user_data = data[user_id]

    clients = user_data.get("clients", [])

    # =========================
    # SIDEBAR
    # =========================

    st.sidebar.title("🚀 Command Center")

    st.sidebar.success(
        f"👤 {user_data['name']}"
    )

    st.sidebar.info(
        f"🏆 Targets Completed: {user_data.get('completed_targets',0)}"
    )

    st.sidebar.write(
        f"👥 Total Users: {len(data)}"
    )

    page = st.sidebar.radio(
        "Navigation",
        ["Dashboard", "Add Client"]
    )

    if st.sidebar.button("🚪 Logout"):

        st.session_state.logged_in = False
        st.session_state.user_id = ""

        st.rerun()

    # =========================
    # TARGET PAGE
    # =========================

    if user_data.get("target", 0) == 0:

        st.title("🎯 Set Your Client Target")

        st.markdown("""
        <div class="goal-box">
        <h2>How many clients do you want to manage?</h2>
        <p>Stay consistent and complete your targets 🚀</p>
        </div>
        """, unsafe_allow_html=True)

        target = st.number_input(
            "Enter Target",
            min_value=1,
            step=1
        )

        if st.button("🚀 Save Target"):

            user_data["target"] = target

            save_data(data)

            st.success("✅ Target Saved Successfully!")

            time.sleep(1)

            st.rerun()

    else:

        target = user_data["target"]

        # =========================
        # DASHBOARD PAGE
        # =========================

        if page == "Dashboard":

            st.title("📊 Freelancer Dashboard")

            total_clients = len(clients)

            yes_count = len([
                c for c in clients
                if c["status"] == "Deal Closed"
            ])

            no_count = len([
                c for c in clients
                if c["status"] == "Cancelled"
            ])

            pending_count = len([
                c for c in clients
                if c["status"] == "No Response"
            ])

            progress = min(total_clients / target, 1.0)

            # =========================
            # METRICS
            # =========================

            c1, c2, c3, c4 = st.columns(4)

            with c1:
                st.markdown(f"""
                <div class="metric-card">
                <h2>{target}</h2>
                <p>🎯 Target</p>
                </div>
                """, unsafe_allow_html=True)

            with c2:
                st.markdown(f"""
                <div class="metric-card">
                <h2>{yes_count}</h2>
                <p>🔥 Closed Deals</p>
                </div>
                """, unsafe_allow_html=True)

            with c3:
                st.markdown(f"""
                <div class="metric-card">
                <h2>{no_count}</h2>
                <p>❌ Cancelled</p>
                </div>
                """, unsafe_allow_html=True)

            with c4:
                st.markdown(f"""
                <div class="metric-card">
                <h2>{pending_count}</h2>
                <p>⏳ Pending</p>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("---")

            # =========================
            # PROGRESS
            # =========================

            st.subheader("🚀 Target Progress")

            st.progress(progress)

            st.write(f"{total_clients}/{target} Clients Added")

            st.markdown("---")

            # =========================
            # SEARCH + FILTER
            # =========================

            search = st.text_input(
                "🔍 Search Client",
                placeholder="Search client name..."
            )

            filter_status = st.selectbox(
                "📂 Filter Status",
                ["All", "Deal Closed", "Cancelled", "No Response"]
            )

            filtered_clients = []

            for client in clients:

                matches_search = (
                    search.lower()
                    in client["client_name"].lower()
                )

                matches_filter = (
                    filter_status == "All"
                    or client["status"] == filter_status
                )

                if matches_search and matches_filter:

                    filtered_clients.append(client)

            st.markdown("---")

            # =========================
            # CLIENTS
            # =========================

            if filtered_clients:

                for index, client in enumerate(filtered_clients):

                    st.markdown(f"""
                    <div class="client-card">

                    <h3>👤 {client['client_name']}</h3>

                    <p>📱 {client['phone']}</p>

                    <p>📅 Follow-Up: {client['date']}</p>

                    <p>💬 {client['last_message']}</p>

                    <p>📌 Status: {client['status']}</p>

                    </div>
                    """, unsafe_allow_html=True)

                    col1, col2, col3 = st.columns(3)

                    # DEAL CLOSED

                    with col1:

                        if st.button(
                            f"🔥 Deal Closed {index}"
                        ):

                            client["status"] = "Deal Closed"

                            save_data(data)

                            st.rerun()

                    # CANCELLED

                    with col2:

                        if st.button(
                            f"❌ Cancelled {index}"
                        ):

                            client["status"] = "Cancelled"

                            save_data(data)

                            st.rerun()

                    # WHATSAPP

                    with col3:

                        phone = str(
                            client["phone"]
                        ).replace("+", "").replace(" ", "")

                        whatsapp_message = (
                            f"Hi {client['client_name']}, "
                            f"just following up regarding our discussion."
                        )

                        whatsapp_url = (
                            f"https://wa.me/{phone}"
                            f"?text={whatsapp_message.replace(' ', '%20')}"
                        )

                        st.markdown(
                            f"""
                            <a href="{whatsapp_url}" target="_blank">
                                <button style="
                                    background:#25D366;
                                    color:white;
                                    border:none;
                                    width:100%;
                                    padding:12px;
                                    border-radius:12px;
                                    font-weight:bold;
                                    cursor:pointer;
                                ">
                                    💬 Open WhatsApp
                                </button>
                            </a>
                            """,
                            unsafe_allow_html=True
                        )

            else:

                st.warning("❌ No matching clients found.")

            # =========================
            # TARGET COMPLETE
            # =========================

            if total_clients >= target:

                st.success(
                    "🎉 Target Completed! Start a new target 🚀"
                )

                if st.button("🚀 New Target"):

                    user_data["target"] = 0
                    user_data["completed_targets"] += 1

                    save_data(data)

                    st.rerun()

        # =========================
        # ADD CLIENT
        # =========================

        if page == "Add Client":

            st.title("➕ Add New Client")

            st.markdown("""
            <div class="goal-box">
            Save client details and manage followups easily 🚀
            </div>
            """, unsafe_allow_html=True)

            client_name = st.text_input(
                "👤 Client Name"
            )

            client_phone = st.text_input(
                "📱 WhatsApp Number",
                placeholder="919876543210"
            )

            last_message = st.text_area(
                "💬 Client Last Message"
            )

            followup_date = st.date_input(
                "📅 Follow-Up Date",
                value=date.today()
            )

            if st.button("💾 Save Client"):

                if (
                    client_name.strip() == ""
                    or client_phone.strip() == ""
                    or last_message.strip() == ""
                ):

                    st.warning(
                        "⚠ Please fill all fields."
                    )

                else:

                    clients.append({
                        "client_name": client_name,
                        "phone": client_phone,
                        "last_message": last_message,
                        "date": str(followup_date),
                        "status": "No Response"
                    })

                    save_data(data)

                    st.success(
                        "✅ Client Saved Successfully! Check your dashboard 🚀"
                    )

                    st.balloons()

                    time.sleep(1.5)

                    st.rerun()

    st.markdown("""
    <div class="footer">
    🚀 Built for ambitious freelancers
    </div>
    """, unsafe_allow_html=True)