# B351FinalProject
AI project to use a Neural Network to do something...

Ben Boskin

James Audretsch

Dilo Zhi



# Important Links:

Explanation of genetic programming in python: http://lethain.com/genetic-algorithms-cool-name-damn-simple/

Evaluation a poker hand: https://github.com/worldveil/deuces

Poker Hand Game: https://pypi.python.org/pypi/PokerCards 

To run with docker: 

>docker build --tag poker .

>docker run -it -v $(pwd):/code --name pokerplayer poker /bin/bash

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
