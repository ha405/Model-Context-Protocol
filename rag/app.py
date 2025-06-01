import argparse
import streamlit as st
from generator import RAGGenerator

parser = argparse.ArgumentParser()
parser.add_argument("--server-url", type=str, default="http://localhost:4000/rpc")
parser.add_argument("--owner", type=str, required=True)
parser.add_argument("--repo", type=str, required=True)
parser.add_argument("--branch", type=str, default="main")
parser.add_argument("--chunk-size", type=int, default=300)
parser.add_argument("--overlap", type=int, default=50)
parser.add_argument("--top-k", type=int, default=3)
args, _ = parser.parse_known_args()

st.set_page_config(page_title="RAG Assistant", layout="centered")
st.title("📄🔍 RAG-powered Assistant")

question = st.text_input("Ask a question:", "")

if st.button("Get Answer") and question:
    rag = RAGGenerator(args.server_url, args.chunk_size, args.overlap)
    rag.initialize(args.owner, args.repo, args.branch)
    answer = rag.answer_query(question, args.top_k)
    st.markdown("### ✅ Answer")
    st.write(answer)
