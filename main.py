import pandas as pd
import matplotlib.pyplot as plt

central = pd.read_excel(
    r"C:\Users\Mingbling\Desktop\Esposa\data\FORMATO DE CONTROL CENTRAL POR INDICADOR DITH.xlsx",
    sheet_name="MATRICULA ",
    skiprows=1,
)

no_central_lima, no_central_la_libertad, no_central_tumbes = pd.read_excel(
    r"C:\Users\Mingbling\Desktop\Esposa\data\REPORTE DE NNA MATRICULADOS  2023- 22024 26.03.24.xlsx",
    sheet_name=["LIMA-ASESORIA", "TRUJ_ASESORIA", "TUMB_ASESORIA"],
).values()


def transform_name_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    columns = df.columns
    new_columns = [str(column).replace("\n", "").strip() for column in columns]
    df = df.rename(columns=dict(zip(columns, new_columns)))
    return df


def create_index(df: pd.DataFrame) -> pd.DataFrame:
    def clean_columns_for_index(df: pd.DataFrame, columns: list):
        df = df.copy()
        for column in columns:
            df[column] = df[column].astype(str).str.strip()
        return df

    df = clean_columns_for_index(
        df,
        [
            "Primer apellido NNA",
            "Segundo apellido NNA",
            "Primer nombre NNA",
            "Otros nombres NNA",
        ],
    )
    df["id"] = (
        (
            df["Primer apellido NNA"].str.slice(0, 3)
            + df["Segundo apellido NNA"].str.slice(0, 3)
            + df["Primer nombre NNA"].str.slice(0, 3)
            + df["Otros nombres NNA"].str.slice(0, 3)
            + df["Región"].str.slice(0, 3)
        )
        .str.lower()
        .str.replace(" ", "x")
    )
    return df


def compare(a, b):
    a = set(a)
    b = set(b)
    return {"only_a": a - b, "only_b": b - a, "both": a & b}


# Central
central = transform_name_columns(central)
central = create_index(central)
central_ids = central["id"].to_list()
central.loc[(central.duplicated(subset=["id"], keep=False), "observación_lizet_1")] = (
    "verificar duplicados o etc"
)
## No Central
no_central_lima = transform_name_columns(no_central_lima)
no_central_lima["Región"] = "LIMA"
no_central_lima = create_index(no_central_lima)
no_central_lima.loc[
    (no_central_lima.duplicated(subset=["id"], keep=False), "observación_lizet_1")
] = "verificar duplicados o etc"
no_central_lima_id = no_central_lima["id"].to_list()

no_central_la_libertad = transform_name_columns(no_central_la_libertad)
no_central_la_libertad["Región"] = "LA LIBERTAD"
no_central_la_libertad = create_index(no_central_la_libertad)
no_central_la_libertad.loc[
    (
        no_central_la_libertad.duplicated(subset=["id"], keep=False),
        "observación_lizet_1",
    )
] = "verificar duplicados o etc"
no_central_la_libertad_id = no_central_la_libertad["id"].to_list()

no_central_tumbes = transform_name_columns(no_central_tumbes)
no_central_tumbes["Región"] = "TUMBES"
no_central_tumbes = create_index(no_central_tumbes)
no_central_tumbes.loc[
    (no_central_tumbes.duplicated(subset=["id"], keep=False), "observación_lizet_1")
] = "verificar duplicados o etc"
no_central_tumbes_id = no_central_tumbes["id"].to_list()

no_central_ids = no_central_lima_id + no_central_la_libertad_id + no_central_tumbes_id


results = compare(central_ids, no_central_ids)

flat_list = [(k, v) for k, values in results.items() for v in values]
df = pd.DataFrame(flat_list, columns=["key", "value"])

## Centra Listo
central.loc[
    central["id"].isin(list(df.loc[(df["key"] == "only_a"), "value"])),
    "observación_lizet_2",
] = "SOLO ESTÁ EN CENTRAL y NO APARECE EN NO CENTRAL"

# list(df.loc[(df["value"].str.endswith("lim")) & (df["key"] == "only_b"), "value"])

no_central_lima.loc[
    no_central_lima["id"].isin(
        list(
            df.loc[(df["value"].str.endswith("lim")) & (df["key"] == "only_b"), "value"]
        )
    ),
    "observación_lizet_2",
] = "SOLO ESTÁ EN NO CENTRAL y NO APARECE EN CENTRAL"

no_central_la_libertad.loc[
    no_central_la_libertad["id"].isin(
        list(
            df.loc[(df["value"].str.endswith("lax")) & (df["key"] == "only_b"), "value"]
        )
    ),
    "observación_lizet_2",
] = "SOLO ESTÁ EN NO CENTRAL y NO APARECE EN CENTRAL"

no_central_tumbes.loc[
    no_central_tumbes["id"].isin(
        list(
            df.loc[(df["value"].str.endswith("tum")) & (df["key"] == "only_b"), "value"]
        )
    ),
    "observación_lizet_2",
] = "SOLO ESTÁ EN NO CENTRAL y NO APARECE EN CENTRAL"


central.to_excel(r"central.xlsx", index=False)

no_central_la_libertad.to_excel(r"no_central_la_libertad.xlsx", index=False)
no_central_lima.to_excel(r"no_central_lima.xlsx", index=False)
no_central_tumbes.to_excel(r"no_central_tumbes.xlsx", index=False)


# def plot_compare_results(results):
#     labels = list(results.keys())
#     sizes = [len(v) for v in results.values()]

#     fig1, ax1 = plt.subplots()
#     ax1.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
#     ax1.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.

#     plt.show()


# plot_compare_results(results)
