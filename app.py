import streamlit as st
import json
import os
import time

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Freelancer Command Center",
    page_icon="🚀",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

html, body, [class*="css"]{
    background-color:#0d1117;
    color:white;
    font-family:'Poppins',sans-serif;
}

.main{
    background-color:#0d1117;
}

section[data-testid="stSidebar"]{
    background:linear-gradient(180deg,#111827,#0f172a);
}

.stButton>button{
    width:100%;
    border:none;
    border-radius:14px;
    padding:12px;
    font-weight:bold;
    color:white;
    background:linear-gradient(to right,#00c6ff,#0072ff);
    transition:0.3s;
}

.stButton>button:hover{
    transform:scale(1.02);
    background:linear-gradient(to right,#7f5af0,#2cb67d);
}

.metric-card{
    background:linear-gradient(135deg,#141e30,#243b55);
    padding:22px;
    border-radius:20px;
    text-align:center;
    color:white;
    box-shadow:0px 0px 15px rgba(0,0,0,0.4);
}

.metric-card h2{
    font-size:34px;
}

.card{
    background:linear-gradient(145deg,#161b22,#1f2937);
    padding:22px;
    border-radius:20px;
    margin-bottom:20px;
    border:1px solid #2d3748;
}

.message-box{
    background:#111827;
    padding:15px;
    border-radius:12px;
    border-left:4px solid #00c6ff;
    margin-top:10px;
}

.goal-box{
    background:#161b22;
    padding:25px;
    border-radius:20px;
    border:1px solid #2d3748;
    text-align:center;
}

.footer{
    text-align:center;
    color:#64748b;
    margin-top:30px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- DATA FILE ----------------

DATA_FILE = "freelancer_data.json"

# ---------------- LOAD DATA ----------------

def load_data():

    if os.path.exists(DATA_FILE):

        try:

            with open(DATA_FILE, "r") as f:

                content = f.read().strip()

                if not content:
                    return {}

                return json.loads(content)

        except:
            return {}

    return {}

# ---------------- SAVE DATA ----------------

def save_data(data):

    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ---------------- SESSION ----------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

data = load_data()

# ---------------- LOGIN / SIGNUP ----------------

if not st.session_state.logged_in:

    st.title("🚀 Freelancer Command Center")

    st.markdown("""
    ## Track Clients Like A Pro

    🎯 Set Client Targets  
    📊 Track YES / NO / No Response  
    🚀 Build Consistency  
    🔥 Stay Productive  
    """)

    st.divider()

    col1, col2 = st.columns(2)

    # ---------------- CREATE ACCOUNT ----------------

    with col1:

        st.subheader("🆕 Create Account")

        create_name = st.text_input("👤 Your Name")

        create_user_id = st.text_input("🆔 Create User ID")

        if st.button("Create Account"):

            if create_user_id.strip() == "":
                st.warning("Please enter User ID")

            elif create_user_id in data:
                st.error("❌ User already exists")

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

                time.sleep(1)

                st.rerun()

    # ---------------- LOGIN ----------------

    with col2:

        st.subheader("🔑 Login")

        login_user_id = st.text_input("Enter Your User ID")

        if st.button("Login"):

            if login_user_id in data:

                st.session_state.logged_in = True
                st.session_state.user_id = login_user_id

                st.success("✅ Login Successful!")

                time.sleep(1)

                st.rerun()

            else:
                st.error("❌ User ID not found")

# ---------------- MAIN APP ----------------

else:

    user_id = st.session_state.user_id
    user_data = data[user_id]

    # ---------------- SAFE DEFAULTS ----------------

    user_data.setdefault("target", 0)
    user_data.setdefault("completed_targets", 0)
    user_data.setdefault("clients", [])

    save_data(data)

    clients = user_data["clients"]

    # ---------------- SIDEBAR ----------------

    st.sidebar.title("🚀 Navigation")

    page = st.sidebar.radio(
        "Menu",
        ["Dashboard", "Add Client"]
    )

    st.sidebar.divider()

    st.sidebar.success(f"👤 {user_data['name']}")

    st.sidebar.info(
        f"🏆 Targets Completed: {user_data['completed_targets']}"
    )

    if st.sidebar.button("Logout"):

        st.session_state.logged_in = False

        st.rerun()

    # ---------------- TARGET PAGE ----------------

    if user_data["target"] == 0:

        st.title("🎯 Set Your Client Target")

        st.markdown("""
        <div class="goal-box">
        <h2>How many clients do you want to contact?</h2>
        <p>Set your target and build consistency 🚀</p>
        </div>
        """, unsafe_allow_html=True)

        target = st.number_input(
            "Enter Client Target",
            min_value=1,
            step=1
        )

        if st.button("Save Target"):

            user_data["target"] = target
            user_data["clients"] = []

            save_data(data)

            st.success("✅ Target Saved Successfully!")

            time.sleep(1)

            st.rerun()

    else:

        # ---------------- STATS ----------------

        total_clients = len(clients)

        yes_clients = len([
            c for c in clients
            if c["status"] == "YES"
        ])

        no_clients = len([
            c for c in clients
            if c["status"] == "NO"
        ])

        no_response = len([
            c for c in clients
            if c["status"] == "No Response"
        ])

        target = user_data["target"]

        progress = min(int((total_clients / target) * 100), 100)

        # ---------------- TARGET COMPLETE ----------------

        if total_clients >= target:

            st.balloons()

            st.success("🎉 Target Completed Successfully!")

            st.info("🚀 Set Your New Client Target")

            user_data["completed_targets"] += 1

            user_data["target"] = 0

            save_data(data)

            time.sleep(2)

            st.rerun()

        # ---------------- DASHBOARD ----------------

        if page == "Dashboard":

            st.title(f"🔥 Welcome {user_data['name']}")

            st.markdown("### Your Freelancer Command Center")

            # ---------------- METRIC CARDS ----------------

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.markdown(f"""
                <div class="metric-card">
                <h2>{target}</h2>
                <p>Client Target</p>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"""
                <div class="metric-card">
                <h2>{yes_clients}</h2>
                <p>YES</p>
                </div>
                """, unsafe_allow_html=True)

            with col3:
                st.markdown(f"""
                <div class="metric-card">
                <h2>{no_clients}</h2>
                <p>NO</p>
                </div>
                """, unsafe_allow_html=True)

            with col4:
                st.markdown(f"""
                <div class="metric-card">
                <h2>{no_response}</h2>
                <p>No Response</p>
                </div>
                """, unsafe_allow_html=True)

            st.divider()

            # ---------------- PROGRESS ----------------

            st.subheader("📈 Target Progress")

            st.progress(progress)

            st.write(f"{total_clients} / {target} Clients Added")

            st.divider()

            # ---------------- CLIENTS ----------------

            st.subheader("📋 Clients Overview")

            if len(clients) == 0:

                st.info("No clients added yet.")

            for i, client in enumerate(clients):

                st.markdown('<div class="card">', unsafe_allow_html=True)

                st.subheader(f"👤 {client['client_name']}")

                st.write(f"📅 Follow-Up Date: {client['date']}")

                st.write(f"📌 Status: {client['status']}")

                st.markdown(f"""
                <div class="message-box">
                💬 {client['last_message']}
                </div>
                """, unsafe_allow_html=True)

                st.write("")

                colA, colB, colC = st.columns(3)

                # YES BUTTON

                if colA.button(f"🔥 YES {i}"):

                    client["status"] = "YES"

                    save_data(data)

                    st.rerun()

                # NO BUTTON

                if colB.button(f"❌ NO {i}"):

                    client["status"] = "NO"

                    save_data(data)

                    st.rerun()

                # DELETE BUTTON

                if colC.button(f"🗑 DELETE {i}"):

                    clients.pop(i)

                    save_data(data)

                    st.rerun()

                st.markdown("</div>", unsafe_allow_html=True)

        # ---------------- ADD CLIENT ----------------

        if page == "Add Client":

            st.title("➕ Add New Client")

            client_name = st.text_input("👤 Client Name")

            last_message = st.text_area("💬 Client Last Message")

            followup_date = st.date_input("📅 Follow-Up Date")

            if st.button("Save Client"):

                if client_name.strip() == "" or last_message.strip() == "":

                    st.warning("Please fill all fields.")

                else:

                    clients.append({
                        "client_name": client_name,
                        "last_message": last_message,
                        "date": str(followup_date),
                        "status": "No Response"
                    })

                    save_data(data)

                    st.success(
                        "✅ Client Saved Successfully! Check your dashboard 🚀"
                    )

                    st.balloons()

                    time.sleep(2)

                    st.rerun()

    st.markdown("""
    <div class="footer">
    🚀 Built for ambitious freelancers
    </div>
    """, unsafe_allow_html=True)