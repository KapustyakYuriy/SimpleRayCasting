# Ray Casting Engine (Pygame)

A simple 2.5D ray casting engine built with **Python** and Pygame.
This project demonstrates the core principles behind classic pseudo-3D rendering techniques used in early games like Wolfenstein 3D.

The engine renders vertical wall slices based on ray–wall intersections and simulates depth using distance scaling and color shading.

---

## 🚀 Features

* Ray casting–based 3D projection
* Configurable field of view (FOV)
* Distance-based wall scaling
* Gamma-based color shading
* Floor gradient rendering
* Player movement (WASD + arrow keys)
* Custom wall heights and colors

---

## 🧠 How It Works

The engine casts rays from the player's position across the screen width:

1. For each vertical column of pixels, a ray is projected at a specific angle.
2. The ray checks intersections with all walls.
3. The nearest visible wall is selected.
4. The wall slice is scaled based on distance.
5. Color shading is applied to simulate lighting depth.
6. The floor is rendered using a vertical gradient.

The result is a simple pseudo-3D scene.

---

## 🎮 Controls

| Key | Action        |
| --- | ------------- |
| `W` | Move forward  |
| `S` | Move backward |
| `A` | Strafe left   |
| `D` | Strafe right  |
| `←` | Turn left     |
| `→` | Turn right    |

---

## 🏗 Project Structure

### `Player`

Stores:

* Position (`x`, `y`)
* Field of view (`fov`)
* Viewing angle
* Render distance
* Movement speed
* Turning speed
* Camera height

### `Wall`

Represents a wall segment:

* Start and end coordinates
* Color
* Height

### `Settings`

Contains:

* Screen size
* Sky & floor colors
* Rendering resolution (`delta`)
* Accuracy for intersection math
* Gamma correction
* Window caption

---

## ⚙️ Installation

1. Install Python 3.9+
2. Install Pygame:

```bash
pip install pygame
```

3. Run the script:

```bash
python main.py
```

---

## 🧩 Customization

You can:

* Modify the `WALLS` list to create new levels
* Change player FOV for different perspectives
* Adjust `delta` for performance vs quality
* Experiment with wall heights and colors
* Change gamma for lighting intensity

---
