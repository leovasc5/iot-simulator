from connection.MongoConnection import MongoConnection
from connection.PostgresConnection import PostgresConnection
from service.simulador import simular, refinar_sensores, ativar_sensores
from service.visualizador import escolher_cliente, escolher_sensor, gerar_plot
from utils.functions import load_init, load_simulator, clear, load_menu, load_analise_menu, load_sensores_disponiveis, load_exit, load_not_found
import os
from time import sleep
from dotenv import load_dotenv
import utils.query as queries

load_dotenv()

def main():
    intervalo = float(os.getenv('INTERVALO_SIMULADOR'))
    ocorrencias_inseridas = 0
    ultimos_dados = None
    load_init(skip=os.getenv('SKIP_INTRO') in ('True', 'true', '1'))
    connMongo = MongoConnection()
    connPostgres = PostgresConnection()

    clientes = connPostgres.get_clientes()
    sensores_disponiveis = load_sensores_disponiveis()
    sensores = refinar_sensores(connPostgres.get_sensores_para_simular(), sensores_disponiveis)
    instancias = connPostgres.load_sensores(sensores_disponiveis)
    ativar_sensores(instancias)
    
    while True:
        clear()

        resp = load_menu()

        if resp == 1:
            while True:

                if not sensores:
                    load_not_found()
                    break

                novos_dados = simular(connMongo, sensores, ultimos_dados)

                if novos_dados:
                    ocorrencias_inseridas+=1
                    ultimos_dados = novos_dados
                
                clear()
                print(f"{ocorrencias_inseridas} dados inseridos\n")

                if intervalo:
                    sleep(intervalo)

        if resp == 2:
            while True:
                clear()
                resp_analise = load_analise_menu()

                if resp_analise == 1:
                    clear()
                    cliente = escolher_cliente(clientes)

                    if cliente:
                        query = queries.retornar_sensores_por_cliente(cliente["id"], sensores_disponiveis)
                        dados = connPostgres.execute_select_query(query)
                        
                        clear()
                        id_sensor_comodo_escolhido, sensor_nome = escolher_sensor(dados)
                        filtro = {f"sensores.{sensor_nome}.comodo_monitorado_sensor_id": id_sensor_comodo_escolhido}
                        dados = connMongo.get_data_list(filtro)
                        
                        valores = [dado['sensores'][sensor_nome]['valor'] for dado in dados]
                        tempos = [dado['timestamp'] for dado in dados]
                        gerar_plot(valores, tempos, sensor_nome)

                        exit()                    
                elif resp_analise == 2:
                    clear()
                    print('Exportando dados...')
                    sleep(1)
                elif resp_analise == 3:
                    break
                else:
                    print('Opção inválida')

        if resp == 3:
            connMongo.close_connection()
            connPostgres.close_connection()
            break

        clear()
        load_exit()

if __name__ == '__main__':
    main()