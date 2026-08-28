import pandas as pd 

#Load valid user IDs
users = pd.read_csv(
    "data/users.csv",
    usecols=["user_id"]
)

valid_user_ids = set(users["user_id"])

invalid_count = 0
total_rows = 0

#Process orders in chunks

for chunk in pd.read_csv(
    "data/orders.csv",
    usecols=["user_id"],
    chunksize=500_000
):
    total_rows += len(chunk)

    invalid = ~chunk["user_id"].isin(valid_user_ids)

    invalid_count += invalid.sum() 

print("Total orders checked:",total_rows)
print("Invalid user references:", invalid_count)    



# Load valid restaurant IDs
restaurants = pd.read_csv(
    "data/restaurant.csv",
    usecols=["id"]
)

valid_restaurant_ids = set(restaurants["id"])

invalid_count = 0
total_rows = 0

# Process orders in chunks
for chunk in pd.read_csv(
    "data/orders.csv",
    usecols=["r_id"],
    chunksize=500_000
):
    total_rows += len(chunk)

    invalid = ~chunk["r_id"].isin(valid_restaurant_ids)

    invalid_count += invalid.sum()

print("Total orders checked:", total_rows)
print("Invalid restaurant references:", invalid_count)




# --------------------------------------------------
# 1. Load valid Order IDs
# --------------------------------------------------

orders = pd.read_csv(
    "data/orders.csv",
    usecols=["order_id"]
)

valid_order_ids = set(orders["order_id"])


# --------------------------------------------------
# 2. Load valid Restaurant IDs
# --------------------------------------------------

restaurants = pd.read_csv(
    "data/restaurant.csv",
    usecols=["id"]
)

valid_restaurant_ids = set(restaurants["id"])


# --------------------------------------------------
# 3. Load valid Food IDs
# --------------------------------------------------

food = pd.read_csv(
    "data/food.csv",
    usecols=["f_id"]
)

valid_food_ids = set(food["f_id"])


# --------------------------------------------------
# Counters
# --------------------------------------------------

total_rows = 0
invalid_order_refs = 0
invalid_restaurant_refs = 0
invalid_food_refs = 0


# --------------------------------------------------
# 4. Process order_items in chunks
# --------------------------------------------------

for chunk in pd.read_csv(
    "data/order_items.csv",
    usecols=["order_id", "r_id", "f_id"],
    chunksize=500_000
):

    total_rows += len(chunk)

    invalid_orders = ~chunk["order_id"].isin(valid_order_ids)
    invalid_restaurants = ~chunk["r_id"].isin(valid_restaurant_ids)
    invalid_food = ~chunk["f_id"].isin(valid_food_ids)

    invalid_order_refs += invalid_orders.sum()
    invalid_restaurant_refs += invalid_restaurants.sum()
    invalid_food_refs += invalid_food.sum()


# --------------------------------------------------
# 5. Results
# --------------------------------------------------

print("Total order_items checked:", total_rows)

print(
    "Invalid order references:",
    invalid_order_refs
)

print(
    "Invalid restaurant references:",
    invalid_restaurant_refs
)

print(
    "Invalid food references:",
    invalid_food_refs
)







