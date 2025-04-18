import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from demographic_utils import (
    load_country_data,
    calculate_demographic_indicators,
    calculate_growth_model
)


def create_growth_rate_plot(
    country: str,
    years: np.ndarray,
    delta: np.ndarray,
    delta_expected: np.ndarray,
    interval: float,
    b: float,
    k: float,
    save_path: str = "./growth_rate"
) -> None:
    """
    Создает визуализацию темпов роста населения.
    
    Args:
        country: Название страны
        years: Массив лет
        delta: Фактические темпы роста
        delta_expected: Ожидаемые темпы роста
        interval: Интервал для расчета экстремальных сценариев
        b: Константа модели роста
        k: Коэффициент модели роста
        save_path: Путь для сохранения графика
    """
    # Создаем массивы для прогнозов
    forecast_years = np.arange(1960, 2101)
    forecast_delta = b + k * forecast_years
    
    # Создаем массивы для всех сценариев
    all_years = np.concatenate([forecast_years, forecast_years, forecast_years, years])
    all_delta = np.concatenate([
        forecast_delta,
        forecast_delta + interval,
        forecast_delta - interval,
        delta
    ])
    
    # Создаем массив типов прогнозов
    n_forecast = len(forecast_years)
    types = np.concatenate([
        np.repeat("Базовый", n_forecast),
        np.repeat("Целевой", n_forecast),
        np.repeat("Консервативный", n_forecast),
        np.repeat("Фактический", len(years))
    ])
    
    # Создаем DataFrame для графика
    graph_data = pd.DataFrame({
        "Год": all_years,
        "Прогноз": types,
        "Темп прироста на 1000 человек": all_delta
    })
    
    # Создаем график
    plt.figure(figsize=(12, 6))
    ax = sns.relplot(
        data=graph_data,
        x="Год",
        y="Темп прироста на 1000 человек",
        hue="Прогноз",
        kind="line",
        palette=sns.color_palette("mako", 4),
        height=6,
        aspect=2
    )
    
    # Настраиваем внешний вид
    plt.xlabel('Год')
    plt.ylabel('Темп прироста на 1000 человек')
    ax.legend.set_title("Прогноз")
    plt.title(f"Прогноз темпов роста населения - {country}", pad=20)
    ax.ax.grid(True, linestyle='--', alpha=0.7)
    
    # Сохраняем график
    plt.savefig(f"{save_path}/{country}.png", dpi=300, bbox_inches='tight')
    plt.close()


def main():
    """
    Основная функция программы.
    """
    try:
        # Получаем входные данные
        country = input("Введите название страны: ")
        check_year = min(int(input("Введите год для проверки: ")), 2022)
        
        # Загружаем данные
        df = load_country_data(country, check_year)
        if df.empty:
            raise ValueError(f"Данные для страны '{country}' не найдены")
        
        # Получаем демографические показатели
        population_data, death_data, birth_data, migration_data = calculate_demographic_indicators(df, check_year)
        
        # Рассчитываем изменение населения
        delta = birth_data + migration_data - death_data
        years = np.arange(1960, check_year)
        b, k, stdev = calculate_growth_model(years, delta)
        interval = 1.282 * stdev
        
        # Выводим прогнозы
        print(f"При экстремально высоком приросте: {(b + interval) / (-k)} год")
        print(f"При экстремально низком приросте: {(b - interval) / (-k)} год")
        print(f"Наиболее вероятный исход: {b / (-k)} год")
        
        # Создаем визуализацию
        create_growth_rate_plot(
            country, years, delta, b + k * years, interval, b, k
        )
        
        print(f"График сохранен в ./growth_rate/{country}.png")
        
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")


if __name__ == "__main__":
    main()