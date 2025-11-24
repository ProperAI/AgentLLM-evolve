from rag.ingest import main as ingest_main
import argparse


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="CLI wrapper for RAG ingestion/indext build"
    )

    parser.add_argument("--mode", # moder: override config.mode"
        help="Override mode (default priority: --mode > APP_MODE env > config.yaml > 'local')",
        required=True)
    
    parser.add_argument("--config", default="config.yaml", help="Path to config YAML (default: config.yaml)")
    args = parser.parse_args()

    ingest_main(mode_arg = args.mode, cfg_path=args.config)

    
    

  

                         