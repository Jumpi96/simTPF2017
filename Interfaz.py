from tkinter import *
from tkinter import messagebox as tkMessageBox

def simular():
    if validar():
        print("Completar")
        
def validar():
    if (not no_negativo(e1.get())) or (not no_negativo(f1.get())):
        tkMessageBox.showinfo("Error", "El precio por auto ingresado no es válido.")
        return False
    if (not no_negativo(e2.get())) or (not no_negativo(f2.get())):
        tkMessageBox.showinfo("Error", "La pérdida por abandono ingresada no es válida.")
        return False
    if (not no_negativo(e3.get())) or (not no_negativo(f3.get())):
        tkMessageBox.showinfo("Error", "El costo por viaje de la grúa no es válida.")
        return False
    if (not no_negativo(e4.get())) or (not no_negativo(f4.get())):
        tkMessageBox.showinfo("Error", "El tiempo de la grúa ingresado no es válido.")
        return False
    if (not mayor_que_cero(e5.get())) or (not mayor_que_cero(f5.get())):
        tkMessageBox.showinfo("Error", "La capacidad de la grúa ingresada no es válida.")
        return False
    if (not no_negativo(e6.get())) or (not no_negativo(f6.get())):
        tkMessageBox.showinfo("Error", "El servicio mínimo ingresado no es válido.")
        return False
    if not mayor_que_cero(e7.get()):
        tkMessageBox.showinfo("Error", "La cantidad de minutos a simular no es válida.")
        return False
    if (not no_negativo(e8.get())) or (float(e8.get())>float(e7.get())):
        tkMessageBox.showinfo("Error", "No se puede mostrar desde el minuto indicado.")
        return False
    if not no_negativo(e9.get()):
        tkMessageBox.showinfo("Error", "El número de iteraciones ingresado no es válido.")
        return False
    return True
    
def is_numeric(value):
    try:
        float(value)
        return True
    except ValueError:
        return False
    
def mayor_que_cero(value):
    return is_numeric(value) and float(value)>0.0
    
def no_negativo(value):
    return is_numeric(value) and float(value)>=0.0

def set_ejercicio():
    e1.delete(0,END)
    e1.insert(0,"2.5")
    e1.config(state='readonly')
    f1.delete(0,END)
    f1.insert(0,"2.5")
    f1.config(state='readonly')
    e2.delete(0,END)
    e2.insert(0,"1.5")
    e2.config(state='readonly')
    f2.delete(0,END)
    f2.insert(0,"1.5")
    f2.config(state='readonly')
    e3.delete(0,END)
    e3.insert(0,"7")
    e3.config(state='readonly')
    f3.delete(0,END)
    f3.insert(0,"7")
    f3.config(state='readonly')
    e4.delete(0,END)
    e4.insert(0,"6")
    e4.config(state='readonly')
    f4.delete(0,END)
    f4.insert(0,"6")
    f4.config(state='readonly')
    e5.delete(0,END)
    e5.insert(0,"5")
    e5.config(state='readonly')
    f5.delete(0,END)
    f5.insert(0,"5")
    f5.config(state='readonly')
    e6.delete(0,END)
    e6.insert(0,"5")
    e6.config(state='readonly')
    f6.delete(0,END)
    f6.insert(0,"3")
    f6.config(state='readonly')
    
    e7.delete(0,END)
    e7.insert(0,'480')
    e7.config(state='readonly')
    e8.delete(0,END)
    e8.insert(0,'0')
    e8.config(state='normal')
    e9.delete(0,END)
    e9.insert(0,'50')
    e9.config(state='normal')

def set_variable():
    e1.config(state='normal')
    f1.config(state='normal')
    e2.config(state='normal')
    f2.config(state='normal')
    e3.config(state='normal')
    f3.config(state='normal')
    e4.config(state='normal')
    f4.config(state='normal')
    e5.config(state='normal')
    f5.config(state='normal')
    e6.config(state='normal')
    f6.config(state='normal')
    e7.config(state='normal')

master = Tk()
master.wm_title("Simulación - TP Final")

v = IntVar()

Radiobutton(master, command=set_ejercicio, text="Ejercicio", variable=v, value=1).grid(row=0,column=1)
Radiobutton(master, command=set_variable, text="Modificable", variable=v, value=2).grid(row=0,column=2)
v.set(1)

Label(master, text="Precio por auto ($)").grid(row=1)
Label(master, text="Pérdida por abandono ($)").grid(row=2)
Label(master, text="Costo de grúa ($)").grid(row=3)
Label(master, text="Tiempo de grúa (min)").grid(row=4)
Label(master, text="Capacidad de grúa (un.)").grid(row=5)
Label(master, text="Servicio mínimo (un.)").grid(row=6)
Label(master, text="Minutos").grid(row=7)
Label(master, text="Mostrar desde min.").grid(row=8)
Label(master, text="Mostrar n iteraciones").grid(row=9)

e1 = Entry(master)
f1 = Entry(master)
e2 = Entry(master)
f2 = Entry(master)
e3 = Entry(master)
f3 = Entry(master)
e4 = Entry(master)
f4 = Entry(master)
e5 = Entry(master)
f5 = Entry(master)
e6 = Entry(master)
f6 = Entry(master)
e7 = Entry(master)
e8 = Entry(master)
e9 = Entry(master)

e1.grid(row=1, column=1)
f1.grid(row=1, column=2)
e2.grid(row=2, column=1)
f2.grid(row=2, column=2)
e3.grid(row=3, column=1)
f3.grid(row=3, column=2)
e4.grid(row=4, column=1)
f4.grid(row=4, column=2)
e5.grid(row=5, column=1)
f5.grid(row=5, column=2)
e6.grid(row=6, column=1)
f6.grid(row=6, column=2)
e7.grid(row=7, column=1, columnspan=2)
e8.grid(row=8, column=1, columnspan=2)
e9.grid(row=9, column=1, columnspan=2)


Button(master, text='Salir', command=master.quit).grid(row=10, column=0, sticky=W, pady=4)
Button(master, text='Simular', command=simular).grid(row=10, column=1, sticky=W, pady=4)

set_ejercicio()
mainloop( )