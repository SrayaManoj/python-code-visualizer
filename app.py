import streamlit as st
import os, zipfile, shutil
from parser.code_parser import parse_directory
from visualizer.graph_builder import build_graph

st.set_page_config(page_title="Codebase Graph", layout="wide")

st.title("🧠 Codebase Knowledge Graph")
st.write("Upload a zip of your Python project and see how it connects.")

uploaded_file = st.file_uploader("Upload a ZIP file of your Python code", type="zip")

if uploaded_file:
    # Save the zip file
    with open("code.zip", "wb") as f:
        f.write(uploaded_file.read())

    # Extract it
    with zipfile.ZipFile("code.zip", 'r') as zip_ref:
        zip_ref.extractall("code_dir")

    # Parse the codebase
    items, edges = parse_directory("code_dir")

    # Build the graph with nodes and edges
    build_graph(items, edges)

    # Display the HTML graph
    st.components.v1.html(open("templates/code_graph.html", "r").read(), height=600)

    # Clean up
    shutil.rmtree("code_dir")
    os.remove("code.zip")
