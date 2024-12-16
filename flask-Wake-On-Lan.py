import tkinter as tk
from tkinter import messagebox, Menu, scrolledtext, filedialog
from wakeonlan import send_magic_packet
from flask import Flask, request, render_template_string
import threading
import logging

# Configurar logging
logging.basicConfig(filename="note.log", level=logging.INFO, format="%(asctime)s - %(message)s")

# Criar a aplicação Flask
app = Flask(__name__)

# Página inicial do Flask
template_html = '''
<!DOCTYPE html>
<html>
<head>
    <title>Wake-on-LAN</title>
</head>
<body>
    <h1>Wake-on-LAN</h1>
    <form method="POST" action="/despertar">
        <label for="mac">Endereço MAC:</label>
        <input type="text" id="mac" name="mac" required><br><br>
        <button type="submit">Despertar</button>
    </form>
</body>
</html>
'''

@app.route("/")
def index():
    return render_template_string(template_html)

@app.route("/despertar", methods=["POST"])
def despertar():
    mac = request.form.get("mac")
    if mac:
        try:
            send_magic_packet(mac)
            logging.info(f"Pacote Wake-on-LAN enviado para: {mac}")
            return f"Pacote enviado para {mac}", 200
        except Exception as e:
            logging.error(f"Erro ao enviar pacote para {mac}: {e}")
            return f"Erro: {e}", 500
    return "MAC address é obrigatório", 400

# Função para iniciar o servidor Flask em uma thread separada
def iniciar_flask(host, port):
    app.run(host=host, port=port, debug=False)

# Função para enviar o pacote Wake-on-LAN
def wake_on_lan(mac_address):
    try:
        send_magic_packet(mac_address)
        log_mensagem = f"Pacote Wake-on-LAN enviado para: {mac_address}"
        logging.info(log_mensagem)
        exibir_log(log_mensagem)
    except Exception as e:
        log_mensagem = f"Erro ao enviar o pacote: {e}"
        logging.error(log_mensagem)
        exibir_log(log_mensagem)

# Função para exibir mensagens de log na interface gráfica
def exibir_log(mensagem):
    log_text.config(state="normal")
    log_text.insert(tk.END, mensagem + "\n")
    log_text.config(state="disabled")
    log_text.see(tk.END)

# Função para iniciar o Flask
def iniciar_servidor():
    host = entry_host.get()
    port = entry_port.get()
    if not host or not port:
        messagebox.showwarning("Atenção", "Por favor, insira o host e a porta.")
        return
    try:
        threading.Thread(target=iniciar_flask, args=(host, int(port)), daemon=True).start()
        exibir_log(f"Servidor Flask iniciado em {host}:{port}")
    except Exception as e:
        exibir_log(f"Erro ao iniciar o servidor Flask: {e}")

# Função para sair da aplicação
def sair():
    janela.destroy()

# Criar a janela principal
janela = tk.Tk()
janela.title("Wake-on-LAN GUI")
janela.geometry("600x400")

# Criar o menu
menu_bar = Menu(janela)
menu_arquivo = Menu(menu_bar, tearoff=0)
menu_arquivo.add_command(label="Sair", command=sair)
menu_bar.add_cascade(label="Ficheiro", menu=menu_arquivo)
janela.config(menu=menu_bar)

# Rótulos e campos de entrada para Flask
label_host = tk.Label(janela, text="Host do Flask:")
label_host.pack(pady=5)
entry_host = tk.Entry(janela, width=30)
entry_host.pack(pady=5)

label_port = tk.Label(janela, text="Porta do Flask:")
label_port.pack(pady=5)
entry_port = tk.Entry(janela, width=30)
entry_port.pack(pady=5)

botao_iniciar_servidor = tk.Button(janela, text="Iniciar Flask", command=iniciar_servidor)
botao_iniciar_servidor.pack(pady=10)

# Rótulos e campos de entrada para Wake-on-LAN
label_ip = tk.Label(janela, text="Endereço IP (opcional):")
label_ip.pack(pady=5)
entry_ip = tk.Entry(janela, width=30)
entry_ip.pack(pady=5)

label_mac = tk.Label(janela, text="Endereço MAC:")
label_mac.pack(pady=5)
entry_mac = tk.Entry(janela, width=30)
entry_mac.pack(pady=5)

botao_ligar = tk.Button(janela, text="Despertar PC", command=lambda: wake_on_lan(entry_mac.get()))
botao_ligar.pack(pady=10)

# Área de log
log_text = scrolledtext.ScrolledText(janela, width=70, height=10, state="disabled")
log_text.pack(pady=10)

# Botão de sair
botao_sair = tk.Button(janela, text="Sair", command=sair)
botao_sair.pack(pady=10)

# Iniciar o loop principal da interface
janela.mainloop()
