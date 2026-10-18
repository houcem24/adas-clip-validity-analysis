# Driving-Clip Validity Analysis for ADAS Data

Master's thesis project (ESPRIT, in collaboration with Magna Electronics, Sailauf). It turns a folder of
recorded driving clips into a clean, analysable dataset, predicts whether a clip is valid for downstream use,
and exposes the results through a Flask web app.

Each clip comes with a JSON annotation describing the recorded scenario: weather, light conditions, maneuver,
parking situation, static and dynamic objects, plus start/end frames, timestamps and GPS positions of the video
and of the annotated scene. The project checks, repairs and models this metadata.

## What it does

1. **Collection:** walks ~5,500 clip folders, keeps the ones with an annotation file and flattens each JSON
   into one row (15,081 rows, 37 columns).
2. **Repair and preprocessing:** fixes inconsistent categorical values, encodes the 13 scenario attributes,
   imputes missing numeric fields and checks timestamp/frame consistency between video and scene boundaries.
3. **Augmentation:** creates synthetic records by perturbing the video and scene timestamps of existing clips
   (up to ±8 s) to enlarge the training set.
4. **Modelling:** compares ten classifiers on predicting `CLIP_VALIDITY`.
5. **Web app:** browse the dataset, view clip statistics, and get a validity prediction for a clip from a form.

## Results

Held-out test set; about 66% of clips are valid, so always predicting "valid" scores 0.66 accuracy.

| Model | Accuracy | Precision | Recall | F1 |
|---|---|---|---|---|
| **Random Forest + AdaBoost** | **0.71** | 0.73 | 0.87 | **0.80** |
| Random Forest | 0.70 | 0.73 | 0.86 | 0.79 |
| XGBoost | 0.69 | 0.72 | 0.87 | 0.79 |
| KNN | 0.69 | 0.73 | 0.82 | 0.78 |
| Gradient Boosting | 0.68 | 0.68 | 0.97 | 0.80 |

The tree ensembles beat the majority baseline by about five points; Logistic Regression, SVM and Naive Bayes
collapsed to predicting the majority class. The Random Forest model is the one served by the web app.

## Repository structure

```
├── Prediction.ipynb               # Data collection, repair, augmentation, modelling, evaluation
├── Clips/                         # Raw clip annotations (one folder per recording)
├── flask_data_no_encoder.csv      # Flattened dataset produced by the notebook
├── run.py                         # Flask entry point
├── apps/
│   ├── authentication/routes.py   # Data view, statistics, prediction form and login routes
│   ├── authentication/model_RandomForest.pkl
│   ├── home/                      # Static pages
│   └── templates/                 # Jinja templates (DataFrame/, Prediction/, Statistics/, ...)
├── Dockerfile, docker-compose.yml, nginx/, gunicorn-cfg.py
└── env.sample                     # Configuration template
```

## Running the app

```bash
git clone https://github.com/houcem24/adas-clip-validity-analysis.git
cd adas-clip-validity-analysis
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp env.sample .env          # then set SECRET_KEY (and MAPBOX_TOKEN for the map page)
flask run                   # or: docker-compose up --build
```

Open http://127.0.0.1:5000, register a local account, and use the sidebar to reach the data, statistics and
prediction pages.

## Credits

The web interface is built on the open-source
[Black Dashboard Flask](https://github.com/app-generator/flask-black-dashboard) template by Creative Tim and
AppSeed (MIT, see [LICENSE.md](LICENSE.md) and [CHANGELOG.md](CHANGELOG.md)). The data pipeline, the model, and
the data, statistics and prediction pages are my own work.
