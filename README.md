# FavoriteMovies

## Brief
Project that provides the user with movies that might interst him using machine learning algorithm. The user is provided with 20 random movies which he need to decide if he likes them or he dont know them. Than the user given with list of movies he might be intersted in.  

## Algorithm
The main algorithm that is used is [ID3](https://en.wikipedia.org/wiki/ID3_algorithm). The steps that are performed are:

1. Movies database file readed and generes of the movies are used as attribute vector.
2. 20 random movies are chosed and given to the user to create training set by labeling them (Like/Dont Like/Unkown movie).
3. ID3 model tree is builded from the trainig data.
4. All the database movies are checked with the model to create potenal movies that the user will like.

## Run example
