@echo off
cd /d "%~dp0"
python probe.py --targets 8.8.8.8 1.1.1.1 --count 20 --output "%~dp0..\dados\probes.csv"
