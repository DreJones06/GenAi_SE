from flask import Flask, jsonify, request
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

ROWS, COLS = 20, 10

SHAPES = {
    "I": ([[1,1,1,1]], "cyan"),
    "O": ([[1,1],[1,1]], "yellow"),
    "T": ([[0,1,0],[1,1,1]], "purple"),
    "L": ([[1,0],[1,0],[1,1]], "orange"),
    "J": ([[0,1],[0,1],[1,1]], "blue"),
    "S": ([[0,1,1],[1,1,0]], "green"),
    "Z": ([[1,1,0],[0,1,1]], "red"),
}


def initial_state():
    return {
        "grid": [[None]*COLS for _ in range(ROWS)],
        "piece": None,
        "x": 0,
        "y": 0,
        "score": 0,
        "game_over": False
    }

state = initial_state()


def reset_game():
    global state
    state = initial_state()


def new_piece():
    name = random.choice(list(SHAPES.keys()))
    shape, color = SHAPES[name]
    state["piece"] = {"shape": shape, "color": color}
    state["x"] = COLS//2 - len(shape[0])//2
    state["y"] = 0

    if not valid(0, 0):
        state["game_over"] = True


def rotate(shape):
    return [list(row) for row in zip(*shape[::-1])]


def valid(dx, dy, shape=None):
    shape = shape or state["piece"]["shape"]
    for i,row in enumerate(shape):
        for j,val in enumerate(row):
            if val:
                x = state["x"] + j + dx
                y = state["y"] + i + dy
                if x < 0 or x >= COLS or y >= ROWS:
                    return False
                if y >= 0 and state["grid"][y][x]:
                    return False
    return True


def merge():
    for i,row in enumerate(state["piece"]["shape"]):
        for j,val in enumerate(row):
            if val:
                x = state["x"] + j
                y = state["y"] + i
                if y < 0:
                    state["game_over"] = True
                else:
                    state["grid"][y][x] = state["piece"]["color"]


def clear_lines():
    new = [row for row in state["grid"] if any(c is None for c in row)]
    cleared = ROWS - len(new)
    for _ in range(cleared):
        new.insert(0, [None]*COLS)
    state["grid"] = new
    state["score"] += cleared * 100


@app.route("/move", methods=["POST"])
def move():
    if state["game_over"]:
        return jsonify(state)

    action = request.json.get("action")

    if not state["piece"]:
        new_piece()

    if action == "left" and valid(-1,0): state["x"] -= 1
    if action == "right" and valid(1,0): state["x"] += 1
    if action == "down" and valid(0,1): state["y"] += 1

    if action == "rotate":
        rotated = rotate(state["piece"]["shape"])
        if valid(0,0,rotated):
            state["piece"]["shape"] = rotated

    if valid(0,1):
        state["y"] += 1
    else:
        merge()
        clear_lines()
        new_piece()

    return jsonify(state)


@app.route("/restart", methods=["POST"])
def restart():
    reset_game()
    return jsonify(state)


if __name__ == "__main__":
    app.run(debug=True)