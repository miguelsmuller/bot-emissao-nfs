import os
from io import StringIO

import pandas as pd


class Conversion():
    def __init__(self, source_folder, destination_folder):
        self.source_folder = source_folder
        self.destination_folder = destination_folder

    def run(self):
        self._converte_hospedagens()
        self._converte_hospedes()
        self._merge()

    def _converte_hospedagens(self):
        source_path = os.path.join(
            self.source_folder,
            "hospedagens.txt"
        )

        try:
            with open(source_path, 'r', encoding="utf-8") as source_content:
                content = source_content.read()
        except FileNotFoundError:
            print(f'O arquivo {source_path} não foi encontrado.')
        except Exception as e:
            print(f"Ocorreu um erro ao ler o arquivo: {str(e)}")

        buffer = StringIO(content)
        html_table = pd.read_html(buffer)

        destination_path = os.path.join(
            self.destination_folder,
            "silver"
        )
        os.makedirs(destination_path, exist_ok=True)

        destination_path = os.path.join(
            destination_path,
            "hospedagens.csv"
        )

        df = html_table[0]
        df.rename(columns={'Hóspede': 'Nome completo'}, inplace=True)
        df.to_csv(destination_path, index=False)

    def _converte_hospedes(self):
        source_path = os.path.join(
            self.source_folder,
            "hospedes.xlsx"
        )

        df = pd.read_excel(source_path, sheet_name="Hóspede", dtype={'CPF': str})

        destination_path = os.path.join(
            self.destination_folder,
            "silver"
        )
        os.makedirs(destination_path, exist_ok=True)

        destination_path = os.path.join(
            destination_path,
            "hospedes.csv"
        )

        df.to_csv(destination_path, index=False)

    def _merge(self):
        cols_to_exclude = [
            "Ativo?",
            "Sexo",
            "RG",
            "Passaporte",
            "Empresa",
            "Profissão",
            "Fone",
            "Fone extra",
            "Endereço",
            "Bairro",
            "CEP",
            "Cidade",
            "Estado",
            "País",
            "Criado em",
            "Atualizado em",
            "Alterado por"
        ]

        dtypes = {
            'CPF': str,
            'Recebido': 'float64',
            'Descontos': 'float64',
            'Total': 'float64'
        }

        silver_hospedes_path = os.path.join(
            self.destination_folder,
            "silver",
            "hospedes.csv"
        )

        silver_hospedagem_path = os.path.join(
            self.destination_folder,
            "silver",
            "hospedagens.csv"
        )

        hopedes = pd.read_csv(silver_hospedes_path, dtype=dtypes)
        hopededagens = pd.read_csv(silver_hospedagem_path)

        hopedes = hopedes.drop(columns=cols_to_exclude)
        
        resultado = pd.merge(hopedes, hopededagens, on='Nome completo', how='inner')

        resultado['Check-in'] = pd.to_datetime(resultado['Check-in'], dayfirst=True)
        resultado['Check-out'] = pd.to_datetime(resultado['Check-out'], dayfirst=True)

        resultado = resultado.sort_values(by='Check-in')

        hospedagem_path = os.path.join(
            self.destination_folder,
            "gold",
        )
        os.makedirs(hospedagem_path, exist_ok=True)

        hospedagem_path = os.path.join(
            self.destination_folder,
            "gold",
            "hospedagens.csv"
        )

        resultado.to_csv(hospedagem_path, index=False)
