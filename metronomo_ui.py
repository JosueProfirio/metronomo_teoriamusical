import tkinter as tk
from tkinter import ttk, filedialog
import os
from metronomo import Metronomo  # sua classe Metronomo

def abrir_metronomo():
    # --- Janela principal do metrônomo ---
    met_win = tk.Tk()
    met_win.title("Metrônomo Profissional")
    met_win.geometry("550x650")

    # --- Variáveis ---
    bpm_var = tk.IntVar(value=120)
    compasso_var = tk.IntVar(value=4)
    volume_var = tk.DoubleVar(value=0.5)
    circulos = []

    # --- Frame visual dos tempos ---
    frame_visual = tk.Frame(met_win)
    frame_visual.pack(pady=20)

    def atualizar_tempo_atual(tempo):
        for i, c in enumerate(circulos):
            c.config(fg="gray")
            if i == tempo - 1:
                c.config(fg="red")

    # --- Instância do metrônomo ---
    metronomo = Metronomo(callback_visual=atualizar_tempo_atual)

    # --- BPM ---
    tk.Label(met_win, text="BPM", font=("Arial", 12)).pack()
    tk.Scale(met_win, from_=30, to=240, orient="horizontal", variable=bpm_var,
             command=lambda val: metronomo.set_bpm(int(val))).pack()

    # --- Compassos ---
    tk.Label(met_win, text="Compassos", font=("Arial", 12)).pack()
    compasso_menu = ttk.Combobox(met_win, textvariable=compasso_var,
                                 values=[2, 3, 4, 6], state="readonly")  # compassos mais comuns
    compasso_menu.pack()

    def atualizar_compasso(event=None):
        metronomo.set_compasso(compasso_var.get())
        # Reinicia os círculos
        for c in circulos:
            c.destroy()
        circulos.clear()
        for i in range(compasso_var.get()):
            lbl = tk.Label(frame_visual, text="●", font=("Arial", 24), fg="gray")
            lbl.pack(side="left", padx=5)
            circulos.append(lbl)
        # Sempre reinicia do tempo 0
        metronomo.reset_tempo()

    compasso_menu.bind("<<ComboboxSelected>>", atualizar_compasso)
    atualizar_compasso()

    # --- Volume ---
    tk.Label(met_win, text="Volume", font=("Arial", 12)).pack()
    tk.Scale(met_win, from_=0, to=1, resolution=0.1, orient="horizontal",
             variable=volume_var,
             command=lambda val: metronomo.set_volume(float(val))).pack()

    # --- Sons disponíveis ---
    frame_sons = tk.Frame(met_win)
    frame_sons.pack(pady=20)

    tk.Label(frame_sons, text="Som Forte:", font=("Arial", 11)).grid(row=0, column=0, padx=5, sticky="e")
    tk.Label(frame_sons, text="Som Fraco:", font=("Arial", 11)).grid(row=1, column=0, padx=5, sticky="e")

    pasta_sons = os.path.join(os.path.dirname(__file__), "sons")
    if not os.path.exists(pasta_sons):
        os.makedirs(pasta_sons)

    def listar_sons():
        return [f for f in os.listdir(pasta_sons) if f.endswith(".wav")]

    sons_disponiveis = listar_sons()
    combo_forte = ttk.Combobox(frame_sons, values=sons_disponiveis, state="readonly", width=30)
    combo_forte.set("Escolha um novo som")

    combo_fraco = ttk.Combobox(frame_sons, values=sons_disponiveis, state="readonly", width=30)
    combo_fraco.set("Escolha um novo som")
    
    combo_forte.grid(row=0, column=1, padx=5)
    combo_fraco.grid(row=1, column=1, padx=5)

    def aplicar_som_forte(event=None):
        if combo_forte.get():
            caminho = os.path.join(pasta_sons, combo_forte.get())
            metronomo.set_som_tempo1(caminho)

    def aplicar_som_fraco(event=None):
        if combo_fraco.get():
            caminho = os.path.join(pasta_sons, combo_fraco.get())
            metronomo.set_som_outros(caminho)

    combo_forte.bind("<<ComboboxSelected>>", aplicar_som_forte)
    combo_fraco.bind("<<ComboboxSelected>>", aplicar_som_fraco)

    def escolher_som_forte():
        path = filedialog.askopenfilename(title="Escolher som FORTE", filetypes=[("WAV files", "*.wav")])
        if path:
            metronomo.set_som_tempo1(path)

    def escolher_som_fraco():
        path = filedialog.askopenfilename(title="Escolher som FRACO", filetypes=[("WAV files", "*.wav")])
        if path:
            metronomo.set_som_outros(path)

    tk.Button(frame_sons, text="📂 Abrir Forte", command=escolher_som_forte).grid(row=0, column=2, padx=5)
    tk.Button(frame_sons, text="📂 Abrir Fraco", command=escolher_som_fraco).grid(row=1, column=2, padx=5)

    # --- Botões de controle ---
    tk.Button(met_win, text="Iniciar", command=lambda: metronomo.start(met_win),
              bg="green", fg="white", font=("Arial", 12, "bold")).pack(pady=10)
    tk.Button(met_win, text="Parar", command=metronomo.stop,
              bg="red", fg="white", font=("Arial", 12, "bold")).pack(pady=10)

    # --- Atalhos ---
    bind_atual = "Nenhum"

    frame_atalho = tk.Frame(met_win)
    frame_atalho.pack(pady=10)

    lbl_atalho = tk.Label(frame_atalho, text=f"Atalho atual: {bind_atual}", fg="black")
    lbl_atalho.grid(row=0, column=0, padx=5)

    def toggle_metronomo(event=None):
        if metronomo.is_running:
            metronomo.stop()
        else:
            metronomo.start(met_win)

    def aguardar_tecla_para_atalho():
        lbl_atalho.config(text="Pressione a tecla ou combinação...", fg="blue")

        def capturar_tecla(event):
            nonlocal bind_atual
            # Remove bind antigo
            met_win.unbind_all(bind_atual)

            mods = []
            if event.state & 0x4:  # Control
                mods.append("Control")
            if event.state & 0x1:  # Shift
                mods.append("Shift")
            if event.state & 0x20000:  # Alt
                mods.append("Alt")

            key = event.keysym
            tk_format = "<" + "-".join(mods + [key]) + ">" if mods else f"<{key}>"
            bind_atual = tk_format

            met_win.bind_all(tk_format, toggle_metronomo)
            lbl_atalho.config(text=f"Atalho atual: {tk_format}", fg="black")
            met_win.unbind_all("<Key>")

        met_win.bind_all("<Key>", capturar_tecla)

    tk.Button(frame_atalho, text="Alterar Atalho", command=aguardar_tecla_para_atalho,
              bg="red", fg="white", font=("Arial", 12, "bold")).grid(row=0, column=1, padx=5)

    met_win.mainloop()


# --- Executa o metrônomo direto ---
if __name__ == "__main__":
    abrir_metronomo()
