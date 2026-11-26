# EDA: библиотека реальных данных и лабораторных работ

Этот пакет добавляет к основному HTML-учебнику практику на **реальных открытых наборах данных**. Все 12 наборов выбраны из UCI Machine Learning Repository; на страницах перечисленных версий указана лицензия **CC BY 4.0**. Для Air Quality страница UCI дополнительно содержит отдельное ограничение «research purposes only / commercial purposes excluded» — не используй этот набор коммерчески без отдельного разрешения. Перед повторной публикацией или распространением производных файлов сохраняй атрибуцию и перепроверяй условия на официальной странице набора.

## Содержимое

- `EDA_Real_Data_Catalog.csv` и `.json` — каталог, источники, DOI, лицензии и исследовательские caveats.
- `download_uci_datasets.py` — скачивает данные через официальный пакет `ucimlrepo` в `data/raw/`, metadata — в `data/metadata/`.
- `EDA_Real_Lab_01_...` — Online Retail, транзакции/RFM/когорты.
- `EDA_Real_Lab_02_...` — Bike Sharing и Appliances Energy, временные ряды.
- `EDA_Real_Lab_03_...` — Online Shoppers и Bank Marketing, conversion и leakage.
- `EDA_Real_Lab_04_...` — Student Performance и Wine Quality, target semantics.
- `EDA_Real_Lab_05_...` — Air Quality, sentinel missing и sensor drift.
- `EDA_Real_Lab_06_...` — Adult и Credit Default, групповой аудит и ограничения fairness.
- `EDA_Real_Lab_07_...` — Wholesale и Abalone, clustering и регрессия.
- `EDA_Real_Labs_Solutions.ipynb` — методические ориентиры и критические caveats.
- `EDA_Real_Data_Blind_Project.ipynb` — самостоятельный проект без пошагового алгоритма.
- `EDA_Research_Report_Template.md` — шаблон итогового аналитического отчёта.
- `EDA_Data_Dictionary_Template.csv` — шаблон словаря переменных и доступности признаков.

## Установка

Из корневой папки курса:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements-eda-real.txt
```

## Скачивание данных

Список доступных наборов:

```powershell
python download_uci_datasets.py --list
```

Скачивание только первого набора:

```powershell
python download_uci_datasets.py --only online_retail
```

Скачивание всех 12 наборов:

```powershell
python download_uci_datasets.py
```

По умолчанию существующие CSV не перезаписываются. Для обновления конкретного набора используй `--force`. Можно передать UCI ID вместо slug, например `--only 352,275`.

**Важно:** загрузка реальных данных требует интернета только при первом запуске downloader. После сохранения `data/raw/*.csv` сами лабораторные работают локально. HTML-учебник и встроенный MathJax не зависят от сети.

## Рекомендуемый порядок

1. `EDA_Real_Lab_01_Online_Retail.ipynb` — учишься определять grain, возвраты, revenue и cohort.
2. `EDA_Real_Lab_02_Bike_and_Energy.ipynb` — осваиваешь временную структуру и leakage.
3. `EDA_Real_Lab_03_Conversion_and_Bank.ipynb` — сравниваешь две классификационные задачи и прогнозный момент.
4. `EDA_Real_Lab_04_Student_and_Wine.ipynb` — изучаешь постановку target и ordinal шкалу.
5. `EDA_Real_Lab_05_Air_Quality.ipynb` — работаешь с sentinel missing и датчиками.
6. `EDA_Real_Lab_06_Adult_and_Credit_Fairness.ipynb` — проводишь ограниченный fairness audit.
7. `EDA_Real_Lab_07_Wholesale_and_Abalone.ipynb` — ненадзорный анализ и чувствительность кластеров.
8. `EDA_Real_Data_Blind_Project.ipynb` — выбери датасет и исследуй его без инструкции.

Смотри `EDA_Real_Labs_Solutions.ipynb` только после собственной попытки.

## Принцип использования реальных данных

Не исправляй значения автоматически до выяснения семантики. Не смешивай строку, событие, пользователя, заказ и временной снимок. Для каждого ML-вопроса определи момент прогноза и проверь, доступны ли признаки в этот момент. Не называй ассоциации причинными эффектами. Фиксируй альтернативные объяснения, ограничения выборки и неопределённость.

## Источники и атрибуция

Все dataset pages и DOI приведены в `EDA_Real_Data_Catalog.csv`. Основной источник — UCI Machine Learning Repository. Лицензия для перечисленных наборов — CC BY 4.0, как указано на соответствующих страницах UCI.

## Отчёт и словарь переменных

Перед началом исследования скопируй `EDA_Data_Dictionary_Template.csv` и опиши смысл переменных, типы, единицы, диапазоны, специальные коды пропусков, роли и доступность на момент прогноза. По итогам заполни `EDA_Research_Report_Template.md`: он требует фиксировать происхождение данных, единицу наблюдения, качество, распределения, связи, ограничения и воспроизводимость. Не ограничивайся графиками — каждый вывод должен опираться на конкретное свидетельство.
