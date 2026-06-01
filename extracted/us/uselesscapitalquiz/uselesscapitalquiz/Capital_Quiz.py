def capital_quiz():
    from .hard_mode import hard_mode
    from .moderate_mode import moderate_mode
    from .easy_mode import easy_mode
    from .all_mode import  all
    difficulty = input('Enter what game mode you would like to play; "All Mode", "Easy Mode", "Moderate Mode", or "Hard Mode": ')
    difficulty = difficulty.lower()
    if difficulty == "all mode":
        all()
    elif difficulty == "easy mode":
        easy_mode()
    elif difficulty == "moderate mode":
        moderate_mode()
    elif difficulty == "hard mode":
        hard_mode()
    else:
        print('Please Enter the difficulty you wish to play with the full phrase. For example, "Easy Mode" or "easy mode" will work, but "easy" will not. Make sure the only space in your request is inbetween the two words.')
        exit()