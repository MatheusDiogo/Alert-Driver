# Projeto Alert Driver com ESP32

## Descrição

O projeto "Alert Driver" utiliza um ESP32 para controlar um buzzer e um LED com base em mensagens recebidas via MQTT. A detecção de alertas é realizada por um modelo de aprendizado de máquina, que analisa imagens capturadas pela webcam do computador.

## Materiais Necessários

- **ESP32**
- **Buzzer**
- **LED**
- **Resistores (para o LED, se necessário)**
- **Cabo USB (para conectar o ESP32 ao computador)**
- **Placa de prototipagem (opcional)**
- **Webcam**
- **Computador com Python e OpenCV instalado**
- **Conexão Wi-Fi**

![image](https://github.com/user-attachments/assets/236f185f-468f-4385-a10e-2d6088dcd62f)

## Funcionamento dos Códigos

### 1. `model.py`

Este código é executado no computador e realiza as seguintes funções:

- **Carregamento do Modelo:** O código carrega um modelo de aprendizado de máquina previamente treinado (armazenado no arquivo `keras_Model.h5`).
- **Leitura das Classes:** As classes que o modelo pode prever são lidas de um arquivo de texto (`labels.txt`).
- **Captura de Imagem:** Utiliza a webcam do computador para capturar imagens em tempo real.
- **Processamento da Imagem:** As imagens capturadas são redimensionadas para o tamanho esperado pelo modelo e normalizadas.
- **Previsão:** O modelo faz a previsão com base na imagem processada, e o código exibe no terminal a classe prevista e a pontuação de confiança.
- **Encerramento:** O loop continua até que a tecla ESC seja pressionada, momento em que o programa encerra e fecha a janela da webcam.

![image](https://github.com/user-attachments/assets/fef3d9d2-63ac-435d-b2fa-f65a1c4e99bf)

### 2. `main.py`

Este código é executado no ESP32 e realiza as seguintes funções:

- **Configuração do Wi-Fi:** Conecta o ESP32 à rede Wi-Fi usando as credenciais fornecidas.
- **Configuração do MQTT:** Conecta-se ao broker MQTT e se inscreve nos tópicos relevantes para o controle do buzzer e do LED.
- **Controle do Buzzer e LED:** Define funções para controlar o buzzer e o LED com base nas mensagens recebidas via MQTT. O buzzer pode ser ligado ou desligado, e o LED pode piscar ou parar.
- **Callback MQTT:** Recebe mensagens do broker MQTT e executa ações específicas com base no tópico e no conteúdo das mensagens.
- **Loop Principal:** Mantém a conexão com o broker MQTT e verifica continuamente se há novas mensagens para processar.

## Instruções de Uso

1. **Configuração do Ambiente:**
   - Instale as bibliotecas necessárias no computador para executar o `model.py`, incluindo `opencv-python` e `keras`.
   - Configure o ambiente MicroPython no ESP32 e carregue o código `main.py` no dispositivo.

2. **Execução do Projeto:**
   - Execute o `model.py` em um computador com uma webcam conectada para começar a capturar e processar imagens.
   - Inicie o `main.py` no ESP32 para conectar-se à rede Wi-Fi e ao broker MQTT.

3. **Testes:**
   - Verifique a funcionalidade do modelo de aprendizado de máquina observando as previsões geradas no terminal.
   - Teste o controle do buzzer e do LED enviando mensagens via MQTT e observando a resposta do ESP32.

## Licença

Este projeto está licenciado sob a [Licença MIT](https://opensource.org/licenses/MIT).
