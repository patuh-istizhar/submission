from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

# Data mappings
CITY_MAPPING = {
    "sao paulo": "São Paulo",
    "rio de janeiro": "Rio de Janeiro",
    "belo horizonte": "Belo Horizonte",
    "brasilia": "Brasília",
    "curitiba": "Curitiba",
}

STATE_MAPPING = {
    "AC": "Acre",
    "AL": "Alagoas",
    "AP": "Amapá",
    "AM": "Amazonas",
    "BA": "Bahia",
    "CE": "Ceará",
    "DF": "Distrito Federal",
    "ES": "Espírito Santo",
    "GO": "Goiás",
    "MA": "Maranhão",
    "MT": "Mato Grosso",
    "MS": "Mato Grosso do Sul",
    "MG": "Minas Gerais",
    "PA": "Pará",
    "PB": "Paraíba",
    "PR": "Paraná",
    "PE": "Pernambuco",
    "PI": "Piauí",
    "RJ": "Rio de Janeiro",
    "RN": "Rio Grande do Norte",
    "RS": "Rio Grande do Sul",
    "RO": "Rondônia",
    "RR": "Roraima",
    "SC": "Santa Catarina",
    "SP": "São Paulo",
    "SE": "Sergipe",
    "TO": "Tocantins",
}

# Merged duplicate categories
CATEGORY_MAPPING = {
    "office_furniture": "Office Furniture",
    "housewares": "Housewares",
    "home_confort": "Home Comfort",
    "home_comfort_2": "Home Comfort",
    "sports_leisure": "Sports & Leisure",
    "computers_accessories": "Computers & Accessories",
    "toys": "Toys",
    "furniture_decor": "Furniture & Decor",
    "auto": "Automotive",
    "air_conditioning": "Air Conditioning",
    "telephony": "Telephony",
    "health_beauty": "Health & Beauty",
    "garden_tools": "Garden Tools",
    "pet_shop": "Pet Shop",
    "bed_bath_table": "Bed, Bath & Table",
    "baby": "Baby Products",
    "watches_gifts": "Watches & Gifts",
    "kitchen_dining_laundry_garden_furniture": "Kitchen, Dining & Garden Furniture",
    "perfumery": "Perfumery",
    "art": "Art",
    "stationery": "Stationery",
    "fashio_female_clothing": "Women's Clothing",
    "consoles_games": "Consoles & Games",
    "construction_tools_lights": "Construction Tools & Lights",
    "food_drink": "Food & Drink",
    "drinks": "Beverages",
    "cool_stuff": "Cool Stuff",
    "fashion_bags_accessories": "Bags & Accessories",
    "home_construction": "Home Construction",
    "luggage_accessories": "Luggage & Accessories",
    "electronics": "Electronics",
    "home_appliances": "Home Appliances",
    "home_appliances_2": "Home Appliances",
    "fashion_male_clothing": "Men's Clothing",
    "small_appliances": "Small Appliances",
    "small_appliances_home_oven_and_coffee": "Oven & Coffee Appliances",
    "books_general_interest": "Books - General",
    "costruction_tools_tools": "Construction Tools",
    "signaling_and_security": "Signaling & Security",
    "musical_instruments": "Musical Instruments",
    "construction_tools_construction": "Construction Equipment",
    "music": "Music",
    "fashion_shoes": "Shoes",
    "industry_commerce_and_business": "Industry & Commerce",
    "fashion_underwear_beach": "Underwear & Beachwear",
    "dvds_blu_ray": "DVDs & Blu-ray",
    "construction_tools_safety": "Construction Safety",
    "food": "Food",
    "fixed_telephony": "Fixed Telephony",
    "furniture_living_room": "Living Room Furniture",
    "tablets_printing_image": "Tablets & Printing",
    "market_place": "Marketplace",
    "christmas_supplies": "Christmas Supplies",
    "agro_industry_and_commerce": "Agro Industry & Commerce",
    "costruction_tools_garden": "Garden Construction Tools",
    "computers": "Computers",
    "furniture_bedroom": "Bedroom Furniture",
    "audio": "Audio",
    "books_imported": "Imported Books",
    "books_technical": "Technical Books",
    "party_supplies": "Party Supplies",
    "furniture_mattress_and_upholstery": "Mattresses & Upholstery",
    "la_cuisine": "La Cuisine",
    "flowers": "Flowers",
    "diapers_and_hygiene": "Diapers & Hygiene",
    "cine_photo": "Cinema & Photography",
    "cds_dvds_musicals": "CDs, DVDs & Musicals",
    "fashion_sport": "Sportswear",
    "arts_and_craftmanship": "Arts & Craftsmanship",
    "fashion_childrens_clothes": "Children's Clothing",
    "security_and_services": "Security & Services",
}

