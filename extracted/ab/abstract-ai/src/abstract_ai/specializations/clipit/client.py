# cli.py
import argparse,sys,os,subprocess
from abstract_utilities.robust_reader import read_file_as_text

def _run_gui():
    from .gui import main as gui_main
    gui_main()

def _run_flask():
    # Launch Flask in‐process (blocking)
    from .flask_app import create_app
    app = create_app()
    app.run(host='127.0.0.1', port=7820)

def _copy_file(path):
    try:
        text = read_file_as_text(path)
        # Use xclip if PyQt is not available
        import subprocess
        p = subprocess.Popen(['xclip','-selection','clipboard'], stdin=subprocess.PIPE)
        p.communicate(input=text.encode('utf-8'))
        print(f"Copied {path!r} to clipboard.")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

def client_main():
    parser = argparse.ArgumentParser(prog='clipit')
    parser.add_argument('--mode', choices=['gui','flask','copy'], default='copy',
                        help="Choose 'gui' (PyQt), 'flask' (HTTP), or 'copy' (CLI)")
    parser.add_argument('--file', type=str,
                        help="When mode=copy, path to file to copy to clipboard")
    args = parser.parse_args()

    if args.mode == 'gui':
        _run_gui()
    elif args.mode == 'flask':
        _run_flask()
    else:  # copy
        if not args.file:
            print("Error: --file is required when mode=copy", file=sys.stderr)
            sys.exit(1)
        _copy_file(args.file)

