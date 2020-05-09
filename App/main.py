import tkinter as tk
from os import environ as env
import requests
import socket

class LoginScreen(tk.Frame):
    def __init__(self,parent):
        super(LoginScreen,self).__init__(parent)
        self.userString = tk.StringVar()
        self.passwordString = tk.StringVar()

        try:
            with open(env["TEMP"] + "\ProgramaReferenciaTextLoginFile.txt", "r") as file:
                self.isLoged = True
        except IOError:
            self.isLoged = False

        if self.isLoged:
            self.label = tk.Label(self,text="Logado com Sucesso!!!")
            self.label.pack(padx=20,pady=20)
            self.button = tk.Button(self,text="Fechar",command=self.CloseLoginScreen())
            self.button.pack(padx=20,pady=20)
        else:
            self.label = tk.Label(self,text="Fazer Login")
            self.label.pack(padx=20,pady=20)
            self.labelUser = tk.Label(self,text="Usuario")
            self.labelUser.pack(padx=20)
            self.textInputUser = tk.Entry(self,textvariable=self.userString)
            self.textInputUser.pack(padx=20)
            self.labelPassword = tk.Label(self,text="Senha")
            self.labelPassword.pack(padx=20)
            self.textInputPassword = tk.Entry(self,textvariable=self.passwordString)
            self.textInputPassword.pack(padx=20)
            self.buttonLogin = tk.Button(self,text="Logar",command=self.TentarLogin)
            self.buttonLogin.pack(padx=20)

    def CloseLoginScreen(self):
        self.destroy()

    def TentarLogin(self):
        IP = socket.gethostbyname(socket.gethostname())
        url = IP + "/login/?user=" + self.userString.get() + "&password=" + self.passwordString.get()
        response = requests.get(url)

        if response == "Login Negado":
            self.isLoged = False
        else:
            self.isLoged = True
            self.destroy()

root = tk.Tk()

main = LoginScreen(root)
main.pack(fill="both",expand=True)

root.mainloop()