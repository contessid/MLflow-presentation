# Demo Guide — MLflow in Practice

Quick reference for linking each demo to the presentation slides.

## Setup

| | |
|---|---|
| **MLflow UI** | http://localhost:5050 |
| **Model serving** | http://localhost:5001 |
| **Experiment** | `temperature-forecast-simple` |
| **Registered model** | `temperature-forecast-simple` |
| **Dataset** | Jena Climate — 2,921 days of daily mean temperature (2009–2017) |
| **Train / Test split** | 2,831 / 90 days |

---

## Demo 1 — Experiment Tracking (Slides 7-8)

**Notebook:** `01_experiment_tracking.ipynb`

**What it shows:**
- Manual logging: `log_param()`, `log_metric()`, `log_artifact()`
- Log a statsmodels ARIMA(5,1,0) as `arima_model`
- Bonus: `mlflow.statsmodels.autolog()` with ARIMA(3,1,2)

**Logged to MLflow:**
- Params: `order`, `n_train_days`, `n_test_days`
- Metrics: RMSE, MAE, AIC, BIC
- Artifacts: `forecast.png`, `arima_model/`

**Show in UI:** Open http://localhost:5050 → experiment `temperature-forecast-simple` → click run → params, metrics, artifacts tabs.

---

## Demo 2 — Hyperparameter Tuning with Optuna (Slide 9)

**Notebook:** `02_optuna_tuning.ipynb`

**What it shows:**
- Optuna objective searching ARIMA(p,d,q) with p∈[0,8], d∈[0,2], q∈[0,8]
- Each trial = nested MLflow run under parent `optuna-tuning`
- 50 trials (fast, ~2 min)
- Bonus: `MLflowCallback` approach (10 trials)

**Show in UI:** Expand parent run → nested trials → sort by RMSE → compare best vs worst.

---

## Demo 3 — Infrastructure (Slides 10-14)

**File:** `docker-compose.yml` + `Dockerfile.mlflow`

**What it shows:**
- MLflow server backed by PostgreSQL (local docker-compose)
- Show the YAML, run `docker compose up -d --build`
- Open UI at http://localhost:5050

**Production variant** (notebook `05_production_setup.ipynb`):
- Backend: Supabase PostgreSQL (session pooler, port 5432)
- Artifacts: Azure Blob Storage (`wasbs://`)
- All config from `.env` file

---

## Demo 4 — Model Registry (Slides 15-16)

**Notebook:** `03_model_registry.ipynb`

**What it shows:**
- Register ARIMA(5,1,2) as v1 → assign `@champion` alias
- Load model by alias: `models:/temperature-forecast-simple@champion`
- Register a worse ARIMA(1,0,0) as v2
- Move `@champion` to v2, then rollback to v1

**Show in UI:** Models tab → `temperature-forecast-simple` → versions, aliases.

---

## Demo 5 — Model Serving (Slide 17)

**Notebook:** `04_model_serving.ipynb`

**What it shows:**
- Custom `ARIMAWrapper(mlflow.pyfunc.PythonModel)` — accepts `{"n_steps": N}`, returns forecast
- Register pyfunc as `arima_model` with `@champion` alias

**Part 1 — Local serve:**
```bash
MLFLOW_TRACKING_URI=http://localhost:5050 mlflow models serve \
  -m "models:/temperature-forecast-simple@champion" -p 5001 --no-conda
```

**Part 2 — Docker:**
```bash
MLFLOW_TRACKING_URI=http://localhost:5050 mlflow models build-docker \
  -m "models:/temperature-forecast-simple@champion" -n temp-forecast-server
docker run -p 5001:8080 temp-forecast-server
```

**Test:**
```bash
curl http://localhost:5001/invocations \
  -H "Content-Type: application/json" \
  -d '{"dataframe_split": {"columns": ["n_steps"], "data": [[30]]}}'
```

---

## Bonus — Production Setup

**Notebook:** `05_production_setup.ipynb`

**What it shows:**
- Load secrets from `.env` with `python-dotenv`
- Launch MLflow server with Supabase backend + Azure Blob artifacts
- Smoke test: log params, metrics, and artifact
- Browse artifacts directly in Azure Blob Storage via `azure.storage.blob`
