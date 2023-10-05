# RECOMMENDER_SYSTEM

# Introduction

Building a content-based recommendation system by calculating the item-item interaction from the given data. Inputting the valid NETFLIX name of the Movie or the TV Show will lead to the model making the description of the content-based recommendations.<br>

# Description

The model used for recommendation is a combination of the Tfidf Vectorizer for text-to-vector conversion and then the unsupervised algorithm of Nearest Neighbors was used to find the cosine distance between the vectors corresponding to the movies/TV shows.<br> The recommendations will be based on the minimum cosine distance i.e., maximum cosine similarity between the two movies, a movie, and a TV show or TV show and a TV show.<br>

# Dataset

We used 3 different datasets and then merged them to form the final dataset. All of them are available on Kaggle.<br>
Netflix Movies and Shows: https://www.kaggle.com/shivamb/netflix-shows <br>
IMDB Movies and Shows: https://www.kaggle.com/stefanoleone992/imdb-extensive-dataset <br>
IMDB Ratings: https://www.kaggle.com/stefanoleone992/imdb-extensive-dataset <be>  

They are given in datasets folder. Use accordingly in the notebook.


Advised to fetch it and not download it separately. More on it ahead. Kaggle Account required for fetching the dataset. <br>

# Requirements

General:<br>

Python>=3.6<br>

For Model Package:<br>

numpy>=1.19.0,<1.21.0<br>
pandas>=1.2.0,<1.3.0<br>
pydantic>=1.8.1,<1.9.0<br>
scikit-learn>=0.24.0,<0.25.0<br>
strictyaml>=1.3.2,<1.4.0<br>
ruamel.yaml==0.16.12<br>
feature-engine>=1.0.2,<1.1.0<br>
joblib>=1.0.1,<1.1.0<br>
kaggle==1.5.2<br>
bash<br>

For API:

uvicorn>=0.11.3,<0.12.0<br>
fastapi>=0.64.0,<1.0.0<br>
python-multipart>=0.0.5,<0.1.0<br>
typing_extensions>=3.7.4,<3.8.0<br>
loguru>=0.5.3,<0.6.0<br>
python-json-logger>=0.1.11,<0.2.0<br>
jinja2==3.0.2<br>
python-multipart==0.0.5<br>

For Testing and Tooling of the Project:<br>

pytest>=6.2.3,<6.3.0<br>
requests>=2.23.0,<2.24.0<br>
black==20.8b1<br>
flake8>=3.9.0,<3.10.0<br>
mypy==0.812<br>
isort==5.8.0<br>

# Setup (Go to the suitable command prompt)

1] Clone the repository on the local system. Here the commands to be adjusted according to the path of the folder. Here the project is on my Desktop (Microsoft C-Drive). <br>

2] For training the model and generating the cosine distances and similarities between content.<br>

cd C:\Users\kshir\OneDrive\Desktop\RECOMMENDER_SYSTEM\ds_project<br>
tox -e fetch_data (fetching the data)<br>
tox -e train_test_package<br>

3] For installing the package locally.<br>

tox -e train_test_package<br>
(use this to ensure that you have a trained model)<br>
cd C:\Users\kshir\OneDrive\Desktop\RECOMMENDER_SYSTEM\ds_project\package<br>
python setup.py sdist bdist_wheel<br>
pip install -e .<br>

**If memory error problem is faced directly use the ind_csv.csv present in the datasets of recommender model package.**<br>

4] For running the Api.<br>

cd C:\Users\kshir\OneDrive\Desktop\RECOMMENDER_SYSTEM\ds_project<br>
tox -e test_api<br>
tox -e run<br>

5] Once the application starts running go to http://localhost:8001/recommendersystem

**More on this repository in this file:** https://drive.google.com/file/d/1nOQCYNwy4yLqpzeLjWL2xubG8qeLKW5z/view?usp=sharing<br>

**Indepth Analysis and explanation of this repository in this file:** https://drive.google.com/file/d/16b4EvfuRbhXnFMoTNd6cmHsJsOpd2kSa/view?usp=sharing<br>

**The files in the above mentioned two links are available in documents of this repository**<br>

# Contributors

VEDANG KSHIRSAGAR (vedang-04)<br>
