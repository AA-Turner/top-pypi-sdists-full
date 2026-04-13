from ascii_magic import AsciiArt


def test_to_file():
    my_art = AsciiArt.from_image('lion.jpg')
    character_list = my_art.to_character_list(
        columns=60,
    )

    print(character_list[0][0])

    for line in character_list:
        assert len(line) == 60
        assert all(isinstance(item, dict) for item in line)
        assert all('character' in item for item in line)
        assert all('terminal-color' in item for item in line)
        assert all('terminal-hex-color' in item for item in line)
        assert all('full-hex-color' in item for item in line)
