#!/usr/bin/env python3
"""
verify_profile_table.py -- calculo manual, columna por columna, de la
tabla "Average Nobs Profiles per 6 Hours", replicando EXACTAMENTE la
logica de _draw_profile_summary_table() en obstimedb_plot.py, para
verificar contra tu .db real sin adivinar fechas a mano.

Uso:
    python3 verify_profile_table.py <ruta.db> <family> <id_stn>

Ejemplo:
    python3 verify_profile_table.py experience_..._ai.db ai BUFR
"""
import sys
import sqlite3
import pandas as pd


def main():
    if len(sys.argv) != 4:
        print("Uso: python3 verify_profile_table.py <ruta.db> <family> <id_stn>")
        sys.exit(1)

    db_path, family, id_stn = sys.argv[1], sys.argv[2], sys.argv[3]

    conn = sqlite3.connect(db_path)

    # run_time = la fecha MAS RECIENTE en TODA la tabla (no solo de esta
    # familia/estacion) -- asi lo calcula obstimedb_plot.py.
    run_time_raw = conn.execute(
        "SELECT MAX(date) FROM moyenne WHERE channel IS NULL").fetchone()[0]
    run_time = pd.to_datetime(str(run_time_raw), format='%Y%m%d%H')
    run_hour = run_time.hour
    print(f"run_time = {run_time_raw}  ({run_time})")
    print(f"PASS (hora) = {run_hour:02d}Z\n")

    # Los mismos limites exactos que _draw_profile_summary_table():
    today_start      = run_time - pd.Timedelta(hours=24)
    yesterday_end     = run_time - pd.Timedelta(hours=48)
    yesterday_start    = run_time - pd.Timedelta(hours=72)
    week_start          = run_time - pd.Timedelta(days=7)
    lastweek_end          = run_time - pd.Timedelta(days=8)
    lastweek_start          = run_time - pd.Timedelta(days=15)
    tenday_start              = run_time - pd.Timedelta(days=10)

    def fmt(d):
        return d.strftime('%Y%m%d%H')

    def period_sum(start, end, same_hour=False):
        q = """SELECT date, Nobsprofile FROM moyenne
               WHERE channel IS NULL AND id_stn = ?
               AND date > ? AND date <= ?"""
        rows = conn.execute(q, (id_stn, int(fmt(start)), int(fmt(end)))).fetchall()
        if same_hour:
            rows = [r for r in rows if int(str(r[0])[-2:]) == run_hour]
        total = sum(r[1] for r in rows)
        return total, rows

    print(f"=== {family} / {id_stn} ===\n")

# Sustituimos el parámetro "agg" por el "divisor_fijo" (número de ficheros esperados)
    for label, start, end, same_hour, divisor_fijo in [
        ("Today",                  today_start,      run_time,      False, 4),  # 1 día = 4 ficheros
        ("Yesterday",              yesterday_start,  yesterday_end, False, 4),  # 1 día = 4 ficheros
        ("This week",              week_start,       run_time,      False, 28), # 7 días = 4 * 7 = 28 ficheros
        ("Last week",              lastweek_start,   lastweek_end,  False, 28), # 7 días = 4 * 7 = 28 ficheros
        ("Last 10 days same PASS", tenday_start,     run_time,      True,  10), # 10 días, misma hora = 10 ficheros
    ]:
        total, rows = period_sum(start, end, same_hour)
        n_rows = len(rows)
        n_dates = len(set(r[0] for r in rows))
        
        # Dividimos SIEMPRE la suma total por el número de ficheros teóricos
        value = total / divisor_fijo
        
        dup_flag = "  <-- OJO: mas filas que fechas, hay DUPLICADOS" if n_rows > n_dates else ""
        print(f"{label:<24} rango: date > {fmt(start)} and date <= {fmt(end)}"
              f"{' (misma hora)' if same_hour else ''}")
        
        # Actualizamos el print para mostrar claramente la división
        print(f"{'':24} {n_rows} filas reales (esperados {divisor_fijo}), {n_dates} fechas distintas -> "
              f"Valor = {value:,.1f}{dup_flag}")
        print()
    at_run = conn.execute(
        "SELECT Nobsprofile FROM moyenne WHERE channel IS NULL AND id_stn = ? AND date = ?",
        (id_stn, run_time_raw)).fetchall()
    print(f"{'Run time':<24} date = {run_time_raw}")
    print(f"{'':24} {len(at_run)} fila(s) -> valor = {[r[0] for r in at_run]}"
          f"{'  <-- OJO: deberia ser 1 sola fila' if len(at_run) != 1 else ''}\n")

    print("--- Filas por fecha, TODA la historia de esta familia/estacion ---")
    print("--- (busca cualquier n_filas > 1 -- ahi esta un duplicado) ---")
    rows = conn.execute(
        "SELECT date, COUNT(*) as n, SUM(Nobsprofile) as suma FROM moyenne "
        "WHERE channel IS NULL AND id_stn = ? GROUP BY date ORDER BY date",
        (id_stn,)).fetchall()
    for date, n, suma in rows:
        flag = "  <-- DUPLICADO" if n > 1 else ""
        print(f"  date={date}  n_filas={n}  suma={suma}/{n}{flag}")

    conn.close()


if __name__ == "__main__":
    main()
