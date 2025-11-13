import pandas as pd

# Create sample data
employee_data = pd.DataFrame({
    "Employee ID": ["E101", "E102", "E103", "E104", "E105"],
    "Employee Name": ["John Smith", "Priya Patel", "Arjun Rao", "Emma Brown", "David Lee"],
    "Department": ["HR", "Finance", "IT", "Marketing", "HR"],
    "Salary": [55000, 56000, 68000, 60000, 53000],
    "Location": ["New York", "Chicago", "Dallas", "San Francisco", "Boston"],
    "Bonus %": [6, 7, 8, 5, 6],
    "Bonus Amount": [3300, 3920, 5440, 3000, 3180],
    "Region Category": ["East", "Central", "South", "West", "East"]
})

sales_data = pd.DataFrame({
    "Product": ["Laptop", "Chair", "Headphones", "Sofa", "Monitor"],
    "Category": ["Electronics", "Furniture", "Electronics", "Furniture", "Electronics"],
    "Units Sold": [45, 150, 80, 30, 50],
    "Price": [900, 70, 120, 800, 250],
    "Month": ["Jan", "Jan", "Feb", "Mar", "Apr"],
    "Region": ["East", "West", "Central", "South", "East"]
})

feedback_data = pd.DataFrame({
    "Feedback ID": ["F001", "F002", "F003", "F004", "F005"],
    "Feedback Text": [
        "The laptop battery drains too fast.",
        "Chair is comfortable and easy to assemble.",
        "Sound quality is amazing, but the cable is short.",
        "Sofa is stylish but expensive.",
        "Monitor display is crisp and clear."
    ],
    "Product": ["Laptop", "Chair", "Headphones", "Sofa", "Monitor"],
    "Rating": [3, 5, 4, 4, 5]
})

# Save to Excel file
with pd.ExcelWriter("NumerousAI_Practice.xlsx", engine='openpyxl') as writer:
    employee_data.to_excel(writer, sheet_name="Employee Data", index=False)
    sales_data.to_excel(writer, sheet_name="Sales Data", index=False)
    feedback_data.to_excel(writer, sheet_name="Product Feedback", index=False)

print("✅ NumerousAI_Practice.xlsx file created successfully!")

