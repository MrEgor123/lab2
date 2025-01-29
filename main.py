import random
import xml.etree.ElementTree as ET
import json
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Функция для обработки данных из XML
def parse_xml_element(element):
    if element.tag in ["original_price", "discounted_price"]:
        return int(element.text)
    return element.text

# Функция для генерации случайных продаж
def generate_sales_for_sofa(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    print(f"\nОбработка файла: {xml_file}")
    print("-" * 50)

    json_data = []

    for sofa in root.findall("sofa"):
        sofa_data = {}
        for child in sofa:
            sofa_data[child.tag] = parse_xml_element(child)

        # Генерируем продажи за 12 месяцев
        sales = [random.randint(50, 200) for _ in range(12)]
        sofa_data["monthly_sales"] = sales
        sofa_data["total_sales"] = sum(sales)

        json_data.append(sofa_data)

        # Вывод информации
        print(f"Модель: {sofa_data['name']}")
        print(f"Цена: {sofa_data['original_price']} руб.")
        print(f"Цена со скидкой: {sofa_data['discounted_price']} руб.")
        print(f"Скидка: {sofa_data['discount_percentage']}")
        print(f"Продажи по месяцам: {sales}")
        print(f"Общие продажи: {sum(sales)}")
        print("-" * 50)

    # Сохраняем JSON
    json_filename = xml_file.replace(".xml", ".json")
    with open(json_filename, "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)

    print(f"Данные сохранены в: {json_filename}")
    return json_data

# Функция для визуализации данных
def visualize_sales(all_json_data, base_filename):
    months = ["Янв", "Фев", "Мар", "Апр", "Май", "Июн",
              "Июл", "Авг", "Сен", "Окт", "Ноя", "Дек"]

    # Создаем DataFrame
    df_data = []
    for json_data in all_json_data:
        for sofa in json_data:
            for month, sale in zip(months, sofa["monthly_sales"]):
                df_data.append({
                    "Модель": sofa["name"],
                    "Месяц": month,
                    "Продажи": sale
                })

    df = pd.DataFrame(df_data)

    # Создаем общий график
    plt.figure(figsize=(12, 6))
    sns.barplot(data=df, x="Месяц", y="Продажи", hue="Модель", palette=["blue", "red"])
    plt.title("Сравнение продаж диванов по месяцам")
    plt.xlabel("Месяц")
    plt.ylabel("Количество продаж")
    plt.xticks(rotation=45)
    plt.legend(title="Модели")
    plt.tight_layout()

    # Сохраняем график
    chart_file = f"{base_filename}_sales_chart.png"
    plt.savefig(chart_file)
    plt.show()

    # Создаем и сохраняем таблицу продаж
    pivot_table = pd.pivot_table(
        df,
        values="Продажи",
        index="Модель",
        columns="Месяц",
        aggfunc="sum"
    )

    table_file = f"{base_filename}_sales_table.csv"
    pivot_table.to_csv(table_file, encoding="utf-8-sig")

    print("\nОбщая таблица продаж:")
    print("=" * 100)
    print(pivot_table)
    print("\nГрафик сохранён в:", chart_file)
    print("Таблица сохранена в:", table_file)

# Главный блок программы
if __name__ == "__main__":
    xml_files = ["sofa1.xml", "sofa2.xml"]
    all_sofas_data = []

    for xml_file in xml_files:
        sofa_data = generate_sales_for_sofa(xml_file)
        all_sofas_data.append(sofa_data)

    # Визуализация данных
    visualize_sales(all_sofas_data, "sofa_comparison")
