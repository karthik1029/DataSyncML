# DataSyncML

ETL (Extract, Transform, Load) using Machine Learning (ML) to transform and load data from PostgreSQL to MongoDB, with real-time data visualization using a Shiny dashboard. 
This application allows users to perform CRUD operations on PostgreSQL data, transfer and clean data using ML techniques during the ETL process, and visualize/export the data.

## Features

- **Data Visualization**: Real-time data visualization using a Shiny dashboard.
- **CRUD Operations**: Supports Create, Read, Update, and Delete operations on data stored in PostgreSQL.
- **ML**: Use ML to clean the data before transferring to MongoDB including filling missing values with custom defaults and converting the data types.
- **ETL**: Load the data into MongoDB collection.
## Prerequisites

- Python 3.8+
- PostgreSQL
- MongoDB Cluster using Atlas
- Shiny for Python

## Installation

### Step 1: Install PostgreSQL

1. [Download and install PostgreSQL](https://www.postgresql.org/download/).
2. Ensure that PostgreSQL is running on your system.
3. [Create a MongoDB cluster using MongoDB Atlas](https://www.mongodb.com/lp/cloud/atlas/try4-reg?utm_source=google&utm_campaign=search_gs_pl_evergreen_atlas_general_prosp-brand_gic-null_amers-us_ps-all_desktop_eng_lead&utm_term=mongodb%20cluster&utm_medium=cpc_paid_search&utm_ad=p&utm_ad_campaign_id=1718986498&adgroup=150907551034&cq_cmp=1718986498&gad_source=1&gclid=CjwKCAjwvKi4BhABEiwAH2gcwz5UZyFmZ4s-gVjlOmnic3PFyN5uibLj4q5TrsEW_WydNDB9vzaRBRoCvh0QAvD_BwE)
4. Create your own Document and Collection.

### Step 2: Set Up Python Environment

1. Set up a Python virtual environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install psycopg2 pandas shiny
   pip install scikit-learn
   pip install Jinja2

### Step 3: Configure Database Connection
Edit the Python script to include your PostgreSQL database credentials:
- Host
- Database name
- User
- Password

MongoDB connection URI:
- MONGO_URI = "your-mongo-uri"

### Step 4:  Launch the Shiny App
   ```bash
   python path/to/your_script.py
   ```

## Usage
### Dashboard Features
- Once the Shiny app is running, navigate to the provided URL (typically http://localhost:8080/).
- PostgreSQL Data: Use the dashboard to view, add, update, and delete data stored in the PostgreSQL database.
- Transfer Data: Use the Transfer Data button to migrate the data from PostgreSQL to MongoDB.
- ML Data Cleaning: During the data transfer, machine learning techniques are used to:
  - Fill missing values with the string "not provided".
  - Convert the year column from a string to an integer.
- MongoDB Data: View the transferred data from PostgreSQL that is now stored in MongoDB.

## Example Workflow
- Start the app and access the Shiny dashboard.
- View and interact with the PostgreSQL data.
- Add new records or update existing records in PostgreSQL.
- Transfer data from PostgreSQL to MongoDB by clicking the Transfer Data button.
- Data will be cleaned using machine learning techniques before it is inserted into MongoDB.
- View the newly transferred data in MongoDB.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.


## Additional Notes
Ensure proper security practices for storing and managing database credentials, especially when deploying to production.