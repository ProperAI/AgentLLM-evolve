
from dotenv import load_dotenv
load_dotenv()

import sys; print(sys.executable)

import os
import pickle

from pathlib import Path
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from box import Box

import yaml

CFG_PATH = "config.yaml"

def load_config(cfg_path: str = CFG_PATH):
    with  open(cfg_path, "r") as f:
        return Box(yaml.safe_load(f))
    
def main(mode_arg: str | None = None, cfg_path: str = CFG_PATH):
    config = load_config(cfg_path)
    mode = mode_arg or os.getenv("APP_MODE") or "local"
    notes_dir = config.paths[mode].notes_dir
    vectordb_dir = Path(config.paths[mode].vectordb_dir)
    vectordb_dir.mkdir(parents=True, exist_ok = True)

    loader = DirectoryLoader(notes_dir, glob="**/*.md", loader_cls=TextLoader)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.rag.chunk_size,  
        chunk_overlap=config.rag.chunk_overlap
    )
    splits = splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings(
        model_name=config.rag.model_name
    )

    vectordb = FAISS.from_documents(splits, embeddings)

    # persists: faiss + docstore
    faiss_path = vectordb_dir / "index.faiss"
    pkl_path = vectordb_dir / "index.pkl"
    vectordb.save_local(str(vectordb_dir))
    print(f"Ingested {len(splits)} chunks into {vectordb_dir}")

    
