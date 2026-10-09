import os
import streamlit as st

from utils.export_docx import create_docx
from utils.export_pdf import create_pdf

from agents.analyst_agent import analyze_project
from agents.llm_utils import is_project_request, NO_ANSWER_MESSAGE

from agents.requirement_agent import generate_requirements
from agents.documentation_agent import generate_srs
from agents.architecture_agent import generate_architecture
from agents.qa_agent import generate_test_cases

from database.db import save_project
from history_page import show_history_page

# ----------------------------------------------------
# 1. PAGE CONFIG (Must be the very first Streamlit command)
# ----------------------------------------------------
st.set_page_config(
    page_title="DocuAI - Requirements to Reality",
    page_icon="🤖",
    layout="wide"
)

# ----------------------------------------------------
# 2. INITIALIZE SESSION STATE
# ----------------------------------------------------
if "page_selection" not in st.session_state:
    st.session_state.page_selection = "Dashboard"

if "analysis_out" not in st.session_state:
    st.session_state.analysis_out = ""
if "req_out" not in st.session_state:
    st.session_state.req_out = ""
if "srs_out" not in st.session_state:
    st.session_state.srs_out = ""
if "arch_out" not in st.session_state:
    st.session_state.arch_out = ""
if "tests_out" not in st.session_state:
    st.session_state.tests_out = ""
if "has_generated" not in st.session_state:
    st.session_state.has_generated = False

