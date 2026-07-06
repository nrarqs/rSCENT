# rSCENT - Perfume Inventory & Sales Manager

A minimalist Command Line Interface (CLI) application built with Python and SQLite to manage perfume stocks and track sales. It features dynamic stock updates and automated financial reports.

## Key Features

* **Stock Management:** Add new perfumes or automatically update the stock and purchase price of existing items.
* **Sales Tracker:** Record individual sales with custom prices, payment methods (Cash/Card), and automated real-time timestamps.
* **Financial Reports:** Live metrics calculating Total Revenue and Net Profit using SQL table joins (`INNER JOIN`) and aggregations.
* **Inventory Control:** Automatically validates and decreases stock quantities upon every successful sale.

## Database Schema

The SQLite database (`bilee.db`) consists of two interconnected tables:
* **inventory:** Stores perfume details (`brand`, `name`, `purchase_price`, `stock`).
* **sales:** Tracks transactional data linked via `perfume_id` as a Foreign Key.

## How to Run

1. Ensure you have Python installed.
2. Clone the repository and navigate to the project directory.
3. Run the application via terminal:

```bash
python3 rSCENT.py
