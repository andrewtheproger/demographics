import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from typing import List, Tuple


def load_demographic_data(country: str) -> pd.DataFrame:
    """
    Загружает демографические данные для указанной страны.
    
    Args:
        country: Название страны
        
    Returns:
        DataFrame с демографическими данными
    """
    df = pd.read_excel("dataset.xls", sheet_name='Data')
    df = df[df["Country Name"] == country]
    
    # Фильтруем только индикаторы возрастных групп (оканчиваются на 5Y)
    age_indicators = df["Indicator Code"].str.endswith("5Y")
    df = df[age_indicators]
    
    return df


def process_demographic_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Обрабатывает демографические данные для построения пирамиды.
    
    Args:
        df: DataFrame с исходными данными
        
    Returns:
        DataFrame с обработанными данными
    """
    # Преобразуем данные для женщин в отрицательные значения
    df["2019"] = df.apply(
        lambda x: -x["2019"] if "FE" in x["Indicator Code"] else x["2019"],
        axis=1
    )
    
    # Добавляем столбцы с полом и возрастной группой
    df["Пол"] = np.where(
        df["Indicator Code"].str.contains("FE"),
        "Женский",
        "Мужской"
    )
    
    # Извлекаем возрастные группы из кода индикатора
    df["age_group"] = df["Indicator Code"].apply(
        lambda x: f'{x.split(".")[2][:2]}-{x.split(".")[2][2:]}'
    )
    
    return df


def create_demographic_pyramid(
    df: pd.DataFrame,
    country: str,
    save_path: str = "./pyramids"
) -> None:
    """
    Создает визуализацию демографической пирамиды.
    
    Args:
        df: DataFrame с обработанными данными
        country: Название страны
        save_path: Путь для сохранения графика
    """
    # Создаем график
    plt.figure(figsize=(10, 8))
    ax = sns.barplot(
        data=df,
        x="2019",
        y="age_group",
        hue="Пол",
        dodge=False,
        palette=sns.color_palette("crest", 2)
    )
    
    # Настраиваем отображение меток оси X (абсолютные значения)
    labels = [abs(x) for x in ax.get_xticks()]
    ax.set_xticklabels(labels)
    
    # Добавляем заголовок и подписи осей
    plt.title(f"Демографическая пирамида - {country}", pad=20)
    plt.xlabel('Процент населения')
    plt.ylabel('Возрастная группа')
    
    # Добавляем сетку для лучшей читаемости
    plt.grid(True, axis='x', linestyle='--', alpha=0.7)
    
    # Сохраняем график
    plt.tight_layout()
    plt.savefig(f"{save_path}/{country}.png", dpi=300, bbox_inches='tight')
    plt.close()


def main():
    """
    Основная функция программы.
    """
    try:
        # Получаем название страны
        country = input("Введите название страны: ")
        
        # Загружаем и обрабатываем данные
        df = load_demographic_data(country)
        if df.empty:
            raise ValueError(f"Данные для страны '{country}' не найдены")
            
        df = process_demographic_data(df)
        
        # Создаем визуализацию
        create_demographic_pyramid(df, country)
        
        print(f"График сохранен в ./pyramids/{country}.png")
        
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")


if __name__ == "__main__":
    main()