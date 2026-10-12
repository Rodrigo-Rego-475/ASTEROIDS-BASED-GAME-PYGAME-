# Defensores da Terra (Asteroids-Style Game)

An Asteroids-style arcade game built with **Python** and **Pygame**. Destroy as many asteroids as you can and keep them from reaching the Earth.

Developed in collaboration with a teammate. The in-game text is in Portuguese.

## Gameplay

You control a spaceship defending the Earth. Asteroids fall from the top of the screen. If one hits your ship, you lose a ship life. If one gets past you and reaches the bottom of the screen (the Earth), the Earth loses a life. The game ends when either your ship or the Earth runs out of lives.

- **Ship lives:** start at 5 (max 5)
- **Earth lives:** start at 5 (max 10)
- **Difficulty:** asteroids get faster and appear more often as time passes

## Controls

| Key | Action |
|---|---|
| `W` `A` `S` `D` | Move the ship |
| `Space` | Use a special charge |
| `P` | Pause / resume |
| `R` | Restart (on the game over screen) |

## Scoring

- **+10** for each asteroid destroyed by the blue shield above the ship
- **+5** for each asteroid destroyed by the special power

## Items

| Item | Effect |
|---|---|
| Red heart | Restores 1 ship life |
| Green heart | Restores 1 Earth life |
| Blue circle | Adds 1 special charge (max 10) |

Items disappear after 6 seconds if they are not collected.

## Special power

Press `Space` to spend one charge. It destroys every asteroid in the lower half of the screen.

## Requirements

- Python 3
- [Pygame](https://www.pygame.org/)

```
pip install pygame
```

## How to run

1. Download or clone this repository.
2. Keep all the files in the same folder: the game code, `nave.png`, and the audio files (`.wav` and `.mpeg`).
3. Run:

```
python main.py
```

## Files

- `main.py` - game code
- `nave.png` - spaceship image
- `asteroide.wav`, `coracoes.wav`, `danos.mpeg`, `game_over.mpeg`, `poder_especial.wav`, `power_ups.wav` - sound effects

## Authors

Rodrigo Rego
