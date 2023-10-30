import os
import argparse
from datetime import datetime, timedelta

from hospedin import Hospedin
from conversion import Conversion

data_atual = datetime.now()

FORMATO_PERIODO = "%d/%m/%Y"
FORMATO_MES_REFERENCIA = "%Y-%m"

primeiro_dia_mes_atual = data_atual.replace(day=1)
ultimo_dia_mes_anterior = primeiro_dia_mes_atual - timedelta(days=1)
primeiro_dia_mes_anterior = ultimo_dia_mes_anterior.replace(day=1)

PERIODO = (
    f"{primeiro_dia_mes_anterior.strftime(FORMATO_PERIODO)}",
    f" - {ultimo_dia_mes_anterior.strftime(FORMATO_PERIODO)}"
)
MES_REFERENCIA = f"{primeiro_dia_mes_anterior.strftime(FORMATO_MES_REFERENCIA)}"
DOWNLOAD_FOLDER = os.path.join(os.getcwd(), 'downloads', MES_REFERENCIA)

parser = argparse.ArgumentParser(description='')
parser.add_argument('--download', action='store_true', help='')
parser.add_argument('--convert', action='store_true', help='')
args = parser.parse_args()

if args.download:
    hospedin = Hospedin(
        destination_folder=os.path.join(DOWNLOAD_FOLDER, "bronze"),
        periodo=PERIODO
    )
    hospedin.run()

if args.convert:
    conversion = Conversion(
        source_folder=os.path.join(DOWNLOAD_FOLDER, "bronze"),
        destination_folder=os.path.join(DOWNLOAD_FOLDER),
    )
    conversion.run()
