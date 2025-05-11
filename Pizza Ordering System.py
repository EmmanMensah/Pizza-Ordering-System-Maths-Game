import tkinter as tk
from tkinter import messagebox, Toplevel, Spinbox, Radiobutton, LabelFrame, Button
import re

# Price constants
FLAVOR_PRICES = {"Margherita": 5.00, "Pepperoni": 6.50, "Vegetarian": 5.75}
TOPPING_PRICES = {"Extra Cheese": 0.75, "Mushroom": 0.75, "Onion": 0.75, "Pepper": 0.75, "Olive": 0.75}
SIZE_MULTIPLIERS = {"Small": 1.0, "Medium": 1.2, "Large": 1.5}
DELIVERY_CHARGE = 2.50
DISCOUNT_THRESHOLD = 20.0
DISCOUNT_RATE = 0.10
MAX_PIZZAS = 6

class Customer:
    PHONE_REGEX = re.compile(r"^\+?\d{7,15}$")

    def __init__(self, name, address, phone):
        self.name = name.strip()
        self.address = address.strip()
        self.phone = phone.strip()
        self.validate()

    def validate(self):
        if not self.name:
            raise ValueError("Name is required.")
        if not self.address:
            raise ValueError("Address is required.")
        if not Customer.PHONE_REGEX.match(self.phone):
            raise ValueError("Phone must be 7-15 digits, optional '+'.")

class PizzaItem:
    def __init__(self, flavor, quantity):
        self.flavor = flavor
        self.quantity = quantity
        self.validate()

    def validate(self):
        if not (0 <= self.quantity <= MAX_PIZZAS):
            raise ValueError(f"Quantity for {self.flavor} must be 0-{MAX_PIZZAS}.")

class Order:
    def __init__(self, customer, pizzas, size, toppings, order_type):
        self.customer = customer
        self.pizzas = pizzas
        self.size = size
        self.toppings = toppings
        self.order_type = order_type
        self.validate()

    def validate(self):
        if sum(q for _, q in self.pizzas) == 0:
            raise ValueError("Select at least one pizza.")

    def calculate_totals(self):
        sub = 0
        mult = SIZE_MULTIPLIERS[self.size]
        for flavor, qty in self.pizzas:
            sub += FLAVOR_PRICES[flavor] * qty * mult
        for name, sel in self.toppings.items():
            if sel.get(): sub += TOPPING_PRICES[name]
        disc = sub * DISCOUNT_RATE if sub > DISCOUNT_THRESHOLD else 0
        total = sub - disc
        if self.order_type == "Delivery":
            total += DELIVERY_CHARGE
        return sub, disc, total

class PizzaOrderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("EmZS PIZZABOX")
        self.build_ui()

    def build_ui(self):
        bg = '#fff0e6'
        self.root.configure(bg=bg)

        tk.Label(self.root, text="EMZS PIZZABOX", font=('Arial',24,'bold'), bg='#ff704d', fg='white').pack(fill='x', pady=(0,10))

        self.build_customer(bg)
        self.build_size(bg)
        self.build_pizza(bg)
        self.build_toppings(bg)
        self.build_order_type(bg)
        self.build_actions(bg)
        self.build_output(bg)

    def build_customer(self, bg):
        sec = LabelFrame(self.root, text="Customer Details", bg='#e6f7ff', padx=10, pady=10)
        sec.pack(fill='x', padx=10, pady=5)
        self.name_var = tk.StringVar()
        self.addr_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        for text, var in [("Name",self.name_var),("Address",self.addr_var),("Phone",self.phone_var)]:
            tk.Label(sec, text=text+":", bg=sec['bg']).pack(anchor='w')
            tk.Entry(sec, textvariable=var, bg='white').pack(fill='x', pady=2)

    def build_size(self, bg):
        sec = LabelFrame(self.root, text="Choose Size", bg='#e6ffe6', padx=10, pady=10)
        sec.pack(fill='x', padx=10, pady=5)
        self.size_var = tk.StringVar(value="Large")
        for size in SIZE_MULTIPLIERS:
            Radiobutton(sec, text=size, variable=self.size_var, value=size, bg=sec['bg']).pack(side='left', padx=5)

    def build_pizza(self, bg):
        sec = LabelFrame(self.root, text="Choose Pizzas", bg='#fff9e6', padx=10, pady=10)
        sec.pack(fill='x', padx=10, pady=5)
        self.pizza_vars = {}
        for flavor in FLAVOR_PRICES:
            frame = tk.Frame(sec, bg=sec['bg'])
            frame.pack(fill='x', pady=2)
            tk.Label(frame, text=f"{flavor} (£{FLAVOR_PRICES[flavor]:.2f}):", bg=sec['bg']).pack(side='left')
            var = tk.IntVar(value=0)
            self.pizza_vars[flavor] = var
            Spinbox(frame, from_=0, to=MAX_PIZZAS, textvariable=var, width=5).pack(side='left', padx=5)

    def build_toppings(self, bg):
        sec = LabelFrame(self.root, text="Select Toppings", bg='#ffe6f2', padx=10, pady=10)
        sec.pack(fill='x', padx=10, pady=5)
        self.topping_vars = {}
        for name in TOPPING_PRICES:
            var = tk.BooleanVar()
            self.topping_vars[name] = var
            tk.Checkbutton(sec, text=f"{name} (£{TOPPING_PRICES[name]:.2f})", variable=var, bg=sec['bg']).pack(anchor='w')

    def build_order_type(self, bg):
        sec = LabelFrame(self.root, text="Order Type", bg='#e6e6ff', padx=10, pady=10)
        sec.pack(fill='x', padx=10, pady=5)
        self.order_type = tk.StringVar(value="Eat-in")
        for opt in ["Eat-in","Takeaway","Delivery"]:
            Radiobutton(sec, text=opt, variable=self.order_type, value=opt, bg=sec['bg']).pack(side='left', padx=5)

    def build_actions(self, bg):
        sec = tk.Frame(self.root, bg=bg)
        sec.pack(fill='x', padx=10, pady=10)
        Button(sec, text="Calculate", command=self.calculate, bg='#4da6ff', fg='white', width=12).pack(side='left', padx=5)
        Button(sec, text="Try Again", command=self.reset, bg='#ffa64d', fg='white', width=12).pack(side='left', padx=5)
        Button(sec, text="Clear Summary", command=self.clear_summary, bg='#ffd11a', fg='black', width=12).pack(side='left', padx=5)
        Button(sec, text="Help", command=self.show_help, bg='#b3b3cc', fg='black', width=12).pack(side='left', padx=5)

    def build_output(self, bg):
        sec = LabelFrame(self.root, text="Summary", bg='#ffffff', padx=10, pady=10)
        sec.pack(fill='both', expand=True, padx=10, pady=5)
        self.output = tk.Text(sec, height=10, wrap='word', bg='#f9f9f9')
        self.output.pack(fill='both', expand=True)

    def show_help(self):
        win = Toplevel(self.root)
        win.title("Help")
        msg = (
            "Enter details.\n"
            "Pick size: small, medium, or large.\n"
            "Set flavor quantities.\n"
            "Choose toppings.\n"
            "Select order type.\n"
            "Click Calculate to see summary.\n"
            "Use Try Again to reset fields.\n"
            "Clear Summary removes only the summary text.")
        tk.Label(win, text=msg, justify='left', padx=10, pady=10, bg='#ffffe6').pack()

    def calculate(self):
        try:
            cust = Customer(self.name_var.get(), self.addr_var.get(), self.phone_var.get())
            pizzas = [(flavor, var.get()) for flavor, var in self.pizza_vars.items()]
            order = Order(cust, pizzas, self.size_var.get(), self.topping_vars, self.order_type.get())
            sub, disc, total = order.calculate_totals()
            lines = [f"Name: {cust.name}", f"Address: {cust.address}", f"Phone: {cust.phone}\n"]
            lines.append(f"Size: {self.size_var.get()}")
            for flavor, qty in pizzas:
                if qty:
                    price = FLAVOR_PRICES[flavor] * qty * SIZE_MULTIPLIERS[self.size_var.get()]
                    lines.append(f"{flavor} x {qty}: £{price:.2f}")
            for name, var in self.topping_vars.items():
                if var.get(): lines.append(f"{name}: £{TOPPING_PRICES[name]:.2f}")
            if disc:
                lines.append(f"Discount: -£{disc:.2f}")
            if self.order_type.get() == "Delivery":
                lines.append(f"Delivery Charge: £{DELIVERY_CHARGE:.2f}")
            lines.append(f"\nTotal: £{total:.2f}")
            self.output.delete('1.0', tk.END)
            self.output.insert('1.0', "\n".join(lines))
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def reset(self):
        self.name_var.set('')
        self.addr_var.set('')
        self.phone_var.set('')
        self.size_var.set('Large')
        for var in self.pizza_vars.values(): var.set(0)
        for var in self.topping_vars.values(): var.set(False)
        self.order_type.set('Eat-in')
        self.clear_summary()

    def clear_summary(self):
        self.output.delete('1.0', tk.END)

if __name__ == '__main__':
    root = tk.Tk()
    app = PizzaOrderApp(root)
    root.mainloop()
