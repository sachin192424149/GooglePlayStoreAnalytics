import pandas as pd


def load_apps():
    """
    Load the original Google Play Store dataset.
    """
    apps = pd.read_csv("data/googleplaystore.csv")
    return apps


def clean_reviews(apps):
    """
    Convert Reviews column to numeric.
    """
    apps["Reviews"] = pd.to_numeric(apps["Reviews"], errors="coerce")
    return apps

def clean_size(apps):
    """
    Convert Size column into MB.
    """
    apps["Size"] = apps["Size"].replace("Varies with device", pd.NA)

    apps["Size"] = apps["Size"].str.replace("M", "", regex=False)
    apps["Size"] = apps["Size"].str.replace("k", "", regex=False)

    apps["Size"] = pd.to_numeric(apps["Size"], errors="coerce")

    return apps

def clean_price(apps):
    """
    Convert Price column into numeric values.
    """

    apps["Price"] = apps["Price"].str.replace("$", "", regex=False)

    apps["Price"] = pd.to_numeric(apps["Price"], errors="coerce")

    return apps

def clean_last_updated(apps):
    """
    Convert Last Updated column to datetime.
    """

    apps["Last Updated"] = pd.to_datetime(
        apps["Last Updated"],
        errors="coerce"
    )

    return apps

def clean_android_version(apps):
    """
    Clean Android Version column.
    """

    apps["Android Ver"] = (
        apps["Android Ver"]
        .astype(str)
        .str.replace("and up", "", regex=False)
        .str.strip()
    )

    return apps

def save_clean_data(apps):
    """
    Save the final cleaned dataset.
    """

    apps.to_csv(
        "cleaned_data/googleplaystore_final.csv",
        index=False
    )

    print("\nFinal cleaned dataset saved successfully!")

def load_reviews():
    """
    Load Google Play Store User Reviews dataset.
    """
    reviews = pd.read_csv(
        "data/googleplaystore_user_reviews.csv"
    )

    return reviews

def merge_datasets(apps, reviews):
    """
    Merge apps dataset with reviews dataset.
    """

    merged = pd.merge(
        apps,
        reviews,
        on="App",
        how="left"
    )

    return merged
def load_merged_data():
    """
    Load the final merged dataset.
    """
    merged = pd.read_csv(
        "cleaned_data/googleplaystore_merged.csv"
    )

    return merged