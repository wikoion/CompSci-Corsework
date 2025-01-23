import random

N = 8

knight_moves = [
    (2, 1), (1, 2), (-1, 2), (-2, 1),
    (-2, -1), (-1, -2), (1, -2), (2, -1)
]

def is_valid_move(x, y, board):
    return 0 <= x < N and 0 <= y < N and board[x][y] == -1

def get_degree(x, y, board):
    count = 0
    for move in knight_moves:
        nx, ny = x + move[0], y + move[1]
        if is_valid_move(nx, ny, board):
            count += 1
    return count

def warnsdorff(x, y, board, move_count, is_closed):
    if move_count == N * N:
        if is_closed:
            for move in knight_moves:
                nx, ny = x + move[0], y + move[1]
                if nx == 0 and ny == 0:  # Check if it forms a closed tour
                    return True
            return False
        else:
            return True

    next_moves = []
    for move in knight_moves:
        nx, ny = x + move[0], y + move[1]
        if is_valid_move(nx, ny, board):
            next_moves.append((nx, ny, get_degree(nx, ny, board)))

    next_moves.sort(key=lambda m: m[2])

    for nx, ny, _ in next_moves:
        board[nx][ny] = move_count
        if warnsdorff(nx, ny, board, move_count + 1, is_closed):
            return True
        board[nx][ny] = -1

    return False

def las_vegas_knights_tour(start_x, start_y):
    board = [[-1 for _ in range(N)] for _ in range(N)]

    x, y = start_x, start_y
    board[x][y] = 0

    for move_count in range(1, N * N):
        valid_moves = []
        for move in knight_moves:
            nx, ny = x + move[0], y + move[1]
            if is_valid_move(nx, ny, board):
                valid_moves.append((nx, ny))

        if not valid_moves:  # No valid moves available
            return False

        x, y = random.choice(valid_moves)
        board[x][y] = move_count

    return True

def knights_tour(is_closed, start_x, start_y, use_backtracking, max_attempts):
    if use_backtracking:
        for attempt in range(max_attempts):
            board = [[-1 for _ in range(N)] for _ in range(N)]
            board[start_x][start_y] = 0

            if warnsdorff(start_x, start_y, board, 1, is_closed):
                print(f"Solution found on attempt {attempt + 1}:")
                for row in board:
                    print(' '.join(f'{cell:2}' for cell in row))
                return True
        print("No solution found within the given attempts.")
        return False
    else:
        if not las_vegas_knights_tour(start_x, start_y):
            print("Las Vegas approach failed.")
            return False

def calculate_success_rate(is_closed, start_x, start_y, use_backtracking, max_attempts):
    success = 0
    for i in range(0, 10000):
        if knights_tour(is_closed, start_x, start_y, use_backtracking, max_attempts):
            success += 1

    return success / 10000

def main():
    try:
        start_x = int(input("Enter the starting row (0-7): "))
        start_y = int(input("Enter the starting column (0-7): "))
        if not (0 <= start_x < N and 0 <= start_y < N):
            raise ValueError("Starting position out of bounds.")
    except ValueError as e:
        print(f"Invalid input: {e}")
        return

    try:
        max_attempts = int(input("Enter the maximum number of attempts: "))
        if max_attempts <= 0:
            raise ValueError("Number of attempts must be positive.")
    except ValueError as e:
        print(f"Invalid input: {e}")
        return

    choice = input("Do you want a closed knight's tour? (yes/no): ").strip().lower()
    is_closed = choice == "yes"

    algorithm_choice = input("Choose algorithm: backtracking or las_vegas (b/l): ").strip().lower()
    use_backtracking = algorithm_choice == "b"

    knights_tour(is_closed, start_x, start_y, use_backtracking, max_attempts)

    if input("Do you want to calculate success rates for 10,000 trials? (yes/no): ").strip().lower() == "yes":
        print("Calculating success rates...")
        backtracking_closed_rate = calculate_success_rate(True, start_x, start_y, True, max_attempts)
        backtracking_open_rate = calculate_success_rate(False, start_x, start_y, True, max_attempts)
        las_vegas_closed_rate = calculate_success_rate(True, start_x, start_y, False, max_attempts)
        las_vegas_open_rate = calculate_success_rate(False, start_x, start_y, False, max_attempts)
        print(f"Backtracking closed success rate: {backtracking_closed_rate * 100:.2f}%")
        print(f"Backtracking open success rate: {backtracking_open_rate * 100:.2f}%")
        print(f"Las Vegas closed success rate: {las_vegas_closed_rate * 100:.2f}%")
        print(f"Las Vegas open success rate: {las_vegas_open_rate * 100:.2f}%")

if __name__ == "__main__":
    main()
