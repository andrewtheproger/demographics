import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from demographic_utils import (
    load_country_data,
    calculate_demographic_indicators,
    calculate_growth_model
)


def predict_population_growth(
    initial_population: int,
    forecast_years: np.ndarray,
    forecast_delta: np.ndarray,
    interval: float
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Прогнозирует рост населения по трем сценариям.
    
    Args:
        initial_population: Начальная численность населения
        forecast_years: Массив лет для прогноза
        forecast_delta: Массив ожидаемых изменений
        interval: Интервал для расчета экстремальных сценариев
        
    Returns:
        Кортеж с прогнозами по трем сценариям
    """
    n_years = len(forecast_years)
    population = np.zeros(n_years, dtype=np.int64)
    population_worst = np.zeros_like(population)
    population_best = np.zeros_like(population)
    
    population[0] = population_worst[0] = population_best[0] = initial_population
    
    for i in range(1, n_years):
        year = forecast_years[i]
        if year > 2020:
            population[i] = int(population[i-1] * (1 + forecast_delta[i-1]/1000))
            population_worst[i] = int(population_worst[i-1] * (1 + (forecast_delta[i-1] + interval)/1000))
            population_best[i] = int(population_best[i-1] * (1 + (forecast_delta[i-1] - interval)/1000))
        else:
            population[i] = int(population[i-1] * (1 + forecast_delta[i-1]/1000))
            population_worst[i] = int(population_worst[i-1] * (1 + forecast_delta[i-1]/1000))
            population_best[i] = int(population_best[i-1] * (1 + forecast_delta[i-1]/1000))
    
    return population, population_worst, population_best


def create_population_plot(
    country: str,
    forecast_years: np.ndarray,
    population: np.ndarray,
    population_worst: np.ndarray,
    population_best: np.ndarray,
    save_path: str = "./population"
) -> None:
    """
    Создает визуализацию прогноза численности населения.
    
    Args:
        country: Название страны
        forecast_years: Массив лет
        population: Прогноз по базовому сценарию
        population_worst: Прогноз по пессимистичному сценарию
        population_best: Прогноз по оптимистичному сценарию
        save_path: Путь для сохранения графика
    """
    # Создаем DataFrame для графика
    n_years = len(forecast_years)
    graph_data = pd.DataFrame({
        "Год": np.tile(forecast_years, 3),
        "Прогноз": np.repeat(["Базовый", "Целевой", "Консервативный"], n_years),
        "Население": np.concatenate([population, population_worst, population_best])
    })
    
    # Создаем график
    plt.figure(figsize=(12, 6))
    ax = sns.scatterplot(
        data=graph_data,
        hue="Прогноз",
        x="Год",
        y="Население",
        palette=sns.color_palette("crest", 3)
    )
    
    # Настраиваем внешний вид
    plt.title(f"Прогноз численности населения - {country}", pad=20)
    plt.grid(True, linestyle='--', alpha=0.7)
    
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
        print(f"При экстремально высокой рождаемости: {int((b + interval) / (-k))} год")
        print(f"При экстремально низкой рождаемости: {int((b - interval) / (-k))} год")
        print(f"Наиболее вероятный исход: {int(b / (-k))} год")
        
        # Создаем прогноз
        forecast_years = np.arange(1960, 2201)
        forecast_delta = np.concatenate([delta, b + k * np.arange(check_year, 2201)])
        initial_population = int(population_data[0])
        
        # Рассчитываем прогнозы населения
        population, population_worst, population_best = predict_population_growth(
            initial_population, forecast_years, forecast_delta, interval
        )
        
        # Создаем визуализацию
        create_population_plot(
            country, forecast_years, population, population_worst, population_best
        )
        
        print(f"График сохранен в ./population/{country}.png")
        
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")


if __name__ == "__main__":
    main()