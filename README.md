# FoodLens - AI Nutrition Analyzer

An AI-powered application that analyzes food images to estimate nutritional content, with tiered functionality for personal and corporate users.

## Features

- Image-based food detection
- Calorie and nutrition estimation
- User authentication system
- Tiered analysis (Personal/Corporate)

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/FoodLens.git
   cd FoodLens

2. Install dependencies:
    ```bash
   pip install -r requirements.txt


3. Create user database: make a users_db.json
4. Get API keys:
    - USDA API: Get Key
    - Add to calorie_detector.py

5. Run the application:
    ```bash
   python project_main.py

## Usage

- Sign up or log in
- Select your subscription tier
- Provide path to food image when prompted
- View nutritional analysis


## File Structure

FoodLens/

├── authentication.py      -> User auth system

├── calorie_detector.py   -> Nutrition analysis

├── foodItem.py           -> Food item class

├── image.py              -> Image processing

├── model_factory.py      -> Detection models

├── project_main.py       -> Main application

├── users_db.json         -> User database (create this)

└── README.md
    


