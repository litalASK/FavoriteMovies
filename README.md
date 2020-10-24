# FavoriteMovies

## Brief
A project that provides user information about favorite movies, using 
**machine learning** algorithm. The user has to decide about 20 random movies: whether he likes it or not, or does not know. Finally the user gets a list of movies he might like.

## Algorithm
The main algorithm in the project: [ID3](https://en.wikipedia.org/wiki/ID3_algorithm). 


Implementation of the steps:

1. Movies database file readed, and each movie genere is used as attribute vector.
2. 20 random movies are chosen and taged by user to create training set(Like/Not Like/Don't know movie).
3. ID3 model tree is builded from the trainig data.
4. All movies in database are checked with the model to create favorite potential movies for the user.

## Run example
```
python .\movie.py
For each movie please enter L if you like, N if you don't like
 and D if you don't know this movie

"Sex and the City 2 " | L/N/D
l
"Buffalo Soldiers " | L/N/D
d
"The Messenger " | L/N/D
l
...
Time Bandits 
Project X 
The Eye 
Johnson Family Vacation 
How High 
Casino Royale 
Frida 
The Fault in Our Stars 
Prophecy 
Spartacus: War of the Damned 
Paper Towns 
My Baby's Daddy 
Tales from the Crypt: Demon Knight 
Max Keeble's Big Move 
...
```
