# Natural-Language Weather Data Explorer

Projekt realizujący zautomatyzowany potok przetwarzania danych pogodowych (ETL) w chmurze AWS z wykorzystaniem architektury serverless. System cyklicznie pobiera surowe dane z OpenWeatherMap API, przetwarza je do wydajnego formatu kolumnowego, a następnie udostępnia przeglądarkowy interfejs pozwalający na odpytywanie bazy danych w języku naturalnym.

## Architektura i wykorzystane technologie

Projekt opiera się na usługach chmurowych Amazon Web Services (AWS):

* **Amazon EventBridge:** Orkiestracja i automatyzacja potoku. Reguły harmonogramu uruchamiają pobieranie danych co 15 minut.
* **AWS Lambda:** * `FetchWeatherData`: Pobieranie surowych danych w formacie JSON z zewnętrznego API.
    * `WeatherAssistant`: Mapowanie pytań z języka naturalnego na zoptymalizowane zapytania SQL i formatowanie odpowiedzi.
* **Amazon S3:** Warstwa składowania danych (Data Lake). Podział na strefę danych surowych (Raw Data - JSON) oraz przetworzonych (Curated Data - Parquet).
* **AWS Glue (Apache Spark):** Rozproszone przetwarzanie ETL. Spłaszczanie zagnieżdżonych struktur, rzutowanie typów oraz wzbogacanie rekordów o uniksowy znacznik czasu (timestamp).
* **Amazon Athena:** Bezserwerowy silnik zapytań uruchamiający instrukcje SQL bezpośrednio na plikach Parquet, gwarantując pobieranie najświeższych pomiarów.
* **Amazon API Gateway:** Konfiguracja interfejsu REST API z włączonym mechanizmem CORS (Lambda Proxy Integration) dla aplikacji klienckiej.
* **Frontend:** Czysty HTML i JavaScript wykorzystujący Fetch API do asynchronicznej komunikacji z chmurą.

## Struktura repozytorium

* `/frontend` - Kod aplikacji klienckiej (interfejs użytkownika).
* `/backend` - Kody źródłowe funkcji AWS Lambda realizujących ingestie danych oraz logikę asystenta Q&A.
* `/glue_etl` - Skrypt PySpark wykorzystany w zadaniu AWS Glue do transformacji danych.
* `/database` - Definicja schematu tabeli zewnętrznej DDL dla usługi Amazon Athena.
* `/documentation` - Sprawozdanie z realizacji projektu w formacie LaTeX.
