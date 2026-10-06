import pandas as pd

def dataset_summary(apps):
    """
    Display basic dataset information.
    """

    print("=" * 60)
    print("DATASET SUMMARY")
    print("=" * 60)

    print("\nRows :", apps.shape[0])
    print("Columns :", apps.shape[1])

    print("\nColumn Names:")
    print(apps.columns.tolist())

    print("\nMissing Values:")
    print(apps.isnull().sum())

def category_summary(apps):
    """
    Number of apps in each category.
    """

    print("\n" + "=" * 60)
    print("CATEGORY SUMMARY")
    print("=" * 60)

    print(apps["Category"].value_counts())


def rating_summary(apps):
    """
    Average rating for every category.
    """

    print("\n" + "=" * 60)
    print("AVERAGE RATING BY CATEGORY")
    print("=" * 60)

    ratings = (
        apps.groupby("Category")["Rating"]
        .mean()
        .sort_values(ascending=False)
    )

    print(ratings)


def installs_summary(apps):
    """
    Total installs by category.
    """

    print("\n" + "=" * 60)
    print("TOTAL INSTALLS BY CATEGORY")
    print("=" * 60)

    installs = (
        apps.groupby("Category")["Installs"]
        .sum()
        .sort_values(ascending=False)
    )

    print(installs)


def reviews_summary(apps):
    """
    Total reviews by category.
    """

    print("\n" + "=" * 60)
    print("TOTAL REVIEWS BY CATEGORY")
    print("=" * 60)

    reviews = (
        apps.groupby("Category")["Reviews"]
        .sum()
        .sort_values(ascending=False)
    )

    print(reviews)


def top_categories(apps):
    """
    Top 10 categories by installs.
    """

    print("\n" + "=" * 60)
    print("TOP 10 CATEGORIES")
    print("=" * 60)

    top = (
        apps.groupby("Category")["Installs"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    print(top)