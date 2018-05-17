# Beat the Crowd
## Analysis/Modeling Workflow:
1. `get_clean_data.ipynb`
* fetch ridership data from BART
* scrape weather data from Weather Underground
* clean data
* build database and insert data
2. `explore.ipynb`
* exploratory graphics
3. `model.ipynb`
* build, assess, and refine predictive models
* linear regression, random forest

## Web App Pipeline
* `run.py`
* `flask_app`
  * connects random forest model to front-end UI using the Flask/Bootstrap framework
