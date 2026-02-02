from abstract_clicks import *
def move_window_with_mouse(pid=None, title=None, monitor_index=1, *args, **kwargs):
       
        monitors = get_monitors()
        if not monitors or monitor_index < 1 or monitor_index > len(monitors):
            print(f"Invalid monitor index: {monitor_index}. Available monitors: {len(monitors)}")
            return False

        target_monitor = monitors[monitor_index - 1]
        input(target_monitor)
        x, y = target_monitor['width'] + 50, target_monitor['height'] + 50
        print(f"Moving window to monitor {monitor_index}: x={x}, y={y}")
        input(platform.system())
        if platform.system() == 'Linux' and (pid or title):
            if pid:
                result = subprocess.run(['xdotool', 'search', '--pid', str(pid)], capture_output=True, text=True)
            elif title:
                result = subprocess.run(['xdotool', 'search', '--name', title], capture_output=True, text=True)
            else:
                print("PID or title required for Linux")
                return False

            window_ids = result.stdout.strip().split()
            if not window_ids:
                print(f"No window found for PID: {pid} or title: {title}")
                return False

            window_id = window_ids[0]
            subprocess.run(['xdotool', 'windowactivate', window_id])
            time.sleep(0.5)

            # Get window geometry
            result = subprocess.run(['xdotool', 'getwindowgeometry', window_id], capture_output=True, text=True)
            output = result.stdout
            position_line = [line for line in output.split('\n') if 'Position' in line]
            if not position_line:
                print(f"No position information for window {window_id}")
                return False

            position_str = position_line[0].split(': ')[1].split(' ')[0]
            try:
                win_x, win_y = map(int, position_str.split(','))
            except ValueError as e:
                print(f"Error parsing position '{position_str}': {e}")
                return False

            pyautogui.moveTo(win_x + 50, win_y + 20)
            pyautogui.mouseDown(button='left')
            time.sleep(0.2)
            pyautogui.moveTo(x, y, duration=1)
            pyautogui.mouseUp(button='left')
            print(f"Dragged window {window_id} to monitor {monitor_index} at x={x}, y={y}")
            return True
        else:
            print(f"Unsupported platform: {platform.system()} or missing PID/title")
            return False
print(is_window_open())
window_mgr = get_window_mgr()
move_window_with_mouse()
##window_mgr.open_browser_tab()
##screenshot_mgr = screenshotManager()
##screenshot_mgr.get_target_items('Tree')
##record_mgr = EventsRecorder()
##record_path = record_mgr.start_recording()
##record_mgr.replay()
##data = safe_load_from_file(record_path)
##input(data)
