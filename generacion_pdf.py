from jinja2 import Environment, FileSystemLoader
import locale
import pandas as pd
from tqdm import tqdm
from weasyprint import HTML

locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")

base = pd.read_excel("BASE CARTAS REVISADA AL 11 SEP 2025.xlsx", sheet_name=1)
base["Fecha Liquid"] = base["Fecha Liquid"].dt.strftime("%d-%m-%Y")
base["Pago"] = base["Pago"].apply(lambda x: "${:,.0f}".format(x).replace(",", "."))
base["PRESTACIÓN"] = base["PRESTACIÓN"].str.capitalize()
base["MODALIDAD REEMBOLSO"] = base["MODALIDAD REEMBOLSO"].str.capitalize()

data = []
for rut in tqdm(base["Rut Asegurado"].drop_duplicates(), desc="Generando Data"):
    sub_base = base[base["Rut Asegurado"] == rut]
    fullname = sub_base["Nombre Asegurado"].iloc[0]
    documents = (
        sub_base[
            [
                "Historial Nro. Docto",
                "ESTADO HISTORIA",
                "Pago",
                "Fecha Liquid",
                "PRESTACIÓN",
                "MODALIDAD REEMBOLSO",
            ]
        ]
        .rename(
            columns={
                "Historial Nro. Docto": "number",
                "Fecha Liquid": "date",
                "ESTADO HISTORIA": "status",
                "Pago": "payment",
                "PRESTACIÓN": "service",
                "MODALIDAD REEMBOLSO": "reimbursement_mode",
            }
        )
        .to_dict(orient="records")
    )

    data.append(
        {
            "rut": rut,
            "fullname": fullname,
            "documents": documents,
        }
    )

env = Environment(loader=FileSystemLoader("."))
current_date = pd.Timestamp.now().strftime("%d de %B de %Y")
for insured in tqdm(data, desc="Generando PDFs"):
    template = env.get_template("template.html")
    output = template.render(
        fullname=insured["fullname"],
        documents=insured["documents"],
        current_date=current_date,
    )
    HTML(string=output, base_url=".").write_pdf(
        f"./cartas-no-enviadas/{insured['rut']}_carta.pdf"
    )
