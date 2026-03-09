import MetaTrader5 as mt5
import os
import sys

def debug():
    print("--- DIAGNÓSTICO PROFISSIONAL MT5 ---")
    print(f"Python: {sys.version}")
    print(f"Versão MT5 Lib: {mt5.__version__}")
    
    # Lista de locais onde o MetaTrader da BTG costuma ser instalado
    possiveis_caminhos = [
        "C:\\Program Files\\Banco BTG Pactual MetaTrader 5\\terminal64.exe",
        "C:\\Program Files\\BTG Pactual MetaTrader 5\\terminal64.exe",
        "C:\\Program Files\\MetaTrader 5\\terminal64.exe",
    ]
    
    sucesso = False
    for path in possiveis_caminhos:
        if os.path.exists(path):
            print(f"\nTentando abrir via: {path}")
            if mt5.initialize(path=path, timeout=60000):
                print("✅ SUCESSO! Conectado com sucesso através do caminho específico.")
                acc = mt5.account_info()
                if acc:
                    print(f"💰 Conta: {acc.login} | Corretora: {acc.company}")
                mt5.shutdown()
                sucesso = True
                break
            else:
                print(f"❌ Falha ao inicializar este caminho: {mt5.last_error()}")
        else:
            print(f"--- Caminho não encontrado: {path}")

    if not sucesso:
        print("\nTentando inicialização padrão (sem caminho)...")
        if mt5.initialize(timeout=60000):
            print("✅ SUCESSO! Conexão padrão funcionou.")
            mt5.shutdown()
        else:
            print(f"❌ Falha total. Erro final: {mt5.last_error()}")
            print("\nSUGESTÃO: Reinicie o computador para limpar as portas IPC do Windows.")

if __name__ == "__main__":
    debug()