PAYMENT_MAPPING = {
    "credit_card": "Credit Card",
    "boleto": "Boleto",
    "voucher": "Voucher",
    "debit_card": "Debit Card",
    "not_defined": "Not Defined",
}


def get_top_cities(df, n=5):
    if df.empty:
        return pd.DataFrame(columns=["City", "Number of Customers"])

    return (
        df.groupby("customer_city")["customer_unique_id"]
        .nunique()
        .nlargest(n)
        .reset_index()
        .assign(
            City=lambda x: x["customer_city"]
            .str.lower()
            .map(CITY_MAPPING)
            .fillna(x["customer_city"])
        )
        .drop(columns="customer_city")
        .rename(columns={"customer_unique_id": "Number of Customers"})
    )


def get_top_states(df, n=5):
    if df.empty:
        return pd.DataFrame(columns=["State", "Number of Customers"])

    return (
        df.groupby("customer_state")["customer_unique_id"]
        .nunique()
        .nlargest(n)
        .reset_index()
        .assign(
            State=lambda x: x["customer_state"]
            .map(STATE_MAPPING)
            .fillna(x["customer_state"])
        )
        .drop(columns="customer_state")
        .rename(columns={"customer_unique_id": "Number of Customers"})
    )


def get_top_categories_by_orders(df, n=5):
    if df.empty:
        return pd.DataFrame(columns=["Category", "Number of Orders"])

    return (
        df.groupby("product_category_name_english")["order_id"]
        .nunique()
        .nlargest(n)
        .reset_index()
        .assign(
            Category=lambda x: x["product_category_name_english"]
            .map(CATEGORY_MAPPING)
            .fillna(x["product_category_name_english"])
        )
        .drop(columns="product_category_name_english")
        .rename(columns={"order_id": "Number of Orders"})
    )


def get_top_categories_by_revenue(df, n=5):
    if df.empty:
        return pd.DataFrame(columns=["Category", "Total Revenue"])

    return (
        df.groupby("product_category_name_english")["price"]
        .sum()
        .nlargest(n)
        .reset_index()
        .assign(
            Category=lambda x: x["product_category_name_english"]
            .map(CATEGORY_MAPPING)
            .fillna(x["product_category_name_english"])
        )
        .drop(columns="product_category_name_english")
        .rename(columns={"price": "Total Revenue"})
    )


def get_payment_counts(df, n=5):
    if df.empty:
        return pd.DataFrame(columns=["Payment", "Count"])

    return (
        df["payment_type"]
        .value_counts()
        .nlargest(n)
        .reset_index()
        .assign(
            Payment=lambda x: x["payment_type"]
            .map(PAYMENT_MAPPING)
            .fillna(x["payment_type"])
        )
        .drop(columns="payment_type")
        .rename(columns={"count": "Count"})
    )


def get_payment_revenue(df, n=5):
    if df.empty:
        return pd.DataFrame(columns=["Payment", "Total Revenue"])

    return (
        df.groupby("payment_type")["payment_value"]
        .sum()
        .nlargest(n)
        .reset_index()
        .assign(
            Payment=lambda x: x["payment_type"]
            .map(PAYMENT_MAPPING)
            .fillna(x["payment_type"])
        )
        .drop(columns="payment_type")
        .rename(columns={"payment_value": "Total Revenue"})
    )


