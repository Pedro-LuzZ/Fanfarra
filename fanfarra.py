import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import os
import platform
import subprocess

class FanfarraApp:
    # Constantes para habilidades e estado inicial
    INITIAL_FANFARRA = 0
    REVIVER_COST_TYPE = "toda fanfarra" # Descritivo, não usado numericamente diretamente
    NEGACAO_COST = 1000
    INITIAL_NEGACAO_USOS = 2  # Ajustado para corresponder à mensagem
    SEQUENCIA_COST = 250
    INITIAL_SEQUENCIA_USOS = 10 # Ajustado para corresponder à mensagem

    # Cores pastéis
    COR_FUNDO = "#fef2cc"
    COR_BOTAO = "#ffb3b3"
    COR_BOTAO_ATIVO = "#ff6666" # Cor ao passar o mouse/ativo
    COR_TEXTO = "#333333"
    COR_ENTRADA_FUNDO = "#ffffff"

    def __init__(self, master):
        self.master = master
        master.title("Gerenciador de Fanfarra - Théo Brasidas")
        master.config(bg=self.COR_FUNDO)

        # Estado da aplicação
        self.fanfarra = self.INITIAL_FANFARRA
        self.reviver_usado = False
        self.negacao_usos = self.INITIAL_NEGACAO_USOS
        self.sequencia_usos = self.INITIAL_SEQUENCIA_USOS

        # Configurar estilo ttk
        self.style = ttk.Style()
        self.style.configure("TButton",
                             font=("Arial", 12),
                             padding=10,
                             relief="flat",
                             background=self.COR_BOTAO,
                             foreground=self.COR_TEXTO,
                             # focuscolor pode ser ajustado para melhor visibilidade do foco
                             # se a cor do botão for a mesma, o foco pode não ser óbvio.
                             # Ex: focuscolor=self.COR_TEXTO ou uma cor de destaque
                             focuscolor=self.COR_BOTAO)
        self.style.map("TButton",
                       background=[("active", self.COR_BOTAO_ATIVO)])

        # --- Widgets ---
        # Botão Abrir PDF
        self.btn_abrir_pdf = ttk.Button(master, text="Abrir PDF", command=self.abrir_pdf)
        self.btn_abrir_pdf.pack(pady=10, anchor='ne', padx=10) # Ancorado no canto superior direito

        # Exibição da Fanfarra
        self.label_fanfarra = tk.Label(master, text=f"Fanfarra Atual: {self.fanfarra}",
                                       font=("Arial", 16, "bold"), bg=self.COR_FUNDO, fg=self.COR_TEXTO)
        self.label_fanfarra.pack(pady=(5, 10)) # Mais espaço antes do próximo elemento

        # Frame para entrada de dano
        frame_dano = tk.Frame(master, bg=self.COR_FUNDO)
        frame_dano.pack(pady=5)

        self.label_entry_dano = tk.Label(frame_dano, text="Dano:", font=("Arial", 12),
                                         bg=self.COR_FUNDO, fg=self.COR_TEXTO)
        self.label_entry_dano.pack(side=tk.LEFT, padx=(0,5))

        self.entry_dano = tk.Entry(frame_dano, font=("Arial", 12), width=10,
                                   bg=self.COR_ENTRADA_FUNDO, fg=self.COR_TEXTO)
        self.entry_dano.pack(side=tk.LEFT, padx=5)
        self.entry_dano.bind("<Return>", lambda event: self.adicionar_dano())

        self.btn_add_dano = ttk.Button(frame_dano, text="Adicionar Dano",
                                       command=self.adicionar_dano)
        self.btn_add_dano.pack(side=tk.LEFT, padx=5)

        # Frame para botões de habilidades
        frame_habilidades = tk.Frame(master, bg=self.COR_FUNDO)
        frame_habilidades.pack(pady=10)

        self.btn_reviver = ttk.Button(frame_habilidades,
                                      text=f"Usar Reviver ({self.REVIVER_COST_TYPE})",
                                      command=self.usar_reviver)
        self.btn_reviver.pack(pady=5, fill=tk.X)

        self.btn_negacao = ttk.Button(frame_habilidades,
                                      text=self._get_negacao_text(),
                                      command=self.usar_negacao)
        self.btn_negacao.pack(pady=5, fill=tk.X)

        self.btn_sequencia = ttk.Button(frame_habilidades,
                                        text=self._get_sequencia_text(),
                                        command=self.usar_sequencia)
        self.btn_sequencia.pack(pady=5, fill=tk.X)

        # Botão de reset
        self.btn_reset = ttk.Button(master, text="Resetar Luta", command=self.resetar_luta, style="TButton") # Garante o estilo
        self.btn_reset.pack(pady=20)

        self.atualizar_interface() # Atualiza estado inicial dos botões

    def _get_negacao_text(self):
        return f"Usar Negação ({self.NEGACAO_COST}) - Restantes: {self.negacao_usos}"

    def _get_sequencia_text(self):
        return f"Usar Sequência ({self.SEQUENCIA_COST}) - Restantes: {self.sequencia_usos}"

    def atualizar_interface(self):
        self.label_fanfarra.config(text=f"Fanfarra Atual: {self.fanfarra}")
        self.btn_negacao.config(text=self._get_negacao_text())
        self.btn_sequencia.config(text=self._get_sequencia_text())
        self.btn_reviver.config(state="disabled" if self.reviver_usado else "normal")

    def adicionar_dano(self):
        try:
            dano = int(self.entry_dano.get())
            if dano > 0:
                self.fanfarra += dano
                self.entry_dano.delete(0, tk.END)
                self.atualizar_interface()
            else:
                messagebox.showwarning("Valor Inválido", "O dano deve ser um número positivo.")
        except ValueError:
            messagebox.showerror("Erro de Entrada", "Digite um valor numérico válido para o dano.")
        self.entry_dano.focus_set() # Devolve o foco para o campo de entrada

    def usar_reviver(self):
        if self.reviver_usado: # Já foi usado, não deveria ser clicável, mas verificamos.
            messagebox.showinfo("Habilidade Usada", "Reviver já foi utilizado nesta luta.")
            return

        if self.fanfarra > 0:
            confirmar = messagebox.askyesno("Confirmar Reviver",
                                            f"Você tem {self.fanfarra} de Fanfarra. Deseja usar Reviver e zerar a Fanfarra?")
            if confirmar:
                self.fanfarra = 0
                self.reviver_usado = True
                messagebox.showinfo("Reviver", "Reviver utilizado! Fanfarra zerada.")
                self.atualizar_interface()
        else:
            messagebox.showwarning("Sem Fanfarra", "Você não tem fanfarra para usar Reviver.")

    def usar_negacao(self):
        if self.negacao_usos <= 0:
            messagebox.showwarning("Limite Atingido",
                                   f"Você já usou Negação à Morte o máximo de {self.INITIAL_NEGACAO_USOS} vezes nesta luta.")
            return
        if self.fanfarra >= self.NEGACAO_COST:
            self.fanfarra -= self.NEGACAO_COST
            self.negacao_usos -= 1
            messagebox.showinfo("Negação à Morte", f"Negação à Morte utilizada! Fanfarra restante: {self.fanfarra}")
            self.atualizar_interface()
        else:
            messagebox.showwarning("Fanfarra Insuficiente",
                                   f"Fanfarra insuficiente para Negação à Morte. Necessário: {self.NEGACAO_COST}")

    def usar_sequencia(self):
        if self.sequencia_usos <= 0:
            messagebox.showwarning("Limite Atingido",
                                   f"Você já usou Sequência da Deusa o máximo de {self.INITIAL_SEQUENCIA_USOS} vezes nesta luta.")
            return
        if self.fanfarra >= self.SEQUENCIA_COST:
            self.fanfarra -= self.SEQUENCIA_COST
            self.sequencia_usos -= 1
            messagebox.showinfo("Sequência da Deusa", f"Sequência da Deusa utilizada! Fanfarra restante: {self.fanfarra}")
            self.atualizar_interface()
        else:
            messagebox.showwarning("Fanfarra Insuficiente",
                                   f"Fanfarra insuficiente para Sequência da Deusa. Necessário: {self.SEQUENCIA_COST}")

    def resetar_luta(self):
        confirmar = messagebox.askyesno("Resetar Luta", "Tem certeza que deseja resetar todos os valores da luta?")
        if confirmar:
            self.fanfarra = self.INITIAL_FANFARRA
            self.reviver_usado = False
            self.negacao_usos = self.INITIAL_NEGACAO_USOS
            self.sequencia_usos = self.INITIAL_SEQUENCIA_USOS
            self.atualizar_interface()
            messagebox.showinfo("Luta Resetada", "Os valores da luta foram resetados.")

    def abrir_pdf(self):
        caminho_arquivo = filedialog.askopenfilename(
            title="Selecione um arquivo PDF",
            filetypes=[("Arquivos PDF", "*.pdf"), ("Todos os arquivos", "*.*")]
        )
        if caminho_arquivo:
            try:
                if platform.system() == "Windows":
                    os.startfile(caminho_arquivo)
                elif platform.system() == "Darwin":  # macOS
                    subprocess.run(["open", caminho_arquivo], check=True)
                else:  # Linux e outros
                    subprocess.run(["xdg-open", caminho_arquivo], check=True)
            except FileNotFoundError:
                messagebox.showerror("Erro", f"O arquivo não foi encontrado: {caminho_arquivo}")
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Erro ao Abrir", f"Não foi possível abrir o PDF com o visualizador padrão.\nErro: {e}")
            except Exception as e:
                messagebox.showerror("Erro Desconhecido", f"Não foi possível abrir o PDF.\nErro: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FanfarraApp(root)
    # Define um tamanho mínimo para a janela para melhor visualização inicial
    root.minsize(400, 500)
    root.mainloop()