# Midi-to-Minecraft
Make your midi file into a datapack that plays the song in minecraft!

Visit this website at (https://aipi22.github.io/Midi-to-Minecraft/)

# How it works

We convert the music notes that are found within the midi file to generate a set of minecraft /playsound commands that play the song in game.

# How to use

Right now, you will need to manually create your own datapack. First create a world, then go into Finder on Mac or File Explorer on Windows and locate the .minecraft folder. Inside of your .minecraft folder, make the following structure:

```
.minecraft
  saves
    "Your world name"
      datapacks
        (make the folder): music
          pack.mcmeta
          data
            minecraft
              tags
                function
                  tick.json
            music
              function
                tick.mcfunction
```

Now paste the following code into pack.mcmeta:

```
{
  "pack": {
    "pack_format": 48,
    "description": "MIDI Music Datapack"
  }
}
```
**Very Important!**

There is a different pack format for every version of minecraft. 48 is for version 1.21.8, but look up your versions number and use that instead.

Next, paste this into tick.json:

```
{
  "values": ["music:tick"]
}
```
This line just simply runs the tick function in the game so that the music progresses without any commands needed in game.

**And finally paste the ouput of the website into your tick.mcfunction file.**

Now you just need to run a few commands in game to start.

First:
```
/scoreboard players set #t music_tick 0
```
This only needs to be run once per world.

Then:
```
/reload
/scoreboard players set #t music_tick 0
```
This will begin playing the song. To hear it, make sure you are at or near 0, 0, 0 in game. You can also set up a command block to run both of these last commands for you for a "start" button.
