import tkinter as tk
from tkinter import messagebox, Toplevel


# Constants
PIZZA_PRICES = {"Small": 3.25, "Medium": 5.50, "Large": 7.15}
TOPPING_PRICES = {1: 0.75, 2: 1.35, 3: 2.00, 4: 2.50}
DELIVERY_CHARGE = 2.50
DISCOUNT_THRESHOLD = 20
DISCOUNT_RATE = 0.10


class PizzaOrderApp:
   def __init__(self, root):
       self.root = root
       self.root.title("EmZS pIZZABOX")
       self.root.geometry("600x700")
       self.root.configure(bg="#fff5e6")


       # Title/Header
       tk.Label(self.root, text="EMZS PIZZABOX", font=("Arial", 24, "bold"), bg="#ff704d", fg="white", pady=10).pack(fill="x")


       # Sections
       self.create_customer_section()
       self.create_pizza_section()
       self.create_toppings_section()
       self.create_delivery_section()
       self.create_buttons_section()
       self.create_output_section()


   def create_customer_section(self):
       frame = tk.LabelFrame(self.root, text="Customer Details", bg="#e6f7ff", padx=10, pady=10)
       frame.pack(fill="x", padx=10, pady=5)
       self.customer_name = tk.StringVar()
       self.customer_address = tk.StringVar()
       self.customer_phone = tk.StringVar()
       self.create_labeled_entry(frame, "Name:", self.customer_name)
       self.create_labeled_entry(frame, "Address:", self.customer_address)
       self.create_labeled_entry(frame, "Phone:", self.customer_phone)


   def create_pizza_section(self):
       frame = tk.LabelFrame(self.root, text="Pizza Order", bg="#e6ffe6", padx=10, pady=10)
       frame.pack(fill="x", padx=10, pady=5)
       self.pizza_quantities = [tk.IntVar(value=0) for _ in range(3)]
       for i, size in enumerate(["Small", "Medium", "Large"]):
           tk.Label(frame, text=f"{size} (\u00a3{PIZZA_PRICES[size]:.2f}):", bg="#e6ffe6").grid(row=i, column=0, sticky="w")
           tk.Entry(frame, textvariable=self.pizza_quantities[i]).grid(row=i, column=1)


   def create_toppings_section(self):
       frame = tk.LabelFrame(self.root, text="Extra Toppings", bg="#fff9e6", padx=10, pady=10)
       frame.pack(fill="x", padx=10, pady=5)
       self.toppings = tk.IntVar(value=0)
       tk.Label(frame, text="Number of Toppings:", bg="#fff9e6").pack(anchor="w")
       tk.Entry(frame, textvariable=self.toppings).pack(anchor="w")
       tk.Button(frame, text="Tip", command=self.show_topping_tip, bg="#ffd11a").pack(anchor="e", pady=5)


   def create_delivery_section(self):
       frame = tk.LabelFrame(self.root, text="Delivery Option", bg="#f0e6ff", padx=10, pady=10)
       frame.pack(fill="x", padx=10, pady=5)
       self.delivery = tk.BooleanVar(value=False)
       tk.Checkbutton(frame, text="Request Delivery (\u00a32.50)", variable=self.delivery, bg="#f0e6ff").pack(anchor="w")


   def create_buttons_section(self):
       frame = tk.Frame(self.root, bg="#fff5e6")
       frame.pack(fill="x", padx=10, pady=10)
       tk.Button(frame, text="Calculate Bill", command=self.calculate_bill, bg="#4da6ff", fg="white", width=15).pack(side="left", padx=5)
       tk.Button(frame, text="Reset", command=self.reset_fields, bg="#ff6666", fg="white", width=10).pack(side="left", padx=5)
       tk.Button(frame, text="Help", command=self.show_help, bg="#b3b3cc", fg="black", width=10).pack(side="left", padx=5)


   def create_output_section(self):
       frame = tk.LabelFrame(self.root, text="Order Summary", bg="#ffffff", padx=10, pady=10)
       frame.pack(fill="both", expand=True, padx=10, pady=5)
       self.output_text = tk.Text(frame, height=10, wrap="word")
       self.output_text.pack(fill="both", expand=True)


   def create_labeled_entry(self, frame, label_text, text_var):
       row = len(frame.winfo_children()) // 2
       tk.Label(frame, text=label_text, bg=frame.cget("bg")).grid(row=row, column=0, sticky="w")
       tk.Entry(frame, textvariable=text_var).grid(row=row, column=1)


   def show_topping_tip(self):
       messagebox.showinfo("Topping Tip", "1 topping = £0.75\n2 toppings = £1.35\n3 toppings = £2.00\n4 or more = £2.50")


   def show_help(self):
       help_win = Toplevel(self.root)
       help_win.title("Help")
       tk.Label(help_win, text="How to Use the Pizza Order System", font=("Arial", 14, "bold")).pack(pady=10)
       instructions = (
           "1. Enter customer name, address, and phone number.\n"
           "2. Choose the number of pizzas per size (max 6 total).\n"
           "3. Add extra toppings if needed.\n"
           "4. Tick delivery option if customer wants delivery.\n"
           "5. Click 'Calculate Bill' to see the full breakdown.\n"
           "6. Use 'Reset' to clear all fields."
       )
       tk.Label(help_win, text=instructions, justify="left").pack(padx=20, pady=10)


   def calculate_bill(self):
       try:
           name = self.customer_name.get().strip()
           address = self.customer_address.get().strip()
           phone = self.customer_phone.get().strip()
           if not name or not address or not phone:
               raise ValueError("Please fill in all customer details.")


           total = 0
           summary = [f"Customer: {name}\nAddress: {address}\nPhone: {phone}\n"]


           for i, size in enumerate(["Small", "Medium", "Large"]):
               qty = self.pizza_quantities[i].get()
               if qty < 0 or qty > 6:
                   raise ValueError("Pizza quantity must be between 0 and 6.")
               if qty:
                   cost = qty * PIZZA_PRICES[size]
                   total += cost
                   summary.append(f"{size} x {qty}: £{cost:.2f}")


           toppings = self.toppings.get()
           if toppings < 0:
               raise ValueError("Toppings cannot be negative.")
           if toppings:
               topping_cost = TOPPING_PRICES.get(toppings, TOPPING_PRICES[4])
               total += topping_cost
               summary.append(f"Extra Toppings: £{topping_cost:.2f}")


           if total > DISCOUNT_THRESHOLD:
               discount = total * DISCOUNT_RATE
               total -= discount
               summary.append(f"Discount (10%): -£{discount:.2f}")


           if self.delivery.get():
               total += DELIVERY_CHARGE
               summary.append(f"Delivery Charge: £{DELIVERY_CHARGE:.2f}")


           summary.append(f"\nTotal Cost: £{total:.2f}")
           self.output_text.delete("1.0", tk.END)
           self.output_text.insert(tk.END, "\n".join(summary))


       except ValueError as e:
           messagebox.showerror("Input Error", str(e))


   def reset_fields(self):
       self.customer_name.set("")
       self.customer_address.set("")
       self.customer_phone.set("")
       for var in self.pizza_quantities:
           var.set(0)
       self.toppings.set(0)
       self.delivery.set(False)
       self.output_text.delete("1.0", tk.END)


if __name__ == "__main__":
   root = tk.Tk()
   app = PizzaOrderApp(root)
   root.mainloop()
