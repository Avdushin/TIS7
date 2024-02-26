import time
import concurrent.futures
import matplotlib.pyplot as plt
from main import ECalc

def run_sequential_requests(expressions, num_iterations):
    calculator = ECalc()
    start_time = time.time()

    for _ in range(num_iterations):
        for expression in expressions:
            calculator.calc_expr(expression)

    end_time = time.time()
    total_time = end_time - start_time
    requests_per_second = (num_iterations * len(expressions)) / total_time

    return requests_per_second, total_time

def run_parallel_requests(expressions, num_workers):
    calculator = ECalc()
    start_time = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        results = list(executor.map(calculator.calc_expr, expressions))

    end_time = time.time()
    return results, end_time - start_time

def plot_bar_chart(ax, x_values, y_values, title, xlabel, ylabel):
    ax.bar(x_values, y_values)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

def main():
    expressions = ["2+(-5)*(7-8)" for _ in range(100)]
    num_iterations = 1000

    sequential_requests_per_second, _ = run_sequential_requests(expressions, num_iterations)
    print(f"Количество запросов в секунду (последовательно): {sequential_requests_per_second:.2f}")

    max_parallel_requests = 0
    max_parallel_time = float('inf')

    #@ Параллельные запросы
    num_workers_list = [2**i for i in range(7)]

    #@ Тест-кейсы
    test_expressions = [
        "2+(-5)*(7-8)",
        "10*(2+3)-7",
        "sqrt(16)+3",
        "sin(0.5)",
        "log(10)",
        "2**10",
        "cos(0.8)",
        "sum(range(10**6))",
    ]

    #@ Макет окна тестов
    num_rows = (len(test_expressions) + 1) // 2
    num_cols = 2

    fig, axes = plt.subplots(num_rows, num_cols, figsize=(10, 5 * num_rows))
    axes = axes.flatten()

    for i, expression in enumerate(test_expressions):
        expression_times = []
        for num_workers in num_workers_list:
            _, time_taken = run_parallel_requests([expression] * 100, num_workers)
            expression_times.append(time_taken)

            if time_taken < max_parallel_time:
                max_parallel_time = time_taken
                max_parallel_requests = num_workers * 100

        #@ Столбчатая диаграмма тестов
        plot_bar_chart(axes[i], num_workers_list, expression_times,
                       f"Тест '{expression}'",
                       "Количество параллельных запросов (log шкала)", "Время выполнения (секунды)")

    print(f"Максимальное количество параллельных запросов без сбоев: {max_parallel_requests}")
    fig.suptitle("Результаты нагрузочного тестирования", y=0.94)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
