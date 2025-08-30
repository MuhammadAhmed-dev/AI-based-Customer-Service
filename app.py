# === app.py (Flask app entry point) ===
from flask import Flask, render_template, request
import os, time
from utils.safety import sanitize_input
from utils.pdf_loader import extract_text_from_pdf
from utils.embedder import get_embeddings, get_model_dimension
from utils.vector_store import VectorStore
from utils.query_handler import retrieve_answer
import webbrowser
import threading
from utils.demo import check_demo_expiry

start_total = time.perf_counter()
print("=== Timer Started ===")

t0 = time.perf_counter()
check_demo_expiry()
print(f"[Timer] Demo check: {time.perf_counter() - t0:.3f} sec")

app = Flask(__name__)

vs = None

# === Load and embed PDF once ===
PDF_PATH = "pdfs/ThaiRecipes.pdf"  # Preloaded static PDF

t1 = time.perf_counter()
print("Loading and embedding PDF...")

# Extract text
t_extract = time.perf_counter()
chunks = extract_text_from_pdf(PDF_PATH)
print(f"[Timer] PDF extraction: {time.perf_counter() - t_extract:.3f} sec")

# Embedding
t_embed = time.perf_counter()
embeddings = get_embeddings(chunks)
print(f"[Timer] Embedding generation: {time.perf_counter() - t_embed:.3f} sec")

# Vector store
t_vs = time.perf_counter()
vs = VectorStore(get_model_dimension()) # dimension for my embedder is 384
vs.add(embeddings, chunks)
print(f"[Timer] Vector store init + add: {time.perf_counter() - t_vs:.3f} sec")

print("Done.")
print(f"[Timer] Total pre-load setup: {time.perf_counter() - t1:.3f} sec")

@app.route("/", methods=["GET", "POST"])
def index():
    answer = None
    question = None

    if request.method == "POST":
        t_post = time.perf_counter()
        question = request.form.get("question")
        if question:
            sanitized = sanitize_input(question)
            if sanitized.startswith("⚠️"):
                answer = sanitized
            else:
                t_retrieve = time.perf_counter()
                answer = retrieve_answer(question, vs, history=[])
                print(f"[Timer] Answer retrieval: {time.perf_counter() - t_retrieve:.3f} sec")
        print(f"[Timer] Request handling: {time.perf_counter() - t_post:.3f} sec")
    return render_template("index.html", answer=answer, question=question)

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

if __name__ == "__main__":
    print(f"[Timer] Total import + setup: {time.perf_counter() - start_total:.3f} sec")
    threading.Timer(1.0, open_browser).start()
    app.run(debug=False)
