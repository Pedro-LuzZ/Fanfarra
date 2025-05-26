import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
import os
import platform
import subprocess


class FanfarraApp:
    def __init__(self, master):
        self.btn_abrir_pdf = ttk.Button(master, text="Abrir PDF", command=self.abrir_pdf)
        self.btn_abrir_pdf.pack(pady=10)
        self.master = master
        master.title("Gerenciador de Fnfarra - Théo Brasidas")

        # Estado inicial
        self.fanfarra = 0
        self.reviver_usado = False
        self.negacao_usos = 200
        self.sequencia_usos = 100

        # Cores pastéis
        self.fundo = "#fef2cc"  
        self.cor_botao = "#ffb3b3"  
        self.cor_texto = "#333333"  

        # Personalizar estilo dos botões com ttk
        self.style = ttk.Style()
        self.style.configure("TButton",
                             font=("Arial", 12),
                             padding=10,
                             relief="flat",
                             background=self.cor_botao,
                             foreground=self.cor_texto,
                             focuscolor=self.cor_botao)
        self.style.map("TButton",
                       background=[("active", "#ff6666")])  # Cor ao passar o mouse

        # Exibição da Fanfarra
        self.label_fanfarra = tk.Label(master, text=f"Fanfarra Atual: {self.fanfarra}", font=("Arial", 14), bg=self.fundo, fg=self.cor_texto)
        self.label_fanfarra.pack(pady=10)

        # Campo para adicionar dano
        self.entry_dano = tk.Entry(master, font=("Arial", 12), bg="#ffffff", fg=self.cor_texto)
        self.entry_dano.bind("<Return>", lambda event: self.adicionar_dano())
        self.btn_add_dano = ttk.Button(master, text="Adicionar Dano", command=self.adicionar_dano)
        self.btn_add_dano.pack(pady=5)
        self.entry_dano.pack()

        self.btn_add_dano = ttk.Button(master, text="Adicionar Dano", command=self.adicionar_dano)
        self.btn_add_dano.pack(pady=5)

        # Botões de habilidades
        self.btn_reviver = ttk.Button(master, text="Usar Reviver (toda fanfarra)", command=self.usar_reviver)
        self.btn_reviver.pack(pady=5)

        self.btn_negacao = ttk.Button(master, text=f"Usar Negação à Morte (1000) - Restantes: {self.negacao_usos}", command=self.usar_negacao)
        self.btn_negacao.pack(pady=5)

        self.btn_sequencia = ttk.Button(master, text=f"Usar Sequência da Deusa (250) - Restantes: {self.sequencia_usos}", command=self.usar_sequencia)
        self.btn_sequencia.pack(pady=5)

        # Botão de reset
        self.btn_reset = ttk.Button(master, text="Resetar Luta", command=self.resetar_luta)
        self.btn_reset.pack(pady=10)

        # Cor de fundo da janela
        master.config(bg=self.fundo)

    def atualizar_interface(self):
        self.label_fanfarra.config(text=f"Fanfarra Atual: {self.fanfarra}")
        self.btn_negacao.config(text=f"Usar Negação à Morte (1000) - Restantes: {self.negacao_usos}")
        self.btn_sequencia.config(text=f"Usar Sequência da Deusa (250) - Restantes: {self.sequencia_usos}")
        self.btn_reviver.config(state="disabled" if self.reviver_usado else "normal")

    def adicionar_dano(self):
        try:
            dano = int(self.entry_dano.get())
            if dano > 0:
                self.fanfarra += dano
                self.entry_dano.delete(0, tk.END)
                self.atualizar_interface()
        except ValueError:
            messagebox.showerror("Erro", "Digite um valor válido de dano.")

            

    def usar_reviver(self):
        if not self.reviver_usado:
            if self.fanfarra > 0:
                self.fanfarra = 0
                self.reviver_usado = True
                self.atualizar_interface()
            else:
                messagebox.showwarning("Sem Fanfarra", "Você não tem fanfarra suficiente para reviver.")

    def usar_negacao(self):
        if self.negacao_usos > 0 and self.fanfarra >= 1000:
            self.fanfarra -= 1000
            self.negacao_usos -= 1
            self.atualizar_interface()
        elif self.negacao_usos <= 0:
            messagebox.showwarning("Limite atingido", "Você já usou a Negação à Morte 2 vezes nesta luta.")
        else:
            messagebox.showwarning("Sem Fanfarra", "Fanfarra insuficiente.")

    def usar_sequencia(self):
        if self.sequencia_usos > 0 and self.fanfarra >= 250:
            self.fanfarra -= 250
            self.sequencia_usos -= 1
            self.atualizar_interface()
        elif self.sequencia_usos <= 0:
            messagebox.showwarning("Limite atingido", "Você já usou a Sequência da Deusa 10 vezes nesta luta.")
        else:
            messagebox.showwarning("Sem Fanfarra", "Fanfarra insuficiente.")

    def resetar_luta(self):
        self.fanfarra = 0
        self.reviver_usado = False
        self.negacao_usos = 200
        self.sequencia_usos = 100
        self.atualizar_interface()

    def abrir_pdf(self):
        caminho_arquivo = filedialog.askopenfilename(
            title="Selecione um arquivo PDF",
            filetypes=[("Arquivos PDF", "*.pdf")]
        )
        if caminho_arquivo:
            try:
                if platform.system() == "Windows":
                    os.startfile(caminho_arquivo)
                elif platform.system() == "Darwin":  # macOS
                    subprocess.run(["open", caminho_arquivo])
                else:  # Linux
                    subprocess.run(["xdg-open", caminho_arquivo])
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível abrir o PDF.\nErro: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = FanfarraApp(root)
    root.mainloop()
