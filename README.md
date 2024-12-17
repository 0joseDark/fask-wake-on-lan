# fask-wake-on-lan
 usa o servidor flask e web page para "wake-on-lan" despertar um pc
 - O script foi atualizado para incluir as seguintes funcionalidades:

1. **Servidor Flask**: Permite controlar o envio de pacotes Wake-on-LAN através de uma página web.
2. **Interface gráfica (GUI)**: Inclui campos para configurar o host e porta do Flask, além de enviar pacotes Wake-on-LAN localmente.
3. **Log**: Exibe mensagens na interface e salva em um arquivo `note.log`.
4. **Botões e menu**: Incluem botões para iniciar o servidor Flask, enviar pacotes e sair.

Certifique-se de instalar os módulos necessários antes de executar:

```bash
pip install wakeonlan flask
``` 

Explicação passo a passo:
1. A aplicação Flask serve uma página web para enviar pacotes Wake-on-LAN remotamente.
2. A interface gráfica em tkinter permite configurar o host e porta do Flask, além de enviar pacotes Wake-on-LAN localmente.
3. O campo de log exibe mensagens sobre ações realizadas e salva-as no arquivo "note.log".
4. O servidor Flask é executado em uma thread separada para não bloquear a interface gráfica.
5. O botão "Despertar PC" permite enviar o pacote mágico diretamente da GUI.
- - Press CTRL+C to quit

