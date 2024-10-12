from shiny import App, reactive, render, ui
from pymongo import MongoClient
import pandas as pd
import psycopg2

# MongoDB connection using the provided URI
MONGO_URI = "mongodb+srv://<uid>:<pwd>@<clusterinfo>/?retryWrites=true&w=majority&appName=Cluster0"
mongo_client = MongoClient(MONGO_URI)
mongo_db = mongo_client['sample_mflix']  # Use your MongoDB database name
mongo_collection = mongo_db['movies_pgsql']  # Use your MongoDB collection name
mongo_pgsql_collection = mongo_db['movies_pgsql']  # New MongoDB collection for transferred data

# PgSQL
pgsql_table = "movies"

# ------------------ PostgreSQL Functions ------------------
def connect_to_pgsql():
    conn = psycopg2.connect(
        host="localhost",  # Replace with your host
        database="test",  # Replace with your database name
        user="<uid>",  # Replace with your username
        password="<pwd>"  # Replace with your password
    )
    return conn

def fetch_pgsql_data():
    conn = connect_to_pgsql()
    query = f"SELECT * FROM {pgsql_table}"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def insert_into_pgsql(new_row):
    conn = connect_to_pgsql()
    cursor = conn.cursor()

    new_row = {k: v for k, v in new_row.items() if v}
    if 'id' in new_row:
        del new_row['id']

    columns = ', '.join(new_row.keys())
    values = ', '.join(['%s'] * len(new_row))
    query = f"INSERT INTO movies ({columns}) VALUES ({values})"
    cursor.execute(query, list(new_row.values()))
    conn.commit()
    cursor.close()
    conn.close()

def update_pgsql_data(row_id, updated_row):
    conn = connect_to_pgsql()
    cursor = conn.cursor()
    set_clause = ', '.join([f"{key} = %s" for key in updated_row.keys()])
    query = f"UPDATE movies SET {set_clause} WHERE id = %s"
    cursor.execute(query, list(updated_row.values()) + [row_id])
    conn.commit()
    cursor.close()
    conn.close()

# ------------------ MongoDB Functions ------------------

# Fetch data from MongoDB
def fetch_mongodb_data(limit=10):
    movies_data = mongo_collection.find().limit(limit)
    df = pd.DataFrame(list(movies_data))

    # Select only a few columns for display
    df = df[['_id', 'movies', 'year', 'director']]  # Simplify by displaying only key columns

    # Flatten lists (if any) in the dataframe
    df = df.apply(lambda col: col.apply(lambda x: ', '.join(x) if isinstance(x, list) else x))

    # Replace NaN values with an empty string for display purposes
    df.fillna('', inplace=True)

    return df


# Transfer data from PostgreSQL to MongoDB (movies_pgsql)
def transfer_data_pgsql_to_mongo():
    pgsql_data = fetch_pgsql_data()

    # ---- Data Cleaning Steps ----
    # Fill missing values with "not provided"
    pgsql_data.fillna("not provided", inplace=True)

    # Convert 'year' from string to integer (handle non-convertible cases)
    pgsql_data['year'] = pd.to_numeric(pgsql_data['year'], errors='coerce').fillna(0).astype(int)

    # ---- Insert Data into MongoDB ----
    for _, row in pgsql_data.iterrows():
        # Convert the row to a dictionary and insert into the MongoDB collection
        mongo_pgsql_collection.insert_one(row.to_dict())

    print(f"Transferred {len(pgsql_data)} records from PostgreSQL to MongoDB.")
# ------------------ Shiny UI and Server ------------------
# Shiny UI layout
app_ui = ui.page_fluid(
    ui.h2("ETL From PostgreSQL to MongoDB"),

    # PostgreSQL Controls
    ui.h3("PostgreSQL Data"),
    ui.input_action_button("refresh_pg", "Refresh PostgreSQL Data"),
    ui.input_text("new_pg_data", "New Data (comma-separated)"),
    ui.input_action_button("add_pg_row", "Add Row to PostgreSQL"),
    ui.input_numeric("update_pg_id", "PostgreSQL Row ID to Update", value=0),
    ui.input_text("update_pg_data", "Updated Data (comma-separated including ID)"),
    ui.input_action_button("update_pg_row", "Update Row in PostgreSQL"),
    ui.output_table("pgsql_table"),

    ui.hr(),

    # MongoDB Controls
    ui.h3("MongoDB Data"),
    ui.input_numeric("num_records_mongo", "Number of MongoDB records to display", value=10, min=1),
    ui.input_action_button("fetch_mongo", "Fetch MongoDB Data"),
    ui.output_table("mongo_table"),

    ui.hr(),

    # Transfer Button
    ui.h3("Transfer Data"),
    ui.input_action_button("transfer_pg_to_mongo", "Transfer PostgreSQL Data to MongoDB")
)


# Server logic
def server(input, output, session):
    # Reactive variable for MongoDB data
    mongo_df = reactive.Value(pd.DataFrame())

    # Reactive variable for PostgreSQL data
    pgsql_df = reactive.Value(fetch_pgsql_data())

    # Fetch and display MongoDB data
    @reactive.Effect
    @reactive.event(input.fetch_mongo)
    def fetch_and_display_mongo_data():
        limit = input.num_records_mongo()
        mongo_df.set(fetch_mongodb_data(limit))

    @output
    @render.table
    def mongo_table():
        return mongo_df()

    # Fetch and display PostgreSQL data
    @reactive.Effect
    @reactive.event(input.refresh_pg)
    def fetch_and_display_pgsql_data():
        pgsql_df.set(fetch_pgsql_data())

    @output
    @render.table
    def pgsql_table():
        return pgsql_df()

    # Add new row to PostgreSQL
    @reactive.Effect
    @reactive.event(input.add_pg_row)
    def add_pg_row():
        if input.new_pg_data():
            new_row = dict(zip(pgsql_df().columns, input.new_pg_data().split(',')))
            insert_into_pgsql(new_row)
            pgsql_df.set(fetch_pgsql_data())

    # Update row in PostgreSQL
    @reactive.Effect
    @reactive.event(input.update_pg_row)
    def update_pg_row():
        if input.update_pg_id() and input.update_pg_data():
            updated_row = dict(zip(pgsql_df().columns, input.update_pg_data().split(',')))
            update_pgsql_data(input.update_pg_id(), updated_row)
            pgsql_df.set(fetch_pgsql_data())

    # Transfer data from PostgreSQL to MongoDB
    @reactive.Effect
    @reactive.event(input.transfer_pg_to_mongo)
    def transfer_pg_to_mongo():
        transfer_data_pgsql_to_mongo()
        ui.notification_show("Data transferred from PostgreSQL to MongoDB!", duration=3)


app = App(app_ui, server)

if __name__ == "__main__":
    app.run()
