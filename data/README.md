# 📦 ML Pipeline Demo (Evolution)

A compact, modular example of an end-to-end machine learning pipeline. This repository shows a clean project structure, clear stage separation, reproducible execution, and MLOps-aligned practices suitable for real-world workflows.

This demo includes:
- Data ingestion  
- Validation  
- Transformation  
- Model training  
- Model evaluation  
- Configuration-driven execution  
- Isolated scripts for each step  
- Artifact and model output management  

The code is organized to be easy to navigate, extend, and integrate with orchestration tools such as Airflow, Prefect, or Dagster.

---

## 🧱 Project Structure
ml-pipeline-demo-evolution/
│
├── configs/                     
│   ├── base.yaml
│   ├── data_ingestion.yaml
│   ├── training.yaml
│   └── evaluation.yaml
│
├── data/                        
│
├── src/
│   ├── ingestion/
│   ├── validation/
│   ├── transform/
│   ├── train/
│   └── evaluate/
│
├── scripts/
│   ├── run_ingestion.py
│   ├── run_validation.py
│   ├── run_transform.py
│   ├── run_training.py
│   └── run_evaluation.py
│
├── models/
│
├── artifacts/
│
├── notebooks/
│
└── README.md



---

## ▶️ How to Run

### **1. Clone**
```bash
git clone https://github.com/ProperAI/ml-pipeline-demo-evolution
cd ml-pipeline-demo-evolution


python scripts/run_ingestion.py --config configs/data_ingestion.yaml
python scripts/run_validation.py --config configs/base.yaml
python scripts/run_transform.py --config configs/base.yaml
python scripts/run_training.py --config configs/training.yaml
python scripts/run_evaluation.py --config configs/evaluation.yaml

Outputs are saved to:

/data
/artifacts
/models

Features
Modular, testable pipeline components
Configuration-driven execution
Clear logging and metrics
Well-defined input/output boundaries per stage
Reproducible, environment-agnostic execution
Easy to extend or orchestrate with workflow tools

Tech Stack
Python 3.10+
Pandas
Scikit-learn
PyYAML
Standard logging


