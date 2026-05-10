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
    font-family: 'Poppins', sans-serif;
    background: #0f172a;
    color: white;
}

.main {
    background: #0f172a;
}

.stTextInput input,
.stTextArea textarea {
    background: #111827 !important;
    color: white !important;
    border-radius: 12px !important;
    border: 1px solid #374151 !important;
}

.stDateInput input {
    background: #111827 !important;
    color: white !important;
}

.stButton button {
    background: linear-gradient(90deg,#2563eb,#7c3aed);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 12px 20px;
    font-weight: bold;
    width: 100%;
    transition: 0.3s;
}

.stButton button:hover {
    transform: scale(1.02);
}

.card {
    background: #111827;
    padding: 20px;
    border-radius: 18px;
    margin-bottom: 20px;
    border: 1px solid #1f2937;
}

.metric-card {
    background: linear-gradient(135deg,#1e293b,#111827);
    padding: 20px;
    border-radius: 20px;
    text-align: center;
    border: 1px solid #374151;
}

.footer {
    text-align:center;
    margin-top:40px;
    color:#9ca3af;
}

</style>
""", unsafe_allow_html=True)

# =========================
# DATABASE
# =========================

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

# =========================
# SESSION
# =========================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_id" not in st.session_state:
    st.session_state.user_id = ""

# =========================
# LOGIN PAGE
# =========================

if not st.session_state.logged_in:

    st.title("🚀 Freelancer Command Center")

    st.markdown("""
    ### Track clients, followups & close more deals effortlessly.
    """)

    col1, col2 = st.columns(2)

    # =========================
    # CREATE ACCOUNT
    # =========================

    with col1:

        st.subheader("🆕 Create Account")

        st.markdown("""
        <div class="card">
        Start your freelancer journey and manage clients smarter 🚀
        </div>
        """, unsafe_allow_html=True)

        create_name = st.text_input(
            "👤 Your Name",
            placeholder="Enter your name"
        )

        create_user_id = st.text_input(
            "🆔 Create User ID",
            placeholder="Choose a unique ID"
        )

        if st.button("🚀 Create Account"):

            create_name = create_name.strip()
            create_user_id = create_user_id.strip().lower()

            if create_name == "" or create_user_id == "":
                st.warning("⚠ Please fill all fields.")

            elif create_user_id in data:
                st.error("❌ User ID already exists.")

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

                st.success("✅ Account Created Successfully!")
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

    st.sidebar.success(f"👤 {user_data['name']}")

    st.sidebar.info(
        f"🏆 Targets Completed: {user_data.get('completed_targets',0)}"
    )

    st.sidebar.write(f"👥 Total Users: {len(data)}")

    page = st.sidebar.radio(
        "Navigate",
        ["Dashboard", "Add Client"]
    )

    if st.sidebar.button("🚪 Logout"):

        st.session_state.logged_in = False
        st.session_state.user_id = ""

        st.rerun()

    # =========================
    # TARGET
    # =========================

    if user_data.get("target", 0) == 0:

        st.title("🎯 Set Your Client Target")

        target = st.number_input(
            "How many clients do you want to manage?",
            min_value=1,
            step=1
        )

        if st.button("🚀 Save Target"):

            user_data["target"] = target
            save_data(data)

            st.success("✅ Target Saved!")
            time.sleep(1)

            st.rerun()

    else:

        target = user_data["target"]

        # =========================
        # DASHBOARD PAGE
        # =========================

        if page == "Dashboard":

            st.title("📊 Freelancer Dashboard")

            yes_count = len([
                c for c in clients if c["status"] == "Deal Closed"
            ])

            no_count = len([
                c for c in clients if c["status"] == "Cancelled"
            ])

            pending_count = len([
                c for c in clients if c["status"] == "No Response"
            ])

            total_clients = len(clients)

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
                <p>🔥 Deals Closed</p>
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
                <p>⏳ No Response</p>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("---")

            # =========================
            # CLIENT CARDS
            # =========================

            if clients:

                for index, client in enumerate(clients):

                    st.markdown(f"""
                    <div class="card">
                    <h3>👤 {client['client_name']}</h3>

                    <p>📱 {client['phone']}</p>

                    <p>📅 Follow-Up: {client['date']}</p>

                    <p>💬 {client['last_message']}</p>

                    <p>📌 Status: {client['status']}</p>
                    </div>
                    """, unsafe_allow_html=True)

                    col1, col2, col3 = st.columns(3)

                    # =========================
                    # YES BUTTON
                    # =========================

                    with col1:

                        if st.button(
                            f"🔥 Deal Closed {index}"
                        ):

                            clients[index]["status"] = "Deal Closed"

                            save_data(data)

                            st.rerun()

                    # =========================
                    # NO BUTTON
                    # =========================

                    with col2:

                        if st.button(
                            f"❌ Cancelled {index}"
                        ):

                            clients[index]["status"] = "Cancelled"

                            save_data(data)

                            st.rerun()

                    # =========================
                    # WHATSAPP BUTTON
                    # =========================

                    with col3:

                        phone = str(client["phone"]).replace("+", "").replace(" ", "")

                        whatsapp_message = (
                            f"Hi {client['client_name']}, "
                            f"just following up regarding our discussion."
                        )

                        whatsapp_url = (
                            f"https://wa.me/91{phone}"
                            f"?text={whatsapp_message.replace(' ', '%20')}"
                        )

                        st.markdown(
                            f"""
                            <a href="{whatsapp_url}" target="_blank">
                                <button style="
                                    background:#25D366;
                                    color:white;
                                    border:none;
                                    padding:12px;
                                    width:100%;
                                    border-radius:12px;
                                    font-weight:bold;
                                    cursor:pointer;
                                ">
                                    💬 WhatsApp
                                </button>
                            </a>
                            """,
                            unsafe_allow_html=True
                        )

            else:

                st.info("No clients added yet 🚀")

            # =========================
            # TARGET COMPLETE
            # =========================

            if total_clients >= target:

                st.success(
                    "🎉 Target Completed! Set your next client goal 🚀"
                )

                if st.button("🚀 Start New Target"):

                    user_data["target"] = 0
                    user_data["completed_targets"] += 1

                    save_data(data)

                    st.rerun()

        # =========================
        # ADD CLIENT PAGE
        # =========================

        if page == "Add Client":

            st.title("➕ Add New Client")

            st.markdown("""
            <div class="card">
            Add your client details and track followups easily 🚀
            </div>
            """, unsafe_allow_html=True)

            client_name = st.text_input(
                "👤 Client Name"
            )

            client_phone = st.text_input(
                "📱 WhatsApp Number",
                placeholder="9876543210"
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

                    st.warning("⚠ Please fill all fields.")

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
                        f"✅ {client_name} saved successfully — Check your dashboard 🚀"
                    )

                    st.balloons()

                    time.sleep(1.5)

                    st.rerun()

    st.markdown("""
    <div class="footer">
    🚀 Built for ambitious freelancers
    </div>
    """, unsafe_allow_html=True)