import streamlit as st
from database.db import get_projects


def show_history_page():

    st.title("📚 Project History")

    projects = get_projects()

    if not projects:
        st.warning("No projects found.")
        return

    for project in projects:

        (
            project_id,
            project_name,
            analysis,
            requirements,
            srs,
            architecture,
            tests,
            created_at
        ) = project

        with st.expander(
            f"📌 {project_name} ({created_at})"
        ):

            st.subheader("Business Analysis")
            st.markdown(analysis)

            st.subheader("Requirements")
            st.markdown(requirements)

            st.subheader("SRS")
            st.markdown(srs)

            st.subheader("Architecture")
            st.markdown(architecture)

            st.subheader("Test Cases")
            st.markdown(tests)