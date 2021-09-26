import discord
from discord.ext import commands
from dotenv import dotenv_values
import datetime
import random


config = dotenv_values(".env"); 
TOKEN = config['TOKEN']

description = '''MovieBot in Python'''
bot = commands.Bot(command_prefix='!', description=description)

MOVIE_FILE = "movies.txt"
WATCHED_FILE = "watched.txt"

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command()
async def hello(ctx):
    """Says world"""
    await ctx.send("world")

@bot.command()
async def list(ctx): 
    """ List movies """
    try: 
        msg = "";
        f = open(MOVIE_FILE, 'r')
        w = open(WATCHED_FILE, 'r'); 
        movies = f.read()
        watched = w.read()
        
        msg += "**Movies**\n" + movies
        msg += "\n"
        msg += "**Watched**\n" + watched
        
        f.close();
        w.close();
        await ctx.send(msg); 
        
    except Exception as e: 
        print(e); 
        await ctx.send('Error getting movie list!'); 
    
    
@bot.command()
async def add(ctx, *args): 
    """ Adds a movie to the list to be watched. """
    try: 
        movie_title = " ".join(args[:]); 
        f = open(MOVIE_FILE, 'a');  
        f.write(movie_title + "\n"); 
        f.close(); 
        await ctx.send("Added " + movie_title); 
    except Exception as e: 
        print(e);
        await ctx.send("Error Adding Movie!"); 
    
@bot.command()
async def watched(ctx, *args): 
    """ Removes movie from the list of movies to watch. """ 
    try: 
        movie_title = " ".join(args[:]); 
        watched_date = datetime.datetime.now(); 
        watched_date = watched_date.strftime("%m/%d/%Y")
        
        #remove from movie file.
        f = open(MOVIE_FILE, 'r'); 
        movies = f.read().splitlines(); 
        f.close();
        if movie_title not in movies: 
            await ctx.send("That's great but I wasn't tracking it...Whatever I guess I'll add it to your watched list."); 
        else: 
            #only need to remove movie if it's in the movies list. 
            new_movies = [m for m in movies if m != movie_title];

            msg = "";
            for m in new_movies: 
                msg += m + "\n";
            f = open(MOVIE_FILE, 'w'); 
            f.write(msg); 
            f.close();
            
        #add to watched movies. 
        w = open(WATCHED_FILE, 'a'); 
        w.write(movie_title + "\t" + watched_date + "\n"); 
        w.close(); 
        
        await ctx.send("Watched " + movie_title); 
    except Exception as e: 
        print(e);
        await ctx.send('Error removing movie!'); 

@bot.command()
async def rollCredits(ctx):
    """ Randomly selects a movie from the list to be watched. """
    try: 
        f = open(MOVIE_FILE, 'r');
        movies = f.read().splitlines(); 
        if(len(movies) > 0): 
            movie = random.choice(movies); 
            await ctx.send(movie); 
        else: 
            await ctx.send("Can't give you a movie when there are none.  Add some movies!")
    except Exception as e: 
        print(e); 
        await ctx.send('Error getting movie! :('); 
    
    
    
bot.run(TOKEN)