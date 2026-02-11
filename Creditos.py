from pathlib import Path
import pandas as pd

def main():
    csv_path = Path(__file__).resolve().parent / "datos" / "datos" / "loanapproval.csv"

    if not csv_path.exists():
        print(f"CSV no encontrado en: {csv_path}")
        return

    df = pd.read_csv(csv_path)

    print("\n--- PRIMERAS FILAS ---")
    print(df.head())

    print("\n--- INFORMACIÓN ---")
    print(df.info())

    print("\n--- NULOS POR COLUMNA ---")
    print(df.isnull().sum())

    print("\n--- TIPOS DE DATOS ---")
    print(df.dtypes)

    print("\n--- ESTADÍSTICAS NUMÉRICAS ---")
    print(df.describe())

if __name__ == "__main__":
    main()

from clean import (
    estandarizar_columnas,
    convertir_categoricas,
    convertir_loan_approved,
    validar_rangos,
    eliminar_duplicados,
)


def load_csv():
    base = Path(__file__).resolve().parent
    raw_path = base / "data" / "raw" / "loanapproval.csv"
    legacy_path = base / "datos" / "datos" / "loanapproval.csv"

    if raw_path.exists():
        csv_path = raw_path
    elif legacy_path.exists():
        csv_path = legacy_path
    else:
        print(f"CSV no encontrado en ninguno de: {raw_path} , {legacy_path}")
        return None, None

    df = pd.read_csv(csv_path)
    return df, csv_path


def main():
    df, csv_path = load_csv()
    if df is None:
        return 1

    print("\n--- PRIMERAS FILAS ---")
    print(df.head())

    print("\n--- INFORMACIÓN ---")
    print(df.info())

    print("\n--- NULOS POR COLUMNA ---")
    print(df.isnull().sum())

    print("\n--- TIPOS DE DATOS ---")
    print(df.dtypes)

    print("\n--- ESTADÍSTICAS NUMÉRICAS ---")
    print(df.describe())

    # --- Limpieza ---
    df = estandarizar_columnas(df)

    # Convertir categóricas solo si existen
    cat_cols = [c for c in ["gender", "marital_status", "employment_status"] if c in df.columns]
    if cat_cols:
        df = convertir_categoricas(df, cat_cols)

    if "loan_approved" in df.columns:
        df = convertir_loan_approved(df)

    range_cols = {"age", "credit_score", "annual_income", "loan_amount"}
    if range_cols.issubset(set(df.columns)):
        df = validar_rangos(df)

    df = eliminar_duplicados(df)

    print("\n--- DESPUÉS DE LIMPIEZA ---")
    print(df.info())

    base = Path(__file__).resolve().parent
    out_dir = base / "data" / "cleaned"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / (csv_path.stem + "_cleaned" + csv_path.suffix)
    df.to_csv(out_path, index=False)
    print(f"\nCSV limpio guardado en: {out_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
