# Monitor de Qualidade do Ar com Flask

## Descrição do Projeto

O projeto consiste em um sistema de monitoramento da qualidade do ar que utiliza um microcontrolador ESP32 simulado no Wokwi para coletar dados de sensores de CO2 e PM2.5, e acionar atuadores como relés e motores para controlar a ventilação do ambiente. Os dados são transmitidos via MQTT para uma aplicação web que exibe as informações em tempo real e permite o controle manual dos atuadores, além de fornecer um histórico dos dados coletados, armazenados em um banco de dados MySQL.

## Tecnologias Utilizadas

### Hardware

* Simulador de ESP32 Wokwi
* Sensores de CO2 e PM2.5 (simulados)
* Relés para acionamento de ventiladores (simulados)
* Motores para abrir e fechar janelas (simulados)

### Software

* Linguagem de programação Python para o ESP32 (MicroPython)
* Biblioteca MQTT para comunicação com o broker
* Framework Flask para a aplicação web
* HTML, CSS e JavaScript para a interface web
* Banco de dados MySQL para armazenar o histórico de dados
* Bibliotecas Python adicionais: Flask-MQTT, Flask-Login, Flask-User, etc.

## Funcionalidades do Sistema

* Coleta de dados de CO2 e PM2.5 em tempo real (simulados)
* Transmissão de dados via MQTT
* Visualização de dados em tempo real na aplicação web
* Acionamento automático de ventiladores e motores em caso de níveis críticos de CO2 ou PM2.5 (simulados)
* Controle manual dos atuadores pela interface web (simulados)
* Registro do histórico de dados no banco de dados MySQL
* Interface web com gráficos para visualizar o histórico de dados
* Autenticação de usuários para acesso à aplicação web

## Estrutura do Projeto

* `controllers`: Contém os controladores da aplicação Flask, responsáveis por receber as requisições e retornar as respostas.
* `models`: Contém as classes que representam as tabelas do banco de dados.
* `static`: Contém os arquivos estáticos da aplicação web, como CSS, JavaScript e imagens.
* `templates`: Contém os templates HTML da aplicação web.
* `utils`: Contém scripts auxiliares, como o script para criar o banco de dados.
* `esp32_wokwi_code`: Contém o código Python para o ESP32 simulado no Wokwi.
