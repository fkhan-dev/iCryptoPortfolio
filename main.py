import requests
import json
from tkinter import *
from tkinter import messagebox , Menu
import sqlite3

# Adding tkinter class and basic settings for GUI
# Adding demo python App

pycrypto = Tk()
pycrypto.title("iCrypto Portfolio")
#pycrypto.iconbitmap('icon.ico')

con = sqlite3.connect('cryptoCurrency.db')
cObj =  con.cursor()
cObj.execute("CREATE TABLE IF NOT EXISTS coin_detail(id INTEGER PRIMARY KEY, symbol TEXT, quantity INTEGER, price REAL)")

def reset():
    for cell in pycrypto.winfo_children():  # it caputred all cells on the GUI window
        cell.destroy()

    app_nav()
    app_header()
    my_portfolio()

def app_nav ():

    def close_app ():
        pycrypto.destroy()

    menu = Menu(pycrypto)
    file_item = Menu(menu)
    file_item.add_command(label='Clear Portfolio',)
    file_item.add_command(label='Clos App',command=close_app)
    menu.add_cascade(label='File',menu=file_item)
    pycrypto.config(menu=menu)

def my_portfolio():
    # Passing URL to the variable
    api_request = requests.get(
        "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?start=1&limit=50&convert=USD&CMC_PRO_API_KEY")

    api = json.loads(api_request.content)  # capturing contents in api variable

    # coins = [
    #             {
    #             "symbol":"BTC",
    #             "quantity":2,
    #             "purchase_price":56000
    #              },
    #             {
    #             "symbol":"SOL",
    #             "quantity":10,
    #             "purchase_price":1500
    #             },
    #             {
    #             "symbol": "ETH",
    #             "quantity": 10,
    #             "purchase_price": 4000
    #             },
    #             {
    #             "symbol": "XRP",
    #             "quantity": 10000,
    #             "purchase_price": 0.5
    #             }
    #          ]
    #
    def insert_val ():
       # cObj.execute("INSERT INTO coin_detail values (?,?,?,?)", (id, symbol, quantity, price))
        cObj.execute("INSERT INTO COIN_DETAIL (symbol,quantity,price) VALUES (?,?,?)", (symbol_txt.get(), quantity_txt.get(), price_txt.get()))
        con.commit()
        messagebox.showinfo("Portfolio Notification","Coin added successfully")
        reset() # it will refresh the screen after adding value

    def update_val ():
        cObj.execute("UPDATE COIN_DETAIL SET symbol = ?, quantity = ? , price = ? WHERE id = ?",(symbol_update.get(), quantity_update.get(), price_update.get(), pfolio_update.get() ))
        con.commit()
        messagebox.showinfo("Portfolio Notification", "Coin Updated successfully")
        reset()

    def del_val ():
        cObj.execute("DELETE FROM COIN_DETAIL WHERE id = ?",(pfolio_del.get(),))
        con.commit()
        messagebox.showinfo("Portfolio Notification", "Coin deleted successfully")
        reset()

    cObj.execute("select * from coin_detail")
    coins = cObj.fetchall()


    def font_color(amount):
        if amount > 0:
            return "green"
        else:
            return "red"

    net_all = 0  # Declare variable for counting total value for all coins
    coin_row = 1 # declared variabel
    coin_total_purchase = 0
    coin_numbers = 0

    for i in range(0,50):
        for coin in coins:
            if api["data"][i]["symbol"] == coin[1]:
                total_purchase = coin[3] * coin[2]
                total_value = api["data"][i]["quote"]["USD"]["price"] * coin[2]
                net = total_value - total_purchase
                net_coin = api["data"][i]["quote"]["USD"]["price"] - coin[3]
                net_all += net
                coin_total_purchase += total_purchase
                coin_numbers += coin[2]

                # print (api["data"][i]["name"] + "--" + api["data"][i]["symbol"])
                # print ("Current Price : {0:.2f}".format(api["data"][i]["quote"]["USD"]["price"])) #Example of fetching price in USD
                # print ("Total Purchase Amount: ",total_purchase)
                # print ("Coin Purchase: ",coin[2])
                # print ("Current Value: {0:.2f}".format(total_value))
                # print ("Net Position: {0:.2f}".format(net))
                # print ("Per Coin P/L: {0:.2f}".format(net_coin))
                # print ("-------------------------------")

                pfolioid = Label(pycrypto, text=coin[0], bg="#F3F4F6", fg="black", font="Lato 12 ", padx="2", pady="2", borderwidth=2, relief="groove")
                pfolioid.grid(row=coin_row, column=0, sticky=N + E + W + S)

                name = Label(pycrypto, text=api["data"][i]["symbol"], bg="#F3F4F6", fg="black", font="Lato 12 ", padx="2", pady="2", borderwidth=2, relief="groove")
                name.grid(row=coin_row, column=1, sticky=N + E + W + S)

                no_coins = Label(pycrypto, text=coin[2], bg="#F3F4F6", fg="black", font="Lato 12 ", padx="2", pady="2", borderwidth=2, relief="groove")
                no_coins.grid(row=coin_row, column=2, sticky=N + E + W + S)

                amount_paid = Label(pycrypto, text="{0:.2f}".format(total_purchase), bg="#F3F4F6", fg="black", font="Lato 12 ", padx="2", pady="2", borderwidth=2, relief="groove")
                amount_paid.grid(row=coin_row, column=3, sticky=N + E + W + S)

                current_price = Label(pycrypto, text="{0:.2f}".format(api["data"][i]["quote"]["USD"]["price"]), bg="grey",fg="black", font="Lato 12 ", padx="2", pady="2", borderwidth=2, relief="groove")
                current_price.grid(row=coin_row, column=4, sticky=N + E + W + S)

                current_val = Label(pycrypto, text="{0:.2f}".format(total_value), bg="#F3F4F6", fg="black", font="Lato 12 ", padx="2", pady="2", borderwidth=2, relief="groove")
                current_val.grid(row=coin_row, column=5, sticky=N + E + W + S)

                pl_coin = Label(pycrypto, text="{0:.2f}".format(net_coin), bg="#F3F4F6", fg=font_color(float("{0:.2f}".format(net_coin))), font="Lato 12 ", padx="2", pady="2", borderwidth=2, relief="groove")
                pl_coin.grid(row=coin_row, column=6, sticky=N + E + W + S)

                net_val = Label(pycrypto, text="{0:.2f}".format(net), bg="#F3F4F6", fg=font_color(float("{0:.2f}".format(net))), font="Lato 12 ", padx="2", pady="2", borderwidth=2, relief="groove")
                net_val.grid(row=coin_row, column=7, sticky=N + E + W + S)

                coin_row += 1



    #print("All coins Net Portfolio {0:.2f} :".format(net_all))
    net_val = Label(pycrypto, text="Total", bg="#142E54", fg="white", font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
    net_val.grid(row=coin_row, column=0, sticky=N + E + W + S)

    total_coin = Label(pycrypto, text=coin_numbers, bg="#142E54", fg="white", font="Lato 12 bold", padx="5",pady="5", borderwidth=2, relief="groove")
    total_coin.grid(row=coin_row, column=2, sticky=N + E + W + S)

    total_pur = Label(pycrypto, text="{0:.2f}".format(coin_total_purchase), bg="#142E54", fg="white", font="Lato 12 bold", padx="5",pady="5", borderwidth=2, relief="groove")
    total_pur.grid(row=coin_row, column=3, sticky=N + E + W + S)

    total_all = Label(pycrypto, text="{0:.2f}".format(net_all),  bg="#142E54", fg=font_color(float("{0:.2f}".format(net_all))), font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
    total_all.grid(row=coin_row, column=7, sticky=N + E + W + S)

    # Adding new coin
    add_coin = Button(pycrypto, text="Add", bg="#142E54", fg="white", command=insert_val, font="Lato 12 bold", padx="5",pady="5", borderwidth=2, relief="groove")
    add_coin.grid(row=coin_row + 1, column=6, sticky=N + E + W + S)

    symbol_txt = Entry(pycrypto, borderwidth=2, relief="groove")
    symbol_txt.grid(row=coin_row + 1, column=1)

    quantity_txt = Entry(pycrypto, borderwidth=2, relief="groove")
    quantity_txt.grid(row=coin_row + 1, column=2)

    price_txt = Entry(pycrypto, borderwidth=2, relief="groove")
    price_txt.grid(row=coin_row + 1, column=3)

    # Updating details of existing coin
    update_coin = Button(pycrypto, text="Update", bg="#142E54", fg="white", command=update_val, font="Lato 12 bold", padx="5",pady="5", borderwidth=2, relief="groove")
    update_coin.grid(row=coin_row + 2, column=6, sticky=N + E + W + S)

    pfolio_update = Entry(pycrypto, borderwidth=2, relief="groove")
    pfolio_update.grid(row=coin_row + 2, column=0)

    symbol_update = Entry(pycrypto, borderwidth=2, relief="groove")
    symbol_update.grid(row=coin_row + 2, column=1)

    quantity_update = Entry(pycrypto, borderwidth=2, relief="groove")
    quantity_update.grid(row=coin_row + 2, column=2)

    price_update = Entry(pycrypto, borderwidth=2, relief="groove")
    price_update.grid(row=coin_row + 2, column=3)

    # Delet coin
    del_coin = Button(pycrypto, text="Delete", bg="#142E54", fg="white", command=del_val, font="Lato 12 bold",padx="5", pady="5", borderwidth=2, relief="groove")
    del_coin.grid(row=coin_row + 3, column=6, sticky=N + E + W + S)

    pfolio_del = Entry(pycrypto, borderwidth=2, relief="groove")
    pfolio_del.grid(row=coin_row + 3, column=0)


    api = ""
    refresh = Button(pycrypto, text="Refresh", bg="#142E54",fg="white", command=reset, font="Lato 12 bold", padx="5", pady="5",borderwidth=2, relief="groove")
    refresh.grid(row=coin_row+1, column=7, sticky=N + E + W + S)

def app_header ():

    pfolioid = Label(pycrypto, text="ID", bg="#142E54", fg="white", font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
    pfolioid.grid(row=0, column=0, sticky=N+E+W+S)

    name = Label(pycrypto, text="Coin Name", bg="#142E54", fg="white", font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
    name.grid(row=0, column=1, sticky=N+E+W+S)

    no_coins = Label(pycrypto, text="Coin Quantity", bg="#142E54", fg="white", font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
    no_coins.grid(row=0, column=2, sticky=N+E+W+S)

    amount_paid = Label(pycrypto, text="Amount Paid", bg="#142E54", fg="white", font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
    amount_paid.grid(row=0, column=3, sticky=N+E+W+S)

    price = Label(pycrypto, text="Latest Price", bg="#142E54", fg="white", font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
    price.grid(row=0, column=4, sticky=N+E+W+S)

    current_val = Label(pycrypto, text="Total Value", bg="#142E54", fg="white", font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
    current_val.grid(row=0, column=5, sticky=N+E+W+S)

    pl_coin = Label(pycrypto, text="P/L Per Coin", bg="#142E54", fg="white", font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
    pl_coin.grid(row=0, column=6, sticky=N+E+W+S)

    net_val = Label(pycrypto, text="Net Value", bg="#142E54", fg="white", font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
    net_val.grid(row=0, column=7, sticky=N+E+W+S)

app_nav()
app_header()
my_portfolio()
pycrypto.mainloop()
print ("Application Exited")


