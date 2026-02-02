import threading


class LockService:
    def __init__(self) -> None:
        self.locks: dict[int, str] = {}
        self.resource_lock = threading.Lock()

    def try_lock(self, number: int, address: str) -> bool:
        """
        Tenta obter a trava do número passado.

        Retorna True caso consiga, e False, caso contrário.
        """

        with self.resource_lock:
            # Verifica se o number está travado
            if number in self.locks:
                return False
            else:
                self.locks[number] = address
                return True

    def release_lock(self, number: int) -> bool:
        """
        Libera a trava do número passado.
        """

        with self.resource_lock:
            # Verifica se o number está travado
            if number in self.locks:
                del self.locks[number]

    def release_locks(self, address: str) -> bool:
        """
        Libera todas as trava de um dado address.
        """

        with self.resource_lock:
            excluir = []

            for number in self.locks:
                if self.locks[number] == address:
                    excluir.append(number)

            for number in excluir:
                del self.locks[number]
