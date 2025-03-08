import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import datetime as dt
from cycler import cycler
from pathlib import Path

# Theme configuration
monoblue_theme = {
    "axes.spines.top": False,
    "axes.spines.right": False,
    "xtick.minor.visible": False,
    "xtick.major.size": 5,
    "ytick.major.size": 5,
    "ytick.minor.visible": False,
    "yaxis.labellocation": "top",
    "xaxis.labellocation": "right",
    "scatter.marker": "o",
    "lines.linewidth": 2.0,
    "axes.labelsize": 12,
    "axes.linewidth": 1.0,
    "text.color": "#002060",
    "axes.facecolor": "#EBF5FF",
    "figure.facecolor": "#EBF5FF",
    "axes.labelcolor": "#002060",
    "axes.edgecolor": "#002060",
    "xtick.color": "#002060",
    "ytick.color": "#002060",
    "axes.prop_cycle": cycler(
        "color", ["#002060", "#4682B4", "#ADD8E6", "#B0C4DE", "#778899"]
    ),
}
plt.rcParams.update(monoblue_theme)

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

CATEGORY_MAPPING = {
    "office_furniture": "Office Furniture",
    "housewares": "Housewares",
    "home_confort": "Home Comfort",
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
    "home_appliances_2": "Home Appliances",
    "fashion_male_clothing": "Men's Clothing",
    "small_appliances": "Small Appliances",
    "small_appliances_home_oven_and_coffee": "Oven & Coffee Appliances",
    "books_general_interest": "Books - General",
    "home_appliances": "Home Appliances",
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
    "home_comfort_2": "Home Comfort",
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


# Helper functions
def get_top_cities(df, n=5):
    return (
        df.groupby("customer_city")["customer_id"]
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
        .rename(columns={"customer_id": "Number of Customers"})
    )


def get_top_states(df, n=5):
    return (
        df.groupby("customer_state")["customer_id"]
        .nunique()
        .nlargest(n)
        .reset_index()
        .assign(
            State=lambda x: x["customer_state"]
            .map(STATE_MAPPING)
            .fillna(x["customer_state"])
        )
        .drop(columns="customer_state")
        .rename(columns={"customer_id": "Number of Customers"})
    )


def get_top_categories_by_orders(df, n=5):
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
    df["order_purchase_timestamp"] = pd.to_datetime(
        df["order_purchase_timestamp"], errors="coerce"
    )

    valid_df = df.dropna(subset=["order_purchase_timestamp"])

    if valid_df.empty:
        # Return an empty DataFrame with the expected structure if no valid data
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
        ("Recency", [5, 4, 3, 2, 1]),
        ("Frequency", [1, 2, 3, 4, 5]),
        ("Monetary", [1, 2, 3, 4, 5]),
    ]:
        try:
            rfm[f"{col[0]}_Score"] = pd.qcut(
                rfm[col] if col != "Frequency" else rfm[col].rank(method="first"),
                q=5,
                labels=labels,
                duplicates="drop",
            )
        except ValueError:
            # Handle case when there are not enough unique values for qcut
            rfm[f"{col[0]}_Score"] = 1

    rfm["RFM_Segment"] = (
        rfm[["R_Score", "F_Score", "M_Score"]].astype(str).agg("".join, axis=1)
    )
    rfm["RFM_Score"] = rfm[["R_Score", "F_Score", "M_Score"]].astype(int).sum(axis=1)
    rfm["Customer_Segment"] = pd.cut(
        rfm["RFM_Score"],
        bins=[-1, 5, 8, 11, float("inf")],
        labels=["Lost Customer", "At Risk", "Potential Loyalist", "Loyal Customer"],
    )
    return rfm


# Plotting function
def create_bar_plot(data, x, y, title, rotate_x=False):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=data, x=x, y=y, ax=ax)
    ax.set(xlabel=None, ylabel=None, title=title)
    if rotate_x:
        plt.xticks(rotation=45)
    plt.tight_layout()
    return fig


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
        df["order_approved_at"] = pd.to_datetime(df["order_approved_at"])
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
        min_date, max_date = (
            df["order_approved_at"].min().date(),
            df["order_approved_at"].max().date(),
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

        mask = df["order_approved_at"].dt.date.between(start_date, end_date)
        filtered_df = df.loc[mask]

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
