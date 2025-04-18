import pandas as pd
import numpy as np
from scipy import stats
from typing import Dict, Tuple, List


def load_country_data(country: str, check_year: int, indicator_code: str = None) -> pd.DataFrame:
    """
    Загружает данные для указанной страны из Excel файла.
    
    Args:
        country: Название страны
        check_year: Год для проверки данных
        indicator_code: Код индикатора (если None, возвращает все данные для страны)
        
    Returns:
        DataFrame с данными
    """
    df = pd.read_excel("dataset.xls", sheet_name='Data')
    df = df[df["Country Name"] == country]
    
    if indicator_code:
        df = df[df["Indicator Code"] == indicator_code]
    
    return df


def get_country_indicator_data(df: pd.DataFrame, indicator_code: str, check_year: int) -> np.ndarray:
    """
    Извлекает данные определенного индикатора для страны.
    
    Args:
        df: DataFrame с данными страны
        indicator_code: Код индикатора
        check_year: Год для проверки данных
        
    Returns:
        Массив значений индикатора
    """
    temp_df = df[df["Indicator Code"] == indicator_code].copy()
    temp_df = temp_df.drop(["Country Code", "Indicator Code", "Indicator Name"], axis=1)
    temp_df = temp_df.set_index('Country Name').transpose()
    temp_df.index = temp_df.index.astype(int)
    return temp_df[temp_df.index < check_year].values.flatten()


def calculate_demographic_indicators(df: pd.DataFrame, check_year: int) -> Tuple[np.ndarray, ...]:
    """
    Рассчитывает основные демографические показатели.
    
    Args:
        df: DataFrame с данными страны
        check_year: Год для проверки данных
        
    Returns:
        Кортеж с показателями (население, смертность, рождаемость, миграция)
    """
    population_data = get_country_indicator_data(df, "SP.POP.TOTL", check_year)
    death_data = get_country_indicator_data(df, "SP.DYN.CDRT.IN", check_year)
    birth_data = get_country_indicator_data(df, "SP.DYN.CBRT.IN", check_year)
    migration_data = get_country_indicator_data(df, "SM.POP.NETM", check_year)
    
    # Конвертируем миграцию в промилле
    migration_data = (migration_data / population_data) * 1000
    
    return population_data, death_data, birth_data, migration_data


def calculate_growth_model(years: np.ndarray, delta: np.ndarray) -> Tuple[float, float, float]:
    """
    Рассчитывает модель роста населения.
    
    Args:
        years: Массив лет
        delta: Массив изменений населения
        
    Returns:
        Кортеж с параметрами модели (коэффициент, константа, стандартное отклонение)
    """
    model = stats.linregress(years, delta)
    b, k = model[1], model[0]
    
    delta_expected = b + k * years
    residuals = delta_expected - delta
    stdev = np.sqrt(np.sum(residuals**2) / (len(years) - 2))
    
    return b, k, stdev 