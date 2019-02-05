# Yelp Restaurant Recommendation System

This recommendation system uses data from the Yelp Open Dataset, available [here](https://www.yelp.com/dataset)

## 1. The Data

The full dataset includes:
* 6,685,900 reviews for 192,609 businesses by 1,637,138 users

The data used for training the recommendation system filtered this raw data down to only reviews for restaurants, and only reviews by users who gave 10 or more reviews:
* 2,295,089 reviews for 73,100 businesses by 81,416 users

The full dataset is in SQLAlchemy tables -- (yelp.db).

## 2. Exploratory Data Analysis

### a. Distribution of Ratings


### b. Distribution of Reviews per User


### c. Distribution of Reviews per Business


## 3. The Recommendation System

The recommendation system is built on a Singular Value Decomposition model from [**surprise**](https://surprise.readthedocs.io/en/stable/index.html).

* The base model (default hyperparameters) returned error metrics **RMSE = 1.0917 and MAE = 0.8587** with 5-fold validation, and took ~20 minutes to train
*
