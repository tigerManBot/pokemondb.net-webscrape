Description
-----------
This project is a webscraper for the pokemon website pokemondb.net.  
The user can select one of 17 possible pokedexes and the program then sorts that pokedex by pokemon type into
a dictionary.  
For example, the fire pokemon are all placed together and so on.  
Any pokemon with two types is placed into two lists.  
Then, the user can enter a type they wish to explore and the program opens a new tab for every pokemon
 of that requested type.  


Basic Performance Notes
-----------------------
The initial sorting phase takes about three minutes to get done. Each pokemon link is opened in a new tab and some data
is taken from each, followed by closing the tab.  
There are around 150 pokemon in most pokedexes (a few have much more), 
so this operation obviously happens around 150 times.


Why tho
-------
When I was a kid I used to like to use sites like this to plan my team for my playthroughs.  
I liked to have very balanced teams with only one type for each pokemon on my team.  
I was always kind of frustrated by doing this because any pokemon game's pokedex isn't sorted by type.  
So if I wanted to look at all the fire type pokemon, I would have to manually go through every fire pokemon
 in a pokedex and open that pokemon in a new tab.  
This program does that instantly for me.




