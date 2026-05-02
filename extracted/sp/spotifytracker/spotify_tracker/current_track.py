import subprocess


def apple_script_call(apple_script):
    full_apple_script_call = ['osascript', '-e', apple_script]
    apple_script_return = subprocess.check_output(full_apple_script_call)
    return apple_script_return.decode("utf-8")


def tell_spotify(command):
    return apple_script_call('tell application "Spotify" to {}'.format(command))


def check_if_playing():
    apple_script_string = tell_spotify('return player state as string')
    return apple_script_string.strip() == 'playing'


def get_track_id_from_apple_script_string(apple_script_string):
    return apple_script_string.split(':')[-1].strip()


def get_current_track_id():
    if not check_if_playing():
        return None
    apple_script_string = tell_spotify('return id of current track as string')
    return get_track_id_from_apple_script_string(apple_script_string)


def main():
    track_id = get_current_track_id()
    print('track_id: {}'.format(track_id))


if __name__ == '__main__':
    main()
