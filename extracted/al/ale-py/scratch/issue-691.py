from ale_py import ALEInterface, roms, LoggerMode

impossible_roms = {"maze_craze", "joust", "warlords", "combat"}

ale = ALEInterface()
ale.setLoggerMode(LoggerMode.Error)

for rom_name in roms.get_all_rom_ids():
    if rom_name in impossible_roms:
        continue

    ale.loadROM(roms.get_rom_path(rom_name))
    if len(ale.getLegalActionSet()) < 18:
        print(f'{rom_name=} -> {len(ale.getLegalActionSet())} ({ale.getLegalActionSet()})')
