from arpakitlib.ar_enumeration_util import Enumeration


class ClientTgBotCommands(Enumeration):
    start = "start"
    about = "about"
    author = "author"
    support = "support"
    healthcheck = "healthcheck"
    cancel = "cancel"


class AdminTgBotCommands(Enumeration):
    arpakitlib_project_template_info = "arpakitlib_project_template_info"
    init_sqlalchemy_db = "init_sqlalchemy_db"
    reinit_sqlalchemy_db = "reinit_sqlalchemy_db"
    drop_sqlalchemy_db = "drop_sqlalchemy_db"
    set_all_tg_bot_commands = "set_all_tg_bot_commands"
    raise_fake_error = "raise_fake_error"
    me = "me"
    log_file = "log_file"
    clear_log_file = "clear_log_file"
    kb_with_old_cd = "kb_with_old_cd"
    kb_with_not_modified = "kb_with_not_modified"
    kb_with_raise_error = "kb_with_raise_error"
    kb_with_remove_message = "kb_with_remove_message"
    current_state = "current_state"
    hello_world = "hello_world"


def __example():
    print("ClientCommandsTgBot:")
    for v in ClientTgBotCommands.values_list():
        print(f"- {v}")
    print()
    print("AdminCommandsTgBot:")
    for v in AdminTgBotCommands.values_list():
        print(f"- {v}")


if __name__ == '__main__':
    __example()
