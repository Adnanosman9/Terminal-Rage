## Terminal-Rage

A terminal-based game built with Python where you need to go through a dungeon, dodge traps and defeat a demon using a sword on every floor. 

<img width="356" height="240" alt="1026" src="https://github.com/user-attachments/assets/2696dd69-3a5c-4906-911e-86bb2b70a0ea" />

## How to run it!!
* Download the source file or the application from [release](https://github.com/Adnanosman9/Terminal-Rage/releases/tag/V1)
* Run the source file or the application

> ### To run the source file you need to install these libraries
```bash
   pip install blessed yaspin emoji
```
Setup done. 


## How to play:

### Controls:
* W to move up
* A to move left
* S to move down
* D to move right
* Q to quit

### Characters:
* 🤠 - It's you
* 🗡️ - Dagger to kill the demon (U need it)
* 👹 - kill it
* 💥 - Trap

> ### That's it

## Debugging
There was an issue in my programme. It required pressing Enter for every move, which was kinda irritating and making it harder. So, to make it move without pressing `enter` every time, we used `msvcrt` library. 
This library and debugging were possible with help from Gemini. 

## Warning

`msvcrt` only works on Windows. On MAC it may throw an error. 
