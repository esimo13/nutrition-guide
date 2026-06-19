# Sofia Thesis: Maternal Nutrition Recommendation Pipeline

This project builds a full pipeline for maternal nutrition guidance:
- Data preparation from CSVs
- Baseline ML models for calorie and iron-tier prediction
- Seasonal food recommendation
- LLM-generated Bangla response
- FastAPI backend and Next.js frontend

## Repository structure
- Backend API: app.py
- Core pipeline script: main_pipeline.py
- Data preparation: generate_datasets.py, preprocess_data.py
- Food matching: recommend_food.py
- Training: train_models.py
- Datasets: users.csv, nutrition_targets.csv, regional_deficiencies.csv, seasonal_foods.csv, cleaned_features.csv
- Frontend (Next.js): frontend/

## Prerequisites
- Python 3.10+
- Node.js 20+
- A valid OpenAI API key

## 1) Backend setup (FastAPI)
1. Create and activate a Python virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a .env file:
   ```bash
   copy .env.example .env
   ```
   Then set:
   ```
   OPENAI_API_KEY=your_key_here
   ```
4. Start the API:
   ```bash
   python app.py
   ```
5. The API will run at:
   http://127.0.0.1:8000

## 2) Frontend setup (Next.js)
1. Go to the frontend folder:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```
4. Open:
   http://localhost:3000

## 3) Datasets and preprocessing
The API loads data at startup. These CSVs must be present in the project root:
- users.csv
- nutrition_targets.csv
- regional_deficiencies.csv
- seasonal_foods.csv
- cleaned_features.csv

If you want to regenerate the cleaned dataset from the raw CSVs:
```bash
python preprocess_data.py
```

If you want to regenerate the raw datasets (for demo data):
```bash
python generate_datasets.py
python preprocess_data.py
```

## 4) API usage
Endpoint:
- POST /api/recommend

Example payload:
```json
{
  "age": 24,
  "district": "Dhaka",
  "trimester": 2,
  "bmi": 21.5,
  "blood_pressure": "Normal",
  "history_diabetes": 0,
  "history_anemia": 1,
  "current_season": "Monsoon"
}
```

## 5) Notes
- The LLM response uses the OpenAI API. Make sure OPENAI_API_KEY is set.
- The recommendation logic is seasonal and can be extended with more rules.

## 6) Common issues
- If /api/recommend returns "OPENAI_API_KEY is not set", verify your .env file.
- If you change datasets, restart the API to reload them.
