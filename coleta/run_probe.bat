@echo off
REM Caminho fixo do Python que tem Scapy/pandas instalados (evita o stub da
REM Microsoft Store quando "python" resolve errado). Em outra maquina, ajuste
REM esse caminho (descubra com "where python").
set PYTHON_EXE=C:\Users\frede\AppData\Local\Programs\Python\Python312\python.exe

cd /d "%~dp0"
echo Coleta rodando. Deixe esta janela aberta. Feche ou Ctrl+C para parar.
"%PYTHON_EXE%" probe.py --targets 8.8.8.8 1.1.1.1 --count 20 --output "%~dp0..\dados\probes.csv" --loop-minutes 15
pause
