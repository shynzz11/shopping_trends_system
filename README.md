

## Dataset Overview
This dataset is used for analyzing shopping trends and generating personalized insights for business owners. It provides detailed information about sales data and various metrics needed to produce verified insights like "Verified by TrendLens" badges.

---

## Columns Description

### 1. **Transaction_ID**
- **Description**: Unique identifier for each transaction.
- **Type**: String
- **Example**: `TXN12345`

### 2. **Date**
- **Description**: Date of the transaction.
- **Type**: Date
- **Format**: `YYYY-MM-DD`
- **Example**: `2025-01-28`

### 3. **Product_Name**
- **Description**: Name of the product sold.
- **Type**: String
- **Example**: `T-shirt`, `Smartphone`

### 4. **Category**
- **Description**: Category of the product.
- **Type**: String
- **Example**: `Clothing`, `Electronics`

### 5. **Units_Sold**
- **Description**: Number of units sold for the product.
- **Type**: Integer
- **Example**: `50`

### 6. **Revenue**
- **Description**: Total revenue generated from the product sales.
- **Type**: Float
- **Format**: In the local currency (e.g., USD).
- **Example**: `500.75`

### 7. **Cost**
- **Description**: Total cost incurred for the product sales.
- **Type**: Float
- **Format**: In the local currency (e.g., USD).
- **Example**: `300.50`

### 8. **Profit**
- **Description**: Total profit calculated as `Revenue - Cost`.
- **Type**: Float
- **Example**: `200.25`

### 9. **Customer_Age**
- **Description**: Age of the customer.
- **Type**: Integer
- **Example**: `25`

### 10. **Customer_Gender**
- **Description**: Gender of the customer.
- **Type**: String
- **Values**: `Male`, `Female`, `Other`
- **Example**: `Female`

### 11. **Customer_Region**
- **Description**: Geographic region of the customer.
- **Type**: String
- **Example**: `North America`, `Europe`

### 12. **Payment_Method**
- **Description**: Payment method used for the transaction.
- **Type**: String
- **Example**: `Credit Card`, `PayPal`

### 13. **Store_ID**
- **Description**: Unique identifier for the store where the transaction occurred.
- **Type**: String
- **Example**: `ST123`

### 14. **Store_Location**
- **Description**: Location of the store.
- **Type**: String
- **Example**: `New York`, `London`

### 15. **Discount_Offered**
- **Description**: Discount applied to the transaction.
- **Type**: Float
- **Example**: `10.5` (indicates 10.5% discount)

### 16. **Return_Status**
- **Description**: Indicates whether the product was returned.
- **Type**: String
- **Values**: `Yes`, `No`
- **Example**: `No`

### 17. **Customer_Feedback**
- **Description**: Feedback provided by the customer.
- **Type**: String
- **Example**: `Satisfied with the product quality.`

---

## Usage Notes
- **Units_Sold** and **Revenue** columns are essential for generating sales insights.
- **Category** and **Customer_Region** can be used for trend analysis.
- **Profit** can highlight the most profitable products for a business.
- **Discount_Offered** and **Return_Status** help identify potential sales strategies and product issues.

---

## Acknowledgements
- This dataset was designed as part of the TrendLens project to provide personalized insights and verified badges for business owners.

## Contact
For questions or support, please contact [support@trendlens.com](mailto:support@trendlens.com).
