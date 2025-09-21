from __future__ import annotations

from typing import Set

import sqlalchemy
from sqlalchemy import CheckConstraint
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.schema import AddConstraint


# --- Вспомогательные функции ---

def _normalize_sql(sql: str) -> str:
    """
    Нормализует текст SQL выражения для сравнения:
    - нижний регистр
    - убирает лишние пробелы и внешние скобки
    - убирает пробелы вокруг операторов
    """
    s = sql.strip().lower()
    # убираем внешние скобки, если они охватывают всё выражение
    while s.startswith("(") and s.endswith(")"):
        # проверим баланс скобок, чтобы не снимать лишнего
        depth = 0
        balanced = True
        for i, ch in enumerate(s):
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth == 0 and i != len(s) - 1:
                    balanced = False
                    break
        if balanced:
            s = s[1:-1].strip()
        else:
            break
    # схлопываем все пробелы
    import re
    s = re.sub(r"\s+", " ", s)
    # уберем пробелы вокруг простых операторов
    s = re.sub(r"\s*([=<>+\-*/%,])\s*", r"\1", s)
    return s


def _render_check_sql(cc: CheckConstraint, engine: Engine) -> str:
    """Компилируем SQL выражение CHECK в текст с подстановкой литералов."""
    compiled = cc.sqltext.compile(
        dialect=engine.dialect,
        compile_kwargs={"literal_binds": True}
    )
    return str(compiled)


# --- Основная функция ---

def ensure_sqlalchemy_check_constraints(*, base_: type[DeclarativeBase], engine: Engine) -> None:
    """
    Синхронизирует CHECK-ограничения, объявленные в моделях Base.metadata,
    с фактическими ограничениями в базе данных.

    Для каждого CheckConstraint в моделях:
      - если уже есть в БД (по имени или по эквивалентному SQL) — пропускаем
      - иначе создаём (ALTER TABLE ... ADD CONSTRAINT ...)

    Параметры:
      Base  : ваш DeclarativeBase (или его подкласс), от которого наследуются все модели
      engine_or_conn: Engine или Connection SQLAlchemy

    Исключения пробрасываются наверх (например, если СУБД не поддерживает добавление CHECK «на лету»).
    """
    # Возьмём соединение и транзакцию (BEGIN), чтобы изменения были атомарными

    with engine.begin() as conn:
        conn_inspector = sqlalchemy.inspect(conn)

        for table in base_.metadata.tables.values():

            # Соберём существующие CHECK-и из БД
            existing = conn_inspector.get_check_constraints(table.name, schema=table.schema)

            # Множества для быстрых проверок
            existing_names: Set[str] = set()
            existing_sql_norms: Set[str] = set()

            for row in existing:
                name = (row.get("name") or "").lower()
                if name:
                    existing_names.add(name)
                sqltext = row.get("sqltext") or row.get("definition") or ""
                if sqltext:
                    existing_sql_norms.add(_normalize_sql(sqltext))

            # Теперь пройдём по CheckConstraint, объявленным в модели
            for constraint in table.constraints:
                if not isinstance(constraint, CheckConstraint):
                    continue

                name = (constraint.name or "").lower()
                # если имя есть и уже существует — готово
                if name and name in existing_names:
                    continue

                # иначе сравним по нормализованному SQL
                try:
                    model_sql = _render_check_sql(constraint, conn)
                    model_sql_norm = _normalize_sql(model_sql)
                except Exception:
                    # если не получилось скомпилировать, попробуем по сырому .sqltext
                    model_sql_norm = _normalize_sql(str(constraint.sqltext))

                if model_sql_norm in existing_sql_norms:
                    continue  # эквивалент уже есть

                # Если сюда дошли — надо создать ограничение
                # Важно: constraint уже «привязан» к таблице (из модели),
                # CreateConstraint сгенерирует корректный ALTER TABLE ... ADD CONSTRAINT ...
                ddl = AddConstraint(constraint)
                conn.execute(ddl)