# ----------------------------------------------------
# 3. GLOBAL STYLE OVERRIDES
# ----------------------------------------------------
st.markdown("""
<style>
    /* Global Background Overrides */
    .stApp {
        background-color: #060B13 !important;
        color: #F1F5F9 !important;
    }
    .main .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
    }

    /* ---- SIDEBAR NAVIGATION ---- */
    [data-testid="stSidebar"] {
        background-color: #090E17 !important;
        border-right: 1px solid #131A26 !important;
    }
    
    /* Flexbox Header Alignment Layer */
    .sidebar-logo-container {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 5px 8px;
        margin-bottom: 15px;
    }
    
    /* Dynamic Round Contrast Mask for White-Background Logos */
    .sidebar-custom-logo {
        width: 42px;
        height: 42px;
        border-radius: 8px;
        object-fit: cover;
        background-color: #FFFFFF;
        box-shadow: 0 0 10px rgba(0, 210, 255, 0.2);
    }
    
    .sidebar-brand-text {
        font-size: 32px;
        font-weight: 800;
        letter-spacing: 0.5px;
        color: #FFFFFF;
        font-family: 'Inter', sans-serif;
        line-height: 1;
    }
    .sidebar-brand-text span {
        color: #00D2FF;
    }
    
    .sidebar-menu-container {
        margin-top: 10px;
    }
    
    /* Native safe custom sidebar override styling buttons */
    div.element-container button[id^="nav_"] {
        background-color: #2563EB !important;
        color: #FFFFFF !important;
        border: none !important;
        text-align: left !important;
        padding: 12px 16px !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        border-radius: 8px !important;
        margin-bottom: 6px !important;
        display: block !important;
        width: 100% !important;
    }
    div.element-container button[id^="nav_"]:hover {
        background-color: #1D4ED8 !important;
    }
    
    /* Top Hero Banner Styling */
    .hero-container {
        background: linear-gradient(135deg, #102A83 0%, #0B194F 50%, #0384C7 100%);
        padding: 35px;
        border-radius: 12px;
        border: 1px solid #1A2E5A;
        margin-bottom: 25px;
    }
    .hero-container h1 {
        color: #FFFFFF !important;
        font-size: 34px !important;
        font-weight: 700 !important;
        margin-bottom: 5px !important;
    }
    .hero-container p {
        color: #94A3B8 !important;
        font-size: 16px !important;
    }
    .check-tags {
        display: flex;
        gap: 15px;
        flex-wrap: wrap;
        margin-top: 15px;
    }
    .check-item {
        font-size: 13px;
        color: #38BDF8;
        display: flex;
        align-items: center;
        gap: 5px;
    }

    /* KPI Grid Dashboard Metrics */
    .kpi-row {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 16px;
        margin-bottom: 25px;
    }
    .kpi-card {
        background: #0D1527;
        border: 1px solid #16223F;
        border-radius: 10px;
        padding: 18px 22px;
        display: flex;
        align-items: center;
        gap: 15px;
    }
    .kpi-icon-circle {
        width: 44px;
        height: 44px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
    }
    .kpi-title {
        font-size: 12px;
        color: #64748B;
        text-transform: uppercase;
    }
    .kpi-value {
        font-size: 26px;
        font-weight: 700;
        color: #FFFFFF;
    }
    .kpi-trend {
        font-size: 11px;
        color: #475569;
    }

    /* Content Panels */
    .panel-box {
        background: #090F1C;
        border: 1px solid #141F35;
        border-radius: 12px;
        padding: 22px;
        margin-bottom: 20px;
    }
    .panel-header {
        font-size: 16px;
        font-weight: 600;
        color: #FFFFFF;
    }
    .panel-subheader {
        font-size: 12px;
        color: #475569;
        margin-bottom: 15px;
    }

    /* AI Workflow Stepper Nodes */
    .flow-wrapper {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 25px 5px;
    }
    .flow-node {
        text-align: center;
        position: relative;
        flex: 1;
    }
    .flow-node:not(:last-child)::after {
        content: "→";
        position: absolute;
        right: -10%;
        top: 12px;
        color: #334155;
        font-size: 16px;
    }
    .flow-circle {
        width: 42px;
        height: 42px;
        border-radius: 50%;
        margin: 0 auto 8px auto;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
    }
    .flow-label {
        font-size: 12px;
        font-weight: 600;
        color: #FFFFFF;
    }
    .flow-desc {
        font-size: 11px;
        color: #475569;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px !important;
        border-bottom: 1px solid #141F35 !important;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent !important;
        color: #64748B !important;
        font-size: 13px !important;
    }
    .stTabs [aria-selected="true"] {
        color: #6366F1 !important;
        border-bottom: 2px solid #6366F1 !important;
    }

    /* Control Button Overrides */
    div.stButton > button:first-child:not([id^="nav_"]) {
        background: #2563EB !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        height: 42px !important;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# 4. INTERACTIVE SIDEBAR NAVIGATION
# ----------------------------------------------------
with st.sidebar:
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Target absolute path finder
    current_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(current_dir, "projectlogo.png")
    
    # If app execution is at root, fallback check
    if not os.path.exists(logo_path):
        logo_path = "projectlogo.png"

    if os.path.exists(logo_path):
        # Premium layout injection wrapping your project logo asset fluidly
        import base64
        with open(logo_path, "rb") as f:
            encoded_img = base64.b64encode(f.read()).decode()
            
        st.markdown(f"""
            <div class="sidebar-logo-container">
                <img class="sidebar-custom-logo" src="data:image/png;base64,{encoded_img}">
                <div class="sidebar-brand-text">Docu<span>AI</span></div>
            </div>
        """, unsafe_allow_html=True)
    else:
        # High-fidelity alignment fallback logic if the asset isn't matched
        st.markdown("""
            <div class="sidebar-logo-container">
                <span style="font-size: 34px; line-height: 1;">🤖</span>
                <div class="sidebar-brand-text">Docu<span>AI</span></div>
            </div>
        """, unsafe_allow_html=True)

    # Dynamic Navigation Menu Options
    pages = ["Dashboard", "Generate Project", "Project History", "Templates", "Analytics", "Export History", "Settings", "Help & Support"]
    icons = ["🏠", "📥", "🕒", "🗂️", "📊", "📤", "⚙️", "❓"]
    
    st.markdown('<div class="sidebar-menu-container">', unsafe_allow_html=True)
    for p, icon in zip(pages, icons):
        if st.button(f"{icon}  {p}", key=f"nav_{p}", use_container_width=True):
            st.session_state.page_selection = p
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: #0B111E; border: 1px solid #141F35; padding: 20px; border-radius: 10px; text-align: center;">
        <span style="font-size: 32px;">🤖</span>
        <div style="font-size: 14px; font-weight: 600; color: #FFFFFF; margin-top: 10px;">AI Agents Working</div>
        <p style="font-size: 12px; color: #475569; margin: 6px 0 15px 0;">Our AI agents are ready to transform your idea into complete documentation.</p>
        <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.2); color: #10B981; font-size: 12px; padding: 6px; border-radius: 20px; display: inline-block; width: 100%;">
            ● All Systems Operational
        </div>
    </div>
    """, unsafe_allow_html=True)

