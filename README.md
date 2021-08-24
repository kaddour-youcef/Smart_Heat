Smart_heater
==============================

this project deals with the use of machine learning techniques for the development of an intelligent temperature control system
the author of this project : Youcef-KADDOUR
made for EXPLEO GROUP

To start the WebApp use the docker image 

OR : 

cd Smart_heat_webapp

 create a virtual environment : 
 
 python3 -m venv smart_heat 
 
install all the dependecis from requirements.txt

to run the app : 

python manage.py runserver 

open local host on the port 8000

if any question on the project e-mail me at : 

kaddouryoucef18@gmail.com

Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── data_senario_11ans       <- Data gathered from 11 years of simulation.
    │   ├── to_use_(with server)        <- data to use on the server.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
	│
	├──docker              <- the docker image of the webapp
	│
    ├── docs               <- some usefull docs
	│
	├── Energy+            <- Energy+ models for building simulation
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Official reports (made by Youcef-KADDOUR).
    │   └── figures        <- Generated graphics and figures to be used in reporting
	│
	├── Smart_heat_webapp            <- The webapp based on django
	│
	├── Smart_heat_landing-page      <- A landing page for the project
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt` (dependecis on the webapp are on the webapp file)
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    


--------

