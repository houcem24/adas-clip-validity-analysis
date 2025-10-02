Data Collection, Repair, Visualization & Analysis for Autonomous Vehicles Parts

Repository: houcem24 / Data_Collection_Repair_Visualization_and_Analysis_For_Autonomous_Vehicles_Parts (github.com
)

This repository contains the implementation of a pipeline for data collection, repair, visualization, and analysis of autonomous vehicle parts data. It was developed as part of a Master’s Thesis by Houssem Ouerdiane at ESPRIT University, Tunisia, conducted in collaboration with Magna Electronics (Germany, Sailauf).

The goal of this thesis was to design and implement a system capable of handling raw sensor and radar data from autonomous vehicles, ensuring data quality, enabling efficient preprocessing, and providing insightful analysis through visualization and prediction workflows.

🚀 Features & Capabilities

Data collection & ingestion from vehicle sensors and radar systems

Data repair & preprocessing including cleaning, anomaly detection, and error correction

Visualization dashboards to explore sensor behaviors, anomalies, and patterns

Data analysis & predictive modeling for automotive use cases

Web API integration (Flask) for serving and interacting with results

Containerized deployment with Docker and Nginx

Environment configuration support (.env, sample templates)

📂 Repository Structure
.
├── .dockerignore
├── .env
├── .gitignore
├── CHANGELOG.md
├── Dockerfile
├── LICENSE.md
├── README.md
├── apps/
├── media/
├── nginx/
├── Prediction.ipynb
├── flask_data_no_encoder.csv
├── docker-compose.yml
├── env.sample
├── run.py
├── requirements.txt
├── gulpfile.js
├── gunicorn-cfg.py
└── package.json

📌 Getting Started
Prerequisites

Python 3.x

Docker & Docker Compose (optional, for containerized deployment)

Flask / Gunicorn web server setup

Node.js (for optional frontend build steps)

Installation
git clone https://github.com/houcem24/Data_Collection_Repair_Visualization_and_Analysis_For_Autonomous_Vehicles_Parts.git
cd Data_Collection_Repair_Visualization_and_Analysis_For_Autonomous_Vehicles_Parts
pip install -r requirements.txt

Running the Application
python run.py


Or via Docker:

docker-compose up --build

🧪 Usage & Workflow

Collect raw automotive sensor data

Apply repair & preprocessing steps (cleaning, imputation, anomaly detection)

Transform into structured formats suitable for analysis

Visualize patterns and system performance

Run prediction workflows (Prediction.ipynb) to derive insights

Deploy results via Flask API or dashboards

📈 Results

Ensures higher reliability of autonomous vehicle data pipelines

Enables clear visualizations of trends, anomalies, and repaired data

Provides a scalable, containerized deployment option for integration with enterprise systems



📬 Acknowledgment

This project was completed as a Master’s Thesis by Houssem Ouerdiane at ESPRIT University (Tunisia) in collaboration with Magna Electronics (Germany, Sailauf).
