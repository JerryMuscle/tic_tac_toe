# app.py
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder="static")
CORS(app)

board = [['.' for _ in range(3)] for _ in range(3)] # 3 × 3のボード作成
current = 'O' # 最初の手番

# 勝利者チェック
def check_winner(bd, player):
    for i in range(3):
        if all(bd[i][j] == player for j in range(3)):
            return True
        if all(bd[j][i] == player for j in range(3)):
            return True
    if all(bd[i][i] == player for i in range(3)):
        return True
    if all(bd[i][2 - i] == player for i in range(3)):
        return True
    return False

# 盤面全埋まりチェック
def is_full(bd):
    return all(cell != '.' for row in bd for cell in row)

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

# 現在の盤面の状態を返す
@app.route("/state")
def get_state():
    return jsonify({"board": board, "current": current})

# 手を打った時の処理
@app.route("/move", methods=["POST"])
def move():
    global current
    data = request.json
    row = data["row"]
    col = data["col"]

    if board[row][col] != '.' or check_winner(board, 'O') or check_winner(board, 'X'):
        return jsonify({"board": board, "current": current, "message": "Invalid move"})

    board[row][col] = current

    if check_winner(board, current):
        return jsonify({"board": board, "winner": current})

    if is_full(board):
        return jsonify({"board": board, "draw": True})

    # 手番の交代
    if current == 'O':
        current = 'X'
    else:
        current = 'O'
    return jsonify({"board": board, "current": current})

@app.route("/reset", methods=["POST"])
def reset():
    global board, current
    board = [['.' for _ in range(3)] for _ in range(3)]
    current = 'O'
    return jsonify({"message": "ゲームをリセットしました。"})

if __name__ == '__main__':
    app.run(debug=True)