def calculate_rfm(df):
    if df.empty:
        return pd.DataFrame(
            columns=[
                "Recency",
                "Frequency",
                "Monetary",
                "R_Score",
                "F_Score",
                "M_Score",
                "RFM_Segment",
                "RFM_Score",
                "Customer_Segment",
            ]
        )

    df["order_purchase_timestamp"] = pd.to_datetime(
        df["order_purchase_timestamp"], errors="coerce"
    )

    valid_df = df.dropna(subset=["order_purchase_timestamp", "customer_unique_id"])

    if valid_df.empty:
        return pd.DataFrame(
            columns=[
                "Recency",
                "Frequency",
                "Monetary",
                "R_Score",
                "F_Score",
                "M_Score",
                "RFM_Segment",
                "RFM_Score",
                "Customer_Segment",
            ]
        )

    ref_date = valid_df["order_purchase_timestamp"].dt.date.max()

    rfm = (
        valid_df.groupby("customer_unique_id")
        .agg(
            {
                "order_purchase_timestamp": lambda x: (ref_date - x.max().date()).days,
                "order_id": "nunique",
                "payment_value": "sum",
            }
        )
        .rename(
            columns={
                "order_purchase_timestamp": "Recency",
                "order_id": "Frequency",
                "payment_value": "Monetary",
            }
        )
    )

    for col, labels in [
        ("Recency", [5, 4, 3, 2, 1]),  # Higher score for lower recency
        ("Frequency", [1, 2, 3, 4, 5]),  # Higher score for higher frequency
        ("Monetary", [1, 2, 3, 4, 5]),  # Higher score for higher monetary value
    ]:
        try:
            if col == "Recency":
                # For recency, lower is better
                rfm[f"{col[0]}_Score"] = pd.qcut(
                    rfm[col], q=5, labels=labels, duplicates="drop"
                )
            else:
                # For frequency and monetary, higher is better
                # Use rank for frequency to handle potential duplicates
                column_data = (
                    rfm[col] if col != "Frequency" else rfm[col].rank(method="first")
                )

                # Check if we have at least 5 unique values for qcut
                if len(column_data.unique()) >= 5:
                    rfm[f"{col[0]}_Score"] = pd.qcut(
                        column_data, q=5, labels=labels, duplicates="drop"
                    )
                else:
                    # Use quantile-based manual binning for fewer unique values
                    percentiles = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
                    bins = [column_data.quantile(p) for p in percentiles]
                    # Ensure bins are unique
                    bins = sorted(set(bins))
                    # If still not enough bins, fall back to equal bins
                    if len(bins) < 3:
                        bins = [
                            column_data.min(),
                            column_data.median(),
                            column_data.max(),
                        ]

                    if len(bins) >= 2:  # Need at least 2 bins
                        rfm[f"{col[0]}_Score"] = pd.cut(
                            column_data,
                            bins=bins,
                            labels=labels[: len(bins) - 1],
                            include_lowest=True,
                        )
                    else:
                        rfm[f"{col[0]}_Score"] = 3  # Neutral middle score if can't bin
        except ValueError:
            # Fallback to manual scoring if qcut fails
            rfm[f"{col[0]}_Score"] = 3  # Assign neutral score as fallback

    # Ensure all scores are integers for calculation
    for score_col in ["R_Score", "F_Score", "M_Score"]:
        if rfm[score_col].dtype != "int64":
            rfm[score_col] = rfm[score_col].astype("int64")

    rfm["RFM_Segment"] = (
        rfm[["R_Score", "F_Score", "M_Score"]].astype(str).agg("".join, axis=1)
    )
    rfm["RFM_Score"] = rfm[["R_Score", "F_Score", "M_Score"]].sum(axis=1)

    rfm["Customer_Segment"] = pd.cut(
        rfm["RFM_Score"],
        bins=[-1, 5, 8, 11, float("inf")],
        labels=["Lost Customer", "At Risk", "Potential Loyalist", "Loyal Customer"],
    )
    return rfm


# Plotting function
def create_bar_plot(data, x, y, title, rotate_x=False):
    """Create bar plot visualization with consistent styling."""
    if data.empty:
        # Return empty figure if no data
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.text(0.5, 0.5, "No data available", ha="center", va="center")
        ax.set(title=title)
        return fig

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=data, x=x, y=y, ax=ax)
    ax.set(xlabel=None, ylabel=None, title=title)
    if rotate_x:
        plt.xticks(rotation=45)
    plt.tight_layout()
    return fig


# Preprocess datetime columns consistently
def preprocess_dataframe(df):
    """Process datetime columns consistently."""
    if df.empty:
        return df

    # Convert all timestamp columns to datetime
    datetime_columns = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]

    for col in datetime_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    return df


