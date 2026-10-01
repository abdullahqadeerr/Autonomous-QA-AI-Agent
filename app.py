from __future__ import annotations

import json
import os
from pathlib import Path

import streamlit as st

from agent.orchestrator import QAOrchestrator
from config.settings import settings

def _init_session_state() -> None:
    if "orchestrator" not in st.session_state:
        st.session_state.orchestrator = QAOrchestrator()
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []


def _render_sidebar() -> None:
    st.sidebar.title("QA Agent")
    st.sidebar.caption("Autonomous conversational quality assurance")

    target_url = st.sidebar.text_input("Website URL", value=st.session_state.get("target_url", "https://www.saucedemo.com/"))
    requirement = st.sidebar.text_area(
        "Requirement / User Story",
        value=st.session_state.get("requirement", "Verify that a valid user can log in and an invalid user cannot log in."),
        height=150,
    )
    mode = st.sidebar.selectbox("Operating mode", ["interactive", "autonomous"], index=0)
    headless = st.sidebar.checkbox("Headless browser", value=settings.default_headless)

    if st.sidebar.button("Start Session"):
        st.session_state.target_url = target_url
        st.session_state.requirement = requirement
        st.session_state.mode = mode
        st.session_state.headless = headless
        st.session_state.orchestrator.start_session(
            url=target_url,
            requirement=requirement,
            mode=mode,
            headless=headless,
        )
        st.success("Session started.")

    if st.sidebar.button("Stop Execution"):
        st.session_state.orchestrator.stop_execution()
        st.warning("Execution requested to stop.")

    st.sidebar.markdown("### Session")
    session = st.session_state.orchestrator.session
    status = session.get("status", "idle") if isinstance(session, dict) else "idle"
    stage = session.get("current_stage", "idle") if isinstance(session, dict) else "idle"
    st.sidebar.write(f"Status: {status}")
    st.sidebar.write(f"Stage: {stage}")



def _render_messages() -> None:
    for role, content in st.session_state.chat_history:
        with st.chat_message(role):
            st.markdown(content)



def main() -> None:
    st.set_page_config(page_title="Autonomous QA Agent", layout="wide")
    _init_session_state()
    _render_sidebar()

    st.title("Autonomous Conversational QA Agent")
    st.caption("Talk to the QA agent, review the session state, and run website QA automation.")

    _render_messages()

    if prompt := st.chat_input("Tell the agent what to do..."):
        st.session_state.chat_history.append(("user", prompt))
        with st.chat_message("user"):
            st.markdown(prompt)

        response = st.session_state.orchestrator.handle_message(prompt)
        st.session_state.chat_history.append(("assistant", response))
        with st.chat_message("assistant"):
            st.markdown(response)

    qa = st.session_state.orchestrator.session
    if not qa:
        return

    with st.expander("Session data", expanded=False):
        st.json(qa)

    status_cols = st.columns(5)
    metrics = {
        "Total Tests": qa.get("test_summary", {}).get("total_tests", 0),
        "Passed": qa.get("test_summary", {}).get("passed", 0),
        "Failed": qa.get("test_summary", {}).get("failed", 0),
        "Skipped": qa.get("test_summary", {}).get("skipped", 0),
        "Repaired": qa.get("test_summary", {}).get("repaired", 0),
    }
    for i, (label, value) in enumerate(metrics.items()):
        with status_cols[i]:
            st.metric(label, value)

    if qa.get("website_analysis"):
        with st.expander("Website Analysis"):
            st.json(qa["website_analysis"])

    if qa.get("test_plan"):
        with st.expander("Test Plan"):
            st.json(qa["test_plan"])

    if qa.get("generated_tests"):
        with st.expander("Generated Playwright Code"):
            st.code(qa["generated_tests"][0]["content"], language="python") if qa["generated_tests"] else None

    if qa.get("execution_log"):
        with st.expander("Execution Logs"):
            st.text(qa["execution_log"])

    if qa.get("bug_reports"):
        with st.expander("Bug Reports"):
            st.json(qa["bug_reports"])


if __name__ == "__main__":
    main()
