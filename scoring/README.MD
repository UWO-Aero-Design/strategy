# Mission Score Calculator

A Streamlit app for calculating SAE Aero Design competition mission scores.

## Setup

1. Clone the repository
2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install requirements:
   ```
   pip install -r requirements.txt
   ```

## Run

```
streamlit run mission_score_calculator.py
```

## Usage

1. Set aircraft and payload weights
2. Select mission segments and modes
3. Choose mission time
4. View calculated score and breakdown

## Requirements

- streamlit
- pandas
- matplotlib