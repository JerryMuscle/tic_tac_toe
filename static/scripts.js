const boardDiv = document.getElementById("board");
const messageP = document.getElementById("message");
const resetBtn = document.getElementById("resetBtn");

let gameOver = false;

function fetchState() {
  fetch("/state")
    .then(res => res.json())
    .then(data => {
      renderBoard(data.board);
      if (data.winner) {
        messageP.textContent = `${data.winner} の勝ち！`;
        gameOver = true;
      } else if (data.draw) {
        messageP.textContent = "引き分けです。";
        gameOver = true;
      } else {
        messageP.textContent = `現在のターン: ${data.current}`;
        gameOver = false;
      }
    });
}

function renderBoard(board) {
  boardDiv.innerHTML = "";
  board.forEach((row, i) => {
    row.forEach((cell, j) => {
      const div = document.createElement("div");
      div.className = "cell";
      div.textContent = cell === '.' ? '' : cell;
      div.onclick = () => {
        if (!gameOver && cell === '.') {
          sendMove(i, j);
        }
      };
      boardDiv.appendChild(div);
    });
  });
}

function sendMove(row, col) {
  fetch("/move", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ row, col }),
  })
    .then(res => res.json())
    .then(data => {
      renderBoard(data.board);
      if (data.winner) {
        messageP.textContent = `${data.winner} の勝ち！`;
        gameOver = true;
      } else if (data.draw) {
        messageP.textContent = "引き分けです。";
        gameOver = true;
      } else if (data.message) {
        messageP.textContent = data.message;
      } else {
        messageP.textContent = `現在のターン: ${data.current}`;
      }
    });
}

resetBtn.onclick = () => {
  fetch("/reset", { method: "POST" })
    .then(() => fetchState());  // 再描画
  location.reload();
};

// 初期表示
fetchState();