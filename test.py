import sys
from lexer import *
from tkinter import *
import os
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from tkinter import scrolledtext as st


def analizar_Datos():
    
    texto_Lexer.config(state="normal")
    texto_Parser.config(state="normal")
    texto_Lexer.delete('1.0',END)
    texto_Parser.delete('1.0',END)
    lexer.lineno = 0 
    respuesta_Parser.clear()
    prueba = '' 
    reunion = []
    datos =texto_Editar.get("1.0", END)
    lexer.input(datos) 
  
    while True: 
        letra = lexer.token() 
        if not letra:
            break
        reunion.append(letra) 
    for i in reunion: 

        texto_Lexer.insert(INSERT,i)
        texto_Lexer.insert(INSERT,'\n')
    texto_Lexer.config(state="disable")
    
    for linea in datos.splitlines():
        if 'SI' in linea or 'SINO' in linea or 'MIENTRAS' in linea or 'PARA' in linea or 'DO' in linea or '[' in linea or ']' in linea :
            prueba += linea
            #print(prueba) 
        else:
            contador = 0
            for i in linea:
                if i == ' ':
                    contador +=1
            if contador == len(linea) or len(linea) == 0:
                pass
            else: 
                parser.parse(linea) 
    parser.parse(prueba)
 
    for i in respuesta_Parser:
        texto_Parser.insert(INSERT,i)
        texto_Parser.insert(INSERT,'\n')
    texto_Parser.config(state="disable")
 

 
def guardar():
    nombrearch=fd.asksaveasfilename(initialdir = "/",title = "Guardar como",filetypes = ((".txt files","*.txt"),("todos los archivos","*.*")))
    if nombrearch!='':
        archivo=open(nombrearch, "w", encoding="utf-8")
        archivo.write(texto_Editar.get("1.0", END))
        archivo.close()
        mb.showinfo("Información", "Los datos fueron guardados en el archivo.")

def abrir_Archivo():
    nombrearch=fd.askopenfilename(initialdir = "/",title = "Seleccione archivo",filetypes = ((".txt files","*.txt"),("todos los archivos","*.*")))
    if nombrearch!='':
        casa = str(nombrearch)
        casa2 = casa.split('/')
        print(casa2)
        casa3 = len(casa2)-1
        nombreFalso = '' 
        for i in range(0,casa3):
                nombreFalso += (casa2[i]+'/')
        nombreFalso+='falso.txt'
        print(nombreFalso) 
        os.rename(nombrearch,nombreFalso)
        archi1=open(nombreFalso, "r", encoding="utf-8")
        contenido=archi1.read()
        archi1.close() 
        texto_Editar.delete("1.0", END) 
        texto_Editar.insert("1.0", contenido)
        os.rename(nombreFalso,nombrearch)


 
# Creacion de la Ventana y modificacion de las dimensiones y titulo.
ventana = Tk()
ventana.title("Lenguaje")
ventana.geometry('602x560')
ventana.config(background="#e4fdfe") 
#---------------------------------


# Titulo y Cuadro de Texto en el cual se colocara el codigo.
titulo_Codigo = Label(ventana, text="Escribir Codigo:")
titulo_Codigo.place(x=1, y=40)
titulo_Codigo.config(font=("Courier",15 ))

texto_Editar = st.ScrolledText(ventana)
texto_Editar.place(x=1,y=70,width=600,height=320)
texto_Editar.config(background="#74f19b")

 


# Titulo y Cuadro donde se imprimira el Parser.


 
texto_Parser = st.ScrolledText(ventana) 
texto_Parser.place(x=1,y=393,width=600,height=160)
texto_Parser.config(state="disable",background="#74f19b")
#------------------------------------------------------------

#---------------------------------------------------
#Titulo y Cuadro donde se imprimira el Lexer.
titulo_lexer = Label(ventana, text="Analizador Lexer:")
titulo_lexer.place(x=640, y=70)
titulo_lexer.config(font=("Courier",15 ))
 
texto_Lexer = st.ScrolledText(ventana)
#texto_Lexer.place(x=550,y=100,width=400,height=220)
texto_Lexer.config(state="disable")
#---------------------------------------------------------

boton_CargarArchivo =  Button(ventana, text="Abrir Archivo",command=abrir_Archivo)
boton_CargarArchivo.place(x=1,y=10)

boton_Analizar =  Button(ventana, text="Analizar",command=analizar_Datos)
boton_Analizar.place(x=160,y=10)

boton_Guardar = Button(ventana,text="Guardar", command=guardar)
boton_Guardar.place(x=90,y=10)

ventana.mainloop()     
