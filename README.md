# Disease Detection from Symptoms

A Flask web app that matches selected symptoms or a short text description to possible conditions using a machine learning model. The included dataset is synthetic, so results are for educational use only and are not medical advice or a diagnosis.

## Run locally

Use Python 3.11 or newer. From the project root:

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

Open <http://127.0.0.1:5000>.

The trained model is included in `model/`. To rebuild it from the included synthetic data, run:

```bash
python create_dataset.py
python dataset/train_model.py
```

## Publish the source on GitHub

Create an empty repository on GitHub, then run these commands from this folder (replace the URL with your repository URL):

```bash
git add .
git commit -m "Prepare disease detection app for deployment"
git branch -M main
git remote add origin https://github.com/USERNAME/REPOSITORY.git
git push -u origin main
```

GitHub stores the source; it does not run this Flask app as a website. To host it, connect the repository to a Python web host such as Render. The included `Procfile` starts the app with Gunicorn; use `pip install -r requirements.txt` as the host's build command. Keep the `model/` files in the repository because the app loads them at startup.

## Features

- Checkbox-based symptom selection.
- Natural-language symptom extraction and prediction endpoints.
- Model confidence and alternative matches where available.
- Educational information and a medical disclaimer.

## Project structure

```text
app.py                       Flask application
create_dataset.py            Synthetic dataset generator
dataset/train_model.py       Model training pipeline
dataset/disease_symptoms.csv Synthetic training data
model/                       Trained model and feature metadata
static/                      CSS and JavaScript
templates/                   HTML templates
utils/                       Symptom parsing and condition information
requirements.txt             Python dependencies
Procfile                     Gunicorn web process
```

The current saved evaluation metrics are in `model/model_metrics.json`. The model was evaluated at 67.5% accuracy on a held-out split of the synthetic dataset; this does not indicate real-world clinical accuracy.

## Medical disclaimer

This project is for educational and informational purposes only. It does not provide a diagnosis and cannot replace assessment by a qualified healthcare professional. Seek urgent care for severe or rapidly worsening symptoms.
