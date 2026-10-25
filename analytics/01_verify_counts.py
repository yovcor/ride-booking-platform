import glob
import pandas as pd

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 50)

for path in sorted(glob.glob("data/raw/*.csv")):
    df = pd.read_csv(path)
    print("\n" + "=" * 70)
    print(path)
    print("rows, cols:", df.shape)
    print("columns:", df.columns.tolist())

    cols = {c.lower().replace("_", " "): c for c in df.columns}
    id_col = next((c for k, c in cols.items() if "booking id" in k), None)
    status_col = next((c for k, c in cols.items() if "booking status" in k), None)
    date_col = next((c for k, c in cols.items() if k == "date"), None)

    if status_col:
        print(f"\n{status_col} counts:")
        print(df[status_col].value_counts(dropna=False))
    if id_col:
        print(f"\nrepeated {id_col} after first:", df[id_col].duplicated().sum())
    if date_col:
        d = pd.to_datetime(df[date_col], errors="coerce")
        print(f"\n{date_col} range:", d.min(), "to", d.max(), "| unparseable:", d.isna().sum())
    for c in df.columns:
        if "incomplete" in c.lower():
            print(f"\n{c} counts:")
            print(df[c].value_counts(dropna=False))