# Main app
def main():
    st.set_page_config(
        page_title="E-Commerce Dashboard",
        page_icon="📊",
        layout="wide",
    )

    # Load data
    try:
        data_path = Path("./dashboard/main_data.csv")
        df = pd.read_csv(data_path)
        df = preprocess_dataframe(df)  # Process all datetime columns consistently
    except FileNotFoundError:
        st.error(f"Data file not found at {data_path}. Please check the file path.")
        return
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return

    # Sidebar
    with st.sidebar:
        st.image(
            "https://upload.wikimedia.org/wikipedia/commons/7/77/Streamlit-logo-primary-colormark-darktext.png"
        )

        # Determine date range based on available data
        date_column = "order_purchase_timestamp"  # Use this column consistently

        if df[date_column].notna().any():
            min_date, max_date = (
                df[date_column].min().date(),
                df[date_column].max().date(),
            )
            start_date, end_date = st.date_input(
                "Time Span",
                min_value=min_date,
                max_value=max_date,
                value=(min_date, max_date),
            )

            if isinstance(start_date, tuple) and len(start_date) == 2:
                # Handle case when streamlit returns a tuple instead of individual dates
                start_date, end_date = start_date

            mask = df[date_column].dt.date.between(start_date, end_date)
            filtered_df = df.loc[mask]
        else:
            st.error(f"No valid dates found in {date_column} column.")
            filtered_df = pd.DataFrame()

        st.write(f"Filtered data: {len(filtered_df)} records")

    # Check if filtered data is empty
    if filtered_df.empty:
        st.warning(
            "No data available for the selected date range. Please adjust your filters."
        )
        return

    # Data preparation
    top_cities = get_top_cities(filtered_df)
    top_states = get_top_states(filtered_df)
    top_categories_orders = get_top_categories_by_orders(filtered_df)
    top_categories_revenue = get_top_categories_by_revenue(filtered_df)
    payment_counts = get_payment_counts(filtered_df)
    payment_revenue = get_payment_revenue(filtered_df)
    rfm_data = calculate_rfm(filtered_df)

    # Dashboard
    st.title("E-Commerce Public Dataset :star:")

    # Locations
    st.header("Top Locations by Customer Count")
    location_tabs = st.tabs(["Cities", "States"])

    with location_tabs[0]:
        if not top_cities.empty:
            st.pyplot(
                create_bar_plot(
                    top_cities,
                    "Number of Customers",
                    "City",
                    "Top 5 Cities by Customer Count",
                )
            )
        else:
            st.info("No city data available for the selected period.")

    with location_tabs[1]:
        if not top_states.empty:
            st.pyplot(
                create_bar_plot(
                    top_states,
                    "Number of Customers",
                    "State",
                    "Top 5 States by Customer Count",
                )
            )
        else:
            st.info("No state data available for the selected period.")

    # Products
    st.header("Top Products by Orders and Revenue")
    product_tabs = st.tabs(["Orders", "Revenue"])

    with product_tabs[0]:
        if not top_categories_orders.empty:
            st.pyplot(
                create_bar_plot(
                    top_categories_orders,
                    "Number of Orders",
                    "Category",
                    "Top 5 Product Categories by Orders",
                )
            )
        else:
            st.info("No product order data available for the selected period.")

    with product_tabs[1]:
        if not top_categories_revenue.empty:
            st.pyplot(
                create_bar_plot(
                    top_categories_revenue,
                    "Total Revenue",
                    "Category",
                    "Top 5 Product Categories by Revenue",
                )
            )
        else:
            st.info("No product revenue data available for the selected period.")

    # Payments
    st.header("Payment Methods Analysis")
    payment_tabs = st.tabs(["Usage", "Revenue"])

    with payment_tabs[0]:
        if not payment_counts.empty:
            st.pyplot(
                create_bar_plot(
                    payment_counts,
                    "Payment",
                    "Count",
                    "Top 5 Payment Methods by Usage",
                    rotate_x=True,
                )
            )
        else:
            st.info("No payment usage data available for the selected period.")

    with payment_tabs[1]:
        if not payment_revenue.empty:
            st.pyplot(
                create_bar_plot(
                    payment_revenue,
                    "Payment",
                    "Total Revenue",
                    "Top 5 Payment Methods by Revenue",
                    rotate_x=True,
                )
            )
        else:
            st.info("No payment revenue data available for the selected period.")

    # RFM Analysis
    if not rfm_data.empty:
        st.header("RFM Distribution")
        fig, axes = plt.subplots(1, 3, figsize=(18, 5))
        for ax, col, color, title, xlabel in [
            (
                axes[0],
                "Recency",
                "blue",
                "Recency Distribution",
                "Days Since Last Transaction",
            ),
            (
                axes[1],
                "Frequency",
                "green",
                "Frequency Distribution",
                "Number of Unique Transactions",
            ),
            (axes[2], "Monetary", "red", "Monetary Distribution", "Total Payment (R$)"),
        ]:
            sns.histplot(rfm_data[col], bins=20, kde=True, ax=ax, color=color)
            ax.set(title=title, xlabel=xlabel)
        plt.tight_layout()
        st.pyplot(fig)

        st.header("Customer Segments by RFM Score")
        segments_order = [
            "Loyal Customer",
            "Potential Loyalist",
            "At Risk",
            "Lost Customer",
        ]
        rfm_data["Customer_Segment"] = pd.Categorical(
            rfm_data["Customer_Segment"], categories=segments_order, ordered=True
        )

        fig, ax = plt.subplots(figsize=(8, 5))
        sns.countplot(data=rfm_data, x="Customer_Segment", order=segments_order, ax=ax)
        for p in ax.patches:
            ax.annotate(
                f"{int(p.get_height())}",
                (p.get_x() + p.get_width() / 2.0, p.get_height()),
                ha="center",
                va="baseline",
                xytext=(0, 5),
                textcoords="offset points",
            )
        ax.set(title="Customer Count per RFM Segment", xlabel=None, ylabel=None)
        plt.tight_layout()
        st.pyplot(fig)
    else:
        st.info("Insufficient data to perform RFM analysis for the selected period.")

    # Show a sample of the filtered data
    with st.expander("View Sample Data"):
        st.dataframe(filtered_df.head(10))

    st.caption("Copyright (c) Patuh Rujhan Al Istizhar 2025")


if __name__ == "__main__":
    main()
