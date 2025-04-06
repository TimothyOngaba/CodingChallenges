import chess
import chess.svg
import cairosvg
from PIL import Image
import io
import matplotlib.pyplot as plt

# Set up a new board
board = chess.Board()

# Apply common opening moves
moves = ["e4", "e5", "Nf3", "Nc3", "d4", "Qh5"]
for move in moves:
    try:
        board.push_san(move)
    except:
        pass  # Skip illegal moves

# Convert board to SVG, then to PNG for display
svg_board = chess.svg.board(board=board, size=400)
png_bytes = cairosvg.svg2png(bytestring=svg_board.encode('utf-8'))
image = Image.open(io.BytesIO(png_bytes))

# Show the image
plt.imshow(image)
plt.axis('off')
plt.title("Key Chess Moves (Based on Feature Importance)")
plt.show()
