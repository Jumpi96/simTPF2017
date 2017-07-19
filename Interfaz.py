from tkinter import *

def simular():
	print("a")

def set_ejercicio():
	print("a")

def set_variable():
	print("a")

master = Tk()
master.wm_title("Simulación - TP Final")

v = IntVar()

Radiobutton(master, command=set_ejercicio, text="Ejercicio", variable=v, value=1).grid(row=0,column=1)
Radiobutton(master, command=set_variable, text="Modificable", variable=v, value=2).grid(row=0,column=2)
v.set(1)
set_variable()

Label(master, text="Precio por auto").grid(row=1)
Label(master, text="Pérdida por abandono").grid(row=2)
Label(master, text="Costo de grúa").grid(row=3)
Label(master, text="Tiempo de grúa").grid(row=4)
Label(master, text="Capacidad de grúa").grid(row=5)
Label(master, text="Servicio mínimo").grid(row=6)
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

mainloop( )