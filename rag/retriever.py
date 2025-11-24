import yaml
from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from box import Box

CFG_PATH = "config.yaml"

def load_config():
    with open(CFG_PATH, "r") as f:
        return Box(yaml.safe_load(f))
    
def get_retriever(k: int=3):
    config = load_config()
    mode = config.mode or "local"
    vectordb_dir = config.paths[mode].vectordb_dir
    embeddings = HuggingFaceEmbeddings(model_name=
                                       config.rag.model_name)
    
    db = FAISS.load_local(
        vectordb_dir, embeddings, allow_dangerous_deserialization=True,
    )
    #jwk note: as_retriever implents LangChain Retriever interface, which has .get_reevant_doucuments(query) method
    return db.as_retriever(search_kwargs={"k": k})


    


    

