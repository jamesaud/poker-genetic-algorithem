# Genetic Poker Algorithem with Heuristics
AI project to use a Genetic Algorithems to Play Poker (terrible idea to do, in the end, but fun to explore genetic algorithems)

Please run Evaluator.py to see the pretty results on a graph!


Ben Boskin

James Audretsch

Dian Zhi


# Important Links:

Explanation of genetic programming in python: http://lethain.com/genetic-algorithms-cool-name-damn-simple/

Evaluation a poker hand: https://github.com/worldveil/deuces

Poker Hand Game: https://pypi.python.org/pypi/PokerCards 


#Docker

To run with docker: 

>docker build --tag poker .

The command above builds the docker image.

>docker run -it -v $(pwd):/code --name pokerplayer poker /bin/bash

The command above will put you inside a vm, and will mount your current directory into it. Now you can edit files on your local machine while you run commands in docker.

To enter your docker vm, type:
>docker exec -it pokerplayer /bin/bash

To exit your docker vm, type:
>exit


If you get an error when running docker, try this to fix it:

```
docker-machine start default
```

and 

```
eval "$(docker-machine env default)"
```
