from src.connection.Connection import Connection
from src.service.simulator import simulate
from src.utils.functions import load_init, load_simulator, clear

def main():
    inserted_data = 0
    load_init()
    conn = Connection()
    load_simulator()
    
    while True:
        clear()
        inserted_data += simulate(conn)
        print(f'{inserted_data} registros inseridos')
    

if __name__ == '__main__':
    main()