# ----------------------------------------------------
# 5. PAGE ROUTING CONTEXT CHECKS
# ----------------------------------------------------
if st.session_state.page_selection == "Project History":
    show_history_page()
    st.stop()

if st.session_state.page_selection not in ["Dashboard", "Generate Project"]:
    st.info(f"Welcome to the {st.session_state.page_selection} module. This section is currently loading configurations.")
    st.stop()

# ----------------------------------------------------
# 6. MAIN DASHBOARD INTERFACE
# ----------------------------------------------------
st.markdown("""
<div class="hero-container">
    <h1>DocuAI Platform</h1>
    <p>Transform your ideas into comprehensive documentation using AI — Requirements to Reality</p>
    <div class="check-tags">
        <div class="check-item">✔ Business Analysis</div>
        <div class="check-item">✔ Requirements Engineering</div>
        <div class="check-item">✔ SRS Documentation</div>
        <div class="check-item">✔ Architecture Design</div>
        <div class="check-item">✔ Test Case Generation</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="kpi-row">
    <div class="kpi-card">
        <div class="kpi-icon-circle" style="background: rgba(37, 99, 235, 0.15); color: #3B82F6;">📊</div>
        <div>
            <div class="kpi-title">Total Projects</div>
            <div class="kpi-value">128</div>
            <div class="kpi-trend">+12 this month</div>
        </div>
    </div>
    <div class="kpi-card">
        <div class="kpi-icon-circle" style="background: rgba(16, 185, 129, 0.15); color: #10B981;">⚙️</div>
        <div>
            <div class="kpi-title">Requirements Generated</div>
            <div class="kpi-value">2,450+</div>
            <div class="kpi-trend">+180 this month</div>
        </div>
    </div>
    <div class="kpi-card">
        <div class="kpi-icon-circle" style="background: rgba(139, 92, 246, 0.15); color: #8B5CF6;">📝</div>
        <div>
            <div class="kpi-title">SRS Documents</div>
            <div class="kpi-value">128</div>
            <div class="kpi-trend">+12 this month</div>
        </div>
    </div>
    <div class="kpi-card">
        <div class="kpi-icon-circle" style="background: rgba(249, 115, 22, 0.15); color: #F97316;">🧪</div>
        <div>
            <div class="kpi-title">Test Cases Generated</div>
            <div class="kpi-value">5,680+</div>
            <div class="kpi-trend">+420 this month</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

col_left_input, col_right_workflow = st.columns([1.1, 0.9], gap="medium")

with col_left_input:
    st.markdown("""
    <div class="panel-box" style="margin-bottom:0px;">
        <div class="panel-header">💡 Describe Your Project Idea</div>
        <div class="panel-subheader">Provide a detailed description of your software project or idea.</div>
    """, unsafe_allow_html=True)
    
    idea = st.text_area(
        "Project description workspace field layer",
        height=125,
        label_visibility="collapsed",
        placeholder="Example: Develop an AI-Powered Customer Support Center for a large e-commerce company..."
    )
    
    c_btn1, c_btn2 = st.columns([1, 3])
    with c_btn1:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.analysis_out = ""
            st.session_state.req_out = ""
            st.session_state.srs_out = ""
            st.session_state.arch_out = ""
            st.session_state.tests_out = ""
            st.session_state.has_generated = False
            st.rerun()
    with c_btn2:
        generate = st.button("🚀 Generate Documentation", use_container_width=True)
        
    st.markdown("</div>", unsafe_allow_html=True)

with col_right_workflow:
    st.markdown("""
    <div class="panel-box" style="margin-bottom:0px;">
        <div class="panel-header">DocuAI Workflow</div>
        <div class="flow-wrapper">
            <div class="flow-node">
                <div class="flow-circle" style="background: rgba(168, 85, 247, 0.15); color: #A855F7; border: 1px dashed #A855F7;">💡</div>
                <div class="flow-label">Idea</div>
                <div class="flow-desc">Your Idea</div>
            </div>
            <div class="flow-node">
                <div class="flow-circle" style="background: rgba(16, 185, 129, 0.15); color: #10B981;">🤖</div>
                <div class="flow-label">Analyst</div>
                <div class="flow-desc">Analyzing</div>
            </div>
            <div class="flow-node">
                <div class="flow-circle" style="background: rgba(59, 130, 246, 0.15); color: #3B82F6;">📋</div>
                <div class="flow-label">Requirement</div>
                <div class="flow-desc">Generating</div>
            </div>
            <div class="flow-node">
                <div class="flow-circle" style="background: rgba(139, 92, 246, 0.15); color: #8B5CF6;">📄</div>
                <div class="flow-label">SRS Agent</div>
                <div class="flow-desc">Creating</div>
            </div>
            <div class="flow-node">
                <div class="flow-circle" style="background: rgba(249, 115, 22, 0.15); color: #F97316;">🕸️</div>
                <div class="flow-label">Architecture</div>
                <div class="flow-desc">Designing</div>
            </div>
            <div class="flow-node">
                <div class="flow-circle" style="background: rgba(14, 165, 233, 0.15); color: #0EA5E9;">🛡️</div>
                <div class="flow-label">QA Agent</div>
                <div class="flow-desc">Testing</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ----------------------------------------------------
# 7. AGENT PROCESSING EXECUTION LOOP
# ----------------------------------------------------

if generate:

    if not is_project_request(idea):

        st.error(NO_ANSWER_MESSAGE)

    else:

        with st.status(
            "🚀 Executing DocuAI Orchestrator Pipeline...",
            expanded=True
        ) as status:

            # ----------------------------------------
            # ANALYST AGENT
            # ----------------------------------------
            st.write("🔄 Running Analyst Agent...")

            analysis_result = analyze_project(idea)

            st.session_state.analysis_out = analysis_result

            if analysis_result:
                st.write("✅ Analyst Agent completed")
            else:
                st.write("⚠️ Analyst Agent returned no output")


            # ----------------------------------------
            # REQUIREMENT AGENT
            # ----------------------------------------
            st.write("🔄 Running Requirement Agent...")

            requirements_result = generate_requirements(idea)

            st.session_state.req_out = requirements_result

            if requirements_result:
                st.write("✅ Requirement Agent completed")
            else:
                st.write("⚠️ Requirement Agent returned no output")


            # ----------------------------------------
            # DOCUMENTATION AGENT
            # ----------------------------------------
            st.write("🔄 Running Documentation Agent...")

            srs_result = generate_srs(
                st.session_state.req_out
            )

            st.session_state.srs_out = srs_result

            if srs_result:
                st.write("✅ Documentation Agent completed")
            else:
                st.write("⚠️ Documentation Agent returned no output")


            # ----------------------------------------
            # ARCHITECTURE AGENT
            # ----------------------------------------
            st.write("🔄 Running Architecture Agent...")

            architecture_result = generate_architecture(
                st.session_state.req_out
            )

            st.session_state.arch_out = architecture_result

            if architecture_result:
                st.write("✅ Architecture Agent completed")
            else:
                st.write("⚠️ Architecture Agent returned no output")


            # ----------------------------------------
            # QA AGENT
            # ----------------------------------------
            st.write("🔄 Running QA Agent...")

            tests_result = generate_test_cases(
                st.session_state.req_out
            )

            st.session_state.tests_out = tests_result

            if tests_result:
                st.write("✅ QA Agent completed")
            else:
                st.write("⚠️ QA Agent returned no output")


            # ----------------------------------------
            # DATABASE
            # ----------------------------------------
            st.write("💾 Saving project to database...")

            save_project(
                idea,
                st.session_state.analysis_out,
                st.session_state.req_out,
                st.session_state.srs_out,
                st.session_state.arch_out,
                st.session_state.tests_out
            )

            st.session_state.has_generated = True

            status.update(
                label="🎉 Complete Documentation Suite Generated!",
                state="complete"
            )
# ----------------------------------------------------
# 8. OUTPUT PANELS & ENGINEERING DIAGRAMS
# ----------------------------------------------------

t1, t2, t3, t4, t5 = st.tabs([
    "📊 Business Analysis",
    "📋 Requirements Engineering",
    "📄 SRS Documentation",
    "🏗️ Architecture & Diagrams",
    "🧪 Test Cases"
])

# ----------------------------------------------------
# TAB 1 - BUSINESS ANALYSIS
# ----------------------------------------------------
with t1:
    st.subheader("📊 Business Analysis")

    if st.session_state.analysis_out:
        st.markdown(
            '<div class="panel-box">',
            unsafe_allow_html=True
        )

        st.markdown(st.session_state.analysis_out)

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )
    else:
        st.info("Generate a project to view the Business Analysis.")


