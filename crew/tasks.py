import streamlit as st

st.write("🔎 AGENTS: Bắt đầu import...")

st.write("🔎 AGENTS: Import Agent...")
from crewai import Agent
st.write("✅ AGENTS: Import Agent thành công.")

st.write("🔎 AGENTS: Import TavilySearchTool...")
from crewai_tools import TavilySearchTool
st.write("✅ AGENTS: Import TavilySearchTool thành công.")

st.write("🔎 AGENTS: Import dotenv...")
from dotenv import load_dotenv
st.write("✅ AGENTS: Import dotenv thành công.")

st.write("🔎 AGENTS: Nạp biến môi trường...")
load_dotenv(override=True)
st.write("✅ AGENTS: Nạp biến môi trường thành công.")

st.write("🔎 AGENTS: Hoàn thành import.")