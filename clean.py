import pandas as pd
import numpy as np


def convertir_fecha(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if "date" in df.columns:
        # Parsear fechas de forma robusta: primero intento estándar, si falla
        parsed = pd.to_datetime(df["date"], errors="coerce")
        # Si demasiadas fechas quedan NaT, reintentar asumiendo dayfirst
        if parsed.isna().sum() / max(1, len(parsed)) > 0.5:
            parsed2 = pd.to_datetime(df["date"], errors="coerce", dayfirst=True)
            if parsed2.notna().sum() > parsed.notna().sum():
                parsed = parsed2
        df["date"] = parsed
    return df


def convertir_available(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if "available" in df.columns:
        s = df["available"].astype(str).str.lower()
        mapping = {"t": True, "f": False, "true": True, "false": False, "yes": True, "no": False, "1": True, "0": False}
        df["available"] = s.map(mapping)
    return df


def limpiar_precios(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    columnas_precio = [c for c in df.columns if "price" in c.lower()]
    for col in columnas_precio:
        df[col] = df[col].astype(str).str.replace("$", "", regex=False).str.replace(",", "", regex=False)
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def eliminar_duplicados(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df.drop_duplicates().reset_index(drop=True)
    return df


if __name__ == "__main__":
    print("Este archivo contiene funciones de limpieza. Importalo desde `main.py`.")

def estandarizar_columnas(df):
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower()
    return df


def convertir_categoricas(df, columnas):
    df = df.copy()
    for col in columnas:
        df[col] = df[col].astype("category")
    return df


def convertir_loan_approved(df):
    df = df.copy()
    df["loan_approved"] = df["loan_approved"].map({1: True, 0: False})
    return df


def validar_rangos(df):
    df = df.copy()
    
    df = df[df["age"] >= 18]
    df = df[df["credit_score"].between(300, 850)]
    df = df[df["annual_income"] > 0]
    df = df[df["loan_amount"] > 0]
    
    return df
