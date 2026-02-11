from pathlib import Path
import pandas as pd
from clean import (
    convertir_fecha,
    convertir_available,
    limpiar_precios,
    eliminar_duplicados,
)


def main():
    csv_path = Path(__file__).resolve().parent / "datos" / "datos" / "calendar.csv"
    if not csv_path.exists():
        print(f"CSV no encontrado en: {csv_path}")
        return
    df = pd.read_csv(csv_path)
    print("Antes:", df.shape)
    df = convertir_fecha(df)
    df = convertir_available(df)
    df = limpiar_precios(df)
    df = eliminar_duplicados(df)
    print("Después:", df.shape)
    out_path = csv_path.with_name("calendar_cleaned.csv")
    df.to_csv(out_path, index=False)
    print(f"CSV limpio guardado en: {out_path}")


if __name__ == "__main__":
    main()
