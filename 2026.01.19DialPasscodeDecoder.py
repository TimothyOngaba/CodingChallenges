'''Creating a Dial Passcode Decoder with CheatCode functionality.'''
# Dial passcode decoder with CheatCode
while True:
    start_position = 50
    current_position = start_position
    passcode = ""
    cheat_code = 0

    dial_moves = input("Enter the dial moves separated by commas: ")
    moves = [move.strip().upper() for move in dial_moves.split(",") if move.strip()]

    for move in moves:
        direction = move[0]
        steps = int(move[1:])

        if direction == "R":
            current_position = (current_position + steps) % 100
        elif direction == "L":
            current_position = (current_position - steps) % 100
        else:
            raise ValueError(f"Invalid movement: {move}")

        if current_position == start_position:
            cheat_code += 1

        passcode += str(current_position).zfill(2)

    print("The decoded passcode is:", passcode)
    print("The cheat code is:", cheat_code)

    restart = input("Would you like to enter another set of movements? (y/n): ").strip().lower()
    if restart != "y":
        print("Exiting decoder.")
        break