# ----------------------------------------------------
# TAB 2 - REQUIREMENTS
# ----------------------------------------------------
with t2:
    st.subheader("📋 Requirements Engineering")

    if st.session_state.req_out:
        st.markdown(
            '<div class="panel-box">',
            unsafe_allow_html=True
        )

        st.markdown(st.session_state.req_out)

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )
    else:
        st.info("Generate a project to view the Requirements.")


# ----------------------------------------------------
# TAB 3 - SRS
# ----------------------------------------------------
with t3:
    st.subheader("📄 Software Requirements Specification")

    if st.session_state.srs_out:
        st.markdown(
            '<div class="panel-box">',
            unsafe_allow_html=True
        )

        st.markdown(st.session_state.srs_out)

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )
    else:
        st.info("Generate a project to view the SRS document.")


# ----------------------------------------------------
# TAB 4 - ARCHITECTURE
# ----------------------------------------------------
with t4:

    st.subheader("🏗️ System Architecture")

    if st.session_state.arch_out:

        st.markdown(
            '<div class="panel-box">',
            unsafe_allow_html=True
        )

        st.markdown(st.session_state.arch_out)

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )

    else:
        st.info("Generate a project to view the Architecture.")


    # ------------------------------------------------
    # SYSTEM ARCHITECTURE DIAGRAM
    # ------------------------------------------------
    st.subheader("🕸️ System Architecture Diagram")

    st.graphviz_chart("""
    digraph {

        bgcolor="#090F1C"

        node [
            color="#6366F1"
            fontcolor="#FFFFFF"
            style=filled
            fillcolor="#131F35"
            shape=box
            fontname="Helvetica"
        ]

        edge [
            color="#334155"
            arrowhead=vee
        ]

        User -> Streamlit
        Streamlit -> FastAPI
        FastAPI -> LangGraph

        LangGraph -> AnalystAgent
        LangGraph -> RequirementAgent
        LangGraph -> DocumentationAgent
        LangGraph -> ArchitectureAgent
        LangGraph -> QAAgent

        RequirementAgent -> FAISS
        LangGraph -> SQLite
        Ollama -> LangGraph
    }
    """, use_container_width=True)


    # ------------------------------------------------
    # USE CASE DIAGRAM
    # ------------------------------------------------
    st.subheader("🎯 Use Case Diagram")

    st.graphviz_chart("""
    digraph {

        bgcolor="#090F1C"

        rankdir=LR

        node [
            color="#10B981"
            fontcolor="#FFFFFF"
            style=filled
            fillcolor="#131F35"
            fontname="Helvetica"
        ]

        edge [
            color="#334155"
        ]

        Customer [shape=box color="#3B82F6"]
        Pharmacist [shape=box color="#F59E0B"]
        Admin [shape=box color="#8B5CF6"]

        BrowseMedicines [label="Browse Medicines"]
        SearchMedicine [label="Search Medicines"]
        PlaceOrder [label="Place Order"]
        UploadPrescription [label="Upload Prescription"]
        TrackOrder [label="Track Order"]
        ManageMedicines [label="Manage Medicines"]

        Customer -> BrowseMedicines
        Customer -> SearchMedicine
        Customer -> PlaceOrder
        Customer -> UploadPrescription
        Customer -> TrackOrder

        Pharmacist -> ManageMedicines
        Admin -> ManageMedicines
    }
    """, use_container_width=True)


    # ------------------------------------------------
    # ER DIAGRAM
    # ------------------------------------------------
    st.subheader("🧬 ER Diagram")

    st.graphviz_chart("""
    digraph {

        bgcolor="#090F1C"

        rankdir=LR

        node [
            color="#2563EB"
            fontcolor="#FFFFFF"
            style="rounded,filled"
            fillcolor="#131F35"
            shape=box
            fontname="Helvetica"
        ]

        edge [
            color="#38BDF8"
            arrowhead=vee
        ]

        User
        Medicine
        Prescription
        Order
        OrderItem
        Payment
        Pharmacist
        Delivery

        User -> Order
        User -> Prescription
        Order -> OrderItem
        OrderItem -> Medicine
        Prescription -> Pharmacist
        Order -> Payment
        Order -> Delivery
    }
    """, use_container_width=True)


