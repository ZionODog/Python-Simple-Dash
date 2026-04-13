import pandas as pd
import logging
from typing import Optional

# Configuração do logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class DataManager:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data: Optional[pd.DataFrame] = None # Atributo protegido

    def load_data(self) -> None:
        try:
            self.data = pd.read_csv(self.file_path)
            logging.info("Dados carregados com sucesso.")

            self._initial_cleanup() # Limpeza inicial dos dados
        except Exception as e:
            logging.error(f"Erro no carregamento dos dados: {e}")
            raise

    def _initial_cleanup(self) -> None: # Função para padronizar os dados logo no inicio
        if self.data is not None:
            if 'year' in self.data.columns:
                self.data['year'] = pd.to_datetime(self.data['year'], format='%Y')
            if 'population' in self.data.columns:
                self.data['population'] = self.data['population'] / 1_000_000
            logging.info("Limpeza inicial concluída.")
        else:
            logging.warning("Nenhum dado para limpar.")

    @property 
    def get_data(self) -> Optional[pd.DataFrame]:
        if self.data is not None:
            return self.data
        else:
            logging.warning("Dados não carregados. Use load_data() para carregar os dados.")
            return None
    
    def filter_data(self, **kwargs) -> pd.DataFrame:
        df = self.data.copy()
        for column, value in kwargs.items():
            if column in df.columns:
                if column == 'year' and isinstance(value, int):
                    df = df[df['year'].dt.year == value]
                else:
                    df = df[df[column] == value]
        return df
    
    def get_stats(self, year: Optional[int] = None) -> dict: # Função para obter estatísticas básicas, com opção de filtro por ano
        df = self.filter_data(year=year) if year else self.data
        if df is not None and not df.empty:
            return {
                'total_population': df['population'].sum(),
                'average_population': df['population'].mean(),
                'max_population': df['population'].max(),
                'min_population': df['population'].min()
            }
        else:
            logging.warning("Dados filtrados estão vazios. Verifique os filtros aplicados.")
            return {}

