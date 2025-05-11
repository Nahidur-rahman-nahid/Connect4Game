from ConnectFour import ConnectFour
from ai import get_ai_move, AI_PLAYER, HUMAN_PLAYER


if __name__ == "__main__":
    game = ConnectFour()
    game.print_board()

    while True:
        if game.current_player == HUMAN_PLAYER:
            try:
                col = int(input(f"Player {game.current_player}, choose column (0-6): "))
                if game.drop_token(col):
                    game.print_board()

                    if game.check_win(game.current_player):
                        print(f"🎉 Player {game.current_player} wins!")
                        break

                    if game.is_draw():
                        print("🤝 It's a draw!")
                        break

                    game.switch_player()

            except ValueError:
                print("❌ Please enter a valid number.")
        else:
            print("🧠 AI is thinking...")
            col = get_ai_move(game, depth=4)
            if col is not None:
                game.drop_token(col)
                game.print_board()

                if game.check_win(game.current_player):
                    print(f"🤖 AI ({game.current_player}) wins!")
                    break

                if game.is_draw():
                    print("🤝 It's a draw!")
                    break

                game.switch_player()