# ----------------------------------------------------
# TAB 5 - TEST CASES
# ----------------------------------------------------
with t5:

    st.subheader("🧪 Software Test Cases")

    if st.session_state.tests_out:

        st.markdown(
            '<div class="panel-box">',
            unsafe_allow_html=True
        )

        st.markdown(st.session_state.tests_out)

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )

    else:
        st.info("Generate a project to view the Test Cases.")

# ----------------------------------------------------
# 9. BOTTOM FOOTER EXPORT ACTION DRAWER
# ----------------------------------------------------
if st.session_state.has_generated:
    st.markdown("---")
    full_report_content = f"BUSINESS ANALYSIS\n\n{st.session_state.analysis_out}\n\nREQUIREMENTS\n\n{st.session_state.req_out}\n\nSRS\n\n{st.session_state.srs_out}\n\nARCHITECTURE\n\n{st.session_state.arch_out}\n\nTEST CASES\n\n{st.session_state.tests_out}"

    col_e1, col_e2, col_e3, col_e4 = st.columns(4)
    with col_e1:
        st.button("📥 Export DocuAI Suite Options", disabled=True, use_container_width=True)
    with col_e2:
        st.download_button("📄 Export as TXT", data=full_report_content, file_name="docuai_srs.txt", mime="text/plain", use_container_width=True)
    with col_e3:
        docx_file = create_docx(full_report_content)
        with open(docx_file, "rb") as file:
            st.download_button("📝 Export as DOCX", data=file, file_name="docuai_srs.docx", use_container_width=True)
    with col_e4:
        pdf_file = create_pdf(full_report_content)
        with open(pdf_file, "rb") as file:
            st.download_button("📕 Export as PDF", data=file, file_name="docuai_srs.pdf", use_container_width=True)