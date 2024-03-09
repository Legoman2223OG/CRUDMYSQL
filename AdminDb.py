import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter.messagebox import showinfo,askquestion
from tkinter.scrolledtext import ScrolledText
import os
import mysql.connector

BASES=[]
TABLAS=[]

class AdminDb:
    def __init__(self):
        self.ventana1=tk.Tk()
        self.ventana1.title("Administracion de Bases de Datos MySql")
        self.ventana1.geometry("1000x650")
        menubar1 = tk.Menu(self.ventana1)
        self.ventana1.config(menu=menubar1)
        opciones1 = tk.Menu(menubar1)
        opciones1.add_command(label="Crear", command=self.abrirventanacrearBD)
        opciones1.add_command(label="Eliminar", command=self.ventanaborrarbd)
        menubar1.add_cascade(label="Base de Datos", menu=opciones1)        
        opciones2 = tk.Menu(menubar1)
        opciones2.add_command(label="Crear", command=self.ventanacreartabla)
        opciones2.add_command(label="Editar", command=self.ventantaeditartablas)
        opciones2.add_command(label="Eliminar", command=self.ventanaeliminartabla)
        menubar1.add_cascade(label="Tablas", menu=opciones2)    
        opciones3 = tk.Menu(menubar1)
        opciones3.add_command(label="Sql", command=self.ventanaSQL)
        opciones3.add_command(label="Importar", command=self.ventanaImport)
        opciones3.add_command(label="Exportar", command=self.exportarSQL)
        menubar1.add_cascade(label="Herramientas", menu=opciones3)
        #COnexion al servidor
        labelSrv=ttk.Label(text="Servidor:")
        labelSrv.grid(column=0, row=0, padx=4, pady=4)
        self.ServerName=ttk.Entry()
        self.ServerName.insert(0,"localhost")
        self.ServerName.grid(column=1, row=0, padx=4, pady=4) 
        
        labelUser=ttk.Label(text="Usuario:")
        labelUser.grid(column=2, row=0, padx=4, pady=4)
        self.UserName=ttk.Entry()
        self.UserName.insert(0,"root")
        self.UserName.grid(column=3, row=0, padx=4, pady=4)
        
        labelPass=ttk.Label(text="Password:")
        labelPass.grid(column=4, row=0, padx=4, pady=4)
        self.PassName=ttk.Entry(show="*")
        self.PassName.insert(0,"")
        self.PassName.grid(column=5, row=0, padx=4, pady=4)
        
        labelPuerto=ttk.Label(text="Puerto:")
        labelPuerto.grid(column=6, row=0, padx=4, pady=4)
        self.PuertoName=ttk.Entry()
        self.PuertoName.insert(0,"3306")
        self.PuertoName.grid(column=7, row=0, padx=4, pady=4)

        botonConn=ttk.Button(text="Conectar",command=self.ConectarServidor)
        botonConn.grid(column=8, row=0, padx=4, pady=4)

        self.labelStsServer=ttk.Label(text="")
        self.labelStsServer.grid(column=9, row=0, padx=4, pady=4)

        labelBaseSel=ttk.Label(text="Base: ")
        labelBaseSel.grid(column=2, row=1, padx=4, pady=4)
        self.BaseSel=ttk.Entry()
        self.BaseSel.grid(column=3, row=1, padx=4, pady=4)

        labelTablaSel=ttk.Label(text="Tabla: ")
        labelTablaSel.grid(column=4, row=1, padx=4, pady=4)
        self.TablaSel=ttk.Entry()
        self.TablaSel.grid(column=5, row=1, padx=4, pady=4)

        #arbol de bases de datos
        self.TvBases = ttk.Treeview(self.ventana1,selectmode="browse",height="5")
        self.TvBases.place(x=0, y=60, width=200, height=600)
        self.TvBases.heading('#0', text='Bases', anchor='center')
        self.TvBases.column('#0', width=200, anchor='center', stretch=True)
        self.TvBases.bind('<<TreeviewSelect>>', self.base_selected)

        self.TvTablas= ttk.Treeview(self.ventana1, selectmode="browse",height="5")
        self.TvTablas.place(x=200, y=60, width=200, height=600)
        self.TvTablas.heading('#0', text='Tablas', anchor='center')
        self.TvTablas.column('#0', width=200, anchor='center', stretch=True)
        self.TvTablas.bind('<<TreeviewSelect>>', self.tabla_selected)
        
        columns = ("#1", "#2", "#3", "#4", "#5", "#6", "#7")  
        self.TvCampos= ttk.Treeview(self.ventana1,show="headings",height="5", columns=columns) 
        self.TvCampos.place(x=400, y=60, width=600, height=600) 
        self.TvCampos.heading('#1', text='P.Key', anchor='nw')  
        self.TvCampos.column('#1', width=60, anchor='nw', stretch=False)  
        self.TvCampos.heading('#2', text='Nombre', anchor='center')  
        self.TvCampos.column('#2', width=10, anchor='nw', stretch=True)  
        self.TvCampos.heading('#3', text='Tipo', anchor='center')  
        self.TvCampos.column('#3',width=10, anchor='nw', stretch=True)  
        self.TvCampos.heading('#4', text='Not NULL', anchor='center')  
        self.TvCampos.column('#4',width=10, anchor='nw', stretch=True)  
        self.TvCampos.heading('#5', text='Auto Inc', anchor='center')  
        self.TvCampos.column('#5',width=10, anchor='nw', stretch=True)  
        self.TvCampos.heading('#6', text='Flags', anchor='center')  
        self.TvCampos.column('#6', width=10, anchor='nw', stretch=True)  
        self.TvCampos.heading('#7', text='Default', anchor='center')  
        self.TvCampos.column('#7', width=10, anchor='nw', stretch=True)  
        #Scroll bars are set up below considering placement position(x&y) ,height and width of treeview widget  
        vsb= ttk.Scrollbar(self.ventana1, orient=tk.VERTICAL,command=self.TvCampos.yview)  
        vsb.place(x=400 + 660 + 1, y=310, height=180 + 20)  
        self.TvCampos.configure(yscroll=vsb.set)  
        #hsb = ttk.Scrollbar(self.ventana1, orient=tk.HORIZONTAL, command=self.TvCampos.xview)  
        #hsb.place(x=40 , y=310+200+1, width=620 + 20)  
        #self.TvCampos.configure(xscroll=hsb.set)  
        self.TvCampos.bind("<<TreeviewSelect>>", self.MostrarCampos)     
        

        self.ventana1.mainloop()
        
    def tabla_selected(self,event):
        for selected_item in self.TvTablas.selection():
            item = self.TvTablas.item(selected_item)
            record = item['values']   
        i=int(selected_item)
        self.TablaSel.delete(0, tk.END)
        self.TablaSel.insert(0,TABLAS[i]) 
        self.MostrarCampos(TABLAS[i])
    
    def base_selected(self,event):
        for selected_item in self.TvBases.selection():
            item = self.TvBases.item(selected_item)
            record = item['values']
        i=int(selected_item)
        self.BaseSel.delete(0, tk.END)
        self.BaseSel.insert(0,BASES[i]) 
        self.MostrarTablas(BASES[i])
    
    def MostrarTablas(self,base): 
        db_connection = mysql.connector.connect(host=self.ServerName.get(),  
        user=self.UserName.get(),  
        password=self.PassName.get())
        db_cursor = db_connection.cursor(buffered=True)
        if db_connection.is_connected() == False:  
            db_connection.connect() 

        if db_connection.is_connected() == True:
            self.labelStsServer['text']="Conectado"
        else:
            self.labelStsServer['text']="Sin Conexion"
        sql = "SHOW FULL TABLES FROM "+ self.BaseSel.get()
        db_cursor.execute(sql)
        total = db_cursor.rowcount
        rows = db_cursor.fetchall()
        self.TvTablas.delete(*self.TvTablas.get_children())
        k=0
        TABLAS.clear()
        for row in rows: 
            TABLAS.append(row[0])
            self.TvTablas.insert("", tk.END,iid=k, text=row[0]) 
            k=k+1
        i=0
        
        while i< len(TABLAS):
            print(TABLAS[i])
            i=i+1
    
    
    def MostrarCampos(self,tabla): 
        db_connection = mysql.connector.connect(host=self.ServerName.get(),  
        user=self.UserName.get(),  
        password=self.PassName.get())
        db_cursor = db_connection.cursor(buffered=True)
        if db_connection.is_connected() == False:  
            db_connection.connect() 

        if db_connection.is_connected() == True:
            self.labelStsServer['text']="Conectado"
        else:
            self.labelStsServer['text']="Sin Conexion"
        sql = "SHOW FULL COLUMNS FROM "+ self.TablaSel.get() + " FROM " +  self.BaseSel.get()
        db_cursor.execute(sql)
        total = db_cursor.rowcount
        rows = db_cursor.fetchall()
        self.TvCampos.delete(*self.TvCampos.get_children())
        k=0
        for row in rows: 
            key = row[4]
            Nombre = row[0]
            tipo = row[1]
            nulo = row[3]
            default = row[6]
            otro = row[5]
            
            self.TvCampos.insert("", 'end', text=Nombre, values=(key, Nombre, tipo, nulo, default, otro)) 
            k=k+1
        i=0
        
        while i< len(TABLAS):
            print(TABLAS[i])
            i=i+1
    
    def ConectarServidor(self):
        
        self.labelStsServer=ttk.Label(text="")
        self.labelStsServer.grid(column=9, row=0, padx=4, pady=4)
        db_connection = mysql.connector.connect(host=self.ServerName.get(),  
        user=self.UserName.get(),  
        password=self.PassName.get())
        db_cursor = db_connection.cursor(buffered=True)
        if db_connection.is_connected() == False:  
            db_connection.connect() 

        if db_connection.is_connected() == True:
            self.labelStsServer['text']="Conectado"
        else:
            self.labelStsServer['text']="Sin Conexion"

        sql = "SHOW DATABASES"  
        db_cursor.execute(sql)
        total = db_cursor.rowcount
        rows = db_cursor.fetchall()
        self.TvBases.delete(*self.TvBases.get_children())
        k=0
        BASES.clear()
        for row in rows: 
            BASES.append(row[0])
            self.TvBases.insert("", tk.END,iid=k,text=row[0]) 
            k=k+1
        i=0
        
        while i< len(BASES):
            print(BASES[i])
            i=i+1
    
    def abrirventanacrearBD(self):
        nuevaVentana = tk.Toplevel(self.ventana1)
        nuevaVentana.title("Crear base de datos")
        nuevaVentana.geometry("350x70")
        labelnombrebd =ttk.Label(nuevaVentana,text="Nombre:")
        labelnombrebd.grid(column=0, row=0, padx=8, pady=8)
        nombreBD=ttk.Entry(nuevaVentana,width=40)
        nombreBD.insert(0,"")
        nombreBD.grid(column=2, row=0, padx=8, pady=4)
        def crearbasededatos():
            if nombreBD.get() == "":
                showinfo("Info","Introduzca un nombre",parent=nuevaVentana)
                return
            db_connection = mysql.connector.connect(host=self.ServerName.get(),  
            user=self.UserName.get(),  
            password=self.PassName.get())
            db_cursor = db_connection.cursor(buffered=True)
            if db_connection.is_connected() == False:  
                db_connection.connect()
            try:
                nuevaBaseDeDatos = "CREATE DATABASE " + str(nombreBD.get())
                db_cursor.execute(nuevaBaseDeDatos)
                db_connection.commit()
                sql = "SHOW DATABASES"  
                db_cursor.execute(sql)
                total = db_cursor.rowcount
                rows = db_cursor.fetchall()
                self.TvBases.delete(*self.TvBases.get_children())
                k=0
                BASES.clear()
                for row in rows: 
                    BASES.append(row[0])
                    self.TvBases.insert("", tk.END,iid=k,text=row[0]) 
                    k=k+1
                i=0
                while i< len(BASES):
                    print(BASES[i])
                    i=i+1
                nuevaVentana.destroy()
                nuevaVentana.update()
            except mysql.connector.Error as err:
                    showinfo("Error","La base de datos ya existe, intente de nuevo",parent=nuevaVentana)
                    return
        botoncrear = ttk.Button(nuevaVentana,text="Crear",command=crearbasededatos)
        botoncrear.grid(column=2, row=1, padx=8,pady=4)

    def ventanaborrarbd(self):
        nuevaVentana = tk.Toplevel(self.ventana1)
        nuevaVentana.title("Eliminar base de datos")
        labelnombrebd =ttk.Label(nuevaVentana,text="Nombre:")
        labelnombrebd.grid(column=0, row=0, padx=8, pady=8)
        nombreBD=ttk.Entry(nuevaVentana,width=40)
        nombreBD.insert(0,self.BaseSel.get())
        nombreBD.grid(column=2, row=0, padx=8, pady=4)
        def borrarbasededatos():
            if nombreBD.get() == "":
                showinfo("Info","Introduzca un nombre",parent=nuevaVentana)
                return
            db_connection = mysql.connector.connect(host=self.ServerName.get(),  
            user=self.UserName.get(),  
            password=self.PassName.get())
            db_cursor = db_connection.cursor(buffered=True)
            if db_connection.is_connected() == False:  
                db_connection.connect()
            checkifexists = "SHOW DATABASES LIKE " + "'" + nombreBD.get() + "'" + ";" 
            db_cursor.execute(checkifexists)
    
            if db_cursor.fetchone() == None:
                showinfo("Info","No existe esa base de datos",parent=nuevaVentana)
                return
            else:
                MsgWarning = askquestion('Borrar','¿Desea borrar esta base de datos?')
                if MsgWarning == 'yes':
                    deletedatabase = "DROP DATABASE " + nombreBD.get() + ";"
                    db_cursor.execute(deletedatabase)
                    db_connection.commit()
                    sql = "SHOW DATABASES"  
                    db_cursor.execute(sql)
                    total = db_cursor.rowcount
                    rows = db_cursor.fetchall()
                    self.TvBases.delete(*self.TvBases.get_children())
                    k=0
                    BASES.clear()
                    for row in rows: 
                        BASES.append(row[0])
                        self.TvBases.insert("", tk.END,iid=k,text=row[0]) 
                        k=k+1
                    i=0
                    
                    while i< len(BASES):
                        print(BASES[i])
                        i=i+1
                    self.TvTablas.delete(*self.TvTablas.get_children())
                    nuevaVentana.destroy()
                    nuevaVentana.update()
                else:
                    return        
        botonborrar = ttk.Button(nuevaVentana,text="Borrar",command=borrarbasededatos)
        botonborrar.grid(column=2, row=1, padx=8,pady=4)
    def ventanacreartabla(self):
        nuevaVentana = tk.Toplevel(self.ventana1)
        nuevaVentana.title("Crear tabla")
        labelnombrebd =ttk.Label(nuevaVentana,text="Nombre BD:")
        labelnombrebd.grid(column=0, row=0, padx=8, pady=8)
        nombreBD=ttk.Entry(nuevaVentana,width=40)
        nombreBD.insert(0,self.BaseSel.get())
        nombreBD.grid(column=2, row=0, padx=8, pady=4)
        labelnombretable =ttk.Label(nuevaVentana,text="Nombre Tabla:")
        labelnombretable.grid(column=0, row=2, padx=8, pady=8)
        nombretable=ttk.Entry(nuevaVentana,width=40)
        nombretable.insert(0,"")
        nombretable.grid(column=2, row=2, padx=8, pady=4)
        labelcontenidotabla = ttk.Label(nuevaVentana,text="Contenido ():")
        labelcontenidotabla.grid(column=0, row=3,padx=8,pady=8)
        contenidotabla = ScrolledText(nuevaVentana,width=30,height=15)
        contenidotabla.grid(column=2,row=3,padx=8,pady=4)
        def crearTabla():
            if nombreBD.get() == "":
                showinfo("Info","Introduzca una base de datos",parent=nuevaVentana)
                return
            if nombretable.get() == "":
                showinfo("Info","Introduzca un nombre para la tabla",parent=nuevaVentana)
                return
            db_connection = mysql.connector.connect(host=self.ServerName.get(),  
            user=self.UserName.get(),  
            password=self.PassName.get())
            db_cursor = db_connection.cursor(buffered=True)
            if db_connection.is_connected() == False:  
                db_connection.connect()
            checkifexists = "SHOW DATABASES LIKE " + "'" + nombreBD.get() + "'" + ";" 
            db_cursor.execute(checkifexists)
    
            if db_cursor.fetchone() == None:
                showinfo("Info","No existe esa base de datos",parent=nuevaVentana)
                return
            else:
                usarBD = "use " + nombreBD.get() + ";"
                db_cursor.execute(usarBD)
                try:
                    content = "(" + contenidotabla.get('1.0', 'end-1c') + ")"
                    creartabla = "CREATE TABLE " + nombretable.get() + content + ";"
                    db_cursor.execute(creartabla)
                    db_connection.commit()
                    sql = "SHOW TABLES"  
                    db_cursor.execute(sql)
                    total = db_cursor.rowcount
                    rows = db_cursor.fetchall()
                    self.TvTablas.delete(*self.TvTablas.get_children())
                    k=0
                    TABLAS.clear()
                    for row in rows: 
                        TABLAS.append(row[0])
                        self.TvTablas.insert("", tk.END,iid=k,text=row[0]) 
                        k=k+1
                    i=0
        
                    while i< len(TABLAS):
                        print(TABLAS[i])
                        i=i+1
                    nuevaVentana.destroy()
                    nuevaVentana.update()
                except mysql.connector.Error as err:
                    showinfo("Error","Datos ingresados incorrectamente/Ya existe la tabla, intente de nuevo",parent=nuevaVentana)
                    return
        botonsubir = ttk.Button(nuevaVentana, text="Crear",command=crearTabla)
        botonsubir.grid(column=2,row=4,padx=8,pady=4)

    def ventantaeditartablas(self):
        nuevaVentana = tk.Toplevel(self.ventana1)
        nuevaVentana.title("Editar tabla")
        labelnombrebd =ttk.Label(nuevaVentana,text="Nombre BD:")
        labelnombrebd.grid(column=0, row=0, padx=8, pady=8)
        nombreBD=ttk.Entry(nuevaVentana,width=40)
        nombreBD.insert(0,self.BaseSel.get())
        nombreBD.grid(column=2, row=0, padx=8, pady=4)
        labelnombretable =ttk.Label(nuevaVentana,text="Nombre Tabla:")
        labelnombretable.grid(column=0, row=2, padx=8, pady=8)
        nombretable=ttk.Entry(nuevaVentana,width=40)
        nombretable.insert(0,self.TablaSel.get())
        nombretable.grid(column=2, row=2, padx=8, pady=4)
        labeltitcambiarnombre = ttk.Label(nuevaVentana,text="Cambiar nombre de la tabla")
        labeltitcambiarnombre.grid(column=2, row=3,padx=8,pady=4)
        labelcambiarnombre = ttk.Label(nuevaVentana,text="Nuevo Nombre:")
        labelcambiarnombre.grid(column=0, row=4,padx=8,pady=4)
        nuevonombre = ttk.Entry(nuevaVentana, width=40)
        nuevonombre.grid(column=2,row=4,padx=8,pady=4)
        def cambiarnombredetabla():
            if nombreBD.get() == "":
                showinfo("Info","Introduzca una base de datos",parent=nuevaVentana)
                return
            if nombretable.get() == "":
                showinfo("Info","Introduzca un nombre para la tabla",parent=nuevaVentana)
                return
            db_connection = mysql.connector.connect(host=self.ServerName.get(),  
            user=self.UserName.get(),  
            password=self.PassName.get())
            db_cursor = db_connection.cursor(buffered=True)
            if db_connection.is_connected() == False:  
                db_connection.connect()
            checkifexists = "SHOW DATABASES LIKE " + "'" + nombreBD.get() + "'" + ";" 
            db_cursor.execute(checkifexists)
    
            if db_cursor.fetchone() == None:
                showinfo("Info","No existe esa base de datos",parent=nuevaVentana)
                return
            else:
                usarBD = "use " + nombreBD.get() + ";"
                db_cursor.execute(usarBD)
                try:
                    cambiarnombre = "ALTER TABLE " + nombretable.get() + " RENAME TO " + nuevonombre.get() + ";"
                    db_cursor.execute(cambiarnombre)
                    db_connection.commit()
                    sql = "SHOW TABLES"  
                    db_cursor.execute(sql)
                    total = db_cursor.rowcount
                    rows = db_cursor.fetchall()
                    self.TvTablas.delete(*self.TvTablas.get_children())
                    k=0
                    TABLAS.clear()
                    for row in rows: 
                        TABLAS.append(row[0])
                        self.TvTablas.insert("", tk.END,iid=k,text=row[0]) 
                        k=k+1
                    i=0
        
                    while i< len(TABLAS):
                        print(TABLAS[i])
                        i=i+1
                except mysql.connector.Error as err:
                    showinfo("Error","Tabla inexistente, dato ingresado incorrectamente, intente de nuevo",parent=nuevaVentana)
                    return
        
        labeltitagregarcolumna = ttk.Label(nuevaVentana,text="Agregar Columna")
        labeltitagregarcolumna.grid(column=2,row=5,padx=8,pady=4)
        labelnuevacolumna = ttk.Label(nuevaVentana,text="Columna:")
        labelnuevacolumna.grid(column=0,row=6,padx=8,pady=4)
        nombredelacolumna = ttk.Entry(nuevaVentana, width=15)
        nombredelacolumna.insert(0,"nombre")
        nombredelacolumna.grid(column=2,row=6,padx=0,pady=4)
        contenidocolumna = ScrolledText(nuevaVentana,width=25,height=2)
        contenidocolumna.grid(column=3,row=6,padx=8,pady=4)
        def agregarcolumna():
            if nombreBD.get() == "":
                showinfo("Info","Introduzca una base de datos",parent=nuevaVentana)
                return
            if nombretable.get() == "":
                showinfo("Info","Introduzca un nombre para la tabla",parent=nuevaVentana)
                return
            db_connection = mysql.connector.connect(host=self.ServerName.get(),  
            user=self.UserName.get(),  
            password=self.PassName.get())
            db_cursor = db_connection.cursor(buffered=True)
            if db_connection.is_connected() == False:  
                db_connection.connect()
            checkifexists = "SHOW DATABASES LIKE " + "'" + nombreBD.get() + "'" + ";" 
            db_cursor.execute(checkifexists)
    
            if db_cursor.fetchone() == None:
                showinfo("Info","No existe esa base de datos",parent=nuevaVentana)
                return
            else:
                usarBD = "use " + nombreBD.get() + ";"
                db_cursor.execute(usarBD)
                try:
                    agregarcolumna = "ALTER TABLE " + nombretable.get() + " ADD " + nombredelacolumna.get() + " " + contenidocolumna.get('1.0','end-1c') + ";"
                    db_cursor.execute(agregarcolumna)
                    db_connection.commit()
                    sql = "SHOW FULL COLUMNS FROM "+ self.TablaSel.get() + " FROM " +  self.BaseSel.get()
                    db_cursor.execute(sql)
                    total = db_cursor.rowcount
                    rows = db_cursor.fetchall()
                    self.TvCampos.delete(*self.TvCampos.get_children())
                    k=0
                    for row in rows: 
                        key = row[4]
                        Nombre = row[0]
                        tipo = row[1]
                        nulo = row[3]
                        default = row[6]
                        otro = row[5]
            
                        self.TvCampos.insert("", 'end', text=Nombre, values=(key, Nombre, tipo, nulo, default, otro)) 
                        k=k+1
                    i=0
        
                    while i< len(TABLAS):
                        print(TABLAS[i])
                        i=i+1
                except mysql.connector.Error as err:
                    showinfo("Error","Tabla inexistente, datos ingresado incorrectamente, intente de nuevo",parent=nuevaVentana)
                    return
        labeltitmodifcolumna = ttk.Label(nuevaVentana,text="Modificar columna")
        labeltitmodifcolumna.grid(column=2,row=7,padx=8,pady=4)
        labelmodifcolumna = ttk.Label(nuevaVentana,text="Columna:")
        labelmodifcolumna.grid(column=0,row=8,padx=8,pady=4)
        nombremodcolumna = ttk.Entry(nuevaVentana, width=15)
        nombremodcolumna.insert(0,"nombre")
        nombremodcolumna.grid(column=2,row=8,padx=0,pady=4)
        contenidomodcolumna = ScrolledText(nuevaVentana,width=25,height=2)
        contenidomodcolumna.grid(column=3,row=8,padx=8,pady=4)
        def modificarcolumna():
            if nombreBD.get() == "":
                showinfo("Info","Introduzca una base de datos",parent=nuevaVentana)
                return
            if nombretable.get() == "":
                showinfo("Info","Introduzca un nombre para la tabla",parent=nuevaVentana)
                return
            db_connection = mysql.connector.connect(host=self.ServerName.get(),  
            user=self.UserName.get(),  
            password=self.PassName.get())
            db_cursor = db_connection.cursor(buffered=True)
            if db_connection.is_connected() == False:  
                db_connection.connect()
            checkifexists = "SHOW DATABASES LIKE " + "'" + nombreBD.get() + "'" + ";" 
            db_cursor.execute(checkifexists)
    
            if db_cursor.fetchone() == None:
                showinfo("Info","No existe esa base de datos",parent=nuevaVentana)
                return
            else:
                usarBD = "use " + nombreBD.get() + ";"
                db_cursor.execute(usarBD)
                try:
                    alterarcolumna = "ALTER TABLE " + nombretable.get() + " MODIFY " + nombremodcolumna.get() + " " +  contenidomodcolumna.get('1.0','end-1c') + ";"
                    db_cursor.execute(alterarcolumna)
                    db_connection.commit()
                    sql = "SHOW FULL COLUMNS FROM "+ self.TablaSel.get() + " FROM " +  self.BaseSel.get()
                    db_cursor.execute(sql)
                    total = db_cursor.rowcount
                    rows = db_cursor.fetchall()
                    self.TvCampos.delete(*self.TvCampos.get_children())
                    k=0
                    for row in rows: 
                        key = row[4]
                        Nombre = row[0]
                        tipo = row[1]
                        nulo = row[3]
                        default = row[6]
                        otro = row[5]
            
                        self.TvCampos.insert("", 'end', text=Nombre, values=(key, Nombre, tipo, nulo, default, otro)) 
                        k=k+1
                    i=0
        
                    while i< len(TABLAS):
                        print(TABLAS[i])
                        i=i+1
                except mysql.connector.Error as err:
                    showinfo("Error","Tabla inexistente, datos ingresado incorrectamente, intente de nuevo",parent=nuevaVentana)
                    return
        labeltiteliminarcolumna = ttk.Label(nuevaVentana,text="Borrar columna")
        labeltiteliminarcolumna.grid(column=2,row=9,padx=8,pady=4)
        labeleliminarcolumna = ttk.Label(nuevaVentana,text="Columna:")
        labeleliminarcolumna.grid(column=0,row=10,padx=8,pady=4)
        nombreelimcolumna = ttk.Entry(nuevaVentana,width=15)
        nombreelimcolumna.insert(0,"nombre")
        nombreelimcolumna.grid(column=2,row=10,padx=0,pady=4)
        def borrarcolumna():
            if nombreBD.get() == "":
                showinfo("Info","Introduzca una base de datos",parent=nuevaVentana)
                return
            if nombretable.get() == "":
                showinfo("Info","Introduzca un nombre para la tabla",parent=nuevaVentana)
                return
            db_connection = mysql.connector.connect(host=self.ServerName.get(),  
            user=self.UserName.get(),  
            password=self.PassName.get())
            db_cursor = db_connection.cursor(buffered=True)
            if db_connection.is_connected() == False:  
                db_connection.connect()
            checkifexists = "SHOW DATABASES LIKE " + "'" + nombreBD.get() + "'" + ";" 
            db_cursor.execute(checkifexists)
    
            if db_cursor.fetchone() == None:
                showinfo("Info","No existe esa base de datos",parent=nuevaVentana)
                return
            else:
                usarBD = "use " + nombreBD.get() + ";"
                db_cursor.execute(usarBD)
                try:
                    borrarlacolumna = "ALTER TABLE " + nombretable.get() + " DROP COLUMN " + nombreelimcolumna.get() + ";"
                    db_cursor.execute(borrarlacolumna)
                    db_connection.commit()
                    sql = "SHOW FULL COLUMNS FROM "+ self.TablaSel.get() + " FROM " +  self.BaseSel.get()
                    db_cursor.execute(sql)
                    total = db_cursor.rowcount
                    rows = db_cursor.fetchall()
                    self.TvCampos.delete(*self.TvCampos.get_children())
                    k=0
                    for row in rows: 
                        key = row[4]
                        Nombre = row[0]
                        tipo = row[1]
                        nulo = row[3]
                        default = row[6]
                        otro = row[5]
            
                        self.TvCampos.insert("", 'end', text=Nombre, values=(key, Nombre, tipo, nulo, default, otro)) 
                        k=k+1
                    i=0
        
                    while i< len(TABLAS):
                        print(TABLAS[i])
                        i=i+1
                except mysql.connector.Error as err:
                    showinfo("Error","Tabla inexistente, Columna no existe, intente de nuevo",parent=nuevaVentana)
                    return
        labeltitrencolumna = ttk.Label(nuevaVentana,text="Renombrar columna")
        labeltitrencolumna.grid(column=2,row=11,padx=8,pady=4)
        labelrencolumna = ttk.Label(nuevaVentana,text="Columna:")
        labelrencolumna.grid(column=0,row=12,padx=8,pady=4)
        nombrerencolumna = ttk.Entry(nuevaVentana, width=15)
        nombrerencolumna.insert(0,"nombre")
        nombrerencolumna.grid(column=2,row=12,padx=0,pady=4)
        contenidorencolumna = ScrolledText(nuevaVentana,width=25,height=2)
        contenidorencolumna.grid(column=3,row=12,padx=8,pady=4)
        def renombrarcolumna():
            if nombreBD.get() == "":
                showinfo("Info","Introduzca una base de datos",parent=nuevaVentana)
                return
            if nombretable.get() == "":
                showinfo("Info","Introduzca un nombre para la tabla",parent=nuevaVentana)
                return
            db_connection = mysql.connector.connect(host=self.ServerName.get(),  
            user=self.UserName.get(),  
            password=self.PassName.get())
            db_cursor = db_connection.cursor(buffered=True)
            if db_connection.is_connected() == False:  
                db_connection.connect()
            checkifexists = "SHOW DATABASES LIKE " + "'" + nombreBD.get() + "'" + ";" 
            db_cursor.execute(checkifexists)
    
            if db_cursor.fetchone() == None:
                showinfo("Info","No existe esa base de datos",parent=nuevaVentana)
                return
            else:
                usarBD = "use " + nombreBD.get() + ";"
                db_cursor.execute(usarBD)
                try:
                    renombrarcolumna = "ALTER TABLE " + nombretable.get() + " CHANGE COLUMN " + nombrerencolumna.get() + " " +  contenidorencolumna.get('1.0','end-1c') + ";"
                    db_cursor.execute(renombrarcolumna)
                    db_connection.commit()
                    sql = "SHOW FULL COLUMNS FROM "+ self.TablaSel.get() + " FROM " +  self.BaseSel.get()
                    db_cursor.execute(sql)
                    total = db_cursor.rowcount
                    rows = db_cursor.fetchall()
                    self.TvCampos.delete(*self.TvCampos.get_children())
                    k=0
                    for row in rows: 
                        key = row[4]
                        Nombre = row[0]
                        tipo = row[1]
                        nulo = row[3]
                        default = row[6]
                        otro = row[5]
            
                        self.TvCampos.insert("", 'end', text=Nombre, values=(key, Nombre, tipo, nulo, default, otro)) 
                        k=k+1
                    i=0
        
                    while i< len(TABLAS):
                        print(TABLAS[i])
                        i=i+1
                except mysql.connector.Error as err:
                    showinfo("Error","Tabla inexistente, datos ingresados incorrectamente, intente de nuevo",parent=nuevaVentana)
                    return

        aplicarnuevonombre = ttk.Button(nuevaVentana,text="Cambiar",command=cambiarnombredetabla)
        aplicarnuevonombre.grid(column=4,row=4,padx=8,pady=4)
        
        aplicarcolumna = ttk.Button(nuevaVentana,text="Agregar",command=agregarcolumna)
        aplicarcolumna.grid(column=4,row=6,padx=8,pady=4)
        
        aplicarmodcolumna = ttk.Button(nuevaVentana,text="Modificar",command=modificarcolumna)
        aplicarmodcolumna.grid(column=4,row=8,padx=8,pady=4)

        eliminarcolumna = ttk.Button(nuevaVentana,text="Eliminar",command=borrarcolumna)
        eliminarcolumna.grid(column=4,row=10,padx=8,pady=4)

        renombrarcolumna = ttk.Button(nuevaVentana,text="Renombrar",command=renombrarcolumna)
        renombrarcolumna.grid(column=4,row=12,padx=8,pady=4)
        
    def ventanaeliminartabla(self):
        nuevaVentana = tk.Toplevel(self.ventana1)
        nuevaVentana.title("Eliminar tabla")
        labelnombrebd =ttk.Label(nuevaVentana,text="Nombre BD:")
        labelnombrebd.grid(column=0, row=0, padx=8, pady=8)
        nombreBD=ttk.Entry(nuevaVentana,width=40)
        nombreBD.insert(0,self.BaseSel.get())
        nombreBD.grid(column=2, row=0, padx=8, pady=4)
        labelnombretable =ttk.Label(nuevaVentana,text="Nombre Tabla:")
        labelnombretable.grid(column=0, row=2, padx=8, pady=8)
        nombretable=ttk.Entry(nuevaVentana,width=40)
        nombretable.insert(0,self.TablaSel.get())
        nombretable.grid(column=2, row=2, padx=8, pady=4)
        def eliminartabla():
            if nombreBD.get() == "":
                showinfo("Info","Introduzca una base de datos",parent=nuevaVentana)
                return
            if nombretable.get() == "":
                showinfo("Info","Introduzca un nombre para la tabla",parent=nuevaVentana)
                return
            db_connection = mysql.connector.connect(host=self.ServerName.get(),  
            user=self.UserName.get(),  
            password=self.PassName.get())
            db_cursor = db_connection.cursor(buffered=True)
            if db_connection.is_connected() == False:  
                db_connection.connect()
            checkifexists = "SHOW DATABASES LIKE " + "'" + nombreBD.get() + "'" + ";" 
            db_cursor.execute(checkifexists)
    
            if db_cursor.fetchone() == None:
                showinfo("Info","No existe esa base de datos",parent=nuevaVentana)
                return
            else:
                usarBD = "use " + nombreBD.get() + ";"
                db_cursor.execute(usarBD)
                try:
                    eliminartabla = "DROP TABLE " + nombretable.get()
                    db_cursor.execute(eliminartabla)
                    db_connection.commit()
                    self.TvCampos.delete(*self.TvCampos.get_children())
                    sql = "SHOW TABLES"  
                    db_cursor.execute(sql)
                    total = db_cursor.rowcount
                    rows = db_cursor.fetchall()
                    self.TvTablas.delete(*self.TvTablas.get_children())
                    k=0
                    TABLAS.clear()
                    for row in rows: 
                        TABLAS.append(row[0])
                        self.TvTablas.insert("", tk.END,iid=k,text=row[0]) 
                        k=k+1
                    i=0
                    self.TablaSel.delete(0,tk.END)
                    nuevaVentana.destroy()
                    nuevaVentana.update()
                except mysql.connector.Error as err:
                    showinfo("Error","Tabla inexistente, Columna no existe, intente de nuevo",parent=nuevaVentana)
                    return
        eliminartablaboton = ttk.Button(nuevaVentana,text="Eliminar",command=eliminartabla)
        eliminartablaboton.grid(column=2,row=3,padx=8,pady=4)

    def ventanaSQL(self):
        nuevaVentana = tk.Toplevel(self.ventana1)
        nuevaVentana.title("SQL")
        labelnombrebd =ttk.Label(nuevaVentana,text="Nombre BD:")
        labelnombrebd.grid(column=0, row=0, padx=8, pady=8)
        nombreBD=ttk.Entry(nuevaVentana,width=40)
        nombreBD.insert(0,self.BaseSel.get())
        nombreBD.grid(column=2, row=0, padx=8, pady=4)
        titlabelsql = ttk.Label(nuevaVentana,text="Iniciar una pregunta SQL desde el select")
        titlabelsql.grid(column=2,row=1,padx=8,pady=4)
        labelsql =ttk.Label(nuevaVentana,text="SQL:")
        labelsql.grid(column=1, row=2, padx=8, pady=8)
        sql = ScrolledText(nuevaVentana,width=30,height=15)
        sql.grid(column=2,row=2,padx=8,pady=4)
        def hacerQuery():
            if nombreBD.get() == "":
                showinfo("Info","Introduzca una base de datos",parent=nuevaVentana)
                return
            db_connection = mysql.connector.connect(host=self.ServerName.get(),  
            user=self.UserName.get(),  
            password=self.PassName.get())
            db_cursor = db_connection.cursor(buffered=True)
            if db_connection.is_connected() == False:  
                db_connection.connect()
            checkifexists = "SHOW DATABASES LIKE " + "'" + nombreBD.get() + "'" + ";" 
            db_cursor.execute(checkifexists)
    
            if db_cursor.fetchone() == None:
                showinfo("Info","No existe esa base de datos",parent=nuevaVentana)
                return
            else:
                usarBD = "use " + nombreBD.get() + ";"
                db_cursor.execute(usarBD)
                try:
                    query = "SELECT " + sql.get('1.0','end-1c')
                    db_cursor.execute(query)
                    headers = db_cursor.description
                    resultado = db_cursor.fetchall()
                    HEADERS = []
                    for x in headers:
                        HEADERS.append(x[0])
                    headersu = ""
                    for x in HEADERS:
                        headersu += x + ", "
                    headersu = headersu[:-2]
                    headersu += "= "
                    columnsu = ""
                    for x in resultado:
                        columnsu += str(x) + ", "
                    columnsu = columnsu[:-2]
                    headersu += columnsu
                    showinfo("Info",headersu,parent=nuevaVentana)
                        
                    
                except mysql.connector.Error as err:
                    showinfo("Error",err,parent=nuevaVentana)
                    return
            
        iniciarpregunta = ttk.Button(nuevaVentana,text="Preguntar",command=hacerQuery)
        iniciarpregunta.grid(column=2,row=3,padx=8,pady=4)

    def ventanaImport(self):
        nuevaVentana = tk.Toplevel(self.ventana1)
        nuevaVentana.title("SQL")
        labelnombrebd =ttk.Label(nuevaVentana,text="Nombre BD:")
        labelnombrebd.grid(column=0, row=0, padx=8, pady=8)
        nombreBD=ttk.Entry(nuevaVentana,width=40)
        nombreBD.insert(0,self.BaseSel.get())
        nombreBD.grid(column=2, row=0, padx=8, pady=4)
        labelpath = ttk.Label(nuevaVentana,text="Directorio:")
        labelpath.grid(column=0,row=1,padx=8,pady=8)
        patharchivo = ttk.Entry(nuevaVentana,width=40)
        patharchivo.insert(0,"")
        patharchivo.grid(column=2,row=1,padx=8,pady=8)
        def getfile():
            path=filedialog.askopenfilename(initialdir="/", title="Select file",filetypes=[("Structured Query Language", ".sql")],parent=nuevaVentana)
            path= path.replace("\\","//")
            patharchivo.delete(0,tk.END)
            patharchivo.insert(0,path)
        path = tk.StringVar()
        def ingresarsql():
            if nombreBD.get() == "":
                showinfo("Info","Introduzca una base de datos",parent=nuevaVentana)
                return
            variable = "C:/xampp/mysql/bin/mysql -u " + self.UserName.get() + " -p" + self.PassName.get() + " " + nombreBD.get() + " < " + patharchivo.get()
            os.system(variable)
            nuevaVentana.destroy()
            nuevaVentana.update()
        buscararchivo = ttk.Button(nuevaVentana,text="Buscar .sql",command=getfile)
        buscararchivo.grid(column=2,row=2,padx=8,pady=4)
        ingresar = ttk.Button(nuevaVentana,text="Ingresar .sql",command=ingresarsql)
        ingresar.grid(column=2,row=3,padx=8,pady=4)

    def exportarSQL(self):
        nuevaVentana = tk.Toplevel(self.ventana1)
        nuevaVentana.title("SQL")
        labelnombrebd =ttk.Label(nuevaVentana,text="Nombre BD:")
        labelnombrebd.grid(column=0, row=0, padx=8, pady=8)
        nombreBD=ttk.Entry(nuevaVentana,width=40)
        nombreBD.insert(0,self.BaseSel.get())
        nombreBD.grid(column=2, row=0, padx=8, pady=4)
        labelcarpeta = ttk.Label(nuevaVentana,text="Directorio:")
        labelcarpeta.grid(column=0, row=1,padx=8,pady=8)
        carpeta=ttk.Entry(nuevaVentana,width=40)
        carpeta.insert(0,"")
        carpeta.grid(column=2, row=1, padx=8, pady=4)
        def askdirectorio():
            path=filedialog.askdirectory(parent=nuevaVentana)
            path= path.replace("/",str("\\"))
            carpeta.delete(0,tk.END)
            carpeta.insert(0,path)
        path = tk.StringVar()
        def exportfile():
            variable = "C:/xampp/mysql/bin/mysqldump -u " + self.UserName.get() + " -p" + self.PassName.get() + " " + nombreBD.get() + " > " + "\"" + carpeta.get() + "\\" + "\"" + nombreBD.get() + ".sql"
            os.system(variable)
            texto = "Se creo el archivo en el directorio: " + carpeta.get()
            showinfo("SQL creado",texto,parent=nuevaVentana)
        creararchivo = ttk.Button(nuevaVentana,text="Exportar .sql",command=exportfile)
        creararchivo.grid(column=2,row=3,padx=8,pady=4)
        botondirectorio = ttk.Button(nuevaVentana,text="Buscar directorio",command=askdirectorio)
        botondirectorio.grid(column=2,row=2,padx=8,pady=4)
    def ventanagrande(self):
        self.ventana1.geometry("1024x800")

AdminDb1=AdminDb()
