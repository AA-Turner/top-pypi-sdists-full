"""Truncate empty RawActivation table to reclaim disk space."""
import re
import subprocess
import psycopg2


def main():
    result = subprocess.run(
        ["supabase", "db", "dump", "--data-only", "--linked", "--dry-run"],
        capture_output=True, text=True,
    )
    host = re.search(r'PGHOST="([^"]+)"', result.stdout).group(1)
    port = re.search(r'PGPORT="([^"]+)"', result.stdout).group(1)
    user = re.search(r'PGUSER="([^"]+)"', result.stdout).group(1)
    password = re.search(r'PGPASSWORD="([^"]+)"', result.stdout).group(1)

    conn = psycopg2.connect(
        host=host, port=int(port), dbname="postgres",
        user=user, password=password, sslmode="require",
    )
    cur = conn.cursor()
    cur.execute("SET ROLE postgres")

    # Verify table is empty before truncating
    cur.execute('SELECT count(*) FROM public."RawActivation"')
    count = cur.fetchone()[0]
    print(f"RawActivation rows: {count}")

    if count > 0:
        print(f"Table is NOT empty ({count} rows). Aborting.")
        conn.close()
        return

    print("Table is empty. Running TRUNCATE...")
    cur.execute('TRUNCATE TABLE public."RawActivation"')
    conn.commit()
    print("TRUNCATE complete.")

    # Also truncate RawActivation_new if empty
    cur.execute('SELECT count(*) FROM public."RawActivation_new"')
    count_new = cur.fetchone()[0]
    print(f"RawActivation_new rows: {count_new}")
    if count_new == 0:
        cur.execute('TRUNCATE TABLE public."RawActivation_new"')
        conn.commit()
        print("RawActivation_new TRUNCATED too.")

    cur.close()
    conn.close()
    print("Done!")


if __name__ == "__main__":
    main()
