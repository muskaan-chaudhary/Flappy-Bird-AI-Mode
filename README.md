# Flappy-Bird-AI-Mode

## About
This AI was trained using __N.E.A.T.__ This is a genetic algorithm that trains the AI by creating generations of agents and simulating them in a environment. Each bird has a Neural Network that will decide to make the bird flap based on its inputs. The birds with the best Neural Networks are selected for the next generation and slightly mutated to create new behavior.

This project was made using __P5js__ to render the game and __TensorFlow__ js to create the Neural Networks.

## Neural Network
Each bird has a Neural network that determines whether to flap or not. This network is a sequential model made up of three dense layers. An input layer with 5 neurons, a hidden layer with 8 neurons and a output layer with 2 neurons.

The five inputs the bird receives are:

The Birds Y position
The Birds velocity
The Birds distance from the pipe
The Y position of the top pipe
The Y position of the bottom pipe
The output layer has a softmax activation and will return two values that will add up to one. The bird will flap if the first value is greater than the second and will not if the opposite is true.


## Whats here
- data (Contains trained model)
- images (Contains game and website images)
- src (Contains code for Flappy Bird AI)
    - main.js (setup and draw loop)
    - Environment.js (render and move environment)
    - Ground.js (render ground)
    - Pipe.js (render and move pipe)
    - Population.js (render and move population of birds)
    - Bird.js (render and make actions using Neural network)
    - Brain.js (create Neural network and make prediction)
    - Neuroevolution.js (evaluate and create next generation)
- index.html (webpage)
- index.js (handles webpage interactions)
