from plyer import notification
from win10toast import ToastNotifier


def task_bar_toast(title: str, message: str, app_name: str, timeout: int = 2):

    notification.notify(
        title=title, message=message, app_name=app_name, timeout=timeout
    )


def show_toast(titulo: str, mensagem: str, icone: str = None, duracao: int = 10):
    """
    Exibe uma notificação na barra de tarefas do Windows.

    :param titulo: Título da notificação.
    :param mensagem: Mensagem da notificação.
    :param icone: Caminho para o arquivo .ico (ícone). Use None para não exibir ícone.
    :param duracao: Tempo em segundos que a notificação ficará visível.
    """
    toaster = ToastNotifier()

    toaster.show_toast(
        titulo,  # Título da notificação
        mensagem,  # Mensagem da notificação
        icon_path=icone,  # Caminho do ícone (ou None)
        duration=duracao,  # Duração da notificação
        threaded=True,  # Para não travar a execução do script
    )

    # Mantém o programa rodando enquanto a notificação está ativa
    while toaster.notification_active():
        pass
