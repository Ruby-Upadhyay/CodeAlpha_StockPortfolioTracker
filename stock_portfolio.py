from datetime import datetime

# Store the available stocks and their prices
stock_prices = {
    "AAPL": 150,
    "TSLA": 120,
    "MSFT": 300,
    "AMZN": 250,
    "GOOGL": 400
}

# Store stocks owned by the user
portfolio = {}

# Save the current portfolio to a file
def save_portfolio():
    with open("portfolio.txt", "w", encoding="utf-8") as file:
        for stock, quantity in portfolio.items():
            file.write(f"{stock} : {quantity} shares\n")

# Save buy, sell, and remove transactions with date, time, price, and total value
def save_transaction(action, quantity, stock):
    current_time = datetime.now().strftime("%d-%m-%y %H:%M:%S")
    price = stock_prices[stock]
    total_value = quantity * price

    with open("transactions.txt", "a", encoding="utf-8") as file:
        if quantity == 1:
            file.write(f"{current_time} - {action} {quantity} share of {stock}"
                       f" at ₹{price} each = ₹{total_value}\n")
        else:
            file.write(f"{current_time} - {action} {quantity} shares of {stock}"
                       f" at ₹{price} each = ₹{total_value}\n")

# Load previously saved portfolio data when the program starts
def load_portfolio():
    try:
        with open("portfolio.txt", "r", encoding="utf-8") as file:

            for line in file:
                try:
                    stock, quantity = line.strip().split(" : ")
                    quantity = int(quantity.replace(" shares", ""))
                    portfolio[stock] = quantity
                except ValueError:
                    print("Invalid line found. Skipping it.")
                    continue

    except FileNotFoundError:
        pass

# Display all available stocks and their prices
def show_stocks():
    print("-----AVAILABLE STOCKS-----")

    for stock, price in stock_prices.items():
        print(f"{stock} - ₹{price}")

# Add shares to the user's portfolio
def add_stock():
    stock = input("Enter stock name: ").upper()

    if stock in stock_prices:
        print("Stock found")
        try:
            quantity = int(input("Enter quantity: "))

            if quantity <= 0:
                print("Quantity should be greater than 0")
                return

        except ValueError:
            print("Invalid quantity")
            return

        if stock in portfolio:
            portfolio[stock] += quantity

        else:
            portfolio[stock] = quantity

        price = stock_prices[stock]
        investment = quantity * price
        print("Investment value: ₹", investment)
        print("Stock added successfully")
        save_portfolio()
        save_transaction("Bought", quantity, stock)

    else:
        print("Stock not found")

# Display the current portfolio and total investment
def view_portfolio():

    if not portfolio:
        print("Your portfolio is empty")
        return

    print("----PORTFOLIO SUMMARY----")
    total_investment = 0

    for stock, quantity in portfolio.items():
        investment = quantity * stock_prices[stock]
        total_investment += investment
        print(f"{stock} : {quantity} shares x ₹{stock_prices[stock]} = ₹{investment}")
    print("Total portfolio value: ₹", total_investment)

# Calculate and display portfolio statistics
def portfolio_statistics():

    if not portfolio:
        print("Your portfolio is empty")
        return

    total_shares = sum(portfolio.values())
    total_investment = 0
    highest_stock = None
    lowest_stock = None
    highest_value = 0
    lowest_value = None

    for stock, quantity in portfolio.items():
        investment = quantity * stock_prices[stock]
        total_investment += investment

        if investment > highest_value:
            highest_value = investment
            highest_stock = stock

        if lowest_value is None or investment < lowest_value:
            lowest_value = investment
            lowest_stock = stock

    print("-----PORTFOLIO STATISTICS-----")
    print("Total different stocks:", len(portfolio))
    print("Total shares:", total_shares)
    print("Total investment: ₹", total_investment)
    print("Highest investment:", highest_stock, "- ₹", highest_value)
    print("Lowest investment:", lowest_stock, "- ₹", lowest_value)

# Remove all shares of a selected stock
def remove_stock():
    stock = input("Enter stock you want to remove: ").upper()

    if stock in portfolio:
        confirmation = input(f"Are you sure you want to remove {stock}? (yes/no): ").lower()

        if confirmation == "yes":
            save_transaction("Removed", portfolio[stock], stock)
            del portfolio[stock]
            save_portfolio()
            print("Stock removed successfully")
        else:
            print("Stock removal cancelled")

    else:
        print("Stock not found in your portfolio")

# Sell a selected number of shares
def sell_shares():
    new_stock = input("Enter the stock whose shares you want to sell: ").upper()

    if new_stock in portfolio:
        try:
            new_quantity = int(input("Enter the number of shares you want to sell: "))
        except ValueError:
            print("Invalid quantity")
            return

        if 0 < new_quantity <= portfolio[new_stock]:
            portfolio[new_stock] -= new_quantity

            if portfolio[new_stock] == 0:
                del portfolio[new_stock]
            save_portfolio()
            save_transaction("Sold", new_quantity, new_stock)
            print("Shares sold successfully")

        else:
            if new_quantity <= 0:
                print("Quantity should be greater than zero")
            else:
                print("You don't have enough shares")

    else:
        print("Stock not found in portfolio")

# Display the complete transaction history
def view_transactions():
    try:
        with open("transactions.txt", "r", encoding="utf-8") as file:
            print("-----TRANSACTION HISTORY-----")
            for line in file:
                print(line.strip())
    except FileNotFoundError:
        print("No transaction history found")

# Main menu loop
load_portfolio()
while True:
    print("\n====STOCK PORTFOLIO TRACKER====")
    print("1. Available stocks")
    print("2. Add stock")
    print("3. View Portfolio")
    print("4. Remove stock")
    print("5. Sell Shares")
    print("6. Transaction History")
    print("7. Portfolio Statistics")
    print("8. Exit")
    menu_choice=input("Enter your choice: ")

    if menu_choice == "1":
        show_stocks()

    elif menu_choice == "2":
        add_stock()

    elif menu_choice == "3":
        view_portfolio()

    elif menu_choice == "4":
        remove_stock()

    elif menu_choice == "5":
        sell_shares()

    elif menu_choice == "6":
        view_transactions()

    elif menu_choice == "7":
        portfolio_statistics()

    elif menu_choice == "8":
        print("Thank you for using the Stock Portfolio Tracker!")
        save_portfolio()
        break

    else:
        print("Invalid choice. Please enter 1, 2, 3, 4, 5, 6, 7 or 8.")




