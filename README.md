# MLflow in Practice — Live Demos

Demo notebooks for the **"MLflow in Practice"** talk at Cloud Native Trento.

All demos use the **Jena Climate dataset** (daily mean temperature) with **ARIMA models** for time series forecasting.

## Prerequisites

- Python 3.10+
- Docker & Docker Compose

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start MLflow server (PostgreSQL backend)
docker compose up -d --build

# 3. Open MLflow UI
open http://localhost:5050

# 4. Launch Jupyter
jupyter notebook notebooks/
```

## Demo Sequence

| #   | Notebook                       | Topic                                           |
| --- | ------------------------------ | ----------------------------------------------- |
| 0   | `00_download_data.ipynb`       | Download & preprocess Jena Climate data         |
| 1   | `01_experiment_tracking.ipynb` | Experiment tracking: params, metrics, artifacts |
| 2   | `02_optuna_tuning.ipynb`       | Hyperparameter tuning with Optuna + nested runs |
| 3   | `docker-compose.yml`           | Infrastructure: MLflow server + PostgreSQL      |
| 4   | `03_model_registry.ipynb`      | Model Registry: versioning & aliases            |
| 5   | `04_model_serving.ipynb`       | Model serving: REST API & Docker                |
| 6   | `05_production_setup.ipynb`    | Production: Supabase + Azure Blob               |

> Notebook **00** is to download the data. Notebooks 01-04 each work standalone as long as `data/jena_daily_temp.csv` exists.

## Inspecting the local PostgreSQL Database

```bash
# Connect to the local PostgreSQL
docker compose exec postgres psql -U mlflow -d mlflow

# Quick queries
SELECT * FROM experiments;
SELECT run_uuid, name, status FROM runs ORDER BY start_time DESC LIMIT 10;
SELECT * FROM registered_models;
```
