###################### NegamaxDraught ######################

Description:

    This project is a try at a Negamax implementation for a
    draught game.
    This try proved the following problem:
        - The euristic evaluation is not correct
        - At search depth >2 the processing is very slow

    In order to improve this small test we should:
        - Fix the euristic evaluation for proper calculation
          for both players
        - Implement a Principal Variation version and test its
          performance
        - Implement an AlphaBeta with pruning version and test
          its performance

Instructions:

    Launch the Run.py file and follow the instructions.
    1 is for a 2 human player game
    2 is for a 1 human player, 1 AI player game
    3 is for a 2 AI player game

    The commands to play are: "[position] [direction]"
    Examples: "g3 se", "f6 ne", "e1 sw", "b7 nw", etc
