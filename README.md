Kesk v1.0
=========

Kesk is a simple keyboard-only drawing software.

Kesk is for KEyboard SKetch.

Kesk is because you want to draw on your computer but don't have a mouse or a tablet.

Kesk is made with python and pygame.

You're free to do what you want with this thing.

Usage
-----

Kesk need pygame. If you don't have it, you may do :

```
sudo pip3 install pygame
```

Then, download Kesk and run kesk.py with the following command :

```
python3 kesk.py
```

Currently Kesk is only made for azerty keyboards.

- Move the cursor with
    ```
    a  z  e
      ↖↑↗
    q ← → r
      ↙↓↘
    w  x  c
    ```

- Draw with `ENTER`
- Erease with `BACKSPACE`
- Undo with `u`
- Redo with `y`
- Zoom in with `+`
- Zoom out with `-`
- Move on the view with arrow keys
- Reset with `r`
- Save as a png with `s`
- Quit with `ESCAPE`
- Use `SHIFT` to do an action 5 times

Config
------

You can change some settings (like sketch size and colors) in the `config.py` file.
