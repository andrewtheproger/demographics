import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from typing import List, Dict


def load_birth_rate_data() -> pd.DataFrame:
    """
    Загружает данные о рождаемости из Excel файла.
    
    Returns:
        DataFrame с данными о рождаемости
    """
    df = pd.read_excel("../dataset.xls", sheet_name='Data')
    df = df[df["Indicator Code"] == "SP.DYN.CBRT.IN"]
    
    return df


def process_birth_rate_data(df: pd.DataFrame, countries: List[str]) -> pd.DataFrame:
    """
    Обрабатывает данные о рождаемости для визуализации.
    
    Args:
        df: DataFrame с исходными данными
        countries: Список стран для анализа
        
    Returns:
        DataFrame с обработанными данными
    """
    # Устанавливаем индекс и удаляем ненужные столбцы
    df = df.set_index('Country Name')
    df = df.drop(["Country Code", "Indicator Code", "Indicator Name"], axis=1)
    
    # Транспонируем данные и преобразуем в длинный формат
    df = df.transpose()
    df = df.reset_index(names="year")
    
    # Преобразуем в формат "длинных данных"
    df = df.melt(
        id_vars=["year"],
        value_vars=[col for col in df.columns if col != "year"]
    )
    
    # Преобразуем год в числовой формат и фильтруем страны
    df["year"] = df["year"].astype("int64")
    df = df[df["Country Name"].isin(countries)]
    
    return df


def create_birth_rate_plot(
    df: pd.DataFrame,
    country_labels: Dict[str, str],
    save_path: str = "./images/birth_rate.png"
) -> None:
    """
    Создает график рождаемости по странам.
    
    Args:
        df: DataFrame с обработанными данными
        country_labels: Словарь с переводами названий стран
        save_path: Путь для сохранения графика
    """
    # Создаем график
    plt.figure(figsize=(12, 6))
    ax = sns.relplot(
        data=df,
        x="year",
        y="value",
        hue="Country Name",
        kind="line",
        palette=sns.color_palette("mako", len(country_labels)),
        height=6,
        aspect=2
    )
    
    # Настраиваем оси и заголовки
    plt.xlabel('Год')
    plt.ylabel('Рождаемость на 1000 человек')
    ax.legend.set_title("Страна")
    
    # Обновляем легенду
    for t, country in zip(ax._legend.texts, df["Country Name"].unique()):
        t.set_text(country_labels.get(country, country))
    
    # Добавляем сетку и настраиваем внешний вид
    ax.ax.grid(True, linestyle='--', alpha=0.7)
    plt.title("Динамика рождаемости по странам", pad=20)
    
    # Сохраняем график
    plt.savefig(save_path, transparent=True, dpi=300, bbox_inches='tight')
    plt.close()


def main():
    """
    Основная функция программы.
    """
    try:
        # Определяем страны и их переводы
        countries = ["Nigeria", "China", "United States", "Russian Federation"]
        country_labels = {
            "China": "Китай",
            "Nigeria": "Нигерия",
            "Russian Federation": "Россия",
            "United States": "США"
        }
        
        # Загружаем и обрабатываем данные
        df = load_birth_rate_data()
        if df.empty:
            raise ValueError("Не удалось загрузить данные о рождаемости")
            
        df = process_birth_rate_data(df, countries)
        
        # Создаем визуализацию
        create_birth_rate_plot(df, country_labels)
        
        print("График сохранен в birth_rate.png")
        
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")


if __name__ == "__main__":
    main()
